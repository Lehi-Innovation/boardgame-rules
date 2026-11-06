# Root QA — Ready for coordinator

Root (BGG 237182), **2026-11-05-batch-002957**. Final bank **v9**, **80 questions**. Both fresh readers scored 80/80, with zero partial/incorrect/unresolved answers or unsupported guesses. Independent source audit and targeted validation passed.

## Scope and authority

The October 13, 2025 Law: common rules, Standard Setup, four base factions, Fall/Autumn and Winter, base Thief/Tinker/Ranger, dominance and Vagabond coalitions. Expansion factions/characters/maps, second Vagabond, hirelings, landmarks, bots and Advanced Setup are excluded. The complete applicable extracted source and PDF were read; PDF glyphs and ruin setup were inspected. Numbered Law sections are the reference IDs, rather than extraction ordering or unlabeled PDF-page numbers.

Authoritative [extracted text](../../../../../../extracted/root-rules.txt), [PDF](../../../../../../source_pdfs/root-recovery.pdf), [source-reading record](../source-reading-notes.md), and [original input manifest](../input-manifest.json). Source files stayed read-only and their hashes remain unchanged. The evaluator saw the original summary before question selection; this is a known regression suite, not a held-out test.

## Results

Every requested part was graded separately from support/confidence labels. A missing or unresolved requested fact is partial; a materially wrong ruling or contradictory caveat is incorrect. Facts were never borrowed from another answer. All frozen inputs, raw responses, grades and failed rounds remain. Historical rows use their original fixed keys, not later corrected targets.

| Iteration | Bank / N | Reader A C/P/I | Reader B C/P/I |
|---|---|---|---|
| [seed-iteration-01](../seed-iteration-01/results.json) | v1 / 20 | 0/11/9 | 0/11/9 |
| [seed-iteration-02](../seed-iteration-02/results.json) | v1 / 20 | 17/2/1 | 16/2/2 |
| [seed-iteration-03](../seed-iteration-03/results.json) | v1 / 20 | 19/1/0 | 19/1/0 |
| [seed-iteration-04](../seed-iteration-04/results.json) | v1 / 20 | 19/1/0 | 20/0/0 |
| [seed-iteration-05](../seed-iteration-05/results.json) | v1 / 20 | 19/1/0 | 18/2/0 |
| [seed-iteration-06](../seed-iteration-06/results.json) | v1 / 20 | 20/0/0 | 20/0/0 |
| [expanded-iteration-01](../expanded-iteration-01/results.json) | v3 / 77 | 70/6/1 | 61/13/3 |
| [expanded-iteration-02](../expanded-iteration-02/results.json) | v3 / 77 | 74/2/1 | 75/1/1 |
| [expanded-iteration-03](../expanded-iteration-03/results.json) | v9 / 80 | 74/5/1 | 76/3/1 |
| [expanded-iteration-04](../expanded-iteration-04/results.json) | v9 / 80 | 74/6/0 | 75/4/1 |
| [expanded-iteration-05](../expanded-iteration-05/results.json) | v9 / 80 | 77/3/0 | 77/3/0 |
| [expanded-iteration-06](../expanded-iteration-06/results.json) | v9 / 80 | 75/5/0 | 79/1/0 |
| [expanded-iteration-07](../expanded-iteration-07/results.json) | v9 / 80 | 78/2/0 | 79/1/0 |
| [expanded-iteration-08](../expanded-iteration-08/results.json) | v9 / 80 | 78/2/0 | 78/2/0 |
| [expanded-iteration-09](../expanded-iteration-09/results.json) | v9 / 80 | 77/3/0 | 79/1/0 |
| [expanded-iteration-10](../expanded-iteration-10/results.json) | v9 / 80 | 80/0/0 | 80/0/0 |

