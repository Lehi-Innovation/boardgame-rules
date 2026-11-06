# Nemesis summary QA — awaiting authoritative source rulings

**Status: `awaiting-source`. No complete PASS and no batch-completion claim.** The final 108-question pair scored **106 correct / 2 partial / 0 incorrect** and **103 correct / 5 partial / 0 incorrect**. Both have zero unsupported guesses. The exact final summary passes an independent audit for **source-supported fidelity**; four unresolved source cases prevent unconditional core completeness. The remaining reader omissions also mean the two-reader 108/108 completion criterion is unmet.

This run began **4 November 2026** and continued **5 November 2026**, America/Phoenix. All work is under this unique run directory and the assigned [canonical Nemesis summary](../../../../../rules/nemesis.md). Shared registries, catalog/index files and trust stamping were not edited by this chat.

## Source and scope

Included: original Nemesis base game, basic board, standard semi-cooperative core, with Captain/Pilot/Scientist/Scout/Soldier/Mechanic. The complete [original extraction](source-snapshot.txt) was read and fingerprinted before repairs. Its canonical source file remains unchanged. A matching 28-page [manual PDF](nemesis-original-rules.pdf) was recovered under this directory; [provenance](source-provenance.json) records the download and edition evidence. The PDF was checked for action-cost/die/crafting symbols and text omitted from the extraction, especially the page-25 Nest/Slime Search prohibitions. [PDF/extraction differences](pdf-extraction-differences.json) are retained.

At the coordinator's direction, the current [official FAQ PDF](nemesis-current-official-faq.pdf) was downloaded from Awaken Realms and added as supplemental authority for its base-game Rules/Actions/Rooms/Items sections. Although its filename says v2.1, its actual cover says **v2.2, 16 April 2025**. The current-host and legacy-host downloads are byte-identical; see [current FAQ provenance](current-faq-provenance.json) and [extracted FAQ](current-official-faq-extraction.txt).

Excluded: solo, fully cooperative, playing as an Intruder, alternative-board and campaign procedures; Aftermath, Carnomorphs, Voidseeders and other expansions. In the FAQ this excludes cooperative Rules 17–18 and cooperative subcases, Intruder-player Actions 16, and expansion pages 5–6. Individual component effects not reproduced in the manual/FAQ remain printed-card dependencies; no card text was invented.

## Four precise source blockers

The [source-gap record](source-gaps.json) gives the exact passages and needed clarification. Independent [coverage review](coverage-review-v7.json) and [final source audit](full-iteration-05/source-audit.json) confirm that the official FAQ does not expressly settle these cases.

| ID | Missing ruling | What would resolve it |
|---|---|---|
| SG01 | Another Adult must appear while all eight Adult models are already in Combat; the procedure can free only non-Combat Adults. | An original-game publisher/designer ruling on this exact model-exhaustion state. |
| SG02 | Queen development adds an Egg after the Nest was marked destroyed; the persistence/reset of Nest destruction and Objective result is unstated. | An official ruling on newly generated Eggs after Nest destruction. |
| SG03 | The Egg Melee exception ends “if they miss”; Contamination on a successful Egg Melee is not separated unambiguously. | An explicit original-game ruling for a successful Egg Melee. No refund, delayed draw or unconditional immunity is invented. |
| SG04 | Dedicated rules say first death unlocks Pods; the Pod overview says any death. Later death after manual relocking is not expressly reconciled. | An official later-death/relocked-Pod clarification. First-death-only is the strongest detailed-rule reading, but the discrepancy is retained. |

FAQ Rules 25 addresses repeated yellow Self-Destruct spaces, not later Character deaths. FAQ Rooms 9 addresses a dropped Egg's contribution to Nest hit points, not Queen generation after destruction. FAQ Rules 19 addresses reusable tokens, not an available Adult miniature.

The coordinator explicitly instructed preserving these as blockers and completing all possible-source QA before this handoff. The goal was active at the initial handoff. After two automatic continuations revalidated the same unchanged blockers, the persistent goal was marked **blocked**, not complete, on 5 November 2026. The [blocked audit](goal-blocked-audit-2026-11-05.json) records the three-turn threshold and remaining dependencies. No publisher or designer was contacted.

## Question-bank growth and preservation

Read the [108-question and answer bank](benchmark-v7/question-bank.md), [questions only](benchmark-v7/questions.json), and [fixed key](benchmark-v7/answer-key.json). The evaluator saw the original summary when selecting questions; this is not a held-out test.

