# So Clover! — ready for coordinator

QA date: November 5, 2026 (America/Phoenix). BGG **329839**. Canonical summary: [rules/so-clover.md](../../../../../rules/so-clover.md).

The new standard-game summary passes the complete **20-question** regression bank with two fresh **gpt-6-luna / high** readers, each **20 correct, 0 partial, 0 incorrect, 0 unresolved, 0 unsupported guesses**. A fresh independent **gpt-6.1-sol / high** auditor returned **PASS** on the exact final snapshot, with no findings. Targeted structural, quality, evidence-integrity and isolated catalog checks passed.

Status is **ready-for-coordinator**, pending the coordinator’s audit recording, catalog integration and verification stamping. The persistent goal remains active. No shared registry, catalog, instruction, audit registry or script was edited. No commit, push, worktree or additional sidebar chat was created. If stamping changes the summary bytes, its new text requires another complete fresh-reader pair and audit coverage before completion.

## Source and scope

Authority is the supplied six-page English Repos base-game rulebook, 2021 publication, sc-en01, copyright 2020: [extracted source](../../../../../extracted/so-clover-rules.txt), [local PDF](../../../../../source_pdfs/so-clover-rules.pdf), [publisher source URL](https://cdn.svc.asmodee.net/production-rprod/storage/downloads/games/so-clover/sc-en01-rules-16197761427wP8d.pdf). Standard setup, all clue constraints, both resolution attempts, scoring, cleanup, progression and endgame are included. **Add a Challenge** is intentionally excluded. Player count and duration are not printed in this booklet; frontmatter records that limitation instead of inventing source support.

The evaluator read the complete source before writing the initial bank or summary, then visually inspected PDF pages 2, 4 and 5 for Pair geometry and card-verification orientation. [Source references](source-references.md) and [source baseline copy](baseline/so-clover-rules.txt) preserve the evidence. There is no essential unresolved source gap for the assigned standard-play scope. Cases the source does not regulate were rejected rather than assigned invented rulings.

## Bank and coverage

Read the [complete questions and answers](question-bank.md), [questions JSON](questions.json), [fixed key](answer-key.json), [coverage map and rejection ledger](coverage-ledger.json), and [fresh independent coverage/key challenge](coverage-review.json).

The initial [v1 seed bank](benchmark-v1/questions.json) and [key](benchmark-v1/answer-key.json) were frozen source-first, before the summary existed. All original IDs, wording and answer entries remain identical in the [v3 complete bank](benchmark-v3/questions.json) and [key](benchmark-v3/answer-key.json). No source or key correction was needed.

Targeted expansion attempted to find new binding rules, distinct outcomes and consequential timing/exception interactions. The fresh reviewer confirmed that Q01–Q20 already cover all core standard procedures and key branches. The six-page source did not support a qualifying addition under the strict novelty rule; twenty was not used as a cap.

| Coverage pass | Focus | Accepted additions |
|---|---|---:|
| 1 | Setup, Clues, transition, reconstruction and verification diagram | 0 after independent novelty review |
| 2 | Scoring timing, silence, destinations and outcome branches | 0 |
| 3 | Every core passage, boundaries, supply and endgame | 0 |
| Independent challenge | Complete source and key; no summary or reader outputs | 0 |
| 4 | Re-read source/map after challenge; timing and branch novelty | 0 |
| 5 | Setup, permissions, geometry, attempts, destinations and end | 0 |

Pass 1 proposed a direct wrong-orientation verification question, Q21. It is source-supported, but the independent reviewer rejected it as a mechanical recombination of Q12’s orientation requirement and Q16’s incorrect-card feedback. The unaccepted, never-reader-tested [v2 candidate bank](benchmark-v2/questions.json), [key](benchmark-v2/answer-key.json), [original draft ledger](coverage-ledger-draft-v2.json) and [status/hashes](benchmark-v2/input-manifest.json) remain intact. This was a novelty correction before final testing, with no removal of an original or failed reader question. Two consecutive zero-addition passes preceded the independent challenge; two more confirmed its result. This establishes working saturation under the supplied source and novelty criteria.

## Reader results and repair

Every reader was newly spawned with `fork_turns="none"`, explicit `gpt-6-luna` and `high`. Each was instructed to read only that iteration’s frozen summary and questions, excluding sources, keys, prior responses, grades, reviews, parent history, browsing and prior game knowledge. Isolation was by fresh context and read restrictions; no separate filesystem sandbox was imposed. Actual model and effort were confirmed from local session metadata/turn contexts in [model provenance](model-provenance.json).

| Iteration | Bank | Reader A correct / partial / incorrect | Reader B correct / partial / incorrect |
|---|---|---|---|
| [Initial](seed-iteration-01/results.json) | v1, 20 | 20 / 0 / 0 | 19 / 1 / 0 |
| [Clarified roles](seed-iteration-02/results.json) | unchanged v1, 20 | 20 / 0 / 0 | 20 / 0 / 0 |
| [Complete-bank final test](final-iteration-01/results.json) | v3, original 20 unchanged | **20 / 0 / 0** | **20 / 0 / 0** |

Initial reader B’s Q11 merely said the other players “resolve” the board, omitting the requested cooperative reconstruction task. [Independent adjudication](seed-iteration-01/adjudication-q11-b.json) retained the partial; it did not borrow the missing facts from that reader’s Q12. The [summary repair diff](seed-iteration-02/summary-changes.patch) makes the other players’ task explicit in Turn Structure, using the general source-supported rule. No rules or question-specific answer list was added.

Some readers accurately noted that the source does not specify a first-Spectator selector or selection method. This caveat does not negate the correct instruction to choose the first Spectator. The clarified pair’s [independent adjudication](seed-iteration-02/adjudication-q11.json) and final reader B’s [fresh adjudication](final-iteration-01/adjudication-q11-b.json) found every requested fact complete. Their self-reported `partial` support labels were not treated as grades. This differs from the actual initial omission, which remains a failure in the historical results.

The evaluator inspected every requested part of all **120** answers against the unchanged source-backed entries, accepting equivalent wording but retaining omissions. Per-question records include original question, expected and observed answer, source references, summary evidence, grade and reason. No missing answer was filled from another answer, and no guessed fact replaced summary support.

## Independent source audits

[Audit 01](source-audit-01.json) passed the initial summary. [Audit 02](source-audit-02.json) independently rechecked the clarified version. A separate fresh final auditor, with no access to either earlier summary/audit, questions, keys, responses or grades, then checked only the exact [final snapshot](final-iteration-01/summary-snapshot.md) and complete source. Its [final source audit](final-iteration-01/source-audit.json) is **PASS**, with no findings and 20 checked claim groups. All auditors and reviewers ran on confirmed gpt-6.1-sol / high.

Final summary SHA-256:

`364b464f7ea8fba8b2a7a04fc142e1f0a28f66f0925b164ad62b8522c99aa962`

The final reader snapshot, final auditor’s input and canonical summary have identical bytes. It also matches the passing clarified seed snapshot.

## Validation and retained evidence

[Final validation](validation.json) confirms source/input hashes, original-entry preservation, every expected ID exactly once per reader and grade array, saved grade/answer/key correspondence, model settings, complete final scores, audit hash, unchanged final inputs, canonical/snapshot equality and report links. [Run input manifest](input-manifest.json) preserves original and final fingerprints. Benchmark manifests and every iteration manifest preserve their own input hashes.

- `scripts.validate rules/so-clover.md`: PASS.
- Targeted `check_quality` against the assigned extraction: PASS, no issues.
- Isolated one-game index/manifest/strict catalog fixture under `targeted-validation/catalog-fixture`: PASS, no errors. This exercises integration using only the assigned game, without rewriting shared files or claiming the live catalog was regenerated.
- Targeted `git diff --check` and explicit Markdown whitespace check: PASS.
- [Final raw reader A](final-iteration-01/reader-a.json), [raw reader B](final-iteration-01/reader-b.json), [all final grades](final-iteration-01/results.json), [frozen inputs](final-iteration-01/input-manifest.json), [model evidence](final-iteration-01/model-provenance.json) and [iteration validation](final-iteration-01/validation.json) are retained.
- Failed initial responses, both earlier snapshots, their diffs, adjudications and audits remain in their original directories.

This is a pass on the fixed regression bank for the supplied standard-game edition and scope. It is not a held-out accuracy study or a claim to enumerate every conceivable table question.
