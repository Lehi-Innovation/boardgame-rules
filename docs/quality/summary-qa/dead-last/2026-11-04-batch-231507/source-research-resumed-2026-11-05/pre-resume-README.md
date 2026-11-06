# Dead Last Rules 2.0 summary QA

Local reader regression: **27/27 for both fresh readers**, with zero partial or incorrect answers and no unsupported guesses replacing requested summary coverage. Independent final audit: **PASS for fidelity to the supplied source**. **Full procedural QA completion is not claimed:** the source itself leaves essential procedures unresolved, and authoritative clarification remains outstanding. See [machine status](game-status.json), [source limitations](source-limitations.json), and [coordinator handoff](coordinator-handoff.json). The persistent goal is blocked awaiting authoritative clarification after the same essential-source impasse was revalidated across three consecutive goal turns.

There was **no pre-existing canonical summary**. The coordinator recovered this game and authored an unverified, source-grounded baseline; the first test evaluates that baseline. This run does not describe a prior published summary as having failed. The [initial fingerprints](input-manifest.json) preserve the baseline, PDF and OCR hashes, and [seed iteration 01](seed-iteration-01/summary-snapshot.md) preserves its exact text.

Report date: November 5, 2026, America/Phoenix. Game: Dead Last (2016), BGG184522. Scope: complete 6–12-player English base game, publisher Rules2.0 including the zero-survivor erratum. No expansions or optional modes were included; the supplied booklet presents none. Sources were not silently exchanged for an older edition. The [publisher-authored PDF](../../../../../source_pdfs/dead-last-rules.pdf) is the university mirror documented in [provenance](source-provenance.json); the [canonical OCR](../../../../../extracted/dead-last-rules.txt) and original font-corrupted extraction both retain their hashes. All eight PDF pages were visually inspected, including image-only voting page5 and the complete page8 Showdown matrix.

## Fixed banks and coverage

The coordinator-prepared [20-question seed](benchmark-v1/question-bank.md), [question JSON](benchmark-v1/questions.json) and [key JSON](benchmark-v1/answer-key.json) were copied and [verified against the complete source before readers](seed-verification.json). All prepared files remain byte-identical. No substantive source/key correction was needed. Every original ID, wording, answer, source reference and entry hash remains intact in its benchmark version.

The [expanded bank](benchmark-v2/question-bank.md) contains **27 questions**: the unchanged original20 plus seven additions. Separate [questions](benchmark-v2/questions.json), [fixed key](benchmark-v2/answer-key.json), [entry hashes](benchmark-v2/hashes.json) and [pre-reader freeze](benchmark-v2/freeze-manifest.json) are retained. The bank and key never changed during expanded repairs.

| Targeted source pass | Focus | Accepted additions |
|---|---|---:|
| 1 | Conspiracy, action/card placement, ID indicators, normal replenishment, Ambush/Target timing and multiway source limitation | 6: Q21–Q26 |
| 2 | All-table winner eligibility during an extra Showdown | 1: Q27 |
| 3 | Alternate counts, tied Targets, Ambush, recipient sets and all payoff branches | 0 |
| 4 | Complete procedural re-read: setup, timing, destinations, round and game ends | 0 |
| Fresh independent challenge | All27 keys and all procedural passages, no summary or reader material | 0 |

The [coverage and rejection ledger](coverage-ledger.json) maps procedural passages and records rejected cosmetic variants, mechanical recombinations and cases for which the source supplies no ruling. The fresh [coverage reviewer](coverage-review.json) found zero substantive key corrections and no new source-resolvable question. Q24's normal refill follows from the four-bars-per-round invariant and explicit retention exceptions; that cross-passage inference is disclosed. Q27 tests the distinct table-wide winner consequence of tie-Showdown compensation. Q26 tests whether a multiway arrangement is supplied; correctly identifying its absence does not resolve it.

This establishes working saturation of source-resolvable procedures under the stated novelty rule. It does not establish that every possible game state has an official ruling. The evaluator had seen the coordinator summary and seed outputs when expanding the bank; the independent coverage reviewer had not.

## Reader results and repairs

Each row used two new **gpt-6-luna/high** readers, explicit model selection, `fork_turns="none"`, exactly the frozen summary and question file, and no sources, keys, browsing, prior answers, grades or parent history. Isolation was prompt-based, not a stronger OS file sandbox. [Actual model provenance](runtime-model-validation.json) verifies every runtime turn context, rather than inferring settings from directory names. All source/coverage reviewers and independent adjudicators were **gpt-6.1-sol/high**. Requested settings and dispatch timestamps are retained in [dispatch metadata](agent-dispatches.json).

Scores below are **correct / partial / incorrect**, for complete requested answers, not percentages of all rules.

