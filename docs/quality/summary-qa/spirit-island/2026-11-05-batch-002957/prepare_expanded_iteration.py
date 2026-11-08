from pathlib import Path
import json,hashlib,shutil,difflib,sys,datetime
B=Path(__file__).parent.resolve();ROOT=B.parents[4]
name,bankname=sys.argv[1:3]
coverage,audit,factpath,scopepath=map(lambda x:Path(x).resolve(),sys.argv[3:7])
load=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
cr,ar,F,sr=map(load,[coverage,audit,factpath,scopepath]);progress=load(B/'progress.json');bank=B/bankname
delivery_path=B/'coverage-delivery-validation.json';delivery=load(delivery_path)
delivery_match=[row for row in delivery['reports'] if row['report']==coverage.name and row['report_sha256']==H(coverage)]
assert len(delivery_match)==1 and delivery_match[0]['all_passed'], 'Validate complete delivery of the exact current coverage report before freezing readers'
delivery_row=delivery_match[0];linked=delivery_row['linked_read_ledger']
assert linked and H(Path(linked['path']))==linked['sha256']
assert cr['read_evidence']['ledger_path']==sr['read_evidence']['ledger_path']==linked['path']
assert cr['read_evidence']['sha256']==sr['read_evidence']['sha256']==linked['sha256']
parallel_authorization_path=B/'coordinator-parallel-pair05-source13-own-note-authorization.json'
parallel_launch=(name=='expanded-iteration-05' and audit.name=='source-audit-final-13.json' and progress['source_audit']['status']!='PASS' and parallel_authorization_path.exists())
parallel07_path=B/'coordinator-parallel-pair07-source15-own-note-authorization.json'
parallel07=(name=='expanded-iteration-07' and audit.name=='source-audit-final-15.json' and progress['source_audit']['status']!='PASS' and parallel07_path.exists())
parallel_launch=parallel_launch or parallel07
if parallel07:
 parallel_authorization_path=parallel07_path;authorization=load(parallel_authorization_path)
 assert authorization['authorized'] and authorization['iteration']==name and authorization['bank']==bankname=='expanded-v24'
 assert authorization['question_count']==173 and authorization['required_facts_per_reader']==506
 assert authorization['candidate_sha256']==ar['candidate_sha256']==H(ROOT/'rules/spirit-island.md')=='ce8f1d645f466686ae2e75fcd29130fa89cbb1c4963d981090e3768a526a6fd1'
 assert authorization['original_audit_sha256']==H(audit) and ar['verdict']=='PASS' and not ar['findings']
 assert all(H(bank/n)==digest for n,digest in authorization['current_bank_hashes'].items())
 coordinator_proof_path=Path(authorization['coordinator_original_transport_proof']);coordinator_proof=load(coordinator_proof_path)
 assert H(coordinator_proof_path)==authorization['coordinator_original_transport_proof_sha256'] and coordinator_proof['verified'] and coordinator_proof['summary_sha256']==ar['candidate_sha256'] and coordinator_proof['audit_sha256']==H(audit) and not coordinator_proof['flagged_forbidden_reads']
 original_transport=B/'source-audit15-original-actual-delivery-validation.json';transport=load(original_transport)
 assert H(original_transport)==authorization['original_transport_proof_sha256'] and transport['verified'] and transport['text_sources']==16 and transport['actual_distinct_text_range_deliveries']==92 and transport['unique_visual_sources']==transport['public_image_blocks']==57 and transport['one_source_range_per_matched_output_event'] and transport['record_cutoff_exclusive']==653
 assert authorization['supersedes_earlier_serial_reader_launch_gate_for_exact07_C26_only'] and authorization['final_corrected_source_semantic_delivery_acceptance_required'] and authorization['exact_stamped_full_pair_required'] and authorization['post_stamp_source_only_current_body_followup_required'] and not authorization['source_semantic_adoption_authorized'] and not authorization['publication_or_stamp_authorized']
 audit_delivery_path=B/'source-audit15-original-evidence-validation.json';audit_delivery=load(audit_delivery_path)
 assert audit_delivery['all_passed'] and audit_delivery['counts']['blocking_failed_checks']==0 and not audit_delivery['semantic_adoption']
 adoption_path=None
