from pathlib import Path
import json,hashlib,re,sys
q=Path(__file__).resolve().parent;metadata=json.loads((q/'model-provenance.json').read_text());reports=[]
def output_text(value):
 if isinstance(value,list):return '\n'.join(x.get('text','') for x in value if isinstance(x,dict))
 return value if isinstance(value,str) else str(value)
def normalize_visible(text):
 # Model-visible JSON-string output preserves these escapes; decode them for semantic coverage matching.
 for _ in range(3):
  old=text
  text=re.sub(r'\\u([0-9a-fA-F]{4})',lambda m:chr(int(m.group(1),16)),text)
  text=text.replace(r'\n','\n').replace(r'\r','\r').replace(r'\t','\t').replace(r'\"','"').replace('\\\\','\\')
  if text==old:break
 return text
def ranges(vals):
 out=[]
 for n in vals:
  if out and n==out[-1][-1]+1:out[-1].append(n)
  else:out.append([n])
 return [[x[0],x[-1]] for x in out]
for m in metadata:
 task=m['agent_path'].split('/')[-1]
 if not (task.startswith('seed') or task.startswith('expanded')) or '_' not in task or task.endswith('adjudicator'):continue
 prefix,r=task.rsplit('_',1)
 if r not in ['a','b']:continue
 kind='seed' if prefix.startswith('seed') else 'expanded';num=prefix[len(kind):];d=q/f'{kind}-iteration-{num}'
 if not d.exists():continue
 calls={};records=[];visible=[];summary_visible=[];question_visible=[]
 for line in Path(m['session_path']).open():
  x=json.loads(line);p=x.get('payload',{});typ=p.get('type')
  if typ in ['custom_tool_call','function_call']:
   inp=p.get('input',p.get('arguments',''));calls[p.get('call_id',p.get('id'))]=str(inp)
  elif typ in ['custom_tool_call_output','function_call_output']:
   inp=calls.get(p.get('call_id'),'');out=output_text(p.get('output',''))
   if 'summary-snapshot.md' not in inp and 'questions.json' not in inp:continue
   # Read operations only: exclude writes and own-output validation/draft printing.
   if 'cat >' in inp or 'json.dump(' in inp or 'reader-a.json' in inp or 'reader-b.json' in inp or 'build_reader' in inp:continue
   if not any(x in inp for x in ['cat ','tail ','head ','sed ','nl -','jq ','print(','rg ','wc ']):continue
   records.append({'call_id':p.get('call_id'),'input':inp,'truncated':'truncated output' in out.lower(),'output_sha256':hashlib.sha256(out.encode()).hexdigest(),'visible_output':out})
   visible.append(out)
   if 'summary-snapshot.md' in inp:summary_visible.append(out)
   if 'questions.json' in inp:question_visible.append(out)
 sv=normalize_visible('\n'.join(summary_visible));qv=normalize_visible('\n'.join(question_visible));summary=(d/'summary-snapshot.md').read_text().splitlines();missing=[i for i,line in enumerate(summary,1) if line.strip() and line not in sv]
 questions=json.loads((d/'questions.json').read_text())['questions'];missingq=[a['id'] for a in questions if a['question'] not in qv]
 report={'agent':m['agent_path'],'session':m['session_path'],'iteration':d.name,'summary_line_count':len(summary),'nonempty_summary_lines_missing_from_visible_read_outputs':missing,'missing_summary_ranges':ranges(missing),'question_count':len(questions),'question_texts_missing_from_visible_read_outputs':missingq,'initial_or_later_read_truncation_observed':any(x['truncated'] for x in records),'all_summary_lines_and_question_texts_visible_in_reads':not missing and not missingq,'method':'JSON-escape-normalized nonempty frozen-summary line and full question-text substring match against model-visible tool outputs of input reads only; excludes own answer writes/validation. A negative match flags unresolved read evidence, not an assertion of model intent.','read_records':records}
 (d/f'reader-{r}-input-read-audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');reports.append({k:v for k,v in report.items() if k!='read_records'})
(q/'input-read-integrity.json').write_text(json.dumps(reports,indent=2,ensure_ascii=False)+'\n')
selected=[r for r in reports if len(sys.argv)<2 or r['iteration']==sys.argv[1]]
print([{k:r[k] for k in ['agent','all_summary_lines_and_question_texts_visible_in_reads','missing_summary_ranges','question_texts_missing_from_visible_read_outputs']} for r in selected])
