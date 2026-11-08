from pathlib import Path
import json,hashlib
B=Path(__file__).parent
agents=json.loads((B/'runtime-provenance.json').read_text());records=[]
for agent in agents:
 p=Path(agent['runtime_log_path']);turns=[]
 for ordinal,line in enumerate(p.open(),1):
  r=json.loads(line)
  if r['type']!='turn_context':continue
  v=r['payload'];m=v.get('model');e=v.get('effort');turns.append({'runtime_path':str(p),'record_ordinal':ordinal,'record_sha256':hashlib.sha256(line.encode()).hexdigest(),'actual_model':m,'actual_effort':e,'matches_requested':m==agent['requested_model'] and e==agent['requested_effort']})
 assert turns and all(x['matches_requested'] for x in turns)
 records.append({'task':agent['task'],'identity':agent['id'],'parent':agent['parent_thread_id'],'requested_model':agent['requested_model'],'requested_effort':agent['requested_effort'],'fork_turns':agent['fork_turns'],'verified_turn_settings':turns})
(B/'runtime-all-turns-provenance.json').write_text(json.dumps({'verified_all_recorded_turns':True,'agents':records,'hygiene':'Only identity/task/parent/requestedactual model-effort/fork/runtime path/record ordinal/opaque original-record hashes. Untouched runtime logs remain external authority; no full metadata copied.'},indent=2)+'\n');print('All',sum(len(x['verified_turn_settings']) for x in records),'turn setting records across',len(records),'agents match requested models/efforts.')
