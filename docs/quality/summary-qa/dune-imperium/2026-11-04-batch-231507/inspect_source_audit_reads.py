from pathlib import Path
import json,ast,sys,runpy,re
P=Path(__file__).resolve().parent
# Import the shared output flattener without requesting any reader iterations.
argv=sys.argv;sys.argv=[argv[0]]
flat=runpy.run_path(str(P/'inspect_input_reads.py'))['flat'];sys.argv=argv
serial=argv[1];D=P/('source-audit-final-'+serial)
e=next(x for x in json.loads((P/'model-provenance.json').read_text()) if x['task']=='/root/final_source_audit_'+serial)
calls={};trace=[]
def count_images(o):
 if isinstance(o,list): return sum(count_images(x) for x in o)
 if isinstance(o,dict): return int(o.get('type') in ['image','image_url','input_image'])+sum(count_images(v) for k,v in o.items() if k not in ['data','image_url'])
 if isinstance(o,str) and o[:1] in '[{':
  for parser in [json.loads,ast.literal_eval]:
   try:return count_images(parser(o))
   except Exception:pass
 return 0
for line in Path(e['runtime_file']).open():
 x=json.loads(line);p=x.get('payload',{})
 if x.get('type')!='response_item':continue
 if p.get('type')=='custom_tool_call':
  inp=p.get('input','')
  if not any(t in inp for t in ['write_text','json.dump']):calls[p['call_id']]=inp
 if p.get('type')=='custom_tool_call_output' and p.get('call_id') in calls:
  out=p.get('output');t=flat(out)
  trace.append({'call_id':p['call_id'],'input':calls[p['call_id']],'truncated':'truncated' in t.lower(),'image_count':count_images(out),'visible_text':t})
normal='\n'.join(x['visible_text'] for x in trace)
for _ in range(3):normal=normal.replace('\\n','\n').replace('\\"','"').replace("\\'", "'")
files=[D/'summary-snapshot.md',Path('/home/jonny/projects/boardgame-rules/extracted/dune-imperium-rules.txt'),P/'faq-columns.txt']
checks=[]
for f in files:
 missing=[i for i,t in enumerate(f.read_text().splitlines(),1) if t.strip() and t not in normal]
 checks.append({'path':str(f.resolve()),'missing_nonblank_lines':missing,'complete':not missing})
visuals=sorted((P/'source-assets').glob('*.png'))+[P/'publisher-house-hagal-harvest-spice-2020.jpg']
visual_returns=[]
for call in trace:
 if not call['image_count']:continue
 # Resolve only the simple literal-array/template loops actually used by this auditor.
 loop=re.search(r'for \(const (\w+) of (\[[^\]]*\])\)',call['input'])
 template=re.search(r'path:`([^`]+)`',call['input'])
 if loop and template:
  try:items=json.loads(loop.group(2))
  except ValueError:continue
  paths=[template.group(1).replace('${'+loop.group(1)+'}',str(v)) for v in items]
  if len(paths)==call['image_count'] and all('${' not in path for path in paths):
   visual_returns.append({'call_id':call['call_id'],'resolved_paths':paths,'returned_image_count':call['image_count']})
resolved_paths={path for call in visual_returns for path in call['resolved_paths']}
missing_visuals=[str(f.resolve()) for f in visuals if str(f.resolve()) not in normal and str(f.resolve()) not in resolved_paths]
a={'auditor':e['task'],'runtime_file':e['runtime_file'],'model':e['contexts'],'actual_spawn_configuration':e['actual_spawn_configuration'],'method':'Inspected actual source-reading tool calls and visible returned output; exact nonblank text-line coverage plus returned image counts. Source-only page path outputs, or literal loop path resolution paired with matching actual image-return counts, identify each successfully displayed page. No image bytes copied to trace.','text_inputs':checks,'returned_image_count':sum(x['image_count'] for x in trace),'expected_image_count':len(visuals),'missing_visual_paths':missing_visuals,'resolved_visual_returns':visual_returns,'any_truncated_read_output':any(x['truncated'] for x in trace),'calls':[{'call_id':x['call_id'],'input':x['input'],'image_count':x['image_count'],'truncated':x['truncated']} for x in trace]}
(D/'actual-input-read-trace.json').write_text(json.dumps(trace,indent=2)+'\n');(D/'input-read-audit.json').write_text(json.dumps(a,indent=2)+'\n')
print({k:v for k,v in a.items() if k not in ['calls']})
