from pathlib import Path
import json,hashlib,datetime,subprocess,re,sys
D=Path(__file__).resolve().parent;P=D.parent;ROOT=P.parents[4];ONE=P/'post-change-20261106-01'
read=lambda p:json.loads(Path(p).read_text())
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
checks={};detail={}
manifest=read(D/'input-manifest.json');sha=h(D/'summary-snapshot.md')
checks['canonical_exact_frozen_bytes']=h(ROOT/'rules/scythe.md')==sha==manifest['summary_sha256']
checks['all_frozen_summary_bank_policy_prompt_hashes_intact']=all(h(name)==fp['sha256'] for name,fp in manifest['inputs'].items())
checks['primary_sources_match_originals']=all(h(ROOT/name)==value for name,value in read(P/'input-manifest.json')['hashes'].items() if name.startswith(('extracted/','source_pdfs/')))
old=read(ONE/'historical-preservation-manifest.json')['sha256'];checks['all_385_prior_evidence_files_preserved']=len(old)==385 and all((P/name).exists() and h(P/name)==value for name,value in old.items())
prior=read(D/'prior-post-change-trial-manifest.json');checks['all_prior_postchange_core_files_preserved']=all(Path(name).exists() and h(name)==value for name,value in prior.items())
for trial in sorted(P.glob('post-change-20261106-*')):
 if trial==D:continue
 if (trial/'results.json').exists():
  rr=read(trial/'results.json');detail[trial.name]={k:v['totals'] for k,v in rr['readers'].items()}
q=read(D/'questions.json')['questions'];key=read(D/'answer-key.json')['answers'];ids=[x['id'] for x in q]
checks['all_63_question_key_ids_exactly_once']=ids==[f'Q{i:02}' for i in range(1,64)] and ids==[x['id'] for x in key]
checks['expanded_v9_question_and_key_bytes_unchanged']=all((D/name).read_bytes()==(P/'expanded-v9'/name).read_bytes() for name in ['questions.json','answer-key.json'])
checks['original_seed_objects_unchanged']=q[:20]==read(P/'questions.json')['questions'] and key[:20]==read(P/'answer-key.json')['answers']
checks['fixed_scope_equivalence_policy_unchanged']=(D/'grading-policy.md').read_bytes()==(ONE/'grading-policy.md').read_bytes()
checks['generic_v4_reader_prompts_unchanged']=all((D/f'reader-{r}-prompt.txt').read_text()==(P/f'integrated-iteration-01/reader-{r}-actual-prompt.txt').read_text().replace(str(P/'integrated-iteration-01'),str(D)) for r in ['a','b'])
provenance=read(D/'model-provenance-final.json');config=read(D/'dispatch-records.json')['agents'];checks['actual_required_models_high_and_original_forknone']=provenance['actual_required_settings_verified'] and set(provenance['agents'])==set(config)
for role,record in provenance['agents'].items():
 request=config[role];sp=provenance['parent_spawn_proof'][role]
 checks['actual_required_models_high_and_original_forknone'] &= len(record['contexts'])==1 and record['contexts'][0]['model']==request['model'] and record['contexts'][0]['effort']=='high' and sp['fork_turns']=='none' and sp['model']==request['model'] and sp['reasoning_effort']=='high'
checks['required_settings_verified_early']=read(D/'model-provenance-early.json')['actual_required_settings_verified'] and read(D/'model-provenance-graders-early-confirmed.json')['actual_required_settings_verified']
results={'benchmark_version':'expanded-v9','grading_method':'Two fresh independent Sol/high/fork-none graders; original raw grader reports retained. Evaluator inspected every current object and every independent judgment under the fixed literal-request/same-local-object scope and equivalence policy.','readers':{}}
for reader in ['a','b']:
 raw=read(D/f'reader-{reader}.json')['answers'];ai={a['id']:a for a in raw};g=read(D/f'grader-{reader}.json');gi={a['id']:a for a in g['grades']}
 checks[f'{reader}_raw_and_grade_ids_exactly_once']=len(raw)==len(ai)==len(g['grades'])==len(gi)==63 and set(ai)==set(gi)==set(ids)
 checks[f'{reader}_grades_link_literal_question_fixed_key_exact_raw']=all(gi[x['id']]['question']==x['question'] and gi[x['id']]['expected_answer']==y['expected_answer'] and gi[x['id']]['source_references']==y['source_references'] and gi[x['id']]['observed_answer']==ai[x['id']]['answer'] and gi[x['id']]['reader_evidence']==ai[x['id']]['evidence'] for x,y in zip(q,key))
 counts={kind:sum(x['grade']==kind for x in g['grades']) for kind in ['correct','partial','incorrect']};checks[f'{reader}_totals_match_all_grades']=counts==g['totals'];checks[f'{reader}_complete_pass_without_unsupported_guesses']=counts=={'correct':63,'partial':0,'incorrect':0} and all(not x['unsupported_guess'] for x in g['grades'])
 checks[f'{reader}_raw_preserved_since_pregrading_freeze']=all(h(name)==fp['sha256'] for name,fp in read(D/f'raw-reader-{reader}-manifest.json')['inputs'].items())
 results['readers'][reader]={'totals':counts,'grades':g['grades'],'independent_grader_report':str(D/f'grader-{reader}.json')}
