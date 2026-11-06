from pathlib import Path
import json,hashlib,sys
q=Path(__file__).resolve().parent;parent='01a1ab7a-6016-7731-81ac-bfdc0de86fca';records=[]
for p in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*.jsonl'):
 try:
  with p.open() as f: meta=json.loads(f.readline())
  payload=meta.get('payload',{})
  if payload.get('parent_thread_id')!=parent:continue
  # Approval-review runtime sessions have no agent_path and are not delegated QA agents.
  if not isinstance(payload.get('agent_path'),str):continue
  turns=[];initial=[]
  with p.open() as f:
   for line in f:
    x=json.loads(line)
    if x.get('type')=='turn_context':
     y=x['payload'];turns.append({'timestamp':x['timestamp'],'model':y.get('model'),'effort':y.get('effort'),'collaboration_settings':y.get('collaboration_mode',{}).get('settings')})
    if x.get('type')=='response_item' and x.get('payload',{}).get('role')=='user':initial.append(x['payload'])
  record={'session_id':payload['id'],'parent_thread_id':parent,'agent_path':payload.get('agent_path'),'session_path':str(p),'session_meta':{k:payload.get(k) for k in ['id','parent_thread_id','timestamp','agent_path','source','model_provider']},'turn_contexts':turns,'fork_turns':'unresolved','initial_user_messages':initial[:1]};records.append(record)
 except (ValueError,OSError):continue
(q/'model-provenance.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
for d in q.glob('*iteration-*'):
 if not d.is_dir(): continue
 name=d.name
 if name.startswith('seed-iteration-'): prefix='seed'+name.rsplit('-',1)[1]
 elif name.startswith('expanded-iteration-'): prefix='expanded'+name.rsplit('-',1)[1]
 elif name.startswith('integration-iteration-'): prefix='integration'+name.rsplit('-',1)[1]
 else: continue
 hits=[x for x in records if str(x['agent_path']).startswith('/root/'+prefix+'_')]
 (d/'model-provenance.json').write_text(json.dumps(hits,indent=2,ensure_ascii=False)+'\n')
print({'delegated_agent_sessions':len(records)})
parent_session=next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*'+parent+'*'))
spawns=[];followups=[]
for line in parent_session.open():
 x=json.loads(line);y=x.get('payload',{})
 if y.get('type')=='function_call' and y.get('name')=='spawn_agent':
  args=json.loads(y['arguments']);spawns.append({'timestamp':x['timestamp'],'arguments':args})
  for iteration in q.glob('*iteration-*'):
   for reader in ['a','b']:
    target=str(iteration/f'reader-{reader}.json')
    if target in args['message']:
     (iteration/f'reader-{reader}-dispatched-prompt.txt').write_text(args['message']+'\n')
 if y.get('type')=='function_call' and y.get('name') in ['followup_task','send_message']:
  followups.append({'timestamp':x['timestamp'],'tool':y.get('name'),'arguments':json.loads(y['arguments'])})
(q/'reviewer-followup-provenance.json').write_text(json.dumps(followups,indent=2,ensure_ascii=False)+'\n')
(q/'dispatch-provenance.json').write_text(json.dumps(spawns,indent=2,ensure_ascii=False)+'\n')
prompts=q/'runtime-opaque-task-bodies';prompts.mkdir(exist_ok=True)
for x in spawns:
 a=x['arguments'];out=prompts/(a['task_name']+'.txt');body=a['message']+'\n'
 if out.exists() and out.read_text()!=body: out=prompts/(a['task_name']+'-'+str(spawns.index(x))+'.txt')
 if not out.exists():out.write_text(body)

for d in q.glob('*iteration-*'):
 if not d.is_dir(): continue
 if d.name.startswith('expanded-iteration-'):
  auditor='/root/final_source_audit'+d.name.rsplit('-',1)[1]
 elif d.name.startswith('integration-iteration-'):
  auditor='/root/integration_source_audit'+d.name.rsplit('-',1)[1]
 else: continue
 hits=[r for r in records if r['agent_path']==auditor]
 (d/'source-audit-model-provenance.json').write_text(json.dumps(hits,indent=2,ensure_ascii=False)+'\n')
 for call in spawns:
  if str(d/'source-audit.json') in call['arguments']['message']:
   (d/'source-audit-dispatched-prompt.txt').write_text(call['arguments']['message']+'\n')

# The runtime session does not itself expose fork policy. Derive the requested
# value from its actual spawn arguments, rather than treating it as a constant.
dispatch_by_task={x['arguments']['task_name']:x['arguments'] for x in spawns}
for r in records:
 a=dispatch_by_task.get(r['agent_path'].split('/')[-1],{})
 r['fork_turns']=a.get('fork_turns','unresolved')
 r['fork_turns_evidence']='actual parent spawn arguments; distinct session identity is independently recorded'
(q/'model-provenance.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
for d in q.glob('*iteration-*'):
 if not d.is_dir():continue
 num=d.name.rsplit('-',1)[1]
 prefix=('seed' if d.name.startswith('seed-') else 'expanded' if d.name.startswith('expanded-') else 'integration')+num
 hits=[r for r in records if r['agent_path'] in ['/root/'+prefix+'_a','/root/'+prefix+'_b']]
 (d/'model-provenance.json').write_text(json.dumps(hits,indent=2,ensure_ascii=False)+'\n')
 if d.name.startswith(('expanded-','integration-')):
  auditor='/root/'+('final_source_audit' if d.name.startswith('expanded-') else 'integration_source_audit')+num
  (d/'source-audit-model-provenance.json').write_text(json.dumps([r for r in records if r['agent_path']==auditor],indent=2,ensure_ascii=False)+'\n')
validation=[]
for x in spawns:
 a=x['arguments'];validation.append({'task':a['task_name'],'fork_turns_none':a.get('fork_turns')=='none','requested_model':a.get('model'),'requested_effort':a.get('reasoning_effort'),'actual_sessions':[r['session_id'] for r in records if r['agent_path']=='/root/'+a['task_name']]})
(q/'dispatch-validation.json').write_text(json.dumps({'all_fresh_contexts':all(x['fork_turns_none'] for x in validation),'dispatches':validation,'task_body_limit':'Runtime message arguments are opaque ciphertext; they do not recover plaintext task bodies.','metadata_method':'Requested settings from actual spawn arguments; actual model/effort from independent turn_context records.'},indent=2)+'\n')
