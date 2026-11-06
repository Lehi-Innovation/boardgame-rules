# El Grande summary QA — awaiting-source

Report date: November 5, 2026 (America/Phoenix).

**Complete-core result: INCOMPLETE — essential source rulings remain unresolved.** A passing reader benchmark or source-fidelity audit below does not certify those missing playable outcomes. The persistent goal is blocked pending applicable primary clarification.

Classic 1996 English Hans im Glück/Rio Grande base rules, Jay Tummelson translation/editing; publisher PDF pp.1–12, including every base Action Card. Expansion mechanics on pp.13–20, 2023 edition changes and optional short game excluded. Primary source bytes remain unchanged.

Both final fresh Luna/high readers scored **54/54**, with zero partial/incorrect answers or unsupported guesses. The final exact-text source audit is **PASS for fidelity** and **MAJOR for complete-core gameplay**.

## Fixed benchmark and results

The evaluator read the existing summary, then the complete authoritative core source and relevant PDF diagrams/card faces before fixing the original 20 targets. Each reader was fresh gpt-6-luna/high with fork_turns=none, given only its frozen summary and question file. No source, key, parent history, prior findings, other answers or browsing was permitted. [Exact dispatched prompts](dispatched-prompts/) and [runtime-confirmed provenance](all-model-provenance.json) are preserved.

| Iteration | Bank | Reader A correct/partial/incorrect | Reader B correct/partial/incorrect |
|---|---|---|---|
| [seed-iteration-01](seed-iteration-01/results.json) | 20 | 5/13/2 | 5/13/2 |
| [seed-iteration-02](seed-iteration-02/results.json) | 20 | 20/0/0 | 20/0/0 |
| [expanded-iteration-01](expanded-iteration-01/results.json) | 52 | 52/0/0 | 50/2/0 |
| [expanded-iteration-02](expanded-iteration-02/results.json) | 53 | 53/0/0 | 52/1/0 |
| [expanded-iteration-03](expanded-iteration-03/results.json) | 53 | 52/0/1 | 53/0/0 |
| [expanded-iteration-04](expanded-iteration-04/results.json) | 53 | 53/0/0 | not dispatched (superseded) |
| [expanded-iteration-05](expanded-iteration-05/results.json) | 53 | 53/0/0 | 53/0/0 |
| [expanded-iteration-06](expanded-iteration-06/results.json) | 53 | 53/0/0 | 53/0/0 |
| [expanded-iteration-07](expanded-iteration-07/results.json) | 53 | 53/0/0 | 53/0/0 |
| [expanded-iteration-08](expanded-iteration-08/results.json) | 54 | 53/1/0 | 54/0/0 |
| [expanded-iteration-09](expanded-iteration-09/results.json) | 54 | 54/0/0 | 54/0/0 |

All requested parts were graded individually against fixed source-backed answers. Equivalent wording was accepted; material omissions, contradictory caveats and unsupported additions remained findings. No answer borrowed missing facts from another answer. The [independent expanded-run adjudication](expanded-iteration-01/independent-adjudication.json) distinguishes actual requested parts from incidental key context; its two retained partial answers were repaired. A second fresh adjudication retained the broader singleton-fallback assertion as partial; the next summary explicitly preserves the source boundary. [Later grading adjudications](expanded-iteration-07/independent-adjudication.json) accepted complete answers despite support labels; [the 54-question adjudication](expanded-iteration-08/independent-adjudication.json) retained the missing destination ruling as partial and prompted the final repair. [Second adjudication](expanded-iteration-02/independent-adjudication.json).

| Version | Size | History |
|---|---|---|
| [v1 seed](benchmark-v1/question-bank.md) |20| Historical original questions/answers remain intact. V5 explicitly corrects two underdetermined stems; all answer objects are unchanged. |
| [v2 expanded](benchmark-v2/question-bank.md) |51| Frozen before review; no readers saw these expanded targets. |
| [v3 corrected](benchmark-v3/question-bank.md) |52| Genuine Q47/Q49 other-region key corrections and new Q52 disk-selection domain. |
| [v4 expanded](benchmark-v4/question-bank.md) |53| Adds Q53 unused-scoreboard introduction versus in-play relocation; preserves all 52 v3 entries. |
| [v5 source-corrected scenarios](benchmark-v5/question-bank.md) |53| Explicit Q12/Q13 five-player→four-player correction removes an unspecified fifth count. All53 answers unchanged; no target relaxation. |
| [v6 score-scope correction](benchmark-v6/question-bank.md) |53| Q13 explicitly asks scoreboard points before bonuses; rank outcomes unchanged. |
| [v7 initial-hand expansion](benchmark-v7/question-bank.md) |54| Adds Q54 full initial power-card hand; all 53 v6 entries preserved. |

See [the explicit correction record](benchmark-corrections.json), [current questions](questions.json), [fixed key](answer-key.json) and [readable full bank](question-bank.md). No target changed within a tested repair series. The [fresh scenario validity review](seed-scenario-validity-review.json) identified underdetermined five-player premises in original Q12/Q13; [v5 corrections](benchmark-corrections-v5.json) explicitly repair those stems in a new version. The [v6 correction](benchmark-corrections-v6.json) separately clarifies Q13 as scoreboard points before bonuses, since unstated bonus eligibility otherwise changes totals. Historical grades compare answers with their historical fixed key and do not certify those ambiguous premises. Earlier drafts, failed iterations and raw responses remain available.

## Coverage stopping check

