# Source audit — PASS (scoped)

Candidate: `/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-final-stamped-iteration-01/summary-snapshot.md`

SHA256: `26ae8cecaa248b4321b6d6d7f601938e52e702057e9b2e4883910c2111f6a6ab`

Complete standard 3–6-player John Company: Second Edition (2022), Rules of Play Second Printing 2023: 1710, 1758, 1813 and Long 1710, including core deregulation/firms. Crown/solo/two-player and optional Draft excluded. Individual component powers, starting holdings and exact scenario maps remain lookup material. Includes the explicitly user-adopted general defense-strength interpretation.

Official claims: **PASS**. User-interpretation fidelity: **PASS**. Overall scoped result: **PASS**. Scoped signoff: **true**.

No material inaccuracies or consequential common-procedure omissions were found. This is a manually reached audit conclusion after complete candidate and relevant original rulebook delivery, correction/ruling reads, original PDF renders and the claim-by-claim checks below. The stamped verification banner was not used as evidence.

## Authority qualification

Original supplied Second Printing rulebook, original publisher-linked PnP board/cards, applicable official correction list/original post and supplied designer originals. These were inspected directly; prior audits and the verification banner were not evidence.

The general newly exhausted defense strength ≥ attack comparison is accepted solely as the explicitly attributed user interpretation in the two original human-authority files. The public designer Foreign Invasion and Fraud rulings are separate authorities. No private publisher email was inspected. This is **not** an unqualified independently verified official-only signoff.

## Findings

None. There are no unresolved findings.

## Deliberate defense-rule authority difference

The printed rulebook (extraction LF2285–2289; printed/PDF page33) says: 

> Ƙ Mounting Defense. The Commander associated with the region 
> must exhaust pieces in the Army equal to the strength of the Crisis 
> or as many as possible. If the newly-exhausted pieces do not equal 
> the strength of the Crisis, the Crisis succeeds. Perform the steps of 
> Region Loss (page 29). 

The candidate explicitly attributes the ≥ comparison to the user at LF216 and LF464–470. The human source, LF10, authorizes “total newly exhausted defense strength equal to or greater than attack makes the Crisis fail.” The candidate applies this generally and correctly includes a strength-2 alliance defending strength1. Normal unrest removal, actual-Commander trophy and failed normal Invasion results remain faithful to official LF2290–2296. The Foreign Invasion designer clarification is a separate public designer source.

## Source-read and visual evidence

The source-read record contains exact paths, SHA256 hashes, inclusive one-based physical LF ranges, all actual text deliveries, native original-to-derivative provenance, page numbering and actual visual inspections. Relevant rulebook delivery was LF1–3015 (all printed pages1–42), plus LF3290–3306 for the 2023 printing identification. The candidate was read at LF1–499. LF numbers use `text.split("\n")`; they are not printed page numbers. Rulebook PDF physical and printed pages coincide for the inspected pages. PnP Bridge physical7–11 are printed sheets18–22; PnP Fronts physical and printed sheet numbers coincide.

Original native PDFs were rendered with PyMuPDF1.28.2 into this directory. No earlier audit renders were imported. Ancillary supplied PNGs were hashed only. Native board figures confirm the prize table, ordered zero-power positions, share queue, Standing/Debt lined and starred spaces, scenario endpoints and power awards. Native scenario fronts confirm all retained setup figures; reverse maps establish the permitted card lookup and Bengal overlay. Rulebook page33 confirms the circle redirect; page42 confirms the firm-value VP symbols. Native corrected card fronts confirm the retained effects.

## Checked claims

Each row records a manual comparison; full paths/hashes and exact LF references are in the JSON. “rules” refers only to the supplied original extraction; “fronts_text” is this audit’s native original-card extraction. Board/icon checks cite the original PDF physical page.

