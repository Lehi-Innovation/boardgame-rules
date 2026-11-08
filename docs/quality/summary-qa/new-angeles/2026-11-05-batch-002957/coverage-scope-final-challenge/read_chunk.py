from pathlib import Path
import sys,json,hashlib,datetime
base=Path('/home/jonny/projects/boardgame-rules');out=Path(__file__).parent
arg=sys.argv[1]; p=base/arg if not arg.startswith('/') else Path(arg)
s=p.read_text();a=int(sys.argv[2]);b=min(a+5500,len(s));part=s[a:b]
r={'path':str(p),'start':a,'end_exclusive':b,'total_chars':len(s),'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'chunk_utf8_sha256':hashlib.sha256(part.encode()).hexdigest(),'chunk_chars':len(part),'no_truncation':True,'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
with (out/'text-receipts.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
print(json.dumps(r));print(part)
