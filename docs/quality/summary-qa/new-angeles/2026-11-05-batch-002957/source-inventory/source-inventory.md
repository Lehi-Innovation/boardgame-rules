# New Angeles source-only procedural inventory

Scope: original Fantasy Flight Games 2016 base game, 4–6 players, BGG 205716. This is a source inventory for the parent agent, not an independent audit of a summary, answer key, question set, or reader. None of those materials was opened. Authoritative source order is official FAQ v1.0 (27 March 2018), Rules Reference (RR), then Learn to Play (LTP); component instructions supply their particular effects. No module behavior or fan transcription was used as rule authority. No browsing was needed.

The three complete assigned texts were read: RR 73,771 Unicode characters, LTP 73,668, FAQ 3,966 (151,405 total). `text-coverage.json` records half-open character ranges and hashes; `text-manifest.json` records the source identities. All 218 used printed cells described below were delivered through `view_image(detail="original")` and forwarded with original detail, using native lossless cell crops. `image-receipts.json` records each parent image hash, actual dimensions, exact crop rectangle, crop byte/pixel hashes, pixel equality and delivery ordinals. The 218 include all 100 action slots (duplicates included), 34 assets, 9 demands, 12 investments, 6 setups, 16 event faces and 16 matching backs, 7 rivals, all 6 emergency faces, and both sides of all 6 corporation sheets. Emergency backs contain no additional rules and were not semantically consulted. Crops preserve decoded parent pixels with no resizing or OCR.

Locator convention: all cell numbers below are zero-based row-major indexes in the named preflight atlas. Files are under `source-preflight/new-angeles/` in batch `2026-11-05-batch-002957`; each crop is retained under this report's `crops/` folder with `-cellNN.png`. The module is only an asset locator. Preflight README and full printed-component-provenance JSON were read; its interpretation of side names was independently checked against the actual icon and draw panels.

## Core procedure and branch inventory

