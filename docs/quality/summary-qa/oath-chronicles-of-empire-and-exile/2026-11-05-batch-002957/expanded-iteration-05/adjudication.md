# Expanded iteration 05 independent adjudication

The fixed expanded-v9 benchmark has 103 questions and 327 required facts per reader. All 206 complete entries and all 654 frozen facts were assessed. No prior grades, history, changes, reviews, or other iterations were consulted. The original raw entries, fixed key, scope and snapshot were preserved.

| Reader | Correct | Partial | Incorrect | Total | Satisfied facts | Missing facts | Contradictory facts |
|---|---:|---:|---:|---:|---:|---:|---:|
| reader-a | 99 | 3 | 1 | 103 | 323 | 3 | 1 |
| reader-b | 99 | 3 | 1 | 103 | 323 | 3 | 1 |

## Non-correct entries

The same findings apply independently to each reader:

- **Q032 — partial; Q032-F03 missing.** The ordinary prohibition on picking up the last site warband is correct. Neither entry states the required Bandit Crown exception, and neither attaches the passage giving it. The answer's general rule is treated as ordinary context, not an explicit denial that an exception can exist.
- **Q037 — incorrect; Q037-F03 contradiction.** Reader-a says bandits use all plans at sites they rule “without cost,” and its scenario result repeats that interpretation. Reader-b says “Bandits use all ruled plans free.” The frozen fact limits bandits to ruled **no-cost plans**. Making every ruled plan free is a materially different rule. The attached sentence “bandits use all ruled plans with no cost” does not silently repair the explicitly incompatible applications. The die-removal substitution, plan order and ordinary use limit are satisfied.
- **Q066 — partial; Q066-F03 missing.** Both entries correctly resolve facedown-site rule, capacity, suit and Muster/Trade eligibility. Neither states the required continued functioning of a ruin's power, and their attached passages do not provide it. Reader-a explicitly leaves that issue unresolved. This is an omission, not a contradictory claim that ruins have no power.
- **Q084 — partial; Q084-F02 missing.** Both entries give the 3/3/5 regional counts and ordered 41-card world-deck remainder. Neither states the seeded regional cards' required facedown orientation. Their attached first-game setup passage likewise omits that orientation. The unattached Components description of facedown discard piles is not imported into the entry. Other Q084 facts are satisfied.

## Scope defect reported separately

**Q025:** the question asks denizen faceup/facedown state, but the immutable fixed expected answer, required facts and snapshot give Longbows/Taming Charm/Elders placements without their orientation. Reader-a explicitly identifies that unresolved detail. Both entries satisfy every frozen placement fact. This mismatch is reported in `gold_or_scope_defects`; no orientation fact has been invented, no fixed fact changed, and no additional penalty added outside the frozen scope.

## Interpretation and evidence rules

Attached quotation text is part of its own entry and may complete a shortened answer. Each fact has independently selected literal evidence, an explicit omission, or a contradiction finding in results.json. Answers and scenario fields were assessed together with their attached passages. Correct general rules do not erase incompatible concrete applications. No fact was borrowed from another entry or from an unattached part of the snapshot.

Compact wording was read in its complete same-entry context. In particular, reader-b Q006's repeat wording conveys two total choices alongside the explicit repeat-once passage; Q014's parenthetical is interpreted with the attached distinct target dice rules; Q030's braid terminology does not override its explicit correct lock rule; and reader-a Q073's awkward reveal sentence expressly says the action occurs in Act, not Wake. These are not material contradictions. Numeric cases in Q038, Q063 and Q072 are actually resolved by their entry text, not passed on formulas alone. Confidence/support and self-review labels were not grades.

## Delivery and validation

The packet (314,584 Unicode characters) and snapshot (46,458) were received model-visible in 73 contiguous chunks of at most 5,000 characters. Each call delivered at most two chunks with explicit outer and nested 7,000-token output budgets; the initial two packet chunks were redelivered under those explicit limits. Every result was inspected and no delivered chunk was truncated. Receipt artifacts are under the batch's delivery-audit directory with the grader05 prefix.

The validation passed 6,787 checks: 206 entry IDs and exact raw reconstructions, 654 fact IDs and exact frozen fact text, fixed expected answers and scope exclusions/notes, 284 attached quote hashes and preserved metadata, 1,329 literal same-entry evidence items, quote subspan containment, all totals, complete chunk coverage, and all immutable input hashes. See grading-validation.json for the machine-readable checks. No external source lookup was needed; the fixed packet and snapshot resolved the assessment.
