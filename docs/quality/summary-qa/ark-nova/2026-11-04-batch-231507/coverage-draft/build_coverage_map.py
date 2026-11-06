import json
from pathlib import Path
from build_expansion import rows, PASS1_END, PASS2_END, PASS3_END, PASS4_END, PASS5_END, PASS6_END, write_outputs

HERE=Path(__file__).resolve().parent
entries=[]
def ids(*sections):
    result=[]
    for s in sections:
        if s.startswith('Q'):
            result.append(s)
        else:
            result += [r['id'] for r in rows if r['coverage_section']==s]
    return list(dict.fromkeys(result))
def cover(pid, source, passage, *sections, note=None):
    qs=ids(*sections)
    assert qs, (pid, sections)
    entries.append(dict(passage_id=pid, source=source, passage=passage, disposition='covered', question_ids=qs, note=note))
def exclude(pid,source,passage,reason):
    entries.append(dict(passage_id=pid,source=source,passage=passage,disposition='excluded',question_ids=[],reason=reason))

# MAIN: enumerate every rules-bearing section, captions and diagrams. Repeated examples
# map to their underlying procedure, rather than multiplying numerical permutations.
exclude('M01','Main p1','Cover/title','Not a procedural rule.')
cover('M02a','Main p2','Action-card printed draw/discard/play tables','main.cards_table','main.animals_table')
cover('M02b','Main p2','Printed Cheetah Sprint 3 effect','diagrams.animal_illustrated_effects')
cover('M02c','Main p2','Printed Science Lab and Reptiles conservation example','sponsor.201','Q16',note='Reptile icon thresholds illustrate the general project support mechanism; no separate numerical permutation.')
cover('M02d','Main p2','Printed Large Animal Zoo final-scoring table','diagrams.final_large_animals')
cover('M02e','Main p2','Building faces, footprints, special capacities','Q09','Q11','diagrams.special_capacity')
exclude('M02f','Main pp2–3','Component quantities, board orientation and map difficulty labels','Inventory/physical orientation/recommendation; component scarcity rule covered separately in M04b.')
cover('M03','Main p3','Goal and opposite scoring tracks','Q20')
cover('M04a','Main p4 global 1/3','Break starting space, Zoo deck and six face-down display cards','Q02','Q05')
cover('M04b','Main p4 global 2/4','Four random Bonus tiles, unused tiles, suitable component substitutes','main.setup')
cover('M04c','Main p4 personal A','Map A/0 selection and advanced-map selection alternatives','main.setup')
cover('M04d','Main p4 personal B','Action-card order and starting side','Q01')
cover('M05a','Main p5 global 5a/b/c','One tile each, base projects by player count, two-player blocking','Q02','Q15')
cover('M05b','Main p5 global 6/7, personal C–G','Final deck, random start, clockwise order; counters, tokens, workers, money, final cards, hand and reveal','Q01','Q02','main.setup')
exclude('M05c','Main p5 shaded setup recommendations','Suggested starting hand/deck composition','Advice rather than mandatory play procedure; not strategy-guide authority.')
cover('M06a','Main p6 Gameplay','No rounds, one action per clockwise turn, intervening breaks','Q03','Q19')
cover('M06b','Main p6 Your Zoo Map paragraphs 1–4','Covered/building/terrain spaces, upgrade-marked spaces and placement bonuses','Q08','Q09','Q10','glossary.terms')
cover('M06c','Main p6 Your Zoo Map paragraphs 5–7','Seven support bonuses, action slots and starting enclosure','Q16','Q03','main.setup')
cover('M06d','Main pp6–7 map diagrams','Partner slot rewards and upgrade gate, university slot rewards, special enclosure sizes','diagrams.partner_slots','diagrams.universities','diagrams.university_third','diagrams.special_capacity')
cover('M06e','Main p6 Map A left edge; Icon Overview pp1–2','All seven support bonuses with four recurring vs three immediate-only effects','diagrams.support_bonuses')
cover('M07a','Main p7 Zoo Cards','Animal/Sponsor/Conservation Project card purposes','Q11','Q16','Q18')
cover('M07b','Main p7 Break Track','Movement, end reward, excess ignored, after-turn break, reset','Q05')
cover('M07c','Main p7 partner/university/workers/notepad','Lowest placement space, unique continents, maximum4 and upgrade, discounts, icons, worker hire order','Q15','main.setup','diagrams.partner_slots','diagrams.universities')
cover('M08a','Main p8 turn procedure and worked slot4 example','Slot strength, select/use/move/shift, X strength and cap, after-finishing','Q03')
cover('M08b','Main p8 upgrades','Flip without movement, next-action use, four upgrade opportunities, cannot upgrade all five','main.upgrades')
cover('M08c','Main p8 no doing nothing and X alternative','Cannot choose empty action; alternate action outline','Q04')
cover('M08d','Main p8 five action overviews','Cards, Build, Animals, Association, Sponsors summaries','Q06','Q08','Q11','Q14','Q18')
cover('M09a','Main p9 Cards I','Table draws and discard choice, snap threshold, break2, no money, hand timing','Q06','main.cards_table')
cover('M09b','Main p9 Cards II','Draw deck/display any order, snap3, upgrade reputation lock','Q06','Q07','main.cards_table')
cover('M09c','Main p9 reputation/display paragraphs','Same/lower folders, one-time bonuses, max15 conversion, refill ordering, no discard search','Q07','Q06')
cover('M09e','Main pp2,4,9 diagrams','Initial reputation1/conservation0, exact folder reputation ranges and individual one-time reputation bonuses','diagrams.reputation')
cover('M09d','Main p9 worked display example','Mixed draws, discard, end-turn shift/refill','Q06','main.cards_table')
cover('M10a','Main p10 Build I paragraphs','Building options, footprints, repeats/caps, payment, first/later placement, spacing, starting faces and covered bonuses','Q08','Q09','Q10','diagrams.special_capacity')
cover('M10b','Main p10 Build II paragraphs','Added specials, immediate-only relocation, no unique Build, different-building budget, sequential pay, upgrade spaces and completion','Q08','Q09','Q10','Q13')
cover('M10c','Main p10 worked placement/payment/kiosk figures','Legal spacing and earlier placement bonus funds later building','Q08','Q10')
cover('M11a','Main p11 Animals I steps1–5','Conditions, full payment/discount before reward, occupancy/terrain, place card then effects, ordered animals and after-finishing','Q11','Q10','main.animals_table')
cover('M11b','Main p11 Animal card layout','Own icons count, category/continent/terrain requirements, interaction threshold and optional alternate effects','golden.icons','golden.terrain','abilities.interactive_eligibility')
cover('M11c','Main p11 Long-billed Vulture illustration','Scavenging3 draw random discard3 keep1','diagrams.animal_illustrated_effects')
cover('M12a','Main p12 Special Enclosures','One each; eligible animals; terrain; token capacities/no flipping; immediate all/individual relocation and standard freeing','Q11','Q13','diagrams.special_capacity')
cover('M12b','Main p12 enclosure/immediate-effect examples','Caiman standard or special, newly drawn Lynx may become second animal','Q11','Q10')
cover('M13a','Main p13 Animals II','Display within reputation, folder cost, mixed sources, optional rep first5+, upgrade condition','Q12','main.animals_table')
cover('M13b','Main p13 Placing Cards','Visible top information and brown endgame reminder','Q20','golden.icons',note='Overlapping cards is presentation advice; visibility and final effects are covered.')
cover('M13c','Main p13 Animal categories','All seven, bear subcategory, Petting Zoo replaces biological category','main.animal_categories')
cover('M13d','Main p13 AnimalsII worked example','Reputation4 unlocks folder3, display cost and end-turn refill','Q12')
cover('M14a','Main p14 Association I and board divisions','Workers, repeat task escalation, other colors ignored, break return, task values and task limits','Q14')
cover('M14b','Main p14 individual reputation/partner/university tasks','+2rep, tiles available only, duplicates/caps/upgrade, placement bonuses/icons/research/handlimit','Q14','Q15','diagrams.partner_slots','diagrams.universities')
cover('M15a','Main p15 conservation work paragraphs','Immediate support only, place/shift/cap/discard tokens, fixed base projects, choose unoccupied condition once, map bonus before/after','Q16')
cover('M15b','Main p15 Project layout and release description','Icon sources; exact depicted release condition; printed appeal loss; discard/free enclosure','Q17','golden.icons')
cover('M15c','Main p15 Large Animals worked example','Discard overflowing project, choose support condition, three-X uncovered bonus','Q16')
cover('M16a','Main p16 release worked example','Release appeal first, remove special tokens, support reward and uncovered money','Q17','Q16')
cover('M16b','Main p16 AssociationII','Different tasks strength total, workers per task, play project from in-range display plus cost/refill','Q14','Q16')
cover('M16c','Main p16 donation paragraphs and example','Task prerequisite, one donation/no extra worker, lowest visible cost, supply token, +1CP, repeatable12','main.donations')
cover('M17a','Main p17 Sponsors I/II','Hand/strength vs totalstrength+1, conditions, display cost, sequential effects, upgraded condition, break money option','Q18','Q10')
cover('M17b','Main p17 Sponsor layout and example','Own icons count, terrain, immediate/recurring/income/final timing and Meerkat self-trigger','golden.icons','Q10','Q19','Q20','sponsor.243_244_247')
cover('M18a','Main p18 X-token action','Any card/side/slot, cannot strengthen, movement/cap','Q04')
cover('M18b','Main p18 conservation milestones','2upgrade/worker,5/8money/tile,10discard final cards','Q20')
cover('M18c','Main pp18–19 break steps1–6','Hand limit, remove action tokens, workers/tiles refill, discard2display, income order, kiosk rules, activated income, reset/next player','Q19')
cover('M19a','Main p19 endgame timing and last turns','Only own end/break, shared scoring area or passing, player last turns','Q20')
cover('M19b','Main p19 score cards and victory calculation','Discard final if no10, final cards and sponsors, cap4 each, target formula incl negative score, tiebreak','Q20')
cover('M19c','Main p19 Final Scoring card illustrations','Sponsored Zoo table; Biodiverse relative-category comparison','final.008','final.009')
exclude('M20','Main p20; FAQ p2 Solo break question','All solo-specific setup, gameplay, rounds, challenge and break exception','Explicit scope exclusion. Optional use of alternate interaction effects in multiplayer is retained as an authorized base multiplayer variant.')

