from pathlib import Path
import datetime,hashlib,json,shutil
P=Path(__file__).resolve().parent;V=P/'expanded-v9';V.mkdir(exist_ok=True);assert not any(V.iterdir())
def J(p):return json.loads(p.read_text())
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def W(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
q=J(P/'expanded-v8/questions.json');k=J(P/'expanded-v8/answer-key.json');s=J(P/'expanded-v8/grading-scope.json')
entry=next(x for x in k['answers'] if x['id']=='Q015');old=entry['material_facts'][0]
replacement=J(P/'coverage-review-08.json')['key_defects'][0]['required_replacement']
phrase='Attacker chooses up to board-force warbands worth of attack dice.'
assert old.startswith(phrase)
entry['material_facts'][0]=old.replace(phrase,replacement)
for obj in [q,k,s]:obj['benchmark_version']='expanded-v9'
s['created_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();s['inputs']['questions']='expanded-v9/questions.json';s['inputs']['fixed_key']='expanded-v9/answer-key.json'
s['preparation_disclosure']='Source-only reviewer08 found the legacy Q015.material_facts[0] field still used board-force wording after v8 expected_answer was repaired. V9 aligns that duplicate field with the exact same K01 correction. All103 question entries, all expected_answer strings, all327 required facts and all103 scope entries remain exactly unchanged from v8; no v9 reader exists.'
assert q['questions']==J(P/'expanded-v8/questions.json')['questions']
assert s['questions']==J(P/'expanded-v8/grading-scope.json')['questions']
for a,b in zip(k['answers'],J(P/'expanded-v8/answer-key.json')['answers']):
 if a['id']!='Q015':assert a==b
 else:
  assert a['expected_answer']==b['expected_answer']
  aa=dict(a);bb=dict(b);aa.pop('material_facts');bb.pop('material_facts');assert aa==bb
  assert a['material_facts'][1:]==b['material_facts'][1:]
W(V/'questions.json',q);W(V/'answer-key.json',k);W(V/'grading-scope.json',s)
W(V/'key-corrections.json',[{'id':'Q015','field':'material_facts[0]','old':old,'new':entry['material_facts'][0],'reason':'Complete the same source-only K01 force-ceiling correction in the legacy duplicated structured field; expected_answer already corrected in v8. Reviewer08 caught this before any v8/v9 reader dispatch.','source':'coverage-review-08 K01; official errata5.5.2','new_question_count':0,'novelty_credit':0,'required_fact_changes':0,'expected_answer_changes_from_v8':0}])
W(V/'input-manifest.json',{f:H(V/f) for f in ['questions.json','answer-key.json']})
inputs=[V/'questions.json',V/'answer-key.json',P/'expanded-v8/grading-scope.json',P/'coverage-review-08.json',P/'errata.txt']
W(V/'grading-scope-manifest.json',{'artifact_type':'grading-scope SHA256 freeze manifest','benchmark_version':'expanded-v9','created_utc':s['created_utc'],'scope_artifact':{'path':str((V/'grading-scope.json').resolve()),'sha256':H(V/'grading-scope.json')},'input_files':[{'path':str(x.resolve()),'sha256':H(x)} for x in inputs],'required_fact_count':327,'question_count':103,'all_prior_scope_entries_exactly_preserved':True,'frozen_before_reader_dispatch':True})
text=['# Oath expanded benchmark v9','','103 retained questions and327 required facts unchanged. Q015 expected_answer was corrected in v8; v9 aligns the duplicate material_facts[0] field with the same official force-ceiling correction. All prior versions remain intact; no new question or novelty credit.','']
for a,b in zip(q['questions'],k['answers']):text+=['## '+a['id'],'',a['question'],'','**Answer:** '+b['expected_answer'],'','**Source:** '+b['source_references'],'']
(V/'question-bank.md').write_text('\n'.join(text))
shutil.copyfile(P/'coverage-ledger.json',P/'coverage-ledger-before-v9.json');l=J(P/'coverage-ledger.json')
l['passes'] += [{'pass':25,'focus':'Align Q015 legacy material_facts duplicate with same source-only K01 correction','count':0,'accepted_ids':[],'new_novelty_credit':0}, {'pass':26,'focus':'Recheck complete structured key, question/scope identity and procedural map; no added question or required fact','count':0,'accepted_ids':[],'rejections':[{'candidate':'Recount force-ceiling example as new rule','reason':'Q015 already asks corrected operator; duplicate field alignment is zero novelty, no new procedure.'}]}]
l['stopping_rule']={'consecutive_zero_addition_passes':2,'passes':[25,26],'all_core_procedural_passages_mapped':True,'independent_challenge':{'verdict':'PASS_WORKING_SATURATION','report':'coverage-review-08.json','final_key_verification':'PENDING coverage-review-08.final-verification.json','new_questions':0,'source_only_key_corrections':['expanded-v8/key-corrections.json','expanded-v9/key-corrections.json']}}
W(P/'coverage-ledger.json',l);shutil.copyfile(P/'coverage-ledger.json',P/'coverage-ledger-reviewed-08-v9.json')
W(V/'freeze-manifest.json',{'question_count':103,'required_fact_count':327,'novelty_credited_questions':93,'retained_historical_overlaps':10,'all_prior_question_entries_and_required_facts_unchanged':True,'all_v8_expected_answers_and_scope_entries_unchanged':True,'hashes':{f:H(V/f) for f in ['questions.json','answer-key.json','grading-scope.json']}})
D=P/'expanded-iteration-04';shutil.copyfile(V/'questions.json',D/'questions.json');m=J(D/'input-manifest.json');m['benchmark_version']='expanded-v9';m['hashes']={a.replace('expanded-v8','expanded-v9'):h for a,h in m['hashes'].items()}
for a in m['hashes']:m['hashes'][a]=H(Path(a))
W(D/'input-manifest.json',m)
script=(D/'build-grading-package.py').read_text().replace('expanded-v7','expanded-v9');(D/'build-grading-package.py').write_text(script)
print('Frozen v9:103 questions/327 facts; all expected answers and scopes unchanged from v8; duplicate key field aligned.')
