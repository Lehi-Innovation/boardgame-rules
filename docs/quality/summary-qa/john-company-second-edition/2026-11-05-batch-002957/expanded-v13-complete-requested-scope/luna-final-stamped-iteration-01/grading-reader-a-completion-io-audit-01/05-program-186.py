from pathlib import Path
import json, hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-final-stamped-iteration-01/grading-reader-a/block-05')
packet=json.loads((base/'packet.json').read_text())
chosen=[
('Q079','The setup passage supplies every shared initial value, location and scenario-card/map/date instruction.',[
('Balance five','Set Balance to £5'),
('Each family VP zero','family VP markers to zero'),
('Alliances in listed Army boxes','Put local alliances in their named Army boxes.'),
('Loot tokens in matching regions','loot tokens money-side up in matching regions.'),
('Loot cash side faceup','loot tokens money-side up in matching regions.'),
('Follow scenario card front instructions','Choose a scenario and follow its setup card for Standing, Debt, treasuries, laws, regiments, ships and the political map of India.'),
('Follow Situation in India diagram',"Copy the exact India towers, flags, closed orders and Elephant from the scenario card's reverse"),
('Turn marker on scenario date','Put the Turn marker on its date'),
('PM arm points at matching date',"point the PM dial's arm to the matching date.")]),
('Q080','The complete phase sequence, conditional Firms insertion and first-turn London Season omission are explicit.',[
('London Season → Family → Hiring → Company Operation → Bonuses → Revenue → Events in India → Parliament Meets → Upkeep and Refresh','London Season → Family → Firms (if deregulated) → Hiring → Company Operation → Bonuses → Revenue → Events in India → Parliament Meets → Upkeep and Refresh.'),
('Between Family and Hiring','Family → Firms (if deregulated) → Hiring'),
('Entire London Season skipped on first game turn',"Skip London Season on the game's first turn.")]),
('Q081','The retirement paragraph resolves priority, optional participation, prize/VP movement and the family payment held aside until the bank payment at London Season end.',[
('Former Chairman first if office vacant','Starting with the Chairman (former Chairman if vacant), clockwise'),
('Otherwise Chairman first','Starting with the Chairman (former Chairman if vacant), clockwise'),
('Then clockwise','Starting with the Chairman (former Chairman if vacant), clockwise'),
('Retirement optional','each player may retire each pensioner to a prize.'),
('Choose prize','each player may retire each pensioner to a prize.'),
('Pay printed cost from family cash','each player may retire each pensioner to a prize. Pay its printed cost'),
('Move pensioner to chosen prize','move the member to the prize'),
('Increase VP by printed amount','gain printed VP.'),
('Set retirement spending aside for display priority','Set actual spending aside until London Season ends to establish display-selection order, then pay bank.'),
('Pay it to bank at end of London Season','Set actual spending aside until London Season ends to establish display-selection order, then pay bank.')]),
('Q082','The answer and operative passage remove the surviving starred flag whenever the last dominated region is lost, explicitly including both named causes.',[
('No','No. Remove the surviving capital’s starred flag'),
('Return remaining capital flag to supply','Remove the surviving capital’s starred flag'),
('Same cleanup whenever last dominated region lost',"Whenever an empire loses its last dominated region, remove the surviving capital's starred flag"),
('Includes Rebellion','regardless of whether the last dominated region was lost to Rebellion or Company conquest.'),
('Includes Company conquest','regardless of whether the last dominated region was lost to Rebellion or Company conquest.')]),
('Q083','The firm-share VP mapping covers every requested Value from one through ten.',[
('Value 1: −1 per share','Firm-track VP per share: Value 1 = −1 VP'),
('Value 2: zero','2 = 0'),
('Values 3–4: half','3–4 = ½'),
('Values 5–7: one','5–7 = 1'),
('Values 8–9: one and a half','8–9 = 1½'),
('Value 10: two','10 = 2')]),
('Q084','The Chairman title holder, clockwise order and completion of all Family actions before New Company Shares are explicit.',[
('Chairman title holder first','Starting with the Chairman title holder, clockwise'),
('Then clockwise','Starting with the Chairman title holder, clockwise'),
('After all players complete Family actions','**New Company shares:** After all family actions')]),
('Q085','The complete office sequence includes the Governor General replacement slot, conditional China office and vacant-office skip.',[
('Chairman → Director → Shipping → Military Affairs → Bombay → Madras → Bengal → China if created','Chairman → Director of Trade (or Governor General) → Manager of Shipping → Military Affairs → Bombay Presidency → Madras Presidency → Bengal Presidency → China Superintendent, if created'),
('GG replaces Director in that slot','Director of Trade (or Governor General)'),
('Skip vacant office','Skip each vacant office.')]),
('Q086','The phase opening and storm table resolve all exposure cases, then the printed event count and sequential draw-stack resolution.',[
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
('Resolve number printed on storm-die face','for as many events as the number printed on that die face'),
('Flip and resolve one draw-stack tile per event sequentially','Then flip and resolve **one tile at a time from the draw stack, for as many events as the number printed on that die face**.')]),
('Q087','The ordinary-Crisis classifier gives both Elephant roles, both attacker branches, the Company interior case and all visual sovereignty markers.',[
('Elephant tail identifies attacker','tail is the attacker/acting region; its head is the defender'),
('Elephant head identifies defender','tail is the attacker/acting region; its head is the defender'),
('Sovereign attacker means Invasion','A sovereign actor (large capital flag or unflagged dome) causes **Invasion**.'),
('Dominated attacker means Rebellion against sovereign','A dominated actor (small flag or no dome) causes **Rebellion against its sovereign**.'),
('Elephant wholly inside Company region means Rebellion against Company','If Elephant is wholly inside a Company region, resolve Rebellion against the Company.'),
('Large flag or unflagged dome sovereign','A sovereign actor (large capital flag or unflagged dome)'),
('Small flag or no dome dominated','A dominated actor (small flag or no dome)')]),
('Q088','The concrete defense result, whole-alliance exhaustion, all success consequences and non-reuse are correct; the general comparison is expressly attributed to the user.',[
('Yes under user interpretation','Yes. Exhaust the entire active alliance; its strength 2 successfully defends against strength 1, so the attack fails.'),
('Exhaust whole active strength-two alliance','Exhaust the entire active alliance; its strength 2 successfully defends against strength 1'),
('Clear target unrest','clear the attacked region’s unrest'),
('Actual Commander gains trophy','the actual Commander gains 1 trophy'),
('Acting Military Affairs or Chairman gains no trophy for successful defense','Military Affairs/Chairman substitutes gain or lose none'),
('Defeated normal primary Invasion loses one attacker tower if possible','if this is a normal primary Invasion, remove one attacker tower if possible.'),
('No reuse that turn','The alliance cannot be used again that turn.'),
('Attribute to user-approved interpretation','This is a user-supplied interpretation adopted at the user’s request'),
('Do not present as independently verified official ruling','not an official ruling'),
('Newly exhausted total defense strength at least attack applies generally in this summary','the stated greater-than-or-equal comparison is the summary’s general rule for newly exhausted Army pieces in this defense context.')]),
('Q089','The conclusion states universal post-Crisis movement and explicitly includes failed Invasion and both Rebellion outcomes.',[
('March after every ordinary Crisis','The Elephant marches after an ordinary Crisis is resolved.'),
('Both successful and failed Invasion trigger March','The Elephant marches after an ordinary Crisis is resolved. A failed Invasion and either result of a Rebellion do not skip the movement; in each case it moves to the top-stack region. Only a successful Invasion moves it to the successful capital.'),
('Both successful and failed Rebellion trigger March','A failed Invasion and either result of a Rebellion do not skip the movement')]),
('Q090','The answer makes the rebel sovereign, removes its flag and closes its orders, with Cascade properly conditional on pre-existing full closure.',[
('Rebel becomes sovereign','On success, the actor becomes sovereign'),
('Return rebel flag to supply','its flag is removed'),
('Close every open order in rebel region','all its orders are closed.'),
('Perform a Cascade only if every order in the rebelling region was already closed.','If all its orders are already closed, it Cascades')]),
('Q091','The pre-voting passage sets the Vote marker using the selected law’s printed starting support.',[
('Before voting set Votes marker on track to selected law starting support',"**Before voting**, PM moves the dial's arm clockwise or counterclockwise, stopping on the **first** policy space matching the chosen law's bottom icon. That space fixes the target and consequence. Read law and set Vote marker to its printed starting support."),
('Use value printed on selected law','Read law and set Vote marker to its printed starting support.')]),
('Q092','The Revenue passages give firms priority before Company expenses and the full initiative/other-firms order with both tiebreakers.',[
('Start of Revenue','At start Revenue before Company'),
('Before Company expenses','If deregulated, firms pay expenses/dividends first. Then Company:'),
('Initiative order first','firms act in initiative order then other firms'),
('Then all other firms','firms act in initiative order then other firms'),
('Break ties by Managers windows',"ties by manager's most windows then PM clockwise order."),
('Then clockwise from Prime Minister',"ties by manager's most windows then PM clockwise order.")]),
('Q093','The Governor General passage supplies its treasury funding, rate, lack of penalty and the successful personal bank bonus per Company region.',[
('GG own office treasury',"Governor General hires Presidents and uses former Director's treasury"),
('£1 per die','paying £1 treasury per die'),
('No dice penalty','paying £1 treasury per die, no penalty.'),
('£1 per Company-controlled region on success',"On success, **the Governor General's FAMILY takes £1 FROM THE BANK per Company region**"),
('GG family receives bonus',"the Governor General's FAMILY takes £1 FROM THE BANK per Company region"),
('Take bonus from bank',"the Governor General's FAMILY takes £1 FROM THE BANK per Company region")]),
('Q094','The London selector may inspect display blackmail; held facedown blackmail inspection requires its owner’s permission.',[
('The acting player choosing a London Season card may inspect any blackmail card in the display','Acting player may peek at display blackmails.'),
('A holder may permit other players to inspect their facedown blackmail cards','The owner may allow others to peek privately at their facedown blackmail.')]),
('Q095','The answer permits interleaving and correctly retains the free-three, majority-consent, Chairman-share and track-end limits.',[
('The Chairman may increase Debt while allocating Company Balance','The Chairman may interleave borrowing and allocation'),
('Up to three advances need no shareholder consent','up to three Debt advances are free of consent'),
('Each additional advance requires consent of players controlling a majority of Company shares','each additional advance requires consent of players controlling a majority of Company shares'),
('The Chairman counts as a share for that majority','Company shares (Chairman counts)'),
('Debt cannot advance beyond the end of its track','Debt cannot pass the track end.')]),
('Q096','The Family purchase rows and Shipping fee instruction assign all six payments to the bank.',[
('Luxury purchase cash goes to the bank','| Purchase Luxury | Pay bank £4'),
('Shipyard purchase cash goes to the bank','| Purchase Shipyard | Pay bank £2'),
('Workshop purchase cash goes to the bank','| Purchase Workshop | Pay bank £5'),
('Extra-ship lease cash goes to the bank','Lease extra ship £2; fit ship from shipyard £3 without owner consent; buy Company ship £5 **only if no ships remain on shipyards**. **Pay these acquisition fees from Shipping’s treasury to the bank'),
('Shipyard-ship fitting cash goes to the bank','Pay these acquisition fees from Shipping’s treasury to the bank; the shipyard owner does not receive the fitting fee.'),
('Company-ship purchase cash goes to the bank','Lease extra ship £2; fit ship from shipyard £3 without owner consent; buy Company ship £5 **only if no ships remain on shipyards**. **Pay these acquisition fees from Shipping’s treasury to the bank')]),
('Q097','The Trade passage resolves paid dice, ordinary and refilled order revenue into Balance, and retains the stated President/writer bonuses for both revenue cases.',[
('Trade buys one die per £1 spent',"Each £1 President's treasury buys one die"),
('The President’s office treasury funds those dice',"Each £1 President's treasury buys one die"),
('Each ordinarily filled Company order generates its full listed value',"Increase Balance by each order's printed value"),
('Normal Company order revenue goes to Company Balance',"Increase Balance by each order's printed value"),
('The Company may fill orders already filled by firms during that turn',"Increase Balance by each order's printed value, **or half rounded down if a firm already filled it this turn under Deregulation**."),
('Such refilled orders pay half listed value rounded down to Company Balance',"Increase Balance by each order's printed value, **or half rounded down if a firm already filled it this turn under Deregulation**."),
('Normal President and placed-writer personal bonuses are unchanged by refilling',"Increase Balance by each order's printed value, **or half rounded down if a firm already filled it this turn under Deregulation**. President earns bank £1 per order; writer owners earn £1 per writer placed.")])
]
grades=[]
assert [c[0] for c in chosen]==[e['id'] for e in packet['entries']]
for (qid, reason, parts), entry in zip(chosen,packet['entries']):
    assert [p[0] for p in parts]==entry['requested_fact_scope_entry']['material_requested_facts'], qid
    reader=entry['reader_a_entry']
    sources=[reader['answer']]+[x for x in reader.get('case_conclusions',[]) if isinstance(x,str)]+[x['quote'] for x in reader.get('evidence',[])]
    for req, quote in parts:
        assert quote and any(quote in source for source in sources),(qid,req,quote)
    grades.append({'id':qid,'grade':'Correct','reason':reason,'material_parts':[{'requirement':req,'status':'covered','reader_quotes':[quote]} for req,quote in parts],'unsupported_guesses':[],'summary_issue_if_any':None})
result={'block_id':'block-05','readers':{'reader-a':{'grades':grades}}}
out=base/'grades-same-entry.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(out),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))