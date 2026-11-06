# Oath first-printing multiplayer summary QA

**COMPLETE — coordinator accepted and authorized goal completion.** Current source audit: PASS; procedural coverage passes; final reader scores: A **104/0/0**, B **104/0/0** (correct/partial/incorrect).

The canonical file is [rules/oath-chronicles-of-empire-and-exile.md](../../../../../rules/oath-chronicles-of-empire-and-exile.md). Scope is the 2021 base first printing: Law dated October20,2020, the corresponding complete Playbook, official base errata dated November15,2022 and Site Reference. Multiplayer, all Oaths/Visions, Empire, Campaign, citizenship, Chronicle and later setup are covered. Clockwork Prince and New Foundations are excluded. Card-specific text remains on the cards.

## Current evidence

- Tested candidate: [expanded-iteration-15/summary-snapshot.md](expanded-iteration-15/summary-snapshot.md), SHA256 `2ce210f14eaa6289253e7b40e0a2648cddbc6bbe8e8c11f12fb5bfe0e61fd67e`. Canonical equality is a final gate.
- Fresh independent [source audit](expanded-iteration-15/source-audit.json): PASS; exact-byte/full-delivery verification is required before readiness.
- Fresh source-only [coverage challenge10](coverage-review-10.json): PASS working saturation, all104 questions/keys and complete source corpus. [Exact reviewed ledger](coverage-ledger-reviewed-10.json). Root passes30/31 added zero.
- [Final frozen bank](expanded-v11/question-bank.md):104 retained questions,328 required-fact groups per reader.93 questions receive novelty credit;11 retained regressions receive zero. Q104 has zero credit because the corrected Q046 key already states the actual-flip guard. No prior question is deleted and there is no count quota/cap. [Final novelty decision](expanded-v11/final-novelty-assessment.json).
- [Reader A](expanded-iteration-15/reader-a.json), [Reader B](expanded-iteration-15/reader-b.json), [strict grades](expanded-iteration-15/results.json), [grading validation](expanded-iteration-15/grading-validation.json), and [final gates](final-certificate.json).
- [Lossless grading transport](expanded-iteration-15/grading-input-losslessness.json) reconstructs every entire original entry, including source quotations and numerical/case fields. Raw files remain unchanged.
- [Reader prompt equality](expanded-iteration-15/prompt-comparison.json), [technical validation](expanded-iteration-15/reader-technical-validation.json), [model provenance](expanded-iteration-15/final-model-provenance.json), and [integrity/targeted checks](validation-in-progress.json).

Iteration15 is a fresh exact-byte post-stamp recheck. Coordinator metadata stamping changed the canonical SHA from5339b6cd496b4f977f9ff6e9c0786ad9104d38d7abda39996dcc44f598eea9bf to2ce210f14eaa6289253e7b40e0a2648cddbc6bbe8e8c11f12fb5bfe0e61fd67e. The complete pre-stamp certificate is retained in [iteration14](expanded-iteration-14/certificate-pre-stamp.json). Two new readers, one new complete-source auditor and six new bounded graders assess the stamped snapshot with the unchanged bank/key/scope; no gameplay change was made by this worker.

Total paired iterations: **26**, defined as folders with both saved primary reader-a.json and reader-b.json. [Explicit folder list, hashes and reconciliation](paired-iteration-count.json). This includes abandoned/historical-unproven pairs and does not assert every pair was qualified. [Coordinator completion authorization](coordinator-completion-authorization.json).

## Reader method and limits

Current readers are fresh-context Luna/high, forked without parent history. Reviewers and grader are Sol/high. Actual runtime model/effort records are preserved in [runtime provenance](runtime-provenance.json), not inferred from requested settings. Readers receive only the frozen summary and questions; keys, grading scope, source originals, old responses and grades are withheld. Isolation is procedural/contextual with recorded tool access, not an extra filesystem sandbox.

Each reader receives every character of both files through bounded contiguous model-visible chunks. Actual tool outputs are independently matched to the frozen inputs, with no gaps. Required-input delivery reports and complete tool records are in [delivery-audit](delivery-audit/). Auxiliary truncated diagnostics are recorded separately and do not substitute for missing input delivery.

The current test is **tool-assisted extractive fixed-set regression**: exact operative rule quotations, complete supporting sections, minimal concrete-case conclusions and concrete numerical results. Readers are instructed to execute arithmetic with Python; the actual tool records preserve which computations were executed. It does not establish one-shot or unaided paraphrase accuracy, held-out accuracy, exhaustive card-interaction coverage or a controlled summary-only improvement. Both summary and reader protocol evolved; [the full protocol history](reader-protocol-history.md) discloses those changes. A material wrong case conclusion still fails despite correct quoted rules; numerical questions require actual substituted results. Support/self-review labels are not grades. Each answer must independently supply every actually requested fact, with no borrowing from another answer or reader.

