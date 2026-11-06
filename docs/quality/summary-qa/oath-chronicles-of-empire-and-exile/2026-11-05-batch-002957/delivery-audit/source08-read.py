from pathlib import Path
import hashlib,json,sys
b=Path('/home/jonny/projects/boardgame-rules');p=b/'docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957'
x={'candidate':p/'expanded-iteration-08/summary-snapshot.md','law':b/'extracted/oath-current-law.txt','playbook':b/'extracted/oath-current-playbook.txt','errata':p/'errata.txt'}[sys.argv[1]]
d=x.read_bytes();s=d.decode('utf-8');h=hashlib.sha256(d).hexdigest()
for a in map(int,sys.argv[2:]):
 z=min(a+5000,len(s));chunk=s[a:z];r={'path':str(x.relative_to(b)),'start':a,'end':z,'total':len(s),'sha256':h,'chunk_sha256_utf8':hashlib.sha256(chunk.encode()).hexdigest(),'lineending_representation':'UTF-8 exact; LF and form feed preserved; CR count recorded; no normalization','cr_count':s.count('\r')};print('BEGIN '+json.dumps(r));print(chunk,end='');print('\nEND '+json.dumps({k:r[k] for k in ['path','start','end','total','sha256']}));(p/'delivery-audit/source08-delivery.jsonl').open('a').write(json.dumps(r)+'\n')
