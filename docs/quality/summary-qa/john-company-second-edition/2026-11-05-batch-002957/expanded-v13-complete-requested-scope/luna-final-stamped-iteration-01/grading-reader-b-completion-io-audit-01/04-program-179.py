from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-final-stamped-iteration-01/grading-reader-b/block-04')
p=json.loads((base/'packet.json').read_text())
q={}
q['Q060']=[
'Each shareholder may make one additional retirement per London Season from supply rather than Pensioners, irrespective of number of firms owned.',
'Each shareholder may make one additional retirement per London Season from supply rather than Pensioners, irrespective of number of firms owned.',
'irrespective of number of firms owned.',
'**Actual cash spent after spouse discounts** cannot exceed the **highest total dividend marker** of any firm they own a share in;',
'No retirement from a firm whose marker is absent or zero.',
'Spouse discounts can allow a higher printed-cost prize;',
'At start of Final Scoring, score firms then allow one special retirement regardless of Company success/failure, before normal final-scoring steps;',
'At start of Final Scoring, score firms then allow one special retirement regardless of Company success/failure, before normal final-scoring steps;']
q['Q061']=[
'**Investment cash always comes FROM the BANK TO London.',
'Place filled tokens; revenue goes to India treasury.',
"Pay **£3 FROM the firm's London treasury TO the BANK**.",
'Commit a secret cash bid from London treasury.',
'can use either/both treasuries.',
'After expenses, manager may pay dividends **from India treasury only**.',
'**Family cash cannot be transferred into or out of firm treasuries.**']
q['Q062']=['After Family share creation, before Hiring, take investments actions without set order until nobody wishes more.','After Family share creation, before Hiring, take investments actions without set order until nobody wishes more.','Manager resolves timing conflicts within firm;','PM resolves conflicts between firms.']
q['Q063']=[
"**must have that shipyard owner's consent**.",
"Pay **£3 FROM the firm's London treasury TO the BANK**.",
'Firms cannot acquire Company or extra ships.',
'Firms cannot acquire Company or extra ships.',
"May buy player-owned ship already in Company with owner's consent:",
'unfatigued £3, fatigued £2',
'unfatigued £3, fatigued £2',
"paid **from the firm's London treasury into Shipping treasury**."]
takeover="Only a player who **manages NO firm at all** may initiate one; managing a different firm also makes you ineligible. Obtain consent of holders of a majority of the target's shares, then move firm's ships, money and shares to own charter, copy both cube positions; former manager returns cubes and flips board to family side."
q['Q064']=[takeover]*10
merger="Managers negotiate with **every shareholder's consent**. Highest-value firm is primary; if tied, players choose among tied. Transfer all secondary shares, ships and treasury funds to primary; secondary boards return to family sides. Players may negotiate share transfers. **If the primary would exceed ten shares, RETURN the excess shares to their OWNERS' SUPPLIES, with those owners' consent.**"
q['Q065']=[merger]*6
hob='| Hobnob | No bid, trade or dividends. Still pay expenses; retain previous dividend marker for retirement. |'
q['Q066']=[hob]*5+['Firm ships face storms in strategy zone; Hobnob exempts them.']
q['Q067']=[
'Yes. At ten shares, an eligible emergency investment can still be made but adds no share;',
'Yes. At ten shares, an eligible emergency investment can still be made but adds no share;',
"return one eligible Company share to supply or flip workshop to invested side.",
'Cannot use Company shares at all when Standing and/or Debt on lined space.',
'Cannot use shares created this turn, even after trading them away.',
'pay expenses, lose any remaining cash, lower Value one space per emergency investment.',
'pay expenses, lose any remaining cash, lower Value one space per emergency investment.',
'pay expenses, lose any remaining cash, lower Value one space per emergency investment.']
q['Q068']=['**emergency negotiated merger with only ONE other firm**.',"The other firm must first pay its own expenses if not already paid, then cover the endangered firm's unpaid expenses.","The other firm must first pay its own expenses if not already paid, then cover the endangered firm's unpaid expenses."]
q['Q069']=['**Voluntary dissolution:** All shareholders must consent.',"shares go to Debtor's Prison (each −1 VP)",'ships return to their matching shipyards','Workshops remain invested for the rest of the game.']
firmrow="| 1. Firms, if deregulated | **BEFORE ordinary Power/Court/final-outcome scoring**, for each player separately add VP from all their shares across all their firms, then **round that player's total DOWN once**. Deduct **1 VP per own family piece in Debtor's Prison**. **The next row (step2) describes the ONE eligible special firm retirement per shareholder, even on Company failure; ordinary scoring begins at step3.** |"
q['Q070']=[firmrow,'Firm-track VP per share: Value 1 = −1 VP; 2 = 0; 3–4 = ½; 5–7 = 1; 8–9 = 1½; 10 = 2.',"Deduct **1 VP per own family piece in Debtor's Prison**.",firmrow,firmrow]
q['Q071']=[]
for row in ['| £2 | £0 | 0 | 0 |','| £4 | £1 | 2 | 1 |','| £8 | £2 | 4 | 2 |','| £14 | £3 | 8 | 3 |','| £20 | £4 | 12 | 4 |']:
 q['Q071'].extend([row]*4)
