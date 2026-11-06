from pathlib import Path
import json,sys
R=Path(__file__).resolve().parent
def grade(name,bank,findings):
 d=R/name;q=json.loads((d/'questions.json').read_text())['questions'];key=json.loads((R/bank/'answer-key.json').read_text())['answers'];v={'benchmark_version':bank,'standard':'Semantic requested-part comparison; correct requires all material requested facts, no unresolved/contradictory answer; support label never accepted as grade. Unrequested key context is not required.','readers':{}}
 for reader in ['a','b']:
  a=json.loads((d/f'reader-{reader}.json').read_text())['answers'];by={x['id']:x for x in a};assert len(by)==len(a)==len(q);grades=[]
  for x,y in zip(q,key):
   z=by[x['id']];assert x['id']==y['id'];g,reason=findings.get(reader,{}).get(x['id'],('correct','Every requested material ruling is present, agrees with fixed source-backed key and is supported by the frozen summary. Equivalent wording accepted; no missing facts imported from another answer.'))
   grades.append({'id':x['id'],'question':x['question'],'expected_answer':y['expected_answer'],'source_references':y['source_references'],'observed_answer':z['answer'],'reader_support':z['support'],'reader_evidence':z['evidence'],'grade':g,'reason':reason,'unsupported_guess':False})
  v['readers'][reader]={'counts':{c:sum(g['grade']==c for g in grades) for c in ['correct','partial','incorrect']},'grades':grades}
 (d/'results.json').write_text(json.dumps(v,indent=2)+'\n');print(name,{k:v['counts'] for k,v in v['readers'].items()})
if __name__=='__main__':
 grade('seed-iteration-04','benchmark-v1',{'a':{'Q16':('incorrect','Opens Yes to whether dressing prevents death, then correctly says any additional Wound kills at three Serious. The answer contains contradictory yes/no rulings; cannot silently discard the affirmative answer.')},'b':{'Q13':('partial','Omits the expressly requested Adult death-check procedure entirely; unrequested caveat about surviving Queen injuries does not fill it.'),'Q19':('partial','Omits Malfunction in corresponding Evacuation Section as a prohibition on entering Pod.')}})
