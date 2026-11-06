from build_evidence import *
from collections import Counter
import subprocess

def validate(final_iteration=None,final_benchmark=None):
 checks=[]
 def check(name,ok,detail=None):checks.append({'check':name,'pass':bool(ok),'detail':detail})
 def unique_object(pairs):
  out={}
  for k,v in pairs:
   if k in out:raise ValueError('Duplicate JSON key: '+k)
   out[k]=v
  return out
 for path in sorted(R.rglob('*.json')):
  try:json.loads(path.read_text(),object_pairs_hook=unique_object);ok=True;detail=None
  except (ValueError,UnicodeError) as e:ok=False;detail=str(e)
  check('valid_unique_json:'+str(path.relative_to(R)),ok,detail)
 original=json.loads((R/'input-manifest.json').read_text())
 for path,expected in original['hashes'].items():
  p=Path(path)
  if path.endswith('rules/root.md'):p=R/'baseline-summary.md'
  check('original_input_hash:'+path,sha(p)==expected)
 seedq=json.loads((R/'benchmark-v1/questions.json').read_text())['questions'];seedk=json.loads((R/'benchmark-v1/answer-key.json').read_text())['answers']
 previous_q=previous_k=None
 cumulative_corrections={}
 for B in sorted(R.glob('benchmark-v*'),key=lambda p:int(p.name.split('-v')[-1])):
  q=json.loads((B/'questions.json').read_text())['questions'];k=json.loads((B/'answer-key.json').read_text())['answers'];ids=[x['id'] for x in q]
  check(str(B.name)+':unique_expected_ids',len(set(ids))==len(ids) and ids==[x['id'] for x in k])
  check(str(B.name)+':original_questions_preserved',q[:20]==seedq)
  correction_file=B/'key-corrections.json'
  if correction_file.exists():
   for c in json.loads(correction_file.read_text())['corrections']:cumulative_corrections[c['id']]=c
  adjusted_seed=[cumulative_corrections[x['id']]['new_entry'] if x['id'] in cumulative_corrections else x for x in seedk]
  check(str(B.name)+':original_answers_preserved_or_explicit_source_correction',k[:20]==adjusted_seed)
  if previous_q is not None:
   check(str(B.name)+':all_previous_questions_preserved',q[:len(previous_q)]==previous_q)
   correction_path=B/'key-corrections.json'
   if correction_path.exists():
    declarations=json.loads(correction_path.read_text())['corrections'];declared={x['id']:x for x in declarations};changed=[(a,b) for a,b in zip(previous_k,k) if a!=b]
    check(str(B.name)+':only_documented_key_corrections',set(a['id'] for a,b in changed)==set(declared) and all(a==declared[a['id']]['old_entry'] and b==declared[a['id']]['new_entry'] for a,b in changed))
    check(str(B.name)+':key_correction_source_evidence',all((B/x['independent_evidence'].split('#')[0]).resolve().exists() and x['source_references'] for x in declarations))
   else:check(str(B.name)+':all_previous_answers_preserved',k[:len(previous_k)]==previous_k)
  previous_q,previous_k=q,k
  for path,h in json.loads((B/'input-manifest.json').read_text())['hashes'].items():check(str(B.name)+':manifest_hash:'+Path(path).name,sha(Path(path))==h)
 for I in sorted(list(R.glob('seed-iteration-*'))+list(R.glob('expanded-iteration-*'))):
  man=json.loads((I/'input-manifest.json').read_text())
  for path,h in man['hashes'].items():check(f'{I.name}:frozen_hash:{Path(path).name}',sha(Path(path))==h)
  for path,h in man.get('prompt_hashes',{}).items():check(f'{I.name}:prospective_prompt_hash:{Path(path).name}',sha(Path(path))==h)
  for field in ['reader_protocol_template','protocol_change_note','continuation_instruction']:
   binding=man.get(field)
   if binding:check(f'{I.name}:prospective_{field}_hash',sha(Path(binding['path']))==binding['sha256'])
  policy=man.get('grading_scope_policy')
  if policy:check(f'{I.name}:prospective_scope_policy_hash',sha(Path(policy['path']))==policy['sha256'] and policy['saved_before_independent_grading'])
  raw_manifest=I/'raw-output-manifest.json'
  if raw_manifest.exists():
   for path,h in json.loads(raw_manifest.read_text())['hashes'].items():check(f'{I.name}:raw_output_hash:{Path(path).name}',sha(Path(path))==h)
  for stage_manifest in I.glob('reader-?-raw-output-manifest.json'):
   for path,h in json.loads(stage_manifest.read_text())['hashes'].items():check(f'{I.name}:staged_raw_output_hash:{Path(path).name}',sha(Path(path))==h)
  completion_note=I/'reader-a-protocol-completion-note.json'
  if completion_note.exists():
   note=json.loads(completion_note.read_text())
   check(f'{I.name}:self_reported_incomplete_original_preserved',sha(Path(note['original_output']))==note['sha256'])
   completion=json.loads((I/'reader-a-protocol-completion-result.json').read_text())
   check(f'{I.name}:completed_deliverable_hash',sha(I/'reader-a.json')==completion['final_raw_sha256'] and completion['no_factual_feedback_or_expected_clauses_supplied'])
  for installment_manifest in I.glob('reader-?-installment-manifest.json'):
   for checkpoint in json.loads(installment_manifest.read_text())['checkpoints']:
    check(f'{I.name}:installment_checkpoint:{Path(checkpoint["path"]).name}',sha(Path(checkpoint['path']))==checkpoint['sha256'])
  q=json.loads((I/'questions.json').read_text())['questions'];ids=[x['id'] for x in q]
  if man.get('execution_status')=='prepared_not_dispatched':
   dispatches=json.loads((R/'agent-dispatch-manifest.json').read_text())
   number=str(int(I.name.rsplit('-',1)[1]))
   no_dispatch=('expanded'+number+'_reader_' not in json.dumps(dispatches))
   no_outputs=not any((I/f'reader-{who}.json').exists() for who in ['a','b'])
   check(f'{I.name}:prepared_only_no_readers_dispatched',no_dispatch and no_outputs and I.name!=final_iteration)
   continue
  provenance=I/'model-provenance.json'
  check(f'{I.name}:runtime_model',provenance.exists() and json.loads(provenance.read_text()).get('actual_settings_confirmed'))
  results=I/'results.json'
  check(f'{I.name}:grades_present',results.exists())
  if not results.exists():continue
  g=json.loads(results.read_text());benchmark=man.get('benchmark','benchmark-v1');key={a['id']:a for a in json.loads((R/benchmark/'answer-key.json').read_text())['answers']}
  for who in ['a','b']:
   a=json.loads((I/f'reader-{who}.json').read_text())['answers'];rows=g[who]['grades']
   check(f'{I.name}:{who}:all_ids_once',Counter(x['id'] for x in a)==Counter(ids) and Counter(x['id'] for x in rows)==Counter(ids))
   raw_by_id={x['id']:x for x in a};question_by_id={x['id']:x for x in q}
   for row in rows:
    raw=raw_by_id[row['id']];question=question_by_id[row['id']]
    check(f'{I.name}:{who}:{raw["id"]}:grade_matches_raw_and_key',row['observed']==raw and row['question']==question['question'] and row['expected_answer']==key[raw['id']]['expected_answer'])
   totals={grade:sum(x['grade']==grade for x in rows) for grade in ['correct','partial','incorrect']}
   check(f'{I.name}:{who}:totals',totals==g[who]['totals'])
   if I.name==final_iteration:
    check(f'final:{who}:N_of_N',totals=={'correct':len(ids),'partial':0,'incorrect':0} and not any(x['unsupported_guess'] for x in rows))
    check(f'final:{who}:summary_support',all(x['summary_support']['status'] in {'supported','supported_for_stated_rulings'} for x in rows))
    check(f'final:{who}:all_requested_facts_resolved',all(x['requested_fact_checklist'] and all(f['status'] in {'satisfied','resolved','satisfied/resolved','context_not_requested','contextual not_requested','context-not-requested','not_requested'} for f in x['requested_fact_checklist']) for x in rows))
 if final_iteration:
  I=R/final_iteration
  if (I/'reader-a-installment-manifest.json').exists() or (I/'reader-b-installment-manifest.json').exists():
   turn_proof=json.loads((I/'reader-turn-provenance.json').read_text())
   check('final_all_reader_turns_actual_model',turn_proof['status']=='PASS' and len(turn_proof['readers'])==2 and all(x['all_turn_settings_confirmed'] for x in turn_proof['readers']))
  ids=[x['id'] for x in json.loads((I/'questions.json').read_text())['questions']]
  check('final_snapshot_byte_identical', (I/'summary-snapshot.md').read_bytes()==(ROOT/'rules/root.md').read_bytes())
  audit=json.loads((I/'source-audit.json').read_text())
  check('final_source_audit_pass',audit.get('verdict')=='PASS' and not audit.get('findings'))
  audit_inputs=audit.get('inputs',audit.get('input_hashes',{}))
  check('final_audit_exact_text',sha(I/'summary-snapshot.md') in json.dumps(audit_inputs))
  check('final_audit_authoritative_hashes',all(sha(p) in json.dumps(audit_inputs) for p in [ROOT/'extracted/root-rules.txt',ROOT/'source_pdfs/root-recovery.pdf']))
  final_manifest=json.loads((I/'input-manifest.json').read_text())
  if final_manifest.get('stamped_retest'):
   repair=final_manifest.get('post_stamp_source_repair')
   if repair:
    repair_path=R/repair['record']
    repair_record=json.loads(repair_path.read_text())
    check('stamped_requested_bytes_preserved_before_explicit_source_repair',repair_record['prior_summary_sha256']==final_manifest['stamped_retest']['coordinator_requested_hash'] and sha(R/'expanded-iteration-15/summary-snapshot.md')==repair_record['prior_summary_sha256'])
    check('post_stamp_repair_exact_record_and_final_bytes',sha(repair_path)==repair['record_sha256'] and sha(I/'summary-snapshot.md')==repair['repaired_summary_sha256']==repair_record['repaired_summary_sha256'] and repair_record['new_full_bank_pair_required'])
   else:check('stamped_final_requested_canonical_hash',sha(I/'summary-snapshot.md')==final_manifest['stamped_retest']['coordinator_requested_hash'])
   reuse=final_manifest.get('fresh_stamped_source_audit_reuse')
   if reuse:
    check('stamped_final_exact_fresh_audit_reuse',sha(R/reuse['audit'])==reuse['audit_sha256']==sha(I/'source-audit.json') and sha(R/reuse['delivery_proof'])==reuse['delivery_sha256']==sha(I/'source-auditor-delivery-audit.json') and reuse['summary_sha256']==sha(I/'summary-snapshot.md'))
   delivery_path=I/'source-auditor-delivery-audit.json'
   check('stamped_final_fresh_source_auditor_delivery_present',delivery_path.exists())
   if delivery_path.exists():
    delivery=json.loads(delivery_path.read_text())
    check('stamped_final_complete_source_and_summary_delivery',delivery['line_coverage_status']=='ALL_SOURCE_AND_SUMMARY_NONEMPTY_LINES_DELIVERED' and all(x['all_nonempty_lines_in_ordered_exact_blocks'] and x['sha256']==sha(Path(x['path'])) for x in delivery['inputs']))
    check('stamped_final_complete_pdf_text_delivery',len(delivery['pdf_pages'])==32 and delivery['pdf_sha256']==sha(ROOT/'source_pdfs/root-recovery.pdf') and all(x['all_nonempty_lines_in_ordered_exact_blocks'] for x in delivery['pdf_pages']))
    check('stamped_final_pdf_visual_inspection',bool(delivery['image_inspection_calls']))
    runtime=json.loads((R/'runtime-model-provenance.json').read_text())['records']
    fresh=[x for x in runtime if x['agent_path']==delivery['agent_path']]
    expected_auditor=final_manifest.get('final_source_audit',{}).get('agent_path','/root/stamped_source_auditor_01')
    check('stamped_final_source_auditor_fresh_actual_model',delivery['agent_path']==expected_auditor and len(fresh)==1 and fresh[0]['actual_model']=='gpt-6.1-sol' and fresh[0]['actual_effort']=='high')
    dispatches=json.loads((R/'agent-dispatch-manifest.json').read_text())['dispatches']
    auditor_requests=[x['arguments_without_message'] for x in dispatches if x['tool']=='spawn_agent' and x['arguments_without_message'].get('task_name')==delivery['agent_path'].split('/')[-1]]
    check('stamped_final_source_auditor_fresh_explicit_request',len(auditor_requests)==1 and auditor_requests[0].get('fork_turns')=='none' and auditor_requests[0].get('model')=='gpt-6.1-sol' and auditor_requests[0].get('reasoning_effort')=='high')
   final_source_binding=final_manifest.get('final_source_audit')
   if final_source_binding:
    check('final_source_report_and_delivery_exact_binding',sha(R/final_source_binding['report'])==final_source_binding['report_sha256']==sha(I/'source-audit.json') and sha(R/final_source_binding['delivery_proof'])==final_source_binding['delivery_sha256']==sha(I/'source-auditor-delivery-audit.json'))
    for path,h in final_source_binding['source_hashes'].items():
     check('final_extended_source_exact_hash:'+Path(path).name,sha(Path(path))==h and h in json.dumps(audit_inputs))
    extended=json.loads((I/'source-auditor-delivery-audit.json').read_text())
    check('final_complete_publisher_text_delivery',any(Path(x['path']).name=='publisher-rules-library-p16.txt' and x['all_nonempty_lines_in_ordered_exact_blocks'] and x['sha256']==sha(Path(x['path'])) for x in extended['inputs']))
    publisher=extended['publisher_json_representation']
    check('final_publisher_json_derivation_and_metadata_delivery',publisher['parsed_results_0_text_plus_newline_equals_txt'] and bool(publisher['metadata_matching_read_indices']) and publisher['raw_json_sha256']==sha(Path(publisher['raw_json_path'])) and publisher['text_sha256']==sha(Path(publisher['text_path'])))
    images=extended['image_delivery_validation']
    check('final_auditor_own_glyph_payload_delivery',images['mode']=='OWN_ACTUAL_RUNTIME_IMAGE_PAYLOADS_ONLY' and images['passed'] and images['all_actual_png_payload_bytes_match_local_pdf_pngs'] and not images['missing_required_physical_pages'])
    check('final_auditor_actual_raw_read_pairs_unchanged',all(sha(Path(x['raw_path']))==x['raw_sha256'] for x in extended['read_calls']))
    auditor_contexts=[json.loads(line)['payload'] for line in Path(extended['runtime_path']).open() if json.loads(line).get('type')=='turn_context']
    check('final_source_auditor_all_actual_turn_models',bool(auditor_contexts) and all(x.get('model')=='gpt-6.1-sol' and x.get('effort')=='high' for x in auditor_contexts))
  if (I/'reader-a-quote-audit.json').exists() or (I/'reader-b-quote-audit.json').exists():
   quotation_review_path=I/'quotation-review-validation.json'
   check('final_quotation_semantic_dispositions_present',quotation_review_path.exists())
   if quotation_review_path.exists():
    quotations=json.loads(quotation_review_path.read_text())
    check('final_quotation_semantic_review_pass',quotations.get('status')=='PASS' and quotations.get('no_material_or_unresolved_findings') and quotations.get('flagged_blocks_expected')==quotations.get('flagged_blocks_independently_disposed'))
    for path,h in quotations['hashes'].items():check('final_quotation_review_exact_input:'+Path(path).name,sha(Path(path))==h)
  for who in ['a','b']:
   delivery=json.loads((I/f'reader-{who}-delivery-audit.json').read_text())
   check(f'final:{who}:actual_complete_input_delivery',delivery['line_coverage_status']=='ALL_NONEMPTY_INPUT_LINES_DELIVERED' and len(delivery['inputs'])==2 and all(x['all_nonempty_lines_in_ordered_exact_blocks'] and x['sha256']==sha(Path(x['path'])) for x in delivery['inputs']))
  check('targeted_catalog_comparison',json.loads((R/'targeted-catalog-comparison.json').read_text())['status']=='PASS')
  ledger=json.loads((R/'coverage-ledger.json').read_text());review=json.loads((R/'coverage-review.json').read_text())
  check('coverage_two_consecutive_zero_addition_passes',len(ledger['passes'])>=2 and all(p['count']==0 and p.get('all_core_procedural_passages_mapped') for p in ledger['passes'][-2:]))
  check('coverage_review_pass',review.get('verdict')=='PASS')
  status=json.loads((R/'coverage-status.json').read_text())
  check('coverage_matches_final_benchmark',status.get('bank')==final_benchmark and status.get('question_count')==len(ids))
  check('coverage_review_current_input_hashes',all(sha(p) in json.dumps(review) for p in [R/final_benchmark/'questions.json',R/final_benchmark/'answer-key.json',R/'coverage-ledger.json']))
  check('all_passages_have_ids',all(x['questions'] for x in ledger['coverage_map']))
  protocols=json.loads((R/'reader-protocol-provenance.json').read_text())['pairs'];protocol=next(x for x in protocols if x['iteration']==final_iteration)
  check('final_readers_identical_prompt_except_output',protocol['same_saved_instructions_except_output_path'])
  check('final_readers_fresh_explicit_requests',all(x['fork_turns']=='none' and x['requested_model']=='gpt-6-luna' and x['requested_effort']=='high' for x in protocol['readers']))
  runtime=json.loads((R/'runtime-model-provenance.json').read_text())['records']
  experts=[x for x in runtime if 'reader_' not in x['agent_path']]
  check('actual_primary_and_reviewer_models',all(x['actual_model']=='gpt-6.1-sol' and x['actual_effort']=='high' for x in experts))
 for cmd in [[str(ROOT/'.venv/bin/python'),'-m','scripts.validate','rules/root.md'],['git','diff','--check','--','rules/root.md',str(R.relative_to(ROOT))]]:
  p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True);check('targeted_repository_check',p.returncode==0,{'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
 result={'status':('PASS' if final_iteration else 'PARTIAL_CHECKS_PASS') if all(x['pass'] for x in checks) else 'INCOMPLETE_OR_FAIL','final_iteration':final_iteration,'final_benchmark':final_benchmark,'checks':checks,'passed':sum(x['pass'] for x in checks),'total':len(checks),'scope':'Only assigned summary and evidence; shared catalogs/registries/stamping deferred to coordinator.'}
 save(R/'validation.json',result);return result
if __name__=='__main__':
 import sys
 print(json.dumps(validate(*(sys.argv[1:])))[0:250])
