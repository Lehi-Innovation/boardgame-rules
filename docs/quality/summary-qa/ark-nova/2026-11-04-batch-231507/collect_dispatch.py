from pathlib import Path
import json,hashlib,re
D=Path(__file__).resolve().parent
p=Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05/rollout-2026-11-05T04-34-13-01a1ab7c-ee08-7cb0-8872-e960cd8afe42.jsonl')
calls=[]
for l in p.open():
 j=json.loads(l);x=j.get('payload',{})
 if x.get('type')=='function_call' and x.get('name') in ['spawn_agent','followup_task','send_message']:
  try:args=json.loads(x['arguments'])
  except:continue
  calls.append({'timestamp':j.get('timestamp'),'tool':x['name'],'arguments':args})
(D/'intended-dispatch-records.json').write_text(json.dumps({'description':'Exact host-stored dispatch records. Task-message bodies may be encrypted ciphertext, not recovered plaintext; exact intended plaintext templates are saved separately. Environment-only child messages are not task-prompt recovery.','parent_session_log_path':str(p),'calls':calls},indent=2))
runtime=json.loads((D/'runtime-provenance.json').read_text())
byname={r['session_meta']['agent_path'].rsplit('/',1)[-1]:r for r in runtime if r['session_meta']['agent_path']}
for c in calls:
 if c['tool']!='spawn_agent':continue
 a=c['arguments'];name=a.get('task_name','')
 match=re.fullmatch(r'(seed|expanded|integrated)(\d+)_([ab])',name)
 if not match:continue
 kind,number,r=match.groups();t=D/f'{kind}-iteration-{number}'
 if not t.exists():continue
 encrypted=a['message'].startswith('gAAAAA')
 if encrypted:
  (t/f'reader-{r}-dispatch-record-message-ciphertext.txt').write_text(a['message'])
 else:
  (t/f'reader-{r}-actual-dispatch-prompt.txt').write_text(a['message'])
 provenance=byname.get(name)
 intended=t/f'reader-{r}-prompt.txt'
 out={'requested_model':a.get('model'),'requested_effort':a.get('reasoning_effort'),'fork_turns':a.get('fork_turns'),'task_name':name,'host_message_body_storage':'encrypted_ciphertext' if encrypted else 'plaintext','actual_dispatch_plaintext_available':not encrypted,'host_stored_message_sha256':hashlib.sha256(a['message'].encode()).hexdigest(),'intended_prompt_path':str(intended),'intended_prompt_sha256':hashlib.sha256(intended.read_bytes()).hexdigest() if intended.exists() else None,'legacy_actual_dispatch_filename_note':'Any existing actual-dispatch-prompt.txt containing gAAAAA is historical mislabeled ciphertext, not plaintext. See provenance-label-correction-01.' if encrypted else None,'runtime':provenance}
 (t/f'reader-{r}-model-provenance.json').write_text(json.dumps(out,indent=2))
 for rr in 'ab':
  if not (t/f'reader-{rr}-model-provenance.json').exists():break
 else:
  (t/'model-provenance.json').write_text(json.dumps({rr:json.loads((t/f'reader-{rr}-model-provenance.json').read_text()) for rr in 'ab'},indent=2))
print('Saved host-stored dispatch records, intended-template identities, explicit encryption labels and per-reader runtime provenance.')
