from pathlib import Path
import sys,json,hashlib
p=Path(sys.argv[1]); start=int(sys.argv[2]); data=p.read_bytes(); s=data.decode('utf-8'); end=min(start+6000,len(s)); chunk=s[start:end]
row={'path':str(p),'start':start,'end':end,'character_length':len(s),'byte_length':len(data),'source_sha256':hashlib.sha256(data).hexdigest(),'slice_sha256':hashlib.sha256(chunk.encode()).hexdigest(),'output_cap':4000,'truncated':False}
log=Path('/tmp/audit13-ledger.jsonl'); log.open('a').write(json.dumps(row)+'\n')
print(json.dumps(row)); print(chunk)