q['Q072']=[
'| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |',
'| 1710 | Recommended first game; Company monopoly, without deregulation procedures. |',
'| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts | One regiment per Army; one Company ship in East Indian. Bengal control token in Bengal Presidency. |',
'| 1758 | Company starts with monopoly; deregulation can be voted in. |',
"| 1813 | 5–8 | £10 expectations / 0 | £3 | Military Oversight, Deregulation (Debtor's Prison side), Calico Acts | Two regiments per Army; one Company ship per sea zone. |",
'| 1813 | Starts deregulated, allowing firms; recommended with five or six players. |',
'| Long 1710 | 1–8 | Same as 1710 | £3 | Royal Protection; Deregulation available separately | Same as 1710. |',
'| Long 1710 | Same initial position as 1710, with deregulation available; can run eight turns, often twice the normal length. |']
r1710=q['Q072'][0]; r1758=q['Q072'][2]; r1813=q['Q072'][4]
q['Q073']=[r1710]*6+[r1758]*7
setup="In 1813, put **+2/−2 share-value token** in Court, create China, place Bombay/Madras/Bengal control tokens in their Presidencies, return the **Governor General law** to the box and place its office overlay over Director of Trade."
q['Q074']=[r1813]*8+[setup]*5
power='Most/second awards are **3/1 VP if final turn 1–3, 5/2 if turn 4–6, 8/4 if turn 7–8**. Tied first: only lower award to each tied player; no other award.'
q['Q075']=[power]*5
initial='**Initial Power positions, from lowest to highest:** Manufacturing 0 → Shipping 0 → Company shares 1 → Social 2. The two zero-Power spaces are distinct ordered positions; Manufacturing starts below Shipping.'
lined='For Deregulation, **lined** Standing £4/6/8 or Debt 5/6/7/8 **PERMITS the PM to call** the special vote; **starred** Standing £4 or Debt 8 **REQUIRES the PM to call** it.'
q['Q076']=[initial]*4+[lined]*6+['reset S is above £10.',initial]
q['Q077']=["unrest does **not** add to a Foreign Invasion's primary attack strength or determine its resulting tower levels.",'**On a successful Foreign Invasion, close all orders in the target region once; if they are already all closed, Cascade instead.**','**On a successful Foreign Invasion, close all orders in the target region once; if they are already all closed, Cascade instead.**']
q['Q078']=['Mercantile/Diplomatic Connection reducing a check to zero dice means failure;','reduce Balance by twice the highest roll (minimum zero)', 'take cash from the bank equal to that actual Balance reduction;', 'Public Demands Impeachment returns member to supply and office card to vacancies;', 'Public Demands Impeachment returns member to supply and office card to vacancies;', 'Military Oversight demotes one Commander to an officer,', '**the SAME former Commander remains eligible to become COMMANDER again**']
reasons={
'Q060':'All limits, supply-piece eligibility, actual-spend cap, discounts, zero-marker restriction and final timing are resolved.',
'Q061':'All treasury destinations, permitted payment accounts and the family-cash restriction are covered.',
'Q062':'The phase follows Family share creation and precedes Hiring; both conflict authorities are explicit.',
'Q063':'Consent, ship prohibitions, both prices and both payment destinations are explicit.',
'Q064':'The complete takeover procedure covers eligibility and majority consent without imposing share ownership, transfers all money/assets and preserves both cube positions while resetting the former manager.',
'Q065':'All shareholder consent, primary selection and ties, excess-share consent and secondary treasury/charter outcomes are covered.',
'Q066':'The Hobnob row and storm rule resolve all six requested facts.',
'Q067':'The concrete cap conclusion and same-entry normal investment restrictions together cover emergency eligibility, resources, persistent restrictions, expense payment, lost remainder and Value loss.',
'Q068':'One-other-firm limit and the order and responsibility for both expense bills are explicit.',
'Q069':'Unanimous consent and every requested destination and workshop status are explicit.',
'Q070':'The ordered scoring table applies firm scoring before either Company-outcome branch, with per-share rates, prison penalty and rounding each player total once.',
'Q071':'The table provides every requested cell and explicitly states values are per family member.',
'Q072':'All four turn ranges and Deregulation statuses are explicit.',
'Q073':'Both scenario rows supply all requested initial values and the Bengal control-token destination.',
'Q074':'The 1813 row and setup paragraph supply all requested finance, laws, pieces, share value and office changes.',
'Q075':'All three award pairs and lower-only tied-first awards are explicit.',
'Q076':'All rates, distinct zero-space ordering, thresholds, permission/requirement and S location are covered; lowest-to-highest ordering conveys the requested relative track positions.',
'Q077':'The FAQ explicitly excludes unrest from both quantities and specifies a single closure or Cascade if already closed.',
'Q078':'The corrected-card paragraph resolves zero-dice failure, capped Balance and payout, impeachment destinations and former Commander eligibility.'}
grades=[]
for e in p['entries']:
 i=e['id']; atoms=e['requested_fact_scope_entry']['material_requested_facts']; quotes=q[i]
 assert len(atoms)==len(quotes),(i,len(atoms),len(quotes))
 a=e['reader_b_entry']['answer']
 assert all(x and x in a for x in quotes),i
 parts=[]
 for atom,quote in zip(atoms,quotes):
  supporting=[quote]
  if i=='Q071': supporting.insert(0,'Values below are per family member.')
  parts.append({'requirement':atom,'status':'covered','reader_quotes':supporting})
 grades.append({'id':i,'grade':'Correct','reason':reasons[i],'material_parts':parts,'unsupported_guesses':[],'summary_issue_if_any':None})
out=base/'grades-same-entry.json'
s=json.dumps({'block_id':'block-04','readers':{'reader-b':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n'
out.write_text(s)
print(json.dumps({'path':str(out),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(s.encode()).hexdigest()}))