| ID | Procedure and meaningful branches | Authoritative reference |
|---|---|---|
| S01 | Make separate shuffled asset, demand, event, investment decks and five separate shuffled action decks; put event deck on board and other decks by slots. | RR p2 Complete Setup 1–2 |
| S02 | Shuffle setup cards, draw one, place one copy of each listed component in each named district. Put its upper-right number of facedown assets on turn slots starting at 1; return all setup cards to box. These give 3, 4, or 5 turns rather than player-count turns. | RR p2 Setup 3; RR53; all six printed setups |
| S03 | Set round to1; five supplies to0; reveal demand and place each target at its printed amount, including0. | RR p2 Setup4–5; RR62 |
| S04 | Choose corporation and matching sheet/emergency; choose side by player count (4 icon versus5–6). Faceup emergency is outside hand. Randomly select first active player with capital tokens; active starts10, clockwise players11,12,etc. Draw each corporation's printed action quantities. | RR p2 Setup6–9; RR12–13,21 |
| S05 | Rival deck consists only of used corporations plus Federalist. Deal one secretly to each; set single extra partially under board. Thus Federalist can be absent; own corporation changes victory test. Rivals cannot be revealed/discussed. | RR p2 Setup10; RR28,50 |
| S06 | Full setup draws two investment cards per player, keeps one facedown and returns other facedown to top. Do not substitute the LTP first-game single-card investment or fixed first-game hands. | RR p2 Setup11; LTP pp4–5,15 |
| S07 | Make reserve of unused android, outage, unrest, illness, development tokens and Human First, orgcrime, prisec units. The fourth android is a replacement, not a fourth productive token. | RR p2 Setup12; FAQ Other |
| R01 | Six numbered standard rounds each have Action→Production→Event; three intervening Demand rounds have separate steps. Move round marker one space after each round. | RR51,55; RR18; LTP pp8–9 |
| A01 | Start-of-turn asset triggers precede Refresh. Refresh readies all exhausted owned assets and then draws in sheet's top-to-bottom order. Thus an asset newly exhausted at start can ready in Refresh; hand size is not checked here. | RR3.1,6.6,26,46 |
| A02 | Each printed General entry selects one action deck not already drawn this Refresh. All cards of one entry come from that single deck. Do not inspect draws before deciding deck. Melange's three separate entries therefore draw from three distinct types; specialist's General excludes its specialty. | RR3.1,29; actual sheets |
| A03 | If required action deck is empty, shuffle whole shared facedown discard, reveal/sort by type, shuffle each into its matching deck; then draw. No rule to shuffle only the empty type. | RR2.2; LTP p14 |
| A04 | Resolve one deal, then optional owned End of Turn abilities in chosen order, each at most once that turn; a card received during this step can be used then. After abilities, discard action cards down to modified hand limit; pass active token left. | RR3.2–3.3,22,30 |
| A05 | Standard hand size5; emergency does not count. Other players are not forced to discard when another player's turn ends. If turn track still has assets, new active player takes next turn; if empty at end of turn, proceed to Production. Some players receive no turn in a round. | RR3.3–3.4,30,67.4 |
| D01 | Reveal rightmost/highest-numbered asset from turn track into Revealed Asset box. Players cannot inspect remaining track assets. | RR16.1,6.9 |
| D02 | Active player must propose one main offer: hand action or faceup emergency. Cannot pass. | RR16.2,34 |
| D03 | Clockwise from active player's left, each other player has exactly one chance to pass/propose counteroffer. Active normally cannot counter. No repeated circuits. | RR15.6,16.3,16.7; FAQ Deals |
| D04 | First counteroffer costs0 extra cards; next costs1,etc.: discard number equal to existing faceup counteroffers before adding new one. Topmost only is current; old countering player loses that role and normally becomes supporting player. Earlier counteroffers are ignored except cost count. Duplicate card names are legal. | RR15.1–15.7,14 |
| D05 | If no counteroffer, skip Support and resolve main offer (LTP explicit). Otherwise everyone except active and current countering player is supporting player. Clockwise from active left, each has one chance to abstain or put1+ hand actions facedown next to just one offer; cannot split support, revisit, or normally add support as proposer. Emergency cannot support. | RR1,16.4,16.6,21.5,59–60; LTP p10; FAQ Deals |
| D06 | Most facedown support cards wins; main offer wins ties, including0–0. Resolve winning offer, then claim revealed asset; losers' effects are not resolved. Discard all played ordinary actions facedown to shared pile. Assets can override normal winner/support sequence; see printed assets below. | RR16.5,59.4 |
| D07 | Emergency discard returns it to original logo owner: face down if winning offer, face up otherwise, including superseded offers. Winning one cannot be proposed again while facedown; no automatic Refresh flip. | RR16.5,21.3 |
| D08 | Claim means winning/deck instruction to claim; receiving via steal, trade or swap only gains, so does not trigger When You Claim. Gained assets go faceup in recipient play area. | RR6.1,9,56.2,61; actual claim assets |
| P01 | Production exploits every android district, ascending district number. Each district produces its resources first, then increases unrest. It is still exploited if strike/outage/orgcrime prevents production. | RR27,44 |
| P02 | Strike or outage blocks all resources; protest produces normally. Orgcrime blocks primary only, including its development bonus; one-resource district then produces nothing. Development adds1 to primary only; secondary unchanged. Supply cannot exceed final track space or go below0. | RR19,27.3–27.5,38,41,43,45,49,52,58 |
| P03 | Without Human First, exploitation raises unrest one stage, capped at strike. With Human First, raises two stages instead; if unable to raise two (protest, strike, or outage), place an outage token, potentially cascading. Only Human First exploitation causes outage because unrest cannot rise. | RR27.1–27.2,31.1,39.5,68.6–68.7 |
| P04 | Merely producing by card is not necessarily exploitation. Apply production modifiers unless card overrides them. Liquidation expressly ignores orgcrime, produces without normal exploitation effects, then explicitly raises unrest to strike. | RR43.6; FAQ Action Cards; Labor15–19 |
| E01 | Reveal top event; resolve top-to-bottom: threat/effect, then printed placements, then next turn-track count. Put resolved event on bottom; advance round. Cannot calculate whole effect as simultaneous net change because threat25 ends immediately. | RR24–25,63; printed events |
| E02 | Event warning back is open information; fronts looked at/reordered through an effect remain secret. Back gives component risk, not precise threshold/formula. Event can cause threat through placement/movement to Root even if top text increases none. | RR24.2–24.3; FAQ Melange |
| E03 | Fill next turn track with indicated number from asset-deck top, lowest slots first; sixth standard round need not reset because no further Action Phase. | RR24.1,67.2–67.5 |
| Q01 | Demand step1: reveal/score investments before checking demand. Particular resource-demand investments score0 if that resource misses target, even if others meet theirs. Then step2: meet all five resource requirements; if any fails, apply one printed Fail Result, not once per shortage. | RR18.1–18.2,33; FAQ Investments |
| Q02 | Nonfinal demand: reset all supplies to0 (surplus not retained), put old demand bottom, reveal next and reset all targets; return all investments/shuffle, draw2/keep1 secretly and return other to top; advance round. | RR18.3–18.5 |
| Q03 | Third demand ends immediately after Pay Demand: score third investment first, apply possible failure threat, then determine ending; no new demand/investment reset. Threat25 during demand failure uses Federalist ending, not normal rival ending. | RR18.2,18.6,28.2,63,69 |
| M01 | Enemy units are Human First and orgcrime only. Prisec is a unit but not enemy. Root is not district/city; city consists of ten districts. | RR8,20.1,23 |
| M02 | District max1 each android, development, illness, outage, Human First, orgcrime, prisec. Different enemy types can coexist. New duplicate enemy/illness/outage must move; unrest/development never move. | RR5.3,19.4,31.2,32.3,35.3–35.5,38.1,39.3,42.3 |
| M03 | Normal moving follows outgoing arrows to higher-numbered district, repeats if unable to remain; district10 exits to Root. Enemy entering/placed with prisec must move, and prisec placed with enemies causes enemies to move. | RR35–36,31.3,38.2,42 |
| M04 | Each enemy/illness/outage entering Root returns reserve and increases threat2; it was moved, not removed by action, and Root is not district, so no removal contracts. Moving out of a district never counts as removing. | RR35.2,35.6,36.1,47.3 |
| M05 | Android relocation ignores movement arrows and may go to any district lacking an android. Multiple relocations resolved one at a time; cannot place into occupied android district. | RR5.1–5.2 |
| M06 | Placing takes from reserve; removing returns to reserve. If reserve lacks required component, do not place that component; no unlimited proxies supplied by core rules. | RR10,40,47–48 |
| U01 | Stable→protest→strike, reverse on decreases. Cannot reduce stable or raise strike/outage. Outage is stable and replaces any unrest token; removing outage leaves stable. Replacing unrest with outage is not NBN's contract trigger. | RR39,45,54,57,68; FAQ NBN |
| I01 | Resolving action involving1+ illness districts increases threat2 total, not2 per district/token. Involvement includes selected district, moves in/out, placements/removals, and attempts prevented by other components or reserve shortage. Chosen unrest districts count. | RR32.1–32.2,32.5,63.2; FAQ Illness |
| I02 | Illness itself does not trigger on exploitation or event resolution, or merely because an asset affects cards/capital. Effects explicitly exempting illness override action's illness threat; Root movement threat remains a distinct source. | RR27.6,32.6; FAQ Illness; printed exemptions |
| C01 | All contracts except Melange require action-card resolution; owner need not resolve it. Removal contracts pay only district removals, not movement/Root. Printed payout amounts and trigger units are below. | RR11.1–11.3; FAQ Contracts |
| T01 | Capital/assets/promises can be traded at any time. Immediately completely fulfillable agreement binds; gifts allowed. Future promises nonbinding; unresolved dispute about binding before agreement makes it nonbinding.3+ player trade binds if all parts immediately/simultaneously resolvable. | RR65.1–65.4; FAQ Trading |
| T02 | Cannot trade ordinary actions, emergency actions, investments (FAQ erratum), rivals or corp sheets. Asset effects may give/steal these explicitly despite ordinary trade prohibition. Exhausted assets stay exhausted when traded/stolen. | RR65.5 corrected by FAQ; RR6.8,26.2,56 |
| H01 | Action contents secret; cannot tell others which are in hand or lie about hand count. Given/stolen hand action stays unrevealed to others. Discards facedown, not inspectable (except explicit reshuffle sorting). Investments secret until score; cannot inspect investment deck; rival identity/discussion forbidden except explicit Thomas information. | RR2.6–2.8,33,50.3; LTP p14; FAQ Thomas |
| X01 | Asset may/End of Turn abilities optional; exhausted cards cannot exhaust again until ready. Same-timing own assets chosen order; multiple players same timing resolve clockwise starting active. Start-of-turn precedes Refresh. | RR6.2–6.6,22,26 |
| W01 | Capital track uses40-side when over39; subtracting below40 flips back. Multiples5 have no mechanical effect. | RR7.2–7.6 |
| W02 | Threat25 ends immediately. Everyone loses except Federalist with at least25 capital at that exact time; if absent or under25, everyone loses. No later investment or effect can rescue failed ending. | RR28,63,69.3 |
| W03 | Normal end after final demand, if threat below25: Federalist loses, each other player beats named rival strictly; ties lose. Own-rival beats at least3 others in5–6-player game or2 in4-player game, strict comparisons. Multiple winners permitted. | RR50,69; all rival faces |

