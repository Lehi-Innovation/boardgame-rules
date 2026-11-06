"""Read-only checks over this run; writes one requested validation artifact."""
from pathlib import Path
import collections,hashlib,json,re,sys
R=Path(__file__).resolve().parent
REPO=R.parents[4]
CANON=REPO/'rules/john-company-second-edition.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text())
def exact_ids(items,ids): return collections.Counter(x['id'] for x in items)==collections.Counter(ids)
checks={'banks':{},'iterations':{},'source_audits':{},'historical_hashes':{},'failures':[],'notes':[]}
checks['source_hashes']={name:sha(REPO/name)==expected for name,expected in read(R/'input-manifest.json')['source_hashes'].items()}
if not all(checks['source_hashes'].values()):checks['failures'].append('original assigned source hash changed')
for b in sorted(R.iterdir()):
 if not b.is_dir() or not (b/'answer-key.json').exists(): continue
 qs=read(b/'questions.json')['questions'];ks=read(b/'answer-key.json')['answers'];ids=[x['id'] for x in qs]
 m=read(b/'input-manifest.json');hashes=m.get('hashes',{})
 c={'count':len(ids),'unique_ids':len(ids)==len(set(ids)),'key_ids':exact_ids(ks,ids),'original_hashes':{f:sha(b/f)==h for f,h in hashes.items()}}
 checks['banks'][b.name]=c
 if not c['unique_ids'] or not c['key_ids'] or not all(c['original_hashes'].values()): checks['failures'].append(b.name+' bank integrity')
 for p in sorted(set(b.glob('luna-iteration-*')) | set(b.glob('luna-final-stamped-iteration-*'))):
  name=str(p.relative_to(R));z={'question_copy':(p/'questions.json').read_bytes()==(b/'questions.json').read_bytes(),'canonical_matches':sha(CANON)==sha(p/'summary-snapshot.md'),'readers':{}}
  m=read(p/'input-manifest.json');hs=m.get('inputs',m.get('hashes',{}));z['frozen_hashes']={f:sha(Path(f) if Path(f).is_absolute() else (REPO/f if (REPO/f).exists() else p/f))==h for f,h in hs.items() if f!=str(CANON)}
  for role in 'ab':
   rawpath=p/f'reader-{role}.json'
   if rawpath.exists():
    raw=read(rawpath)['answers'];rc={'count':len(raw),'exact_ids':exact_ids(raw,ids),'evidence_fields_present':all(x.get('evidence') for x in raw)};z['readers'][role]=rc
    if not rc['exact_ids']:checks['failures'].append(name+' reader '+role+' IDs')
  rp=p/'results.json'
  if rp.exists():
   d=read(rp);z['grades']={}
   for role in 'ab':
    rv=d['readers']['reader-'+role];gs=rv['grades'];raw={x['id']:x for x in read(p/f'reader-{role}.json')['answers']};qmap={x['id']:x for x in qs};active_keys=read(Path(d['answer_key_source']))['answers'] if d.get('answer_key_source') else ks;kmap={x['id']:x for x in active_keys}
    c={'exact_ids':exact_ids(gs,ids),'counts_match':all(rv['counts'].get(k,0)==sum(x['grade']==k for x in gs) for k in ['Correct','Partial','Incorrect']),'question_matches':all(x.get('question')==qmap[x['id']]['question'] for x in gs),'expected_matches':all(x.get('expected_answer')==kmap[x['id']]['expected_answer'] for x in gs),'observed_matches':all(x.get('observed_answer')==raw[x['id']]['answer'] for x in gs)}
    z['grades'][role]=c
    if not all(c.values()):checks['failures'].append(name+' grades '+role)
  if not z['question_copy'] or not all(z['frozen_hashes'].values()):checks['failures'].append(name+' frozen inputs')
  checks['iterations'][name]=z
for p in sorted(R.glob('source-audit-*/source-audit.json')):
 d=read(p);m=read(p.parent/('input-manifest.json' if (p.parent/'input-manifest.json').exists() else 'manifest.json'));snap=p.parent/'summary-snapshot.md'
 if not snap.exists():
  snap=Path(d.get('candidate_snapshot',d.get('snapshot_path',p.parent/'candidate-snapshot.md')))
  if not snap.is_absolute():snap=p.parent/snap
 checks['source_audits'][p.parent.name]={'summary_hash_intact':sha(snap)==d.get('candidate_sha256',d.get('summary_sha256',d.get('snapshot_sha256',m.get('candidate_sha256',m.get('summary_sha256',m.get('snapshot_sha256',sha(snap))))))),'canonical_matches':sha(CANON)==sha(snap),'verdict':d.get('machine_verdicts',{}).get('overall_scoped_result',d.get('overall_verdict',d.get('verdict'))),'scoped_signoff':d.get('machine_verdicts',{}).get('scoped_signoff',d.get('scoped_signoff')),'complete_core_signoff':d.get('complete_core_signoff')}
for f,h in read(R/'historical-input-hashes.json').items(): checks['historical_hashes'][f]=sha(R/f)==h
if not all(checks['historical_hashes'].values()):checks['failures'].append('historical original file changed')
checks['report_links']={}
for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',(R/'README.md').read_text()):
 if '://' not in target: checks['report_links'][target]=(R/target.split('#')[0]).exists()
if not all(checks['report_links'].values()):checks['failures'].append('report links')
checks['notes']=['Historical snapshots intentionally differ from canonical; only latest exact-text snapshot is eligible for current assertions.','Original seed-v1 A has preserved schema/evidence defects; no raw output repaired.','The user-approved >= interpretation resolves the normative defense scope; artifact integrity does not establish current reader or source PASS.']
checks['canonical_sha256']=sha(CANON)
out=R/(sys.argv[1] if len(sys.argv)>1 else 'run-integrity-current.json');out.write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps({'output':str(out),'failures':checks['failures'],'banks':len(checks['banks']),'iterations':len(checks['iterations']),'historical_original_hashes_intact':all(checks['historical_hashes'].values())},indent=2))
