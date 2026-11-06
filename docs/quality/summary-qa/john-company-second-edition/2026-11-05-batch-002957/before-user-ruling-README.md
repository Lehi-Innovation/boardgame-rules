# John Company: Second Edition — incomplete QA checkpoint

**Awaiting an authoritative source; unverified and not ready for stamping/publication.** November 5, 2026 (America/Phoenix). No complete-core PASS, 87/87 pair or final coverage closure is claimed. Goal status returned by the host: **blocked**, after the same genuine source dependency was revalidated across three actual goal turns.

Current bank: **[expanded-v6, 87 questions](expanded-v6/question-bank.md)**. Exact tested text: [iteration07 snapshot](expanded-v6/luna-iteration-07/summary-snapshot.md), byte-identical to canonical and audit12. Both final readers scored **86 Correct / 1 Partial / 0 Incorrect**. Their only Partial is Q015. A supplies every known requested fact and preserves the authority gap. B additionally omits known defense details and does not acknowledge the unresolved counting case. All grades remain unchanged.

| Check | Result |
|---|---|
| Independent source audit12 | **MAJOR overall**, known claims **PASS**, complete-core signoff **false**. Audit11’s MINOR sequencing ambiguity is resolved. |
| Supported-source coverage | All87 questions/key approved outside the essential gap, after zero-addition passes9/10 plus independent review06. Full closure remains **false**. |
| Reader regression | Incomplete: A86/1/0, B86/1/0. Q015 cannot receive Correct without authority; B also has actual omissions. |
| Input/model/artifact integrity | Source/key/frozen-input hashes, delivery, models, IDs and grade alignment checked; [validation](checkpoint-validation.json), [source hashes](checkpoint-source-integrity.json), [model proof](checkpoint-model-provenance.json). |
| Goal | **Blocked** after three actual goal turns; not paused or complete; [actual host-turn audit](goal-blocking-audit.json). |

Machine records: [checkpoint](checkpoint.json), [all remaining findings](checkpoint-findings.json), [progress](progress.json). No approved final snapshot is designated; the linked snapshot is an incomplete checkpoint.

## Remaining dependency and reader findings

**GAP-DEFENSE-OVERSHOOT**, coordinator alias **JC-DEFENSE-OVERSHOOT**: the only available active defense is a strength-2 local alliance against a strength-1 Crisis. Must that piece exhaust, does defense succeed, and how is unused excess counted/discarded?

Rules p22 forbids splitting alliance strength among more than one purpose. Page33 requires equal newly exhausted strength and says non-equality makes the Crisis succeed. The official player aid says defenders win ties but does not explicitly define this excess-counting case. Extensive publisher/designer/errata searches and the coordinator’s independent search found no exact authoritative ruling. Assigned sources and official components were obtained; this is source sufficiency, not an access failure.

A verifiable **publisher/designer clarification or corrected authoritative text answering that concrete case** is needed. Neither a verified greater-than-or-equal defense rule nor automatic loss from full-strength excess has been invented. [Source-gap evidence](source-gap.json) preserves primary passages, search evidence and the precise citation needed. No publisher contact or messages to other chats were sent.

The final pair’s remaining findings are:

| Reader / question | Finding |
|---|---|
| A / Q015 | Source-blocked Partial only; known requested defense procedure matches, and uncertainty is expressly preserved. |
| B / Q015 | Source-blocked Partial **plus** omission of the printed non-equality failure branch and alliance printed-strength/once-only/one-purpose constraints. The answer also leaves the excess-strength uncertainty unacknowledged, without asserting a verified >= ruling. |

The B omissions concern rules explicitly present in the current summary (canonical lines 213, 208); exact observed answers, criteria and current-rule quotations are in [checkpoint-findings.json](checkpoint-findings.json) and [B’s independent grade](expanded-v6/luna-iteration-07/grades-reader-b.json). They do not identify a missing or ambiguous supported rule in the current summary. Confidence/self-review labels do not excuse them. No grade is waived, and no facts are borrowed from other answers.

Known claims are source-accurate, the supported-source map is approved, and no additional meaningful input-independent rule repair is identified. Under the coordinator’s checkpoint instruction, further full-bank sampling is deferred: it cannot supply the missing authoritative ruling. This remains **incomplete**, with every failure retained. An authoritative citation would trigger a new explicit key/bank version, necessary rule repair, coverage review, fresh full-bank testing and exact-text source audit before coordinator verification/stamping.

## Source and scope

The complete assigned 48-page Rules of Play was read: **Second Edition game (2022), Second Printing 2023**, not the 2017 edition. Scope includes standard multiplayer, 1710, 1758, 1813, Long 1710 and Deregulation/firms. Crown solo/two-player and optional setup Draft are excluded. Printed card powers, starting holdings and scenario diagrams remain read from their components.

