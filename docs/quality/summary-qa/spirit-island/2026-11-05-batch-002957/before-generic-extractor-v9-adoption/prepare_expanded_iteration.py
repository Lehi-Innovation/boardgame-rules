from pathlib import Path
import json,hashlib,shutil,difflib,sys,datetime
B=Path(__file__).parent.resolve();ROOT=B.parents[4]
name,bankname=sys.argv[1:3]
coverage,audit,factpath,scopepath=map(lambda x:Path(x).resolve(),sys.argv[3:7])
load=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cr,ar,F,sr=map(load,[coverage,audit,factpath,scopepath]);progress=load(B/'progress.json');bank=B/bankname
Q=load(bank/'questions.json');ids=[x['id'] for x in Q['questions']];n=len(ids)
assert cr['verdict']=='PASS' and progress['coverage_review']['status']=='PASS'
assert progress['coverage_review']['benchmark']==bankname and progress['coverage_stopping_rule']['independent_challenge']=='PASS'
assert cr['checked_question_ids']==ids
assert ar['verdict']=='PASS' and not ar['findings'] and ar['candidate_sha256']==H(ROOT/'rules/spirit-island.md')
assert sr['asked_fact_mapping_verdict']=='PASS' and sr['asked_fact_map_sha256']==H(factpath)
assert not sr['asked_fact_mapping_findings']
assert sr['fixed_key_verdict']=='PASS' and not sr['fixed_key_findings']
assert not sr['missing_truly_asked_facts_in_map'] and not sr['missing_truly_asked_facts_in_fixed_key']
assert sr['checked_question_ids']==ids
for p in [bank/'questions.json',bank/'answer-key.json',factpath]:
 assert sr['input_hashes'][str(p.resolve())]==H(p)
assert cr['asked_fact_mapping_verdict']=='PASS' and cr['asked_fact_map_sha256']==H(factpath)
assert F.get('benchmark',F.get('benchmark_version'))==bankname and F['question_count']==n
assert [x['id'] for x in F['questions']]==ids
assert all(x.get('question',x.get('literal_question'))==y['question'] for x,y in zip(F['questions'],Q['questions']))
D=B/name;D.mkdir(exist_ok=False)
shutil.copyfile(ROOT/'rules/spirit-island.md',D/'summary-snapshot.md')
shutil.copyfile(bank/'questions.json',D/'questions.json')
shutil.copyfile(factpath,D/'asked-fact-map.json')
sources=load(B/'source-manifest.json')['paths_and_sha256']
sources.update({x['path']:x['sha256'] for x in load(B/'supplemental-source-manifest-v4.json')['source_records']})
inputs={str(p):{'sha256':H(p),'characters':len(p.read_text())} for p in [D/'summary-snapshot.md',D/'questions.json',bank/'answer-key.json',D/'asked-fact-map.json']}
m={'game':'Spirit Island','benchmark_version':bankname,'question_count':n,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'summary_path':str(D/'summary-snapshot.md'),'canonical_path':str(ROOT/'rules/spirit-island.md'),'questions_path':str(D/'questions.json'),'key_path':str(bank/'answer-key.json'),'inputs':inputs,'source_hashes':sources,'requested_model':'gpt-6-luna','requested_effort':'high','fork_turns':'none','reader_inputs_only':['summary-snapshot.md','questions.json'],'coverage_report':{'path':str(coverage),'sha256':H(coverage),'verdict':cr['verdict']},'independent_source_audit':{'path':str(audit),'sha256':H(audit),'candidate_sha256':ar['candidate_sha256']},'asked_fact_mapping':{'original':str(factpath),'snapshot':str(D/'asked-fact-map.json'),'sha256':H(factpath),'scope_review':str(scopepath),'scope_review_sha256':H(scopepath),'scope_verdict':sr['asked_fact_mapping_verdict']},'grading':'New fresh Sol/high graders in disjoint15–20-question blocks; full summary, exact source-backed fixed key, independently validated pre-test asked-fact map, and complete original raw entries; every actual clause independently graded.'}
template=(B/'reader-protocol-template.txt').read_text()
helper=B/'generic_reader_source_units.py'
assert H(helper)=='c3d73d720ffdfbe805875357c569171b18fb7b7113e10f68c6fd51f75f672280'
generic_code='\nGENERIC METHOD CODE (instructions only; no additional rules authority):\n```python\n'+helper.read_text()+'```\n'
for r in 'ab':(D/f'reader-{r}-prompt.txt').write_text(template.format(summary=D/'summary-snapshot.md',questions=D/'questions.json',output=D/f'reader-{r}.json')+generic_code)
m['reader_prompt_sha256']={r:H(D/f'reader-{r}-prompt.txt') for r in 'ab'}
m['reader_protocol']={'template_sha256':H(B/'reader-protocol-template.txt'),'operative_unit_boundary_validator_sha256':H(B/'validate_operative_units.py'),'same_entry_quotations_count':True,'known_fixed_set_tool_assisted_regression':True,'programmatic_pre_save_source_boundaries':True,'format_diagnostics_separate_from_factual_grades':True,'coordinator_steering_sha256':H(B/'coordinator-source-boundary-steering-before-expanded-pair.txt')}
m['reader_protocol']['embedded_generic_method_sha256']=H(helper)
m['reader_protocol']['generic_method_is_inline_instruction_not_third_input']=True
(D/'input-manifest.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
old=B/'seed-iteration-02/summary-snapshot.md'
(D/'summary-changes.patch').write_text(''.join(difflib.unified_diff(old.read_text().splitlines(True),(D/'summary-snapshot.md').read_text().splitlines(True),fromfile='seed-iteration-02/summary-snapshot.md',tofile=name+'/summary-snapshot.md')))
(D/'dispatch-status.json').write_text(json.dumps({'dispatched':False,'status':'ready_to_dispatch','preconditions_passed':True,'never_dispatched_prior_preflight':'expanded-iteration-01'},indent=2)+'\n')
progress['phase']='expanded-full-bank-readers-ready';progress['active_iteration']=name
(B/'progress.json').write_text(json.dumps(progress,indent=2)+'\n')
print(json.dumps({'iteration':name,'questions':n,'summary_sha256':H(D/'summary-snapshot.md'),'asked_facts_sha256':H(factpath),'prompt_a':str(D/'reader-a-prompt.txt'),'prompt_b':str(D/'reader-b-prompt.txt')},indent=2))
