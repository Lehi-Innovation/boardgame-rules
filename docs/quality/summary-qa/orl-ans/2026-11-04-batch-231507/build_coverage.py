from pathlib import Path
import json
P=Path(__file__).parent;key=json.loads((P/'bank-v2/answer-key.json').read_text())
coverage=[
('pp12–13 lines15–111','Personal and shared setup; first event; all player-count reductions',['Q08','Q15','Q21','Q22','Q23']),
('p12 player-board illustration','All ten printed core activation costs',['Q14','Q24','Q25','Q26']),
('p14 lines120–127','Youngest starts, 18 rounds, event reveal and exceptional timing',['Q15','Q21','Q29','Q30']),
('p14 lines129–133','Census track comparison, unique/tied leaders/last, two-player exception',['Q01','Q31','Q50']),
('p14 lines135–144','Optional bounded draws, Market space and retained tiles, Planning',['Q02','Q03','Q29']),
('p15 lines154–170','Activation over rounds, one action/pass rotation, destinations, saving activations',['Q03','Q04','Q07','Q43']),
('p15 lines171–175','Event resolution and Start Player transfer',['Q15','Q29','Q30']),
('p16 lines180–201','Core activation/recruitment; Farmer and Boatman rewards',['Q05','Q06','Q24']),
('p16 lines202–218','Craftsman and all Technology timing/permanence/placement restrictions',['Q06','Q07','Q40']),
('p17 lines224–236','Trader recruitment, Place categories and inspectable stacks',['Q06','Q08','Q24']),
('p17 lines237–260','Scholar/Knight/Monk recruitment, fourth Knight plateau, final-track limits, wild/reverse restriction',['Q09','Q10','Q24']),
('p18 lines263–278','Ship/Wagon route distance/collection; Guildhall location/occupancy/Orléans; Scriptorium',['Q11','Q12','Q13','Q25','Q26']),
('p18 lines279–296','Town Hall one/two, exact Deed types, permanent destinations, rewards, completion, marked restriction',['Q10','Q14','Q26','Q48','Q49']),
('p19 lines306–316','Development rewards on landing/passing and immediate Status',['Q13','Q32','Q38']),
('p19 lines317–335','Game end, unique final Citizen, full scoring/tiebreak',['Q20','Q30']),
('p20 lines343–361','All six events and their distinct payment/loss/timing branches',['Q15','Q16','Q17','Q32','Q33','Q34','Q44','Q45']),
('p21 lines364–377','Torture payment alternatives, random redraw, DP floor, loss destinations',['Q18']),
('p21 lines379–383','Finite tile supply, multi-effect action unavailable, stock restored, coin shortage',['Q19','Q35']),
('p21 lines384–386','Bag inspection and reshuffle',['Q28']),
('p21 lines387–391','Empty links and protected starting Followers',['Q10','Q11','Q14','Q17','Q18','Q49']),
('p21 lines392–395','Assigned Follower recovery in Phase3, declined-draw exchange, no direct reassignment',['Q27']),
('p21 lines396–401','Common coin destinations, simultaneous planning, announce done, ordered payments',['Q29']),
('p22 lines405–451 and tile illustrations','Five goods producers; Shipping Line/Brewery/Windmill/Library; Pharmacy; Cellar/Office; activation costs',['Q35','Q36','Q37','Q38']),
('p23 lines454–549 and tile illustrations','Sacristy/Lab/Tower/Herb Garden/Hospital/School/Horse Wagon/Bathhouse; all costs and branches',['Q38','Q39','Q40','Q41','Q42','Q43','Q44','Q45','Q46','Q47','Q48','Q49']),
('p24 lines594–626','Components: no standalone count trivia; setup quantities included',['Q21','Q22','Q23'])]
rejected=[
{'candidate':'Another Ship example with three goods instead of two','reason':'Same one-connection, choose-one branch as Q11.'},
{'candidate':'Repeat Market constraint using different allowance/capacity','reason':'Changed numbers within Q02; no new outcome branch.'},
{'candidate':'A second first-Technology scenario at another Farmer space','reason':'Same first-Farmer restriction and one-per-Place constraints as Q07/Q40.'},
{'candidate':'Town Hall completion race with a different named Deed','reason':'Action priority and last-slot reward already Q04/Q14; mechanical recombination without new exception.'},
{'candidate':'Put Technology on Hayrick, Brewery, or Pharmacy','reason':'Single-Follower Place ban already Q07; cosmetic destination changes.'},
{'candidate':'Herb Garden Boatman on a Farmer action with different ingredients','reason':'Same substitution set as Q46.'},
{'candidate':'Change Tax goods count from eight to eleven','reason':'Same complete-group rounding branch as Q33.'},
{'candidate':'Sacrifice a different mix of items for four missing coins','reason':'Same per-missing-coin choices as Q18.'},
{'candidate':'All players tied in Census','reason':'Composition of covered tied-lead and tied-last branches Q01/Q50; no additional exception.'},
{'candidate':'Office income with two built stations instead of four','reason':'Variable built-only payout already Q38.'},
{'candidate':'Final tied score with identical Development Status but different exact track positions','reason':'Q20 explicitly keys actual track-position tiebreak; numerical example adds no rule.'},
{'candidate':'Bathhouse newer revised timing or updated tile errata','reason':'Different edition/rules; original matching 2014 booklet specifically selected.'},
{'candidate':'Pregame exclusion of Places by experienced players','reason':'Explicit optional mode excluded by assigned scope; p19 lines336–339.'},
{'candidate':'Five-player or invasion/cooperative/event expansion rules','reason':'Outside 2–4 player 2014 base-game source.'},
{'candidate':'Plague draw with an empty bag or torture with no eligible neutral follower','reason':'No explicit ruling in this edition for these speculative boundary cases; no source-backed answer invented. Would require a matching official clarification if such a ruling is requested; not an omitted source procedure.'},
{'candidate':'More questions for component-count trivia or medieval-France narrative','reason':'Not consequential procedural coverage.'}]
ledger={'benchmark_version':'bank-v2','question_count':len(key['answers']),'novelty_standard':'New rule, rule-defined outcome branch, or consequential timing/priority/exception interaction; no cosmetic variants or mechanical recombinations.','coverage_map':[{'source_passage':a,'procedure':b,'questions':c} for a,b,c in coverage],'accepted_additions':key['answers'][20:],'passes':[{'pass':1,'focus':'Complete setup, action-cost diagrams, remaining general procedures/events and all 20 base Places','added_ids':[f'Q{i:02}' for i in range(21,51)],'added_count':30},{'pass':2,'focus':'Re-read all mapped core passages; challenge payment boundaries, identity protection, technology, routes and activated Place timing','added_ids':[],'added_count':0,'core_passages_mapped':True},{'pass':3,'focus':'Second complete procedural/source-diagram pass; challenge alternate outcomes and exceptions across all phases and base Places','added_ids':[],'added_count':0,'core_passages_mapped':True}],'rejections':rejected,'excluded_source_passages':[{'source':'p19 lines336–339','reason':'Optional pregame Place exclusion; explicitly excluded'},{'source':'p24 credits/promotions and pp1 contents','reason':'Nonprocedural'},{'source':'German parallel text of pp22–23','reason':'Parallel explanations checked as needed; English is the assigned language'}],'scope_limit':'Working saturation under this edition/source and novelty standard, not every conceivable scenario.'}
(P/'coverage-ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