| Iteration and detailed grades | N | ReaderA | ReaderB | Prompt |
|---|---:|---:|---:|---|
| [seed-iteration-01](seed-iteration-01/results.json) | 20 | 19 / 1 / 0 | 19 / 1 / 0 | v1 |
| [seed-iteration-02](seed-iteration-02/results.json) | 20 | 20 / 0 / 0 | 19 / 1 / 0 | v1 |
| [seed-iteration-03](seed-iteration-03/results.json) | 20 | 17 / 2 / 1 | 20 / 0 / 0 | v1 |
| [seed-iteration-04](seed-iteration-04/results.json) | 20 | 19 / 1 / 0 | 19 / 1 / 0 | v1 |
| [seed-iteration-05](seed-iteration-05/results.json) | 20 | 20 / 0 / 0 | 20 / 0 / 0 | v1 |
| [expanded-iteration-01](expanded-iteration-01/results.json) | 27 | 25 / 2 / 0 | 25 / 2 / 0 | v1 |
| [expanded-iteration-02](expanded-iteration-02/results.json) | 27 | 26 / 1 / 0 | 27 / 0 / 0 | v1 |
| [expanded-iteration-03](expanded-iteration-03/results.json) | 27 | 26 / 1 / 0 | 27 / 0 / 0 | v1 |
| [expanded-iteration-04](expanded-iteration-04/results.json) | 27 | 26 / 0 / 1 | 27 / 0 / 0 | v2 self-check |
| [expanded-iteration-05](expanded-iteration-05/results.json) | 27 | 27 / 0 / 0 | 27 / 0 / 0 | v2 self-check |

Seed repairs made the three Showdown choices and face-down procedure explicit, clarified repeated tie Showdowns, added the booklet's three-player Ambush example and guaranteed Grab One & Go payout, and emphasized upright IDs. Expanded repairs added the exact location of voting cards, hidden-value next-round preparation, precise source-limit disclosures and the same reward/all-table scoring rule for extra Showdowns. The last repair added the source's Blue4/Purple3 example after a reader falsely called those totals tied. See the [complete baseline-to-final diff](summary-changes.patch); every intervening frozen snapshot and patch remains available.

Iteration04 of the expanded series changed only the prompt, with identical summary bytes to expanded03. During expanded03, a coordinator follow-up authorized a generic pre-submission completeness check. Its first reader had already been dispatched, so that pair retained v1; **expanded04 was the first v2 pair**, and expanded05 also used v2. The [prompt policy](prompt-policy.json) records the exact added paragraph. All original prompt files remain untouched, and each iteration retains readable templates, exact dispatch-text copies and prompt hashes. V2 supplied no question-specific facts or hints. Its first pair still produced an incorrect answer; the reminder was not treated as a pass. Changes across versions and repeated known-bank testing do not isolate a model or prompt effect.

Grading considered every requested part independently and never borrowed missing facts from another answer. For example, missing Showdown card identities, repeated tie resolution, upright ID setup, tied-Target elimination, voting-card destination or hidden-value preparation remained partial; the reversed Grab/Share payout and the claim that4 and3 were tied remained incorrect. Complete conditional rulings were accepted despite cautious support labels. A correct answer about an explicitly missing official procedure is distinct from an unsupported guessed procedure.

Borderline decisions received independent adjudication: [seed01](seed-iteration-01/adjudication.json), [seed03](seed-iteration-03/adjudication.json), [expanded01](expanded-iteration-01/adjudication.json), [expanded02](expanded-iteration-02/adjudication.json), and [final expanded05](expanded-iteration-05/adjudication.json). In the final ReaderB Q06, the adjudicator reads the zero phrase as Red's Ambush contribution, followed by the explicit one-vote-each tally; its wording is imprecise but does not give a materially contradictory outcome. In expanded01 ReaderB Q10, an unrequested assertion about received-card reveal timing was recorded separately as unsupported; the canonical summary now explicitly discloses the source's lack of that rule. All failed iterations and raw outputs remain preserved.

Final evidence: [snapshot](expanded-iteration-05/summary-snapshot.md), [frozen questions](expanded-iteration-05/questions.json), [readerA](expanded-iteration-05/reader-a.json), [readerB](expanded-iteration-05/reader-b.json), [all54 grades](expanded-iteration-05/results.json), [actual provenance](expanded-iteration-05/model-provenance.json), and [input hashes](expanded-iteration-05/input-manifest.json).

## Independent source audit and unresolved limits

