from pathlib import Path
import json,hashlib,collections,subprocess,difflib
B=Path(__file__).parent.resolve();ROOT=B.parents[4];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
checks=[]
def check(name,condition,detail=None):checks.append({'check':name,'pass':bool(condition),'detail':detail})
r=subprocess.run([str(ROOT/'.venv/bin/python'),str(B/'restore_preserved_derived_inputs.py')],cwd=ROOT,text=True,capture_output=True)
check('preserved_derived_input_bytes_available',r.returncode==0,{'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
sm=read(B/'source-manifest.json')['paths_and_sha256']
check('assigned_source_hashes_unchanged',all(H(ROOT/p)==h for p,h in sm.items()),sm)
extra=read(B/'supplemental-source-manifest.json');check('supplemental_primary_capture_hashes_unchanged',all(H(Path(x['path']))==x['sha256'] for x in extra['source_records']),len(extra['source_records']))
extra2=read(B/'supplemental-source-manifest-v2.json');check('supplemental_primary_v2_capture_hashes_unchanged',all(H(Path(x['path']))==x['sha256'] for x in extra2['source_records']),len(extra2['source_records']))
previous=extra2
for version in [3,4]:
 extra_next=read(B/f'supplemental-source-manifest-v{version}.json')
 check(f'supplemental_primary_v{version}_capture_hashes_unchanged',all(H(Path(x['path']))==x['sha256'] for x in extra_next['source_records']),len(extra_next['source_records']))
 check(f'supplemental_primary_v{version}_previous_prefix_preserved',extra_next['source_records'][:len(previous['source_records'])]==previous['source_records'])
 previous=extra_next
first40=(B/'card-scope-source/provenance-initial-40.jsonl').read_bytes();check('initial_scope_provenance_preserved',first40==b''.join((B/'card-scope-source/provenance.jsonl').read_bytes().splitlines(keepends=True)[:40]))
banks=['seed-v1']+[f'expanded-v{i}' for i in range(1,21)]
for n,bank in enumerate(banks):
 d=B/bank;q=read(d/'questions.json')['questions'];k=read(d/'answer-key.json')['answers'];ids=[x['id'] for x in q]
 check(bank+'_unique_ids',len(ids)==len(set(ids)) and ids==[x['id'] for x in k],len(ids))
 if n:
  old=B/banks[n-1];oq=read(old/'questions.json')['questions'];ok=read(old/'answer-key.json')['answers']
  if bank=='expanded-v6':
   corrections=read(d/'scope-corrections.json');changed={x['id'] for a,b,x in zip(oq,q,q) if a!=b}|{x['id'] for a,b,x in zip(ok,k,k) if a!=b}
   byq={x['id']:x for x in q};byk={x['id']:x for x in k};oldq={x['id']:x for x in oq};oldk={x['id']:x for x in ok}
   check(bank+'_only_explicit_scope_corrections',changed=={'Q100','Q105'} and all(c['old_question']==oldq[c['id']] and c['new_question']==byq[c['id']] and c['old_key']==oldk[c['id']] and c['new_key']==byk[c['id']] for c in corrections))
  elif bank=='expanded-v8':
   corrections=read(d/'key-corrections.json');byk={x['id']:x for x in k};oldk={x['id']:x for x in ok};changed={b['id'] for a,b in zip(ok,k) if a!=b}
   check(bank+'_only_explicit_key_precision_correction',q[:len(oq)]==oq and changed=={'Q105'} and all(c['old_key']==oldk[c['id']] and c['new_key']==byk[c['id']] and c['question_unchanged'] for c in corrections))
  elif bank=='expanded-v16':
   corrections=read(d/'key-corrections.json');byk={x['id']:x for x in k};oldk={x['id']:x for x in ok};changed={b['id'] for a,b in zip(ok,k) if a!=b}
   check(bank+'_only_explicit_Q18_asked_survival_correction',q[:len(oq)]==oq and changed=={'Q18'} and all(c['old_key']==oldk[c['id']] and c['new_key']==byk[c['id']] for c in corrections))
  elif bank=='expanded-v17':
   corrections=read(d/'question-corrections.json');byq={x['id']:x for x in q};oldq={x['id']:x for x in oq};changed={b['id'] for a,b in zip(oq,q) if a!=b}
   check(bank+'_only_explicit_Q157_source_wording_correction',changed=={'Q157'} and k[:len(ok)]==ok and all(c['old_question']==oldq[c['id']] and c['new_question']==byq[c['id']] and c['key_unchanged'] and c['timing_request_preserved'] and c['no_hard_ask_removed'] for c in corrections))
  else:
   check(bank+'_previous_entries_preserved',q[:len(oq)]==oq and k[:len(ok)]==ok)
  seedq=read(B/'seed-v1/questions.json')['questions'];seedk=read(B/'seed-v1/answer-key.json')['answers']
  if bank.startswith('expanded-') and int(bank.rsplit('v',1)[1])>=16:
   check(bank+'_original_seed20_questions_and19_keys_preserved_with_versioned_Q18_correction',q[:20]==seedq and all(a==z for a,z in zip(k[:20],seedk) if a['id']!='Q18') and k[17]==read(B/'expanded-v16/key-corrections.json')[0]['new_key'])
  else:check(bank+'_original_seed20_preserved',q[:20]==seedq and k[:20]==seedk)
 m=read(d/'input-manifest.json')
 check(bank+'_frozen_hashes_match',all(H(ROOT/p)==v for p,v in m['sha256'].items()))
 if bank=='expanded-v19':
  oldmap=read(old/'asked-fact-map.json')['questions'];newmap=read(d/'asked-fact-map.json')['questions'];c=read(d/'map-corrections.json')[0]
  check(bank+'_Q84_only_two_map_precision_strings',oldmap[83]==c['old_map'] and newmap[83]==c['new_map'] and all(a==z for a,z in zip(oldmap,newmap) if a['id']!='Q84') and sum(a!=z for a,z in zip(oldmap[83]['requested_clauses'][0]['required_facts'],newmap[83]['requested_clauses'][0]['required_facts']))==2 and oldmap[83]['key_context_not_required']==newmap[83]['key_context_not_required'] and c['old_question']==c['new_question'] and c['old_key']==c['new_key'])
  check(bank+'_170_questions_505_facts',len(q)==170 and sum(len(c['required_facts']) for x in newmap for c in x['requested_clauses'])==505)
 if bank=='expanded-v20':
  oldmap=read(old/'asked-fact-map.json')['questions'];newmap=read(d/'asked-fact-map.json')['questions'];sc=read(d/'core-scope-credit.json');osc=read(old/'core-scope-credit.json');correction=read(d/'metadata-corrections.json');a=read(B/'working-novelty-adjudication-14.json')['coverage_decisions'][0]
  check(bank+'_all170_prior_map_entries_exact_and171_506',newmap[:170]==oldmap and len(q)==len(newmap)==171 and sum(len(c['required_facts']) for x in newmap for c in x['requested_clauses'])==506)
  check(bank+'_only_Q36_Q164_prior_scope_rows_changed', [x['id'] for x,y in zip(sc['questions'][:170],osc['questions']) if x!=y]==['Q36','Q164'] and correction['Q36_scope']['old']==osc['questions'][35] and correction['Q36_scope']['new']==sc['questions'][35] and correction['Powerstorm_scope_source_reference']['old']==osc['questions'][163]['primary_sources'][2] and correction['Powerstorm_scope_source_reference']['new']==sc['questions'][163]['primary_sources'][2])
  check(bank+'_Q171_exact_refined_source_only_new_branch',q[170]['question']==a['literal_surviving_pretest_question'] and k[170]['answer']==a['source_correct_answer'] and [f for c in newmap[170]['requested_clauses'] for f in c['required_facts']]==a['minimum_new_required_facts'] and len(a['minimum_new_required_facts'])==1)
  counts=collections.Counter(x['scope_result'] for x in sc['questions']);overlay=sc['working_scope_credit_overlay']
  check(bank+'_working_scope_counts_and_no_grade_waiver',dict(counts)=={'base_supported':154,'mixed_supported_and_noncredited':14,'noncredited_pending_base_proof':3} and overlay['working_question_counts_for171']=={'base_supported':154,'mixed_supported_and_noncredited':14,'noncredited_only':3} and overlay['working_audited_clause_counts_after_explicit_element_grant']=={'base_supported':484,'unverified_base_reachability':26,'generalized_engine_regression':1} and sc['questions'][35]['all_four_conditional_grading_facts_retained'] and len(newmap[35]['requested_clauses'][0]['required_facts'])==4 and sc['scope_revision_v20']['audited_clause_total']==511 and sc['scope_revision_v20']['required_grading_fact_total']==506)
  corrections=read(B/'coverage-v20-source-corrections.json');ledger=read(B/'coverage-ledger.json');patches=corrections['working_source_reference_patches']
  def ptr(value,pointer):
   for part in pointer.strip('/').split('/'):value=value[int(part)] if isinstance(value,list) else value[part]
   return value
  check(bank+'_current_source_transcription_errata_versioned',len(patches)==3 and all(ptr(ledger,p['pointer'])==p['new'] and hashlib.sha256(p['new'].get('transcription',p['new'].get('transcribed_passage')).encode()).hexdigest()==p['new']['transcription_sha256'] for p in patches) and H(Path(corrections['prior_ledger_preserved']['path']))==corrections['prior_ledger_preserved']['sha256'])
iterations=[]
for d in sorted(B.glob('*iteration-*')):
 if not (d/'input-manifest.json').exists():continue
 m=read(d/'input-manifest.json');q=read(d/'questions.json')['questions'];ids=[x['id'] for x in q];bank=m['benchmark_version'];key={x['id']:x for x in read(B/bank/'answer-key.json')['answers']}
 check(d.name+'_question_copy',read(d/'questions.json')==read(B/bank/'questions.json'))
 check(d.name+'_frozen_input_hashes',all(H(Path(p))==v['sha256'] for p,v in m['inputs'].items()))
 results=read(d/'results.json') if (d/'results.json').exists() else None
 dispatch=read(d/'dispatch-status.json') if (d/'dispatch-status.json').exists() else {}
 if dispatch.get('dispatched') is False or dispatch.get('status')=='never_dispatched':
  check(d.name+'_undispatched_preserved',not results and not any((d/f'reader-{r}.json').exists() for r in 'ab'),dispatch)
  iterations.append({'path':d.name,'question_count':len(ids),'results_present':False,'dispatched':False})
  continue
 for r in 'ab':
  p=d/f'reader-{r}.json'
  if not p.exists():check(d.name+f'_reader_{r}_exists',False);continue
  out=read(p);answers=out['answers'];counts=collections.Counter(x['id'] for x in answers)
  check(d.name+f'_reader_{r}_ids_once',set(counts)==set(ids) and all(v==1 for v in counts.values()))
  allowed={str((d/'summary-snapshot.md').resolve()),str((d/'questions.json').resolve())}
  declared={str(Path(x.get('file',x.get('path',''))).resolve()) for x in out['inputs_read']}
  check(d.name+f'_reader_{r}_declared_inputs_only_summary_questions',declared==allowed and len(out['inputs_read'])==2)
  for inp in out['inputs_read']:
   path=Path(inp.get('file',inp.get('path','')));actual=len(path.read_text());ranges=inp.get('read_ranges',inp.get('complete_read_ranges',inp.get('ranges',inp.get('delivered_character_ranges',[]))))
   pairs=[(x['start'],x['end']) if isinstance(x,dict) else tuple(x) for x in ranges]
   cover=bool(pairs) and pairs[0][0]==0 and pairs[-1][1]==actual and all(b-a<=6000 and b>a for a,b in pairs) and all(pairs[i][1]==pairs[i+1][0] for i in range(len(pairs)-1))
   check(d.name+f'_reader_{r}_delivery_'+path.name,cover and H(path)==inp['sha256'],{'characters':actual,'ranges':pairs})
   if d.name.startswith('expanded-'):
    cap=inp.get('output_cap_tokens');check(d.name+f'_reader_{r}_output_cap_'+path.name,isinstance(cap,int) and cap>=4000,cap)
  if results:
   rr=results['readers'][f'reader-{r}'];grades=rr['grades'];gc=collections.Counter(x['id'] for x in grades);by={x['id']:x for x in answers}
   check(d.name+f'_reader_{r}_grades_once',set(gc)==set(ids) and all(v==1 for v in gc.values()))
   check(d.name+f'_reader_{r}_expected_observed_integrity',all(g['expected']==key[g['id']] and g['observed']==by[g['id']] for g in grades))
   count=collections.Counter(x['grade'] for x in grades);check(d.name+f'_reader_{r}_totals',all(count[t]==rr['totals'][t] for t in ['correct','partial','incorrect']),dict(count))
 iterations.append({'path':d.name,'question_count':len(ids),'results_present':results is not None})
# Confirm actual model metadata for readers and reviewers.
prov=read(B/'model-provenance.json')
for p in prov:
 expected='gpt-6-luna' if 'reader' in p['agent'] else ('gpt-6-sol' if p['agent']=='/root/scope_and_coverage_09' else 'gpt-6.1-sol')
 check('runtime_'+p['agent'],bool(p['settings']) and all(x=={'model':expected,'effort':'high'} for x in p['settings']),p['settings'])
# Canonical/final checks are enabled once progress names a final snapshot.
progress=read(B/'progress.json');final=progress.get('final_snapshot_path')
deliveryproof=B/'coverage-delivery-validation.json'
if deliveryproof.exists():
 proof=read(deliveryproof)
 check('completed_coverage_reviews_full_delivery',proof['all_passed'] and all(H(B/x['report'])==x['report_sha256'] and (not x.get('linked_read_ledger') or H(Path(x['linked_read_ledger']['path']))==x['linked_read_ledger']['sha256']) for x in proof['reports']),{'reports':len(proof['reports']),'path':str(deliveryproof)})
for proofname,ledgername in [('novelty10-delivery-validation.json','coverage-novelty-adjudication-10-read-ledger.json'),('novelty11-delivery-validation.json','coverage-novelty-adjudication-11-read-ledger.json'),('Q71-delivery-validation.json','base-reachability-Q71-check-01-read-ledger.json'),('novelty12-delivery-validation.json','native-panel-novelty-adjudication-12-read-ledger.json')]:
 proof=read(B/proofname)
 check(proofname+'_exact_completed_ledger',proof['all_passed'] and H(B/ledgername)==proof['ledger_sha256'])
proof=read(B/'panel-delivery-validation.json')
check('native_panel_and_baseline_delivery_exact_ledgers',proof['all_passed'] and all(H(B/x['ledger'])==x['sha256'] for x in proof['ledgers']))
proof=read(B/'working-sweeps37-38-delivery-validation.json')
check('working_sweeps37_38_exact_delivery_and_reconstruction',proof['status']=='PASS' and proof['summary']['failed']==0 and all(H(Path(x['path']))==x['sha256'] for x in proof['validated_working_artifacts']) and all(x['exact_all_fields_object_equality'] and H(Path(x['current_path']))==x['current_full_file_sha256'] for x in proof['exact_bank_reconstruction'].values()),{'checks':proof['summary']['checks'],'bank':'expanded-v18','working_evidence_only':True})
proof=read(B/'novelty13-delivery-validation.json')
check('novelty13_exact_completed_delivery_and_source_precision',proof['status']=='VALID' and proof['passed_check_count']==proof['check_count'] and not proof['exceptions'] and all(H(B/n)==h for n,h in proof['immutable_artifact_expected_sha256'].items()),{'checks':proof['check_count'],'no_global_verdict':True})
proof=read(B/'working-sweeps39-40-delivery-validation.json')
check('working_sweeps39_40_exact_delivery_zero_records_and_reconstruction',proof['status']=='PASS' and proof['summary']['failed']==0 and all(H(B/n)==h for n,h in proof['working_artifact_hashes'].items()) and proof['summary']['pass39_new_questions']==proof['summary']['pass40_new_questions']==0 and H(Path(proof['separate_source_annotation_reinspection']['path']))==proof['separate_source_annotation_reinspection']['sha256'],{'checks':proof['summary']['checks'],'two_working_zeros_only_not_independent_PASS':True})
proof=read(B/'source-audit08-delivery-validation.json');adopt=read(B/'source-audit08-adoption.json');nonpass=[x for x in proof['checks'] if not x['passed']]
check('sourceaudit08_exact_delivery_with_scoped_render_diagnostic',proof['counts']['blocking_failed_checks']==0 and proof['counts']['successful_text_slices']==92 and proof['counts']['visual_sources']==56 and len(nonpass)==1 and nonpass[0]['name']=='publisher legend complete PNG byte reproducibility' and nonpass[0]['kind']=='nonblocking_render_diagnostic' and adopt['explicit_diagnostic_disposition']['membership_top600_pixels_exact'] and all(H(B/n)==h for n,h in proof['frozen_artifact_sha256'].items()),{'checks':proof['counts']['checks'],'nonblocking_diagnostics':1,'raw_diagnostic_preserved':True})
actual=adopt['coordinator_actual_pre_report_delivery_model_verification'];external=read(Path(actual['path']))
check('sourceaudit08_coordinator_actual_delivery_and_model_verified',H(Path(actual['path']))==actual['sha256'] and external['verified'] and external['summary_sha256']==H(ROOT/'rules/spirit-island.md') and external['audit_sha256']==H(B/'source-audit-final-08.json') and external['actual_initial_spawn']=={'task_name':'final_source_audit_08','model':'gpt-6.1-sol','reasoning_effort':'high','fork_turns':'none'},'Delivery/model verification only; final coverage/readers remain independent gates.')
auditinfo=progress.get('source_audit',{})
if (B/'scope11-delivery-validation.json').exists():
 proof=read(B/'scope11-delivery-validation.json');adopt11=read(B/'scope11-adoption.json')
 check('scope11_exact_completed_delivery_and_inventory',proof['validation_verdict']=='PASS' and not proof['actual_failures'] and all(x['passed'] for x in proof['checks']) and all(H(B/n)==h for n,h in proof['frozen_completed_artifacts'].items()) and all(H(B/n)==h for n,h in proof['frozen_benchmark_inputs'].items()) and proof['checked_counts']=={'frozen_input_hashes':75,'text_inputs':21,'primary_text_slices':207,'redelivery_records':8,'native_images':54,'questions':170,'mapped_grading_facts':505,'checks':1709},'Filesystem and recorded-attestation consistency; not an independent historical-transport/perception proof or semantic coverage PASS.')
 check('scope11_parent_adoption_exact_raw_evidence',all(H(B/n)==h for n,h in adopt11['raw_bindings'].items()) and adopt11['review_outcome']=='FAIL preserved; no coverage or stopping PASS' and adopt11['full_current_bank']['coverage_gap_count']==1 and adopt11['no_expanded_pair_dispatched'])
if (B/'novelty14-delivery-validation.json').exists():
 proof=read(B/'novelty14-delivery-validation.json')
 check('novelty14_complete_recorded_evidence_and_exact_inputs',proof['status']=='VALID_FOR_RECORDED_EVIDENCE' and proof['check_count']==888 and proof['filesystem_check_count']==693 and proof['recorded_attestation_check_count']==195 and not proof['exceptions'] and all(x['ok'] for x in proof['checks']) and all(H(B/n)==h for n,h in proof['immutable_expected_sha256'].items()) and proof['counts']['current_questions']==170 and proof['counts']['current_asked_facts']==505 and proof['counts']['all_new_recorded_slices']==28 and proof['counts']['fresh_native_full_view_records']==10,'Filesystem checks and recorded-attestation checks distinct; no new global coverage verdict.')
if (B/'working-sweeps41-42-delivery-validation.json').exists():
 proof=read(B/'working-sweeps41-42-delivery-validation.json');working=read(B/'working-source-sweeps-41-42.json');adopt=read(B/'working41-42-adoption.json')
 check('working41_42_exact_delivery_reconstruction_and_raw1_0',proof['passed']==579 and proof['failed']==0 and all(x['pass'] for x in proof['checks']) and proof['report_sha256']==H(B/'working-source-sweeps-41-42.json') and proof['ledger_sha256']==H(B/'working-source-sweeps-41-42-read-ledger.json') and working['delivery_validation']['helper_sha256']==H(B/'working-sweeps41-42-delivery-validator.py') and [x['new_question_count'] for x in working['passes']]==[1,0] and working['current_questions']==171 and working['current_required_facts']==506 and not working['global_fresh_independent_PASS'],'Retained scope-boundary proposal is not a bank addition or two-zero closure; source/scope adjudication15 independent.')
 check('working41_42_parent_adoption_exact_raw_evidence',all(H(B/n)==h for n,h in adopt['raw_evidence'].items()) and adopt['actual_working_counts']==[1,0] and adopt['no_two_zero_or_independent_coverage_or_reader_PASS'])
if isinstance(auditinfo,dict) and auditinfo.get('status')=='PASS':
 audit=read(Path(auditinfo['path']));candidate=ROOT/audit['candidate']
 check('current_source_audit_exact_bytes',audit['verdict']=='PASS' and not audit['findings'] and audit['candidate_sha256']==H(candidate)==H(ROOT/'rules/spirit-island.md'))
 delivery=collections.defaultdict(list)
 for item in audit['source_delivery']:delivery[item['path']].append(item)
 for name,rows in delivery.items():
  path=ROOT/name;s=path.read_text();pairs=[(x['start'],x['end']) for x in rows]
  complete=pairs[0][0]==0 and pairs[-1][1]==len(s) and all(a[1]==b[0] for a,b in zip(pairs,pairs[1:]))
  integrity=all(0<x['end']-x['start']<=6000 and not x['truncated'] and x['source_sha256']==H(path) and x['slice_sha256']==hashlib.sha256(s[x['start']:x['end']].encode()).hexdigest() for x in rows)
  check(Path(auditinfo['path']).stem+'_delivery_'+path.name,complete and integrity,{'slices':len(rows),'characters':len(s)})
if final:
 final=Path(final);check('final_snapshot_matches_canonical_bytes',final.read_bytes()==(ROOT/'rules/spirit-island.md').read_bytes(),H(final))
 finalresults=read(final.parent/'results.json');n=finalresults['question_count']
 proof=read(final.parent/'operative-unit-boundary-validation.json')
 check('final_source_boundary_diagnostics_completed_and_exact',proof['validation_completed'] and proof['format_diagnostics_only'] and proof['grading_may_proceed'] and proof['summary_sha256']==H(final) and all(x['raw_output_sha256']==H(final.parent/(x['reader']+'.json')) for x in proof['checks']))
 proof=read(final.parent/'grader-delivery-validation.json');check('final_grader-delivery-validation.json',proof['all_passed'])
 check('final_pair_complete_correct',all(rr['totals']['correct']==n and rr['totals']['partial']==0 and rr['totals']['incorrect']==0 and all(g['grade']=='correct' and not g.get('unsupported_guesses') and not g.get('missing_requested_material_facts') and not g.get('contradictions') for g in rr['grades']) for rr in finalresults['readers'].values()),{r:rr['totals'] for r,rr in finalresults['readers'].items()})
 check('coverage_two_zero_passes_and_fresh_challenge',progress.get('coverage_stopping_rule',{}).get('independent_challenge')=='PASS' and progress.get('coverage_review',{}).get('status')=='PASS',progress.get('coverage_stopping_rule'))
 auditpath=progress.get('source_audit',{}).get('path') if isinstance(progress.get('source_audit'),dict) else None
 if auditpath:
  audit=read(Path(auditpath));check('independent_final_source_audit_PASS',audit.get('verdict')=='PASS' and not audit.get('findings') and audit.get('candidate_sha256')==H(final),auditpath)
# Scope validation: no global mutation jobs.
r=subprocess.run([str(ROOT/'.venv/bin/python'),'-m','scripts.validate','rules/spirit-island.md'],cwd=ROOT,text=True,capture_output=True)
check('targeted_repository_validate',r.returncode==0,{'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
r=subprocess.run(['git','diff','--check','--','rules/spirit-island.md',str(B.relative_to(ROOT))],cwd=ROOT,text=True,capture_output=True)
check('targeted_git_diff_check',r.returncode==0,{'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
ws=[]
for p in [ROOT/'rules/spirit-island.md']+list(B.rglob('*.md')):
 for i,l in enumerate(p.read_text().splitlines(),1):
  if l.rstrip()!=l:ws.append([str(p),i])
check('untracked_markdown_whitespace',not ws,ws)
report={'game':'Spirit Island','canonical_summary_sha256':H(ROOT/'rules/spirit-island.md'),'completion_gates_enabled':bool(final),'current_source_audit_status':progress.get('source_audit',{}).get('status'),'current_coverage_review_status':progress.get('coverage_review',{}).get('status'),'checks':checks,'all_passed':all(x['pass'] for x in checks),'iterations':iterations,'note':'Catalog registration/audit recording/stamping/global generation reserved to coordinator. Historical failing reader grades preserved and are expected; integrity of those iterations must still pass. Passing working integrity checks does not imply pending source/coverage/final-reader gates have passed.'}
write(B/'validation.json',report)
print(json.dumps({'checks':len(checks),'all_passed':report['all_passed'],'failures':[x for x in checks if not x['pass']]},indent=2))