The original 20-question v1 bank passed in seed iteration 6. Ambush-disposal and operation-list scope over-grading were corrected only after fresh independent adjudication; previous grades and original independent-grade reports remain. [Grading correction ledger](../grading-corrections.json), [seed adjudication](../seed-iteration-04/adjudication.json), [operations-scope adjudication](../operations-scope-adjudication.json). Q47 asks operation names, so its key context was not inflated into tested Recruit procedure; Q78 explicitly tests that procedure. Iteration 4 also received a fresh [semantic scope adjudication](../expanded-iteration-04/scope-adjudication.json): defined terms and same-answer equivalents received credit, while consequential quantities and wrong volunteered permissions remained failures. Its [original grades](../expanded-iteration-04/independent-grades.json), [before-adjudication results](../expanded-iteration-04/results-before-scope-adjudication.json), and [grade changes](../expanded-iteration-04/adjudication-grade-changes.json) remain. The resulting [v2 grader policy](../grading-scope-policy-v2.json) was frozen before iteration 5 grading. Iteration 5 received another fresh [scope adjudication](../expanded-iteration-05/scope-adjudication.json), with [original grades](../expanded-iteration-05/independent-grades.json), [pre-adjudication grades](../expanded-iteration-05/results-before-scope-adjudication.json) and [changes](../expanded-iteration-05/adjudication-grade-changes.json) retained. The resulting [v3 policy](../grading-scope-policy-v3.json) was frozen before iteration 6 grading. Iteration 6 received a further [same-answer semantic adjudication](../expanded-iteration-06/scope-adjudication.json); its [original grades](../expanded-iteration-06/independent-grades.json), [pre-adjudication results](../expanded-iteration-06/results-before-scope-adjudication.json) and [changes](../expanded-iteration-06/adjudication-grade-changes.json) remain. [V4 grader policy](../grading-scope-policy-v4.json) propagated those prior semantic decisions before iteration 7 grading. The [v5 grader policy](../grading-scope-policy-v5.json) carried the fresh iteration 9 narrow-shortage and repetition decisions into iteration 10. These policies were never supplied to readers; questions and key stayed unchanged. Reader A’s [iteration 6 field-layout defect](../expanded-iteration-06/reader-format-notes.json) was preserved and all factual fields were graded without a format-only penalty.

Iteration 10 raw independent grades were A78/2/0 and B80/0/0. Fresh setup-scope adjudication corrected A Q07; a second fresh Sol/high adjudicator then reviewed the complete A Q04 response without seeing grades or preferred outcome. Its exact quotation explicitly defines hammer payment as exhaustion, and its ruling consistently applies the payment. The final semantic decision is correct, without requiring the same fact twice across fields. No contradictory or explicitly unresolved ruling was excused, and no fact was borrowed from another question. [Fresh Q04 decision](../expanded-iteration-10/q04-fresh-adjudication.json), [additive grade change](../expanded-iteration-10/q04-fresh-grade-change.json), [before-change results](../expanded-iteration-10/results-before-q04-fresh-adjudication.json), [interpretation note](../whole-response-semantic-adjudication-note.json). Original grades and earlier contrary adjudications remain intact. Iteration 11 was prepared but never dispatched; its prospective files remain, and it contributes no reader scores.

## Coverage and key history

The bank grew 20 → 66 → 77 → 78 → 79 → 80. It contains **20 seeds, 52 qualifying additions and eight retained overlapping regressions**. The overlaps (Q38, Q41, Q44, Q45, Q46, Q52, Q60, Q61) remain in every full test but do not count as new source coverage. No hard question was removed. The [coverage/rejection ledger](../coverage-ledger.json) records accepted novelty, rejected candidates, source mappings, historical stopping failures and the two final clean zero-addition passes **24 and 25**. A fresh source/key reviewer independently upheld them with no further additions or corrections: [final coverage PASS](../coverage-review-08.json), [current coverage status](../coverage-status.json). This is saturation under the stated scope/novelty rule, not enumeration of every possible combination.

Question IDs and wording are preserved. Four answer targets required source-backed completeness corrections, transparently versioned before the final test:

- [v6 Q37](../benchmark-v6/key-corrections.json): broad wood production includes Daylight Overwork, not just Birdsong.
- [v7 Q04](../benchmark-v7/key-corrections.json): one ready undamaged Vagabond hammer per crafting icon.
- [v8 Q07/Q12](../benchmark-v8/key-corrections.json): hidden ruin shuffle/return and ordinary Eyrie Recruit placement.
- [v9 Q07](../benchmark-v9/key-corrections.json): initial shared-deck shuffle before dealing.

Original entries and hashes remain intact within their own benchmark versions. Every other prior answer is unchanged. The [final readable bank](../benchmark-v9/question-bank.md), [questions](../benchmark-v9/questions.json), [key](../benchmark-v9/answer-key.json) and [benchmark hashes](../benchmark-v9/input-manifest.json) are preserved separately. Q25’s shorthand means treating birds as the prompted suit, not bird-first selection or extra quantity.

## Summary repairs and independent audit

Repairs corrected faction setup, crafting costs and destinations, battle timing/scoring, dominance/coalition conditions, Keep/hospitals, the wood network, Decree/turmoil/leaders, Alliance supporters/Outrage/Train/Organize, and Vagabond quests/items/relationships. General rules and procedure tables were clarified; no scenario answer key was appended to the summary. Per-iteration diffs retain the changes. An early independent audit rejected an unsupported Revolt placement prerequisite; it was removed.

