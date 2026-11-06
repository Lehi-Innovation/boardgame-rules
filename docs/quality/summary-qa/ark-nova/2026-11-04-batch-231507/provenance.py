from pathlib import Path
import json,hashlib
D=Path(__file__).resolve().parent
records=[]
for p in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*.jsonl'):
 with p.open() as f:
  try:m=json.loads(f.readline())
  except:continue
  pl=m.get('payload',{})
  if pl.get('parent_thread_id')!='01a1ab7c-ee08-7cb0-8872-e960cd8afe42':continue
  contexts=[];prompts=[];finals=[];reads=[]
  for l in f:
   try:j=json.loads(l)
   except:continue
   if j.get('type')=='turn_context':contexts.append({k:j['payload'].get(k) for k in ['model','effort','turn_id']})
   if j.get('type')=='response_item':
    x=j.get('payload',{})
    if x.get('type')=='message' and x.get('role')=='user':prompts.append(x)
    if x.get('type')=='message' and x.get('role')=='assistant' and x.get('phase')=='final':finals.append(x)
    if x.get('type') in ['function_call','custom_tool_call']:reads.append({'type':x.get('type'),'call_id':x.get('call_id'),'name':x.get('name'),'arguments':x.get('arguments',x.get('input'))})
    if x.get('type') in ['function_call_output','custom_tool_call_output']:
     blocks=x.get('output','');public=''.join(b.get('text','') for b in blocks) if isinstance(blocks,list) else str(blocks)
     reads.append({'type':'tool_output_access_summary','call_id':x.get('call_id'),'characters':len(public),'truncation_notice':('Warning: truncated output' in public or 'tokens truncated' in public),'prefix':public[:350]})
  r={'session_log_path':str(p),'session_log_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'session_meta':{k:pl.get(k) for k in ['id','parent_thread_id','timestamp','agent_path','model_provider','thread_source']},'turn_contexts':contexts,'runtime_user_messages_not_task_prompt_recovery':prompts,'tool_calls':reads,'final_messages':finals};records.append(r)
(D/'runtime-provenance.json').write_text(json.dumps(records,indent=2));print([(x['session_meta']['agent_path'],x['turn_contexts']) for x in records])
