from pathlib import Path
import json,hashlib,re
q=Path(__file__).resolve().parent;d=q/'expanded-iteration-22'
m=next(x for x in json.loads((q/'model-provenance.json').read_text()) if x['agent_path']=='/root/expanded22_q14_isolated')
def norm(text):
 for _ in range(8):
  old=text;text=text.replace('\\\\','\\').replace(r'\"','"').replace(r'\n','\n').replace(r'\r','\r').replace(r'\t','\t')
  if old==text:break
 return re.sub(r'\\u([0-9a-fA-F]{4})',lambda m:chr(int(m[1],16)),text)
calls={};reads=[]
for line in Path(m['session_path']).open():
 p=json.loads(line).get('payload',{});typ=p.get('type')
 if typ in ['function_call','custom_tool_call']:calls[p.get('call_id',p.get('id'))]=str(p.get('input',p.get('arguments','')))
 if typ not in ['function_call_output','custom_tool_call_output']:continue
 code=calls.get(p.get('call_id'),'');out=p.get('output','')
 if isinstance(out,list):out='\n'.join(x.get('text','') for x in out if isinstance(x,dict))
 else:out=str(out)
 if not any(v in code for v in ['summary-snapshot.md','q14-isolated-input.json']):continue
 if any(v in code for v in ['write_text','json.dump(','q14-isolated-adjudication.json']):continue
 if not any(v in code for v in ['cat ','sed ','tail ','head ','nl -','print(']):continue
 reads.append({'input':code,'visible_output':out,'truncated':'truncated output' in out.lower()})
sv=norm('\n'.join(x['visible_output'] for x in reads if 'summary-snapshot.md' in x['input']));pv=norm('\n'.join(x['visible_output'] for x in reads if 'q14-isolated-input.json' in x['input']));summary=(d/'summary-snapshot.md').read_text().splitlines();missing=[i for i,l in enumerate(summary,1) if l.strip() and norm(l) not in sv];packet=json.loads((d/'q14-isolated-input.json').read_text());parts={'question':packet['question']['question'],'key_expected':packet['key']['expected_answer'],'key_sources':packet['key']['source_references'],'key_novelty':packet['key']['novelty']}
for r in ['a','b']:
 for k in ['answer','evidence']:parts[r+'_'+k]=packet['readers'][r][k]
mp=[k for k,v in parts.items() if norm(str(v)) not in pv];report={'agent':m['agent_path'],'session_id':m['session_id'],'actual_models':m['turn_contexts'],'fork_turns':m['fork_turns'],'summary_line_count':len(summary),'missing_nonempty_summary_lines':missing,'missing_complete_case_fields':mp,'all348_summary_lines_and_complete_isolated_case_visible':not missing and not mp,'method':'Nested-JSON-escape-normalized exact nonempty summary-line and complete question/key/answer/evidence field matching in actual model-visible input reads. Own report writes excluded. No other question, answer or report is authorized.','input_hashes':{str(d/f):hashlib.sha256((d/f).read_bytes()).hexdigest() for f in ['summary-snapshot.md','q14-isolated-input.json']},'read_records':reads};(d/'q14-isolated-input-read-integrity.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print({k:v for k,v in report.items() if k not in ['read_records','actual_models','input_hashes']})
