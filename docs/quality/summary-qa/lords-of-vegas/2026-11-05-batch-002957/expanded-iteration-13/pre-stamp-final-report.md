# Lords of Vegas — Mayfair base summary QA

**Ready for coordinator review of the declared source-limits benchmark.** The persistent goal remains active until the coordinator accepts the qualification, completes stamping verification and authorizes completion.

The [canonical summary](../../../../../rules/lords-of-vegas.md) covers the original Mayfair 2010/2013 English 2–4-player base game. Only positively applicable base clarifications from the publisher’s previous-Mayfair unified book are included. Up!, Underworld, Americana, Con Jobs, the revised six-player edition and the optional Gamble Variant are excluded. Assigned sources remain unchanged.

## Certification scope and unresolved source limit

Final bank **expanded-v10** tests source knowledge, including accurate source limits. Its [independent source/key/coverage review](source-key-v10-review.json) returns `PASS_FOR_DECLARED_EXPANDED_V10_SOURCE_LIMITS_BENCHMARK`.

This is **not an unqualified pass for the earlier definite physical-actor target**. Q27 still asks who rolls after a trade creates a boss tie. The assigned books specify the affected dice and timing, but do not expressly assign the physical thrower of every free tie die. The summary and key state that limit; they invent neither an owner-only mandate, an anyone-may-roll permission nor a house convention. A definite mandatory physical actor remains unrecovered and would require applicable official clarification. The owner-specific roller instruction is expressly local to paid Reorganization. [Independent full-source actor review](tie-actor-source-review.json).

The original Q27 wording is retained. Its old unsupported mandatory-owner key is preserved in historical versions; the only baseline-record correction is explicitly recorded in [source-key-correction.json](expanded-v9/source-key-correction.json). All other old answer records and all question wording are preserved. [Earlier qualified rejection](source-key-v9-review.json) remains unchanged. The explicit benchmark-mode decision changes what is certified; it does not retrospectively recover the missing gameplay actor or convert earlier failures into passes.

## Reader results and repairs

Each pair comprised two NEW gpt-6-luna/high agents with `fork_turns=none`, answering the entire frozen bank. Counts below are original strict grades.

| Frozen run | Questions | A correct / partial / incorrect | B correct / partial / incorrect |
|---|---:|---:|---:|
| [seed-iteration-01](seed-iteration-01/results.json) | 20 | 19 / 1 / 0 | 20 / 0 / 0 |
| [seed-iteration-02](seed-iteration-02/results.json) | 20 | 20 / 0 / 0 | 20 / 0 / 0 |
| [expanded-iteration-03](expanded-iteration-03/results.json) | 35 | 34 / 1 / 0 | 34 / 1 / 0 |
| [expanded-iteration-05](expanded-iteration-05/results.json) | 38 | 36 / 2 / 0 | 37 / 1 / 0 |
| [expanded-iteration-06](expanded-iteration-06/results.json) | 38 | 36 / 1 / 1 | 37 / 1 / 0 |
| [expanded-iteration-08](expanded-iteration-08/results.json) | 39 | 37 / 0 / 2 | 39 / 0 / 0 |
| [expanded-iteration-09](expanded-iteration-09/results.json) | 39 | 37 / 0 / 2 | 38 / 0 / 1 |
| [expanded-iteration-11](expanded-iteration-11/results.json) | 39 | 36 / 0 / 3 | 39 / 0 / 0 |
| [expanded-iteration-13](expanded-iteration-13/results.json) | 39 | 39 / 0 / 0 | 39 / 0 / 0 |

The seed failure omitted the operational draw/acquisition/payout/discard sequence. [Independent adjudication](seed-iteration-01/q02-adjudication.json) confirmed Partial. The general turn overview was repaired, and a fresh pair passed the unchanged 20-question seed. [Repair diff](seed-iteration-02/summary-changes.patch).

Run03’s Q31 Partial demanded restating boss eligibility already supplied by the question. A [fresh scope adjudicator](expanded-iteration-03/q31-scope-adjudication.json) judged the actually asked trade outcomes Correct. Original strict grades remain unchanged; the scope correction was versioned before later testing.

Run05 retained genuine recipient, merger-outcome and discard omissions. [Independent case/scope adjudication](expanded-iteration-05/case-scope-adjudication.json) also identified two unasked background requirements and Reader A’s ambiguous recipient wording. Its [separate conservative view](expanded-iteration-05/adjudicated-results.json) is A 35/38 and B 37/38; it does not replace the strict grades.

