# Q015 independent requested-scope review

Created: 2026-11-05T16:26:15.905132+00:00

Both complete raw answers are **Correct for Q015’s requested facts**. Applying the original key’s unconditional source-gap cap mechanically gives **Partial** for each. These are new independent judgments, not retrieved prior grades. The official excess-alliance counting uncertainty remains separate and does not establish complete core approval.

## Exact question

When Company regions face a Crisis, which regions are attacked, in what order and at what strength? How is defense mounted and what happens on successful defense?

## Applicable original scope and policy

```json
{
  "questions_metadata": {
    "game": "John Company: Second Edition",
    "scope": "Complete multiplayer core and all standard scenarios, including deregulation and firms. Crown/solo/two-player and optional setup draft excluded. Explicitly labelled user-approved table case is tested separately from official-source verification.",
    "benchmark_version": "expanded-v7-table-ruling"
  },
  "key_policy": {
    "benchmark_version": "expanded-v7-table-ruling",
    "grading_standard": "Correct: every requested material fact resolved correctly, without contradictory caveat and supported by summary. Partial: material omission or abstention, no material contradiction. Incorrect: material contradiction. Judge each answer separately; do not import facts from other answers. Flag unsupported correct guesses separately. Equivalent wording accepted.",
    "source_gap_grading": "Q015 cannot be Correct while GAP-DEFENSE-OVERSHOOT remains unresolved. With no known-rule contradiction, grade Partial and separately identify known omissions versus the source gap. A material contradiction on a known procedure is Incorrect under the general standard; the authority gap never excuses a reader error. Do not claim N/N or complete core PASS."
  }
}
```

## Exact complete original key entry

```json
{
  "id": "Q015",
  "expected_answer": "Resolve primary attack first, then secondary Rebellions in every other Company-controlled region with unrest, Bombay/Madras/Bengal Army order with each Commander choosing order in its Presidency. A normal primary Crisis uses ordinary Invasion/Rebellion attack strength plus target unrest; other regions attack with only local unrest. Use the printed Mounting Defense procedure: exhaust active Army pieces equal to Crisis strength or as many as possible. The book says the Crisis succeeds when newly exhausted pieces do not equal that strength. A matched defense removes all target unrest and gives the Commander one trophy; if a normal primary Invasion failed, also remove one attacker tower if possible. Vacant Commander: Military Affairs acts, then Chairman if vacant, and acting player gains/loses no trophies. The source does not settle how an indivisible strength-2 alliance counts against a strength-1 attack; that concrete survival branch remains unresolved, not a verified >= ruling.",
  "source_references": "Rules p33; lines 2262–2296; Rules p33 lines2290–2296; source-gap.json; supplements/defense-and-fraud-rulings.json; coverage-review-04.json",
  "novelty": "Crisis propagation and compulsory defense.",
  "source_gap": "GAP-DEFENSE-OVERSHOOT",
  "grading_limit": "Retain this ID and grade all sourced parts. A complete core defense ruling cannot be signed off while the exact excess-alliance branch is unresolved; record source-blocked Partial separately from reader omissions."
}
```

## Reader A: complete raw Q015 entry and input metadata

```json
{
  "inputs_read": [
    "/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v7-table-ruling/luna-iteration-01/summary-snapshot.md",
    "/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v7-table-ruling/luna-iteration-01/questions.json"
  ],
  "complete_raw_Q015_entry": {
    "id": "Q015",
    "answer": "Resolve primary Crisis first, then secondary rebellions in every other Company region with unrest, in Bombay→Madras→Bengal Army order; each Commander sets order of associated regions. Primary normal Crisis strength is its usual attack strength plus target unrest; primary Foreign Invasion uses only its ordinary die; each secondary Rebellion uses only that region’s unrest cubes. Defense is chosen by associated Commander; if vacant Military Affairs acts, and if both vacant Chairman chooses. Exhaust active Army pieces equal to strength or as many as possible. Equal newly exhausted strength defeats attack, clears all target unrest, gives actual Commander one trophy (substitutes no trophies); if normal primary Invasion, remove one attacker tower if possible. Non-equal means attack succeeds and Region Loss; successful primary Invasion also applies empire growth.",
    "support": "supported",
    "evidence": [
      {
        "summary_location": "Events in India — Attacks on Company and mounting defense",
        "quote": "An Invasion or Rebellion against a Company region also triggers secondary Rebellions in every other Company region with unrest. Resolve attacks in this order: **primary Crisis first**, then secondary regions in **Bombay → Madras → Bengal** Army order. **Within each Presidency, that Commander chooses the order of its associated regions.**"
      }
    ]
  }
}
```

