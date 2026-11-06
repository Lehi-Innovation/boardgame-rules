from pathlib import Path
import json,sys,collections
P=Path(__file__).resolve().parent
bank,it=sys.argv[1:3]
D=P/it;q=json.loads((D/'questions.json').read_text())['questions'];k=json.loads((P/bank/'answer-key.json').read_text())['answers']
# Every answer is manually read in full; default is all requested facts semantically correct and supported.
findings=json.loads((D/'grading-findings.json').read_text())
result={'bank':bank,'iteration':it,'grading_standard':json.loads((P/bank/'answer-key.json').read_text())['grading'],'readers':{}}
for r in 'ab':
 raw=json.loads((D/f'reader-{r}.json').read_text());obs={a['id']:a for a in raw['answers']};rows=[]
 assert len(obs)==len(q)==len(raw['answers'])
 for quest,key in zip(q,k):
  assert quest['id']==key['id'];id=quest['id'];f=findings.get(r,{}).get(id,{})
  rows.append({'id':id,'question':quest['question'],'expected_answer':key['expected_answer'],'source_references':key['source_references'],'observed_answer':obs[id]['answer'],'reader_support':obs[id]['support'],'summary_evidence':obs[id]['evidence'],'grade':f.get('grade','correct'),'reason':f.get('reason','All requested material facts are correctly resolved in this answer and supported by the frozen summary; equivalent wording accepted.'),'unsupported_guess':f.get('unsupported_guess',False)})
 counts=collections.Counter(x['grade'] for x in rows)
 result['readers'][r]={'totals':{**{g:counts[g] for g in ['correct','partial','incorrect']},'unsupported_guesses':sum(x['unsupported_guess'] for x in rows)},'grades':rows}
(D/'results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
print({r:x['totals'] for r,x in result['readers'].items()})