Iteration11 introduced mechanical whole-Markdown-section checks before any grader: each attachment must include its actual heading and every body/subheading through the next equal-or-higher heading, with all answer excerpts contained inside attached complete sections. Earlier literal-substring checks did not establish this. Iteration12 additionally records each numerical computation once in numeric_application, without a duplicate numerical case_result. The earlier contradictory prose remains Incorrect; no original field or judgment is removed from historical transport or grades. These are prospective protocol changes, not a controlled measure of summary-only improvement.

## Historical failures and source repairs

All raw failures, initial grades, independent adjudications and superseded snapshots remain preserved. A [runtime delivery audit](delivery-audit/decision.json) found truncation in28 historical reader sessions; complete delivery was not established for those older runs. Their grades remain historical, including seed13’s20/20 pair, and are not final certification. Expanded03 onward uses independently proven full input delivery.

| Run | N | A C/P/I | B C/P/I | Qualification |
|---|---:|---|---|---|
| [seed-iteration-01](seed-iteration-01/results.json) |20|14/6/0|15/5/0|Historical; full delivery not certified|
| [seed-iteration-02](seed-iteration-02/results.json) |20|14/6/0|14/6/0|Historical; full delivery not certified|
| [seed-iteration-03](seed-iteration-03/results.json) |20|16/2/2|19/1/0|Historical; full delivery not certified|
| [seed-iteration-04](seed-iteration-04/results.json) |20|17/3/0|19/0/1|Historical; full delivery not certified|
| [seed-iteration-05](seed-iteration-05/results.json) |20|19/1/0|18/1/1|Historical; full delivery not certified|
| [seed-iteration-06](seed-iteration-06/results.json) |20|20/0/0|18/2/0|Historical; full delivery not certified|
| [seed-iteration-07](seed-iteration-07/results.json) |20|20/0/0|19/1/0|Historical; full delivery not certified|
| [seed-iteration-08](seed-iteration-08/results.json) |20|18/1/1|17/3/0|Historical; full delivery not certified|
| [seed-iteration-09](seed-iteration-09/results.json) |20|19/0/1|19/0/1|Historical; full delivery not certified|
| [seed-iteration-10](seed-iteration-10/results.json) |20|18/0/2|20/0/0|Historical; full delivery not certified|
| [seed-iteration-11](seed-iteration-11/results.json) |20|19/1/0|19/1/0|Historical; full delivery not certified|
| [seed-iteration-12](seed-iteration-12/results.json) |20|20/0/0|19/1/0|Historical; full delivery not certified|
| [seed-iteration-13](seed-iteration-13/results.json) |20|20/0/0|20/0/0|Historical; full delivery not certified|
| [expanded-iteration-03](expanded-iteration-03/results.json) |100|85/14/1|74/23/3|Full input delivery proved|
| [expanded-iteration-04](expanded-iteration-04/results.json) |103|93/7/3|92/10/1|Full input delivery proved|
| [expanded-iteration-05](expanded-iteration-05/results.json) |103|99/3/1|99/3/1|Full input delivery proved; Q025 scope precision defect separately flagged|
| [expanded-iteration-07](expanded-iteration-07/results.json) |104|103/0/1|101/1/2|Full input delivery proved|
| [expanded-iteration-08](expanded-iteration-08/results.json) |104|100/4/0|99/5/0|Full input delivery proved; extractive protocol|
| [expanded-iteration-09](expanded-iteration-09/results.json) |104|96/8/0|99/5/0|Full input delivery proved|
| [expanded-iteration-10](expanded-iteration-10/results.json) |104|92/12/0|85/19/0|Full input delivery proved|
| [expanded-iteration-11](expanded-iteration-11/results.json) |104|101/2/1|102/2/0|Full input delivery proved|
| [expanded-iteration-12](expanded-iteration-12/results.json) |104|104/0/0|102/2/0|Full input delivery proved|
| [expanded-iteration-13](expanded-iteration-13/results.json) |104|104/0/0|102/2/0|Full input delivery proved|
| [expanded-iteration-14](expanded-iteration-14/results.json) |104|104/0/0|104/0/0|Full input delivery proved|
| [expanded-iteration-15](expanded-iteration-15/results.json) |104|104/0/0|104/0/0|Full input delivery proved|

Expanded02 retains incomplete/generic A drafts and B’s self-reported role mistake; it was abandoned after the input-delivery problem was found. Expanded06 was a prepared source-audit candidate, not a reader test: its [audit failed with a P2 finding](expanded-iteration-06/source-audit.json). The Chronicle denizen-discard instruction wrongly covered all retained sites not ruled by the winner. Law8.3.3 discards denizens only at sites where an intact edifice actually flipped to ruin in that step. A power-kept site without a flip exposes the difference. The corrected guard, source finding and Q104 regression are preserved. Earlier source PASS reports remain historical and are superseded by the fresh exact-byte audit of the current candidate.

