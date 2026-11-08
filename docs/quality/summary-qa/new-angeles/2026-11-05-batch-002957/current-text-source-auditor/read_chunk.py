from pathlib import Path
import sys,json,hashlib
p=Path(sys.argv[1]); start=int(sys.argv[2]); text=p.read_text(); end=min(start+5500,len(text)); chunk=text[start:end]
r={"path":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"start_inclusive":start,"end_exclusive":end,"total_chars":len(text),"chunk_sha256":hashlib.sha256(chunk.encode()).hexdigest(),"complete":True}
out=Path(__file__).parent
with (out/"text-receipts.jsonl").open("a") as f:f.write(json.dumps(r)+"\n")
print(json.dumps(r));print(chunk)
