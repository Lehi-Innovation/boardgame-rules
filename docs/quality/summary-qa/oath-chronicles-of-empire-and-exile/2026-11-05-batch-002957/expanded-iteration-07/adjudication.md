# Independent iteration 07 adjudication

Frozen benchmark: expanded-v11. Reviewed all 208 entries and all 656 required fact groups, including every requested conjunct, scenario field and own-entry attached quotation. No earlier grades, other iterations, history or change files were read. No external rule lookup was needed. Original/key/scope files were used only for integrity comparisons after semantic review.

| Reader | Correct | Partial | Incorrect | Total |
|---|---:|---:|---:|---:|
| reader-a | 103 | 0 | 1 | 104 |
| reader-b | 101 | 1 | 2 | 104 |

| Reader | Satisfied facts | Missing facts | Contradicted facts | Total |
|---|---:|---:|---:|---:|
| reader-a | 327 | 0 | 1 | 328 |
| reader-b | 324 | 1 | 3 | 328 |

## Adverse decisions

- **reader-a Q056 — incorrect.** The answer says the summary names no specific site-power override. Its attached Site powers passage explicitly names Shrouded Wood and says travel from it ignores Hidden Place. The false availability assertion is material because identifying the named override is expressly asked. The correct quotation does not erase this explicit negative statement. Q056-F02 is contradicted; the other facts are supplied in the entry.
- **reader-b Q038 — partial.** The five-warband case asks for the actual number killed and surviving. The answer gives only the general half-rounded-down rule and board destination; its attached passage supplies the same general formula. Neither resolves this case to two killed and three survivors. Q038-F01 is missing, rather than contradicted: there is no wrong number. The defender taking no attacker relics is satisfied.
- **reader-b Q055 — incorrect.** After describing the two restrictions the answer says ruling Narrow Pass removes “those conditions.” That expressly removes the entry restriction too. Ruling it exempts Campaign targeting, not entry. Q055-F01 and F03 are contradicted; F02 is satisfied. Its correct attached quotation cannot erase the incompatible application.
- **reader-b Q070 — incorrect.** The opening says a Citizen defensive plan cannot restrict other Allies. Shared defending-side power language permits exactly that restriction. Q070-F01 is contradicted; the attached passage resolves the other two facts, including user payment, without curing the opening contradiction.

## Fair contextual readings

**reader-a Q001 passes.** The answer says the first *check* is at the next Wake, rather than expressly asserting a win then. That is accurate. Its own attached timing passage explicitly states next Wake checks before flipping, ordinary victory at the following Wake, an intervening round-eight window, and the resetting transfer rule. Reading the complete entry resolves the question without forcing “first check” to mean “first possible win.”

**reader-b Q017 passes.** The compressed final temporary-status sentence is interpreted using its explicit attached Campaign conditions: Chancellor attacking Citizen makes that Citizen non-Imperial. No statement unambiguously assigns the Chancellor that status. All other detailed Imperial facts are supplied within the same entry.

Other compact wording was read in its own entry's explicit context. Examples include “up to” gains/draws qualified by finite sources or mandatory draw rules, and a generic access statement qualified by a passage expressly allowing adviser plans. An omitted detail in answer prose can be supplied by that entry's attached text; another question's or reader's passage cannot supply it. Generic formulas do not settle expressly requested numerical applications.

No gold/scope defect was established. Contextual exclusions were honored rather than silently expanding requested facts.

## Delivery and validation

The complete 311,356-character packet and 47,126-character summary were delivered before grading in 73 contiguous chunks of at most 5,000 characters, at most two per tool call. Every output was inspected, untruncated, with both outer and nested output budgets explicitly set to 7,000 tokens. There were no directive deviations. Per-chunk receipt hashes and boundaries are saved in `delivery-audit/grader07-receipts.json`.

`grading-validation.json` passes 5,048 checks: exact 208 IDs/entries, all 656 fact IDs and fixed scope texts, 301 exact original attached quotations with representation/metadata preserved, all original input hashes, exact key answers, literal same-entry evidence and subspans, complete delivery coverage, and all score totals/derivations. Evidence extraction formats short local excerpts after the independent decisions; it does not assign grades. Mechanical validation does not itself prove semantic judgments.