Run06 retained a missing zero-point outcome, an extra-die interpretation and the physical-actor issue. The final summary explicitly states other investors’ zero casino points, explains that trading replaces the die at the existing tile rather than adding a second die there, and states the free-tie physical-actor source limit. A fresh pure source audit checked all revised bytes. The bank’s genuine source correction and added gambler-actor question were separately versioned before run08.

Run08 failed for Reader A: it explicitly awarded 2 points for a three-tile casino and described the same remaining Red 6 as rerolled and untouched. Correct general quotations did not cure those case errors. Reader B passed 39/39. Original strict failures are preserved. The summary and v10 bank did not change between run08 and run09; protocol v4 added recorded generic calculation/inventory checks for that fresh pair.

Run09 strict grades are A 37/39 and B 38/39. A’s correct object check was contradicted by extra-die prose; both readers denied an assigned Gamble roller despite the imperative procedure. These were material failures. The new summary explicitly names the acting gambler and explains conditional one-die transfer counts, including the supply-recycling exception. [Current repair diff](expanded-iteration-11/summary-changes.patch). A new pure source audit reviews these exact bytes.

Run10’s protocol-v5 dispatch was canceled before either reader produced an output because that text had been superseded by the canonical repairs. Frozen inputs, prompts, actual dispatch/runtime records and [cancellation disclosure](expanded-iteration-10/cancellation.json) are retained. No run10 score or pass is claimed. Run11 is a fresh full 39-question pair on the repaired current text.

Run11 strict grades are A 36/39 and B 39/39. A invented an initial highest-die ownership inconsistent with a non-boss given, contradicted its correct inherited-die check in the answer, and invented a concrete cost from pip values absent from that question. These material failures remain unchanged. Protocol v7 implements shared rendering with generic code and preserves unspecified inputs; it changes neither the summary nor fixed target. Snapshot12 was a preparatory v6 instruction freeze with no dispatch; run13 tested the full 39-question bank with the implemented generic renderer.

## Source audit and coverage

A NEW independent gpt-6.1-sol/high pure source auditor compares the complete original and unified source extractions and original native pages 1–4 plus unified physical pages 2, 5 and 16 against the current summary. Its current result is **PASS with zero findings**. It sees no questions, keys, reader answers or grades, authors no repairs and makes no agent/chat metadata reads. [Current independent audit](expanded-iteration-11/source-audit.json). Run13 and the canonical file are byte-identical to the fresh run11 auditor’s candidate. [Exact-byte carry-forward proof](expanded-iteration-13/source-audit-reuse.json). Earlier audits on different historical bytes remain preserved, but are not substituted for this current audit.

The bank grew from 20 to 39 through source-first design and independent challenges. Additions cover exhaustion/recycling, takeover states, immediate boss timing, interrupted/multiparty/end-card trades, initial player state and Banker role, directly asked Build/Sprawl eligibility, occupied ownerless Sprawl targets and the gambler as two-dice roller. Q36–39 ask conditions or actors not actually requested by earlier questions; scenario givens are not credited as independent coverage.

Parent passes **23 and 24** added zero after Q39. The final independent reviewer checked the complete sources and sanitized v10 questions, effective key, asked-scope map, freeze manifest and coverage ledger, without summary, reader, grade or metadata exposure. It confirmed the declared source-limits mode and no further qualifying source-supported procedural gap. [Coverage and rejection ledger](coverage-ledger-v10.json), [readable bank](expanded-v10/question-bank.md), [questions](expanded-v10/questions.json), [effective fixed key](expanded-v10/grading-key.json), [asked-scope map](expanded-v10/scope-map.json), [version history](bank-version-history.json).

Other explicit source silences are initial-roll ties and a final tie in both points and money. [Source-limit record](source-silences.json). No ruling was invented.

One intermediate reviewer accidentally read old grading-status metadata through `list_agents`. Its [NOT_PASS report and disclosure](coverage-reopen-final-review.json) are retained and excluded from final clean sign-off. Legacy scope history also included an old seed-performance note. Final v8+ source-review packets remove that history while preserving all source facts and earlier frozen versions. [Packet hygiene](source-review-packet-hygiene.json). Final pure source audit, source/key reviewer, readers and graders have no metadata-reading exposure; outbound progress to the parent is distinguished from metadata reads in [independence checks](independence-tool-check.json).

