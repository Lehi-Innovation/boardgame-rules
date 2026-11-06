from pathlib import Path
import json,hashlib,shutil,sys,datetime,difflib
R=Path(__file__).resolve().parent; ROOT=R.parents[4]
benchmark,iteration=sys.argv[1:3]
out=R/iteration;out.mkdir(exist_ok=False)
for name in ['questions.json','answer-key.json']:shutil.copyfile(R/benchmark/name,out/name)
shutil.copyfile(ROOT/'rules/so-clover.md',out/'summary-snapshot.md')
paths=[out/'summary-snapshot.md',out/'questions.json',out/'answer-key.json',ROOT/'extracted/so-clover-rules.txt',ROOT/'source_pdfs/so-clover-rules.pdf']
(out/'input-manifest.json').write_text(json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'benchmark':benchmark,'requested_model':'gpt-6-luna','requested_effort':'high','fork_turns':'none','inputs':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}},indent=2)+'\n')
previous=sorted(R.glob('*iteration-*/summary-snapshot.md'))
previous=[p for p in previous if p.parent!=out]
a=previous[-1].read_text() if previous else ''
(out/'summary-changes.patch').write_text(''.join(difflib.unified_diff(a.splitlines(True),(out/'summary-snapshot.md').read_text().splitlines(True),fromfile=str(previous[-1]) if previous else '/dev/null',tofile=str(out/'summary-snapshot.md'))))
p=json.loads((R/'progress.json').read_text());p['phase']='blind-readers';p['iterations'].append({'path':str(out),'benchmark':benchmark,'status':'frozen'});(R/'progress.json').write_text(json.dumps(p,indent=2)+'\n')
