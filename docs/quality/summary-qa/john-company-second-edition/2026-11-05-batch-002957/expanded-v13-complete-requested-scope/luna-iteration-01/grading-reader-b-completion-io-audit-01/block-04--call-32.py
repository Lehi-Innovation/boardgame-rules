from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-01/grading-reader-b/block-04')
p=json.loads((base/'packet.json').read_text())
# Human-selected content grades and exact same-entry supporting quotations, in fixed atom order.
decisions=[
('Q060','Correct','All eight requested retirement limits, eligibility conditions and final-scoring timing are covered.',[
'Each shareholder may make one additional retirement per London Season from supply rather than Pensioners, irrespective of number of firms owned.',
'Each shareholder may make one additional retirement per London Season from supply rather than Pensioners, irrespective of number of firms owned.',
'Each shareholder may make one additional retirement per London Season from supply rather than Pensioners, irrespective of number of firms owned.',
'Actual spending after spouse discounts cannot exceed highest total dividend marker among any firm where shareholder has a share; printed prize price may exceed marker if discount covers difference.',
'No retirement from a firm whose marker is absent or zero.',
'Spouse discounts can allow a higher printed-cost prize;',
'At start of Final Scoring, score firms then allow one special retirement regardless of Company success/failure, before normal final-scoring steps;',
'At start of Final Scoring, score firms then allow one special retirement regardless of Company success/failure, before normal final-scoring steps;']),
('Q061','Correct','Every requested treasury destination, payment source and family-cash restriction is correctly resolved.',[
'Bank pays £5 per investment to London treasury; trade revenue goes India treasury.',
'Bank pays £5 per investment to London treasury; trade revenue goes India treasury.',
'London pays ship acquisitions/fitting and bids; expenses can use either or both treasuries; dividends are from India only.',
'London pays ship acquisitions/fitting and bids; expenses can use either or both treasuries; dividends are from India only.',
'London pays ship acquisitions/fitting and bids; expenses can use either or both treasuries; dividends are from India only.',
'London pays ship acquisitions/fitting and bids; expenses can use either or both treasuries; dividends are from India only.',
'No, family cash cannot transfer into or out of firm treasuries.']),
('Q062','Correct','Phase placement includes Family share creation and precedes Hiring; both conflict authorities are correct.',[
'After Family share creation, before Hiring, take investments actions without set order until nobody wishes more.',
'After Family share creation, before Hiring, take investments actions without set order until nobody wishes more.',
'Manager resolves timing conflicts within firm; PM resolves conflicts between firms.',
'Manager resolves timing conflicts within firm; PM resolves conflicts between firms.']),
('Q063','Correct','All fitting and purchase consent requirements, prohibited ship types, costs and payment destinations are covered.',[
'No; fitting a ship from another player’s yard requires yard owner’s consent.',
'Fit costs £3 from firm London treasury to bank;',
'No, firms cannot acquire Company ships or extra ships.',
'No, firms cannot acquire Company ships or extra ships.',
'Yes, if owner consents; buy a player-owned ship already in Company.',
'Unfatigued ship costs £3, fatigued £2; firm London treasury pays Shipping treasury.',
'Unfatigued ship costs £3, fatigued £2; firm London treasury pays Shipping treasury.',
'Unfatigued ship costs £3, fatigued £2; firm London treasury pays Shipping treasury.']),
('Q064','Correct','The complete takeover instructions cover eligibility, majority consent, all assets and both markers, and former-manager reset. Their stated eligibility permits a non-shareholding initiator; money covers both firm treasuries.',[
'Only a player who **manages NO firm at all** may initiate one; managing a different firm also makes you ineligible.',
"Obtain consent of holders of a majority of the target's shares",
"Only a player who **manages NO firm at all** may initiate one; managing a different firm also makes you ineligible. Obtain consent of holders of a majority of the target's shares, then move firm's ships, money and shares to own charter, copy both cube positions; former manager returns cubes and flips board to family side.",
'Target firm ships, money and shares move to new charter; copy both cube positions.',
'Target firm ships, money and shares move to new charter; copy both cube positions.',
'Target firm ships, money and shares move to new charter; copy both cube positions.',
'Target firm ships, money and shares move to new charter; copy both cube positions.',
'Target firm ships, money and shares move to new charter; copy both cube positions.',
'Former manager returns cubes and flips family board to family side.',
'Former manager returns cubes and flips family board to family side.']),
('Q065','Correct','Unanimous consent, primary selection and tie choice, excess-share consent, treasury consolidation and charter reset are all supplied.',[
"Managers negotiate with **every shareholder's consent**.",
'Highest-value firm is primary; if tied, players choose among tied firms.',
'Highest-value firm is primary; if tied, players choose among tied firms.',
'If primary would exceed ten shares, return excess shares to their owners’ supplies with those owners’ consent.',
'Transfer secondary treasury funds, shares and ships to primary; secondary boards return to family side.',
'Transfer secondary treasury funds, shares and ships to primary; secondary boards return to family side.']),
('Q066','Correct','All six requested Hobnob restrictions and consequences are explicit.',[
'Hobnob has no bid, trade or dividends.',
'Hobnob has no bid, trade or dividends.',
'Hobnob has no bid, trade or dividends.',
'Yes, Hobnob firm still pays expenses.',
'Retain prior dividend marker for retirement; Hobnob ships are exempt from storms.',
'Retain prior dividend marker for retirement; Hobnob ships are exempt from storms.']),
('Q067','Correct','The emergency-investment answer preserves ordinary investment eligibility and both share restrictions, permits capped investment without a new share, and resolves cash and Value effects.',[
'Yes. Emergency investments may still be accepted at ten shares; the cap prevents a new share but not the investment contribution.',
'Yes. Emergency investments may still be accepted at ten shares; the cap prevents a new share but not the investment contribution.',
"return one eligible Company share to supply or flip workshop to invested side.",
'Company shares while Standing or Debt is lined are ineligible.',
'Yes. Shares created this turn cannot be contributed, even if traded away.',
'Use funds to pay expenses, lose any remaining cash, and lower Value one space per emergency investment.',
'Use funds to pay expenses, lose any remaining cash, and lower Value one space per emergency investment.',
'Use funds to pay expenses, lose any remaining cash, and lower Value one space per emergency investment.']),
('Q068','Correct','The one-other-firm limit and order of both expense payments are correct.',[
'Emergency merger may use only one other firm;',
'Other firm pays its own expenses first if not already paid, then covers endangered firm’s unpaid expenses.',
'Other firm pays its own expenses first if not already paid, then covers endangered firm’s unpaid expenses.']),
('Q069','Correct','All-shareholder consent and the share, ship and invested-workshop outcomes are explicit.',[
'All shareholders must consent.',
'Shares go to Debtor’s Prison (−1 VP each); ships return to matching shipyards; charter flips to family side.',
'Shares go to Debtor’s Prison (−1 VP each); ships return to matching shipyards; charter flips to family side.',
'No; invested workshops remain invested for rest of game.']),
('Q070','Correct','The entry resolves firm-share Value rates, prison losses, aggregate rounding, timing and applicability under either Company outcome.',[
'Before ordinary Power/Court/outcome scoring, add each player’s firm-share VP across all firms, round that total down once, then deduct 1 VP per own family piece in Debtor’s Prison.',
'Per-share Value rates: 1 = −1 VP; 2 = 0; 3–4 = ½; 5–7 = 1; 8–9 = 1½; 10 = 2.',
'Before ordinary Power/Court/outcome scoring, add each player’s firm-share VP across all firms, round that total down once, then deduct 1 VP per own family piece in Debtor’s Prison.',
'Before ordinary Power/Court/outcome scoring, add each player’s firm-share VP across all firms, round that total down once, then deduct 1 VP per own family piece in Debtor’s Prison.',
'This firm scoring happens whether Company survived or failed.']),
('Q071','Correct','All twenty requested prize values are correct, with the per-member basis explicit.',[
'Per member: £2/£0/0/0; £4/£1/2/1; £8/£2/4/2; £14/£3/8/3; £20/£4/12/4 (cost/upkeep/VP/windows).'
]*20),
('Q072','Correct','All four start/end turn ranges and deregulation statuses match the fixed key.',[
'1710 turns 1–5; 1758 turns 3–7; 1813 turns 5–8; Long 1710 turns 1–8.',
'1758 can vote it in; Long 1710 makes it available separately; 1813 starts deregulated; 1710 has no deregulation procedures.',
'1710 turns 1–5; 1758 turns 3–7; 1813 turns 5–8; Long 1710 turns 1–8.',
'1758 can vote it in; Long 1710 makes it available separately; 1813 starts deregulated; 1710 has no deregulation procedures.',
'1710 turns 1–5; 1758 turns 3–7; 1813 turns 5–8; Long 1710 turns 1–8.',
'1758 can vote it in; Long 1710 makes it available separately; 1813 starts deregulated; 1710 has no deregulation procedures.',
'1710 turns 1–5; 1758 turns 3–7; 1813 turns 5–8; Long 1710 turns 1–8.',
'1758 can vote it in; Long 1710 makes it available separately; 1813 starts deregulated; 1710 has no deregulation procedures.']),
('Q073','Correct','Every requested 1710 and 1758 setup figure is provided, including Eastern ship placement and the Bengal control token.',[
'| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |',
'| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |',
'| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |',
'| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |',
'| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |',
'| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |',
'| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts | One regiment per Army; one Company ship in East Indian. Bengal control token in Bengal Presidency. |',
'| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts | One regiment per Army; one Company ship in East Indian. Bengal control token in Bengal Presidency. |',
'| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts | One regiment per Army; one Company ship in East Indian. Bengal control token in Bengal Presidency. |',
'| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts | One regiment per Army; one Company ship in East Indian. Bengal control token in Bengal Presidency. |',
'| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts | One regiment per Army; one Company ship in East Indian. Bengal control token in Bengal Presidency. |',
'| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts | One regiment per Army; one Company ship in East Indian. Bengal control token in Bengal Presidency. |',
'| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts | One regiment per Army; one Company ship in East Indian. Bengal control token in Bengal Presidency. |']),
('Q074','Correct','The full 1813 setup covers every requested financial, law, force, share-value, office and control-token change.',[
'1813: £10 expectations/0 Debt; £3 each office; Military Oversight, Deregulation (Debtor’s Prison side), Calico Acts; two regiments per Army, one Company ship per sea zone.',
'1813: £10 expectations/0 Debt; £3 each office; Military Oversight, Deregulation (Debtor’s Prison side), Calico Acts; two regiments per Army, one Company ship per sea zone.',
'1813: £10 expectations/0 Debt; £3 each office; Military Oversight, Deregulation (Debtor’s Prison side), Calico Acts; two regiments per Army, one Company ship per sea zone.',
'1813: £10 expectations/0 Debt; £3 each office; Military Oversight, Deregulation (Debtor’s Prison side), Calico Acts; two regiments per Army, one Company ship per sea zone.',
'1813: £10 expectations/0 Debt; £3 each office; Military Oversight, Deregulation (Debtor’s Prison side), Calico Acts; two regiments per Army, one Company ship per sea zone.',
'1813: £10 expectations/0 Debt; £3 each office; Military Oversight, Deregulation (Debtor’s Prison side), Calico Acts; two regiments per Army, one Company ship per sea zone.',
'1813: £10 expectations/0 Debt; £3 each office; Military Oversight, Deregulation (Debtor’s Prison side), Calico Acts; two regiments per Army, one Company ship per sea zone.',
'1813: £10 expectations/0 Debt; £3 each office; Military Oversight, Deregulation (Debtor’s Prison side), Calico Acts; two regiments per Army, one Company ship per sea zone.',
'Place ±2 share-value token in Court.',
'Create China; place Bombay/Madras/Bengal control tokens in respective Presidencies. Return Governor General law to box, put overlay over Director, use GG instead of Director and no Governors.',
'Create China; place Bombay/Madras/Bengal control tokens in respective Presidencies. Return Governor General law to box, put overlay over Director, use GG instead of Director and no Governors.',
'Create China; place Bombay/Madras/Bengal control tokens in respective Presidencies. Return Governor General law to box, put overlay over Director, use GG instead of Director and no Governors.',
'Create China; place Bombay/Madras/Bengal control tokens in respective Presidencies. Return Governor General law to box, put overlay over Director, use GG instead of Director and no Governors.']),
('Q075','Correct','All award pairs and tied-first lower-award-only outcomes are covered.',[
'Power first/second: turns 1–3 3/1 VP; 4–6 5/2; 7–8 8/4. Tied first group each lower award only; no other award.',
'Power first/second: turns 1–3 3/1 VP; 4–6 5/2; 7–8 8/4. Tied first group each lower award only; no other award.',
'Power first/second: turns 1–3 3/1 VP; 4–6 5/2; 7–8 8/4. Tied first group each lower award only; no other award.',
'Power first/second: turns 1–3 3/1 VP; 4–6 5/2; 7–8 8/4. Tied first group each lower award only; no other award.',
'Power first/second: turns 1–3 3/1 VP; 4–6 5/2; 7–8 8/4. Tied first group each lower award only; no other award.']),
('Q076','Correct','The starting Power rates and relative order, all lined/starred thresholds and their effects, and S at the £10 expectations column are covered. “Above £10” describes the printed reset marker location.',[
'Manufacturing 0 below Shipping 0; Company shares 1; Social 2. The two zero spaces are distinct ordered positions.',
'Manufacturing 0 below Shipping 0; Company shares 1; Social 2. The two zero spaces are distinct ordered positions.',
'Manufacturing 0 below Shipping 0; Company shares 1; Social 2. The two zero spaces are distinct ordered positions.',
'Manufacturing 0 below Shipping 0; Company shares 1; Social 2. The two zero spaces are distinct ordered positions.',
'Lined Standing £4/6/8 or Debt 5/6/7/8 permits PM call; starred Standing £4 or Debt 8 requires PM call.',
'Lined Standing £4/6/8 or Debt 5/6/7/8 permits PM call; starred Standing £4 or Debt 8 requires PM call.',
'Lined Standing £4/6/8 or Debt 5/6/7/8 permits PM call; starred Standing £4 or Debt 8 requires PM call.',
'Lined Standing £4/6/8 or Debt 5/6/7/8 permits PM call; starred Standing £4 or Debt 8 requires PM call.',
'Lined Standing £4/6/8 or Debt 5/6/7/8 permits PM call; starred Standing £4 or Debt 8 requires PM call.',
'Lined Standing £4/6/8 or Debt 5/6/7/8 permits PM call; starred Standing £4 or Debt 8 requires PM call.',
'Reset S is above £10.',
'**Initial Power positions, from lowest to highest:** Manufacturing 0 → Shipping 0 → Company shares 1 → Social 2. The two zero-Power spaces are distinct ordered positions; Manufacturing starts below Shipping.']),
('Q077','Correct','The ruling excludes unrest from both quantities and correctly closes orders once or Cascades when all are already closed.',[
"unrest does **not** add to a Foreign Invasion's primary attack strength or determine its resulting tower levels.",
'Successful Foreign Invasion closes all target orders once, Cascading if already all closed; Region Loss does not close them a second time.',
'Successful Foreign Invasion closes all target orders once, Cascading if already all closed; Region Loss does not close them a second time.']),
('Q078','Correct','All four corrected card cases are resolved, including the Fraud floor and actual-reduction payout and former Commander reappointment.',[
'Mercantile/Diplomatic Connection reducing a check to zero dice means failure;',
'reduce Balance by twice highest roll (minimum zero), and take from bank only the actual Balance reduction.',
'reduce Balance by twice highest roll (minimum zero), and take from bank only the actual Balance reduction.',
'Return member to supply and office card to vacancies.',
'Return member to supply and office card to vacancies.',
'Demote one Commander to officer, then appoint Commander from officers; same former Commander remains eligible for Commander appointment again.',
'Demote one Commander to officer, then appoint Commander from officers; same former Commander remains eligible for Commander appointment again.'])
]
assert len(decisions)==len(p['entries'])==19
grades=[]
for entry,(qid,grade,reason,quotes) in zip(p['entries'],decisions):
 assert qid==entry['id']
 atoms=entry['requested_fact_scope_entry']['material_requested_facts']
 assert len(atoms)==len(quotes),(qid,len(atoms),len(quotes))
 reader=entry['reader_b_entry']
 allowed=[reader['answer']]+[x['supported_fact_or_case_result'] for x in reader.get('clause_ledger',[])]+[x for x in reader.get('case_conclusions',[]) if isinstance(x,str)]+[x['quote'] for x in reader.get('evidence',[])]
 for quote in quotes:
  assert quote and any(quote in s for s in allowed),(qid,quote)
 grades.append({'id':qid,'grade':grade,'reason':reason,'material_parts':[{'requirement':atom,'status':'covered','reader_quotes':[quote]} for atom,quote in zip(atoms,quotes)],'unsupported_guesses':[],'summary_issue_if_any':None})
output=base/'grades-same-entry.json'
output.write_text(json.dumps({'block_id':'block-04','readers':{'reader-b':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(output),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}))