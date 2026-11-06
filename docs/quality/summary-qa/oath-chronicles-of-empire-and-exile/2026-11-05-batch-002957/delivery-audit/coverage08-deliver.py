from pathlib import Path
import sys,hashlib,json
b=Path('/home/jonny/projects/boardgame-rules');p=b/'docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957'
files={'law':b/'extracted/oath-current-law.txt','playbook':b/'extracted/oath-current-playbook.txt','errata':p/'errata.txt','questions':p/'expanded-v7/questions.json','answers':p/'expanded-v7/answer-key.json','ledger':p/'coverage-ledger-reviewed-08.json'}
f=files[sys.argv[1]];s=f.read_text();receipts=[]
for start in map(int,sys.argv[2:]):
 end=min(start+5000,len(s));chunk=s[start:end];sha=hashlib.sha256(chunk.encode()).hexdigest();r={'filename':str(f),'start':start,'end':end,'total':len(s),'sha256':sha};print('BEGIN '+json.dumps(r));print(chunk);print('END '+json.dumps(r));receipts.append(r)
with (p/'delivery-audit/coverage08-receipts.jsonl').open('a') as out:
 for r in receipts:out.write(json.dumps(r)+'\n')
