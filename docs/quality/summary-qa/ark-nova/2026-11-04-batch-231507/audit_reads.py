from pathlib import Path
import json,re
D=Path(__file__).resolve().parent
records=json.loads((D/'runtime-provenance.json').read_text())
out=[]
for a in records:
 name=a['session_meta']['agent_path']
 if not name or not re.search(r'/(seed|expanded|integrated)\d+_[ab]$',name):continue
 calls={x.get('call_id'):x for x in a['tool_calls'] if x.get('type') in ['function_call','custom_tool_call']}
 items=[]
 for x in a['tool_calls']:
  if x.get('type')!='tool_output_access_summary':continue
  c=calls.get(x.get('call_id'),{})
  arg=c.get('arguments','')
  items.append({'call_id':x.get('call_id'),'tool_input_code':arg,'output':x,'read_candidate':any(w in str(arg) for w in ['cat ','sed ','read_text','readFile','rg ','tail ','head '])})
 out.append({'agent_path':name,'session_log_path':a['session_log_path'],'model_effort':a['turn_contexts'],'calls':items,'evaluator_complete_input_verdict':'pending manual range review; truncation alone is not failure if recovered by later reads'})
(D/'runtime-input-read-summaries.json').write_text(json.dumps(out,indent=2))
print([(r['agent_path'],len(r['calls']),sum(bool(x['output'].get('truncation_notice')) for x in r['calls'])) for r in out])
