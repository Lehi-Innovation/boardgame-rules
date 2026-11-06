from pathlib import Path
import json,hashlib,sys,re
ROOT=Path(__file__).resolve().parent
LOGROOT=Path('/mnt/c/Users/jonny/.codex/sessions')
def sha(b):return hashlib.sha256(b).hexdigest()
def strings(x):
 if isinstance(x,dict):
  for v in x.values():yield from strings(v)
 elif isinstance(x,list):
  for v in x:yield from strings(v)
 elif isinstance(x,str):
  yield x
  # Tool responses may encode nested exec output as JSON.
  dec=json.JSONDecoder()
  for match in re.finditer(r'[\[{]',x):
   try:v,end=dec.raw_decode(x[match.start():])
   except:continue
   if isinstance(v,(dict,list)):
    yield from strings(v);break

def log_for(task):
 for p in sorted(LOGROOT.glob('2026/11/*/*.jsonl')):
  try:
   first=p.open().readline();m=json.loads(first)['payload']
  except:continue
  if m.get('agent_path')==task and m.get('parent_thread_id')=='01a1b0b3-0030-70b2-8947-7a940fdf364f':return p
 raise ValueError('No runtime for '+task)
def verify(iteration,reader,task):
 d=ROOT/iteration;p=d/f'reader-{reader}.json';result=json.loads(p.read_text());log=log_for(task);tooloutputs=[];identity=None;turns=[];answer_writes=[]
 for n,line in enumerate(log.open(),1):
  rec=json.loads(line);pay=rec.get('payload',{})
  if rec.get('type')=='session_meta':identity={'id':pay.get('id'),'parent':pay.get('parent_thread_id'),'task':pay.get('agent_path'),'history_mode':pay.get('history_mode'),'ordinal':n,'record_sha256':sha(line.encode())}
  if rec.get('type')=='turn_context':turns.append({'ordinal':n,'actual_model':pay.get('model'),'actual_effort':pay.get('effort'),'record_sha256':sha(line.encode())})
  if pay.get('type') in ['custom_tool_call','function_call']:
   code=str(pay.get('input',pay.get('arguments','')))
   if p.name in code and any(t in code for t in ['write_text','writeFile','json.dump',".open('w'",".open(\"w\""]):answer_writes.append(n)
  if pay.get('type') in ['custom_tool_call_output','function_call_output']:
   tooloutputs.append({'ordinal':n,'record_sha256':sha(line.encode()),'text':list(strings(pay.get('output')))})
 assert answer_writes,'No answer-file write located for input-before-write proof'
 first_answer_write=min(answer_writes)
 receipts=[]
 supplied_receipts=result['delivery_receipts']
 if isinstance(supplied_receipts,dict) and 'summary_slices' in supplied_receipts:
  supplied_receipts=[{'file':'summary-snapshot.md','ranges':supplied_receipts['summary_slices']},{'file':'questions.json','ranges':supplied_receipts['questions_slices']}]
 metadata_diagnostics=[]
 if isinstance(supplied_receipts,list) and supplied_receipts and all(isinstance(z,dict) and 'start' in z and 'end' in z for z in supplied_receipts):
  grouped={}
  for z in supplied_receipts:grouped.setdefault(z.get('file',z.get('path')),[]).append(z)
  normalized=[]
  for filename,items in grouped.items():
   source=d/Path(filename).name;length=len(source.read_text());starts=sorted(set(z['start'] for z in items));ranges=[[a,starts[j+1] if j+1<len(starts) else length] for j,a in enumerate(starts)]
   # Candidate ranges are only accepted after exact content matching against actual runtime outputs below.
   normalized.append({'file':filename,'ranges':ranges})
   metadata_diagnostics.append({'file':filename,'raw_receipts':items,'actual_source_characters':length,'note':'Raw receipt end/total fields may be metadata errors; parent derives candidate intervals from recorded starts and actual source length, then independently requires exact full-slice presence in model-visible runtime outputs. No missing delivery is assumed or excused.'})
  supplied_receipts=normalized
 for inp in supplied_receipts:
  source=d/Path(inp.get('file',inp.get('path'))).name;text=source.read_text();ranges=inp.get('contiguous_ranges',inp.get('ranges',inp.get('slices',inp.get('delivered_ranges_0_based_half_open'))))
  if ranges and isinstance(ranges[0],dict): ranges=[[v['start'],v['end']] for v in ranges]
  assert ranges and ranges[0][0]==0 and ranges[-1][1]==len(text)
  checked=[]
  for i,(a,b) in enumerate(ranges):
   assert 0<=a<b<=len(text) and b-a<=6000
   if i:assert a==ranges[i-1][1]
   needle=text[a:b];found=[]
   for out in tooloutputs:
    if any(needle in v for v in out['text']):found.append({k:out[k] for k in ['ordinal','record_sha256']})
   assert found,(source,a,b,'actual model-visible full slice not found')
   assert any(v['ordinal']<first_answer_write for v in found),(source,a,b,'No complete delivery before first answer-file write')
   checked.append({'start':a,'end':b,'characters':b-a,'slice_sha256_utf8':sha(needle.encode()),'matching_runtime_outputs':found})
  receipts.append({'source_path':str(source),'source_sha256':sha(source.read_bytes()),'source_characters':len(text),'complete_nontruncated_ranges':checked,'exact_actual_output_match':True})
 expected=[q['id'] for q in json.loads((d/'questions.json').read_text())['questions']];actual=[x['id'] for x in result['answers']]
 assert actual==expected or (len(actual)==len(set(actual)) and set(actual)==set(expected))
 spanchecks=[]
 s=(d/'summary-snapshot.md').read_text()
 for answer in result['answers']:
  evidence=answer['evidence']
  if isinstance(evidence,list):
   for e in evidence:
    if isinstance(e,dict) and all(k in e for k in ['start','end','text']):spanchecks.append({'id':answer['id'],'start':e['start'],'end':e['end'],'literal':s[e['start']:e['end']]==e['text']})
 assert all(x['literal'] for x in spanchecks)
 assert turns and all(t['actual_model']=='gpt-6-luna' and t['actual_effort']=='high' for t in turns)
 payload={'reader':reader,'requested_model':'gpt-6-luna','requested_effort':'high','fork_turns':'none','runtime_source_path':str(log),'identity':identity,'model_records':turns,'input_delivery':receipts,'raw_receipt_metadata_diagnostics':metadata_diagnostics,'first_answer_file_write_record_ordinal':first_answer_write,'all_inputs_delivered_before_first_answer_file_write':True,'all_expected_ids_exactly_once':True,'evidence_literal_span_checks':spanchecks,'raw_response_sha256':sha(p.read_bytes()),'validation':'PASS','scope':'Technical input/output integrity separate from factual grades. Opaque original-record hashes retained, no internal instructions/account/permissions copied.'}
 (d/f'reader-{reader}-runtime-delivery.json').write_text(json.dumps(payload,indent=2)+'\n');print(iteration,reader,'runtime and delivery PASS',len(actual))
if __name__=='__main__':verify(*sys.argv[1:])