# GLOSSARY: golden rules, all named ability entries, all listed Sponsor entries,
# every final clarifier and every listed advanced-map clarifier.
for name, sections in [
 ('Self-counting icons, card-text precedence and double icons',['golden.icons']),
 ('Water/rock distinct adjacent hexes',['golden.terrain']),
 ('Immediate/simultaneous/after-finishing order',['Q10']),
 ('113–122 release play bonus, exact requirement, retained/lost benefits, freeing enclosure',['Q17','projects.release_reputation']),
 ('123–127 equal Breeding Program conditions',['projects.release_reputation'])]:
 cover('G01.'+str(len(entries)), 'Glossary p1',name,*sections)
ability_sections={
 'Action':'abilities.action_determination','Assertion':'abilities.assertion_dominance',
 'Boost':'abilities.boost_clever','Clever':'abilities.boost_clever',
 'Constriction':'abilities.constriction','Constriction low slots':'abilities.constriction_low_strength',
 'Determination':'abilities.action_determination','Digging':'abilities.digging',
 'Dominance':'abilities.assertion_dominance','Flock Animal':'abilities.flock',
 'Full-throated':'abilities.full_throated','Hunter':'abilities.hunter',
 'Hypnosis':'abilities.hypnosis','Hypnosis four upgrade examples':'abilities.hypnosis_upgrade_scope',
 'Jumping':'abilities.jumping','Multiplier':'abilities.multiplier',
 'Peacocking/Posturing':'abilities.peacocking_posturing','Petting Zoo animal':'abilities.petting',
 'Pilfering targets':'abilities.pilfering_target','Pilfering payment/repeat':'abilities.pilfering_payment',
 'Pouch/Sunbathing':'abilities.pouch_sunbathing','Resistance':'abilities.resistance',
 'Scavenging':'abilities.scavenging','Snapping/Sponsor Magnet':'abilities.snapping_magnet',
 'Venom':'abilities.venom'}
