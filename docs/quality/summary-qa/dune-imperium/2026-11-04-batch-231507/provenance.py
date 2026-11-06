from pathlib import Path
import json
P=Path(__file__).resolve().parent
entries=[]
spawn_args={}
root_runtime=Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05/rollout-2026-11-05T04-16-30-01a1ab6c-b248-72b2-988a-bb4a70bda3e3.jsonl')
for line in root_runtime.open():
 x=json.loads(line);pay=x.get('payload',{})
 if x.get('type')=='response_item' and pay.get('type')=='function_call' and pay.get('name')=='spawn_agent':
  a=json.loads(pay.get('arguments','{}'));name=a.get('task_name')
  if name:spawn_args[name]={k:a.get(k) for k in ['task_name','fork_turns','model','reasoning_effort']}

for path in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*.jsonl'):
 try:
  f=path.open();m=json.loads(next(f))
  meta=m.get('payload',{})
  if meta.get('parent_thread_id')!='01a1ab6c-b248-72b2-988a-bb4a70bda3e3' or not meta.get('agent_path'):f.close();continue
  contexts=[];messages=[]
  for line in f:
   x=json.loads(line)
   if x.get('type')=='turn_context':
    pay=x['payload'];contexts.append({'model':pay.get('model'),'effort':pay.get('effort'),'timestamp':x.get('timestamp'),'turn_id':pay.get('turn_id')})
   if x.get('type')=='response_item' and x['payload'].get('role')=='user':messages.append(x['payload'])
  f.close()
  entry={'task':meta.get('agent_path'),'session_id':meta.get('id'),'parent_thread_id':meta.get('parent_thread_id'),'runtime_file':str(path),'contexts':contexts,'evidence':'session_meta and turn_context records plus parent spawn_agent configuration arguments','actual_spawn_configuration':spawn_args.get(meta.get('agent_path','').split('/')[-1]),'parent_spawn_runtime_file':str(root_runtime),'runtime_user_message_items':messages,'task_prompt_recovered_from_runtime':False,'task_prompt_note':'Readable user capture is environment context only; task/tool bodies may be encrypted. Intended dispatch text is stored separately and must not be represented as runtime recovered.'}
  entries.append(entry)
 except (ValueError,StopIteration):pass
(P/'model-provenance.json').write_text(json.dumps(entries,indent=2,ensure_ascii=False)+'\n')
for d in P.glob('*iteration-*'):
 if not d.is_dir():continue
 prefix=d.name.replace('seed-iteration-','seed_').replace('expanded-iteration-','expanded_')
 subset=[x for x in entries if x['task'] in ['/root/'+prefix+'_a','/root/'+prefix+'_b']]
 (d/'model-provenance.json').write_text(json.dumps(subset,indent=2,ensure_ascii=False)+'\n')
print(f'{len(entries)} agents recorded; task bodies remain encrypted, model/effort/fork settings read from runtime.')