| Version | Questions | Change |
|---|---:|---|
| v1 | 20 | Predetermined seed questions/key frozen before either reader. |
| v2 | 53 | Remaining setup, action, inventory, room and ending procedures. |
| v3 | 57 | PDF recipe symbols, Combat legality, survival Objectives, Door supply. |
| v4 | 57 | Explicit reference-only correction after independent adjudication caught line-offset errors. |
| v5 | 62 | Independent review added Storage, first-death unlock, Nest Egg acquisition, one-use Item consumption and Pod Earth status; genuine source/key overcertainty corrected. |
| v6 | 107 | Official base-game FAQ procedures/exceptions plus two manual coverage additions; six earlier expected answers were explicitly amended for official clarifications. |
| v7 | 108 | PDF-only prohibition of Search in Nest/Slime Room. All preceding 107 entries retained unchanged. |

Original Q01–Q20 wording is identical in every version. Original files and their hashes remain intact. Genuine source/key corrections are disclosed in [reference corrections](benchmark-corrections.json), [v5 corrections](benchmark-corrections-v5.json), and [FAQ corrections](benchmark-corrections-v6.json). These include correcting the unsupported certainty of the original Egg Melee key and the FAQ's Search-bottom, post-pass Interruption, waiting-Pod exit, Adult-token return and other rulings. [Benchmark preservation](benchmark-preservation.json) records original-entry hashes and exactly which expected answers changed; no target was silently changed to produce a pass.

The [coverage/rejection ledger](coverage-ledger.json) and [procedural map](procedural-coverage-map.json) cover 72 manual sections and all 61 in-scope FAQ entries. After the final PDF addition, targeted passes **12 and 13 added zero questions**. A fresh independent reviewer then found **zero further distinct source-supported additions** and returned [source-supported passage coverage PASS](coverage-review-v7.json). Earlier challenges and their discovered gaps remain in [initial review](coverage-review.json), [manual followup](coverage-review-v5.json), and [manual-plus-FAQ review](coverage-review-v6.json).

New questions require a new rule, source-defined outcome or consequential timing/exception. Cosmetic number/color/species changes, repeated procedures, mechanical recombinations and invented answers to source gaps were rejected. This is working saturation of supplied procedural passages, not proof that every conceivable game state has a unique ruling.

## Blind readers and all results

Every original reader dispatch used **gpt-6-luna / high / fork_turns=none**. Readers received only their frozen summary and question copy, excluding authoritative sources, keys, earlier outputs/grades/reviews, browsing and prior game knowledge. Actual model/effort are confirmed from runtime `session_meta`/`turn_context` records in [model provenance](model-provenance.json), also copied per iteration. Reviewers used **gpt-6.1-sol / high**. Isolation was by fresh context and restricted-input instructions, not an OS filesystem sandbox.

Scores below are **factual matches to each version's key**, not percentages of all rules that are accurate. Correct source-aware answers can explicitly acknowledge missing source rulings: Q18/Q51 carry `source_unresolved` flags, so even a factual-key match does not meet the zero-unresolved/core-completion criterion. Support/confidence labels were never accepted as grades.

| Iteration | Fixed benchmark | Reader A | Reader B |
|---|---|---|---|
| [full-iteration-02](full-iteration-02/results.json) | benchmark-v7 | 93/108; 15 partial; 0 incorrect | 102/108; 5 partial; 1 incorrect |
| [full-iteration-04](full-iteration-04/results.json) | benchmark-v7 | 100/108; 8 partial; 0 incorrect | 105/108; 2 partial; 1 incorrect |
| [full-iteration-05](full-iteration-05/results.json) | benchmark-v7 | 106/108; 2 partial; 0 incorrect | 103/108; 5 partial; 0 incorrect |
| [seed-iteration-01](seed-iteration-01/results.json) | benchmark-v1 | 15/20; 5 partial; 0 incorrect | 15/20; 5 partial; 0 incorrect |
| [seed-iteration-02](seed-iteration-02/results.json) | benchmark-v1 | 17/20; 3 partial; 0 incorrect | 18/20; 2 partial; 0 incorrect |
| [seed-iteration-03](seed-iteration-03/results.json) | benchmark-v1 | 18/20; 2 partial; 0 incorrect | 19/20; 1 partial; 0 incorrect |
| [seed-iteration-04](seed-iteration-04/results.json) | benchmark-v1 | 19/20; 0 partial; 1 incorrect | 18/20; 2 partial; 0 incorrect |
| [seed-iteration-05](seed-iteration-05/results.json) | benchmark-v1-source-corrected | 20/20; 0 partial; 0 incorrect | 20/20; 0 partial; 0 incorrect |
| [seed-iteration-06](seed-iteration-06/results.json) | benchmark-seed-faq-v1 | 18/20; 2 partial; 0 incorrect | 19/20; 1 partial; 0 incorrect |
| [seed-iteration-08](seed-iteration-08/results.json) | benchmark-seed-faq-v1 | 20/20; 0 partial; 0 incorrect | 19/20; 1 partial; 0 incorrect |

