# Ark Nova summary QA — in progress

The accepted coverage bank now has **95 questions**. Iteration05 finished at A 92 correct / 2 partial / 1 incorrect and B 94 / 0 / 1 after fresh independent semantic adjudication. Iteration06 finished at A 94 correct / 1 partial / 0 incorrect and B 93 / 1 / 1 after independent scope adjudication. Iteration07 finished at A94 correct /0 partial /1 incorrect and B92 /3 /0 after independent scope review. Two NEW clean readers are running iteration08 on the clarified snapshot with generic named-alternative promptv5. **No full-bank reader pass or coordinator readiness is claimed.** A new final-only source audit will begin only after the same full-bank pair passes. The persistent goal remains active through coordinator integration.

Current machine-readable progress: [game-status.json](game-status.json). Earlier report text is preserved in [report-history](report-history/README-before-expanded05-review.md).

## Sources and scope

This run covers original English base main rulebook **v1.2**, base glossary, official base FAQ, and the separately accepted official base Icon Overview. Optional solo mode, Marine Worlds, promos, map packs and the strategy guide are excluded. The coordinator upgraded the former v1.0 extraction before this run; that historical extraction remains in batch source discovery.

[Initial fingerprints](input-manifest.json), [original summary](original-summary.md) and the [neutral source manifest](neutral-source-manifest.json) preserve provenance. All seven accepted raw sources retain their hashes. The main rulebook has 20 pages, glossary 8, FAQ 3 and Icon Overview 2. Original publisher component photos narrowly supplement obscured Animals II numeric cells and tiny board numerals; English prose controls. Rejected strategy-guide downloads remain history, without authority. The source text has **1,898 logical lines but 1,897 LF characters**: its final unterminated line is only spaces and page-number footer 3. [The same-reviewer EOF supplement](coverage-challenge-06/eof-completeness-supplement.json) preserves and qualifies earlier line-count claims; future source auditors must inspect true EOF.

[Component-source checks](table-source-check/followup-source-report.json) and [board/icon checks](table-source-check/reputation-map-source-report.json) retain source images and narrow identity evidence. No obscured printed value is invented: the Aquatic Breeding middle condition remains unreported because a cube hides it.

## Coverage and frozen bank

The initial 20-question seed was frozen before reader dispatch. The author had already read the summary and sources while designing it. The expansion began at 132 draft questions and underwent independent source-first challenges and novelty adjudication. Distinct rule/outcome/timing/priority/exception branches earn question credit; numerical variants, renamed examples and mechanical recombinations do not. Printed lookup facts remain available without inflating the question count. All retired questions, keys and earlier versions remain intact.

[Revision07](coverage-revision-07/sealed-manifest.json) is accepted at **95 active questions, 233 passage records and 42 lookup records**. It includes two terminal author zero-addition passes. [Fresh source-first challenge07](coverage-challenge-07/) reviewed all raw sources before the bank; [same-reviewer delta acceptance](coverage-challenge-07/final-acceptance.json) accepts the exact final mapping and scope qualifications. This is a fresh full review followed by a delta verification, not a second fresh context.

The coordinator has formally accepted these final95 coverage and clean-payload proofs: [coverage review](../../batches/2026-11-04-batch-231507/ark-nova-final95-coverage-coordinator-review.json) and [final runtime check](../../batches/2026-11-04-batch-231507/ark-nova-final95-coverage-final-runtime-check.json). These records remain outside the blind-reader and final-only-auditor inputs.

The earlier 94-question stopping claim was reopened when the independent reviewer found an unasked branch: if nobody reaches 10 conservation before game end, all players discard one Final Scoring card before end-game scoring. Q20's key contained that context, but its question did not ask it. New **Q141** asks that distinct timing branch. All original 94 question/key/fact objects remain exact, and no tested question was dropped or weakened. Revision07 only corrects passage-to-question scope for contextual placement clauses in Q98/Q99. [Scope qualifications](coverage-revision-07/scope-qualifications.json) make those limits explicit without rewriting factual keys.

[Benchmark-v3](benchmark-v3/benchmark-freeze-manifest.json) freezes all 95 questions and accepted keys. Original20 question objects are unchanged. Four explicit source/key corrections remain separately versioned and preserved:

- [SC01](source-key-correction-SC01.json): Q17 release size bands are 2− / 3 / 4+, rather than literal exact integers.
- [SC02](source-key-clarification-SC02.json): remove eligible special-enclosure tokens when possible; standard housing is only the fallback. [Seed08 raw-answer check](SC02-retrospective-seed08-check.json) confirms both historical answers already directed this mandatory priority.
- [SC03](source-key-correction-SC03.json): draft Q133 permits up to two Digging choices.
- [SC04](source-key-precision-SC04.json): draft Q116 names Map5's Reptile House / Large Bird Aviary alternatives.

