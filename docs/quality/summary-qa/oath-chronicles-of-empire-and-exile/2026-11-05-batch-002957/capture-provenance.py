"""Capture only minimal actual-runtime model/identity fields and opaque record hashes."""
from pathlib import Path
import datetime,json
from provenance_runtime import SESSION_DIR,ROOT_THREAD,load,minimal_record,digest
P=Path(__file__).resolve().parent
CHAIN=P/'provenance-metadata-update-chain.json'
def write(path,value):
 data=(json.dumps(value,indent=2)+'\n').encode();before=digest(path.read_bytes()) if path.exists() else None;after=digest(data)
 if before==after:return
 path.write_bytes(data)
 chain=json.loads(CHAIN.read_text()) if CHAIN.exists() else {'schema':'metadata-update-chain-v1','updates':[]}
 chain['updates'].append({'path':str(path.resolve()),'before_sha256':before,'after_sha256':after,'operation':'refresh_minimal_actual_runtime_projection','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 CHAIN.write_text(json.dumps(chain,indent=2)+'\n')
records=[]
for path in SESSION_DIR.glob('*.jsonl'):
 with path.open('rb') as h:m=json.loads(h.readline()).get('payload',{})
 if m.get('id')!=ROOT_THREAD and m.get('parent_thread_id')!=ROOT_THREAD:continue
 records.append(minimal_record(path))
write(P/'runtime-provenance.json',records)
for n in range(1,30):
 for prefix in ['seed','expanded']:
  d=P/f'{prefix}-iteration-{n:02d}'
  if not d.exists():continue
  if prefix=='seed':
   names={f'seed{n:02}_reader_a',f'seed{n:02}_reader_b','seed_grader',f'seed{n:02}_borderline_adjudicator',f'seed{n:02}_quantifier_adjudicator'}
   if n==1:names.update(['seed_reader_a','seed_reader_b','early_source_auditor'])
   if n==3:names.add('seed03_borderline_adjudicator')
  else:
   names={f'expanded{n:02}_reader_a',f'expanded{n:02}_reader_b',f'final_source_auditor_{n:02}','seed_grader',f'expanded{n:02}_grader',f'full{n:02}_grader','scope_adjudicator_09'}|{f'block{n:02}_grader_{b:02}' for b in range(1,7)}
  selected=[r for r in records if r['agent_path'].split('/')[-1] in names];write(d/'model-provenance.json',selected)
  if prefix=='expanded' and ((d/'final-model-provenance.json').exists() or d.name==Path(json.loads((P/'progress.json').read_text())['final_snapshot_path']).parent.name):
   final={f'expanded{n:02}_reader_a',f'expanded{n:02}_reader_b',f'final_source_auditor_{n:02}','coverage_challenge_10','scope_adjudicator_09'}|{f'block{n:02}_grader_{b:02}' for b in range(1,7)}
   write(d/'final-model-provenance.json',[r for r in records if r['agent_path'].split('/')[-1] in final])
print('Minimal actual-runtime records:',len(records),'with per-record path/ordinal/hash references; no full payloads saved.')
