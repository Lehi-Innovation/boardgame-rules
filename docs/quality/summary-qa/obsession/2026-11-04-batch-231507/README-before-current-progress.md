# Obsession summary QA — 2026-11-04 batch 231507

Work performed November 5, 2026 (America/Phoenix). **In progress: the 60-question bank and source coverage have passed independent review; full-bank blind repair/retest continues.**

Scope: Dan Hallagan / Kayenta Obsession (BGG 231733), second-edition base/core standard 16-round multiplayer for 2–4 players, base objective deck. The publisher Universal Rules Compendium (2025-12-17) and Corrigendum 1.0 (2026-10-06) replace the former third-party condensed 2.2E source. Marked expansions, optional variants and alternate modes are excluded; the current default seasonal Market refresh is included.

The official French publisher base rulebook is supplemental only for the unchanged reputation objective. Its worked objective example resolves the Max-level versus wheel-position ambiguity; no older general flow rules were imported. See [provenance](supplemental-source-provenance.json), [initial finding](source-review-01/source-audit.json) and [independent resolution](source-review-01/supplemental-resolution.json).

## Benchmark history

| Iteration | Bank | Reader A correct / partial / incorrect | Reader B correct / partial / incorrect |
|---|---|---|---|
| Original summary | seed-v1, 20 | 0 / 20 / 0 | 0 / 20 / 0 |
| First repair | seed-v1, 20 | 19 / 1 / 0 | 19 / 1 / 0 |
| Availability clarification | seed-v2, 20 | 20 / 0 / 0 | 20 / 0 / 0 |
| Expanded 1 | expanded-v2, 60 | 53 / 6 / 1 | 55 / 3 / 2 |
| Expanded 2 | expanded-v2, 60 | 59 / 0 / 1 | 59 / 1 / 0 |
| Expanded 3 | expanded-v2, 60 | 55 / 3 / 2 | 59 / 1 / 0 |
| Expanded 4 | expanded-v2, 60 | grading review | grading review |

Q09’s question asked when an underbutler becomes available, but its initial fixed key only specified immediate Expended placement. A [fresh adjudicator](adjudication-01/report.json) identified that key omission and graded both answers partial. [seed-v2](seed-v2/question-bank.md) explicitly adds normal two-rotation availability and earlier refresh mechanisms. All question wording and all historical files remain intact; see [version corrections](benchmark-corrections.json).

Coverage expanded to 56 questions. The [first independent challenge](coverage-challenge-01.json) added four distinct gaps: no hand/discard limit; public/select-any Reserve; voluntary versus forced passing; separate refresh methods. The current [60-question bank](expanded-v2/question-bank.md), [questions](expanded-v2/questions.json) and [key](expanded-v2/answer-key.json) preserve the original IDs and wording, inheriting only the documented Q09 key correction. Earlier [56-question draft](expanded-v1/question-bank.md) is preserved and was never reader-tested.

Two new targeted source passes after accepting the four additions found no more qualifying rules. The [coverage/rejection ledger](coverage-ledger.json) maps procedural passages and exclusions; this is working saturation under the guide’s novelty rule, not enumeration of every conceivable game situation. The [second fresh coverage challenge](coverage-challenge-02.json) returned PASS, with no further distinct additions or material key corrections.

Independent source audits of successive snapshots [1](final-source-audit-01/source-audit.json), [2](final-source-audit-02/source-audit.json), [3](final-source-audit-03/source-audit.json), and [4](final-source-audit-04/source-audit.json) passed with no material errors or important omissions. Each fresh source auditor saw only its frozen summary and authoritative sources, including the narrow official localized clarification, and did not see questions, keys, reader responses or prior audits or author repairs. Further reader-led wording changes require a new audit and exact-text retest.

## Evidence

