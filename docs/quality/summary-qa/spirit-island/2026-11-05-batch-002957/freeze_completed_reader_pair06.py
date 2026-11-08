"""Freeze both entire original completed outputs before any factual diagnostics."""
from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).resolve().parent;D=B/'expanded-iteration-06';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text())
ids=[x['id'] for x in load(D/'questions.json')['questions']];prepared=[]
for r in 'ab':
 p=D/f'reader-{r}.json';data=load(p);assert data['stage']=='complete';got=[x['id'] for x in data['answers']];assert len(got)==len(ids)==173 and set(got)==set(ids) and len(got)==len(set(got));dest=D/f'reader-{r}-original-completed.json';receipt=D/f'reader-{r}-original-freeze.json';assert not dest.exists() and not receipt.exists();prepared.append((p,dest,receipt))
for p,dest,receipt in prepared:
 shutil.copyfile(p,dest);assert dest.read_bytes()==p.read_bytes();receipt.write_text(json.dumps({'path':str(p),'sha256':H(p),'characters':len(p.read_text()),'bytes':p.stat().st_size,'immutable_copy':str(dest),'immutable_copy_sha256':H(dest),'stage':'complete','answer_count':173,'frozen_before_any_factual_diagnostics':True,'entire_original_fields_and_quotations_retained':True},indent=2)+'\n');print(json.dumps({'path':str(dest),'sha256':H(dest),'answer_count':173}))
