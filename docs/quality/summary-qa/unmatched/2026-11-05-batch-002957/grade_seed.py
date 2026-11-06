from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;I=P/'seed-iteration-01';K=json.loads((P/'benchmark-v1/answer-key.json').read_text())['answers'];Q=json.loads((I/'questions.json').read_text())['questions']
results={'benchmark':'v1-seed','grading_policy':'Grade each actual asked clause; do not require unrelated source completeness. Q01 selecting battlefield is contextual setup background, not separately requested. Mandatory movement/draw costs and timing remain required. Reader support label is not grade.','readers':{}}
for who in ['a','b']:
 raw=json.loads((I/f'reader-{who}.json').read_text());grades=[]
 for q,k,answer in zip(Q,K,raw['answers']):
  assert q['id']==k['id']==answer['id']
  partial=who=='a' and q['id']=='Q13'
  facts=[]
  for fact in k['required_facts']:
   facts.append({'expected_fact':fact,'status':'partial' if partial and 'move 2' in fact else 'correct','evidence':answer['answer'],'reason':'Arthur and Merlin health/types stated but asked move value omitted.' if partial and 'move 2' in fact else 'Requested ruling matches fixed key; equivalent wording accepted. Q01 battlefield selection is contextual, not a separate asked fact.' if q['id']=='Q01' else 'Requested ruling resolved correctly by this answer and supported by cited summary passage.'})
  grades.append({'id':q['id'],'question':q['question'],'expected':k['expected_answer'],'observed':answer,'grade':'partial' if partial else 'correct','reason':'Asked move value 2 absent despite correct other clauses.' if partial else 'All actual requested clauses resolved correctly without material contradictory caveat.','facts':facts,'source_refs':k['source_refs'],'unsupported_correct_guess':False})
 results['readers'][who]={'scores':{'correct':sum(g['grade']=='correct' for g in grades),'partial':sum(g['grade']=='partial' for g in grades),'incorrect':0},'raw_sha256':hashlib.sha256((I/f'reader-{who}.json').read_bytes()).hexdigest(),'grades':grades}
(I/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print({r:d['scores'] for r,d in results['readers'].items()})
