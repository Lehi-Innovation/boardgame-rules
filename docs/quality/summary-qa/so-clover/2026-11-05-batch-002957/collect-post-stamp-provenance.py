from pathlib import Path
import json
R=Path(__file__).resolve().parent;parent='01a1aaa1-7482-7400-9e88-21f4cb9de263';records=[]
for path in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*.jsonl'):
 with path.open() as f:
  try:meta=json.loads(next(f))
  except Exception:continue
  m=meta.get('payload',{});task=m.get('agent_path','')
  if m.get('parent_thread_id')!=parent or not (task.startswith('/root/stamped') or task=='/root/grading_scope_reviewer'):continue
  contexts=[]
  for lineno,l in enumerate(f,2):
   try:d=json.loads(l)
   except Exception:continue
   if d.get('type')=='turn_context':
    c=d['payload'];contexts.append({'line':lineno,'timestamp':d.get('timestamp'),'model':c.get('model'),'effort':c.get('effort')})
  expected='gpt-6-luna' if '_reader_' in task else 'gpt-6.1-sol'
  records.append({'task':task,'session_id':m.get('id'),'session_path':str(path),'metadata_record':{'type':'session_meta','timestamp':meta.get('timestamp'),'id':m.get('id'),'parent_thread_id':m.get('parent_thread_id'),'source':m.get('source'),'agent_path':task,'model_provider':m.get('model_provider')},'turn_context_records':contexts,'requested_model':expected,'requested_effort':'high','fork_turns':'none','verified':bool(contexts) and all(c['model']==expected and c['effort']=='high' for c in contexts),'evidence':'Actual local session_meta and turn_context fields; no private base instructions copied.'})
assert records and all(x['verified'] for x in records)
old={x['session_id'] for x in json.loads((R/'model-provenance.json').read_text())}
assert all(x['session_id'] not in old for x in records)
(R/'post-stamp-model-provenance.json').write_text(json.dumps(records,indent=2)+'\n')
for it,prefix in [('stamped-iteration-01','/root/stamped_reader_'),('stamped-iteration-02','/root/stamped02_reader_'),('stamped-iteration-03','/root/stamped03_reader_')]:
 readers=[x for x in records if x['task'].startswith(prefix)];assert len(readers)==2
 (R/it/'model-provenance.json').write_text(json.dumps(readers,indent=2)+'\n')
print('Confirmed',len(records),'new independent sessions; all requested models/high match runtime.')
