import json,hashlib
from pathlib import Path
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-03/grading-reader-b/block-05')
packet=json.loads((base/'packet.json').read_text())
chosen={
'Q079': [
('Balance five','Set Balance to £5'),
('Each family VP zero','family VP markers to zero'),
('Alliances in listed Army boxes','Put local alliances in their named Army boxes.'),
('Loot tokens in matching regions','loot tokens money-side up in matching regions.'),
('Loot cash side faceup','loot tokens money-side up in matching regions.'),
('Follow scenario card front instructions','Choose a scenario and follow its setup card for Standing, Debt, treasuries, laws, regiments, ships and the political map of India.'),
('Follow Situation in India diagram',"Copy the exact India towers, flags, closed orders and Elephant from the scenario card's reverse"),
('Turn marker on scenario date','Put the Turn marker on its date'),
('PM arm points at matching date',"point the PM dial's arm to the matching date.")],
'Q080': [
('London Season → Family → Hiring → Company Operation → Bonuses → Revenue → Events in India → Parliament Meets → Upkeep and Refresh','London Season → Family → Firms (if deregulated) → Hiring → Company Operation → Bonuses → Revenue → Events in India → Parliament Meets → Upkeep and Refresh.'),
('Between Family and Hiring','Family → Firms (if deregulated) → Hiring'),
('Entire London Season skipped on first game turn',"Skip London Season on the game's first turn.")],
'Q081': [
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
'Q082': [
('No',"remove the surviving capital's starred flag"),
('Return remaining capital flag to supply',"remove the surviving capital's starred flag"),
('Same cleanup whenever last dominated region lost',"Whenever an empire loses its last dominated region, remove the surviving capital's starred flag: it is no longer an empire. This applies regardless of cause, including Rebellion or Company conquest of that last dominated region."),
('Includes Rebellion','including Rebellion or Company conquest of that last dominated region.'),
('Includes Company conquest','including Rebellion or Company conquest of that last dominated region.')],
'Q083': [
('Value 1: −1 per share','Firm-track VP per share: Value 1 = −1 VP'),
('Value 2: zero','2 = 0'),
('Values 3–4: half','3–4 = ½'),
('Values 5–7: one','5–7 = 1'),
('Values 8–9: one and a half','8–9 = 1½'),
('Value 10: two','10 = 2.')],
'Q084': [
('Chairman title holder first','Starting with the Chairman title holder, clockwise'),
('Then clockwise','Starting with the Chairman title holder, clockwise'),
('After all players complete Family actions','**New Company shares:** After all family actions')],
'Q085': [
('Chairman → Director → Shipping → Military Affairs → Bombay → Madras → Bengal → China if created','Chairman → Director of Trade (or Governor General) → Manager of Shipping → Military Affairs → Bombay Presidency → Madras Presidency → Bengal Presidency → China Superintendent, if created'),
('GG replaces Director in that slot','Director of Trade (or Governor General)'),
('Skip vacant office','Skip each vacant office.')],
'Q086': [
('Roll storm die first','First roll the storm die:'),
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
'Q087': [
('Elephant tail identifies attacker','tail is the attacker/acting region; its head is the defender'),
('Elephant head identifies defender','tail is the attacker/acting region; its head is the defender'),
('Sovereign attacker means Invasion','A sovereign actor (large capital flag or unflagged dome) causes **Invasion**.'),
('Dominated attacker means Rebellion against sovereign','A dominated actor (small flag or no dome) causes **Rebellion against its sovereign**.'),
('Elephant wholly inside Company region means Rebellion against Company','If Elephant is wholly inside a Company region, resolve Rebellion against the Company.'),
('Large flag or unflagged dome sovereign','A sovereign actor (large capital flag or unflagged dome)'),
('Small flag or no dome dominated','A dominated actor (small flag or no dome)')],
'Q088': [
('Yes under user interpretation','For example, an active strength-2 local alliance can successfully defend a strength-1 Crisis by exhausting the whole alliance piece.'),
('Exhaust whole active strength-two alliance','For example, an active strength-2 local alliance can successfully defend a strength-1 Crisis by exhausting the whole alliance piece.'),
('Clear target unrest','clear the attacked region’s unrest'),
('Actual Commander gains trophy','the actual Commander gains one trophy'),
('Acting Military Affairs or Chairman gains no trophy for successful defense','Military Affairs/Chairman substitutes gain or lose none'),
('Defeated normal primary Invasion loses one attacker tower if possible','if this defeats a normal primary Invasion, remove one attacker tower if possible.'),
('No reuse that turn','The exhausted alliance cannot be used again that turn.'),
('Attribute to user-approved interpretation','**Attribution:** User-supplied interpretation of Local Alliances (Rules p22) and Mounting Defense (p33).'),
('Do not present as independently verified official ruling','**Attribution:** User-supplied interpretation of Local Alliances (Rules p22) and Mounting Defense (p33).'),
('Newly exhausted total defense strength at least attack applies generally in this summary','Compare the combined strength of the newly exhausted Army pieces with the attacking strength. **If defense strength equals or exceeds attacking strength, the Crisis fails.**')],
'Q089': [
('March after every ordinary Crisis','The Elephant Marches after the ordinary Crisis resolution; failed Invasion and either Rebellion result do not skip it.'),
('Both successful and failed Invasion trigger March','The Elephant Marches after the ordinary Crisis resolution; failed Invasion and either Rebellion result do not skip it. A successful Invasion moves to its successful capital; otherwise it moves to the top-stack region.'),
('Both successful and failed Rebellion trigger March','failed Invasion and either Rebellion result do not skip it.')],
'Q090': [
('Rebel becomes sovereign','Success makes actor sovereign'),
('Return rebel flag to supply','Success makes actor sovereign, removes its flag'),
('Close every open order in rebel region','closes all its orders (Cascade if already closed).'),
('Perform a Cascade only if every order in the rebelling region was already closed.','closes all its orders (Cascade if already closed).')],
'Q091': [
('Before voting set Votes marker on track to selected law starting support','Read law and set Vote marker to its printed starting support.'),
('Use value printed on selected law','Read law and set Vote marker to its printed starting support.')],
'Q092': [
('Start of Revenue','At start Revenue before Company'),
('Before Company expenses','At start Revenue before Company'),
('Initiative order first','firms act in initiative order then other firms'),
('Then all other firms','firms act in initiative order then other firms'),
('Break ties by Managers windows',"ties by manager's most windows then PM clockwise order."),
('Then clockwise from Prime Minister',"ties by manager's most windows then PM clockwise order.")],
'Q093': [
('GG own office treasury',"Governor General hires Presidents and uses former Director's treasury and turn position"),
('£1 per die','paying £1 treasury per die, no penalty.'),
('No dice penalty','paying £1 treasury per die, no penalty.'),
('£1 per Company-controlled region on success',"On success, **the Governor General's FAMILY takes £1 FROM THE BANK per Company region** (a personal bonus)"),
('GG family receives bonus',"the Governor General's FAMILY takes £1 FROM THE BANK per Company region"),
('Take bonus from bank',"the Governor General's FAMILY takes £1 FROM THE BANK per Company region")],
'Q094': [
('The acting player choosing a London Season card may inspect any blackmail card in the display','Acting player may peek at display blackmails.'),
('A holder may permit other players to inspect their facedown blackmail cards','The owner may allow others to peek privately at their facedown blackmail.')],
'Q095': [
('The Chairman may increase Debt while allocating Company Balance','May interleave borrowing and allocation while respecting total borrowing rules.'),
('Up to three advances need no shareholder consent','May add up to three Debt freely'),
('Each additional advance requires consent of players controlling a majority of Company shares','Each additional advance requires consent of players controlling majority Company shares (Chairman counts)'),
('The Chairman counts as a share for that majority','majority Company shares (Chairman counts)'),
('Debt cannot advance beyond the end of its track','never pass Debt track end.')],
'Q096': [
('Luxury purchase cash goes to the bank','| Purchase Luxury | Pay bank £4'),
('Shipyard purchase cash goes to the bank','| Purchase Shipyard | Pay bank £2'),
('Workshop purchase cash goes to the bank','| Purchase Workshop | Pay bank £5'),
('Extra-ship lease cash goes to the bank','Pay these acquisition fees from Shipping’s treasury to the bank; the shipyard owner does not receive the fitting fee.'),
('Shipyard-ship fitting cash goes to the bank','Pay these acquisition fees from Shipping’s treasury to the bank; the shipyard owner does not receive the fitting fee.'),
('Company-ship purchase cash goes to the bank','Pay these acquisition fees from Shipping’s treasury to the bank; the shipyard owner does not receive the fitting fee.')],
'Q097': [
('Trade buys one die per £1 spent',"Each £1 President's treasury buys one die"),
('The President’s office treasury funds those dice',"Each £1 President's treasury buys one die"),
('Each ordinarily filled Company order generates its full listed value',"Increase Balance by each order's printed value"),
('Normal Company order revenue goes to Company Balance',"Increase Balance by each order's printed value"),
('The Company may fill orders already filled by firms during that turn','or half rounded down if a firm already filled it this turn under Deregulation'),
('Such refilled orders pay half listed value rounded down to Company Balance',"Increase Balance by each order's printed value, **or half rounded down if a firm already filled it this turn under Deregulation**."),
('Normal President and placed-writer personal bonuses are unchanged by refilling','President earns bank £1 per order; writer owners earn £1 per writer placed.')]
}
reasons={
'Q079':'All shared positions, loot orientation, scenario instructions/map and date settings appear in the same-entry setup passage.',
'Q080':'The complete phase sequence explicitly inserts Firms between Family and Hiring and skips London Season on the first turn.',
'Q081':'The retirement passage supplies both priority cases, clockwise optional player retirement, prize/cost/VP movements and deferred bank payment. The personal player payment clearly denotes family spending.',
'Q082':'The universal flag-removal instruction covers the surviving capital and expressly includes both named causes; removing that flag is the requested return cleanup.',
'Q083':'The complete firm Value-to-VP mapping is stated exactly.',
'Q084':'Chairman-title priority, clockwise play and the all-family-actions gate are explicit.',
'Q085':'The entire office sequence, Governor General substitution and vacancy skip are explicit.',
'Q086':'The same-entry passage supplies storm-first sequencing, every requested ship eligibility rule and sequential die-counted events.',
'Q087':'The classifier explicitly supplies tail/head roles, all requested Crisis branches and the sovereign/dominated markers.',
'Q088':'The concrete defense succeeds under the attributed general user interpretation; whole-alliance exhaustion, successful-defense consequences and non-reuse are all present. No official-authority claim is made.',
'Q089':'The concrete conclusion and unconditional Crisis-table March instruction cover both results of both ordinary Crisis types.',
'Q090':'The rebellion-success passage covers sovereignty, flag removal and all-order closure with Cascade conditioned on orders already closed.',
'Q091':'The marker initialization immediately preceding Voting uses the selected law’s printed starting support.',
'Q092':'The firm passage explicitly places firms first at Revenue and supplies initiative/other-firm ordering and both tie breakers.',
'Q093':'The Governor General passage identifies the office treasury, one-pound dice with no penalty and the per-region bank-paid family bonus.',
'Q094':'Both display inspection by the acting player and held-card inspection by owner permission are explicit.',
'Q095':'Interleaving is expressly allowed while all three borrowing restrictions and the Chairman share count remain in force.',
'Q096':'All three family purchases name the bank, and Shipping’s acquisition-fee instruction covers its three listed acquisitions.',
'Q097':'The passage supplies President-funded one-pound dice, normal listed-value Balance revenue, the firm-refill rounded-down half exception and unchanged per-order/per-writer bonuses.'
}
grades=[]
assert list(chosen)==[e['id'] for e in packet['entries']]
for e in packet['entries']:
    qid=e['id']
    pairs=chosen[qid]
    assert [x[0] for x in pairs]==e['requested_fact_scope_entry']['material_requested_facts'],qid
    r=e['reader_b_entry']
    strings=[r['answer']]+r.get('case_conclusions',[])+[v['quote'] for v in r.get('evidence',[])]
    for atom,quote in pairs:
        assert quote and any(quote in s for s in strings),(qid,atom)
    grades.append({'id':qid,'grade':'Correct','reason':reasons[qid],'material_parts':[{'requirement':atom,'status':'covered','reader_quotes':[quote]} for atom,quote in pairs],'unsupported_guesses':[],'summary_issue_if_any':None})
result={'block_id':'block-05','readers':{'reader-b':{'grades':grades}}}
out=base/'grades-same-entry.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(out),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))