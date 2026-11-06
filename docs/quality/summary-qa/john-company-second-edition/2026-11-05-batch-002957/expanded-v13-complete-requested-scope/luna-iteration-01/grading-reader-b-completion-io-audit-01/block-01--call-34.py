from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-01/grading-reader-b/block-01')
p=json.loads((base/'packet.json').read_text())
# Each list below is the independently selected supporting quotation for each
# fixed atom, in the packet's original order. Content grades are chosen here.
chosen={
'Q001':[
'Roll one die simultaneously for each held office card',
'add one per fatigue',
'modified 1–2 does nothing',
'3–4 adds fatigue',
'5+ retires the officeholder',
'Add one to the Chairman’s office attrition roll.',
'Move retiree to Pensioners',
'flip the office card into Vacant Offices',
'return its fatigue to supply.'
],
'Q002':[
'Players who completed at least one pensioner retirement **or an eligible firm special retirement during this London Season** must each take or discard one display card',
'If the display becomes empty, immediately skip every remaining eligible player.',
'in descending actual total retirement spending.',
'Ties: most total windows, including new prizes, then clockwise from PM.',
'Ties: most total windows, including new prizes, then clockwise from PM.',
'discarding all remaining cards and refilling exactly three: prestige faceup, blackmail facedown, even if nobody took a card',
'discarding all remaining cards and refilling exactly three: prestige faceup, blackmail facedown, even if nobody took a card',
'prestige faceup, blackmail facedown',
'Return all remaining Pensioners to their supplies.'
],
'Q003':[
'Choose a main family action: take it once',
'Check where your opportunity marker was **at phase start** (it begins off the board).\n2. Choose a main family action: take it once, or **may take it twice if the marker already matched it**.',
'Place/move the opportunity marker onto your chosen main action.',
'After the main action, only the latest passed extra-action law may grant its extra action.',
'This extra action is never doubled by the marker and never moves the marker.',
'This extra action is never doubled by the marker and never moves the marker.',
'With at least four vacant offices, place one additional writer **once this turn**',
'Three writers can be placed in total.'
],
'Q004':[
'After all Family actions, while Debt and applicants remain, move the rightmost applicant into Court and lower Debt by one; repeat while both remain.',
'After all Family actions, while Debt and applicants remain, move the rightmost applicant into Court and lower Debt by one; repeat while both remain.',
'lower Debt by one',
'With no Debt, slide applicants as far right as possible preserving order.',
'preserving order.',
'Seeking a share pays the listed price to the bank'
],
'Q005':[
'Fill vacant offices in ascending number on their card backs.',
'insert the old card as vacant in ascending hiring order.',
'Ordinary own-family hiring requires verbal consent from every other player represented in that office\'s candidate pool',
'Chairman elections and Commander appointments are exempt.',
'Transfer the officeholder\'s fatigue to the new card',
'If no candidate exists, or the hirer is vacant, skip the office',
'it stays vacant',
'takes no actions, including hiring.'
],
'Q006':[
'Any shareholder may campaign',
'the number of shares needed for a pure majority** (more than half of current shares)',
'first candidate supported by players controlling that many shares wins.',
'give title marker.',
'Move one winner\'s Company shares into Chairman slot',
'former Chairman picks any shareholder including self',
'no Nepotism consent.',
'It still counts as a share for dividends, majority and scoring',
'cannot be traded or invested in firms.'
],
'Q007':[
'First commit resources/cash',
'all cash for a Company-office check comes from that acting office\'s treasury and is paid to the bank',
'Gather dice, subtract penalties, then roll.',
'Use lowest die: 1–2 success',
'Use lowest die: 1–2 success; 3–4 failure',
'retry if resources and office-specific limits allow',
'5–6 catastrophic failure',
'no more office actions',
'return officeholder to supply',
'discard fatigue',
'flip card into Vacant Offices.',
'You cannot take a dead action with no effect or chance of success'
],
'Q008':[
'May add up to three Debt freely',
'each +£5 Balance.',
'Each additional advance requires consent of players controlling majority Company shares (Chairman counts)',
'(Chairman counts)',
'never pass Debt track end.',
'allocate all Balance** to other offices\' treasuries',
'lowering Balance by each transfer.'
],
'Q009':[
'Must spend treasury until **£2 or less remains**.',
'Lease extra ship £2',
'fit ship from shipyard £3',
'without owner consent',
'buy Company ship £5',
'Place each acquired ship in any sea zone, including China once office exists.',
'Place each acquired ship in any sea zone, including China once office exists.',
'only if no ships remain on shipyards'
],
'Q010':[
'Declare regions for Trade: include home region',
'only regions reachable through open orders with available ship capacity.',
'subtract one per declared nonhome region.',
'Fill as many orders as possible within declared regions.',
'Successful Trade capacity is one order per ship in this Presidency\'s sea zone.',
'First writer goes to home port.',
'Every later order must extend the connected route filled during this same Presidency\'s Trade. **Writers from another Presidency cannot extend this route**, even when adjacent.',
'Writers do not limit capacity: use all available writers, then continue filling with filled-order tokens for the remaining ships.',
'No President may fill another President\'s home region, even if its office vacant.',
'President earns bank £1 per order',
'writer owners earn £1 per writer placed.',
'one successful Trade per President per turn'
],
'Q011':[
'Target own Presidency\'s home',
'any associated region',
'any region bordering an associated region.',
'Cannot target another home region',
'or another Presidency\'s Company-controlled region.',
'Company region must have unrest or a closed order to give action an effect.',
'Exhaust chosen officers/regiments to bottom for one die each',
'local alliances for printed dice.',
'Subtract the combined strength of target and **all other regions in its empire, counting target only once**.',
'Company-controlled defense strength is zero.',
'After **each attempt**, owners roll one die per officer exhausted in attempt; each 6 returns an officer to supply.',
'owners roll one die per officer exhausted in attempt; each 6 returns an officer to supply.',
'Regiments never roll officer losses.'
],
'Q012':[
'£4 per target tower',
'+ faceup loot modifier',
'with a minimum of (surviving officers used in this attempt + 1)',
'The Commander also receives one trophy per target tower.',
'Remove target tower and dome.',
'If target was an empire capital, remove **every matching empire flag throughout India**.',
'Open **all** target orders',
'remove **all** its unrest.',
'Turn it region-symbol side up and put it **ABOVE THE ASSOCIATED PRESIDENT\'S BOX**.',
'Put it **IN THE CONQUERED REGION ON THE MAP**.',
'Put **only the CARD** in **Vacant Offices**, awaiting later Hiring.',
'After loot and trophies, impose successful control in this order:',
'On catastrophe, Commander returns half own family\'s trophies rounded up',
'Commander member to supply.',
'Exhausted officers still check losses.'
],
'Q013':[
'Take the printed dice pool.',
'Each attempt rolls the current pool without penalty',
'then reduces the pool by one **regardless of result**.',
'choose exactly one option below.',
'Thus the two stages require two successes in total.',
'Place it in **the Army associated with the Governor\'s President**.',
'Add an **unsplit £2** to Company Balance or the Governor\'s President\'s treasury.',
'Success | Take £1',
'or **£2 if the immediately preceding roll was unsuccessful**',
'Each Tax after the first this turn adds regional unrest.',
'Any unsuccessful roll | Add one unrest in the region.',
'Repeat using the shrinking pool until choosing to stop, no dice remaining, or catastrophe.',
'Repeat using the shrinking pool until choosing to stop, no dice remaining, or catastrophe.',
'Catastrophe also removes the officeholder under the normal rule.',
'if no partial ship is in the Governor\'s region, **this single success places the partial ship there**. If a partial ship is already there, **this single success completes it into the sea zone associated with the Governor\'s President**. Thus the two stages require two successes in total. Partial ship has no other effect.',
'If a partial ship is already there, **this single success completes it into the sea zone associated with the Governor\'s President**.'
],
'Q014':[
'If insufficient, take £5 emergency loans.',
'If insufficient, take £5 emergency loans.',
'Each loan advances Debt one **only while a track space remains**.',
'At maximum Debt, keep taking loans without advancing Debt any further.',
'Newly added emergency Debt causes no extra current-turn expense.',
'After using emergency loans, set Balance to zero.',
'One or two loans lower Standing one',
'three or more lower Standing two.',
'Compare remaining Balance to the expectations under **current** Standing; if lower, lower Standing one.',
'if lower, lower Standing one.',
'Chairman may pay any affordable number.',
'If total cash paid as dividends is **strictly greater** than expectations, advance Standing one space.',
'Standing reaching leftmost space means Company failure. During Revenue, go immediately to Final Scoring.'
],
'Q015':[
'primary Crisis first',
'An Invasion or Rebellion against a Company region also triggers secondary Rebellions in every other Company region with unrest.',
'Bombay → Madras → Bengal',
'Within each Presidency, that Commander chooses the order of its associated regions.',
'Attack strengths are distinct:',
'Sovereign attacker\'s whole empire strength + event modifier',
'Compare only rebelling region strength + modifier',
'only the number of unrest cubes in that secondary region',
'That Commander chooses and exhausts pieces',
'The acting player exhausts active Army pieces to reach at least the Crisis strength, or as many as possible if unable to reach it.',
'Military Affairs itself acts in the Commander\'s stead',
'Chairman chooses pieces',
'**EQUAL TO OR GREATER THAN** Crisis strength | **The attack FAILS; defense SUCCEEDS.**',
'Remove all unrest in the attacked region.',
'actual Commander gains one trophy',
'Military Affairs/Chairman substitutes gain OR lose NO trophies',
'If this defeated a normal primary Invasion, also remove one attacker tower if possible.'
],
'Q016':[
'-1 or less fails',
'discard law',
'resolve dilemma\'s If Failed text',
'Zero or higher passes',
'place law with passed laws',
'PM takes passed-law token',
'Opposition Leader returns token',
'Opposition Leader returns token and takes PM dial',
'new PM moves proposed policy one space either direction and resolves that adjacent policy.',
'resolve selected policy **then** immediate law effects.',
'Finally restore every card used for voting to its regular orientation'
],
'Q017':[
'In 1758/Long 1710',
'at turn start before London Season',
'PM **may** call special Deregulation vote if Standing and/or Debt on lined space',
'**must** if either on starred space.',
'Lower Debt one per two current Debt',
'set Standing to S',
'PM takes passed-law token',
'activate firms.',
'Increase Company-share scoring value by flipping/placing Court VP token, **up to a MAXIMUM of ±3 VP per share**.',
'No policy accompanies this vote',
'Deregulation law is NOT discarded.',
'PM stays in power',
'PM may vote against it.'
],
'Q018':[
'Form a firm — only if you currently manage none',
'return one eligible Company share to supply or flip workshop to invested side.',
'Flip your family board to its firm-charter side',
'place a family member as first firm share',
'set value cube to leftmost track space',
'take £5 from bank into the London treasury.',
'With manager\'s consent',
'same Company-share/workshop contribution',
'creates one firm share and £5 bank to London.',
'creates one firm share and £5 bank to London. Up to ten firm shares',
'Cannot use Company shares at all when Standing and/or Debt on lined space.',
'Cannot use shares created this turn, even after trading them away.',
'Cannot use Chairman share.',
'Invested workshops never return to uninvested: no bonus or Company-failure VP',
'Invested workshops never return to uninvested: no bonus or Company-failure VP',
'Up to ten firm shares',
'further investments still contribute £5 but create no shares.'
],
'Q019':[
'After the Firm Investments step ends, managers choose firm strategies.',
'Only a firm with at least one ship may select a trade strategy',
'it may select a closed home port.',
'Reveal cash bids simultaneously',
'keep strategy cards facedown until their matching Presidency begins.',
'At beginning of associated Presidency\'s operations, before any actions, matching firms reveal strategy',
'Each firm gets exactly one trade attempt per turn.',
'paying bid to bank.',
'President\'s successful Trade creates initiative the same way using Presidency ships. After that success, fill orders lowest initiative first.',
'Firm initiative = ship count minus number of successful dice (1s/2s)',
'President\'s successful Trade creates initiative the same way using Presidency ships.',
'fill orders lowest initiative first.',
'The President chooses the order among tied traders',
'If President is vacant or never successfully trades, firms fill **after Commander/Governors had chance to act**',
'Chairman choosing initiative ties.',
'Fill only OPEN orders**, as many as possible up to **ships + 1**, starting strategy home port, always tracing through its own filled route back there.',
'starting strategy home port',
'Each firm may fill any particular order only ONCE per turn',
'A firm may refill an order filled by a DIFFERENT firm or the Company this turn; Company may refill firms\' orders. A previously filled order pays **half listed revenue, rounded down**, not repeated full value.',
'revenue goes to India treasury.',
'Advance firm Value one space per full £6 added to India treasury this turn.'
],
'Q020':[
'Pay £1 per charter ship',
'plus higher of share count or firm value',
'can use either/both treasuries.',
'from India treasury only',
'Each dividend pays £1 per firm share',
'plus £1 manager.',
'If unable to pay, dissolve unless rescued.',
'Dissolution: shares to Debtor\'s Prison',
'(each -1 VP)',
'ships back to shipyards',
'charter back to family side',
'workshops remain invested.'
]
}
reasons={
'Q001':'All per-office roll modifiers, thresholds and retirement destinations are present.',
'Q002':'Eligibility including special firm retirements, cash order, both tiebreakers, exhausted display, refill orientations and pensioner cleanup are explicit.',
'Q003':'Main-action repetition and marker movement, latest-law limits and the three-writer application are correct.',
'Q004':'Rightmost-first issue timing, Debt condition/reduction, preserved queue movement and bank payment are explicit.',
'Q005':'The complete entry covers vacancy ordering including promotions, the consent pool and election exception, fatigue and vacancy consequences.',
'Q006':'Shareholder eligibility, pure majority, first successful candidate, title/share placement, deadlock and trade restriction are covered.',
'Q007':'The complete check passage gives office resources/payment, penalties, every result, retries, catastrophe destinations and the dead-action restriction; discarding fatigue denotes return to supply.',
'Q008':'Free and consent-dependent borrowing, share majority, Debt cap and allocation/debit duties are all explicit.',
'Q009':'Mandatory spending, all three prices, fitting consent, sea-zone/China eligibility and the shipyard prerequisite are explicit.',
'Q010':'Declarations, penalty, capacity, connected own route, token continuation, home protection, bonuses and success cap are covered.',
'Q011':'All target restrictions, active exhaustion/dice, whole-empire penalty and zero Company defense, and every-attempt owner loss checks including catastrophe are present.',
'Q012':'Loot/trophy formula and minimum, full control procedure and Presidency association through its control-token placement, and catastrophe consequences are covered.',
'Q013':'The shrinking pool, personal bonuses, benefit choices with both ship stages, tax/failure unrest and all stop conditions are covered; catastrophe expressly uses the normal office-removal rule.',
'Q014':'The complete Revenue passage covers compulsory loans through the Debt cap, Standing consequences, ordered expectations/dividends and immediate failure stopping remaining steps.',
'Q015':'The complete entry combines the Invasion/Rebellion formulas with target unrest and covers all attack order, defense actors, accepted strength comparison and successful-defense outcomes.',
'Q016':'Both thresholds and all law, token, PM, policy, effect-order and voting-card cleanup consequences are explicit.',
'Q017':'Scenario/timing, lined/starred triggers, all pass/fail effects and voting exceptions are covered.',
'Q018':'Formation and investment contributions, charter/share/Value setup, bank funding, manager consent, all share/workshop restrictions and cap behavior are explicit.',
'Q019':'The complete strategy passage covers secret London bids and reveals, checks/payment, successful-President fill gate and fallback, initiative, route/capacity, refills, India revenue and Value growth.',
'Q020':'Expense/dividend formulas and funding, rescue-or-dissolve rule and all dissolution destinations and workshop persistence are covered.'
}
grades=[]
for entry in p['entries']:
 qid=entry['id']; atoms=entry['requested_fact_scope_entry']['material_requested_facts']; quotes=chosen[qid]
 assert len(atoms)==len(quotes),(qid,len(atoms),len(quotes))
 r=entry['reader_b_entry']
 candidates=[r['answer']]+[x['supported_fact_or_case_result'] for x in r.get('clause_ledger',[])]+r.get('case_conclusions',[])+[x['quote'] for x in r.get('evidence',[])]
 parts=[]
 for atom,quote in zip(atoms,quotes):
  assert quote and any(quote in candidate for candidate in candidates),(qid,quote)
  parts.append({'requirement':atom,'status':'covered','reader_quotes':[quote]})
 grades.append({'id':qid,'grade':'Correct','reason':reasons[qid],'material_parts':parts,'unsupported_guesses':[],'summary_issue_if_any':None})
assert len(grades)==20
out={'block_id':'block-01','readers':{'reader-b':{'grades':grades}}}
path=base/'grades-same-entry.json'
encoded=json.dumps(out,ensure_ascii=False,indent=2)+'\n'
path.write_text(encoded)
print(json.dumps({'path':str(path),'count':len(grades),'material_parts':sum(len(x['material_parts']) for x in grades),'sha256':hashlib.sha256(encoded.encode()).hexdigest()}))