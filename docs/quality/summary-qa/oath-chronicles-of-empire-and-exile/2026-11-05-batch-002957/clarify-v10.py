from pathlib import Path
import datetime,hashlib,json,shutil
P=Path(__file__).resolve().parent;V=P/'expanded-v10';V.mkdir(exist_ok=False)
def J(p):return json.loads(p.read_text())
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def W(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
review=J(P/'source-key-clarification-09.json');case=next(x for x in review['cases'] if x['id']=='Q025')
q=J(P/'expanded-v9/questions.json');k=J(P/'expanded-v9/answer-key.json');s=J(P/'expanded-v9/grading-scope.json')
for obj in [q,k,s]:obj['benchmark_version']='expanded-v10'
e=next(x for x in k['answers'] if x['id']=='Q025');assert e['expected_answer']==case['expected_answer_change']['old'];e['expected_answer']=case['expected_answer_change']['new']
for change in case['material_fact_changes']:
 i=change['index_1_based']-1;assert e['material_facts'][i]==change['old'];e['material_facts'][i]=change['new']
e['source_references']+='; original Playbook pp6–7 setup diagrams, fresh source-key-clarification-09'
ss=next(x for x in s['questions'] if x['id']=='Q025');ss['fixed_key_expected_answer_sha256']=hashlib.sha256(e['expected_answer'].encode()).hexdigest();ss['source_references']=e['source_references']
for change in case['required_fact_changes']:
 f=next(x for x in ss['required_facts'] if x['fact_id']==change['fact_id']);assert f['expected_fact']==change['old'];f['expected_fact']=change['new']
s['created_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();s['inputs']['questions']='expanded-v10/questions.json';s['inputs']['fixed_key']='expanded-v10/answer-key.json'
s['preparation_disclosure']='Source-only independent reviewer09 inspected original setup diagrams and made three existing Q025 placement/orientation fact groups explicitly faceup, as already asked. All103 questions remain unchanged; all other324 required-fact groups, every clause map and contextual exclusion remain unchanged. No new question/novelty. Old v9 and its reader/grade runs remain intact. This precision is frozen before fresh iteration06 dispatch.'
assert q['questions']==J(P/'expanded-v9/questions.json')['questions']
for a,b in zip(k['answers'],J(P/'expanded-v9/answer-key.json')['answers']):
 if a['id']!='Q025':assert a==b
for a,b in zip(s['questions'],J(P/'expanded-v9/grading-scope.json')['questions']):
 if a['id']!='Q025':assert a==b
 else:
  assert a['asked_clause_map']==b['asked_clause_map'] and a['contextual_exclusions']==b['contextual_exclusions']
  for x,y in zip(a['required_facts'],b['required_facts']):
   if x['fact_id'] not in [c['fact_id'] for c in case['required_fact_changes']]:assert x==y
W(V/'questions.json',q);W(V/'answer-key.json',k);W(V/'grading-scope.json',s);W(V/'key-corrections.json',[{'id':'Q025','discovery':'Independent source-only reviewer09; sources/diagrams, no summary/readers/grades','expected_answer_change':case['expected_answer_change'],'material_fact_changes':case['material_fact_changes'],'required_fact_changes':case['required_fact_changes'],'question_change':None,'novelty_credit':0,'contextual_exclusions_unchanged':True,'prior_versions_and_grades_preserved':True}])
W(V/'input-manifest.json',{f:H(V/f) for f in ['questions.json','answer-key.json']})
inputs=[V/'questions.json',V/'answer-key.json',P/'expanded-v9/grading-scope.json',P/'source-key-clarification-09.json',Path('/home/jonny/projects/boardgame-rules/extracted/oath-current-playbook.txt')]
W(V/'grading-scope-manifest.json',{'artifact_type':'grading-scope SHA256 freeze manifest','benchmark_version':'expanded-v10','created_utc':s['created_utc'],'scope_artifact':{'path':str((V/'grading-scope.json').resolve()),'sha256':H(V/'grading-scope.json')},'input_files':[{'path':str(f.resolve()),'sha256':H(f)} for f in inputs],'required_fact_count':327,'question_count':103,'three_Q025_fact_groups_precision_corrected':True,'all_other_required_facts_clauses_exclusions_unchanged':True,'frozen_before_reader_dispatch':True})
text=['# Oath expanded benchmark v10','','103 retained questions. Q025 explicitly states the faceup initial sites/denizens shown in the original setup diagrams; three existing required-fact groups receive that precision, with all other324 unchanged. All question wording, clause maps and contextual exclusions remain unchanged. No new question/novelty; ten historical overlaps retain zero credit.','']
for a,b in zip(q['questions'],k['answers']):text+=['## '+a['id'],'',a['question'],'','**Answer:** '+b['expected_answer'],'','**Source:** '+b['source_references'],'']
(V/'question-bank.md').write_text('\n'.join(text))
shutil.copyfile(P/'coverage-ledger.json',P/'coverage-ledger-before-v10.json');l=J(P/'coverage-ledger.json')
l['passes'] += [{'pass':27,'focus':'Apply source-only reviewer09 explicit setup orientation to already-asked Q025 clauses','count':0,'accepted_ids':[],'new_novelty_credit':0,'key_scope_correction':'expanded-v10/key-corrections.json'}, {'pass':28,'focus':'Recheck complete key/scope identity and operative source map after orientation precision','count':0,'accepted_ids':[],'rejections':[{'candidate':'New question asking those first-game cards faceup/down','reason':'Already explicitly asked by Q025; source precision repairs existing expected content, no new procedure.'}]}]
l['stopping_rule']={'consecutive_zero_addition_passes':2,'passes':[27,28],'all_core_procedural_passages_mapped':True,'independent_challenge':{'verdict':'PASS_WORKING_SATURATION','report':'coverage-review-08.json','final_key_verification':'PENDING coverage-review-08.v10-verification.json','new_questions':0,'source_only_precision_correction':'expanded-v10/key-corrections.json'}}
W(P/'coverage-ledger.json',l);shutil.copyfile(P/'coverage-ledger.json',P/'coverage-ledger-reviewed-08-v10.json')
W(V/'freeze-manifest.json',{'question_count':103,'required_fact_group_count':327,'novelty_credited_questions':93,'retained_historical_overlaps':10,'all_question_entries_unchanged':True,'three_existing_fact_groups_explicit_orientation':True,'all_other324_required_fact_groups_unchanged':True,'hashes':{f:H(V/f) for f in ['questions.json','answer-key.json','grading-scope.json']}})
D=P/'expanded-iteration-06';D.mkdir(exist_ok=False);shutil.copyfile('/home/jonny/projects/boardgame-rules/rules/oath-chronicles-of-empire-and-exile.md',D/'summary-snapshot.md');shutil.copyfile(V/'questions.json',D/'questions.json')
m=J(P/'expanded-iteration-05/input-manifest.json');m['benchmark_version']='expanded-v10';m['hashes']={a.replace('expanded-iteration-05','expanded-iteration-06').replace('expanded-v9','expanded-v10'):h for a,h in m['hashes'].items()}
for a in m['hashes']:m['hashes'][a]=H(Path(a))
W(D/'input-manifest.json',m);(D/'build-grading-package.py').write_text((P/'expanded-iteration-05/build-grading-package.py').read_text().replace('expanded-v9','expanded-v10'))
W(D/'summary-changes.json',{'previous_snapshot':'expanded-iteration-05/summary-snapshot.md','sha256':H(D/'summary-snapshot.md'),'changes':[{'clarification':'Initial Longbows/TamingCharm/Elders explicitly placed faceup','source':'Original Playbook pp6–7 setup diagrams; source-key-clarification-09'}, {'clarification':'Power printed on ruin side remains usable under ordinary access and printed conditions','source':'Law2.10,7.1.1,8.2; source-key-clarification-09 Q066 confirms key correct'}],'source_auditor_and_readers_must_not_read_this_file':True,'no_question_words_removed_or_added':True,'verification_banner_unchanged':True})
print('Frozen v10 and iteration06',H(D/'summary-snapshot.md'))
