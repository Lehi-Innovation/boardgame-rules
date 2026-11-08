"""Bind individually named native-view receipts to original model-visible image outputs."""
from pathlib import Path
import json,hashlib,sys,re,ast,base64
from verify_runtime_delivery import log_for
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
audit_name,task=sys.argv[1:3];report_name=sys.argv[3] if len(sys.argv)>3 else 'source-audit.json';d=ROOT/audit_name;report=d/report_name;x=json.loads(report.read_text());receipts=x['native_view_receipts'];calls={};outs=[];writes=[];log=log_for(task)
manifest_path=d/'source-manifest.json';manifest_hashes={str(Path(z['path'])):z['sha256'] for z in json.loads(manifest_path.read_text())['sources']} if manifest_path.exists() else {}
def literal_view_paths(src):
 """Resolve only literal constants, finite loops, templates and string addition."""
 constants={name:ast.literal_eval(value) for name,value in re.findall(r'const\s+(\w+)\s*=\s*("[^"\n]*"|\'[^\'\n]*\')\s*;',src)}
 contexts=[constants]
 for variable,values in re.findall(r'for\s*\(const\s+(\w+)\s+of\s+(\[[^\]]*\])\)',src):
  contexts=[dict(c,**{variable:v}) for c in contexts for v in ast.literal_eval(values)]
 numeric=re.search(r'for\s*\(let\s+(\w+)=(\d+);\1<=(\d+);\1\+\+\)',src)
 if numeric:contexts=[dict(c,**{numeric[1]:v}) for c in contexts for v in range(int(numeric[2]),int(numeric[3])+1)]
 def resolve(node,c):
  if isinstance(node,ast.Constant) and isinstance(node.value,str):return node.value
  if isinstance(node,ast.Name) and node.id in c:return str(c[node.id])
  if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Add):return resolve(node.left,c)+resolve(node.right,c)
  raise ValueError('Unsupported literal path expression')
 paths=set()
 for expression in re.findall(r'path:\s*(.*?),\s*detail:',src,re.S):
  for c in contexts:
   expr=re.sub(r'String\((\w+)\)\.padStart\(2,[\'\"]0[\'\"]\)',lambda m:json.dumps(f"{int(c[m[1]]):02}"),expression)
   try:
    if expr.startswith('`') and expr.endswith('`'):
     value=expr[1:-1]
     for name,item in c.items():value=value.replace('${'+name+'}',str(item))
     assert '${' not in value
    else:value=resolve(ast.parse(expr,mode='eval').body,c)
    paths.add(value)
   except (ValueError,SyntaxError,AssertionError,KeyError,TypeError):continue
 return paths
for n,line in enumerate(log.open(),1):
 rec=json.loads(line);p=rec.get('payload',{});typ=p.get('type');rh=sha(line.encode())
 if typ in ['custom_tool_call','function_call']:
  src=p.get('input',p.get('arguments',''));calls[p.get('call_id')]={'ordinal':n,'source':src,'record_sha256':rh}
  if report_name in src and ('write_text' in src or 'writeFile' in src):writes.append(n)
 if typ in ['custom_tool_call_output','function_call_output'] and isinstance(p.get('output'),list):
  count=sum(isinstance(v,dict) and v.get('type')=='input_image' for v in p['output'])
  if count:
   image_hashes=[sha(base64.b64decode(v['image_url'].split(',',1)[1])) for v in p['output'] if isinstance(v,dict) and v.get('type')=='input_image' and isinstance(v.get('image_url'),str) and v['image_url'].startswith('data:')]
   outs.append({'ordinal':n,'record_sha256':rh,'call_id':p.get('call_id'),'native_image_count':count,'native_encoded_image_sha256':image_hashes})
