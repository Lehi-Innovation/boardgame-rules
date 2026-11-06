# John Company: Second Edition — user table ruling added; QA incomplete

**Current revision — user instruction accepted:** The user supplied the general defense-strength rule and requested attribution as their interpretation. The canonical now uses total exhausted defense strength **equal to or greater than** attack strength for a failed Crisis. [Decision and exact revision](user-interpretation-defense-strength-2026-11-05.json). No further citation is requested. The reports and scores below describe the previous frozen text; the new revision has not received an independent retest or verification stamp.

The requested table interpretation is implemented: an active strength-2 local alliance successfully defends a strength-1 Crisis by exhausting the whole piece. Normal successful-defense results apply, and the alliance cannot be used again that turn. The summary labels the decision as **user-approved**, limits it to this concrete case, and keeps official verification pending. [Recorded user decision](user-ruling-decision.json).

Independent source/attribution audit13 passes the published claims and the new table interpretation as written. Independent bank review07 approves the separately attributed supplement. Both fresh readers answer Q088 correctly. The full regression remains **FAILED**, and official excess-alliance counting remains unresolved; the canonical is **unverified**. No complete-core PASS or final coverage closure is claimed.

| Current check | Result and evidence |
|---|---|
| Exact tested text | [Frozen snapshot](expanded-v7-table-ruling/luna-iteration-01/summary-snapshot.md), byte-identical to canonical and audit13. SHA256 `c0369248da5d80e610fbc8eb054281594086c3e3abf451e218384ae473ad04db`. |
| Official sourced claims | **PASS**; [independent audit13](source-audit-13/source-audit.md) finds no new factual errors. |
| User interpretation | **PASS** for whole-piece exhaustion, normal benefits, one-use limit, attribution and concrete-case scope. Official completeness remains **MAJOR** solely for the authority gap. |
| Bank | [88 questions](expanded-v7-table-ruling/question-bank.md). All 87 prior question and full key entries are exactly unchanged; Q088 adds only the user-case decision/results/authority test. [Preservation proof](user-ruling-bank-preservation.json), [independent review07](coverage-review-07-user-table.md). |
| Blind reader A | **86 Correct / 1 Partial / 1 Incorrect**; [independent grades](expanded-v7-table-ruling/luna-iteration-01/grades-reader-a.json). |
| Blind reader B | **84 Correct / 3 Partial / 1 Incorrect**; [independent grades](expanded-v7-table-ruling/luna-iteration-01/grades-reader-b.json). |
| Added Q088 | **Correct for both**. User authority remains separate from publisher/designer authority. |
| Formal QA | **Incomplete**; [all current grades](expanded-v7-table-ruling/luna-iteration-01/results.json), [checkpoint](checkpoint.json). Q015 retains its original official-source limitation. |
| Integrity and format | [Final validation](user-ruling-final-validation.json), [all-run integrity](user-ruling-run-integrity-final.json), [immutable evidence inventory](user-ruling-immutable-artifact-hashes.json). Structural validation and scoped whitespace checks pass. |

The current non-Correct answers are retained in full, with exact reader/summary quotations and every material criterion in [checkpoint findings](checkpoint-findings.json):

| Reader / question | Finding |
|---|---|
| A / Q015 — Partial | Official source-blocked. Known requested procedures are covered, but the answer omits the official excess-counting boundary. |
| A / Q082 — Incorrect | Opens with “Yes” to keeping a capital's starred flag, then correctly says to remove it. The direct answer contradicts its own explanation and the explicit summary. |
| B / Q015 — Partial | Official source-blocked, plus an unstated normal primary attack base and an unqualified unequal-strength conclusion. |
| B / Q024 — Partial | Omits concrete starting-holding destinations. |
| B / Q033 — Incorrect | Assigns hiring the Director to the Director; the Chairman hires the Director. |
| B / Q074 — Partial | Names the three 1813 control tokens without their Presidency destinations. |

Independent review found no supported summary defect causing these reader failures. The relevant rules are explicit. Under the coordinator's checkpoint instruction, this run stops after preserving the current grades rather than resampling accurate text. Grades are not waived, and Q088's correct answer cannot fill omissions in Q015 or another answer.

The source gap remains **GAP-DEFENSE-OVERSHOOT / JC-DEFENSE-OVERSHOOT**. Printed p22 provides Army-piece status, alliance strength, one-use timing and the single-purpose restriction. Page33 uses equality and non-equality language without explicitly reconciling excess printed alliance strength. The official aid supports the successful-defense reading. The [source-gap record](source-gap.json) retains the evidence and prior searches; the user decision selects the concrete outcome for this table without closing official-source verification. An authoritative clarification is still required for official completeness, followed by any warranted source/key revision, required QA and final exact-text audit before coordinator stamping.

Both readers were fresh-context **gpt-6-luna/high**, `fork_turns:none`, using only frozen summary/questions and their own draft/final. Independent graders, source auditor and supplement reviewer were **gpt-6.1-sol/high**. [Actual runtime provenance](user-ruling-model-provenance.json) confirms six distinct sessions. [Dispatch records](user-ruling-agent-dispatches.json) and [all-reader verification](reader-model-verification.json) retain the model trail. Isolation was instructional within the shared filesystem.

[Input-delivery validation](expanded-v7-table-ruling/luna-iteration-01/input-delivery-validation.json) confirms all 482 summary lines and all 88 questions reached each reader without truncation. The initial scan's six B false negatives were exact ASCII-escaped JSON question strings; that [original scan](expanded-v7-table-ruling/luna-iteration-01/input-delivery-validation-initial.json) remains retained. [Draft/self-review checks](expanded-v7-table-ruling/luna-iteration-01/self-review-validation.json) confirm all IDs, retained complete drafts and reported changes. These checks establish delivery/artifact consistency, not correctness or perfect attention.

There are now 21 retained full-bank pairs. All prior 20 pairs, failures, genuine key corrections, coverage saturation work and source audits remain described in the [preserved earlier report](before-user-ruling-README.md). Its 87-question scores and audit12 apply to the previous bytes, not this revision. The [previous checkpoint](before-user-ruling-checkpoint.json) and original 310-file immutable inventory remain unchanged. Current [source integrity](user-ruling-source-integrity.json) checks all 31 audit13 manifest inputs. Method and text changes prevent a controlled model-performance comparison claim.

The user resumed the goal and this turn completed the authorized table change and reviews. The earlier three-turn blocking record is preserved; its threshold is not reused after resumption. The broader verification goal remains incomplete. [Progress](progress.json), [fresh resumed-turn audit](goal-blocking-audit.json). No stamping, publication, shared registries/catalogs, commits, pushes or messages to other chats were performed.

The host has now set the goal to **blocked** after the same official-source dependency persisted through three actual turns since user resumption. The [fresh blocking audit](goal-completion-audit-resumed-turn03.json) records requirement-by-requirement evidence and terminal worker status. The user table ruling remains complete; full formal QA, official completeness and final stamping remain unmet.
