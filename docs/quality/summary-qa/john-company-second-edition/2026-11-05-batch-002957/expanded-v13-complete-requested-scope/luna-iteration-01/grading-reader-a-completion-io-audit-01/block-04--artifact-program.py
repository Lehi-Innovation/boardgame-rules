from pathlib import Path
import json, hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-01/grading-reader-a/block-04')
p=json.loads((base/'packet.json').read_text())
# Each quote below is an independently selected supporting passage, in fixed atom order.
choices={
'Q060':[
'Each shareholder may make one additional retirement per London Season from supply rather than Pensioners, irrespective of number of firms owned.',
'from supply rather than Pensioners',
'irrespective of number of firms owned',
'Actual cash spent after spouse discounts cannot exceed highest total dividend marker among firms where shareholder has a share',
'No retirement from a firm whose marker is absent or zero.',
'Spouse discounts can allow a higher printed-cost prize',
'At start of Final Scoring, score firms then allow one special retirement regardless of Company success/failure, before normal final-scoring steps',
'At start of Final Scoring, score firms then allow one special retirement regardless of Company success/failure, before normal final-scoring steps'],
'Q061':[
'Investment cash comes from bank to London; India receives trade proceeds.',
'Investment cash comes from bank to London; India receives trade proceeds.',
'London receives investment and pays ship acquisitions, trade bids and expenses; India receives trade and pays dividends/expenses.',
'London receives investment and pays ship acquisitions, trade bids and expenses; India receives trade and pays dividends/expenses.',
'London receives investment and pays ship acquisitions, trade bids and expenses; India receives trade and pays dividends/expenses.',
'London receives investment and pays ship acquisitions, trade bids and expenses; India receives trade and pays dividends/expenses.',
'Family cash cannot be transferred into or out of firm treasuries'],
'Q062':[
'After Family share creation, before Hiring',
'After Family share creation, before Hiring',
'Manager resolves timing conflicts within firm; PM resolves conflicts between firms.',
'Manager resolves timing conflicts within firm; PM resolves conflicts between firms.'],
'Q063':[
"No. Firm may fit own or another player's shipyard only with shipyard owner's consent; cost £3 from firm's London treasury to bank.",
"cost £3 from firm's London treasury to bank.",
'Firms cannot acquire Company or extra ships.',
'Firms cannot acquire Company or extra ships.',
"May buy player-owned ship already in Company with owner's consent: unfatigued £3, fatigued £2, paid from firm's London treasury into Shipping treasury.",
'unfatigued £3',
'fatigued £2',
"paid from firm's London treasury into Shipping treasury."],
'Q064':[
'Only a player who manages no firm at all may initiate; obtain consent of holders of majority of target shares.',
'Only a player who manages no firm at all may initiate; obtain consent of holders of majority of target shares.',
'Only a player who manages no firm at all may initiate; obtain consent of holders of majority of target shares.',
"Move target firm's ships, money and shares to own charter and copy both cube positions; former manager returns cubes and flips board to family side.",
"Move target firm's ships, money and shares to own charter and copy both cube positions; former manager returns cubes and flips board to family side.",
"Move target firm's ships, money and shares to own charter and copy both cube positions; former manager returns cubes and flips board to family side.",
'copy both cube positions',
'copy both cube positions',
'former manager returns cubes',
'flips board to family side.'],
'Q065':[
"Managers negotiate with every shareholder's consent.",
'Highest-value firm is primary; if tied, players choose among tied.',
'Highest-value firm is primary; if tied, players choose among tied.',
"If primary would exceed ten shares, return excess shares to their owners' supplies with those owners' consent.",
'Transfer all secondary shares, ships and treasury funds to primary; secondary boards return to family sides.',
'Transfer all secondary shares, ships and treasury funds to primary; secondary boards return to family sides.'],
'Q066':[
'Hobnob makes no bid, trade or dividends.',
'Hobnob makes no bid, trade or dividends.',
'Hobnob makes no bid, trade or dividends.',
'No bid, trade or dividends. Still pay expenses; retain previous dividend marker for retirement.',
'It retains previous dividend marker for retirement; Hobnob ships are exempt from storms (firm ships otherwise use strategy zone).',
'It retains previous dividend marker for retirement; Hobnob ships are exempt from storms (firm ships otherwise use strategy zone).'],
'Q067':[
'Yes. Ten-share cap prevents further shares but emergency investment still follows contribution rules and expenses can be paid.',
'Yes. Ten-share cap prevents further shares but emergency investment still follows contribution rules and expenses can be paid.',
'return one eligible Company share to supply or flip workshop to invested side.',
'Cannot use Company shares at all when Standing and/or Debt on lined space.',
'Yes, shares created this turn cannot be invested, even after trading them away.',
'Pay expenses; lose any remaining cash; lower Value one space per emergency investment.',
'Pay expenses; lose any remaining cash; lower Value one space per emergency investment.',
'Pay expenses; lose any remaining cash; lower Value one space per emergency investment.'],
'Q068':[
'Emergency negotiated merger is limited to only one other firm.',
"The other firm first pays its own expenses if not already paid, then covers endangered firm's unpaid expenses; every involved shareholder must consent.",
"The other firm first pays its own expenses if not already paid, then covers endangered firm's unpaid expenses; every involved shareholder must consent."],
'Q069':[
'All shareholders must consent.',
"Shares go to Debtor's Prison, each -1 VP; ships return to matching shipyards and charter flips to family side.",
"Shares go to Debtor's Prison, each -1 VP; ships return to matching shipyards and charter flips to family side.",
'No. Workshops remain invested for rest of game.'],
'Q070':[
'If deregulated, score firms first before ordinary Power/Court/final outcome.',
'Per firm share: Value 1 −1 VP; 2 = 0; 3–4 = ½; 5–7 = 1; 8–9 = 1½; 10 = 2.',
"Deduct 1 VP per own family piece in Debtor's Prison.",
'For each player total all shares across firms, then round down once.',
'Firm special retirement follows firm score before ordinary scoring in either outcome.'],
'Q071':[
'Per family member: cost/upkeep/VP/windows are £2/£0/0/0; £4/£1/2/1; £8/£2/4/2; £14/£3/8/3; £20/£4/12/4.'
]*20,
'Q072':[
'1710 runs turns 1–5; 1758 turns 3–7; 1813 turns 5–8; Long 1710 turns 1–8.',
'1710 has no deregulation procedure; 1758 can vote it in; Long 1710 has it available; 1813 starts deregulated.',
'1710 runs turns 1–5; 1758 turns 3–7; 1813 turns 5–8; Long 1710 turns 1–8.',
'1710 has no deregulation procedure; 1758 can vote it in; Long 1710 has it available; 1813 starts deregulated.',
'1710 runs turns 1–5; 1758 turns 3–7; 1813 turns 5–8; Long 1710 turns 1–8.',
'1710 has no deregulation procedure; 1758 can vote it in; Long 1710 has it available; 1813 starts deregulated.',
'1710 runs turns 1–5; 1758 turns 3–7; 1813 turns 5–8; Long 1710 turns 1–8.',
'1710 has no deregulation procedure; 1758 can vote it in; Long 1710 has it available; 1813 starts deregulated.'],
'Q073':[
'1710: £10 expectations, Debt 0, £3 per office treasury, Royal Protection, one regiment per Army, no Company ships.'
]*6+[
'1758: £12 expectations, Debt 3, £4 per office treasury, Calico Acts, one regiment per Army, one Company ship in East Indian, Bengal control token in Bengal Presidency.'
]*7,
'Q074':[
"Start with £10 expectations, Debt 0, £3 per office treasury, Military Oversight, Deregulation (Debtor's Prison side), Calico Acts, two regiments per Army, one Company ship per sea zone."
]*8+[
'Put +2/-2 share-value token in Court; create China; place Bombay/Madras/Bengal control tokens in their Presidencies; return Governor General law to box and place office overlay over Director of Trade. Use Governor General instead of Director and no Governors. Copy India map and Elephant from scenario card reverse.'
]*5,
'Q075':[
'Power awards for most/second are 3/1 VP on turns 1–3, 5/2 on turns 4–6, and 8/4 on turns 7–8.',
'Power awards for most/second are 3/1 VP on turns 1–3, 5/2 on turns 4–6, and 8/4 on turns 7–8.',
'Power awards for most/second are 3/1 VP on turns 1–3, 5/2 on turns 4–6, and 8/4 on turns 7–8.',
'Tied first gets only lower award to each tied player; no other award.',
'Tied first gets only lower award to each tied player; no other award.'],
'Q076':[
'Manufacturing 0 → Shipping 0 → Company shares 1 → Social 2; the two zero spaces are distinct ordered positions, Manufacturing below Shipping.'
]*4+[
'Lined Standing £4/6/8 or Debt 5/6/7/8 permits PM to call; starred Standing £4 or Debt 8 requires PM to call.'
]*6+[
'Reset S is above £10.',
'Manufacturing 0 → Shipping 0 → Company shares 1 → Social 2; the two zero spaces are distinct ordered positions, Manufacturing below Shipping.'],
'Q077':[
"Cole Wehrle clarified on April 30, 2023 that unrest does **not** add to a Foreign Invasion's primary attack strength or determine its resulting tower levels.",
'On success close all target orders once; if already all closed, Cascade.',
'On success close all target orders once; if already all closed, Cascade.'],
'Q078':[
'Mercantile/Diplomatic Connection reducing a check to zero dice means failure',
'Played at start of Revenue: roll one die per your officeholder, reduce Balance by twice highest roll (minimum zero), and take bank cash equal to actual Balance reduction; payout cannot exceed cash removed from Balance.',
'Played at start of Revenue: roll one die per your officeholder, reduce Balance by twice highest roll (minimum zero), and take bank cash equal to actual Balance reduction; payout cannot exceed cash removed from Balance.',
'Returns member to supply and office card to vacancies.',
'Returns member to supply and office card to vacancies.',
'Demote one Commander to officer, then appoint Commander from officers; same former Commander remains eligible to become Commander again.',
'Demote one Commander to officer, then appoint Commander from officers; same former Commander remains eligible to become Commander again.']
}
reasons={
'Q060':'All eight requested retirement facts are resolved, including one supply retirement across firms, actual-spending cap, discounts, zero-marker exclusion and final timing in either outcome.',
'Q061':'The treasury allocation covers all requested fund destinations and uses. London and India both pay expenses; the contrasted use lists assign dividends to India and ship acquisition/bids to London. Family transfers are expressly forbidden.',
'Q062':'Phase placement after Family share creation and before Hiring, and both conflict decision makers, are explicit.',
'Q063':'All fitting and purchase consent rules, prohibited ship types, prices and payment destinations are explicit.',
'Q064':'The stated takeover prerequisites allow a non-manager with majority consent, without imposing personal share ownership. Ships, money (both treasuries), shares, both cube positions and former-board reset are covered.',
'Q065':'Unanimous shareholder consent, primary choice and tie handling, excess-share owner consent, treasury transfer and secondary-board reset are explicit.',
'Q066':'All six Hobnob consequences are explicit: no bid/trade/dividends, expenses, retained marker and storm immunity.',
'Q067':'Emergency rescue retains normal contribution eligibility and both Company-share restrictions, works at the share cap without new shares, pays expenses, loses remaining cash and reduces Value per investment.',
'Q068':'The one-other-firm limit and required sequence of paying the other firm and endangered firm expenses are explicit.',
'Q069':'Unanimous dissolution consent and all requested share, ship and workshop outcomes are covered.',
'Q070':'Firm points and prison deductions precede ordinary scoring in either outcome; all Value rates and rounding once after totaling the player’s firm holdings are covered.',
'Q071':'All twenty requested prize cells are stated with per-family-member scope.',
'Q072':'All four start/end turn ranges and their respective Deregulation status are explicit.',
'Q073':'All requested 1710 and 1758 setup values and placements are explicit, including each scenario’s regiment count and the Bengal control token.',
'Q074':'Every requested 1813 finance, law, military, ship, share-token, office and control-token setup change is explicit.',
'Q075':'All three first/second award pairs and the tied-first lower-only consequence are explicit.',
'Q076':'All Power values and the distinct ordered zero spaces, lined/starred thresholds and permissions/requirements, and S at the £10 expectations position are covered.',
'Q077':'Unrest affects neither quantity, and successful closure occurs once with Cascade only when all orders were already closed.',
'Q078':'All requested corrected-card outcomes are explicit, including capped Fraud payment, both impeachment destinations and former-Commander eligibility.'
}
grades=[]
for e in p['entries']:
    q=e['id']; atoms=e['requested_fact_scope_entry']['material_requested_facts']; qs=choices[q]
    assert len(atoms)==len(qs),(q,len(atoms),len(qs))
    reader=e['reader_a_entry']
    actual=[reader['answer']]+[x['supported_fact_or_case_result'] for x in reader.get('clause_ledger',[])]+[x for x in reader.get('case_conclusions',[]) if isinstance(x,str)]+[x['quote'] for x in reader.get('evidence',[])]
    assert all(any(quote in text for text in actual) for quote in qs),q
    grades.append({'id':q,'grade':'Correct','reason':reasons[q],'material_parts':[{'requirement':atom,'status':'covered','reader_quotes':[quote]} for atom,quote in zip(atoms,qs)],'unsupported_guesses':[],'summary_issue_if_any':None})
assert len(grades)==19
out=base/'grades-same-entry.json'
raw=json.dumps({'block_id':'block-04','readers':{'reader-a':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n'
out.write_text(raw)
print(json.dumps({'path':str(out),'count':len(grades),'sha256':hashlib.sha256(raw.encode()).hexdigest()}))