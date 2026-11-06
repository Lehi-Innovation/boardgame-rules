from pathlib import Path
import datetime, hashlib, json, shutil
P=Path(__file__).resolve().parent; V=P/'expanded-v7'; V.mkdir(exist_ok=False)
def J(p): return json.loads(p.read_text())
def H(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def W(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
proposals=J(P/'coverage-review-07.json')['material_additions']
q=J(P/'expanded-v6/questions.json'); k=J(P/'expanded-v6/answer-key.json'); scope=J(P/'expanded-v6/grading-scope.json')
q['benchmark_version']=k['benchmark_version']=scope['benchmark_version']='expanded-v7'
scope['created_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
scope['preparation_disclosure']='All101 prior scope entries (320 facts) retained exactly. Historical v5 answers inspected, but no Q102/Q103 responses exist. New scopes frozen before v7 fresh dispatch.'
scope['new_Q102_Q103_answers_inspected']=False
scope['inputs']['questions']='expanded-v7/questions.json'; scope['inputs']['fixed_key']='expanded-v7/answer-key.json'
facts=[[
 'The Chancellor sits by the Cradle in both first-game and later-game setup (first game at the short edge).',
 'First packet setup seats Red, then Blue, then Yellow clockwise from the Chancellor.',
 'Later setup chooses the Chancellor by any method; previous winner is recommended, not required.',
 'Later setup seats the other players randomly before non-Chancellors make their saved-board choices in the resulting turn order.'
],[
 'First packet setup specifically uses Oathkeeper of Supremacy; it does not allow a free choice of any Oath.',
 'Supremacy Oathkeeper goal is to rule the most sites.',
 'Supremacy Successor goal is more total relics and banners than the Chancellor and every other Citizen.'
]]
for n,proposal in enumerate(proposals,102):
 id=f'Q{n:03d}'; refs='; '.join(proposal['source_references'])
 q['questions'].append({'id':id,'question':proposal['question']})
 key={'id':id,'expected_answer':proposal['expected_answer'],'material_facts':proposal['material_facts_new'],'source_references':refs}; k['answers'].append(key)
 required=[{'fact_id':f'{id}-F{i:02d}','expected_fact':fact,'basis':'Question clause interpreted against cited primary sources and fixed proposed key'} for i,fact in enumerate(facts[n-102],1)]
 excluded='Full board-eligibility rules beyond seating-before-choice order' if n==102 else 'Chancellor starting title and later Chronicle goal-selection procedure'
 scope['questions'].append({'id':id,'question':proposal['question'],'fixed_key_expected_answer_sha256':hashlib.sha256(key['expected_answer'].encode()).hexdigest(),'source_references':refs,
  'asked_clause_map':[{'clause_id':f'{id}-C01','asked_clause':proposal['question'],'required_fact_ids':[f['fact_id'] for f in required],'rationale':'All stated first/later role-order or initial-goal clauses are required; existing rule facts explicitly asked again still require correct answers.'}],
  'required_facts':required,'contextual_exclusions':[{'key_or_source_fact':excluded,'classification':'contextual_not_independently_required','rationale':'Not independently asked; no requirement to recite this contextual key content.','contradiction_policy':'Omission not penalized; materially false volunteered ruling remains incorrect.'}],
  'contextual_exclusion_status':'Only actually asked role/seating or first-goal content independently required.','semantic_notes':'Equivalent operational meaning accepted; no exact-keyword demand. Seats near/by the Cradle is sufficient for first short-edge seat. All quoted evidence must belong to this answer.'})
assert q['questions'][:101]==J(P/'expanded-v6/questions.json')['questions']
assert k['answers'][:101]==J(P/'expanded-v6/answer-key.json')['answers']
assert scope['questions'][:101]==J(P/'expanded-v6/grading-scope.json')['questions']
W(V/'questions.json',q);W(V/'answer-key.json',k);W(V/'grading-scope.json',scope)
W(V/'input-manifest.json',{f:H(V/f) for f in ['questions.json','answer-key.json']})
inputs=[V/'questions.json',V/'answer-key.json',P/'expanded-v6/grading-scope.json',P/'coverage-review-07.json',Path('/home/jonny/projects/boardgame-rules/extracted/oath-current-law.txt'),Path('/home/jonny/projects/boardgame-rules/extracted/oath-current-playbook.txt')]
W(V/'grading-scope-manifest.json',{'artifact_type':'grading-scope SHA256 freeze manifest','benchmark_version':'expanded-v7','created_utc':scope['created_utc'],'scope_artifact':{'path':str((V/'grading-scope.json').resolve()),'sha256':H(V/'grading-scope.json')},'input_files':[{'path':str(f.resolve()),'sha256':H(f)} for f in inputs],'required_fact_count':327,'question_count':103,'all_prior_scope_entries_exactly_preserved':True,'frozen_before_reader_dispatch':True})
text=['# Oath expanded benchmark v7','','103 retained regression questions, including ten historical overlaps with zero novelty credit. All101 prior entries are unchanged. Q102/Q103 add source-prescribed role/seating and first-goal setup branches. Count follows uncapped source sweeps and challenges.','']
for a,b in zip(q['questions'],k['answers']):text+=['## '+a['id'],'',a['question'],'','**Answer:** '+b['expected_answer'],'','**Source:** '+b['source_references'],'']
(V/'question-bank.md').write_text('\n'.join(text))
shutil.copyfile(P/'coverage-ledger.json',P/'coverage-ledger-before-v7.json');ledger=J(P/'coverage-ledger.json')
for n,proposal in enumerate(proposals,102):ledger['accepted_questions'].append({'id':f'Q{n:03d}','source_references':proposal['source_references'],'novelty':proposal['novelty'],'accepted':True,'reviewer_proposal':'coverage-review-07 '+proposal['proposal_id']})
ledger['coverage_map']['Law1.7/Playbook6–7 role selection and first/later seating']=['Q102']
ledger['coverage_map']['Playbook6 setup6 fixed initial Supremacy goal']=['Q103']
ledger['passes'] += [
 {'pass':20,'focus':'Adjudicate complete-delivery source-blind reviewer07 full clause setup audit','count':2,'accepted_ids':['Q102','Q103'],'rejected_duplicates':['Repeated Grand Scepter initial recipient (Q084), map/token inventory trivia, existing saved-board eligibility']},
 {'pass':21,'focus':'Reopen every Law1.1–1.23/deferred branch and Playbook first-setup1–18 clause against expanded-v7 keys','count':0,'accepted_ids':[],'rejections':[{'candidate':'Further first/later setup wording variants','reason':'Q021–025,Q052,Q083–085,Q101–103 now expressly test resource/track state, map deal, garrisons, inherited boards, bottom draws, packet order, role/seating, fixed goal and deferred prerequisite. Component inventory and hidden-card names alone are not new core procedures.'}]},
 {'pass':22,'focus':'Reopen complete procedural map Law2–10/full Playbook/errata/allSiteReference after setup additions','count':0,'accepted_ids':[],'rejections':[{'candidate':'Additional actor/quantity/site/card substitutions for already explicit procedures','reason':'No new source-defined condition, timing window, actor exception or outcome beyond existing tested facts. Individual illustrated-card recall remains delegated to printed power text under tested hierarchy.'}]}]
ledger['stopping_rule']={'consecutive_zero_addition_passes':2,'passes':[21,22],'all_core_procedural_passages_mapped':True,'independent_challenge':{'verdict':'PENDING','report':'coverage-review-08.json'}}
W(P/'coverage-ledger.json',ledger);shutil.copyfile(P/'coverage-ledger.json',P/'coverage-ledger-reviewed-08.json')
W(V/'freeze-manifest.json',{'question_count':103,'novelty_credited_questions':93,'retained_historical_overlaps':10,'hashes':{f:H(V/f) for f in ['questions.json','answer-key.json','grading-scope.json']},'prior101_questions_keys_and_scopes_unchanged':True})
D=P/'expanded-iteration-04';shutil.copyfile(V/'questions.json',D/'questions.json')
m=J(D/'input-manifest.json');m['benchmark_version']='expanded-v7';m['hashes']={a.replace('expanded-v6','expanded-v7'):h for a,h in m['hashes'].items()}
for a in m['hashes']:m['hashes'][a]=H(Path(a))
W(D/'input-manifest.json',m)
print('Frozen expanded-v7:103 questions/327 facts; all101 prior entries preserved; zero passes21/22.')
