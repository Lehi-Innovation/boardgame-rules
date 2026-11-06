# Pandemic summary QA — November 4, 2026

Local status: **complete**. Phase: complete. Coordinator recording, unchanged-byte stamping, catalog integration and completion checks are complete.

Scope: standard Pandemic, BGG 30549, the 2015 seven-role modern base booklet represented by the original 24,430-byte extraction. Legacy, expansions, puzzle/scenario mechanics and optional solo modes are excluded. Core difficulty levels and the optional experienced-group open-hand rule are included.

The complete fixed regression bank has **39 questions**. Read the [question and answer bank](benchmark-v4/question-bank.md), or use the separate [questions](benchmark-v4/questions.json) and [key](benchmark-v4/answer-key.json). The evaluator saw the original summary during source-first bank preparation; this was not a held-out evaluation. Keys were frozen before reader dispatch.

Final tested candidate SHA-256: `9e566dba69578343700872ae2f08512cf6881e81076e307afc9d0803874418d9`. The [final validation](final-validation.json) records the exact-byte comparison to the canonical summary.

## Results

Scores count fully correct answers; partial and incorrect counts remain separate. Every iteration used two fresh **gpt-6-luna/high** readers, with `fork_turns="none"`, frozen inputs, and the guide’s blind-reader restrictions. Readers had no source, key, earlier answers, grades or parent context. Runtime settings are [confirmed](runtime-provenance.json); context isolation was instruction-based, without stronger filesystem isolation.

| Iteration | Bank | Reader A: correct / partial / incorrect | Reader B: correct / partial / incorrect |
|---|---|---|---|
| [seed-iteration-01](seed-iteration-01/results.json) | benchmark-v1 | 11 / 9 / 0 | 9 / 10 / 1 |
| [seed-iteration-02](seed-iteration-02/results.json) | benchmark-v1 | 19 / 1 / 0 | 17 / 3 / 0 |
| [seed-iteration-03](seed-iteration-03/results.json) | benchmark-v1 | 19 / 1 / 0 | 19 / 1 / 0 |
| [seed-iteration-04](seed-iteration-04/results.json) | benchmark-v1 | 20 / 0 / 0 | 20 / 0 / 0 |
| [expanded-iteration-01](expanded-iteration-01/results.json) | benchmark-v4 | 37 / 2 / 0 | 36 / 3 / 0 |
| [expanded-iteration-02](expanded-iteration-02/results.json) | benchmark-v4 | 37 / 2 / 0 | 39 / 0 / 0 |
| [expanded-iteration-03](expanded-iteration-03/results.json) | benchmark-v4 | 38 / 1 / 0 | 36 / 3 / 0 |
| [expanded-iteration-04](expanded-iteration-04/results.json) | benchmark-v4 | 38 / 1 / 0 | 39 / 0 / 0 |
| [expanded-iteration-05](expanded-iteration-05/results.json) | benchmark-v4 | 39 / 0 / 0 | 38 / 1 / 0 |
| [expanded-iteration-06](expanded-iteration-06/results.json) | benchmark-v4 | 39 / 0 / 0 | 39 / 0 / 0 |

The original seed answers and wording stayed fixed across all four seed iterations. Source-backed repairs clarified action and cube destinations, face-down deck preparation, immediate eradication at cure discovery, cure-marker movement, continued infection after cure, Researcher transfer direction, hand-limit priority, and Dispatcher origin/consent rules. The incorrect main infection-rate table was repaired to 2/2/2/3/3/4/4, matching the already-correct reference table. Forecast now explicitly returns its cards to the deck top. See the [complete diff](summary-changes.patch) and individual repair patches in the [evidence index](evidence-index.md).

Grading required all predetermined material facts in each answer. No missing fact was borrowed from a different answer. Correct answers with partial support labels were accepted only when their complete content resolved the question. Independent Sol/high adjudication resolved disputed omissions and caveats; the [reports](evidence-index.md) preserve every decision. Seed iteration 3 remained 19/20 for both because the cure answer omitted continued infection, despite correct answers to that point elsewhere. The fourth pair passed 20/20 each.

Expanded iteration 3 deliberately retested the unchanged iteration-2 text because the omitted facts were already explicit; that failed run remains retained. Later formatting made numerical steps and hand-limit priority easier to scan. Expanded iteration 5 also added a [generic completeness instruction](reader-protocol-revision.json) asking procedural answers to state their amounts, costs, timing and destinations within each response. It disclosed no source, key, prior responses or findings; questions, expected facts and grading stayed fixed. Its results therefore also reflect that prompt instruction; no isolated summary-effect or model-equivalence claim is made.

