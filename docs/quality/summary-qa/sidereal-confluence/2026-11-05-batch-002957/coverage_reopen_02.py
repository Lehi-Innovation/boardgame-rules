from build_bank import ROOT,write
import json,copy,shutil
q=json.loads((ROOT/'expanded-v3/questions.json').read_text())['questions'];k=json.loads((ROOT/'expanded-v3/answer-key.json').read_text())['answers'];rows=[dict(a,question=b['question']) for a,b in zip(k,q)];before=copy.deepcopy(rows)
for e in rows:
 fs=e['required_facts'];ctx=e['contextual_background'];i=e['id']
 if i=='Q14':
  next(f for f in fs if f['id']=='Q14.F04')['fact']='Detector additional converter costs one colony of any climate and three green cubes'
  ctx.append('Consumed ordinary colony goes beneath colony deck; destination not independently asked by this cost clause (tested separately by Q28).')
 if i=='Q22':
  next(f for f in fs if f['id']=='Q22.F04')['fact']='Initial research-team track dealt from technology deck lowest minimum bid upward'
  ctx.append('Initial colony track is likewise dealt lowest minimum upward; same track-filling procedure, not a separate asked technology-deck clause.')
 if i=='Q37':
  ctx.append('Network holder gains two additional Colony Support; numeric support amount is not independently asked.')
  e['required_facts']=[f for f in fs if f['id']!='Q37.F03']
 if i=='Q51':
  next(f for f in fs if f['id']=='Q51.F02')['fact']='Named-card route flips the target'
  ctx.append('Spent card goes underneath target; destination is asked separately by Q05, not this target-flip clause.')
def add(question,answer,facts,refs,novelty):
 i=f'Q{len(rows)+1:02}';rows.append({'id':i,'question':question,'expected_answer':answer,'required_facts':[{'id':f'{i}.F{j+1:02}','fact':f} for j,f in enumerate(facts)],'contextual_background':[],'source_references':refs,'novelty':novelty})
add('May Faderan trade its Acknowledgment tokens to other players during the Trade Phase?',
 'Yes. Faderan may trade Acknowledgment tokens to other players during Trade.',
 ['Faderan may trade its Acknowledgment tokens to others during Trade'],['Faderan original front Acknowledgements, first two sentences; Booklet Trade phase'],'Positive Faderan-only token distribution permission, distinct from non-Faderan circulation prohibition')
add('For a cheaper Zeth stealing-input option conditional on envoy tokens, whose token holdings determine eligibility? If the intended target has no envoy tokens, do tokens still in Zeth’s stash alone unlock that envoy-conditioned discount?',
 'The intended theft target must hold the envoy tokens specified by the input option. Tokens in Zeth’s stash do not qualify an unmarked target for an envoy-conditioned cheaper input.',
 ['Envoy-conditioned cheaper input depends on tokens held by intended theft target','Zeth stash alone does not qualify target with no envoy tokens'],['Zeth original front Theft, paragraph beginning All stealing converters'],'Actor-specific condition for cheaper stealing input, not merely token non-consumption')
assert all(a['question']==b['question'] and a['expected_answer']==b['expected_answer'] for a,b in zip(rows,before))
write('expanded-v4',rows)
(ROOT/'expanded-v4/coverage-scope-correction-record.json').write_text(json.dumps({'review':'../expanded-v3/coverage-scope-review.json','previous_versions_preserved':True,'existing73_question_and_expected_answer_text_unchanged':True,'actual_asked_scope_corrections':[{'id':a['id'],'before':b,'after':a} for a,b in zip(rows,before) if a!=b],'additions':['Q74','Q75'],'reader_feedback_used':False,'expanded_reader_dispatches_so_far':0},ensure_ascii=False,indent=2)+'\n')
shutil.copyfile(ROOT/'coverage-ledger.json',ROOT/'expanded-v3/parent-coverage-ledger-before-renewed-challenge.json');shutil.copyfile(ROOT/'coverage-map.md',ROOT/'expanded-v3/parent-coverage-map-before-renewed-challenge.md');x=json.loads((ROOT/'coverage-ledger.json').read_text());x['benchmark_version']='expanded-v4';x['question_count']=75;x['independent_challenge_history'].append({'review':'expanded-v3/coverage-scope-review.json','verdict':'NOT_SATURATED','accepted_new_question_ids':['Q74','Q75'],'scope_corrections':['Q14','Q22','Q37','Q51']});km={e['id']:e for e in rows}
for u in x['core_procedural_units']:
 if u['source_procedural_unit'].startswith('Faderan Acknowledgments') and 'Q74' not in u['questions']:u['questions'].append('Q74')
 if u['source_procedural_unit'].startswith('Zeth last-of-turn') and 'Q75' not in u['questions']:u['questions'].append('Q75')
 u['actually_asked_fact_ids']=[f['id'] for i in u['questions'] for f in km[i]['required_facts']]
for e in rows[73:]:x['accepted_questions'].append({'id':e['id'],'wording':e['question'],'novelty':e['novelty'],'source_references':e['source_references']})
x['passes'] += [{'pass':9,'focus':'New fresh independent73-question/source challenge','new_questions':['Q74','Q75'],'status':'Two real source permissions/conditions accepted; reset stopping check; four scope atoms corrected'},{'pass':10,'focus':'Rewalk all source actor permissions and eligibility conditions, including who distributes tokens and whose holdings unlock options','accepted_count':0,'new_questions':[],'reason':'Every source actor/cost/trigger/conditional outcome is now actually asked; changed token counts and other resource quantities repeat covered branches.'},{'pass':11,'focus':'Rewalk entire original booklet and all9 sheets plus accepted components/designer clarifications for procedure destinations, endgame, positivity and exceptions','accepted_count':0,'new_questions':[],'reason':'No new source-defined rule/outcome/timing/priority/exception beyond75; ordinary numerical component values and cosmetic recombinations rejected.'}]
x['coverage_stopping_rule']={'all_core_procedural_groups_mapped':True,'consecutive_zero_addition_passes':2,'fresh_independent_challenge':'pending final fresh expanded-v4 challenge','working_saturation_only':True};(ROOT/'coverage-ledger.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
text='# Sidereal Confluence source coverage\n\nCurrent expanded-v4 contains75 questions. Earlier independent challenges and all failed stopping claims are preserved. Passes10 and11 added zero after the final actor/eligibility additions. Final independent challenge pending.\n\n'
for u in x['core_procedural_units']:text+='- '+u['source_procedural_unit']+': '+', '.join(u['questions'])+'.\n'
text+='\nExact sources, asked-fact IDs, novelty/rejections and pass history are in coverage-ledger.json. Context alone earns no coverage credit.\n';(ROOT/'coverage-map.md').write_text(text)
print('expanded-v4',len(rows),'required facts',sum(len(e['required_facts']) for e in rows))
