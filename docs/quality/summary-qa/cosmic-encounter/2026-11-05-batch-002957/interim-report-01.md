# Cosmic Encounter — QA in progress

**Not ready for coordinator stamping.** The original 2008 CE01 summary has been repaired, the initial 20-question bank has passed two fresh Luna readers, and the expanded candidate bank contains 155 questions. Its independent source/coverage/key-scope challenge is running. The complete expanded blind test and fresh final source audit remain required.

This run covers the original Fantasy Flight English 2008 CE01 game, BGG 39463, its fifty original alien sheets, normal flare system and applicable base-only official FAQ. Optional Technology and variants, Anniversary additions and expansions are excluded. The original summary and assigned sources are preserved by hash. Only `rules/cosmic-encounter.md` and this exclusive evidence directory are written.

## Seed results

Each iteration used two new `gpt-6-luna` readers at `high`, with `fork_turns="none"`. Actual model/effort are verified from external runtime records in the sanitized [provenance](model-provenance.json). Frozen questions and key remain unchanged. Scores below use the independently adjudicated actual question scope; all original grades remain available.

| Frozen iteration | A correct / partial / incorrect | B correct / partial / incorrect | Outcome |
|---|---|---|---|
| [Original summary](seed-iteration-01/summary-snapshot.md) | 0 / 17 / 3 | 0 / 18 / 2 | Failed; edition mix and missing rules |
| [First repair](seed-iteration-02/summary-snapshot.md) | 18 / 1 / 1 | 17 / 1 / 2 | Failed; Morph discard omission and material reader errors |
| [Second repair](seed-iteration-03/summary-snapshot.md) | 20 / 0 / 0 | 20 / 0 / 0 | Passed the fixed seed bank |

For iteration 2, the first grader scored B 15/20. A [fresh adjudicator](seed-iteration-02/scope-adjudication.json) correctly treated two citation omissions as documentation defects: the facts were directly asserted and supported by the complete frozen summary. It retained both actual wrong rulings and the missing requested Morph discard outcome. For iteration 3, the first grader scored both 19/20; [fresh scope adjudication](seed-iteration-03/scope-adjudication.json) found that “which flares” was fully answered by all dealt flares plus random extras to ten. The key's equivalent six-plus-four arithmetic was not a separately asked calculation. No question/key was edited to obtain these results.

The baseline scope adjudicator initially misclassified missing-only Q015 answers as incorrect. Its explicit [grade-definition correction](seed-iteration-01/scope-adjudication-grade-definition-correction.json) restores Partial; both original artifacts remain intact.

## Repairs and authority

The repair replaces Anniversary component/setup material with fifty aliens and original two-flare selection. It adds the full encounter flow, destinations, hand-replacement windows, power/flare rules, original fifty abilities and applicable base FAQ exceptions. Retained official May 6, 2009 errata recover Macron, Spiff, Warrior, Mind Wild and Reincarnator Wild corrections omitted from the later FAQ's errata list; later 2018 answers supersede older answers.

The [preliminary independent source audit](source-review/preliminary-source-audit.json) returned **MINOR**, finding one omitted reward-choice commitment rule and the designer/developer attribution. Both have been repaired in [the current candidate snapshot](repair-freeze-03.md). That snapshot is newer than the passing seed snapshot and has **not** yet passed the expanded bank or final audit. The inherited verification banner remains machine-managed and untouched.

The source audit visually inspected all fifty original sheets with explicit original-resolution forwarding. Its delivery receipt records actual returned JPEG hashes/dimensions matching the pinned originals. The parent is completing equivalent renewed native-delivery receipts. Original file hashes alone are not presented as image-transport proof.

The official 2018 FAQ has an unresolved reinforcement/negotiate wording conflict. The original setup also omits its ordinary reveal window. Original evidence and [independent source adjudication](source-review/conflict-adjudication.json) remain preserved. The coordinator has asked the human about those and Calculator/Hate equality boundaries; no answer or interpretation is assumed. No dependent outcome key is frozen.

## Expanded coverage and remaining work

[Candidate questions](expanded-candidate-05/questions.json), [key](expanded-candidate-05/answer-key.json), [readable bank](expanded-candidate-05/question-bank.md), and [coverage map](expanded-candidate-05/coverage-map.json) preserve the original twenty entries. The map covers 44 rulebook passage groups, fifty printed sheets, 164 base-relevant FAQ rows and retained earlier errata. These counts include explicit pending/excluded mappings and are not a completed-coverage verdict.

The [acceptance/rejection ledger](expanded-candidate-05/acceptance-rejection-ledger.json) and [targeted passes](expanded-candidate-05/review-inputs/targeted-coverage-passes.json) reject cosmetic/numerical variants and excluded-module scenarios. Two parent passes added no further source-resolvable question after the reward-source timing addition. The complete-scope stopping rule remains pending the fresh challenge and coordinator scope resolutions. The fresh reviewer must validate an actual-asked-clause/fact map before the full-bank blind test.

Readers see only their frozen summary/questions and identical generic process instructions, differing only in output path. They read complete inputs in bounded character chunks, choose complete operative units themselves, and provide required direct case rulings/calculations. The latest protocol permits complete quotations to answer ordinary lookups, reducing inconsistent restatement. This is a **known fixed-set tool-assisted regression**, not held-out accuracy or exhaustive scenario coverage. Exact model-visible chunk contents are independently checked against runtime tool outputs; encrypted task bodies prevent independent plaintext prompt comparison, a separately disclosed provenance limit.

Remaining gates: finish the independent bank/key/scope challenge, resolve authorized source scope, renew stopping checks if additions arise, freeze the full bank/key/scope, run two fresh Luna readers over every ID until both pass, obtain a new final source-only audit, validate exact canonical/snapshot/source/key integrity, and await coordinator audit recording/stamping and any exact-byte retest.

Report date: November 6, 2026 (America/Phoenix). Persistent goal remains active.
