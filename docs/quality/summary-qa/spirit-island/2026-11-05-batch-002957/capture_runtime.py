from pathlib import Path
import json,hashlib,datetime
from provenance_runtime import minimal_metadata
B=Path(__file__).parent;parent='01a1ac01-c763-7bb1-901e-7458891630b8';out=B/'runtime';out.mkdir(exist_ok=True)
def write_metadata(path,value):
 data=(json.dumps(value,indent=2)+'\n').encode();before=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None;after=hashlib.sha256(data).hexdigest()
 if before==after:return
 path.write_bytes(data);chainpath=B/'provenance-metadata-update-chain.json';chain=json.loads(chainpath.read_text()) if chainpath.exists() else {'schema':'metadata-update-chain-v1','updates':[]}
 chain['updates'].append({'path':str(path.resolve()),'before_sha256':before,'after_sha256':after,'operation':'refresh_minimal_runtime_projection','timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat()});chainpath.write_text(json.dumps(chain,indent=2)+'\n')
found=[]
# The active batch spans UTC midnight; retain the parent-thread filter across dates.
for f in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11').glob('*/*.jsonl'):
 with f.open() as h:
  first=json.loads(next(h))
 m=first.get('payload',{})
 if m.get('parent_thread_id')!=parent and m.get('id')!=parent:continue
 prompts=[];taskmessages=[];toolproof=[]
 for n,l in enumerate(f.open(),1):
  j=json.loads(l)
  if j['type']=='response_item':
   p=j.get('payload',{})
   if p.get('role')=='user':prompts.append({'line':n,'record':j})
   if p.get('type')=='agent_message':taskmessages.append({'line':n,'record':j})
   if 'output' in p or p.get('type','').endswith('tool_call') or p.get('type','').endswith('tool_call_output') or p.get('type') in ['function_call','function_call_output','custom_tool_call','custom_tool_call_output']:
    toolproof.append({'line':n,'record':j})
 path=m.get('agent_path','/root').split('/')[-1];record=minimal_metadata(f)
 write_metadata(out/f'{path}-metadata.json',record)
 (out/f'{path}-prompts.json').write_text(json.dumps(prompts,indent=2)+'\n')
 (out/f'{path}-task-messages.json').write_text(json.dumps({'note':'Agent task text is encrypted by the application in local session records. Exact submitted prompt text is preserved separately in the iteration prompt files; these records preserve task sender/recipient and opaque runtime delivery evidence.','records':taskmessages},indent=2)+'\n')
 (out/f'{path}-tool-transcript.json').write_text(json.dumps(toolproof,indent=2)+'\n')
 found.append({'agent':record['agent'],'thread_id':m['id'],'settings':record['confirmed_settings'],'metadata':str(out/f'{path}-metadata.json'),'prompt_proof':str(out/f'{path}-prompts.json'),'input_delivery_proof':str(out/f'{path}-tool-transcript.json')})
(B/'model-provenance.json').write_text(json.dumps(found,indent=2)+'\n')
print(json.dumps([{'agent':x['agent'],'settings':x['settings']} for x in found]))
