#!/usr/bin/env python3
"""Semantically verify a rules summary against its extracted source via the Claude API.

This ports the calibrated audit checklist (.claude/skills/audit-rules/SKILL.md,
see docs/quality/2026-06-12-auditor-calibration.md) into the batch pipeline so
accuracy is a *generation gate*, not a retroactive audit: a summary only
reaches `verified` status after it has been fact-checked against its source,
with up to N repair rounds in between.

Flow per game:  verify -> (findings? repair -> re-verify)* -> verdict
  PASS  -> status `verified`, frontmatter stamped
  MINOR -> status `verified`, frontmatter stamped `minor_issues`
  MAJOR -> status `flagged` with review_notes (needs re-summarization or a human)

Usage:
    python -m scripts.verify_summary rules/catan.md
    python -m scripts.verify_summary --batch --limit 10
    python -m scripts.verify_summary --batch --no-repair
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date

from dotenv import load_dotenv

from scripts.registry import get_games_by_status, update_game, update_status
from scripts.summarize import _find_extracted_file, parse_frontmatter

load_dotenv()

MODEL = "claude-sonnet-4-6"
MAX_REPAIR_ROUNDS = 2
MAX_SOURCE_CHARS = 600_000  # ~150k tokens; nearly all extracted texts fit whole
VERDICT_RANK = {"MAJOR": 0, "MINOR": 1, "PASS": 2}  # higher is better

VERIFIER_SYSTEM = """You are a meticulous fact-checker auditing an AI-generated board game \
rules summary against the game's extracted rulebook text. Roughly half of such summaries \
contain serious errors. Non-negotiable rules:

1. NEVER use outside knowledge of the game. Only the extracted rulebook text counts as \
truth. If you "know" the real rules but the source says otherwise, the source wins.
2. Every finding needs evidence: a short quote from the summary AND either a short \
contradicting quote from the source, or the statement "no support found".
3. Only report findings you are confident in. The extracted text has OCR artifacts and \
mangled tables — search mentally for alternate phrasings before declaring something \
unsupported. An uncertain finding is worse than no finding: drop it.
4. Correct numbers do NOT make a correct summary. The most damaging errors are in \
procedures and relationships. Never soften a verdict because the numbers check out.

You must verify, at minimum:
- EVERY sentence of the summary's victory / game-end / tiebreaker rules, in BOTH \
directions (summary claims missing from source AND source conditions missing from summary).
- The source's DEFINITION of every term the victory/scoring rules depend on ("control", \
"majority", "adjacent"...) — a matching headline sentence is not verification.
- Every number in the Scoring / Victory Conditions section.
- At least 5 procedural claims from Turn Structure / Actions.
- Exhaustion rules: if the summary states what happens when a deck/bag/supply runs out, \
the source must state it too — summaries frequently INVENT reshuffle rules.
- Invented mechanics: phases, actions, components, or subsystems with no source support.
- If the game is a variant/spinoff of a famous game, check that base-game rules did not \
replace the variant's actual ones.
- Each row of the Player Reference table (mappings get scrambled).

Verdicts:
- MAJOR: a contradicted rule, invented mechanic, wrong scoring/cost number, missing \
game-end condition or scoring source, scrambled reference table — anything that would \
mislead players at the table.
- MINOR: only omissions or unsupported flavor that would not change play or scoring.
- PASS: nothing beyond trivial wording drift. Do not force findings; simple games pass.

Respond with ONLY a JSON object, no markdown fences:
{"verdict": "PASS"|"MINOR"|"MAJOR",
 "reason": "<one line, empty for PASS>",
 "findings": [{"severity": "major"|"minor",
               "summary_quote": "...",
               "source_evidence": "<contradicting quote or 'no support found'>",
               "fix": "<what the summary should say, per the source>"}]}"""

REPAIRER_SYSTEM = """You are correcting an AI-generated board game rules summary using \
audit findings, with the extracted rulebook text as the only source of truth. Apply every \
fix the findings call for. Do not introduce any claim that is not supported by the source \
text. Keep the document's existing structure, frontmatter fields, section headings, style, \
and any HTML comment markers exactly as they are unless a finding requires a change. \
Output the COMPLETE corrected Markdown document (starting with the --- frontmatter line) \
and nothing else."""


def _truncate_source(text: str) -> str:
    if len(text) <= MAX_SOURCE_CHARS:
        return text
    return text[:MAX_SOURCE_CHARS] + "\n\n[SOURCE TRUNCATED FOR LENGTH]"


def _call_claude(system: str, prompt: str, max_tokens: int) -> str:
    import anthropic

    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set.")
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text


def parse_verifier_response(raw: str) -> dict:
    """Parse the verifier's JSON, tolerating stray fences/prose around it."""
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.DOTALL)
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object in verifier response: {raw[:200]!r}")
    result = json.loads(match.group(0))
    if result.get("verdict") not in ("PASS", "MINOR", "MAJOR"):
        raise ValueError(f"Invalid verdict: {result.get('verdict')!r}")
    result.setdefault("reason", "")
    result.setdefault("findings", [])
    return result


def verify_text(summary: str, source: str) -> dict:
    """Run one verification pass. Returns {verdict, reason, findings}."""
    prompt = (
        "Here is the extracted rulebook text (the only source of truth):\n\n"
        f"<rulebook>\n{_truncate_source(source)}\n</rulebook>\n\n"
        "Here is the summary to audit:\n\n"
        f"<summary>\n{summary}\n</summary>\n\n"
        "Audit the summary per your instructions and respond with the JSON verdict object."
    )
    return parse_verifier_response(_call_claude(VERIFIER_SYSTEM, prompt, max_tokens=4096))