| ID | Candidate LF | Claims and assessment | Original evidence |
|---|---:|---|---|
| C01 | 23–27 | Edition, player scope, scenarios and exclusions: Matches the multiplayer scope; Crown and optional Draft are expressly outside this audit. | rules LF334–388 (printed 4); rules LF2625–2634 (printed 37); rules LF3300–3304 (printed 48) |
| C02 | 29–34 | Component types and quantities: Family and enterprise counts, office counts, overlays and resource types agree. | rules LF44–150 (printed 2–3); rules LF389–407 (printed 4) |
| C03 | 36–36 | Component limits, proxies, unlimited tracks and hidden information: Correct exceptions and temporarily hidden firm decisions. | rules LF654–666 (printed 6); rules LF2774–2789 (printed 40) |
| C04 | 38–40 | Regions, strength, sovereignty, empires and mandatory empire decline: Tower/dome distinction and global last-dominated-region rule retained. | rules LF669–726 (printed 6–7) |
| C05 | 42–45 | General setup, date, loot, local alliances and starting resources: Board and scenario-card instructions correctly combined. | rules LF335–388 (printed 4) |
| C06 | 46–46 | Scenario setup-card dealing and all kinds of starting holdings: Extra-card counts, placed pieces, ship destinations and luxury points agree. | rules LF416–425 (printed 5); rules LF453–477 (printed 5) |
| C07 | 47–47 | Remaining offices, combined prestige/blackmail deck, law deck: One mixed display deck, correct orientations and unused offices. | rules LF427–433 (printed 5) |
| C08 | 49–54 | Scenario applicability, Long 1710 duration and initial position: Deregulation applicability and eight-turn Long scenario correct. | rules LF360–380 (printed 4); rules LF2628–2630 (printed 37) |
| C09 | 56–61 | 1710 and Long scenario figures: £10/0 debt, £3 treasuries, Royal Protection, one regiment per Army, no Company ships; Long matches initial position. | fronts_text LF1017–1034 (printed PnP Fronts physical9, card74); rules LF374–380 (printed 4) |
| C10 | 62–65 | 1758 figures, Bengal control and Governor: £12/3 debt, £4 treasuries, Calico Acts and East Indian ship verified; Bengal overlay visible on scenario reverse. | fronts_text LF997–1016 (printed PnP Fronts physical9, card75); errata LF200–204; bridge PDF physical9 / printed sheet20: 1758 reverse map includes Bengal Governor overlay |
| C11 | 63–65 | 1813 figures, overlays, China and corrected control/share tokens: £10/0 debt, £3 treasuries, named laws, two regiments per Army and one Company ship per sea agree. | fronts_text LF973–996 (printed PnP Fronts physical9, card76); errata LF192–199 |
| C12 | 58–67 | Initial power, Standing, deregulation thresholds and turn endpoints: Native board inspected: power ordering, Standing S and lined/starred thresholds, dates/final-turn arrows match. | rules LF345–346 (printed 4); rules LF2588–2601 (printed 36); board PDF physical1: power tree, Standing/Debt tracks and Turn track |
| C13 | 69–79 | All prize costs/upkeep/VP/windows: Native original board inspected: all five prize rows match, including the free-upkeep zero-VP £2 prize. | board PDF physical1: all five prizes |
| C14 | 81–85 | Phase order, first-turn London skip and special vote timing: Standard phases and inserted firm phase agree. | rules LF862–887 (printed 10); rules LF898–900 (printed 11); rules LF2588–2593 (printed 36); rules LF2679–2682 (printed 38) |
| C15 | 87–89 | Office attrition, Chairman stress, pensioners and fatigue destinations: Modified result bands, retirement order, costs and set-aside spending agree; Commanders have no office card. | rules LF901–928 (printed 11) |
| C16 | 91–91 | Prestige ordering, eligibility, skip, no replacement, complete refill: Spending/windows/PM ordering correct; firm special retirement is otherwise normal and confers eligibility. | rules LF1002–1014 (printed 12); rules LF2651–2660 (printed 37) |
| C17 | 93–93 | Spouse restrictions, discount timing, returned shipyards: Personal stacking discounts and fitted-ship persistence/blocked repurchase retained. | rules LF1018–1031 (printed 12); rules LF2346–2350 (printed 34) |
| C18 | 95–95 | Prestige enterprises and one-time blackmail; final power: Correct transfer and power treatment. | rules LF1033–1042 (printed 12) |
| C19 | 97–104 | Family order, opportunity marker double and extra-action laws: Phase-start test, optional doubling, main marker placement and most-recent extra law accurate. | rules LF1076–1099 (printed 13) |
| C20 | 106–106 | Mandatory prize-piece reuse and impossible family action: VP loss, applicability to firm shares and marker return correct. | rules LF1083–1085 (printed 13); rules LF1097–1099 (printed 13) |
| C21 | 110–111 | Writer bonus and officer enlistment: Four-vacancy writer bonus only once per turn; training destination accurate. | rules LF1100–1106 (printed 13) |
| C22 | 112–114 | Enterprise purchases, costs, bonuses, votes and VP: Correct £4/£2/£5 costs and unfitted-ship destination. | rules LF1107–1121 (printed 13) |
| C23 | 115–117 | Seek shares queue costs and conversion/debt procedure: Native board confirms five queue spaces £2/£3/£3/£4/£5; rightmost/debt and preserved order correct. | rules LF1128–1145 (printed 14); board PDF physical1: Stock Exchange arrows and five spaces |
| C24 | 119–123 | General hiring order, promotions and skipped vacancies: Ascending vacancies, fatigue transfer, candidate-pool consent and unavailable hirer handling accurate. | rules LF1146–1169 (printed 14) |
| C25 | 125–131 | Nepotism and normal Commander exception: Chairman election and ordinary Commander assignment exempt; individual law powers remain component-specific. | rules LF1155–1157 (printed 14); rules LF1485–1494 (printed 19); rules LF1513–1520 (printed 19) |
| C26 | 133–142 | All office hirers and eligible candidate pools: Matches rulebook pools, including Presidency-specific Presidents and exclusion of Commanders as Governor candidates. | rules LF1234–1254 (printed 16); rules LF1853–1857 (printed 26) |
| C27 | 144–144 | Chairman majority election, deadlock and empty Court: Pure majority, support, share movement/restrictions and forced former Chairman correctly summarized. | rules LF1175–1194 (printed 15) |
| C28 | 146–152 | Operation sequence, vacancies and Presidency order autonomy: Ribbon order checked visually on original board; uninterrupted opportunities and later Governorship hiring agree. | rules LF1331–1339 (printed 17); rules LF1527–1539 (printed 20); rules LF1816–1816 (printed 25); board PDF physical1: operation ribbon |
| C29 | 150–150 | Success checks, cash location, penalties, retries, catastrophe, dead actions: All result bands and resource commitment match, with office-specific limits qualified. | rules LF1341–1365 (printed 17) |
| C30 | 154–156 | Bonuses and duplicate activation prohibition: Invested-workshop exclusion and fitted-yard bonus accurate. | rules LF1894–1896 (printed 27); rules LF770–776 (printed 8); rules LF2719–2720 (printed 38) |
| C31 | 158–162 | Company expenses, emergency loans including maximum Debt: Resource counts, no Commander expense, loan increments/cap behavior and Standing penalties match. | rules LF1897–1920 (printed 27); rules LF1812–1815 (printed 25) |
| C32 | 163–166 | Expectations, dividends, Standing changes and immediate Revenue failure: Strict dividend threshold and no shareholder waiver correct. | rules LF1900–1902 (printed 27); rules LF1921–1934 (printed 27); rules LF2895–2902 (printed 42) |
| C33 | 168–182 | Storm die ordering, event counts, stack location and ship eligibility: Storm resolution, fatigue/sinking, China and Hobnob exceptions correct. | rules LF1939–1961 (printed 28); rules LF1812–1815 (printed 25); rules LF2919–2922 (printed 42) |
| C34 | 184–184 | Writer loss and complete cascade behavior: Destinations, connected closed-order substitution, once-per-tile initiation and multiple receipts match. | rules LF1962–1975 (printed 28) |
| C35 | 186–190 | Turmoil, Windfall and Shuffle: Locations, bordering regions, shuffle order and empty-stack exception correct. | rules LF2111–2123 (printed 31) |
| C36 | 191–192 | Leader and Peace: Leader sovereign/domination split, restricted redirect and Peace border/inside effects correct. | rules LF2124–2139 (printed 31) |
| C37 | 193–196 | Crisis classification, tail/head and March timing: Ordinary crisis distinguished from Foreign Invasion location. | rules LF2186–2197 (printed 32); rules LF2210–2215 (printed 32) |
| C38 | 198–200 | Invasion and Rebellion strength, flags, decline, failure penalties: Strict comparisons, empire scope, flag exhaustion and shattering correct. | rules LF2192–2219 (printed 32); rules LF713–714 (printed 7) |
| C39 | 202–206 | Company attack propagation, order and three strength cases: Primary first, Army/Commander order and unrest-only secondary strength accurate; Foreign Invasion exception sourced separately. | rules LF2262–2283 (printed 33); foreign LF1–1 |
| C40 | 208–216 | Vacant defense offices, mandatory exhaustion and trophy handling: Military Affairs acts directly, Chairman fallback; substitutes never gain/lose trophies; alliances exhaust whole. | rules LF2274–2277 (printed 33); rules LF2285–2296 (printed 33); rules LF1622–1626 (printed 22) |
| C41 | 216–223 | User-adopted defense threshold and consequences: General newly-exhausted strength ≥ attack rule faithfully attributed to user; not treated as independently verified official wording. | scope LF3–25; human LF5–11; rules LF2290–2296 (printed 33) |
| C42 | 225–225 | Complete Region Loss, destinations, closures and escalating humiliation: Commander/officer/Governor handling, face-down loot token, no repeat loot, loss-specific closure, scaling Standing and phase completion all correct. | rules LF1987–2012 (printed 29); rules LF1858–1859 (printed 26); foreign LF1–1 |
| C43 | 227–227 | Elephant March/Imperial Ambitions/fully formed empires: Successful capital priority, Company/domination classification and clockwise/redirect placement accurate. | rules LF2045–2082 (printed 30) |
| C44 | 229–231 | Law drawing, forced dilemma, policy direction and initial support: Up to three one-at-a-time choices and first matching policy space correct. | rules LF2330–2343 (printed 34); rules LF2365–2367 (printed 34) |
| C45 | 233–233 | Voting sources, card use across rounds, opposition and coalitions: Once-per-vote card use, no-vote stopping, irreversible opposition and PM restriction correct. | rules LF2525–2564 (printed 35) |
| C46 | 235–235 | Pass/fail resolution, policy shift, law effects and legislated failure: Correct order and restoration of voting cards retained. | rules LF2570–2587 (printed 36) |
| C47 | 237–244 | Tax, all-window tax, bonus and power policy: Payments/destinations, Chairman taxation, lost VP, fitted ship persistence and highest-marker exception accurate. | rules LF2344–2364 (printed 34); rules LF1033–1037 (printed 12) |
| C48 | 246–258 | Prize upkeep, final-turn distinction and all refresh destinations: Writers, filled tokens/dividers, extra ships, Army activation, alliance exhaustion and no routine ship fatigue removal correct. | rules LF2602–2621 (printed 36); rules LF1950–1954 (printed 28) |
| C49 | 262–264 | Chairman debt consent/cap and all Balance allocation: Three free advances, consent for each subsequent one, interleaving permitted and all allocation retained. | rules LF1403–1416 (printed 18) |
| C50 | 266–268 | Director envoys, immediate China hire and two later transfers: Resources, non-Company order eligibility and sequencing correct. | rules LF1417–1433 (printed 18); rules LF1808–1815 (printed 25) |
| C51 | 270–272 | Shipping mandatory spend, acquisition priorities, payments and destinations: At most £2, £2/£3/£5, no consent for Company fit and no direct yard payout correct. | rules LF1457–1471 (printed 19); rules LF1812–1815 (printed 25) |
| C52 | 274–276 | Military Affairs transfers, all trainees and Commander appointment: Top-half destination, piece counts including Commander, tie retention and no nepotism accurate. | rules LF1472–1494 (printed 19); rules LF1495–1520 (printed 19) |
| C53 | 278–282 | Presidency operation order, vacancy and uninterrupted Trade retries: Chairman only orders when President absent; region declaration and penalties correct. | rules LF1527–1554 (printed 20) |
| C54 | 284–284 | Successful Trade capacity, route, writers, privileges and personal payouts: One order per ship, own connected route, tokens after writers, one success, no other home region, half refills and payouts correct. | rules LF1555–1582 (printed 20–21); rules LF2817–2820 (printed 40) |
| C55 | 286–288 | Alliance purchase timing, whole-piece use and refresh: Start-of-Commander timing, President approval/funds, temporary use and exhaustion correct. | rules LF1617–1627 (printed 22); rules LF2618–2619 (printed 36) |
| C56 | 290–294 | Repeated Deploy, target boundaries, dice, empire penalties and losses: No one-success cap, effects required for Company target, target counted once, and losses after every attempt correct. | rules LF1627–1650 (printed 22) |
| C57 | 296–304 | Deploy loot minimum, cyclic distribution and trophies: Minimum surviving officers+1, Commander plus own officers, clockwise others, bank per regiment/alliance piece, repeat cycle correct. | rules LF1674–1695 (printed 23) |
| C58 | 306–321 | Deploy political changes, Governorship token/overlay/card and catastrophe: Distinct destinations and postconquest hiring, existing-region loot minimum, GG exception and trophy loss correct. | rules LF1693–1710 (printed 23); rules LF1842–1847 (printed 26) |
| C59 | 323–338 | Governor Administer pool, results, build stages, regiment and tax: Printed pool lookup, decrement every attempt, prior-failure bonus, unrest, two-success ship, unsplit tax and repeat limits accurate. | rules LF1742–1771 (printed 24) |
| C60 | 340–351 | China creation/hiring, treasury, no-export prohibition, one attempt and payouts: All creation routes, eastern treatment, controlled exports only, £4 and £1 per icon accurate. | rules LF1808–1823 (printed 25) |
| C61 | 353–357 | Governor General replacement, hiring, offices, regions and action: Governors pensioned, fatigue transferred, treasury/turn position, upfront revenue, sixes/unrest, compulsory benefits and one success correct. | rules LF1841–1889 (printed 26) |
| C62 | 359–368 | Deregulation special vote and all pass/fail exceptions: Thresholds, turn timing, no policy, PM may oppose/stays, debt reduction, S reset and ±3 cap agree. | rules LF2588–2601 (printed 36); rules LF2628–2630 (printed 37) |
| C63 | 370–374 | Firm treasuries and normal/special retirement: No family treasury transfer; dividends limit actual retirement spending; one retirement even across firms; final scoring ordering correct. | rules LF2631–2674 (printed 37); rules LF2710–2717 (printed 38) |
| C64 | 376–378 | Firm phase timing, investment conflicts and strategy transition: Investment after Family and before Hiring, no set order, manager/PM conflict resolution accurate. | rules LF2679–2688 (printed 38); rules LF2773–2775 (printed 40) |
| C65 | 380–381 | Firm formation, investment, eligibility restrictions and share cap: Eligible contributions, bank £5, first cube/share/charter, weak/immature and Chairman restrictions, invested workshops and ten-share limit correct. | rules LF2689–2724 (printed 38); rules LF1184–1187 (printed 15) |
| C66 | 382–383 | Firm ships and hostile takeover: Owner consent, London payment, fitting bank versus buyback Shipping destination, prices and no-manager restriction correct. | rules LF2729–2748 (printed 39) |
| C67 | 384–385 | Normal merger and voluntary dissolution: All shareholders, primary-value ties, excess consent/return and all dissolution destinations correct. | rules LF2749–2768 (printed 39); rules LF2648–2650 (printed 37); rules LF2839–2843 (printed 41) |
| C68 | 387–400 | Strategy, bids, eligibility, closed ports and Hobnob: One attempt, ships required, secret strategy/open bids, Hobnob expenses/no dividends/storm exemption accurate. | rules LF2773–2790 (printed 40); rules LF2919–2922 (printed 42) |
| C69 | 402–402 | Firm trade checks, initiative/ties and Presidency timing: Firm checks before any Presidency actions; filling follows President success or all other office opportunities; ties chosen by President/Chairman accurate. | rules LF2791–2809 (printed 40) |
| C70 | 404–404 | Firm capacity, own route, one fill, refilling and value advance: Ships+1, open home port, distinct once-per-own-order and halved other-trader fills, per-£6 value accurate. | rules LF2810–2822 (printed 40) |
| C71 | 406–410 | Firm expense ordering, costs, rescue and dissolution: Initiative/windows/PM order, shares-or-value maximum, both treasuries, permanent invested workshops, rescue loss/value and one-other-firm merger accurate. | rules LF2827–2855 (printed 41) |
| C72 | 412–412 | Firm dividends, manager consent, actual payout marker and sweep: India only, £1/share plus manager, two-party waiver, total actual payout, Hobnob retention and remainder transfer agree. | rules LF2888–2918 (printed 42) |
| C73 | 414–437 | End conditions, game-over restrictions and ordinary final scoring: Company failure timing, no negotiation/promises, firm-before-normal ordering and random failure alternative retained. | rules LF811–853 (printed 9); rules LF1900–1902 (printed 27); rules LF2008–2012 (printed 29); rules LF2586–2587 (printed 36); rules LF2665–2674 (printed 37) |
| C74 | 422–441 | Final firm scoring, Debtor prison, power rates/awards and tiebreaks: Per-player aggregate rounding, −1 prisoner, current Court value, workshops exception, native firm value rates and board awards correct. | rules LF812–835 (printed 9); rules LF850–853 (printed 9); rules LF2665–2674 (printed 37); rules LF2839–2841 (printed 41); board PDF physical1: Power Award panel; pdf PDF physical42 / printed42: firm charter Value rate symbols |
| C75 | 443–462 | Negotiation assets, share replacement, promises and cash location: Allowed/prohibited transfers, binding immediacy, nonbinding future promises, guarantor choice and no double activation accurate. | rules LF757–807 (printed 8); rules LF663–666 (printed 6); rules LF2635–2647 (printed 37) |
| C76 | 464–470 | User interpretation wording and attribution: Correct general ≥ comparison, whole alliance example and source boundary; no claim of inspected email. | scope LF3–25; human LF5–11; rules LF1622–1626 (printed 22); rules LF2285–2296 (printed 33) |
| C77 | 476–476 | Company Fraud cap and corrected start-of-Revenue timing: Designer confirms alternative2; candidate example and dated attribution faithful. | ruling LF1–1; errata LF227–235; fronts_text LF83–92 (printed PnP Fronts physical1, card2) |
| C78 | 194–194 | Foreign Invasion designer exception and single closure: Die-only strength, half rounded-down towers, storm/top-stack region targeting and circle redirect agree. | rules LF2297–2316 (printed 33); foreign LF1–1 |
| C79 | 478–480 | Foreign Invasion FAQ and errata provenance: No unrest added to primary Foreign Invasion; secondary crises retained; no double close/cascade. | foreign LF1–1; errata_original LF51–62; publisher LF3065–3076 |
| C80 | 480–480 | Retained corrected-card effects and setup corrections: Zero-dice forced rerolls fail; fraud timing/cap; impeachment destinations; previous Commander eligible under Military Oversight all match. | errata LF192–242; fronts_text LF6–25 (printed PnP Fronts physical1); fronts_text LF539–547 (printed PnP Fronts physical6, card51); fronts_text LF603–614 (printed PnP Fronts physical6, card47) |
| C81 | 472–498 | Quick player reference and source boundary: Reference restates checked procedures without adding conflicting rules; component consultation expressly required. | rules LF862–887 (printed 10); rules LF897–928 (printed 11); rules LF2679–2682 (printed 38); rules LF2602–2621 (printed 36) |

