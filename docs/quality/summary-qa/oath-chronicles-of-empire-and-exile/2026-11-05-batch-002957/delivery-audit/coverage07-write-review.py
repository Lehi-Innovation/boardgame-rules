from pathlib import Path
import json
p=Path('docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957')
keys={k['id']:k for k in json.loads((p/'expanded-v6/answer-key.json').read_text())['answers']}
setup=[
 ('1.1','Deal saved sites and attachments by region and top-down slot order',['Q022'],'Covered; placing the map on the table adds no distinct decision.'),
 ('1.2','Initialize round and Visions Drawn markers',['Q083'],'Both initial spaces explicitly tested.'),
 ('1.3','Use the Chronicled goal reference',['Q020','Q023'],'Q020 explicitly chooses the new Oath and saves its reference; Q023 applies the starting title/banner determined by that Oath. No separate credit for moving the saved reference near the map.'),
 ('1.4','Shared bank and normal-side People\u2019s Favor',['Q021','Q040'],'Normal banner side is explicit; component quantity inventory is not a new procedural rule.'),
 ('1.5','One favor/secret on respective banners',['Q021'],'Explicit.'),
 ('1.6','Three favor per suit or four with five/six players',['Q021'],'Both player-count allocations explicit in key; no numeric variant credited.'),
 ('1.7','Select Chancellor, recommend prior winner only, Cradle seat, random other seats',[],'NEW A01: no expected key specifies these role/seating choices.'),
 ('1.8','Chancellor board/pieces, Reliquary and Grand Scepter',['Q021','Q084','Q051'],'No separate addition: the same Chancellor starting-Scepter assignment is directly tested by Q084; Q051 tests the special saved Scepter/reset relic destinations. Repeating the same assignment in a later-game scenario receives no credit. Piece totals are component inventory.'),
 ('1.9','Other players choose saved-side boards in turn order and take matching pieces',['Q023','Q052','Q021'],'Explicit board choice/status and resources; no mandatory identity ownership inherited.'),
 ('1.10','All Supply markers leftmost',['Q021'],'All full Supply explicit.'),
 ('1.11','Chancellor board favor/secrets',['Q021'],'Explicit.'),
 ('1.12','Chancellor board warbands and map garrisons, intact versus ruin eligibility',['Q021','Q022'],'All deployment branches explicit.'),
 ('1.13','Starting banner depends on People/Devotion Oath',['Q023'],'Both banner branches explicit.'),
 ('1.14','Chancellor starts Oathkeeper side',['Q023'],'Explicit.'),
 ('1.15','Exile/Citizen board resources and warband color',['Q021'],'Explicit status-dependent color.'),
 ('1.16','Site favor/secret prompts and Chancellor allocation on favor shortage',['Q022'],'Both printed prompts and allocation actor explicit.'),
 ('1.17','Four facedown Reliquary relics, random spaces',['Q024'],'Random one-per-space explicitly tested.'),
 ('1.18','Remaining relics form relic deck',['Q051','Q024','Q067'],'Chronicle explicitly stacks saved relics, setup draws the four, and Draw takes top cards. No new instruction to shuffle exists; moving remaining stack to its map space is not a distinct branch.'),
 ('1.19','Three total bottom-world-deck cards seed one per discard',['Q024'],'Explicit; not three cards per pile.'),
 ('1.20','Players in turn order draw three bottom cards',['Q024'],'Explicit.'),
 ('1.21','Put remaining world deck on map',['Q024','Q008'],'No distinct choice/branch from identifying the remaining world deck and legal Search source.'),
 ('1.22','Advance Visions Drawn for setup Visions',['Q024'],'Explicit.'),
 ('1.23','In turn order each places pawn, chooses facedown adviser, then discards two',['Q023','Q024'],'Pawn location and Chancellor exception explicit; Q024 preserves pawn-before-discard and facedown-adviser choice.'),
 ('p3 setup box','Deferred rebuild before step19',['Q101'],'Exact conditional prerequisite and before-seeding/dealing order now explicit. No further recipe credit.')]
