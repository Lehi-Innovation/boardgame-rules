from pathlib import Path
import json,hashlib,datetime,sys
D=Path(__file__).resolve().parent;P=D.parent
side=sys.argv[1];stage=int(sys.argv[2]);assert side in ['a','b'] and stage in [1,2,3,4]
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fp(p):return {'sha256':h(p),'size':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns}
p=D/(f'reader-{side}.json' if stage==4 else f'reader-{side}-draft-{stage}.json')
x=json.loads(p.read_text());a=x['answers'];ids=[z['id'] for z in a];n=63 if stage==4 else stage*21
assert ids==[f'Q{i:02}' for i in range(1,n+1)],ids
checks={'ordered_unique_ids':True,'all_required_fields':all(all(k in z for k in ['id','answer','support','evidence']) for z in a)}
assert checks['all_required_fields']
if stage in [2,3]:
 prior=json.loads((D/f'reader-{side}-draft-{stage-1}.json').read_text())['answers'];checks['exact_prior_prefix_preserved']=a[:len(prior)]==prior;assert checks['exact_prior_prefix_preserved']
if stage==4:
 prior=json.loads((D/f'reader-{side}-draft-3.json').read_text())['answers'];changes=[{'id':old['id'],'draft':old,'final':new} for old,new in zip(prior,a) if old!=new]
 dest=D/f'reader-{side}-review-changes.json';assert not dest.exists();dest.write_text(json.dumps({'method':'Mechanical comparison only; no semantic draft feedback supplied to reader.','changes':changes,'changed_count':len(changes)},indent=2)+'\n')
dest=D/f'reader-{side}-stage-{stage}-checkpoint.json';assert not dest.exists();record={'frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':stage,'reader':side,'count':n,'checks':checks,'inputs':{str(p):fp(p)}};dest.write_text(json.dumps(record,indent=2)+'\n')
watch=P/'post-change-20261106-01/additional-watched-inputs.json';w=json.loads(watch.read_text());w.update(record['inputs']);w[str(dest)]=fp(dest);watch.write_text(json.dumps(w,indent=2)+'\n')
print(json.dumps({'reader':side,'stage':stage,'count':n,'checks':checks,'sha256':h(p)}))