Official PNP board/setup components, publisher-linked errata and verified designer rulings supplement the assigned PDF/text. [Research notes](supplements/research-notes.md) retain authority/provenance; [source read record](source-read-record.json) retains scope and inspections. Unverified FAQs were not promoted over primary evidence. Verified designer rulings establish Foreign Invasion’s unrest exclusion and Company Fraud’s payout cap.

| Checkpoint input | SHA256 |
|---|---|
| Canonical = iteration07 = audit12 snapshot | `04219e8b7d48c4b01de073bacce1eea81061a43bdc176d06a8435e8cc7282e26` |
| expanded-v6 questions | `4d903a89bbadbed2e05b314b014286e4d75182f87415730477e7b88f15a04c94` |
| expanded-v6 key | `c8390e7acb5ecdf98760d97e07e7d97e2e491afc0ebaf9f7dd6b1175d12f7e7c` |
| Assigned extracted rules | `105ff1bb4a774e9cc62e068567fa611947cac134f9c7c2e5bf29cc482f5bd30f` |
| Assigned PDF | `29fdc157234951b517190c82298ea578a543d25f183224e9fa86c1ca8c470dd0` |

## Bank and coverage history

Seed 20 was frozen source-first before summary creation. Every earlier question ID/wording remains preserved; genuine source/key corrections create new versions. [Version checks](bank-version-validation.json), original manifests and each bank’s correction record preserve the trail.

| Version | Explicit change |
|---|---|
| seed-v1 | Original 20 questions and initial key retained. |
| seed-v2 / expanded-v2 | Company/firm half-revenue refills, target empire counted once, defended-Invasion attacker tower removal and Company bonuses clarified. Expanded-v2 also adds five independently found questions. |
| seed-v3 / expanded-v3 | Governor overlay remains on map; only office card goes to Vacant Offices. Expanded-v3 adds exact Stock Exchange costs to the key. |
| expanded-v4 | Designer-confirmed Company Fraud payout capped at actual Balance removed. |
| seed-v4 / expanded-v5 | Printed defense equality restored; essential excess-alliance authority gap explicitly retained. |
| expanded-v6 | Q084 Family priority, Q085 global office order, Q086 Events initiation/count, Q087 ordinary Crisis classifier added; Q038 corrected to forbid splitting among purposes without deciding excess counting. |

Coverage grew **20→70→78→83→87**. Later independent findings supersede historical zero-addition passes. After review05’s four additions, [passes9/10](coverage-passes-09-10.json) added zero and [independent review06](coverage-review-06.json) approved all source-supported coverage outside the authority gap. [Ledger](coverage-ledger.json) retains novelty, accepted candidates and rejections. This is working saturation under declared scope/novelty criteria, not proof of every conceivable case. Full closure remains false for the essential missing ruling.

## All reader iterations

Counts are **Correct / Partial / Incorrect** complete answers. All 20 pairs are fresh-context **gpt-6-luna/high**, explicit `fork_turns:none`; graders/source/coverage reviewers use **gpt-6.1-sol/high**. Actual runtime models/efforts and distinct sessions are in [all-reader verification](reader-model-verification.json) and [provenance](model-provenance.json). Instruction isolation was used within a shared filesystem.

| Frozen iteration / full grades | A C/P/I | B C/P/I |
|---|---|---|
| [expanded-v5/luna-iteration-01](expanded-v5/luna-iteration-01/results.json) | 70/12/1 | 67/15/1 |
| [expanded-v5/luna-iteration-02](expanded-v5/luna-iteration-02/results.json) | 79/3/1 | 76/7/0 |
| [expanded-v5/luna-iteration-03](expanded-v5/luna-iteration-03/results.json) | 77/4/2 | 73/9/1 |
| [expanded-v5/luna-iteration-04](expanded-v5/luna-iteration-04/results.json) | 73/10/0 | 79/4/0 |
| [expanded-v5/luna-iteration-05](expanded-v5/luna-iteration-05/results.json) | 76/5/2 | 79/2/2 |
| [expanded-v6/luna-iteration-01](expanded-v6/luna-iteration-01/results.json) | 84/3/0 | 84/3/0 |
| [expanded-v6/luna-iteration-02](expanded-v6/luna-iteration-02/results.json) | 83/4/0 | 83/4/0 |
| [expanded-v6/luna-iteration-03](expanded-v6/luna-iteration-03/results.json) | 85/1/1 | 84/3/0 |
| [expanded-v6/luna-iteration-04](expanded-v6/luna-iteration-04/results.json) | 83/4/0 | 84/3/0 |
| [expanded-v6/luna-iteration-05](expanded-v6/luna-iteration-05/results.json) | 86/1/0 | 84/3/0 |
| [expanded-v6/luna-iteration-06](expanded-v6/luna-iteration-06/results.json) | 84/3/0 | 85/2/0 |
| [expanded-v6/luna-iteration-07](expanded-v6/luna-iteration-07/results.json) | 86/1/0 | 86/1/0 |
| [seed-v1/luna-iteration-01](seed-v1/luna-iteration-01/results.json) | 12/7/1 | 12/5/3 |
| [seed-v2/luna-iteration-01](seed-v2/luna-iteration-01/results.json) | 19/1/0 | 19/0/1 |
| [seed-v3/luna-iteration-01](seed-v3/luna-iteration-01/results.json) | 17/2/1 | 18/2/0 |
| [seed-v3/luna-iteration-02](seed-v3/luna-iteration-02/results.json) | 16/3/1 | 19/1/0 |
| [seed-v3/luna-iteration-03](seed-v3/luna-iteration-03/results.json) | 20/0/0 | 19/1/0 |
| [seed-v3/luna-iteration-04](seed-v3/luna-iteration-04/results.json) | 19/1/0 | 18/2/0 |
| [seed-v3/luna-iteration-05](seed-v3/luna-iteration-05/results.json) | 19/1/0 | 20/0/0 |
| [seed-v3/luna-iteration-06](seed-v3/luna-iteration-06/results.json) | 20/0/0 | 19/1/0 |

