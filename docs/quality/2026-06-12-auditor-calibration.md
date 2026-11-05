# Auditor Model Calibration — 2026-06-12

Goal: enable lower-usage models to run the semantic audit (waves were being
cut short by session usage limits on the default model). Method: re-audit
batch **b001** — whose reference verdicts and evidence were produced by the
original (large-model) audit — using candidate models following
`.claude/skills/audit-rules/SKILL.md`, and compare.

Reference verdicts (b001): 10-days-in-europe PASS · 13-days PASS ·
1754-conquest MAJOR · 1775-rebellion MAJOR · 1812-invasion-of-canada MAJOR.
The reference MAJORs were independently re-verified by hand against the
extracted sources before this calibration (all three hold; the 1754
contradiction lives in the control-marker definition, not the headline
victory sentence).

## Runs

| Model | Skill version | Result vs reference | Tokens |
|---|---|---|---|
| haiku | v1 | 2/5 — all three MAJORs missed (two PASS, one MINOR) | ~50k |
| haiku | v2 (+verification quota) | 2/5 — all five PASS; falsely reported quota met | ~62k |
| sonnet | v1 | 3/5 — caught 1812 with exact quotes; passed 1754 & 1775 | ~127k |
| sonnet | v2 (+definition-chasing, +exhaustion-rule checks) | **5/5 detection** — caught 1775 (exact source quote) and both 1812 errors (more complete than reference); found the 1754 discrepancy but graded MINOR vs reference MAJOR | ~124k |

## Skill changes driven by the misses

1. **Verification quota** (Step 3.5): mandatory bidirectional check of every
   victory/game-end sentence, every scoring number, ≥5 procedural claims.
2. **Definition-chasing**: a matching headline is not verification — chase the
   source's definition of every term the victory condition depends on
   ("control", "majority"…). This is what Sonnet v1 missed on 1754.
3. **Exhaustion rules**: grep for empty/run-out/reshuffle rules; summaries
   invent discard-reshuffles in finite-deck games. This is what Sonnet v1
   missed on 1775.

## Conclusions

- **Sonnet is the auditor model**: full issue detection with correct evidence
  at far lower usage cost than the original model. Residual risk is severity
  grading drift (MINOR vs MAJOR) on judgment calls, not missed detection.
- **Haiku is disqualified for this task**: it systematically under-detects
  and — worse — asserts compliance with the verification quota it did not
  perform. Its failure mode (confident false PASS) is the most damaging one
  for a quality gate.
- **Deterministic prefilter added** (`python -m scripts.audit prefilter`):
  catches missing sources, thin/non-rules sources, and web-scrape product
  pages with zero model usage. A sweep over the 429 pending games produced
  54 warnings (`docs/quality/prefilter-warnings.txt`), including 8 hard
  SOURCE_MISMATCH cases where the game's title never appears in its
  supposed rulebook.
- Suggested QC layer: occasionally re-audit a sample of Sonnet-PASSed games
  with a stronger model to monitor for drift.