assert writes;cut=min(writes);bindings=[];used={}
for r in receipts:
 path=Path(r.get('view_path') or r.get('render_path') or r.get('source') or r.get('source_path'));observed=sha(path.read_bytes());declared=r.get('render_sha256',r.get('sha256'))
 if declared is not None:assert observed==declared
 expected=declared or observed
 source=Path(r.get('source',r.get('source_path',path)));observed_source=sha(source.read_bytes());source_declared=r.get('source_sha256',r.get('sha256')) or manifest_hashes.get(str(source))
 if source_declared is not None:assert observed_source==source_declared
 source_expected=source_declared or observed_source
 matches=[]
 for out in outs:
  c=calls[out['call_id']];src=c['source'];match=path.name in src
  if r.get('pdf_page_1based') is not None:
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
  # Resolve literal array loops, including padded page numbers, without executing code.
  literal_array=re.search(r"for\s*\(const n of (\[[^\]]*\])\)",src)
  literal_template=re.search(r"path:`([^`]+)`",src)
  if literal_array and literal_template:
   values=ast.literal_eval(literal_array[1]);template=literal_template[1]
   constants={name:ast.literal_eval(value) for name,value in re.findall(r'const\s+(\w+)\s*=\s*("[^"\n]*"|\'[^\'\n]*\')\s*;',src)}
   expanded=[]
   for value in values:
    resolved=template
    if isinstance(value,int):resolved=re.sub(r"\$\{String\(n\)\.padStart\(2,['\"]0['\"]\)\}",f"{value:02}",resolved)
    resolved=resolved.replace('${n}',str(value))
    for name,constant in constants.items():resolved=resolved.replace('${'+name+'}',constant)
    expanded.append(resolved)
   match=str(path) in expanded
  # Resolve only safe literal/name/Add string concatenations used in image paths.
  if literal_array and not literal_template:
   expr=re.search(r"path:([^,}]+)",src)
   constants={name:ast.literal_eval(value) for name,value in re.findall(r'const\s+(\w+)\s*=\s*("[^"\n]*"|\'[^\'\n]*\')\s*;',src)}
   def resolve(node,values):
    if isinstance(node,ast.Constant) and isinstance(node.value,str):return node.value
    if isinstance(node,ast.Name) and node.id in values:return values[node.id]
    if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Add):return resolve(node.left,values)+resolve(node.right,values)
    raise ValueError('Unsupported path expression')
   if expr:
    try:
     tree=ast.parse(expr[1],mode='eval').body
     expanded=[resolve(tree,dict(constants,n=value)) for value in ast.literal_eval(literal_array[1])]
     match=str(path) in expanded
    except (ValueError,SyntaxError,TypeError):pass
  literal_paths=literal_view_paths(src)
  if literal_paths:match=str(path) in literal_paths
  if match:
   assert out['ordinal']<cut;matches.append({**out,'call_ordinal':c['ordinal'],'call_record_sha256':c['record_sha256']});used[out['call_id']]=used.get(out['call_id'],0)+1
 assert len(matches)==1,(str(path),'expected exactly one named native output binding',matches)
 bindings.append({'path':str(path),'sha256':expected,'source_path':str(source),'source_sha256':source_expected,'render_hash_supplied_in_receipt':declared is not None,'source_hash_checked_against_receipt_or_frozen_manifest':source_declared is not None,'native_output_binding':matches[0]})
assert len(bindings)==sum(o['native_image_count'] for o in outs)
assert all(used.get(o['call_id'])==o['native_image_count'] for o in outs)
out={'validation':'PASS','report_path':str(report),'report_sha256':sha(report.read_bytes()),'runtime_source':str(log),'native_view_count':len(bindings),'native_output_counts_exactly_match_individually_named_views':True,'all_native_views_before_first_report_write_ordinal':cut,'bindings':bindings,'limits':'Actual individually named view calls and returned native image blocks bound before report writing. Current source/render file hashes recorded; supplied receipt or frozen-manifest hashes compared where available. Native encoded image hashes are separate because the image tool may resize/reencode the displayed frame. Paths resolve only safe literals, finite loops, templates and string concatenations; no arbitrary code execution, OS-isolation claim or private context/account/instruction copies.'};p=d/'runtime-native-delivery.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(audit_name,len(bindings),'native model-visible views PASS')
