"""Freeze the completed original audit before any parent semantic review."""
from pathlib import Path
import datetime,hashlib,json
B=Path(__file__).resolve().parent
H=lambda data:hashlib.sha256(data).hexdigest()
load=lambda p:json.loads(p.read_text())
names=['source-audit-final-15.json','source-audit-final-15-read-ledger.json','source-audit-final-15-visual-manifest.json']
assert all((B/name).is_file() for name in names)
dest=B/'source-audit15-original-completed'
assert not dest.exists()
freeze_path=B/'source-audit15-original-freeze.json'
boundary_path=B/'source-audit15-original-completed-runtime-boundary.json'
assert not freeze_path.exists() and not boundary_path.exists()
# Read only bytes for preservation; semantic review is a later, distinct step.
raw={name:(B/name).read_bytes() for name in names}
profile=load(B/'runtime/final_source_audit_15-initial-projection.json')
session=Path(profile['session_path'])
prefix_hash=hashlib.sha256();prefix_bytes=0;record_count=0
with session.open('rb') as f:
 for line in f:
  assert line.endswith(b'\n'), 'runtime record still being written; retry after agent completion'
  prefix_hash.update(line);prefix_bytes+=len(line);record_count+=1
boundary={'session_path':str(session),'record_count':record_count,'prefix_bytes':prefix_bytes,'prefix_sha256':prefix_hash.hexdigest(),'captured_after_agent_reported_completion':True,'before_parent_semantic_review':True,'no_runtime_bodies_copied':True}
dest.mkdir()
files={}
for name,data in raw.items():
 (dest/name).write_bytes(data)
 assert (dest/name).read_bytes()==(B/name).read_bytes()
 files[name]={'sha256':H(data),'bytes':len(data),'original_completed_copy':str(dest/name)}
boundary_path.write_text(json.dumps(boundary,indent=2)+'\n')
freeze={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':files,'before_parent_semantic_review':True,'no_semantic_adoption':True,'runtime_boundary':str(boundary_path),'runtime_boundary_sha256':H(boundary_path.read_bytes())}
freeze_path.write_text(json.dumps(freeze,indent=2)+'\n')
print(json.dumps({'frozen':True,'files':files,'runtime_records':record_count,'freeze_sha256':H(freeze_path.read_bytes())}))