for name,sec in ability_sections.items():
 cover('GAB.'+name.lower().replace(' ','_').replace('/','_'), 'Glossary pp2–3',name,sec)
cover('G04.syntax','Glossary p4 Effect Syntax','Per-effect vs once/highest numerical threshold','glossary.effect_syntax')
cover('G04.terms','Glossary p4 Term Definitions','Connected/isolated/border/your zoo/any zoo','glossary.terms')
cover('G04.unique','Glossary p4 Unique buildings','Mandatory placement, cannot play if no fit, free, colored side, rotate not flip, not enclosures or terrain','glossary.unique_buildings')
cover('G04.effects','Glossary p4 Types of Effects','Permanent/recurring, break income, on-play and endgame effect timing','Q10','Q18','Q19','Q20',note='Background colors and strip are visual encoding; timing branches are assessed in the referenced questions.')
for row in rows:
 if row['coverage_section'].startswith('sponsor.'):
  for card in row['coverage_section'].removeprefix('sponsor.').split('_'):
   # Expand groups named by their range endpoints, maintaining one map row per card.
   cards=[card]
   if row['coverage_section']=='sponsor.231_235': cards=list(map(str,range(231,236))) if card=='231' else []
   if row['coverage_section']=='sponsor.236_240': cards=list(map(str,range(236,241))) if card=='236' else []
   for c in cards:
    cover('GSP.'+c, row['source_references'], 'Individual Sponsor '+c+' all listed immediate, recurring, income, final and exception clauses', row['coverage_section'])
