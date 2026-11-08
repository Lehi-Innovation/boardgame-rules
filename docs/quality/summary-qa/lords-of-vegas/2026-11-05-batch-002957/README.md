# Lords of Vegas — exact stamped summary QA

**Exact stamped QA complete after coordinator final verification.** The coordinator completed local publication verification and explicitly authorized goal completion. [Authorization](../../batches/2026-11-05-batch-002957/coordinator-checks/lords-final-completion-authorization.json), [completion audit](completion-audit.json).

The [canonical summary](../../../../../rules/lords-of-vegas.md) covers the Mayfair 2010/2013 English 2–4-player base game, using only positively applicable base clarifications from the publisher’s previous-Mayfair unified book. All assigned sources and the complete frozen 39-question v10 bank remain unchanged. Up!, Underworld, Americana, Con Jobs, the revised six-player edition and optional Gamble Variant remain excluded.

## Exact stamped version

The coordinator accepted the pre-stamp evidence, recorded the source verdict, and changed verification metadata plus the named verification notice through the repository workflow. The worker did not edit the stamp or rules text. [Coordinator authorization](../../batches/2026-11-05-batch-002957/coordinator-checks/lords-exact-stamped-retest-authorization.json), [stamp integrity](stamped-iteration-01/stamp-integrity.json), [exact diff](stamped-iteration-01/stamp-changes.patch).

- Pre-stamp tested SHA256: `60000c000b4c9a54d5b80c617788cd905c12e024be26fffa68bc9cbde1710ae7`.
- Current stamped SHA256: `a3e5c5b7f40b6dc1f3249617f0c39c176a087128029d5d537889fdc4cf46d575`.
- The [final reader snapshot](stamped-iteration-02/summary-snapshot.md) must remain byte-identical to the canonical summary. Changing these bytes requires fresh full-bank testing and an applicable independent source audit.

## Reader and grading results

Every listed pair answered all 39 unchanged questions. Counts are original strict correct / partial / incorrect grades.

| Frozen pair | Reader A | Reader B |
|---|---:|---:|
| [expanded-iteration-13](expanded-iteration-13/results.json) | 39 / 0 / 0 | 39 / 0 / 0 |
| [stamped-iteration-01](stamped-iteration-01/results.json) | 37 / 1 / 1 | 39 / 0 / 0 |
| [stamped-iteration-02](stamped-iteration-02/results.json) | 39 / 0 / 0 | 39 / 0 / 0 |

Stamped01 is a failed historical run. Reader A’s checked_inputs asserted the wrong per-pip rate in Q04, despite correct asked facts, and Q27 gave a conditional general tie rule without resolving the concrete affected dice. Both findings and all original raw fields are preserved; neither was waived. Reader B scored 39/39. The coordinator requested one NEW Sol6.1/high/fork-none neutral on the complete original Q27 entry, fixed scope/key and full frozen summary, without prior grades. Its single decision was **Partial**: known inputs plus a conditional selector still left the affirmative case conclusion to the reader. This was not a demand for a standalone list of color labels. No resampling occurred. Primary and effective historical scores remain unchanged. [Neutral report](stamped-iteration-01/q27-neutral-adjudication.json), [preserved primary/effective view](stamped-iteration-01/adjudicated-results.json).

Stamped02 uses two NEW gpt-6-luna/high agents with `fork_turns=none` and identical prebound protocol v8 apart from output path. They receive only the frozen summary/questions as rules data. The generic fact-free renderer now requires explicit case_decisions when applying givens, preserves unspecified attributes, and copies a single independently checked result into answer, clause rulings and case_check. It includes no failed IDs, game facts, key facts, earlier answers/grades or case hints. [Method decision](reader-protocol-v8-decision.json).

Two NEW independent gpt-6.1-sol/high graders assess Q01–20 and Q21–39 for both readers. Their bundles losslessly reconstruct every original field, including all quotation metadata and case checks. All99 required-fact records are assessed once per reader; no fact is borrowed across answers. Ordinary lookup facts may be supplied by complete same-entry operative quotations; concrete decisions/calculations still must be resolved. Correct quotes do not erase a wrong ruling. Confidence labels and optional formatting do not replace factual assessment. [Results](stamped-iteration-02/results.json), [fact/ID validation](stamped-iteration-02/grading-validation.json), [raw manifest](stamped-iteration-02/raw-response-manifest.json), [model provenance](stamped-iteration-02/model-provenance.json).