first=[
 ('1','Unroll map',[],'Physical preparation only.'),
 ('2','Specified faceup sites and five facedown sites',['Q025'],'Positions/states explicit. Hidden a/c/d card-name recall adds no new procedure.'),
 ('3','Pawns at specified sites',['Q025'],'Explicit.'),
 ('4','Initial purple site garrisons',['Q025'],'Explicit; total piece count is not a new rule.'),
 ('5','Round and Vision markers',['Q083'],'Explicit.'),
 ('6','Shared bank, banners, and Supremacy goal reference',['Q021','Q040'],'NEW A02 for fixed Supremacy reference only; bank/banner components already tested.'),
 ('7','Three favor per suit',['Q021'],'Already explicit ordinary player-count allocation.'),
 ('8','Choose Chancellor, Cradle seat, boards',[],'A01 includes the selection/seating rule; no extra credit for board names.'),
 ('9','Chancellor board resources, Supply, Oathkeeper title',['Q021','Q023'],'Same starting resources/title already explicit; no scenario-only credit.'),
 ('10','Fixed clockwise Red, Blue, Yellow seats',[],'A01 includes first-game fixed seating versus later random seating. No independent credit for color names.'),
 ('11','Exile board resources and Supply',['Q021'],'Already explicit generic Exile starting resources.'),
 ('12','Initial denizens and 3/3/5 regional discards',['Q025','Q084'],'Explicit.'),
 ('13','Assigned facedown advisers',['Q025','Q084'],'Explicit.'),
 ('14','Remaining41 cards preserve PacketB order',['Q084'],'Explicit; no later-game bottom draws or shuffle.'),
 ('15','Grand Scepter to Chancellor',['Q084'],'Explicit.'),
 ('16','Ivory Eye facedown at Mountain',['Q025','Q084'],'Explicit.'),
 ('17','Next four relics facedown in Reliquary',['Q084'],'Explicit first-game recipe.'),
 ('18','Remaining15 relics form deck',['Q084'],'Explicit first-game recipe.')]