elif parallel_launch:
 authorization=load(parallel_authorization_path)
 assert authorization['authorized'] and authorization['iteration']==name and authorization['bank']==bankname=='expanded-v24'
 assert authorization['question_count']==173 and authorization['required_facts_per_reader']==506
 assert authorization['candidate_sha256']==ar['candidate_sha256']==H(ROOT/'rules/spirit-island.md')=='954d203e6d2b1a59a5835381e786b01e0a88d86218ba1bde663018b2c6cab1de'
 assert authorization['original_audit_sha256']==H(audit) and ar['verdict']=='PASS' and not ar['findings']
 assert all(H(bank/n)==h for n,h in authorization['current_bank_hashes'].items())
 coordinator_proof_path=Path(authorization['coordinator_original_transport_proof']);coordinator_proof=load(coordinator_proof_path)
 assert H(coordinator_proof_path)==authorization['coordinator_original_transport_proof_sha256'] and coordinator_proof['verified'] and coordinator_proof['summary_sha256']==ar['candidate_sha256'] and not coordinator_proof['flagged_forbidden_reads']
 original_transport=B/'source-audit13-original-actual-delivery-validation.json';transport=load(original_transport)
 assert H(original_transport)==authorization['original_transport_proof_sha256'] and transport['verified'] and transport['text_sources']==15 and transport['actual_distinct_text_range_deliveries']==90 and transport['unique_visual_sources']==transport['public_image_blocks']==57
 assert authorization['supersedes_earlier_serial_reader_launch_gate'] and authorization['final_corrected_source_semantic_delivery_acceptance_required'] and authorization['exact_stamped_full_pair_required'] and not authorization['source_semantic_adoption_authorized'] and not authorization['publication_or_stamp_authorized']
 audit_delivery_path=B/'source-audit13-original-evidence-validation.json';audit_delivery=load(audit_delivery_path)
 assert audit_delivery['all_passed'] and not audit_delivery['semantic_adoption']
 adoption_path=None
else:
 adoption_path=Path(progress['source_audit']['delivery_adoption']);adoption=load(adoption_path)
 audit_delivery_path=Path(progress['source_audit']['delivery_validation']);audit_delivery=load(audit_delivery_path)
 assert progress['source_audit']['status']=='PASS' and adoption['semantic_verdict']=='PASS' and adoption['unresolved_findings']==0
 assert adoption['candidate_sha256']==H(ROOT/'rules/spirit-island.md')
 assert adoption['evidence'][audit.name]==H(audit) and adoption['evidence'][audit_delivery_path.name]==H(audit_delivery_path)
assert audit_delivery['counts']['blocking_failed_checks']==0
assert audit_delivery['frozen_artifact_sha256'][audit.name]==H(audit)
Q=load(bank/'questions.json');ids=[x['id'] for x in Q['questions']];n=len(ids)
assert cr['verdict']=='PASS' and progress['coverage_review']['status']=='PASS'
assert progress['coverage_review']['benchmark']==bankname and progress['coverage_stopping_rule']['independent_challenge']=='PASS'
assert cr['checked_question_ids']==ids
assert ar['verdict']=='PASS' and not ar['findings'] and ar['candidate_sha256']==H(ROOT/'rules/spirit-island.md')
assert sr['verdict']=='PASS', 'Resolve the complete current independent scope/key report before freezing readers'
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
template_path=B/'reader-protocol-v15-template.txt'
template=template_path.read_text()
v13_adoption_path=B/'generic-reader-protocol-v15-adoption.json'
v13_adoption=load(v13_adoption_path)
assert v13_adoption['pre_authoring_checkpoint'] and v13_adoption['template_sha256']==H(template_path)
staged_checker=B/'verify_staged_reader_actual_delivery.py'
readiness_freezer=B/'freeze_staged_reader_readiness.py'
assert v13_adoption['staged_actual_delivery_checker']['sha256']==H(staged_checker)
helper=B/'generic_reader_source_units_v9.py'
assert H(helper)=='f7818be51316125128d7f675d4a09696c88633ea5126abace01025632897b219'
generic_code='\nGENERIC METHOD CODE (instructions only; no additional rules authority):\n```python\n'+helper.read_text()+'```\n'
for r in 'ab':(D/f'reader-{r}-prompt.txt').write_text(template.format(summary=D/'summary-snapshot.md',questions=D/'questions.json',output=D/f'reader-{r}.json')+generic_code)
m['reader_prompt_sha256']={r:H(D/f'reader-{r}-prompt.txt') for r in 'ab'}
m['pre_reader_delivery_gates']={'coverage_delivery_validation':{'path':str(delivery_path),'sha256':H(delivery_path),'exact_current_report_complete':True},'source_audit_delivery_validation':{'path':str(audit_delivery_path),'sha256':H(audit_delivery_path),'blocking_failed_checks':0},('source_audit_parallel_launch_authorization' if parallel_launch else 'source_audit_delivery_adoption'):{'path':str(parallel_authorization_path if parallel_launch else adoption_path),'sha256':H(parallel_authorization_path if parallel_launch else adoption_path)}}
if parallel_launch:
 m['independent_source_audit'].update({'reported_verdict':'PASS','semantically_adopted_before_dispatch':False,'own_note_correction_pending':True,'parallel_launch_authorization_sha256':H(parallel_authorization_path),'final_corrected_source_and_exact_stamped_pair_required':True,'no_publication_or_stamp_approval':True})
