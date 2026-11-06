# Expanded iteration 08 independent adjudication

All 208 entries and 656 required fact groups were graded against frozen expanded-v11. No earlier grades, history, changes, reviews or other iterations were read. No external sources were needed and no gold/scope defects were found.

| Reader | Correct | Partial | Incorrect | Satisfied facts | Missing facts | Contradictions |
|---|---:|---:|---:|---:|---:|---:|
| reader-a | 100 | 4 | 0 | 323 | 5 | 0 |
| reader-b | 99 | 5 | 0 | 319 | 9 | 0 |
| Total | 199 | 9 | 0 | 642 | 14 | 0 |

The complete 315,182-character grading packet and 47,341-character summary were delivered model-visible before grading in 74 contiguous BEGIN/END chunks, each at most 5,000 characters and at most two chunks per call. Every call included the required outer pragma and nested output limit. Every output was inspected, complete and untruncated. Individual receipts are in `delivery-audit/grader08-*`; no delivery format deviations occurred.

The packet hash is `ddb023315c456c5f99d0c4c920d0452474b6be31fc2ebd7be80e38cd6c1d6761`; summary hash is `39dddb1b0c1e5097c2b0cfd09099dfd519b9df1cf37330d17e75db2dd581da61`. Every attached passage and answer quotation was reconstructed from its summary span and checked against its quoted-text hash. All 208 entire reconstructed entries equal the corresponding raw reader entries, including all original fields. The saved `observed_answer` values equal the original answers exactly. Raw reader, question, key and scope hashes match the frozen packet. Required fact IDs/text, question text, expected answers, exclusions, notes and references match the frozen files. The scope's additional `basis` metadata is not a fact-text change.

Quoted procedures and rows are operative answers. Both answer quotations and attached verbatim passages count only for their own entry. All case results and numerical applications were also assessed. Missing facts were not borrowed from unattached summary text or other entries. Every satisfied fact has specifically selected, literal, same-entry evidence in `results.json`.

## Partial entries

| Reader | Question | Incomplete required fact groups | Finding |
|---|---|---|---|
| reader-a | Q058 | F01 | The site passage gives draw one fewer with pawn there, but supplies neither ordinary Search's three-card count nor the required ordinary result of two. |
| reader-a | Q062 | F01, F02 | The conditional River bonus is present; ordinary Muster's two and River's ordinary total of three are absent. Without-rule ordinary gain of two is unresolved. |
| reader-a | Q088 | F02 | Campaign bonuses and Imperial sharing are present; collective Imperial Supremacy holdings earning the physical title for Chancellor are absent. |
| reader-a | Q094 | F01 | Either eligible role may choose either sign, but the passage does not identify gradient as permitting both attacker and defender. |
| reader-b | Q032 | F01 | The minor-action list permits facedown-adviser play/discard; it does not state the requested prohibition on freely discarding faceup advisers. |
| reader-b | Q036 | F03 | The title passage covers ties and new-holder side, but lacks transfer at Campaign end rather than during temporary rule losses. |
| reader-b | Q043 | F03 | General binding promises and Tribunal are covered; the Citizenship-only Reliquary exchange restriction is absent. |
| reader-b | Q084 | F01–F03 | The attached later-game setup does not resolve the requested first-game packet procedures. |
| reader-b | Q096 | F01–F03 | The overview does not contain site/card rule, pawn movement's lack of effect on garrisons/rule, or the one-color restriction. |

Every other entry is correct. No material contradictions were found. The Q058/Q062 baseline and numerical outcomes are expressly included in the frozen fact groups; their absence was recorded without changing the scope or filling them from an unattached Search/Muster rule.

## Context and application decisions

- reader-b Q084's quoted procedure is expressly later-game setup in its attached context. It does not explicitly volunteer that later procedure as the first-game rule. It therefore leaves the requested branch unresolved; it is partial rather than a fabricated contradictory application.
- reader-b Q001's compressed Wake sequence was read with its same-entry explicit round-eight exception, which directly supplies F02. reader-b Q074's title-side statement was read with its immediate alternative of a qualifying revealed Vision and its attached ordered endgame rules. Neither was forced into an exclusive ruling contrary to the explicit same-entry conditions.
- For nonnumeric cases, an attached exact conditional procedure that directly resolves the situation supplies the conclusion. No independent paraphrase was demanded. Exclusive eligibility conditions can establish that the conditional bonus does not apply; they do not invent an absent baseline quantity.
- Q038 gives actual two casualties and three survivors after skulls; Q063 gives actual costs three and zero; Q072 gives one ordinary choice and two already-Mob choices, with the six-favor threshold. The five-player setup answer includes the actual four-per-bank result under the explicit five-to-six-player condition. Q079 asks for brackets and supplies no concrete remaining-warband input, so the complete bracket table is sufficient.
- Procedural non-reversal of Mob was assessed from the complete quoted Wake procedure, which flips to Mob at six and contains no below-six return step. Recover's separate normal-side instruction was not borrowed into those entries.

## Validation

`grading-validation.json` reports passed checks for 208 original-entry reconstructions, 656 fact assessments, all IDs/text/counts and totals, 807 literal same-entry evidence checks, and 788 exact summary-span checks. All frozen inputs remain preserved. The result includes 199 correct and 9 partial entries, with 642 satisfied and 14 missing fact groups.
