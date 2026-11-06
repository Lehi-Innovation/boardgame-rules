from pathlib import Path
import json,re,hashlib
q=Path(__file__).resolve().parent
m=next(x for x in json.loads((q/'model-provenance.json').read_text()) if x['agent_path']=='/root/q103_independent_novelty_review')
def norm(s):
 for _ in range(3):
  s=re.sub(r'\\u([0-9a-fA-F]{4})',lambda m:chr(int(m[1],16)),s)
  s=s.replace(r'\n','\n').replace(r'\r','\r').replace(r'\t','\t').replace(r'\"','"').replace('\\\\','\\').replace(chr(92)+chr(10),chr(10))
 return s
calls={};reads=[];images=[]
for line in Path(m['session_path']).open():
 p=json.loads(line).get('payload',{});typ=p.get('type')
 if typ in ['custom_tool_call','function_call']:calls[p.get('call_id',p.get('id'))]=str(p.get('input',p.get('arguments','')))
 elif typ in ['custom_tool_call_output','function_call_output']:
  code=calls.get(p.get('call_id'),'');o=p.get('output','')
  if 'view_image' in code and 'shaddam-original-2023-leader.png' in code and isinstance(o,list):images += [x.get('type') for x in o if x.get('type') in ['input_image','image']]
  text='\n'.join(x.get('text','') for x in o if isinstance(x,dict)) if isinstance(o,list) else str(o)
  if any(s in code for s in ['print(','cat ','sed ','nl -','tail ']) and 'write_text' not in code and 'json.dump(' not in code:reads.append({'input':code,'visible_output':text})
checks=[]
for f,arr,field in [('questions.json','questions','question'),('answer-key.json','answers','expected_answer')]:
 p=q/'benchmark-v14'/f;v=norm('\n'.join(r['visible_output'] for r in reads if f in r['input']));rows=json.loads(p.read_text())[arr];missing=[x['id'] for x in rows if x[field] not in v];checks.append({'file':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'entry_count':len(rows),'missing':missing,'complete':not missing})
r={'agent':m['agent_path'],'session':m['session_path'],'all101_prior_questions_and_keys_visible':all(x['complete'] for x in checks),'original_leader_image_returned_to_agent':bool(images),'checks':checks,'read_records':reads,'method':'Actual model-visible complete question and expected-answer strings, escape-normalized. Own report writes excluded; actual image content returned after original Leader view_image call. No proof inferred merely from claimed reading ranges.'}
(q/'q103-novelty-input-read-integrity.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n');print({k:v for k,v in r.items() if k not in ['read_records','checks']})
