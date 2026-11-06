from qa_tools import *
from collections import Counter
import subprocess,re
final_name=sys.argv[1];bank_name=sys.argv[2];dest=P/final_name;bank=P/bank_name
checks={};details={}
integrity();checks['source_hashes_unchanged']=True
orig=json.loads((P/'input-manifest.json').read_text());checks['baseline_preserved']=h(P/'baseline-summary.md')==orig['hashes']['rules/scythe.md']
checks['final_snapshot_byte_identical_to_canonical']=(dest/'summary-snapshot.md').read_bytes()==(ROOT/'rules/scythe.md').read_bytes()
seedq=json.loads((P/'questions.json').read_text())['questions'];seedk=json.loads((P/'answer-key.json').read_text())['answers'];q=json.loads((bank/'questions.json').read_text())['questions'];k=json.loads((bank/'answer-key.json').read_text())['answers'];ids=[x['id'] for x in q]
checks['final_ids_unique_and_contiguous']=ids==[f'Q{i:02}' for i in range(1,len(q)+1)] and ids==[x['id'] for x in k]
checks['original_seed_entries_preserved']=q[:len(seedq)]==seedq and k[:len(seedk)]==seedk
checks['expanded_versions_preserve_every_previous_entry']=True
previous_q,previous_k=seedq,seedk
for b in sorted(P.glob('expanded-v[0-9]*'),key=lambda x:int(x.name.split('-v')[-1])):
 bq=json.loads((b/'questions.json').read_text())['questions'];bk=json.loads((b/'answer-key.json').read_text())['answers'];assert bq[:len(previous_q)]==previous_q and bk[:len(previous_k)]==previous_k,b
 previous_q,previous_k=bq,bk
all_counts={};assessment_counts={};reader_count=grade_count=0
for d in sorted(P.glob('*-iteration-*')):
 if not d.is_dir():continue
 iq=json.loads((d/'questions.json').read_text())['questions'];ik=json.loads((d/'answer-key.json').read_text())['answers'];im=json.loads((d/'input-manifest.json').read_text());pr=json.loads((d/'model-provenance.json').read_text());expected=[x['id'] for x in iq]
 reports=[d/'results.json']
 reports+=sorted(d.glob('results-adjudicated-v*.json'),key=lambda x:int(x.stem.split('-v')[-1]))
 assert set(pr['readers'])=={'a','b'},d
 for name,sha in im['hashes'].items():assert h(d/name)==sha,(d,name,'hash changed')
 if d.name.startswith('seed-'):assert iq==seedq and ik==seedk,d
 all_counts[d.name]={};assessment_counts[d.name]={}
 for r in ['a','b']:
  actual=json.loads((d/f'reader-{r}.json').read_text())['answers'];ai={x['id']:x for x in actual}
  assert len(ai)==len(actual)==len(expected) and set(ai)==set(expected),(d,r,'reader IDs')
  for report in reports:
   res=json.loads(report.read_text());grades=res['readers'][r]['grades'];gi={x['id']:x for x in grades}
   assert len(gi)==len(grades)==len(expected) and set(gi)==set(expected),(d,r,report.name,'grade IDs')
   for x,y in zip(iq,ik):
    g=gi[x['id']];a=ai[x['id']];assert g['question']==x['question'] and g['expected_answer']==y['expected_answer'] and g['observed_answer']==a['answer'] and g['source_references']==y['source_references'],(d,r,x['id'],report.name)
   totals=dict(Counter(x['grade'] for x in grades));counts={g:totals.get(g,0) for g in ['correct','partial','incorrect']};assert counts==res['readers'][r]['totals']
   assessment_counts[d.name].setdefault(report.name,{})[r]=counts
   all_counts[d.name][r]=counts
   grade_count+=len(grades)
  assert pr['readers'][r]['runtime_contexts'] and all(c['model']=='gpt-6-luna' and c['effort']=='high' for c in pr['readers'][r]['runtime_contexts']),(d,r,'actual model')
  assert (d/f'reader-{r}-actual-prompt.txt').exists()
  reader_count+=len(actual)
for directory in [P]+sorted(P.glob('expanded-v[0-9]*')):
 manifest=json.loads((directory/'benchmark-manifest.json').read_text())
 assert h(directory/'questions.json')==manifest['questions_sha256'] and h(directory/'answer-key.json')==manifest['answer_key_sha256'],directory
checks['all_benchmark_version_hashes_preserved']=True
checks['grading_correction_transparent_and_preserved']=(P/'grading-correction.json').exists() and all((P/d/'results-adjudicated-v2.json').exists() for d in ['seed-iteration-02','seed-iteration-03','seed-iteration-04'])
checks['Q01_grading_correction_transparent_and_preserved']=(P/'q01-grading-correction.json').exists() and all((P/d/'results-adjudicated-v3.json').exists() for d in ['expanded-iteration-05','expanded-iteration-07','expanded-iteration-08'])
checks['all_reader_and_grade_ids_complete_once']=True;checks['all_grades_link_exact_expected_and_observed_answers']=True;checks['actual_reader_models_and_effort_confirmed']=True;checks['all_historical_snapshot_question_and_key_hashes_intact']=True
runtime=json.loads((P/'runtime-provenance.json').read_text())
for role,record in runtime.items():
 expected_model='gpt-6-luna' if (role.startswith(('seed_','expanded_','integrated_')) and role.endswith(('_a','_b'))) else 'gpt-6.1-sol'
 assert record['runtime_contexts'] and all(c['model']==expected_model and c['effort']=='high' for c in record['runtime_contexts']),(role,'actual agent model/effort')
