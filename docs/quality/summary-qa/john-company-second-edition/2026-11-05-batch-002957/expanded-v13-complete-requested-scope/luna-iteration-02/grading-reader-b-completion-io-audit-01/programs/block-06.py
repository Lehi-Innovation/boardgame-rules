from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-02/grading-reader-b/block-06')
p=json.loads((base/'packet.json').read_text())
# Explicit human-selected coverage and quotation evidence in each entry's required-atom order.
choices=[
('Correct', 'The attached Deploy passage supplies surviving-participant eligibility, the entire payment order/rates, the bank shares and repeated cycles until cash is exhausted.', [
['Count only this attempt\'s surviving participating officers and used regiments/alliances.'],
['| Commander family first | £1 for Commander **plus £1 for each of their used surviving officers**. |'],
['| Other families clockwise | £1 per used surviving officer of that family. |'],
['| Each payout cycle | Pay in this order, stopping when cash runs out |'],
['| Bank last | £1 per used regiment and per used local-alliance **piece**, regardless of strength. |'],
['| Bank last | £1 per used regiment and per used local-alliance **piece**, regardless of strength. |'],
['**Repeat that entire cycle from the Commander until all loot is distributed.**']]),
('Correct', 'The conquered-region Elephant row gives both the inward relocation and the resulting Rebellion threat against the now Company-controlled region.', [
['| 4. Elephant | If it faced outward from the conquered region, move it **fully inside that region**, now threatening Rebellion. |'],
['| 4. Elephant | If it faced outward from the conquered region, move it **fully inside that region**, now threatening Rebellion. |']]),
('Partial', 'The entry attaches Events in India rather than Revenue. It supplies no ordinary expense census or rates, no Commander expense exemption, and no China expense inclusion. Its China storm classification does not resolve the expense question.', [[],[],[],[],[],[]]),
('Correct', 'The attached dividend settlement paragraph covers waiver scope and manager consent, actual total payout on the Company Balance track, and the India-to-London remainder sweep.', [
['With that consent, the shareholder may forgo payment for any number of shares on any dividend.'],
["**Waiving a dividend requires BOTH the shareholder's choice and the MANAGER'S CONSENT**; shareholder consent alone is insufficient."],
['Record **total actual cash paid out**, not per-share dividend, with dividend cube on Company Balance track.'],
['Record **total actual cash paid out**, not per-share dividend, with dividend cube on Company Balance track.'],
['Sweep remaining India money into London.']]),
('Correct', 'The game-over instruction explicitly prohibits blackmail play unless a card permits final-scoring use.', [
['Once game over, stop negotiations, calling promises and playing blackmail unless a card explicitly permits final-scoring use.'],
['Once game over, stop negotiations, calling promises and playing blackmail unless a card explicitly permits final-scoring use.']]),
('Correct', 'The Director passage identifies office treasury cash, one pound per die, no penalty, and up to two single-piece transfers between the stated locations including China.', [
['### Director of Trade (p18)\n\nMay make repeated Special Envoy checks: £1 treasury cash per die, no penalty.'],
['£1 treasury cash per die, no penalty.'],
['£1 treasury cash per die, no penalty.'],
['After all envoys, may make up to two transfers, each moving one writer or ship between any Presidencies/sea zones (including China once created).'],
['After all envoys, may make up to two transfers, each moving one writer or ship between any Presidencies/sea zones (including China once created).'],
['After all envoys, may make up to two transfers, each moving one writer or ship between any Presidencies/sea zones (including China once created).'],
['After all envoys, may make up to two transfers, each moving one writer or ship between any Presidencies/sea zones (including China once created).']]),
('Correct', 'Military Affairs supplies the transfer count, eligible single piece, other-Army destination and top-half state, followed by mandatory assignment of every trainee to any Army top half.', [
['May make up to two transfers, each officer or regiment from one Army to another, remaining in top half.'],
['May make up to two transfers, each officer or regiment from one Army to another, remaining in top half.'],
['May make up to two transfers, each officer or regiment from one Army to another, remaining in top half.'],
['May make up to two transfers, each officer or regiment from one Army to another, remaining in top half.'],
["Then assign **every** Officer-in-Training to any Army's top half."],
["Then assign **every** Officer-in-Training to any Army's top half."],
["Then assign **every** Officer-in-Training to any Army's top half."]]),
('Correct', 'Separating the adjacent different-Presidency writers with dividers clearly places the divider between their connected orders and preserves their affiliation for correct Refresh return.', [
['Separate adjacent writers from different Presidencies with dividers for correct return at Refresh.'],
['Separate adjacent writers from different Presidencies with dividers for correct return at Refresh.'],
['Separate adjacent writers from different Presidencies with dividers for correct return at Refresh.']]),
('Correct', 'Region Loss supplies normal Invasion closure and Cascade; the attached FAQ expressly excludes a second closure for Foreign Invasion, while the Region Loss contrast excludes it for Rebellion too.', [
['An Invasion Crisis closes all its orders, or Cascades if already closed; Rebellion/Foreign Invasion already close them.'],
['An Invasion Crisis closes all its orders, or Cascades if already closed; Rebellion/Foreign Invasion already close them.'],
['An Invasion Crisis closes all its orders, or Cascades if already closed; Rebellion/Foreign Invasion already close them.', 'Region Loss does not close them a second time: its additional closure is only for a normal Invasion Crisis.']]),
('Correct', 'The investment introduction states no set order until nobody wishes more, followed by strategy choice; this permits actions freely during that step.', [
['After Family share creation, before Hiring, take investments actions without set order until nobody wishes more.'],
['After Family share creation, before Hiring, take investments actions without set order until nobody wishes more.'],
['After Family share creation, before Hiring, take investments actions without set order until nobody wishes more.'],
['Then choose strategies.']]),
('Correct', 'The merger paragraph transfers all secondary ships and shares to the primary firm.', [
['Transfer all secondary shares, ships and treasury funds to primary; secondary boards return to family sides.'],
['Transfer all secondary shares, ships and treasury funds to primary; secondary boards return to family sides.']]),
('Correct', 'The attached corrected-card text specifies start of Revenue, one die per own officeholder, and twice the highest result before the Balance minimum.', [
['Company Fraud is played at start of Revenue: roll one die per your officeholder, reduce Balance by twice the highest roll (minimum zero), and take cash from the bank equal to that actual Balance reduction'],
['roll one die per your officeholder'],
['reduce Balance by twice the highest roll (minimum zero)']]),
('Partial', 'The entry covers repeated success, exhaustion/remaining resources, ordinary target boundaries and removal of the Commander on catastrophe. It does not state the full no-dead-action restriction against an attempt with no chance of success, including deploying without dice; the Company-region effect requirement covers only part of that requested atom.', [
['**May Deploy repeatedly while able, including after a success: there is no one-success-per-turn cap.**'],
['Exhaust chosen officers/regiments to bottom for one die each and local alliances for printed dice.', 'Roll normal check; a noncatastrophic failure can retry using remaining resources.', 'Its strength is usable once that turn and cannot be split among more than one purpose.'],
[],
["On catastrophe, Commander returns half own family's trophies rounded up and Commander member to supply."]]),
('Correct', 'The explicit blackmail instruction gives one use, retained faceup in the player area, and continuing printed Power at Final Scoring in either orientation.', [
['A blackmail effect is one-time: after use, keep the card faceup in your player area; it cannot be used again or traded.'],
['A blackmail effect is one-time: after use, keep the card faceup in your player area; it cannot be used again or traded.'],
['A blackmail effect is one-time: after use, keep the card faceup in your player area; it cannot be used again or traded.'],
['Any printed Power still counts at Final Scoring whether the card is faceup or facedown.']]),
('Partial', 'The entry supplies only Events in India and contains none of the requested ordinary Company dividend procedure. Chairman discretion, multiple/affordable Balance-funded payments, share cost/payout including Chairman, waiver prohibition and Standing threshold are omitted.', [[],[],[],[],[],[],[],[],[]]),
('Correct', 'The initial off-board marker and phase-start matching condition clearly establish that the first main action cannot be doubled under the normal marker rule.', [
['1. Check where your opportunity marker was **at phase start** (it begins off the board).'],
['1. Check where your opportunity marker was **at phase start** (it begins off the board).\n2. Choose a main family action: take it once, or **may take it twice if the marker already matched it**.']]),
('Partial', 'The attached Events passage omits the ordinary expense account and the debit operation. No same-entry text charges expenses to Company Balance or lowers its marker by the expense total.', [[],[]]),
('Correct', 'The ordinary Invasion paragraph explicitly removes one tower from the attacker on failure.', [
['On failure, attacker loses one tower.']]),
('Correct', 'Manager may pay dividends from India treasury identifies discretionary payouts; the non-Hobnob zero-marker instruction confirms that choosing no payout is allowed.', [
['After expenses, manager may pay dividends **from India treasury only**.', 'Each dividend pays £1 per firm share plus £1 manager.'],
['After expenses, manager may pay dividends **from India treasury only**.', 'An active non-Hobnob firm paying none records zero; Hobnob retains prior marker.']])
]
issues={
'Q100': {'type':'reader_error','summary_location':'### VI. Revenue (p27; firms pp41–42), line 153','summary_quote':'**Expenses:** Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China. Exclude Commanders.','finding':'The full summary explicitly covers every expense atom; the reader selected the Events section and omitted them. There is no summary gap.'},
'Q110': {'type':'reader_error','summary_location':'### IV. Company Operation, line 144','summary_quote':'You cannot take a dead action with no effect or chance of success: for example trade with no ship or deploy without dice to trigger possible officer losses.','finding':'The selected Deploy passage preserves ordinary targeting and the Company-region effect requirement but omits the general no-chance-of-success restriction, which the full summary states explicitly. No summary gap.'},
'Q112': {'type':'reader_error','summary_location':'### VI. Revenue (p27; firms pp41–42), lines 153–155','summary_quote':'3. **Dividends:** Chairman may pay any affordable number. Each dividend costs one cash per Company share; pay each owner £1 per share, including Chairman. **Company shareholders cannot waive payment.** If total cash paid as dividends is **strictly greater** than expectations, advance Standing one space.','finding':'Within the Company Revenue sequence following expenses and expectations against remaining Balance, this supplies the ordinary Balance-funded dividend procedure. The reader selected only Events and omitted all nine requested atoms; no summary gap.'},
'Q114': {'type':'reader_error','summary_location':'### VI. Revenue (p27; firms pp41–42), line 153','summary_quote':'**Expenses:** Reduce Balance £1 per existing Debt, each officer/regiment in an Army, and each ship in sea zones, including China.','finding':'The summary supplies Company Balance and its reduction by the expense total. The reader selected only Events, omitting both facts. No summary gap.'}
}
grades=[]
for entry,(grade,reason,quotes_per_atom) in zip(p['entries'],choices,strict=True):
    facts=entry['requested_fact_scope_entry']['material_requested_facts']
    assert len(facts)==len(quotes_per_atom),(entry['id'],len(facts),len(quotes_per_atom))
    answer=entry['reader_b_entry']['answer']
    parts=[]
    for fact,quotes in zip(facts,quotes_per_atom,strict=True):
        for quote in quotes:
            assert quote in answer,(entry['id'],quote)
        parts.append({'requirement':fact,'status':'covered' if quotes else 'omitted','reader_quotes':quotes})
    grades.append({'id':entry['id'],'grade':grade,'reason':reason,'material_parts':parts,'unsupported_guesses':[],'summary_issue_if_any':issues.get(entry['id'])})
report={'block_id':'block-06','readers':{'reader-b':{'grades':grades}}}
out=base/'grades-same-entry.json'
raw=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode()
out.write_bytes(raw)
print(json.dumps({'path':str(out),'entries':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'grades':{g:sum(x['grade']==g for x in grades) for g in ['Correct','Partial','Incorrect']},'sha256':hashlib.sha256(raw).hexdigest()},ensure_ascii=False))