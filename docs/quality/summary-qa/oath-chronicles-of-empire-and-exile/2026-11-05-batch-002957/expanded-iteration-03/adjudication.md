# Expanded iteration 03 grading

Complete package and summary were delivered before grading in contiguous at-most-5,000-character chunks, at most two chunks per call, with explicit inner/outer 7,000-token caps. The delivery receipt proves full coverage without gaps. Initial prefix reads with default outer-cap configuration were transparently replayed with explicit caps before grading. All200 entries reconstruct exactly; all244 attached spans match the summary.

All100 questions and319 frozen facts per reader were assessed. Quotes count only for their own answer. A heading cannot supply omitted body rules; a correct quote cannot cancel a contrary application. Labels and excluded context do not assign grades. Evidence retrieval only locates exact excerpts.

Independent adjudication has been incorporated for exactly A Q017, B Q021, and A/B Q037. A Q017 and B Q021 remain incorrect. Both Q037 entries are correct: their complete same-entry quotations resolve the compact cost qualifier as no-cost plans, without an explicit contrary paid-plan application. All other 196 records are unchanged.

| Reader | Correct | Partial | Incorrect | Total |
|---|---:|---:|---:|---:|
| reader-a | 85 | 14 | 1 | 100 |
| reader-b | 74 | 23 | 3 | 100 |

| Reader | Satisfied facts | Missing | Contradicted | Total |
|---|---:|---:|---:|---:|
| reader-a | 302 | 16 | 1 | 319 |
| reader-b | 284 | 32 | 3 | 319 |

**Result: FAIL.** All 200 answers and 638 facts are graded.

## Independent decisions and provenance

Report: `/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957/expanded-iteration-03/independent-adjudication.json`; SHA256 `bec7516847f7150c3ca2a012b5012279595e53827f20452ac395e7560cd46218`. The adjudicator independently assessed frozen cases against source, without provisional grades or desired outcomes. Reported source hashes/locators and exact verified same-entry evidence are embedded per fact in results.json.

- **reader-a Q017 — incorrect**: The final answer clause predicates non-Imperial status of the Chancellor when the Chancellor attacks a Citizen. Law 5.5.1 instead removes the defending Citizen’s status, and the Chancellor is always Imperial. The attached procedure gives the correct rule but leaves the answer’s incompatible application present. The requested declared-defender priority rule is also absent.
  The final sentence is awkward, but its second coordinated subject is expressly “Chancellor attacking a Citizen.” Reading it as “a Citizen being attacked by Chancellor” requires replacing the written actor and voice. The attached correct sentence does not explicitly retract or resolve this conflicting application.
  “Once total” and “its user” are accepted semantic equivalents for the one-use and single-payer requirements; no exact phrase is demanded. The title bonus is accepted through the attached modifier identification plus the answer’s side sharing.
- **reader-b Q021 — incorrect**: The answer supplies both three and four favor as the five-player bank amount. Its final parenthetical conclusion is correctly four, but the opening explicit five-player assertion of three remains materially incompatible. All other requested setup facts are present.
  “So here 4” is a correct explicit final conclusion and gives a plausible intended correction. Under the frozen strict criterion, however, the sentence also expressly says five players means three; it does not present three as a different player-count default or mark it as withdrawn. The result is an internally contradictory scenario ruling, not merely an omitted condition.
  The attached heading supplies no numerical rule. The unasked two–four-player default is not independently required and its absence does not affect the grade.
- **reader-a Q037 — correct**: All three requested meanings are present in this raw entry: empty-pool removal adds a defense die, the attacker then defender choose ruled plans once each, and bandits use their ruled plans with no cost. The complete attached procedure supplies the once-only/rule restrictions and resolves the compact bandit qualifier as a restriction to no-cost plans.
  “Without cost” alone could be read as a blanket payment waiver. The complete same-entry attached passage instead describes “plans with no cost,” a normal restrictive noun phrase. With no explicit contrary cost-bearing-plan application, this is a fair restriction-preserving interpretation of the complete entry, not a repair of an asserted contrary scenario.
  The once-per-plan requirement need not be repeated in the short answer because the same raw entry attaches it explicitly. Occupied-plan payment is contextual and is not independently required.
