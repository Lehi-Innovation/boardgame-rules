from pathlib import Path
import sys,hashlib,json,datetime
out=Path(__file__).parent;p=out.parent.parent/'expanded-summary-preparation-01.md';s=p.read_text();n=int(sys.argv[1]);a=n*5500;b=min(a+5500,len(s));t=s[a:b]
r={'source':str(p.resolve()),'chunk':n,'start_char':a,'end_char_exclusive':b,'total_chars':len(s),'chunk_sha256_utf8':hashlib.sha256(t.encode()).hexdigest(),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with (out/'text-delivery-receipts.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
print(json.dumps(r));print(t);print('END_CHUNK '+str(n)+' '+r['chunk_sha256_utf8'])
