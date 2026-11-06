from pathlib import Path
import json,hashlib,collections,sys
P=Path(__file__).resolve().parent;I=P/sys.argv[1];G=I/'grading'
def read(f):return json.loads(f.read_text())
def digest(f):return hashlib.sha256(f.read_bytes()).hexdigest()
if (I/'results.json').exists() and read(I/'results.json').get('adjudication'):
 raise SystemExit('Refusing to overwrite adjudicated aggregate; original block grades and initial-results snapshot remain separately preserved.')
manifest=read(G/'input-manifest.json');out={'iteration':I.name,'method':'Four fresh independent graders, disjoint fixed question blocks. Every original raw-entry field retained in grader inputs. Same-entry operative quotations count; asked contradictions and unresolved clauses fail. No source/key/scope changes.','summary_sha256':digest(I/'summary-snapshot.md'),'benchmark':read(I/'input-manifest.json')['benchmark'],'readers':{},'grading_blocks':[]}
ids=[x['id'] for x in read(I/'questions.json')['questions']]
for b in manifest['blocks']:
 f=G/f"block-{b['block']:02d}-grades.json";d=read(f);pack=read(Path(b['path']))
 assert digest(Path(b['path']))==b['sha256']
 assert d['block']==b['block']
 out['grading_blocks'].append({'block':b['block'],'path':str(f.resolve()),'sha256':digest(f),'ids':b['ids']})
 for r in ['a','b']:
  grades=d['readers'][r]['grades'];assert [x['id'] for x in grades]==b['ids']
  counts=collections.Counter(x['grade'].lower() for x in grades)
  assert d['readers'][r]['scores']=={k:counts[k] for k in ['correct','partial','incorrect']}
  for grade,row in zip(grades,pack['records']):
   assert [x['fact_index'] for x in grade['facts']]==list(range(len(row['frozen_scope']['required_answer_facts'])))
   assert all(x['assessment'] in ['satisfied','missing','incorrect','unresolved'] for x in grade['facts'])
   assert isinstance(grade['unsupported_correct_guess'],bool)
   if grade['grade']=='correct':assert all(x['assessment']=='satisfied' for x in grade['facts'])
   grade['raw_entry_canonical_sha256']=row['raw_entry_canonical_sha256'][r]
  out['readers'].setdefault(r,{'grades':[]})['grades'].extend(grades)
for r in ['a','b']:
 rv=out['readers'][r];assert [x['id'] for x in rv['grades']]==ids
 c=collections.Counter(x['grade'] for x in rv['grades']);rv['scores']={k:c[k] for k in ['correct','partial','incorrect']}
 rv['required_fact_count']=sum(len(x['facts']) for x in rv['grades'])
 rv['unresolved_asked_facts']=sum(x['assessment']=='unresolved' for g in rv['grades'] for x in g['facts'])
 rv['unsupported_correct_guesses']=[g['id'] for g in rv['grades'] if g['unsupported_correct_guess']]
 rv['raw_file_sha256']=digest(I/f'reader-{r}.json')
 assert rv['raw_file_sha256']==manifest['raw_file_sha256'][r]
out['both_full_bank_semantic_pass']=all(rv['scores']=={'correct':len(ids),'partial':0,'incorrect':0} and not rv['unresolved_asked_facts'] and not rv['unsupported_correct_guesses'] for rv in out['readers'].values())
out['operative_unit_gate']={r:read(I/f'reader-{r}-operative-unit-validation.json')['pass'] for r in ['a','b']}
out['both_full_bank_pass']=out['both_full_bank_semantic_pass']
out['technical_protocol_deviations_do_not_alone_fail_factual_gate']=True
(I/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print({r:{k:v for k,v in rv.items() if k!='grades'} for r,rv in out['readers'].items()});print('Both full-bank pass:',out['both_full_bank_pass'])