Expanded snapshots 01, 02, 04 and 07 were preparatory freezes with no reader dispatch or claimed scores. Actual expanded reader runs are 03, 05, 06, 08, 09, 11 and 13. Snapshot11 is the current pure-audit target; snapshot13 is the byte-identical final reader target. Snapshot12 was an untested method freeze, not a reader run. All historical reports and raw responses remain preserved.

## Reader and grading method

Final reader protocol **v7** is prebound and identical apart from output path. Readers receive only the frozen summary and questions as rules data. Generic instructions require full governing heading units, explicit rulings for each asked clause, requested participant/outcome tables including zero results, and tracking each object through replacement without double counting. V4 records arithmetic expressions and before/change/after object inventories. V5 instructed readers to reuse one verified structured result; the retained run11 failures show that prose instructions alone did not ensure compliance. [Method decision](reader-protocol-v5-decision.json). These are rule-agnostic instructions with no failed IDs, key facts, old answers, grades or case hints. The optional extraction helper was reviewed but not embedded or used. V7 embeds a separate fact-free rendering function directly in the identical prompts to construct all repeated result fields from one independently checked result. It supplies no game facts or case answers. The instructions require needed givens/consequences and preservation of unspecified attributes. All 78 final entries pass shared-result equality checks. Reader A repeats its full result in checked_inputs instead of isolating minimal givens; that format limitation is preserved, with every substantive field still graded. [Unmodified reader self-notes and disposition](expanded-iteration-13/reader-self-notes.json). [Current method decision](reader-protocol-v7-decision.json).

Each text input was delivered in bounded contiguous character slices and checked against actual model-visible tool outputs, rather than inferred from line counts. Final readers use <=5000-character chunks; source reviewers use <=4800. Two historical readers mislabeled valid UTF-8 byte slices as character slices. Their original receipts are preserved; exact decoded source coverage is independently verified from pre-save tool outputs, and v4 explicitly requires Unicode slicing. [Protocol decision and disclosure](reader-protocol-v4-decision.json). Full delivery, requested/actual model and effort, fresh context and dispatch proof are retained in [runtime provenance](runtime-provenance.json), [dispatch provenance](dispatch-provenance.json) and [final model provenance](expanded-iteration-13/model-provenance.json). Only sanitized identity/task/model/effort/timestamp/path/record/hash proof is retained from external runtime logs.

Historical run03 B had one missing space in its prompt. Both readers received the same immediate technical correction; original texts remain preserved and are not claimed literally identical. Later pairs, including final run13, are literally identical after normalizing only the output filename.

Two fresh gpt-6.1-sol/high graders assess disjoint Q01–20 and Q21–39 blocks for both final readers. Bundles preserve all raw answer fields through a reversible quote dictionary with exact reconstruction/hash checks. Run09 graders used zero-based fact indexes; original reports retain them unchanged, and aggregation normalizes only proof-pair indexing after checking exact fixed fact text. Every one of 99 required-fact records is assessed once per reader. Same-entry complete quotations may supply ordinary lookup rules; concrete case results/calculations must be resolved. Equivalent expressions are accepted, factual omissions remain failures, and no fact is borrowed from another answer. [Original grader reports and aggregated results](expanded-iteration-13/results.json), [fact/ID validation](expanded-iteration-13/grading-validation.json).

This is a known fixed-set, tool-assisted regression with source-coverage saturation, not a held-out accuracy claim or proof that every imaginable scenario is enumerated. Context isolation relies on fresh agents and instructions in a shared workspace, not a separately restricted filesystem.

## Integrity and coordinator handoff

Final summary SHA256: `60000c000b4c9a54d5b80c617788cd905c12e024be26fffa68bc9cbde1710ae7`.

[Validation](validation.json) checks assigned source and seed integrity, all historical prefixes with the single declared Q27 source correction, frozen inputs, raw response and grade correspondence, every question/fact once, verbatim excerpts, actual complete delivery, actual models/efforts, independent qualified coverage verdict, audit exact-byte reuse, targeted structural validation and whitespace. [Final raw-response manifest](expanded-iteration-13/raw-response-manifest.json).

The worker wrote only the assigned summary and unique evidence directory. It did not commit, push, change branches/worktrees, edit shared catalogs/instructions/registries or stamp the verification banner. The coordinator owns acceptance of the declared benchmark qualification, audit recording, catalog registration and stamping. If stamping changes summary bytes, that exact version requires a NEW full 39-question pair and fresh pure source audit. The persistent goal remains active pending coordinator verification and authorization.
