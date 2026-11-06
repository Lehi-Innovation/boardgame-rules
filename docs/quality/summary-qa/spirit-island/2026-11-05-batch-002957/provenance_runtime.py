"""Whitelist-only runtime metadata; original records remain in external logs."""
from pathlib import Path
import hashlib,json
ROOT_THREAD='01a1ac01-c763-7bb1-901e-7458891630b8'
SESSION_DIR=Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05')
def digest(b):return hashlib.sha256(b).hexdigest()
def reference(path,n,row,line):
 return {'runtime_path':str(path),'runtime_line_ordinal':n,'runtime_event_ordinal':row.get('ordinal',n),'runtime_record_sha256':digest(line),'runtime_record_type':row.get('type'),'timestamp':row.get('timestamp')}
def project_record(path,n,row,line):
 p=row.get('payload',{});kind=row.get('type')
 if kind=='session_meta':
  fields={k:p[k] for k in ['id','session_id','parent_thread_id','agent_path','timestamp','history_mode','model_provider'] if k in p}
  source=p.get('source',{});spawn=source.get('subagent',{}).get('thread_spawn',{}) if isinstance(source,dict) else {}
  if spawn:fields['fork_context']={k:spawn[k] for k in ['parent_thread_id','depth','agent_path','agent_nickname','agent_role'] if k in spawn}
 elif kind=='turn_context':fields={k:p[k] for k in ['turn_id','root_turn_id','model','effort'] if k in p}
 else:raise ValueError('Metadata projection only accepts session_meta and turn_context')
 return {'source_record':reference(path,n,row,line),'fields':fields}
_CACHE={}
def load_selected(path):
 path=Path(path)
 if str(path) in _CACHE:return _CACHE[str(path)]
 selected={};spawns={};filehash=hashlib.sha256()
 with path.open('rb') as h:
  for n,line in enumerate(h):
   filehash.update(line);row=json.loads(line);p=row.get('payload',{});kind=row.get('type')
   if kind in ['session_meta','turn_context']:selected[n]={'row':row,'projection':project_record(path,n,row,line)}
   if kind=='response_item' and p.get('type')=='function_call' and p.get('name')=='spawn_agent':
    try:a=json.loads(p.get('arguments','{}'))
    except (ValueError,TypeError):continue
    if isinstance(a,dict) and a.get('task_name'):spawns.setdefault(a['task_name'],[]).append({'source_record':reference(path,n,row,line),'fields':{k:a[k] for k in ['task_name','fork_turns','model','reasoning_effort'] if k in a}})
 data={'selected':selected,'spawns':spawns,'session_sha256':filehash.hexdigest()};_CACHE[str(path)]=data;return data
_PARENT=None
def parent_path():
 global _PARENT
 if _PARENT:return _PARENT
 matches=[]
 for p in SESSION_DIR.glob('*.jsonl'):
  with p.open('rb') as h:m=json.loads(h.readline()).get('payload',{})
  if m.get('id')==ROOT_THREAD:matches.append(p)
 assert len(matches)==1
 _PARENT=matches[0];return _PARENT

def minimal_metadata(path,context_ordinals=None,legacy_capture_sha=None):
 path=Path(path);data=load_selected(path);meta=data['selected'][0]['projection'];mf=meta['fields'];agent=mf.get('agent_path',mf.get('fork_context',{}).get('agent_path','/root'))
 if context_ordinals is None:context_ordinals=[n for n,x in data['selected'].items() if x['row']['type']=='turn_context']
 contexts=[data['selected'][n]['projection'] for n in context_ordinals]
 out={'schema':'minimal-runtime-metadata-v1','agent':agent,'thread_id':mf.get('id',mf.get('session_id')),'parent_thread_id':mf.get('parent_thread_id'),'task_name':agent.rsplit('/',1)[-1],'session_path':str(path),'session_sha256_at_capture':legacy_capture_sha or data['session_sha256'],'session_meta':meta,'turn_contexts':contexts,'confirmed_settings':[{'model':x['fields'].get('model'),'effort':x['fields'].get('effort')} for x in contexts]}
 if agent!='/root':
  requests=load_selected(parent_path())['spawns'].get(agent.rsplit('/',1)[-1],[])
  if len(requests)==1:out['requested_spawn']=requests[0]
  else:out['requested_spawn_lookup']={'matches':len(requests),'limits':'No unverified fork/model request claimed.'}
 return out

def legacy_recipe(old):
 path=Path(old['session_path']);data=load_selected(path);recipe=dict(old)
 assert old.get('source')==data['selected'][0]['row']['payload'].get('source')
 recipe['source']={'$external_runtime_record':data['selected'][0]['projection']['source_record'],'view':['payload','source']}
 ordinals=[];turns=[]
 for item in old['turn_contexts']:
  n=item['line']-1;original=data['selected'][n];assert item['record']==original['row'];ordinals.append(n)
  turns.append({'line':item['line'],'record':{'$external_runtime_record':original['projection']['source_record'],'view':'whole'}})
 recipe['turn_contexts']=turns
 minimal=minimal_metadata(path,ordinals,old['session_sha256_at_capture'])
 assert minimal['agent']==old['agent'] and minimal['thread_id']==old['thread_id'] and minimal['confirmed_settings']==old['confirmed_settings']
 return recipe,minimal

def reconstruct(value):
 if isinstance(value,dict) and '$external_runtime_record' in value:
  ref=value['$external_runtime_record'];path=Path(ref['runtime_path']);n=ref['runtime_line_ordinal'];row=load_selected(path)['selected'][n]['row'];projection=load_selected(path)['selected'][n]['projection'];assert projection['source_record']==ref
  if value['view']=='whole':return row
  result=row
  for key in value['view']:result=result[key]
  return result
 if isinstance(value,dict):return {k:reconstruct(v) for k,v in value.items()}
 if isinstance(value,list):return [reconstruct(v) for v in value]
 return value

def validate_projection(pr):
 ref=pr['source_record'];data=load_selected(ref['runtime_path']);n=ref['runtime_line_ordinal']
 if 'task_name' in pr['fields']:
  return any(x==pr for items in data['spawns'].values() for x in items)
 return data['selected'][n]['projection']==pr
