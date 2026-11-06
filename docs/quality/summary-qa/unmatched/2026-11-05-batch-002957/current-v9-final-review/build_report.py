from pathlib import Path
import json,hashlib
B=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/unmatched/2026-11-05-batch-002957'); O=B/'current-v9-final-review'; bank=B/'benchmark-v9'
q=json.loads((bank/'questions.json').read_text());key=json.loads((bank/'answer-key.json').read_text());scope=json.loads((bank/'scope-map.json').read_text()); ledger=json.loads((B/'coverage-ledger-v9.json').read_text())
notes={
'Q01':'PDF p6 fixes younger hero1, then its separate sidekicks sharing any hero zone; older hero2 and own sidekicks second; size selected at placement. Each matching30-card deck is shuffled and draws5; character health, including1 for undialed sidekicks, is set. Younger begins. Scope correctly treats choosing battlefield and a separate face-down apparatus inventory as background.',
'Q02':'PDF p8 requires exactly2 maneuver/scheme/attack actions, permitting repetition and forbidding skips. Temporarily holding9 is allowed; end-turn discard2 to own pile reaches7. Following opponent turn is correct unasked background.',
'Q03':'PDF p9: mandatory draw1 precedes optional movement. Each own fighter independently moves0 through character allowance, one complete move at a time in any chosen order. Friendly transit allowed, opposing transit blocked, occupied endpoint forbidden. Adjacent-step definition is true source background rather than another omission clause.',
'Q04':'PDF p10: discard exactly1 hand card; its BOOST adds to the maneuver movement value used by every fighter. Payment effect is ignored; cards of defeated fighters remain eligible payments if they have a BOOST value.',
'Q05':'PDF p9 imposes2 damage per surviving fighter per impossible mandatory draw and no reshuffle. Two failures total4 each if those fighters survive and duel continues; p14 immediate hero defeat correctly conditions continuation.',
'Q06':'PDF pp7/11: both attack types can target adjacent opponents across a zone edge. Only ranged can reach nonadjacent shared-zone spaces, including disconnected parts of one colored zone. No invented line-of-sight test.',
'Q07':'PDF p11 requires a legal attacking card and target, named active attacker, permitted user of each role-appropriate card; defense is optional; choices precede simultaneous reveal. Versatile counts as attack and defense for effects. Scope correctly excludes independent target-declaration/hidden-commitment inventory now directly asked Q67.',
'Q08':'PDF p12 orders immediately, during combat, damage/result, after-combat card effects, other after-combat game effects, and respective discard piles. Defender resolves same-timing effects first; card effects mandatory unless specified. Face-up status verified p10.',
'Q09':'PDF p12:4 minus4 gives0 attack damage, so defender wins despite2 effect damage. No defense against value4 gives4 attack damage. Winner test uses attack damage alone.',
'Q10':'PDF pp12/14: defeated sidekick token removed immediately, but played after-combat effect resolves if duel continues. Hero at0 ends duel immediately; subsequent healing cannot rescue it.',
'Q11':'PDF p10: scheme face up from hand, declare a permitted active fighter, cannot use a defeated listed fighter; resolve then discard. Both players may inspect either face-up discard pile at any time.',
'Q12':'Original Alice character: Alice13, melee, move2; Jabberwock8 melee. Choose BIG/SMALL on placement. BIG adds2 to Alice attack cards; SMALL adds1 to Alice defense cards. Neither changes Jabberwock. Tracking apparatus is correctly contextual.',
'Q13':'Original Arthur character: Arthur18 melee, Merlin7 ranged, move2. Arthur attacks may commit a BOOST face down with attack; add BOOST value. If attack-card effects actually canceled, discard BOOST without effect. Current textless-Excalibur exception is not a contradiction because no effects actually cancel there.',
'Q14':'Original Medusa character:16, ranged, move3;3 melee Harpies with1 health each. Own-turn start may deal1 to one opposing fighter in Medusa zone. Actor, optionality, timing, zone and amount preserved.',
'Q15':'Original Sinbad character:15 melee, Porter6 melee, base move2. Three discarded Voyages give each own fighter5 maneuver movement and newly played base2 Voyage combat value5. Played Voyage is not yet discarded and does not count itself.',
'Q16':'Alice r1c6/r2c1 Eat Me moves Alice up to3 then changes size; r2c5-6 Drink Me draws2 then changes size. BIG/SMALL toggles obligatorily, including zero chosen movement; effects are not elective as a whole.',
'Q17':'PDF p13 and original sheets:4 versus4 gives0 attack damage and Arthur win. Defender Skirmish moves Jabberwock first; Jaws then has no adjacent target. A lone adjacent friendly fighter must take2. General either-combatant/up-to2 Skirmish details are correctly contextual to given chosen move.',
'Q18':'Arthur r2c2: positive health4 or less becomes8;5 does not trigger. At0 duel is already lost. PDF p5 forbids health beyond dial maximum.',
'Q19':'Medusa r3c3-4: each own fighter up to3, may pass opposing occupied spaces; afterward return exactly one defeated Harpy if any to an unoccupied space in Medusa zone. Transit permission does not waive destination occupancy.',
'Q20':'Sinbad r1c5: base2 plus4 other discarded Voyages=6. Other Voyages return discard-to-hand after combat; Home itself discards only at combat end, leaving one Voyage and next allowance3 for each own fighter. Key correctly says only Voyage, not only card.',
'Q21':'Regroup in all four sheets draws2 instead of1 on a win and1 on a loss. PDF p12 preserves defeated sidekick played after-combat draw if duel continues.',
'Q22':'Momentous Shift condition compares fighter current space to its position at start of this turn, not whether it ever moved. Return to start gives3; different current space gives5, including defense during opponent turn.',
'Q23':'Alice r1c1-2 requires two different choices from draw2, Alice heal3, place Alice in another space. Cannot draw twice; cannot place in current or occupied space. SMALL defense2+1=3.',
'Q24':'Alice r1c3 requires combat win. Alice player looks at opponent hand and chooses1 for opponent to discard to opponent pile. On a loss no hand/discard effect resolves.',
'Q25':'Alice originals: O Frabjous changes size only; Other Side moves Alice up to3; Im Late moves Alice up to5; Mad as Hatter moves each own fighter up to2. Each changes size after its move after combat, obligatorily; resolved damage is not recalculated.',
'Q26':'Alice r4c5-6: during combat discard own deck top card to own discard, then add its BOOST2 rather than combat5 to printed3, giving5. This is a discard, not a draw.',
'Q27':'Alice r3c3-4: Claws is Jabberwock attack3, replaced by5 against a hero; sidekick target leaves3. Alice BIG adds nothing to Jabberwock cards.',
'Q28':'Arthur r1c1-3 plus character: initial BOOST2 committed with attack; optional extra BOOST3 during combat gives2+2+3=7. Defending Feint resolves immediately first, cancels Noble effect and ability BOOST; initial payment discards, later extra payment cannot occur; printed value2 remains.',
'Q29':'Arthur r2c3 Lady is Arthur-only and searches own deck/discard for Excalibur into hand; shuffle if deck searched. Excalibur r1c4 is Arthur-only attack6. Lady scheme type is true but correctly unasked background.',
'Q30':'Arthur r1c5: Arthur-only; after combat draw2, not win-gated, mandatory while game continues. Its attack-only role is correctly contextual here, directly asked Q63.',
'Q31':'Arthur r1c6/r2c1 Divine is Arthur-only versatile; after combat moves Arthur up to5 with no win gate. Both attack and defense use permitted.',
'Q32':'Arthur r2c4 Prophecy is Merlin-only scheme: inspect top4 own deck, add2 to hand, return other2 to top in any order. Not a shuffle or an attack.',
'Q33':'Arthur r2c5-6 Bewilderment is Merlin defense0. During combat prevents all damage; after combat optional placement in any unoccupied space. With no attack damage defender wins; printed0 does not override prevention.',
'Q34':'Arthur r3c1 Aid Chosen is Merlin attack4; after combat win draws2 and loss draws none from this effect.',
'Q35':'Arthur r3c2 Restless: active Merlin; selected space in Merlin zone plus one adjacent space; deal2 to each opposing fighter there. No defeat means no draw; one or two defeats draws1 total. Hero defeat ends game before draw. Scheme type correctly contextual.',
'Q36':'Arthur r3c3-4 Command: Merlin user; each fighter including opposing up to3. For opposing fighter, its owner perspective governs friendly passage and enemy blockers. Scheme and occupied endpoint are true unasked background in this transit question.',
'Q37':'Arthur r3c5-6 Swift ANY permits Merlin, whose own fighting figure moves up to4 after combat without win condition. Scope properly accepts direct Merlin permission without requiring generalized label inventory.',
'Q38':'Medusa r1c1-2/c4 Gaze2 versus defense2 causes0 attack damage, defender win, no extra8. Undefended causes2, Medusa win, then8 effect damage if game continues. Conditions and arithmetic explicit.',
'Q39':'Medusa r1c5-6 Glance is Medusa scheme: resolving it deals2 to any one fighter in Medusa zone. Friendly targets permitted; unlike character ability it is not opposing-only or start-of-turn.',
'Q40':'Medusa r2c1-3 Hiss is Medusa defense; Clutch r2c6/r3c1-2 is Harpy versatile. Both cause opponent discard1 after combat without win requirement. Opponent chooses own discard; neither random nor chosen by effect owner.',
'Q41':'Medusa r2c4-5 Hounds is Harpy-only versatile4; moves each Harpy up to3 after combat, not only the combatant; Medusa cannot play it.',
'Q42':'Medusa r3c5-6/r4c1 Second Shot is Medusa attack3, optional BOOST during combat by discarding1 hand card. BOOST2 gives5; ignored payment effect does not resolve.',
'Q43':'Medusa r4c2-4 Dash is ANY versatile and permits a Harpy defense. The combatant Harpy moves up to3 after combat without win condition. Direct defense permission suffices; literal ANY/versatile words are not extra scored clauses.',
'Q44':'Medusa r4c5-6/r5c1 Snipe is ANY versatile; attack or defense permitted. Draw1 after combat on loss or win if duel continues.',
'Q45':'Sinbad r1c1-4 Toil is Sinbad versatile, moves Sinbad up to3 after combat. Voyage-count ability triggers during maneuver, so it does not enlarge this card movement.',
'Q46':'Sinbad r1c6/r2c1 Riches is Sinbad scheme; draw3 obligatorily. Midturn8 cards does not require immediate discard;7 enforced end turn.',
'Q47':'Sinbad r2c2-4 By Fortune is Porter attack3; after combat draw2 without win gate. Defeated Porter cannot initiate, but its printed BOOST1 can still pay a BOOST.',
'Q48':'Sinbad r3c5 Command Impact is ANY attack5; r4c2-3 Exploit is ANY versatile4. Both draw1 after combat without win condition.',
'Q49':'Sinbad r3c6/r4c1 Leap is ANY versatile4. Win after combat permits moving either combatant up to4; loss grants none. Normal movement blockers apply when moving opponent; clear reference to defined normal movement satisfies asked yes/no clause.',
'Q50':'Sinbad r2c5 Whale recovers2 after combat without win requirement. Sinbad14 rises only to maximum15. Defeated Sinbad has already lost duel and cannot recover afterward.',
'Q51':'Sinbad r2c6 Snakes only looks at opponent hand after combat, without win gate. It grants no discard.',
'Q52':'Sinbad r3c1 Coals makes opponent discard1 random card after combat, without win gate. Randomness is explicit and differs from Q40 opponent-choice effect.',
'Q53':'Sinbad r3c2 Cannibals allows optional Sinbad movement up to2 after combat without win gate.',
'Q54':'Sinbad r3c3 Apes deals2 to opposing combatant after combat even on a loss while duel continues. Effect damage cannot change winner already determined by attack damage.',
'Q55':'Sinbad r3c4 Serendib draws1 to own hand after combat without win gate; mandatory if game continues.',
'Q56':'PDF p9: first draw takes remaining card; second impossible draw deals2 to each own fighter. Empty deck alone only marks exhaustion; damage waits for required draw. No discard reshuffle.',
'Q57':'All original Feints cancel opponent card effects immediately. PDF p12 defender resolves first, suppressing attacker Feint cancellation. Numeric values remain because they are not effects.',
'Q58':'Alice O Frabjous attack4+BIG2=6 against4 gives2 damage. Only after combat changes to SMALL; next played defense card gains1. Scope correctly accepts ordinary next-defense shorthand absent an affirmative no-card error.',
'Q59':'Original sheet six non-Home Voyages show no BOOST value; Home shows1. Verified 2019 designer post explicitly says absent values keep Sinbad from dumping Voyages. They cannot pay BOOST and absence is not printed0.',
'Q60':'Alice Momentous effect replaced-value5 is canceled by Feint, but character BIG bonus remains. Printed3+2=5 versus Feint2 causes3. No conflation of character and card effect cancellation.',
'Q61':'Discarding Home before movement puts a Voyage in discard. Base2 + Home BOOST1 + current Voyage count1=4 for Sinbad and Porter. BOOST payment ignores Home after-combat retrieval effect.',
'Q62':'All named Alice user/role cells match original sheet: Looking Glass Alice defense; Snicker/O Frabjous/Other Alice attack; Im Late/Hatter Alice versatile; Jaws/Claws Jabberwock attack; Manxome ANY versatile. Shared Feint/Regroup/Momentous/Skirmish ANY versatile where present. Jabberwock cannot defend with Alice-only or attack-only cards. Retained zero-novelty regression.',
'Q63':'Original sheets: Morgana Arthur attack; Swift ANY attack; Gaze Medusa attack; Winged Frenzy ANY scheme; all7 Voyages Sinbad attack. Merlin cannot defend with Swift or Morgana; Harpy can initiate Frenzy but not Gaze; Porter cannot Voyage and Sinbad cannot defend with Voyage. Retained zero-novelty regression.',
'Q64':'Verified designer/publisher author43936 historical 2021 article36640902 says Feint cancels boosted Excalibur boost. Given explicitly historical condition, BOOST discards without effect, attack6, damage6-2=4. Current2025 rule is not substituted for this asked condition.',
'Q65':'Alice SMALL modifies value of defense cards, not innate damage prevention. No defense card means no value to increase. Undefended attack4 deals4 and attacker wins. Condition directly tested here rather than borrowed from Q58.',
'Q66':'Official iello.fr post dated11 August2025 describes immediately applicable Restoration Games change, casual and tournaments: textless Excalibur cannot have effects canceled and retains ability BOOST.6+3=9,9-2=7. Noble Sacrifice has effects actually canceled by Feint, so ability BOOST is discarded without effect. Source-correction branch retained with zero novelty.',
'Q67':'PDF p11 Step1 declares target before Step2 card choices. Attacker commits attack face down first; defender then commits defense face down or declines without seeing attack. Simultaneous reveal follows decisions. No ordinary post-defense card substitution or retargeting. Only target-before-cards and hidden attacker-before-defender commitment supply novel coverage, not reused reveal/permission facts.'
}
assert len(notes)==67
ks={x['id']:x for x in key['answers']};ss={x['id']:x for x in scope['questions']}
ids=[f'Q{i:02d}' for i in range(1,68)];assert [x['id'] for x in q['questions']]==ids;assert list(ks)==ids;assert list(ss)==ids
checks=[]
for row in q['questions']:
 i=row['id'];assert ss[i]['asked_clauses']==row['question']
 checks.append({'id':i,'verdict':'PASS','source_key_outcome':'PASS','asked_clause_mapping':'PASS','actual_question':row['question'],'actual_required_facts':ss[i]['required_answer_facts'],'contextual_exclusions':ss[i]['contextual_key_background'],'independent_check':notes[i],'source_refs':ks[i]['source_refs'],'corrections':[]})
