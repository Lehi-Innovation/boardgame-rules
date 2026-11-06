"""Verify actual review-model identity and exact complete model-visible text delivery."""
from pathlib import Path
import json,sys,hashlib
from verify_runtime_delivery import log_for,strings
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def verify(report_rel,task,output_rel):
 report=ROOT/report_rel;x=json.loads(report.read_text());log=log_for(task);outs=[];identity=None;turns=[];calls=[]
 for n,line in enumerate(log.open(),1):
  rec=json.loads(line);p=rec.get('payload',{});typ=p.get('type');rh=sha(line.encode())
  if rec.get('type')=='session_meta':identity={'id':p.get('id'),'parent':p.get('parent_thread_id'),'task':p.get('agent_path'),'history_mode':p.get('history_mode'),'ordinal':n,'record_sha256':rh}
  if rec.get('type')=='turn_context':turns.append({'ordinal':n,'actual_model':p.get('model'),'actual_effort':p.get('effort'),'record_sha256':rh})
  if typ in ['custom_tool_call_output','function_call_output']:outs.append({'ordinal':n,'record_sha256':rh,'text':list(strings(p.get('output')))})
  if typ in ['function_call','custom_tool_call']:calls.append({'name':p.get('name'),'ordinal':n,'record_sha256':rh})
 assert turns and all(t['actual_model']=='gpt-6.1-sol' and t['actual_effort']=='high' for t in turns)
 checked=[]
 receipts=x.get('delivery_receipts')
 if 'text_read_receipts' in x:
  receipts=[{'file':z['path'],'ranges':z.get('read_ranges_zero_based_half_open_characters',z.get('read_ranges'))} for z in x['text_read_receipts']]
 if receipts is None and 'text_range_receipts' in x:
  receipts=[{'file':z['path'],'ranges':z['ranges']} for z in x['text_range_receipts']]
 if receipts is None and 'receipts' in x and 'text_range_receipts' in x['receipts']:
  receipts=[{'file':z['path'],'ranges':z['ranges']} for z in x['receipts']['text_range_receipts']]
 if receipts is None and 'receipts' in x and 'text_ranges' in x['receipts']:
  receipts=[{'file':z['path'],'ranges':[[t['start'],t['end']] for t in z['slices']]} for z in x['receipts']['text_ranges']]
 if isinstance(receipts,dict):
  candidates=[receipts['input']]+receipts.get('authority_and_provenance_deliveries',[])
  receipts=[{'file':z['path'],'ranges':[[t['start_inclusive'],t['end_exclusive']] for t in z['slices']]} for z in candidates if 'slices' in z]
 for r in receipts:
  p=Path(r['file']);p=p if p.is_absolute() else report.parent/p;s=p.read_text();ranges=r.get('ranges',r.get('contiguous_character_slices'));ranges=[[z.get('start',z.get('start_inclusive')),z.get('end',z.get('end_exclusive'))] if isinstance(z,dict) else z for z in ranges];assert ranges[0][0]==0 and ranges[-1][1]==len(s);units=[]
  for i,(a,b) in enumerate(ranges):
   assert 0<=a<b<=len(s) and b-a<=6000
   if i:assert a==ranges[i-1][1]
   matches=[{k:o[k] for k in ['ordinal','record_sha256']} for o in outs if any(s[a:b] in v for v in o['text'])]
   assert matches,(str(p),a,b,'No exact actual model-visible full slice')
   units.append({'start':a,'end':b,'sha256':sha(s[a:b].encode()),'matching_runtime_outputs':matches})
  checked.append({'file':str(p),'sha256':sha(p.read_bytes()),'characters':len(s),'ranges':units})
 output=ROOT/output_rel;assert not output.exists();output.write_text(json.dumps({'report':str(report),'report_sha256':sha(report.read_bytes()),'runtime_source_path':str(log),'identity':identity,'model_records':turns,'tool_call_name_hash_records':calls,'input_delivery':checked,'validation':'PASS','boundary':'Minimal identity/model/effort and record ordinal/opaque hashes; no private runtime instructions/account/permissions copied. Requested fork verified separately in runtime-provenance.json.'},indent=2)+'\n');print(report_rel,'actual model and exact full delivery PASS')
if __name__=='__main__':verify(*sys.argv[1:])