## Reader B: complete raw Q015 entry and input metadata

```json
{
  "inputs_read": [
    "/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v7-table-ruling/luna-iteration-01/summary-snapshot.md",
    "/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v7-table-ruling/luna-iteration-01/questions.json"
  ],
  "complete_raw_Q015_entry": {
    "id": "Q015",
    "answer": "Company-directed Invasion/Rebellion first resolves the primary Crisis, then secondary Rebellions in every other unrest Company region, Bombay→Madras→Bengal; within a Presidency its Commander orders regions. Primary normal Crisis strength includes target unrest; Foreign Invasion primary uses ordinary attack die with no unrest; secondary strength is only that region's unrest. Associated Commander chooses/exhausts pieces; if vacant Military Affairs acts instead, and if both vacant Chairman chooses; substitutes gain/lose no trophies. Exhaust active pieces equal strength or as many as possible. Exact equality means attack fails/defense succeeds, clears all target unrest, actual Commander gains one trophy (substitutes none); if defeating normal primary Invasion remove one attacker tower if possible. Unequal means attack succeeds and Region Loss follows.",
    "support": "supported",
    "evidence": [
      {
        "summary_location": "§ VII. Attacks on Company",
        "quote": "Resolve attacks in this order: primary Crisis first"
      }
    ]
  }
}
```

## Ordered requested-fact matrix

Every quote below comes from that reader’s answer field. Evidence arrays and support labels do not fill omissions.

1. **The primary Company-region target and every other Company-controlled region with unrest are attacked.**
   - A — Satisfied: “Resolve primary Crisis first, then secondary rebellions in every other Company region with unrest”
   - B — Satisfied: “Company-directed Invasion/Rebellion first resolves the primary Crisis, then secondary Rebellions in every other unrest Company region”
   - Summary lines 194–194; Rules p33, extracted lines 2264–2268.
   - Explicitly answered by both readers.

2. **Primary Crisis first.**
   - A — Satisfied: “Resolve primary Crisis first”
   - B — Satisfied: “first resolves the primary Crisis”
   - Summary lines 194–194; Rules p33, extracted lines 2270–2273.
   - Explicitly answered by both readers.

3. **Secondary attacks follow Bombay, Madras, Bengal Army order.**
   - A — Satisfied: “in Bombay→Madras→Bengal Army order”
   - B — Satisfied: “Bombay→Madras→Bengal”
   - Summary lines 194–194; Rules p33, extracted lines 2270–2273.
   - Explicitly answered by both readers.

4. **Each Commander chooses the order within the associated Presidency.**
   - A — Satisfied: “each Commander sets order of associated regions”
   - B — Satisfied: “within a Presidency its Commander orders regions”
   - Summary lines 194–194; Rules p33, extracted lines 2270–2273.
   - Explicitly answered by both readers.

5. **A normal primary Crisis retains the normal Invasion/Rebellion strength and adds target unrest.**
   - A — Satisfied: “Primary normal Crisis strength is its usual attack strength plus target unrest”
   - B — Satisfied: “Primary normal Crisis strength includes target unrest”
   - Summary lines 196–196; Rules p33, extracted lines 2280–2284.
   - A explicitly gives the additive formula. B calls it the primary normal Crisis strength and says it includes target unrest; this clearly retains normal Crisis strength while incorporating unrest. B does not say the strength is only unrest, and its explicit only for secondary strength reinforces the distinction. This is accepted equivalent wording, not facts borrowed from A. Neither the question nor original key requires re-expanding the underlying ordinary Invasion/Rebellion formula here.

6. **Secondary Rebellion strength is only that region’s unrest.**
   - A — Satisfied: “each secondary Rebellion uses only that region’s unrest cubes”
   - B — Satisfied: “secondary strength is only that region's unrest”
   - Summary lines 198–198; Rules p33, extracted lines 2280–2284.
   - Explicitly answered by both readers.

7. **Associated Commander chooses the Army pieces to exhaust.**
   - A — Satisfied: “Defense is chosen by associated Commander”
   - B — Satisfied: “Associated Commander chooses/exhausts pieces”
   - Summary lines 204–208; Rules p33, extracted lines 2286–2288.
   - Explicitly answered by both readers.

