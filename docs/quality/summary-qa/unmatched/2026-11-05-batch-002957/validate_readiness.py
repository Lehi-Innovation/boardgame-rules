from pathlib import Path
import hashlib,json,datetime,sys
P=Path(__file__).resolve().parent;R=P.parents[4];I=P/sys.argv[1];n=I.name.rsplit('-',1)[-1]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
result=read(I/'results.json');audit_path=Path(read(P/'progress.json')['source_audit']['current_exact_text']['path']);audit=read(audit_path);review=read(P/'current-v9-final-review/coverage-key-scope.json');validation=read(P/'validation-in-progress.json');integrity=read(I/'whole-entry-source-integrity-validation.json')
assert result['both_full_bank_pass'] and result['both_full_bank_semantic_pass']
assert audit['verdict']=='PASS' and not audit['findings']
canonical=R/'rules/unmatched.md';assert canonical.read_bytes()==(I/'summary-snapshot.md').read_bytes()==(audit_path.parent/'summary-snapshot.md').read_bytes()
assert sha(canonical)==audit['summary_sha256']==result['summary_sha256']==integrity['summary_sha256']
assert review['verdict']=='PASS' and all(v=='PASS' for v in review['verdicts'].values()) and review['two_zero_stopping_conclusion']['satisfied']
assert integrity['complete_disjoint_ids'] and integrity['question_count']==67
for r in ['a','b']:
 v=result['readers'][r];assert v['scores']=={'correct':67,'partial':0,'incorrect':0} and v['required_fact_count']==216 and v['unresolved_asked_facts']==0 and not v['unsupported_correct_guesses']
 assert v['raw_file_sha256']==sha(I/f'reader-{r}.json')==integrity['raw_file_sha256'][r]
assert all(x['every_field_preserved'] for x in integrity['packs'])
for b in result['grading_blocks']:assert sha(Path(b['path']))==b['sha256']
prov=read(P/'model-provenance.json')['agents'];tasks=['/root/'+I.name.replace('-','_')+'_reader_'+r for r in ['a','b']]+['/root/expanded'+n+'_grader_block'+str(b).zfill(2) for b in range(1,5)]+['/root/current_source_audit_'+audit_path.parent.name.rsplit('-',1)[-1],'/root/current_v9_final_challenge']
for task in tasks:
 a=next(x for x in prov if x['task']==task);assert a['confirmed'] and a['parent']=='01a1ad02-d3f0-7083-bb2c-847ca80bb819'
 expected='gpt-6-luna' if 'reader_' in task else 'gpt-6.1-sol';assert a['turns'] and all(t['model']==expected and t['effort']=='high' for t in a['turns'])
readers=[x for x in read(P/'actual-input-delivery-validation.json')['readers'] if x['iteration']==I.name];assert {x['reader'] for x in readers}=={'a','b'}
for x in readers:
 assert x['model_confirmed'] and len(x['receipts'])==3 and all(r['complete_contiguous'] for r in x['receipts'])
 for r in x['receipts']:assert sha(Path(r['path']))==r['sha256']
bounded=read(I/'bounded-input-delivery-validation.json');assert bounded['all_inputs_have_bounded_delivery']
graders=read(I/'grading/actual-input-delivery-validation.json')['graders'];assert {x['task'] for x in graders}==set(tasks[2:6])
for g in graders:
 assert g['actual_model_confirmed'] and len(g['verified_inputs'])==2
 for x in g['verified_inputs']:assert x['complete_contiguous'] and sha(Path(x['path']))==x['sha256']
generic_path=I/'generic-extraction-proof.json'
if generic_path.exists():
 generic=read(generic_path);assert generic['same_method_for_both_readers'] and generic['only_synthetic_neutral_fixtures'] and generic['neutral_test_count']>=6
 assert all(sha(Path(path))==value for path,value in generic['files'].items())
 execution=read(I/'generic-extraction-execution-provenance.json');assert execution['same_prebound_generic_method_supplied_to_both'] and len(execution['actors'])==2
 helper_path=next(Path(path) for path in generic['files'] if Path(path).name=='source_units.py');assert execution['provided_helper_sha256']==sha(helper_path)
 helper=helper_path.read_text()
 for r in ['a','b']:assert helper in (I/f'reader-{r}-prompt.txt').read_text()