new=[
 {'proposal_id':'A01','question':'During first-game packet setup, how are the Chancellor and other players seated? In later-game setup, must the previous winner become Chancellor, and how are seats assigned before the other players choose boards?',
  'expected_answer':'For the first game, choose one player as Chancellor and seat them on the short edge near the Cradle; seat Red, Blue and Yellow in that clockwise order from the Chancellor. In later-game setup, choose the Chancellor in any way: the previous winner is recommended, not required. Seat the Chancellor next to the Cradle and seat the other players randomly. Non-Chancellors then choose among the boards on their Chronicled sides in that turn order.',
  'material_facts_new':['The next Chancellor may be selected in any way; the previous winner is a recommendation, not a mandatory inherited role.','The Chancellor sits next to the Cradle and other seats are random in later setup; first packet setup prescribes the Red, Blue, Yellow clockwise order.'],
  'source_references':['Law printed p2 Setup1.7; Law1.9 for the already-tested subsequent board choice','Playbook printed p6 setup8; printed p7 setup10'],
  'novelty':'A source-prescribed role/seating procedure and its first/later setup branch. The choice determines the Chancellor and order of turns/board choices. No separate novelty credit for color names, repeating clockwise turns, or repeating Chronicled-board eligibility.',
  'existing_key_cross_check':[
   {'ids':['Q023'],'actual_test':'Saved-side Citizen/Exile board eligibility, pawn placement, starting banners/title.','missing':'Does not state how Chancellor is selected or how seats are assigned.'},
   {'ids':['Q052'],'actual_test':'Saved map/board state, people may change, and non-Chancellor saved-board choice.','missing':'Does not state that previous winner is merely recommended as Chancellor, or random seating.'},
   {'ids':['Q083'],'actual_test':'Chancellor starts rounds; clockwise turns; phases and track timing.','missing':'Does not assign seats or select the Chancellor before those turns.'},
   {'ids':['Q025','Q084'],'actual_test':'First packet map, pawns, cards, discards and relic configuration.','missing':'Neither expected key specifies first-game clockwise seating order.'}],
  'all101_key_check':'Read all101 complete keys. No expected_answer contains seat/seating; no key states selection by any method or prior-winner recommendation. Closest keys above test downstream consequences, not this choice.'},
 {'proposal_id':'A02','question':'Which goal reference does the first-game packet setup use, and what are its Oathkeeper and Successor goals? Does that setup allow choosing any of the four Oaths?',
  'expected_answer':'The first-game packet setup uses the Oathkeeper of Supremacy goal reference. Its Oathkeeper goal is to rule the most sites; its Successor goal is to hold more relics and banners in total than the Chancellor and every other Citizen. The Chancellor begins with the Oathkeeper title. The printed first-game setup specifies Supremacy rather than offering a free choice among the four Oaths; later games use the goal selected in the preceding Chronicle.',
  'material_facts_new':['The prescribed first packet game starts with the Supremacy goal reference.'],
  'source_references':['Playbook printed p6 setup6: shared pieces include the Oathkeeper of Supremacy goal reference','Playbook printed p8 The Chancellor: in your first game, Chancellor begins as Oathkeeper of Supremacy','Playbook printed p26 Winning as a Citizen; Law3.3.1 for already-tested Successor definition','Law1.3 and8.1 for already-tested later Chronicled reference'],
  'novelty':'One fixed initial victory-regime assignment. The same physical setup with a People/Protection/Devotion reference would use different victory and starting-banner conditions. No credit for restating the already-tested definition of Supremacy, Successor comparison, starting title or later Chronicle selection.',
  'existing_key_cross_check':[
   {'ids':['Q002','Q005'],'actual_test':'Define all four Oath/Vision and Successor pairings.','missing':'Do not say which pairing is prescribed for the first game.'},
   {'ids':['Q025','Q084'],'actual_test':'First-game sites, pawns, garrisons, denizens/advisers and deck/relic recipe.','missing':'Neither key assigns the first-game Oathkeeper goal reference.'},
   {'ids':['Q020','Q075'],'actual_test':'Choose the next Oath in Chronicle.','missing':'The first game has no preceding Chronicle; these do not supply its fixed Supremacy initial condition.'},
   {'ids':['Q021','Q023'],'actual_test':'Later-game resources and starting banners/title conditional on the chosen Oath.','missing':'Do not identify the first-game Oath.'}],
  'all101_key_check':'Read all101 complete keys. Supremacy occurs in expected keys Q002,Q005,Q017,Q036,Q088; these concern definitions, sharing or transfer, never the first-game assignment.'}
]
covered=[
 {'domain':'Law2 Key Components and title','ids':['Q002','Q010','Q012','Q013','Q019','Q030','Q036','Q044','Q066','Q088','Q096'],'challenge':'Checked component locations/capacity, facedown restrictions, Reliquary exclusion from goals/access, banner seizure, title incumbency/ties/defense, positive rule and Imperial sharing; explicit tests found.'},
 {'domain':'Law3 Victory','ids':['Q001','Q002','Q003','Q004','Q005','Q073','Q074'],'challenge':'Checked all four goals and Successors, strict most, Vision global threshold/revelation deadline, Wake flip delay, early end-die ranges, all round-eight priorities and ties. New first-game reference assignment is A02, not another endgame permutation.'},
 {'domain':'Law4 Phases','ids':['Q006','Q007','Q068','Q072','Q079','Q083','Q092','Q095'],'challenge':'Checked mandatory versus optional Wake, Mob threshold and repeat order, win-before-flip-before-income, single uninterrupted action, Rest resource destinations/exhaustion, refresh/save cap and Citizen marker, Rest effects.'},
 {'domain':'Law5.1 Search /6.1 facedown advisers','ids':['Q008','Q009','Q010','Q030','Q031','Q067','Q073','Q076','Q082','Q089'],'challenge':'Checked cost/source choices, prescribed draws/empty source/world-Vision stop versus corrected generic Draw, discard before play, regional resource/card destinations, capacities/restrictions/new adviser limit, true Vision replacement and Conspiracy optional theft/mandatory boxing.'},
 {'domain':'Law5.2–5.4 Muster/Trade/Recover','ids':['Q011','Q012','Q013','Q027','Q040','Q062','Q069','Q087'],'challenge':'Checked local empty denizen/intact edifice eligibility, matching/adviser conditions, gain sources and shortfalls, Recover relic versus globally accessible banners, Darkest Secret corrected no-adviser branch, resource redistribution and self-recovery versus seizure.'},
 {'domain':'Law5.5 Campaign','ids':['Q014','Q015','Q016','Q017','Q027','Q036','Q037','Q038','Q039','Q065','Q070','Q077','Q078','Q080','Q081','Q088','Q090','Q093','Q094'],'challenge':'Checked defender/local-target gate/remote sites, all dice sources, force versus rolled dice, mandatory defender modifiers versus timed battle plans, side colors/rule/cost/once limit, empty attack-pool conversion, Imperial allies/status/power scope/arbitration, shields/doubles/skulls/sacrifices/ties, defeated side loss/survivors, all attacker-target outcomes, defender victory/defeat/victory/end-discard timing, title reassessment after entire Campaign.'},
 {'domain':'Law5.6 Travel /6 minor actions','ids':['Q018','Q032','Q033','Q034','Q035','Q054','Q055','Q056','Q057','Q060','Q063','Q068'],'challenge':'Checked full travel matrix and reveal prompts, fixed-cost/increase/free priority, named site overrides, forced banishment routing, peeking memory/Scepter delay, warband pickup/drop ownership/last-warband/Imperial consent, forced versus self-exile payment and Act ending.'},
 {'domain':'Law6.6/7.6.1 Citizenship','ids':['Q019','Q071','Q086'],'challenge':'Checked Scepter holder/self-offer/one Reliquary relic, binding permitted extra assets, conversion shortage decision, map/board color/status/Vision/title/Supply/turn changes, compulsory modifier uncovering and forced conversion without ordinary offer. No numerical or actor replacement credit.'},
 {'domain':'Law7 Powers and Card Reference','ids':['Q026','Q027','Q028','Q029','Q030','Q040','Q043','Q044','Q065','Q070','Q080','Q086','Q087','Q088','Q094','Q095'],'challenge':'Checked access versus persistence/rule-only plans, occupied-card/no-cost/battle-plan exceptions, out-of-turn favor and secret exhaustion, costs versus effects/no-effect payment, all standalone timing and optionality, modifier lifetime/no active discard, restriction banners/new lowest adviser limit, all four mandatory Reliquary modifiers, binding promises/Tribunal, generic forced Citizenship and explicit Law Bandit Crown exception. Individual denizen/relic/edifice recall beyond these source-defined procedures is not a required addition.'},
 {'domain':'Law8 Chronicle /Playbook29–30','ids':['Q020','Q045','Q046','Q047','Q048','Q049','Q050','Q051','Q052','Q075','Q085','Q101'],'challenge':'Checked Vision-only versus multiple wins, Exile winner turnover/excluded old Citizens/one garrison replacement, build/repair actor/occupancy rules, discarded/retained/ruined attachment destinations including corrected denizens, ordered compaction/reversed ruins/faceup guarantee, suit selection/addition/healing alternative, Dispossessed eligibility, relic refill-before-stack, board/map packing, 10+2/15+3 deck recipe and newly covered deferred-before-setup19 trigger.'},
 {'domain':'Law9–10 /Playbook31–32 /errata','ids':['Q009','Q040','Q041','Q042','Q043','Q067','Q069','Q081','Q089','Q090','Q096','Q097','Q098','Q099','Q100'],'challenge':'Checked every operative glossary entry, literal interpretation/hierarchy, must/cannot/named ignore/if-able, component limits, private/public information, no unprompted loss/transfer/binding promises, Move/Swap/Play/Reveal distinctions, After immediacy and Take/Give/Burn/Exchange defaults. All base errata reviewed; bot-specific entries excluded. Optional group rollback/sharing conventions have no single mandatory core answer to add.'}
]
sites=[
 ('Opportunity: Salt Flats, Mine, Drowned City',['Q092','Q095'],'Pawn-local optional one-total site income at end Wake; empty source.'),
 ('Homeland suit sites',['Q053','Q029'],'Same-suit discard-at-this-site suppression, all reward types/direct relic Recover, timing before When Played.'),
 ('Coast sites',['Q054'],'Both endpoints; fixed1 cost; named Narrow Pass ignore.'),
 ('Plains/Mountain',['Q061','Q037'],'Any target at site, even if ruler; required sign; zero-attack handling.'),
 ('River',['Q062'],'Muster at site plus rule condition.'),
 ('Charming Valley',['Q063','Q018'],'Origin increase; free Travel overrides.'),
 ('Shrouded Wood',['Q060','Q018','Q056'],'Fixed2 cost, named gate ignores, enemy-ruler/Chancellor routing even forced travel.'),
 ('Narrow Pass',['Q055','Q054','Q057'],'Distinct region-entry and Campaign gate conditions; rule exception only Campaign; explicit named overrides.'),
 ('Great Slum',['Q059','Q089','Q030'],'Timed discard before play or move, capacities/locks.'),
 ('Marshes',['Q058'],'Pawn-local required one-fewer Search, not remote rule.'),
 ('Buried Giant',['Q057'],'Optional own-board faceup secret exhaustion; zero Supply/Narrow Pass only.'),
 ('Hidden Place',['Q056'],'Own-board secret flip to travel or target; only named ignores override.'),
 ('Tribunal',['Q064','Q043','Q100'],'Ruler/pawn access, favor/secrets and future actions, disputed breach coin flip; binding versus Exchange.')]
