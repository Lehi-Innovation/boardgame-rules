#!/usr/bin/env python3
"""Semantic-audit toolkit for rules summaries.

Manages the audit of rules/<slug>.md files against extracted/<slug>-rules.txt
sources, tracked in docs/quality/semantic-audit-manifest.json (batch queue)
and docs/quality/semantic-audit-results.yaml (verdicts).

Usage:
    python -m scripts.audit status
    python -m scripts.audit next [--batches N]
    python -m scripts.audit prefilter <slug> [<slug> ...]
    python -m scripts.audit record <results-file> <batch-id> [<batch-id> ...]

`record` reads RESULT|slug|VERDICT|reason lines, updates the results tracker,
flags MAJOR games in games.yaml with review_notes, and marks batches done.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

import yaml

from scripts.registry import load_registry, locked_registry

MANIFEST_PATH = "docs/quality/semantic-audit-manifest.json"
RESULTS_PATH = "docs/quality/semantic-audit-results.yaml"
EXTRACTED_DIR = "extracted"

TITLE_STOPWORDS = {
    "the", "of", "and", "game", "board", "edition", "deluxe", "second",
    "third", "first", "new", "with", "for", "card",
}
RULES_KEYWORDS = [
    "player", "turn", "win", "rule", "setup", "card", "dice", "die",
    "score", "round", "move", "board",
]
# Navigation chrome typical of scraped web pages (not rulebooks)
WEB_MARKERS = [
    "buy now", "our games", "add to cart", "newsletter", "cookie",
    "press & content", "retailer", "distributor", "shop\n", "menu\n",
]


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def load_manifest() -> dict:
    with open(MANIFEST_PATH) as f:
        return json.load(f)


def save_manifest(manifest: dict) -> None:
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=1)


def load_tracker() -> dict:
    try:
        with open(RESULTS_PATH) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def cmd_status(_args) -> None:
    manifest = load_manifest()
    batches = manifest["batches"]
    done = sum(1 for b in batches.values() if b["status"] == "done")
    tracker = load_tracker()
    counts: dict[str, int] = {}
    for v in tracker.values():
        counts[v["verdict"]] = counts.get(v["verdict"], 0) + 1
    print(f"batches: {done}/{len(batches)} done")
    print(f"games audited: {len(tracker)}")
    print(f"verdicts: {counts}")


def cmd_next(args) -> None:
    manifest = load_manifest()
    shown = 0
    for bid, batch in manifest["batches"].items():
        if batch["status"] != "pending":
            continue
        print(f"{bid} {' '.join(batch['slugs'])}")
        shown += 1
        if shown >= args.batches:
            break
    if shown == 0:
        print("NO_PENDING_BATCHES")


def prefilter_slug(slug: str, name_by_slug: dict[str, str]) -> list[str]:
    """Deterministic source checks. Returns a list of warning strings."""
    warnings = []
    path = os.path.join(EXTRACTED_DIR, f"{slug}-rules.txt")
    if not os.path.exists(path):
        return ["MISSING_EXTRACTED: no source text to audit against"]

    size = os.path.getsize(path)
    if size < 2000:
        warnings.append(f"SOURCE_THIN: extracted text only {size} bytes")

    with open(path, errors="replace") as f:
        text = f.read()
    head = text[:3000].lower()
    full_lower = text.lower()

    # Title-token overlap: does the source actually mention this game?
    name = name_by_slug.get(slug, slug.replace("-", " "))
    tokens = [
        t for t in re.findall(r"[a-z0-9]+", name.lower())
        if len(t) >= 4 and t not in TITLE_STOPWORDS
    ]
    if tokens:
        hits_head = sum(1 for t in tokens if t in head)
        hits_full = sum(1 for t in tokens if t in full_lower)
        if hits_full == 0:
            warnings.append(
                f"SOURCE_MISMATCH: no title tokens {tokens} found anywhere in source"
            )
        elif hits_head == 0:
            warnings.append(
                f"SOURCE_SUSPECT: title tokens {tokens} absent from first 3000 chars"
            )

    # Rules-ness: does this read like a rulebook at all?
    distinct = sum(1 for kw in RULES_KEYWORDS if kw in full_lower)
    if distinct < 4:
        warnings.append(
            f"NOT_RULES: only {distinct}/12 rules keywords present "
            "(may be a product page or article)"
        )

    # Web-scrape detection: nav chrome + low "player" density
    markers = sum(1 for m in WEB_MARKERS if m in full_lower)
    word_count = max(len(full_lower.split()), 1)
    player_density = 1000 * full_lower.count("player") / word_count
    if markers >= 5 or (markers >= 3 and player_density < 10):
        warnings.append(
            f"WEB_SCRAPE: {markers} nav markers, 'player' density "
            f"{player_density:.0f}/1000 words (likely a product page, not rules)"
        )

    return warnings


def cmd_prefilter(args) -> None:
    games = load_registry("games.yaml")
    name_by_slug = {slugify(g["name"]): g["name"] for g in games}
    any_warn = False
    for slug in args.slugs:
        warnings = prefilter_slug(slug, name_by_slug)
        if warnings:
            any_warn = True
            for w in warnings:
                print(f"{slug}: WARN {w}")
        else:
            print(f"{slug}: OK")
    sys.exit(1 if any_warn else 0)


def cmd_record(args) -> None:
    lines = [
        l.strip() for l in open(args.results_file)
        if l.strip().startswith("RESULT|")
    ]
    parsed = []
    for l in lines:
        _, slug, verdict, reason = l.split("|", 3)
        verdict = verdict.strip()
        if verdict not in ("PASS", "MINOR", "MAJOR"):
            print(f"skipping malformed verdict line: {l}")
            continue
        parsed.append(
            {"slug": slug.strip(), "verdict": verdict, "reason": reason.strip()}
        )

    manifest = load_manifest()
    slug_batch = {
        s: bid for bid, b in manifest["batches"].items() for s in b["slugs"]
    }

    tracker = load_tracker()
    for p in parsed:
        tracker[p["slug"]] = {
            "verdict": p["verdict"],
            "batch": slug_batch.get(p["slug"], "?"),
            "reason": p["reason"] if p["reason"] != "-" else "",
        }
    with open(RESULTS_PATH, "w") as f:
        yaml.dump(
            tracker, f, default_flow_style=False, sort_keys=True,
            allow_unicode=True, width=120,
        )

    majors = {p["slug"]: p for p in parsed if p["verdict"] == "MAJOR"}
    flagged = []
    if majors:
        with locked_registry("games.yaml") as (games, save):
            for g in games:
                s = slugify(g["name"])
                if s in majors:
                    g["status"] = "flagged"
                    bid = slug_batch.get(s, "?")
                    g["review_notes"] = (
                        f"Semantic audit ({bid}): {majors[s]['reason']} "
                        f"-- see docs/quality/audit-findings/{bid}.md"
                    )
                    flagged.append(g["name"])
            save(games)

    for bid in args.batch_ids:
        manifest["batches"][bid]["status"] = "done"
    save_manifest(manifest)

    done = sum(1 for b in manifest["batches"].values() if b["status"] == "done")
    counts: dict[str, int] = {}
    for v in tracker.values():
        counts[v["verdict"]] = counts.get(v["verdict"], 0) + 1
    print(f"recorded {len(parsed)} verdicts; flagged {len(flagged)} games: {flagged}")
    print(f"progress: {done}/{len(manifest['batches'])} batches; cumulative: {counts}")


def main():
    parser = argparse.ArgumentParser(description="Semantic-audit toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show batch progress and verdict counts")

    p_next = sub.add_parser("next", help="Print next pending batches")
    p_next.add_argument("--batches", type=int, default=6)

    p_pre = sub.add_parser("prefilter", help="Deterministic source checks")
    p_pre.add_argument("slugs", nargs="+")

    p_rec = sub.add_parser("record", help="Record RESULT lines from a wave")
    p_rec.add_argument("results_file")
    p_rec.add_argument("batch_ids", nargs="+")

    args = parser.parse_args()
    {
        "status": cmd_status,
        "next": cmd_next,
        "prefilter": cmd_prefilter,
        "record": cmd_record,
    }[args.command](args)


if __name__ == "__main__":
    main()
