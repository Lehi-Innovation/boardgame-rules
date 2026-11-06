# Root QA — Ready for final coordinator acceptance

**benchmark-v10, 81 questions.** Two new gpt-6-luna/high readers each scored **81/81**, with zero partial or incorrect answers and no unsupported guesses. A genuinely new gpt-6.1-sol/high source-only auditor passed these exact summary bytes. Targeted evidence validation passed.

Coordinator acceptance remains required before completing the goal. Shared audit recording, verification stamping, catalogs, commit and push remain coordinator-owned.

## Scope and authoritative sources

October 13, 2025 Law: common rules, Standard Setup, four base factions, Fall/Winter, base Thief/Tinker/Ranger, dominance and coalitions; plus applicable base-game FAQs in the complete official publisher English p16 Rules Library, retrieved November 5, 2026. Expansion factions, characters, maps, card decks, second Vagabond, hirelings, landmarks, bots and Advanced Setup are excluded.

Sources: [original extracted Law](../../../../../extracted/root-rules.txt), [original PDF](../../../../../source_pdfs/root-recovery.pdf), [complete publisher rendered text](../../batches/2026-11-05-batch-002957/source-preflight/root/publisher-rules-library-p16.txt), [raw publisher response](../../batches/2026-11-05-batch-002957/source-preflight/root/publisher-rules-library-p16.json), and [live publisher library](https://rules.ledergames.com/?product=root&locale=en-US&printing=p16). All remain read-only. The publisher JSON rendered text plus one newline equals the supplied text exactly. Individual FAQ publication dates are not displayed; none were inferred. Printed item glyphs were checked in PDF images. The Law delegates individual printed card/quest and track values to physical components.

This is a known regression suite: the evaluator saw the initial summary while selecting questions. It is not a held-out test or proof of exhaustive scenario coverage.

## Complete iteration history

C/P/I means correct/partial/incorrect. Historical rows retain their original frozen keys. In particular, the v9 scores do **not** establish source correctness for Q20/Q46: the later full publisher FAQ review found their key omission/error. Original outputs, keys and scores remain unchanged; v10 explicitly corrects them.

| Iteration | Bank / N | A C/P/I | B C/P/I |
|---|---|---|---|
| [seed-iteration-01](seed-iteration-01/results.json) | benchmark-v1 / 20 | 0/11/9 | 0/11/9 |
| [seed-iteration-02](seed-iteration-02/results.json) | benchmark-v1 / 20 | 17/2/1 | 16/2/2 |
| [seed-iteration-03](seed-iteration-03/results.json) | benchmark-v1 / 20 | 19/1/0 | 19/1/0 |
| [seed-iteration-04](seed-iteration-04/results.json) | benchmark-v1 / 20 | 19/1/0 | 20/0/0 |
| [seed-iteration-05](seed-iteration-05/results.json) | benchmark-v1 / 20 | 19/1/0 | 18/2/0 |
| [seed-iteration-06](seed-iteration-06/results.json) | benchmark-v1 / 20 | 20/0/0 | 20/0/0 |
| [expanded-iteration-01](expanded-iteration-01/results.json) | benchmark-v3 / 77 | 70/6/1 | 61/13/3 |
| [expanded-iteration-02](expanded-iteration-02/results.json) | benchmark-v3 / 77 | 74/2/1 | 75/1/1 |
| [expanded-iteration-03](expanded-iteration-03/results.json) | benchmark-v9 / 80 | 74/5/1 | 76/3/1 |
| [expanded-iteration-04](expanded-iteration-04/results.json) | benchmark-v9 / 80 | 74/6/0 | 75/4/1 |
| [expanded-iteration-05](expanded-iteration-05/results.json) | benchmark-v9 / 80 | 77/3/0 | 77/3/0 |
| [expanded-iteration-06](expanded-iteration-06/results.json) | benchmark-v9 / 80 | 75/5/0 | 79/1/0 |
| [expanded-iteration-07](expanded-iteration-07/results.json) | benchmark-v9 / 80 | 78/2/0 | 79/1/0 |
| [expanded-iteration-08](expanded-iteration-08/results.json) | benchmark-v9 / 80 | 78/2/0 | 78/2/0 |
| [expanded-iteration-09](expanded-iteration-09/results.json) | benchmark-v9 / 80 | 77/3/0 | 79/1/0 |
| [expanded-iteration-10](expanded-iteration-10/results.json) | benchmark-v9 / 80 | 80/0/0 | 80/0/0 |
| [expanded-iteration-12](expanded-iteration-12/results.json) | benchmark-v9 / 80 | 75/3/2 | 79/1/0 |
| [expanded-iteration-13](expanded-iteration-13/results.json) | benchmark-v9 / 80 | 77/3/0 | 80/0/0 |
| [expanded-iteration-14](expanded-iteration-14/results.json) | benchmark-v9 / 80 | 80/0/0 | 79/1/0 |
| [expanded-iteration-15](expanded-iteration-15/results.json) | benchmark-v9 / 80 | 80/0/0 | 80/0/0 |
| [expanded-iteration-16](expanded-iteration-16/results.json) | benchmark-v10 / 81 | 81/0/0 | 81/0/0 |
| [expanded-iteration-17](expanded-iteration-17/results.json) | benchmark-v10 / 81 | 81/0/0 | 81/0/0 |

Iteration11 was prepared but never dispatched. All failed runs, intermediate snapshots, raw grades and semantic adjudications remain. The [grading correction ledger](grading-corrections.json) records earlier corrections; [iteration10 whole-response adjudication](whole-response-semantic-adjudication-note.json) preserves the decision to accept explicit source quotations with a consistent application without demanding duplicate wording. Missing requested outcomes and materially false volunteered rules still fail.

Iteration15 originally received 80/0/0 for both readers under v9. A separate Q41 dispute was resolved by verified publisher FAQ and a [fresh independent decision](expanded-iteration-15/q41-publisher-resolution-independent.json): actual one-warrior placement before Turmoil is true. [Resolution record](expanded-iteration-15/q41-resolution-record.json) retains the contrary inference, neutral Law-only assessment and final authority. This does not erase the separate Q46 error discovered by the full-source review. The [additive same80-question source reassessment](expanded-iteration-15/publisher-source-extension-assessment.json) records78/1/1 for each without altering the original results; it is not a full81-question test.

Iteration16 raw grades were80/1/0 for each reader. Fresh [Q14 literal scope review](expanded-iteration-16/q14-independent-scope-adjudication.json) confirmed that full capacity is a stated condition, so defining its numerical threshold is key context; both corrected totals are81/0/0. [Additive changes](expanded-iteration-16/q14-adjudication-application-note.json) and original grades remain. A first focused Q15 reviewer interpreted B’s repeated normal scoring sentence as an extra award, while the full grader and a [fresh isolated resolution](expanded-iteration-16/q15-fresh-resolution.json) found it co-referred to the same ordinary award. The [resolution record](expanded-iteration-16/q15-resolution-record.json) preserves both interpretations; no actual extra award was excused. The final summary nevertheless removes the redundant scoring sentence for clarity. New bytes require the new exact audit and full81 pair reported here.

## Publisher-source extension, repairs and coverage

The complete-source [independent audit](expanded-iteration-15/source-only-audit-full-publisher/source-audit.json) found three material issues: Charismatic placement-before-Turmoil was ambiguous, Allied Alliance movement was wrongly said to cause Outrage, and coalition eligibility omitted already-dominant players. All three were repaired, with publisher clarifications in a labeled FAQ section. The FAQ also clarifies Field Hospitals returning attackers before the ambush no-attacker check. [Repair record](publisher-repair-record-v2.json), [exact changes](source-audit-candidate-18/summary-changes-from-stamped.patch), [historical full-source delivery proof](expanded-iteration-15/source-only-audit-full-publisher/source-delivery-audit.json).

The first fresh complete-FAQ [coverage review](publisher-faq-coverage-review-01.json) classified all58 FAQ occurrences and found one genuine new priority branch: Hospitals can prevent ambush from ending battle. It became Q81. Q20 and Q46 were corrected as existing targets, with no novelty credit: [v10 explicit key corrections](benchmark-v10/key-corrections.json). All prior80 question IDs/wording and other78 prior answers are preserved. Old benchmark versions and [v9 coverage ledger](coverage-ledger-v9.json) remain.

The bank grew 20 →66 →77 →78 →79 →80 →81: **20 seeds,53 qualifying additions,8 retained overlapping regressions**. Overlaps Q38,Q41,Q44,Q45,Q46,Q52,Q60,Q61 remain tested but do not count as novel coverage. The current [coverage/rejection ledger](coverage-ledger.json) maps the original Law and applicable FAQ branches. Targeted passes27/28 added zero; a new source/key-only reviewer actively challenged and upheld saturation: [final coverage review](publisher-faq-coverage-review-02.json), [coverage status](coverage-status.json). This is working saturation under the documented novelty criterion.

Final [readable bank](benchmark-v10/question-bank.md), [questions](benchmark-v10/questions.json), [key](benchmark-v10/answer-key.json), [source/bank hashes](benchmark-v10/input-manifest.json). Contextual key facts are not extra requested targets; actual requested eligibility, costs, operations and consequential exceptions are required.

## Final blind pair and fresh source audit

Both final readers were new independent Luna/high sessions with fork_turns=none. They saw only the same frozen summary and questions, with identical saved instructions except output path. The [v8 reader protocol](reader-protocol-v8-template.txt) preserves generic quote/apply/check instructions, complete procedural passages, groups of at most five and the same ten-question-per-turn schedule; v8 updates the bank size to81 and handles the final remainder explicitly, while retaining the generic process. Continuations supplied no rule facts, key, expected clauses or grade feedback. Original sessions answered the entire bank, with immutable checkpoints.

Final [Reader A](expanded-iteration-17/reader-a.json), [Reader B](expanded-iteration-17/reader-b.json), [independent full-bank grades](expanded-iteration-17/independent-grades.json), [results](expanded-iteration-17/results.json), [raw-output hashes](expanded-iteration-17/raw-output-manifest.json), [quotation review](expanded-iteration-17/quotation-review-validation.json), and [all-turn model proof](expanded-iteration-17/reader-turn-provenance.json). The primary evaluator read all final answers; every requested part and any volunteered material ruling were graded. No answer borrowed facts from another question.

[Actual runtime model evidence](runtime-model-provenance.json), [final pair provenance](expanded-iteration-17/model-provenance.json), [saved-prompt comparison](reader-protocol-provenance.json), [dispatch metadata](agent-dispatch-manifest.json). Isolation is fresh context plus explicit input restrictions, not a stronger filesystem jail. Runtime dispatch message bodies are encrypted; saved prospective plaintext prompts and visible tool inputs are retained, while actual model/fork/task metadata and encrypted-message hashes are independently recorded.

Actual [reader delivery evidence](reader-delivery-audit.json) matches nonempty source lines in ordered exact delivered blocks, decoding JSON transport and declared line-number prefixes only. It proves delivery, not cognitive attention. The historical [iteration9 A delivery gap](expanded-iteration-09/delivery-defect.json) remains disclosed; no grade was changed because of that delivery defect. Final readers have separate complete-input proofs.

The final source-only auditor is **publisher_final_source_auditor_03**, a genuinely new Sol/high fork_turns=none agent, distinct from the earlier auditor who found the issues and all repair/key/grading actors. It received only the final candidate and complete authority sources: no prior findings, repair history, questions, key, reader outputs or grades. It independently read the complete summary, Law extraction, publisher source and all32 PDF page texts, and inspected essential glyph renders. [Final exact-source audit](expanded-iteration-17/source-audit.json), [actual source-delivery proof](expanded-iteration-17/source-auditor-delivery-audit.json). The earlier candidate17 auditor’s first source-delivery claim had a skipped publisher range and a small PDF gap; that auditor recovered them and re-evaluated before its PASS. [Original audit](source-audit-candidate-17/source-only-audit/source-audit-before-delivery-recovery.json) and [initial incomplete delivery proof](source-audit-candidate-17/source-delivery-proof/source-delivery-audit.json) remain. Final actual delivery is complete. Candidate18’s [declared-prefix comparison refinement](source-audit-candidate-18/source-proof-prefix-disposition.json) preserves its initial verifier result and the exact prefix-only correction; no source text changed. No findings remain unresolved.

## Validation and handoff

Final summary SHA-256: `844f9b73297121dc8813cb18c623d68cdafc9942bcba8485ca0cccaec56eebec`.

[Evidence validation](validation.json) verifies unique JSON keys, immutable input/prompt/source/raw/checkpoint hashes, documented-only key corrections, complete ID sets, grades matching actual responses and fixed keys, all requested facts supported, actual models across all reader turns, complete source delivery, current coverage hashes and byte equality with canonical [Root summary](../../../../../rules/root.md). [Targeted Root catalog comparison](targeted-catalog-comparison.json), structural validation and scoped git diff --check passed. No shared artifacts were regenerated.

**Ready for final coordinator acceptance.** Preserve these exact tested bytes. Any later stamping/body change requires complete-bank retesting on the changed bytes. The goal remains open until acceptance.
