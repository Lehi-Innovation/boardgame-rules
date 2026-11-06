from build_evidence import *
import re
p=next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*01a1aa9d-614e-7493-a3f2-715a8c52e03d.jsonl'))
rows=[];readers=[]
for l in p.open():
 d=json.loads(l);v=d.get('payload',{})
 if d.get('type')!='response_item' or v.get('type')!='function_call' or not any(t in v.get('name','') for t in ['spawn_agent','followup_task']):continue
 args=v.get('arguments',{})
 if isinstance(args,str):
  try:args=json.loads(args)
  except ValueError:continue
 message=args.get('message','');opaque=message.startswith('gAAAAA');safe={k:v for k,v in args.items() if k!='message'}
 entry={'timestamp':d.get('timestamp'),'ordinal':d.get('ordinal'),'tool':v['name'],'arguments_without_message':safe,'runtime_message_storage':'encrypted opaque body' if opaque else 'plaintext','runtime_message_sha256':hashlib.sha256(message.encode()).hexdigest()};rows.append(entry)
 task=args.get('task_name','')
 if v['name']=='spawn_agent' and re.search(r'(?:^|_)reader_[ab]$',task):
  side=task[-1]
  if task.startswith('seed_reader_'):name='seed-iteration-01'
  elif task.startswith('seed'):name='seed-iteration-'+str(int(re.search(r'seed(\d+)',task).group(1))).zfill(2)
  else:name='expanded-iteration-'+str(int(re.search(r'expanded(\d+)',task).group(1))).zfill(2)
  I=R/name;prompt=I/f'reader-{side}-prompt.txt'
  if not opaque:prompt.write_text(message+'\n')
  record={'agent_task_name':task,'iteration':name,'side':side,'fork_turns':args.get('fork_turns'),'requested_model':args.get('model'),'requested_effort':args.get('reasoning_effort'),'actual_dispatch_timestamp':d.get('timestamp'),'runtime_message_storage':entry['runtime_message_storage'],'runtime_message_sha256':entry['runtime_message_sha256']}
  if prompt.exists():
   normalized=prompt.read_text().replace('/reader-'+side+'.json','/reader-{reader}.json');record.update(prompt_path=str(prompt),prompt_sha256=sha(prompt),normalized_prompt_sha256=hashlib.sha256(normalized.encode()).hexdigest(),plaintext_provenance='Saved before dispatch; sent as visible tool input. Runtime encrypts message body, so plaintext-to-ciphertext equality cannot be independently computed here.' if opaque else 'Exported actual plaintext runtime tool argument')
  readers.append(record)
save(R/'agent-dispatch-manifest.json',{'runtime_path':str(p),'dispatches':rows,'note':'Runtime encrypts dispatch message bodies; retain their hashes and clear model/fork/task fields, without claiming plaintext was recovered. Actual model evidence is separate turn_context metadata.'})
pairs=[]
for name in sorted({r['iteration'] for r in readers}):
 rs=[r for r in readers if r['iteration']==name];same=len(rs)==2 and all('normalized_prompt_sha256' in r for r in rs) and len({r.get('normalized_prompt_sha256') for r in rs})==1;pairs.append({'iteration':name,'same_saved_instructions_except_output_path':same,'readers':rs})
save(R/'reader-protocol-provenance.json',{'method':'Runtime dispatch metadata and encrypted message hashes retained. Prospective plaintext prompt copies are preserved for the clarified scenario-givens protocol; earlier visible prompts remain in tool history and follow the guide, with encrypted runtime bodies disclosed.','pairs':pairs})
