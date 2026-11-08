import json,hashlib,collections,subprocess
from pathlib import Path
from quote_texts import quote_texts
R=Path(__file__).parent.resolve();h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();read=lambda p:json.loads(p.read_text()); checks={};issues=[]
def check(name,value):
 checks[name]=value
 if value is not True:issues.append(name)
manifest=read(R/'input-manifest.json');check('assigned_sources_unchanged',all(h(Path(x['path']))==x['sha256'] for x in manifest['sources']))
seedq=read(R/'seed-v1/questions.json')['questions'];seedk=read(R/'seed-v1/answer-key.json')['answers'];expq=read(R/'expanded-v10/questions.json')['questions'];expk=read(R/'expanded-v10/answer-key.json')['answers'];check('original_20_questions_preserved',expq[:20]==seedq);check('original_20_answer_records_preserved',expk[:20]==seedk)
check('original_31_questions_preserved',expq[:31]==read(R/'expanded-v1/questions.json')['questions']);check('original_31_answer_records_preserved_except_explicit_Q27_source_correction',all(a==b for a,b in zip(expk[:31],read(R/'expanded-v1/answer-key.json')['answers']) if a['id']!='Q27'))
check('seed_bank_hashes_preserved',all(h(R/'seed-v1'/n)==v for n,v in manifest['seed_hashes'].items()))
cancel=read(R/'expanded-iteration-10/cancellation.json');check('canceled_superseded_dispatch_has_no_claimed_reader_outputs',not any(cancel['outputs_present_at_cancellation'].values()) and not any((R/'expanded-iteration-10'/f'reader-{l}.json').exists() for l in 'ab'))
bf=read(R/'expanded-v10/bank-freeze-manifest.json');check('expanded_bank_freeze_hashes_intact',all(h(R/'expanded-v10'/n)==v for n,v in bf['files'].items()))
history=[R/'seed-v1']+[R/f'expanded-v{i}' for i in range(1,11)]
chain=[]
for old,new in zip(history,history[1:]):
 oq=read(old/'questions.json')['questions'];ok=read(old/'answer-key.json')['answers'];nq=read(new/'questions.json')['questions'];nk=read(new/'answer-key.json')['answers'];chain.append({'from':old.name,'to':new.name,'questions_preserved':nq[:len(oq)]==oq,'baseline_answers_preserved':nk[:len(ok)]==ok,'explicit_source_correction_only':new.name=='expanded-v9' and all(a==b for a,b in zip(nk[:len(ok)],ok) if a['id']!='Q27')})
check('every_historical_question_answer_prefix_preserved',all(x['questions_preserved'] and (x['baseline_answers_preserved'] or x['explicit_source_correction_only']) for x in chain))
correction=read(R/'expanded-v9/source-key-correction.json');vh=lambda o:hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
old27=next(x for x in read(R/'expanded-v8/answer-key.json')['answers'] if x['id']=='Q27');new27=next(x for x in expk if x['id']=='Q27')
check('declared_Q27_source_correction_exactly_matches_historical_and_current_records',old27==correction['historical_record'] and new27==correction['corrected_record'] and vh(old27)==correction['old_record_sha256'] and vh(new27)==correction['new_record_sha256'] and correction['question_wording_changed'] is False)
(R/'original-entry-preservation.json').write_text(json.dumps(chain,indent=2)+'\n')
for D in sorted(R.glob('*iteration-*')):
 if not D.is_dir():continue
 im=read(D/'input-manifest.json');q=read(D/'questions.json')['questions'];expected=[x['id'] for x in q];detail={};check(D.name+'_frozen_inputs_unchanged',all(h(D/n)==v for n,v in im['inputs'].items()))
 if im.get('prompt_hashes'):check(D.name+'_prebound_prompts_unchanged',all(h(D/f'reader-{l}-prompt.txt')==v for l,v in im['prompt_hashes'].items()))
 if im.get('grading_inputs'):check(D.name+'_grading_inputs_unchanged',all(h(D/n)==v for n,v in im['grading_inputs'].items()))
 if not all((D/f'reader-{l}.json').exists() for l in 'ab'):continue
 result=read(D/'results.json') if (D/'results.json').exists() else None
 for l in 'ab':
  raw=read(D/f'reader-{l}.json');ids=[x['id'] for x in raw['answers']];check(D.name+'_'+l+'_all_ids_once',collections.Counter(ids)==collections.Counter(expected));qs=[]
  for a in raw['answers']:
   for s in quote_texts(a.get('operative_quotes',[])):
    qs.append(s in (D/'summary-snapshot.md').read_text())
  check(D.name+'_'+l+'_all_quotes_verbatim',all(qs))
  if result:
   rr=result['readers'][l];gs=rr['grades'];check(D.name+'_'+l+'_grade_ids_once',collections.Counter(x['id'] for x in gs)==collections.Counter(expected));rawby={x['id']:x for x in raw['answers']};check(D.name+'_'+l+'_grades_match_raw_entries',all(x.get('observed_raw_entry',rawby[x['id']])==rawby[x['id']] for x in gs));detail[l]={'raw_sha256':h(D/f'reader-{l}.json'),'counts':rr['counts']}
 (D/'validation.json').write_text(json.dumps({'checks':{k:v for k,v in checks.items() if k.startswith(D.name)},'readers':detail},indent=2)+'\n')
