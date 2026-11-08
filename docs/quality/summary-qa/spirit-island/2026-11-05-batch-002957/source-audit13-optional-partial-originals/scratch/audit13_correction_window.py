from pathlib import Path
import sys,json,hashlib
p=Path(sys.argv[1]); start=int(sys.argv[2]); stop=int(sys.argv[3]); data=p.read_bytes(); s=data.decode(); end=min(stop,len(s)); assert end-start<=6000; chunk=s[start:end]
r={'path':str(p),'start':start,'end':end,'character_length':len(s),'byte_length':len(data),'source_sha256':hashlib.sha256(data).hexdigest(),'slice_sha256':hashlib.sha256(chunk.encode()).hexdigest(),'output_cap':4000,'truncated':False,'read_type':'new focused reopen','focused_window':[start,end]}
Path('/tmp/audit13-correction-reads.jsonl').open('a').write(json.dumps(r)+'\n');print(json.dumps(r));print(chunk)