One stamped01 reader stored operative_quotes as a section-keyed dictionary. The initial diagnostic iterated keys; it is preserved separately. The corrected checker verifies the actual stored passage values, with no fuzzy matching or raw-entry edits. Both stamped01 responses contain complete verbatim heading units. Original full dictionaries were already present in the unchanged grading bundles. [Diagnostic correction](stamped-iteration-01/quote-schema-diagnostic-correction.json). This changed no factual grade.

## New post-stamp source audit

A NEW independent gpt-6.1-sol/high/fork-none PURE auditor compared the exact stamped candidate against both complete authoritative book extractions and inspected all seven specified native images. It saw no question bank, key, scope map, reader response, grade, prior audit, benchmark note or agent/chat metadata; the verification banner was not evidence. Verdict: **PASS**, with **0 findings**. [Fresh stamped audit](stamped-iteration-01/source-audit.json).

Actual delivery includes all 18 text chunks covering the candidate and both complete books, plus seven distinct model-visible native image outputs before the report was saved. [Native delivery proof](stamped-iteration-01/native-delivery-proof.json), [runtime text/model proof](runtime-provenance.json), [independence checks](independence-tool-check.json).

This is a NEW post-stamp audit, not a pre-stamp verdict carried onto changed bytes. Its candidate in stamped01 and the stamped02 reader snapshot have identical bytes and immutable source hashes. Only the generic reader method changed after stamped01. [Exact-byte audit applicability](stamped-iteration-02/source-audit-reuse.json).

## Scope qualification and history

The coordinator accepted **expanded-v10 source-knowledge/source-limits** certification. This does **not** recover or certify a mandatory physical thrower for free boss-tie rerolls. The books specify the affected dice/timing but do not expressly assign that physical person. Q27 retains its complete who-rolls clause and requires the honest source-limit statement alongside the concrete known dice selection. No owner-only mandate, anyone-may-roll permission or house convention is invented; the unsupported mandatory-actor clause receives no recovered gameplay-rule credit. The own-dice roller instruction is expressly local to paid Reorganization.

[Independent source/key/coverage review](source-key-v10-review.json) returns `PASS_FOR_DECLARED_EXPANDED_V10_SOURCE_LIMITS_BENCHMARK`; the original definite-actor target remains unresolved. The only historical baseline correction is the explicit Q27 source correction; all other old records and all question wording remain intact. [Correction](expanded-v9/source-key-correction.json), [original-entry preservation](original-entry-preservation.json), [readable bank](expanded-v10/question-bank.md), [fixed key](expanded-v10/grading-key.json), [asked scope](expanded-v10/scope-map.json).

The bank grew from 20 to 39 with independent challenges; parent passes 23 and 24 added zero after Q39. [Coverage/rejection ledger](coverage-ledger-v10.json). The [preserved pre-stamp final report](expanded-iteration-13/pre-stamp-final-report.md) documents every earlier failed/scored run, source repairs, independent adjudications, preparatory freezes, the canceled superseded dispatch, scope/key versioning, source silences, the excluded metadata-exposed reviewer and sanitized clean source-review packets. Earlier reports, raw answers and grades are unchanged. [Version history](bank-version-history.json).

This is a known fixed-set, tool-assisted source regression and coverage-saturation exercise, not held-out accuracy or proof that every imaginable scenario was enumerated. Fresh-context instructions isolate roles in a shared workspace; there is no separate reader filesystem sandbox.

## Validation and final handoff

[Validation](validation.json) covers assigned source/seed integrity, frozen inputs and prompts, all IDs/facts once, exact raw reconstruction and grader input hashes, zero unresolved factual findings for the final pair, complete actual input delivery, actual requested/model/effort settings, source-only independence, native inspections, the declared coverage contract, exact stamped canonical equality, targeted structural validation and whitespace.

The worker changed only its assigned summary before coordinator stamping and its own evidence directory. It did not commit, push, switch branches/worktrees, edit shared catalogs/registries/instructions, run global publication, or change any stamp metadata. The coordinator owns final evidence inspection, local publication/catalog checks and completion authorization. No game goal completion is claimed before that authorization. Any subsequent canonical-byte change reopens exact-version testing/audit requirements.
