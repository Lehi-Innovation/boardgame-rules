from pathlib import Path
import hashlib,json,sys
r=Path('/home/jonny/projects/boardgame-rules')
p=r/sys.argv[1]; start=int(sys.argv[2]); end=int(sys.argv[3]); b=p.read_bytes(); t=b.decode('utf-8'); end=min(end,len(t))
assert 0<=start<end<=len(t) and end-start<=5000
rec={'file':str(p),'start':start,'end':end,'total':len(t),'sha256':hashlib.sha256(b).hexdigest(),'range_sha256':hashlib.sha256(t[start:end].encode()).hexdigest()}
m=json.dumps(rec,ensure_ascii=False)
print('BEGIN '+m); print(t[start:end],end=''); print('\nEND '+m)
with (r/'docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957/delivery-audit/source-audit03-receipts.jsonl').open('a') as f: f.write(m+'\n')