# Every physical cell was visually read from the four original full-resolution sheets.
grids={
'alice-action-cards.png':[
['Looking Glass','Looking Glass','Snicker-Snack','O Frabjous Day!','The Other Side of the Mushroom','Eat Me'],
['Eat Me',"I’m Late, I’m Late","I’m Late, I’m Late","I’m Late, I’m Late",'Drink Me','Drink Me'],
['Jaws That Bite','Jaws That Bite','Claws That Catch','Claws That Catch','Momentous Shift','Momentous Shift'],
['Skirmish','Skirmish','Mad as a Hatter','Mad as a Hatter','Manxome Foe','Manxome Foe'],
['Feint','Feint','Feint','Regroup','Regroup','Regroup']],
'king-arthur-action-cards.png':[
['Noble Sacrifice','Noble Sacrifice','Noble Sacrifice','Excalibur','The Aid of Morgana','Divine Intervention'],
['Divine Intervention','The Holy Grail','The Lady of the Lake','Prophecy','Bewilderment','Bewilderment'],
['Aid the Chosen One','Restless Spirits','Command the Storms','Command the Storms','Swift Strike','Swift Strike'],
['Skirmish','Skirmish','Skirmish','Momentous Shift','Momentous Shift','Momentous Shift'],
['Feint','Feint','Feint','Regroup','Regroup','Regroup']],
'medusa-action-cards.png':[
['Gaze of Stone','Gaze of Stone','Regroup','Gaze of Stone','A Momentary Glance','A Momentary Glance'],
['Hiss and Slither','Hiss and Slither','Hiss and Slither','The Hounds of Mighty Zeus','The Hounds of Mighty Zeus','Clutching Claws'],
['Clutching Claws','Clutching Claws','Winged Frenzy','Winged Frenzy','Second Shot','Second Shot'],
['Second Shot','Dash','Dash','Dash','Snipe','Snipe'],
['Snipe','Feint','Feint','Feint','Regroup','Regroup']],
'sinbad-action-cards.png':[
['Toil and Danger','Toil and Danger','Toil and Danger','Toil and Danger','Voyage Home','Riches Beyond Compare'],
['Riches Beyond Compare','By Fortune and Fate','By Fortune and Fate','By Fortune and Fate','Voyage to the Island That Was a Whale','Voyage to the Valley of the Giant Snakes'],
['Voyage to the Creature with Eyes Like Coals of Fire','Voyage to the Cannibals with the Root of Madness','Voyage to the City of the Man-Eating Apes','Voyage to the City of the King of Serendib','Commanding Impact','Leap Away'],
['Leap Away','Exploit','Exploit','Momentous Shift','Momentous Shift','Momentous Shift'],
['Feint','Feint','Feint','Regroup','Regroup','Regroup']]}
cells=[]
for file,grid in grids.items():
 for r,row in enumerate(grid,1):
  for c,name in enumerate(row,1):cells.append({'original':file,'cell':f'r{r}c{c}','title':name,'visually_inspected':True,'user_role_value_boost_effect_copy_markings_checked':True})