- [Initial input hashes](input-manifest.json), [preserved baseline](baseline/obsession.md), [source-reading log and PDF inspections](source-reading-log.json), [source with extraction line numbers](source-numbered.txt).
- [Seed-v1 bank](seed-v1/question-bank.md), [seed-v2 bank](seed-v2/question-bank.md), [all version corrections](benchmark-corrections.json).
- Iteration 1: [summary](seed-iteration-01/summary-snapshot.md), [reader A](seed-iteration-01/reader-a.json), [reader B](seed-iteration-01/reader-b.json), [detailed grades](seed-iteration-01/results.json).
- Iteration 2: [summary](seed-iteration-02/summary-snapshot.md), [reader A](seed-iteration-02/reader-a.json), [reader B](seed-iteration-02/reader-b.json), [detailed grades](seed-iteration-02/results.json).
- Seed passing iteration 3: [summary](seed-iteration-03/summary-snapshot.md), [reader A](seed-iteration-03/reader-a.json), [reader B](seed-iteration-03/reader-b.json), [detailed grades](seed-iteration-03/results.json).
- [Runtime model provenance and full intended prompts and encrypted-payload inspection-limit disclosure](model-provenance.json), [integrity checks](validation.json), [machine-readable progress](game-status.json). Each iteration retains its own frozen question copy, manifests, prompt files and raw output.

Readers use gpt-6-luna at high effort, forked without parent history and restricted by prompt to the frozen summary and questions only, with no rulebook/key/earlier answers/grades/web/prior-game knowledge. Actual models and effort are confirmed by local session metadata and turn contexts. Source, coverage and adjudication reviewers use gpt-6.1-sol at high effort. Context isolation is instruction-based, not an OS filesystem barrier.

The coordinator owns global semantic-audit recording, stamping and catalog regeneration. This chat will not mark its persistent goal complete until coordinator integration has been checked against exact tested bytes.

## Expanded grading and repairs (in progress)

Every expanded iteration uses the same complete expanded-v2 bank and key. Repairs clarify general source rules: family eligibility by gender; underbutler recruitment immunity; Fairchild genders and dismissal status; unchanged Market prices and reserve selection; multiple VP refreshes; recovered gentry’s same-turn use; named objective sets; last-player round advancement; and precise event/service timing.

Reader B’s first expanded run includes one factually correct answer relying on unstated Charles gender, separately flagged as unsupported. Correct ruling counts never override the final requirement for zero unsupported guesses.

Fresh [adjudication 2](adjudication-02/report.json) accepted iteration-2 B’s Q32/Q50 despite their partial support labels: the answers resolve the requested rulings, and their caveats concern literal wording only. A later [independent full grading audit](grading-audit-03.json) identified missing procedural details and explicitly distinguished requested facts from incidental key explanation. [Grading corrections](grading-corrections.json) preserve earlier grade JSON beside the corrected records. Iteration-2 B is therefore 59 correct/1 partial (Q02 marker advance), not the earlier provisional 60. Iteration-1 B’s Q44 is also partial for omitting the requested ordinary-rotation comparison. All raw responses and keys remain unchanged.

Expanded evidence: [iteration 1 grades](expanded-iteration-01/results.json), [iteration 2 grades](expanded-iteration-02/results.json), [iteration 3 grades](expanded-iteration-03/results.json). Each directory contains raw reader A/B output, exact snapshot, unchanged question copy, manifests, prepared and full intended prompts and encrypted-payload inspection-limit disclosure, runtime provenance and diffs.


## Coordinator-requested Q22 correction in progress

The apparent expanded-v2 iteration-7 full pass is superseded by the [fresh focused Q22 adjudication](coordinator-review-01/q22/adjudication.json). Its unqualified starting-reputation request requires Cavendish1.4 in each standalone answer. Expanded-v3 preserves every question and all other keys, adding that missing exception explicitly; all historical banks, raw answers and pre-correction grades remain preserved. Full60-question retesting and fresh source/coverage review are pending. Runtime task payload encryption is disclosed in [provenance interpretation](provenance-interpretation.json); environment-only captures are not recovered full dispatched prompts.
