from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-03/grading-reader-a/block-01')
p=json.loads((base/'packet.json').read_text())
# Every grade and atom disposition below is an explicit human-semantic selection.
selections=[
('Q001','The complete attrition passage resolves every modifier, threshold and destination.',[
([0],'Simultaneously roll one die for each held office card.'),
([1],'Add one per fatigue on that card; Chairman also adds one.'),
([2,3,4],'Modified 1–2: nothing; 3–4: add fatigue; 5+: retire.'),
([5],'Chairman also adds one.'),
([6,7,8],'Move retiree to Pensioners, flip card into Vacant Offices, return its fatigue to supply.')]),
('Q002','The complete prestige passage supplies all eligibility, ordering, tiebreaking and cleanup facts.',[
([0],'Players who completed at least one pensioner retirement **or an eligible firm special retirement during this London Season** must each take or discard one display card, in descending actual total retirement spending.'),
([1],'If the display becomes empty, immediately skip every remaining eligible player.'),
([2],'in descending actual total retirement spending.'),
([3,4],'Ties: most total windows, including new prizes, then clockwise from PM.'),
([5,6,7],'discarding all remaining cards and refilling exactly three: prestige faceup, blackmail facedown, even if nobody took a card'),
([8],'Return all remaining Pensioners to their supplies.')]),
('Q003','The main-action and law rules are complete, and the stated fixture correctly yields three writers.',[
([0,1],'1. Check where your opportunity marker was **at phase start** (it begins off the board).\n2. Choose a main family action: take it once, or **may take it twice if the marker already matched it**.'),
([2],'**Place/move the opportunity marker onto your chosen main action.**'),
([3,4,5],'After the main action, only the latest passed extra-action law may grant its extra action. This extra action is never doubled by the marker and never moves the marker.'),
([6],'With at least four vacant offices, place one additional writer **once this turn**, so a doubled Writer action can place three total.'),
([7],'Four vacant offices permit the once-per-turn extra writer, and the matching opportunity marker allows the main Writer action twice; therefore three writers can be placed.')]),
('Q004','Share issuance, applicant movement and initial bank payment are all resolved.',[
([0,1,2],'After all family actions, if Debt and applicants remain, move the rightmost applicant into Court and lower Debt by one. Repeat while both remain.'),
([3,4],'With no Debt, slide remaining applicants as far right as possible, preserving order.'),
([5],'Place a member on an empty Stock Exchange space and pay bank:')]),
('Q005','Hiring order, consent, promotion fatigue and vacancy fallbacks are all covered.',[
([0],'Fill vacant offices in ascending number on their card backs.'),
([1,4],'When promoting an officeholder, transfer its fatigue to the new card and insert its old card, vacant, into ascending hiring order.'),
([2,3],"Own-family hiring needs verbal consent from every other player in that office's candidate pool, EXCEPT that a Chairman election never requires Nepotism consent."),
([5,6,7],'If no candidate exists, or the hirer is vacant, skip the office; it stays vacant and takes no actions, including hiring.')]),
('Q006','The election passage supplies eligibility, majority, winner, deadlock and share restriction facts.',[
([0,1,2],'**Chairman election:** Former Chairman first announces **the number of shares needed for a pure majority** (more than half of current shares). Any shareholder may campaign; first candidate supported by players controlling that many shares wins.'),
([3,4],"Move one winner's Company shares into Chairman slot and give title marker."),
([5,6],'If no candidate gets support, former Chairman picks any shareholder including self; no Nepotism consent.'),
([7,8],'It still counts as a share for dividends, majority and scoring, but cannot be traded or invested in firms.')]),
('Q007','The general success-check passage resolves resources, cash, lowest-die results, retry limits, catastrophe destinations and dead actions.',[
([0,1],"First commit resources/cash: **all cash for a Company-office check comes from that acting office's treasury and is paid to the bank**."),
([2],'Gather dice, subtract penalties, then roll.'),
([3,4,5,6,7,8,9,10],'Use lowest die: 1–2 success; 3–4 failure, retry if resources and office-specific limits allow; 5–6 catastrophic failure, no more office actions, return officeholder to supply, discard fatigue and flip card into Vacant Offices.'),
([11],'You cannot take a dead action with no effect or chance of success:')]),
('Q008','All voluntary borrowing and allocation duties are explicit.',[
([0,1],'May add up to three Debt freely, each +£5 Balance.'),
([2,3,4],'Each additional advance requires consent of players controlling majority Company shares (Chairman counts); never pass Debt track end.'),
([5,6],"Then **allocate all Balance** to other offices' treasuries, lowering Balance by each transfer.")]),
('Q009','Shipping spending, acquisition prices, consent, destinations and Company-ship prerequisite are complete.',[
([0],'Must spend treasury until **£2 or less remains**.'),
([1,2,3,4,7],'Lease extra ship £2; fit ship from shipyard £3 without owner consent; buy Company ship £5 **only if no ships remain on shipyards**.'),
([5,6],'Place each acquired ship in any sea zone, including China once office exists.')]),
('Q010','The Trade passage covers every requested region, penalty, route, capacity, writer, home-protection, bonus and limit fact.',[
([0,1,2],"Declare regions for Trade: include home region, and only regions reachable through open orders with available ship capacity. Each £1 President's treasury buys one die; subtract one per declared nonhome region."),
([3],'Fill as many orders as possible within declared regions.'),
([4],"Successful Trade capacity is one order per ship in this Presidency's sea zone."),
([5,6],"First writer goes to home port. Every later order must extend the connected route filled during this same Presidency's Trade. **Writers from another Presidency cannot extend this route**, even when adjacent."),
([7],'Writers do not limit capacity: use all available writers, then continue filling with filled-order tokens for the remaining ships.'),
([8],"No President may fill another President's home region, even if its office vacant."),
([9,10],'President earns bank £1 per order; writer owners earn £1 per writer placed.'),
([11],'one successful Trade per President per turn')]),
('Q011','All Deploy targets, resource/empire penalties and officer-loss timing and destinations are covered.',[
([0,1,2,3,4,5],"Target own Presidency's home, any associated region, or any region bordering an associated region. Cannot target another home region or another Presidency's Company-controlled region. Company region must have unrest or a closed order to give action an effect."),
([6,7],'Exhaust chosen officers/regiments to bottom for one die each and local alliances for printed dice.'),
([8,9],'Subtract the combined strength of target and **all other regions in its empire, counting target only once**. Company-controlled defense strength is zero.'),
([10,11,12],'After **each attempt**, owners roll one die per officer exhausted in attempt; each 6 returns an officer to supply. Regiments never roll officer losses.'),
([10],'Exhausted officers still check losses.')]),
('Q012','Successful Deploy loot, trophy and control effects and catastrophic losses are fully supplied, including contextual Presidency association.',[
([0,1,2],'£4 per target tower + faceup loot modifier, with a minimum of (surviving officers used in this attempt + 1)'),
([3],'The Commander also receives one trophy per target tower.'),
([4,5],'Remove target tower and dome. If target was an empire capital, remove **every matching empire flag throughout India**.'),
([6,7],'Open **all** target orders and remove **all** its unrest.'),
([8,11],"Loot/control token, on a new conquest | Turn it region-symbol side up and put it **ABOVE THE ASSOCIATED PRESIDENT'S BOX**."),
([9],'Governor overlay, on a new conquest | Put it **IN THE CONQUERED REGION ON THE MAP**.'),
([10],'Governor office card, on a new conquest | Put **only the CARD** in **Vacant Offices**, awaiting later Hiring.'),
([11],'Steps 3a–3c form a new Governorship only if the target was not already Company-controlled.'),
([12,13,14],"On catastrophe, Commander returns half own family's trophies rounded up and Commander member to supply. Exhausted officers still check losses.")]),
('Q013','The Administer passage covers shrinking dice, all success options and construction stages, bonus/unrest rules and stopping; its normal-rule catastrophe reference supplies vacancy.',[
([0,1,2],'Take the printed dice pool. Each attempt rolls the current pool without penalty, then reduces the pool by one **regardless of result**.'),
([3,7,8],'Success | Take £1, or **£2 if the immediately preceding roll was unsuccessful**; then choose exactly one option below.'),
([4,14,15],"Build Company ship | Each successful Build performs **one stage**: if no partial ship is in the Governor's region, **this single success places the partial ship there**. If a partial ship is already there, **this single success completes it into the sea zone associated with the Governor's President**. Thus the two stages require two successes in total. Partial ship has no other effect."),
([5],"Commission regiment | Place it in **the Army associated with the Governor's President**."),
([6,9],"Tax | Add an **unsplit £2** to Company Balance or the Governor's President's treasury. Each Tax after the first this turn adds regional unrest."),
([10,13],'Any unsuccessful roll | Add one unrest in the region. Catastrophe also removes the officeholder under the normal rule.'),
([11,12,13],'Repeat using the shrinking pool until choosing to stop, no dice remaining, or catastrophe.')]),
('Q014','Emergency loans and Standing consequences are complete; the explicit immediate-scoring stop qualifies the numbered expectations/dividend sequence.',[
([0,1,2,3],'If insufficient, take £5 emergency loans. Each loan advances Debt one **only while a track space remains**. **At maximum Debt, keep taking loans without advancing Debt any further.**'),
([4,5],'Newly added emergency Debt causes no extra current-turn expense. After using emergency loans, set Balance to zero.'),
([6,7],'One or two loans lower Standing one; three or more lower Standing two.'),
([8,9],'2. **Expectations:** Compare remaining Balance to the expectations under **current** Standing; if lower, lower Standing one.'),
([10],'3. **Dividends:** Chairman may pay any affordable number.'),
([11],'If total cash paid as dividends is **strictly greater** than expectations, advance Standing one space.'),
([8,10,12],'Standing reaching leftmost space means Company failure. During Revenue, go immediately to Final Scoring.')]),
('Q015','All target/order/strength, defense fallback and successful-defense facts are present, with the accepted defense comparison explicitly attributed to the user.',[
([0,1,2,3],'**Attacks on Company:** An Invasion or Rebellion against a Company region also triggers secondary Rebellions in every other Company region with unrest. Resolve attacks in this order: **primary Crisis first**, then secondary regions in **Bombay → Madras → Bengal** Army order. **Within each Presidency, that Commander chooses the order of its associated regions.**'),
([4,5,6],'- **Primary normal Crisis:** normal Invasion/Rebellion attack strength **plus unrest in its target region**.\n- **Primary Foreign Invasion:** the ordinary attack die, with no added unrest (designer ruling in FAQ).'),
([5],"**Invasion Crisis:** Sovereign attacker's whole empire strength + event modifier must be **greater than** defender's whole empire strength."),
([6],"**Rebellion Crisis:** Compare only rebelling region strength + modifier against its sovereign capital's strength; other empire regions do not count."),
([7],'**Every secondary Rebellion:** **only the number of unrest cubes in that secondary region**; no event modifier or empire strength.'),
([8],'Associated Commander occupied | That Commander chooses and exhausts pieces; normal trophy gains/losses apply.'),
([8,9],'The acting player exhausts active Army pieces to reach at least the Crisis strength, or as many as possible if unable to reach it.'),
([10],"Commander vacant | **Military Affairs itself acts in the Commander's stead**, choosing pieces; gains/loses **no trophies**."),
([11],'Commander AND Military Affairs vacant | **Chairman chooses pieces** and gains/loses **no trophies**.'),
([12,13,14,15,16],'**EQUAL TO OR GREATER THAN** Crisis strength | **The attack FAILS; defense SUCCEEDS.** Remove all unrest in the attacked region. The **actual Commander gains one trophy**; **Military Affairs/Chairman substitutes gain OR lose NO trophies**. If this defeated a normal primary Invasion, also remove one attacker tower if possible.')]),
('Q016','Both threshold branches, PM/policy consequences, effect ordering and card restoration are explicit.',[
([0,1,2,6,7,8],"-1 or less fails: discard law, resolve dilemma's If Failed text, Opposition Leader returns token and takes PM dial; new PM moves proposed policy one space either direction and resolves that adjacent policy."),
([3,4,5,9],'Zero or higher passes: place law with passed laws, PM takes passed-law token, resolve selected policy **then** immediate law effects.'),
([10],'**Finally restore every card used for voting to its regular orientation**, after either outcome.')]),
('Q017','The special Deregulation introduction explicitly supplies all triggers, outcomes and ordinary-vote exceptions; its special branches qualify the included general voting rules.',[
([0,1,2,3],'In 1758/Long 1710, at turn start before London Season, PM **may** call special Deregulation vote if Standing and/or Debt on lined space, and **must** if either on starred space.'),
([4,5,6,7],'Pass | Lower Debt one per two current Debt; set Standing to S; PM takes passed-law token; activate firms.'),
([8,10,11],'Fail | Increase Company-share scoring value by flipping/placing Court VP token, **up to a MAXIMUM of ±3 VP per share**. **PM stays in power and Deregulation law is NOT discarded.**'),
([9,12],'**No policy accompanies this vote, and PM may vote against it.**')]),
('Q018','All firm formation/investment steps, bank funding, share/workshop restrictions and cap behavior are explicit.',[
([0,1,2,3,4,5],'**Form a firm — only if you currently manage none:** return one eligible Company share to supply or flip workshop to invested side. **Flip your family board to its firm-charter side**, then place a family member as first firm share, set value cube to leftmost track space and take £5 from bank into the London treasury.'),
([6,7,8,9],"**Invest:** With manager's consent, same Company-share/workshop contribution creates one firm share and £5 bank to London."),
([10],'Cannot use Company shares at all when Standing and/or Debt on lined space.'),
([11],'Cannot use shares created this turn, even after trading them away.'),
([12],'Cannot use Chairman share.'),
([13,14],'Invested workshops never return to uninvested: no bonus or Company-failure VP; they remain invested even if firm fails.'),
([15,16],'Up to ten firm shares; further investments still contribute £5 but create no shares.')]),
('Q019','Strategy secrecy, check timing, President-success filling gate, initiative, fallback, capacity, refill revenue and Value growth are all covered.',[
([0],'After the Firm Investments step ends, managers choose firm strategies.'),
([0],'Managers select their strategy simultaneously and secretly:'),
([0],'Trade zone/home port | Commit a secret cash bid from London treasury.'),
([1,2],'Only a firm with at least one ship may select a trade strategy; it may select a closed home port.'),
([3,4],'**Reveal cash bids simultaneously, but keep strategy cards facedown until their matching Presidency begins.**'),
([5,6,7],"At beginning of associated Presidency's operations, before any actions, matching firms reveal strategy and roll one die per committed £1, paying bid to bank."),
([6],'Each firm gets exactly one trade attempt per turn.'),
([8,10,11],"President's successful Trade creates initiative the same way using Presidency ships. After that success, fill orders lowest initiative first."),
([9],'Firm initiative = ship count minus number of successful dice (1s/2s); can be negative.'),
([12],'**The President chooses the order among tied traders; the Company does not automatically go first.**'),
([8,13,14],'If President is vacant or never successfully trades, firms fill **after Commander/Governors had chance to act**, Chairman choosing initiative ties.'),
([15,16],'**Fill only OPEN orders**, as many as possible up to **ships + 1**, starting strategy home port, always tracing through its own filled route back there.'),
([17],'**Each firm may fill any particular order only ONCE per turn; it cannot refill its OWN earlier order.**'),
([18],'A firm may refill an order filled by a DIFFERENT firm or the Company this turn; Company may refill firms\' orders. A previously filled order pays **half listed revenue, rounded down**, not repeated full value.'),
([19],'Place filled tokens; revenue goes to India treasury.'),
([20],'Advance firm Value one space per full £6 added to India treasury this turn.')]),
('Q020','Expense and dividend funding/formulas and every requested dissolution destination and workshop consequence are supplied.',[
([0,1,2],'Pay £1 per charter ship **plus higher of share count or firm value**; can use either/both treasuries.'),
([3,4,5],'After expenses, manager may pay dividends **from India treasury only**. Each dividend pays £1 per firm share plus £1 manager.'),
([6,7,8,10,11],"If unable to pay, dissolve unless rescued. Dissolution: shares to Debtor's Prison (each -1 VP), ships back to shipyards, charter back to family side; workshops remain invested."),
([9],'ships return to their matching shipyards')])
]
grades=[]
for entry,(qid,reason,groups) in zip(p['entries'],selections):
 assert entry['id']==qid
 atoms=entry['requested_fact_scope_entry']['material_requested_facts']
 parts=[{'requirement':atom,'status':'covered','reader_quotes':[]} for atom in atoms]
 reader=entry['reader_a_entry']
 substantive=[reader['answer']]+reader.get('case_conclusions',[])+[x['quote'] for x in reader.get('evidence',[])]+[x['supported_fact_or_case_result'] for x in reader.get('clause_ledger',[]) if 'supported_fact_or_case_result' in x]
 for indexes,quote in groups:
  assert any(quote in s for s in substantive),(qid,quote)
  for i in indexes: parts[i]['reader_quotes'].append(quote)
 assert all(part['reader_quotes'] for part in parts),qid
 grades.append({'id':qid,'grade':'Correct','reason':reason,'material_parts':parts,'unsupported_guesses':[],'summary_issue_if_any':None})
assert len(grades)==20
out=base/'grades-same-entry.json'
encoded=(json.dumps({'block_id':'block-01','readers':{'reader-a':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n').encode()
out.write_bytes(encoded)
print(json.dumps({'path':str(out),'grades':len(grades),'atoms':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(encoded).hexdigest()}))