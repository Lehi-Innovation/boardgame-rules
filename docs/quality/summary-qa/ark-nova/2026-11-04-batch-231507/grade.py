from pathlib import Path
import json,sys,hashlib
D=Path(__file__).resolve().parent
it,version=sys.argv[1:3];t=D/it;v=D/version
# Per-answer judgments are supplied by evaluator after reading full raw outputs.
notes=json.loads((t/'grade-decisions.json').read_text());q=json.loads((t/'questions.json').read_text());key=json.loads((v/'answer-key.json').read_text());key={x['id']:x for x in key['answers']};res={'grading_standard':'Every requested part, no cross-answer borrowing; unsupported parts partial, contradictions incorrect. Extra key details not requested are not separately demanded.','readers':{}}
for r in 'ab':
 raw=json.loads((t/f'reader-{r}.json').read_text());out=[]
 assert sorted(x['id'] for x in raw['answers'])==sorted(key)
 if it.startswith(('expanded-','integrated-')):
  assert set(notes[r])==set(key), 'Full-bank runs require an explicit judgment for every answer'
 observed_by_id={a['id']:a for a in raw['answers']}
 for question in q['questions']:
  a=observed_by_id[question['id']];n=notes[r].get(a['id'],['correct','Every requested part is resolved in the observed answer and supported by the frozen summary; equivalent wording accepted.'])
  if it.startswith(('expanded-','integrated-')):
   assert len(n)>2 and isinstance(n[2],bool), 'Full-bank judgments must explicitly adjudicate unsupported guesses'
  out.append({'id':a['id'],'question':question['question'],'expected':key[a['id']],'observed':a,'grade':n[0],'reason':n[1],'unsupported_guess':bool(n[2]) if len(n)>2 else False})
 counts={g:sum(x['grade']==g for x in out) for g in ['correct','partial','incorrect']};res['readers'][r]={'counts':counts,'grades':out}
(t/'results.json').write_text(json.dumps(res,indent=2));print(it,{r:res['readers'][r]['counts'] for r in 'ab'})
