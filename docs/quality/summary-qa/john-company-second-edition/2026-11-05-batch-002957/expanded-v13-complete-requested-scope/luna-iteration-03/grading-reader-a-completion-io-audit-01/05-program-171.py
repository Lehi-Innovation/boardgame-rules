from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-03/grading-reader-a/block-05')
packet=json.loads((base/'packet.json').read_text())
chosen={
'Q079':[
('Balance five','Set Balance to £5'),
('Each family VP zero','family VP markers to zero'),
('Alliances in listed Army boxes','Put local alliances in their named Army boxes.'),
('Loot tokens in matching regions','loot tokens money-side up in matching regions.'),
('Loot cash side faceup','loot tokens money-side up in matching regions.'),
('Follow scenario card front instructions','Choose a scenario and follow its setup card for Standing, Debt, treasuries, laws, regiments, ships and the political map of India.'),
('Follow Situation in India diagram',"Copy the exact India towers, flags, closed orders and Elephant from the scenario card's reverse"),
('Turn marker on scenario date','Put the Turn marker on its date'),
('PM arm points at matching date',"point the PM dial's arm to the matching date.")],
'Q080':[
('London Season → Family → Hiring → Company Operation → Bonuses → Revenue → Events in India → Parliament Meets → Upkeep and Refresh','London Season → Family → Firms (if deregulated) → Hiring → Company Operation → Bonuses → Revenue → Events in India → Parliament Meets → Upkeep and Refresh.'),
('Between Family and Hiring','Family → Firms (if deregulated) → Hiring'),
('Entire London Season skipped on first game turn',"Skip London Season on the game's first turn.")],
'Q081':[
('Former Chairman first if office vacant','Starting with the Chairman (former Chairman if vacant), clockwise'),
('Otherwise Chairman first','Starting with the Chairman (former Chairman if vacant), clockwise'),
('Then clockwise','Starting with the Chairman (former Chairman if vacant), clockwise'),
('Retirement optional','each player may retire each pensioner to a prize.'),
('Choose prize','each player may retire each pensioner to a prize.'),
('Pay printed cost from family cash','each player may retire each pensioner to a prize. Pay its printed cost'),
('Move pensioner to chosen prize','move the member to the prize'),
('Increase VP by printed amount','gain printed VP.'),
('Set retirement spending aside for display priority','Set actual spending aside until London Season ends to establish display-selection order, then pay bank.'),
('Pay it to bank at end of London Season','Set actual spending aside until London Season ends to establish display-selection order, then pay bank.')],
'Q082':[
('No','No. When an empire loses its last dominated region, remove the surviving capital’s starred flag'),
('Return remaining capital flag to supply','remove the surviving capital’s starred flag'),
('Same cleanup whenever last dominated region lost',"Whenever an empire loses its last dominated region, remove the surviving capital's starred flag"),
('Includes Rebellion','This applies regardless of cause, including Rebellion or Company conquest of that last dominated region.'),
('Includes Company conquest','This applies regardless of cause, including Rebellion or Company conquest of that last dominated region.')],
'Q083':[
('Value 1: −1 per share','Firm-track VP per share: Value 1 = −1 VP'),
('Value 2: zero','2 = 0'),
('Values 3–4: half','3–4 = ½'),
('Values 5–7: one','5–7 = 1'),
('Values 8–9: one and a half','8–9 = 1½'),
('Value 10: two','10 = 2.')],
'Q084':[
('Chairman title holder first','Starting with the Chairman title holder, clockwise'),
('Then clockwise','Starting with the Chairman title holder, clockwise'),
('After all players complete Family actions','**New Company shares:** After all family actions')],
'Q085':[
('Chairman → Director → Shipping → Military Affairs → Bombay → Madras → Bengal → China if created','Chairman → Director of Trade (or Governor General) → Manager of Shipping → Military Affairs → Bombay Presidency → Madras Presidency → Bengal Presidency → China Superintendent, if created'),
('GG replaces Director in that slot','Director of Trade (or Governor General)'),
('Skip vacant office','Skip each vacant office.')],
'Q086':[
('Roll storm die first','**First roll the storm die:**'),
('Resolve storms before India event tiles','Resolve all required storms **before drawing any event**.'),
('Eligible player-owned ships in indicated zone','| Player-owned ships in Company fleets | Check ships in the affected sea zone(s). |'),
('All zones for three storms','three storms affects **ALL sea zones**'),
('No checks for no storms','no storm indication means **NO storm checks**'),
('Company ships exempt','| Company and extra ships | **Exempt**; never roll storm checks. |'),
('Extra ships exempt','| Company and extra ships | **Exempt**; never roll storm checks. |'),
('China ships count Eastern','| Ships assigned to China | Count as **Eastern** sea zone. |'),
('Firm ships use chosen strategy zone','| Firm ships | Count in the sea zone on their **firm strategy**, even though on a charter. |'),
('Hobnob ships exempt','| Hobnob firm ships | **Exempt** from storms. |'),
('Resolve number printed on storm-die face','one tile at a time from the draw stack, for as many events as the number printed on that die face'),
('Flip and resolve one draw-stack tile per event sequentially','Then flip and resolve **one tile at a time from the draw stack, for as many events as the number printed on that die face**.')],
'Q087':[
('Elephant tail identifies attacker','tail is the attacker/acting region; its head is the defender'),
('Elephant head identifies defender','tail is the attacker/acting region; its head is the defender'),
('Sovereign attacker means Invasion','A sovereign actor (large capital flag or unflagged dome) causes **Invasion**.'),
('Dominated attacker means Rebellion against sovereign','A dominated actor (small flag or no dome) causes **Rebellion against its sovereign**.'),
('Elephant wholly inside Company region means Rebellion against Company','If Elephant is wholly inside a Company region, resolve Rebellion against the Company.'),
('Large flag or unflagged dome sovereign','A sovereign actor (large capital flag or unflagged dome)'),
('Small flag or no dome dominated','A dominated actor (small flag or no dome)')],
'Q088':[
('Yes under user interpretation','Yes. Strength 2 equals or exceeds Crisis strength 1'),
('Exhaust whole active strength-two alliance','an active strength-2 local alliance can successfully defend a strength-1 Crisis by exhausting the whole alliance piece.'),
('Clear target unrest','clear the attacked region’s unrest'),
('Actual Commander gains trophy','the actual Commander gains one trophy'),
('Acting Military Affairs or Chairman gains no trophy for successful defense','Military Affairs/Chairman substitutes gain or lose none'),
('Defeated normal primary Invasion loses one attacker tower if possible','if this defeats a normal primary Invasion, remove one attacker tower if possible.'),
('No reuse that turn','The exhausted alliance cannot be used again that turn.'),
('Attribute to user-approved interpretation','**Attribution:** User-supplied interpretation of Local Alliances (Rules p22) and Mounting Defense (p33).'),
('Do not present as independently verified official ruling','**Attribution:** User-supplied interpretation of Local Alliances (Rules p22) and Mounting Defense (p33).'),
('Newly exhausted total defense strength at least attack applies generally in this summary','Compare the combined strength of the newly exhausted Army pieces with the attacking strength. **If defense strength equals or exceeds attacking strength, the Crisis fails.**')],
'Q089':[
('March after every ordinary Crisis','The Elephant marches after each ordinary Crisis.'),
('Both successful and failed Invasion trigger March','After a failed Invasion or either result of a Rebellion, it moves to the top-stack region; only after a successful Invasion does it move to the successful capital.'),
('Both successful and failed Rebellion trigger March','After a failed Invasion or either result of a Rebellion, it moves to the top-stack region')],
'Q090':[
('Rebel becomes sovereign','On a successful non-Company Rebellion, the region becomes sovereign'),
('Return rebel flag to supply','its flag is removed'),
('Close every open order in rebel region','all its orders close'),
('Perform a Cascade only if every order in the rebelling region was already closed.','if all are already closed, Cascade instead.')],
'Q091':[
('Before voting set Votes marker on track to selected law starting support','Read law and set Vote marker to its printed starting support.'),
('Use value printed on selected law','Read law and set Vote marker to its printed starting support.')],
'Q092':[
('Start of Revenue',"At start Revenue before Company, firms act in initiative order then other firms; ties by manager's most windows then PM clockwise order."),
('Before Company expenses',"At start Revenue before Company, firms act in initiative order then other firms; ties by manager's most windows then PM clockwise order."),
('Initiative order first','firms act in initiative order then other firms'),
('Then all other firms','firms act in initiative order then other firms'),
('Break ties by Managers windows',"ties by manager's most windows then PM clockwise order."),
('Then clockwise from Prime Minister',"ties by manager's most windows then PM clockwise order.")],
'Q093':[
('GG own office treasury',"Governor General hires Presidents and uses former Director's treasury and turn position"),
('£1 per die','paying £1 treasury per die'),
('No dice penalty','paying £1 treasury per die, no penalty.'),
('£1 per Company-controlled region on success',"On success, **the Governor General's FAMILY takes £1 FROM THE BANK per Company region**"),
('GG family receives bonus',"the Governor General's FAMILY takes £1 FROM THE BANK per Company region"),
('Take bonus from bank',"the Governor General's FAMILY takes £1 FROM THE BANK per Company region")],
'Q094':[
('The acting player choosing a London Season card may inspect any blackmail card in the display','Acting player may peek at display blackmails.'),
('A holder may permit other players to inspect their facedown blackmail cards','The owner may allow others to peek privately at their facedown blackmail.')],
'Q095':[
('The Chairman may increase Debt while allocating Company Balance','May interleave borrowing and allocation while respecting total borrowing rules.'),
('Up to three advances need no shareholder consent','May add up to three Debt freely'),
('Each additional advance requires consent of players controlling a majority of Company shares','Each additional advance requires consent of players controlling majority Company shares (Chairman counts)'),
('The Chairman counts as a share for that majority','Each additional advance requires consent of players controlling majority Company shares (Chairman counts)'),
('Debt cannot advance beyond the end of its track','never pass Debt track end.')],
'Q096':[
('Luxury purchase cash goes to the bank','| Purchase Luxury | Pay bank £4'),
('Shipyard purchase cash goes to the bank','| Purchase Shipyard | Pay bank £2'),
('Workshop purchase cash goes to the bank','| Purchase Workshop | Pay bank £5'),
('Extra-ship lease cash goes to the bank','Lease extra ship £2; fit ship from shipyard £3 without owner consent; buy Company ship £5 **only if no ships remain on shipyards**. **Pay these acquisition fees from Shipping’s treasury to the bank; the shipyard owner does not receive the fitting fee.**'),
('Shipyard-ship fitting cash goes to the bank','Lease extra ship £2; fit ship from shipyard £3 without owner consent; buy Company ship £5 **only if no ships remain on shipyards**. **Pay these acquisition fees from Shipping’s treasury to the bank; the shipyard owner does not receive the fitting fee.**'),
('Company-ship purchase cash goes to the bank','Lease extra ship £2; fit ship from shipyard £3 without owner consent; buy Company ship £5 **only if no ships remain on shipyards**. **Pay these acquisition fees from Shipping’s treasury to the bank; the shipyard owner does not receive the fitting fee.**')],
'Q097':[
('Trade buys one die per £1 spent',"Each £1 President's treasury buys one die"),
('The President’s office treasury funds those dice',"Each £1 President's treasury buys one die"),
('Each ordinarily filled Company order generates its full listed value',"Increase Balance by each order's printed value"),
('Normal Company order revenue goes to Company Balance',"Increase Balance by each order's printed value"),
('The Company may fill orders already filled by firms during that turn',"Increase Balance by each order's printed value, **or half rounded down if a firm already filled it this turn under Deregulation**."),
('Such refilled orders pay half listed value rounded down to Company Balance',"Increase Balance by each order's printed value, **or half rounded down if a firm already filled it this turn under Deregulation**."),
('Normal President and placed-writer personal bonuses are unchanged by refilling','President earns bank £1 per order; writer owners earn £1 per writer placed.')]
}
reasons={
'Q079':'All shared setup quantities, locations, loot orientation and scenario/date instructions are covered; the reverse-card map instruction resolves the Situation in India requirement.',
'Q080':'The complete phase sequence, conditional Firms insertion and first-turn London Season skip are explicit.',
'Q081':'All requested retirement order, optionality, piece/VP movement and spending timing are covered; the player paying the prize cost clearly denotes personal retirement cash.',
'Q082':'Capital flag removal is explicit for every last-dominated-region loss, including both named causes; removing the flag is equivalent to returning the unused flag to supply.',
'Q083':'The full Value-to-VP mapping matches all requested firm Value ranges.',
'Q084':'Chairman-title priority, clockwise order and the all-family-actions completion gate are explicit.',
'Q085':'The complete office sequence, Governor General replacement slot and vacancy skip are explicit.',
'Q086':'All requested storm sequencing, eligibility, exemptions, zone identities and sequential die-count event draws are covered.',
'Q087':'The Elephant roles, Crisis classifier and sovereign/dominated component markers are all explicit.',
'Q088':'The fixture, whole-piece exhaustion, all successful-defense results and non-reuse are correct; the general comparison is explicitly attributed to the user, without an official-authority claim.',
'Q089':'The answer explicitly applies March after every ordinary Crisis and resolves both outcomes of both Crisis types.',
'Q090':'The successful rebel becomes sovereign, its flag is removed, and orders close with Cascade conditioned on all already being closed.',
'Q091':'The selected law supplies printed starting support and the Vote marker is set before the subsequent Voting step.',
'Q092':'The beginning-of-Revenue priority before Company, initiative/other-firm ordering and both tiebreakers are explicit.',
'Q093':'The Govern office treasury, paid-die rate, lack of penalty and success bonus amount, family recipient and bank source are covered.',
'Q094':'Both display inspection by the acting selector and inspection of held blackmail by owner permission are covered.',
'Q095':'Interleaving is explicitly permitted subject to the free-three, further-majority, Chairman-share and track-end limits.',
'Q096':'All three Family purchase rows pay the bank, and the Shipping acquisition-fee instruction covers all three requested shipping cases.',
'Q097':'The paid dice and funding, full ordinary revenue to Balance, half-rounded-down refill revenue and unchanged per-order/per-writer bonuses are all covered.'
}
grades=[]
assert list(chosen)==[e['id'] for e in packet['entries']]
for entry in packet['entries']:
 qid=entry['id']; pairs=chosen[qid]
 assert [x[0] for x in pairs]==entry['requested_fact_scope_entry']['material_requested_facts'],qid
 reader=entry['reader_a_entry']
 texts=[reader['answer']]+reader.get('case_conclusions',[])+[e['quote'] for e in reader.get('evidence',[])]
 texts += [e['supported_fact_or_case_result'] for e in reader.get('clause_ledger',[]) if isinstance(e.get('supported_fact_or_case_result'),str)]
 for requirement,quote in pairs:
  assert quote and any(quote in s for s in texts),(qid,requirement)
 grades.append({'id':qid,'grade':'Correct','reason':reasons[qid],'material_parts':[{'requirement':req,'status':'covered','reader_quotes':[quote]} for req,quote in pairs],'unsupported_guesses':[],'summary_issue_if_any':None})
output=base/'grades-same-entry.json'
content=json.dumps({'block_id':'block-05','readers':{'reader-a':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n'
output.write_text(content)
print(json.dumps({'path':str(output),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(content.encode()).hexdigest()}))