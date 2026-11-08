from pathlib import Path
import sys,json,hashlib
from PIL import Image
O=Path('docs/quality/summary-qa/new-angeles/2026-11-05-batch-002957/coverage-fresh-final-94')
files=['extracted/new-angeles-rules.txt','extracted/new-angeles-learn-to-play.txt','extracted/new-angeles-faq.txt']+[f'docs/quality/summary-qa/new-angeles/2026-11-05-batch-002957/expanded-supported-bank-v11/{x}.json' for x in ['questions','answer-key','asked-clause-map']]
if sys.argv[1]=='init':
 m=[]
 for f in files:
  b=Path(f).read_bytes(); s=b.decode();m.append({'file':f,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'unicode_chars':len(s),'ranges':[[i,min(i+5500,len(s))] for i in range(0,len(s),5500)]})
 (O/'input-manifest.json').write_text(json.dumps(m,indent=2));print(json.dumps(m,indent=2))
elif sys.argv[1]=='read':
 f=files[int(sys.argv[2])];s=Path(f).read_text();start=int(sys.argv[3]);end=min(start+5500,len(s));t=s[start:end];rec={'file':f,'start':start,'end':end,'chars':len(t),'sha256_utf8':hashlib.sha256(t.encode()).hexdigest(),'complete':True}
 with (O/'unicode-range-receipts.jsonl').open('a') as out:out.write(json.dumps(rec)+'\n')
 print(json.dumps(rec));print(t,end='');print('\nEND_EXACT_RANGE')