exclude('GSP.223','Glossary pp4–7','Sponsor 223','No entry appears in the supplied glossary; no missing card text is invented. This is a source-document boundary, not exclusion of a printed procedural passage.')
cover('GF.004','Glossary p8','Architectural Zoo connected and building spaces','final.004_006')
cover('GF.005','Glossary p8','Conservation Zoo count by missing tokens','final.005')
cover('GF.006','Glossary p8','Naturalists Zoo building/upgrade spaces','final.004_006')
cover('GF.009','Glossary p8','Biodiverse Zoo absent right-neighbor category/cap; example','final.009')
for m in [1,2,4,5,6,7,8]:
 cover('GM.'+str(m),'Glossary p8','All Map '+str(m)+' clarification paragraphs/examples','map.'+str(m))
exclude('GM.3','Glossary p8','No additional Map 3 clarification passage','No Map 3 entry or legible Map 3 ability passage is supplied. General use of the chosen map special ability is covered in M06c; all actually supplied advanced-map passages are covered. No ability is inferred from another edition or strategy guide.')
exclude('G.credits','Glossary p8','Image credits','Nonprocedural credits.')

# FAQ: individual Q/A entries, including repeats, retained as source locations.
faq=[
 ('errata','FAQ p1','Shared relocation/release smallest fitting, size-only fallback, none fallback',['Q13','Q17']),
 ('boost','FAQ p1','Boost card shifts to1/5',['abilities.boost_clever']),
 ('interaction_alt','FAQ p1','Use alternate interaction effects',['abilities.interactive_eligibility']),
 ('hypnosis_tokens','FAQ p1','Hypnosis Constriction/Venom apply and clear, Multiplier forbidden',['abilities.hypnosis']),
 ('macaque','FAQ p1','Most conservation tie and minimum1',['abilities.pilfering_target']),
 ('multiplier_bonus','FAQ p1','Multiplier immediate placement',['abilities.multiplier']),
 ('partner_upgrade_bonus','FAQ p1','Third partner and map upgrade spaces remain gated via bonuses',['diagrams.partner_slots','map.8']),
 ('tiles_source','FAQ p1','Bonus zoo/university from Association board',['Q15']),
 ('sponsor_hand','FAQ p1','Pay-level bonus only from hand even SponsorsII',['faq.sponsor_bonus']),
 ('waza_small','FAQ p1','Display small animal even if no additional hand animal',['sponsor.228']),
 ('polar_end','FAQ p1','Other-turn appeal waits for own end/break',['Q20','sponsor.251']),
 ('native_border','FAQ p1','Terrain not empty border building spaces; upgrade spaces count',['sponsor.260']),
 ('water_hexes','FAQ p2','Adjacent actual hex vs connected area',['golden.terrain']),
 ('mapA_kiosk','FAQ p2','Printed kiosk already built and grants adjacency',['main.setup']),
 ('map2_size','FAQ p2','Cannot ignore effective+2 size for release/relocation',['map.2']),
 ('map5_special','FAQ p2','One free depicted special before upgrade',['map.5']),
 ('map8_partner','FAQ p2','Bonus partner and map-space upgrade gates',['map.8','diagrams.partner_slots']),
 ('upgrade_during','FAQ p2','Next-action new behavior, instant condition satisfaction',['main.upgrades']),
 ('bonus_reuse','FAQ p2','Use gained worker in later task, strength/kind locked',['Q10']),
 ('venom_x','FAQ p2','X-token alternative clears Venom except cap',['abilities.venom_x']),
 ('terrain_art','FAQ p2','Decorative illustrations do not count',['golden.terrain']),
 ('release_order','FAQ p2','Appeal loss before conservation gain',['Q17']),
 ('move_all','FAQ p2','May move all corresponding animals on special build',['Q13']),
 ('border','FAQ p3','At least1 of6 sides lacks another map hex',['glossary.terms']),
 ('break_refill','FAQ p3','Refill after each income player',['Q19']),
 ('caps','FAQ p3','Maximum113appeal/41conservation',['faq.track_caps']),
 ('partner_discount','FAQ p3','3per top continent,6double; conditions not icons',['Q11','golden.icons']),
 ('multiplier_stack','FAQ p3','Each token adds1action,2tokens=3',['abilities.multiplier_stacking_x']),
 ('multiplier_x','FAQ p3','2X actions allowed, mix with regular forbidden',['abilities.multiplier_stacking_x']),
 ('multiplier_animals','FAQ p3','Bonus token may go on Animals',['abilities.multiplier']),
 ('named_action_x','FAQ p3','Named action not X; Determination any action may',['abilities.action_determination'])]