Historical seed scores predate discovery of the essential source gap and do not establish core PASS. Seed-v1’s original independent grading is retained beside its source-key correction. Its original A schema/evidence defects remain unchanged and are disclosed in validation. Seed-v3 iteration02’s `results-format-error.json` is a retained grading-adapter failure, not an actual 0/20 reader test; real complete grades are in `results.json`. No failed responses were overwritten or discarded.

Graders check every requested material part, accept equivalent wording/clear implications, distinguish unasked key context, avoid cross-answer borrowing and flag unsupported guesses. Scope judgments remain in their original reports. Final quoted operative sentences count as answer content; references/evidence alone cannot fill missing answer facts. Both checkpoint graders found zero unsupported correct guesses.

## Delivery, review and source-audit trail

Iteration04 A’s combined read was truncated and follow-up reads skipped negotiations; the [delivery review](expanded-v5/luna-iteration-04/input-delivery-review.json) retains evidence. Both failed outputs/grades remain. B recovered its full input through follow-up chunks.

From expanded-v5 iteration05 onward, readers use bounded summary/question reads. The [checkpoint delivery proof](expanded-v6/luna-iteration-07/input-delivery-validation.json) confirms all 476 summary lines and all 87 question texts reached each current reader without truncation. Complete delivery does not prove perfect attention or understanding.

Later protocols requested numbered subanswers, then retained first-pass drafts plus blind self-review, and finally small question batches with full operative summary facts in answers. No answer key, source rulebook, prior reader output or evaluator feedback was supplied. [Protocol notes](expanded-v6/luna-iteration-05/protocol-note.json) and each iteration’s draft/final validation retain these changes. [Checkpoint review validation](expanded-v6/luna-iteration-07/self-review-validation.json) distinguishes factual edits from the reported all-answer numbering pass. These method/summary changes prevent a controlled model-performance comparison claim; this is a fixed regression exercise, not held-out generalization evidence.

Audits01–03 passed historical snapshots. Audits04–10 retained MAJOR completeness/source-gap findings while passing known claims. [Audit11](source-audit-11/source-audit.json) additionally caught a MINOR overlapping scoring directive introduced in a clarity revision. That text/finding remains preserved. [Audit12](source-audit-12/source-audit.json) independently resolves it: row1 refers to row2, where the single retirement occurs. Known claims PASS, no new findings, overall MAJOR/complete-core false solely for the authority gap.

## Validation and status

Targeted repository validation and scoped `git diff --check` pass; authored text/JSON and report links are checked. [Checkpoint integrity](checkpoint-validation.json) covers immutable source/question/key/snapshot hashes, every ID once, grade/response alignment, original historical hashes and current snapshot identity. [Latest-audit source integrity](checkpoint-source-integrity.json) verifies all eight recorded primary/supplement source hashes. [Immutable artifact inventory](checkpoint-immutable-artifact-hashes.json) fingerprints retained benchmark inputs, raw responses/drafts, grade reports and audits.

The canonical remains `unverified` with no verification date. No commits, pushes, worktrees, new chats, shared catalog/audit-registry edits, stamping or publication were performed. The host returned **blocked** after the original goal turn and two goal continuations revalidated the same authority gap, unchanged canonical text and no remaining independent work. The goal was not marked paused or complete. The batch may continue other games while this precise source dependency awaits input.
