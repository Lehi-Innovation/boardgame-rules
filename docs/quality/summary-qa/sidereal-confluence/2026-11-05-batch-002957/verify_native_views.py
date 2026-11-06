"""Bind individually named native-view receipts to original model-visible image outputs."""
from pathlib import Path
import json,hashlib,sys,re
from verify_runtime_delivery import log_for
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
audit_name,task=sys.argv[1:3];report_name=sys.argv[3] if len(sys.argv)>3 else 'source-audit.json';d=ROOT/audit_name;report=d/report_name;x=json.loads(report.read_text());receipts=x['native_view_receipts'];calls={};outs=[];writes=[];log=log_for(task)
for n,line in enumerate(log.open(),1):
 rec=json.loads(line);p=rec.get('payload',{});typ=p.get('type');rh=sha(line.encode())
 if typ in ['custom_tool_call','function_call']:
  src=p.get('input',p.get('arguments',''));calls[p.get('call_id')]={'ordinal':n,'source':src,'record_sha256':rh}
  if report_name in src and ('write_text' in src or 'writeFile' in src):writes.append(n)
 if typ in ['custom_tool_call_output','function_call_output'] and isinstance(p.get('output'),list):
  count=sum(isinstance(v,dict) and v.get('type')=='input_image' for v in p['output'])
  if count:outs.append({'ordinal':n,'record_sha256':rh,'call_id':p.get('call_id'),'native_image_count':count})
assert writes;cut=min(writes);bindings=[];used={}
for r in receipts:
 path=Path(r.get('view_path',r.get('source',r.get('source_path'))));expected=r.get('render_sha256',r.get('sha256'));assert sha(path.read_bytes())==expected
 source=Path(r.get('source',r.get('source_path',path)));source_expected=r.get('source_sha256',r.get('sha256'));assert sha(source.read_bytes())==source_expected
 matches=[]
 for out in outs:
  c=calls[out['call_id']];src=c['source'];match=path.name in src
  if 'pdf_page_1based' in r:
   number=f"{r['pdf_page_1based']:02}";prefix=re.sub(r'\d+\.png$','',str(path));match=prefix in src and json.dumps(number) in src
   # Expand only the literal bounded numeric PDF loops used by this viewer call.
   loop=re.search(r'for\(let i=(\d+);i<=(\d+);i\+\+\)',src)
   if loop and str(path.parent) in src and 'tools.view_image' in src and prefix in src:
    page=r['pdf_page_1based'];template_ok=('pdf-0${i}.png' in src and page<10) or any(t in src for t in ["pdf-${String(i).padStart(2,'0')}.png", 'page-${String(i).padStart(2,"0")}.png'])
    match=template_ok and int(loop[1])<=page<=int(loop[2])
  # Resolve literal string-array loops and template paths, without executing code.
  arr=re.search(r'for\s*\(const n of (\[[^\]]*\])\)',src)
  base=re.search(r'const b=("[^"]*");',src)
  template=re.search(r'path:`([^`]+)`',src)
  if arr and base and template:
   names=json.loads(arr[1]);b=json.loads(base[1]);expanded=[template[1].replace('${b}',b).replace('${n}',n) for n in names]
   match=str(path) in expanded
  if match:
   assert out['ordinal']<cut;matches.append({**out,'call_ordinal':c['ordinal'],'call_record_sha256':c['record_sha256']});used[out['call_id']]=used.get(out['call_id'],0)+1
 assert len(matches)==1,(str(path),'expected exactly one named native output binding',matches)
 bindings.append({'path':str(path),'sha256':expected,'source_path':str(source),'source_sha256':source_expected,'native_output_binding':matches[0]})
assert len(bindings)==sum(o['native_image_count'] for o in outs)
assert all(used.get(o['call_id'])==o['native_image_count'] for o in outs)
out={'validation':'PASS','report_path':str(report),'report_sha256':sha(report.read_bytes()),'runtime_source':str(log),'native_view_count':len(bindings),'native_output_counts_exactly_match_individually_named_views':True,'all_native_views_before_first_report_write_ordinal':cut,'bindings':bindings,'limits':'Actual named view call code, original returned native image blocks and exact source/render bytes checked. PDF loops use either individually named pages or a verified literal bounded numeric loop and exact path template. No general OS isolation claim and no private context/account/instructions copied.'};p=d/'runtime-native-delivery.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(audit_name,len(bindings),'native model-visible views PASS')