## Important omission review

- **Setup and scenarios:** No consequential common setup omission found. Initial figures for every scenario, extra-card counts, complete holdings placement, corrected control/share tokens, map-copy instruction and Long deregulation are present. Exact scenario map pieces and individual dealt holdings may be read from cards as permitted.
- **London and Family:** Attrition/fatigue/destinations, retirement spending/windows/display exhaustion/refill, restrictions/discounts, forced prize-piece reuse, extra-action timing and debt/share conversion retained.
- **Hiring and operations:** All standard candidate pools, nepotism, promotions, fallback elections, vacant offices, operation order, optional/mandatory actions, costs, destinations, retry and success limits reviewed. Military Oversight is an individual law exception to ordinary Commander appointment, available on the card; the retained correction is accurate.
- **India and Company-region changes:** Every standard event, stack-versus-Elephant location, storm exceptions, cascade limits, empire decline, Invasion/Rebellion classification, primary/secondary strengths, substitute defense actors, trophy exclusions, Region Loss destinations/escalation, single Foreign Invasion closure and March redirects retained. The accepted user defense comparison is separately attributed.
- **Revenue, Parliament, Refresh and ends:** Full expense/loan/expectation/dividend order, maximum Debt loans, policy/vote timing and consequences, card vote exhaustion, tax destinations, upkeep, refresh and all end timing exceptions retained.
- **Firms:** Full core system checked: formation/investment limits and bank funding, two treasuries, owner consent/prices, hostile takeover, merger/dissolution, secret strategies and open bid amounts, one attempt, initiative/filling limits, expenses/rescues, actual dividends, special retirement and final aggregate rounding.
- **Negotiation and scoring:** Transfer legality, family replacement on shares, immediate binding agreements, future promises, repeated activation, no game-over negotiation/promises, power awards, Court/workshop success/failure effects, firms-before-normal scoring, random failure card and tie order retained.
- **Individual components and corrections:** Exact individual law/spouse/promise/failure powers and scenario maps intentionally remain component lookups. Every retained corrected-card claim was checked against original errata and native fronts. Examples of component overrides, such as Royal Protection, Military Oversight and Industry’s Greed Condemned, are not interpreted as absent merely because the generic procedures do not reprint every card.

## Limits

- This is a source audit, not a blind-reader or gameplay test.
- No private publisher email was accessed or independently verified.
- Exact individual component effects/holdings/maps are permitted lookup material and not reproduced exhaustively by the candidate.
- The supplied ancillary PNGs were hashed but not substituted for native original PDF inspection.
- Model/effort and independence attestation at the orchestration level must be verified by the parent; this report does not self-certify hidden runtime settings.
