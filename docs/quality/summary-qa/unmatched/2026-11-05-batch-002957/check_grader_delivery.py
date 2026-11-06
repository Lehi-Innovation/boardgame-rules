from pathlib import Path
import json,hashlib,sys
P=Path(__file__).resolve().parent;I=P/sys.argv[1];prefix=sys.argv[2];prov=json.loads((P/'model-provenance.json').read_text())['agents']
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
  if x.get('type') in ['image','input_image','image_url']:return
  for k,y in x.items():
   if k not in ['data','image_url','encrypted_content']:yield from strings(y)
results=[]
for block in range(1,5):
 task='/root/'+prefix+f'_grader_block{block:02d}';agent=next(x for x in prov if x['task']==task);assert agent['confirmed']
 records=[]
 for ordinal,line in enumerate(Path(agent['runtime_source_path']).open()):
  d=json.loads(line);v=d.get('payload',{})
  if d.get('type')=='response_item' and v.get('type')=='custom_tool_call_output':records.append((ordinal,'\n'.join(strings(v.get('output')))))
 report=I/'grading'/f'block-{block:02d}-grades.json';d=json.loads(report.read_text());r=d['delivery_receipts'];receipts=r.get('files',r.get('inputs',list(r.values()))) if isinstance(r,dict) else r;verified=[]
 for receipt in receipts:
  if not isinstance(receipt,dict) or not (receipt.get('path') or receipt.get('input_path')):continue
  path=Path(receipt.get('path',receipt.get('input_path')));text=path.read_text();length=receipt.get('character_length',receipt.get('char_length'));assert len(text)==length
  sha=hashlib.sha256(path.read_bytes()).hexdigest();assert sha==receipt['sha256'];end0=0;chunks=[]
  for bounds in receipt.get('read_ranges',receipt.get('exact_read_ranges',receipt.get('reads',receipt.get('slices',[])))):
   start,end=(bounds['start'],bounds['end']) if isinstance(bounds,dict) else bounds
   assert start==end0 and 0<end-start<=5000;end0=end
   matches=[ordinal for ordinal,out in records if text[start:end] in out];assert matches,(task,str(path),start,end)
   chunks.append({'start':start,'end':end,'runtime_output_record_ordinals':matches,'exact_expected_text_found':True})
  assert end0==len(text),(task,str(path),end0,len(text));verified.append({'path':str(path),'sha256':sha,'characters':length,'complete_contiguous':True,'slices':chunks})
 assert {Path(x['path']).name for x in verified}=={'summary-snapshot.md',f'block-{block:02d}-inputs.json'}
 results.append({'task':task,'report':str(report.resolve()),'actual_model_confirmed':True,'runtime_source_path':agent['runtime_source_path'],'verified_inputs':verified})
(I/'grading/actual-input-delivery-validation.json').write_text(json.dumps({'method':'Every exact original declared Unicode slice independently located in model-visible runtime outputs, recursively decoding JSON wrappers. Summary and full lossless packs each delivered completely; no compressed/reconstructed reader evidence substituted.','graders':results},indent=2)+'\n')
print('Full actual grader input delivery verified:',[(x['task'],len(x['verified_inputs'])) for x in results])
