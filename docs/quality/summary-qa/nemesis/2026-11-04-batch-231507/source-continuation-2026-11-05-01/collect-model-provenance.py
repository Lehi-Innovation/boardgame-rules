"""Retain compact actual model/effort/fork metadata without disclosing task or system bodies."""
from pathlib import Path
import json,datetime,sys
R=Path(__file__).resolve().parent
parent=Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/04/rollout-2026-11-04T23-15-54-01a1aa59-7f47-7aa0-b41e-cdb1bdbea5fa.jsonl')
requests={}
with parent.open() as f:
    for line in f:
        try:o=json.loads(line)
        except ValueError:continue
        p=o.get('payload',{})
        if p.get('name')!='spawn_agent':continue
        try:a=json.loads(p['arguments']) if isinstance(p.get('arguments'),str) else p['arguments']
        except (KeyError,ValueError):continue
        name=a.get('task_name','')
        if name.startswith('source_continuation_'):
            requests['/root/'+name]={'model':a.get('model'),'effort':a.get('reasoning_effort'),'fork_turns':a.get('fork_turns'),'timestamp':o.get('timestamp')}
records=[]
for day in ['05','06']:
    folder=Path('/mnt/c/Users/jonny/.codex/sessions/2026/11')/day
    if not folder.exists():continue
    for path in folder.glob('*.jsonl'):
        with path.open() as f:
            try:first=json.loads(next(f));m=first['payload']
            except (ValueError,KeyError,StopIteration):continue
            name=m.get('agent_path','')
            if m.get('parent_thread_id')!='01a1aa59-7f47-7aa0-b41e-cdb1bdbea5fa' or name not in requests:continue
            contexts=[]
            for line in f:
                try:o=json.loads(line)
                except ValueError:continue
                if o.get('type')=='turn_context':
                    p=o['payload'];contexts.append({'timestamp':o.get('timestamp'),'model':p.get('model'),'effort':p.get('effort')})
            req=requests[name]
            ok=bool(contexts) and req['effort']=='high' and req['fork_turns']=='none' and all(c['model']==req['model'] and c['effort']=='high' for c in contexts)
            records.append({'agent_path':name,'session_id':m.get('id'),'runtime_log':str(path),'requested':req,'turn_contexts':contexts,'requested_model_high_forknone_confirmed':ok})
assert records and all(x['requested_model_high_forknone_confirmed'] for x in records)
report={'recorded_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checkpoint':sys.argv[2],'records':records,'actual_runtime_records':len(records),'all_settings_confirmed':True,'isolation':'All continuation initial spawns fork none. Source-only followups retain source context; blind reader followups see only frozen summary/questions/own draft. Graders see own final response and fixed allowed inputs.','task_text_runtime_limit':'Task bodies opaque in runtime log; no plaintext task-hash comparison asserted. Saved prompts and actual dispatch calls retain supplied instructions.','parent_dispatch_log':str(parent)}
with (R/sys.argv[1]).open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps({'actual_runtime_records':len(records),'all_settings_confirmed':True,'models':sorted(set(x['requested']['model'] for x in records))}))
