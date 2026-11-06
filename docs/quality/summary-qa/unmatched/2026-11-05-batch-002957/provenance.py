from pathlib import Path
import json,hashlib,re,datetime
P=Path(__file__).resolve().parent;root='01a1ad02-d3f0-7083-bb2c-847ca80bb819';projections=[]
runtime_base=Path('/mnt/c/Users/jonny/.codex/sessions');start_day=datetime.date(2026,11,5);end_day=datetime.datetime.now(datetime.timezone.utc).date()
runtime_dirs=[runtime_base/(start_day+datetime.timedelta(days=i)).strftime('%Y/%m/%d') for i in range((end_day-start_day).days+1)]
for f in (f for directory in runtime_dirs for f in directory.glob('*.jsonl')):
 try:
  it=f.open();line=next(it);d=json.loads(line);meta=d.get('payload',{});source=meta.get('source',{});spawn=source.get('subagent',{}).get('thread_spawn',{}) if isinstance(source,dict) else {}
  if spawn.get('parent_thread_id')!=root and meta.get('id')!=root:continue
  record={'task':spawn.get('agent_path','/root'),'identity':meta.get('id'),'parent':spawn.get('parent_thread_id'),'session_timestamp':meta.get('timestamp'),'runtime_source_path':str(f),'session_meta_record_ordinal':0,'session_meta_record_sha256':hashlib.sha256(line.encode()).hexdigest(),'turns':[],'tool_outputs':[]}
  for ordinal,line in enumerate(it,1):
   d=json.loads(line);v=d.get('payload',{})
   if d.get('type')=='turn_context':record['turns'].append({'ordinal':ordinal,'timestamp':d.get('timestamp'),'model':v.get('model'),'effort':v.get('effort'),'record_sha256':hashlib.sha256(line.encode()).hexdigest()})
   if d.get('type')=='response_item' and v.get('type')=='custom_tool_call_output':
    text='\n'.join(x.get('text','') for x in v.get('output',[]) if isinstance(x,dict)) if isinstance(v.get('output'),list) else str(v.get('output'))
    record['tool_outputs'].append({'ordinal':ordinal,'call_id':v.get('call_id'),'record_sha256':hashlib.sha256(line.encode()).hexdigest(),'contains_truncation_warning':bool(re.search(r'Warning: truncated output|tokens truncated|Output truncated',text)),'visible_character_count':len(text)})
  task=record['task'];reader='reader_' in task
  record.update(requested_model='gpt-6-luna' if reader else 'gpt-6.1-sol',requested_effort='high',fork_turns='none' if task!='/root' else None)
  record['confirmed']=bool(record['turns']) and all(x['model']==record['requested_model'] and x['effort']=='high' for x in record['turns'])
  projections.append(record)
 except (StopIteration,ValueError,KeyError):pass
(P/'model-provenance.json').write_text(json.dumps({'policy':'Minimal runtime projection only; no full session_meta/turn_context or account/instruction data copied. Original runtime logs remain authority. Fork mode is dispatch setting and isolated input protocol, not OS-level filesystem isolation.','agents':projections},indent=2)+'\n')
for r in projections: print(r['task'],r['identity'],r['confirmed'],[(x['model'],x['effort']) for x in r['turns']], 'truncated tool outputs',sum(x['contains_truncation_warning'] for x in r['tool_outputs']))
root_log=next(Path(record['runtime_source_path']) for record in projections if record['identity']==root)
dispatches=[];continuations=[]
for ordinal,line in enumerate(root_log.open()):
 d=json.loads(line);v=d.get('payload',{})
 if v.get('type')=='function_call' and v.get('name')=='spawn_agent':
  a=json.loads(v['arguments'])
  dispatches.append({'task_name':a['task_name'],'fork_turns':a.get('fork_turns'),'requested_model':a.get('model'),'requested_effort':a.get('reasoning_effort'),'timestamp':d.get('timestamp'),'runtime_source_path':str(root_log),'record_ordinal':ordinal,'record_sha256':hashlib.sha256(line.encode()).hexdigest(),'encrypted_task_message_sha256':hashlib.sha256(a['message'].encode()).hexdigest()})
 if v.get('type')=='function_call' and v.get('name')=='followup_task':
  a=json.loads(v['arguments'])
  continuations.append({'target':a['target'],'timestamp':d.get('timestamp'),'runtime_source_path':str(root_log),'record_ordinal':ordinal,'record_sha256':hashlib.sha256(line.encode()).hexdigest(),'task_message_sha256':hashlib.sha256(a['message'].encode()).hexdigest()})
(P/'dispatch-provenance.json').write_text(json.dumps({'note':'Actual root dispatch settings and opaque record hashes only; no full internal metadata or encrypted content copied.','dispatches':dispatches},indent=2)+'\n')
(P/'technical-continuation-provenance.json').write_text(json.dumps({'note':'Actual followup-task targets and record hashes; continuation templates and unchanged cumulative checkpoints retained separately. No encrypted content or internal metadata copied.','continuations':continuations},indent=2)+'\n')
