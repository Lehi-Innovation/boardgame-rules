# Independent Re-Audit — 2026-07-03

## The finding: a repairer cannot grade its own work

The pipeline's accuracy gate (`scripts/verify_summary.py`) and the manual
subagent repair passes share one structural blind spot: **the same agent that
finds an error also fixes it, then declares the result verified.** There is no
independent check. This over-claims, and we measured by how much.

### Method

1. **Sample.** Drew a random 15-game sample from ~103 summaries that a repair
   pass had marked `verified`, and had *fresh* auditor agents (no knowledge of
   the repair) re-check each against its extracted rulebook — audit only, no
   editing. A MAJOR found here is a genuine residual error.
2. **Full pass.** Ran an **audit → repair-if-MAJOR → re-verify** pipeline over
   all ~92 repaired games, with the audit, the repair, and the re-verify each
   done by a *separate* agent, so a repair that didn't actually work is caught
   by an independent re-verify instead of being stamped `verified`.

### Result

| Stage | Sample (n=15) | Full pass (n=92) |
|---|---:|---:|
| Residual MAJOR after one repair pass | ~27% (4/15) | — |
| Still MAJOR after a *second*, independent repair | — | **~35% (32/92)** |

About **a third of "verified" summaries still contained a table-misleading
error.** The independent re-verify re-flagged them with the specific finding in
`review_notes`; only games that pass the independent check keep `verified`.

## Why ~1/3 resist automated fixing

The stubborn cases cluster into three kinds, none of which another automated
pass reliably fixes:

- **OCR-degraded sources** — the extracted text lost the numbers/tables the
  claim depends on, so the summary can't be verified from it (the summary may
  even be right; it's just unsupported). E.g. cacao payouts, captain-sonar
  charge costs, cosmic-encounter card values.
- **Omitted subsystems** — a whole phase or economy is missing from a complex
  game, and the repairer patches the cited finding without adding the missing
  system. E.g. civilization's culture-track spend, caverna's grain rounding,
  claustrophobia's combat resolution, d-day-at-omaha-beach's event phase.
- **Invented mechanics** — the summary asserts a rule the source never states;
  the repairer sometimes trims the cited instance but leaves the pattern. E.g.
  conan's time-limit victory, dog's home-pass restriction, descent's
  large-monster movement exception.

These need a better source PDF (re-extraction) or human attention, not a third
automated pass — the automated loop plateaus here.

## What this changes

- **`verified` requires an *independent* pass.** A single audit-or-repair
  agent's own verdict is necessary but not sufficient. The three-stage
  audit → repair → **independent** re-verify is the standard for earning the
  badge; treat any self-graded `verified` as provisional.
- **The re-audit is a standing second gate**, not a one-off. It can be re-run
  over any set of repaired/`verified` games to catch drift and over-claims.
- **Flagged is honest, not a failure.** A game that can't be verified from its
  source stays `flagged` with the specific reason, pointing users at the full
  rulebook text via the on-page banner — which is strictly better than a
  confident-but-wrong `verified` stamp.

## Reproducing

The independent re-audit was run as a multi-agent workflow (audit → repair →
re-verify, one separate agent per stage, results consolidated into
`docs/quality/semantic-audit-results.yaml` and stamped via
`scripts/stamp_verification.py`). See
`docs/quality/2026-06-12-auditor-calibration.md` for the auditor checklist the
agents follow, and `.claude/skills/audit-rules/SKILL.md` for the audit
procedure. The measured residual rates above should be re-checked whenever the
summarization or repair prompts change materially.