The current [grading scope index03](grading-request-scope-03.json) is evaluator-only. It distinguishes requested parts, given conditions and accurate extra context; actual question wording controls. Missing requested parts are partial, material false volunteered rules incorrect, and source-correct unsupported guesses cannot pass. Ordinary logical entailment and clear procedure shorthand are accepted. Support labels do not independently determine grades. Missing facts are never borrowed from another answer.

## Executed reader trials

Every executed pair uses two new history-free **gpt-6-luna / high** readers, with fresh `fork_turns=none` requested. Readers may use only the exact frozen summary and questions. All raw outputs, intended prompts, initial grades, adjudications, failed runs and detailed raw/key-linked results remain preserved. Prepared-only directories are not counted as executed trials.

| Seed iteration | A correct / partial / incorrect | B correct / partial / incorrect |
|---|---|---|
| 01 | 13 / 5 / 2 | 13 / 5 / 2 |
| 02 | 19 / 0 / 1 | 19 / 0 / 1 |
| 03 | 20 / 0 / 0 | 19 / 1 / 0 |
| 04 | 20 / 0 / 0 | 19 / 1 / 0 |
| 05 | 20 / 0 / 0 | 18 / 1 / 1 |
| 06, legacy key; incomplete delivery | 19 / 1 / 0 | 18 / 2 / 0 |
| 07, corrected v1.1 key | 20 / 0 / 0 | 18 / 1 / 1 |
| 08, corrected v1.1 key | 20 / 0 / 0 | 20 / 0 / 0 |

Seed01 independent adjudication supersedes preliminary parent counts without deleting them. Seed08 has complete actual-read/truncation-recovery evidence and fresh borderline adjudication. Its later SC02 raw check does not rewrite historical grades. Seed07/08 did expose a version label saying source-correction-01, without descriptive correction facts; [historical metadata audit](historical-seed-reader-metadata-audit.json) discloses this limitation. The clean final full bank repeats all original20.

| Expanded iteration | N | A correct / partial / incorrect | B correct / partial / incorrect | Status |
|---|---|---|---|---|
| [01](expanded-iteration-01/results.json) | 94 | 88 / 6 / 0 | 88 / 5 / 1 | Invalid final blind boundary: descriptive correction metadata exposed to both readers |
| [02](expanded-iteration-02/results.json) | 94 | 91 / 1 / 2 | 89 / 5 / 0 | Clean complete inputs; failing content |
| [03](expanded-iteration-03/results.json) | 94 | 92 / 1 / 1 | 94 / 0 / 0 | Clean complete inputs; A misses next ordinary turn and misstates Sponsor reward |
| [04](expanded-iteration-04/results.json) | 94 | 91 / 1 / 2 | 94 / 0 / 0 | Clean complete inputs; A misstates two Sponsor effects and leaves target floor unresolved |
| [05](expanded-iteration-05/results.json) | 95 | 92 / 2 / 1 | 94 / 0 / 1 | Clean complete inputs; A omits two parts; both volunteer a false statement |
| [06](expanded-iteration-06/results.json) | 95 | 94 / 1 / 0 | 93 / 1 / 1 | Clean complete inputs; icon omission, explicit zero-case uncertainty and false volunteered Pilfering target |
| [07](expanded-iteration-07/results.json) | 95 | 94 / 0 / 1 | 92 / 3 / 0 | False volunteered building exclusion; project/Multiplier omissions and ambiguous target floor |
| 08 | 95 | Pending | Pending | Two NEW readers running; unchanged95 bank, generic promptv5 |

[Expanded01 actual boundary trace](expanded-iteration-01/reader-metadata-boundary-trace.json) proves both readers saw the author bank's SC01/SC02 description. It is diagnostic only. Separate clean reader-only payloads preserve every question object: [r01 sanitation](reader-payload-sanitation-01.json) for 94 and [r02 sanitation](reader-payload-sanitation-02.json) for 95. Their metadata contains only game, neutral scope and opaque version. Readers never receive evaluator scope indexes, keys or source reports.

Prompt evolution is recorded in [reader-prompt-versions.md](reader-prompt-versions.md): v1 generic self-check, v2 complete bounded input reading, v3 standalone complete answers, v4 separate numbered clauses for requested parts; v5 explicitly resolves named alternatives and qualifier scope. Each adds only generic evaluation guidance, without question IDs, rule facts, prior findings or answers. Exact intended templates are saved before each dispatch.

[Expanded05 actual input proof](expanded-iteration-05/input-access-validation.json) matches visible tool outputs to every line of the 644-line summary and 387-line question file. Reader A's one truncated chunk was fully reread. [Clean boundary proof](expanded-iteration-05/reader-boundary-validation.json) confirms opaque r02 metadata and no forbidden feedback. [Expanded06 input proof](expanded-iteration-06/input-access-validation.json) directly matches all659 summary lines and387 question lines to actual visible text, with full read-output traces retained. Reader B’s truncated161–320 range was fully recovered. All other commands were inspected for knowledge access. [Expanded07 input proof](expanded-iteration-07/input-access-validation.json) directly matches all665 summary and387 question-file lines to actual visible text, with both readers’ truncation recovery and full read traces preserved. Earlier per-iteration proofs retain their own exact ranges and recovery evidence.

