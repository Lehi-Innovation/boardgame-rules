from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-final-stamped-iteration-01/grading-reader-a/block-04')
packet=json.loads((base/'packet.json').read_text())
chosen={
'Q060':[
['Each shareholder may make one additional retirement per London Season'],
['from supply rather than Pensioners'],
['irrespective of number of firms owned'],
['**Actual cash spent after spouse discounts** cannot exceed the **highest total dividend marker** of any firm they own a share in'],
['No retirement from a firm whose marker is absent or zero.'],
['the printed prize cost may exceed that marker when discounts cover the difference','Retirement discounts can stack, are personal'],
['At start of Final Scoring, score firms then allow one special retirement'],
['allow one special retirement regardless of Company success/failure']
],
'Q061':[
['**Investment cash always comes FROM the BANK TO London.'],
['Place filled tokens; revenue goes to India treasury.'],
["Pay **£3 FROM the firm's London treasury TO the BANK**."],
['Commit a secret cash bid from London treasury.'],
['can use either/both treasuries.'],
['After expenses, manager may pay dividends **from India treasury only**.'],
['**Family cash cannot be transferred into or out of firm treasuries.**']
],
'Q062':[
['After Family share creation, before Hiring'],
['After Family share creation, before Hiring'],
['Manager resolves timing conflicts within firm'],
['PM resolves conflicts between firms.']
],
'Q063':[
["**must have that shipyard owner's consent**"],
["Pay **£3 FROM the firm's London treasury TO the BANK**."],
['Firms cannot acquire Company or extra ships.'],
['Firms cannot acquire Company or extra ships.'],
["May buy player-owned ship already in Company with owner's consent"],
['unfatigued £3'],
['fatigued £2'],
["from the firm's London treasury into Shipping treasury"]
],
'Q064':[
['Only a player who **manages NO firm at all** may initiate one; managing a different firm also makes you ineligible.'],
["Obtain consent of holders of a majority of the target's shares"],
["Only a player who **manages NO firm at all** may initiate one; managing a different firm also makes you ineligible. Obtain consent of holders of a majority of the target's shares, then move firm's ships, money and shares to own charter"],
["move firm's ships, money and shares to own charter"],
["move firm's ships, money and shares to own charter"],
["move firm's ships, money and shares to own charter"],
['copy both cube positions'],
['copy both cube positions'],
['former manager returns cubes'],
['flips board to family side.']
],
'Q065':[
["Managers negotiate with **every shareholder's consent**."],
['Highest-value firm is primary'],
['if tied, players choose among tied.'],
["If the primary would exceed ten shares, RETURN the excess shares to their OWNERS' SUPPLIES, with those owners' consent."],
['Transfer all secondary shares, ships and treasury funds to primary'],
['secondary boards return to family sides.']
],
'Q066':[
['No bid, trade or dividends.'],
['No bid, trade or dividends.'],
['No bid, trade or dividends.'],
['Still pay expenses'],
['retain previous dividend marker for retirement.'],
['Firm ships face storms in strategy zone; Hobnob exempts them.']
],
'Q067':[
['Emergency investments follow the Company-share/workshop eligibility rules under **Firms phase: investments**, even when ten-share cap prevents more shares'],
['Up to ten firm shares; further investments still contribute £5 but create no shares.'],
["return one eligible Company share to supply or flip workshop to invested side","Emergency investments follow the Company-share/workshop eligibility rules under **Firms phase: investments**"],
['Cannot use Company shares at all when Standing and/or Debt on lined space.','Emergency investments follow the Company-share/workshop eligibility rules'],
['Cannot use shares created this turn, even after trading them away.','Emergency investments follow the Company-share/workshop eligibility rules'],
['pay expenses, lose any remaining cash, lower Value one space per emergency investment.'],
['lose any remaining cash'],
['lower Value one space per emergency investment.']
],
'Q068':[
['emergency negotiated merger with only ONE other firm'],
['The other firm must first pay its own expenses if not already paid'],
["then cover the endangered firm's unpaid expenses."]
],
'Q069':[
['**Voluntary dissolution:** All shareholders must consent.'],
["shares go to Debtor's Prison"],
['ships return to their matching shipyards'],
['Workshops remain invested for the rest of the game.']
],
'Q070':[
['1. Firms, if deregulated','**BEFORE ordinary Power/Court/final-outcome scoring**'],
['Firm-track VP per share: Value 1 = −1 VP; 2 = 0; 3–4 = ½; 5–7 = 1; 8–9 = 1½; 10 = 2.'],
["Deduct **1 VP per own family piece in Debtor's Prison**."],
["for each player separately add VP from all their shares across all their firms, then **round that player's total DOWN once**."],
['1. Firms, if deregulated','5. Final retirements OR failure card','Resolve the appropriate Company outcome below.']
],
'Q071':[
['Values below are per family member.','| £2 | £0 | 0 | 0 |'],
['Values below are per family member.','| £2 | £0 | 0 | 0 |'],
['Values below are per family member.','| £2 | £0 | 0 | 0 |'],
['Values below are per family member.','| £2 | £0 | 0 | 0 |'],
['Values below are per family member.','| £4 | £1 | 2 | 1 |'],
['Values below are per family member.','| £4 | £1 | 2 | 1 |'],
['Values below are per family member.','| £4 | £1 | 2 | 1 |'],
['Values below are per family member.','| £4 | £1 | 2 | 1 |'],
['Values below are per family member.','| £8 | £2 | 4 | 2 |'],
['Values below are per family member.','| £8 | £2 | 4 | 2 |'],
['Values below are per family member.','| £8 | £2 | 4 | 2 |'],
['Values below are per family member.','| £8 | £2 | 4 | 2 |'],
['Values below are per family member.','| £14 | £3 | 8 | 3 |'],
['Values below are per family member.','| £14 | £3 | 8 | 3 |'],
['Values below are per family member.','| £14 | £3 | 8 | 3 |'],
['Values below are per family member.','| £14 | £3 | 8 | 3 |'],
['Values below are per family member.','| £20 | £4 | 12 | 4 |'],
['Values below are per family member.','| £20 | £4 | 12 | 4 |'],
['Values below are per family member.','| £20 | £4 | 12 | 4 |'],
['Values below are per family member.','| £20 | £4 | 12 | 4 |']
],
'Q072':[
['| 1710 | 1–5 |'],
['Company monopoly, without deregulation procedures.'],
['| 1758 | 3–7 |'],
['Company starts with monopoly; deregulation can be voted in.'],
['| 1813 | 5–8 |'],
['Starts deregulated, allowing firms'],
['| Long 1710 | 1–8 |'],
['Same initial position as 1710, with deregulation available']
],
'Q073':[
['| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |'],
['| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |'],
['| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |'],
['| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |'],
['| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |'],
['| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |'],
['| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts |'],
['| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts |'],
['| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts |'],
['| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts |'],
['| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts | One regiment per Army;'],
['one Company ship in East Indian.'],
['Bengal control token in Bengal Presidency.']
],
'Q074':[
["| 1813 | 5–8 | £10 expectations / 0 | £3 | Military Oversight, Deregulation (Debtor's Prison side), Calico Acts |"],
["| 1813 | 5–8 | £10 expectations / 0 | £3 | Military Oversight, Deregulation (Debtor's Prison side), Calico Acts |"],
["| 1813 | 5–8 | £10 expectations / 0 | £3 | Military Oversight, Deregulation (Debtor's Prison side), Calico Acts |"],
["| 1813 | 5–8 | £10 expectations / 0 | £3 | Military Oversight, Deregulation (Debtor's Prison side), Calico Acts |"],
["Deregulation (Debtor's Prison side)"],
["| 1813 | 5–8 | £10 expectations / 0 | £3 | Military Oversight, Deregulation (Debtor's Prison side), Calico Acts |"],
['Two regiments per Army'],
['one Company ship per sea zone.'],
['put **+2/−2 share-value token** in Court'],
['return the **Governor General law** to the box'],
['place its office overlay over Director of Trade.'],
['create China'],
['place Bombay/Madras/Bengal control tokens in their Presidencies']
],
'Q075':[
['Most/second awards are **3/1 VP if final turn 1–3, 5/2 if turn 4–6, 8/4 if turn 7–8**.'],
['Most/second awards are **3/1 VP if final turn 1–3, 5/2 if turn 4–6, 8/4 if turn 7–8**.'],
['Most/second awards are **3/1 VP if final turn 1–3, 5/2 if turn 4–6, 8/4 if turn 7–8**.'],
['Most/second awards are **3/1 VP if final turn 1–3, 5/2 if turn 4–6, 8/4 if turn 7–8**.','Tied first: only lower award to each tied player'],
['no other award.']
],
'Q076':[
['Social 2.'],
['Company shares 1'],
['Shipping 0'],
['Manufacturing 0'],
['**lined** Standing £4/6/8'],
['Debt 5/6/7/8'],
['**PERMITS the PM to call** the special vote'],
['**starred** Standing £4'],
['Debt 8 **REQUIRES the PM to call** it.'],
['**REQUIRES the PM to call** it.'],
['reset S is above £10.'],
['**Initial Power positions, from lowest to highest:** Manufacturing 0 → Shipping 0 → Company shares 1 → Social 2. The two zero-Power spaces are distinct ordered positions; Manufacturing starts below Shipping.']
],
'Q077':[
["unrest does **not** add to a Foreign Invasion's primary attack strength or determine its resulting tower levels."],
['On a successful Foreign Invasion, close all orders in the target region once'],
['if they are already all closed, Cascade instead.']
],
'Q078':[
['Mercantile/Diplomatic Connection reducing a check to zero dice means failure'],
['reduce Balance by twice the highest roll (minimum zero)'],
['take cash from the bank equal to that actual Balance reduction'],
['Public Demands Impeachment returns member to supply'],
['office card to vacancies'],
['Military Oversight demotes one Commander to an officer'],
['the SAME former Commander remains eligible to become COMMANDER again']
]
}
reasons={
'Q060':'All eight requested limits, eligibility conditions, discount effects and final-scoring timing are stated in the same-entry retirement passage.',
'Q061':'All seven treasury destinations, permitted uses and the family-cash restriction are resolved by the included firm passages.',
'Q062':'The included investment introduction places Firms after Family share creation and before Hiring and names both conflict decision makers.',
'Q063':'The ship paragraph correctly supplies both consent rules, prohibited ship types, prices and payment destinations.',
'Q064':'The takeover paragraph supplies the complete eligibility/majority-consent procedure without requiring initiator share ownership, and preserves all assets and both cube positions while resetting the former charter.',
'Q065':'All requested consent, primary-firm, tie, excess-share and secondary-asset outcomes are explicit.',
'Q066':'The Hobnob row and storm sentence correctly resolve every prohibition, expense obligation and retained-marker/storm outcome.',
'Q067':'Emergency investment explicitly inherits normal eligibility, remains available at the share cap without new shares, pays expenses, loses remaining cash and reduces Value once per investment.',
'Q068':'The emergency-merger passage states the one-other-firm limit and the required ordering and coverage of both firms’ expenses.',
'Q069':'The voluntary-dissolution paragraph gives unanimous consent and each requested share, ship and workshop outcome.',
'Q070':'The final-scoring sequence applies firm points and prison deductions before ordinary outcome scoring, supplies the Value rates and totals each player’s fractional points before rounding once.',
'Q071':'Every requested table cell matches the fixed values, with the table explicitly stated per family member.',
'Q072':'The scenario tables correctly give all four start/end ranges and Deregulation statuses.',
'Q073':'Both scenario rows state all requested finance, laws, regiments, Company ships and the 1758 Bengal control-token placement.',
'Q074':'The 1813 row and following paragraph contain every requested numeric setup value, law, token, overlay and office change.',
'Q075':'The Power paragraph correctly gives all award pairs and the lower-only/no-other-award tied-first result.',
'Q076':'All initial Power rates and their order, lined/starred thresholds and their permissions/obligations are explicit; S above the £10 expectation is the requested £10 position.',
'Q077':'The Foreign Invasion ruling excludes unrest from both quantities and explicitly closes orders once or Cascades if already all closed.',
'Q078':'The errata paragraph correctly gives zero-dice failure, the capped Balance/payout procedure, impeachment destinations and former-Commander reappointment eligibility.'
}
grades=[]
for entry in packet['entries']:
 qid=entry['id']
 facts=entry['requested_fact_scope_entry']['material_requested_facts']
 quotes=chosen[qid]
 assert len(quotes)==len(facts),(qid,len(quotes),len(facts))
 reader=entry['reader_a_entry']
 allowed=[reader['answer']]+[e['quote'] for e in reader.get('evidence',[])]
 for group in quotes:
  for quote in group:
   assert quote and any(quote in field for field in allowed),(qid,quote)
 grades.append({'id':qid,'grade':'Correct','reason':reasons[qid],'material_parts':[{'requirement':fact,'status':'covered','reader_quotes':group} for fact,group in zip(facts,quotes)],'unsupported_guesses':[],'summary_issue_if_any':None})
assert len(grades)==19
out=base/'grades-same-entry.json'
data=json.dumps({'block_id':'block-04','readers':{'reader-a':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n'
out.write_text(data)
print(json.dumps({'path':str(out),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(data.encode()).hexdigest()}))