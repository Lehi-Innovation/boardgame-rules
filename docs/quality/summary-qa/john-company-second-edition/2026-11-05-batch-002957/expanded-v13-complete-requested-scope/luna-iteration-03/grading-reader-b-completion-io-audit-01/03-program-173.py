from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-03/grading-reader-b/block-03')
packet=json.loads((base/'packet.json').read_text())
chosen={
'Q041': [
'Created by successful envoy **or** Envoy to China law',
'in either case the Chairman immediately hires any writer',
'Its treasury holds ships, not cash.',
'After Bengal, may attempt China Trade',
'They count Eastern for expenses, events, storms and laws.'
],
'Q042': [
'only ONCE, including a failed attempt: no retry',
'Without an export icon in Company-controlled regions, do not attempt China Trade at all.',
'Neither payment counts exports in non-Company regions',
'Roll one die per ship.',
'On success, count export icons in **all Company-controlled regions only**:\n\n| Recipient | Amount |\n|---|---|\n| Company Balance | **£4 × number of those export icons**. |',
"| Superintendent's family | **£1 × number of those export icons**, from bank. |"
],
'Q043': [
'immediately make all Governors pensioners',
'remove their overlays and partially built Company ships',
'remove their overlays and partially built Company ships',
'Replace Director of Trade with Governor General, preserving holder and fatigue',
'preserving holder and fatigue',
"uses former Director's treasury and turn position",
"uses former Director's treasury and turn position",
'return Governor/Director cards to box.',
'No further Governors/overlays created upon conquest',
'Skip Governor Elimination when regions are lost.'
],
'Q044': [
'First Balance +£3 per Company region. Then may attempt Govern repeatedly',
'Every 6 rolled adds one unrest to each Company region',
'On failure add another unrest to every Company region.',
'or £2 Balance/any office treasury **except own**, adding unrest to a Company region.',
'Multiple Tax choices this turn must put their unrest in different regions.',
'must choose one benefit per region',
'complete Company ship into any sea zone including China',
'regiment into any Army',
'or £2 Balance/any office treasury **except own**',
'At most one successful Govern per turn.'
],
'Q045': [
'Roll **once per eligible ship**',
'1–2 nothing',
'3–4 fatigue, or sink if already fatigued',
'3–4 fatigue, or sink if already fatigued',
'5–6 sink.',
'Return a sunk ship to its shipyard **unfatigued**.',
'| Company and extra ships | **Exempt**; never roll storm checks. |',
'| Company and extra ships | **Exempt**; never roll storm checks. |',
'| Ships assigned to China | Count as **Eastern** sea zone. |',
'| Firm ships | Count in the sea zone on their **firm strategy**, even though on a charter. |',
'| Hobnob firm ships | **Exempt** from storms. |'
],
'Q046': [
"Return any writer on a newly closed order to its owner's supply",
'flip a filled token to closed.',
"If told to close an order in an already fully closed region, Cascade: close all open orders directly connected to that region's orders.",
"If a connected order is already closed, close that region's northernmost open order instead.",
'If none are open, it also Cascades.',
'A region can initiate a Cascade only once per event tile',
"can receive multiple Cascades' effects."
],
'Q047': [
'Close northernmost open order in top-stack region',
'Close northernmost open order in top-stack region',
'if all closed, Cascade.',
'top-stack region and every bordering region',
'Owners take £1 per writer on orders in top-stack region and every bordering region.',
"Elephant's March, then shuffle this tile with remaining draw stack",
'shuffle this tile with remaining draw stack',
'separately shuffle discards and place on top.',
'If draw stack empty, March last instead.'
],
'Q048': [
'Top-stack sovereign region gains one tower.',
'Top-stack sovereign region gains one tower.',
'Dominated region instead rebels with printed explosion modifier.',
'March only if Elephant was fully inside a Company region that successfully rebelled.'
],
'Q049': [
"Open orders connected across Elephant's border",
'add one tower to each touched non-Company region.',
'If Elephant wholly inside a region, instead open all its orders and remove its unrest.',
'If Elephant wholly inside a region, instead open all its orders and remove its unrest.',
'Then March.'
],
'Q050': [
"Sovereign attacker's whole empire strength + event modifier",
"defender's whole empire strength",
"Sovereign attacker's whole empire strength + event modifier must be **greater than** defender's whole empire strength.",
"Sovereign attacker's whole empire strength + event modifier must be **greater than** defender's whole empire strength.",
"On success, replace defender's flag with attacker's dominated flag",
'taking a capital shatters its entire empire.',
'If attacker had no empire, use a free capital/star flag and matching small flag',
'if none available no new empire/flags form.'
],
'Q051': [
'Compare only rebelling region strength + modifier',
"against its sovereign capital's strength",
'other empire regions do not count.',
'Must be strictly greater.',
'Must be strictly greater.',
'Failure removes one tower from the capital.'
],
'Q052': [
'Commander member returns to supply.',
"Commander returns half their family's trophies rounded up",
'Eliminate Governor: return office card to unused stack, fatigue and member to supplies.',
'Eliminate Governor: return office card to unused stack, fatigue and member to supplies.',
'Eliminate Governor: return office card to unused stack, fatigue and member to supplies.',
'Remove Governor overlay, partially built Company ship and unrest.',
'Remove Governor overlay, partially built Company ship and unrest.',
'Remove Governor overlay, partially built Company ship and unrest.',
"Restore dome with one tower (or Foreign Invasion's specified strength) and appropriate invasion flag.",
"Restore dome with one tower (or Foreign Invasion's specified strength) and appropriate invasion flag.",
'Return control token to its region with **the £ loot side DOWN and the region-symbol side UP**.',
'region loses its Presidency association.',
'Roll once per officer in associated Army: each 6 removes that officer.',
'Roll once per officer in associated Army: each 6 removes that officer.',
'Future conquest gets no loot modifier',
'Standing loss equals number of regions lost **so far this turn**, including this one: first -1, second additional -2, etc.',
'Standing loss equals number of regions lost **so far this turn**, including this one: first -1, second additional -2, etc.',
'Losing one region does not automatically lose any other Company region',
'resolve each other attack and its defense separately.'
],
'Q053': [
'After successful Invasion Crisis, move to successful capital (Imperial Ambitions)',
'otherwise top-stack region.',
'Company region: place fully inside.',
'Dominated region: point toward its sovereign.',
'Sovereign: point across shape-marked border on tile.',
'If that neighbor is already dominated by actor, choose first clockwise neighbor that is not.',
"If all neighbors dominated, use the redirect-arrow shape's border, pointing toward empire capital."
],
'Q054': [
'West→Bombay',
'South→Madras',
'East→Bengal',
'all storms means each',
'none means top-stack region.',
'Per target roll ordinary die for attack strength',
'the ordinary attack die, with no added unrest',
'resolve Invasion/Company attack.',
'On success close all orders (Cascade if already all closed)',
'On success close all orders (Cascade if already all closed)',
"remove target's flag",
'all matching flags if capital',
'restore dome if Company-controlled',
'set tower strength to half attack roll rounded down.',
'March with circle shape only if Elephant was fully inside a Company region that was invaded.',
'March with circle shape only if Elephant was fully inside a Company region that was invaded.'
],
'Q055': [
'PM must draw at least one law, revealing them one at a time. **After one or two ordinary (non-dilemma) draws, the PM may stop drawing, or continue up to three total.',
'Choose any one law already revealed',
'discard the others.',
'Drawing a dilemma instead forces selection of that dilemma and ends drawing immediately.',
'Drawing a dilemma instead forces selection of that dilemma and ends drawing immediately.',
"PM moves the dial's arm clockwise or counterclockwise",
"stopping on the **first** policy space matching the chosen law's bottom icon.",
'That space fixes the target and consequence.',
"**Before voting**, PM moves the dial's arm"
],
'Q056': [
'Each family pays £1 TO THE BANK per target it owns.',
'Each unpaid target returns to supply, including Chairman if taxed.',
"When selected policy includes windows, additionally pay each window on enterprises and each family member's prize",
'return enterprise/prize member if unable.',
'The BANK PAYS EACH FAMILY £1 per target that family owns.',
'Swap target Power marker with next higher marker',
'if already highest, swap any other pair.',
'Prestige enterprises count as enterprises of their printed type for these policies.'
],
'Q057': [
'each £1 family cash buys one vote',
"Each card's votes may be used only once in the entire vote, across all rounds",
'rotate it when used and leave it rotated until vote resolution.',
'It cannot vote again in a later round of the same vote.',
'Starting PM, clockwise, players cast votes',
'PM may call another full round or stop after each',
'PM may call another full round or stop after each',
'a round with no votes must end voting.'
],
'Q058': [
'A player who voted for may later oppose',
'once opposed, cannot vote for during this vote.',
'Track all opposition votes: biggest opponent holds Opposition Leader',
'tied current holder retains it.',
"With recipient's consent",
'someone who already opposed or commits to oppose',
"add them to that person's opposition total.",
'PM cannot oppose or consent to enterprises opposing',
'PM cannot oppose or consent to enterprises opposing',
'except forced use of the "Vote with my enterprises" promise.'
],
'Q059': [
'Pay printed upkeep separately for each family member on a prize. If unpaid, return that member and lose that prize\'s printed VP. Negotiating help remains possible while game continues. On final turn, perform upkeep but skip Refresh and go to Final Scoring.',
'If unpaid, return that member',
"lose that prize's printed VP.",
'On final turn, perform upkeep but skip Refresh and go to Final Scoring.',
"| Writers on orders | Return to their **associated Presidency's Writers box**; use dividers to preserve affiliation. |",
'| Filled tokens and Presidency dividers | Return to supply. |',
'| Filled tokens and Presidency dividers | Return to supply. |',
'| Extra ships | Return to supply. |',
'| Exhausted Army officers and regiments | Reactivate. |',
'| Active local alliances | Exhaust; do not reactivate alliances. |',
'Advance one turn, then begin London Season.'
]
}
reasons={
'Q041':'All creation, immediate hiring, treasury, timing and Eastern identity facts are present in the complete China passage.',
'Q042':'The full China passage resolves all eligibility limits, dice and both export-based payouts.',
'Q043':'The transition passage covers every requested removal, continuity and future conquest/loss exception.',
'Q044':'The Govern passage covers guaranteed revenue, all unrest triggers, mandatory choices and their restrictions, and the success cap. The single £2 alternative conveys an unsplit payment.',
'Q045':'The storm table and outcome sentence cover every ownership, fatigue, destination and strategy branch.',
'Q046':'The closure paragraph covers writer/token handling, Cascade propagation, closed targets and regional limits.',
'Q047':'The complete event rows provide the requested locations, payments, shuffle sequence and empty-stack exception.',
'Q048':'The Leader row supplies its location, sovereign/dominated branches and restricted March condition.',
'Q049':'The Peace row distinguishes both positional branches and specifies subsequent March.',
'Q050':'The Invasion paragraph covers both whole empires, strict comparison (therefore tie failure), flag changes, capital shattering and flag shortage. Shattering the whole empire clearly conveys removal of its flags.',
'Q051':'The Rebellion paragraph includes only rebel and capital strengths, strict comparison (therefore tie failure) and capital tower loss.',
'Q052':'The Region Loss paragraph covers all listed destinations, checks, token/loot effects, Standing escalation and separate attacks. Removing an officer on a six conveys its return to its owner supply in this piece-removal context.',
'Q053':'The March paragraph covers the successful-capital priority, ordinary destination and every posture/fallback branch.',
'Q054':'The Foreign Invasion row, primary-strength bullet and FAQ cover all target, strength, cleanup and conditional circle-March facts.',
'Q055':'The opening Parliament paragraph covers the complete drawing and policy-selection procedure.',
'Q056':'The policy table and prestige sentence cover all requested amounts, payment directions, unpaid returns and Power exceptions. Both separately requested £1 atoms are retained in order.',
'Q057':'The Voting paragraph covers prices, rotating single-use cards across rounds, complete-round order and PM/forced-stop rules.',
'Q058':'The Voting paragraph resolves all switching, opposition leadership, coalition consent/counting and PM promise exceptions.',
'Q059':'The upkeep paragraph and Refresh table cover final-turn payment, nonpayment, final scoring and every nonfinal Refresh item.'
}
grades=[]
assert list(chosen)==[e['id'] for e in packet['entries']]
for entry in packet['entries']:
    qid=entry['id']
    facts=entry['requested_fact_scope_entry']['material_requested_facts']
    quotes=chosen[qid]
    assert len(facts)==len(quotes),(qid,len(facts),len(quotes))
    actual=entry['reader_b_entry']['answer']
    for quote in quotes:
        assert quote and quote in actual,(qid,quote)
    grades.append({'id':qid,'grade':'Correct','reason':reasons[qid],'material_parts':[{'requirement':fact,'status':'covered','reader_quotes':[quote]} for fact,quote in zip(facts,quotes)],'unsupported_guesses':[],'summary_issue_if_any':None})
result={'block_id':'block-03','readers':{'reader-b':{'grades':grades}}}
out=base/'grades-same-entry.json'
serialized=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
out.write_text(serialized)
print(json.dumps({'path':str(out),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(serialized.encode()).hexdigest()}))