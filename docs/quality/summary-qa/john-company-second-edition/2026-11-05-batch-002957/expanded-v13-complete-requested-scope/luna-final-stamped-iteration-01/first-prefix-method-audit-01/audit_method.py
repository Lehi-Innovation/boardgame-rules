"""Narrow method audit. Never persists runtime bodies or semantic answer content."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import ast, builtins, collections, contextlib, hashlib, importlib.util, io, json, re, shlex, types

F = Path(__file__).parent.parent
OUT = Path(__file__).parent
RUNTIMES = {
 'a': Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/06/rollout-2026-11-06T08-34-19-01a1b17f-1872-7782-85b1-9ebbe7cd6c20.jsonl'),
 'b': Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/06/rollout-2026-11-06T08-35-24-01a1b180-1984-7c62-b190-2d40090f9831.jsonl')}
def sha(v):
 return hashlib.sha256(v if isinstance(v, bytes) else v.encode()).hexdigest()
def jsha(v): return sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')))
def binding(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
summary=(F/'summary-snapshot.md').read_text()
questions=json.loads((F/'questions.json').read_text())['questions']
slines=summary.splitlines(keepends=True)
spec=importlib.util.spec_from_file_location('frozen_source_checker',F/'source-unit-checker.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
units=checker.units(summary)

def script_from_call(raw):
 m=re.search(r'cmd:("(?:\\.|[^"\\])*")',raw)
 if not m:return None,None
 cmd=json.loads(m.group(1))
 if cmd.startswith('python3 -c '):return cmd,shlex.split(cmd)[2]
 if cmd.startswith("python3 - <<'PY'\n"):return cmd,cmd.split('\n',1)[1].rsplit('\nPY',1)[0]
 return cmd,None

def audit(role,path):
 data=path.read_bytes(); lines=data.splitlines(keepends=True)
 manifest=json.loads((F/'bounded-turn-history'/f'reader-{role}-turn-01'/'manifest.json').read_text())
 frozen={k:json.loads((F/'bounded-turn-history'/f'reader-{role}-turn-01'/f'reader-{role}-{k}.json').read_text()) for k in ['draft','self-check']}
 frozen_records=frozen['self-check'].get('records',frozen['self-check'].get('source_checks'))
 physical=[]; calls=[]; outputs={}; contexts=[]; actor={}; labels=[]
 for ordinal,line in enumerate(lines,1):
  try:o=json.loads(line)
  except json.JSONDecodeError:break
  typ=o.get('type');p=o.get('payload',{})
  # Only event labels, not event/message bodies, are retained or inspected.
  subtype=p.get('type') if isinstance(p,dict) else None
  physical.append({'ordinal':ordinal,'bytes':len(line),'sha256':sha(line),'event_type':typ,'event_label':subtype})
  if typ=='session_meta':
   s=p.get('source',{});sub=s.get('subagent',{}) if isinstance(s,dict) else {}; spawn=sub.get('thread_spawn',{}) if isinstance(sub,dict) else {}
   actor={'session_id':p.get('id'),'parent_thread_id':spawn.get('parent_thread_id'),'actor':spawn.get('agent_path')}
  elif typ=='turn_context':contexts.append({'ordinal':ordinal,'model':p.get('model'),'effort':p.get('effort')})
  elif typ=='event_msg':labels.append({'ordinal':ordinal,'event_label':subtype})
  elif typ=='response_item' and subtype in ['custom_tool_call','function_call']:
   raw=p.get('input',p.get('arguments',''));cmd,script=script_from_call(raw)
   calls.append({'ordinal':ordinal,'call_id':p.get('call_id'),'name':p.get('name'),'raw':raw,'cmd':cmd,'script':script})
  elif typ=='response_item' and subtype in ['custom_tool_call_output','function_call_output']:
   value=p.get('output','')
   texts=[x.get('text','') for x in value if isinstance(x,dict) and x.get('type') in ['input_text','text']] if isinstance(value,list) else [value] if isinstance(value,str) else []
   outputs[p.get('call_id')]={'ordinal':ordinal,'text':''.join(texts),'body_sha256':jsha(texts),'body_chars':sum(map(len,texts))}
 first_write=next(c['ordinal'] for c in calls if c['script'] and 'write_text' in c['script'])
 # Memory-only replay of permitted deterministic Python mechanics. No real writes.
 mem={str(F/'summary-snapshot.md'):summary,str(F/'questions.json'):(F/'questions.json').read_text()}
 reads=[];writes=[];current=0
 class MemoryPath:
  def __init__(self,v):self.value=str(v)
  def __truediv__(self,v):return MemoryPath(self.value+'/'+str(v))
  def __str__(self):return self.value
  def exists(self):return self.value in mem
  def with_name(self,name):return MemoryPath(self.value.rsplit('/',1)[0]+'/'+name)
  def read_text(self,*args,**kwargs):
   reads.append({'call_ordinal':current,'path':self.value,'sha256':sha(mem[self.value])});return mem[self.value]
  def write_text(self,v,*args,**kwargs):
   allowed={str(F/f'reader-{role}-{x}.json') for x in ['draft','self-check']}|{str(F/f'reader-{role}.json')}
   assert self.value in allowed,'Unpermitted replay path'
   mem[self.value]=v;writes.append({'call_ordinal':current,'path':self.value,'sha256':sha(v),'bytes':len(v.encode())});return len(v)
 def restricted_import(name,*args,**kwargs):
  if name=='pathlib':return types.SimpleNamespace(Path=MemoryPath)
  if name in ['json','re','hashlib']:return {'json':json,'re':re,'hashlib':hashlib}[name]
  raise ValueError('unapproved import '+name)
 safe_builtins={k:v for k,v in vars(builtins).items() if k not in ['open','eval','exec','compile','input','breakpoint']}
 safe_builtins['__import__']=restricted_import
 call_records=[];composition=[];failed=[];frozen_point=None
 terminal_before=contexts[1]['ordinal'] if len(contexts)>1 else len(physical)+1
 for c in calls:
  current=c['ordinal'];script=c['script'];out=outputs.get(c['call_id'],{})
  record={k:c[k] for k in ['ordinal','call_id','name']}
  record.update({'input_chars':len(c['raw']),'input_sha256':sha(c['raw']),'output_ordinal':out.get('ordinal'),'visible_output_chars':out.get('body_chars'),'visible_output_sha256':out.get('body_sha256')})
  if frozen_point is not None and current>=terminal_before:
   record['scope']='later live continuation; not per-entry audited';call_records.append(record);continue
  if script is None:
   record['unparsed_tool']=True;call_records.append(record);continue
  # Scripts are limited to Python primitives and the above read/write membrane.
  tree=ast.parse(script)
  assert not any(isinstance(n,ast.Attribute) and n.attr.startswith('__') and n.attr!='__name__' for n in ast.walk(tree))
  capture=io.StringIO();before=len(writes);error=None
  try:
   with contextlib.redirect_stdout(capture):exec(compile(tree,'<reader mechanical call>','exec'),{'__builtins__':safe_builtins})
  except Exception as e:error=type(e).__name__
  expected=capture.getvalue();visible=out.get('text','')
  record['mechanical_replay_error_type']=error
  record['mechanical_stdout_sha256']=sha(expected)
  record['expected_stdout_visibly_received']=bool(expected) and expected in visible
  record['visible_truncation_marker']=bool(re.search(r'(?:tokens? truncated|truncated output|output truncated)',visible,re.I))
  # Match complete original objects, never mere IDs or clipped question strings.
  decoded=[]
  def visit_json(value):
   if isinstance(value,dict):
    if value in questions: decoded.append(value['id'])
    for child in value.values():visit_json(child)
   elif isinstance(value,list):
    for child in value:visit_json(child)
  for match in re.finditer(r'[\[{]',visible):
   try:value,_=json.JSONDecoder().raw_decode(visible[match.start():]);visit_json(value)
   except (ValueError,TypeError):pass
  record['complete_question_objects_received']=sorted(set(decoded))
  # A summary chunk's source text is checked as an exact contiguous LF slice.
  if 'summary-snapshot.md' in script and not len(writes)>before:
   spans=[]
   for start in range(len(slines)):
    # Source blank lines alone provide no independent receipt evidence.
    if slines[start] not in expected:continue
    for end in range(start+1,len(slines)+1):
     piece=''.join(slines[start:end])
     if piece not in expected:break
     if end==len(slines) or ''.join(slines[start:end+1]) not in expected:
      if end-start>=2 and piece.strip():spans.append({'start_line':start+1,'end_line':end,'physical_lines':end-start,'slice_sha256':sha(piece),'actually_visible':piece in visible})
   # Keep maximal ranges; include leading/trailing blank lines through expected output matching.
   spans=[s for s in spans if not any(t['start_line']<=s['start_line'] and t['end_line']>=s['end_line'] and t!=s for t in spans)]
   record['source_spans']=spans
   record['complete_units_received']=[uid for uid,u in units.items() if u['text'] in visible and u['text'] in expected]
  else:record['source_spans']=[];record['complete_units_received']=[]
  if error or record['visible_truncation_marker']:
   failed.append({'call_ordinal':current,'output_ordinal':out.get('ordinal'),'replay_error_type':error,'truncated':record['visible_truncation_marker']})
  if error and 'write_text' in script: print('REPLAY_WRITE_ERROR',role,current,error)
  if len(writes)>before:
   d=json.loads(mem[str(F/f'reader-{role}-draft.json')]);sc=json.loads(mem[str(F/f'reader-{role}-self-check.json')]);sr=sc.get('records',sc.get('source_checks'))
   entry=d['answers'][-1];r=sr[-1]
   composition_record={'call_ordinal':current,'prefix_count':len(d['answers']),'id':entry['id'],'entry_sha256':jsha(entry),'record_sha256':jsha(r),
    'during_work_record_matches_question_map_metadata_cases':r['question']==questions[len(d['answers'])-1]['question'] and r['clause_to_unit_map']==entry['clause_ledger'] and r['selected_source_metadata']==entry['operative_sections'] and r['case_conclusions']==entry['case_conclusions'],
    'literal_during_work':checker.check_data(summary,questions[:len(d['answers'])],d,role),
    'draft_prefix_matches_frozen_now':d['answers']==frozen['draft']['answers'][:len(d['answers'])]}
   if not composition or len(d['answers'])>composition[-1]['prefix_count']:composition.append(composition_record)
   if len(d['answers'])==10:
    if frozen_point is None:frozen_point=current
    record['first_ten_replay_byte_binding']={k:sha(mem[str(F/f'reader-{role}-{k}.json')]) for k in ['draft','self-check']}
    record['first_ten_replay_manifest_binding']={k:sha(mem[str(F/f'reader-{role}-{k}.json')])==manifest['files'][f'reader-{role}-{k}.json'] for k in ['draft','self-check']}
  call_records.append(record)
 # Frozen prefix literal checks use both whole original bank and explicit prefix.
 full=checker.check_data(summary,questions,frozen['draft'],role)
 prefix=checker.check_data(summary,questions[:10],frozen['draft'],role)
 per=[]
 for i,(e,r) in enumerate(zip(frozen['draft']['answers'],frozen_records)):
  comp=next(x for x in composition if x['id']==e['id']);previous=composition[i-1]['call_ordinal'] if i else 0
  qreads=[c for c in call_records if previous<c['ordinal']<comp['call_ordinal'] and c['ordinal']>=(228 if role=='a' else 223) and e['id'] in c.get('complete_question_objects_received',[])]
  lastq=qreads[-1]['ordinal'] if qreads else None
  unit_reads=[]
  for s in e['operative_sections']:
   candidates=[c for c in call_records if previous<c['ordinal']<comp['call_ordinal'] and s['section_id'] in c.get('complete_units_received',[])]
   all_prior=[c['ordinal'] for c in call_records if c['ordinal']>=(228 if role=='a' else 223) and c['ordinal']<comp['call_ordinal'] and s['section_id'] in c.get('complete_units_received',[])]
   unit_reads.append({'section_id':s['section_id'],'slice_sha256':s['sha256'],'start_line':s['start_line'],'end_line':s['end_line'],'source_line_count':s['end_line']-s['start_line']+1,'read_call_ordinals':[c['ordinal'] for c in candidates],
     'all_individual_work_source_read_call_ordinals_before_composition':all_prior,
     'visibly_reread_since_previous_composition':bool(candidates),'visibly_reread_after_latest_exact_question':any(lastq is not None and c['ordinal']>lastq for c in candidates),
     'bounded_source_receipt':any(all(sp['physical_lines']<=45 for sp in c.get('source_spans',[])) for c in candidates)})
  per.append({'id':e['id'],'composition_call_ordinal':comp['call_ordinal'],'exact_question_reread_call_ordinals':[c['ordinal'] for c in qreads], 'question_sha256':sha(questions[i]['question']),
   'clause_map_sha256':jsha(e['clause_ledger']),'clause_count':len(e['clause_ledger']),'case_conclusions_plain_strings':isinstance(e['case_conclusions'],list) and all(isinstance(v,str) for v in e['case_conclusions']),
   'case_count':len(e['case_conclusions']),'source_units':unit_reads,
   'frozen_source_record_matches':r['question']==questions[i]['question'] and r['clause_to_unit_map']==e['clause_ledger'] and r['selected_source_metadata']==e['operative_sections'] and r['case_conclusions']==e['case_conclusions'],
   'frozen_entry_matches_composed_entry':jsha(e)==comp['entry_sha256'],'frozen_record_matches_composed_record':jsha(r)==comp['record_sha256'],
   'record_empty_contexts':not r.get('contexts_rechecked',r.get('rechecked_contexts',[])),
   'clause_fields':[sorted(v) for v in e['clause_ledger']]})
 initial=[c for c in call_records if c['ordinal']<first_write]
 summary_receipt=[]
 for c in initial:
  if c.get('source_spans'):summary_receipt.extend([dict(x,call_ordinal=c['ordinal'],output_ordinal=c['output_ordinal']) for x in c['source_spans']])
 terminal_mem_bindings={k:sha(mem[str(F/f'reader-{role}-{k}.json')])==manifest['files'][f'reader-{role}-{k}.json'] for k in ['draft','self-check']}
 result={'role':role,'runtime_read_binding':{'path':str(path),'snapshot_bytes':len(data),'snapshot_sha256':sha(data),'complete_physical_records':len(physical),'live_file_may_grow':True},
 'actual_actor':actor,'all_visible_contexts':contexts,'actor_matches_manifest':actor.get('actor')==manifest['actor'],
 'terminal_prefix_replay_matches_manifest_bytes':terminal_mem_bindings,'first_turn_replay_stops_before_context_ordinal':terminal_before,
 'all_contexts_luna_high':all(x['model']=='gpt-6-luna' and x['effort']=='high' for x in contexts),'first_artifact_write_call_ordinal':first_write,'first_ten_last_composition_call_ordinal':frozen_point,
 'initial_summary_receipts':summary_receipt,'initial_complete_question_ids_received':sorted(set(q for c in initial for q in c.get('complete_question_objects_received',[]))),
 'initial_question_response_counts':[{'call_ordinal':c['ordinal'],'output_ordinal':c['output_ordinal'],'count':len(c['complete_question_objects_received'])} for c in initial if c.get('complete_question_objects_received')],
 'failed_truncated_attempts':failed,'frozen_full_bank_ordered_ids_flag':full['exact_ordered_unique_ids'],'frozen_prefix_ordered_ids_flag':prefix['exact_ordered_unique_ids'],
 'frozen_literal_structure_flag':full['all_structure_and_declared_source_spans_valid'],'frozen_literal_checks':full['checks'],'per_entry_method_records':per,
 'composition_records':composition,'tool_call_records':call_records,'actual_data_reads':reads,'actual_artifact_writes_replayed_in_memory':writes,
 'limits':['Runtime bodies are not copied; bindings refer to physical original records.','Manual source selection is assessed from explicit per-entry constants and serialization flow, not private reasoning.','No semantic coverage or factual grading is performed.','All116-complete admission is out of scope; live continuation remains ongoing.']}
 narrow_physical=[p for p in physical if p['event_type'] in ['session_meta','turn_context'] or p['event_label'] in ['custom_tool_call','custom_tool_call_output','function_call','function_call_output','task_started','task_complete']]
 (OUT/f'reader-{role}-physical-record-bindings.json').write_text(json.dumps(narrow_physical,indent=2)+'\n')
 (OUT/f'reader-{role}-method-evidence.json').write_text(json.dumps(result,indent=2)+'\n')
 return result

if __name__=='__main__':
 results={r:audit(r,p) for r,p in RUNTIMES.items()}
 allowed=['summary-snapshot.md','questions.json','reader-protocol.txt','source-unit-checker.py','reader-dispatch-template.json','parent-record-reader-a-dispatch.txt','parent-record-reader-b-dispatch.txt','reader-continuation-template.json','method-freeze.json']
 files=[binding(F/n) for n in allowed]
 for role in 'ab':
  d=F/'bounded-turn-history'/f'reader-{role}-turn-01'
  for name in ['manifest.json',f'reader-{role}-draft.json',f'reader-{role}-self-check.json']:files.append(binding(d/name))
 (OUT/'input-bindings.json').write_text(json.dumps({'files':files,'summary_physical_LF_lines':len(slines),'question_objects':len(questions),'final_question_id':questions[-1]['id'],'source_units':len(units)},indent=2)+'\n')
 print(json.dumps({r:{'initial_question_count':len(v['initial_complete_question_ids_received']),'first_write':v['first_artifact_write_call_ordinal'],'prefix_last_write':v['first_ten_last_composition_call_ordinal'],'literal_structure':v['frozen_literal_structure_flag'],'prefix_ordered':v['frozen_prefix_ordered_ids_flag'],'failed_attempts':v['failed_truncated_attempts'],'terminal_manifest_binding':v['terminal_prefix_replay_matches_manifest_bytes']} for r,v in results.items()},indent=2))
