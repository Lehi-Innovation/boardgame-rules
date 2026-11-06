from qa_tools import *
from collections import Counter
import sys

def adopt(n):
 I=P/f'expanded-iteration-{n:02}';A=P/f'grading-audit-{n:02}.json';ad=json.loads(A.read_text());readers=ad['readers']
 if isinstance(readers,list):readers={x['reader'].replace('reader-','').lower():x for x in readers}
 else:readers={x.replace('reader-','').lower():v for x,v in readers.items()}
 manifest=json.loads((I/'input-manifest.json').read_text());kp=next(Path(x['path']) for x in manifest['inputs'] if Path(x['path']).name=='answer-key.json');keydoc=json.loads(kp.read_text());q=json.loads((I/'questions.json').read_text())['questions'];k=keydoc['answers'];res={'benchmark_version':keydoc['benchmark_version'],'independent_grading_audit':A.name,'root_review':'Evaluator independently read both complete raw sets and compares all requested facts with fixed key; independent audit resolves completeness boundaries.','readers':{}}
 for w in ['a','b']:
  raw=json.loads((I/f'reader-{w}.json').read_text())['answers'];rv=readers[w];rows=rv.get('grades',rv.get('answers'));assert len(rows)==len(raw)==len(q);g=[]
  for a,qq,kk,x in zip(raw,q,k,rows):
   assert a['id']==x['id']==qq['id']==kk['id']
   for f in ['raw_answer','answer']:
    if f in x:assert x[f]==a['answer'],(n,w,a['id'],f)
   un=x.get('unsupported_guess',False)
   g.append({'id':a['id'],'question':qq['question'],'expected_answer':kk['expected_answer'],'source_refs':kk['source_refs'],'actual_answer':a['answer'],'reader_evidence':a['evidence'],'grade':x['grade'].lower(),'reason':x['reason'],'independent_requested_fact_checks':x.get('requested_fact_checks',x.get('resolved_facts',x.get('requested_material_facts',x.get('covered_requested_facts')))),'missing_or_incorrect_facts':x.get('missing_material_facts',x.get('missing_or_unresolved_facts',x.get('missing_or_incorrect_facts',x.get('missing_facts',[]))))+x.get('wrong_rulings',x.get('material_contradictions',x.get('material_wrong_rulings',[]))),'scope_boundary':x.get('boundary',x.get('scope_boundary')),'unsupported_guess':bool(un)})
  c=Counter(x['grade'] for x in g);res['readers'][w]={**{x:c[x] for x in ['correct','partial','incorrect']},'unsupported_guesses':sum(x['unsupported_guess'] for x in g),'grades':g}
 dump(I/'results.json',res);return res
if __name__=='__main__':
 for n in map(int,sys.argv[1:]):
  r=adopt(n);print(n,{w:{k:v for k,v in x.items() if k!='grades'} for w,x in r['readers'].items()})
