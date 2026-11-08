from pathlib import Path
import json,hashlib,re,sys
B=Path(__file__).parent
ROOT='01a1b3fc-466c-7322-8413-9e59ff041286'
LOGS=Path('/mnt/c/Users/jonny/.codex/sessions')
rootlog=next(LOGS.rglob('*'+ROOT+'.jsonl'))
def digest(raw):return hashlib.sha256(raw).hexdigest()
requested={}
for ordinal,line in enumerate(rootlog.open(),1):
 r=json.loads(line);v=r.get('payload',{})
 if r['type']=='response_item' and v.get('name')=='spawn_agent':
  x=json.loads(v['arguments']);requested['/root/'+x['task_name']]={'requested_model':x['model'],'requested_effort':x['reasoning_effort'],'fork_turns':x['fork_turns'],'request_log_path':str(rootlog),'request_record_ordinal':ordinal,'request_record_sha256':digest(line.encode())}
meta=[];tasklogs={}
for p in LOGS.rglob('*.jsonl'):
 m={};task=None;turn=None
 for ordinal,line in enumerate(p.open(),1):
  r=json.loads(line);v=r.get('payload',{})
  if ordinal==1:
   if v.get('parent_thread_id')!=ROOT:break
   m={'id':v.get('id'),'parent_thread_id':v.get('parent_thread_id'),'timestamp':v.get('timestamp'),'runtime_log_path':str(p),'identity_record_ordinal':ordinal,'identity_record_sha256':digest(line.encode())}
  if r['type']=='turn_context' and turn is None:turn={'actual_model':v.get('model'),'actual_effort':v.get('effort'),'settings_record_ordinal':ordinal,'settings_record_sha256':digest(line.encode())}
  if r['type']=='response_item' and v.get('type')=='agent_message':task=v.get('recipient')
  if task and turn:break
 if task and turn:
  item={**m,**requested[task],**turn,'task':task};item['model_effort_verified']=item['requested_model']==item['actual_model'] and item['requested_effort']==item['actual_effort'];assert item['model_effort_verified'];meta.append(item);tasklogs[task]=p
(B/'runtime-provenance.json').write_text(json.dumps(meta,indent=2)+'\n')

def strings(x):
 if isinstance(x,str):
  yield x
  if x[:1] in ['{','[']:
   try:yield from strings(json.loads(x))
   except (ValueError,TypeError):pass
 elif isinstance(x,list):
  for y in x:yield from strings(y)
 elif isinstance(x,dict):
  for k,y in x.items():
   if k not in ['encrypted_content','internal_chat_message_metadata_passthrough']:yield from strings(y)

def check(iteration,taskprefix):
 I=B/iteration;manifest=json.loads((I/'input-manifest.json').read_text());reports={}
 paths=json.loads((I/'reader-output-manifest.json').read_text()) if (I/'reader-output-manifest.json').exists() else {}
 for letter in ['a','b']:
  task='/root/'+taskprefix+letter;output=Path(paths.get(letter,I/f'reader-{letter}.json'));assert output.resolve().is_relative_to(I.resolve())
  if not output.exists():continue
  p=tasklogs[task]
  reader=json.loads(output.read_text());receipts=[]
  outputs=[]
  for ordinal,line in enumerate(p.open(),1):
   r=json.loads(line);v=r.get('payload',{})
   if r['type']=='response_item' and v.get('type')=='custom_tool_call_output':outputs.append((ordinal,digest(line.encode()),list(strings(v.get('output')))))
  inputs=reader['inputs_read']
  if isinstance(inputs,dict):
   if 'range_receipts' in inputs:
    flat=inputs['range_receipts']
    inputs=[{**receipt,'ranges':[r for r in flat if r['path']==receipt['path']]} for name,receipt in inputs.items() if name!='range_receipts']
   else:inputs=inputs['files'] if 'files' in inputs else [{'file':name,**receipt} for name,receipt in inputs.items()]
  for inp in inputs:
   path=inp.get('file',inp.get('filename',inp.get('path')))
   path=Path(path)
   if not path.is_absolute():path=path.resolve() if path.exists() else I/path
   raw=path.read_bytes();source=raw.decode();ranges=inp.get('ranges',inp.get('chunks'));assert ranges,'Missing actual range receipts';normal=[]
   for x in ranges:
    if isinstance(x,list):start,end=x
    else:start,end=x['start'],x['end']
    normal.append((start,end))
   total=inp.get('total_characters',inp.get('total_chars',inp.get('total',inp.get('characters'))))
   mode='characters' if total==len(source) else 'bytes' if total==len(raw) else 'unknown'
   if mode=='unknown' and normal[-1][1]==len(source):mode='characters';total=len(source)
   hits=[]
   for start,end in normal:
    wanted=source[start:end] if mode=='characters' else raw[start:end].decode() if mode=='bytes' else ''
    found=[{'record_ordinal':ordinal,'record_sha256':h} for ordinal,h,items in outputs if wanted and any(wanted in s for s in items)]
    hits.append({'start':start,'end':end,'actual_exact_model_visible_matches':found,'range_sha256':digest(wanted.encode()),'chars':len(wanted),'within_5500_characters':len(wanted)<=5500,'within_6000_characters':len(wanted)<=6000})
   receipts.append({'path':str(path.resolve()),'source_sha256':digest(raw),'range_mode':mode,'ranges':hits,'complete':normal[0][0]==0 and normal[-1][1]==total and all(x[1]==y[0] for x,y in zip(normal,normal[1:])) and all(x['actual_exact_model_visible_matches'] for x in hits),'log_path':str(p)})
  reports[letter]={'input_receipts':receipts,'all_input_data_verified_complete':len(receipts)==2 and all(x['complete'] for x in receipts),'all_ranges_at_most5500_characters':all(r['within_5500_characters'] for x in receipts for r in x['ranges']),'model_provenance':next(x for x in meta if x['task']==task),'raw_output_path':str(output.resolve()),'raw_output_sha256':digest(output.read_bytes()),'expected_ids':len(json.loads((I/'questions.json').read_text())['questions']),'actual_ids':[a['id'] for a in reader['answers']]}
 (I/'actual-delivery-verification.json').write_text(json.dumps(reports,indent=2)+'\n');(I/'model-provenance.json').write_text(json.dumps([x for x in meta if x['task'].startswith('/root/'+taskprefix)],indent=2)+'\n')
 print(iteration,{k:v['all_input_data_verified_complete'] for k,v in reports.items()})
for iteration,prefix in [('seed-luna-iteration-01','seed_reader_'),('seed-luna-iteration-02','seed2_reader_'),('seed-luna-iteration-03','seed3_reader_'),('seed-luna-iteration-04','seed4_reader_'),('expanded-luna-iteration-01','expanded1_reader_'),('expanded-luna-iteration-02','expanded2_reader_'),('expanded-luna-iteration-03','expanded3_reader_'),('expanded-luna-iteration-04','expanded4_reader_')]:
 if not (B/iteration).exists():continue
 check(iteration,prefix)
print('Verified actual models/efforts for',len(meta),'agents.')
