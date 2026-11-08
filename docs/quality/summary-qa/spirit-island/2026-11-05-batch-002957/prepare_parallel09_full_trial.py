"""Freeze explicitly authorized full09 parallel trial; never invent a source PASS."""
from pathlib import Path
import hashlib,json,shutil,datetime
B=Path(__file__).resolve().parent
ROOT=B.parents[4]
D=B/'expanded-iteration-09'
bank=B/'expanded-v24'
load=lambda p:json.loads(p.read_text())
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
authpath=B/'coordinator-parallel-pair09-full-trial-authorization.json'
auth=load(authpath)
progress=load(B/'progress.json')
assert auth['authorized'] and auth['iteration']==D.name and auth['bank']==bank.name
assert auth['candidate_sha256']==H(ROOT/'rules/spirit-island.md')==H(B/'source-candidate-28.md')
assert auth['questions']==173 and auth['facts_per_reader']==506
assert auth['full_trial_authoring_authorized_after_actual_input_checkpoints'] and auth['current_source_accuracy_and_reader_performance_are_independent_final_gates']
assert all(H(bank/n)==v for n,v in auth['bank_sha256'].items())
coverage=Path(progress['coverage_review']['path'])
scope=Path(progress['coverage_review']['question_key_scope_path'])
cr,sr=load(coverage),load(scope)
factpath=bank/'asked-fact-map.json'
F=load(factpath)
Q=load(bank/'questions.json')
ids=[q['id'] for q in Q['questions']]
assert len(ids)==len(set(ids))==173 and sum(len(c['required_facts']) for q in F['questions'] for c in q['requested_clauses'])==506
assert progress['coverage_review']['status']=='PASS' and progress['coverage_stopping_rule']['independent_challenge']=='PASS'
assert cr['verdict']==sr['verdict']==sr['fixed_key_verdict']==sr['asked_fact_mapping_verdict']=='PASS'
assert not sr['fixed_key_findings'] and not sr['asked_fact_mapping_findings'] and not sr['missing_truly_asked_facts_in_map'] and not sr['missing_truly_asked_facts_in_fixed_key']
assert cr['checked_question_ids']==sr['checked_question_ids']==ids
assert sr['asked_fact_map_sha256']==cr['asked_fact_map_sha256']==H(factpath)
assert all(sr['input_hashes'][str(p.resolve())]==H(p) for p in [bank/'questions.json',bank/'answer-key.json',factpath])
delivery_path=B/'coverage-delivery-validation.json'
match=[r for r in load(delivery_path)['reports'] if r['report']==coverage.name and r['report_sha256']==H(coverage)]
assert len(match)==1 and match[0]['all_passed']
linked=match[0]['linked_read_ledger']
assert H(Path(linked['path']))==linked['sha256']==cr['read_evidence']['sha256']==sr['read_evidence']['sha256']
assert cr['read_evidence']['ledger_path']==sr['read_evidence']['ledger_path']==linked['path']
assert [q['id'] for q in F['questions']]==ids
assert all(q.get('question',q.get('literal_question'))==r['question'] for q,r in zip(F['questions'],Q['questions']))
original=B/'source-audit15-C27-own-current-body-semantic-adoption.json'
orig=load(original)
assert orig['semantic_verdict']=='PASS' and orig['unresolved_findings']==0 and orig['candidate_sha256']==H(B/'source-candidate-27.md')
assert progress['source_audit']['candidate_sha256']==auth['candidate_sha256'] and progress['source_audit']['same_initially_fresh_pure_actor']
assert progress['source_audit']['status']!='PASS' and progress['source_audit']['current_PASS'] is False
review=load(B/'expanded09-planned-reader-prompts-v15/parent-full-instruction-read-receipt.json')
assert review['whole_native_instructions_fully_read_before_dispatch'] and len(review['prompts'])==2
assert all(H(Path(r['path']))==r['sha256'] and r['all_whole_native_instructions_actually_read'] for r in review['prompts'])
assert not D.exists()
D.mkdir()
for p,n in [(ROOT/'rules/spirit-island.md','summary-snapshot.md'),(bank/'questions.json','questions.json'),(factpath,'asked-fact-map.json')]:shutil.copyfile(p,D/n)
inputs={str(p):{'sha256':H(p),'characters':len(p.read_text())} for p in [D/'summary-snapshot.md',D/'questions.json',bank/'answer-key.json',D/'asked-fact-map.json']}
sources=load(B/'source-manifest.json')['paths_and_sha256']
sources.update({x['path']:x['sha256'] for x in load(B/'supplemental-source-manifest-v4.json')['source_records']})
assert all(H(ROOT/p)==v for p,v in sources.items())
template_path=B/'reader-protocol-v15-template.txt'
adoption_path=B/'generic-reader-protocol-v15-adoption.json'
adoption=load(adoption_path)
assert adoption['template_sha256']==H(template_path) and adoption['parent_full_new_template_actually_read']
helper=B/'generic_reader_source_units_v9.py'
assert H(helper)=='f7818be51316125128d7f675d4a09696c88633ea5126abace01025632897b219'
generic='\nGENERIC METHOD CODE (instructions only; no additional rules authority):\n```python\n'+helper.read_text()+'```\n'
for r in 'ab':
 p=D/f'reader-{r}-prompt.txt'
 p.write_text(template_path.read_text().format(summary=D/'summary-snapshot.md',questions=D/'questions.json',output=D/f'reader-{r}.json')+generic)
 assert p.read_bytes()==(B/'expanded09-planned-reader-prompts-v15'/f'reader-{r}-prompt.txt').read_bytes()
