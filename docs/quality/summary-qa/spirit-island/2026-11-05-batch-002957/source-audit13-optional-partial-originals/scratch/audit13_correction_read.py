from pathlib import Path
import hashlib,sys,json
p=Path(sys.argv[1]); start=int(sys.argv[2]); data=p.read_bytes(); s=data.decode(); end=min(start+6000,len(s)); chunk=s[start:end]
row={'path':str(p),'start':start,'end':end,'character_length':len(s),'byte_length':len(data),'source_sha256':hashlib.sha256(data).hexdigest(),'slice_sha256':hashlib.sha256(chunk.encode()).hexdigest(),'output_cap':4000,'truncated':False,'read_type':'new whole-file reread'}
Path('/tmp/audit13-correction-reads.jsonl').open('a').write(json.dumps(row)+'\n'); print(json.dumps(row)); print(chunk)