The final independent auditor was fresh at its full audit, authored no summary repairs, and never saw questions, key, reader responses or grades. It checked the full applicable source, then verified every subsequent exact-text update. [Final exact-text source audit](../expanded-iteration-10/source-audit.json), [fresh full-source audit](../source-audit-candidate-07/source-audit.json), [final audited source snapshot](../source-audit-candidate-16/summary-snapshot.md). No material findings remain.

The Law delegates printed faction-track values and individual card/quest faces to physical components; those exact values are not reconstructed or invented. The audit also does not verify inherited play-time catalog metadata. These recorded source limitations do not leave an essential procedural ruling gap in this scoped test.

## Reader isolation and model provenance

Each iteration used two new **gpt-6-luna / high** readers with `fork_turns="none"`; primary/source/question reviewers used **gpt-6.1-sol / high**. Actual settings and independent session identities are confirmed from runtime `session_meta` and `turn_context`, not directory names or requested labels: [runtime evidence](../runtime-model-provenance.json), [final pair provenance](../expanded-iteration-10/model-provenance.json). Isolation is fresh context plus explicit two-file access instructions, not a stronger filesystem jail.

The final prompt uses the coordinator-authorized [v5 quote/apply/check protocol](../reader-protocol-v5-template.txt), introduced in iteration 10. It distinguishes question-stated scenario givens from summary-only rules authority, requires bounded complete input reads, relevant source quotations, per-clause applications and a self-check. This generic process supplies no rules facts. Iteration 10 kept candidate16 summary bytes, questions and key unchanged from iteration 9; the protocol change did not regrade earlier attempts. Both readers received identical text except output path, saved before dispatch: [A prompt](../expanded-iteration-10/reader-a-prompt.txt), [B prompt](../expanded-iteration-10/reader-b-prompt.txt), [protocol provenance](../reader-protocol-provenance.json), [dispatch metadata](../agent-dispatch-manifest.json). No question/key answer facts were leaked. Runtime dispatch message bodies are encrypted; their hashes and clear model/fork/task metadata are retained, while the final prompt plaintext copies and visible tool inputs preserve the new protocol. Older raw reader outputs and visible tool-history prompts remain unchanged.

Actual input delivery was checked against runtime read-call/output pairs for 32 reader sessions: [delivery audit](../reader-delivery-audit.json). Ordered exact matching blocks, raw outputs, hashes, requested caps, truncation markers and recovery ranges are retained; declared line-number prefixes alone are removed for comparison. This proves delivery rather than cognitive attention. Iteration 9 A had a [confirmed delivery gap](../expanded-iteration-09/delivery-defect.json): the ordinary-removal VP table and following note were lost across the initial truncated output and recovery ranges. That failed run and its factual grades remain, flagged as affected; no score was changed because of delivery. Both iteration 10 readers separately proved complete delivery of the frozen summary and all questions. Iterations 6 and 7 retested identical candidate13 bytes under the same protocol; the repeated attempt is explicit in the iteration 7 manifest.

Iteration 10 A has 114 exact contiguous quotations. B has 93 quotations, including 18 mechanical substring flags. A fresh independent reviewer inspected every flagged block with its complete application and source; the [itemized dispositions](../expanded-iteration-10/quotation-disposition-independent.json) distinguish formatting/noncontiguous joins or equivalent wording from actual altered claims. Mechanical mismatch alone does not change a semantic grade. The [original mechanical audits](../expanded-iteration-10/reader-b-quote-audit.json) and raw responses remain unchanged.

## Validation and handoff

Final summary SHA-256: `06fd7ebcde0f0bba4bf074405dea68f0bc3d6125cd6f636861b5d7a0bc9f87c0`.

[Final validation](../validation.json) checks original/frozen hashes, documented-only key changes, all expected IDs once per reader/grade set, grades against actual raw answers and fixed keys, actual models, current coverage hashes, exact audit input hashes, and byte equality with canonical [rules/root.md](../../../../../../rules/root.md). [Targeted catalog comparison](../targeted-catalog-comparison.json) checks Root only. Structural validation and scoped `git diff --check` pass; unrelated/shared artifacts were not regenerated.

All evidence is local to this assigned run. Shared registries/catalogs, audit recording, verification stamping, commits and pushes remain coordinator-owned. **Ready for coordinator**: retain this exact snapshot. If stamping changes any tested bytes, run the complete fixed final bank with a new reader pair on the stamped version before publishing.
