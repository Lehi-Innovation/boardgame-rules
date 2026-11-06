# Splendor — expanded question coverage

**PASS: 23 added questions, 43 total.** Two fresh readers each answered the complete final bank **43/43**, with zero partial or incorrect answers and no unsupported guesses. The exact final summary has an independent source-audit PASS. A separate independent coverage reviewer confirmed practical saturation after finding and closing one additional setup gap.

Scope: **2014 first-edition core rules**, using the complete [extraction](../../../../../../extracted/splendor-rules.txt), excluding the nonmatching cached 2024 PDF. Requested and runtime-confirmed model: **gpt-6.1-sol**, **high** reasoning effort. This follows the [original twenty-question run](../README.md).

## Question-bank versions and novelty

The [final expanded-43-v1 questions](expanded-43-questions.json) and [fixed answer key](expanded-43-answer-key.json) preserve every original question, ID and answer. Extensions and their source-backed keys were frozen before readers saw them; manifests retain SHA-256 hashes. The evaluator had seen earlier results, so this is regression expansion, not an independently authored held-out evaluation.

| Added set | IDs | New coverage |
|---|---|---|
| [Extension 1](extension-01/questions.json) | 21–36 (16) | Reserved versus purchased benefits; zero-point bonuses; self-payment versus noble timing; excess discounts; persistent noble eligibility; reserve affordability; blind-draw refill; depletion; zero-net-gain token taking; gold recirculation; level access; compulsory noble after fifteen; last-player ending; noble depletion; component identities |
| [Extension 2](extension-02/questions.json) | 37–40 (4) | Gold payment choice when matching gems are owned; sparse gem piles; direct exchange; voluntary passing with legal actions |
| [Extension 3](extension-03/questions.json) | 41–42 (2) | Sorted accessible supply piles; unused tokens do not score |
| [Extension 4](extension-04/questions.json) | 43 (1) | Noble tiles must be shuffled before selection/reveal |

The [novelty policy](novelty-policy.json) accepts a new source-backed fact, different-outcome condition, or untested timing/exception interaction. Names, number changes and mechanical combinations without a new ruling do not qualify. Batch sizes follow meaningful coverage instead of padding to twenty. The earlier [42-question bank](question-bank.json) and [key](answer-bank.json) remain unchanged as a separate frozen version.

## Reader runs and repair

Every run used a new blind reader pair with `fork_turns: "none"`, seeing only its frozen summary and question file. Readers had no source, key, earlier answers, grades or browsing. Isolation was instruction-based rather than a separate filesystem sandbox.

| Run | Reader A: correct / partial / incorrect | Reader B: correct / partial / incorrect |
|---|---|---|
| [Extension 1, prior summary](extension-01/iteration-01/results.json) | 15 / 1 / 0 | 15 / 1 / 0 |
| [Extension 2, prior summary](extension-02/iteration-01/results.json) | 4 / 0 / 0 | 4 / 0 / 0 |
| [Combined forty, attempt 1](combined-iteration-01/results.json) | 40 / 0 / 0 | 39 / 1 / 0 |
| [Combined forty, attempt 2](combined-iteration-02/results.json) | 39 / 1 / 0 | 39 / 1 / 0 |
| [Original twenty regression](original-20-regression/results.json) | 20 / 0 / 0 | 20 / 0 / 0 |
| [Extension 3](extension-03/iteration-01/results.json) | 2 / 0 / 0 | 2 / 0 / 0 |
| [Full expanded-42-v1](expanded-42-iteration-01/results.json) | 42 / 0 / 0 | 42 / 0 / 0 |
| **[Full expanded-43-v1](expanded-43-iteration-01/results.json)** | **43 / 0 / 0** | **43 / 0 / 0** |

Q29 exposed the only new summary clarity gap. Both readers recognized remaining legal actions but abstained on whether complete development-card exhaustion itself ends the game. The [repair patch](combined-iteration-01/summary-changes.patch) adds one paragraph: exhaustion does not end play; remaining legal actions continue until the normal prestige ending. This is a source-supported deduction from empty market spaces being permitted and the stated prestige ending (extraction lines 152–157 and 182–188), not a new shortage or pass rule.

