from pathlib import Path
import sys,json,hashlib
out=Path(__file__).parent
p=Path(sys.argv[1]); start=int(sys.argv[2]); end=int(sys.argv[3]); assert end-start<50
b=p.read_bytes(); lines=b.decode().split('\n'); end=min(end,len(lines))
record={'path':str(p.resolve()),'sha256':hashlib.sha256(b).hexdigest(),'start_physical_LF':start,'end_physical_LF':end,'physical_LF_lines':len(lines)}
f=out/'source-read-record.json'; records=json.loads(f.read_text()) if f.exists() else []; records.append(record);f.write_text(json.dumps(records,indent=2)+'\n')
for n in range(start,end+1): print(str(n)+': '+lines[n-1])
