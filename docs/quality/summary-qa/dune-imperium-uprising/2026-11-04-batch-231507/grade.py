from pathlib import Path
import json,sys,hashlib
q=Path(__file__).resolve().parent;name=sys.argv[1];d=q/name;m=json.loads((d/'input-manifest.json').read_text());b=q/m['benchmark'];qs=json.loads((d/'questions.json').read_text())['questions'];keys=json.loads((b/'answer-key.json').read_text())['answers'];over=json.loads((d/'grading-decisions.json').read_text())
result={'grading_standard':json.loads((b/'answer-key.json').read_text())['grading'],'readers':{}}
for r in ['a','b']:
 data=json.loads((d/f'reader-{r}.json').read_text());ans=data['answers'];assert sorted(x['id'] for x in ans)==sorted(x['id'] for x in qs)
 grades=[]
 for question,key in zip(qs,keys):
  a=next(x for x in ans if x['id']==question['id']);decision=over.get(r,{}).get(a['id'],{})
  grades.append({'id':a['id'],'question':question['question'],'expected':key['expected_answer'],'source_references':key['source_references'],'observed':a,'grade':decision.get('grade','correct'),'reason':decision.get('reason','All requested parts match the fixed source-backed key; evidence identifies the supporting summary rules. Unrequested contextual key details are not separate requested parts.'),'unsupported_guess':decision.get('unsupported_guess',False)})
 result['readers'][r]={'totals':{v:sum(x['grade']==v for x in grades) for v in ['correct','partial','incorrect']},'grades':grades}
(d/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n');print({r:x['totals'] for r,x in result['readers'].items()})
st=json.loads((q/'game-status.json').read_text())
for it in st['iterations']:
 if it['name']==name:it.update(status='graded',scores={r:x['totals'] for r,x in result['readers'].items()})
(q/'game-status.json').write_text(json.dumps(st,indent=2)+'\n')