## Exact corporation panels and contracts

Each row was read on BOTH native sheet sides. All specialty panels are printed topmost and read first. `corporation-sheets-face.jpg` has no4-player icon and is the5–6-player side; `corporation-sheets-back.jpg` has the4-player icon for the five specialists. Melange's identical side has no differing panel.

| Cell / corporation | 4 players, top-to-bottom | 5–6 players, top-to-bottom | Exact printed contract; controlling qualification |
|---|---|---|---|
|0 Globalsec |2 Security;1 General |2 Security;1 Media |The Conflict Solution: “When an enemy unit is removed from a district, gain1 capital.” Per enemy removed through action, including both enemy types; not prisec or Root/movement. |
|1 Haas-Bioroid |2 Labor;1 General |2 Labor;1 Construction |Engineering the Future: “When1 or more android tokens are moved, gain2 capital.” FAQ: can trigger only ONCE PER TURN regardless of how many android tokens move. |
|2 Jinteki |2 Biotech;1 General |2 Biotech;1 Labor |Personal Evolution: “When an illness token is removed from a district, gain2 capital.” Per token; not illness moved to Root. |
|3 Melange Mining |1 General;1 General;1 General |1 General;1 General;1 General |Powering Change: “When an event card is resolved, if threat does not increase by at least2, gain3 capital.” Counts ALL threat from resolving entire event, including placements overflowing to Root;0 or1 qualifies,2+ does not. |
|4 NBN |2 Media;1 General |2 Media;1 Biotech |Making News: “When unrest decreases, gain1 capital for each stage it decreased.” Only action resolution; no payout for an outage erasing unrest token. |
|5 Weyland Consortium |2 Construction;1 General |2 Construction;1 Security |Building a Better World: “When an outage token is removed from a district, gain2 capital.” Per token; not outage moved to Root. |

