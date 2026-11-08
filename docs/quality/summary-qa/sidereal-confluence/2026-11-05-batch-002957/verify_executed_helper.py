"""Inspect generic helper literal bytes in actual calls; never execute inspected code."""
from pathlib import Path
import json,hashlib,sys,ast,re,zlib,base64
from verify_runtime_delivery import log_for
ROOT=Path(__file__).resolve().parent
iteration,reader,task=sys.argv[1:]
d=ROOT/iteration;expected=hashlib.sha256((ROOT/'reader-protocol-v2/source_units.py').read_bytes()).hexdigest();matches=[]
for n,line in enumerate(log_for(task).open(),1):
 v=json.loads(line).get('payload',{});s=v.get('input',v.get('arguments',''))
 if v.get('type') not in ['custom_tool_call','function_call']:continue
 raw=re.search(r'String\.raw`(.*?)`;\s*\n',s,re.S)
 if raw:cmd=raw[1]
 else:
  m=re.search(r'cmd\s*:\s*(")',s)
  if not m:continue
  try:cmd,_=json.JSONDecoder().raw_decode(s[m.start(1):])
  except Exception:continue
 body=cmd.split("<<'PY'\n",1)[1].rsplit('\nPY',1)[0] if "<<'PY'\n" in cmd else cmd
 try:tree=ast.parse(body)
 except Exception:continue
 for node in ast.walk(tree):
  if not isinstance(node,ast.Constant) or not isinstance(node.value,str):continue
  value=node.value;encoding='literal'
  if 'def _span' not in value:
   if not (1000<len(value)<10000 and re.fullmatch(r'[A-Za-z0-9+/=]+',value)):continue
   try:value=zlib.decompress(base64.b64decode(value,validate=True)).decode();encoding='base64/zlib'
   except Exception:continue
  if 'def _span' not in value:continue
  h=hashlib.sha256(value.encode()).hexdigest();matches.append({'ordinal':n,'record_sha256':hashlib.sha256(line.encode()).hexdigest(),'transport':encoding,'decoded_helper_sha256':h,'matches_supplied_code':h==expected})
assert any(x['matches_supplied_code'] for x in matches),'No actual matching generic helper bytes found'
out=d/f'reader-{reader}-executed-helper-identity.json';assert not out.exists();out.write_text(json.dumps({'validation':'PASS actual tool-call generic helper bytes match originally supplied helper','task':task,'expected_helper_sha256':expected,'records':matches,'limits':'Static code-literal/transport identity only. Reader reports execution; returned complete units are independently validated and substantive answers independently graded.'},indent=2)+'\n')
print(iteration,reader,'actual original-helper identity PASS',sum(x['matches_supplied_code'] for x in matches),'records')
