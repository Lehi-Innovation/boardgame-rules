from pathlib import Path
import sys,json,hashlib
from infer_runtime_ranges import infer_exact_slices
P=Path(__file__).resolve().parent;I=P/sys.argv[1];prov=json.loads((P/'model-provenance.json').read_text())['agents']
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
result=[]
for r in ['a','b']:
 task='/root/'+I.name.replace('-','_')+'_reader_'+r;a=next(x for x in prov if x['task']==task);records=[]
 for ordinal,line in enumerate(Path(a['runtime_source_path']).open()):
  d=json.loads(line);v=d.get('payload',{})
  if d.get('type')=='response_item' and v.get('type')=='custom_tool_call_output':
   records.append((ordinal,[s for s in strings(v.get('output')) if len(s)<=6000]))
 files=[]
 for name in ['summary-snapshot.md','questions.json',f'reader-{r}-prompt.txt']:
  f=I/name;t=f.read_text();slices=None
  for width in [5000,4500,4000,3500,3000,2500,2000,1500,1000,500]:
   candidate=[]
   for start in range(0,len(t),width):
    end=min(start+width,len(t));matches=[ordinal for ordinal,leaves in records if any(t[start:end] in leaf for leaf in leaves)]
    if not matches:break
    candidate.append({'start':start,'end':end,'characters':end-start,'runtime_output_record_ordinals':matches,'bounded_original_slice_found':True})
   if candidate and candidate[-1]['end']==len(t):slices=candidate;break
  if not slices:
   inferred=infer_exact_slices(a['runtime_source_path'],f)
   assert inferred,(task,name,'No complete bounded actual delivery found')
   slices=[dict(z,characters=z['end']-z['start'],bounded_original_slice_found=True) for z in inferred['slices']]
  assert slices,(task,name,'No complete bounded grid found')
  files.append({'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'characters':len(t),'slices':slices,'complete_contiguous_bounded_text_delivery':True})
 result.append({'reader':r,'task':task,'runtime_source_path':a['runtime_source_path'],'files':files})
out={'method':'Independently locate complete original logical slices of at most5000 characters in actual model-visible runtime string leaves no longer than6000 characters including transport labels. This rejects proving small slices solely as substrings of an oversized full-file response. Existing original oversized delivery findings remain separately preserved; a subsequent bounded reread may establish this proof.','all_inputs_have_bounded_delivery':True,'readers':result}
(I/'bounded-input-delivery-validation.json').write_text(json.dumps(out,indent=2)+'\n');print('Both readers: all original data/instructions have complete bounded model-visible delivery.')
