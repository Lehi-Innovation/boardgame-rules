import sys,json,hashlib
from pathlib import Path
out=Path(__file__).parent
p=Path(sys.argv[1]); start=int(sys.argv[2]);end=int(sys.argv[3]); assert end-start<50
lines=p.read_text().splitlines();data=lines[start-1:end]
print('\n'.join(f'{i}: {l}' for i,l in enumerate(data,start)))
f=out/'source-read-record.json';r=json.loads(f.read_text());r['reads'].append({'path':str(p.resolve()),'start_physicalLF':start,'end_physicalLF':min(end,len(lines)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'complete_output':True});f.write_text(json.dumps(r,indent=2))
