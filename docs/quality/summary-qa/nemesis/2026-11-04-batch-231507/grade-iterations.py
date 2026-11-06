from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent
D=R/'seed-iteration-01';p=D/'results.json';shutil.copyfile(p,D/'results-provisional.json');v=json.loads(p.read_text());up={'a':['Q06','Q19'],'b':['Q13']}
for reader,ids in up.items():
 for x in v['readers'][reader]['grades']:
  if x['id'] in ids:x.update(grade='correct',reason='Independent adjudication: requested ruling is resolved; initial penalty demanded an unrequested detail or discounted equivalent general movement wording. See seed-adjudication.json.')
 for kind in ['correct','partial','incorrect']:v['readers'][reader]['counts'][kind]=sum(x['grade']==kind for x in v['readers'][reader]['grades'])
v['adjudication']='../seed-adjudication.json';p.write_text(json.dumps(v,indent=2)+'\n')
D=R/'seed-iteration-02';q=json.loads((D/'questions.json').read_text())['questions'];key=json.loads((R/'benchmark-v1/answer-key.json').read_text())['answers']
f={'a':{'Q05':'Does not state the requested token destination (removed from game/box); only says remove token.','Q12':'Omits requested Contamination destination and Weapon-in-Hand prerequisite while giving costs and outcomes.','Q20':'Omits entire requested infected-survivor shuffle/draw/death procedure; naming step B is not an answer. Also omits death of Intruders/everything else aboard on engine explosion.'},'b':{'Q05':'Does not state Exploration token destination (removed from game/box); setting Item Counter also omits Nest/Slime exceptions.','Q20':'Engine failure effects omit that Intruders/everything else aboard dies; infection procedure otherwise resolved.'}}
v={'benchmark_version':'benchmark-v1','readers':{}}
for reader in ['a','b']:
 a=json.loads((D/f'reader-{reader}.json').read_text())['answers'];g=[]
 for x,y,z in zip(q,key,a):
  assert x['id']==y['id']==z['id'];reason=f[reader].get(x['id']);g.append({'id':x['id'],'question':x['question'],'expected_answer':y['expected_answer'],'source_references':y['source_references'],'observed_answer':z['answer'],'reader_support':z['support'],'reader_evidence':z['evidence'],'grade':'partial' if reason else 'correct','reason':reason or 'All requested material rulings resolved correctly with summary support. Equivalent phrasing accepted. Unrequested key context and cleanup not required.','unsupported_guess':False})
 v['readers'][reader]={'counts':{x:sum(z['grade']==x for z in g) for x in ['correct','partial','incorrect']},'grades':g}
(D/'results.json').write_text(json.dumps(v,indent=2)+'\n');print({k:z['counts'] for k,z in v['readers'].items()})
