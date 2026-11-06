from pathlib import Path
import json
R=Path(__file__).resolve().parent
parent='01a1aaa1-7482-7400-9e88-21f4cb9de263'
targets=['/root/stamped_reader_a','/root/stamped_reader_b','/root/stamped_source_auditor','/root/stamped_answer_adjudicator']
records=[]
for path in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*.jsonl'):
 with path.open() as f:
  try:meta=json.loads(next(f))
  except Exception:continue
  m=meta.get('payload',{});task=m.get('agent_path')
  if m.get('parent_thread_id')!=parent or task not in targets:continue
  context=[]
  for lineno,line in enumerate(f,2):
   try:d=json.loads(line)
   except Exception:continue
   if d.get('type')=='turn_context':
    v=d['payload'];context.append({'line':lineno,'timestamp':d.get('timestamp'),'model':v.get('model'),'effort':v.get('effort')})
  expected='gpt-6-luna' if 'reader' in task else 'gpt-6.1-sol'
  safe={'type':'session_meta','timestamp':meta.get('timestamp'),'id':m.get('id'),'parent_thread_id':m.get('parent_thread_id'),'source':m.get('source'),'agent_path':task,'model_provider':m.get('model_provider')}
  records.append({'task':task,'session_id':m.get('id'),'session_path':str(path),'metadata_record':safe,'turn_context_records':context,'requested_model':expected,'requested_effort':'high','fork_turns':'none','verified':bool(context) and all(c['model']==expected and c['effort']=='high' for c in context),'evidence':'Actual session_meta and turn_context provenance fields; no private base instructions copied.'})
assert len(records)==len(targets) and all(x['verified'] for x in records),records
(R/'stamped-model-provenance.json').write_text(json.dumps(records,indent=2)+'\n')
readers=[x for x in records if 'reader' in x['task']]
old=json.loads((R/'model-provenance.json').read_text());oldids={x['session_id'] for x in old}
assert all(x['session_id'] not in oldids for x in records)
(R/'stamped-iteration-01/model-provenance.json').write_text(json.dumps(readers,indent=2)+'\n')
print([(x['task'],x['verified']) for x in records])
