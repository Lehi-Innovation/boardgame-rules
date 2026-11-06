"""Bind individually named native-view receipts to original model-visible image outputs."""
from pathlib import Path
import json,hashlib,sys,re
from verify_runtime_delivery import log_for
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
audit_name,task=sys.argv[1:];d=ROOT/audit_name;report=d/'source-audit.json';x=json.loads(report.read_text());receipts=x['native_view_receipts'];calls={};outs=[];writes=[];log=log_for(task)
for n,line in enumerate(log.open(),1):
 rec=json.loads(line);p=rec.get('payload',{});typ=p.get('type');rh=sha(line.encode())
 if typ in ['custom_tool_call','function_call']:
  src=p.get('input',p.get('arguments',''));calls[p.get('call_id')]={'ordinal':n,'source':src,'record_sha256':rh}
  if 'source-audit.json' in src and ('write_text' in src or 'writeFile' in src):writes.append(n)
 if typ in ['custom_tool_call_output','function_call_output'] and isinstance(p.get('output'),list):
  count=sum(isinstance(v,dict) and v.get('type')=='input_image' for v in p['output'])
  if count:outs.append({'ordinal':n,'record_sha256':rh,'call_id':p.get('call_id'),'native_image_count':count})
assert writes;cut=min(writes);bindings=[];used={}
for r in receipts:
 path=Path(r.get('view_path',r['source']));expected=r.get('render_sha256',r.get('sha256'));assert sha(path.read_bytes())==expected
 matches=[]
 for out in outs:
  c=calls[out['call_id']];src=c['source'];match=path.name in src
  if 'pdf_page_1based' in r:
   number=f"{r['pdf_page_1based']:02}";prefix=re.sub(r'\d+\.png$','',str(path));match=prefix in src and json.dumps(number) in src
  if match:
   assert out['ordinal']<cut;matches.append({**out,'call_ordinal':c['ordinal'],'call_record_sha256':c['record_sha256']});used[out['call_id']]=used.get(out['call_id'],0)+1
 assert len(matches)==1,(str(path),'expected exactly one named native output binding',matches)
 bindings.append({'path':str(path),'sha256':expected,'native_output_binding':matches[0]})
assert len(bindings)==sum(o['native_image_count'] for o in outs)
assert all(used.get(o['call_id'])==o['native_image_count'] for o in outs)
out={'validation':'PASS','report_path':str(report),'report_sha256':sha(report.read_bytes()),'runtime_source':str(log),'native_view_count':len(bindings),'native_output_counts_exactly_match_individually_named_views':True,'all_native_views_before_first_report_write_ordinal':cut,'bindings':bindings,'limits':'Actual named view call code, original returned native image blocks and exact source/render bytes checked. PDF loops name each two-digit page explicitly. No general OS isolation claim and no private context/account/instructions copied.'};p=d/'runtime-native-delivery.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(audit_name,len(bindings),'native model-visible views PASS')
