import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,re,hashlib,ast
O=Path(__file__).parent;F=O.parent;sha=lambda b:hashlib.sha256(b).hexdigest();item=next(x for x in json.loads((O/'six-B-initial-provenance.json').read_text()) if x['agent']=='/root/v13_stamped_i1_grade_b_06');b=Path(item['runtime_source']).read_bytes();initial=json.loads((O/'06-initial-runtime-projection.json').read_text());assert sha(b[:initial['prefix_bytes']])==initial['prefix_sha256']
records=[json.loads(line) for line in b.splitlines()];events=[(n,x['payload']['type']) for n,x in enumerate(records,1) if x.get('type')=='event_msg' and x.get('payload',{}).get('type') in ['task_started','task_complete','turn_aborted']]
if not events or events[-1][1]!='task_complete' or not (F/'grading-reader-b/block-06/grades-same-entry.json').exists():print(json.dumps({'sixth_actual_terminal':False,'event_labels_only':events}));sys.exit(0)
p={'original_runtime_path':item['runtime_source'],'prefix_bytes':len(b),'prefix_sha256':sha(b),'physical_records':[],'tool_calls':[],'tool_outputs':[],'actual_metadata':[],'events':[],'task_event_metadata':[]};boundary=None;S=r'"(?:\\.|[^"\\])*"'
for n,(x,line) in enumerate(zip(records,b.splitlines(keepends=True)),1):
 q=x.get('payload',{});typ=x.get('type');pt=q.get('type') if isinstance(q,dict) else None;p['physical_records'].append(dict(physical_record=n,ordinal=n-1,sha256=sha(line),bytes=len(line),type=typ,payload_type=pt))
 if typ=='session_meta':
  spawn=q.get('source',{}).get('subagent',{}).get('thread_spawn',{});p['actor_binding']={'physical_record':n,'agent_path':spawn.get('agent_path'),'parent_thread_id':spawn.get('parent_thread_id'),'session_id':q.get('id')}
 if typ=='turn_context':p['actual_metadata'].append({'physical_record':n,'model':q.get('model'),'effort':q.get('effort')})
 if typ=='event_msg' and pt in ['task_started','task_complete','turn_aborted']:p['events'].append({'physical_record':n,'event':pt});p['task_event_metadata'].append({'physical_record':n,'event':pt,'turn_id':q.get('turn_id')})
 if typ=='response_item' and pt in ['custom_tool_call','function_call']:
  raw=q.get('input',q.get('arguments'));p['tool_calls'].append({'physical_record':n,'name':q.get('name'),'call_id':q.get('call_id'),'input':raw})
  if 'QA_ARTIFACT_WRITE_V1' in raw and boundary is None:boundary=n
  if boundary is not None:
   m=re.search(r'(?:cmd|"cmd")\s*:\s*('+S+r')(?:\s*\+\s*('+S+r'))?',raw);assert m;cmd=json.loads(m.group(1))+(json.loads(m.group(2)) if m.group(2) else '');(O/f'06-command-{n}.txt').write_text(cmd)
   if "<<'PY'\n" in cmd:
    program=cmd.split("<<'PY'\n",1)[1].split('\nPY',1)[0];(O/f'06-program-{n}.py').write_text(program);tree=ast.parse(program);print('TERMINAL_PROGRAM',n,'imports',[ast.unparse(x) for x in tree.body if isinstance(x,(ast.Import,ast.ImportFrom))],'calls',sorted(set(ast.unparse(x.func) for x in ast.walk(tree) if isinstance(x,ast.Call))))
   else:print('OTHER_POSTWRITE_COMMAND',n,cmd[:120])
 if typ=='response_item' and pt in ['custom_tool_call_output','function_call_output']:
  v=q['output'];texts=[v] if isinstance(v,str) else [part['text'] for part in v if part.get('type') in ['text','input_text']];p['tool_outputs'].append({'physical_record':n,'call_id':q['call_id'],'text_blocks':texts})
(O/'06-runtime-projection.json').write_text(json.dumps(p,indent=2)+'\n');(O/'06-grades-same-entry.json').write_bytes((F/'grading-reader-b/block-06/grades-same-entry.json').read_bytes());(O/'06-initial-to-terminal-prefix-binding.json').write_text(json.dumps({'initial_prefix_bytes':initial['prefix_bytes'],'initial_prefix_sha256':initial['prefix_sha256'],'initial_prefix_preserved_in_terminal_original':True,'terminal_prefix_bytes':len(b),'terminal_prefix_sha256':sha(b),'actual_task_complete_record':events[-1][0]},indent=2)+'\n');print(json.dumps({'sixth_actual_terminal':True,'first_mutation':boundary,'task_events':events,'all_contexts':p['actual_metadata']}))
