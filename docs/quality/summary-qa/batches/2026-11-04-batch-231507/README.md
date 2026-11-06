# Multi-game rules-summary QA batch

Run `2026-11-04-batch-231507`. Updated 2026-11-06T04:26:39.324453-07:00.

At most three game chats run concurrently, in the existing local checkout. Game evaluators/reviewers use gpt-6.1-sol/high; blind readers use gpt-6-luna/high. No commits or pushes are authorized.

| Game | Questions | Iterations | Final reader scores | Source audit | Status | Chat | Evidence |
|---|---:|---:|---|---|---|---|---|
| Nemesis | 127 | 19 trials (18 pairs) | A: 127/127; B: 127/127 | PASS (source fidelity only) | awaiting-source: known-rule-QA-stopped-native-goal-blocked-on-primary-authority | [Rules QA — Nemesis](codex://threads/01a1aa59-7f47-7aa0-b41e-cdb1bdbea5fa) | [Report](/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/nemesis/2026-11-04-batch-231507/README.md) |
| Pandemic | 39 | 10 | A: 39/39; B: 39/39 | PASS | complete | [Rules QA — Pandemic](codex://threads/01a1aa59-9cbf-7673-878d-28aedbe910c3) | [Report](/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/pandemic/2026-11-04-batch-231507/README.md) |
| Orleans | 60 | 10 | A: 60/60; B: 60/60 | PASS | complete | [Rules QA — Orléans](codex://threads/01a1aa59-bae3-71a3-afd7-182f8b7a1490) | [Report](/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/orl-ans/2026-11-04-batch-231507/README.md) |
| Obsession | 62 | 14 | A: 62/62; B: 62/62 | PASS | complete | [Rules QA — Obsession](codex://threads/01a1aa94-b6a2-7823-9d8b-2b4a666d8223) | [Report](/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/obsession/2026-11-04-batch-231507/README.md) |
| Scythe | 63 | 19 | A: 63/63; B: 63/63 | PASS | complete | [Rules QA — Scythe](codex://threads/01a1aac5-76e9-7752-846f-420015969a30) | [Report](/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/scythe/2026-11-04-batch-231507/README.md) |
| El Grande | 54 | 11 trials (10 pairs) | A: 54/54; B: 54/54 | PASS (source fidelity only) | awaiting-source: supported-source-qa-finished-awaiting-authoritative-clarification | [Rules QA — El Grande](codex://threads/01a1aae3-a2a3-70f3-80bf-7dc6cc814c6a) | [Report](/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/el-grande/2026-11-04-batch-231507/README.md) |
| Dead Last | 27 | 10 | A: 27/27; B: 27/27 | PASS (source fidelity only) | awaiting-source: bounded resumed research and fresh source-only applicability/key review finished; English essential gaps remain | [Rules QA — Dead Last](codex://threads/01a1ab26-bd68-7da0-a839-5f50c7d304ef) | [Report](/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/dead-last/2026-11-04-batch-231507/README.md) |
| Dune Imperium | 76 | 9 | A: 76/76; B: 76/76 | PASS | complete | [Rules QA — Dune Imperium](codex://threads/01a1ab6c-b248-72b2-988a-bb4a70bda3e3) | [Report](/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/dune-imperium/2026-11-04-batch-231507/README.md) |
| Dune Imperium Uprising | 101 | 26 | A: 101/101; B: 101/101 | PASS | complete | [Rules QA — Dune Imperium Uprising](codex://threads/01a1ab7a-6016-7731-81ac-bfdc0de86fca) | [Report](/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/dune-imperium-uprising/2026-11-04-batch-231507/README.md) |
| Ark Nova | 95 | 27 | A: 95/95; B: 95/95 | PASS | complete | [Rules QA — Ark Nova](codex://threads/01a1ab7c-ee08-7cb0-8872-e960cd8afe42) | [Report](/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507/README.md) |

Iterations count trials with actual saved reader responses, including stopped partial drafts; prepared but undispatched candidates and copies of an existing pair are excluded. Complete pairs are identified separately when a trial is partial. Historical invalid or nonpassing trials remain in the count and evidence.

## Outstanding external inputs

- **Nemesis:** SG01: all eight Adult models in Combat when another must be placed; SG02: Queen-generated Egg after Nest destruction; SG03: ordered Contamination handling on a missed Egg Melee; SG04: later Character death after manual Pod relocking. Precise original-game primary rulings remain missing. The complete physical-card corpus is not established; source fidelity covers included readable claims only. Full-core verification and stamping remain withheld.
- **El Grande:** Complete-core QA remains incomplete. The final audit flags essential unresolved classic-English rulings: return-action/secret-choice shortfalls, actor disk participation, Court shortage, Movement-to-Castillo, mobile4Castillo scoring and multi-origin other-region semantics. Bounded primary-authority research has not established applicable definitive rulings. Exact requests are in source-gap-register.json; do not promote/stamp complete-core PASS.
- **Dead Last:** Polishp4 explicitly defines a localized multiway fallback, but applicability as an EnglishRules2.0 amendment is not established. Original BGG post author/date/full context remain unverified; all-Ambush outcome and extra endgame Showdown pot supply still lack explicit applicable rulings. No full-core stamping/promotion.

Completion requires working coverage saturation in the documented source/scope, a resolved independent coverage challenge, two fresh full-bank Luna N/N results, independent source-audit PASS, verified model/input integrity, exact canonical snapshot equality, and repository checks. A partial result remains incomplete. This does not prove every conceivable scenario is covered.

Dead Last’s 27/27 figures are factual quiz results including Q26, which correctly reports that the booklet omits a multiway Showdown procedure. That answer does not resolve the missing gameplay ruling; full-core completion remains awaiting-source.

See [manifest](manifest.json), [identity/source decisions](identity-and-source-decisions.md), [initial checkout status](initial-git-status.txt), and [initial catalog check](initial-catalog-check.txt). Shared-file baseline copies are in `baseline-shared/`; worker assignments and historical failed iterations must remain intact.