Other general repairs clarify force versus dice-pool choice, post-skull casualty bookkeeping, banishment’s no-Supply permission versus destination constraints, phase-power frequencies, resource readiness, initial card orientations and saved-board choice. The test’s numerical example is not inserted into the summary. Independent semantic adjudications retain initial grades before any revision; sources and same-entry evidence, not desired scores, determine outcomes.

Iteration10 retained its oversized original packet and two abandoned whole-pair attempts, including [v1 constraint](expanded-iteration-10/transport-constraint-v1.json) and [v3 handoff](expanded-iteration-10/transport-constraint-v3.json). Neither attempt produced grades. Coordinator directed [six bounded disjoint blocks](expanded-iteration-10/grading-block-manifest.json), each with its complete snapshot and both complete original entries for only14–18fixed IDs, encoded through reversible dictionaries. Every field/quote reconstructs exactly. Each fresh Sol/high none block grader independently assesses its entries; root aggregation preserves every grade/finding and verifies full104/328 per reader with no duplicates/gaps, all hashes, actual delivery and model provenance. This is technical delivery repair, without reader feedback or rubric relaxation.

## Bank/key precision history

The original [seed-v1 questions/key](seed-v1/question-bank.md) remain intact. All question words/IDs are carried forward. Source-backed key changes are explicitly versioned: [v2](expanded-v2/key-corrections.json) for Search/Imperial-defense/facedown restrictions; [v5](expanded-v5/key-corrections.json) for Conspiracy’s target-player wording; [v8](expanded-v8/key-corrections.json) and [v9](expanded-v9/key-corrections.json) for the attacking-force ceiling and its duplicate structured field; [v10](expanded-v10/key-corrections.json) for already-asked first-game orientations confirmed by original diagrams; [v11](expanded-v11/key-corrections.json) for the actual-flip Chronicle guard. Prior keys, scopes and grades remain frozen to their own versions. No asked clause or contextual exclusion is removed to obtain passing scores.

Reviewer06’s independently discovered deferred-rebuild gap is retained in Q101, but a subsequent parent message disclosed its presence in the summary. [That disclosure](coverage-review-06-parent-disclosure.json) is recorded; reviewer06 is a historical discovery record, not the final independent saturation gate. Subsequent source-only reviewers remain isolated from summary/readers/grades.

The separately frozen [scope-v12 precision](grading-scope-v12/precision-changes.json) follows [fresh independent requested-scope adjudication09](expanded-iteration-08/scope-adjudication-09.json). Q058 requires no fact change; its one-card statement semantically conveys ordinary count and locality, and unchanged stopping rules were already context. Q088 moves only unasked title-allocation background from F02 into explicit context, keeping the bonus on any Imperial defense required. All104 question words, answer-key text and328 fact IDs remain. Initial08 scores stay A100/4/0 and B99/5/0; [adjudicated delta](expanded-iteration-08/adjudication-delta-09.json) gives A102/2/0 and B99/5/0. This remains a failure. Scope-v12 froze after09A but before grader09 and before all10readers; no09answers drove the correction. Source09 MINOR wording ambiguity is retained separately and repaired in10.

The [metadata-only redaction manifest](provenance-metadata-redaction-manifest.json) records before/after hashes for46 provenance files (27 full-runtime copies plus19 related context-bearing copies). [Metadata integrity validation](provenance-metadata-validation.json) reconstructs every before-hash from untouched external runtime records, checks retained identity/model/effort/fork fields and opaque source-record hashes, validates subsequent minimal refresh chains, and scans for copied private runtime payloads.257 existing gameplay files were unchanged at correction. No full-content backup was created. The [generator](capture-provenance.py) now saves only minimal projections and source path/ordinal/hash references. This metadata correction itself does not trigger semantic retesting; later gameplay revisions are separately frozen and source-audited.

## Provenance and handoff

The four assigned source originals are read-only and unchanged: [source hashes](source-input-manifest.json). Supplemental primary-source copies/hashes and honest publisher-link provenance are in [supplemental manifest](supplemental-source-manifest.json), [source provenance](source-provenance.json) and [official-resource link proof](official-resource-link-proof.json). Failed guessed downloads are explicitly unused; New Foundations resources are not imported.

Checks are scoped to this worker’s canonical file and evidence: source/key/scope/reader hashes, all IDs and prior-entry preservation, quote/whole-entry reconstruction, strict grade/fact totals, targeted repository structural validation, whitespace and merge-marker checks. Integrity-check counts do not stand in for semantic grading.

Coordinator accepted all final evidence, confirmed idempotent stamp changed:false and completed targeted catalog publication while preserving unrelated entries. Completion authorization and the unchanged tested/audited/stamped hash are recorded. This worker changed only its report/progress after acceptance; canonical, sources, keys, raw reader outputs, grades and shared files remain untouched.
