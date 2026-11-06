# So Clover! — final stamped-version QA

Status: **ready-for-coordinator inspection**. Date: November 5, 2026 (America/Phoenix). BGG 329839. Canonical summary: [so-clover.md](../../../../../rules/so-clover.md).

Both NEW final **gpt-6-luna / high** readers answered the unchanged complete **20-question v3 bank** correctly: **20 correct, 0 partial, 0 incorrect, 0 unresolved, 0 unsupported guesses each**. A NEW fresh independent **gpt-6.1-sol / high** source auditor returned **PASS**, no findings, on the same exact summary bytes, including publisher metadata. Targeted validation is recorded in [stamped-validation.json](stamped-validation.json).

Final canonical, reader snapshot and audit SHA-256:

`4adc800dc4ccf01f4f35806f6f6b5f03f9c01f3fade31377c959840fd1b9b0c1`

The coordinator confirmed this managed-banner restamp was idempotent. The worker made no summary changes after that restamp. Earlier [README](README.md), reports, failed answers and grading revisions remain historical evidence; this report supersedes their completion and score claims where the grading corrections below apply. The persistent goal remains active until coordinator inspection is complete.

## Authority and scope

Gameplay authority is the complete six-page English Repos base-game rulebook, sc-en01, ©2020, assigned as the 2021 publication: [extraction](../../../../../extracted/so-clover-rules.txt), [PDF](../../../../../source_pdfs/so-clover-rules.pdf), [publisher PDF](https://cdn.svc.asmodee.net/production-rprod/storage/downloads/games/so-clover/sc-en01-rules-16197761427wP8d.pdf). Complete standard setup, Clue restrictions, both Resolution attempts, feedback, scoring, cleanup and endgame are included. Optional **Add a Challenge** remains explicitly excluded.

The rulebook omits player count and duration. The coordinator supplied an [official publisher capture](../../batches/2026-11-05-batch-002957/publisher-pages/so-clover-publisher-text.txt), preserved as a [local evidence copy](metadata-source/so-clover-publisher-text.txt), stating **3–6 players** and **30 min**. [Metadata supplement provenance](publisher-metadata-supplement.json) records its origin and hash. The final fresh auditor read the full capture and inspected the original publisher HTML’s English PDF link. Frontmatter now records `player_count: "3-6"`, `play_time: "30 min"`, `source_pdf: "so-clover-rules.pdf"`, and the official PDF URL in `source_url` with `source_type: "rulebook_pdf"` and `source_language: "English"`. The coordinator’s managed banner now links the source PDF.

This supplement adds metadata authority, not a new gameplay rule, exception or timing branch. It does not change the gameplay questions, answers, rulebook hashes, scope exclusion or saturation findings. No essential standard-rule source gap remains unresolved.

## Frozen bank and coverage

The original bank was written source-first before the new summary. [v1 questions](benchmark-v1/questions.json) and [key](benchmark-v1/answer-key.json) remain unchanged. Their original 20 entries are identical in the [complete v3 questions](benchmark-v3/questions.json) and [key](benchmark-v3/answer-key.json), as well as the final frozen copies. No question, expected answer or source-backed requested requirement was removed, softened or changed during repairs.

[Coverage map and rejection ledger](coverage-ledger.json) map all core standard procedural passages. Two consecutive targeted passes added zero questions before the [fresh independent source/key challenge](coverage-review.json). It confirmed all original20 keys, found no missing standard branch, and rejected proposed Q21 as the existing orientation requirement plus existing incorrect-card handling. Two subsequent passes again added zero. The [unaccepted v2 draft](benchmark-v2/questions.json) and [draft ledger](coverage-ledger-draft-v2.json) remain intact. Q21 was never reader-tested and was rejected for redundancy, not difficulty. Working saturation is 20 under the stated source and novelty rule, not a universal quota.

Read the [complete readable question/answer bank](question-bank.md).

## Grades, corrections and repairs

Each reader was freshly spawned with `fork_turns="none"`, explicitly requested Luna/high, and restricted to only its frozen summary and questions. No source, key, prior response, grade, review, parent history, browsing or prior game knowledge was allowed. Actual model/effort and distinct runtime identities are saved in [post-stamp model provenance](post-stamp-model-provenance.json); the final pair’s proof is [here](stamped-iteration-03/model-provenance.json). Fresh context and read restrictions were used; there was no separate filesystem sandbox.

| Iteration | Reader A correct / partial / incorrect | Reader B correct / partial / incorrect | Current grading evidence |
|---|---|---|---|
| Initial seed01 | 19 / 1 / 0 | 18 / 2 / 0 | [Additive corrected grades](corrected-historical-grades/seed-iteration-01-results.json) |
| Clarified roles seed02 | 19 / 1 / 0 | 19 / 1 / 0 | [Additive corrected grades](corrected-historical-grades/seed-iteration-02-results.json) |
| Pre-stamp final01 | 20 / 0 / 0 | 19 / 1 / 0 | [Additive corrected grades](corrected-historical-grades/final-iteration-01-results.json) |
| First stamped version01 | 19 / 1 / 0 | 20 / 0 / 0 | [Final requested-part grades](stamped-iteration-01/results.json) |
| Clarified preparation version02 | 20 / 0 / 0 | 20 / 0 / 0 | [Grades](stamped-iteration-02/results.json); superseded by metadata/restamp |
| Exact final metadata/restamp version03 | **20 / 0 / 0** | **20 / 0 / 0** | [Final full grades](stamped-iteration-03/results.json) |

Two genuine requested-part omissions drove presentation repairs: initial reader B’s Q11 said only “resolve” without explaining cooperative reconstruction, and several Q09 answers omitted placing the prepared board **in front of its owner**. The summary now states the reconstruction task explicitly and emphasizes the board location in both the preparation procedure and reference. It also names the source’s individual/team phases explicitly. These are general source-supported presentation clarifications, not an appended answer key.

The earlier grading overlooked Q09’s board-location requirement in five historical answers. Those answers now have additive corrected grades and lower scores, with original files preserved. [Historical grading corrections](historical-grading-corrections.json) identifies each changed grade and its basis. The original three iteration results and old README were not overwritten; all 73 artifacts in the original seal remain intact.

A provisional adjudication of stamped01 also treated the unasked Resolution/team label in Q02 as mandatory. That report and its [provisional literal-key grades](stamped-iteration-01/results-provisional-literal-key.json) remain intact. A separate NEW [blind bank-only grading-scope reviewer](grading-scope-review.json), given no summary, response, grade or prior finding, reviewed all20 question/key pairs and the guide/source. It confirmed the original standard: require every material part actually requested by the question, using the fixed key/source for the answer; do not add background requirements from elaborative key wording. It found **no benchmark correction required**. Thus Q02’s phase labels and Q08’s secrecy are source-backed background beyond those narrow asks, while Q09’s exact preparation expressly requires board location. This interpretation is applied uniformly, with no question/key changes and no credit borrowed from other answers. The actual Q09 omission remains a partial. A truthful first-Spectator selection-method caveat is likewise not an error because the rulebook specifies no special chooser or method.

The final03 evaluator inspected all40 answers separately against all requested parts and fixed source-backed answers, independently of support labels. Both explicitly supply the required Q09 board location. Neither has an unresolved selection caveat or missing reconstruction task. All240 raw answers from the six reader pairs are preserved, as are every snapshot, fixed question/key copy, hash manifest, source audit, repair diff and adjudication.

## Exact final source audit and validation

The [NEW final source audit](stamped-iteration-03/source-audit.json) checked 16 claim groups against the complete rulebook, Pair/verification diagrams and publisher metadata authority. It found no material error or important standard-rule omission. This auditor had authored no repairs and saw no questions, keys, reader outputs, grades, earlier audits or summaries. It treated the verification banner as an unaudited claim. Its exact summary hash matches the final pair and canonical file.

[Final validation](stamped-validation.json) verifies original sealed artifacts, original-entry preservation, frozen source/key/metadata hashes, every expected ID once per reader and grade list, grade-to-raw/key correspondence, totals, actual models/efforts and distinct new identities, final 20/20 scores, audit/snapshot/canonical equality, metadata-capture equality, and report links. Structural validation, source-based quality gate, targeted whitespace/diff checks and an isolated one-game index/manifest/strict catalog integration fixture pass. Shared catalogs, audit registries, instructions and scripts remain read-only for the worker. The first validation run flagged links to its own not-yet-created output; that [initial result](stamped-validation-initial-self-link.json) is retained. Rerunning after the output existed resolved those two self-links; no summary, bank, source, model check or catalog check failed.

Final evidence: [snapshot](stamped-iteration-03/summary-snapshot.md), [questions](stamped-iteration-03/questions.json), [key](stamped-iteration-03/answer-key.json), [input manifest](stamped-iteration-03/input-manifest.json), [raw A](stamped-iteration-03/reader-a.json), [raw B](stamped-iteration-03/reader-b.json), [all grades](stamped-iteration-03/results.json), [model metadata](stamped-iteration-03/model-provenance.json), [audit](stamped-iteration-03/source-audit.json), and [diff](stamped-iteration-03/summary-changes.patch).

This is a fixed-bank regression pass within the supplied standard-game scope. It is not a held-out accuracy study. The coordinator should inspect this exact-version evidence and update its shared audit/catalog records to the final hash without changing tested bytes; any further summary-byte change requires another complete fresh pair and matching audit coverage.
