from pathlib import Path
import json,hashlib,sys,collections,subprocess
P=Path(__file__).resolve().parent;R=Path('/home/jonny/projects/boardgame-rules');report={'stage':'final-candidate-validation' if len(sys.argv)>2 else 'historical-evidence-integrity-only'};fail=[]
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(name,value):report[name]=value;fail.extend([name] if not value else [])
seedq=json.loads((P/'v1-seed/questions.json').read_text())['questions'];seedk=json.loads((P/'v1-seed/answer-key.json').read_text())['answers']
initial=json.loads((P/'input-manifest.json').read_text())['initial_hashes']
check('sources_unchanged',all(h(Path(p))==v for p,v in initial.items() if not p.startswith('rules/')))
if (P/'harvest-source-provenance.json').exists():
 hp=json.loads((P/'harvest-source-provenance.json').read_text());check('additional_publisher_source_unchanged',h(Path(hp['local_asset']))==hp['sha256'])
report['benchmarks']={}
for d in sorted(P.glob('v*-*')):
 if not d.is_dir():continue
 q=json.loads((d/'questions.json').read_text())['questions'];k=json.loads((d/'answer-key.json').read_text())['answers'];m=json.loads((d/'input-manifest.json').read_text())['sha256']
 data={'frozen_hashes_match':all(h(d/n)==v for n,v in m.items()),'unique_ids':len({x['id'] for x in q})==len(q)==len(k),'original_questions_preserved':q[:20]==seedq,'original_expected_answers_preserved':all(a['expected_answer']==b['expected_answer'] for a,b in zip(k[:20],seedk))}
 report['benchmarks'][d.name]=data
 for n,v in data.items():check(d.name+'/'+n,v)
prov=json.loads((P/'model-provenance.json').read_text());pm={x['task'].split('/')[-1]:x for x in prov}
report['iterations']={}
for d in sorted(P.glob('*iteration-*')):
 if not d.is_dir():continue
 if not (d/'results.json').exists():continue
 q=json.loads((d/'questions.json').read_text())['questions'];ids=[x['id'] for x in q];res=json.loads((d/'results.json').read_text());bank=res['bank'];key=json.loads((P/bank/'answer-key.json').read_text())['answers'];manifest=json.loads((d/'input-manifest.json').read_text())['hashes']
 read_audit=json.loads((d/'input-read-audit.json').read_text()) if (d/'input-read-audit.json').exists() else None
 checks={'questions_unchanged_from_bank':(d/'questions.json').read_bytes()==(P/bank/'questions.json').read_bytes(),'manifest_immutable_inputs':all(h(Path(p))==v for p,v in manifest.items())}
 for reader in 'ab':
  rawdoc=json.loads((d/f'reader-{reader}.json').read_text());raw=rawdoc['answers'];checks[f'{reader}_declared_only_two_inputs']=len(rawdoc['inputs_read'])==2 and {Path(x).name for x in rawdoc['inputs_read']}=={'summary-snapshot.md','questions.json'} and all(x in ['summary-snapshot.md','questions.json'] or ((Path(x) if Path(x).is_absolute() else R/Path(x)).resolve() in {(d/'summary-snapshot.md').resolve(),(d/'questions.json').resolve()}) for x in rawdoc['inputs_read']);grades=res['readers'][reader]['grades'];ri=[x['id'] for x in raw];gi=[x['id'] for x in grades]
  checks[f'{reader}_complete_visible_inputs']=bool(read_audit) and not read_audit['readers'][reader]['unresolved_missing_input']
  checks[f'{reader}_unique_complete_ids']=collections.Counter(ri)==collections.Counter(ids)==collections.Counter(gi)
  checks[f'{reader}_grade_matches_original_inputs']=all(g['question']==a['question'] and g['expected_answer']==b['expected_answer'] and g['observed_answer']==c['answer'] and g['summary_evidence']==c['evidence'] for g,a,b,c in zip(grades,q,key,raw))
  task=d.name.replace('seed-iteration-','seed_').replace('expanded-iteration-','expanded_')+'_'+reader
  checks[f'{reader}_runtime_model_confirmed']=task in pm and bool(pm[task]['contexts']) and all(x['model']=='gpt-6-luna' and x['effort']=='high' for x in pm[task]['contexts'])
  checks[f'{reader}_fork_none_confirmed']=task in pm and pm[task].get('actual_spawn_configuration',{}).get('fork_turns')=='none'
  if task in pm:(d/f'reader-{reader}-runtime-user-messages.json').write_text(json.dumps(pm[task]['runtime_user_message_items'],indent=2,ensure_ascii=False)+'\n')
 report['iterations'][d.name]={'checks':checks,'scores':{r:res['readers'][r]['totals'] for r in 'ab'}}
 for n,v in checks.items():check(d.name+'/'+n,v)
# Final checks only when requested.
if len(sys.argv)>1:
 d=P/sys.argv[1];res=json.loads((d/'results.json').read_text());N=len(json.loads((d/'questions.json').read_text())['questions'])
 check('final_snapshot_byte_identical',h(d/'summary-snapshot.md')==h(R/'rules/dune-imperium.md'))
 check('final_readers_all_correct_no_guesses',all(len(x['grades'])==N and all(g['grade']=='correct' and not g['unsupported_guess'] for g in x['grades']) for x in res['readers'].values()))
 report['final_summary_sha256']=h(d/'summary-snapshot.md')
 report['final_snapshot']=str(d/'summary-snapshot.md')
 if len(sys.argv)>2:
  ad=P/sys.argv[2];audit=json.loads((ad/'source-audit.json').read_text());am=json.loads((ad/'input-manifest.json').read_text())
  check('final_source_audit_PASS_no_findings',audit.get('verdict')=='PASS' and not audit.get('findings'))
  check('final_audit_inputs_immutable',all(h(Path(path))==v for path,v in am.items()))
  check('final_audit_same_summary_bytes',h(ad/'summary-snapshot.md')==h(d/'summary-snapshot.md'))
  ar=json.loads((ad/'input-read-audit.json').read_text())
  check('final_audit_complete_actual_text_reads',all(x['complete'] for x in ar['text_inputs']) and not ar['any_truncated_read_output'])
  check('final_audit_complete_actual_visual_reads',ar['returned_image_count']>=ar['expected_image_count']==25 and not ar['missing_visual_paths'])
  dispatch=json.loads((ad/'intended-dispatch.json').read_text());at=dispatch['task_name'];ap=pm.get(at,{})
  check('final_auditor_fresh_sol_high_fork_none',bool(ap) and bool(ap.get('contexts')) and ap.get('actual_spawn_configuration',{}).get('fork_turns')=='none' and all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in ap.get('contexts',[])) and all(ap.get('session_id')!=x.get('session_id') for x in prov if x.get('task')!='/root/'+at))
  (ad/'model-provenance.json').write_text(json.dumps(ap,indent=2,ensure_ascii=False)+'\n')
  report['final_source_audit_path']=str(ad/'source-audit.json')

report['repository_checks']={}
for name,cmd in [('targeted_validate',[str(R/'.venv/bin/python'),'-m','scripts.validate','rules/dune-imperium.md']),('diff_check',['git','diff','--check','--','rules/dune-imperium.md',str(P.relative_to(R))])]:
 x=subprocess.run(cmd,cwd=R,text=True,capture_output=True);report['repository_checks'][name]={'exit_code':x.returncode,'stdout':x.stdout,'stderr':x.stderr};check(name,x.returncode==0)
report['failed_checks']=fail;report['status']='PASS' if not fail else 'FAIL';(P/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(report['status'],fail)
