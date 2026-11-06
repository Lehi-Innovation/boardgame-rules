from pathlib import Path
import sys,hashlib,json
p=Path('docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957')
files=[Path('extracted/oath-current-law.txt'),Path('extracted/oath-current-playbook.txt'),p/'errata.txt',p/'expanded-v6/questions.json',p/'expanded-v6/answer-key.json',p/'coverage-ledger-reviewed-07.json']
i,start=map(int,sys.argv[1:]); path=files[i];s=path.open(newline='').read(); sha=hashlib.sha256(s.encode()).hexdigest();end=min(start+5000,len(s))
r={'filename':str(path),'newline_preserved':True,'start':start,'end':end,'total':len(s),'sha256':sha,'chunk_sha256':hashlib.sha256(s[start:end].encode()).hexdigest()}
print('BEGIN '+json.dumps(r));print(s[start:end]);print('END '+json.dumps(r))
with (p/'delivery-audit/coverage07-receipts.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
