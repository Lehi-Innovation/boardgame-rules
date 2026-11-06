import sys,json,hashlib
from pathlib import Path
b=Path('/home/jonny/projects/boardgame-rules');p=b/'docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957'
fs={'candidate':p/'expanded-iteration-05/summary-snapshot.md','law':b/'extracted/oath-current-law.txt','playbook':b/'extracted/oath-current-playbook.txt','errata':p/'errata.txt'}
f=fs[sys.argv[1]];raw=f.read_bytes();s=raw.decode('utf-8');h=hashlib.sha256(raw).hexdigest()
for a in map(int,sys.argv[2:]):
 e=min(a+5000,len(s));chunk=s[a:e];rec={'filename':str(f),'start':a,'end':e,'total':len(s),'sha256':h,'chunk_sha256_utf8':hashlib.sha256(chunk.encode()).hexdigest(),'offsets':'zero-based character offsets, end exclusive','line_endings':'UTF-8 bytes decoded directly; original CRLF preserved; console displays line breaks'}
 print('BEGIN '+json.dumps(rec));print(chunk,end='');print('\nEND '+json.dumps(rec))
 with (p/'delivery-audit/source05-text-receipts.jsonl').open('a') as out:out.write(json.dumps(rec)+'\n')
