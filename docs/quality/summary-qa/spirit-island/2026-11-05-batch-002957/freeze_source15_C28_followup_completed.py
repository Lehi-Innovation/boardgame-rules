"""Freeze both whole own-current-body followup originals before semantics."""
from pathlib import Path
import hashlib,json,shutil
B=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert H(B/'source-candidate-28.md')==H(B.parents[4]/'rules/spirit-island.md')=='8f17f3ce025a16045709c4302e1c2e46d9da22c1e705fc4db28d8b7182985e5c'
names=['source-audit15-current-body-C28-followup.json','source-audit15-current-body-C28-followup-read-view-ledger.json']
prepared=[]
for name in names:
 p=B/name
 obj=json.loads(p.read_text())
 assert isinstance(obj,dict) and obj
 prepared.append((p,obj))
D=B/'source-audit15-C28-followup-original-completed'
assert not D.exists()
D.mkdir()
rows=[]
for p,obj in prepared:
 q=D/p.name
 shutil.copyfile(p,q)
 assert p.read_bytes()==q.read_bytes()
 rows.append({'path':str(p),'sha256':H(p),'bytes':p.stat().st_size,'characters':len(p.read_text()),'immutable_copy':str(q),'immutable_copy_sha256':H(q)})
profile=json.loads((B/'runtime/final_source_audit_15-metadata.json').read_text())
f=Path(profile['session_path'])
sha=hashlib.sha256();count=0
with f.open('rb') as stream:
 for line in stream:
  sha.update(line);count+=1
receipt={'originals':rows,'parent_semantic_inspection_not_yet_started':True,'same_original_pure_auditor_not_new_vote':True,'external_runtime_path':str(f),'runtime_records_at_completed_freeze':count,'runtime_sha256_at_completed_freeze':sha.hexdigest(),'prior_completed_records_excluded_from_new_delivery_claim':811,'new_record_interval':[811,count],'all_original_fields_retained':True,'private_runtime_bodies_copied':False}
(D/'original-freeze.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'both_followup_originals_frozen':True,'files':rows,'new_record_interval':[811,count]}))
