from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-03/grading-reader-a/block-04')
p=json.loads((base/'packet.json').read_text())
# Independently selected substantive quotations, in the fixed requested-atom order.
chosen={
'Q060':[
'Each shareholder may make one additional retirement per London Season from supply rather than Pensioners, irrespective of number of firms owned.',
'from supply rather than Pensioners',
'irrespective of number of firms owned',
"**Actual cash spent after spouse discounts** cannot exceed the **highest total dividend marker** of any firm they own a share in",
'No retirement from a firm whose marker is absent or zero.',
'Spouse discounts can allow a higher printed-cost prize',
'At start of Final Scoring, score firms then allow one special retirement regardless of Company success/failure, before normal final-scoring steps',
'allow one special retirement regardless of Company success/failure'],
'Q061':[
'**London** receives the bank\'s £5 per investment',
'**India** receives trade and pays dividends/expenses.',
"Pay **£3 FROM the firm's London treasury TO the BANK**.",
'Commit a secret cash bid from London treasury.',
'can use either/both treasuries.',
'After expenses, manager may pay dividends **from India treasury only**.',
'**Family cash cannot be transferred into or out of firm treasuries.**'],
'Q062':[
'After Family share creation, before Hiring',
'After Family share creation, before Hiring',
'Manager resolves timing conflicts within firm',
'PM resolves conflicts between firms.'],
'Q063':[
"**must have that shipyard owner's consent**",
"Pay **£3 FROM the firm's London treasury TO the BANK**.",
'Firms cannot acquire Company or extra ships.',
'Firms cannot acquire Company or extra ships.',
"May buy player-owned ship already in Company with owner's consent",
'unfatigued £3, fatigued £2',
'unfatigued £3, fatigued £2',
"paid **from the firm's London treasury into Shipping treasury**"],
'Q064':[
'Only a player who **manages NO firm at all** may initiate one; managing a different firm also makes you ineligible.',
"Obtain consent of holders of a majority of the target's shares",
"Only a player who **manages NO firm at all** may initiate one; managing a different firm also makes you ineligible. Obtain consent of holders of a majority of the target's shares",
"move firm's ships, money and shares to own charter",
"move firm's ships, money and shares to own charter",
"move firm's ships, money and shares to own charter",
'copy both cube positions',
'copy both cube positions',
'former manager returns cubes',
'flips board to family side.'],
'Q065':[
"Managers negotiate with **every shareholder's consent**.",
'Highest-value firm is primary',
'if tied, players choose among tied.',
"**If the primary would exceed ten shares, RETURN the excess shares to their OWNERS' SUPPLIES, with those owners' consent.**",
'Transfer all secondary shares, ships and treasury funds to primary',
'secondary boards return to family sides.'],
'Q066':[
'| Hobnob | No bid, trade or dividends. Still pay expenses; retain previous dividend marker for retirement. |',
'| Hobnob | No bid, trade or dividends. Still pay expenses; retain previous dividend marker for retirement. |',
'| Hobnob | No bid, trade or dividends. Still pay expenses; retain previous dividend marker for retirement. |',
'Still pay expenses',
'retain previous dividend marker for retirement.',
'Firm ships face storms in strategy zone; Hobnob exempts them.'],
'Q067':[
'Emergency investments follow the Company-share/workshop eligibility rules under **Firms phase: investments**, even when ten-share cap prevents more shares',
'Up to ten firm shares; further investments still contribute £5 but create no shares.',
'return one eligible Company share to supply or flip workshop to invested side.',
'Cannot use Company shares at all when Standing and/or Debt on lined space.',
'Cannot use shares created this turn, even after trading them away.',
'pay expenses, lose any remaining cash, lower Value one space per emergency investment.',
'lose any remaining cash',
'lower Value one space per emergency investment.'],
'Q068':[
'**emergency negotiated merger with only ONE other firm**',
'The other firm must first pay its own expenses if not already paid',
"then cover the endangered firm's unpaid expenses."],
'Q069':[
'**Voluntary dissolution:** All shareholders must consent.',
"shares go to Debtor's Prison (each −1 VP)",
'ships return to their matching shipyards',
'Workshops remain invested for the rest of the game.'],
'Q070':[
'| 1. Firms, if deregulated | **BEFORE ordinary Power/Court/final-outcome scoring**',
'Firm-track VP per share: Value 1 = −1 VP; 2 = 0; 3–4 = ½; 5–7 = 1; 8–9 = 1½; 10 = 2.',
"Deduct **1 VP per own family piece in Debtor's Prison**.",
"for each player separately add VP from all their shares across all their firms, then **round that player's total DOWN once**.",
'| 1. Firms, if deregulated | **BEFORE ordinary Power/Court/final-outcome scoring**, for each player separately add VP from all their shares across all their firms, then **round that player\'s total DOWN once**. Deduct **1 VP per own family piece in Debtor\'s Prison**. **The next row (step2) describes the ONE eligible special firm retirement per shareholder, even on Company failure; ordinary scoring begins at step3.** |'],
'Q071':[
'| £2 | £0 | 0 | 0 |','| £2 | £0 | 0 | 0 |','| £2 | £0 | 0 | 0 |','| £2 | £0 | 0 | 0 |',
'| £4 | £1 | 2 | 1 |','| £4 | £1 | 2 | 1 |','| £4 | £1 | 2 | 1 |','| £4 | £1 | 2 | 1 |',
'| £8 | £2 | 4 | 2 |','| £8 | £2 | 4 | 2 |','| £8 | £2 | 4 | 2 |','| £8 | £2 | 4 | 2 |',
'| £14 | £3 | 8 | 3 |','| £14 | £3 | 8 | 3 |','| £14 | £3 | 8 | 3 |','| £14 | £3 | 8 | 3 |',
'| £20 | £4 | 12 | 4 |','| £20 | £4 | 12 | 4 |','| £20 | £4 | 12 | 4 |','| £20 | £4 | 12 | 4 |'],
'Q072':[
'| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |',
'| 1710 | Recommended first game; Company monopoly, without deregulation procedures. |',
'| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts | One regiment per Army; one Company ship in East Indian. Bengal control token in Bengal Presidency. |',
'| 1758 | Company starts with monopoly; deregulation can be voted in. |',
"| 1813 | 5–8 | £10 expectations / 0 | £3 | Military Oversight, Deregulation (Debtor's Prison side), Calico Acts | Two regiments per Army; one Company ship per sea zone. |",
'| 1813 | Starts deregulated, allowing firms; recommended with five or six players. |',
'| Long 1710 | 1–8 | Same as 1710 | £3 | Royal Protection; Deregulation available separately | Same as 1710. |',
'| Long 1710 | Same initial position as 1710, with deregulation available; can run eight turns, often twice the normal length. |'],
'Q073':[
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
'Bengal control token in Bengal Presidency.'],
'Q074':[
"| 1813 | 5–8 | £10 expectations / 0 | £3 | Military Oversight, Deregulation (Debtor's Prison side), Calico Acts | Two regiments per Army; one Company ship per sea zone. |",
"| 1813 | 5–8 | £10 expectations / 0 | £3 | Military Oversight, Deregulation (Debtor's Prison side), Calico Acts | Two regiments per Army; one Company ship per sea zone. |",
"| 1813 | 5–8 | £10 expectations / 0 | £3 | Military Oversight, Deregulation (Debtor's Prison side), Calico Acts | Two regiments per Army; one Company ship per sea zone. |",
'Military Oversight, Deregulation (Debtor\'s Prison side), Calico Acts',
"Deregulation (Debtor's Prison side)",
'Military Oversight, Deregulation (Debtor\'s Prison side), Calico Acts',
'Two regiments per Army; one Company ship per sea zone.',
'Two regiments per Army; one Company ship per sea zone.',
'put **+2/−2 share-value token** in Court',
'return the **Governor General law** to the box',
'place its office overlay over Director of Trade.',
'create China',
'place Bombay/Madras/Bengal control tokens in their Presidencies'],
'Q075':[
'**3/1 VP if final turn 1–3, 5/2 if turn 4–6, 8/4 if turn 7–8**',
'**3/1 VP if final turn 1–3, 5/2 if turn 4–6, 8/4 if turn 7–8**',
'**3/1 VP if final turn 1–3, 5/2 if turn 4–6, 8/4 if turn 7–8**',
'Most/second awards are **3/1 VP if final turn 1–3, 5/2 if turn 4–6, 8/4 if turn 7–8**. Tied first: only lower award to each tied player; no other award.',
'no other award.'],
'Q076':[
'Manufacturing 0 → Shipping 0 → Company shares 1 → Social 2.',
'Manufacturing 0 → Shipping 0 → Company shares 1 → Social 2.',
'Manufacturing 0 → Shipping 0 → Company shares 1 → Social 2.',
'Manufacturing 0 → Shipping 0 → Company shares 1 → Social 2.',
'**lined** Standing £4/6/8 or Debt 5/6/7/8 **PERMITS the PM to call** the special vote',
'**lined** Standing £4/6/8 or Debt 5/6/7/8 **PERMITS the PM to call** the special vote',
'**lined** Standing £4/6/8 or Debt 5/6/7/8 **PERMITS the PM to call** the special vote',
'**starred** Standing £4 or Debt 8 **REQUIRES the PM to call** it.',
'**starred** Standing £4 or Debt 8 **REQUIRES the PM to call** it.',
'**starred** Standing £4 or Debt 8 **REQUIRES the PM to call** it.',
'reset S is above £10.',
'**Initial Power positions, from lowest to highest:** Manufacturing 0 → Shipping 0 → Company shares 1 → Social 2. The two zero-Power spaces are distinct ordered positions; Manufacturing starts below Shipping.'],
'Q077':[
'Unrest adds neither to the primary attack nor to resulting tower levels',
'On a successful Foreign Invasion, close all orders in the target region once',
'if they are already all closed, Cascade instead'],
'Q078':[
'Mercantile/Diplomatic Connection reducing a check to zero dice means failure',
'reduce Balance by twice the highest roll (minimum zero)',
'and take cash from the bank equal to that actual Balance reduction',
'Public Demands Impeachment returns member to supply and office card to vacancies',
'Public Demands Impeachment returns member to supply and office card to vacancies',
'Military Oversight demotes one Commander to an officer',
'**the SAME former Commander remains eligible to become COMMANDER again**']}
reasons={
'Q060':'All eight requested limits, eligible-piece, cap, discount and Final Scoring facts are stated in the same-entry passage.',
'Q061':'All requested treasury destinations, authorized uses and family-cash prohibition are explicit across the included passages.',
'Q062':'The passage places investments after Family share creation and before Hiring and identifies both conflict decision makers.',
'Q063':'The ship passage gives both consent requirements, ship-type prohibitions, prices and payment destinations.',
'Q064':'The complete takeover procedure supplies the eligibility and majority consent conditions without requiring share ownership; its ships, money and shares move to the new charter and both cube positions continue while the former manager resets. Money clearly includes both firm treasuries; both cube positions are the Value and dividend positions.',
'Q065':'The merger passage states unanimity, highest Value and tie choice, owner consent for excess shares, and treasury/charter destinations.',
'Q066':'The Hobnob row and storm sentence explicitly cover every requested permission, prohibition and retained marker.',
'Q067':'The emergency clause applies the included normal investment restrictions, allows investment at the share cap, and states the expense use, lost remainder and Value reduction.',
'Q068':'The emergency-merger passage explicitly limits the rescue to one other firm and orders payment of both firms\' expenses.',
'Q069':'The voluntary-dissolution passage directly states full consent and the requested share, ship and workshop outcomes.',
'Q070':'The unconditional first Final Scoring step scores firms and prison before ordinary scoring; the included rate table supplies positive and negative share VP. It sums all firm fractions per player before one rounding and precedes both Company-outcome branches.',
'Q071':'The per-member heading and all five rows provide every requested cost, upkeep, VP and window value.',
'Q072':'The two setup tables give all four start/end ranges and each scenario\'s Deregulation status.',
'Q073':'The two scenario rows give all requested initial quantities, laws and destinations, including the Bengal token. The repeated regiment atom is preserved separately for the two scenarios.',
'Q074':'The 1813 row and following paragraph state all requested finances, laws, military, ships, share value and office/control changes.',
'Q075':'The Power paragraph gives all award pairs and states that each tied-first player receives only the lower award with no other award.',
'Q076':'The ordered Power list supplies the distinct zero-space order; the threshold sentence gives all lined/starred values and permissions. S above £10 identifies the printed £10-expectations space.',
'Q077':'The concrete conclusion and ruling passage explicitly exclude unrest from both quantities and close orders once, cascading only when all were already closed.',
'Q078':'The corrected-card paragraph explicitly supplies each requested zero-dice, capped Fraud, Impeachment and Commander-reappointment result.'}
grades=[]
for e in p['entries']:
    ident=e['id']
    atoms=e['requested_fact_scope_entry']['material_requested_facts']
    quotes=chosen[ident]
    assert len(atoms)==len(quotes), ident
    answer=e['reader_a_entry']['answer']
    parts=[]
    for atom,quote in zip(atoms,quotes):
        assert quote in answer, (ident,quote)
        support=[quote]
        if ident=='Q071':
            support=['Values below are per family member.','| Cost | Upkeep | VP | Windows |',quote]
        if ident=='Q067' and atom in ['Normal eligible Company share or uninvested workshop','Weak/lined Company-share restriction persists','Same-turn Company-share restriction persists even after transfer']:
            support.append('Emergency investments follow the Company-share/workshop eligibility rules under **Firms phase: investments**')
        parts.append({'requirement':atom,'status':'covered','reader_quotes':support})
    grades.append({'id':ident,'grade':'Correct','reason':reasons[ident],'material_parts':parts,'unsupported_guesses':[],'summary_issue_if_any':None})
assert len(grades)==19
out=base/'grades-same-entry.json'
out.write_text(json.dumps({'block_id':'block-04','readers':{'reader-a':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n')
b=out.read_bytes()
print(json.dumps({'path':str(out),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(b).hexdigest()}))