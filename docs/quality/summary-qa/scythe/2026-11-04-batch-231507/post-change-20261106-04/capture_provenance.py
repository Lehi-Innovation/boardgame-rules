from pathlib import Path
import json,sys,datetime
D=Path(__file__).resolve().parent
stage=sys.argv[1]
roles=json.loads((D/'dispatch-records.json').read_text())['agents']
if (D/'grader-dispatch-records.json').exists():
 roles.update(json.loads((D/'grader-dispatch-records.json').read_text())['agents'])
if len(sys.argv)>2:
 roles={k:v for k,v in roles.items() if k in sys.argv[2:]}
found={}
for path in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/06').glob('*.jsonl'):
 meta=None;contexts=[];calls=[]
 for line in path.open():
  try:d=json.loads(line)
  except ValueError:continue
  v=d.get('payload',{})
  if d.get('type')=='session_meta':
   source=v.get('source',{});spawn=source.get('subagent',{}).get('thread_spawn',{}) if isinstance(source,dict) else {};role=spawn.get('agent_path','').split('/')[-1]
   if role not in roles or spawn.get('parent_thread_id')!='01a1aac5-76e9-7752-846f-420015969a30':break
   meta={'role':role,'session_id':v['id'],'session_log':str(path),'source':source,'started':d.get('timestamp')}
  elif meta and d.get('type')=='turn_context':contexts.append({k:v.get(k) for k in ['model','effort','turn_id']})
  elif meta and d.get('type')=='response_item' and v.get('type') in ['function_call','custom_tool_call']:calls.append(v)
 if meta:found[meta['role']]={**meta,'contexts':contexts,'tool_calls':calls}
parent=Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05/rollout-2026-11-05T01-13-50-01a1aac5-76e9-7752-846f-420015969a30.jsonl')
spawns={}
for line in parent.open():
 try:d=json.loads(line);v=d.get('payload',{})
 except ValueError:continue
 if d.get('type')!='response_item' or 'spawn_agent' not in v.get('name',''):continue
 try:a=json.loads(v.get('arguments','{}'))
 except (ValueError,TypeError):continue
 if a.get('task_name') in roles:spawns[a['task_name']]={k:a.get(k) for k in ['task_name','model','reasoning_effort','fork_turns']}
checks={}
for role,request in roles.items():
 record=found.get(role,{});spawn=spawns.get(role,{})
 checks[role]=bool(record.get('contexts')) and all(c['model']==request['model'] and c['effort']=='high' for c in record['contexts']) and spawn.get('fork_turns')=='none' and spawn.get('model')==request['model'] and spawn.get('reasoning_effort')=='high'
out={'stage':stage,'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'parent_runtime_path':str(parent),'parent_spawn_proof':spawns,'agents':found,'actual_required_settings_verified':all(checks.values()),'checks':checks,'isolation_limit':'Original parent fork settings and actual child turn contexts are verified. Saved prompts retain the intended dispatch text; encrypted task payloads are not decrypted. Context/input restriction is prompt-based, not OS enforcement.'}
dest=D/f'model-provenance-{stage}.json'
assert not dest.exists(),dest
dest.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'stage':stage,'all_required_settings_verified':out['actual_required_settings_verified'],'agents':{k:{'session_id':v['session_id'],'contexts':v['contexts'],'parent_spawn':spawns.get(k)} for k,v in found.items()}},indent=2))
assert all(checks.values()),checks
