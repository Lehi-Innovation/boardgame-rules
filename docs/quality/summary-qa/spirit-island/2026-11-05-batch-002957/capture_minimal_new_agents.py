"""Capture explicitly named new agents without copying privileged runtime bodies."""
from pathlib import Path
import datetime,hashlib,json,sys
from provenance_runtime import minimal_metadata,reference
B=Path(__file__).parent.resolve();ROOT_THREAD='01a1ac01-c763-7bb1-901e-7458891630b8';D=B/'runtime';D.mkdir(exist_ok=True)
H=lambda value:hashlib.sha256(value).hexdigest()
def write(path,value,chain=False):
 data=(json.dumps(value,indent=2)+'\n').encode();before=H(path.read_bytes()) if path.exists() else None;after=H(data)
 if before==after:return
 path.write_bytes(data)
 if chain:
  cp=B/'provenance-metadata-update-chain.json';c=json.loads(cp.read_text()) if cp.exists() else {'schema':'metadata-update-chain-v1','updates':[]};c['updates'].append({'path':str(path),'before_sha256':before,'after_sha256':after,'operation':'minimal_new_agent_metadata_and_opaque_hash_receipts_only','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()});cp.write_text(json.dumps(c,indent=2)+'\n')
wanted=set(sys.argv[1:]);assert wanted and all('/' not in x for x in wanted)
existing=json.loads((B/'model-provenance.json').read_text());found={}
for f in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11').glob('*/*.jsonl'):
 with f.open('rb') as h:row=json.loads(h.readline())
 meta=row.get('payload',{});agent=meta.get('agent_path','');task=agent.rsplit('/',1)[-1]
 if meta.get('parent_thread_id')!=ROOT_THREAD or task not in wanted:continue
 assert task not in found
 record=minimal_metadata(f);settings=record['confirmed_settings'];expected='gpt-6-luna' if 'reader' in task else 'gpt-6.1-sol';assert settings and all(x=={'model':expected,'effort':'high'} for x in settings),{'agent':agent,'settings':settings}
 request=record.get('requested_spawn',{}).get('fields',{})
 if request:assert request.get('fork_turns')=='none' and request.get('model')==expected and request.get('reasoning_effort')=='high'
 write(D/f'{task}-metadata.json',record,chain=True)
 receipts={'prompts':[],'task-messages':[],'tool-transcript':[]}
 with f.open('rb') as h:
  for n,line in enumerate(h):
   event=json.loads(line)
   if event.get('type')!='response_item':continue
   p=event.get('payload',{});kind=p.get('type','');roles=[]
   if p.get('role')=='user':roles.append('prompts')
   if kind=='agent_message':roles.append('task-messages')
   if 'output' in p or kind.endswith('tool_call') or kind.endswith('tool_call_output') or kind in ['function_call','function_call_output','custom_tool_call','custom_tool_call_output']:roles.append('tool-transcript')
   if not roles:continue
   receipt={'source_record':reference(f,n,event,line),'payload_type':kind}
   if isinstance(p.get('name'),str):receipt['tool_name']=p['name']
   if isinstance(p.get('role'),str):receipt['role']=p['role']
   for field in ['arguments','output']:
    if field in p:receipt[field+'_opaque_value_sha256']=H(json.dumps(p[field],ensure_ascii=False,sort_keys=True).encode())
   for role in roles:receipts[role].append(receipt)
 for role,items in receipts.items():write(D/f'{task}-{role}.json',{'schema':'opaque-runtime-record-hash-receipts-v1','note':'Only record references, whitelisted event names and hashes are stored. Full original records remain in read-only external runtime; no privileged prompt/environment/permission bodies or decrypted task text copied. Prepared plaintext task instructions and exact game inputs are separate artifacts; no cryptographic plaintext equality claim.','agent':agent,'records':items})
 found[task]={'agent':record['agent'],'thread_id':record['thread_id'],'settings':settings,'metadata':str(D/f'{task}-metadata.json'),'prompt_proof':str(D/f'{task}-prompts.json'),'input_delivery_proof':str(D/f'{task}-tool-transcript.json'),'proof_kind':'minimal_metadata_and_opaque_record_hash_receipts','task_message_proof':str(D/f'{task}-task-messages.json')}
assert set(found)==wanted,{'missing':sorted(wanted-set(found))}
updated=[]
for old in existing:
 key=old['agent'].rsplit('/',1)[-1];updated.append(found.pop(key) if key in found else old)
updated.extend(found.values());write(B/'model-provenance.json',updated)
print(json.dumps({'agents':[{'agent':x['agent'],'settings':x['settings']} for x in updated if x['agent'].rsplit('/',1)[-1] in wanted],'total_profiles':len(updated),'raw_runtime_bodies_copied':False}))
