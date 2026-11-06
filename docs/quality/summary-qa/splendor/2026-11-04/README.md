# Splendor summary QA — November 4, 2026

> **Follow-up:** The question bank was expanded to 43 questions and the summary clarified further. See the [expanded coverage report](coverage-expansion/README.md) for current results and exact final bytes. This report preserves the initial twenty-question run.

**PASS on the fixed 20-question regression set.** Two fresh readers each answered all 20 questions completely and correctly from the exact final summary, with no unsupported guesses. An independent source auditor passed the final text with no unresolved findings.

Scope: **Splendor, first edition (2014), core game**, using the complete [authoritative extraction](../../../../../extracted/splendor-rules.txt). The cached `source_pdfs/splendor-rules.pdf` is a different, 2024 revision; it was inspected during preparation, fingerprinted, and excluded from the key and audits. No diagram-dependent questions were used. References in the key and audits are **extraction line numbers**, not PDF page numbers.

## Results

All readers requested and runtime-confirmed **gpt-6.1-sol, high reasoning effort**. Each row uses a new pair of readers with `fork_turns: "none"`; readers saw only their frozen summary and identical question file. Isolation was instruction-based, without a separate filesystem sandbox. The source auditor was separate from the evaluator/repairer and never received questions, key, responses or grades.

| Iteration | Reader A: correct / partial / incorrect | Reader B: correct / partial / incorrect | Independent source audit |
|---|---|---|---|
| [Original](iteration-01/results.json) | 17 / 3 / 0 | 17 / 3 / 0 | [MAJOR](iteration-01/source-audit.json): six findings |
| [Final repaired and stamped](iteration-02/results.json) | 20 / 0 / 0 | 20 / 0 / 0 | [PASS](iteration-02/source-audit.json): no findings |

The evaluator read the source and original summary before choosing questions. The [20 questions](questions.json), [predetermined answer key](answer-key.json), grading standard and [original fingerprints](input-manifest.json) were fixed before dispatch. They remained unchanged; this is a regression evaluation, not a held-out test or exhaustive coverage claim. No comparison with another model was performed.

## Findings and repairs

Both original readers abstained on token visibility (Q5) and noble tile destination/orientation (Q17). The summary now requires all owned tokens to remain visible to all players at all times, and places received nobles face-up in front of the recipient.

Both also gave incomplete action lists (Q4): they named the four choices and rejected combined actions, but omitted the same-color supply condition and legal purchase sources included in the frozen key. Reader A also omitted the empty-gold exception. These rules already existed elsewhere in the summary; this was an answer-completeness failure rather than absent coverage. The main action list now states the conditions together.

The source audit independently identified six findings. All were resolved in the [repair patch](iteration-02/summary-changes.patch):

- Removed the depleted-supply exception for taking fewer than three different gems, which the selected 2014 extraction does not establish. This does not assert the opposite ruling or disprove a later-edition rule.
- Added token visibility and noble tile placement.
- Relabeled the ten noble tiles as box inventory, distinct from the players-plus-one tiles used in a game.
- Removed unsupported card-level cost/point generalizations, card-field positions and the exact 0–5 prestige range.
- Limited the hidden-deck-card wording to drawing a reservation, replacing the overbroad “never shown.” Purchased cards still display bonuses and points.

The token-limit description now explicitly permits temporary excess and returning newly drawn gold, applying the source's end-of-turn limit and return-any-new-token rule.

The [repaired summary before stamping](repaired-summary-before-stamp.md) received an [independent PASS](repaired-source-audit.json). That verdict was [recorded](audit-record.txt) with `scripts.audit record`, then the canonical page was stamped. The auditor inspected the [exact final snapshot](iteration-02/summary-snapshot.md), confirmed only verification metadata/banner changed after the earlier audit, and retained PASS. The [prior semantic status](prior-verification.json) is preserved. The QA scores alone did not supply semantic sign-off.

The source does not resolve smaller token draws under shortage, optional under-taking, passing, or a further tiebreak after equal points and equal purchased developments. The summary adds no rulings on these cases. The audit also notes that play-time metadata and exact overall player range are not fully established by this extraction.

## Evidence and validation

| Evidence | Original | Final |
|---|---|---|
| Frozen summary | [Snapshot](iteration-01/summary-snapshot.md) | [Snapshot](iteration-02/summary-snapshot.md) |
| Frozen inputs and hashes | [Manifest](iteration-01/input-manifest.json) | [Manifest](iteration-02/input-manifest.json) |
| Original reader responses | [A](iteration-01/reader-a.json), [B](iteration-01/reader-b.json) | [A](iteration-02/reader-a.json), [B](iteration-02/reader-b.json) |
| Every question's expected/observed answer and grade | [Results](iteration-01/results.json) | [Results](iteration-02/results.json) |
| Actual model/effort and runtime identities | [Provenance](iteration-01/model-provenance.json) | [Provenance](iteration-02/model-provenance.json) |
| Independent source audit | [Audit](iteration-01/source-audit.json) | [Audit](iteration-02/source-audit.json) |
| Completion checks | [Validation](iteration-01/validation.json) | [Validation](iteration-02/validation.json) |

The final summary SHA-256 is `294f9e9e8b38a6201ca95014bac96416d0dda2ae5feada56dc5248705203b9cc`. At completion of this initial run, its frozen final snapshot and the [canonical summary](../../../../../rules/splendor.md) were byte-identical; the follow-up above records the later canonical revision. The source, question and key hashes remain unchanged. Each response and grade array contains IDs 1–20 exactly once; grades preserve actual reader answers and evidence.

[Repository checks](repository-checks.json): structural validation, idempotent stamping, index/manifest regeneration, and catalog consistency all passed (1,665 summaries). Temporary generated outputs were compared before replacing live artifacts, preserving unrelated shared-worktree work. The Splendor-scoped whitespace check passed. Global `git diff --check` reports 562 whitespace issues in unrelated edits to `extracted/13-dead-end-drive-rules.txt`, `extracted/cluedo-rules.txt`, and `extracted/mexican-train-rules.txt`; these were left unchanged.

All original responses, failed baseline evidence, repairs and audits are retained. A future held-out evaluation should freeze a separately authored, previously unseen question set.
