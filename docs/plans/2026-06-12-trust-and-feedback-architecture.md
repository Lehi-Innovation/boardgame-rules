# Trust & Feedback Architecture — 2026-06-12

## Problem

The project's objective is mid-game rules Q&A via any LLM, with a feedback
loop so summaries improve. The system as of 2026-06-12 did not serve either:

1. **Delivery**: the only end-user channel was a pasted prompt that fetched
   summary pages by guessed slug. The good tiered lookup (summary → extracted
   text → BGG → labeled intuition) lived in Claude Code skills no end user runs.
2. **Accuracy**: summaries were generated in a single pass and gated only
   structurally. The semantic audit measured **55% MAJOR** (153/280 audited,
   plus 58 MINOR) — and known-MAJOR games were still published with no warning.
   ~680 summaries have no extracted source committed and are unverifiable.
3. **Feedback**: no end-user channel existed, and the `rules-lookup` skill
   wrote Tier-3 (forum) and Tier-4 (intuition) answers into canonical rules
   prose marked only with invisible HTML comments — a hallucination-injection
   path.

## Decisions

**Invert the quality model: verify before publishing, not audit after.**

- New pipeline stage `verify` (`scripts/verify_summary.py`): the calibrated
  audit checklist (see `2026-06-12-auditor-calibration.md`) ported to an API
  verifier + repair loop. `validated` (structural) → `verified` (semantic).
  PASS/MINOR → `verified`; MAJOR after repairs → `flagged`.
- Trust is stamped into every page (`scripts/stamp_verification.py`):
  `verification` frontmatter + a visible banner (verified / minor_issues /
  inaccurate / unverified / unverifiable) with links to the full rulebook
  text and the report-an-error form. Known-bad pages now say so and point at
  the source instead.

**Publish the lossless layer.** `extracted/` is now served by the site and
linked from every page and from `games.json`; mid-game questions are about
edge cases that summarization compresses away, so the answering LLM needs
tier-2 fallback. `games.json` (machine-readable manifest with slugs, URLs,
verification states) replaces slug-guessing.

**Close the loop with users, safely.**

- `rule-error` issue form linked from every page; `rule-error-triage`
  workflow dispatches Claude with `.claude/skills/triage-rule-error/SKILL.md`
  to verify reports against the extracted text and fix-via-PR when confirmed.
  The extracted text outranks the reporter, training data, and BGG.
- `rules-lookup` tier rules hardened: canonical sections accept only
  source-verified claims; forum rulings go to a labeled `FAQ & Rulings`
  section; intuition is never written anywhere (opens a `needs-research`
  issue instead).

**Meet users where they are.** `mcp_server/` exposes `list_games`,
`get_rules`, `search_rulebook`, `report_rule_error` over MCP so Claude
mobile/desktop (voice mode at the table) gets tiered lookup natively.

## Status at time of writing

- All 1,649 rules pages stamped: 69 verified, 58 minor_issues,
  153 + 4 (calibration) inaccurate, ~690 unverified, ~679 unverifiable.
- 69 audit-PASS games promoted `validated → verified` in the registry;
  the 4 calibration MAJORs recorded and flagged.

## Remaining operational work (not code)

1. Re-summarize the 157 MAJOR games through summarize → verify, prioritized
   by BGG popularity (needs API budget).
2. Finish the audit waves over the pre-existing `validated` backlog
   (98 batches remain), or run them through the `verify` stage instead.
3. Re-source PDFs for the ~679 unverifiable summaries, or accept the caution
   banner permanently.
4. Add the `ANTHROPIC_API_KEY` repo secret to activate the triage workflow.
5. Optionally host the MCP server remotely (currently stdio/local).