The quote text above regularizes spaces only. Refer to retained original crops for literal typography. LTP first-game fixed starting hands do not override this complete-setup panel selection. RR3.1 controls draw order, not the extraction's floating illustrative text order.

## Exact emergency face effects

Atlas `emergency-cards-face.png`, cells0–5 in same corporation order. Emergency status follows RR21 regardless of current holder; Bryan can steal either face state, does not ready it, and cannot take unused corporations' cards. Ordinary hand-steal/discard abilities cannot touch emergencies; emergencies never support. Returned to original corporation on discard, winning face down/otherwise up.

| Cell / card | Printed procedure, in sequence |
|---|---|
|0 Globalsec: Ruthless Tactics |Remove up to4 enemy units from city. THEN increase unrest by1 stage in2 districts not in strike or outage. Not2 stages in one district. Those selected districts count for illness. |
|1 Haas-Bioroid: Underpaid, Overclocked |Choose up to2 resources; increase each chosen resource's quantity in supply by1. THEN gain4 capital and place2 Human First units in city. Direct supply increase is not district exploitation or android movement. |
|2 Jinteki: Mandatory Quarantine |Remove up to4 illness tokens from city. THEN place2 outage tokens in city. Illness tokens do not increase threat during this action. Outages may displace unrest or move from duplicate placements; their Root threat is separate. |
|3 Melange: Energy for All |Each player draws4 actions of a type OF HIS CHOICE, starting active and proceeding clockwise. THEN increase threat by1. Does not say draw4 of different types or that resolving player picks everyone else's types. |
|4 NBN: Sweeps Week |Reduce unrest by up to4 stages in any districts. THEN place2 illness tokens in any districts. Total4 stages distributed, not4 per district. No printed illness immunity. |
|5 Weyland: Massive Reconstruction |Remove up to3 outage tokens from city. THEN place2 orgcrime units in city. Enemy placement/Root cascade remains applicable. |

“Up to” applies only where printed; it does not make later mandatory sentences optional. All six faces were actually read, not inferred from corporation role.

## Printed ordinary action procedures

Each action atlas has20 used cells, four distinct instructions repeated five times: cells0–4,5–9,10–14,15–19 respectively. All100 slots were natively delivered/read, with duplicates collapsed here. Refer to card specifics rather than importing a generic 'good effect' without its later consequence.

