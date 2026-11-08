"""Save only allowed identity/model fields and opaque record hashes."""
from pathlib import Path
import json, hashlib, sys, re
ROOT=Path(__file__).parent
PARENT='01a1b3c7-0daa-70f1-9158-0e75d24cbb22'
previous=json.loads((ROOT/'model-provenance.json').read_text())
prefixes=sys.argv[1:]
assert prefixes
rows=[]
for p in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11').rglob('*.jsonl'):
    try:
        with p.open() as f:
            raw=f.readline();r=json.loads(raw);d=r.get('payload',{})
            src=d.get('source',{}); sub=src.get('subagent',{}) if isinstance(src,dict) else {};spawn=sub.get('thread_spawn',{})
            if d.get('id')!=PARENT and spawn.get('parent_thread_id')!=PARENT:continue
            task=spawn.get('agent_path','/root')
            if task!='/root' and not any(task.startswith(prefix) for prefix in prefixes):continue
            rec={'identity':d.get('id'),'parent':spawn.get('parent_thread_id'),'task':spawn.get('agent_path','/root'),'runtime_source_path':str(p),'session_record_ordinal':r.get('ordinal',0),'session_record_sha256':hashlib.sha256(raw.encode()).hexdigest(),'created_at':r.get('timestamp'),'requested_fork_context':'none' if spawn else 'root','actual_fork_context_metadata':None,'context_isolation_evidence':'Explicit fork_turns:none in submitted spawn requests; runtime session metadata confirms identity/parent/path but does not expose a fork-turns setting. Fresh-context request is not misreported as a separately verified runtime field.','turn_records':[]}
            for n,raw in enumerate(f,1):
                r=json.loads(raw)
                if r.get('type')=='turn_context':
                    x=r['payload'];rec['turn_records'].append({'record_ordinal':r.get('ordinal',n),'timestamp':r.get('timestamp'),'actual_model':x.get('model'),'actual_effort':x.get('effort',x.get('reasoning_effort')),'record_sha256':hashlib.sha256(raw.encode()).hexdigest()})
            task=rec['task'];rec['requested_model']='gpt-6-luna' if re.fullmatch(r'/root/expanded[0-9]+_reader_[ab]',task) else 'gpt-6.1-sol';rec['requested_effort']='high'
            rec['settings_verified']=bool(rec['turn_records']) and all(x['actual_model']==rec['requested_model'] and x['actual_effort']=='high' for x in rec['turn_records'])
            rows.append(rec)
    except (ValueError,OSError):continue
updated={r['task']:r for r in rows}
merged=[updated.pop(r['task'],r) for r in previous['agents']]
merged.extend(updated.values())
previous['agents']=merged
previous['filtered_capture_limit']='Only root and explicitly requested task prefixes reread; all other prior task rows preserved unchanged. No old model review repeated.'
(ROOT/'model-provenance.json').write_text(json.dumps(previous,indent=2)+'\n')
print([(r['task'],r['settings_verified']) for r in rows])
