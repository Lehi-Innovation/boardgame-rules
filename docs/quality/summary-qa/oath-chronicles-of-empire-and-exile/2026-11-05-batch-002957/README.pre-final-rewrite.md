# Oath first-printing multiplayer summary QA — in progress

**Fresh complete-delivery source audit and full expanded blind-reader test: in progress. Historical coverage challenge: PASS working saturation; delivery proof is being rechecked.** This is not yet ready for coordinator stamping.

The canonical summary is `rules/oath-chronicles-of-empire-and-exile.md`. Scope: 2021 base first printing, Law October 20, 2020, corresponding full Playbook, official base errata November 15, 2022 and Site Reference. All four Oaths/Visions, Empire, campaigns, citizenship, victory, Chronicle and later setup are included. Clockwork Prince and New Foundations are excluded.

The complete [expanded-v5 bank](expanded-v5/question-bank.md) contains 100 retained regression questions. Ten historical overlaps receive zero novelty credit; no prior ID is removed. The total is incidental, not a quota or cap. [Questions](expanded-v5/questions.json) and [key](expanded-v5/answer-key.json) are frozen. Key wording clarifications are explicitly recorded in [v2](expanded-v2/key-corrections.json) and [v5](expanded-v5/key-corrections.json), with prior versions preserved.

The [coverage ledger](coverage-ledger.json) records additions, rejections, all procedural source mappings and successive failed saturation challenges. Root passes 15/16 added zero; a [new independent source/key reviewer](coverage-review-05.json) challenged the complete 100-question bank and returned PASS working saturation. It did not see summary/readers/grades. [The exact ledger it reviewed](coverage-ledger-reviewed-05.json) preserves its input hash.

A separate fresh [source auditor](expanded-iteration-01/source-audit.json), given only candidate summary and authoritative sources, checked 41 claim groups and returned PASS with zero findings. It has not authored repairs or seen questions, keys, reader answers or grades. The audited snapshot SHA-256 is `a2e5081f25d4b77d16defe06f1a5dced3d473c5411ada1a2c90d8c9fdea8620f` covers the preserved candidate-01 snapshot. The canonical has since received a goal-presentation repair separating Oaths, Visions and Citizen Successor criteria; candidate-02 has received a fresh source-audit PASS and still requires exact-text blind tests. No rules or question/key facts changed. Blind-reader completion remains required.

## Seed iterations

Original [seed-v1 bank/key](seed-v1/question-bank.md) remain unchanged and hashed. Scores are complete-answer counts in correct/partial/incorrect order. All reader outputs and failures remain saved.

| Iteration | Reader A C/P/I | Reader B C/P/I |
|---|---|---|
| seed-iteration-01 | 14/6/0 | 15/5/0 |
| seed-iteration-02 | 14/6/0 | 14/6/0 |
| seed-iteration-03 | 16/2/2 | 19/1/0 |
| seed-iteration-04 | 17/3/0 | 19/0/1 |
| seed-iteration-05 | 19/1/0 | 18/1/1 |
| seed-iteration-06 | 20/0/0 | 18/2/0 |
| seed-iteration-07 | 20/0/0 | 19/1/0 |
| seed-iteration-08 | 18/1/1 | 17/3/0 |
| seed-iteration-09 | 19/0/1 | 19/0/1 |
| seed-iteration-10 | 18/0/2 | 20/0/0 |
| seed-iteration-11 | 19/1/0 | 19/1/0 |
| seed-iteration-12 | 20/0/0 | 19/1/0 |
| seed-iteration-13 | 20/0/0 | 20/0/0 |

Early source audit found six material/minor findings; general source-supported repairs resolved those before the final independent PASS. Later reader failures include genuine missing details, ambiguous paraphrases and unsupported caveats even where summary text existed. New readers are used for every iteration. Borderline cases have separate independent adjudication; provisional scores are preserved where changed. No support label is treated as a grade and no requested fact is borrowed from another answer.

## Provenance and limits

[Assigned source hashes](source-input-manifest.json), [supplemental hashes](supplemental-source-manifest.json), [source provenance](source-provenance.json), [runtime model/effort proof](runtime-provenance.json), [reader access command records](reader-access-provenance.json), and [in-progress integrity checks](validation-in-progress.json).