| Atlas / cells / card | Procedure and important exception |
|---|---|
|Labor1 /0–4 Efficiency Experts |Move1 android to a district without android. Illness does not increase threat during this action. |
|Labor1 /5–9 High-Risk Investments |Choose3 players; first gains3 capital, second2, third1. Choice order matters; not one equal grant to all. |
|Labor1 /10–14 Labor Solutions |Move up to3 androids to districts without androids, one at a time (RR5.2). THEN place1 orgcrime in any district. No illness exemption. Haas pays only once per turn. |
|Labor1 /15–19 Liquidation |Choose1 district NOT in strike/outage. It immediately produces ALL resources; orgcrime DOES NOT affect this production. THEN increase that district's unrest TO STRIKE. FAQ: this is production without exploitation; no normal exploitation unrest increment or Human First outage. Explicit strike still applies and chosen illness district still triggers illness. Development still applies. |
|Media2 /0–4 Media Circus |Decrease unrest2 stages in any district. THEN place1 Human First in any district. Actual decline may be capped by stable; no illness exemption. |
|Media2 /5–9 24/7 Live Feeds |Choose between decrease unrest1 stage in any district OR remove1 orgcrime. Different contract beneficiaries and possible illness involvement. |
|Media2 /10–14 Puff Piece |Each player MAY draw2 actions of a type of his choice, or3 if he supported THIS offer; resolve active then clockwise. Ordinary offer proposers normally are not supporters. |
|Media2 /15–19 Spin Doctors |Decrease unrest1 stage in up to2 districts. THEN reduce supply credits1; if credits already0, increase threat1 INSTEAD. Not a deficit/negative resource. |
|Security5 /0–4 Arrest Orders |Place1 prisec in any district TO REMOVE all OTHER UNITS in that district. Specific removal instruction differs from ordinary prisec-induced enemy movement; tokens are not units. See ambiguity note for blocked placement edge cases. |
|Security5 /5–9 Full Deployment |Choose ANOTHER player, and choose whether that player draws5 actions of a type of YOUR choice OR flips his emergency faceup. Not a self-target, not recipient's choice. |
|Security5 /10–14 Riot Control |Remove1 prisec from any district TO REMOVE up to2 enemies from city. THEN increase unrest1 stage in1 district not in strike/outage. Prisec sacrifice itself does not pay Globalsec. |
|Security5 /15–19 Scorched Earth |Place1 outage in a district not already in outage TO REMOVE all enemies in that district AND another district in same tier. Printed outage may erase unrest without NBN pay; chosen illness districts matter. |
|Construction6 /0–4 Ark Construction |Place1 development in any district. Max1 applies; chosen/attempted illness district counts even if blocked. |
|Construction6 /5–9 Gentrification |Remove1 outage from any district. THEN place1 prisec there IF it does not contain prisec. Each enemy in that district moves. Outage removal pays Weyland; enemy movement is not Globalsec removal. |
|Construction6 /10–14 Budget Renovations |Remove up to2 outages from city. THEN increase unrest1 stage in EACH district where an outage was removed; removal first makes those districts stable, then protest. |
|Construction6 /15–19 Vanity Project |Choose1 player; that player gains2 capital, or4 if he supported THIS offer. THEN discard1 asset belonging to that player, IF POSSIBLE. No asset does not prevent the capital grant. |
|Biotech7 /0–4 Clean Slate |Remove up to2 illnesses from city. THEN place1 outage in a district WHERE an illness was removed. Illness does not increase threat during this action. No qualifying removal means no qualifying destination for that sentence. |
|Biotech7 /5–9 Clinical Trials |Remove1 illness from any district. Illness does not increase threat during this action. |
|Biotech7 /10–14 Information Procurement |Reduce threat2 IF players spend capital equal to or exceeding player count. Each can spend any amount, active then clockwise. Can be overpaid; no automatic per-player fixed charge. |
|Biotech7 /15–19 Unorthodox Knowledge |Look at top3 events; put1 bottom, return others top in ANY order. RR2.9: Caprice Nisei cannot affect this card and resolver is not bound by stated plan. Fronts stay secret, backs open. |

## Printed asset timing and outcome branches

All34 cells of `asset-cards-face.jpg` were read natively. These are effect summaries for consultation, not new generalized rules. Normal exhaust/optional/timing rules apply; RR golden rule gives asset text priority when incompatible with RR.

