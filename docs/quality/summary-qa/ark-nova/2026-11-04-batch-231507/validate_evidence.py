from pathlib import Path
import json,hashlib,sys
D=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
initial=json.loads((D/'input-manifest.json').read_text())
checks={'original_summary_preserved':h(D/'original-summary.md')==initial['hashes'][str(Path('rules/ark-nova.md').resolve())],'original_sources_unchanged':{p:h(p)==v for p,v in initial['hashes'].items() if p!=str(Path('rules/ark-nova.md').resolve())},'source_supplements_unchanged':{s['path']:h(s['path'])==s['sha256'] for s in json.loads((D/'neutral-source-manifest.json').read_text())['sources']},'benchmarks':{},'iterations':{}}
v1q=json.loads((D/'benchmark-v1/questions.json').read_text())['questions'];v1k=json.loads((D/'benchmark-v1/answer-key.json').read_text())['answers'];v11q=json.loads((D/'benchmark-v1.1/questions.json').read_text())['questions'];v11k=json.loads((D/'benchmark-v1.1/answer-key.json').read_text())['answers']
checks['SC01']={'questions_all20_identical':v1q==v11q,'other19_key_entries_identical':all(a==b for a,b in zip(v1k,v11k) if a['id']!='Q17'),'only_changed_key_id':[a['id'] for a,b in zip(v1k,v11k) if a!=b],'correction_record_exists':(D/'source-key-correction-SC01.json').exists()}
v12q=json.loads((D/'benchmark-v1.2/questions.json').read_text())['questions'];v12k=json.loads((D/'benchmark-v1.2/answer-key.json').read_text())['answers']
checks['SC02']={'questions_all20_identical':v1q==v12q,'other19_key_entries_identical':all(a==b for a,b in zip(v11k,v12k) if a['id']!='Q17'),'only_changed_key_id':[a['id'] for a,b in zip(v11k,v12k) if a!=b],'clarification_record_exists':(D/'source-key-clarification-SC02.json').exists()}
expanded_corrections={name:json.loads((D/name).read_text()) for name in ['source-key-correction-SC03.json','source-key-precision-SC04.json']}
checks['expanded_key_correction_history']={name:{'old_sealed_key_preserved':h(D/'coverage-revision-03/answer-key.json')==record['old_key_sha256'],'original20_unchanged':record['baseline_original20_unchanged']} for name,record in expanded_corrections.items()}
for b in sorted(D.glob('benchmark-*')):
 if not (b/'questions.json').exists():continue
 q=json.loads((b/'questions.json').read_text())['questions'];k=json.loads((b/'answer-key.json').read_text())['answers'];ids=[x['id'] for x in q];kids=[x['id'] for x in k]
 baseline=v11k if b.name=='benchmark-v1.1' else v12k
 checks['benchmarks'][b.name]={'count':len(q),'unique_question_ids':len(ids)==len(set(ids)),'question_and_key_ids_match':set(ids)==set(kids),'unique_key_ids':len(kids)==len(set(kids)),'question_sha256':h(b/'questions.json'),'key_sha256':h(b/'answer-key.json'),'original20_question_objects_preserved':q[:20]==v1q,'corrected20_key_objects_preserved':k[:20]==baseline if b.name!='benchmark-v1' else None}
 freeze_manifest=b/'benchmark-freeze-manifest.json'
 if freeze_manifest.exists():
  frozen=json.loads(freeze_manifest.read_text());checks['benchmarks'][b.name]['frozen_artifacts_match']={n:h(b/n)==v for n,v in frozen['files_sha256'].items()}
 if len(q)>20:
  byid={x['id']:x for x in k}
  checks['benchmarks'][b.name]['expanded_source_key_corrections_exact']={name:byid.get(record['affected_id'])==record['corrected_entry'] for name,record in expanded_corrections.items()}