8. **If Commander is vacant, Military Affairs acts; if both are vacant, Chairman chooses.**
   - A — Satisfied: “if vacant Military Affairs acts, and if both vacant Chairman chooses”
   - B — Satisfied: “if vacant Military Affairs acts instead, and if both vacant Chairman chooses”
   - Summary lines 205–206; Rules p33, extracted lines 2275–2278.
   - Explicitly answered by both readers.

9. **Exhaust active Army pieces equal to Crisis strength, or as many as possible.**
   - A — Satisfied: “Exhaust active Army pieces equal to strength or as many as possible”
   - B — Satisfied: “Exhaust active pieces equal strength or as many as possible”
   - Summary lines 208–208; Rules p33, extracted lines 2286–2289.
   - Both give compulsory exhaustion, active status, equality and the as-many-as-possible fallback. B’s immediately preceding Associated Commander chooses/exhausts pieces establishes the Army-defense context; no different pool is suggested.

10. **Under the printed comparison, matched defense makes the attack fail.**
   - A — Satisfied: “Equal newly exhausted strength defeats attack”
   - B — Satisfied: “Exact equality means attack fails/defense succeeds”
   - Summary lines 212–213; Rules p33, extracted lines 2286–2292.
   - Both report the printed comparison correctly. Neither specifies how an indivisible alliance’s printed strength is counted against a weaker attack. Their equality/inequality sentences do not explicitly decide that separate counting question or claim an official ruling for it.

11. **Remove all unrest in the attacked region.**
   - A — Satisfied: “clears all target unrest”
   - B — Satisfied: “clears all target unrest”
   - Summary lines 212–212; Rules p33, extracted lines 2291–2292.
   - Explicitly answered by both readers.

12. **Actual Commander gains one trophy; acting substitutes gain or lose none.**
   - A — Satisfied: “gives actual Commander one trophy (substitutes no trophies)”
   - B — Satisfied: “actual Commander gains one trophy (substitutes none)”
   - Summary lines 205–206; Rules p33, extracted lines 2275–2278.
   - A’s substitutes no trophies expresses the no-trophy consequence. B additionally explicitly says substitutes gain/lose no trophies. The trophy award is also anchored at summary line 212 and source lines 2291–2292.

13. **If a normal primary Invasion is defeated, remove one attacker tower if possible.**
   - A — Satisfied: “if normal primary Invasion, remove one attacker tower if possible”
   - B — Satisfied: “if defeating normal primary Invasion remove one attacker tower if possible”
   - Summary lines 212–212; Rules p33, extracted lines 2294–2297.
   - Explicitly answered by both readers.

## Independent answer judgments

| Reader | Requested scope | Original key mechanically applied | Material omissions | Material contradictions |
|---|---|---|---|---|
| A | Correct | Partial: unconditional source-gap cap | None | None |
| B | Correct | Partial: unconditional source-gap cap | None | None |

B’s “Primary normal Crisis strength includes target unrest” clearly retains the normal Crisis baseline while adding its unrest component. The explicit contrast with secondary strength being “only” local unrest supports this reading from B’s own answer. The original key also uses ordinary Invasion/Rebellion strength rather than requiring a fresh expansion of all ordinary formulas.

Both include the summary-supported Foreign Invasion die/no-unrest exception. Both correctly give the non-equality/Region Loss converse. A also includes empire growth after a successful attacking Invasion; B’s absence of that extra is not an omission from the question about successful defense. Neither response contains a known-rule contradiction or unsupported correct guess in the requested facts.

## Scope and authority boundary

Q015 does not name alliances, a strength-2 piece, a strength-1 attack, excess strength, or an official verification caveat. Its top-level scope expressly says the labelled table case is tested separately. Do not require a volunteered numerical edge case merely because the expected-answer context mentions it. The one-use/non-splitting alliance detail and full Region Loss expansion are also contextual here; neither answer excludes alliances, authorizes splitting, or permits reuse.

The responses’ equality and inequality statements reproduce the printed comparison (Rules p33 lines 2286–2292; frozen summary lines 208–215). Neither explicitly counts a particular indivisible alliance against a weaker attack. It would be speculative to convert those generic statements into an explicit rejection of the adopted 2-versus-1 table case. An express assertion that the table’s 2-versus-1 defense fails would warrant a separate contradiction finding.