| Cell / asset | Trigger, operation, meaningful branch |
|---|---|
|0 Aaron Marrón |When ANOTHER player discards1+ cards to propose counteroffer, those cards go to you instead of discard. Does not capture arbitrary discards or your own cost. |
|1 Alex Westlund |End of Turn choose2 in-play assets and swap. If ANY of yours chosen (including Alex), lose2 capital BEFORE swap. Swaps are not claims (RR61.1). |
|2 Bernice Mai |End of Turn give up to2 hand cards to ANOTHER player, gain capital equal to count given. Explicit exception to inability to trade hand actions; emergency outside hand. |
|3 Braintrust |Doubles quantity of each action-card type on corp sheet; hand size reduced1. Each Melange General entry becomes2 from one deck, still distinct from other entries. |
|4 Bryan Stinson |When claimed, discard to steal2 emergency actions from other players. Faceup or facedown allowed, stays same state, only participating corporations. RR21.6 return rules remain. |
|5 Caprice Nisei |When player proposes offer, MAY exhaust; proposer must state EXACTLY how action will resolve and is bound. RR2.9 excludes Unorthodox Knowledge completely. |
|6 Chief Gorman |After counteroffer proposed, MAY exhaust; return it to countering player's hand unless he GIVES YOU2 capital; he cannot counter again this turn. He ceases countering; cost discards not returned (RR15.8). FAQ excludes Fall Guy counteroffer because Support begins immediately. |
|7 Coach Walden |When player to your RIGHT wins a deal, gain1 capital. Not any adjacent winner. |
|8 Eiko |When player abstains during Support, MAY exhaust; abstainer must play1 card supporting MAIN offer OR lose1 capital. |
|9 Elizabeth Mills |End of Turn GIVE card to another player; THEN choose whether recipient must discard3 actions or draw3 of TOPMOST TYPE on his sheet. Ownership changes before latter effect. |
|10 The Fall Guy |After YOU propose main offer, MAY discard to propose counteroffer as well; immediately proceed Support, skipping other counteroffer chances. FAQ Chief cannot cancel this counteroffer. |
|11 Floyd2X3A7C |When claimed draw5 actions OF ANY TYPES; continuous hand size +5 while owned. Only draw part requires claim. |
|12 Fumiko Yamamori |End of Turn choose resource NOT0; reduce it1 TO gain2 capital. Cannot choose already0 for free payout. |
|13 Gurren Imaishi |When claimed discard to gain5 capital. Not triggered by trade/steal. |
|14 Hernando Cortez |When claimed discard to steal1 asset from ANOTHER player OR gain2 capital. Stealing is not claiming and keeps exhaustion. |
|15 Isabel McGuire |At START of Support, MAY exhaust to place top card from ANY action deck as support of either offer. FAQ owner is NOT thereby a supporting player/supporter of chosen offer and may still normally support either side if eligible. It bypasses Locust's hand-card restriction. |
|16 Jackson Howard |When asset REVEALED, MAY exhaust and choose ANOTHER player; if that player wins deal, you gain2 capital. Predict before outcome, not choose after winner known. |
|17 Lily Lockwell |START of a player's turn, if he has MORE capital than you, MAY steal1 RANDOM hand card. Before Refresh per RR6.6; no trigger on equal capital. |
|18 Locust Company |START of Support, MAY exhaust and choose player; that player cannot play hand cards supporting counteroffer. FAQ still permits Isabel from deck. Does not prohibit main-offer support. |
|19 Marco Cubrero |End of Turn steal1 capital from any player OR2 from richest player; if tied richest choose1 of tied. |
|20 Mark Yale |AFTER player proposes offer, MAY exhaust; that player cannot trade capital/assets until end of deal. Does not generally prohibit all players trading. |
|21 Midori |When determining winner during Resolution, IF support tied, MAY exhaust and decide which player wins. Requires tie; distinguish Tanaka's start-of-Resolution override. |
|22 Monica Singh |When YOU lose as ACTIVE player, MAY steal2 capital from countering player. Not merely losing as any proposer. |
|23 Mr. Li |End of Turn choose any player; that player loses1 capital and draws2 actions OF ANY TYPES. |
|24 “Mr. White” |End of Turn look at ANOTHER player's hand; MAY steal1 of those actions. Card explicitly permits private inspection. |
|25 Naoko Watanabe |When claimed discard to CLAIM top2 assets, ONE AT A TIME. FAQ first card's When You Claim effect must finish before second is claimed. This can change deck/ownership state before second draw. |
|26 Rachel Beckmann |End of EACH DEAL, if hand has0 cards, MAY draw1 action of sheet's TOPMOST TYPE. Not only own turn; emergency doesn't prevent empty hand. |
|27 Saul Eustecio |When COUNTERING player wins, MAY exhaust; YOU gain1 capital, THEN active player gains1. |
|28 Sunny LeBeau |When threat increases1+, MAY draw2 actions of sheet's TOPMOST TYPE. FAQ triggers EACH INSTANCE, e.g. separate Root overflows are separate triggers. Does not multiply by amount in one increase. |
|29 Susan Chen |End of Turn gain2 capital, THEN give card to ANOTHER player. |
|30 Tanaka |START of Resolution, MAY discard and choose active OR countering player; chosen player wins deal. No support-tie requirement. |
|31 Thomas Haas |End of Turn look at extra rival partially under board; MAY swap it with own (both facedown). FAQ must openly announce whether swapped; identity still secret. Can add/remove Federalist identity. |
|32 Toshiyuki Sakai |When claimed discard; draw2 actions OF EACH TYPE; do NOT discard down to hand size THIS TURN. Not a permanent hand-size increase. |
|33 Wong Ya Ching |When effect OF ILLNESS TOKEN increases threat, gain2 capital. Different from Sunny's all-threat trigger; no payout for generic event/demand threat or nonillness Root overflow. |

