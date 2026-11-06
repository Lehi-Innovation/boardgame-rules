from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-01/grading-reader-a/block-03')
# Each coverage judgment and quotation below was chosen independently from the visible complete entry.
chosen=[
('Q041','Correct','All five requested China creation, hiring, treasury, timing and Eastern-status facts are supported in this entry.',[
('Successful Special Envoy to China or Envoy to China law creates office','covered','Successful envoy or Envoy to China law creates it; Chairman immediately hires any writer.'),
('Chairman immediately hires any writer','covered','Chairman immediately hires any writer.'),
('Ships only','covered','Treasury holds ships, not cash; Shipping and Director may send ships there as to any sea zone.'),
('China acts after Bengal','covered','China acts after Bengal; ships assigned to China count Eastern for expenses, events, storms and laws.'),
('Ships in China count as Eastern sea-zone ships.','covered','ships assigned to China count Eastern for expenses, events, storms and laws.')]),
('Q042','Correct','The entry resolves all attempt limits and export eligibility, dice and both payment formulas correctly.',[
('Only one attempt','covered','Only once including failed attempt; no retry.'),
('Cannot attempt without export in Company-controlled region','covered','Without an export icon in Company-controlled regions, do not attempt China Trade.'),
('Non-Company exports excluded','covered','No. Count export icons in Company-controlled regions only.'),
('One die per China ship','covered','Roll one die per ship.'),
('Success gives Balance £4 per export in all Company-controlled regions','covered','On success Company Balance gets £4 per Company-region export icon; Superintendent\'s family gets £1 per such icon from bank.'),
('Superintendent receives £1 per such export','covered','Superintendent\'s family gets £1 per such icon from bank.')]),
('Q043','Correct','The transition and later conquest/loss effects are complete; the copied applicable passage explicitly preserves treasury and operation position as well as holder and fatigue.',[
('Governors retire to Pensioners','covered','All Governors become pensioners; remove their overlays and partial ships, return Governor/Director cards to box.'),
('Remove Governor overlays','covered','remove their overlays and partial ships'),
('Remove unfinished Company ships','covered','remove their overlays and partially built Company ships'),
('Replace Director holder/card with GG','covered','Replace Director of Trade with Governor General, preserving holder and fatigue, and place its ribbon overlay.'),
('Preserve fatigue','covered','preserving holder and fatigue'),
('Preserve office treasury','covered','Governor General hires Presidents and uses former Director\'s treasury and turn position; it is hired like Director and rolls attrition normally.'),
('Preserve operation slot','covered','uses former Director\'s treasury and turn position'),
('Box Director and Governor cards','covered','return Governor/Director cards to box.'),
('No new Governors or overlays after conquest','covered','No further Governors/overlays created upon conquest; printed Company symbols indicate controlled regions.'),
('Region Loss skips Governor elimination','covered','Skip Governor Elimination when regions are lost.')]),
('Q044','Correct','Guaranteed revenue, all three unrest triggers, region choices and destinations, treasury restriction and success cap are covered.',[
('Company Balance gains £3 per Company-controlled region before checks','covered','First Balance +£3 per Company region. Then may attempt Govern repeatedly'),
('Each rolled six adds unrest to every Company region','covered','Every 6 rolled adds one unrest to each Company region, even on success'),
('Unsuccessful check adds another unrest to each','covered','failure adds another unrest to every Company region.'),
('Each tax choice adds unrest','covered','or £2 Balance/any office treasury **except own**, adding unrest to a Company region.'),
('Multiple tax choices use different Company regions','covered','Multiple Tax choices this turn must put their unrest in different regions.'),
('Success must benefit each Company-controlled region once','covered','must choose one benefit per region'),
('Place a Company ship in any sea zone, including China.','covered','complete Company ship into any sea zone including China'),
('Or regiment to any Army','covered','regiment into any Army'),
('Or unsplit £2 to Balance or an office treasury except GG own','covered','or £2 Balance/any office treasury **except own**, adding unrest to a Company region.'),
('At most one successful Govern','covered','At most one successful Govern per turn.')]),
('Q045','Correct','All storm outcomes, ship exemptions, China identity and firm strategy/Hobnob rules are present.',[
('Roll per affected player-owned ship','covered','| Player-owned ships in Company fleets | Check ships in the affected sea zone(s). |'),
('1–2 no change','covered','1–2 nothing'),
('3–4 fatigue if unfatigued','covered','3–4 fatigue, or sink if already fatigued'),
('3–4 sink if already fatigued','covered','3–4 fatigue, or sink if already fatigued'),
('5–6 sink','covered','5–6 sink.'),
('Sunk ship returns matching yard unfatigued','covered','A sunk ship returns to shipyard unfatigued.'),
('Company ships exempt','covered','Company and extra ships are exempt and never roll storm checks.'),
('Extra ships exempt','covered','Company and extra ships are exempt and never roll storm checks.'),
('China ships count Eastern','covered','Ships assigned to China count as Eastern sea zone.'),
('Firm ships use strategy zone','covered','Firm ships count in the zone on their firm strategy; Hobnob firm ships are exempt.'),
('Hobnob ships exempt','covered','Hobnob firm ships are exempt.')]),
('Q046','Correct','Writer/token destinations, Cascade propagation and closed-target fallback, and the distinction between initiation and incoming effects are covered.',[
('Writer returns owner supply','covered','Return any writer on newly closed order to its owner\'s supply; flip filled token to closed.'),
('Flip filled token closed','covered','flip filled token to closed.'),
('Fully closed source region Cascades to connected orders','covered','If told to close an order in an already fully closed region, Cascade: close all open orders directly connected to that region\'s orders.'),
('Already closed connected target redirects to northernmost open order in that region','covered','If a connected order is already closed, close that region\'s northernmost open order instead.'),
('If none open Cascade there','covered','If none are open, it also Cascades.'),
('Region initiates Cascade at most once per event tile','covered','A region initiates a Cascade only once per event tile, but may receive effects from multiple Cascades.'),
('Region may receive multiple effects','covered','A region initiates a Cascade only once per event tile, but may receive effects from multiple Cascades.')]),
('Q047','Correct','All three events have the correct location, effects and sequence, including the empty-stack Shuffle exception.',[
('Top draw-stack region','covered','Turmoil closes northernmost open order in top-stack region, Cascade if all closed.'),
('Close northernmost open order','covered','Turmoil closes northernmost open order in top-stack region, Cascade if all closed.'),
('If all closed Cascade','covered','Turmoil closes northernmost open order in top-stack region, Cascade if all closed.'),
('Top draw-stack region and adjacent regions','covered','Windfall pays owners £1 per writer on orders in top-stack region and each bordering region.'),
('Pay £1 per writer on orders there','covered','Windfall pays owners £1 per writer on orders in top-stack region and each bordering region.'),
('Normally March first','covered','March Elephant, shuffle tile with remaining draw stack, then separately shuffle discards and place them on top.'),
('Shuffle tile into remaining draw stack','covered','shuffle tile with remaining draw stack'),
('Shuffle discards and put them on top','covered','then separately shuffle discards and place them on top.'),
('If draw stack empty March last','covered','If draw stack is empty, March last instead.')]),
('Q048','Correct','Leader location, sovereign and dominated branches and restricted March condition are complete.',[
('Use top draw-stack region','covered','Top-stack sovereign region gains one tower; dominated region instead rebels with printed explosion modifier.'),
('Sovereign gains tower','covered','Top-stack sovereign region gains one tower'),
('Dominated resolves Rebellion with printed explosion modifier','covered','dominated region instead rebels with printed explosion modifier.'),
('March only if Elephant wholly within Company region that successfully rebelled','covered','March only if Elephant was fully inside a Company region that successfully rebelled.')]),
('Q049','Correct','Both positional branches and the subsequent March are correctly resolved without mixing their effects.',[
('Border: open connected orders across border','covered','On border, open orders connected across Elephant\'s border and add one tower to each touched non-Company region.'),
('Border: add tower to each touched non-Company region','covered','On border, open orders connected across Elephant\'s border and add one tower to each touched non-Company region.'),
('Fully inside: open all local orders','covered','If Elephant wholly inside a region, open all its orders and remove its unrest instead.'),
('Fully inside: clear unrest','covered','If Elephant wholly inside a region, open all its orders and remove its unrest instead.'),
('Then March','covered','Then Elephant Marches in either case.')]),
('Q050','Correct','The entry covers whole-empire comparison, tie failure and all flag branches. Shattering the entire defender empire conveys removal of that empire\'s flags.',[
('Whole attacking empire plus modifier','covered','Sovereign attacker\'s whole empire strength plus event modifier is compared with defender\'s whole empire strength.'),
('Whole defending empire','covered','Sovereign attacker\'s whole empire strength plus event modifier is compared with defender\'s whole empire strength.'),
('Attacker must be strictly greater','covered','Attacker must be strictly greater, so equal strength is insufficient; failure costs attacker one tower.'),
('Tie fails','covered','Attacker must be strictly greater, so equal strength is insufficient'),
('Success puts matching attacker dominated flag on defender','covered','On success replace defender\'s flag with attacker\'s dominated flag; taking a capital shatters entire defender empire.'),
('Capturing capital removes all old defender-empire flags','covered','taking a capital shatters entire defender empire.'),
('Unflagged attacker creates capital and dominated flags if set available','covered','If attacker has no empire, use a free capital/star flag and matching small flag; if none available, no new empire/flags form.'),
('No new flags or empire if no set available','covered','if none available, no new empire/flags form.')]),
('Q051','Correct','The strengths included and excluded, strict comparison and failed-Rebellion capital loss are all explicit.',[
('Rebel region strength plus modifier','covered','Compare only rebelling region\'s strength plus modifier against its sovereign capital\'s strength; other empire regions do not count.'),
('Defending sovereign capital strength','covered','Compare only rebelling region\'s strength plus modifier against its sovereign capital\'s strength; other empire regions do not count.'),
('Ignore other empire regions','covered','other empire regions do not count.'),
('Rebel must be strictly greater','covered','Must be strictly greater, so tie fails; failure removes one tower from the capital.'),
('Tie fails','covered','Must be strictly greater, so tie fails'),
('Capital loses one tower, not rebel','covered','failure removes one tower from the capital.')]),
('Q052','Correct','All requested loss cleanup, officer checks, spent-loot status, escalating Standing losses and separate attack resolution are covered. Removal of an officer is clear contextual elimination back to its family supply; no alternative holding destination is asserted.',[
('Commander returns supply','covered','Commander member to supply.'),
('Return half family trophies rounded up','covered','Commander returns half own family\'s trophies rounded up'),
('Governor card returns unused offices','covered','Governor card goes to unused stack; fatigue and member to supplies.'),
('Governor member returns supply','covered','Governor card goes to unused stack; fatigue and member to supplies.'),
('Governor fatigue returns supply','covered','Governor card goes to unused stack; fatigue and member to supplies.'),
('Remove Governor overlay','covered','Remove overlay, partial Company ship, unrest'),
('Remove unfinished ship','covered','Remove overlay, partial Company ship, unrest'),
('Remove unrest','covered','Remove overlay, partial Company ship, unrest'),
('Restore dome with one tower','covered','restore dome with one tower and appropriate invasion flag'),
('Apply appropriate normal-Invasion flag','covered','restore dome with one tower and appropriate invasion flag'),
('Return control token loot-down to region','covered','Return control token to region with £ loot side down and region-symbol side up.'),
('Region no longer associated with Presidency','covered','region loses Presidency association.'),
('Roll per officer in associated Army','covered','Roll once per officer in associated Army; each 6 removes that officer.'),
('Each six removes officer to owner supply','covered','Roll once per officer in associated Army; each 6 removes that officer.'),
('Loot side down means no further loot bonus','covered','Future conquest gets no loot modifier.'),
('First region lost this turn loses one Standing','covered','Loss equals number of regions lost so far this turn: first -1, second additional -2, etc.'),
('Second loses two, and so on','covered','Loss equals number of regions lost so far this turn: first -1, second additional -2, etc.'),
('No automatic loss of other regions','covered','No. Each other Company region\'s attack and defense resolves separately.'),
('Resolve each region attack separately','covered','Each other Company region\'s attack and defense resolves separately.')]),
('Q053','Correct','The successful-Invasion destination, normal destination and all posture/neighbor fallback branches are covered.',[
('Successful Invasion uses successful capital through Imperial Ambitions','covered','After successful Invasion Crisis, move to successful capital (Imperial Ambitions); otherwise top-stack region.'),
('Other Marches use top draw-stack region','covered','After successful Invasion Crisis, move to successful capital; otherwise move to top-stack region.'),
('Company: fully inside','covered','Company region: fully inside.'),
('Dominated: faces sovereign','covered','Dominated: point toward sovereign.'),
('Sovereign: tile-shape border toward neighbor','covered','Sovereign: point across shape-marked border.'),
('Skip own dominated neighbors clockwise','covered','If neighbor is already dominated by actor, choose first clockwise neighbor not so'),
('All neighbors dominated: redirect-arrow shape border toward empire capital','covered','if all neighbors are dominated, use redirect-arrow border pointing to empire capital.')]),
('Q054','Correct','All target branches, per-target die strength, applicable combat procedure, success cleanup and conditional circle March are supported.',[
('Storm die West targets Bombay','covered','Storm die selects zones: West Bombay, South Madras, East Bengal; all storms means each target, no storms means top-stack region.'),
('South targets Madras','covered','Storm die selects zones: West Bombay, South Madras, East Bengal; all storms means each target, no storms means top-stack region.'),
('East targets Bengal','covered','Storm die selects zones: West Bombay, South Madras, East Bengal; all storms means each target, no storms means top-stack region.'),
('All storms targets each once','covered','all storms means each target'),
('No storms targets top draw-stack region','covered','no storms means top-stack region.'),
('Roll attack die per target','covered','For each target roll ordinary die for attack strength; no unrest is added.'),
('Attack strength equals die','covered','For each target roll ordinary die for attack strength; no unrest is added.'),
('Resolve as Invasion or Company attack as appropriate','covered','Per target roll ordinary die for attack strength and resolve Invasion/Company attack.'),
('Success closes every open order','covered','On success close all orders (Cascade if already all closed)'),
('Cascade only if all already closed','covered','On success close all orders (Cascade if already all closed)'),
('Return local flag','covered','remove target\'s flag and all matching flags if capital'),
('If capital return all matching flags','covered','remove target\'s flag and all matching flags if capital'),
('Restore Company dome if applicable','covered','restore dome if Company-controlled'),
('Set tower strength to half attack die rounded down','covered','set tower strength to half attack roll rounded down.'),
('If Elephant wholly within invaded Company region March with circle','covered','March with circle shape only if Elephant was fully inside a Company region that was invaded.'),
('Otherwise no redirect','covered','March with circle shape only if Elephant was fully inside a Company region that was invaded.')]),
('Q055','Correct','Law draw/selection limits, mandatory dilemma selection and the first-matching directional policy procedure before voting are complete.',[
('Reveal laws one at a time up to three','covered','PM must draw at least one law, revealing them one at a time.'),
('May stop and choose an earlier draw','covered','after one or two ordinary non-dilemma laws, may stop or continue up to three total, then choose any revealed law and discard others.'),
('Discard unselected draws','covered','then choose any revealed law and discard others.'),
('Must stop on dilemma','covered','Drawing a dilemma forces selection of that dilemma and immediately ends drawing.'),
('Must select dilemma','covered','Drawing a dilemma forces selection of that dilemma and immediately ends drawing.'),
('Choose clockwise or counterclockwise','covered','Before voting, move dial arm clockwise or counterclockwise and stop on first policy space matching chosen law\'s bottom icon; that space fixes target and consequence.'),
('Stop at first matching law icon','covered','stop on first policy space matching chosen law\'s bottom icon'),
('Policy includes target and consequence','covered','that space fixes target and consequence.'),
('Move PM arm before vote','covered','Before voting, move dial arm clockwise or counterclockwise')]),
('Q056','Correct','All tax, window, bonus and Power consequences are present; the applicable passage also explicitly includes prestige enterprises.',[
('£1 per target','covered','Each family pays bank £1 per target owned; unpaid target returns to supply, including Chairman if taxed.'),
('Return unpaid target including Chairman','covered','unpaid target returns to supply, including Chairman if taxed.'),
('Additional charge for all windows on enterprises and prize members','covered','When policy includes windows, additionally pay each window on enterprises and each family member\'s prize; return enterprise/prize member if unable.'),
('Return unaffordable enterprise or member','covered','return enterprise/prize member if unable.'),
('£1 per target','covered','Bank pays each family £1 per target owned; family receives it.'),
('Swap target with next higher marker','covered','Swap target Power marker with next higher; if already highest, swap any other pair.'),
('If target highest swap any other pair','covered','if already highest, swap any other pair.'),
('Prestige enterprises count in their category','covered','Prestige enterprises count as enterprises of their printed type for these policies.')]),
('Q057','Correct','The entry covers vote costs and once-per-vote card usage, rotation, complete clockwise rounds, PM control and forced ending after a zero-vote round.',[
('Family cash costs £1 per vote','covered','Each £1 family cash buys one vote plus printed card votes.'),
('Card vote icons usable once per entire vote','covered','Each card\'s votes may be used only once in entire vote across all rounds; rotate when used and keep rotated until resolution.'),
('Rotate card to record use','covered','rotate when used and keep rotated until resolution.'),
('Card votes do not reset between rounds','covered','It cannot vote again in a later round of the same vote.'),
('PM acts first then clockwise in complete rounds','covered','Starting PM, clockwise, players cast votes'),
('PM may call another full round','covered','PM may call another full round or stop after each round.'),
('PM may resolve after full round','covered','PM may call another full round or stop after each round.'),
('Round with no votes forces resolution','covered','A round with no votes must end voting.')]),
('Q058','Correct','Vote-switch direction, opposition leadership and ties, coalition consent and attribution, and the PM promise exception are complete.',[
('Supporter may later oppose','covered','A player who voted for may later oppose; once opposed, cannot vote for during this vote.'),
('Opponent cannot later support same vote','covered','once opposed, cannot vote for during this vote.'),
('Most opposition votes','covered','Track all opposition votes: biggest opponent holds Opposition Leader; tied current holder retains it.'),
('Incumbent retains tie','covered','tied current holder retains it.'),
('Need recipient consent','covered','With recipient consent, votes may be cast on behalf of someone who already opposed or commits to oppose; add them to that person\'s opposition total.'),
('Recipient already opposing or committed to oppose','covered','votes may be cast on behalf of someone who already opposed or commits to oppose'),
('Coalition votes count toward recipient opposition total','covered','add them to that person\'s opposition total.'),
('PM cannot oppose','covered','PM cannot oppose or consent to enterprises opposing, except forced use of Vote with my enterprises promise.'),
('PM cannot consent enterprises to opposition','covered','PM cannot oppose or consent to enterprises opposing, except forced use of Vote with my enterprises promise.'),
('Vote promise can force PM enterprises against law','covered','PM cannot oppose or consent to enterprises opposing, except forced use of Vote with my enterprises promise.')]),
('Q059','Correct','Final-turn upkeep and skipped Refresh, unpaid-prize consequences and all required nonfinal Refresh items are supported. Returning an unpaid family member has the clear contextual destination of its supply.',[
('Every prize member pays upkeep even final scheduled turn','covered','Yes. Pay printed upkeep separately for each family member on a prize; on final turn perform upkeep then skip Refresh and go to Final Scoring.'),
('Unpaid member returns supply','covered','Return the unpaid member and lose that prize\'s printed VP.'),
('Lose its VP','covered','Return the unpaid member and lose that prize\'s printed VP.'),
('Final turn skips Refresh and scores','covered','on final turn perform upkeep then skip Refresh and go to Final Scoring.'),
('Otherwise map writers return associated Presidencies','covered','Writers return to associated Presidency Writers box'),
('Filled tokens return supply','covered','filled tokens/dividers and extra ships to supply'),
('Dividers return supply','covered','filled tokens/dividers and extra ships to supply'),
('Extra ships return supply','covered','filled tokens/dividers and extra ships to supply'),
('Officers and regiments reactivate','covered','exhausted officers/regiments reactivate'),
('Active alliances exhaust','covered','active local alliances exhaust and do not reactivate'),
('Advance Turn','covered','advance turn marker then begin London Season.')])
]
packet=json.loads((base/'packet.json').read_text())
assert [x[0] for x in chosen]==[e['id'] for e in packet['entries']]
grades=[]
for (qid,grade,reason,parts),entry in zip(chosen,packet['entries']):
    assert [p[0] for p in parts]==entry['requested_fact_scope_entry']['material_requested_facts'],qid
    reader=entry['reader_a_entry']
    fields=[reader['answer']]+[x['supported_fact_or_case_result'] for x in reader.get('clause_ledger',[])]+[x for x in reader.get('case_conclusions',[]) if isinstance(x,str)]+[x['quote'] for x in reader.get('evidence',[])]
    for req,status,q in parts:
        assert any(q in field for field in fields),(qid,req,q)
    grades.append({'id':qid,'grade':grade,'reason':reason,'material_parts':[{'requirement':req,'status':status,'reader_quotes':[q]} for req,status,q in parts],'unsupported_guesses':[],'summary_issue_if_any':None})
output={'block_id':'block-03','readers':{'reader-a':{'grades':grades}}}
path=base/'grades-same-entry.json'
payload=json.dumps(output,ensure_ascii=False,indent=2)+'\n'
path.write_text(payload)
print(json.dumps({'path':str(path),'grades':len(grades),'material_parts':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(payload.encode()).hexdigest()}))