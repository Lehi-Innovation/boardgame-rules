from pathlib import Path
import json,hashlib,re
q=Path(__file__).resolve().parent;metadata=json.loads((q/'model-provenance.json').read_text());reports=[]
def tx(v):return '\n'.join(a.get('text','') for a in v if isinstance(a,dict)) if isinstance(v,list) else str(v)
def normalize_visible(text):
 # Model-visible JSON-string output preserves these escapes; decode them for semantic coverage matching.
 for _ in range(3):
  old=text
  text=re.sub(r'\\u([0-9a-fA-F]{4})',lambda m:chr(int(m.group(1),16)),text)
  text=text.replace(r'\n','\n').replace(r'\r','\r').replace(r'\t','\t').replace(r'\"','"').replace('\\\\','\\')
  if text==old:break
 return text
def rs(nums):
 out=[]
 for n in nums:
  if out and n==out[-1][1]+1:out[-1][1]=n
  else:out.append([n,n])
 return out
for m in metadata:
 name=m['agent_path'].split('/')[-1]
 if not name.startswith('final_source_audit'):continue
 num=name[len('final_source_audit'):];d=q/f'expanded-iteration-{num}'
 if not d.exists():continue
 calls={};reads=[]
 for line in Path(m['session_path']).open():
  x=json.loads(line);p=x.get('payload',{});typ=p.get('type')
  if typ in ['custom_tool_call','function_call']:calls[p.get('call_id',p.get('id'))]=str(p.get('input',p.get('arguments','')))
  if typ not in ['custom_tool_call_output','function_call_output']:continue
  code=calls.get(p.get('call_id'),'');out=tx(p.get('output',''))
  if not any(a in code for a in ['cat ','tail ','head ','sed ','awk ','nl -','print(']):continue
  if 'json.dump(' in code or 'write_text' in code or 'checks=[]' in code or 'source-audit.json' in code:continue
  reads.append({'call_id':p.get('call_id'),'input':code,'truncated':'truncated output' in out.lower(),'visible_output':out})
 checks=[]
 files=[d/'summary-snapshot.md',Path('/home/jonny/projects/boardgame-rules/extracted/dune-imperium-uprising-rules.txt'),q/'dune-imperium-uprising-supplements.txt',q/'dune-imperium-official-faq-2025-01-13.txt']
 if int(num)>=12:files += [q/'shaddam-original-2023-leader-transcription.txt',q/'shaddam-source-origin-metadata.json']
 for f in files:
  key='extracted/dune-imperium-uprising-rules.txt' if f.parent.name=='extracted' else f.name
  visible=normalize_visible('\n'.join(r['visible_output'] for r in reads if key in r['input']));lines=f.read_text().splitlines();missing=[i for i,l in enumerate(lines,1) if l.strip() and l not in visible]
  # All of the full source packet is checked, even source portions outside scope; report exact ranges rather than hide them.
  checks.append({'path':str(f),'line_count':len(lines),'missing_nonempty_line_ranges':rs(missing),'all_nonempty_lines_visible':not missing})
 report={'agent':m['agent_path'],'session':m['session_path'],'files':checks,'all_authorized_primary_texts_and_summary_visible':all(x['all_nonempty_lines_visible'] for x in checks),'read_records':reads,'method':'JSON-escape-normalized nonempty-line substrings in model-visible read outputs for each named primary text; excludes report writing and hash-only commands. Missing matches flag evidence gaps, not an assertion of intent. Alternative main PDF extraction/visual inspections are corroboration, not silently substituted for missing primary-text lines.'}
 (d/'source-audit-input-read-integrity.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');reports.append({k:v for k,v in report.items() if k!='read_records'})
(q/'source-audit-input-read-integrity.json').write_text(json.dumps(reports,indent=2,ensure_ascii=False)+'\n');print([{r['agent']:r['all_authorized_primary_texts_and_summary_visible']} for r in reports])