assert len(cells)==120
meta=json.loads((O/'text-metadata.json').read_text());reads=[json.loads(x) for x in (O/'text-read-receipts.jsonl').read_text().splitlines()];textr=[]
for k,m in meta.items():
 a=sorted((x for x in reads if x['key']==k),key=lambda x:x['start'])
 if k=='publisher-page.html':
  parsed=json.loads((O/'html-mechanical-check.json').read_text());assert parsed['equals_delivered_full_visible'];m.update({'read_mode':'Complete HTML mechanically parsed using BeautifulSoup; script/style/noscript removed; all resulting visible text delivered and reviewed','raw_mechanically_processed_bounds':[0,m['characters']],'parsed_visible_characters':parsed['mechanically_parsed_visible_characters'],'matches_full_visible_text_after_strip':True,'truncated':False})
 else:
  complete=bool(a) and a[0]['start']==0 and a[-1]['end']==m['characters'] and all(x['end']==y['start'] for x,y in zip(a,a[1:]));assert complete and all(x['end']-x['start']<=4800 and not x['truncated'] for x in a)
  m.update({'read_mode':'Contiguous original UTF-8 character slices, at most4800 source characters per response, max_output_tokens at least sufficient to avoid truncation','bounds':[[x['start'],x['end']] for x in a],'complete':True,'truncated':False})
 textr.append({'source':k,**m})
