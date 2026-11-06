from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-02/grading-reader-b/block-01')
p=json.loads((base/'packet.json').read_text())
# Explicit human semantic decisions, in requested-atom order. Repeated quotes retain context.
quotes={
'Q001':[
'Simultaneously roll one die for each held office card.', 'Add one per fatigue on that card; Chairman also adds one.', 'Modified 1–2: nothing; 3–4: add fatigue; 5+: retire.', 'Modified 1–2: nothing; 3–4: add fatigue; 5+: retire.', 'Modified 1–2: nothing; 3–4: add fatigue; 5+: retire.', 'Chairman also adds one.', 'Move retiree to Pensioners, flip card into Vacant Offices, return its fatigue to supply.', 'Move retiree to Pensioners, flip card into Vacant Offices, return its fatigue to supply.', 'Move retiree to Pensioners, flip card into Vacant Offices, return its fatigue to supply.'],
'Q002':[
'Players who completed at least one pensioner retirement **or an eligible firm special retirement during this London Season** must each take or discard one display card, in descending actual total retirement spending.',
'If the display becomes empty, immediately skip every remaining eligible player.',
'in descending actual total retirement spending.',
'Ties: most total windows, including new prizes, then clockwise from PM.',
'Ties: most total windows, including new prizes, then clockwise from PM.',
'discarding all remaining cards and refilling exactly three: prestige faceup, blackmail facedown, even if nobody took a card',
'discarding all remaining cards and refilling exactly three: prestige faceup, blackmail facedown, even if nobody took a card',
'prestige faceup, blackmail facedown', 'Return all remaining Pensioners to their supplies.'],
'Q003':[
'Choose a main family action: take it once, or **may take it twice if the marker already matched it**.',
'Check where your opportunity marker was **at phase start** (it begins off the board).\n2. Choose a main family action: take it once, or **may take it twice if the marker already matched it**.',
'Place/move the opportunity marker onto your chosen main action.',
'After the main action, only the latest passed extra-action law may grant its extra action. This extra action is never doubled by the marker and never moves the marker.',
'This extra action is never doubled by the marker and never moves the marker.',
'This extra action is never doubled by the marker and never moves the marker.',
'With at least four vacant offices, place one additional writer **once this turn**, so a doubled Writer action can place three total.',
'With four vacant offices and the marker already on Enlist Writer, the doubled action places two writers, and the vacancy bonus adds one: three writers total.'],
'Q004':[
'After all family actions, if Debt and applicants remain, move the rightmost applicant into Court and lower Debt by one.',
'Repeat while both remain.', 'move the rightmost applicant into Court and lower Debt by one.',
'With no Debt, slide remaining applicants as far right as possible, preserving order.',
'preserving order.', 'Place a member on an empty Stock Exchange space and pay bank:'],
'Q005':[
'Fill vacant offices in ascending number on their card backs.',
'When promoting an officeholder, transfer its fatigue to the new card and insert its old card, vacant, into ascending hiring order.',
'Own-family hiring needs verbal consent from every other player in that office\'s candidate pool, EXCEPT that a Chairman election never requires Nepotism consent.',
'a Chairman election never requires Nepotism consent.',
'transfer its fatigue to the new card',
'If no candidate exists, or the hirer is vacant, skip the office; it stays vacant and takes no actions, including hiring.',
'it stays vacant and takes no actions, including hiring.', 'it stays vacant and takes no actions, including hiring.'],
'Q008':[
'May add up to three Debt freely, each +£5 Balance.', 'each +£5 Balance.',
'Each additional advance requires consent of players controlling majority Company shares (Chairman counts); never pass Debt track end.',
'(Chairman counts)', 'never pass Debt track end.',
'Then **allocate all Balance** to other offices\' treasuries, lowering Balance by each transfer.',
'lowering Balance by each transfer.'],
'Q009':[
'Must spend treasury until **£2 or less remains**.', 'Lease extra ship £2;',
'fit ship from shipyard £3 without owner consent;', 'fit ship from shipyard £3 without owner consent;',
'buy Company ship £5 **only if no ships remain on shipyards**.',
'Place each acquired ship in any sea zone, including China once office exists.',
'Place each acquired ship in any sea zone, including China once office exists.',
'only if no ships remain on shipyards'],
'Q010':[
'Declare regions for Trade: include home region, and only regions reachable through open orders with available ship capacity.',
'Declare regions for Trade: include home region, and only regions reachable through open orders with available ship capacity.',
'subtract one per declared nonhome region.', 'Fill as many orders as possible within declared regions.',
'Successful Trade capacity is one order per ship in this Presidency\'s sea zone.',
'First writer goes to home port.',
'Every later order must extend the connected route filled during this same Presidency\'s Trade. **Writers from another Presidency cannot extend this route**, even when adjacent.',
'Writers do not limit capacity: use all available writers, then continue filling with filled-order tokens for the remaining ships.',
'No President may fill another President\'s home region, even if its office vacant.',
'President earns bank £1 per order; writer owners earn £1 per writer placed.',
'writer owners earn £1 per writer placed.', 'one successful Trade per President per turn'],
'Q011':[
'Target own Presidency\'s home, any associated region, or any region bordering an associated region.',
'Target own Presidency\'s home, any associated region, or any region bordering an associated region.',
'Target own Presidency\'s home, any associated region, or any region bordering an associated region.',
'Cannot target another home region or another Presidency\'s Company-controlled region.',
'Cannot target another home region or another Presidency\'s Company-controlled region.',
'Company region must have unrest or a closed order to give action an effect.',
'Exhaust chosen officers/regiments to bottom for one die each and local alliances for printed dice.',
'Exhaust chosen officers/regiments to bottom for one die each and local alliances for printed dice.',
'Subtract the combined strength of target and **all other regions in its empire, counting target only once**.',
'Company-controlled defense strength is zero.',
'After **each attempt**, owners roll one die per officer exhausted in attempt; each 6 returns an officer to supply.',
'After **each attempt**, owners roll one die per officer exhausted in attempt; each 6 returns an officer to supply.',
'Regiments never roll officer losses.'],
'Q012':[
'£4 per target tower + faceup loot modifier, with a minimum of (surviving officers used in this attempt + 1)',
'£4 per target tower + faceup loot modifier, with a minimum of (surviving officers used in this attempt + 1)',
'£4 per target tower + faceup loot modifier, with a minimum of (surviving officers used in this attempt + 1)',
'The Commander also receives one trophy per target tower.', 'Remove target tower and dome.',
'If target was an empire capital, remove **every matching empire flag throughout India**.',
'Open **all** target orders and remove **all** its unrest.', 'Open **all** target orders and remove **all** its unrest.',
'Turn it region-symbol side up and put it **ABOVE THE ASSOCIATED PRESIDENT\'S BOX**.',
'Put it **IN THE CONQUERED REGION ON THE MAP**.',
'Put **only the CARD** in **Vacant Offices**, awaiting later Hiring.',
'After loot and trophies, impose successful control in this order:',
'On catastrophe, Commander returns half own family\'s trophies rounded up and Commander member to supply.',
'On catastrophe, Commander returns half own family\'s trophies rounded up and Commander member to supply.',
'Exhausted officers still check losses.'],
'Q013':[
'Take the printed dice pool.', 'Each attempt rolls the current pool without penalty, then reduces the pool by one **regardless of result**.',
'Each attempt rolls the current pool without penalty, then reduces the pool by one **regardless of result**.',
'Take £1, or **£2 if the immediately preceding roll was unsuccessful**; then choose exactly one option below.',
'Thus the two stages require two successes in total.',
'Place it in **the Army associated with the Governor\'s President**.',
'Add an **unsplit £2** to Company Balance or the Governor\'s President\'s treasury.',
'Take £1, or **£2 if the immediately preceding roll was unsuccessful**;',
'Take £1, or **£2 if the immediately preceding roll was unsuccessful**;',
'Each Tax after the first this turn adds regional unrest.',
'Add one unrest in the region. Catastrophe also removes the officeholder under the normal rule.',
'Repeat using the shrinking pool until choosing to stop, no dice remaining, or catastrophe.',
'Repeat using the shrinking pool until choosing to stop, no dice remaining, or catastrophe.',
'Catastrophe also removes the officeholder under the normal rule.',
'if no partial ship is in the Governor\'s region, **this single success places the partial ship there**. If a partial ship is already there, **this single success completes it into the sea zone associated with the Governor\'s President**. Thus the two stages require two successes in total. Partial ship has no other effect.',
'If a partial ship is already there, **this single success completes it into the sea zone associated with the Governor\'s President**.'],
'Q015':[
'primary Crisis first',
'An Invasion or Rebellion against a Company region also triggers secondary Rebellions in every other Company region with unrest.',
'Bombay → Madras → Bengal',
'Within each Presidency, that Commander chooses the order of its associated regions.',
'Attack strengths are distinct:',
'Sovereign attacker\'s whole empire strength + event modifier must be **greater than** defender\'s whole empire strength.',
'Compare only rebelling region strength + modifier against its sovereign capital\'s strength; other empire regions do not count.',
'**Every secondary Rebellion:** **only the number of unrest cubes in that secondary region**; no event modifier or empire strength.',
'The acting player exhausts active Army pieces to reach at least the Crisis strength, or as many as possible if unable to reach it.',
'The acting player exhausts active Army pieces to reach at least the Crisis strength, or as many as possible if unable to reach it.',
'Commander vacant | **Military Affairs itself acts in the Commander\'s stead**, choosing pieces; gains/loses **no trophies**.',
'Commander AND Military Affairs vacant | **Chairman chooses pieces** and gains/loses **no trophies**.',
'If defense strength equals or exceeds attacking strength, the Crisis fails.',
'Remove all unrest in the attacked region.', 'actual Commander gains one trophy',
'Military Affairs/Chairman substitutes gain OR lose NO trophies',
'If this defeated a normal primary Invasion, also remove one attacker tower if possible.'],
'Q016':[
'-1 or less fails: discard law, resolve dilemma\'s If Failed text, Opposition Leader returns token and takes PM dial;',
'discard law', 'resolve dilemma\'s If Failed text', 'Zero or higher passes:',
'place law with passed laws', 'PM takes passed-law token', 'Opposition Leader returns token and takes PM dial',
'Opposition Leader returns token and takes PM dial',
'new PM moves proposed policy one space either direction and resolves that adjacent policy.',
'resolve selected policy **then** immediate law effects.',
'Finally restore every card used for voting to its regular orientation'],
'Q017':[
'In 1758/Long 1710, at turn start before London Season,',
'at turn start before London Season',
'PM **may** call special Deregulation vote if Standing and/or Debt on lined space, and **must** if either on starred space.',
'PM **may** call special Deregulation vote if Standing and/or Debt on lined space, and **must** if either on starred space.',
'Lower Debt one per two current Debt', 'set Standing to S', 'PM takes passed-law token', 'activate firms.',
'Increase Company-share scoring value by flipping/placing Court VP token, **up to a MAXIMUM of ±3 VP per share**.',
'No policy accompanies this vote, and PM may vote against it.',
'PM stays in power and Deregulation law is NOT discarded.',
'PM stays in power and Deregulation law is NOT discarded.',
'PM may vote against it.'],
'Q018':[
'Form a firm — only if you currently manage none:',
'return one eligible Company share to supply or flip workshop to invested side.',
'Flip your family board to its firm-charter side',
'place a family member as first firm share', 'set value cube to leftmost track space',
'take £5 from bank into the London treasury.',
'With manager\'s consent, same Company-share/workshop contribution creates one firm share and £5 bank to London.',
'With manager\'s consent, same Company-share/workshop contribution creates one firm share and £5 bank to London.',
'With manager\'s consent, same Company-share/workshop contribution creates one firm share and £5 bank to London.',
'Up to ten firm shares; further investments still contribute £5 but create no shares.',
'Cannot use Company shares at all when Standing and/or Debt on lined space.',
'Cannot use shares created this turn, even after trading them away.',
'Cannot use Chairman share.', 'Invested workshops never return to uninvested: no bonus or Company-failure VP;',
'Invested workshops never return to uninvested: no bonus or Company-failure VP;',
'Up to ten firm shares;', 'further investments still contribute £5 but create no shares.'],
'Q019':[
'After the Firm Investments step ends, managers choose firm strategies.',
'Only a firm with at least one ship may select a trade strategy;', 'it may select a closed home port.',
'Reveal cash bids simultaneously, but keep strategy cards facedown until their matching Presidency begins.',
'Reveal cash bids simultaneously, but keep strategy cards facedown until their matching Presidency begins.',
'At beginning of associated Presidency\'s operations, before any actions, matching firms reveal strategy and roll one die per committed £1, paying bid to bank.',
'Each firm gets exactly one trade attempt per turn.',
'paying bid to bank.',
'President\'s successful Trade creates initiative the same way using Presidency ships. After that success, fill orders lowest initiative first.',
'Firm initiative = ship count minus number of successful dice (1s/2s); can be negative.',
'President\'s successful Trade creates initiative the same way using Presidency ships.',
'After that success, fill orders lowest initiative first.',
'The President chooses the order among tied traders;',
'If President is vacant or never successfully trades, firms fill **after Commander/Governors had chance to act**, Chairman choosing initiative ties.',
'Chairman choosing initiative ties.',
'**Fill only OPEN orders**, as many as possible up to **ships + 1**, starting strategy home port, always tracing through its own filled route back there.',
'starting strategy home port',
'Each firm may fill any particular order only ONCE per turn; it cannot refill its OWN earlier order.',
'A firm may refill an order filled by a DIFFERENT firm or the Company this turn; Company may refill firms\' orders. A previously filled order pays **half listed revenue, rounded down**, not repeated full value.',
'revenue goes to India treasury.',
'Advance firm Value one space per full £6 added to India treasury this turn.'],
'Q020':[
'Pay £1 per charter ship **plus higher of share count or firm value**; can use either/both treasuries.',
'Pay £1 per charter ship **plus higher of share count or firm value**; can use either/both treasuries.',
'can use either/both treasuries.', 'from India treasury only',
'Each dividend pays £1 per firm share plus £1 manager.', 'Each dividend pays £1 per firm share plus £1 manager.',
'If unable to pay, dissolve unless rescued.',
'Dissolution: shares to Debtor\'s Prison (each -1 VP), ships back to shipyards, charter back to family side; workshops remain invested.',
'each -1 VP', 'ships back to shipyards', 'charter back to family side', 'workshops remain invested.']}
# Multi-part context quotes supplement atoms whose rule spans separate paragraphs.
extras={('Q012',11): ['Turn it region-symbol side up and put it **ABOVE THE ASSOCIATED PRESIDENT\'S BOX**.'],('Q015',5):['**Primary normal Crisis:** normal Invasion/Rebellion attack strength **plus unrest in its target region**.'],('Q015',6):['**Primary normal Crisis:** normal Invasion/Rebellion attack strength **plus unrest in its target region**.'],('Q015',8):['Associated Commander occupied | That Commander chooses and exhausts pieces; normal trophy gains/losses apply.'],('Q019',0):['Managers select their strategy simultaneously and secretly:', 'Trade zone/home port | Commit a secret cash bid from London treasury.'],('Q019',6):['roll one die per committed £1'],('Q019',8):['If President is vacant or never successfully trades, firms fill **after Commander/Governors had chance to act**, Chairman choosing initiative ties.'],('Q011',10):['Exhausted officers still check losses.'],('Q013',13):['Repeat using the shrinking pool until choosing to stop, no dice remaining, or catastrophe.']}
partial={
'Q006': ('III. Hiring, summary line 138', '**Chairman election:** Former Chairman first announces **the number of shares needed for a pure majority** (more than half of current shares). Any shareholder may campaign; first candidate supported by players controlling that many shares wins. Move one winner\'s Company shares into Chairman slot and give title marker. It still counts as a share for dividends, majority and scoring, but cannot be traded or invested in firms. If no candidate gets support, former Chairman picks any shareholder including self; no Nepotism consent.'),
'Q007': ('IV. Company Operation, summary line 144', '**Success checks (p17):** First commit resources/cash: **all cash for a Company-office check comes from that acting office\'s treasury and is paid to the bank**. Gather dice, subtract penalties, then roll. Use lowest die: 1–2 success; 3–4 failure, retry if resources and office-specific limits allow; 5–6 catastrophic failure, no more office actions, return officeholder to supply, discard fatigue and flip card into Vacant Offices. Specific Commander/firm procedures modify this. You cannot take a dead action with no effect or chance of success: for example trade with no ship or deploy without dice to trigger possible officer losses.'),
'Q014': ('VI. Revenue, summary lines 156–160', '1. **Expenses:** Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China. Exclude Commanders. If insufficient, take £5 emergency loans. Each loan advances Debt one **only while a track space remains**. **At maximum Debt, keep taking loans without advancing Debt any further.** Newly added emergency Debt causes no extra current-turn expense. After using emergency loans, set Balance to zero. One or two loans lower Standing one; three or more lower Standing two.\n2. **Expectations:** Compare remaining Balance to the expectations under **current** Standing; if lower, lower Standing one.\n3. **Dividends:** Chairman may pay any affordable number. Each dividend costs one cash per Company share; pay each owner £1 per share, including Chairman. **Company shareholders cannot waive payment.** If total cash paid as dividends is **strictly greater** than expectations, advance Standing one space.\n\nStanding reaching leftmost space means Company failure. During Revenue, go immediately to Final Scoring.')}
grades=[]
for e in p['entries']:
 id=e['id']; facts=e['requested_fact_scope_entry']['material_requested_facts']; answer=e['reader_b_entry']['answer']
 if id in partial:
  loc,q=partial[id]
  grades.append(dict(id=id,grade='Partial',reason='Reader error: the complete entry supplies an unrelated section and omits all requested facts listed below. The full summary resolves these facts explicitly; no wrong concrete conclusion is asserted. Technical section-selection failure is distinct from the factual omission.',material_parts=[dict(requirement=f,status='omitted',reader_quotes=[]) for f in facts],unsupported_guesses=[],summary_issue_if_any=dict(classification='reader error; summary adequate',location=loc,controlling_summary_quote=q,missing_facts=facts)))
 else:
  assert len(quotes[id])==len(facts),(id,len(quotes[id]),len(facts))
  parts=[]
  for n,(f,q) in enumerate(zip(facts,quotes[id])):
   qs=[q]+extras.get((id,n),[])
   for s in qs: assert s and s in answer,(id,n,s)
   parts.append(dict(requirement=f,status='covered',reader_quotes=qs))
  grades.append(dict(id=id,grade='Correct',reason='Every exact requested fact is resolved by the complete same-entry substantive text, including its applicable summary passages. No material contradiction or unsupported guess.',material_parts=parts,unsupported_guesses=[],summary_issue_if_any=None))
out=base/'grades-same-entry.json'
b=(json.dumps({'block_id':'block-01','readers':{'reader-b':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n').encode()
out.write_bytes(b)
print(json.dumps({'path':str(out),'entries':len(grades),'atoms':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(b).hexdigest()}))