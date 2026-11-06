from pathlib import Path
import json,hashlib,sys
from infer_runtime_ranges import infer_exact_slices
P=Path(__file__).resolve().parent
PROV=json.loads((P/'model-provenance.json').read_text())['agents']
def strings(x):
 if isinstance(x,str):
  yield x
  try:
   y=json.loads(x)
   if y!=x:yield from strings(y)
  except (ValueError,RecursionError):pass
 elif isinstance(x,list):
  for y in x:yield from strings(y)
 elif isinstance(x,dict):
  for y in x.values():yield from strings(y)
def normalize(receipts):
 if isinstance(receipts,dict):
  if 'path' in receipts or 'file' in receipts:return [receipts]
  return [dict(x,path=x.get('path',x.get('file',k))) for k,x in receipts.items()]
 return receipts
results=[]
for iteration in sys.argv[1:]:
 I=P/iteration
 for who in ['a','b']:
  f=I/f'reader-{who}.json'
  if not f.exists():continue
  raw=json.loads(f.read_text());task={'seed-iteration-01':'seed','seed-iteration-02':'seed2','seed-iteration-03':'seed3','seed-iteration-04':'seed4'}.get(iteration,iteration.replace('-','_'))+'_reader_'+who
  agents=[x for x in PROV if x['task']=='/root/'+task]
  if not agents:raise ValueError('No provenance '+task)
  agent=agents[0];output_records=[]
  for ordinal,line in enumerate(Path(agent['runtime_source_path']).open()):
   d=json.loads(line);v=d.get('payload',{})
   if d.get('type')=='response_item' and v.get('type')=='custom_tool_call_output':
    alltext='\n'.join(strings(v.get('output')));output_records.append((ordinal,alltext))
  receipts=[]
  receipt_data=raw['delivery_receipt'];nested_instruction=receipt_data.get('instruction_delivery') if isinstance(receipt_data,dict) else None
  if nested_instruction:receipt_data={k:v for k,v in receipt_data.items() if k!='instruction_delivery'}
  data_receipts=normalize(receipt_data)
  for receipt in data_receipts:
   reported=Path(receipt.get('path',receipt.get('file')))
   if not reported.is_absolute():
    resolved=(I/reported).resolve() if len(reported.parts)==1 else (P.parents[4]/reported).resolve()
    assert resolved in [(I/'summary-snapshot.md').resolve(),(I/'questions.json').resolve()],('Unexpected relative input receipt',task,str(reported))
    receipt['reported_path']=str(reported);receipt['path']=str(resolved)
  all_receipts=[dict(r,role='rules_or_test_data') for r in data_receipts]
  instruction=raw.get('instruction_delivery',nested_instruction)
  if instruction:
   assert {Path(r.get('path',r.get('file'))).resolve() for r in data_receipts}=={(I/'summary-snapshot.md').resolve(),(I/'questions.json').resolve()}
   assert Path(instruction['path']).resolve()==(I/f'reader-{who}-prompt.txt').resolve()
   all_receipts.append(dict(instruction,role='generic_instructions_not_rules_data'))
  elif json.loads((I/'input-manifest.json').read_text()).get('protocol_version','').startswith(('v3-','v4-','v5-','v6-','v7-','v8-','v9-','v10-')):
   # A missing optional self-reported instruction receipt is not a factual
   # failure. Independently prove actual complete instruction text delivery.
   instruction_path=I/f'reader-{who}-prompt.txt';instruction_text=instruction_path.read_text();found_ranges=None
   for width in [5000,4500,4000,3500,3000,2500,2000,1500,1000,500]:
    candidate=[[start,min(start+width,len(instruction_text))] for start in range(0,len(instruction_text),width)]
    if all(any(instruction_text[start:end] in out for ordinal,out in output_records) for start,end in candidate):found_ranges=candidate;break
   assert found_ranges,('Cannot independently prove complete instruction delivery',task)
   all_receipts.append({'role':'generic_instructions_not_rules_data','path':str(instruction_path),'sha256':hashlib.sha256(instruction_path.read_bytes()).hexdigest(),'char_length':len(instruction_text),'read_ranges':found_ranges,'receipt_basis':'Independent exact contiguous text matching in actual model-visible runtime, not a reader self-report'})
  for r in all_receipts:
   path=Path(r.get('path',r.get('file')));text=path.read_text();ranges=r.get('read_ranges',r.get('all_actually_read_ranges',r.get('all_read_ranges',r.get('ranges'))));prior=0;verified=[]
   assert r['sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
   assert r.get('char_length',r.get('character_length'))==len(text)
   declared_ranges=ranges
   declared_match=all(any(text[(b['start'] if isinstance(b,dict) else b[0]):(b['end'] if isinstance(b,dict) else b[1])] in out for ordinal,out in output_records) for b in ranges)
   inferred=None
   if not declared_match:
    inferred=infer_exact_slices(agent['runtime_source_path'],path)
    assert inferred,('Neither declared nor independently inferred complete actual input delivery',task,str(path))
    ranges=[[b['start'],b['end']] for b in inferred['slices']]
    r['receipt_basis']='Independent literal runtime slice reconstruction; original declared boundaries differ but complete original text is actually present'
   for bounds in ranges:
    start,end=(bounds['start'],bounds['end']) if isinstance(bounds,dict) else bounds
    assert 0<=start<=prior and start<end<=len(text)
    reread=start<prior
    prior=max(prior,end)
    matches=[ordinal for ordinal,out in output_records if text[start:end] in out]
    assert matches,(task,path,start,end)
    verified.append({'start':start,'end':end,'characters':end-start,'runtime_output_record_ordinals':matches,'exact_expected_slice_found':True,'technical_reread':reread})
   assert prior==len(text)
   receipts.append({'role':r['role'],'receipt_basis':r.get('receipt_basis','Reader-declared ranges independently verified against original runtime'),'path':str(path),'sha256':r['sha256'],'char_length':len(text),'slices':verified,'complete_contiguous':True,'largest_recorded_slice':max(x['characters'] for x in verified),'original_declared_read_ranges':declared_ranges,'actual_range_reconstruction':inferred})
  results.append({'iteration':iteration,'reader':who,'task':agent['task'],'model_confirmed':agent['confirmed'],'runtime_source_path':agent['runtime_source_path'],'receipts':receipts})
(P/'actual-input-delivery-validation.json').write_text(json.dumps({'method':'Independently locate every exact declared character slice in model-visible original runtime tool outputs (recursively decode JSON wrappers); check receipt hashes/lengths and contiguous complete range coverage. Runtime paths/ordinals identify authority without copying internal metadata.','readers':results},indent=2)+'\n')
print([(x['iteration'],x['reader'],[(r['char_length'],r['largest_recorded_slice']) for r in x['receipts']]) for x in results])