- **reader-b Q037 — correct**: All three requested meanings are present in this raw entry: empty-pool removal adds a defense die, the attacker then defender choose ruled plans once each, and bandits use their ruled plans with no cost. The complete attached procedure supplies the once-only/rule restrictions and resolves the compact bandit qualifier as a restriction to no-cost plans.
  “Without cost” alone could be read as a blanket payment waiver. The complete same-entry attached passage instead describes “plans with no cost,” a normal restrictive noun phrase. With no explicit contrary cost-bearing-plan application, this is a fair restriction-preserving interpretation of the complete entry, not a repair of an asserted contrary scenario.
  The once-per-plan requirement need not be repeated in the short answer because the same raw entry attaches it explicitly. Occupied-plan payment is contextual and is not independently required.

Initial artifacts are preserved as results.pre-independent-adjudication.json, adjudication.pre-independent-adjudication.md, and grading-validation.pre-independent-adjudication.json. Initial result SHA256: 26708033d95250502d0b1c32f6d27fdcc7cab018dd107c130da80daa9a7f7590. Only the two Q037 grades and their bandit facts changed; A Q017/B Q021 decisions were upheld with added provenance.

## Every final failed question

### reader-a

- **Q011 — partial**
  - Q011-F03 (missing): Trade favor must come from the card’s matching suit bank; neither the application nor its two heading-only quotes identifies that destination/source.
  - Q011-F05 (missing): Finite-source shortfall and unlimited secrets are omitted; attached Muster/Trade headings supply neither limitation.
- **Q012 — partial**
  - Q012-F03 (missing): People’s Favor payment placement is stated, but placement of the new secret bid on Darkest Secret is not; the Recover heading does not supply it.
- **Q017 — incorrect**
  - Q017-F01 (contradiction): The Citizen-attacker branch is correct. The alternative grammatical subject “Chancellor attacking a Citizen” makes the Chancellor temporarily non-Imperial. The attached quote correctly identifies “that Citizen,” creating an internal conflict rather than an unambiguous correct application.
  - Q017-F07 (missing): The general side-sharing portion is present. Neither the answer nor any attached passage assigns contested timing, order, or shared-power-user priority to the declared defender.
- **Q018 — partial**
  - Q018-F02 (missing): New favor/secrets/relics are mentioned, but the required facedown state of the stocked relics is omitted; attached Travel heading provides no reveal procedure.
- **Q032 — partial**
  - Q032-F03 (missing): Normal last-warband restriction is stated, but Bandit Crown’s exception is absent from application and the attached Minor-actions passage.
- **Q033 — partial**
  - Q033-F02 (missing): Reliquary peek permission is stated without the Scepter-acquisition-turn prohibition; the attached Minor-actions passage lacks that prohibition.
- **Q038 — partial**
  - Q038-F01 (missing): The five-warband scenario is not calculated: only the generic half-rounded-down rule is repeated, with no two killed/three survivors result. The source excerpt is also generic.
- **Q043 — partial**
  - Q043-F03 (missing): The answer identifies Scepter-offer gifting and bans free trade, but does not establish that every other binding-deal power also cannot exchange Reliquary relics. Its priority/site excerpts do not state the exclusive Citizenship-offer permission.
- **Q053 — partial**
  - Q053-F04 (missing): Site-play favor → Homeland reward → When Played timing is absent; the attached site-power passage describes the reward but not this order.
- **Q057 — partial**
  - Q057-F02 (missing): Facedown board disposition is stated, but inability to pay with that secret again until readied is omitted; the site-power excerpt lacks the exhaustion rule.
- **Q059 — partial**
  - Q059-F01 (missing): Timed discard permission is stated but the locked-card restriction is omitted; its own site-power excerpt does not supply locks.
- **Q066 — partial**
  - Q066-F03 (missing): No statement that a ruin’s power can still function under normal access/text; the application and attached Components passage only address capacity, suit and Muster/Trade.
- **Q068 — partial**
  - Q068-F01 (missing): May stop without spending all Supply is stated, but preservation of unspent Supply through Rest is not; attached Act heading supplies no saving rule.
