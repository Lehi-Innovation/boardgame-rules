from pathlib import Path
import datetime, hashlib, json, shutil
P=Path(__file__).resolve().parent;V=P/'expanded-v8';V.mkdir(exist_ok=False)
def J(p):return json.loads(p.read_text())
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def W(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
q=J(P/'expanded-v7/questions.json');k=J(P/'expanded-v7/answer-key.json');scope=J(P/'expanded-v7/grading-scope.json')
defect=J(P/'coverage-review-08.json')['key_defects'][0]
old=next(x for x in k['answers'] if x['id']=='Q015')['expected_answer']
entry=next(x for x in k['answers'] if x['id']=='Q015')
assert defect['current_phrase'] in old
entry['expected_answer']=old.replace(defect['current_phrase'],defect['required_replacement'])
entry['source_references']+='; official errata Law5.5.2 attacking FORCE ceiling'
for obj in [q,k,scope]:obj['benchmark_version']='expanded-v8'
scope['created_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
scope['preparation_disclosure']='Source-only reviewer08 corrected Q015 expected-key wording from board-force to attacking force. All327 pre-existing required facts, all questions, clause maps and exclusions remain exactly unchanged; Q015-F01 already correctly stated force. Only Q015 key-hash/source locator changed. No new v8 reader response exists.'
scope['inputs']['questions']='expanded-v8/questions.json';scope['inputs']['fixed_key']='expanded-v8/answer-key.json'
f=next(x for x in scope['questions'] if x['id']=='Q015');f['fixed_key_expected_answer_sha256']=hashlib.sha256(entry['expected_answer'].encode()).hexdigest();f['source_references']=entry['source_references']
assert q['questions']==J(P/'expanded-v7/questions.json')['questions']
for a,b in zip(k['answers'],J(P/'expanded-v7/answer-key.json')['answers']):
 if a['id']!='Q015':assert a==b
prior_scope=J(P/'expanded-v7/grading-scope.json')
for a,b in zip(scope['questions'],prior_scope['questions']):
 assert a['required_facts']==b['required_facts'] and a['asked_clause_map']==b['asked_clause_map'] and a['contextual_exclusions']==b['contextual_exclusions']
 if a['id']!='Q015':assert a==b
W(V/'questions.json',q);W(V/'answer-key.json',k);W(V/'grading-scope.json',scope)
W(V/'key-corrections.json',[{'id':'Q015','old':old,'new':entry['expected_answer'],'reason':defect['reason'],'source_references':defect['source_locators'],'discovered_by':'source-only coverage-review-08 K01, not reader grading','new_question_count':0,'novelty_credit':0,'required_fact_changes':0,'prior_keys_and_grades_retained':True}])
W(V/'input-manifest.json',{f:H(V/f) for f in ['questions.json','answer-key.json']})
inputs=[V/'questions.json',V/'answer-key.json',P/'expanded-v7/grading-scope.json',P/'coverage-review-08.json',P/'errata.txt']
W(V/'grading-scope-manifest.json',{'artifact_type':'grading-scope SHA256 freeze manifest','benchmark_version':'expanded-v8','created_utc':scope['created_utc'],'scope_artifact':{'path':str((V/'grading-scope.json').resolve()),'sha256':H(V/'grading-scope.json')},'input_files':[{'path':str(f.resolve()),'sha256':H(f)} for f in inputs],'required_fact_count':327,'question_count':103,'all_prior_required_facts_clauses_exclusions_exactly_preserved':True,'frozen_before_reader_dispatch':True})
text=['# Oath expanded benchmark v8','','103 retained questions; all wording and327 required facts unchanged. Ten historical overlaps retain zero novelty credit. Q015 expected-key wording is corrected to attacking force by official errata; see key-corrections.json. The already-frozen fact Q015-F01 already used force. No new question or novelty credit.','']
for a,b in zip(q['questions'],k['answers']):text+=['## '+a['id'],'',a['question'],'','**Answer:** '+b['expected_answer'],'','**Source:** '+b['source_references'],'']
(V/'question-bank.md').write_text('\n'.join(text))
shutil.copyfile(P/'coverage-ledger.json',P/'coverage-ledger-before-v8-key-correction.json');ledger=J(P/'coverage-ledger.json')
ledger['passes'] += [{'pass':23,'focus':'Apply independent reviewer08 source-only Q015 key correction; general calculation already asked','count':0,'accepted_ids':[],'key_corrections':['expanded-v8/key-corrections.json'],'new_novelty_credit':0}, {'pass':24,'focus':'Reopen complete procedural coverage after key precision correction; no question or required-fact change','count':0,'accepted_ids':[],'rejections':[{'candidate':'Power-expanded attack-force numerical example','reason':'Same general force ceiling expressly asked by Q015 and already stated in frozen Q015-F01; source-based key precision repair, not new procedural novelty.'}]}]
ledger['stopping_rule']={'consecutive_zero_addition_passes':2,'passes':[23,24],'all_core_procedural_passages_mapped':True,'independent_challenge':{'verdict':'PASS_WORKING_SATURATION','report':'coverage-review-08.json','final_key_verification':'PENDING coverage-review-08.final-verification.json','new_questions':0,'source_only_key_correction':'expanded-v8/key-corrections.json'}}
W(P/'coverage-ledger.json',ledger);shutil.copyfile(P/'coverage-ledger.json',P/'coverage-ledger-reviewed-08-v8.json')
W(V/'freeze-manifest.json',{'question_count':103,'required_fact_count':327,'novelty_credited_questions':93,'retained_historical_overlaps':10,'all_prior_question_entries_unchanged':True,'all_prior_required_facts_unchanged':True,'hashes':{f:H(V/f) for f in ['questions.json','answer-key.json','grading-scope.json']}})
D=P/'expanded-iteration-04';shutil.copyfile(V/'questions.json',D/'questions.json');m=J(D/'input-manifest.json');m['benchmark_version']='expanded-v8';m['hashes']={a.replace('expanded-v7','expanded-v8'):h for a,h in m['hashes'].items()}
for a in m['hashes']:m['hashes'][a]=H(Path(a))
W(D/'input-manifest.json',m)
print('Frozen expanded-v8:103 questions/327 facts unchanged; Q015 source-only key correction recorded.')