## Event-specific branches and instance consultation

All16 event faces and their matching backs were read. Placements follow each face's lower table, one per listed district; empty table cells mean no copy. Each face includes a3/4/5 next-turn count. Table below retains distinct upper-half branches, warning identity, and enough location data to find each exact instance. City counts are assessed before lower-half placements because resolution is top-to-bottom. Events do not trigger illness merely by involving ill districts; Root cascades can still add threat. Melange tests total threat from the whole card, not just this upper half.

| Cell / printed event | Upper-half effect; warning back; next turns |
|---|---|
|0 Report: Record Unemployment |If6+ districts protest OR strike, threat+4; unrest back;4 turns. |
|1 Human First Starts Riot |If any Human First in tier2, threat+2; OTHERWISE every Human First moves, highest-numbered district first; Human First back;4 turns. |
|2 Helium-3 Transport Threatened |If any outage in tier3, threat+5; OTHERWISE if outage tier2, threat+3; no sum of both tests; outage back;3 turns. |
|3 Social Apps Spark Revolution |Threat+1 per district in protest OR strike; unrest back;5 turns. |
|4 Humanity Labor Hosts Union Heads |Threat+1 per Human First in city; Human First back;3 turns. |
|5 Gang Wars at All-Time High! |Threat+1 per orgcrime in city; orgcrime back;3 turns. |
|6 Welfare Programs Slashed |Threat+1 per district in STRIKE (not protest); unrest back;3 turns. |
|7 Tri-Maf Leaders Unite! |Threat+1 per orgcrime in city; orgcrime back;5 turns. Same formula as5, different placement/turn instance. |
|8 Crumbling Infrastructure |Threat+1 per district in outage; outage back;5 turns. |
|9 Activist Cells Awaken |Every Human First moves TWICE, starting highest-numbered district. Movement chain/Root rules still apply; do not treat twice as two mandatory district placements regardless of blocks. Human First back;4 turns. |
|10 Beanstalk Owned by Mob? |If any orgcrime in tier3, threat+4; OTHERWISE each orgcrime moves, highest-numbered district first; orgcrime back;3 turns. |
|11 Earthquake Rocks City |If3+ districts in outage, threat+5; outage back;4 turns. |
|12 Rolling Outages Increase |Threat+1 per district in outage; outage back;3 turns. |
|13 Beanstalk Beset by Protesters |If any Human First in tier3, threat+4; OTHERWISE each Human First moves, highest-numbered first; Human First back;3 turns. |
|14 Average Wage Falls Again |If3+ districts in STRIKE, threat+4; unrest back;4 turns. |
|15 Pistoleros Hit Squads Strike! |If any orgcrime in tier2, threat+3; OTHERWISE each orgcrime moves, highest-numbered first; orgcrime back;3 turns. |

Event instance placement tables remain directly consultable in delivered crops, including multiple districts of same component and placement into district10; they do not create an additional procedure family per numeric/location substitution.

## Investments, demand and setup consultation

All12 investment faces read. Demands for individual resource must be met for sector payout; if not, payout0 (FAQ). When met, sector formula uses TOTAL supply of that resource, not surplus above target, and printed maximum caps the total. At demand0, supply0 meets target and earns any stated base amount.

| Investment cell/name | Exact payout rule |
|---|---|
|0 Banking Sector |Credits meets demand:2 +1 per credit, max6. |
|1 Energy Sector |Energy meets demand:3 +2 per energy, max7. |
|2 Entertainment Sector |Entertainment meets demand:2 +1 per entertainment, max6. |
|3 Healthcare Initiative |Illness count2→3 capital,3→5,4+→7. |
|4 Laundering Scheme |Orgcrime count2→3,3→5,4+→7. |
|5 Militarized Police |Prisec count1→3,2→6,3+→8. |
|6 Populist Dismissal |1 capital per district in protest or strike. Outage is stable and does not count. |
|7 Power Siphoning |Outage count1→3,2→5,3+→7. |
|8 Retail Sector |Consumables meets demand:2 +2 per consumable, max6. |
|9 Short Sale |Number of RESOURCE TYPES at1 OR LESS in supply:1→3,2→5,3+→7. Includes0, not only exact1. |
|10 Technology Sector |Tech meets demand:3 +1 per tech, max6. |
|11 Union Agreement |Human First count2→3,3→5,4+→7. |

