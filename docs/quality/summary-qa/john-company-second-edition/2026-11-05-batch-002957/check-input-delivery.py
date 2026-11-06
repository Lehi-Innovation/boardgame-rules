"""Confirm that blind readers received every summary line and question text."""
from pathlib import Path
import json,sys
R=Path(__file__).resolve().parent
benchmark,iteration,agent_prefix=sys.argv[1:4]
base=R/benchmark/iteration
records=json.loads((R/'model-provenance.json').read_text())['records']
results={}
for role in 'ab':
 rec=next(x for x in records if x['agent']==f'/root/{agent_prefix}_reader_{role}')
 outputs=[];calls=[]
 for line in Path(rec['runtime_source']).open():
  item=json.loads(line);payload=item.get('payload',{})
  if item.get('type')!='response_item':continue
  if payload.get('type')=='custom_tool_call':
   code=payload.get('input','')
   if any(marker in code for marker in ['cat >','write_text','open(output','json.dump(']):break
   calls.append({'id':payload.get('call_id'),'input':code})
  elif payload.get('type')=='custom_tool_call_output':
   value=payload.get('output','')
   outputs.append('\n'.join(x.get('text','') for x in value) if isinstance(value,list) else str(value))
 delivered='\n'.join(outputs)
 lines=(base/'summary-snapshot.md').read_text().splitlines()
 missing=[n for n,line in enumerate(lines,1) if line.strip() and line not in delivered]
 questions=json.loads((base/'questions.json').read_text())['questions']
 absent=[q['id'] for q in questions if q['question'] not in delivered and json.dumps(q['question'],ensure_ascii=False)[1:-1] not in delivered]
 results[role]={'runtime_source':rec['runtime_source'],'read_calls':calls,'truncated_responses':sum('Warning: truncated output' in x for x in outputs),'summary_lines':len(lines),'nonblank_summary_lines_not_visible':missing,'question_texts_not_visible':absent,'complete_input_delivery_confirmed':not missing and not absent and not any('Warning: truncated output' in x for x in outputs),'limits':'Instruction isolation within shared filesystem; confirms supplied text visibility, not perfect attention or understanding.'}
(base/'input-delivery-validation.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({role:{k:v for k,v in data.items() if k not in ['read_calls','runtime_source','limits']} for role,data in results.items()},indent=2))
