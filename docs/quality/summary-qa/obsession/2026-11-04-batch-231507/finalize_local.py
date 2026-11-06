from qa_tools import *
from validate_evidence import run
import subprocess,re

def main():
 v=run();assert not v['errors'],v['errors']
 I=max((x.parent for x in P.glob('expanded-iteration-*/results.json')),key=lambda x:int(x.name.split('-')[-1]));f=ROOT/'rules/obsession.md';q=P/'expanded-v4/questions.json';k=P/'expanded-v4/answer-key.json'
 audits=[x for x in P.glob('final-source-audit-*/source-audit.json') if json.loads(x.read_text()).get('verdict')=='PASS' and (x.parent/'summary-snapshot.md').read_bytes()==f.read_bytes()]
 A=max(audits,key=lambda x:int(x.parent.name.split('-')[-1]));r=json.loads((I/'results.json').read_text());a=json.loads(A.read_text())
 assert f.read_bytes()==(I/'summary-snapshot.md').read_bytes()==(A.parent/'summary-snapshot.md').read_bytes()
 assert a['verdict']=='PASS' and a['summary_sha256']==sha(f)
 # The coordinator owns verification stamping. Only this explicitly known,
 # nonmaterial date finding may remain at local readiness.
 assert all(x.get('material') is False and x.get('type')=='metadata' and x.get('severity')=='minor' and x.get('location')=='Front matter: verification_date' for x in a.get('findings',[])),a.get('findings')
 for w in ['a','b']:
  assert all(r['readers'][w][x]==n for x,n in [('correct',62),('partial',0),('incorrect',0),('unsupported_guesses',0)])
 assert json.loads((P/'coverage-challenge-04.json').read_text())['verdict']=='PASS'
 ledger=json.loads((P/'coverage-ledger.json').read_text());assert [x['new_count'] for x in ledger['passes'][-2:]]==[0,0]
 assert [x['pass'] for x in ledger['passes'][-2:]]==[11,12]
 checks=[]
 for cmd in [[str(ROOT/'.venv/bin/python'),'-m','scripts.validate','rules/obsession.md'],['git','diff','--check','--','rules/obsession.md',str(P.relative_to(ROOT))]]:
  cp=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True);checks.append({'command':cmd,'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr});assert cp.returncode==0
 dump(P/'repository-checks.json',{'targeted_checks':checks,'coordinator_owned_pending':['semantic audit recording','targeted verification stamping','index and manifest regeneration','final catalog/repository checks and explicit integration follow-up'],'no_shared_registry_or_generated_file_edits_by_this_game_chat':True})
 total_answers=total_grades=0;iterations=[]
 names=[x.parent.name for x in sorted(P.glob('seed-iteration-*/results.json'))+sorted(P.glob('expanded-iteration-*/results.json'))]
 for name in names:
  it=P/name;rr=json.loads((it/'results.json').read_text());n=len(json.loads((it/'questions.json').read_text())['questions']);entry={'path':name,'bank':rr['benchmark_version'],'question_count':n,'summary_sha256':sha(it/'summary-snapshot.md'),'results_path':str(it/'results.json')}
  for w in ['a','b']:
   raw=json.loads((it/f'reader-{w}.json').read_text());total_answers+=len(raw['answers']);total_grades+=len(rr['readers'][w]['grades']);entry[f'reader_{w}']={x:rr['readers'][w].get(x,0) for x in ['correct','partial','incorrect','unsupported_guesses']}
  iterations.append(entry)
 assert total_answers==total_grades==sum(2*x['question_count'] for x in iterations)
 # Verify actual runtime provenance for every tested fresh reader.
 prov=provenance();reader_tasks={f'/root/obs_{"seed" if name.startswith("seed") else "expanded"}_{name.split("-")[-1]}_{w}' for name in names for w in ['a','b']};assert len(reader_tasks)==2*len(iterations)
 actual={x['task']:x for x in prov};assert reader_tasks<=actual.keys()
 for task in reader_tasks:
  assert actual[task]['contexts'] and all(c['model']=='gpt-6-luna' and c['effort']=='high' for c in actual[task]['contexts'])
 for x in prov:
  if x['task'] not in reader_tasks:assert x['contexts'] and all(c['model']=='gpt-6.1-sol' and c['effort']=='high' for c in x['contexts'])
 for x in prov:
  expected='gpt-6-luna' if x['task'] in reader_tasks else 'gpt-6.1-sol'
  assert x['parent_spawn_settings'] and all(t['fork_turns']=='none' and t['model']==expected and t['reasoning_effort']=='high' for t in x['parent_spawn_settings'])
 manifest={'benchmark_version':'expanded-v4','question_count':62,'reader_snapshot':str(I/'summary-snapshot.md'),'canonical_summary':str(f),'source_audit':str(A),'inputs':[{'path':str(x),'sha256':sha(x)} for x in [f,I/'summary-snapshot.md',q,k,ROOT/'extracted/obsession-rules.txt',ROOT/'source_pdfs/obsession-universal-rules.pdf',ROOT/'source_pdfs/obsession-corrigendum-1.0.pdf',P/'publisher-fr-base-rules.pdf',P/'publisher-fr-base-rules.txt',A,P/'coverage-challenge-04.json',I/'reader-a.json',I/'reader-b.json',I/'results.json',P/f'grading-audit-{I.name.split("-")[-1]}.json']]};dump(P/'final-input-manifest.json',manifest)
 proof={'local_result':'PASS','coordinator_integration':'pending explicit follow-up; goal remains active','question_count':62,'benchmark_version':'expanded-v4','all_procedural_passage_groups_mapped':len(ledger['coverage']),'two_final_zero_addition_passes':[x['pass'] for x in ledger['passes'][-2:]],'independent_coverage_verdict':'PASS','final_source_audit':'PASS','final_audit_snapshot_matches_reader_and_canonical':True,'canonical_summary_sha256':sha(f),'every_benchmark_input_hash_matches':True,'original_seed_questions_preserved':True,'original_seed_keys_preserved_except_explicit_Q09_version_correction':True,'expanded_original56_question_wording_preserved':v['expanded_question_prefix_preserved'],'all_reader_ids_and_grade_ids_exactly_once':True,'every_grade_matches_original_question_fixed_key_and_raw_answer':True,'saved_reader_answer_count':total_answers,'saved_grade_count':total_grades,'fresh_blind_reader_count':len(reader_tasks),'all_actual_reader_models_and_efforts_confirmed':True,'actual_reviewer_models_and_efforts_confirmed':True,'readers':{w:{x:r['readers'][w][x] for x in ['correct','partial','incorrect','unsupported_guesses']} for w in ['a','b']},'targeted_repository_checks':'PASS','errors':[]};dump(P/'final-validation.json',proof)
 scores='\n'.join('| '+e['path']+' | '+e['bank']+' | '+str(e['question_count'])+' | '+' / '.join(str(e['reader_a'][x]) for x in ['correct','partial','incorrect'])+' | '+' / '.join(str(e['reader_b'][x]) for x in ['correct','partial','incorrect'])+' |' for e in iterations)
 perlinks='\n'.join(f'- {e["path"]}: [summary]({e["path"]}/summary-snapshot.md), [questions]({e["path"]}/questions.json), [reader A]({e["path"]}/reader-a.json), [reader B]({e["path"]}/reader-b.json), [detailed grades]({e["path"]}/results.json), [input hashes]({e["path"]}/input-manifest.json).' for e in iterations)
 report=(P/'final-report-template.md').read_text().replace('{{SCORES}}',scores).replace('{{ITERATION_LINKS}}',perlinks).replace('{{SUMMARY_SHA}}',sha(f)).replace('{{COVERAGE_GROUPS}}',str(len(ledger['coverage']))).replace('{{FINAL_ITERATION}}',I.name).replace('{{AUDIT_DIR}}',A.parent.name).replace('{{GRADING_AUDIT}}',f'grading-audit-{I.name.split("-")[-1]}.json').replace('{{TOTAL_ANSWERS}}',format(total_answers,',')).replace('{{READER_COUNT}}',str(len(reader_tasks)))
 (P/'README.md').write_text(report)
 # Local relative report/bank links, excluding the deliberate publisher web URL.
 broken=[]
 for doc in [P/'README.md',P/'expanded-v4/question-bank.md',P/'seed-v1/question-bank.md',P/'seed-v2/question-bank.md']:
  for dest in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',doc.read_text()):
   if '://' in dest or dest.startswith('#'):continue
   if not (doc.parent/dest.split('#')[0]).exists():broken.append({'document':str(doc),'target':dest})
 assert not broken,broken
 proof['source_audit_findings']=a.get('findings',[]);proof['expanded_v4_previous60_questions_and_keys_preserved']=v['expanded_v4_previous60_questions_and_keys_identical_to_v3'];proof['Q22_key_correction_and_historical_regrading']='coordinator-review-01/q22/grading-corrections.json';proof['task_prompt_inspection_limit']='Runtime task bodies encrypted, not inspected/decrypted; intended prompts and unencrypted parent spawn settings/child turn contexts retained. Environment-only captures are not full delivered prompts.';proof['report_links_resolve']=True;proof['report_sha256']=sha(P/'README.md');dump(P/'final-validation.json',proof)
 status={'game':'Obsession','slug':'obsession','bgg_id':231733,'phase':'local-qa-passed-awaiting-coordinator-integration','status':'ready-for-coordinator','question_count':62,'question_bank_version':'expanded-v4','iterations':iterations,'final_reader_scores':proof['readers'],'source_audit':{'verdict':'PASS','path':str(A),'snapshot_path':str(A.parent/'summary-snapshot.md'),'summary_sha256':sha(f)},'coverage_review':{'verdict':'PASS','path':str(P/'coverage-challenge-04.json'),'zero_addition_passes':[11,12]},'report_path':str(P/'README.md'),'blocking_reason':None,'integration_required':'Wait for explicit game-specific coordinator audit-recording/stamping/repository-check follow-up; retest complete bank if exact bytes change; goal intentionally remains active.','final_snapshot_path':str(I/'summary-snapshot.md'),'source_paths':[str(ROOT/'extracted/obsession-rules.txt'),str(ROOT/'source_pdfs/obsession-universal-rules.pdf'),str(ROOT/'source_pdfs/obsession-corrigendum-1.0.pdf'),str(P/'publisher-fr-base-rules.pdf'),str(P/'publisher-fr-base-rules.txt')],'hashes':{'canonical_summary':sha(f),'final_snapshot':sha(I/'summary-snapshot.md'),'source':sha(ROOT/'extracted/obsession-rules.txt'),'questions':sha(q),'answer_key':sha(k),'source_pdf':sha(ROOT/'source_pdfs/obsession-universal-rules.pdf'),'corrigendum':sha(ROOT/'source_pdfs/obsession-corrigendum-1.0.pdf'),'supplemental_pdf':sha(P/'publisher-fr-base-rules.pdf'),'report':sha(P/'README.md')},'validation_path':str(P/'final-validation.json'),'actual_models_verified':True,'task_prompt_inspection_limit':proof['task_prompt_inspection_limit'],'persistent_goal_status':'active'};dump(P/'game-status.json',status)
 print(json.dumps({'status':status['status'],'scores':proof['readers'],'summary_sha256':sha(f),'total_answers':total_answers,'total_grades':total_grades,'errors':proof['errors'],'report':status['report_path']}))
if __name__=='__main__':main()
