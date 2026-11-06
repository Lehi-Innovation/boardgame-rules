from pathlib import Path
import json,sys,hashlib
out=Path(__file__).parent
p=out/'text-receipts.json'
r=json.loads(p.read_text()); i=int(sys.argv[1]); start=int(sys.argv[2]); e=r[i]; s=Path(e['path']).read_text(); end=min(start+4800,len(s)); part=s[start:end]
assert len(part)<=5000
rec={'start_inclusive':start,'end_exclusive':end,'chars':len(part),'sha256':hashlib.sha256(part.encode()).hexdigest(),'delivered':True,'truncated':False}
e['slices']=[x for x in e['slices'] if x['start_inclusive']!=start]+[rec];p.write_text(json.dumps(r,indent=2))
print(json.dumps({'index':i,'path':e['path'],'bounds':[start,end],'length':len(s),'slice_chars':len(part),'truncated':False}));print(part)
