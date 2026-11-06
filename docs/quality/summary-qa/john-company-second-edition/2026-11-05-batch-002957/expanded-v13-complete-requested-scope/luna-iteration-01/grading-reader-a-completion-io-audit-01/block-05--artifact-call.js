// @exec: {"max_output_tokens":24000}
// QA_ARTIFACT_WRITE_V1
const output = "/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-01/grading-reader-a/block-05/grades-same-entry.json";
const decisions = [
["Q079","Correct","All shared setup values, component locations, scenario instructions, map diagram and matching dates are supplied.",[
["Balance five","covered","Set Balance to £5"],
["Each family VP zero","covered","family VP markers to zero"],
["Alliances in listed Army boxes","covered","Put local alliances in their named Army boxes."],
["Loot tokens in matching regions","covered","loot tokens money-side up in matching regions."],
["Loot cash side faceup","covered","loot tokens money-side up in matching regions."],
["Follow scenario card front instructions","covered","Choose a scenario and follow its setup card for Standing, Debt, treasuries, laws, regiments, ships and the political map of India."],
["Follow Situation in India diagram","covered","Copy the exact India towers, flags, closed orders and Elephant from the scenario card's reverse"],
["Turn marker on scenario date","covered","Put the Turn marker on its date"],
["PM arm points at matching date","covered","point the PM dial's arm to the matching date."]]],
["Q080","Correct","The full phase sequence, conditional Firms insertion and first-turn London Season skip are covered.",[
["London Season → Family → Hiring → Company Operation → Bonuses → Revenue → Events in India → Parliament Meets → Upkeep and Refresh","covered","London Season → Family → Firms (if deregulated) → Hiring → Company Operation → Bonuses → Revenue → Events in India → Parliament Meets → Upkeep and Refresh."],
["Between Family and Hiring","covered","Firms phase follows Family and precedes Hiring when deregulated."],
["Entire London Season skipped on first game turn","covered","Skip London Season on the game's first turn."]]],
["Q081","Correct","The entry supplies the acting order, optional personal retirement, prize and VP movement, and spending reservation/payment timing. Personal payment is clear in the player-retirement context.",[
["Former Chairman first if office vacant","covered","Starting with the Chairman (former Chairman if vacant), clockwise"],
["Otherwise Chairman first","covered","Starting with the Chairman (former Chairman if vacant), clockwise"],
["Then clockwise","covered","Starting with the Chairman (former Chairman if vacant), clockwise"],
["Retirement optional","covered","each player may retire each pensioner to a prize."],
["Choose prize","covered","each player may retire each pensioner to a prize."],
["Pay printed cost from family cash","covered","each player may retire each pensioner to a prize. Pay its printed cost"],
["Move pensioner to chosen prize","covered","move the member to the prize"],
["Increase VP by printed amount","covered","gain printed VP."],
["Set retirement spending aside for display priority","covered","Set actual spending aside until London Season ends to establish display-selection order, then pay bank."],
["Pay it to bank at end of London Season","covered","Set actual spending aside until London Season ends to establish display-selection order, then pay bank."]]],
["Q082","Correct","Capital-flag removal is expressly universal and includes both named causes; removal of the unused flag clearly entails returning it to supply.",[
["No","covered","No. When empire loses last dominated region, remove surviving capital's starred flag; it is no longer an empire."],
["Return remaining capital flag to supply","covered","remove surviving capital's starred flag"],
["Same cleanup whenever last dominated region lost","covered","Whenever an empire loses its last dominated region, remove the surviving capital's starred flag"],
["Includes Rebellion","covered","This applies regardless of cause, including Rebellion or Company conquest of that last dominated region."],
["Includes Company conquest","covered","This applies regardless of cause, including Rebellion or Company conquest of that last dominated region."]]],
["Q083","Correct","Every requested Value-to-VP rate is correctly stated.",[
["Value 1: −1 per share","covered","Value 1: −1 VP; 2: 0; 3–4: ½; 5–7: 1; 8–9: 1½; 10: 2 VP per share."],
["Value 2: zero","covered","Value 1: −1 VP; 2: 0; 3–4: ½; 5–7: 1; 8–9: 1½; 10: 2 VP per share."],
["Values 3–4: half","covered","Value 1: −1 VP; 2: 0; 3–4: ½; 5–7: 1; 8–9: 1½; 10: 2 VP per share."],
["Values 5–7: one","covered","Value 1: −1 VP; 2: 0; 3–4: ½; 5–7: 1; 8–9: 1½; 10: 2 VP per share."],
["Values 8–9: one and a half","covered","Value 1: −1 VP; 2: 0; 3–4: ½; 5–7: 1; 8–9: 1½; 10: 2 VP per share."],
["Value 10: two","covered","Value 1: −1 VP; 2: 0; 3–4: ½; 5–7: 1; 8–9: 1½; 10: 2 VP per share."]]],
["Q084","Correct","First player, clockwise order and the all-actions completion gate are covered.",[
["Chairman title holder first","covered","Chairman title holder acts first, then clockwise."],
["Then clockwise","covered","Chairman title holder acts first, then clockwise."],
["After all players complete Family actions","covered","After all family actions."]]],
["Q085","Correct","The whole office sequence, Governor General slot and vacancy skip are correct.",[
["Chairman → Director → Shipping → Military Affairs → Bombay → Madras → Bengal → China if created","covered","Chairman → Director of Trade → Manager of Shipping → Military Affairs → Bombay → Madras → Bengal → China Superintendent if created."],
["GG replaces Director in that slot","covered","Governor General occupies Director of Trade's position in sequence."],
["Skip vacant office","covered","Skip each vacant office."]]],
["Q086","Correct","All storm timing, eligibility, exemptions, zone identities and sequential die-count event procedures are present.",[
["Roll storm die first","covered","First roll storm die; resolve all required storms before drawing any event."],
["Resolve storms before India event tiles","covered","First roll storm die; resolve all required storms before drawing any event."],
["Eligible player-owned ships in indicated zone","covered","Player-owned ships in Company fleets in affected zones"],
["All zones for three storms","covered","three storms affects **ALL sea zones**"],
["No checks for no storms","covered","no storm indication means **NO storm checks**"],
["Company ships exempt","covered","Company and extra ships exempt"],
["Extra ships exempt","covered","Company and extra ships exempt"],
["China ships count Eastern","covered","China ships count Eastern"],
["Firm ships use chosen strategy zone","covered","firm ships count strategy zone"],
["Hobnob ships exempt","covered","Hobnob firm ships exempt."],
["Resolve number printed on storm-die face","covered","Storm die face specifies event count. Flip and resolve one tile at a time from draw stack for that count."],
["Flip and resolve one draw-stack tile per event sequentially","covered","Flip and resolve one tile at a time from draw stack for that count."]]],
["Q087","Correct","Attacker/defender, all ordinary Crisis branches and both visual component classifications are covered.",[
["Elephant tail identifies attacker","covered","Elephant tail is attacker/acting region; head is defender."],
["Elephant head identifies defender","covered","Elephant tail is attacker/acting region; head is defender."],
["Sovereign attacker means Invasion","covered","Sovereign actor produces Invasion"],
["Dominated attacker means Rebellion against sovereign","covered","dominated actor causes Rebellion against its sovereign"],
["Elephant wholly inside Company region means Rebellion against Company","covered","If Elephant is wholly inside a Company region, resolve Rebellion against the Company."],
["Large flag or unflagged dome sovereign","covered","Sovereign: large capital flag or unflagged dome."],
["Small flag or no dome dominated","covered","Dominated: small flag or no dome."]]],
["Q088","Correct","The whole-alliance example, all requested success effects, no reuse and general user-attributed comparison are explicitly resolved.",[
["Yes under user interpretation","covered","Yes. Exhaust the whole alliance; strength 2 is equal to or greater than Crisis strength 1, so defense succeeds."],
["Exhaust whole active strength-two alliance","covered","An active strength-2 local alliance can defend a strength-1 Crisis by exhausting the whole piece"],
["Clear target unrest","covered","clear attacked region unrest."],
["Actual Commander gains trophy","covered","Actual Commander gains one trophy"],
["Acting Military Affairs or Chairman gains no trophy for successful defense","covered","Military Affairs/Chairman substitute gains/loses none."],
["Defeated normal primary Invasion loses one attacker tower if possible","covered","If it defeats normal primary Invasion, remove one attacker tower if possible."],
["No reuse that turn","covered","exhausted alliance cannot be reused that turn."],
["Attribute to user-approved interpretation","covered","It is a user-supplied interpretation, adopted at user's request, not an official ruling."],
["Do not present as independently verified official ruling","covered","It is a user-supplied interpretation, adopted at user's request, not an official ruling."],
["Newly exhausted total defense strength at least attack applies generally in this summary","covered","The adopted comparison generally makes defense succeed when combined newly exhausted piece strength equals or exceeds attacking strength; it includes local alliance strength."]]],
["Q089","Correct","The unconditional ordinary Crisis March and all named success/failure cases are resolved.",[
["March after every ordinary Crisis","covered","Crisis resolves at Elephant's location and then Marches."],
["Both successful and failed Invasion trigger March","covered","After successful Invasion it moves to successful capital; otherwise top-stack region.","No. A failed Invasion and either Rebellion result use the otherwise/top-stack March; neither skips movement."],
["Both successful and failed Rebellion trigger March","covered","No. A failed Invasion and either Rebellion result use the otherwise/top-stack March; neither skips movement."]]],
["Q090","Correct","Sovereignty, removal of the now-unused rebel flag and conditional closure/Cascade outcomes are covered.",[
["Rebel becomes sovereign","covered","Actor becomes sovereign, removes its flag and closes all its orders."],
["Return rebel flag to supply","covered","Actor becomes sovereign, removes its flag and closes all its orders."],
["Close every open order in rebel region","covered","Actor becomes sovereign, removes its flag and closes all its orders."],
["Perform a Cascade only if every order in the rebelling region was already closed.","covered","Cascade if all its orders are already closed."]]],
["Q091","Correct","The selected law's printed starting support initializes the Vote marker before voting.",[
["Before voting set Votes marker on track to selected law starting support","covered","Set Vote marker on the support track to the law's printed starting support.","Read law and set Vote marker to its printed starting support."],
["Use value printed on selected law","covered","The chosen law's printed starting support value."]]],
["Q092","Correct","Start-of-Revenue placement, priority over Company, initiative/other order and both tiebreakers are covered.",[
["Start of Revenue","covered","Expenses occur at start of Revenue before Company; manager may pay dividends after expenses."],
["Before Company expenses","covered","Expenses occur at start of Revenue before Company; manager may pay dividends after expenses."],
["Initiative order first","covered","Firms act in initiative order, then other firms."],
["Then all other firms","covered","Firms act in initiative order, then other firms."],
["Break ties by Managers windows","covered","Ties by manager with most windows, then PM clockwise order."],
["Then clockwise from Prime Minister","covered","Ties by manager with most windows, then PM clockwise order."]]],
["Q093","Correct","The Governor General's office context identifies its treasury, and the rate, absence of penalty and bank-funded family bonus are explicit.",[
["GG own office treasury","covered","Governor General hires Presidents and uses former Director's treasury and turn position; it is hired like Director and rolls attrition normally.","Then may attempt Govern repeatedly, paying £1 treasury per die, no penalty."],
["£1 per die","covered","Pay £1 from treasury per die"],
["No dice penalty","covered","No penalty."],
["£1 per Company-controlled region on success","covered","On success the Governor General's family takes £1 from bank per Company region; this is personal bonus."],
["GG family receives bonus","covered","On success the Governor General's family takes £1 from bank per Company region; this is personal bonus."],
["Take bonus from bank","covered","On success the Governor General's family takes £1 from bank per Company region; this is personal bonus."]]],
["Q094","Correct","Both display inspection and holder-controlled private inspection permissions are covered.",[
["The acting player choosing a London Season card may inspect any blackmail card in the display","covered","Acting player may peek at display blackmails."],
["A holder may permit other players to inspect their facedown blackmail cards","covered","The owner may allow other players to peek privately at their facedown blackmail."]]],
["Q095","Correct","Interleaving is allowed with the free-three, further majority consent, Chairman-share inclusion and track-end constraints.",[
["The Chairman may increase Debt while allocating Company Balance","covered","Yes. May interleave borrowing and allocation while respecting total borrowing rules"],
["Up to three advances need no shareholder consent","covered","up to three Debt freely"],
["Each additional advance requires consent of players controlling a majority of Company shares","covered","Each additional advance requires consent of players controlling majority Company shares (Chairman counts); never pass Debt track end."],
["The Chairman counts as a share for that majority","covered","Each additional advance requires consent of players controlling majority Company shares (Chairman counts); never pass Debt track end."],
["Debt cannot advance beyond the end of its track","covered","never pass Debt track end."]]],
["Q096","Correct","The bank is correctly identified for all six purchases/acquisitions, including the fitting fee.",[
["Luxury purchase cash goes to the bank","covered","Bank receives purchase price for luxury (£4), shipyard (£2), and workshop (£5)."],
["Shipyard purchase cash goes to the bank","covered","Bank receives purchase price for luxury (£4), shipyard (£2), and workshop (£5)."],
["Workshop purchase cash goes to the bank","covered","Bank receives purchase price for luxury (£4), shipyard (£2), and workshop (£5)."],
["Extra-ship lease cash goes to the bank","covered","Bank receives £2 extra-ship lease, £3 fitting and £5 Company ship purchase from Shipping treasury; shipyard owner does not receive fitting fee."],
["Shipyard-ship fitting cash goes to the bank","covered","Bank receives £2 extra-ship lease, £3 fitting and £5 Company ship purchase from Shipping treasury; shipyard owner does not receive fitting fee."],
["Company-ship purchase cash goes to the bank","covered","Bank receives £2 extra-ship lease, £3 fitting and £5 Company ship purchase from Shipping treasury; shipyard owner does not receive fitting fee."]]],
["Q097","Correct","Paid dice, full and refilled Company revenue/destination and unchanged personal bonuses are correctly supplied; the conditional refill procedure clearly permits refilling firm orders.",[
["Trade buys one die per £1 spent","covered","Each £1 from President's treasury buys one die."],
["The President’s office treasury funds those dice","covered","Each £1 from President's treasury buys one die."],
["Each ordinarily filled Company order generates its full listed value","covered","Increase Company Balance by each order's printed value."],
["Normal Company order revenue goes to Company Balance","covered","Increase Company Balance by each order's printed value."],
["The Company may fill orders already filled by firms during that turn","covered","Company Balance gets half listed order revenue rounded down if a firm already filled that order this turn."],
["Such refilled orders pay half listed value rounded down to Company Balance","covered","Company Balance gets half listed order revenue rounded down if a firm already filled that order this turn."],
["Normal President and placed-writer personal bonuses are unchanged by refilling","covered","President still earns £1 from bank per order; writer owners £1 per writer placed."]]]
];
const result = {block_id:"block-05",readers:{"reader-a":{grades:decisions.map(([id,grade,reason,parts])=>({id,grade,reason,material_parts:parts.map(([requirement,status,...reader_quotes])=>({requirement,status,reader_quotes})),unsupported_guesses:[],summary_issue_if_any:null}))}}};
const payload = JSON.stringify(result,null,2);
const cmd = "python3 - <<'PY'\nfrom pathlib import Path\nimport json,hashlib\npacket=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-01/grading-reader-a/block-05/packet.json')\nout=Path('" + output + "')\ndata=json.loads(" + JSON.stringify(payload) + ")\np=json.loads(packet.read_text())\ngrades=data['readers']['reader-a']['grades']\nassert [g['id'] for g in grades]==[e['id'] for e in p['entries']]\nfor g,e in zip(grades,p['entries']):\n assert [a['requirement'] for a in g['material_parts']]==e['requested_fact_scope_entry']['material_requested_facts'],g['id']\n r=e['reader_a_entry']\n sources=[r['answer']]+[v['supported_fact_or_case_result'] for v in r['clause_ledger']]+r['case_conclusions']+[v['quote'] for v in r['evidence']]\n for a in g['material_parts']:\n  assert a['reader_quotes'],(g['id'],a['requirement'])\n  for q in a['reader_quotes']: assert q and any(q in s for s in sources),(g['id'],q)\ntext=json.dumps(data,ensure_ascii=False,indent=2)+'\\n'\nout.write_text(text)\nprint(json.dumps({'path':str(out),'grade_count':len(grades),'atom_count':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(text.encode()).hexdigest()}))\nPY";
const r = await tools.exec_command({cmd,max_output_tokens:24000});
text(r.output);