- **Q074 — partial**
  - Q074-F02 (missing): Vision/fallback priority is described, but possible Citizen Successor replacing the fallback Chancellor is omitted; the attached War-exhaustion introduction has no tiers or succession text.
- **Q088 — partial**
  - Q088-F02 (missing): Shared Imperial defense benefit is supplied, but Supremacy title ownership when the Empire collectively meets its goal is omitted from the application and its own Campaign/Imperial excerpts.

### reader-b

- **Q007 — partial**
  - Q007-F01 (missing): Generic 'card favor' does not identify denizens/edifices as the favor-return sources; the attached quote is only the Rest heading.
  - Q007-F02 (missing): Generic 'card secrets' does not identify denizens/edifices/relics as the return sources; the Rest heading supplies no categories. Board-secret readying itself is stated.
- **Q011 — partial**
  - Q011-F02 (missing): Two warbands to board are stated, but personal-bank origin is omitted; the attached Muster heading supplies no origin.
  - Q011-F03 (missing): Trade formulas are given without the matching suit-bank source for favor or shared-bank source for secrets; the heading-only quote does not supply these requested destinations/sources.
  - Q011-F05 (missing): Finite favor/warband source limits and unlimited secrets are omitted.
- **Q012 — partial**
  - Q012-F02 (missing): Facedown/local eligibility and site cost are stated, but taking the recovered relic faceup into personal bank is omitted.
  - Q012-F05 (missing): The one/rest and self-recovery rules are given, but the no-previous-player shared-bank remainder case is not resolved; the quote is only the Recover heading.
- **Q014 — incorrect**
  - Q014-F02 (contradiction): Application requires at least one SITE at the attacker pawn, whereas the required local TARGET can instead be a co-located defender relic if that defender does not rule the attacker site. Its later relic statement and correct quote conflict with the explicit mandatory-site ruling.
- **Q017 — partial**
  - Q017-F02 (missing): Join permission/location is stated but the non-attacker Citizen restriction is not; the attached Imperial-defense heading supplies no eligibility rules.
  - Q017-F03 (missing): No clear activation of all defender/Ally Campaign modifiers or shared title-defense bonus; side powers alone does not specify that activation/bonus instruction.
  - Q017-F04 (missing): Access and once-total use are stated, but the chosen plan user paying its cost is omitted.
  - Q017-F05 (missing): Eligible allies may join, but the answer never states their board warbands contribute defense under the specified pawn-location condition.
- **Q018 — partial**
  - Q018-F02 (missing): Only 'reveal and stock' is stated; printed favor/secrets and the facedown relic stocking operation are not described, and the quote is merely the heading.
- **Q019 — partial**
  - Q019-F03 (missing): Promised exchange is stated but Chancellor gaining the newly uncovered mandatory Reliquary modifier is omitted; the attached Offer paragraph does not contain acceptance consequences.
  - Q019-F04 (missing): Recipient/shortage conversion is stated generically for all own-color warbands, without identifying the board/map pieces being replaced; the attached Offer paragraph supplies no conversion locations.
- **Q021 — incorrect**
  - Q021-F01 (contradiction): “Five players means 3 favor” directly conflicts with the requested scenario and Law 1.6. The parenthetical includes the correct 5–6-player condition and “so here 4,” but the entry gives two incompatible numerical applications without expressly withdrawing the first.
- **Q022 — partial**
  - Q022-F01 (missing): Region/top-down dealing order is given but preservation/dealing of attached cards with each saved site is omitted; the attached setup heading does not supply it.
- **Q023 — partial**
  - Q023-F01 (missing): The required saved-side constraint is not established: 'choose Exile or Citizen side on saved boards' does not clearly restrict choosing to boards on their already-saved sides.
  - Q023-F02 (missing): The answer says pawn locations are not freely chosen but gives neither ordinary any-faceup-site permission nor Chancellor’s required top faceup Cradle site.
- **Q024 — partial**
  - Q024-F02 (missing): Bottom draw/keep-one/discard-two is given, but turn-order pawn placement before adviser/discard selection is omitted; setup heading cannot supply it.
- **Q025 — partial**
  - Q025-F04 (missing): Four facedown adviser names are listed but not assigned to Chancellor/Red/Blue/Yellow. The order resembles the source’s order, but no 'respectively' or other owner relationship establishes the mapping.
