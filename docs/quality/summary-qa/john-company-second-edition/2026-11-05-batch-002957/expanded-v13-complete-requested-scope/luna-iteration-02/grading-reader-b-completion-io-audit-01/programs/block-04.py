from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-02/grading-reader-b/block-04')
p=json.loads((base/'packet.json').read_text())
# Quotes and statuses below are the grader's individual semantic judgments.
choices={}
def choose(id,quotes,grade='Correct',omitted=(),reason=None,issue=None):
 choices[id]={'quotes':quotes,'grade':grade,'omitted':set(omitted),'reason':reason,'issue':issue}
special="Each shareholder may make one additional retirement per London Season from supply rather than Pensioners, irrespective of number of firms owned."
cap="**Actual cash spent after spouse discounts** cannot exceed the **highest total dividend marker** of any firm they own a share in; the printed prize cost may exceed that marker when discounts cover the difference."
final="At start of Final Scoring, score firms then allow one special retirement regardless of Company success/failure, before normal final-scoring steps; no display cards in Final Scoring."
choose('Q060',[special,special,special,cap,"No retirement from a firm whose marker is absent or zero.",cap,final,final])
choose('Q061',["**Investment cash always comes FROM the BANK TO London.","**India** receives trade and pays dividends/expenses.","Pay **£3 FROM the firm's London treasury TO the BANK**.","Commit a secret cash bid from London treasury.","can use either/both treasuries.","After expenses, manager may pay dividends **from India treasury only**.","**Family cash cannot be transferred into or out of firm treasuries.**"])
phase="After Family share creation, before Hiring, take investments actions without set order until nobody wishes more."
choose('Q062',[phase,phase,"Manager resolves timing conflicts within firm; PM resolves conflicts between firms.","Manager resolves timing conflicts within firm; PM resolves conflicts between firms."])
shipconsent="A firm may fit a ship from **its own OR ANOTHER PLAYER'S shipyard**, but **must have that shipyard owner's consent**."
shipbuy="May buy player-owned ship already in Company with owner's consent: unfatigued £3, fatigued £2, paid **from the firm's London treasury into Shipping treasury**."
choose('Q063',[shipconsent,"Pay **£3 FROM the firm's London treasury TO the BANK**.","Firms cannot acquire Company or extra ships.","Firms cannot acquire Company or extra ships.",shipbuy,shipbuy,shipbuy,shipbuy])
takeover="Only a player who **manages NO firm at all** may initiate one; managing a different firm also makes you ineligible. Obtain consent of holders of a majority of the target's shares, then move firm's ships, money and shares to own charter, copy both cube positions; former manager returns cubes and flips board to family side."
choose('Q064',[takeover,takeover,takeover,takeover,takeover,takeover,takeover,takeover,takeover,takeover],reason="All requested takeover facts are resolved by the complete takeover passage. Its eligibility and consent requirements apply to any player managing no firm; it does not require the initiator to hold a share. Moving the firm's money covers both treasuries, and copying both cubes preserves Value and dividend positions.")
merge="Managers negotiate with **every shareholder's consent**. Highest-value firm is primary; if tied, players choose among tied."
choose('Q065',[merge,merge,merge,"**If the primary would exceed ten shares, RETURN the excess shares to their OWNERS' SUPPLIES, with those owners' consent.**","Transfer all secondary shares, ships and treasury funds to primary; secondary boards return to family sides.","Transfer all secondary shares, ships and treasury funds to primary; secondary boards return to family sides."])
hob="| Hobnob | No bid, trade or dividends. Still pay expenses; retain previous dividend marker for retirement. |"
choose('Q066',[hob,hob,hob,hob,hob,"Firm ships face storms in strategy zone; Hobnob exempts them."])
rescue="Emergency investments follow the Company-share/workshop eligibility rules under **Firms phase: investments**, even when ten-share cap prevents more shares: pay expenses, lose any remaining cash, lower Value one space per emergency investment."
choose('Q067',[rescue,rescue,None,None,None,rescue,rescue,rescue],grade='Partial',omitted=(2,3,4),reason="The same-entry rescue passage confirms investment at the ten-share cap without new shares, expense payment, loss of remaining cash and Value loss. It refers to normal eligibility rules but does not state the uninvested-workshop condition, lined-space Company-share prohibition, or prohibition on same-turn Company shares even after transfer. These are reader omissions; the full summary supplies them in Firms phase: investments (lines 374-375).",issue={'classification':'reader_error','summary_location':'Firms phase: investments, lines 374-375; Firm expenses, rescue and dividends, line 404','controlling_summary_quotes':["return one eligible Company share to supply or flip workshop to invested side.","Cannot use Company shares at all when Standing and/or Debt on lined space. Cannot use shares created this turn, even after trading them away. Invested workshops never return to uninvested: no bonus or Company-failure VP; they remain invested even if firm fails.",rescue],'actual_missing_facts':['Uninvested workshop condition is not resolved in this entry.','Company-share restriction on lined Standing/Debt is not stated.','Same-turn Company-share restriction, including after transfer, is not stated.'],'summary_gap_or_ambiguity':False})
choose('Q068',["**emergency negotiated merger with only ONE other firm**","The other firm must first pay its own expenses if not already paid, then cover the endangered firm's unpaid expenses.","The other firm must first pay its own expenses if not already paid, then cover the endangered firm's unpaid expenses."])
choose('Q069',["**Voluntary dissolution:** All shareholders must consent.","shares go to Debtor's Prison (each −1 VP)","ships return to their matching shipyards","Workshops remain invested for the rest of the game."])
firmfirst="| 1. Firms, if deregulated | **BEFORE ordinary Power/Court/final-outcome scoring**, for each player separately add VP from all their shares across all their firms, then **round that player's total DOWN once**. Deduct **1 VP per own family piece in Debtor's Prison**. **The next row (step2) describes the ONE eligible special firm retirement per shareholder, even on Company failure; ordinary scoring begins at step3.** |"
firmvalues="Firm-track VP per share: Value 1 = −1 VP; 2 = 0; 3–4 = ½; 5–7 = 1; 8–9 = 1½; 10 = 2."
choose('Q070',[firmfirst,firmvalues,firmfirst,firmfirst,firmfirst],reason="All requested facts are resolved in the scoring attachment: firm scoring is step 1, before outcome-dependent scoring, with Value-based positive/negative VP and per-player total rounding. The ordered scoring procedure applies to either Company outcome.")
prizes=["| £2 | £0 | 0 | 0 |","| £4 | £1 | 2 | 1 |","| £8 | £2 | 4 | 2 |","| £14 | £3 | 8 | 3 |","| £20 | £4 | 12 | 4 |"]
choose('Q071',[["Values below are per family member.",row] for row in prizes for _ in range(4)])
row1710="| 1710 | 1–5 | £10 expectations / 0 | £3 | Royal Protection | One regiment per Army; no Company ships. |"
row1758="| 1758 | 3–7 | £12 expectations / 3 | £4 | Calico Acts | One regiment per Army; one Company ship in East Indian. Bengal control token in Bengal Presidency. |"
row1813="| 1813 | 5–8 | £10 expectations / 0 | £3 | Military Oversight, Deregulation (Debtor's Prison side), Calico Acts | Two regiments per Army; one Company ship per sea zone. |"
rowlong="| Long 1710 | 1–8 | Same as 1710 | £3 | Royal Protection; Deregulation available separately | Same as 1710. |"
choose('Q072',[row1710,"| 1710 | Recommended first game; Company monopoly, without deregulation procedures. |",row1758,"| 1758 | Company starts with monopoly; deregulation can be voted in. |",row1813,"| 1813 | Starts deregulated, allowing firms; recommended with five or six players. |",rowlong,rowlong])
choose('Q073',[row1710,row1710,row1710,row1710,row1710,row1710,row1758,row1758,row1758,row1758,row1758,row1758,row1758])
setup1813="In 1813, put **+2/−2 share-value token** in Court, create China, place Bombay/Madras/Bengal control tokens in their Presidencies, return the **Governor General law** to the box and place its office overlay over Director of Trade."
choose('Q074',[row1813,row1813,row1813,row1813,row1813,row1813,row1813,row1813,setup1813,setup1813,setup1813,setup1813,setup1813])
powerawards="Most/second awards are **3/1 VP if final turn 1–3, 5/2 if turn 4–6, 8/4 if turn 7–8**."
tie="Tied first: only lower award to each tied player; no other award."
choose('Q075',[powerawards,powerawards,powerawards,[powerawards,tie],tie])
powerstart="**Initial Power positions, from lowest to highest:** Manufacturing 0 → Shipping 0 → Company shares 1 → Social 2. The two zero-Power spaces are distinct ordered positions; Manufacturing starts below Shipping. Standing expectations run £4/6/8/10/12/14/16; reset S is above £10. For Deregulation, **lined** Standing £4/6/8 or Debt 5/6/7/8 **PERMITS the PM to call** the special vote; **starred** Standing £4 or Debt 8 **REQUIRES the PM to call** it."
choose('Q076',[None]*12,grade='Partial',omitted=tuple(range(12)),reason="The attached Turn Structure passage supplies only phase order and special-vote timing. It omits every requested Power starting position, ordered zero-Power placement, lined/starred Standing and Debt threshold, permission/requirement distinction and S location. This is a reader selection error: the full summary provides all of these in Setup, line 61.",issue={'classification':'reader_error','summary_location':'Setup, line 61','controlling_summary_quotes':[powerstart],'actual_missing_facts':['Social 2, Company shares 1, Shipping 0, Manufacturing 0 and ordered Manufacturing/Shipping positions.','Lined Standing £4/£6/£8 and Debt 5–8 permit a vote; starred Standing £4 or Debt 8 require it.','S is at £10 expectations.'],'summary_gap_or_ambiguity':False})
foreign="unrest does **not** add to a Foreign Invasion's primary attack strength or determine its resulting tower levels."
close="**On a successful Foreign Invasion, close all orders in the target region once; if they are already all closed, Cascade instead.**"
choose('Q077',[foreign,close,close])
choose('Q078',["Mercantile/Diplomatic Connection reducing a check to zero dice means failure","reduce Balance by twice the highest roll (minimum zero)","take cash from the bank equal to that actual Balance reduction","Public Demands Impeachment returns member to supply and office card to vacancies","Public Demands Impeachment returns member to supply and office card to vacancies","Military Oversight demotes one Commander to an officer","**the SAME former Commander remains eligible to become COMMANDER again**"])
grades=[]
for entry in p['entries']:
 id=entry['id']; c=choices[id]; reqs=entry['requested_fact_scope_entry']['material_requested_facts']
 assert len(c['quotes'])==len(reqs),(id,len(c['quotes']),len(reqs))
 reader=entry['reader_b_entry']; substantive=[reader.get('answer','')]
 substantive += [x.get('fact','') for x in reader.get('clause_ledger',[])]
 substantive += [x for x in reader.get('case_conclusions',[]) if isinstance(x,str)]
 substantive += [x.get('quote','') for x in reader.get('evidence',[])]
 parts=[]
 for i,(req,q) in enumerate(zip(reqs,c['quotes'])):
  quotes=[] if q is None else q if isinstance(q,list) else [q]
  for quote in quotes: assert any(quote in text for text in substantive),(id,quote)
  parts.append({'requirement':req,'status':'omitted' if i in c['omitted'] else 'covered','reader_quotes':quotes})
 grades.append({'id':id,'grade':c['grade'],'reason':c['reason'] or 'All exact requested facts are correctly resolved and supported by the complete same-entry applicable summary text; no material contradiction or unsupported guess.','material_parts':parts,'unsupported_guesses':[],'summary_issue_if_any':c['issue']})
assert len(grades)==19
out={'block_id':'block-04','readers':{'reader-b':{'grades':grades}}}
path=base/'grades-same-entry.json'
blob=json.dumps(out,ensure_ascii=False,indent=2)+'\n'
path.write_text(blob)
print(json.dumps({'path':str(path),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(blob.encode()).hexdigest()}))