for t in sorted([*D.glob('seed-iteration-*'),*D.glob('expanded-iteration-*'),*D.glob('integrated-iteration-*')]):
 if not (t/'input-manifest.json').exists():continue
 m=json.loads((t/'input-manifest.json').read_text());b=D/m['benchmark'];q=json.loads((t/'questions.json').read_text())['questions'];k=json.loads((b/'answer-key.json').read_text())['answers'];key={a['id']:a for a in k};ids={x['id'] for x in q}
 delivered=Path(m['reader_question_payload']['path']) if 'reader_question_payload' in m else b/'questions.json'
 r={'benchmark':m['benchmark'],'frozen_hashes_match':{p:h(p)==v for p,v in m['hashes'].items()},'question_copy_exact':(t/'questions.json').read_bytes()==delivered.read_bytes(),'question_objects_match_accepted_bank':q==json.loads((b/'questions.json').read_text())['questions'],'summary_sha256':h(t/'summary-snapshot.md'),'reader_checks':{}}
 if 'reader_question_payload' in m:
  delivery=m['reader_question_payload'];r['sanitized_delivery_hashes_preserved']=h(delivery['path'])==delivery['sha256'] and h(delivery['accepted_bank_path'])==delivery['accepted_bank_sha256']
 if 'authoritative_sources' in m:
  r['authoritative_sources_match']={p:h(p)==v for p,v in m['authoritative_sources'].items()}
 result=json.loads((t/'results.json').read_text()) if (t/'results.json').exists() else None
 for side in 'ab':
  f=t/f'reader-{side}.json'
  if not f.exists():continue
  raw=json.loads(f.read_text());a=raw['answers'];aids=[x['id'] for x in a];byid={x['id']:x for x in a};one={'count':len(a),'each_expected_id_once':len(aids)==len(ids)==len(set(aids)) and set(aids)==ids,'raw_sha256':h(f)}
  if result:
   grades=result['readers'][side]['grades'];gids=[x['id'] for x in grades];counts={g:sum(x['grade']==g for x in grades) for g in ['correct','partial','incorrect']}
   one.update(grade_each_expected_id_once=len(gids)==len(ids)==len(set(gids)) and set(gids)==ids,grades_link_to_raw_and_fixed_key=all(g['observed']==byid[g['id']] and g['expected']==key[g['id']] and g['question']==next(x['question'] for x in q if x['id']==g['id']) for g in grades),counts_match=counts==result['readers'][side]['counts'],counts=counts)
  prov=t/f'reader-{side}-model-provenance.json'
  if prov.exists():
   p=json.loads(prov.read_text());turns=(p.get('runtime') or {}).get('turn_contexts',[]);one['model_and_effort_confirmed']=bool(turns) and all(x['model']=='gpt-6-luna' and x['effort']=='high' for x in turns);one['fresh_fork_none_requested']=p['fork_turns']=='none';one['actual_dispatch_plaintext_available']=p.get('actual_dispatch_plaintext_available',False);one['intended_prompt_saved']=(t/f'reader-{side}-prompt.txt').exists();one['host_message_body_storage']=p.get('host_message_body_storage','legacy_label_not_verified')
  r['reader_checks'][side]=one
 checks['iterations'][t.name]=r
if len(sys.argv)>1:
 t=D/sys.argv[1];checks['final_candidate']={'iteration':t.name,'snapshot_matches_canonical':(t/'summary-snapshot.md').read_bytes()==Path('rules/ark-nova.md').read_bytes(),'canonical_sha256':h('rules/ark-nova.md'),'complete_input_access_verified':json.loads((t/'input-access-validation.json').read_text()).get('verdict')=='COMPLETE_AUTHORIZED_INPUTS_CONFIRMED' if (t/'input-access-validation.json').exists() else False}
 boundary=t/'reader-boundary-validation.json'
 checks['final_candidate']['clean_reader_delivery_verified']=boundary.exists() and json.loads(boundary.read_text()).get('verdict')=='CLEAN_READER_ONLY_DELIVERY_CONFIRMED'
 results=t/'results.json'
 if results.exists():
  result=json.loads(results.read_text());n=len(json.loads((t/'questions.json').read_text())['questions'])
  checks['final_candidate']['both_readers_all_N_correct']=all(result['readers'][side]['counts']=={'correct':n,'partial':0,'incorrect':0} and not any(g.get('unsupported_guess') for g in result['readers'][side]['grades']) for side in 'ab')
 else:checks['final_candidate']['both_readers_all_N_correct']=False
(D/'validation.json').write_text(json.dumps(checks,indent=2))
print(json.dumps({'original_summary_preserved':checks['original_summary_preserved'],'sources_unchanged':all(checks['original_sources_unchanged'].values()),'supplements_unchanged':all(checks['source_supplements_unchanged'].values()),'SC01':checks['SC01'],'iteration_count':len(checks['iterations']),'final_candidate':checks.get('final_candidate')},indent=2))
