# Independent strict adjudication — expanded iteration 04

Frozen benchmark: expanded-v9, 103 questions and 327 required facts per reader. All 206 entries and 654 facts were adjudicated after full model-visible delivery. No previous grades, histories, other iterations, reviews, or reader protocol reports were consulted.

| Reader | Correct | Partial | Incorrect | Total | Satisfied facts | Missing facts | Contradictory facts |
|---|---:|---:|---:|---:|---:|---:|---:|
| reader-a | 93 | 7 | 3 | 103 | 317 | 7 | 3 |
| reader-b | 92 | 10 | 1 | 103 | 315 | 11 | 1 |

## Delivery and integrity

The complete 295,776-character packet and 43,979-character summary were received in 69 contiguous chunks, each at most 5,000 characters, through 35 calls containing at most two chunks. Both the outer and nested output budgets were 7,000 tokens. Every output was inspected; none was truncated. Range receipts and the delivery script are under `delivery-audit/grader04*`.

All six packet-listed original file hashes match. Both sets of 103 original entries reconstruct exactly from the transport and summary spans, including all retained fields. All 451 attached quote hashes match. The frozen key answers, all 327 fact identities/texts, exclusions, and semantic notes match the frozen scope. Source/key/scope/raw files were preserved.

## Grading rules applied

Each fact has specific literal evidence from its own application or its own attached passages. Applications can state facts directly; the complete summary verifies their truth, but an unattached section cannot supply a missing fact. Complete attached sections may supply general procedures. Numerical scenarios still require an actual resolution. An explicitly incompatible application remains contradictory even when its attachment states the right general rule. Missing required details produce partial answers, separately from contradictions. Labels such as supported and reader self-review did not determine grades.

## Material contradictions

- Both readers, Q038-F01: five warbands are already the post-skull force. The applications instead subtract skull casualties from five again. Correct defeat resolution is two killed and three survivors. Correct attached general procedure does not erase the changed premise.
- Reader-a, Q060-F03: the application expressly says forced travel/banishment does not bypass the cost. Banishment itself spends no Supply. A conditional Free Travel exception does not establish this automatic permission or retract the contrary statement.
- Reader-a, Q078-F01: the application distinguishes chosen attacking-force warbands from unchosen board force in response to choosing fewer attack dice. Dice choice does not itself exclude board warbands from the force or skull casualties.

## Missing requested facts

### reader-a

- Q033-F02: Scepter Reliquary peek permission is present, but the no-use-on-turn-taken condition is absent from this application and its Minor-actions attachment.
- Q052-F03: Different players/status ownership is allowed, but selection of saved boards by non-Chancellors in turn order is absent from the application and Chronicle attachment.
- Q053-F04: The application and attached Homeland procedure omit the requested site-favor → Homeland → When Played order; reader-b also attaches Search, which does not supply that timing.
- Q057-F02: Flipping an own-board secret facedown establishes its location/state, but inability to repay with it until readied is absent from this entry. Neither attached Travel nor Site powers supplies that payment/readiness rule.
- Q059-F01: Timed discard permission is stated, but respecting locked cards is absent. The Site attachment for reader-a and Overview attachment for reader-b do not supply the lock restriction.
- Q068-F01: The application allows stopping with Supply unspent, but does not explain preservation through Rest. Its sole Act attachment omits the Rest saving rule.
- Q088-F02: Imperial sharing is supplied, but this entry does not identify the Chancellor as title holder when the Empire collectively meets the Supremacy goal. Reader-a uses the broader Empire-holds-title shorthand; reader-b omits collective goal/holder allocation.

### reader-b

- Q036-F02: Outgoing-holder selection is stated, but receiving the title Oathkeeper-side is absent from this application and its Overview attachment.
- Q052-F03: Different players/status ownership is allowed, but selection of saved boards by non-Chancellors in turn order is absent from the application and Chronicle attachment.
- Q053-F04: The application and attached Homeland procedure omit the requested site-favor → Homeland → When Played order; reader-b also attaches Search, which does not supply that timing.
- Q057-F02: Flipping an own-board secret facedown establishes its location/state, but inability to repay with it until readied is absent from this entry. Neither attached Travel nor Site powers supplies that payment/readiness rule.
- Q059-F01: Timed discard permission is stated, but respecting locked cards is absent. The Site attachment for reader-a and Overview attachment for reader-b do not supply the lock restriction.
- Q060-F03: The ruler chooses even for banishment, and a spend-no-Supply effect may override base cost, but this entry never establishes that banishment itself supplies that no-Supply permission. The Campaign passage containing it is not attached.
- Q061-F01: The trigger and lack of rule exemption are stated, but mandatory +1 attack die for Plains and −1 for Mountain are absent from the application and its Overview attachment.
- Q083-F03: The round-end check-before-advance sequence is stated, but automatic ending at round eight is absent from the application and its Overview attachment.
- Q088-F02: Imperial sharing is supplied, but this entry does not identify the Chancellor as title holder when the Empire collectively meets the Supremacy goal. Reader-a uses the broader Empire-holds-title shorthand; reader-b omits collective goal/holder allocation.
- Q095-F01: Mandatory resolution/explicit may is present, but once-each ordinary Wake-power frequency is absent from this application and its Wake procedure attachment.
- Q095-F02: Rest powers are called optional, but once each at the end of Rest is absent from this application and its Wake-only attachment.

## Contextual interpretation and exclusions

- Q037: “all plans … without cost” is read in the complete same-entry context of the attached eligible no-cost plans, rather than inventing permission to waive a costly plan. No contradiction is forced from that compact wording.
- Reader-b Q081: the slash wording about specified attacker/defender status is interpreted with the attached explicit conditions: a Citizen attacking another Imperial player, or a Citizen chosen by a Chancellor attacker. The complete entry does not require a false reading that the Chancellor becomes non-Imperial.
- Reader-a Q066: in its immediate ruined-edifice context, “site powers remain as printed otherwise” conveys continued power operation under the printed conditions. A vocabulary distinction alone is not a missing fact.
- Q072: “repeat choice twice” is read as two total choices when already Mob, consistent with its explicit attached repeat-once procedure.
- Q074: title-side insufficiency is read in context with the same entry’s separate qualifying-Vision route, not as a ban on that Exile winning by any method.
- Q085: references to all edifices and each suit stack cover the complete set; literal repetition of the numeral six is not demanded.
- Q101: before any seeding/dealing is accepted as the operational timing. Original Law step numbers are not demanded.
- Contextual exclusions from the frozen scope were honored. No extra requirements were imported from another answer or from source-only context.

## Validation and possible gold/source issues

Validation passed: 206 question IDs, 654 frozen fact checks, 908 literal evidence excerpts (90 application and 818 attached-quote excerpts), all excerpt spans and same-entry attachment membership, totals, status-to-grade consistency, original hashes, and exact raw reconstruction. The largest excerpt is 277 characters.

No external source consultation or key/scope modification was needed. No confirmed gold/source problem was identified. Semantic judgments remain separate from mechanical integrity validation.

Artifacts: `results.json`, `adjudication.md`, `grading-validation.json`; technical delivery, extraction and validation artifacts: `delivery-audit/grader04*`.
