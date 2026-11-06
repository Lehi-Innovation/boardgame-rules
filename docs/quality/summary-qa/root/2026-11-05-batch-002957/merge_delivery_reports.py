from build_evidence import *
from collections import Counter
p=R/'reader-delivery-audit.json'
old=json.loads(p.read_text())
reports={(x['iteration'],x['side']):x for x in old['reports']}
for directory in sorted(list(R.glob('seed-iteration-*'))+list(R.glob('expanded-iteration-*'))):
 for who in ['a','b']:
  path=directory/f'reader-{who}-delivery-audit.json'
  if path.exists():
   report=json.loads(path.read_text());reports[directory.name,who]=report
out={'trigger':'Actual read-call/output delivery verification; no factual score changed because of delivery. Historical reports retained, with stamped-round transport-aware exact-line proofs merged from local immutable-source reports.','reports':list(reports.values()),'summary':dict(Counter(x['line_coverage_status'] for x in reports.values()))}
save(p,out)
print(json.dumps({'reports':len(reports),'summary':out['summary']}))