## Coverage and stopping check

[Benchmark revisions](benchmark-revisions.json) preserve all earlier questions and answers: v1 seeded 20; v2 added 17 distinct procedures/branches; v3 added the two remaining core Event effects after source recovery; v4 made only the independently requested Q38 citation cleanup. Its question text, expected answers and material facts are unchanged from v3. Original entries and per-entry hashes are [retained](benchmark-entry-hashes.json).

The [procedural coverage map](procedural-coverage-map.json) maps the source to the bank. The [acceptance/rejection ledger](coverage-ledger.json) records all passes. After the final two Event additions, targeted passes 5 and 6 found zero meaningful additions. A fresh **gpt-6.1-sol/high** [coverage challenge](coverage-challenge.json), blind to summary and reader outputs, found all 39 answers supported and no meaningful omitted question. Its sole minor citation request was [resolved](coverage-resolution.json) in v4. This establishes working saturation for this source and novelty rule, not enumeration of every conceivable table scenario.

## Independent source audits

The first independent [source audit](source-audit-01.json) returned MINOR: Dispatcher consent needed to apply explicitly to both movement options. That was [repaired](source-audit-01-resolution.json). A different fresh **gpt-6.1-sol/high** [final auditor](final-source-audit-03.json), given only summary and sources and no questions/key/reader outputs, returned **PASS with zero findings**. It authored no repairs. [Byte linkage](source-audit-byte-link.json) proves its snapshot, the expanded-test snapshot and the canonical candidate are identical. The [earlier passing audit](final-source-audit.json) is retained for the text before expanded-test clarifications.

## Source evidence

The [source recovery notes](source-supplement.md) describe the exact scope, edition match and limitations. The [original input manifest](input-manifest.json) fingerprints the unchanged extraction and pre-edit summary. A [matching publisher PDF](matching-publisher-rules.pdf) and all eight page renders restore extraction omissions, particularly setup values, Direct Flight and the rate track. The newer `publisher-rules.pdf` recovery candidate is retained as history and was not used as authority.

Government Grant is supported only by the matching base-card reproduction on page 2 of the [official Event puzzle PDF](official-event-puzzle.pdf); expansion and puzzle mechanics are excluded. Forecast is supported by a [photo of the matching printed component](forecast-card-photo.jpg), corroborated by the [publisher component photo](official-components-2.webp). Its full text is third-party hosted; both independent source/coverage reviewers assessed the provenance and accepted this as printed component evidence, not seller-authored rules. Download URLs, SHA-256 hashes and the legacy publisher’s expired-TLS-certificate retrieval limitation are preserved in the provenance files.

## Validation and coordinator handoff

[Integrity validation](integrity-validation.json) checks frozen hashes, original entries, every expected ID exactly once, grades matching actual answers and the fixed key, and grade totals. [Repository validation](repository-validation.json) records current checks and retains historical intermediate catalog discrepancies. [Model provenance](runtime-provenance.json), saved runtime records and [reviewer provenance](reviewer-model-provenance.json) verify the actual requested models/effort. The [completion audit](completion-validation.json) maps the ten assigned requirements to their evidence and verifies coordinator integration.

The coordinator completed audit recording, targeted stamping, and registry/index/manifest integration. I inspected the saved [coordinator validation](coordinator-followup-01/integration-evidence/coordinator-validation.json), [iteration integrity check](coordinator-followup-01/integration-evidence/coordinator-iteration-check.json), [recording/stamping evidence](coordinator-followup-01/integration-evidence/recording-validation.json), and [publication checks](coordinator-followup-01/integration-evidence/publication-validation.json). My [integration checks](coordinator-followup-01/integration-checks.json) independently verify preservation of other manifest entries/index lines, current Pandemic entries matching regeneration, the recorded source verdict, and exact stamped/canonical/tested-byte equality. The final read-only catalog command passed for all 1666 summaries. Earlier catalog mismatches are historical only. No retest was required because stamping changed no bytes. This game chat changed no shared integration files and made no commit or push.

Every frozen summary, question copy, raw response, detailed grade, audit, model record, hash and diff is linked in the [complete evidence index](evidence-index.md). Machine-readable progress is in [game-status.json](game-status.json).
