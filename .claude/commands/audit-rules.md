---
allowed-tools: Bash, Read, Agent, TaskOutput
description: Run semantic-audit waves over validated rules summaries using low-cost subagents. Usage: /audit-rules [--waves N] [--model sonnet|haiku]
---

# Audit Rules Orchestrator

Run waves of the semantic audit until `--waves N` waves are done (default: keep
going until stopped or no pending batches remain). Default subagent model:
`sonnet`. **Do not use `haiku` for auditing**: in calibration against a batch
with known errors (2026-06-12, see `docs/quality/2026-06-12-auditor-calibration.md`)
haiku produced false PASSes on all three known-MAJOR games — twice — while
claiming the verification quota was met. Sonnet with the current skill found
every known issue with correct evidence.

Arguments: $ARGUMENTS

## Per-wave loop

1. **Get the next wave:** `python -m scripts.audit next --batches 6`
   (prints `bNNN slug1 slug2 ...` lines; stop if `NO_PENDING_BATCHES`).

2. **Dispatch one subagent per batch, in parallel,** using the Agent tool with
   `subagent_type: general-purpose`, `model: <haiku unless overridden>`, and
   `run_in_background: true`. Each prompt must be exactly:

   > Read /home/user/boardgame-rules/.claude/skills/audit-rules/SKILL.md and
   > follow it exactly for batch <bNNN> with these slugs: <slug1, slug2, ...>.
   > Work from the repository root /home/user/boardgame-rules.

3. **Collect results** (TaskOutput / completion notifications). Save all
   RESULT lines from the wave to a temp file, then:
   `python -m scripts.audit record /tmp/waveN.txt bNNN bNNN ...`
   - If a subagent returned malformed output or died (e.g. session limit),
     do NOT mark its batch done; delete any partial
     `docs/quality/audit-findings/<bNNN>.md` it wrote and re-dispatch the
     batch next wave.
   - If a RESULT line's reason looks generic or evidence-free, treat that
     game as unaudited: remove the line before recording and re-queue the
     batch (small models occasionally skip the evidence step; do not record
     guesses).

4. **Commit and push** after every wave:
   `git add docs/quality games.yaml && git commit -m "audit: wave (<batch ids>, <n> games)" && git push -u origin <current branch>`

5. Report a one-line progress update (use `python -m scripts.audit status`),
   then start the next wave.

## Notes

- The manifest/tracker live in `docs/quality/`; MAJOR games are auto-flagged
  in `games.yaml` with `review_notes` by the record step.
- Batches are pre-sized (≤7 games, ≤200 KB source text) to fit small-model
  context. Never merge batches.
- Subagents must not touch `games.yaml`, the manifest, or the tracker — only
  the orchestrator writes those (via `scripts.audit record`).