- **Q027 — partial**
  - Q027-F02 (missing): Until faceup restriction is stated but own Rest as the readying time is not; the payment paragraph lacks Rest timing.
- **Q032 — partial**
  - Q032-F03 (missing): Bandit Crown exception allowing last physical pickup is omitted from application and its attached Minor-actions passage.
- **Q033 — partial**
  - Q033-F02 (missing): Scepter-acquisition-turn prohibition on using its peek power is omitted; attached Minor-actions passage does not contain it.
- **Q038 — partial**
  - Q038-F01 (missing): No explicit application of the five-warband scenario to two killed and three survivors; generic half-rounded-down rule alone leaves the requested numeric result unstated.
- **Q052 — partial**
  - Q052-F03 (missing): New people/no fixed status ownership is stated, but non-Chancellor choice among saved boards in turn order is not; attached Chronicle passage lacks later setup selection.
- **Q053 — partial**
  - Q053-F04 (missing): Site-play favor → Homeland reward → When Played sequence is omitted from application and site-power attachment.
- **Q055 — incorrect**
  - Q055-F03 (contradiction): 'Ruling Narrow Pass removes those requirements' applies the exception to both Travel entry and Campaign targets. Rule removes only the Campaign additional-target condition; Travel entry still requires Narrow Pass absent a named ignore effect.
- **Q057 — partial**
  - Q057-F02 (missing): Facedown board secret is given but its inability to pay again until readied is omitted; site-power attachment lacks exhaustion rules.
- **Q059 — partial**
  - Q059-F01 (missing): Great Slum timing is correct but respecting locked cards is omitted from this answer’s application/attachment.
- **Q066 — partial**
  - Q066-F03 (missing): Ruin capacity/suit/Muster/Trade are covered, but continued operation of its power under normal access/text is not.
- **Q068 — partial**
  - Q068-F01 (missing): Not spending all Supply is allowed, but preserving it through Rest is omitted; own Act-heading quote does not supply it.
- **Q069 — partial**
  - Q069-F02 (missing): Outbid/old-resource redistribution is described, but placing the new payment stack and People’s Favor turning normal on Recover are not resolved; attached Campaign excerpt contains no Recover normal-side rule.
- **Q084 — partial**
  - Q084-F03 (missing): Ivory Eye’s Mountain placement is stated without its facedown state; the attached first-game heading gives no relic placement state.
- **Q088 — partial**
  - Q088-F02 (missing): Title defense sharing is given, but Chancellor holding Supremacy when the Empire collectively meets its goal is omitted; attached Campaign excerpt has no collective-title ownership rule.

## Other semantic decisions and evidence preservation

Other contextual equivalents accepted: optional once-each Rest powers need not parrot any-order; A Q029 after governs its precursor list; A Q072 Mob twice branch means two total rather than an explicit three; B Q076 and A Q096 explicitly reject tentative rhetorical claims; B Q093 recaps rather than explicitly double-activates victorious effects. Treating bandits as own warbands supplies inherited normal defense eligibility; at-most-eight prevents round nine; all provided edifices/suits means complete Archive preparation; Citizen-purple context is not an Exile survivor rule.

Support labels were ignored: A Q030 is correct despite unsupported, and B Q071’s unasked own-color shortage caveat does not retract requested conversion facts despite unsupported.

## Evidence and preservation

results.json contains every unchanged question/key answer, exact application, full reconstructed raw entry with original quote strings, span ownership/hashes, all638 fact statuses/reasons, and specific same-entry literal evidence locations. Complete observed entries remain available when multiple selected fragments jointly carry a fact. Delivery receipt: /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957/delivery-audit/grader03-delivery-complete-1140bed2e963401fbcb5d9bc9c984565.json. Package SHA256 d9bef787c7a2799538dda61abe66d1210fd15359a3ade89053249448c27953db; summary SHA256 ef257d044d6cfa436227cd08a93ca35983aaa7828c7d0a65e783155dfc57046e; scope SHA256 a1a598f07f53d6b2765b4c8419f01ce2f65ff3c12b51587427c41462ae03fa0b.