The combined-forty non-passes were Q4 answer-completeness failures: “take gold if available” omitted the one-token quantity in the fixed action definition. The summary already states one gold. Those failures remain recorded and no further rule repair followed. The final 42/43-series prompt explicitly requests quantities and legal conditions when listing actions. This is a disclosed output-instruction clarification, not a changed key or proof that summary changes alone explain the different scores. The same clarified instruction was kept for both full-bank versions.

## Independent challenge and stopping point

The initial [coverage map](source-rule-coverage.json) and [candidate review](candidate-review.json) reached 42 questions after two zero-addition sweeps. A separate source reviewer then actively challenged that claim, without keys, reader outputs or summary audits. Its [GAPS review](saturation-review.json) found that ledger R07 overstated coverage: Q3 asks about shuffling development decks, while the noble questions only ask counts and removal. No question tested shuffling nobles before revealing them.

Question 43 closes that gap. The [corrected map](source-rule-coverage-v2.json) cites Q43, and [two repeated targeted sweeps](candidate-review-v2.json) reviewed **13 source-clause candidates and 12 boundary/interaction candidates**, accepting zero additions. The separate reviewer reread the complete source and revised inputs, rechecked all 25 candidates, and challenged ten further scenarios. Its [final verdict is SATURATED](saturation-review-v2.json), with no further meaningful source-backed target.

The revised map covers 41 groups of gameplay/component/setup instructions. Candidates and rejection reasons remain available, including source limits: depleted-color under-taking, optional reduced draws, all-actions-impossible handling, unresolved further ties and voluntary below-limit token returns. Q40 separately covers voluntary passing **when legal actions exist**. No later-edition ruling was imported to fill source gaps.

This is practical saturation relative to the selected source and novelty criteria, not exhaustive enumeration of every hypothetical combination. New authoritative material or another edition can yield meaningful new questions.

## Final text, audits and validation

[Final coverage](final-coverage.json) now comes from **one fresh pair answering all 43 questions**, replacing the earlier [batched coverage milestone](batched-coverage.json). Both complete raw response sets and all failed attempts are retained.

| Final evidence | Link |
|---|---|
| Exact final summary | [Snapshot](expanded-43-iteration-01/summary-snapshot.md) |
| Frozen inputs, version and hashes | [Manifest](expanded-43-iteration-01/input-manifest.json) |
| Reader responses | [A](expanded-43-iteration-01/reader-a.json), [B](expanded-43-iteration-01/reader-b.json) |
| Every expected/observed answer and grade | [Results](expanded-43-iteration-01/results.json) |
| Actual model, effort and runtime identities | [Provenance](expanded-43-iteration-01/model-provenance.json) |
| Independent complete summary/source audit | [PASS, 27 claim groups](combined-iteration-01/source-audit.json) |
| Exact-byte audit reuse for final test | [Reuse record](expanded-43-iteration-01/source-audit.json) |
| Separate saturation review | [SATURATED](saturation-review-v2.json) |
| Completion and repository checks | [Validation](validation.json), [repository checks](repository-checks.json) |

The source auditor read the complete revised summary and complete source without questions, keys or reader answers. Later runs reuse its PASS only after verifying identical summary and source bytes. The [audit record](audit-record.txt) was applied using `scripts.audit record`, then stamping was confirmed unchanged. Question scores did not supply semantic sign-off.

Reader A's original output contained one unescaped quotation-mark pair in Q24 evidence. Its [raw bytes](expanded-43-iteration-01/reader-a.raw.json) are preserved; [normalization](expanded-43-iteration-01/serialization-normalization.json) only escaped those marks to make valid JSON. No answer, evidence wording, support label or ID changed.

Final summary SHA-256: `4b3b5c9c08624e81d2521ebe7d08669c16c70697c3908973495b9b5c8c0fbc66`.

Source SHA-256: `441009ef496552586c58811ecf40bf287292193753c553303748c39b92b03f70`.

Validation checks all 43 IDs exactly once in each final response/grade array, every expected/observed answer, unchanged constituent benchmarks, frozen hashes, exact [canonical summary](../../../../../../rules/splendor.md) equality, runtime models/effort, both source reviews, stopping evidence and report links. Structural validation, idempotent stamping, index/manifest regeneration and catalog checks passed. Both task-scoped and global `git diff --check` passed at final validation. Unrelated shared-worktree changes were preserved.
