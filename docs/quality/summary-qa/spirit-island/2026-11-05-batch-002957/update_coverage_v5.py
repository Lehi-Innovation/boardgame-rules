from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).parent;p=B/'coverage-ledger.json';shutil.copyfile(p,B/'coverage-ledger-after-challenge-01-before-expansion.json');j=json.loads(p.read_text());r=json.loads((B/'coverage-review-01.json').read_text());new=json.loads((B/'expanded-v5/novelty.json').read_text());j['benchmark']='expanded-v5';j['question_count']=112
for a in j['acceptance_ledger']:
 if a['id']=='Q32':a['reason']='Retained earlier frozen regression. The asked replacement survival outcome repeats Q18; do not count new coverage.'
for a in new:j['acceptance_ledger'].append({**a,'bank':'expanded-v5','decision':'accepted','origin':'independent challenge 01' if a['id']!='Q112' else 'parent reopened procedural sweep'})
ids={f'C{i:02}':f'Q{103+i}' for i in range(1,9)}
j['precise_clause_mappings']=j.get('precise_clause_mappings',[])
for c in r['proposed_additions']:
 i=ids[c['candidate_id']];j['precise_clause_mappings'].append({'topic':c['topic'],'source_refs':c['source_refs'],'question_ids':[i],'tested_clause':next(a['new_coverage'] for a in new if a['id']==i)})
 j['faq_rulings'].append({'ruling_id':'challenge01-'+c['candidate_id'],'rule':c['predetermined_answer'],'source_refs':c['source_refs'],'question_ids':[i],'scope':'included','reason':'Precise previously unasked source clause, now explicitly tested.'})
for item in r['mapping_audit']['map_only_repairs']:
 j['faq_rulings'].append({'ruling_id':'direct-'+item['existing_question'],'rule':item['action'],'source_refs':[item['source']],'question_ids':[item['existing_question']],'scope':'included','reason':'Map-only repair; existing frozen question and key already test this.'})
for x in j['faq_rulings']:
 if x['ruling_id']=='repeat-new-power':x['question_ids']=['Q107']
 if x['ruling_id']=='bringer-real-effects':x['question_ids']=list(dict.fromkeys(x['question_ids']+['Q104']))
 if x['ruling_id']=='shadows-range':x['question_ids']=list(dict.fromkeys(x['question_ids']+['Q105']))
 if x['ruling_id']=='repeat-boost':x['question_ids']=list(dict.fromkeys(x['question_ids']+['Q106']))
for row in j['book_passages']:
 extra={'Blight setup':['Q109'],'Island and supply setup':['Q112'],'Presence and Sacred Sites':['Q108'],'Innates':['Q110'],'Dahan':['Q110'],'One target/turn/use':['Q111'],'Repeat':['Q107']}.get(row['passage'],[])
 row['question_ids']=list(dict.fromkeys(row['question_ids']+extra))