The [fresh exact-final source audit](fresh-final-source-audit.json) is PASS for summary fidelity, with zero summary defects, covering38 claim groups and all eight visually inspected source pages. The new reviewer `/root/fresh_exact_final_audit` used explicit Sol/high and `fork_turns="none"`; it received only the exact expanded05/current summary and original PDF, OCR and eight source page images. It saw no earlier summaries, reviews, repair notes, banks, keys, reader material or grades and authored no repairs. Its [exact prompt](fresh-final-auditor-prompt.txt), [confirmed actual runtime model](fresh-final-audit-model-provenance.json), eleven input hashes and isolation statement establish this fresh final boundary. It requested no text change, so the existing27/27 reader pair still covers the final bytes. The [earlier continuing source audit of expanded05](expanded-iteration-05/source-audit.json) remains valid history and is not presented as the newly isolated reviewer. Earlier audits remain preserved for [seed04](seed-iteration-04/source-audit.json), [seed05](seed-iteration-05/source-audit.json), [expanded02](expanded-iteration-02/source-audit.json), [expanded03](expanded-iteration-03/source-audit.json), and the [identical-byte audit reuse for expanded04](expanded-iteration-04/audit-reuse.json). Continuing-auditor runtime provenance is [retained](final-source-audit-model-provenance.json), separately from the [fresh final auditor](fresh-final-audit-model-provenance.json).

The audit's PASS certifies fidelity to the rules actually supplied. It separately reports that the source is **not fully executable** for all legal states:

- A three-or-more-way qualifying highest-score tie has no arrangement for the mandated two-player Showdown. The separate [source-only review](tie-source-review.json) proves reachability: six solo-win rounds can leave A/B/C on24 points each with no earlier25-point win; a later zero-survivor round legally gives each a4-point compensation card, producing28/28/28. All vote steps, previous victory checks and the26/43/11 denomination inventory are audited in that report.
- An all-Ambush vote has zero counted votes. The booklet does not settle Target status or voter-restricted retaliation when nobody voted for anyone.
- Extra game-end tie Showdowns lack an express procedure for supplying their central pot. Applying the existing payout and deck-reward rules does not invent or resolve that provisioning step.
- Minor source gaps concern revealed-card recovery, assignment of particular hidden payout cards and publicity of received values; no invented official handling was supplied.

[Source limitations and resolution requirements](source-limitations.json) distinguish these gaps from summary errors. [Bounded official research](tie-source-review.json) found no accessible attributable clarification; BGG forum titles are leads only, and access failures are recorded. No publisher/community messages were sent. The coordinator's23+1 reachability lead used a nonexistent1-point bar; the independent24+4 witness replaces that lead, with no bank/key alteration. The coordinator subsequently superseded its invalid lead explicitly; its new21+3 candidate is not used in this report, because this run already has the fully verified six-player witness. [Research notes](source-research-notes.json) preserve this distinction.

An attributable publisher/designer clarification is needed for the essential missing procedures. If new authority changes a key, explicitly version it, preserve the existing benchmark, and repeat coverage review, full-bank blind tests and source audit. No bracket, multiway payoff, joint victory or extra-pot rule has been invented. These limitations prevent an unqualified complete-base procedural PASS even though readers recover every requested fact in this bank.

## Integrity, repository checks and handoff

[Final validation](validation.json) checks all470 reader answers and grades across ten pairs, unique expected IDs, exact correspondence to raw answers and fixed keys, frozen hashes, original prepared-file and20-entry preservation, all runtime model/effort contexts, all eight audited image hashes, links, and byte-for-byte equality of the final snapshot with the [canonical summary](../../../../../rules/dead-last.md). The [local validator](validate_evidence.py) records the targeted repository structural check and whitespace check. The [evidence index](evidence-index.md) links all artifacts, including every raw response and failed iteration.

Only the assigned canonical summary and this QA directory were written. Shared sources retain their initial fingerprints. No registry, index, manifest, global audit registry or shared script was edited; no stamping, regeneration, commit, push or branch operation was performed. Verification remains unverified while essential source gaps remain. The coordinator expressly excludes this incomplete game from full-core stamping or promotion; no such step is pending.

Status is **awaiting-source**, with local regression and source-fidelity audit complete. The coordinator accepts an honest awaiting-source handoff without an unconditional shared PASS, stamping or promotion. The goal was marked blocked after the same essential-source impasse recurred across three consecutive goal turns; authoritative clarification remains necessary, and no objective or batch completion is claimed. The [fresh final auditor runtime record](fresh-final-audit-model-provenance.json) and its [isolation statement](fresh-final-source-audit.json) are the exact evidence requested for coordinator inspection. Later continuation requires explicit new-source versioning when applicable, fresh full-bank readers and independent audit; any changed canonical bytes must be tested exactly. Known-bank passes are regression evidence, not a held-out general-accuracy result.