final=R/'stamped-iteration-02';check('final_snapshot_equals_canonical',final.exists() and (final/'summary-snapshot.md').read_bytes()==Path('rules/lords-of-vegas.md').read_bytes())
stamp=read(final/'stamp-integrity.json');authorization=read(final/'coordinator-authorization-snapshot.json')
check('coordinator_authorized_exact_stamped_hash_and_complete39_bank',authorization['authorized'] is True and authorization['question_count']==len(expq)==39 and authorization['exact_stamped_summary_sha256']==h(final/'summary-snapshot.md')==stamp['exact_stamped_summary_sha256'])
check('canonical_verification_stamp_present', 'verification: "verified"' in Path('rules/lords-of-vegas.md').read_text().split('---',2)[1] and Path('rules/lords-of-vegas.md').read_text().count('<!-- verification:begin -->')==1 and Path('rules/lords-of-vegas.md').read_text().count('<!-- verification:end -->')==1)
native=read(R/'stamped-iteration-01/native-delivery-proof.json');check('new_post_stamp_auditor_actual_seven_native_images_verified',native['verified'] is True and native['image_count']==7 and native['all_expected_distinct_pages_seen'] and native['all_views_before_report_saved'] and native['source_audit_sha256']==h(final/'source-audit.json') and all(Path(x['path']).exists() and h(Path(x['path']))==x['sha256'] for x in native['images']))
neutral=read(R/'stamped-iteration-01/q27-neutral-adjudication.json');effective=read(R/'stamped-iteration-01/adjudicated-results.json')
check('single_historical_neutral_decision_preserved_and_applied_without_resampling',effective['one_neutral_only_no_resampling'] and effective['neutral_report_sha256']==h(R/'stamped-iteration-01/q27-neutral-adjudication.json') and effective['decision_applied']['effective_grade']==neutral['grade'].lower() and effective['primary_results_sha256']==h(R/'stamped-iteration-01/results.json') and effective['primary_raw_responses_and_grades_unchanged'])
check('neutral_packet_and_complete_original_entry_hashes_verified',all(h(Path(x['path']))==x['sha256'] for x in neutral['input_hashes']) and neutral['original_entry_hash_verification']['match'] and neutral['original_entry_hash_verification']['computed_sha256']==neutral['original_entry_hash_verification']['expected_sha256'])
neutral_packet=read(Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/coordinator-checks/lords-stamped01-q27-neutral-packet.json'));original27=next(x for x in read(R/'stamped-iteration-01/reader-a.json')['answers'] if x['id']=='Q27');entry27h=hashlib.sha256(json.dumps(original27,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest();check('neutral_compared_actual_complete_original_Q27_entry',neutral_packet['complete_original_entry']==original27 and entry27h==neutral_packet['original_entry_canonical_sha256']==neutral['original_entry_hash_verification']['computed_sha256'])
dispatches=read(R/'dispatch-provenance.json');nd=[x for x in dispatches if x['task']=='stamped_q27_neutral'];check('exactly_one_explicit_fresh_Sol_high_neutral_dispatch',len(nd)==1 and nd[0]['model']=='gpt-6.1-sol' and nd[0]['effort']=='high' and nd[0]['fork_turns']=='none')
if (final/'results.json').exists():
 result=read(final/'results.json');check('both_final_readers_all_correct',all(x['counts']=={'correct':len(expq),'partial':0,'incorrect':0} and not x.get('unsupported_guesses',[]) for x in result['readers'].values()));check('all_final_required_fact_statuses_met',all(f['status']=='met' for rr in result['readers'].values() for g in rr['grades'] for f in g.get('required_facts',g.get('required_answer_facts',[]))))
else:check('both_final_readers_all_correct',False)
if (final/'source-audit.json').exists():
 audit=read(final/'source-audit.json');check('all_source_audit_input_hashes_unchanged',all(Path(x['path']).exists() and h(Path(x['path']))==x['sha256'] for x in audit['input_hashes']));check('fresh_independent_source_audit_PASS',audit['verdict']=='PASS' and not [f for f in audit.get('findings',[]) if not f.get('resolved',False)]);check('current_source_audit_binds_exact_final_candidate',any(Path(x['path']).name=='summary-snapshot.md' and Path(x['path']).read_bytes()==(final/'summary-snapshot.md').read_bytes() and x['sha256']==h(final/'summary-snapshot.md') for x in audit['input_hashes']))
else:check('fresh_independent_source_audit_PASS',False)
if (R/'source-key-v10-review.json').exists():check('fresh_coverage_review_PASS',read(R/'source-key-v10-review.json')['verdict']=='PASS_FOR_DECLARED_EXPANDED_V10_SOURCE_LIMITS_BENCHMARK')
else:check('fresh_coverage_review_PASS',False)
ledger=read(R/'coverage-ledger-v10.json');check('two_final_zero_addition_passes',all(not x['accepted'] for x in ledger['passes'][-2:]));check('all_questions_in_scope_map_once',collections.Counter(x['id'] for x in read(R/'expanded-v10/scope-map.json')['entries'])==collections.Counter(x['id'] for x in expq))
mode=ledger['benchmark_scope_decision'];check('declared_source_limits_contract_identical_in_all_final_bank_artifacts',all(read(R/'expanded-v10'/n)['benchmark_scope_decision']==mode for n in ['scope-map.json','grading-key.json','bank-freeze-manifest.json']))
proof=read(R/'runtime-provenance.json')
check('actual_models_and_efforts_confirmed',all(r['turn_contexts'] and all(c['actual_model']==r['requested_model'] and c['actual_effort']=='high' for c in r['turn_contexts']) for r in proof['agents']))
required_tasks=['/root/seed_reader_a','/root/seed_reader_b','/root/seed_reader2_a','/root/seed_reader2_b','/root/coverage_challenge','/root/final_scope_coverage','/root/source_audit_final','/root/expanded_reader_a','/root/expanded_reader_b','/root/final_grader_block1','/root/final_grader_block2','/root/clean_final_coverage','/root/expanded_reader2_a','/root/expanded_reader2_b','/root/final_grader2_block1','/root/final_grader2_block2','/root/source_only_v8_review','/root/expanded_reader3_a','/root/expanded_reader3_b','/root/final_grader3_block1','/root/final_grader3_block2','/root/source_audit_revision2','/root/source_key_v9_review','/root/expanded_reader4_a','/root/expanded_reader4_b','/root/final_grader4_block1','/root/final_grader4_block2','/root/expanded_reader5_a','/root/expanded_reader5_b','/root/final_grader5_block1','/root/final_grader5_block2','/root/expanded_reader7_a','/root/expanded_reader7_b','/root/final_grader7_block1','/root/final_grader7_block2','/root/source_audit_revision3','/root/expanded_reader8_a','/root/expanded_reader8_b','/root/final_grader8_block1','/root/final_grader8_block2','/root/expanded_reader9_a','/root/expanded_reader9_b','/root/final_grader9_block1','/root/final_grader9_block2','/root/source_audit_stamped1','/root/expanded_reader10_a','/root/expanded_reader10_b','/root/final_grader10_block1','/root/final_grader10_block2','/root/stamped_q27_neutral']
by_task={r['task']:r for r in proof['agents']}
check('required_actual_agents_present',all(t in by_task for t in required_tasks))
check('all_required_complete_model_visible_delivery',all(t in by_task and by_task[t]['content_delivery_proof'] and all(x['all_character_slices_seen'] for x in by_task[t]['content_delivery_proof']) for t in required_tasks))
if (final/'grading-validation.json').exists():
 gp=read(final/'grading-validation.json');check('all_final_asked_fact_records_once',all(x['all_expected_once'] and x['expected']==x['observed']==x['unique'] for x in gp['facts'].values()))
if (final/'grader-input-validation.json').exists():
 bundles=read(final/'grader-input-validation.json');check('final_grader_bundle_hashes_intact',all(h(Path(b['path']))==b['sha256'] for b in bundles['blocks']))
 reconstructed=[];reconstruction_ok=True;scopeby={x['id']:x for x in read(final/'scope-map.json')['entries']};keyby={x['id']:x for x in read(final/'grading-key.json')['answers']};rawby={l:{x['id']:x for x in read(final/f'reader-{l}.json')['answers']} for l in 'ab'}
 for b in bundles['blocks']:
  bundle=read(Path(b['path']));dictionary=bundle['dictionary']
  def decode(v):
   if isinstance(v,dict) and set(v)=={'__literal_quote__'}:return dictionary[v['__literal_quote__']]
   if isinstance(v,dict):return {k:decode(x) for k,x in v.items()}
   if isinstance(v,list):return [decode(x) for x in v]
   return v
  reconstruction_ok=reconstruction_ok and bundle['benchmark_scope_decision']==mode
  for e in bundle['entries']:
   reconstructed.append(e['id']);reconstruction_ok=reconstruction_ok and e['asked_scope']==scopeby[e['id']] and e['effective_fixed_key']==keyby[e['id']] and all(decode(e['raw_entries'][l])==rawby[l][e['id']] for l in 'ab')
 check('final_grader_bundle_reconstruction_and_fixed_key_exact',reconstruction_ok and collections.Counter(reconstructed)==collections.Counter(x['id'] for x in expq))
 if all((final/f'grader-block-{n}-results.json').exists() for n in [1,2]):
  report_inputs_ok=True
  for n in [1,2]:
   found={}
   def collect_input_hashes(v,context=None):
    if isinstance(v,dict):
     path=v.get('path',v.get('file_path',v.get('filename',context)))
     if path and isinstance(v.get('sha256'),str):
      pp=Path(path);pp=pp if pp.is_absolute() or pp.exists() else final/pp
      found[str(pp.resolve())]=v['sha256']
     for k,x in v.items():collect_input_hashes(x,k)
    elif isinstance(v,list):
     for x in v:collect_input_hashes(x,context)
    elif context and isinstance(v,str) and len(v)==64 and context.endswith(('.md','.json')):
     pp=Path(context);pp=pp if pp.is_absolute() or pp.exists() else final/pp;found[str(pp.resolve())]=v
   collect_input_hashes(read(final/f'grader-block-{n}-results.json')['input_hashes'])
   report_inputs_ok=report_inputs_ok and all(found.get(str(p.resolve()))==h(p) for p in [final/'summary-snapshot.md',final/f'grader-block-{n}.json'])
  check('final_grader_report_input_hashes_match_exact_assigned_files',report_inputs_ok)
if (final/'source-audit-reuse.json').exists():check('source_audit_exact_byte_reuse',read(final/'source-audit-reuse.json')['exact_bytes_equal'] and h(final/'summary-snapshot.md')==read(final/'source-audit-reuse.json')['audited_snapshot_sha256'])
if (final/'source-audit-reuse.json').exists():
 reuse=read(final/'source-audit-reuse.json');check('original_current_source_audit_hash_matches_reuse',h(Path(reuse['original_audit']))==reuse['original_audit_sha256'] and h(final/'source-audit.json')==reuse['original_audit_sha256'])
if (final/'raw-response-manifest.json').exists():check('final_raw_response_manifest_intact',all(h(final/n)==v for n,v in read(final/'raw-response-manifest.json')['files'].items()))
else:check('final_raw_response_manifest_intact',False)
clean=read(R/'independence-tool-check.json');final_roles=['/root/source_audit_revision2','/root/source_key_v9_review','/root/expanded_reader5_a','/root/expanded_reader5_b','/root/final_grader5_block1','/root/final_grader5_block2','/root/expanded_reader7_a','/root/expanded_reader7_b','/root/final_grader7_block1','/root/final_grader7_block2','/root/source_audit_revision3','/root/expanded_reader8_a','/root/expanded_reader8_b','/root/final_grader8_block1','/root/final_grader8_block2','/root/expanded_reader9_a','/root/expanded_reader9_b','/root/final_grader9_block1','/root/final_grader9_block2','/root/source_audit_stamped1','/root/expanded_reader10_a','/root/expanded_reader10_b','/root/final_grader10_block1','/root/final_grader10_block2','/root/stamped_q27_neutral'];cb={x['task']:x for x in clean};check('final_roles_no_metadata_reads',all(t in cb and not cb[t]['agent_or_chat_metadata_reads'] for t in final_roles))
completion_auth_path=Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/coordinator-checks/lords-final-completion-authorization.json')
coordinator_done=False
if completion_auth_path.exists():
 ca=read(completion_auth_path);cp=Path(ca['actual_local_publication_validation']);pv=read(cp);coordinator_done=ca['authorized'] is True and ca['summary_sha256']==h(Path('rules/lords-of-vegas.md')) and h(cp)==ca['actual_local_publication_validation_sha256'] and pv['slugs']==['lords-of-vegas'] and all(pv[k] is True for k in ['non_selected_index_lines_preserved','non_selected_manifest_entries_preserved','selected_manifest_entries_match_regeneration','selected_index_rows_match_regeneration']);check('coordinator_final_completion_authorization_matches_current_bytes_and_publication',coordinator_done)
validation=subprocess.run(['.venv/bin/python','-m','scripts.validate','rules/lords-of-vegas.md'],capture_output=True,text=True);check('targeted_structural_validation',validation.returncode==0)
whitespace=subprocess.run(['git','diff','--check','--','rules/lords-of-vegas.md',str(R.relative_to(Path.cwd()))],capture_output=True,text=True);check('targeted_git_diff_check',whitespace.returncode==0)
# Untracked files are not covered by git diff; inspect them directly too.
ws=[]
for f in [Path('rules/lords-of-vegas.md'),*R.rglob('*.md'),*R.rglob('*.py')]:
 for n,l in enumerate(f.read_text().splitlines(),1):
  if l.rstrip()!=l:ws.append({'file':str(f),'line':n})
check('untracked_authored_text_has_no_trailing_whitespace',not ws)
result={'checks':checks,'pending_or_failed':issues,'benchmark_scope':'expanded-v10 source-knowledge/source-limits; not unqualified earlier definite-physical-actor gameplay certification','original_definite_physical_actor_target_recovered':False,'coordinator_final_inspection_and_publication_pending':not coordinator_done,'targeted_validation_output':validation.stdout,'git_diff_check_output':whitespace.stdout+whitespace.stderr,'whitespace_findings':ws,'shared_catalog_and_stamping':'Reserved for coordinator; worker does not modify shared catalog, registry, banner, index or manifest.','canonical_sha256':h(Path('rules/lords-of-vegas.md'))}
(R/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'checks_passed':sum(v is True for v in checks.values()),'check_count':len(checks),'pending_or_failed':issues},indent=2))