The [first independent grading adjudication](seed-adjudication.json) removed penalties for unrequested details and accepted equivalent wording. A later [fresh Q13 adjudication](q13-adjudication.json) established that the asked Queen-arrow outcome does not separately demand Event routing/discard. Its [uniform application](q13-adjudication-application.json) changed two historical grades; pre-adjudication results remain alongside revised results. Missing Adult/Carcass facts and contradictory precedence caveats remain failures. No question/key was changed for this grading clarification.

The final pair has these supported-fact omissions:

- Reader A: **Q22**, random Player Number assignment; **Q30**, Special Rooms prohibit Search.
- Reader B: **Q04**, post-pass Interruption exception; **Q07**, drawn non-Blank token set aside; **Q18**, Fire destruction of Eggs; **Q19**, second boarder may launch; **Q22**, random Player Number assignment.

These facts are explicit in the independently audited summary. They remain partial answers, not inferred passes or omissions filled from other answers. The final reviewer reports identify no further source-supported summary error or key error. All failed iterations, raw responses and detailed requested-part grades remain available. The current full-bank regression therefore **does not pass**.

The final full-bank evidence is [snapshot](full-iteration-05/summary-snapshot.md), [reader A](full-iteration-05/reader-a.json), [reader B](full-iteration-05/reader-b.json), [all grades](full-iteration-05/results.json), [independent A grading](full-iteration-05/grading-review-a.json), and [independent B grading](full-iteration-05/grading-review-b.json).

Reader A initially stopped after Q59. Its [raw incomplete response](full-iteration-05/reader-a-incomplete-Q01-Q59.json) was preserved; the same still-blind assignment was continued with no factual feedback. [Protocol evidence](full-iteration-05/reader-a-protocol-continuation.json) verifies the first 59 entries remained identical and the final output contains Q01–Q108 exactly once. This was output completion, not reuse of an informed reader for a repair retest.

Generic completeness instructions evolved, including numbered clauses and a requested-parts self-check. The final pair's [exact prompts](full-iteration-05/reader-prompts.json) and [protocol history](reader-protocol-history.json) record this. No expected ruling or question-specific hint was disclosed. Score changes cannot be attributed solely to summary revisions or model behavior; this is a fixed-bank regression exercise, not a controlled model comparison.

Three frozen candidates were superseded before reader dispatch and retained: [seed07](seed-iteration-07/cancelled-before-dispatch.json), [full01](full-iteration-01/cancelled-before-dispatch.json), [full03](full-iteration-03/cancelled-before-dispatch.json). They are not scored reader runs.

## Repairs, audit and integrity

Repairs corrected/generalized Egg wording without inventing an unresolved ruling, clarified token/card destinations and costs, added PDF-only Search prohibitions and crafting/die symbols, incorporated the scoped official FAQ, and made Pod, injury, scan, discard, Coordinates and endgame procedures easier to retrieve. Historical mode text was replaced by explicit scope exclusions. The original and every frozen tested summary are retained, with [final cumulative diff](full-iteration-05/summary-changes.patch) and individual repair patches.

The first independent [source audit](seed-iteration-03/source-audit.json) found two minor quick-reference issues: ship destruction was overbroad about evacuated survivors, and attack targeting lost the Action-card qualifier. Both were repaired. A separate fresh final auditor, which saw only summary and authoritative sources and never questions/keys/readers/grades, returned source-fidelity PASS for [full02](full-iteration-02/source-audit.json), [full04](full-iteration-04/source-audit.json), and [exact final full05](full-iteration-05/source-audit.json). Earlier audit files were not overwritten.

The [final validation](validation.json) verifies original-source preservation, original benchmark entries and frozen hashes, every expected reader/grade ID exactly once, raw-response/key correspondence, actual runtime models, and equality of the canonical summary with the final snapshot. Per-iteration manifests, model provenance, audit input manifests and integrity results are also retained. [Repository checks](repository-checks.json) pass targeted rules validation and whitespace checks.

Final canonical/snapshot SHA-256:

`50b69eeda13a8328409a7ee5e974883e8fbd9499ec80f8cab2da60d4257742ec`

No trust stamping, shared semantic-audit recording, index/manifest regeneration, commit, push or branch operation was performed. The final snapshot matches the canonical summary byte for byte; this is not a claim that the coordinator has completed its own repository/audit/stamping validation.

## Required continuation

Obtain original-game authoritative rulings for SG01–SG04, retain provenance, and create an explicit source/key version for any changed answer. Repair only as supported, then run the entire updated bank with two new blind Luna/high readers until both have zero partial, incorrect or source-unresolved answers, and obtain an audit of the exact resulting text. The coordinator owns audit recording, targeted stamping, registry/index/manifest work and final repository validation; any changed stamped bytes require fresh exact-byte testing. The goal is not marked complete while these requirements remain.
