from qa_tools import *
from collections import Counter
import re

def entries_sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def run():
 out={'scope':'Assigned Obsession evidence only; no global stamping/regeneration.','source_integrity':[],'benchmarks':{},'iterations':{},'errors':[]}
 initial=json.loads((P/'input-manifest.json').read_text())
 for x in initial['inputs']:
  f=Path(x['path']);base=P/'baseline'/f.name
  r={'original_path':str(f),'baseline_hash_matches':sha(base)==x['sha256'],'current_hash_matches':sha(f)==x['sha256']}
  if f.name!='obsession.md' and not r['current_hash_matches']:out['errors'].append(f'Unexpected assigned source change: {f}')
  if not r['baseline_hash_matches']:out['errors'].append(f'Baseline changed: {base}')
  out['source_integrity'].append(r)
 seedq=json.loads((P/'seed-v1/questions.json').read_text())['questions'];seedk=json.loads((P/'seed-v1/answer-key.json').read_text())['answers'];seed2k=json.loads((P/'seed-v2/answer-key.json').read_text())['answers']
 for b in ['seed-v1','seed-v2','expanded-v1','expanded-v2','expanded-v3','expanded-v4']:
  bp=P/b;q=json.loads((bp/'questions.json').read_text())['questions'];k=json.loads((bp/'answer-key.json').read_text())['answers'];ids=[a['id'] for a in q];kid=[a['id'] for a in k]
  r={'question_count':len(ids),'question_ids_unique':len(ids)==len(set(ids)),'key_ids_match_order':ids==kid,'original_twenty_question_entries_intact':q[:20]==seedq,'original_question_entries_sha256':entries_sha(q[:20]),'seed_v1_question_entries_sha256':entries_sha(seedq),'original_keys_intact_except_explicit_Q09_correction':all(a==b for i,(a,b) in enumerate(zip(k[:20],seedk)) if i!=8),'Q09_key_version':'original' if k[8]==seedk[8] else 'explicit-seed-v2-correction' if k[8]==seed2k[8] else 'UNEXPECTED','questions_sha256':sha(bp/'questions.json'),'key_sha256':sha(bp/'answer-key.json')}
  if not all(r[x] for x in ['question_ids_unique','key_ids_match_order','original_twenty_question_entries_intact','original_keys_intact_except_explicit_Q09_correction']):out['errors'].append(f'Benchmark preservation error {b}')
  out['benchmarks'][b]=r
 for I in sorted(P.glob('*iteration-*')):
  if not I.is_dir():continue
  m=json.loads((I/'input-manifest.json').read_text());q=json.loads((I/'questions.json').read_text())['questions'];ids=[x['id'] for x in q];r={'manifest_all_hashes_match':all(sha(x['path'])==x['sha256'] for x in m['inputs']),'summary_sha256':sha(I/'summary-snapshot.md'),'canonical_summary_identical_now':(I/'summary-snapshot.md').read_bytes()==(ROOT/'rules/obsession.md').read_bytes(),'readers':{}}
  if (I/'results.json').exists():res=json.loads((I/'results.json').read_text())
  else:res=None
  key_path=next(Path(x['path']) for x in m['inputs'] if Path(x['path']).name=='answer-key.json'); frozen_key=json.loads(key_path.read_text())['answers']
  for w in ['a','b']:
   f=I/f'reader-{w}.json'
   if not f.exists():continue
   raw=json.loads(f.read_text());ans=raw['answers'];aid=[x['id'] for x in ans];rr={'all_ids_once':Counter(aid)==Counter(ids),'exactly_two_declared_input_files':len(raw.get('inputs_read',[]))==2,'output_sha256':sha(f)}
   if res:
    g=res['readers'][w]['grades'];rr.update({'grade_ids_once':Counter(x['id'] for x in g)==Counter(ids),'raw_answers_match_grades':all(x['actual_answer']==next(a for a in ans if a['id']==x['id'])['answer'] for x in g),'original_questions_match_grades':all(x['question']==next(a for a in q if a['id']==x['id'])['question'] for x in g),'expected_key_matches_grades':all(x['expected_answer']==next(a for a in frozen_key if a['id']==x['id'])['expected_answer'] and x['source_refs']==next(a for a in frozen_key if a['id']==x['id'])['source_refs'] for x in g),'counts':dict(Counter(x['grade'] for x in g))})
   if res and any(not rr[x] for x in ['grade_ids_once','raw_answers_match_grades','original_questions_match_grades','expected_key_matches_grades']):out['errors'].append(f'Grade correspondence error {I.name}/{w}')
   if not rr['all_ids_once']:out['errors'].append(f'Answer ID error {I.name}/{w}')
   r['readers'][w]=rr
  if not r['manifest_all_hashes_match']:out['errors'].append(f'Frozen input integrity error {I.name}')
  out['iterations'][I.name]=r
 prov=provenance();out['models']=[{'task':x['task'],'session_id':x['session_id'],'contexts':x['contexts'],'all_high':all(c['effort']=='high' for c in x['contexts']),'actual_models':sorted(set(c['model'] for c in x['contexts']))} for x in prov]
 for I in P.glob('*iteration-*'):
  if not I.is_dir():continue
  for w in ['a','b']:
   task=f'/root/obs_{"seed" if I.name.startswith("seed") else "expanded"}_{I.name.split("-")[-1]}_{w}'
   match=next((x for x in prov if x['task']==task),None)
   if match:
    dump(I/f'reader-{w}-runtime-environment-user-messages.json',match['visible_environment_user_messages']);dump(I/f'reader-{w}-runtime-provenance.json',{a:b for a,b in match.items() if a!='visible_environment_user_messages'})
    if not match['contexts'] or any(c['model']!='gpt-6-luna' or c['effort']!='high' for c in match['contexts']):out['errors'].append(f'Reader model mismatch {task}')
 out['expanded_question_prefix_preserved']=json.loads((P/'expanded-v2/questions.json').read_text())['questions'][:56]==json.loads((P/'expanded-v1/questions.json').read_text())['questions']
 if not out['expanded_question_prefix_preserved']:out['errors'].append('Expanded question prefix changed')
 out['expanded_v3_question_wording_identical_to_v2']=json.loads((P/'expanded-v3/questions.json').read_text())['questions']==json.loads((P/'expanded-v2/questions.json').read_text())['questions']
 v2k=json.loads((P/'expanded-v2/answer-key.json').read_text())['answers'];v3k=json.loads((P/'expanded-v3/answer-key.json').read_text())['answers'];out['expanded_v3_keys_identical_except_explicit_Q22_correction']=all(x==y for i,(x,y) in enumerate(zip(v2k,v3k)) if i!=21)
 if not out['expanded_v3_question_wording_identical_to_v2'] or not out['expanded_v3_keys_identical_except_explicit_Q22_correction']:out['errors'].append('Unexpected v3 question/key change')
 v4q=json.loads((P/'expanded-v4/questions.json').read_text())['questions'];v4k=json.loads((P/'expanded-v4/answer-key.json').read_text())['answers'];out['expanded_v4_previous60_questions_and_keys_identical_to_v3']=v4q[:60]==json.loads((P/'expanded-v3/questions.json').read_text())['questions'] and v4k[:60]==v3k
 if not out['expanded_v4_previous60_questions_and_keys_identical_to_v3']:out['errors'].append('Unexpected v4 prefix change')
 dump(P/'validation.json',out);return out
if __name__=='__main__':
 o=run();print(json.dumps({'errors':o['errors'],'benchmarks':{k:v['question_count'] for k,v in o['benchmarks'].items()},'iterations':{k:{w:r['counts'] for w,r in v['readers'].items() if 'counts' in r} for k,v in o['iterations'].items()}}))
