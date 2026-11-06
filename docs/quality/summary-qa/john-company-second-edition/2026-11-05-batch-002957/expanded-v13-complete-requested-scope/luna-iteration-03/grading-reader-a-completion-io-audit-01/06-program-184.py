from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-03/grading-reader-a/block-06')
p=json.loads((base/'packet.json').read_text())
choices={
'Q098':('Correct','The same-entry Deploy passage gives surviving-participant eligibility, the full ordered payout cycle, bank shares per regiment/alliance piece, stopping and repetition.',[
["Count only this attempt's surviving participating officers and used regiments/alliances."],
['| Commander family first | £1 for Commander **plus £1 for each of their used surviving officers**. |'],
['| Other families clockwise | £1 per used surviving officer of that family. |'],
['Pay in this order, stopping when cash runs out'],
['| Bank last | £1 per used regiment and per used local-alliance **piece**, regardless of strength. |'],
['| Bank last | £1 per used regiment and per used local-alliance **piece**, regardless of strength. |'],
['**Repeat that entire cycle from the Commander until all loot is distributed.**']]),
'Q099':('Correct','The conditional inward movement and resulting Company Rebellion threat are resolved directly in the conquest context.',[
['If the Elephant faced outward from the conquered region, move it fully inside that region; it now threatens Rebellion.'],
['If the Elephant faced outward from the conquered region, move it fully inside that region; it now threatens Rebellion.']]),
'Q100':('Correct','The Revenue expense passage covers every requested category, rate, Army qualification, Commander exemption and China inclusion.',[
['Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China.'],
['Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China.'],
['Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China.'],
['Exclude Commanders.'],
['Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China.'],
['Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China.']]),
'Q101':('Correct','The full dividend-settlement passage specifies waiver scope and manager consent, the actual-total cube and its track, and the remainder sweep.',[
['With that consent, the shareholder may forgo payment for any number of shares on any dividend.'],
["**Waiving a dividend requires BOTH the shareholder's choice and the MANAGER'S CONSENT**"],
['Record **total actual cash paid out**, not per-share dividend, with dividend cube on Company Balance track.'],
['Record **total actual cash paid out**, not per-share dividend, with dividend cube on Company Balance track.'],
['Sweep remaining India money into London.']]),
'Q102':('Correct','The direct conclusion and included endgame passage state the blackmail ban and explicit card-text exception.',[
['No, players generally stop playing blackmail once the game is over; the exception is a card that explicitly permits final-scoring use.'],
['the exception is a card that explicitly permits final-scoring use.']]),
'Q103':('Correct','The Director section identifies the acting treasury, £1-per-die rate, no penalty and the complete subsequent transfer allowance including China.',[
['### Director of Trade (p18)', '£1 treasury cash per die, no penalty.'],
['£1 treasury cash per die, no penalty.'],
['£1 treasury cash per die, no penalty.'],
['After all envoys, may make up to two transfers, each moving one writer or ship between any Presidencies/sea zones (including China once created).'],
['each moving one writer or ship between any Presidencies/sea zones (including China once created).'],
['each moving one writer or ship between any Presidencies/sea zones (including China once created).'],
['each moving one writer or ship between any Presidencies/sea zones (including China once created).']]),
'Q104':('Correct','The Military Affairs passage supplies the two single-piece transfers, Army destinations and active-half placements, followed by mandatory assignment of every trainee.',[
['May make up to two transfers, each officer or regiment from one Army to another, remaining in top half.'],
['each officer or regiment from one Army to another, remaining in top half.'],
['each officer or regiment from one Army to another, remaining in top half.'],
['each officer or regiment from one Army to another, remaining in top half.'],
["Then assign **every** Officer-in-Training to any Army's top half."],
["Then assign **every** Officer-in-Training to any Army's top half."],
["Then assign **every** Officer-in-Training to any Army's top half."]]),
'Q105':('Correct','Separating adjacent writers with a divider clearly places it between them on their connecting route; the same sentence gives the different-Presidency trigger and correct Refresh affiliation purpose.',[
['Separate adjacent writers from different Presidencies with dividers for correct return at Refresh.'],
['Separate adjacent writers from different Presidencies with dividers for correct return at Refresh.'],
['Separate adjacent writers from different Presidencies with dividers for correct return at Refresh.']]),
'Q106':('Correct','The direct conclusion distinguishes ordinary Invasion closure/Cascade from the absence of an additional Rebellion or Foreign Invasion closure.',[
['For an ordinary Invasion Crisis Region Loss, close all the region’s orders, or Cascade if they are already closed.'],
['For an ordinary Invasion Crisis Region Loss, close all the region’s orders, or Cascade if they are already closed.'],
['Region Loss does not impose a second closure/Cascade for Rebellion or Foreign Invasion, which already close the orders.']]),
'Q107':('Correct','The included investment paragraph allows actions without set order until nobody wants more and then moves to strategies; this also establishes anytime participation within the step.',[
['take investments actions without set order until nobody wishes more.'],
['take investments actions without set order until nobody wishes more.'],
['take investments actions without set order until nobody wishes more.'],
['Then choose strategies.']]),
'Q108':('Correct','The direct conclusion transfers both ships and shares from secondary firms to the primary, with a supported excess-share qualification.',[
['In a negotiated merger, all secondary-firm ships and shares transfer to the primary firm.'],
['In a negotiated merger, all secondary-firm ships and shares transfer to the primary firm.']]),
'Q109':('Correct','The included corrected-card text explicitly supplies start-of-Revenue timing, own-officeholder dice and twice-highest raw amount.',[
['Company Fraud is played at start of Revenue: roll one die per your officeholder, reduce Balance by twice the highest roll (minimum zero)'],
['roll one die per your officeholder'],
['reduce Balance by twice the highest roll']]),
'Q110':('Correct','The direct conclusion covers repeated successes, unexhausted resources, legal effectful targeting and catastrophe ending operations; the full operative passages support each.',[
['A Commander may Deploy repeatedly after a success with no one-success-per-turn cap'],
['each attempt must remain a legal, effectful action using available unexhausted resources.'],
['each attempt must remain a legal, effectful action using available unexhausted resources.'],
['Catastrophic failure ends office actions and returns the Commander to supply']]),
'Q111':('Correct','The included blackmail passage states single use, retention faceup in the player area and continued printed Power at Final Scoring.',[
['A blackmail effect is one-time'],
['after use, keep the card faceup in your player area'],
['after use, keep the card faceup in your player area'],
['Any printed Power still counts at Final Scoring whether the card is faceup or facedown.']]),
'Q112':('Correct','The Company Revenue sequence establishes remaining Balance as the available funds; the dividend step states Chairman discretion over any affordable number, per-share costs/payments including Chairman, no waivers and the strict Standing threshold.',[
['Chairman may pay any affordable number.'],
['Chairman may pay any affordable number.'],
['Compare remaining Balance to the expectations under **current** Standing', 'Chairman may pay any affordable number.'],
['Then Company:', 'Compare remaining Balance to the expectations under **current** Standing', 'Chairman may pay any affordable number. Each dividend costs one cash per Company share'],
['Each dividend costs one cash per Company share'],
['pay each owner £1 per share, including Chairman.'],
['Each dividend costs one cash per Company share; pay each owner £1 per share, including Chairman.'],
['**Company shareholders cannot waive payment.**'],
['If total cash paid as dividends is **strictly greater** than expectations, advance Standing one space.']]),
'Q113':('Correct','The direct answer gives the initial off-board state and denies the first-action double under the phase-start matching rule.',[
['At the game’s start the opportunity marker is off the board'],
['No. At the game’s start the opportunity marker is off the board, and an action may be taken twice only if the marker already matched that action at phase start.']]),
'Q114':('Correct','Reducing Balance by £1 for each counted expense both identifies the Company account and records the total debit on its Balance track.',[
['Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China.'],
['Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China.']]),
'Q115':('Correct','The direct conclusion identifies the attacking region as the one that loses the tower after the failed ordinary Invasion.',[
['The attacker—the region at the Elephant’s tail—loses one tower.']]),
'Q116':('Correct','The direct answer grants manager payout discretion from India funds, including none; the included per-dividend procedure supports choosing the number rather than any compulsory payout.',[
['After expenses, the manager chooses whether to pay dividends from the India treasury', 'After expenses, manager may pay dividends **from India treasury only**. Each dividend pays £1 per firm share plus £1 manager.'],
['yes, an active non-Hobnob firm may pay none and records zero.']])
}
grades=[]
for e in p['entries']:
    grade,reason,quote_sets=choices[e['id']]
    atoms=e['requested_fact_scope_entry']['material_requested_facts']
    assert len(atoms)==len(quote_sets)
    reader=e['reader_a_entry']
    strings=[reader['answer']]+reader.get('case_conclusions',[])+[x['quote'] for x in reader.get('evidence',[])]+[x.get('supported_fact_or_case_result','') for x in reader.get('clause_ledger',[])]
    for qs in quote_sets:
        assert qs and all(any(q in s for s in strings if isinstance(s,str)) for q in qs),e['id']
    grades.append({'id':e['id'],'grade':grade,'reason':reason,'material_parts':[{'requirement':atom,'status':'covered','reader_quotes':qs} for atom,qs in zip(atoms,quote_sets)],'unsupported_guesses':[],'summary_issue_if_any':None})
assert len(grades)==19 and len(choices)==19
out=base/'grades-same-entry.json'
out.write_text(json.dumps({'block_id':'block-06','readers':{'reader-a':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(out),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))