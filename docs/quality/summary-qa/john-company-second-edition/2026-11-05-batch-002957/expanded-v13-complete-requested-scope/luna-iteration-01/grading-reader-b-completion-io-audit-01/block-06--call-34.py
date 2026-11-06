from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-01/grading-reader-b/block-06')
packet=json.loads((base/'packet.json').read_text())
chosen=[
('Q098','Correct','The same entry supplies surviving-participant eligibility, the full Commander/clockwise/bank payout cycle, piece-based alliance shares, exhaustion of cash and repetition.',[
["Count only this attempt's surviving participating officers and used regiments/alliances."],
['Commander first gets £1 for self plus £1 per own used surviving officer; other families clockwise £1 per used surviving officer.'],
['Commander first gets £1 for self plus £1 per own used surviving officer; other families clockwise £1 per used surviving officer.'],
['Repeat whole cycle until loot distributed, stopping when cash runs out; no remaining pool after distribution.'],
['Bank last gets £1 per used regiment and per used alliance piece regardless of alliance strength.'],
['Bank last gets £1 per used regiment and per used alliance piece regardless of alliance strength.'],
['Repeat whole cycle until loot distributed, stopping when cash runs out; no remaining pool after distribution.']]),
('Q099','Correct','Moving the outward-facing Elephant fully inside the newly conquered Company region and threatening Rebellion resolves both requested facts in context.',[
['If the Elephant faced outward from the conquered region, move it fully inside; it then threatens Rebellion.'],
['If the Elephant faced outward from the conquered region, move it fully inside; it then threatens Rebellion.']]),
('Q100','Correct','The entry gives every expense category at £1, the Army qualification, Commander exclusion and China inclusion.',[
['Expenses reduce Balance £1 per Debt, each officer/regiment in an Army and each ship in sea zones including China; exclude Commanders.'],
['Expenses reduce Balance £1 per Debt, each officer/regiment in an Army and each ship in sea zones including China; exclude Commanders.'],
['Expenses reduce Balance £1 per Debt, each officer/regiment in an Army and each ship in sea zones including China; exclude Commanders.'],
['Expenses reduce Balance £1 per Debt, each officer/regiment in an Army and each ship in sea zones including China; exclude Commanders.'],
['Expenses reduce Balance £1 per Debt, each officer/regiment in an Army and each ship in sea zones including China; exclude Commanders.'],
['Expenses reduce Balance £1 per Debt, each officer/regiment in an Army and each ship in sea zones including China; exclude Commanders.']]),
('Q101','Correct','The quoted applicable passage covers waiver scope and manager consent, actual-total marker and its track, and the complete India-to-London remainder sweep.',[
['With that consent, the shareholder may forgo payment for any number of shares on any dividend.'],
["**Waiving a dividend requires BOTH the shareholder's choice and the MANAGER'S CONSENT**"],
['Record **total actual cash paid out**, not per-share dividend, with dividend cube on Company Balance track.'],
['Record **total actual cash paid out**, not per-share dividend, with dividend cube on Company Balance track.'],
['Sweep remaining India money into London.']]),
('Q102','Correct','The answer states the endgame blackmail ban and explicit card-text exception.',[
['No. After game over, players stop playing blackmail unless a card explicitly permits final-scoring use.'],
['No. After game over, players stop playing blackmail unless a card explicitly permits final-scoring use.']]),
('Q103','Correct','The entry resolves Director treasury/rate/no penalty and the later two single-piece transfers between the eligible Presidencies/sea zones, including China.',[
['Director pays £1 treasury per die; no penalty.'],
['Director pays £1 treasury per die; no penalty.'],
['Director pays £1 treasury per die; no penalty.'],
['Up to two transfers, each one writer or ship between any Presidencies/sea zones, including China once created.'],
['Up to two transfers, each one writer or ship between any Presidencies/sea zones, including China once created.'],
['Up to two transfers, each one writer or ship between any Presidencies/sea zones, including China once created.'],
['Up to two transfers, each one writer or ship between any Presidencies/sea zones, including China once created.']]),
('Q104','Correct','The same entry covers two optional single-officer/regiment Army transfers and compulsory assignment of every trainee, with both destinations in the top half.',[
['Up to two transfers, each officer or regiment from one Army to another, remaining in top half.'],
['Up to two transfers, each officer or regiment from one Army to another, remaining in top half.'],
['Up to two transfers, each officer or regiment from one Army to another, remaining in top half.'],
['Up to two transfers, each officer or regiment from one Army to another, remaining in top half.'],
["Then assign **every** Officer-in-Training to any Army's top half."],
["Then assign **every** Officer-in-Training to any Army's top half."],
["Then assign **every** Officer-in-Training to any Army's top half."]]),
('Q105','Correct','Separating adjacent writers of different Presidencies with the divider clearly places it between their connected orders; the entry expressly preserves affiliation and correct Refresh return.',[
['Separate adjacent writers from different Presidencies with dividers to preserve affiliation for return to correct Writers box at Refresh.'],
['Separate adjacent writers from different Presidencies with dividers to preserve affiliation for return to correct Writers box at Refresh.'],
['Separate adjacent writers from different Presidencies with dividers to preserve affiliation for return to correct Writers box at Refresh.']]),
('Q106','Correct','The entry states ordinary Invasion closure and the all-closed Cascade condition, and expressly rejects a second Region Loss closure for Rebellion/Foreign Invasion.',[
['Normal Invasion Crisis closes all orders; Cascade if already closed.'],
['Normal Invasion Crisis closes all orders; Cascade if already closed.'],
['No. Region Loss additional closure is only for normal Invasion Crisis; Rebellion/Foreign Invasion already close them.']]),
('Q107','Correct','Unordered investment actions until nobody wants more, followed by strategies, resolves all timing and endpoint atoms.',[
['No fixed order; take investment actions without order until nobody wants more, then choose strategies.'],
['No fixed order; take investment actions without order until nobody wants more, then choose strategies.'],
['No fixed order; take investment actions without order until nobody wants more, then choose strategies.'],
['No fixed order; take investment actions without order until nobody wants more, then choose strategies.']]),
('Q108','Correct','Both secondary ships and shares explicitly transfer into the primary firm; the stated excess-share exception is consistent with the summary.',[
['The secondary firm’s ships transfer to the primary.'],
['All secondary shares transfer to the primary; if the primary would exceed ten shares, excess shares return to their owners’ supplies with those owners’ consent.']]),
('Q109','Correct','The applicable corrected-card text supplies start-of-Revenue timing, one die per own officeholder, and twice the highest roll before the cap.',[
['Company Fraud is played at start of Revenue: roll one die per your officeholder, reduce Balance by twice the highest roll (minimum zero)'],
['Company Fraud is played at start of Revenue: roll one die per your officeholder, reduce Balance by twice the highest roll (minimum zero)'],
['Company Fraud is played at start of Revenue: roll one die per your officeholder, reduce Balance by twice the highest roll (minimum zero)']]),
('Q110','Correct','Repeated successful Deploys are allowed while able; the same entry retains target/dead-action limits, exhaustion and remaining-resource constraints, and catastrophe termination.',[
['Yes. Deploy may repeat while able, including after success; there is no one-success-per-turn cap.'],
['Further attempts require remaining resources; noncatastrophic failures can retry with remaining resources. Catastrophe ends that office’s actions and removes its holder.','Exhaust chosen officers/regiments to bottom for one die each and local alliances for printed dice.'],
['Yes. Continue to use the listed legal target restrictions, including Company-region effect requirements; do not take a dead action with no effect or success chance.'],
['Further attempts require remaining resources; noncatastrophic failures can retry with remaining resources. Catastrophe ends that office’s actions and removes its holder.']]),
('Q111','Correct','The entry supplies one use, retained faceup card in the owner area, and retained printed Power regardless of orientation.',[
['A blackmail effect is one-time: after use, keep the card faceup in your player area; it cannot be used again or traded.'],
['A blackmail effect is one-time: after use, keep the card faceup in your player area; it cannot be used again or traded.'],
['A blackmail effect is one-time: after use, keep the card faceup in your player area; it cannot be used again or traded.'],
['Any printed Power still counts at Final Scoring whether the card is faceup or facedown.']]),
('Q112','Correct','All requested Company-dividend rules are resolved across ledger and applicable text, including Balance funding, Chairman inclusion, no individual waiver and strict Expectations threshold.',[
['Chairman chooses any affordable number from Company Balance.'],
['Chairman chooses any affordable number from Company Balance.'],
['Chairman chooses any affordable number from Company Balance.'],
['Chairman chooses any affordable number from Company Balance.'],
['Costs £1 per Company share and pays each owner £1 per share, including Chairman.'],
['Costs £1 per Company share and pays each owner £1 per share, including Chairman.'],
['Costs £1 per Company share and pays each owner £1 per share, including Chairman.'],
['No, Company shareholders cannot waive payment.'],
['If total cash paid as dividends is **strictly greater** than expectations, advance Standing one space.']]),
('Q113','Correct','Initial off-board placement and the explicit first-action no-double conclusion cover both atoms.',[
['It begins off the board.'],
['No; the first chosen main Family action cannot be doubled under the marker rule.']]),
('Q114','Correct','Reducing Company Balance by £1 for each listed liability clearly records the ordinary expense total as a Balance reduction.',[
['Expenses reduce Company Balance by £1 for each listed liability; if insufficient take emergency loans, then set Balance to zero.'],
['Expenses reduce Company Balance by £1 for each listed liability; if insufficient take emergency loans, then set Balance to zero.']]),
('Q115','Correct','The direct answer correctly identifies the attacking region as losing one tower after failed non-Company Invasion.',[
['On a failed non-Company Invasion, the attacker loses one tower.']]),
('Q116','Correct','The entry gives manager discretion over dividend number, India-only funding, and an explicit zero-dividend option.',[
['Manager chooses whether and how many after expenses.','After expenses, manager may pay dividends **from India treasury only**.'],
['Yes; may pay none, with marker recording zero for active non-Hobnob firm.']])
]
grades=[]
assert len(chosen)==len(packet['entries'])==19
for entry,(qid,grade,reason,quote_lists) in zip(packet['entries'],chosen):
 assert entry['id']==qid
 atoms=entry['requested_fact_scope_entry']['material_requested_facts']
 assert len(atoms)==len(quote_lists),(qid,len(atoms),len(quote_lists))
 reader=entry['reader_b_entry']
 sources=[reader['answer']]+[v['supported_fact_or_case_result'] for v in reader.get('clause_ledger',[])]+reader.get('case_conclusions',[])+[v['quote'] for v in reader.get('evidence',[])]
 for qs in quote_lists:
  assert qs
  for q in qs:
   assert any(q in s for s in sources),(qid,q)
 grades.append({'id':qid,'grade':grade,'reason':reason,'material_parts':[{'requirement':a,'status':'covered','reader_quotes':qs} for a,qs in zip(atoms,quote_lists)],'unsupported_guesses':[],'summary_issue_if_any':None})
result={'block_id':'block-06','readers':{'reader-b':{'grades':grades}}}
out=base/'grades-same-entry.json'
out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(out),'grade_count':len(grades),'atom_count':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))