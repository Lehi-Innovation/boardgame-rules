import json,hashlib
from pathlib import Path
r=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957'); o=r/'benchmark-revision13-proposal/independent-review-01'
qs=json.loads((r/'benchmark-revision13-proposal/bank/questions.json').read_text())['questions']
raw='''attrition die/fatigue thresholds; Chairman +1; retiree/card/fatigue destinations|11:903-916
selection eligibility; spending order; windows/PM ties; display depletion/refill; unused pensioners|12:1003-1014
marker repeat condition; latest extra law timing/no marker benefit; vacancy writer bonus once; three writers in stated case|13:1080-1104
seek cost to bank; rightmost applicant per Debt; Debt decrease; residual rightward compression|14:1128-1145
ascending vacancy number; candidate-pool consent; promotions vacancy/fatigue; empty candidate/hirer skip|14:1149-1169
shareholding candidacy; majority announcement/support election; deadlock former choice; Chairman share counts but untradable|15:1176-1194
resource commitment/office bank payment; penalty before roll; lowest die thresholds; retry; catastrophic holder/card/fatigue; no dead action|17:1341-1364
three £5 advances; majority per additional; Chairman included; debt end cap; allocate all balance to other offices and debit|18:1404-1416
mandatory spend to <=£2; extra £2; fit £3 no consent; Company £5 iff no yard ships; sea/China destinations|19:1457-1471;25:1813-1815
home declared; reachable by ships/open route; £1 die and outside-region penalty; mandatory maximum connected placement/ship capacity; writer fallback; home protections; bank bonuses; one success|20:1540-1575
legal target adjacency and Presidency prohibitions; own effect prerequisite; active officer/regiment/alliance dice exhaustion; region/empire penalty and Company zero; used officer six losses|22:1618-1650
£4 tower plus faceup modifier; survivor minimum; loot distribution; tower trophies/dome/flags; open/clear; control/overlay/card; Elephant redirect; catastrophic half up trophies/Commander|23:1674-1710
printed pool; repeated no penalty checks; success £1 or £2 after failure; build/regiment/tax options; tax £2 unsplit and unrest after first; failure unrest; decrement and stop|24:1742-1771
expense emergency £5 debt advances/no new expenses; beyond cap allowed; zero remainder; embarrassment 1/2; expectations then discretionary dividends; failure immediately|27:1897-1934
primary then unrest regions by Army order; primary strength plus unrest/secondary unrest alone; substitute Commander choices; newly exhausted strength>=attack by user interpretation; defeat unrest removal/trophy and failed invasion tower|33:2262-2296;user original
fail -1/lower dilemma then new PM adjacent policy; pass >=0 token/policy then law; restore vote cards; legislated failure finish vote|36:2570-2587
1758/Long start special lined permitted/star mandatory; pass Debt reduction/S/token; fail share cap3/no policy/PM retained/not discarded; PM may oppose|36:2588-2601
nonmanager form with mature strong Company share or workshop; manager consent investment; bank£5 London and supply firm share/value1; invested workshop income/scoring; 10 shares no further share|38:2689-2724
secret strategy/bid at least ship; reveal bid only; single attempt start Presidency; fill after successful President check or after officers opportunity; initiative ships minus successes ascending/ties; connected capacity ships+1; repeat revenue half down; £6 Value|40:2773-2822
ship £1 plus max shares/Value; either treasury expenses; India manager/share dividends; insolvent prison/ships/charter/workshops; rescue options|41:2827-2855;42:2888-2918
finite supplies incomplete actions; proxies cash/trophy/law/dice/regiments; infinite Balance/VP/Votes; all public except facedown blackmail|6:654-661
transferable enterprises/down blackmail/family cash/shares/promises; prohibited personal positions/prizes/spouses/laws/played blackmail/PM/trophies; share replacement; Chairman cannot trade|8:757-807
immediate binding/future nonbinding; capable promise fulfilment/no final calls; simultaneous choice; no second activation transfer|8:762-807
extra setup cards 3 for5/6 for6; shuffle/deal equally; holdings offices/cash/icons; luxury2VP; remaining office cards near board; display three orientations|5:445-470
scenario final turn; Standing left failure; Events finish phase; law finish vote; no final negotiation/promises|9:836-853;29:2008-2012;36:2586-2587
enterprise/share track; law1/PM2; faceup/down blackmail/spouse/trophy; tie-first lower only/second none; victory windows then PM|9:812-853
surviving shares positive printed/failed negative; failure workshop1; survive final attrition retire no cards/fail random card|9:829-835
spouse restrictions permanent/immediate required deals; no transfer; discounts self stack once London/Final; affects spend order|12:1018-1031
fitted ships persist; returned yard unavailable while ship in play; tax same treatment|12:1022-1025;34:2346-2350
writer/officer free destinations/bonus once; luxury£4 +2VP window social; yard£2 matching ship unfitted £1 if fitted vote1 shipping; workshop£5 £1 votes2 failureVP1 manufacturing; share printed cost bank applicant|13:1100-1121;14:1128-1134
must cannibalize prize/pay VP; no possible action return marker supply|13:1083-1099
former Chairman auto next supply/prize else vacant|15:1191-1194
hiring actors/pools/fallbacks and excluded Governors/Chairman/Commanders; China any writer; Governor associated region|16:1234-1254
Envoy open China immediate hire or one closed nonCompany order; repeat then up to2 ship/writer transfers|18:1417-1433
optional2 Army transfers; mandatory trainees; majority incumbent rule and choices; officer promotion/demotion active; no Nepotism|19:1472-1520
President sets sequence; opportunities not mandatory actions; no interrupt; vacant Chairman sequencing only not trade/alliances|20:1527-1539
ships not exhausted by trade; Refresh writer affiliation/divider supply; no final refresh|20:1555-1575;21:1580-1582;36:2609-2621
commander before deploy asks President treasury listed cost moves active; once per turn Deploy/defense strength indivisible; exhaust|22:1618-1626
own Company target closed order/unrest effect; strength zero; loot survivor officers+Commander minimum; no tower trophies|22:1630-1647;23:1681-1696
two successes region partial to associated sea; partial no effect; regiments like officers but bank loot/no loss rolls|24:1753-1762
Envoy or law creates; immediate Chairman any writer; ships only; manager/director send sea; East classification; after Bengal|25:1808-1816
one attempt no export cannot; ship dice; only Company icons; £4 balance/£1 bank personal per icon|25:1818-1823
law retires Governors/removes overlays/partial ships; Director replaced fatigue; GG hires Presidents treasury/time; no new governors; losses skip elimination|26:1841-1859
£3 per Company region first; six unrest each; failed unrest each; successful each region mandatory ship/regiment/tax options/different unrest; at most1 success|26:1860-1889
storm targeted ships outcomes 1/2 safe3/4fatigue or sink5/6sink return unfatigued; Company/extra exempt; China East; firms zone/Hobnob|28:1943-1954;25:1813-1815;42:2919-2922
writer supply/filled flip; Cascade all region closed; connected closure redirect to northernmost if already closed; extra Cascade if no open; one overflow region/event repeated floods allowed|28:1962-1975
Turmoil northernmost top region/Cascade; Windfall£1 writers top+adjacent bank; Shuffle March then current+draw then discards on top; empty stack March last|31:2111-2123
Leader top region sovereign tower else rebellion explosion modifier; March only successful Company revolt Elephant fully inside|31:2124-2132
border connected open/towers nonCompany; wholly inside all orders/unrest; then March|31:2133-2139
attacker empire+modifier vs defender empire strictly greater; flags/capital shatter/new flags shortage; failed attacker tower|32:2192-2208
dominated vs own sovereign only no other empire; strictly greater; failure capital tower|32:2209-2219
half-up trophies/Commander supply; all officer six rout; Governor/card/fatigue supply; overlay/partial ship/unrest remove/dome1 flag; control no loot/no association; invasion only close/Cascade; escalating Standing and no automatic connected losses|29:1987-2012;33:2263-2283
successful invasion capital else top region; Company center/dominated toward sovereign/sovereign shape clockwise skip own dominated; fullyformed arrow border toward capital|30:2045-2082
storm home targets/all/none top; roll strength unrest excluded designer; successful closes once/Cascade; flags shatter/dome/half down die; Elephant conditional redirect shape|33:2297-2325;designer original
PM up to3 may stop; dilemma force stop/select; other discard; first matching policy either direction|34:2330-2343
£1/target bank unpaid returned incl Chairman; windows payment/discard; bonus£1 bank; Power next higher/highest choose other swap|34:2344-2364
PM clockwise vote rounds; £1 family/vote/card rotate only once until resolved; unlimited support track; PM chooses further round/no votes must stop|35:2525-2540
support->oppose allowed reverse forbidden; largest opposed tie incumbent; coalition consent/commit opposition; PM cannot oppose/consent except enterprise promise|35:2541-2564
upkeep even final each prize unpaid return and VP loss; nonfinal writer/filled/dividers/extra/exhausted officers regiments/alliances/turn refresh|36:2602-2621
one extra per player despite firms; supply piece; largest firm's total dividend cap; spouse discounts; unplaced/zero unavailable; final regardless Company before ordinary/no display|37:2651-2674
bank investment London; trade India; London fitting/bid; both expenses; India dividends; no gifts family treasury either way|37:2635-2647;39:2730-2739;40:2776-2779
after Family before Hiring; investments/strategy; manager firm conflicts/PM interfirm|38:2679-2688
fit£3 bank London consent; no Company/extra; player ship buyback owner consent London unfatigued£3/fatigued£2 Shipping|39:2729-2740
nonmanager majority shareholder consent; charter/cubes same positions; ships/funds/shares transfer old resets|39:2741-2748
all shareholder consent immediate binding; highest primary ties choice; overflow owners consent returns; consolidate treasuries/ships/shares and secondary family|39:2749-2768
Hobnob no bid/trade/dividend; retains marker; storm immunity; expenses still|40:2782-2785;42:2913-2922
10 share investment no share; normal workshop/Company restrictions; bank£5; value-1 each; rescue remainder lost; immature restriction persists|41:2845-2850;38:2689-2724
only one other firm; both own expenses and distressed outstanding before merger|41:2852-2855
all shareholders agree; dissolution prison/ships back/charter; workshop permanently invested|37:2648-2650;41:2839-2843
firm value per share; prison -1; sum fractions rounddown; before ordinary; special retire regardless Company|37:2665-2674;41:2839-2843
five prizes printed cost/upkeep/VP/windows|board PDF native
scenario start/end turns and dereg status|scenario fronts PDF native
1710/1758 Standing Debt all treasury laws regiments ships and Bengal control|scenario fronts PDF native
1813 Standing Debt treasury laws regiments ships share2 GG China/control|scenario fronts PDF native
turn1-3/4-6/7-8 first-second Power VP and tied-first lower|board PDF native
initial four Power markers; lined/star Standing/Debt spaces; S location|board PDF native
Foreign unrest no strength or resulting tower; closes once normal/Cascade|designer original;33:2303-2312
connection zero ordinary failure; Fraud capped available Balance; Impeachment holder supply/card vacant; Oversight incumbent officer eligible|errata originals
Balance5 VP0 alliance printed Army/loot matching faceup; scenario map/cards dates Turn/PM|4:325-381
nine phases order; firms between Family/Hiring; first London skipped|10:862-887;11:898-900;38:2679-2682
Chairman/former first clockwise optional pensioners prize cost/VP; retirement cash held then bank season end|11:918-928
empire last dominated gone capital flag removed regardless Rebellion/conquest|7:707-714
firm Value1-10 per-share VP table|42:2962-2982;firm charter component
Chairman first clockwise; all actions done new shares|13:1076-1082;14:1135-1145
office ribbon sequence Chairman/Director or GG/Shipping/MA/Bombay/Madras/Bengal/China; vacant skipped|17:1331-1339;26:1855-1857;board
storm first then events number die; targeted all nonCompany/nonextra ship checks; tile face event location top back successive|28:1939-1961
Elephant tail attacker head defender; sovereign invasion/dominated rebellion; large/dome sovereign small/no dome dominated|6:698-701;7:718-727;32:2186-2215
user-approved strength2 alliance stops1; exhaust whole alliance once, clear unrest/trophy/invasion tower when applicable; general >= interpretation; not verified official|human originals;33:2285-2296
ordinary Crisis always March after any result; invasion success Imperial Ambitions|32:2186-2191;30:2049-2051
successful rebel sovereign return flag close all else Cascade|32:2216-2219
printed law bottom-right starting support to Votes before voting|34:2365-2367
firms before Company expenses initiative then others; ties manager windows then PM clockwise|41:2827-2830
GG office treasury£1/die no penalty; personal£1 per region bank|26:1866-1871;17:1348-1349
acting selector peek any display blackmail; owner may allow negotiation peeks|12:1008-1009;8:779-783
interleave Debt allocation allowed same3/majority/end limits|18:1406-1416
luxury/yard/workshop and Shipping three forms pay bank|13:1107-1119;19:1462-1471
President treasury£1/die; printed order amount balance; repeat firm-filled half down; President/writer bonuses unchanged bank|20:1549-1575;40:2817-2820;41:2877-2879
Commander+own officers £1 then clockwise officers; bank regiment/alliance£1 each; repeat until exhausted pool|23:1684-1692
Elephant in conquered facing other becomes center shows Company rebellion|23:1705-1707
£1 debt/officer/regiment/ship; Commander exempt; China East counts|27:1903-1906;25:1813-1815
shareholder waiver manager consent; total actual paid marker Balance track incl0; India remainder London|42:2888-2918
final no blackmail except text expressly permits|9:843-847
Envoy office£1 die no penalty then up to2 one writer/ship Presidency/sea to other includes China ships|18:1417-1433;25:1813-1815
up to2 officer/regiment Army other Army active top; all trainees any3 top|19:1476-1484
adjacent different Presidency writers divider on connection retain affiliation Refresh|21:1580-1582
ordinary invasion close all/open or Cascade if none; no double Rebellion/Foreign closing|29:2005-2007
investment no fixed order; all finished when none wants more then Strategy|38:2683-2688;40:2773-2775
secondary shares/ships consolidate into primary|39:2763-2768
corrected Fraud start Revenue dice each own officeholder twice highest before cap|errata original;fronts PDF
multiple successes permitted; targeting/effect/resource/check constraints; catastrophic stops removes commander/half trophies|22:1627-1650;23:1708-1710
blackmail effect one use kept own faceup; power retained both orientations|12:1039-1042
Chairman chooses number affordable Balance; cost shares£1 each holder/Chairman; no shareholder waiver; Standing +1 iff total>Expectations|27:1925-1934;42:2895-2907
marker off actions start; repeat only if already there start phase so no first repeat|13:1080-1089
Company Balance charged; lower marker expense total|27:1903-1906'''
lines=raw.split('\n');assert len(lines)==114,len(lines)
rows=[]
for q,l in zip(qs,lines):
 c,s=l.split('|');rows.append(dict(id=q['id'],question=q['question'],independent_asked_clauses=c.split('; '),original_source_anchors=s))
record={'stage':'QUESTION-AND-ORIGINALS ONLY; saved before opening candidate key/scope/corrections/coverage or baseline','question_count':114,'decompositions':rows,'principle':'Broad procedures include their real steps, constraints and consequences. Adjacent true material outside the requested action is not mandatory merely because nearby in the rulebook.'}
(o/'question-only-prereview.json').write_text(json.dumps(record,indent=2)+'\n')
(o/'question-only-prereview.md').write_text('# Independent question-only prereview\n\nSaved before key/scope/correction/coverage access.\n\n'+'\n\n'.join(f"**{x['id']}** {x['question']}\n\nAsked: {'; '.join(x['independent_asked_clauses'])}.\n\nOriginal anchors: {x['original_source_anchors']}" for x in rows)+'\n')
print('saved',len(rows),'prereviews',hashlib.sha256((o/'question-only-prereview.json').read_bytes()).hexdigest())
