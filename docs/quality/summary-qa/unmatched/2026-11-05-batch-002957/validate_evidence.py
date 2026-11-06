from pathlib import Path
import json,hashlib,collections,subprocess
P=Path(__file__).resolve().parent;R=P.parents[4]
def read(x):return json.loads(x.read_text())
def digest(x):return hashlib.sha256(x.read_bytes()).hexdigest()
checks={'benchmarks':{},'iterations':{},'source_integrity':{},'canonical_candidate':{}}
base=read(P/'benchmark-v1/questions.json')['questions']
for B in sorted(P.glob('benchmark-v*')):
 q=read(B/'questions.json')['questions'];k=read(B/'answer-key.json')['answers'];ids=[x['id'] for x in q]
 assert ids==[x['id'] for x in k] and len(set(ids))==len(ids)
 assert q[:20]==base
 m=read(B/'input-manifest.json');hashes=m['hashes'];assert all(digest(B/n)==v for n,v in hashes.items())
 checks['benchmarks'][B.name]={'count':len(q),'ids_once':True,'initial_question_entries_unchanged':True,'frozen_hashes_unchanged':True}
 if (B/'scope-map.json').exists():
  s=read(B/'scope-map.json')['questions'];assert [x['id'] for x in s]==ids
  assert all(x['asked_clauses']==y['question'] for x,y in zip(s,q));checks['benchmarks'][B.name]['scope_map_ids_once_and_question_match']=True
for I in sorted(list(P.glob('seed-iteration-*'))+list(P.glob('expanded-iteration-*'))):
 ids=[x['id'] for x in read(I/'questions.json')['questions']];entry={'attempt_classification':('aborted_dispatched_pair' if (I/'superseded-status.json').exists() else 'completed_scored_pair' if (I/'results.json').exists() else 'pending_full_pair')}
 bank='benchmark-v1' if I.name.startswith('seed-') else read(I/'input-manifest.json')['benchmark']
 assert (I/'questions.json').read_bytes()==(P/bank/'questions.json').read_bytes()
 if I.name.startswith('expanded-'):
  manifest=read(I/'input-manifest.json')
  for label in ['hashes','prompt_hashes','authoritative_source_hashes']:
   assert all(digest(Path(path))==value for path,value in manifest[label].items()),(I.name,label)
  entry['all_frozen_input_prompt_source_bindings_unchanged']=True
 for who in ['a','b']:
  f=I/f'reader-{who}.json'
  if f.exists():
   raw=read(f)
   if (I/'superseded-status.json').exists():
    assert [x['id'] for x in raw['answers']]==ids[:len(raw['answers'])]
    entry['superseded_not_completed_benchmark']=True
   else:assert [x['id'] for x in raw['answers']]==ids
   entry[who]={'raw_sha256':digest(f),'ids_once':True,'answer_count':len(raw['answers'])}
 if (I/'results.json').exists():
  d=read(I/'results.json')
  for who,rv in d['readers'].items():
   grades=rv['grades'];assert [g['id'] for g in grades]==ids
   counts=collections.Counter(g['grade'].lower() for g in grades)
   for label in ['correct','partial','incorrect']:assert rv['scores'][label]==counts[label]
   raw=read(I/f'reader-{who}.json')['answers']
   for g,a in zip(grades,raw):
    if 'observed' in g:assert g['observed']==a
   entry[who]['scores']=rv['scores'];entry[who]['grade_ids_once']=True
 checks['iterations'][I.name]=entry
for name in ['input-manifest.json','supplemental-source-manifest.json','arthur-source-manifest.json']:
 m=read(P/name);h=m.get('sources',m.get('paths',m.get('hashes',{})));assert all(digest(Path(n))==v for n,v in h.items());checks['source_integrity'][name]={'file_count':len(h),'unchanged':True}
m=read(P/'current-official-source-manifest.json');h={**m['normative_hashes'],**m['provenance_and_independent_checks']};assert all(digest(Path(n))==v for n,v in h.items());checks['source_integrity']['current-official-source-manifest.json']={'file_count':len(h),'unchanged':True}
canonical=R/'rules/unmatched.md';progress=read(P/'progress.json');audit_path=Path(progress['source_audit']['current_exact_text']['path']);candidate=audit_path.parent/'summary-snapshot.md';assert canonical.read_bytes()==candidate.read_bytes();audit=read(audit_path);assert audit['verdict']=='PASS' and not audit['findings'] and audit['summary_sha256']==digest(canonical)
current=sorted(P.glob('expanded-iteration-*'))[-1];result=read(current/'results.json') if (current/'results.json').exists() else None
blind_pass=bool(result and result['both_full_bank_pass'])
if blind_pass:
 assert canonical.read_bytes()==(current/'summary-snapshot.md').read_bytes()
 for r in ['a','b']:
  assert result['readers'][r]['raw_file_sha256']==digest(current/f'reader-{r}.json')
 assert (current/'grading/actual-input-delivery-validation.json').exists()
 assert (current/'whole-entry-source-integrity-validation.json').exists()
checks['canonical_candidate']={'byte_equal_to_audited_current_snapshot':True,'sha256':digest(canonical),'current_rule_scope_approved':True,'current_source_audit':'PASS','final_bank_blind_pass':blind_pass}
check=subprocess.run([str(R/'.venv/bin/python'),'-m','scripts.validate',str(canonical)],cwd=R,capture_output=True,text=True);assert check.returncode==0
checks['targeted_repository_validation']={'exit_code':check.returncode,'output':check.stdout}
check=subprocess.run(['git','diff','--check','--','rules/unmatched.md',str(P.relative_to(R))],cwd=R,capture_output=True,text=True);assert check.returncode==0
checks['targeted_git_diff_check']={'exit_code':check.returncode,'output':check.stdout+check.stderr}
checks['scope_dependency']='Resolved by official IELLO primary source, trusted coordinator direction and subsequent explicit human confirmation; no historical cutoff/current user choice is pending.'
(P/'validation-in-progress.json').write_text(json.dumps(checks,indent=2)+'\n')
classification_counts=collections.Counter(x['attempt_classification'] for x in checks['iterations'].values())
print('Validated',len(checks['benchmarks']),'frozen banks; attempt classifications:',dict(classification_counts),'; all original questions/source hashes intact; final blind pass:',blind_pass)
