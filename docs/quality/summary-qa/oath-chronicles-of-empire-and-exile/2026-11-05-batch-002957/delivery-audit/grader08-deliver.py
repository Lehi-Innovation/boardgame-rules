from pathlib import Path
import sys,hashlib,json
p=Path(__file__).resolve().parent.parent
name=sys.argv[1];s=(p/'expanded-iteration-08'/name).read_text();sha=hashlib.sha256((p/'expanded-iteration-08'/name).read_bytes()).hexdigest()
for start in map(int,sys.argv[2:]):
 end=min(start+5000,len(s));chunk=s[start:end]
 receipt=dict(filename=name,start=start,end=end,total=len(s),sha256=sha,chunk_sha256=hashlib.sha256(chunk.encode()).hexdigest(),complete_output=True)
 print('BEGIN '+json.dumps(receipt));print(chunk);print('END '+json.dumps(receipt))
 (p/'delivery-audit'/('grader08-'+name.replace('.','-')+'-'+str(start).zfill(6)+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
