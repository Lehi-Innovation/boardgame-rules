import sys
sys.dont_write_bytecode=True
import pathlib,json,hashlib,datetime
P=pathlib.Path(__file__).parent;I=P.parent;role=sys.argv[1];O=P/sys.argv[2];assert role in 'ab';O.mkdir(exist_ok=False)
H=lambda b:hashlib.sha256(b).hexdigest()
old=json.loads((P/'prefix-freeze-manifest.json').read_text())
rt=old['readers'][role]['runtime_path'];fs={}
for kind in ['draft','self-check','final']:
 name=f'reader-{role}.json'if kind=='final'else f'reader-{role}-{kind}.json'
 if not(I/name).exists():fs[kind]={'original_path':str(I/name),'exists':False};continue
 raw=(I/name).read_bytes();(O/('prefix-'+name)).write_bytes(raw);x=json.loads(raw);fs[kind]={'original_path':str(I/name),'bytes':len(raw),'sha256':H(raw),'answer_count':len(x['answers'])if'answers'in x else None,'top_keys':list(x)}
raw=pathlib.Path(rt).read_bytes();raw=raw[:raw.rfind(b'\n')+1];records=[];calls=[];outputs=[];meta=[];events=[]
for physical,line in enumerate(raw.splitlines(keepends=True),1):
 r=json.loads(line);p=r.get('payload',{});records.append({'physical_record':physical,'original_ordinal':r.get('ordinal'),'bytes':len(line),'sha256':H(line),'type':r['type'],'payload_type':p.get('type')})
 if r['type']=='session_meta':meta.append({'physical_record':physical,**{k:p[k]for k in ['agent_path','parent_thread_id','model_provider']if k in p}})
 elif r['type']=='turn_context':meta.append({'physical_record':physical,**{k:p[k]for k in ['model','effort']if k in p}})
 elif p.get('type')=='custom_tool_call':calls.append({'physical_record':physical,'call_id':p.get('call_id'),'name':p.get('name'),'input':p.get('input')})
 elif p.get('type')=='custom_tool_call_output':
  z=p.get('output');outputs.append({'physical_record':physical,'call_id':p.get('call_id'),'visible_text_blocks':[q.get('text','')for q in z if isinstance(q,dict)and q.get('type')in ['input_text','text']]if isinstance(z,list)else[z]if isinstance(z,str)else[]})
 elif p.get('type')in ['task_started','task_complete']:events.append({'physical_record':physical,'event':p['type']})
projection={'original_runtime_path':rt,'prefix_bytes':len(raw),'prefix_sha256':H(raw),'records':records,'actual_metadata':meta,'task_events':events,'tool_calls':calls,'tool_outputs':outputs}
(O/f'prefix-reader-{role}-runtime-projection.json').write_text(json.dumps(projection,ensure_ascii=False,indent=2)+'\n')
manifest={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':old['inputs'],'readers':{role:{'runtime_path':rt,'prefix_bytes':len(raw),'prefix_sha256':H(raw),'records':len(records),'files':fs,'last_event':events[-1]}}}
(O/'prefix-freeze-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
source=(P/'prefix-supplement-02/audit-supplement.py').read_text().replace("for role in 'ab':",f"for role in '{role}':").replace("for r in 'ab'",f"for r in '{role}'")
source=source.replace('Incomplete frozen answer bank, absent frozen final file; partial normal turn completion is not full-task completion.','Terminal candidate: final admission is assessed separately after manual review and root terminal confirmation.')
(O/'audit-complete-trace.py').write_text(source)
print(json.dumps(manifest,indent=2))