rejected=[
 {'candidate':'Separate later-game Grand Scepter starting-recipient question','existing':['Q084','Q051','Q033'],'reason':'Identical Chancellor starting recipient already directly tested; Chronicle saves Scepter separately and memory/use restrictions are explicit. A later-game scenario alone does not earn a new rule.'},
 {'candidate':'Separate first-game color-name seating question','existing':[],'reason':'Included only as the fixed-versus-random branch of A01, with no independent color-name recall credit.'},
 {'candidate':'Later setup obtains Reliquary from saved top relics, not a new full shuffle','existing':['Q051','Q024','Q067'],'reason':'Composition of explicit saved top-stack, setup four draws/random spaces, and corrected top-of-source Draw. No new source instruction or conditional exception.'},
 {'candidate':'Repeat deferred world-deck rebuild with a different missing-Chronicle story','existing':['Q101','Q020','Q024'],'reason':'Exact missing prerequisite and order now directly tested; same recipe repeated is zero novelty.'},
 {'candidate':'Every setup component total, hidden first-game site identity or map-space placement','existing':['Q021','Q025','Q084'],'reason':'No independent consequential procedure beyond the existing recipes; numbers/names/physical placement do not earn new procedural credit.'},
 {'candidate':'Another Campaign total, Travel route, actor name, Oath priority combination or Chronicle suit order example','existing':['Q004','Q015','Q017','Q018','Q047','Q048'],'reason':'Complete existing conditions and ordering determine the answer without a new source-defined rule.'},
 {'candidate':'Individual illustrated card-specific powers such as Forest Temple, Ancient Forge or Fallen Spire','existing':['Q026','Q028','Q042','Q089'],'reason':'Printed card content supplies the isolated power; generic access, timing, literal priority and manipulation rules are tested. Explicit Law exceptions (Bandit Crown/forced Citizenship) and all Site Reference powers were included rather than excluded by this distinction.'}
]
report={
 'reviewer':'coverage_challenge_07',
 'verdict':'MATERIAL_GAPS_FOUND',
 'scope':'2021 base first printing; Law October20 2020, complete Playbook, official base first-print errata dated November15 2022; complete multiplayer including Chronicle/later setup; no bots/New Foundations.',
 'independence':{'summary_blind':True,'summary_or_answers_or_grades_read':False,'other_reviewer_reports_read':False,'allowed_inputs_only':True,'parent_supplied_summary_facts':False,'bank_and_ledger_unmodified':True},
 'delivery':{'complete_before_verdict':True,'text_characters':330210,'unique_contiguous_chunks':68,'maximum_chunk_characters':5000,'all101_questions_and_keys_delivered':True,'both_reference_pages_visually_inspected':True,'receipts':'delivery-audit/coverage07-receipts.jsonl','verified_manifest':'delivery-audit/coverage07-complete-delivery.json'},
 'assessment':'The current101 retained questions test most source-defined procedures and exceptions, including the recently added deferred rebuild prerequisite. Two setup assignments remain untested. This is a source/key-only coverage challenge, not a summary quality verdict or an exhaustive/held-out coverage claim.',
 'material_additions':new,
 'retention_and_novelty':{'retain_all_existing_questions':True,'historical_overlap_ids_zero_credit':['Q039','Q071','Q072','Q073','Q074','Q075','Q077','Q078','Q079','Q082'],'new_distinct_procedure_groups':2,'no_target_count_or_cap_used':True,'repeated_goal_definitions_and_seat_color_names_receive_no_separate_credit':True},
 'law_setup_clause_audit':[{'source':a,'clause':b,'existing_keys':c,'assessment':d} for a,b,c,d in setup],
 'first_game_setup_clause_audit':[{'playbook_step':a,'clause':b,'existing_keys':c,'assessment':d} for a,b,c,d in first],
 'remaining_source_challenge':covered,
 'complete_site_reference_challenge':[{'power':a,'existing_keys':b,'coverage':c} for a,b,c in sites],
 'rejected_candidates':rejected,
 'limitations':'No summary, generated answers/grades, scope/grading files, or other reviewer reports were inspected. Prior ledger assertions were challenged against all complete source text and actual keys. Ordinary printed individual card powers were not treated as a requirement to memorize every card. No unsupported special rulings were invented.'
}
(p/'coverage-review-07.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
proof={'method':'Complete101-key manual reading plus exact closest-key comparison; keyword results are supporting evidence only.','candidate_A01_closest_keys':{i:keys[i]['expected_answer'] for i in ['Q023','Q052','Q083','Q025','Q084']},'candidate_A02_closest_keys':{i:keys[i]['expected_answer'] for i in ['Q002','Q005','Q020','Q021','Q023','Q025','Q084']},'seat_term_expected_answer_matches':[i for i,k in keys.items() if 'seat' in k['expected_answer'].lower()],'Supremacy_expected_answer_matches':[i for i,k in keys.items() if 'supremacy' in k['expected_answer'].lower()]}
(p/'delivery-audit/coverage07-key-comparison.json').write_text(json.dumps(proof,indent=2,ensure_ascii=False)+'\n')
print('Wrote',p/'coverage-review-07.json')
print('Verdict:',report['verdict'],'proposals:',[x['proposal_id'] for x in new])
print('Law setup entries:',len(setup),'first setup entries:',len(first),'Site Reference groups:',len(sites))
