from pathlib import Path
import json,hashlib,collections,subprocess,sys,re
P=Path(__file__).parent
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
checks={};details={};final_name=sys.argv[1] if len(sys.argv)>1 else 'stamped-iteration-03'
v1=read(P/'bank-v1/questions.json');k1=read(P/'bank-v1/answer-key.json');previous=None
for D in sorted(P.glob('bank-v*')):
 q=read(D/'questions.json');k=read(D/'answer-key.json');bh=read(D/'benchmark-hashes.json')
 checks[D.name+'_frozen_hashes']=all(h(D/f)==v for f,v in bh.items())
 checks[D.name+'_original_20_preserved']=q['questions'][:20]==v1['questions'] and k['answers'][:20]==k1['answers']
 checks[D.name+'_ids_once']=len({a['id'] for a in q['questions']})==len(q['questions'])==len(k['answers']) and [a['id'] for a in q['questions']]==[a['id'] for a in k['answers']]
 checks[D.name+'_source_references_present']=all(x.get('source_references') for x in k['answers'])
 if previous:
  pq,pk=previous;checks[D.name+'_all_previous_entries_preserved']=q['questions'][:len(pq['questions'])]==pq['questions'] and k['answers'][:len(pk['answers'])]==pk['answers']
 previous=q,k
original=read(P/'input-manifest.json')['original_inputs']
checks['original_authoritative_source_unchanged']=h('extracted/orl-ans-rules.txt')==h(P/'authoritative-source.txt')==original['extracted/orl-ans-rules.txt']
checks['original_summary_preserved']=h(P/'original-summary.md')==original['rules/orl-ans.md']
for D in sorted([*P.glob('seed-iteration-*'),*P.glob('expanded-iteration-*'),*P.glob('stamped-iteration-*')]):
 if not D.is_dir():continue
 q=read(D/'questions.json');bank=q['benchmark_version'];k=read(P/bank/'answer-key.json');expected=[x['id'] for x in q['questions']];m=read(D/'input-manifest.json')
 local={'frozen_inputs_unchanged':all(h(f)==v for f,v in m['sha256'].items()),'questions_identical_to_benchmark':(D/'questions.json').read_bytes()==(P/bank/'questions.json').read_bytes()};counts={}
 if (D/'results.json').exists():
  result=read(D/'results.json');prov=read(D/'model-provenance.json')
  local['both_models_confirmed']=set(prov['readers'])=={'a','b'} and all(x['confirmed'] for x in prov['readers'].values())
  for who in ['a','b']:
   raw=read(D/f'reader-{who}.json');a=raw['answers'];r=result['readers'][who];g=r['grades'];qa={x['id']:x for x in a}
   local[who+'_all_ids_once']=collections.Counter(x['id'] for x in a)==collections.Counter(expected) and collections.Counter(x['id'] for x in g)==collections.Counter(expected)
   local[who+'_grades_align_raw_key_questions']=all(x['observed_answer']==qa[x['id']] and x['expected_answer']==k['answers'][i]['expected_answer'] and x['question']==q['questions'][i]['question'] and x['source_references']==k['answers'][i]['source_references'] for i,x in enumerate(g))
   counter=collections.Counter(x['grade'] for x in g);actual={z:counter[z] for z in ['correct','partial','incorrect']};local[who+'_totals_match']=actual==r['counts'];counts[who]=actual
  if D.name==final_name:local['both_full_pass']=all(x=={'correct':len(expected),'partial':0,'incorrect':0} for x in counts.values()) and all(not x['unsupported_correct_guess'] for r in result['readers'].values() for x in r['grades'])
  local['raw_output_hashes']={f'reader-{who}.json':h(D/f'reader-{who}.json') for who in ['a','b']}
 elif (D/'iteration-state.json').exists() and read(D/'iteration-state.json')['state']=='superseded-before-reader-dispatch':
  local['superseded_before_dispatch']=True;local['no_reader_output_claimed']=not (D/'reader-a.json').exists() and not (D/'reader-b.json').exists()
 else:local['grading_complete']=False
 local['question_count']=len(expected);local['scores']=counts
 (D/'validation.json').write_text(json.dumps(local,indent=2)+'\n');details[D.name]=local;checks[D.name+'_integrity']=all(v for v in local.values() if isinstance(v,bool))
final=P/final_name;audit=read(final/'source-audit.json')
if final_name.startswith('stamped-iteration-'):
 original_stamp=(P/'stamped-iteration-01/summary-snapshot.md').read_text();current_final=(final/'summary-snapshot.md').read_text()
 checks['coordinator_stamped_header_preserved']=original_stamp[:original_stamp.index('## Overview')]==current_final[:current_final.index('## Overview')]
