from pathlib import Path
import json,hashlib,sys
base=Path(__file__).parent
p=Path(sys.argv[1]); a=int(sys.argv[2]); b=int(sys.argv[3])
assert b-a+1<=50
lines=p.read_text().splitlines()
r=json.loads((base/'source-read-record.json').read_text())
r['reads'].append({'path':str(p.resolve()),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'start_line':a,'end_line':min(b,len(lines)),'total_lines':len(lines),'truncated':False})
(base/'source-read-record.json').write_text(json.dumps(r,indent=2))
for n in range(a,min(b,len(lines))+1): print(f'{n}: {lines[n-1]}')
