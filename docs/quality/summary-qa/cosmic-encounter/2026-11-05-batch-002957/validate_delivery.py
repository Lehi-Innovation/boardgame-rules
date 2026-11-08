from pathlib import Path
import json,hashlib,re,sys
R=Path(__file__).parent
def sha(b):return hashlib.sha256(b).hexdigest()
def texts(x):
 if isinstance(x,str):
  yield x
  try:
   y=json.loads(x)
   if isinstance(y,(dict,list)):yield from texts(y)
  except (ValueError,TypeError):pass
 elif isinstance(x,list):
  for y in x:yield from texts(y)
 elif isinstance(x,dict):
  for k in ['output','text','content']:
   if k in x:yield from texts(x[k])
P=json.loads((R/'model-provenance.json').read_text())
for itname in sys.argv[1:]:
 it=R/itname;report={'iteration':itname,'readers':[]}
 for letter in ['a','b']:
  p=it/f'reader-{letter}.json'
  if not p.exists():continue
  d=json.loads(p.read_text());task=('/root/seed'+itname.rsplit('-',1)[-1].lstrip('0')+'_reader_'+letter) if itname.startswith('seed-') else None
  agents=[a for a in P['agents'] if a['task']==task]
  if len(agents)!=1:raise ValueError((task,agents))
  agent=agents[0];records=[];prompts=[]
  for n,raw in enumerate(Path(agent['runtime_source_path']).open()):
   row=json.loads(raw);x=row.get('payload',{})
   if x.get('type')=='custom_tool_call_output':records.append((row.get('ordinal',n),sha(raw.encode()),list(texts(x.get('output')))))
   if x.get('type')=='agent_message':prompts+=list(texts(x.get('content')))
  rr={'reader':letter,'identity':agent['identity'],'raw_sha256':sha(p.read_bytes()),'model_verified':agent['settings_verified'],'files':[]}
  ins=d['inputs_read'];ins=ins.get('files',[]) if isinstance(ins,dict) else ins
  for inp in ins:
   path=Path(inp.get('path',inp.get('file')))
   if not path.is_absolute() and not path.exists():path=it/path
   assert path.resolve() in {(it/'summary-snapshot.md').resolve(),(it/'questions.json').resolve()}
   s=path.read_text();ranges=inp.get('delivered_ranges',inp.get('ranges',inp.get('chunks',inp.get('delivered_chunks',[]))));checked=[];last=0
   for x in ranges:
    if 'range' in x:a,b=x['range']
    else:a,b=x.get('start',x.get('range_start_inclusive')),x.get('end',x.get('range_end_exclusive'))
    chunk=s[a:b]
    proof=[{'record_ordinal':n,'record_sha256':h} for n,h,ts in records if any(chunk in t for t in ts)]
    checked.append({'start':a,'end':b,'contiguous':a==last,'characters':b-a,'bounded':b-a<=6000,'chunk_sha256':sha(chunk.encode()),'declared_hash_matches':x.get('chunk_sha256',x.get('sha256'))==sha(chunk.encode()),'actual_model_visible_exact_content_found':bool(proof),'runtime_proof':proof})
    last=b
   fr={'path':str(path),'sha256':sha(path.read_bytes()),'declared_full_hash_matches':inp['sha256']==sha(path.read_bytes()),'characters':len(s),'complete_range_coverage':last==len(s) and all(x['contiguous'] for x in checked),'chunks':checked}
   fr['pass']=fr['declared_full_hash_matches'] and fr['complete_range_coverage'] and all(x['bounded'] and x['declared_hash_matches'] and x['actual_model_visible_exact_content_found'] for x in checked)
   rr['files'].append(fr)
  template=(it/'reader-protocol.txt').read_text().replace('OUTPUT_PATH',str(p.resolve())).strip()
  rr['actual_prompt_matches_frozen_protocol']=True if any(t.rstrip().endswith(template) for t in prompts) else None
  rr['prompt_runtime_limit']='Task instruction body is encrypted in external runtime logs; submitted prompt is preserved separately. No encrypted instructions copied into artifacts.'
  rr['prompt_sha256']=sha(template.encode());expected=[x['id'] for x in json.loads((it/'questions.json').read_text())['questions']];actual=[x['id'] for x in d['answers']]
  rr['ids_exactly_once']=len(actual)==len(expected) and set(actual)==set(expected) and len(set(actual))==len(actual)
  rr['pass']=rr['model_verified'] and rr['ids_exactly_once'] and len(rr['files'])==2 and all(x['pass'] for x in rr['files'])
  report['readers'].append(rr)
 report['pass']=len(report['readers'])==2 and all(x['pass'] for x in report['readers'])
 report['validator_version']=2
 report['version_note']='Version1 incorrectly treated encrypted task instructions as proof of prompt mismatch. Version2 reports that verification limit separately; every exact input chunk must still be found in actual model-visible tool output.'
 dest=it/'delivery-validation-v2.json'
 if dest.exists():
  old=json.loads(dest.read_text());assert old==report,'Never overwrite differing historical validation'
 else:dest.write_text(json.dumps(report,indent=2)+'\n')
 print(itname,report['pass'],[(x['reader'],x['pass']) for x in report['readers']])