checks['final_snapshot_equals_canonical']=(final/'summary-snapshot.md').read_bytes()==Path('rules/orl-ans.md').read_bytes()
checks['final_audit_pass_no_findings']=audit['verdict']=='PASS' and not audit['findings'] and not audit.get('essential_source_gaps')
checks['final_source_audit_inputs_match']=all(h(v['path'])==v['sha256'] for v in audit['file_hashes'])
checks['final_audit_exact_snapshot']=audit['summary_path']==str((final/'summary-snapshot.md').resolve()) and any(v['path']==str((final/'summary-snapshot.md').resolve()) and v['sha256']==h(final/'summary-snapshot.md') for v in audit['file_hashes'])
checks['matching_pdf_provenance_and_extraction']=h(P/'matching-rulebook.pdf')==read(P/'source-provenance.json')['sha256'] and read(P/'source-provenance.json')['normalized_extraction_identical']
checks['supplement_pdf_provenance']=h(P/'base-clarification-invasion-2015.pdf')==read(P/'base-clarification-provenance.json')['sha256']
prov=read(P/'reviewer-model-provenance.json')
checks['all_reviewers_model_confirmed']=all(v.get('actual_model')=='gpt-6.1-sol' and v.get('actual_effort')=='high' for v in prov.values())
audit_actor={'stamped-iteration-01':'stamped_source_audit','stamped-iteration-02':'stamped_source_audit_02','stamped-iteration-03':'stamped_source_audit_03'}.get(final_name,'source_audit_certified_exact')
for actor in [audit_actor,'coverage_complete_review']:
 checks[actor+'_model_confirmed']=prov.get(actor,{}).get('actual_model')=='gpt-6.1-sol' and prov.get(actor,{}).get('actual_effort')=='high'
ledger=read(P/'coverage-ledger-v6.json');checks['two_final_zero_addition_passes']=all(x['added_count']==0 and x['core_passages_mapped'] for x in ledger['passes'][-2:])
coverage=read(P/'coverage-complete-review.json');checks['fresh_coverage_challenge_pass']=coverage['verdict'].startswith('PASS') and not coverage['findings'] and not coverage['proposed_questions'] and coverage['two_zero_pass_working_saturation_check']['stands']
checks['coverage_ledger_additions_match_key']=ledger['accepted_additions']==read(P/'bank-v6/answer-key.json')['answers'][20:]
checks['immutable_evidence_hashes_match']=all(h(P/f)==digest for f,digest in read(P/'evidence-hashes.json').items())
prior_inventory=read(P/'evidence-hashes.pre-prompt-record.json');current_inventory=read(P/'evidence-hashes.json');checks['original100_evidence_fingerprints_preserved']=len(prior_inventory)==100 and all(current_inventory.get(f)==digest for f,digest in prior_inventory.items())
prompts=read(final/'reader-prompt-record.json')
def prompt_valid(r):
 settings=r.get('dispatch_runtime_evidence',r)
 return h(final/r['prompt_path'])==r['prompt_sha256'] and settings['requested_model']=='gpt-6-luna' and settings['reasoning_effort']=='high' and settings['fork_turns']=='none'
checks['final_prompt_record_integrity']=set(prompts['readers'])=={'a','b'} and all(prompt_valid(r) for r in prompts['readers'].values())
status=read(P/'game-status.json')
integration=None
if status['status']=='complete':
 integration=read(P/'coordinator-final-validation.json')
 checks['coordinator_integration_complete']=integration['assigned_game_integration_pass'] and all(integration['checks'].values()) and integration['summary_sha256']==h('rules/orl-ans.md') and all(h(x['path'])==x['sha256'] for x in integration['coordinator_evidence']) and not status['coordinator_pending']
checks['handoff_status_matches_final']=status['status'] in ['ready-for-coordinator','complete'] and status['final_snapshot_path']==str((final/'summary-snapshot.md').resolve()) and status['question_count']==len(read(final/'questions.json')['questions']) and status['final_reader_scores']=={who:read(final/'results.json')['readers'][who]['counts'] for who in ['a','b']}
checks['all_saved_json_parse']=all(isinstance(read(x),(dict,list)) for x in P.rglob('*.json'))
if (P/'README.md').exists():
 targets=re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',(P/'README.md').read_text());links=[x.split('#')[0] for x in targets if not re.match(r'https?://',x)];checks['report_local_links_resolve']=all((P/x).exists() for x in links if x)
commands=[['.venv/bin/python','-m','scripts.validate','rules/orl-ans.md'],['git','diff','--check','--','rules/orl-ans.md',str(P)]];repo=[]
for cmd in commands:
 r=subprocess.run(cmd,text=True,capture_output=True);repo.append({'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
checks['targeted_repository_checks']=all(x['exit_code']==0 for x in repo)
out={'checks':checks,'iterations':details,'targeted_repository_checks':repo,'final_summary_sha256':h('rules/orl-ans.md'),'global_stamping_registry_index_manifest_catalog':{'coordinator_responsibility':True,'worker_read_only_integration_review':str((P/'coordinator-final-validation.json').resolve()) if integration else None,'observed_global_catalog_errors':integration['current_global_catalog_errors'] if integration else None,'completion_scope':'Assigned Orléans only'},'all_local_checks_pass':all(checks.values())}
(P/'validation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'all_local_checks_pass':out['all_local_checks_pass'],'failed_checks':[k for k,v in checks.items() if not v],'iteration_scores':{n:d['scores'] for n,d in details.items()}},indent=2))
