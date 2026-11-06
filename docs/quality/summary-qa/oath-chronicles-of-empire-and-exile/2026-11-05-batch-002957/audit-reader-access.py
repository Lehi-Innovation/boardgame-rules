"""Audit actual reader tool calls for content outside the authorized inputs."""
from pathlib import Path
import json,re,hashlib,sys
P=Path(__file__).resolve().parent
D=P/sys.argv[1];tag=int(D.name.rsplit('-',1)[1]);out={}
patterns=[r'(?:expanded|seed)-iteration-(?!'+f'{tag:02d}'+r')\d+',r'/expanded-v\d+',r'grading-scope',r'answer-key',r'extracted/',r'source_pdfs/',r'/errata\.txt',r'/reference\.pdf',r'runtime-provenance',r'model-provenance',r'source-audit',r'/results\.json',r'/adjudication',r'\.codex/sessions',r'rules/oath-chronicles-of-empire-and-exile\.md',r'tools\.(?:web|mcp)|read_mcp_resource']
for who in 'ab':
 name=f'expanded{tag:02d}_reader_{who}';path=P/'delivery-audit'/f'{name}.actual-tool-records.json';records=json.loads(path.read_text());calls=[];hits=[]
 for n,row in enumerate(records):
  if row['kind']!='call':continue
  s=row.get('input','');cmds=[]
  for m in re.finditer(r'\bcmd\s*:\s*("(?:\\.|[^"\\])*")',s):
   try:cmds.append(json.loads(m[1]))
   except ValueError:pass
  calls.append({'call_index':n,'call_id':row['call_id'],'commands':cmds,'call_input_sha256':hashlib.sha256(s.encode()).hexdigest()})
  for pat in patterns:
   if re.search(pat,s):hits.append({'call_index':n,'pattern':pat})
 out[name]={'record_path':str(path.resolve()),'record_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'tool_call_count':len(calls),'forbidden_content_markers':hits,'decoded_commands':calls,'scope':'Actual tool inputs screened for source/key/scope/history/canonical/network paths; whole call records retained independently. Inputs and own generated builders allowed.'}
(D/'reader-access-provenance.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:{'calls':v['tool_call_count'],'forbidden_markers':v['forbidden_content_markers']} for k,v in out.items()})