images=json.loads((O/'image-metadata.json').read_text())
for x in images:
 if x['file'].endswith('.png'):x.update({'visually_inspected_original':True,'readability':'All normative card text and icons legible at original resolution; no uninspected cells','cell_count':30 if 'action-cards' in x['file'] else 1})
 else:x.update({'full_text_read_via_extraction':True,'visually_verified_pdf_pages':[6,7,8,9,10,11,12,13,14,16],'render_scale':1.3,'renders_written_only_under':str(O),'render_truncation':False})
rejections=[
{'candidate':'Add target/card commitment sequence again under a different attacking hero or card','reason':'Q67 now directly asks target-before-cards, attacker face-down commitment before optional hidden defender choice, reveal and inability to substitute after defense information. Cosmetic actor/card variants add no condition.'},
{'candidate':'Treat simultaneous reveal or optional defense as additional new Q67 rules','reason':'These are already directly asked Q07. Only previously unasked target and hidden commitment timing are novel.'},
{'candidate':'Count named user/type examples Q62/Q63 as new procedural rules','reason':'Retained overlap of directly asked Q07/Q11 legality mechanisms. Zero novelty even though every answer must still be correct.'},
{'candidate':'Count current Excalibur Q66 as another new mechanic or import its9/7 result into historical Q64','reason':'Official source-correction regression earns zero novelty; explicitly historical Q64 still requires6/4. No human scope dependency or authority gap remains.'},
{'candidate':'Require unasked labels/inventory in Q07 or Q43','reason':'Direct permitted-fighter/role and defense permission statements resolve actual questions. Q67 covers formerly unasked hidden order; Q43 does not require reciting ANY or versatile.'},
{'candidate':'New ordinary movement path/endpoint arrangements or card-driven movement variants','reason':'Q03 defines core allowances, per-fighter completion, friendly/enemy transit and endpoints; Q36 explicitly owner-relative; Q49 accepts defined normal movement; Q19 asks enemy-transit exception. Numerical/path rearrangements add no rule-defined consequence.'},
{'candidate':'Make a separate source-definition question about adjacent steps, deck orientation, size token or selecting battlefield','reason':'These source definitions/background cannot become extra scored omissions in an actual question that does not request them. Defined normal movement/deck references remain adequate equivalents; no consequential new condition beyond the mapped mechanics was identified.'},
{'candidate':'Different hand sizes or draws crossing exhaustion boundary','reason':'Q02/Q46 give end-turn-only hand enforcement; Q05/Q56 give mandatory per-missing-draw damage and no automatic damage on merely empty deck. Changed counts do not add mechanics.'},
{'candidate':'New zero-move size switch, health cap, dead-fighter card, or after-defeat effect example','reason':'Q16/Q25/Q58 explicitly ask non-retroactive mandatory switches; Q18/Q50 cap/defeat; Q04/Q47 unusable payment; Q10/Q21 played-after-defeat continuation. Actor/card substitutions add no exception.'},
{'candidate':'Different Voyages/BOOST/card-combat values or more defeated Harpies','reason':'Q15/Q20/Q59/Q61 cover current discard count, played-versus-discard timing, absent BOOST, Home exception and retrieval; Q19 covers return-one if-any. Cosmetic numbers or copies receive no novelty.'},
{'candidate':'Unspecified incomplete-deck Prophecy resolution, simultaneous unfamiliar damage ties, or later-set cancellation/map effects','reason':'No explicit supported new ruling within the supplied standard-duel original-product authorities, or outside scope; do not invent a key.'},
{'candidate':'Reinstate historical R16 or R21 rejection premises','reason':'The supplied addendum explicitly supersedes authority uncertainty and pending-human-choice premises. Raw official iello.fr visible post verifies direct source and current applicability.'}
]
report={
 'review':'Fresh independent current-v9 final source/key/scope/coverage challenge',
 'verdict':'PASS',
 'verdicts':{'source_integrity_and_authority':'PASS','all_67_key_outcomes':'PASS','all_actual_asked_clause_mappings':'PASS','current_historical_excalibur_scope':'PASS','coverage_saturation':'PASS','two_zero_stopping_rule':'PASS'},
 'scope':q['scope'],
 'independence':{'read_only_inputs':True,'summaries_read':False,'readers_read':False,'grades_read':False,'prior_reviews_or_audits_read':False,'parent_context_used':False,'allowed_ledger_history_only':True,'writes_and_renders_only_in_assigned_folder':str(O),'no_external_research_or_extra_source_files':True},
 'findings':{'key_corrections':[],'scope_corrections':[],'source_corrections':[],'coverage_additions':[],'remaining_supported_procedural_gaps':[],'question_count':67,'all_ids_unique_contiguous_and_present_in_key_and_map':True,'all_scope_asked_clauses_equal_actual_questions':True,'input_manifest_hashes_checked_for_permitted_JSON_inputs':True,'historical_rejection_override':'R16 and R21 are historical, superseded by allowed addendum and verified current official source. Neither creates a present authority or human-input dependency.'},
 'all_67_id_checks':checks,
 'official_current_source_check':{'url':'https://iello.fr/unmatched-inarretable-excalibur/','canonical_domain':'iello.fr','title':'[Unmatched] Inarrêtable Excalibur !','published_date':'2025-08-11','raw_html_sha256':meta['publisher-page.html']['sha256'],'full_visible_text_matches_mechanical_parse':True,'full_visible_text':(B/'source-research/iello-2025-official-erratum/publisher-full-visible-text-v2.txt').read_text(),'complete_article_body':(B/'source-research/iello-2025-official-erratum/publisher-article-body-v2.txt').read_text(),'operative_understanding':'Official Restoration Games rule change communicated by IELLO, immediately applicable to friendly and tournament play. Textless Excalibur retains ability BOOST against Feint; effects-bearing Noble Sacrifice cancellation still discards ability BOOST without effect. Related product date19 February2021 is distinct from post date11 August2025.','historical_primary_check':'Author43936 verified as Justin D. Jacobson, designer4083/publisher34846 Restoration Games. Article36640902 dated2021-01-02 explicitly cancels boosted Excalibur boost; valid for historical Q64, superseded for current Q66.'},
 'novelty_challenge':{'criterion':'A supported previously unasked rule-defined condition, timing, priority or exception with consequence; no cosmetic wording/card-copy/number variants or mechanical recombinations without consequence.','accepted_additions':[],'rejected_candidates':rejections,'existing_novelty_dispositions':{'Q62':0,'Q63':0,'Q66':0,'Q67':'One genuine procedural addition: target-before-card and hidden attacker-before-defender commitment; simultaneous reveal/permission overlap receives no extra novelty.'}},
 'complete_sweeps':[
 {'id':'final-source-procedure-sweep','addition_count':0,'scope':'All complete core source procedures and actual Q01-Q67 asked-clause mappings','checked':['setup health/decks/hands/placement/size/turn order','space/zone/adjacency definitions and movement semantics','two required actions and hand-limit timing','mandatory draws/exhaustion per missing card/no reshuffle','maneuver draw-before-move, each fighter, independent distance, zero, complete-before-next, blockers and occupied endpoints','BOOST payment/cost/effect suppression/unusable-fighter cards','scheme actor/legal role/face-up execution/discard/public pile inspection','attack legality and melee/ranged targets','target declaration then hidden attacker commitment then optional hidden defense then simultaneous reveal','immediately/during/damage/after-card/after-other/discard order and defender-first priority','mandatory effects, damage versus effect damage, winner','sidekick removal and continued played effects versus immediate hero defeat/end']},
 {'id':'final-components-exceptions-sweep','addition_count':0,'scope':'All4 original character cards, all120 original action-card cells, all unique printed effects and primary2019/2021/current2025 rules','checked':['all hero/sidekick stats and size/BOOST/start-turn/Voyage abilities','every action-card user, type, printed number, BOOST presence/absence, copies and normative effect','win-dependent versus unconditional versus optional effects','friendly/opposing/ANY targets and owner-relative movement','movement versus placement and occupancy','size change sequence/bonus eligibility/no-card branch/cancellation scope','Noble Sacrifice two BOOST timings and cancellation','Voyage scaling/current discard membership/Home retrieval destination and BOOST exception','health cap/defeat interruption and after-combat continuation','discard chooser versus random versus look-only','historical2021 and immediately applicable official2025 Excalibur branches independently computed']}
 ],
 'two_zero_stopping_conclusion':{'ledger_zero_addition_sweeps':[15,16],'fresh_challenge_addition_count':0,'fresh_complete_procedural_sweep_zero':True,'fresh_complete_component_exception_sweep_zero':True,'satisfied':True,'explanation':'Q67 closes the consequential attack commitment gap. Complete independent source-to-asked-clause and component/exception sweeps found no genuine remaining procedural addition. The ledger15/16 two-zero conclusion survives this challenge. No universal novelty quota imposed.'},
 'text_receipts':textr,
 'image_and_pdf_receipts':images,
 'all_120_original_card_cells':cells,
 'verification_limits':['This review determines source/key/scope/coverage correctness, not reader performance or summary quality; no such prohibited materials were read.','PDF complete normative text was read through the supplied complete extraction and visually checked on pages6-14 and16 as needed; other pages were not separately rendered for visual reading.','Raw HTML was processed completely mechanically; normative visible output was delivered completely, while non-visible markup was not manually read as a rule source.']
}
manifest=json.loads((bank/'input-manifest.json').read_text())
for name in ['questions.json','answer-key.json','scope-map.json','versioned-corrections.json']:assert hashlib.sha256((bank/name).read_bytes()).hexdigest()==manifest['hashes'][name]
(O/'coverage-key-scope.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'report':str(O/'coverage-key-scope.json'),'verdict':report['verdict'],'id_checks':len(checks),'original_image_receipts':8,'action_cells':len(cells),'text_sources':len(textr),'corrections':0,'novelty_additions':0,'two_zero_satisfied':True},indent=2))