No listed threshold met means no listed payout (e.g.0–1 illness); payouts are tier values, not cumulative additions of all reached rows.

All9 demand faces use the same five-resource comparison and one failure increase. Exact observed amounts, in order Energy/Consumables/Tech/Entertainment/Credits:

| Demand cell/name | Targets | Failure threat |
|---|---|---|
|0 Network Disruption |0/0/4/4/3 |7 |
|1 Power Grid Overload |2/0/1/2/2 |6 |
|2 Refugee Influx |0/3/1/3/2 |5 |
|3 Retail Shortage |1/1/0/5/1 |7 |
|4 Space Elevator Malfunction |1/0/2/2/6 |6 |
|5 Tourism Spike |2/0/0/5/5 |5 |
|6 Hosting World's Cup |0/1/3/4/2 |5 |
|7 Recreational Drug Ban |0/1/0/6/6 |7 |
|8 Increased Martian Violence |1/2/0/2/6 |6 |

All6 setup faces use the same one-copy-per-listed-cell procedure. Native read names and counts:0 Hit the Bricks4 turns;1 Lights Out4;2 New Arrivals3;3 Outbreak5;4 Slum Lords3;5 Storming the Stalk3. Their actual placement tables are retained for instance consultation; they establish exactly3 initial android districts. No printed setup-specific exception beyond differing state and turn count was found. All7 rivals likewise match RR50/69; Federalist cell0, then Globalsec/Haas/Jinteki/Melange/NBN/Weyland cells1–6.

## Source conflicts, ambiguities and limits

1. **Investment discard destination inside RR:** Complete Setup11 and Demand18.4 explicitly return unchosen cards facedown to TOP. General RR33.2 says discarded investments are shuffled into deck without revealing. Use the explicit setup/demand step for that procedure and flag the wording discrepancy rather than inventing an additional visible discard pile. LTP first-game setup is intentionally different (single investment and specified starting hands), not an alternate complete-game rule.
2. **Sequential costs/effects under impossible states:** Printed “place/remove … to …” and “then” instructions (e.g. Arrest Orders, Riot Control, Clean Slate) must be retained verbatim in scope. RR10 establishes what happens if reserve empty but the packet has no universal 'do as much as possible' or cost-feasibility glossary. Do not manufacture a confident generic ruling for absent prisec, no qualifying removal location, or similar pathological state beyond what exact card/rule text supports. Arrest Orders' specific instruction says REMOVE all other units, whereas normal placement of prisec moves enemies; the specific printed removal instruction is essential, but blocked-placement edge cases are not separately clarified by FAQ.
3. **Complex same-timing combinations:** RR6.4 establishes clockwise active-player priority and chosen order for one player's same-timing assets. It does not provide a modern generalized stack/interrupt framework for every newly enabled trigger or multi-card pathological loop. Retain exact headers and FAQ exceptions (particularly Fall Guy/Chief, Naoko, Isabel/Locust) rather than adding unprinted priority rules.
4. **Threat ending priority:** RR69's normal-end introduction says Federalist loses if game ends during third demand; RR18/28/63/69.3 distinguish final-demand failure reaching25. The controlling threat ending remains immediate and is the one that can let Federalist win with third investment capital. Do not read the normal-end introduction as erasing that explicit branch.
5. **No source absence for ordinary scope:** Complete core procedures, corporation sides, emergencies, and all meaningful printed card instructions were available and read. The FAQ exists as the assigned complete one-page extraction with official identity and capture note; its local PDF was not newly downloaded. Printed facsimiles remain community-located images pinned by hashes, supported by preflight edition corroboration; they are not publisher-hosted new downloads. No claim of independent physical-card inspection or module-authoritative behavior.
6. **Delivery-bound deviations:** Initial full provenance print and one combined RR-tail+FAQ output exceeded the requested6000-character bound, without truncation. Both were redelivered in bounded chunks and this is explicitly recorded in `text-coverage.json`. All remaining source-text reads were bounded to5400 Unicode characters or less; image delivery uses original dimensions. This report does not conceal those two initial protocol deviations.

Suggested consultation anchors for subsequent work: RR3/16/18 for procedure; RR27/35/32 for exploitation/movement/illness; RR11 plus exact corporation panels/FAQ for contracts; the complete printed Liquidation instruction; and the asset table's exact timing clauses. This inventory supplies evidence and branches only; the parent remains responsible for independent review and any summary/question/audit decisions.
