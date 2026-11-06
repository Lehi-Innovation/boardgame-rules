#!/usr/bin/env python3
"""Stamp verification status into rules files from semantic-audit verdicts.

Joins three sources of truth per game:
  - docs/quality/semantic-audit-results.yaml  (PASS / MINOR / MAJOR verdicts)
  - presence of extracted/<slug>-rules.txt    (is the summary checkable at all?)
  - rules/<slug>.md frontmatter               (existing verification fields)

and writes two things into each rules file, idempotently:
  1. frontmatter fields:  verification, verification_date
  2. a visible status block (badge + rulebook-text link + report-an-error link)
     between VERIFICATION_BEGIN/END markers, placed after the H1 heading.

Verification states:
  verified     audit verdict PASS
  minor_issues audit verdict MINOR (small omissions; would not change play)
  inaccurate   audit verdict MAJOR (known table-misleading errors)
  unverified   no audit yet, but source text exists to check against
  unverifiable no extracted source text exists; summary cannot be checked

Usage:
    python -m scripts.stamp_verification                  # stamp all rules files
    python -m scripts.stamp_verification rules/catan.md   # stamp one file
    python -m scripts.stamp_verification --update-registry  # also promote
        audit-PASS games from 'validated' to 'verified' in games.yaml
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from urllib.parse import quote, urlsplit

import yaml

from scripts.registry import locked_registry
from scripts.site import extracted_text_url, report_issue_url, site_base_url

RESULTS_PATH = "docs/quality/semantic-audit-results.yaml"
RULES_DIR = "rules"
EXTRACTED_DIR = "extracted"

VERIFICATION_BEGIN = "<!-- verification:begin -->"
VERIFICATION_END = "<!-- verification:end -->"

VERDICT_TO_STATE = {
    "PASS": "verified",
    "MINOR": "minor_issues",
    "MAJOR": "inaccurate",
}

BADGES = {
    "verified": "✅ **Verified** — this summary was fact-checked against the rulebook text and no significant issues were found.",
    "minor_issues": "✅ **Verified (minor gaps)** — fact-checked against the rulebook text; only small omissions were found, nothing that changes how the game is played or scored.",
    "inaccurate": "❗ **Known errors** — an audit found inaccuracies in this summary that could mislead players{reason}. Until corrections pass a new audit, prefer the full rulebook text linked below.",
    "unverified": "⚠️ **Unverified** — this AI-generated summary has not yet been fact-checked against the rulebook. Double-check critical rules against the full rulebook text linked below.",
    "unverifiable": "⚠️ **Unverifiable** — no source rulebook text is available to check this AI-generated summary against. Treat all details with caution.",
}


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def load_audit_results(path: str = RESULTS_PATH) -> dict[str, dict]:
    """Return {slug: {verdict, reason, batch}} from the audit results tracker."""
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def has_extracted_source(slug: str, extracted_dir: str = EXTRACTED_DIR) -> bool:
    """Require readable text, rather than accepting an empty extraction file."""
    for pattern in (f"{slug}-rules.txt", f"{slug}_rules.txt", f"{slug}.txt"):
        path = os.path.join(extracted_dir, pattern)
        if os.path.isfile(path):
            with open(path, errors="replace") as source:
                if source.read().strip():
                    return True
    return False


def compute_state(slug: str, audit_results: dict[str, dict], extracted_dir: str = EXTRACTED_DIR) -> tuple[str, str]:
    """Return (state, reason) for a game slug."""
    if not has_extracted_source(slug, extracted_dir):
        return "unverifiable", ""
    entry = audit_results.get(slug)
    if entry and entry.get("verdict") in VERDICT_TO_STATE:
        return VERDICT_TO_STATE[entry["verdict"]], entry.get("reason") or ""
    return "unverified", ""


def build_block(slug: str, title: str, state: str, reason: str, base_url: str | None = None,
                source_url: str = "", source_language: str = "English", source_type: str = "rulebook_pdf") -> str:
    """Build the visible status block for a rules page."""
    base = base_url or site_base_url()
    badge = BADGES[state]
    if state == "inaccurate":
        badge = badge.format(reason=f": {reason.rstrip().rstrip('.')}" if reason else "")
    if source_type != "rulebook_pdf":
        badge = badge.replace("against the rulebook.", "against its rules source.")
        badge = badge.replace("the full rulebook text linked below", "the linked rules source")

    links = []
    if state != "unverifiable":
        text_label = {
            "third_party_rules_transcription": "Rules source text",
            "third_party_rules_translation": "Translated rules text",
            "learn_to_play": "Learn-to-play text",
            "research_paper": "Rules reference text",
            "author_rules_html": "Author's rules text",
            "author_rules_text": "Author's rules text",
            "rules_reference_html": "Rules reference text",
            "rules_reference_text": "Rules reference text",
            "rules_reference_pdf": "Rules reference text",
            "rules_reference_images": "Rules reference text",
            "rulebook_images": "Rulebook text",
            "rulebook_archive": "Rulebook text",
        }.get(source_type, "Full rulebook text")
        links.append(f"📄 [{text_label}]({extracted_text_url(slug, base)})")
    parsed = urlsplit(source_url)
    if parsed.scheme in {"http", "https"} and parsed.netloc:
        label = {
            "third_party_rules_transcription": "Rules transcription",
            "research_paper": "Research paper",
            "author_rules_html": "Author's rules",
            "author_rules_text": "Author's rules",
            "rules_reference_html": "Rules reference",
            "rules_reference_text": "Rules reference",
            "rules_reference_pdf": "Rules reference PDF",
            "rules_reference_images": "Rules reference images",
            "rulebook_images": "Rulebook images",
            "rulebook_archive": "Rulebook archive",
        }.get(source_type, "Source PDF")
        safe_url = quote(source_url, safe=":/?&=%#@+;,._~-")
        links.append(f"🌐 [{label} ({source_language})]({safe_url})")
    links.append(f"🚩 [Report a rules error]({report_issue_url(title, slug)})")

    return (
        f"{VERIFICATION_BEGIN}\n"
        f"> {badge}\n"
        f">\n"
        f"> {' · '.join(links)}\n"
        f"{VERIFICATION_END}"
    )


def _stamp_frontmatter(fm_text: str, state: str, stamp_date: str) -> tuple[str, bool]:
    """Set verification fields in raw frontmatter text, preserving everything else.

    Returns (new_fm_text, state_changed). The date is only refreshed when the
    state changes, so re-running the stamper is a no-op for unchanged games.
    """
    old_state = None
    old_date_line = None
    kept = []
    for line in fm_text.split("\n"):
        if line.startswith("verification:"):
            old_state = line.split(":", 1)[1].strip().strip("\"'")
        elif line.startswith("verification_date:"):
            old_date_line = line
        else:
            kept.append(line)

    changed = old_state != state
    kept.append(f'verification: "{state}"')
    if changed or old_date_line is None:
        kept.append(f'verification_date: "{stamp_date}"')
    else:
        kept.append(old_date_line)
    return "\n".join(kept), changed


def stamp_file(
    path: str,
    audit_results: dict[str, dict],
    base_url: str | None = None,
    extracted_dir: str = EXTRACTED_DIR,
    stamp_date: str | None = None,
) -> str | None:
    """Stamp one rules file. Returns the state, or None if the file was skipped."""
    slug = os.path.splitext(os.path.basename(path))[0]
    content = open(path).read()

    fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not fm_match:
        return None
    fm_text = fm_match.group(1)
    body = content[fm_match.end():]

    try:
        fm = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        return None
    title = str(fm.get("title", slug))

    state, reason = compute_state(slug, audit_results, extracted_dir)
    new_fm, _ = _stamp_frontmatter(fm_text, state, stamp_date or date.today().isoformat())
    block = build_block(slug, title, state, reason, base_url,
                        source_url=str(fm.get("source_url") or ""),
                        source_language=str(fm.get("source_language") or "English"),
                        source_type=str(fm.get("source_type") or "rulebook_pdf"))

    # Replace an existing managed block, else insert after the H1 (or at top).
    block_re = re.compile(
        re.escape(VERIFICATION_BEGIN) + r".*?" + re.escape(VERIFICATION_END),
        re.DOTALL,
    )
    if block_re.search(body):
        body = block_re.sub(lambda _: block, body, count=1)
    else:
        h1 = re.search(r"^# .+$", body, re.MULTILINE)
        if h1:
            insert_at = h1.end()
            body = body[:insert_at] + "\n\n" + block + body[insert_at:]
        else:
            body = block + "\n\n" + body

    new_content = f"---\n{new_fm}\n---\n{body}"
    if new_content != content:
        with open(path, "w") as f:
            f.write(new_content)
    return state


def promote_registry(registry_path: str, audit_results: dict[str, dict]) -> int:
    """Promote audit-PASS games from 'validated' to 'verified' in the registry."""
    promoted = 0
    with locked_registry(registry_path) as (games, save):
        for game in games:
            slug = slugify(game["name"])
            entry = audit_results.get(slug)
            if not entry or entry.get("verdict") != "PASS":
                continue
            if game.get("status") == "validated":
                game["status"] = "verified"
                promoted += 1
        if promoted:
            save(games)
    return promoted


def main():
    parser = argparse.ArgumentParser(description="Stamp verification status into rules files")
    parser.add_argument("files", nargs="*", help="Specific rules files (default: all of rules/)")
    parser.add_argument("--rules-dir", default=RULES_DIR)
    parser.add_argument("--extracted-dir", default=EXTRACTED_DIR)
    parser.add_argument("--results", default=RESULTS_PATH)
    parser.add_argument("--registry", default="games.yaml")
    parser.add_argument(
        "--update-registry",
        action="store_true",
        help="Promote audit-PASS games from 'validated' to 'verified' in games.yaml",
    )
    args = parser.parse_args()

    audit_results = load_audit_results(args.results)

    if args.files:
        paths = args.files
    else:
        paths = sorted(
            os.path.join(args.rules_dir, f)
            for f in os.listdir(args.rules_dir)
            if f.endswith(".md")
        )

    base_url = site_base_url()
    counts: dict[str, int] = {}
    skipped = 0
    for path in paths:
        state = stamp_file(path, audit_results, base_url=base_url, extracted_dir=args.extracted_dir)
        if state is None:
            print(f"  skipped (no/bad frontmatter): {path}", file=sys.stderr)
            skipped += 1
        else:
            counts[state] = counts.get(state, 0) + 1

    print(f"Stamped {sum(counts.values())} files ({skipped} skipped): {counts}")

    if args.update_registry:
        promoted = promote_registry(args.registry, audit_results)
        print(f"Registry: promoted {promoted} audit-PASS games validated -> verified")


if __name__ == "__main__":
    main()
