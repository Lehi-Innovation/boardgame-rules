from pathlib import Path
import json,hashlib,copy
P=Path(__file__).parent
q=json.loads((P/'bank-v2/questions.json').read_text());k=json.loads((P/'bank-v2/answer-key.json').read_text());r=json.loads((P/'coverage-review.json').read_text())
new=[]
for x in r['proposed_questions']:new.append({'id':x['proposed_id'],'question':x['question'],'expected_answer':x['expected_answer'],'source_references':x['source_references'],'novelty':x['novelty']})
new.extend([
{'id':'Q53','question':'How many victory points does each remaining coin score at the end of the game?', 'expected_answer':'Each coin is worth 1 victory point.','source_references':['p.19; extraction line321'],'novelty':'Coin VP is an independent scoring source. Q20 key mentions it incidentally, but its prompt does not ask for it; independent review clarified not to grade unrequested facts as required.'},
{'id':'Q54','question':'Before any track advancement, what are your initial Development Status and Knight-track draw allowance?', 'expected_answer':'Initial Development Status is1; initial Knight draw allowance is4 Followers (subject to free Market capacity).','source_references':['p.19 lines311–313; p.14 lines135–139; p.17 lines243–249'],'novelty':'Tests the initial Development Status branch before a later threshold is reached; earlier questions test changes and current Status-based rewards. Starting Knight allowance is supporting initial-state context.'},
{'id':'Q55','question':'After torture, which lost asset type can be regained, and do surrendered goods, Followers, stations, Places or Technology return to their supplies?', 'expected_answer':'Only lost Development Points can be regained. All surrendered physical items are removed from game, not returned to supplies, so cannot become available there again through normal return effects.','source_references':['p.21 lines364–377'],'novelty':'Explicit recovery exception for Development Points; Q18 asks payment/destinations, and independent adjudication treated later Development recovery as incidental rather than a requested part.'}
])
for x in new:
 q['questions'].append({z:x[z] for z in ['id','question']});k['answers'].append({z:x[z] for z in ['id','expected_answer','source_references','novelty']})
q['benchmark_version']=k['benchmark_version']='bank-v3';d=P/'bank-v3';d.mkdir()
for name,obj in [('questions.json',q),('answer-key.json',k)]: (d/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
qm={x['id']:x['question'] for x in q['questions']}
(d/'question-bank.md').write_text('# Orléans bank-v3:55 questions\n\n'+q['scope']+'\n\n'+'\n\n'.join(f"## {x['id']}\n\n{qm[x['id']]}\n\n**Answer:** {x['expected_answer']}\n\n**Source:** {'; '.join(x['source_references'])}\n\n**Distinct coverage:** {x['novelty']}" for x in k['answers'])+'\n')
(d/'benchmark-hashes.json').write_text(json.dumps({x:hashlib.sha256((d/x).read_bytes()).hexdigest() for x in ['questions.json','answer-key.json']},indent=2)+'\n')
l=json.loads((P/'coverage-ledger.json').read_text());l['benchmark_version']='bank-v3';l['question_count']=55;l['previous_ledger']='coverage-ledger.json';l['independent_challenge']='coverage-review.json';l['accepted_additions'].extend(k['answers'][50:]);l['passes'].extend([
{'pass':4,'focus':'Resolve independent challenge and inspect incidental-key facts for unrequested procedures','added_ids':[x['id'] for x in new],'added_count':5,'rationale':'Independent Q51–52 plus parent follow-through Q53–55; keys unchanged for original50.'},
{'pass':5,'focus':'Target setup/end-state branches, individual scoring sources and irreversible-loss/recovery exceptions after challenge additions','added_ids':[],'added_count':0,'core_passages_mapped':True},
{'pass':6,'focus':'Re-read all procedural passages and diagrams; challenge remaining timing/outcome conditions and reject covered/unsupported variants','added_ids':[],'added_count':0,'core_passages_mapped':True}]);l['coverage_map'].extend([
{'source_passage':'pp12–14 lines36–40,99–103,123–125','procedure':'Hour Glass stack randomization/orientation and reveal','questions':['Q52']},
{'source_passage':'p19 lines318–330','procedure':'Unique-most Citizen branch and coin scoring','questions':['Q51','Q53']},
{'source_passage':'p19 lines311–313; p14 lines135–139','procedure':'Initial Development Status and supporting starting Knight allowance','questions':['Q54']},
{'source_passage':'p21 line377','procedure':'Development recovery exception after torture','questions':['Q55']}]);l['rejections'].extend([
{'candidate':'A distinct initial Knight allowance question','reason':'Included as supporting context Q54; further numeric draw scenarios repeat Q02.'},
{'candidate':'A higher/lower DevelopmentStatus value after different threshold','reason':'Threshold changes Q13 and Status-based payouts Q32/Q38 already covered; initial branch now Q54.'},
{'candidate':'Different recipient of unique-most final Citizen','reason':'Same unique-leader branch Q51; player names/counts do not add a rule.'},
{'candidate':'Reorder narrative of HourGlass setup','reason':'Q52 now directly tests all operative randomization/reveal steps.'},
{'candidate':'Torture of different physical tile followed by supply-return effect','reason':'Same permanent-removal versus Development recovery exception now Q18/Q55.'}]);
(P/'coverage-ledger-v3.json').write_text(json.dumps(l,ensure_ascii=False,indent=2)+'\n')