for fid,ref,topic,qs in faq: cover('FAQ.'+fid,ref,topic,*qs)

# SUPPLEMENT: official English original-base icon aid, read in full.
icon=[
 ('continents_categories','Icon Overview p1 left','Five continent and seven category icons',['main.animal_categories','golden.icons']),
 ('sizes','Icon Overview p1 left','Small 1–2/petting; large4–5',['sponsor.227','sponsor.229_230']),
 ('strength_tracks_tokens','Icon Overview p1 middle','Strength/level/task, appeal/conservation/reputation/money/research/X and Multiplier',['Q03','Q14','Q18','abilities.multiplier']),
 ('worker_tiles','Icon Overview p1 middle','Hire worker and obtain partner/university from board',['abilities.full_throated','Q15']),
 ('support_hand_ignore','Icon Overview p1 middle','Support conservation; hand5; ignore1left condition',['Q16','Q15','icon.conditions']),
 ('buildings','Icon Overview p1 middle','Specific standard or special free immediate build, capacity numbers, terrain adjacency, kiosk/pavilion',['Q08','Q09','diagrams.special_capacity','golden.terrain']),
 ('draw_snap','Icon Overview p1 middle','Reputation display/deck choice vs any-display snap',['Q06','abilities.snapping_magnet']),
 ('conditions','Icon Overview p1 right','Owned vs condition icon, partner continent, upgraded action, max25, minimumrep',['golden.icons','icon.conditions','main.upgrades']),
 ('after_actions','Icon Overview p1 right','After-finishing Clever/Determination and upgrade in place',['abilities.boost_clever','abilities.action_determination','main.upgrades']),
 ('zoo_scope','Icon Overview p1 right','Your zoo versus any zoo triggering scope',['glossary.terms','sponsor.236_240','sponsor.208']),
 ('threshold_reminders','Icon Overview p2 left','5interaction marker and25card condition reminder',['abilities.interactive_eligibility','icon.conditions']),
 ('effect_timing','Icon Overview p2 left','Yellow immediate vs purple immediate+recurring, lightning/hourglass/hand',['Q16','Q10','Q19','Q20']),
 ('pouch_perception','Icon Overview p2 left','Pouch up toX hand cards2appeal, PerceptionX deck keep half',['icon.pouch_perception_sunbathing']),
 ('hunter','Icon Overview p2 left','RevealX keep1Animal discardrest',['sponsor.252','abilities.hunter']),
 ('sunbathing','Icon Overview p2 left','Sell up toX hand cards4each',['icon.pouch_perception_sunbathing']),
 ('sponsor_pay','Icon Overview p2 top right','Hand Sponsor pay level conditions, Action card unmoved',['faq.sponsor_bonus']),
 ('venom','Icon Overview p2 right','All higher appeal, lowest slots, duplicate/payment/removal',['icon.targets','abilities.venom']),
 ('hypnosis','Icon Overview p2 right','Highest appeal, onlyslots1–3, X allowed, move card1',['icon.targets','abilities.hypnosis']),
 ('pilfer','Icon Overview p2 right','Pilfer1highestappeal;2highestappeal and mostconservation;self no effect',['icon.targets','abilities.pilfering_payment']),
 ('constriction','Icon Overview p2 right','All ahead1/bothtracks, highestslots1/2tokens,reduce2,removal',['icon.targets','abilities.constriction']),
 ('action_icons','Icon Overview p2 bottom','Any action and five named actions, either side',['abilities.action_determination'])]
