from build_evidence import *
PARENT='01a1aa9d-614e-7493-a3f2-715a8c52e03d'
records=[]
for p in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*.jsonl'):
 try:
  with p.open() as f:
   first=json.loads(next(f));m=first.get('payload',{})
   if m.get('id')!=PARENT and m.get('parent_thread_id')!=PARENT:continue
   context=None
   for l in f:
    d=json.loads(l)
    if d['type']=='turn_context':context=d;break
   if not context:continue
   records.append({'runtime_path':str(p),'session_id':m['id'],'agent_path':m.get('agent_path','/root'),'session_meta_evidence':{'timestamp':first['timestamp'],'ordinal':first.get('ordinal'),'type':first['type'],'payload':{k:m.get(k) for k in ['id','parent_thread_id','source','agent_path','thread_source','model_provider']}},'turn_context_evidence':{'timestamp':context['timestamp'],'ordinal':context.get('ordinal'),'type':context['type'],'payload':{k:context['payload'].get(k) for k in ['turn_id','model','effort','cwd']}},'actual_model':context['payload'].get('model'),'actual_effort':context['payload'].get('effort')})
 except (StopIteration,ValueError):pass
save(R/'runtime-model-provenance.json',{'records':records,'method':'Read actual session_meta and first turn_context from runtime JSONL; retain bounded non-sensitive excerpts. Context isolation via fork_turns none, two input file instruction; no stronger filesystem jail claimed.'})
import re
iterations=[]
for directory in sorted(R.glob('*-iteration-*')):
 match=re.fullmatch(r'(seed|expanded)-iteration-(\d+)',directory.name)
 if match:
  kind,num=match.group(1),int(match.group(2));prefix='seed_reader_' if kind=='seed' and num==1 else kind+str(num)+'_reader_';iterations.append((directory.name,prefix))
for it,prefix in iterations:
 if (R/it).exists():
  rs=[r for r in records if r['agent_path'].startswith('/root/'+prefix)]
  save(R/it/'model-provenance.json',{'requested_model':'gpt-6-luna','requested_effort':'high','readers':rs,'actual_settings_confirmed':len(rs)==2 and all(r['actual_model']=='gpt-6-luna' and r['actual_effort']=='high' for r in rs)})
