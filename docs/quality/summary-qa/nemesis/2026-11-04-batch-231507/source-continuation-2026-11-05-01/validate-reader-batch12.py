"""Preserve a completed reader batch using only structural checks, without grading or reader feedback."""
from pathlib import Path
import datetime,hashlib,json,sys
R=Path(__file__).resolve().parent
D=R/'full-iteration-12'
side=sys.argv[1]
assert side in ['a','b']
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,o):
    with p.open('x') as f:json.dump(o,f,ensure_ascii=False,indent=2);f.write('\n')
p=D/('reader-'+side+'-draft.json')
raw=read(p);answers=raw['answers']
ids=[q['id'] for q in read(D/'questions.json')['questions']]
actual=[a['id'] for a in answers]
count=len(actual)
assert 1<=count<=125 and actual==ids[:count], 'Draft must be a contiguous original-order prefix with no repeated or skipped IDs.'
for a in answers:
    assert isinstance(a['requested_parts'],list) and a['requested_parts']
    assert isinstance(a['answer'],str) and isinstance(a['evidence'],str)
    assert a['support'] in ['supported','partial','unsupported']
progress_path=D/('batch-progress-'+side+'.json')
old=read(progress_path) if progress_path.exists() else {'reader':side,'saved_answer_count':0,'batches':[]}
previous=old['saved_answer_count']
assert count>previous, 'No new answered prefix to preserve.'
changes=[]
if old['batches']:
    prev=old['batches'][-1]
    assert sha(Path(prev['snapshot']))==prev['sha256']
    before=read(Path(prev['snapshot']))['answers']
    changes=[before[i]['id'] for i in range(previous) if before[i]!=answers[i]]
folder=D/('draft-batches-'+side)
folder.mkdir(exist_ok=True)
step=len(old['batches'])+1
snapshot=folder/('step-'+str(step).zfill(3)+'.json')
with snapshot.open('xb') as f:f.write(p.read_bytes())
deviations=[]
if changes:deviations.append('Earlier saved answer content changed during drafting; every earlier byte snapshot is preserved. No factual feedback or correction supplied.')
if count-previous>10:deviations.append('Reader exceeded planned up-to10 batch size; actual prefix saved without score-based selection.')
record={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reader':side,'step':step,'previous_count':previous,'saved_answer_count':count,'new_answer_count':count-previous,'remaining':125-count,'snapshot':str(snapshot),'sha256':sha(snapshot),'schema_valid':True,'original_order_prefix_ids_valid':True,'prior_answer_prefix_unchanged':not changes,'prior_answer_ids_changed':changes,'protocol_deviations':deviations,'structural_checks_only':True,'no_rule_grade_or_finding_feedback':True}
new(folder/('step-'+str(step).zfill(3)+'-validation.json'),record)
old.update(saved_answer_count=count,remaining=125-count)
old['batches'].append(record)
progress_path.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ['reader','step','saved_answer_count','new_answer_count','remaining','prior_answer_prefix_unchanged','protocol_deviations']}))