for fid,ref,topic,qs in icon: cover('IO.'+fid,ref,topic,*qs)

def write_map():
    output={'game':'Ark Nova','scope':'Original English base v1.2 main + base glossary + official base FAQ + accepted official English base Icon Overview. Original component images supplement hidden Animals II numeric cells and tiny reputation-board numerals only. No solo, Marine Worlds or strategy-guide authority.',
            'authoring_role':'Question-bank author; this is a source coverage map, not an independent final audit.',
            'source_boundaries':{'canonical_sources_unchanged':True,'component_numeric_supplement':'Accepted matching original publisher German component photographs resolve hidden Animals II strengths1–3; matching publisher board photograph corroborates tiny English reputation-track numerals. See table-source-check/followup-source-report.json and reputation-map-source-report.json. No German revised rules prose adopted.','icon_overview':'Accepted original official English base rules aid separately downloaded by parent. See table-source-check/evidence-manifest.json.','no_rules_inferred_from_nonpacket_card_or_map_text':True},
            'passages':entries}
    assert len({e['passage_id'] for e in entries})==len(entries)
    all_ids={f'Q{i:02}' for i in range(1,21)}|{r['id'] for r in rows}
    assert all(set(e['question_ids'])<=all_ids for e in entries)
    (HERE/'coverage-map.json').write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
    print(f'{len(entries)} source passage records; {sum(e["disposition"]=="covered" for e in entries)} covered; {sum(e["disposition"]=="excluded" for e in entries)} explicit exclusions')

if __name__=='__main__':
    write_outputs();write_map()