[Procedural map and rejection ledger](coverage-ledger.md) / [machine-readable ledger](coverage-ledger.json) map every in-scope procedural passage either to supported questions or to the separately disclosed source gaps. The first independent challenge found genuine destination-key precision and secret-scoring domain issues; the second found the scoreboard state-transition gap. Later source-only challenges required explicit scenario/bonus scope and the full initial power-card hand. The final 54-pair challenge found no additions or key corrections after the final two zero-addition passes. After each accepted addition the evaluator repeated the zero-addition checks. These are working saturation checks under the stated novelty rule, not proof of every possible scenario.

- [First source-only coverage challenge](coverage-review-01.json).
- [Second fresh source-only coverage challenge](coverage-review-02.json).
- [Third fresh source-only coverage challenge](coverage-review-03.json).

- [Final corrected-bank source-only coverage challenge](coverage-review-04.json).

- [Final v6 source-only coverage challenge](coverage-review-05.json).

- [Final expanded-bank source-only coverage challenge](coverage-review-06.json).

Changed numbers, cosmetic rewording, duplicate printed cards and independent-action recombinations were rejected. Source-undefined branches were recorded as unresolved rather than padded into definitive answer targets.

## Changes to the summary

Corrected the first power-card starter, at-most recruitment and noninterleaving timing; clarified used-card display, unselected-card disposal, Castillo protection and invalid disk destinations; repaired multiway tie ranks, player-count cutoffs and final-scoring timing; added the complete base Action Card reference and source limitations. Corrected source_pdf/extracted_date to the assigned publisher authority and removed out-of-scope variants. Each iteration retains its snapshot and [diff from original](expanded-iteration-09/summary-changes.patch). Machine-managed verification metadata/banner have not been manually promoted or stamped.

## Source fidelity versus complete-core result

The [fresh essential-gap assessment](essential-gap-assessment.json) gave source fidelity PASS and **complete-core FAIL_UNRESOLVED_ESSENTIAL_RULINGS**. Seven high-confidence playable branches remain without a definitive procedure in the supplied source:

1. The King returns when a player has fewer than three eligible pieces.
2. One-per-player return when a player has no eligible regional piece.
3. Secret remove-two with no eligible region, or only protected doubles plus legal singletons.
4. Secret remove-all with pieces only in the King’s region.
5. The Court when provinces contain fewer than two pieces.
6. Forced Movement to Castillo versus a disk that cannot select Castillo.
7. All-4 scoring when Castillo has the 4/0/0 mobile scoreboard.

The final exact-text audit additionally flags actor disk participation and the per-piece versus collective interpretation of “other regions” in multi-origin Intrigue effects. Earlier reviewers classify some choreography differently; none supplies a verified missing procedure. An additional medium-confidence candidate concerns zero-count scoring eligibility. The assessment separates these state-changing outcomes from nonessential disk choreography, an internally resolvable participant-heading discrepancy and the absent endgame tiebreaker. [Exact missing rulings and evidence](source-gap-register.json) / [independent classification and clarification requests](essential-gap-assessment.json).

[Bounded authoritative clarification research](clarification-research/README.md) checked matching 1996 German publisher material, the 1997 explicit base FAQ, publisher download routes, and a 2005 authored clarification claiming designer approval. Differences and later-edition material were not silently imported. [Independent applicability review](clarification-research/independent-applicability-review.json) records what, if anything, each source resolves and what still requires publisher/designer confirmation for this English edition.

A fresh independent source audit of the final exact text is stored as [final source audit](expanded-iteration-09/source-audit.json). It passes fidelity to the documented source and returns MAJOR for complete-core gameplay; no unresolved essential branch is treated as passed. The earlier [seed02 audit](seed-iteration-02/source-audit.json) covers only its historical exact bytes.

## Integrity, validation and handoff

[Third-turn blocked audit](continuation-02/README.md) records unchanged inputs and the external ruling dependency.

[Complete evidence index](evidence-index.md) links every saved artifact, including all frozen inputs, raw reader responses, detailed grades, model records, diffs, source audits and validation files. [Evidence inventory hashes](evidence-inventory.json) cover these artifacts.

- [Original input hashes and preexisting work status](input-manifest.json); [source page/extraction-line reference index](source-reference-index.json).
- [Final validation](validation.json): original benchmark preservation and explicit independently reviewed stem corrections, version hashes, IDs exactly once, every grade tied to exact raw/key/question, runtime models and effort, canonical/snapshot byte equality, targeted rules validation and whitespace checks.
- [Completion grading](completion-grading.json) explicitly keeps overall completion false; [reader tool/input isolation review](input-isolation-review.json) and [historical scratch deviations](reader-scratch-deviations.json) disclose access-control limits.

- [Machine-readable status](game-status.json) records exact tested bytes and incomplete completion grading.

[Coordinator handoff confirmation](continuation-01/README.md) independently verifies the exact canonical bytes, preserved seed, runtime models and target catalog checks. It explicitly retains awaiting-source and does not authorize verified stamping.

Shared audit registries, stamping, index/manifest/catalog regeneration, commits and publishing belong to the coordinator and were not changed here. **Do not promote this game as complete-core PASS.** Obtain applicable primary clarification for remaining essential rulings, version any resulting key changes, reopen coverage where needed, and test/audit the exact repaired and ultimately stamped bytes. No coordinator integration pass is claimed. The final tested byte hash and source hashes are available in the status and input manifests.

Current exact tested snapshot: [expanded-iteration-09/summary-snapshot.md](expanded-iteration-09/summary-snapshot.md); SHA-256 `f82522b8fead3aab7203454a2d4f874237f5a12a43b43e62320f2e62601221c7`.

