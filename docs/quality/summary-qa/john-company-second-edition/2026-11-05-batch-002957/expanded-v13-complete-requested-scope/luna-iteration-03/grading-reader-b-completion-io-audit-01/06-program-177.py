from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-03/grading-reader-b/block-06')
p=json.loads((base/'packet.json').read_text())
choices={
'Q098':[
["Count only this attempt's surviving participating officers and used regiments/alliances."],
["Commander family first | £1 for Commander **plus £1 for each of their used surviving officers**."],
["Other families clockwise | £1 per used surviving officer of that family."],
["Pay in this order, stopping when cash runs out"],
["Bank last | £1 per used regiment and per used local-alliance **piece**, regardless of strength."],
["Bank last | £1 per used regiment and per used local-alliance **piece**, regardless of strength."],
["**Repeat that entire cycle from the Commander until all loot is distributed.**"]],
'Q099':[
["If it faced outward from the conquered region, move it **fully inside that region**, now threatening Rebellion."],
["If it faced outward from the conquered region, move it **fully inside that region**, now threatening Rebellion."]],
'Q100':[
["Reduce Balance £1 per existing Debt"],
["Reduce Balance £1 per existing Debt, each officer/regiment in an Army"],
["Reduce Balance £1 per existing Debt, each officer/regiment in an Army"],
["Exclude Commanders."],
["Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China."],
["Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China."]],
'Q101':[
["With that consent, the shareholder may forgo payment for any number of shares on any dividend."],
["**Waiving a dividend requires BOTH the shareholder's choice and the MANAGER'S CONSENT**"],
["Record **total actual cash paid out**, not per-share dividend, with dividend cube on Company Balance track."],
["with dividend cube on Company Balance track."],
["Sweep remaining India money into London."]],
'Q102':[
["Once game over, stop negotiations, calling promises and playing blackmail unless a card explicitly permits final-scoring use."],
["unless a card explicitly permits final-scoring use."]],
'Q103':[
["### Director of Trade (p18)", "£1 treasury cash per die"],
["£1 treasury cash per die"],
["no penalty."],
["After all envoys, may make up to two transfers"],
["each moving one writer or ship"],
["between any Presidencies/sea zones"],
["between any Presidencies/sea zones (including China once created)"]],
'Q104':[
["May make up to two transfers"],
["each officer or regiment from one Army to another"],
["from one Army to another"],
["from one Army to another, remaining in top half."],
["Then assign **every** Officer-in-Training to any Army's top half."],
["Then assign **every** Officer-in-Training to any Army's top half."],
["Then assign **every** Officer-in-Training to any Army's top half."]],
'Q105':[
["Separate adjacent writers from different Presidencies with dividers for correct return at Refresh."],
["Separate adjacent writers from different Presidencies with dividers for correct return at Refresh."],
["Separate adjacent writers from different Presidencies with dividers for correct return at Refresh."]],
'Q106':[
["An Invasion Crisis closes all its orders, or Cascades if already closed; Rebellion/Foreign Invasion already close them."],
["An Invasion Crisis closes all its orders, or Cascades if already closed"],
["An Invasion Crisis closes all its orders, or Cascades if already closed; Rebellion/Foreign Invasion already close them.", "Region Loss does not close them a second time: its additional closure is only for a normal Invasion Crisis."]],
'Q107':[
["take investments actions without set order until nobody wishes more."],
["take investments actions without set order until nobody wishes more."],
["until nobody wishes more."],
["Then choose strategies."]],
'Q108':[
["Transfer all secondary shares, ships and treasury funds to primary"],
["Transfer all secondary shares, ships and treasury funds to primary"]],
'Q109':[
["Company Fraud is played at start of Revenue"],
["roll one die per your officeholder"],
["reduce Balance by twice the highest roll (minimum zero)"]],
'Q110':[
["**May Deploy repeatedly while able, including after a success: there is no one-success-per-turn cap.**"],
["Exhaust chosen officers/regiments to bottom for one die each and local alliances for printed dice.", "a noncatastrophic failure can retry using remaining resources.", "Its strength is usable once that turn and cannot be split among more than one purpose."],
["Cannot target another home region or another Presidency's Company-controlled region.", "Company region must have unrest or a closed order to give action an effect.", "You cannot take a dead action with no effect or chance of success"],
["5–6 catastrophic failure, no more office actions", "On catastrophe, Commander returns half own family's trophies rounded up and Commander member to supply."]],
'Q111':[
["A blackmail effect is one-time"],
["after use, keep the card faceup in your player area"],
["after use, keep the card faceup in your player area"],
["Any printed Power still counts at Final Scoring whether the card is faceup or facedown."]],
'Q112':[
["Chairman may pay any affordable number."],
["Chairman may pay any affordable number."],
["Compare remaining Balance to the expectations under **current** Standing", "Chairman may pay any affordable number."],
["Then Company:", "Compare remaining Balance to the expectations under **current** Standing", "Chairman may pay any affordable number. Each dividend costs one cash per Company share"],
["Each dividend costs one cash per Company share"],
["pay each owner £1 per share, including Chairman."],
["Each dividend costs one cash per Company share; pay each owner £1 per share, including Chairman."],
["**Company shareholders cannot waive payment.**"],
["If total cash paid as dividends is **strictly greater** than expectations, advance Standing one space."]],
'Q113':[
["The marker begins off the board, so it does not match the first chosen action; that action is taken once."],
["The marker begins off the board, so it does not match the first chosen action; that action is taken once."]],
'Q114':[
["Then Company:", "**Expenses:** Reduce Balance £1 per existing Debt"],
["Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China."]],
'Q115':[["On failure, attacker loses one tower."]],
'Q116':[
["After expenses, manager may pay dividends **from India treasury only**. Each dividend pays £1 per firm share plus £1 manager."],
["Yes. The manager may choose to pay none; an active non-Hobnob firm then records zero."]]
}
reasons={
'Q098':'Covers surviving participants, Commander-first clockwise payout cycles, bank shares per regiment/alliance piece, cash exhaustion and repetition.',
'Q099':'The conditional inward move and intended Rebellion against the newly controlling Company are clear.',
'Q100':'Covers every £1 expense category, the Commander exclusion and China ship inclusion.',
'Q101':'Covers waiver scope and manager consent, actual-total dividend cube and track, and the India-to-London sweep.',
'Q102':'States the endgame blackmail prohibition and explicit card-text exception.',
'Q103':'Director heading supplies the office context for treasury cash; all dice economics and transfer details are covered.',
'Q104':'Covers the two transfers, eligible units and Armies, active placement, and mandatory assignment of every trainee.',
'Q105':'Separating the adjacent differently affiliated writers with dividers clearly places the divider between them on their connection and preserves correct Refresh affiliation.',
'Q106':'Covers ordinary Invasion closure/Cascade and excludes a duplicate Region Loss closure for Rebellion or Foreign Invasion.',
'Q107':'Covers unrestricted action order, continuation until nobody wishes more, and subsequent strategy selection.',
'Q108':'Explicitly consolidates secondary ships and shares into the primary firm.',
'Q109':'Covers corrected timing, own-officeholder dice and twice-highest raw amount.',
'Q110':'Repeated success is explicit; exhaustion and remaining resources govern further attempts, target/dead-action rules still apply, and catastrophe ends operations.',
'Q111':'Covers one use, retained faceup card in the player area and continued printed Power.',
'Q112':'Covers discretion, multiple affordable dividends, full share cost/payout including Chairman, no waiver and strictly-greater Standing threshold. In the Company Revenue sequence, the remaining Balance is the clear contextual source and affordability limit for dividends.',
'Q113':'Explicitly resolves initial marker absence and the first-action single use.',
'Q114':'The Company expense instruction explicitly reduces Balance by the full calculated per-item charge.',
'Q115':'Explicitly removes one tower from the attacker on a failed ordinary Invasion.',
'Q116':'Manager discretion and India-only funding are clear; the case conclusion expressly permits zero dividends.'
}
grades=[]
for e in p['entries']:
 q=e['id']; req=e['requested_fact_scope_entry']['material_requested_facts']; qs=choices[q]
 assert len(req)==len(qs), q
 reader=e['reader_b_entry']
 strings=[reader['answer']]+[x for x in reader.get('case_conclusions',[]) if isinstance(x,str)]+[x['quote'] for x in reader.get('evidence',[])]
 for group in qs:
  for quote in group:
   assert quote and any(quote in s for s in strings),(q,quote)
 grades.append({'id':q,'grade':'Correct','reason':reasons[q],'material_parts':[{'requirement':atom,'status':'covered','reader_quotes':quotes} for atom,quotes in zip(req,qs)],'unsupported_guesses':[],'summary_issue_if_any':None})
assert len(grades)==19 and len({g['id'] for g in grades})==19
out=base/'grades-same-entry.json'
out.write_text(json.dumps({'block_id':'block-06','readers':{'reader-b':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(out),'grades':len(grades),'atoms':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))