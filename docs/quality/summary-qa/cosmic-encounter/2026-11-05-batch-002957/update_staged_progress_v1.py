"""Update only current metadata from immutable stage reports, never grade answers."""
from pathlib import Path
from datetime import datetime,timezone
import json,sys
R=Path(__file__).parent.resolve();it=Path(sys.argv[1]).resolve()
assert it.is_relative_to(R)
p=R/'progress.json';doc=json.loads(p.read_text());entry=next(x for x in doc['iterations'] if x['id']==it.name)
for stage in ('draft','review'):
    counts={};snapshots={}
    for c in 'ab':
        reports=sorted(it.glob(f'reader-{c}-{stage}-batch-[0-9][0-9]-structure.json'))
        if reports:
            latest=json.loads(reports[-1].read_text())
            counts[c]=latest['expected_records'];snapshots[c]={'count':len(reports),'latest_pass':latest['pass'],'latest_report':str(reports[-1])}
        else:counts[c]=0;snapshots[c]={'count':0}
    entry[stage+'_prefix_counts']=counts;entry[stage+'_snapshots']=snapshots
entry['status']='Fixed staged work in progress; archived draft prefixes A%d/B%d and reviewed prefixes A%d/B%d. No factual grading before both reviewed banks complete.' % (entry['draft_prefix_counts']['a'],entry['draft_prefix_counts']['b'],entry['review_prefix_counts']['a'],entry['review_prefix_counts']['b'])
doc['updated_at_utc']=datetime.now(timezone.utc).isoformat()
p.write_text(json.dumps(doc,indent=2)+'\n')
print(entry['status'])
