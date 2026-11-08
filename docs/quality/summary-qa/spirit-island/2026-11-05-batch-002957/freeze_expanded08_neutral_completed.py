"""Freeze the complete original neutral before parent semantic review."""
from pathlib import Path
import collections, hashlib, json, shutil
B=Path(__file__).resolve().parent
A=B/'expanded-iteration-08/adjudication-01'
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
p=A/'adjudication.json'
j=load(p)
expected=load(A/'raw-cases.json')['requested_cases']
assert collections.Counter((x['reader'],x['id']) for x in j['adjudications'])==collections.Counter((x['reader'],x['id']) for x in expected)
q=A/'adjudication-original-completed.json'
r=A/'adjudication-original-freeze.json'
assert not q.exists() and not r.exists()
shutil.copyfile(p,q)
assert p.read_bytes()==q.read_bytes()
r.write_text(json.dumps({'path':str(p),'sha256':H(p),'immutable_copy':str(q),'immutable_copy_sha256':H(q),'characters':len(p.read_text()),'bytes':p.stat().st_size,'complete_selected_cases':len(expected),'parent_semantic_review_not_yet_started':True,'all_original_fields_retained':True},indent=2)+'\n')
print(json.dumps({'complete_original_neutral_frozen':True,'sha256':H(p),'characters':len(p.read_text()),'selected_cases':len(expected)}))
