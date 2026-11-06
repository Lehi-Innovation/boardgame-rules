from pathlib import Path
import json,hashlib
q=Path(__file__).resolve().parent
reports=[]
for m in json.loads((q/'model-provenance.json').read_text()):
 name=m['agent_path'].split('/')[-1]
 is_coverage=name.startswith('coverage_final_independent_v') and int(name.rsplit('v',1)[1])>=14
 is_auditor=name.startswith('final_source_audit') and int(name[len('final_source_audit'):])>=12
 if not (is_coverage or is_auditor):continue
 calls={};evidence=[]
 for line in Path(m['session_path']).open():
  p=json.loads(line).get('payload',{});typ=p.get('type')
  if typ in ['custom_tool_call','function_call']:calls[p.get('call_id',p.get('id'))]=str(p.get('input',p.get('arguments','')))
  elif typ in ['custom_tool_call_output','function_call_output']:
   code=calls.get(p.get('call_id'),'');out=p.get('output',[])
   if 'view_image' in code and 'shaddam-original-2023-leader.png' in code:
    imgs=[x for x in out if isinstance(x,dict) and x.get('type') in ['input_image','image']] if isinstance(out,list) else []
    evidence.append({'call_id':p.get('call_id'),'input':code,'returned_image_count':len(imgs),'image_payloads_sha256':[hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest() for x in imgs]})
 report={'agent':m['agent_path'],'session':m['session_path'],'original_leader_image_returned_to_agent':any(x['returned_image_count']>0 for x in evidence),'evidence':evidence,'method':'Actual runtime view_image invocation naming original Leader image followed by successful model-visible image content. Image payload digests retained without duplicating base64.'}
 if is_coverage:dest=q/('benchmark-v'+name.rsplit('v',1)[1])
 else:dest=q/('expanded-iteration-'+name[len('final_source_audit'):])
 (dest/'primary-image-read-integrity.json').write_text(json.dumps(report,indent=2)+'\n');reports.append(report)
(q/'primary-image-read-integrity.json').write_text(json.dumps(reports,indent=2)+'\n')
print([{x['agent']:x['original_leader_image_returned_to_agent']} for x in reports])
