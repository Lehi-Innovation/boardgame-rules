from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-01/grading-reader-a/block-06')
packet=json.loads((base/'packet.json').read_text())
choices=[
('Q098','Correct','The complete same-entry Deploy passage covers surviving participating officers, all payout amounts and order, bank shares per used piece, stopping and repetition.',[
["Count only this attempt's surviving participating officers and used regiments/alliances."],
['Commander family first | £1 for Commander **plus £1 for each of their used surviving officers**.'],
['Other families clockwise | £1 per used surviving officer of that family.'],
['Pay in this order, stopping when cash runs out'],
['Bank last | £1 per used regiment and per used local-alliance **piece**, regardless of strength.'],
['Bank last | £1 per used regiment and per used local-alliance **piece**, regardless of strength.'],
['Repeat that entire cycle from the Commander until all loot is distributed.']]),
('Q099','Correct','The conquest passage moves the outward-facing Elephant fully inside the conquered region and states that it now threatens Rebellion; in this Company-conquest context the target is the Company.',[
['If the Elephant faced outward from the conquered region, move it fully inside that region after the conquest.'],
['If it faced outward from the conquered region, move it **fully inside that region**, now threatening Rebellion.']]),
('Q100','Correct','The entry supplies the full £1 expense census, Army qualification, Commander exclusion and China inclusion.',[
['Expenses are £1 for each existing Debt, each officer or regiment in an Army, and each ship in a sea zone, including China.'],
['Expenses are £1 for each existing Debt, each officer or regiment in an Army, and each ship in a sea zone, including China.'],
['Expenses are £1 for each existing Debt, each officer or regiment in an Army, and each ship in a sea zone, including China.'],
['Exclude Commanders.'],
['Expenses are £1 for each existing Debt, each officer or regiment in an Army, and each ship in a sea zone, including China.'],
['Yes. Ships in sea zones, including China, each cost £1.']]),
('Q101','Correct','The complete dividend passage supplies waiver scope and manager consent, the actual-total marker and track, and the India-to-London sweep.',[
['With that consent, the shareholder may forgo payment for any number of shares on any dividend.'],
["Waiving a dividend requires BOTH the shareholder's choice and the MANAGER'S CONSENT"],
['Record **total actual cash paid out**, not per-share dividend, with dividend cube on Company Balance track.'],
['Record **total actual cash paid out**, not per-share dividend, with dividend cube on Company Balance track.'],
['Sweep remaining India money into London.']]),
('Q102','Correct','The entry explicitly states the game-over blackmail ban and the exception for explicit card permission.',[
['Once the game is over, players stop playing blackmail cards, except when a card explicitly permits final-scoring use.'],
['unless a card explicitly permits final-scoring use.']]),
('Q103','Correct','The Director section supplies its treasury cash, £1-per-die/no-penalty Envoy procedure and every requested transfer limit and destination.',[
['### Director of Trade (p18)', 'May make repeated Special Envoy checks: £1 treasury cash per die, no penalty.'],
['May make repeated Special Envoy checks: £1 treasury cash per die, no penalty.'],
['May make repeated Special Envoy checks: £1 treasury cash per die, no penalty.'],
['After all envoys, may make up to two transfers'],
['each moving one writer or ship between any Presidencies/sea zones (including China once created).'],
['each moving one writer or ship between any Presidencies/sea zones (including China once created).'],
['each moving one writer or ship between any Presidencies/sea zones (including China once created).']]),
('Q104','Correct','The complete Military Affairs passage gives two single-piece Army transfers, top-half placement, and mandatory assignment of every trainee to any Army’s top half.',[
['May make up to two transfers'],
['each officer or regiment from one Army to another'],
['each officer or regiment from one Army to another'],
['May make up to two transfers, each officer or regiment from one Army to another, remaining in top half.'],
['Then assign **every** Officer-in-Training to any Army\'s top half.'],
['Then assign **every** Officer-in-Training to any Army\'s top half.'],
['Then assign **every** Officer-in-Training to any Army\'s top half.']]),
('Q105','Correct','Separating adjacent writers with dividers clearly places the divider between them on their connecting route; the same sentence gives the affiliation-preservation purpose at Refresh.',[
['Separate adjacent writers from different Presidencies with dividers for correct return at Refresh.'],
['Separate adjacent writers from different Presidencies with dividers for correct return at Refresh.'],
['Separate adjacent writers from different Presidencies with dividers for correct return at Refresh.']]),
('Q106','Correct','The Region Loss and FAQ passages give ordinary Invasion closure, its all-closed Cascade alternative, and exclusion of duplicate closure for Rebellion and Foreign Invasion.',[
['An Invasion Crisis closes all its orders, or Cascades if already closed; Rebellion/Foreign Invasion already close them.'],
['An Invasion Crisis closes all its orders, or Cascades if already closed; Rebellion/Foreign Invasion already close them.'],
['Rebellion/Foreign Invasion already close them.', 'Region Loss does not close them a second time: its additional closure is only for a normal Invasion Crisis.']]),
('Q107','Correct','No set order covers anytime investment actions; the entry expressly ends them when nobody wishes more and then chooses strategies.',[
['take investments actions without set order until nobody wishes more.'],
['take investments actions without set order until nobody wishes more.'],
['take investments actions without set order until nobody wishes more.'],
['Then choose strategies.']]),
('Q108','Correct','The merger passage expressly transfers secondary ships and shares into the primary firm.',[
['Transfer all secondary shares, ships and treasury funds to primary; secondary boards return to family sides.'],
['Transfer all secondary shares, ships and treasury funds to primary; secondary boards return to family sides.']]),
('Q109','Correct','The corrected-card passage states start-of-Revenue timing, one die per own officeholder and twice the highest roll.',[
['Company Fraud is played at start of Revenue'],
['roll one die per your officeholder'],
['reduce Balance by twice the highest roll (minimum zero)']]),
('Q110','Partial','Repeated successful Deploys, remaining resources and catastrophe removal are covered. The entry gives targeting and the Company-region effect restriction but never resolves the requested general prohibition on a Deploy with no chance of success. The full summary covers this at line 144: "You cannot take a dead action with no effect or chance of success: for example trade with no ship or deploy without dice to trigger possible officer losses." This is a reader omission, not missing summary coverage.',[
['May Deploy repeatedly while able, including after a success: there is no one-success-per-turn cap.'],
['Exhaust chosen officers/regiments to bottom for one die each and local alliances for printed dice.', 'a noncatastrophic failure can retry using remaining resources.', 'Its strength is usable once that turn and cannot be split among more than one purpose.'],
['Target own Presidency\'s home, any associated region, or any region bordering an associated region. Cannot target another home region or another Presidency\'s Company-controlled region. Company region must have unrest or a closed order to give action an effect.'],
['On catastrophe, Commander returns half own family’s trophies rounded up and Commander member to supply; the Commander is removed, so no further Deploy can be made by that Commander.']]),
('Q111','Correct','The entry covers one-time use, keeping the card faceup in the player area, and retained printed Power at Final Scoring.',[
['A blackmail effect is one-time'],
['keep the card faceup in your player area'],
['keep the card faceup in your player area'],
['Any printed Power still counts at Final Scoring whether the card is faceup or facedown.']]),
('Q112','Correct','The ledger and complete Revenue passage resolve Chairman discretion and multiple affordable dividends, Balance funding, share cost/payout including Chairman, no waiver and the strict Standing threshold.',[
['Chairman may pay any affordable number.'],
['Chairman may pay any affordable number.'],
['They are limited to the Company’s available Balance.'],
['Company Balance is the Company cash used for Revenue dividends.'],
['Each dividend costs one cash per Company share and pays each owner £1 per share, including Chairman.'],
['Each dividend costs one cash per Company share and pays each owner £1 per share, including Chairman.'],
['Each dividend costs one cash per Company share and pays each owner £1 per share, including Chairman.'],
['No. Company shareholders cannot waive payment.'],
['If total cash paid as dividends is strictly greater than expectations, advance Standing one space.']]),
('Q113','Correct','The initial off-board state and inability to double the first action are explicit in the ledger and supported by the Family procedure.',[
['it begins off the board.'],
['No. It may be taken twice only if the opportunity marker already matched that action at phase start; at the start of the game the marker begins off the board.']]),
('Q114','Correct','The entry identifies Company Balance as the charged account and instructs reducing it by the stated ordinary expenses, which is the requested debit operation.',[
['Ordinary Company expenses reduce the Company Balance.'],
['Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China.']]),
('Q115','Correct','The ordinary Invasion passage explicitly removes one tower from the attacker on failure.',[
['On failure, attacker loses one tower.']]),
('Q116','Correct','The entry assigns dividend discretion to the manager with India-only funding and expressly permits no payout; the plural dividends and optional payment cover the number chosen.',[
['After expenses, manager may pay dividends from India treasury only.'],
['Yes. The manager may pay no dividends; an active non-Hobnob firm paying none records zero.']])
]
assert len(choices)==len(packet['entries'])==19
grades=[]
for entry,(qid,grade,reason,quotes_by_atom) in zip(packet['entries'],choices):
 assert qid==entry['id']
 atoms=entry['requested_fact_scope_entry']['material_requested_facts']
 assert len(atoms)==len(quotes_by_atom)
 reader=entry['reader_a_entry']
 fields=[reader['answer']]+[x['supported_fact_or_case_result'] for x in reader.get('clause_ledger',[])]+[x for x in reader.get('case_conclusions',[]) if isinstance(x,str)]+[x['quote'] for x in reader.get('evidence',[])]
 for quotes in quotes_by_atom:
  for quote in quotes:
   assert any(quote in field for field in fields),(qid,quote)
 parts=[{'requirement':atom,'status':('omitted' if qid=='Q110' and i==2 else 'covered'),'reader_quotes':quotes} for i,(atom,quotes) in enumerate(zip(atoms,quotes_by_atom))]
 issue=None
 if qid=='Q110':
  issue={'cause':'reader omission','summary_coverage':'Present and clear','summary_location':'summary-snapshot.md:144, Success checks (p17)','summary_quote':'You cannot take a dead action with no effect or chance of success: for example trade with no ship or deploy without dice to trigger possible officer losses.','finding':'The same entry covers target restrictions and the need for an effect in a Company region, but omits the general no-chance-of-success restriction explicitly requested for subsequent Deploy actions.'}
 grades.append({'id':qid,'grade':grade,'reason':reason,'material_parts':parts,'unsupported_guesses':[],'summary_issue_if_any':issue})
output=base/'grades-same-entry.json'
output.write_text(json.dumps({'block_id':'block-06','readers':{'reader-a':{'grades':grades}}},ensure_ascii=False,indent=2)+'\n')
print(str(output))
print('grades='+str(len(grades)))
print('sha256='+hashlib.sha256(output.read_bytes()).hexdigest())