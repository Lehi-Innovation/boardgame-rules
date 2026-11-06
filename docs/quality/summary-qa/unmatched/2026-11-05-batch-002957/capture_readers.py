"""Preserve every observed raw version, recording own revisions without scoring."""
from pathlib import Path
import json,hashlib,sys,datetime
P=Path(__file__).resolve().parent;I=P/sys.argv[1];index=I/'capture-index.json'
state=json.loads(index.read_text()) if index.exists() else {'method':'Byte-preserve each observed raw version. Own append-policy deviations are recorded separately from the whole-answer factual gate; no raw response is repaired or normalized.','latest':{},'observations':[]}
ids=[x['id'] for x in json.loads((I/'questions.json').read_text())['questions']];rows=[]
for who in ['a','b']:
 f=I/f'reader-{who}.json'
 if not f.exists():rows.append({'reader':who,'count':0,'status':'output_not_yet_written'});continue
 raw=f.read_bytes();d=json.loads(raw);answers=d['answers'];assert [x['id'] for x in answers]==ids[:len(answers)]
 folder=I/f'reader-{who}-batches';folder.mkdir(exist_ok=True);sha=hashlib.sha256(raw).hexdigest();dest=folder/f'captured-{len(answers):03d}-{sha[:16]}.json'
 previous=state['latest'].get(who)
 if not previous:
  old=sorted(folder.glob('count-*.json'))
  previous={'path':str(old[-1])} if old else None
 changes=[]
 if previous:
  before=json.loads(Path(previous['path']).read_text())['answers']
  for x,y in zip(before,answers):
   if x!=y:changes.append({'id':x['id'],'changed_fields':sorted(k for k in set(x)|set(y) if x.get(k)!=y.get(k))})
 if dest.exists():assert dest.read_bytes()==raw
 else:dest.write_bytes(raw)
 row={'reader':who,'count':len(answers),'expected':len(ids),'raw_sha256':sha,'path':str(dest.resolve()),'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'prefix_ids_once':True,'previous_snapshot':previous['path'] if previous else None,'own_saved_entry_changes':changes,'previous_prefix_unchanged':not changes}
 if not state['latest'].get(who) or state['latest'][who]['raw_sha256']!=sha:state['observations'].append(row)
 state['latest'][who]=row;rows.append(row)
index.write_text(json.dumps(state,indent=2)+'\n')
(I/'assembly-progress.json').write_text(json.dumps({'mode':'Observed raw versions preserved with explicit own-revision inventory; no factual assessment inferred','readers':rows},indent=2)+'\n')
print([{k:v for k,v in row.items() if k in ['reader','count','expected','raw_sha256','status','own_saved_entry_changes']} for row in rows])