## Source audits and repairs

[Preflight audit](preflight-audit/preflight-source-audit.json) found two major and four minor omissions on its historical snapshot. It is supporting evidence, not the final-only audit.

[Final-only audit01](final-source-audit-01/report.json), from a new raw-only Sol/high context, failed with two minor omissions: Pack and illustrated project values. Its [source clarification](final-source-audit-01/source-evidence-clarification.json) withdraws an unproven Aquatic middle threshold. [Repairs](source-audit01-repairs/repair-record.json) add Pack, visible table values and correctly typed Reptile Breeding rewards. Independent review gives those ordinary printed-data clusters no extra question credit.

[Final-only audit02](final-source-audit-02/report.json) **passed only its archived expanded02 snapshot**, SHA256 `27e24bc5fed7016f3616c44a126eed947f789ea05364622d738677350e4c9f0a`. Its independent auditor received only exact snapshot, raw sources and neutral identity/hash provenance. Later canonical clarity/layout changes require a new audit. No prior audit pass is claimed for current bytes.

Repairs preserve before/after snapshots and diffs. [Expanded02 clarity](expanded02-clarity-repairs/repair-record.json) and [layout refinement](expanded02-clarity-repairs/layout-refinement/repair-record.json) clarify placement, icons, income and effect timing. [Sponsor-reference clarity](expanded04-sponsor-reference-clarity/repair-record.json) separates all 48 Sponsor entries by card and phase, preserving 46 effect strings exactly and clarifying the already sourced Diversity Researcher money award and Okapi payment direction. No tested questions or factual keys change to rescue reader failures.

[Iteration05 semantic review](expanded-iteration-05/fresh-semantic-adjudication.json) preserves all initial grades and corrects scope deductions beyond actual questions. Its [same-reviewer factual-input supplement](expanded-iteration-05/fresh-semantic-fact-input-supplement.json) corrects an authorized filename typo and confirms no verdict changes. [Procedural layout repairs](expanded05-action-layout-proposal/repair-record.json) separate existing animal housing, project and Sponsors II steps and repeat the existing five-appeal floor locally in Pilfering. All95 question/key/fact objects and promptv4 remain unchanged.

[Iteration06 clarity repairs](expanded06-reference-clarity-proposal/repair-record.json) explicitly name terrain-icon requirements on Animal and unique-building Sponsor cards and state the direct all-zero-conservation Pilfering consequence. The source packet and95 question/key/fact objects remain unchanged. All initial06 grades/raw-linked exports and same-reviewer scope supplements are retained.

[Iteration07 repairs](expanded07-procedure-clarity-proposal/repair-record.json) repeat existing project-card source access beside the project procedure, emphasize fulfillment of the printed condition, split Multiplier rules into labeled bullets, and explicitly identify Side Entrance as a unique building that qualifies for kiosk income. [Promptv5 delta](prompt-v5-change-record.json) changes only generic named-alternative output guidance and iteration paths; it adds no rule, question ID, prior finding or answer. Existing95 question/key/fact objects remain exact.

The next final-only auditor will be a new Sol/high/none context after a complete passing reader pair, receiving only that exact snapshot, the seven raw sources and neutral manifest. It will receive no banks, reader answers/grades, prior reports, repair history or expected findings. Any subsequent body or verification-stamp byte change requires the authorized exact-byte validation sequence before completion.

## Provenance and integration

[Runtime provenance](runtime-provenance.json) preserves actual model/effort and empirical tool accesses. [All30 reader identity checks](provenance-reader-identity-correction-02/verification.json) confirm exact reader agent identities and actual Luna/high execution. An earlier metadata helper accidentally matched grader agent suffixes; preserved generated artifacts and the explicit correction record distinguish that bookkeeping defect from unchanged reader execution.

Host parent session logs encrypt task-message bodies. Exact intended plaintext templates are preserved, but encrypted messages are **not recovered plaintext** and child environment-only messages are not dispatch recovery. [Label correction](provenance-label-correction-01/correction-record.json) retains historical mislabeled files and accurately distinguishes intended templates, ciphertext dispatch records, actual runtime and public input/output traces. No unsupported plaintext prompt hash-match is claimed. [Descriptive payload-label clarification](reader-payload-version-label-clarification.json) preserves old evaluator-only manifests that said r01 despite actual r02 delivery; the delivered files, neutral metadata and complete visible-read proofs were correct and remain unchanged.

[Validation](validation.json) checks preserved originals, all accepted source hashes, separately versioned key corrections, benchmark freezes, raw/key/result linkage, reader runtime and input evidence. Structural validation and whitespace checks are rerun when canonical changes. This worker owns only `rules/ark-nova.md` and this QA directory; shared registries, verification stamps, commits and integration belong to the coordinator.

The goal stays active until explicit coordinator integration completion. Local readiness will be reported through `game-status.json`; it does not mean batch completion.
