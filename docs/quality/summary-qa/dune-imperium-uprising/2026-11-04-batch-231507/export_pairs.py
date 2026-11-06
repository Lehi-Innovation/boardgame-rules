from pathlib import Path
import json
q=Path(__file__).resolve().parent
pairs=[];prepared=[];pending=[];awaiting=[]
for d in sorted(q.glob('*iteration-*')):
 if (d/'UNDISPATCHED.md').exists():prepared.append(d.name);continue
 if not all((d/f'reader-{r}.json').exists() for r in 'ab'):awaiting.append(d.name);continue
 if not (d/'results.json').exists():pending.append(d.name);continue
 res=json.loads((d/'results.json').read_text());pairs.append({'iteration':d.name,'questions':len(json.loads((d/'questions.json').read_text())['questions']),'has_A_B_results':True,'scores':{r:res['readers'][r]['totals'] for r in 'ab'}})
d={'executed_graded_pairs':len(pairs),'answers':sum(x['questions']*2 for x in pairs),'prepared_only':prepared,'pending_grading':pending,'awaiting_reader_outputs':awaiting,'pairs':pairs}
(q/'executed-pair-export-ledger.json').write_text(json.dumps(d,indent=2)+'\n')
print({k:v for k,v in d.items() if k!='pairs'})