adjudication_input=I/'adjudication/q63-b-inputs.json'
if adjudication_input.exists():
 adjudication=read(I/'adjudication/q63-b-assessment.json');assert adjudication['grade']=='correct' and all(x['assessment']=='satisfied' for x in adjudication['facts'])
 assert adjudication['raw_entry_canonical_sha256']==read(adjudication_input)['raw_entry_canonical_sha256'] and not adjudication['unsupported_correct_guess']
 review_proof=read(I/'adjudication/actual-delivery-validation.json');assert review_proof['complete_original_text_before_first_assessment_write'] and review_proof['actual_requested_fresh_model_confirmed']
 assert review_proof['assessment_sha256']==sha(I/'adjudication/q63-b-assessment.json')
timing=read(I/'prewrite-input-delivery-validation.json');assert timing['actor_count']==8 and timing['all_complete_text_inputs_before_first_target_write']
native=read(audit_path.parent/'native-scope-integrity-validation.json');assert native['all120_cell_coordinates_once'] and native['exactly_eight_original_images'] and native['source_audit_sha256']==sha(audit_path)
assert validation['canonical_candidate']['final_bank_blind_pass'] and validation['targeted_repository_validation']['exit_code']==0 and validation['targeted_git_diff_check']['exit_code']==0
stamped='verification: \"verified\"' in canonical.read_text();ready_status='ready_for_coordinator_final_publication' if stamped else 'ready_for_coordinator_inspection'
report={'status':ready_status,'goal_status':'active','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'canonical_path':str(canonical),'canonical_sha256':sha(canonical),'final_iteration':I.name,'question_count_per_reader':67,'required_fact_count_per_reader':216,'scores':{r:result['readers'][r]['scores'] for r in ['a','b']},'source_audit':str(audit_path.relative_to(P)),'coverage_review':'current-v9-final-review/coverage-key-scope.json','gates':{'both_same_iteration_all_67_correct':True,'no_missing_incorrect_unresolved_asked_facts':True,'no_unsupported_correct_guesses_replacing_summary_support':True,'exact_tested_audited_canonical_bytes':True,'source_and_bank_hash_integrity':True,'all_raw_fields_and_exact_source_spans':True,'actual_complete_reader_data_and_instruction_delivery':True,'bounded_reader_delivery_independently_proved':True,'all8_actor_inputs_before_first_factual_target_write':True,'generic_extraction_proof_and_actual_execution_traces':generic_path.exists(),'required_single_independent_whole_entry_review_complete':(not adjudication_input.exists() or review_proof['complete_original_text_before_first_assessment_write']),'native_source_scope_hashes_and_cell_receipts':True,'actual_complete_grader_input_delivery':True,'actual_requested_models_and_efforts':True,'targeted_repository_and_diff_checks':True},'limitations':['Known fixed-set tool-assisted regression, not held-out accuracy or proof of every conceivable scenario.','Fresh-context/instruction isolation; no OS-level filesystem sandbox claim.','Optional v2 Markdown metadata diagnostics are retained separately from whole-answer factual grading.','Ancillary catalog metadata remains outside independently authenticated normative audit scope.'],'generic_execution_deviations':read(I/'generic-execution-deviations.json') if (I/'generic-execution-deviations.json').exists() else None,'technical_delivery_deviations':read(I/'technical-delivery-correction.json') if (I/'technical-delivery-correction.json').exists() else None,'pending_coordinator_actions':(['Inspect retained final evidence for the exact coordinator-stamped bytes.','Accept final evidence and finalize shared publication/recording as coordinator.','Explicitly authorize worker goal completion.'] if stamped else ['Inspect retained evidence and exact canonical candidate.','Coordinator owns shared recording, generation and trust stamping.','After any stamping changes, verify final exact stamped text and required final checks before explicit goal-completion authorization.']),'independent_whole_entry_assessment':str((I/'adjudication/q63-b-assessment.json').relative_to(P)) if adjudication_input.exists() else None,'goal_completion_authorized':False}
(P/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('All readiness gates PASS; goal ACTIVE pending coordinator inspection and stamping verification.')
