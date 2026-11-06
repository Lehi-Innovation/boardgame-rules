from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-03/grading-reader-b/block-04')
packet=json.loads((base/'packet.json').read_text())
def c(*quotes): return {'status':'covered','reader_quotes':list(quotes)}
decisions={
'Q060':('Correct','All eight requested retirement facts are stated in the same-entry special-retirement passage.',[
c('Each shareholder may make one additional retirement per London Season'),
c('from supply rather than Pensioners'),
c('irrespective of number of firms owned.'),
c('**Actual cash spent after spouse discounts** cannot exceed the **highest total dividend marker** of any firm they own a share in'),
c('No retirement from a firm whose marker is absent or zero.'),
c('the printed prize cost may exceed that marker when discounts cover the difference.'),
c('At start of Final Scoring, score firms then allow one special retirement'),
c('allow one special retirement regardless of Company success/failure')]),
'Q061':('Correct','The same entry identifies both receipts and permitted payments, including expenses from either treasury and India-only dividends.',[
c('**London** receives the bank\'s £5 per investment'),
c('**India** receives trade and pays dividends/expenses.'),
c('**London** receives the bank\'s £5 per investment and pays for ship acquisition, trade bids and expenses'),
c('**London** receives the bank\'s £5 per investment and pays for ship acquisition, trade bids and expenses'),
c('can use either/both treasuries.'),
c('After expenses, manager may pay dividends **from India treasury only**.'),
c('**Family cash cannot be transferred into or out of firm treasuries.**')]),
'Q062':('Correct','The phase follows Family share creation and precedes Hiring; the manager and PM jurisdictions are explicit.',[
c('After Family share creation, before Hiring'),
c('before Hiring'),
c('Manager resolves timing conflicts within firm'),
c('PM resolves conflicts between firms.')]),
'Q063':('Correct','All ship eligibility, consent, prices and treasury/payment destinations are explicit.',[
c("**must have that shipyard owner's consent**"),
c("Pay **£3 FROM the firm's London treasury TO the BANK**."),
c('Firms cannot acquire Company or extra ships.'),
c('Firms cannot acquire Company or extra ships.'),
c("May buy player-owned ship already in Company with owner's consent"),
c('unfatigued £3'),
c('fatigued £2'),
c("paid **from the firm's London treasury into Shipping treasury**")]),
'Q064':('Correct','The complete takeover rule gives non-manager eligibility and majority consent without requiring the initiator to own shares. Ships, all money and shares move; both cube positions persist and the former board/cubes reset.',[
c('Only a player who **manages NO firm at all** may initiate one; managing a different firm also makes you ineligible.'),
c("Obtain consent of holders of a majority of the target's shares"),
c("Only a player who **manages NO firm at all** may initiate one; managing a different firm also makes you ineligible. Obtain consent of holders of a majority of the target's shares"),
c("move firm's ships, money and shares to own charter"),
c("move firm's ships, money and shares to own charter"),
c("move firm's ships, money and shares to own charter"),
c('copy both cube positions'),
c('copy both cube positions'),
c('former manager returns cubes'),
c('flips board to family side.')]),
'Q065':('Correct','The merger passage resolves unanimity, primary/tied-primary selection, excess-share consent and both secondary treasury/charter outcomes.',[
c("Managers negotiate with **every shareholder's consent**."),
c('Highest-value firm is primary'),
c('if tied, players choose among tied.'),
c("**If the primary would exceed ten shares, RETURN the excess shares to their OWNERS' SUPPLIES, with those owners' consent.**"),
c('Transfer all secondary shares, ships and treasury funds to primary'),
c('secondary boards return to family sides.')]),
'Q066':('Correct','The Hobnob row and storm passage supply all six requested facts.',[
c('No bid, trade or dividends.'),
c('No bid, trade or dividends.'),
c('No bid, trade or dividends.'),
c('Still pay expenses'),
c('retain previous dividend marker for retirement.'),
c('Firm ships face storms in strategy zone; Hobnob exempts them.')]),
'Q067':('Correct','Emergency rescue expressly uses the normal contribution restrictions, including lined spaces and transferred same-turn shares, remains available at the cap, pays expenses and loses surplus while reducing Value per investment.',[
c('Emergency investments follow the Company-share/workshop eligibility rules under **Firms phase: investments**, even when ten-share cap prevents more shares'),
c('Up to ten firm shares; further investments still contribute £5 but create no shares.'),
c('return one eligible Company share to supply or flip workshop to invested side.',"same Company-share/workshop contribution creates one firm share and £5 bank to London.",'Invested workshops never return to uninvested'),
c('Cannot use Company shares at all when Standing and/or Debt on lined space.','Emergency investments follow the Company-share/workshop eligibility rules under **Firms phase: investments**'),
c('Cannot use shares created this turn, even after trading them away.','Emergency investments follow the Company-share/workshop eligibility rules under **Firms phase: investments**'),
c('pay expenses, lose any remaining cash, lower Value one space per emergency investment.'),
c('lose any remaining cash'),
c('lower Value one space per emergency investment.')]),
'Q068':('Correct','The emergency merger passage states the one-other-firm limit and the required order for paying both firms\' expenses.',[
c('**emergency negotiated merger with only ONE other firm**'),
c('The other firm must first pay its own expenses if not already paid'),
c("then cover the endangered firm's unpaid expenses.")]),
'Q069':('Correct','The voluntary dissolution passage supplies unanimous consent, both destinations and permanently invested workshops.',[
c('**Voluntary dissolution:** All shareholders must consent.'),
c("shares go to Debtor's Prison (each −1 VP)"),
c('ships return to their matching shipyards'),
c('Workshops remain invested for the rest of the game.')]),
'Q070':('Correct','The first Final Scoring row applies before the outcome branch, sums all firm points before rounding once and deducts each prison piece. The same entry gives the Value-to-VP rates, including negative and fractional values.',[
c('1. Firms, if deregulated | **BEFORE ordinary Power/Court/final-outcome scoring**'),
c('Firm-track VP per share: Value 1 = −1 VP; 2 = 0; 3–4 = ½; 5–7 = 1; 8–9 = 1½; 10 = 2.'),
c("Deduct **1 VP per own family piece in Debtor's Prison**."),
c("for each player separately add VP from all their shares across all their firms, then **round that player's total DOWN once**."),
c('1. Firms, if deregulated | **BEFORE ordinary Power/Court/final-outcome scoring**','5. Final retirements OR failure card | Resolve the appropriate Company outcome below.')]),
'Q071':('Correct','Every requested table cell is present with the explicit per-family-member basis.',[
c('Values below are per family member.','| £2 | £0 | 0 | 0 |'),
c('Values below are per family member.','| £2 | £0 | 0 | 0 |'),
c('Values below are per family member.','| £2 | £0 | 0 | 0 |'),
c('Values below are per family member.','| £2 | £0 | 0 | 0 |'),
c('Values below are per family member.','| £4 | £1 | 2 | 1 |'),
c('Values below are per family member.','| £4 | £1 | 2 | 1 |'),
c('Values below are per family member.','| £4 | £1 | 2 | 1 |'),
c('Values below are per family member.','| £4 | £1 | 2 | 1 |'),
c('Values below are per family member.','| £8 | £2 | 4 | 2 |'),
c('Values below are per family member.','| £8 | £2 | 4 | 2 |'),
c('Values below are per family member.','| £8 | £2 | 4 | 2 |'),
c('Values below are per family member.','| £8 | £2 | 4 | 2 |'),
c('Values below are per family member.','| £14 | £3 | 8 | 3 |'),
c('Values below are per family member.','| £14 | £3 | 8 | 3 |'),
c('Values below are per family member.','| £14 | £3 | 8 | 3 |'),
c('Values below are per family member.','| £14 | £3 | 8 | 3 |'),
c('Values below are per family member.','| £20 | £4 | 12 | 4 |'),
c('Values below are per family member.','| £20 | £4 | 12 | 4 |'),
c('Values below are per family member.','| £20 | £4 | 12 | 4 |'),
c('Values below are per family member.','| £20 | £4 | 12 | 4 |')]),
'Q072':('Correct','All four scenario ranges and their deregulation statuses are stated in the same setup section.',[
c('| 1710 | 1–5 |'),
c('Company monopoly, without deregulation procedures.'),
c('| 1758 | 3–7 |'),
c('Company starts with monopoly; deregulation can be voted in.'),
c('| 1813 | 5–8 |'),
c('Starts deregulated, allowing firms'),
c('| Long 1710 | 1–8 |'),
c('Same initial position as 1710, with deregulation available')]),
'Q073':('Correct','Both scenario rows provide every requested setup value, with the 1758 eastern ship and Bengal control-token location.',[
c('| 1710 | 1–5 | £10 expectations / 0 |'),
c('| 1710 | 1–5 | £10 expectations / 0 |'),
c('| 1710 | 1–5 | £10 expectations / 0 | £3 |'),
c('| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection |'),
c('| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |'),
c('no Company ships.'),
c('| 1758 | 3–7 | £12 expectations / 3 |'),
c('| 1758 | 3–7 | £12 expectations / 3 |'),
c('| 1758 | 3–7 | £12 expectations / 3 | £4 |'),
c('| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts |'),
c('| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts | One regiment per Army;'),
c('one Company ship in East Indian.'),
c('Bengal control token in Bengal Presidency.')]),
'Q074':('Correct','The 1813 table and following paragraph cover all thirteen requested finance, law, military, token and office changes.',[
c('| 1813 | 5–8 | £10 expectations / 0 |'),
c('| 1813 | 5–8 | £10 expectations / 0 |'),
c('| 1813 | 5–8 | £10 expectations / 0 | £3 |'),
c('Military Oversight, Deregulation'),
c("Deregulation (Debtor's Prison side)"),
c("Military Oversight, Deregulation (Debtor's Prison side), Calico Acts"),
c('Two regiments per Army'),
c('one Company ship per sea zone.'),
c('put **+2/−2 share-value token** in Court'),
c('return the **Governor General law** to the box'),
c('place its office overlay over Director of Trade. Use Governor General instead of Director and no Governors.'),
c('create China'),
c('place Bombay/Madras/Bengal control tokens in their Presidencies')]),
'Q075':('Correct','All three award pairs and the lower-award-only treatment of each tied-first player are explicit.',[
c('3/1 VP if final turn 1–3'),
c('5/2 if turn 4–6'),
c('8/4 if turn 7–8'),
c('Most/second awards are **3/1 VP if final turn 1–3, 5/2 if turn 4–6, 8/4 if turn 7–8**. Tied first: only lower award to each tied player'),
c('no other award.')]),
'Q076':('Correct','The setup paragraph gives every initial Power rate and their ordered zero spaces, the permissive/mandatory thresholds and the S location above the printed £10 expectations.',[
c('Social 2.'),
c('Company shares 1'),
c('Shipping 0'),
c('Manufacturing 0'),
c('**lined** Standing £4/6/8'),
c('Debt 5/6/7/8'),
c('**PERMITS the PM to call** the special vote'),
c('**starred** Standing £4'),
c('**starred** Standing £4 or Debt 8'),
c('**REQUIRES the PM to call** it.'),
c('reset S is above £10.'),
c('**Initial Power positions, from lowest to highest:** Manufacturing 0 → Shipping 0 → Company shares 1 → Social 2. The two zero-Power spaces are distinct ordered positions; Manufacturing starts below Shipping.')]),
'Q077':('Correct','The Foreign Invasion ruling explicitly excludes unrest from both quantities and limits order closure to once, with Cascade only when all were already closed.',[
c("unrest does **not** add to a Foreign Invasion's primary attack strength or determine its resulting tower levels."),
c('**On a successful Foreign Invasion, close all orders in the target region once; if they are already all closed, Cascade instead.**'),
c('if they are already all closed, Cascade instead.')]),
'Q078':('Correct','All four corrected-card cases are covered, including both Fraud caps, both Impeachment destinations and eligibility of the demoted Commander for reappointment.',[
c('Mercantile/Diplomatic Connection reducing a check to zero dice means failure'),
c('reduce Balance by twice the highest roll (minimum zero)'),
c('take cash from the bank equal to that actual Balance reduction'),
c('Public Demands Impeachment returns member to supply'),
c('office card to vacancies'),
c('Military Oversight demotes one Commander to an officer'),
c('**the SAME former Commander remains eligible to become COMMANDER again**')])
}
grades=[]
assert list(decisions)==[e['id'] for e in packet['entries']]
for e in packet['entries']:
 grade,reason,parts=decisions[e['id']]
 facts=e['requested_fact_scope_entry']['material_requested_facts']
 assert len(parts)==len(facts),(e['id'],len(parts),len(facts))
 material=[]
 for requirement,part in zip(facts,parts):
  for quote in part['reader_quotes']:
   assert quote and quote in e['reader_b_entry']['answer'],(e['id'],quote)
  material.append({'requirement':requirement,**part})
 grades.append({'id':e['id'],'grade':grade,'reason':reason,'material_parts':material,'unsupported_guesses':[],'summary_issue_if_any':None})
output=base/'grades-same-entry.json'
output.write_text(json.dumps({'block_id':'block-04','readers':{'reader-b':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(output),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(output.read_bytes()).hexdigest()}))