previous=load(B/'expanded-iteration-08/input-manifest.json')['reader_protocol']
protocol={**previous,'template_path':str(template_path),'template_sha256':H(template_path),'quotation_first_generic_method':{'version':'v15','select_complete_units_before_ruling':True,'actual_asked_case_results_and_calculations_still_required':True,'no_case_hints':True}}
protocol['staged_pre_authoring_method']['protocol_adoption']={'path':str(adoption_path),'sha256':H(adoption_path)}
source={'path':str(B/'source-audit15-current-body-C28-followup.json'),'sha256':None,'candidate_sha256':auth['candidate_sha256'],'reported_verdict':None,'semantically_adopted_before_dispatch':False,'current_body_review_pending_at_dispatch':True,'review_role':'same_initially_fresh_pure15_own_current_body_followup','new_fresh_vote':False,'original_C27_own_current_body_adoption':{'path':str(original),'sha256':H(original)},'authorization':{'path':str(authpath),'sha256':H(authpath)},'no_current_source_PASS_claim':True}
m={'game':'Spirit Island','benchmark_version':'expanded-v24','question_count':173,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'summary_path':str(D/'summary-snapshot.md'),'canonical_path':str(ROOT/'rules/spirit-island.md'),'questions_path':str(D/'questions.json'),'key_path':str(bank/'answer-key.json'),'inputs':inputs,'source_hashes':sources,'requested_model':'gpt-6-luna','requested_effort':'high','fork_turns':'none','reader_inputs_only':['summary-snapshot.md','questions.json'],'coverage_report':{'path':str(coverage),'sha256':H(coverage),'verdict':'PASS'},'independent_source_audit':source,'asked_fact_mapping':{'original':str(factpath),'snapshot':str(D/'asked-fact-map.json'),'sha256':H(factpath),'scope_review':str(scope),'scope_review_sha256':H(scope),'scope_verdict':'PASS'},'grading':'Fresh disjoint Sol/high full5input graders, all346 whole entries1012 facts; same factual standard; needed complete-set neutral.','reader_prompt_sha256':{r:H(D/f'reader-{r}-prompt.txt') for r in 'ab'},'reader_protocol':protocol,'pre_reader_delivery_gates':{'coverage_delivery_validation':{'path':str(delivery_path),'sha256':H(delivery_path),'exact_current_report_complete':True},'source_currentbody_pending_authorized_full_parallel_trial':{'path':str(authpath),'sha256':H(authpath),'authoring_after_actual_empty_checkpoint_authorized_independently_of_pending_source':True}}}
(D/'input-manifest.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
(D/'dispatch-status.json').write_text(json.dumps({'dispatched':False,'status':'ready_to_dispatch_full_parallel_trial_after_empty_actual_checkpoint','preconditions_passed':True,'source_currentbody_pending_at_dispatch':True,'actual_empty_checkpoint_not_yet_cleared':True},indent=2)+'\n')
print(json.dumps({'iteration':D.name,'questions':173,'facts':506,'source_status':'PENDING_OWN15_CURRENTBODY','whole_native_prompts_byte_equal_fully_parent_reviewed_plans':True,'characters_each':len((D/'reader-a-prompt.txt').read_text()),'actual_readers_not_yet_dispatched':True}))
