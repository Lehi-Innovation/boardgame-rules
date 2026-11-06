import pathlib,json,hashlib,re
P=pathlib.Path(__file__).resolve().parent;parent_id='01a1aae3-a2a3-70f3-80bf-7dc6cc814c6a';S=pathlib.Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05');records={}
for f in S.glob('*.jsonl'):
 if f.stat().st_mtime<1793868420:continue
 meta=None;contexts=[]
 for line in f.open():
  try:r=json.loads(line)
  except:continue
  if r.get('type')=='session_meta':meta=r
  if r.get('type')=='turn_context':contexts.append(r)
  if not meta:continue
 source=meta['payload'].get('source',{});spawn=source.get('subagent',{}).get('thread_spawn',{}) if isinstance(source,dict) else {}
 if spawn.get('parent_thread_id')!=parent_id:continue
 name=spawn['agent_path'].split('/')[-1]
 request_path=P/'dispatched-prompts'/(name+'-request.json')
 request=json.loads(request_path.read_text()) if request_path.exists() else {}
 records[name]={'task_name':spawn['agent_path'],'session_id':meta['payload']['id'],'runtime_path':str(f),'session_meta':{k:meta['payload'][k] for k in ['id','source','agent_nickname'] if k in meta['payload']},'turn_context':[{k:r['payload'].get(k) for k in ['model','effort','cwd']} for r in contexts], 'requested_model':request.get('model','gpt-6-luna' if re.match(r'^(seed|expanded|integration)\d+_[ab]$',name) else 'gpt-6.1-sol'),'requested_effort':request.get('reasoning_effort','high')}
for name,r in records.items():
 r['confirmed']=all(c['model']==r['requested_model'] and c['effort']=='high' for c in r['turn_context'])
(P/'all-model-provenance.json').write_text(json.dumps(records,indent=2)+'\n')
for prefix,d in [('seed01','seed-iteration-01'),('seed02','seed-iteration-02'),('expanded01','expanded-iteration-01'),('expanded02','expanded-iteration-02'),('expanded03','expanded-iteration-03'),('expanded04','expanded-iteration-04'),('expanded05','expanded-iteration-05'),('expanded06','expanded-iteration-06'),('expanded07','expanded-iteration-07'),('expanded08','expanded-iteration-08'),('expanded09','expanded-iteration-09'),('integration01','integration-iteration-01')]:
 if (P/d).exists():
  a={n:r for n,r in records.items() if n.startswith(prefix+'_')};(P/d/'model-provenance.json').write_text(json.dumps(a,indent=2)+'\n')
# Preserve exact dispatched prompts from parent runtime rather than reconstructing them.
for f in S.glob('*'+parent_id+'.jsonl'):
 for line in f.open():
  try:r=json.loads(line)
  except:continue
  d=r.get('payload',{})
  if d.get('type')=='function_call' and d.get('name','').endswith('spawn_agent'):
   try:args=json.loads(d['arguments'])
   except:continue
   name=args['task_name']; out=P/'dispatched-prompts';out.mkdir(exist_ok=True);(out/(name+'.txt')).write_text(args['message']);(out/(name+'-request.json')).write_text(json.dumps({k:v for k,v in args.items() if k!='message'},indent=2))
print({'agents':len(records),'confirmed':sum(r['confirmed'] for r in records.values()),'all_confirmed':all(r['confirmed'] for r in records.values())})
