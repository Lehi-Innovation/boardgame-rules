from pathlib import Path
import sys,json,hashlib
P=Path(__file__).resolve().parent;I=P/sys.argv[1];n=I.name.rsplit('-',1)[-1];A=sys.argv[2]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
readers=[x for x in read(P/'actual-input-delivery-validation.json')['readers'] if x['iteration']==I.name]
graders=read(I/'grading/actual-input-delivery-validation.json')['graders'];reviewers=read(P/'actual-reviewer-input-delivery-validation.json')['reviewers']
jobs=[]
for x in readers:jobs.append((x['task'],x['runtime_source_path'],I/f"reader-{x['reader']}.json",x['receipts']))
for x in graders:
 b=int(x['task'].rsplit('block',1)[-1]);jobs.append((x['task'],x['runtime_source_path'],I/'grading'/f'block-{b:02d}-grades.json',x['verified_inputs']))
for task in ['/root/current_source_audit_'+A,'/root/current_v9_final_challenge']:
 x=next(x for x in reviewers if x['task']==task);jobs.append((task,x['runtime_source_path'],Path(x['report']),x['verified_text_inputs']))
assert len(jobs)==8
results=[]
for task,runtime,target,inputs in jobs:
 writes=[];visual_outputs=[]
 for ordinal,line in enumerate(Path(runtime).open()):
  d=json.loads(line);v=d.get('payload',{})
  if d.get('type')!='response_item':continue
  typ=v.get('type')
  if typ in ['custom_tool_call','function_call']:
   code=v.get('input',v.get('arguments',''));code=code if isinstance(code,str) else json.dumps(code)
   if target.name in code and any(token in code for token in ['write_text','write_bytes','json.dump','*** Add File','*** Update File']):writes.append({'ordinal':ordinal,'record_sha256':hashlib.sha256(line.encode()).hexdigest(),'tool':v.get('name')})
  if typ=='custom_tool_call_output' and ('data:image/' in line or '"type": "image"' in line or '"type":"image"' in line):visual_outputs.append(ordinal)
 assert writes,('No direct final-output write call identified; inspect original runtime rather than infer',task,str(target))
 first=min(x['ordinal'] for x in writes);verified=[]
 for r in inputs:
  assert sha(Path(r['path']))==r['sha256'];chunks=[]
  for s in r['slices']:
   before=[o for o in s['runtime_output_record_ordinals'] if o<first];assert before,(task,r['path'],s['start'],s['end'],first)
   chunks.append({'start':s['start'],'end':s['end'],'actual_delivery_records_before_first_write':before})
  verified.append({'path':r['path'],'sha256':r['sha256'],'all_original_text_delivered_before_first_target_write':True,'slices':chunks})
 results.append({'task':task,'runtime_source_path':runtime,'target':str(target),'first_target_write':next(x for x in writes if x['ordinal']==first),'complete_text_inputs_before_first_target_write':True,'verified_inputs':verified,'native_image_output_records_before_target_write':[o for o in visual_outputs if o<first],'native_scope_coverage_authority':'Source report original-image/cell and PDF receipts; output-event count alone is not a card-cell audit.'})
(I/'prewrite-input-delivery-validation.json').write_text(json.dumps({'method':'Independently compare original model-visible delivery record ordinals for every complete declared input slice with the earliest direct tool call writing the assigned factual output. Each slice has actual exact delivery before that first write. All original raw files retained; no inferred sequence from intent. Native coverage is separately reported by source auditor.','actor_count':8,'all_complete_text_inputs_before_first_target_write':True,'actors':results},indent=2)+'\n')
print('All8 final actors: complete original text inputs delivered before first assigned factual-output write.')