The frozen summary says at line 215: “For this summary’s user-approved strength-2-alliance versus strength-1-Crisis case, exhaust the whole active alliance and treat the defense as successful”. Line 452 limits that interpretation to the stated case and says it is not a publisher/designer ruling; line 458 keeps official counting verification open. This review does not settle that official question, grant a general >= rule, claim N/N, or approve complete official core coverage.

## Precise proposed key corrections

- **answer-key.json::source_gap_grading**: The unconditional Q015 cannot be Correct rule turns an overall official-source-completeness gate into a reader-correctness gate even when this fixed question’s material facts are answered.

  Proposed text: Grade Q015 independently against its expressly requested regions, order, attack strengths, defense procedure and successful-defense consequences under the general grading standard. Do not automatically cap the answer at Partial solely because GAP-DEFENSE-OVERSHOOT remains unresolved. Record that gap separately as blocking complete official core-defense verification. A missing, unsupported or contradictory fact actually requested by Q015 still affects its grade; a response that explicitly decides an excess-alliance counting case must be assessed against the stated authority and table scope.

- **answer-key.json::answers[Q015].grading_limit**: Complete-core signoff and correctness of this fixed answer have different scopes; source-blocked Partial is not justified without an actually asked unresolved branch.

  Proposed text: Retain Q015 and grade all its requested facts. Record GAP-DEFENSE-OVERSHOOT separately as preventing complete official core-defense signoff. Do not impose a question-level Partial solely for an unasked excess-alliance numerical branch.

- **answer-key.json::answers[Q015].expected_answer, final sentence**: Valid official-source boundary, but an unasked numerical counting branch and authority caveat should not be a compulsory volunteered answer element. For this checkpoint it also needs to acknowledge the summary’s separately labelled, accepted table solution rather than imply that the stated case remains unresolved for play here.

  Proposed text: Context only, not a required Q015 answer element: official excess-alliance counting remains unverified. The frozen summary separately adopts successful defense for a strength-2 alliance versus strength-1 Crisis as a user-approved table interpretation; it is not an official ruling and does not establish a general >= rule.

Preserve the existing general grading standard and questions scope: they already distinguish every requested material fact, equivalent wording, and separate table-case testing. Preserve the source-gap identifier as an audit concern; remove only its automatic reader-grade consequence and the implied compulsory volunteered caveat. No canonical file was changed.

## Evidence and uncertainty

The JSON contains the exact relevant rulebook excerpt, line-anchored summary evidence, all complete raw responses, and per-input SHA256 values. The rulebook’s wording supports equality and failure/success consequences, but does not expressly decide the concrete alliance overshoot. The frozen summary’s linked Foreign Invasion designer ruling was not independently opened; its no-unrest rule is assessed against the allowed frozen summary.

## Input SHA256s

- `questions` — `e8e14031e40ca3f6bc12ead96ff5bb43d6246e13388da43884c16372c204fe82` — /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v7-table-ruling/questions.json
- `answer_key` — `cae47182972bfa1f9679d158567f9238ca2d5199ddad91bc3bfdc364b5b0f0ac` — /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v7-table-ruling/answer-key.json
- `reader_a` — `a3a4ab7f6d36287a6d627f8df11a607243457f66e3d1819b96cdedaa931e225b` — /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v7-table-ruling/luna-iteration-01/reader-a.json
- `reader_b` — `1b2ceb4c27cfbfcbd0fcc0586283562c1df3d678a5879b10421784e02f5eb6e1` — /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v7-table-ruling/luna-iteration-01/reader-b.json
- `summary` — `c0369248da5d80e610fbc8eb054281594086c3e3abf451e218384ae473ad04db` — /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v7-table-ruling/luna-iteration-01/summary-snapshot.md
- `authoritative_rules` — `105ff1bb4a774e9cc62e068567fa611947cac134f9c7c2e5bf29cc482f5bd30f` — /home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

## Delivery verification

All 482 frozen-summary lines were read in chunks of at most 60 summary lines per response. All 13 ordered requested facts were checked independently against both answer fields; each quoted string was verified as an exact substring of that reader’s answer. Complete question, key, raw answers and input metadata are preserved without truncation. No other IDs’ answer content, prior grades, reports, drafts, gap files, reviewer messages, web sources or repository instructions were inspected. The new outputs alone were written.
