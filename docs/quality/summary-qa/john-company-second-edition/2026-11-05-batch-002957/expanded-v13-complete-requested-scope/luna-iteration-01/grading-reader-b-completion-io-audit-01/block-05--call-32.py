from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-01/grading-reader-b/block-05')
p=json.loads((base/'packet.json').read_text())
# Each quote below is a manually selected supporting passage, aligned to the fixed atoms.
quotes={
'Q079':[
'Set Balance to £5','family VP markers to zero','Put local alliances in their named Army boxes.','loot tokens money-side up in matching regions.','loot tokens money-side up in matching regions.',
'Choose a scenario and follow its setup card for Standing, Debt, treasuries, laws, regiments, ships and the political map of India.',
'Copy the exact India towers, flags, closed orders and Elephant from the scenario card\'s reverse;',
'Put the Turn marker on its date','point the PM dial\'s arm to the matching date.'],
'Q080':[
'London Season → Family → Firms (if deregulated) → Hiring → Company Operation → Bonuses → Revenue → Events in India → Parliament Meets → Upkeep and Refresh.',
'Family → Firms (if deregulated) → Hiring',"Skip London Season on the game's first turn."],
'Q081':[
'Starting with the Chairman (former Chairman if vacant), clockwise, each player may retire each pensioner to a prize.',
'Starting with the Chairman (former Chairman if vacant)', 'clockwise, each player may retire each pensioner to a prize.',
'each player may retire each pensioner to a prize.', 'each player may retire each pensioner to a prize.',
'Pay its printed cost, move the member to the prize and gain printed VP.',
'move the member to the prize','gain printed VP.',
'Set actual spending aside until London Season ends to establish display-selection order, then pay bank.',
'Set actual spending aside until London Season ends to establish display-selection order, then pay bank.'],
'Q082':[
'No. The capital loses its starred flag when the empire loses its last dominated region, whether that region was lost through Rebellion or Company conquest.',
"remove the surviving capital's starred flag",'This applies regardless of cause, including Rebellion or Company conquest of that last dominated region.',
'This applies regardless of cause, including Rebellion or Company conquest of that last dominated region.',
'This applies regardless of cause, including Rebellion or Company conquest of that last dominated region.'],
'Q083':['Firm-track VP per share: Value 1 = −1 VP','2 = 0','3–4 = ½','5–7 = 1','8–9 = 1½','10 = 2.'],
'Q084':['Starting with the Chairman title holder, clockwise, each player resolves their family action:',
'Starting with the Chairman title holder, clockwise, each player resolves their family action:', 'After all family actions'],
'Q085':[
'Chairman → Director of Trade (or Governor General) → Manager of Shipping → Military Affairs → Bombay Presidency → Madras Presidency → Bengal Presidency → China Superintendent, if created',
'Director of Trade (or Governor General)','Skip each vacant office.'],
'Q086':[
'First roll the storm die:', 'Resolve all required storms **before drawing any event**.',
'Player-owned ships in Company fleets | Check ships in the affected sea zone(s).',
'three storms affects **ALL sea zones**','no storm indication means **NO storm checks**',
'Company and extra ships | **Exempt**; never roll storm checks.', 'Company and extra ships | **Exempt**; never roll storm checks.',
'Ships assigned to China | Count as **Eastern** sea zone.',
'Firm ships | Count in the sea zone on their **firm strategy**, even though on a charter.',
'Hobnob firm ships | **Exempt** from storms.',
'one tile at a time from the draw stack, for as many events as the number printed on that die face',
'Then flip and resolve **one tile at a time from the draw stack, for as many events as the number printed on that die face**.'],
'Q087':[
'Its **tail is the attacker/acting region; its head is the defender**.',
'Its **tail is the attacker/acting region; its head is the defender**.',
'A sovereign actor (large capital flag or unflagged dome) causes **Invasion**.',
'A dominated actor (small flag or no dome) causes **Rebellion against its sovereign**.',
'If Elephant is wholly inside a Company region, resolve Rebellion against the Company.',
'A sovereign actor (large capital flag or unflagged dome)', 'A dominated actor (small flag or no dome)'],
'Q088':[
"Yes; exhaust the whole strength-2 alliance to defend the strength-1 Crisis. This is the summary's user-approved interpretation.",
'For example, an active strength-2 local alliance can successfully defend a strength-1 Crisis by exhausting the whole alliance piece.',
'clear the attacked region’s unrest','the actual Commander gains one trophy',
'Military Affairs/Chairman substitutes gain or lose none',
'if this defeats a normal primary Invasion, remove one attacker tower if possible.',
'The exhausted alliance cannot be used again that turn.',
'It is an interpretation supplied by the user, not an official ruling.',
'It is an interpretation supplied by the user, not an official ruling.',
'The table applies the general comparison: total newly exhausted defense strength equal to or greater than attack strength defeats the Crisis, including excess strength; alliance strength cannot be split.'],
'Q089':[
'Crisis | Resolve at Elephant\'s location, tail attacking head, then March. Use procedures below.',
'After resolving Crisis. Successful Invasion moves to successful capital; otherwise top-stack region.',
'No; unsuccessful Invasion moves to top-stack; Rebellion either result also follows otherwise/top-stack March.'],
'Q090':['Success makes actor sovereign, removes its flag and closes all its orders (Cascade if already closed).',
'Success makes actor sovereign, removes its flag and closes all its orders (Cascade if already closed).',
'Success makes actor sovereign, removes its flag and closes all its orders (Cascade if already closed).',
'Success makes actor sovereign, removes its flag and closes all its orders (Cascade if already closed).'],
'Q091':['Before vote, set Vote marker to law\'s printed starting support; PM moves dial to policy matching law icon before voting.',
'Read law and set Vote marker to its printed starting support.'],
'Q092':['At start Revenue before Company, firms act in initiative order then other firms; ties by manager\'s most windows then PM clockwise order.']*6,
'Q093':['Governor General hires Presidents and uses former Director\'s treasury and turn position;',
'paying £1 treasury per die, no penalty.', 'paying £1 treasury per die, no penalty.',
"On success, **the Governor General's FAMILY takes £1 FROM THE BANK per Company region** (a personal bonus)",
"On success, **the Governor General's FAMILY takes £1 FROM THE BANK per Company region** (a personal bonus)",
"On success, **the Governor General's FAMILY takes £1 FROM THE BANK per Company region** (a personal bonus)"],
'Q094':['Acting player may peek at display blackmails.', 'The owner may allow others to peek privately at their facedown blackmail.'],
'Q095':['May interleave borrowing and allocation while respecting total borrowing rules.',
'May add up to three Debt freely',
'Each additional advance requires consent of players controlling majority Company shares (Chairman counts); never pass Debt track end.',
'Company shares (Chairman counts)', 'never pass Debt track end.'],
'Q096':['Purchase Luxury | Pay bank £4','Purchase Shipyard | Pay bank £2','Purchase Workshop | Pay bank £5',
'Pay these acquisition fees from Shipping’s treasury to the bank; the shipyard owner does not receive the fitting fee.',
'Pay these acquisition fees from Shipping’s treasury to the bank; the shipyard owner does not receive the fitting fee.',
'Pay these acquisition fees from Shipping’s treasury to the bank; the shipyard owner does not receive the fitting fee.'],
'Q097':["Each £1 President's treasury buys one die", "Each £1 President's treasury buys one die", 
"Increase Balance by each order's printed value", "Increase Balance by each order's printed value",
'or half rounded down if a firm already filled it this turn under Deregulation',
"Increase Balance by each order's printed value, **or half rounded down if a firm already filled it this turn under Deregulation**.",
'Company gets half printed value rounded down; President still earns bank £1/order and writer owners £1/writer.']
}
reasons={
'Q079':'All shared setup quantities, locations, orientation and scenario map/date instructions are present.',
'Q080':'The complete phase sequence, conditional Firms insertion and first-turn London skip are present.',
'Q081':'The passage gives the Chairman fallback, clockwise optional retirement, prize/VP movement and cash timing; the player paying the prize cost clearly denotes family spending.',
'Q082':'The answer removes the surviving capital flag for either named cause; removing that flag supplies its normal supply disposition.',
'Q083':'All requested firm Value-to-VP rates are explicitly listed.',
'Q084':'Chairman title priority, clockwise order and the completion gate before new shares are explicit.',
'Q085':'The full office sequence includes Governor General in the Director slot and skips vacancies.',
'Q086':'All storm eligibility branches, exemptions and zone identities plus sequential die-counted events are explicitly present.',
'Q087':'The Elephant roles, Crisis branches and both visual region classifications are explicit.',
'Q088':'The complete entry covers whole-alliance exhaustion, all successful-defense consequences, no reuse and the general comparison with user attribution.',
'Q089':'The unconditional Crisis-then-March procedure and ledger resolve all ordinary success and failure cases.',
'Q090':'Sovereignty, rebel flag removal and closure with the already-closed Cascade condition are stated; flag removal supplies the normal supply disposition.',
'Q091':'The marker uses the selected law’s printed starting support before the vote.',
'Q092':'Revenue timing, initiative then other firms and both tiebreakers are explicit.',
'Q093':'The office treasury is identified in context, with the paid-die rate, no penalty and correct bank-paid family bonus.',
'Q094':'Both display inspection by the selecting player and holder permission for held blackmail are stated.',
'Q095':'Interleaving retains all three consent/counting/track restrictions.',
'Q096':'All three Family purchases and all three Shipping acquisition fees go to the bank.',
'Q097':'Rate, President treasury, full and repeat-filled Balance revenue and unchanged personal bonuses are covered.'
}
grades=[]
for e in p['entries']:
 i=e['id']; facts=e['requested_fact_scope_entry']['material_requested_facts']; qs=quotes[i]
 assert len(facts)==len(qs),(i,len(facts),len(qs))
 r=e['reader_b_entry']
 texts=[r['answer']]+[x['supported_fact_or_case_result'] for x in r['clause_ledger']]+r['case_conclusions']+[x['quote'] for x in r['evidence']]
 for q in qs: assert any(q in t for t in texts),(i,q)
 grades.append({'id':i,'grade':'Correct','reason':reasons[i],'material_parts':[{'requirement':f,'status':'covered','reader_quotes':[q]} for f,q in zip(facts,qs)],'unsupported_guesses':[],'summary_issue_if_any':None})
output=base/'grades-same-entry.json'
output.write_text(json.dumps({'block_id':'block-05','readers':{'reader-b':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(output),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}))