j['precise_clause_mappings'].append({'topic':'Island and supply shared setup','source_refs':['CORE p.6 Island and Supply'],'question_ids':['Q112'],'tested_clause':new[-1]['new_coverage']})
j['independent_challenge_history']=[{'report':'coverage-review-01.json','verdict':r['verdict'],'key_verdict':r['key_verdict'],'accepted_additions':8,'resolved_by_ids':[f'Q{i}' for i in range(104,112)],'prior_zero_pass_claim_revoked':True}]
j['passes'] += [{'pass':7,'focus':'Fresh independent source/key challenge; actual prompt clauses versus broad map labels','new_questions':8,'ids':'Q104–Q111','review':'coverage-review-01.json'},{'pass':8,'focus':'Reopened initial island population and shared supplies sweep','new_questions':1,'ids':'Q112'},{'pass':9,'focus':'All setup, Growth, resources, Powers, Innates, geography, Presence and supply source clauses against actual prompts/keys','new_questions':0},{'pass':10,'focus':'All Invader/Fear/Blight procedures, timing, outcome branches and original Spirit/card exceptions; reject equivalent cases','new_questions':0}]
j['rejection_ledger'] += [
 {'pass':9,'candidate':'Randomizing another setup stack as standalone question','decision':'rejected','because':'Q01 handles deck randomization; Q109 specifically adds hidden random Blight procedure. Minor/Major separate setup is included in the genuinely new shared-island/supply Q112 rather than counted separately.'},
 {'pass':9,'candidate':'Power at distance1 instead of2, or at its source','decision':'rejected','because':'Maximum versus exact Range already probed by Q21 (Range0 counts withinRange1); changing distances supplies no new branch.'},
 {'pass':9,'candidate':'Another normal card pay/use count or innate Energy count','decision':'rejected','because':'New Q110/Q111 directly cover costs/availability and normal one-use restrictions; surplus resources do not alter ruling.'},
 {'pass':9,'candidate':'Another internal Range-arrow or Repeat threshold number','decision':'rejected','because':'Q105/Q106 cover general versus targeting-only and retained-but-not-stacked thresholds, including old wording exception.'},
 {'pass':10,'candidate':'Q73 novelty rejection based solely on extra Q15 key explanation','decision':'rejected challenge','because':'Q15 actual prompt never requests consistently lowering Elements or refusing a lower level while retaining a higher one. Q73 uniquely asks that branch. Independent reviewer reconsidered and retained novelty.'},
 {'pass':10,'candidate':'Ocean/Vengeance/Bringer recursive concrete chain','decision':'rejected','because':'Q89 tests indirect self-trigger prohibition; Q80/Q81 cleanup. Pure recombination without a new rule.'},
 {'pass':10,'candidate':'Trade Suffers same-piece repeated downgrade','decision':'rejected','because':'Q51/Q99 cover sequential each-player choice and repeated piece decisions; expansion simultaneous-upgrade cases excluded.'},
 {'pass':10,'candidate':'Further Fear totals, Blight cascades, damaged-piece values or player counts','decision':'rejected','because':'Existing defined branches Q06/Q11/Q13/Q18/Q31/Q44–47/Q79/Q82–86; changed numbers alone do not qualify.'},
 {'pass':10,'candidate':'Simultaneous multi-Blight Presence-loss producer','decision':'not added','because':'No additional original-core producer established in assigned source; do not import excluded Sweden/expansion examples. Q94 preserves explicit source pool-transition rule.'},
 {'pass':10,'candidate':'Any optional timeboxing, scoring, difficulty modules, thematic maps, Events/Aspects','decision':'excluded','because':'Playstyle/reference advice or explicitly excluded modules, not another standard-core procedural outcome.'}
]
j['stopping_rule']={'consecutive_zero_addition_passes':[9,10],'all_in_scope_procedural_passages_mapped':True,'independent_challenge':'pending-new-fresh-review','claim':'Working saturation only within documented sources/scope and novelty criteria. First stopping claim was independently rejected and is preserved.'}
j['input_hashes']={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [B/'expanded-v5/questions.json',B/'expanded-v5/answer-key.json',Path('extracted/spirit-island-rules.txt')]}
p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
# Complete compact map for fresh reviewer: current source mapping and stopping criterion, without earlier review conclusions or summary/readers.
compact={'benchmark':j['benchmark'],'question_count':112,'source_hierarchy':j['source_hierarchy'],'novelty_policy':j['novelty_policy'],'stopping_rule':j['stopping_rule'],'book_passages':j['book_passages'],'faq_rulings':[{'ruling_id':x['ruling_id'],'rule':x['rule'],'question_ids':x['question_ids'],'scope':x['scope'],'reason':x.get('reason'),'source_refs':[{'label':s.get('entry_anchor',s.get('label')),'file':s['file'],'range':s.get('character_range',s.get('anchor_character_range'))} if isinstance(s,dict) else s for s in x['source_refs']]} for x in j['faq_rulings']],'precise_clause_mappings':j['precise_clause_mappings'],'retained_non_novel_regressions':['Q32','Q100'],'last_targeted_passes':j['passes'][-2:],'last_rejections':j['rejection_ledger'][-10:]}
(B/'coverage-map-for-review-02.json').write_text(json.dumps(compact,indent=2,ensure_ascii=False)+'\n')
p=B/'progress.json';v=json.loads(p.read_text());v.update(phase='expanded-bank-frozen-independent-coverage-review-02',question_count=112);v['coverage_review']={'status':'pending','path':str((B/'coverage-review-02.json').resolve()),'benchmark':'expanded-v5','question_count':112,'prior_review':'coverage-review-01.json: eight gaps, all resolved with Q104–Q111'};v['coverage_stopping_rule']={'passes':[9,10],'new_questions':[0,0],'independent_challenge':'pending'};v['source_audit'].update(candidate_path=str((B/'source-candidate-04.md').resolve()),path=str((B/'source-audit-final-03.json').resolve()));p.write_text(json.dumps(v,indent=2)+'\n')
print('Updated full and compact maps. Compact characters:',len((B/'coverage-map-for-review-02.json').read_text()))
