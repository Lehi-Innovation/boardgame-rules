from pathlib import Path
import sys,hashlib,json
p=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957')
files={'questions-v10':p/'expanded-v10/questions.json','answers-v10':p/'expanded-v10/answer-key.json','ledger-v10':p/'coverage-ledger-reviewed-08-v10.json'}
f=files[sys.argv[1]];s=f.read_text();receipts=[]
for start in map(int,sys.argv[2:]):
 end=min(start+5000,len(s));chunk=s[start:end];r={'filename':str(f),'start':start,'end':end,'total':len(s),'sha256':hashlib.sha256(chunk.encode()).hexdigest(),'outer_max_output_tokens':7000,'nested_max_output_tokens':7000};print('BEGIN '+json.dumps(r));print(chunk);print('END '+json.dumps(r));receipts.append(r)
with (p/'delivery-audit/coverage08-final-v10-receipts.jsonl').open('a') as out:
 for r in receipts:out.write(json.dumps(r)+'\n')