m['reader_protocol']={'template_path':str(template_path),'template_sha256':H(template_path),'operative_unit_boundary_validator_sha256':H(B/'validate_operative_units.py'),'same_entry_quotations_count':True,'known_fixed_set_tool_assisted_regression':True,'programmatic_pre_save_source_boundaries':True,'format_diagnostics_separate_from_factual_grades':True,'coordinator_steering_sha256':H(B/'coordinator-source-boundary-steering-before-expanded-pair.txt')}
m['reader_protocol']['quotation_first_generic_method']={'version':'v15','select_complete_operative_units_before_ruling':True,'direct_lookup_complete_quotes_count':True,'actual_application_results_and_calculations_still_required':True,'no_case_ID_or_game_fact_hints':True}
if progress['source_audit'].get('same_initially_fresh_pure_actor'):
 m['independent_source_audit'].update({'review_role':'same_initially_fresh_pure_auditor_own_current_body_followup','new_fresh_vote':False,'original_source_only_actor':progress['source_audit']['agent'],'authorized_policy':progress['source_audit']['authorized_policy'],'honest_unchanged_authority_reuse_allowed':True})
m['reader_protocol']['embedded_generic_method_sha256']=H(helper)
m['reader_protocol']['generic_method_is_inline_instruction_not_third_input']=True
m['reader_protocol']['stage3_separate_original_self_review_turn']={'draft_stage':'draft_ready','freeze_draft_without_parent_factual_diagnostics':True,'same_original_actor_not_resampling':True,'identical_stage3_technical_resume':{'path':str(B/'reader-protocol-v14-stage3-technical-resume.txt'),'sha256':H(B/'reader-protocol-v14-stage3-technical-resume.txt')},'no_game_fact_or_grading_feedback':True}
m['reader_protocol']['staged_pre_authoring_method']={
 'protocol_adoption':{'path':str(v13_adoption_path),'sha256':H(v13_adoption_path)},
 'actual_delivery_checker':{'path':str(staged_checker),'sha256':H(staged_checker)},
 'readiness_freezer':{'path':str(readiness_freezer),'sha256':H(readiness_freezer)},
 'identical_technical_resume':{'path':str(B/'reader-protocol-v14-stage2-technical-resume.txt'),'sha256':H(B/'reader-protocol-v14-stage2-technical-resume.txt')},
 'mandatory_empty_answer_checkpoint_before_technical_resume':True,
 'both_original_complete_outputs_frozen_before_factual_diagnostics':True,
 'same_technical_resume_message_for_both_original_readers':True,
 'no_game_specific_feedback_before_completed_output_freezes':True}

(D/'input-manifest.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
old=B/'seed-iteration-02/summary-snapshot.md'
(D/'summary-changes.patch').write_text(''.join(difflib.unified_diff(old.read_text().splitlines(True),(D/'summary-snapshot.md').read_text().splitlines(True),fromfile='seed-iteration-02/summary-snapshot.md',tofile=name+'/summary-snapshot.md')))
(D/'dispatch-status.json').write_text(json.dumps({'dispatched':False,'status':'ready_to_dispatch','preconditions_passed':True,'never_dispatched_prior_preflight':'expanded-iteration-01'},indent=2)+'\n')
progress['phase']='expanded-full-bank-readers-ready';progress['active_iteration']=name
(B/'progress.json').write_text(json.dumps(progress,indent=2)+'\n')
print(json.dumps({'iteration':name,'questions':n,'summary_sha256':H(D/'summary-snapshot.md'),'asked_facts_sha256':H(factpath),'prompt_a':str(D/'reader-a-prompt.txt'),'prompt_b':str(D/'reader-b-prompt.txt')},indent=2))
