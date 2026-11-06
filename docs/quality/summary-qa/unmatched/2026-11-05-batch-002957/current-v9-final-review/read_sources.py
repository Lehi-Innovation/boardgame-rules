from pathlib import Path
import hashlib,json,sys
BASE=Path('/home/jonny/projects/boardgame-rules'); OUT=BASE/'docs/quality/summary-qa/unmatched/2026-11-05-batch-002957/current-v9-final-review'
B='docs/quality/summary-qa/unmatched/2026-11-05-batch-002957/'
P='docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/unmatched/'
files={x:B+'benchmark-v9/'+x+'.json' for x in ['questions','answer-key','scope-map','versioned-corrections','input-manifest']}
files.update({x:B+x+'.json' for x in ['coverage-ledger-v9','coverage-ledger-v8-addendum']})
files['rules']='extracted/unmatched-rules.txt'
files.update({x:P+x+'.json' for x in ['designer-boost-values-2019-primary-post','designer-public-author-profile']})
files.update({x:B+'source-research/arthur-clarification/'+x+'.json' for x in ['justin-excalibur-primary-article36640902-api','justin-jacobson-author43936-api']})
files.update({x:B+'source-research/iello-2025-official-erratum/'+x for x in ['publisher-full-visible-text-v2.txt','publisher-article-body-v2.txt','publisher-page.html','extraction-v2-provenance.json']})
if sys.argv[1]=='meta':
 data={k:{'path':str(BASE/v),'bytes':len((BASE/v).read_bytes()),'characters':len((BASE/v).read_text()),'sha256':hashlib.sha256((BASE/v).read_bytes()).hexdigest()} for k,v in files.items()}
 (OUT/'text-metadata.json').write_text(json.dumps(data,indent=2));print(json.dumps(data,indent=2))
else:
 key=sys.argv[1];start=int(sys.argv[2]);s=(BASE/files[key]).read_text();end=min(start+4800,len(s)); print(f'{key} [{start},{end})/{len(s)}\n'+s[start:end]);
 log=OUT/'text-read-receipts.jsonl'
 with log.open('a') as f:f.write(json.dumps({'key':key,'start':start,'end':end,'total':len(s),'characters_returned':end-start,'truncated':False,'sha256':hashlib.sha256((BASE/files[key]).read_bytes()).hexdigest()})+'\n')
