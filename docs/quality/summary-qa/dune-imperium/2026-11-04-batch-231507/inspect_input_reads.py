from pathlib import Path
import json,ast,sys
P=Path(__file__).resolve().parent;prov=json.loads((P/'model-provenance.json').read_text())
def flat(o):
 if isinstance(o,list):return '\n'.join(flat(x) for x in o)
 if isinstance(o,dict):
  if o.get('type') in ['image','image_url','audio']:return ''
  return '\n'.join(flat(o[k]) for k in ['text','output','content'] if k in o)
 if isinstance(o,str):
  if o[:1] in '[{':
   for parser in [json.loads,ast.literal_eval]:
    try:v=parser(o)
    except Exception:continue
    if isinstance(v,(dict,list)):return flat(v)
  return o
 return ''
for it in sys.argv[1:]:
 D=P/it;qtext=(D/'questions.json').read_text();questions=json.loads(qtext)['questions'];summary=(D/'summary-snapshot.md').read_text().splitlines();audit={'iteration':it,'method':'Inspected actual child tool call inputs and visible returned text. Exact question-string and every nonblank frozen-summary-line presence supplements recorded read ranges. Writer calls are excluded. Recovered initial truncation does not invalidate an otherwise complete read.','readers':{}}
 for r in 'ab':
  task=it.replace('seed-iteration-','seed_').replace('expanded-iteration-','expanded_')+'_'+r;e=next(x for x in prov if x['task']=='/root/'+task);calls={};outs=[]
  for l in Path(e['runtime_file']).open():
   x=json.loads(l);p=x.get('payload',{})
   if x.get('type')!='response_item':continue
   if p.get('type')=='custom_tool_call':
    inp=p.get('input','')
    if isinstance(inp,str) and any(z in inp for z in ['summary-snapshot.md','questions.json']) and not any(z in inp for z in ['cat >','write_text','json.dump']):calls[p.get('call_id')]=inp
   if p.get('type')=='custom_tool_call_output' and p.get('call_id') in calls:
    t=flat(p.get('output'));outs.append({'call_id':p['call_id'],'input':calls[p['call_id']],'truncated':'truncated output' in t,'visible_output':t})
  normal='\n'.join(x['visible_output'] for x in outs)
  for _ in range(3):normal=normal.replace('\\n','\n').replace('\\"','"').replace("\\'", "'")
  mq=[x['id'] for x in questions if x['question'] not in normal];ms=[i for i,t in enumerate(summary,1) if t and t not in normal]
  (D/f'reader-{r}-input-read-trace.json').write_text(json.dumps(outs,indent=2,ensure_ascii=False)+'\n')
  audit['readers'][r]={'runtime_file':e['runtime_file'],'question_texts_complete':not mq,'summary_nonblank_lines_complete':not ms,'missing_question_ids':mq,'missing_summary_lines':ms,'entire_questions_json_in_visible_output':qtext.strip() in normal,'initial_truncation_recovered':any(x['truncated'] for x in outs) and not mq and not ms,'unresolved_missing_input':bool(mq or ms),'trace':f'reader-{r}-input-read-trace.json'}
 (D/'input-read-audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n');print(it,{r:{k:v for k,v in a.items() if k in ['missing_question_ids','missing_summary_lines','initial_truncation_recovered']} for r,a in audit['readers'].items()})