(D/'results.json').write_text(json.dumps(results,indent=2)+'\n')
audit=read(D/'source-audit.json');checks['fresh_source_audit_PASS_no_material_findings']=audit['verdict']=='PASS' and not audit.get('material_findings',audit.get('findings',[])) and not audit.get('required_repairs',[])
checks['new_source_audit_covers_current_exact_hash']=sha in json.dumps(audit)
checks['source_audit_primary_hashes_match_current']=all(h(ROOT/name) in json.dumps(audit) for name in ['extracted/scythe-rules.txt','source_pdfs/scythe-recovery.pdf'])
coverage=read(P/'coverage-review-08.json');ledger=read(P/'coverage-ledger.json');checks['unchanged_scope_retains_coverage_stopping_evidence']=coverage['verdict']=='PASS' and not coverage['proposed_additions'] and [x['pass'] for x in ledger['passes'][-2:]]==[23,24] and all(not x['accepted'] for x in ledger['passes'][-2:])
watch=read(ONE/'input-watch-state.json');age=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(watch['at_utc'])).total_seconds();checks['live_input_watcher_recent_and_currently_stable']=age<60 and watch['content_stable'];checks['no_unexplained_input_content_changes_observed']=True
events=[json.loads(line) for line in (ONE/'input-watch-events.jsonl').read_text().splitlines()];authorized=[e for e in events if e.get('event')=='authorized-clarity-repair']
for e in events:
 for name,change in e.get('content_changes',{}).items():
  permitted=any(a['path']==name and a['from_sha256']==change['expected']['sha256'] and a['to_sha256']==change['actual'].get('sha256') for a in authorized)
  checks['no_unexplained_input_content_changes_observed'] &= permitted
commands=[]
for cmd in [['.venv/bin/python','-m','scripts.validate','rules/scythe.md'],['git','diff','--check','--','rules/scythe.md',str(P.relative_to(ROOT))]]:
 r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True);commands.append({'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
checks['target_structural_and_scoped_diff_checks_pass']=all(x['exit_code']==0 for x in commands)
links=[]
for md in [P/'README.md',D/'README.md']:
 if not md.exists():continue
 for value in re.findall(r'\]\(([^)]+)\)',md.read_text()):
  if value.startswith(('https:','http:','#')):continue
  target=value.split('#')[0];links.append({'document':str(md),'target':target,'exists':(md.parent/target).exists()})
checks['report_local_links_resolve']=all(x['exists'] for x in links)
output={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'question_count':63,'final_summary_sha256':sha,'all_pass':all(checks.values()),'checks':checks,'current_reader_scores':{r:v['totals'] for r,v in results['readers'].items()},'previous_postchange_scores':detail,'original_prior_reader_pairs':15,'executed_pairs_this_followup':len(list(P.glob('post-change-20261106-*/reader-a.json'))),'watch_state':str(ONE/'input-watch-state.json'),'watch_events':str(ONE/'input-watch-events.jsonl'),'commands':commands,'report_link_checks':links,'coordinator_work_remaining':'Exact-final validation, audit recording, idempotent standard stamping and targeted publication/catalog acceptance. Any stamp byte change requires a fresh exact-text run. No shared changes or chat contacts by this evaluator.'}
(D/'validation.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({'all_pass':output['all_pass'],'checks':checks,'reader_scores':output['current_reader_scores']},indent=2));assert output['all_pass']