checks['all_reader_reviewer_adjudicator_actual_model_settings_confirmed']=True
finalres=json.loads(effective_results(dest).read_text());checks['final_pair_full_pass']=all(v['totals']=={'correct':len(q),'partial':0,'incorrect':0} and all(not g['unsupported_guess'] for g in v['grades']) for v in finalres['readers'].values())
checks['final_bank_copy_matches_frozen_bank']=all((dest/n).read_bytes()==(bank/n).read_bytes() for n in ['questions.json','answer-key.json'])
audit_path=P/(sys.argv[3] if len(sys.argv)>3 else 'source-audit-05.json');audit=json.loads(audit_path.read_text());checks['source_audit_pass_no_findings']=audit.get('verdict')=='PASS' and not audit.get('findings') and not audit.get('material_findings')
# Audit schemas vary, so verify the exact final hash occurs in the independently written report.
checks['independent_audit_covers_final_hash']=h(dest/'summary-snapshot.md') in json.dumps(audit)
dispatch_path=audit_path.with_name(audit_path.stem+'-dispatch.json')
dispatch=json.loads(dispatch_path.read_text());auditor_role=dispatch['agent_path'].split('/')[-1];auditor_runtime=runtime[auditor_role]
checks['fresh_final_auditor_requested_without_forked_history']=dispatch['fork_turns']=='none' and dispatch['requested_model']=='gpt-6.1-sol' and dispatch['reasoning_effort']=='high'
checks['fresh_final_auditor_actual_model_and_single_context']=len(auditor_runtime['runtime_contexts'])==1 and auditor_runtime['runtime_contexts'][0]['model']=='gpt-6.1-sol' and auditor_runtime['runtime_contexts'][0]['effort']=='high'
review=json.loads((P/(sys.argv[4] if len(sys.argv)>4 else 'coverage-review-08.json')).read_text());checks['independent_coverage_challenge_pass']=str(review.get('verdict','')).upper()=='PASS' and not review.get('proposed_additions')
ledger=json.loads((P/'coverage-ledger.json').read_text());checks['two_latest_targeted_passes_zero_additions']=all(not x['accepted'] for x in ledger['passes'][-2:]);checks['passage_map_ids_valid']=all(set(x['question_ids'])<=set(ids) for x in json.loads((P/'source-coverage-map.json').read_text())['procedural_passages'])
if not (P/'validation.json').exists():save(P/'validation.json',{'status':'validation-in-progress'})
links=[]
for md in [P/'README.md',bank/'question-bank.md']:
 for raw in re.findall(r'\]\(([^)]+)\)',md.read_text()):
  if raw.startswith(('http:','https:','#')):continue
  target=raw.split('#')[0];links.append((str(md),target,(md.parent/target).exists()))
checks['report_local_links_resolve']=all(x[2] for x in links)
closure=None
if (P/'completion-audit.json').exists():
 closure=json.loads((P/'completion-audit.json').read_text());accepted=json.loads((P/'coordinator-final-acceptance.json').read_text());cv=json.loads((ROOT/'docs/quality/summary-qa/batches/2026-11-04-batch-231507/scythe-coordinator-validation.json').read_text())
 checks['completion_requirement_audit_pass']=closure['all_requirements_pass'] and all(r['status']=='PASS' for r in closure['requirements']) and closure['executed_reader_pairs']==15
 checks['completion_requirement_evidence_paths_resolve']=all(Path(path).is_absolute() and Path(path).exists() for r in closure['requirements'] for path in r['evidence'])
 checks['explicit_final_coordinator_acceptance']=accepted['accepted'] and accepted['canonical_sha256']==h(dest/'summary-snapshot.md')
 checks['coordinator_final_integration_pass_exact_bytes']=cv['canonical_sha256']==closure['final_summary_sha256']==h(dest/'summary-snapshot.md') and not cv['stamping_changed_tested_bytes'] and not cv['target_catalog_errors'] and cv['target_manifest_entry_matches_regeneration'] and cv['target_index_row_matches_regeneration'] and cv['structural_validation']=='PASS' and cv['targeted_git_diff_check']=='PASS'
commands=[]
for cmd in [['.venv/bin/python','-m','scripts.validate','rules/scythe.md'],['git','diff','--check','--','rules/scythe.md',str(P.relative_to(ROOT))]]:
 completed=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True);commands.append({'command':cmd,'exit_code':completed.returncode,'stdout':completed.stdout,'stderr':completed.stderr})
checks['targeted_repository_checks_pass']=all(x['exit_code']==0 for x in commands)
result={'checks':checks,'all_pass':all(checks.values()),'question_count':len(q),'reader_answers_checked':reader_count,'grades_checked':grade_count,'iteration_scores':all_counts,'assessment_versions':assessment_counts,'final_summary_sha256':h(dest/'summary-snapshot.md'),'source_hashes':{x:y for x,y in orig['hashes'].items() if x!='rules/scythe.md'},'commands':commands,'report_link_checks':links,'coordinator_work_remaining':'Audit recording, targeted stamp, shared index/manifest regeneration and final repository catalog checks are coordinator-owned. Retest exact stamped bytes if changed.'}
if closure:
 result.update(coordinator_work_remaining=None,coordinator_integration_completed=True,completion_audit=str(P/'completion-audit.json'),global_catalog_errors_outside_scope=closure['outside_scope_global_catalog_errors'],global_catalog_scope_note='No Scythe errors. Recorded outside-scope discrepancies were preserved; no claim of global catalog PASS.')
save(P/'validation.json',result);save(dest/'validation.json',result);print(json.dumps({'all_pass':result['all_pass'],'checks':checks,'reader_answers_checked':reader_count,'grades_checked':grade_count},indent=2));assert all(checks.values())