def repair_text(summary: str, source: str, findings: list[dict]) -> str:
    """Apply verifier findings to produce a corrected summary."""
    prompt = (
        "Here is the extracted rulebook text (the only source of truth):\n\n"
        f"<rulebook>\n{_truncate_source(source)}\n</rulebook>\n\n"
        "Here is the current summary document:\n\n"
        f"<summary>\n{summary}\n</summary>\n\n"
        "Here are the audit findings to fix:\n\n"
        f"{json.dumps(findings, indent=2, ensure_ascii=False)}\n\n"
        "Output the complete corrected document."
    )
    result = _call_claude(REPAIRER_SYSTEM, prompt, max_tokens=16384).strip()
    if result.startswith("```"):
        result = re.sub(r"^```(?:markdown)?\s*|\s*```$", "", result, flags=re.DOTALL)
    if not result.startswith("---"):
        raise ValueError("Repaired document does not start with frontmatter")
    return result


def _stamp_after_verdict(rules_path: str, verdict: str) -> None:
    """Stamp verification frontmatter + visible block to match the verdict."""
    from scripts.stamp_verification import stamp_file

    slug = os.path.splitext(os.path.basename(rules_path))[0]
    synthetic = {slug: {"verdict": verdict, "reason": "", "batch": "pipeline"}}
    stamp_file(rules_path, synthetic)


def verify_game(
    game: dict,
    registry_path: str,
    extracted_dir: str = "extracted",
    rules_dir: str = "rules",
    repair: bool = True,
    max_repair_rounds: int = MAX_REPAIR_ROUNDS,
    restore_status: str | None = None,
) -> bool:
    """Verify (and optionally repair) one game's summary. Returns True on success."""
    name = game["name"]
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    rules_path = os.path.join(rules_dir, f"{slug}.md")
    extracted_path = _find_extracted_file(slug, extracted_dir)

    if not os.path.exists(rules_path):
        print(f"  Skipping {name}: no rules file at {rules_path}")
        if restore_status:
            update_status(registry_path, name, restore_status)
        return False
    if not extracted_path:
        print(f"  {name}: no extracted source — unverifiable, flagging")
        update_game(
            registry_path, name,
            status="flagged",
            review_notes="Unverifiable: no extracted source text; re-source the PDF",
        )
        return False

    original_summary = open(rules_path).read()
    source = open(extracted_path).read()

    try:
        summary = original_summary
        result = verify_text(summary, source)
        # Track the best-scoring version across rounds. The verifier has
        # run-to-run severity drift, and a repair round can introduce a new
        # nitpick that drops the verdict again — so we keep the best content
        # we ever achieved rather than whatever the last round produced, and
        # we never write a degraded version (or any repair that failed to
        # beat the original) to disk.
        best_verdict, best_reason, best_summary = (
            result["verdict"], result["reason"], summary)
        rounds = 0
        while result["verdict"] != "PASS" and repair and rounds < max_repair_rounds:
            rounds += 1
            print(f"  {name}: {result['verdict']} — repair round {rounds} "
                  f"({len(result['findings'])} findings)")
            summary = repair_text(summary, source, result["findings"])
            result = verify_text(summary, source)
            if VERDICT_RANK[result["verdict"]] > VERDICT_RANK[best_verdict]:
                best_verdict, best_reason, best_summary = (
                    result["verdict"], result["reason"], summary)
            if result["verdict"] == "PASS":
                break
    except Exception as e:
        print(f"  Error verifying {name}: {e}")
        if restore_status:
            update_status(registry_path, name, restore_status)
        return False

    verdict, reason = best_verdict, best_reason
    if best_summary != original_summary:
        with open(rules_path, "w") as f:
            f.write(best_summary)
    _stamp_after_verdict(rules_path, verdict)

    if verdict == "MAJOR":
        print(f"  {name}: MAJOR after {rounds} repair round(s) — flagged")
        update_game(
            registry_path, name,
            status="flagged",
            review_notes=f"Semantic verification MAJOR: {reason}"[:500],
        )
        return False

    update_game(
        registry_path, name,
        status="verified",
        verified_date=date.today().isoformat(),
    )
    print(f"  {name}: {verdict} -> verified")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Semantically verify rules summaries against extracted sources"
    )
    parser.add_argument("rules_file", nargs="?", help="Path to a rules/<slug>.md file")
    parser.add_argument("--batch", action="store_true",
                        help="Process all games with status 'validated'")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--registry", default="games.yaml")
    parser.add_argument("--no-repair", action="store_true",
                        help="Verify only; do not attempt repairs")
    args = parser.parse_args()

    if args.batch:
        games = get_games_by_status(args.registry, "validated", limit=args.limit)
        if not games:
            print("No games with status 'validated' found.")
            sys.exit(0)
        print(f"Verifying {len(games)} game(s)...")
        ok = sum(
            verify_game(g, args.registry, repair=not args.no_repair) for g in games
        )
        print(f"\nDone: {ok}/{len(games)} verified.")
    else:
        if not args.rules_file:
            parser.error("rules_file is required unless --batch is used")
        slug = os.path.splitext(os.path.basename(args.rules_file))[0]
        extracted_path = _find_extracted_file(slug, "extracted")
        if not extracted_path:
            print(f"Error: no extracted source for {slug}")
            sys.exit(1)
        summary = open(args.rules_file).read()
        source = open(extracted_path).read()
        result = verify_text(summary, source)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(0 if result["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
