from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-02/grading-reader-b/block-03')
packet=json.loads((base/'packet.json').read_text())
# These quotations and coverage judgments were selected after reading every complete entry.
chosen={
'Q041':[
'Created by successful envoy **or** Envoy to China law;',
'**in either case the Chairman immediately hires any writer**.',
'Its treasury holds ships, not cash.',
'After Bengal, may attempt China Trade',
'They count Eastern for expenses, events, storms and laws.'
],
'Q042':[
'**only ONCE, including a failed attempt: no retry**.',
'**Without an export icon in Company-controlled regions, do not attempt China Trade at all.**',
'Neither payment counts exports in non-Company regions;',
'Roll one die per ship.',
'On success, count export icons in **all Company-controlled regions only**:\n\n| Recipient | Amount |\n|---|---|\n| Company Balance | **£4 × number of those export icons**. |',
"| Superintendent's family | **£1 × number of those export icons**, from bank. |"
],
'Q043':[
'Law creates this office: immediately make all Governors pensioners,',
'remove their overlays and partially built Company ships,',
'remove their overlays and partially built Company ships,',
'Replace Director of Trade with Governor General, preserving holder and fatigue,',
'preserving holder and fatigue,',
"Governor General hires Presidents and uses former Director's treasury and turn position;",
"Governor General hires Presidents and uses former Director's treasury and turn position;",
'return Governor/Director cards to box.',
'No further Governors/overlays created upon conquest;',
'Skip Governor Elimination when regions are lost.'
],
'Q044':[
'First Balance +£3 per Company region.',
'**Every 6 rolled adds one unrest to each Company region**, even on successful roll.',
'On failure add another unrest to every Company region.',
'or £2 Balance/any office treasury **except own**, adding unrest to a Company region.',
'Multiple Tax choices this turn must put their unrest in different regions.',
'**must choose one benefit per region**:',
'complete Company ship into any sea zone including China;',
'regiment into any Army;',
'or £2 Balance/any office treasury **except own**, adding unrest to a Company region.',
'At most one successful Govern per turn.'
],
'Q045':[
'Roll **once per eligible ship**:',
'1–2 nothing;',
'3–4 fatigue, or sink if already fatigued;',
'3–4 fatigue, or sink if already fatigued;',
'5–6 sink.',
'Return a sunk ship to its shipyard **unfatigued**.',
'| Company and extra ships | **Exempt**; never roll storm checks. |',
'| Company and extra ships | **Exempt**; never roll storm checks. |',
'| Ships assigned to China | Count as **Eastern** sea zone. |',
'| Firm ships | Count in the sea zone on their **firm strategy**, even though on a charter. |',
'| Hobnob firm ships | **Exempt** from storms. |'
],
'Q046':[
"Return any writer on a newly closed order to its owner's supply;",
'flip a filled token to closed.',
"If told to close an order in an already fully closed region, Cascade: close all open orders directly connected to that region's orders.",
"If a connected order is already closed, close that region's northernmost open order instead.",
'If none are open, it also Cascades.',
'A region can initiate a Cascade only once per event tile but can receive multiple Cascades\' effects.',
'A region can initiate a Cascade only once per event tile but can receive multiple Cascades\' effects.'
],
'Q047':[
'| Turmoil | Close northernmost open order in top-stack region; if all closed, Cascade. |',
'| Turmoil | Close northernmost open order in top-stack region; if all closed, Cascade. |',
'| Turmoil | Close northernmost open order in top-stack region; if all closed, Cascade. |',
'| Windfall | Owners take £1 per writer on orders in top-stack region and every bordering region. |',
'| Windfall | Owners take £1 per writer on orders in top-stack region and every bordering region. |',
"| Shuffle | Elephant's March, then shuffle this tile with remaining draw stack; separately shuffle discards and place on top. If draw stack empty, March last instead. |",
'shuffle this tile with remaining draw stack;',
'separately shuffle discards and place on top.',
'If draw stack empty, March last instead.'
],
'Q048':[
'| Leader | Top-stack sovereign region gains one tower.',
'Top-stack sovereign region gains one tower.',
'Dominated region instead rebels with printed explosion modifier.',
'March only if Elephant was fully inside a Company region that successfully rebelled.'
],
'Q049':[
"| Peace | Open orders connected across Elephant's border and add one tower to each touched non-Company region.",
'add one tower to each touched non-Company region.',
'If Elephant wholly inside a region, instead open all its orders and remove its unrest.',
'If Elephant wholly inside a region, instead open all its orders and remove its unrest.',
'If Elephant wholly inside a region, instead open all its orders and remove its unrest. Then March.'
],
'Q050':[
"Sovereign attacker's whole empire strength + event modifier must be **greater than** defender's whole empire strength.",
"Sovereign attacker's whole empire strength + event modifier must be **greater than** defender's whole empire strength.",
'An Invasion attacker must be strictly stronger; equal strength fails, so the attacker loses one tower.',
'An Invasion attacker must be strictly stronger; equal strength fails, so the attacker loses one tower.',
"On success, replace defender's flag with attacker's dominated flag;",
'taking a capital shatters its entire empire.',
'If attacker had no empire, use a free capital/star flag and matching small flag;',
'if none available no new empire/flags form.'
],
'Q051':[
"Compare only rebelling region strength + modifier against its sovereign capital's strength; other empire regions do not count.",
"Compare only rebelling region strength + modifier against its sovereign capital's strength; other empire regions do not count.",
'other empire regions do not count.',
'A Rebellion must be strictly stronger; a tie fails, and the sovereign capital loses one tower.',
'A Rebellion must be strictly stronger; a tie fails, and the sovereign capital loses one tower.',
'Failure removes one tower from the capital.'
],
'Q052':[
'Commander member returns to supply.',
"Commander returns half their family's trophies rounded up,",
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
'Future conquest gets no loot modifier;',
'Standing loss equals number of regions lost **so far this turn**, including this one: first -1, second additional -2, etc.',
'Standing loss equals number of regions lost **so far this turn**, including this one: first -1, second additional -2, etc.',
'**Losing one region does not automatically lose any other Company region: resolve each other attack and its defense separately.**',
'**Losing one region does not automatically lose any other Company region: resolve each other attack and its defense separately.**'
],
'Q053':[
"**Elephant's March:** After successful Invasion Crisis, move to successful capital (Imperial Ambitions); otherwise top-stack region.",
'otherwise top-stack region.',
'Company region: place fully inside.',
'Dominated region: point toward its sovereign.',
'Sovereign: point across shape-marked border on tile.',
'If that neighbor is already dominated by actor, choose first clockwise neighbor that is not.',
"If all neighbors dominated, use the redirect-arrow shape's border, pointing toward empire capital."
],
'Q054':[
'Roll storm die for target regions: West→Bombay, South→Madras, East→Bengal;',
'Roll storm die for target regions: West→Bombay, South→Madras, East→Bengal;',
'Roll storm die for target regions: West→Bombay, South→Madras, East→Bengal;',
'all storms means each, none means top-stack region.',
'all storms means each, none means top-stack region.',
'Per target roll ordinary die for attack strength and resolve Invasion/Company attack.',
'- **Primary Foreign Invasion:** the ordinary attack die, with no added unrest (designer ruling in FAQ).',
'Per target roll ordinary die for attack strength and resolve Invasion/Company attack.',
'**On a successful Foreign Invasion, close all orders in the target region once; if they are already all closed, Cascade instead.**',
'**On a successful Foreign Invasion, close all orders in the target region once; if they are already all closed, Cascade instead.**',
"remove target's flag and all matching flags if capital,",
"remove target's flag and all matching flags if capital,",
'restore dome if Company-controlled,',
'set tower strength to half attack roll rounded down.',
'March with circle shape only if Elephant was fully inside a Company region that was invaded.',
'March with circle shape only if Elephant was fully inside a Company region that was invaded.'
],
'Q055':[
'PM must draw at least one law, revealing them one at a time. **After one or two ordinary (non-dilemma) draws, the PM may stop drawing, or continue up to three total.',
'After one or two ordinary (non-dilemma) draws, the PM may stop drawing, or continue up to three total. Choose any one law already revealed and discard the others.',
'Choose any one law already revealed and discard the others.',
'Drawing a dilemma instead forces selection of that dilemma and ends drawing immediately.',
'Drawing a dilemma instead forces selection of that dilemma and ends drawing immediately.',
"**Before voting**, PM moves the dial's arm clockwise or counterclockwise,",
"stopping on the **first** policy space matching the chosen law's bottom icon.",
'That space fixes the target and consequence.',
"**Before voting**, PM moves the dial's arm clockwise or counterclockwise,"
],
'Q056':[
'**Each family pays £1 TO THE BANK per target it owns.**',
'Each unpaid target returns to supply, including Chairman if taxed.',
"When selected policy includes windows, additionally pay each window on enterprises and each family member's prize;",
'return enterprise/prize member if unable.',
'**The BANK PAYS EACH FAMILY £1 per target that family owns.**',
'Swap target Power marker with next higher marker;',
'if already highest, swap any other pair.',
'Prestige enterprises count as enterprises of their printed type for these policies.'
],
'Q057':[
'each £1 family cash buys one vote, plus printed card votes.',
"**Each card's votes may be used only once in the entire vote, across all rounds: rotate it when used and leave it rotated until vote resolution. It cannot vote again in a later round of the same vote.**",
'rotate it when used and leave it rotated until vote resolution.',
'It cannot vote again in a later round of the same vote.',
'Starting PM, clockwise, players cast votes;',
'PM may call another full round or stop after each;',
'PM may call another full round or stop after each;',
'a round with no votes must end voting.'
],
'Q058':[
'A player who voted for may later oppose; once opposed, cannot vote for during this vote.',
'A player who voted for may later oppose; once opposed, cannot vote for during this vote.',
'Track all opposition votes: biggest opponent holds Opposition Leader; tied current holder retains it.',
'Track all opposition votes: biggest opponent holds Opposition Leader; tied current holder retains it.',
"With recipient's consent, votes may be cast on behalf of someone who already opposed or commits to oppose; add them to that person's opposition total.",
"With recipient's consent, votes may be cast on behalf of someone who already opposed or commits to oppose; add them to that person's opposition total.",
"With recipient's consent, votes may be cast on behalf of someone who already opposed or commits to oppose; add them to that person's opposition total.",
'PM cannot oppose or consent to enterprises opposing, except forced use of the "Vote with my enterprises" promise.',
'PM cannot oppose or consent to enterprises opposing, except forced use of the "Vote with my enterprises" promise.',
'PM cannot oppose or consent to enterprises opposing, except forced use of the "Vote with my enterprises" promise.'
],
'Q059':[
'Pay printed upkeep separately for each family member on a prize. If unpaid, return that member and lose that prize\'s printed VP. Negotiating help remains possible while game continues. On final turn, perform upkeep but skip Refresh and go to Final Scoring.',
"If unpaid, return that member and lose that prize's printed VP.",
"If unpaid, return that member and lose that prize's printed VP.",
'On final turn, perform upkeep but skip Refresh and go to Final Scoring.',
"| Writers on orders | Return to their **associated Presidency's Writers box**; use dividers to preserve affiliation. |",
'| Filled tokens and Presidency dividers | Return to supply. |',
'| Filled tokens and Presidency dividers | Return to supply. |',
'| Extra ships | Return to supply. |',
'| Exhausted Army officers and regiments | Reactivate. |',
'| Active local alliances | Exhaust; do not reactivate alliances. |',
'| Turn marker | **Advance one turn, then begin London Season.** |'
]
}
reasons={
'Q041':'The attached China procedure resolves both creation routes, immediate hire, ship-only treasury, timing and Eastern status.',
'Q042':'All attempt restrictions, dice and controlled-export payment formulas are explicitly resolved in the attached procedure.',
'Q043':'The complete transition passage covers all pieces, office continuity and subsequent conquest/loss changes.',
'Q044':'The attached Govern procedure correctly states guaranteed revenue, each unrest trigger, mandatory regional choices, destinations and success limit. The £2 option is a single destination choice.',
'Q045':'The attached storm procedure resolves every fatigue branch, ship return and ownership/zone/strategy exception.',
'Q046':'The attached Cascade procedure states all closure destinations, propagation branches and repeated-effect limits.',
'Q047':'All three event rows and the surrounding draw-stack context resolve the requested locations and Shuffle order exception.',
'Q048':'The Leader row resolves location, both political branches and the exclusive March condition.',
'Q049':'The Peace row separates border and wholly-inside effects and explicitly follows them with March.',
'Q050':'The concrete tie conclusion is correct, and the attached Invasion passage resolves full-empire strengths and all flag branches. Shattering the entire defender empire conveys removal of its empire flags.',
'Q051':'The concrete tie/capital-loss conclusion and attached Rebellion passage resolve every requested comparison and failed-side effect.',
'Q052':'The full Region Loss passage resolves destinations, losses, loot, Standing escalation and independent attacks. Removing the failed officer conveys its removal from play back to its family supply; the separate Foreign Invasion tower exception is correctly conditional.',
'Q053':'The attached March passage resolves destination priority and every political/posture branch.',
'Q054':'The full event procedure and applicable FAQ resolve targets, unmodified attack die, success cleanup and exclusive circle-March condition.',
'Q055':'The attached Parliament passage resolves discretionary stopping, earlier selection, compulsory dilemma and the first matching directional policy choice before voting.',
'Q056':'The policy table resolves payment amounts and directions, unpaid targets, windows and both Power cases; prestige-category treatment is explicit.',
'Q057':'The attached voting passage resolves cash/cards, card rotation and nonreuse, complete rounds and the PM/zero-vote stopping rules.',
'Q058':'The attached voting passage resolves switching direction, opposition leadership/ties, coalition consent/counting and the PM promise exception.',
'Q059':'The attached Upkeep/Refresh procedure resolves final-turn payment, returning unpaid members to supply with VP loss, the final-turn branch and all ordinary refresh items.'
}
grades=[]
for entry in packet['entries']:
    qid=entry['id']; atoms=entry['requested_fact_scope_entry']['material_requested_facts']; quotes=chosen[qid]
    assert len(atoms)==len(quotes),(qid,len(atoms),len(quotes))
    answer=entry['reader_b_entry']['answer']
    assert all(q in answer for q in quotes),qid
    grades.append({'id':qid,'grade':'Correct','reason':reasons[qid], 'material_parts':[{'requirement':atom,'status':'covered','reader_quotes':[quote]} for atom,quote in zip(atoms,quotes)], 'unsupported_guesses':[], 'summary_issue_if_any':None})
assert len(grades)==19
output={'block_id':'block-03','readers':{'reader-b':{'grades':grades}}}
path=base/'grades-same-entry.json'
path.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(path),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))