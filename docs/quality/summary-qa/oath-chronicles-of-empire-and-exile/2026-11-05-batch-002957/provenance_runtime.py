"""Minimal, hash-linked actual-runtime metadata; never persist full runtime payloads."""
from pathlib import Path
import hashlib,json
ROOT_THREAD='01a1aad5-d462-7b90-9cb0-ed14a110aee7'
SESSION_DIR=Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05')
def digest(b):return hashlib.sha256(b).hexdigest()
def canonical_hash(x):return digest(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
_CACHE={}
_PARENT_PATH=None
def reference(path,ordinal,row,line):
 return {'runtime_path':str(path),'runtime_line_ordinal':ordinal,'runtime_event_ordinal':row.get('ordinal',ordinal),'runtime_record_sha256':digest(line),'runtime_record_type':row.get('type'),'timestamp':row.get('timestamp')}
def project(path,ordinal,row,line):
 p=row.get('payload',{});kind=row.get('type');fields={}
 if kind=='session_meta':
  fields={k:p[k] for k in ['id','session_id','parent_thread_id','agent_path','model_provider','timestamp','history_mode'] if k in p}
  src=p.get('source',{});sp=src.get('subagent',{}).get('thread_spawn',{}) if isinstance(src,dict) else {}
  if sp:fields['fork_context']={k:sp[k] for k in ['parent_thread_id','depth','agent_path','agent_role'] if k in sp}
 elif kind=='turn_context':fields={k:p[k] for k in ['turn_id','root_turn_id','model','effort'] if k in p}
 else:
  fields={k:p[k] for k in ['id','type','role','turn_id'] if k in p}
  md=p.get('internal_chat_message_metadata_passthrough',{})
  if md.get('turn_id'):fields['turn_id']=md['turn_id']
 return {'source_record':reference(path,ordinal,row,line),'fields':fields}
def load(path):
 path=Path(path)
 if str(path) in _CACHE:return _CACHE[str(path)]
 lookup={};views={};meta=None;contexts=[];spawns={}
 with path.open('rb') as h:
  for n,line in enumerate(h):
   row=json.loads(line);p=row.get('payload',{});kind=row.get('type')
   selected=kind in ['session_meta','turn_context'] or (kind=='response_item' and p.get('type')=='message' and p.get('role')=='user')
   if selected:
    pr=project(path,n,row,line);lookup[canonical_hash(row)]=pr;lookup[canonical_hash(p)]=pr;views[canonical_hash(row)]=(pr,'whole');views[canonical_hash(p)]=(pr,'payload')
    if kind=='session_meta':meta=pr
    elif kind=='turn_context':contexts.append(pr)
   if kind=='response_item' and p.get('type')=='function_call' and p.get('name','').endswith('spawn_agent'):
    a=p.get('arguments',{});a=json.loads(a) if isinstance(a,str) else a
    if isinstance(a,dict) and a.get('task_name'):
     spawns.setdefault(a['task_name'],[]).append({'source_record':reference(path,n,row,line),'fields':{k:a[k] for k in ['task_name','fork_turns','model','reasoning_effort'] if k in a}})
 assert meta,(str(path),'missing metadata')
 result={'meta':meta,'contexts':contexts,'lookup':lookup,'views':views,'spawns':spawns};_CACHE[str(path)]=result;return result
def parent_path():
 global _PARENT_PATH
 if _PARENT_PATH is not None:return _PARENT_PATH
 found=[]
 for path in SESSION_DIR.glob('*.jsonl'):
  with path.open('rb') as h:m=json.loads(h.readline()).get('payload',{})
  if m.get('id')==ROOT_THREAD:found.append(path)
 assert len(found)==1,len(found)
 _PARENT_PATH=found[0]
 return _PARENT_PATH
def minimal_record(path,meta=None,contexts=None):
 data=load(path);meta=meta or data['meta'];contexts=data['contexts'] if contexts is None else contexts;mf=meta['fields'];sp=mf.get('fork_context',{});agent=mf.get('agent_path',sp.get('agent_path','/root'));model=list(dict.fromkeys(c['fields'].get('model') for c in contexts));effort=list(dict.fromkeys(c['fields'].get('effort') for c in contexts));out={'schema':'minimal-runtime-provenance-v1','agent_path':agent,'session_path':str(path),'session_id':mf.get('id',mf.get('session_id')),'parent_thread_id':mf.get('parent_thread_id'),'model_confirmed':bool(contexts),'models':model,'efforts':effort,'runtime_records':[meta]+contexts}
 if agent!='/root':
  matches=load(parent_path())['spawns'].get(agent.rsplit('/',1)[-1],[])
  if len(matches)==1:out['actual_spawn_request']=matches[0]
  else:out['spawn_request_lookup']={'matches':len(matches),'limits':'No unverified fork-context claim.'}
 return out
def captured_record(old):
 path=old['session_path'];data=load(path)
 def locate(row):
  key=canonical_hash(row);assert key in data['lookup'],(path,'captured record not identical to external original')
  return data['lookup'][key]
 meta=locate(old['session_meta']) if 'session_meta' in old else data['meta'];turns=old.get('turn_contexts',old.get('actual_turn_contexts',old.get('actual_runtime_contexts',[])));contexts=[locate(c) for c in turns];out=minimal_record(path,meta,contexts)
 if 'models' in old:assert out['models']==old['models'],(path,'model projection mismatch')
 if 'efforts' in old:assert out['efforts']==old['efforts'],(path,'effort projection mismatch')
 if old.get('agent_path'):assert out['agent_path']==old['agent_path']
 return out
def validate_record(pr):
 ref=pr['source_record'];path=Path(ref['runtime_path'])
 with path.open('rb') as h:
  for n,line in enumerate(h):
   if n==ref['runtime_line_ordinal']:break
  else:raise AssertionError('runtime ordinal missing')
 assert digest(line)==ref['runtime_record_sha256'],(str(path),n,'record hash')
 row=json.loads(line);p=row.get('payload',{})
 if 'task_name' in pr['fields']:
  a=p.get('arguments',{});a=json.loads(a) if isinstance(a,str) else a;expected={k:a[k] for k in ['task_name','fork_turns','model','reasoning_effort'] if k in a}
  assert expected==pr['fields']
 else:assert project(path,n,row,line)==pr
 return True
