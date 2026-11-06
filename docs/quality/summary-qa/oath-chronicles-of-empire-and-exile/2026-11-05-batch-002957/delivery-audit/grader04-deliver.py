import pathlib,json,hashlib,sys
base=pathlib.Path(__file__).parent.parent
fn=sys.argv[1]; start=int(sys.argv[2]); t=(base/'expanded-iteration-04'/fn).read_text(); sha=hashlib.sha256(t.encode()).hexdigest()
for st in range(start,min(start+10000,len(t)),5000):
 en=min(st+5000,len(t)); print(f'BEGIN {fn} start={st} end={en} total={len(t)} sha256={sha}'); print(t[st:en]); print(f'END {fn} start={st} end={en} total={len(t)} sha256={sha}')
 with open(base/'delivery-audit'/'grader04-delivery-ranges.jsonl','a') as f: f.write(json.dumps(dict(filename=fn,start=st,end=en,total=len(t),sha256=sha))+'\n')