Readers are fresh-context Luna/high, reviewers Sol/high, confirmed from local session metadata. Context isolation and explicit two-file access instructions are used, not an extra filesystem sandbox. Fixed-set regression success will not establish held-out accuracy or every conceivable card interaction. No shared catalog/audit registry, instruction, branch or machine-managed verification banner is modified by this worker. Coordinator stamping and exact-byte rechecks remain separate.


## Input delivery correction

The [runtime delivery audit](delivery-audit/decision.json) found truncated tool output in all 28 historical reader sessions. The saved historical scores above are not changed, but do not establish complete input delivery, including seed13's 20/20 pair. Expanded02 retains its generic/incomplete A draft and B's self-reported scenario-role error. No answer is upgraded because of a delivery failure. The new [expanded03 dispatch](expanded-iteration-03/reader-dispatch.json) gives both fresh readers identical technical instructions except identity/destination, with no key or rule feedback. Its [prompt comparison](expanded-iteration-03/prompt-comparison.json) confirms that equality.

[Reader A actual delivery](delivery-audit/expanded03_reader_a.verified-delivery.json) and [Reader B actual delivery](delivery-audit/expanded03_reader_b.verified-delivery.json) compare every displayed chunk against the frozen files: both files cover character0 through EOF without gaps or truncation. Saved actual tool records preserve the receipts. A fresh source auditor uses the same bounded delivery discipline. Summary bytes and the frozen100-question bank are unchanged.


## Expanded-v6: deferred setup prerequisite

The full-delivery [sixth challenge](coverage-review-06.json) found one bank gap: the deferred world-deck rebuild must precede setup discard seeding/adviser draws. Q101 adds that timing branch; repeated deck arithmetic receives zero new credit. [Expanded-v6](expanded-v6/question-bank.md) retains all100 prior questions/keys exactly, with101 total questions and320 requestedfacts. Existing319 scope entries are unchanged. The summary is unchanged and already states this prerequisite. Rootpasses18/19 found no further additions.

Reviewer06 identified the gap before a parent follow-up disclosed its presence in the summary. [That disclosure](coverage-review-06-parent-disclosure.json) is preserved, and reviewer06 is a historical discovery record only. Fresh reviewer07 receives sources/bank/ledger only and will supply the independent final challenge. Expanded03's full100 answers will still be graded and preserved; final certification now requires a new full101 pair.


## Expanded-v7: complete setup-clause challenge

[Reviewer07](coverage-review-07.json) received all sources/all101 keys without truncation and found two further setup gaps: role/seating assignment and the fixed first-game Supremacy reference. [Expanded-v7](expanded-v7/question-bank.md) retains all101 prior question/key/scope entries unchanged, adds Q102/Q103, and freezes103 questions/327 requestedfacts before fresh readers. Rootpasses21/22 add zero after these repairs; fresh reviewer08 remains pending.

The summary now explicitly states first-game Chancellor seating at the Cradle and that later Chancellor selection is by any method, with previous winner recommended only. [The change record](expanded-iteration-04/summary-change.json) cites the source clauses. Prior source-audit03 applies to the preserved old bytes; a fresh source-audit04 must certify the changed candidate. No verification banner was touched.


## Current iteration05 candidate

[Iteration04](expanded-iteration-04/results.json) failed A93/7/3 and B92/10/1 despite full input delivery. [Iteration05 changes](expanded-iteration-05/summary-changes.json) clarify reusable force/dice/casualty bookkeeping, banishment versus destination constraints, and related phase/site/next-game cross-references. No test's numerical example is inserted. The same103 questions and327 required facts are fixed in [v9](expanded-v9/question-bank.md). Its [final source-only key verification](coverage-review-08.final-verification.json) passes after preserving v8's incomplete duplicate-field correction. The expected-answer correction aligns a legacy field with the already-frozen force fact; no required fact changed.

Fresh [sourceaudit05](expanded-iteration-05/source-audit.json) passes exact SHA256 `f0a2d8c22acaeb43563f5470476ea3fb42cd9f17bb13525a971f3fca64487fec`, with complete source delivery and diagrams. Fresh readers05 receive only the frozen summary/questions, with identical generic clause-retrieval and brief scenario-state bookkeeping instructions; no IDs, expected facts, grades or rule hints are provided. Their full103 outputs and654fact grading remain required before readiness.
