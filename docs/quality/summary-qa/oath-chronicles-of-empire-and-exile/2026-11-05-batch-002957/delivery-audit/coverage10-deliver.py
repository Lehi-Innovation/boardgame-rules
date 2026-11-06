from pathlib import Path
import hashlib,json,sys
p=Path(sys.argv[1]);s=p.read_text();h=hashlib.sha256(s.encode()).hexdigest();start=int(sys.argv[2]);end=min(start+5000,len(s)); chunk=s[start:end]
print(f"BEGIN {p} start={start} end={end} total={len(s)} SHA256={h}")
print(chunk,end="")
print(f"\nEND {p} start={start} end={end} total={len(s)} SHA256={h}")
r=Path("docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957/delivery-audit/coverage10-delivery.jsonl")
with r.open("a") as out:out.write(json.dumps(dict(file=str(p),start=start,end=end,total=len(s),sha256=h,chunk_sha256=hashlib.sha256(chunk.encode()).hexdigest()))+"\n")
