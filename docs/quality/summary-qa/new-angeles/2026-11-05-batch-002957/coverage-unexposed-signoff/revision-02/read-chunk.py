from pathlib import Path
import sys,hashlib,json
p=Path(sys.argv[1]); start=int(sys.argv[2]); s=p.read_text(); end=min(start+5500,len(s)); t=s[start:end]
r={'path':str(p.resolve()),'start':start,'end_exclusive':end,'total_chars':len(s),'chunk_chars':len(t),'chunk_utf8_sha256':hashlib.sha256(t.encode()).hexdigest(),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'no_truncation':True}
with (Path(__file__).parent/'text-receipts.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
print(json.dumps(r));print(t);print('END EXACT CHUNK',start,end)
