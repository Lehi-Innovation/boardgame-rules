#!/usr/bin/env python3
"""Re-verify and repair the flagged MAJOR backlog through the verify+repair loop.

The retroactive semantic audit left games with MAJOR verdicts in `flagged`
status. This driver re-runs each through `scripts.verify_summary.verify_game`
(generate-free: it verifies the *current* summary against its extracted source
and repairs fixable findings), which moves PASS/MINOR games to `verified` and
keeps genuinely-broken ones `flagged`. verify_game itself stamps the page and
records the verdict into the audit results tracker, so this driver only has to:
select candidates, drive the loop, log progress, and checkpoint to git.

It is **resumable**: a game that becomes `verified` drops out of the candidate
set, so re-running picks up wherever a previous run (or a reclaimed container)
left off. Because the run is long and the container is ephemeral, it commits
and pushes every `--checkpoint-every` games so progress survives.

Usage:
    python -m scripts.reverify_backlog --dry-run
    python -m scripts.reverify_backlog --limit 5 --no-push
    python -m scripts.reverify_backlog --checkpoint-every 10 --push \
        --branch claude/youthful-cray-6ck2mx
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

import yaml

from scripts.registry import load_registry
from scripts.summarize import parse_frontmatter
from scripts.verify_summary import RESULTS_PATH, verify_game

RULES_DIR = "rules"
EXTRACTED_DIR = "extracted"
STATE_TO_VERDICT = {
    "verified": "PASS",
    "minor_issues": "MINOR",
    "inaccurate": "MAJOR",
    "unverifiable": "MAJOR",
    "unverified": "MAJOR",
}


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def has_source(slug: str, extracted_dir: str = EXTRACTED_DIR) -> bool:
    return any(
        os.path.exists(os.path.join(extracted_dir, f"{slug}{s}"))
        for s in ("-rules.txt", "_rules.txt", ".txt")
    )


def select_candidates(
    games: list[dict],
    results: dict,
    rules_dir: str = RULES_DIR,
    extracted_dir: str = EXTRACTED_DIR,
) -> list[tuple[str, str]]:
    """Flagged games with a MAJOR verdict, a rules file, and an extracted source.

    Sorted by slug for deterministic, resumable ordering.
    """
    out = []
    for g in games:
        if g.get("status") != "flagged":
            continue
        slug = slugify(g["name"])
        if results.get(slug, {}).get("verdict") != "MAJOR":
            continue
        if not os.path.exists(os.path.join(rules_dir, f"{slug}.md")):
            continue
        if not has_source(slug, extracted_dir):
            continue
        out.append((g["name"], slug))
    out.sort(key=lambda x: x[1])
    return out


def read_state(slug: str, rules_dir: str = RULES_DIR) -> str:
    fm = parse_frontmatter(open(os.path.join(rules_dir, f"{slug}.md")).read())
    return fm.get("verification", "")


def git_checkpoint(processed: int, branch: str, push: bool, log) -> None:
    subprocess.run(["git", "add", "-A"], check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode == 0:
        return  # nothing to commit
    msg = (
        f"data: re-verify backlog checkpoint ({processed} games processed)\n\n"
        "https://claude.ai/code/session_01XA4KLQ5NLNQBWtoYL6PWgi"
    )
    subprocess.run(["git", "commit", "-q", "-m", msg], check=True)
    if not push:
        return
    for delay in (2, 4, 8, 16, 0):
        if subprocess.run(["git", "push", "origin", branch]).returncode == 0:
            log(f"  [checkpoint] committed + pushed at {processed} games")
            return
        if delay:
            time.sleep(delay)
    log(f"  [checkpoint] committed but PUSH FAILED at {processed} games")


def main():
    parser = argparse.ArgumentParser(description="Re-verify+repair the flagged MAJOR backlog")
    parser.add_argument("--registry", default="games.yaml")
    parser.add_argument("--limit", type=int, default=0, help="Max games (0 = all)")
    parser.add_argument("--checkpoint-every", type=int, default=10,
                        help="Commit (+push) every N games (0 = only at end)")
    parser.add_argument("--push", dest="push", action="store_true", default=True)
    parser.add_argument("--no-push", dest="push", action="store_false")
    parser.add_argument("--no-repair", action="store_true", help="Verify only, no repairs")
    parser.add_argument("--branch", default="claude/youthful-cray-6ck2mx")
    parser.add_argument("--log", default="", help="Append progress to this file too")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    log_fh = open(args.log, "a") if args.log else None

    def log(msg: str) -> None:
        print(msg, flush=True)
        if log_fh:
            log_fh.write(msg + "\n")
            log_fh.flush()

    results = yaml.safe_load(open(RESULTS_PATH)) if os.path.exists(RESULTS_PATH) else {}
    candidates = select_candidates(load_registry(args.registry), results or {})

    if args.dry_run:
        log(f"{len(candidates)} candidates:")
        for name, slug in candidates:
            log(f"  {slug}")
        return

    if args.limit:
        candidates = candidates[: args.limit]

    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    log(f"=== reverify backlog: {len(candidates)} games, repair={not args.no_repair}, "
        f"checkpoint-every={args.checkpoint_every}, push={args.push} @ {started} ===")

    counts: dict[str, int] = {}
    errors = 0
    for i, (name, slug) in enumerate(candidates, 1):
        log(f"[{i}/{len(candidates)}] {slug}")
        try:
            verify_game(
                {"name": name},
                args.registry,
                repair=not args.no_repair,
                restore_status="flagged",
            )
            verdict = STATE_TO_VERDICT.get(read_state(slug), "MAJOR")
            counts[verdict] = counts.get(verdict, 0) + 1
            log(f"    -> {verdict}")
        except Exception as e:  # one bad game must not kill the run
            errors += 1
            log(f"    -> ERROR: {e}")
        if args.checkpoint_every and i % args.checkpoint_every == 0:
            git_checkpoint(i, args.branch, args.push, log)

    git_checkpoint(len(candidates), args.branch, args.push, log)
    log(f"=== done: processed {len(candidates)}, verdicts {counts}, errors {errors} ===")
    if log_fh:
        log_fh.close()


if __name__ == "__main__":
    main()
