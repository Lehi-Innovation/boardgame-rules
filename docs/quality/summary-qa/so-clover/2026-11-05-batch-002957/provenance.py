from pathlib import Path
import json,sys
R=Path(__file__).resolve().parent
parent='01a1aaa1-7482-7400-9e88-21f4cb9de263'
records=[]
for path in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*.jsonl'):
 with path.open() as f:
  try:meta=json.loads(next(f))
  except Exception:continue
  m=meta.get('payload',{})
  if m.get('id')!=parent and m.get('parent_thread_id')!=parent:continue
  task=m.get('agent_path','/root')
  context=[]
  for lineno,l in enumerate(f,2):
   try:d=json.loads(l)
   except Exception:continue
   if d.get('type')=='turn_context':
    v=d['payload'];context.append({'line':lineno,'timestamp':d.get('timestamp'),'model':v.get('model'),'effort':v.get('effort')})
  expected='gpt-6-luna' if 'reader' in task else 'gpt-6.1-sol'
  safe={'type':'session_meta','timestamp':meta.get('timestamp'),'id':m.get('id'),'parent_thread_id':m.get('parent_thread_id'),'source':m.get('source'),'agent_path':task,'model_provider':m.get('model_provider')}
  records.append({'task':task,'session_id':m.get('id'),'session_path':str(path),'metadata_record':safe,'turn_context_records':context,'requested_model':expected,'requested_effort':'high','fork_turns':'none' if task!='/root' else 'root session','verified':bool(context) and all(c['model']==expected and c['effort']=='high' for c in context),'evidence':'Actual local session_meta and turn_context records; only provenance fields copied, no private base instructions.'})
assert all(r['verified'] for r in records),records
(R/'model-provenance.json').write_text(json.dumps(records,indent=2)+'\n')
for it,prefix in [('seed-iteration-01','/root/seed_reader_'),('seed-iteration-02','/root/seed02_reader_'),('final-iteration-01','/root/final_reader_')]:
 if (R/it).exists():
  arr=[x for x in records if x['task'].startswith(prefix)]
  (R/it/'model-provenance.json').write_text(json.dumps(arr,indent=2)+'\n')
print([(x['task'],x['verified']) for x in records])
