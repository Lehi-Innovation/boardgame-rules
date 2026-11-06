import sys
sys.dont_write_bytecode=True
import pathlib,json,re,ast,shlex,hashlib,difflib,datetime
O=pathlib.Path(__file__).parent;I=O.parents[1];H=lambda b:hashlib.sha256(b).hexdigest()
def put(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
ns={'__name__':'source_checker_audit'};exec(compile((I/'source-unit-checker.py').read_text(),str(I/'source-unit-checker.py'),'exec'),ns)
summary=(I/'summary-snapshot.md').read_text();questions=json.loads((I/'questions.json').read_text())['questions'];units=ns['units'](summary)
def command(c):
 m=re.search(r'(?:"cmd"|cmd)\s*:\s*("(?:\\.|[^"\\])*")',c['input']);return json.loads(m[1]) if m else None
def code_for(c):
 cmd=command(c)
 if not cmd:return None
 if "<<'PY'\n"in cmd:return cmd.split("<<'PY'\n",1)[1].rsplit('\nPY',1)[0]
 try:
  a=shlex.split(cmd);return a[a.index('-c')+1] if '-c'in a else None
 except ValueError:return None
def decoder(t):
 try:return json.JSONDecoder().raw_decode(t.lstrip())[0]
 except (ValueError,TypeError):return None
def question_received(q,text):
 d=decoder(text)
 if d==q or isinstance(d,dict)and d.get('question')==q or q['question']+'\n' in text:return True
 # Prefix/status text may precede an otherwise complete original JSON object.
 return any(decoder(text[m.start():])==q for m in re.finditer(r'\{',text))
def unit_receipt(u,outs):
 lines=u['text'].splitlines(keepends=True);coverage=set();chunks=[];numbered=[]
 for out in outs:
  rendered=out['text'].splitlines(keepends=True)
  for b in difflib.SequenceMatcher(None,lines,rendered,autojunk=False).get_matching_blocks():
   if not b.size:continue
   matched=lines[b.a:b.a+b.size]
   # Exclude isolated blank-line matches; all retained blocks are exact LF slices.
   if not any(x.strip()for x in matched):continue
   coverage.update(range(b.a,b.a+b.size));chunks.append({'output_record':out['physical_record'],'unit_line_first':b.a+1,'unit_line_last':b.a+b.size,'source_physical_first':u['start_line']+b.a,'source_physical_last':u['start_line']+b.a+b.size-1,'exact_slice_sha256':H(''.join(matched).encode()),'source_line_count':b.size,'within_45':b.size<=45})
 raw_missing=[u['start_line']+i for i in range(len(lines))if i not in coverage]
 decorated=set()
 for out in outs:
  received=[]
  for rendered in out['text'].splitlines(keepends=True):
   match=re.match(r'^(\d+):',rendered)
   if not match:continue
   physical=int(match[1]);offset=physical-u['start_line']
   if not 0<=offset<len(lines):continue
   rest=rendered[match.end():]
   if rest==lines[offset] or rest.startswith(' ')and rest[1:]==lines[offset]:decorated.add(offset);received.append(physical)
  if received:numbered.append({'output_record':out['physical_record'],'exact_full_LF_lines_after_removing_only_visible_number_prefix':received})
 missing=[u['start_line']+i for i in range(len(lines))if i not in coverage|decorated]
 # Blank-only edges also require literal receipt adjacent to a substantive exact block.
 for out in outs:
  for c in list(chunks):
   if c['output_record']!=out['physical_record']:continue
   st=c['unit_line_first']-1;en=c['unit_line_last']
   while st>0 and not lines[st-1].strip() and ''.join(lines[st-1:en])in out['text']:st-=1
   while en<len(lines) and not lines[en].strip() and ''.join(lines[st:en+1])in out['text']:en+=1
   coverage.update(range(st,en))
 raw_missing=[u['start_line']+i for i in range(len(lines))if i not in coverage]
 missing=[u['start_line']+i for i in range(len(lines))if i not in coverage|decorated]
 return {'section_id':u['section_id'],'full_unit_sha256':u['sha256'],'start_line':u['start_line'],'end_line':u['end_line'],'exact_received_chunks':chunks,'raw_unmodified_slice_missing_lines':raw_missing,'numbered_lossless_line_receipts':numbered,'missing_physical_lines':missing,'complete_receipt':not missing,'all_contiguous_received_blocks_within_45':all(c['within_45']for c in chunks)and all(len(x['exact_full_LF_lines_after_removing_only_visible_number_prefix'])<=45 for x in numbered)}
report={'scope':'Frozen prefix-only method audit; no gameplay grading or private-attention inference.','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'question_count':len(questions),'readers':{},'prior_qualifications_bound_to':['first-ten-prefix-method-audit-01/audit.json','first-ten-procedure-completion-audit-02/audit.json']}
for role in 'a':
 p=json.loads((O/f'prefix-reader-{role}-runtime-projection.json').read_text());d=json.loads((O/f'prefix-reader-{role}-draft.json').read_text());sc=json.loads((O/f'prefix-reader-{role}-self-check.json').read_text());records=sc.get('checks',sc.get('records'));outs=p['tool_outputs'];outmap={x['call_id']:x for x in outs}
 for x in outs:x['text']=''.join(x['visible_text_blocks'][1:])
 calls=[];appends={};attempts=[];external=[];turn=0;turn_by_record={}
 for r in p['records']:
  if r['payload_type']=='task_started':turn+=1
  turn_by_record[r['physical_record']]=turn
 for c in p['tool_calls']:
  code=code_for(c);out=outmap.get(c['call_id']);text=out['text']if out else '';tree=None
  try:tree=ast.parse(code)if code else None
  except SyntaxError:pass
  append=False;ids=[]
  if tree:
   for n in ast.walk(tree):
    if isinstance(n,ast.Dict):
     for k,v in zip(n.keys,n.values):
      if isinstance(k,ast.Constant)and k.value=='id'and isinstance(v,ast.Constant)and isinstance(v.value,str)and re.fullmatch(r'Q\d{3}',v.value):ids.append(v.value)
    if isinstance(n,ast.Call)and isinstance(n.func,ast.Attribute)and n.func.attr=='append'and isinstance(n.func.value,ast.Subscript):
     if isinstance(n.func.value.slice,ast.Constant)and n.func.value.slice.value=='answers':append=True
  bad=bool(re.search(r'Traceback \(most recent call last\)|SyntaxError:|/bin/bash:.*(?:error|unexpected)',text,re.S))
  if append:
   qid=max(set(ids),default=None)
   attempts.append({'call_record':c['physical_record'],'question_id':qid,'output_record':out['physical_record']if out else None,'visible_execution_error':bad})
   if qid and not bad and qid not in appends:appends[qid]=c
  paths=sorted(set(re.findall(r'/home/jonny/projects/boardgame-rules[^\s\"\'\\;()]*',code or '')))
  outside=[z for z in paths if not(z==str(I)or z.startswith(str(I)+'/'))]
  if outside:external.append({'call_record':c['physical_record'],'attempted_paths':outside,'visible_error':bad,'output_sha256':H(text.encode())})
  calls.append({'call_record':c['physical_record'],'tool':c['name'],'python_parsed':tree is not None,'answers_append':append,'literal_entry_ids':sorted(set(ids)),'visible_execution_error':bad,'command_sha256':H((command(c)or c['input']).encode()),'control_constructs':[ast.unparse(n)for n in ast.walk(tree)if isinstance(n,(ast.For,ast.While,ast.If,ast.FunctionDef))]if tree else []})
 firstwrites=[246,260,274,288,302,316,330,344,358,372]if role=='a'else[263,284,303,322,341,367,386,405,424,449]
 bycall={c['physical_record']:c for c in p['tool_calls']}
 for n,write in enumerate(firstwrites,1):appends[f'Q{n:03d}']=bycall[write]
 entries=[];previous=219 if role=='a'else 238
 for q,e,record in zip(questions,d['answers'],records):
  c=appends.get(q['id']);write=c['physical_record']if c else None
  window=[x for x in outs if previous<x['physical_record']<(write or 0)]
  rereads=[x['physical_record']for x in window if question_received(q,x['text'])]
  receipts=[unit_receipt(units[m['section_id']],window)for m in e['operative_sections']if m['section_id']in units]
  literal=ns['check_data'](summary,questions,{'answers':[e]},role)['checks'][0]
  entries.append({'id':q['id'],'turn':turn_by_record.get(write),'first_successful_composition_append_call':write,'exact_question_reread_output_records':rereads,'source_unit_receipts':receipts,'actual_manual_selection_and_case_evidence_call':write,'source_record_same_entry_alignment':record.get('question')==q['question']and record.get('clause_map',record.get('clause_to_unit_map'))==e['clause_ledger']and record.get('selected_source_metadata')==e['operative_sections'],'during_work_source_record_written_in_composition_call':bool(c and ('self-check.json'in c['input']or "cp="in c['input'])),'plain_case_strings':isinstance(e.get('case_conclusions'),list)and all(isinstance(v,str)for v in e.get('case_conclusions',[])),'case_placement':not e.get('case_conclusions')or e['answer'].startswith(e['case_conclusions'][0])or e['answer'].startswith('Case conclusion: '+e['case_conclusions'][0]),'literal_checks':literal})
  if c and c['call_id']in outmap:previous=outmap[c['call_id']]['physical_record']
 put(f'prefix-reader-{role}-per-entry-method.json',entries);put(f'prefix-reader-{role}-call-method-records.json',{'calls':calls,'append_attempts':attempts,'outside_assigned_base_path_attempts':external})
 snapshots=[]
 for folder in sorted((I/'bounded-turn-history').glob(f'reader-{role}-turn-*')):
  mp=folder/'manifest.json';m=json.loads(mp.read_text());fs={}
  for name,expected in m.get('files',{}).items():
   fp=folder/name;b=fp.read_bytes();fs[name]={'bytes':len(b),'sha256':H(b),'manifest_hash_matches':H(b)==expected}
  snapshots.append({'manifest_path':str(mp),'manifest_sha256':H(mp.read_bytes()),'turn':m.get('turn'),'prefix':m.get('ordered_prefix'),'source_records':m.get('source_records'),'files':fs})
 put(f'prefix-reader-{role}-bounded-snapshot-bindings.json',snapshots)
 counts={}
 for e in entries:counts[str(e['turn'])]=counts.get(str(e['turn']),0)+1
 report['readers'][role]={'available_prefix':len(d['answers']),'available_source_records':len(records),'prefix_runtime_bytes':p['prefix_bytes'],'prefix_runtime_sha256':p['prefix_sha256'],'runtime_last_event':p['task_events'][-1],'all_contexts_luna_high':all(m.get('model')=='gpt-6-luna'and m.get('effort')=='high'for m in p['actual_metadata']if'model'in m),'actual_metadata':p['actual_metadata'],'new_question_counts_by_turn':counts,'all_turns_at_most_ten_new_entries':all(n<=10 for n in counts.values()),'ordered_unique_available_prefix':[e['id']for e in d['answers']]==[q['id']for q in questions[:len(d['answers'])]],'full_bank_terminal_admission':False,'admission_reason':'Terminal candidate: final admission is assessed separately after manual review and root terminal confirmation.','questions_without_exact_reread':[e['id']for e in entries if not e['exact_question_reread_output_records']],'unit_receipt_gaps':[{'id':e['id'],'unit':u['section_id'],'missing_lines':u['missing_physical_lines']}for e in entries for u in e['source_unit_receipts']if not u['complete_receipt']],'source_blocks_over_45':[{'id':e['id'],'unit':u['section_id'],'blocks':[b for b in u['exact_received_chunks']if not b['within_45']]}for e in entries for u in e['source_unit_receipts']if not u['all_contiguous_received_blocks_within_45']],'source_record_alignment_failures':[e['id']for e in entries if not e['source_record_same_entry_alignment']],'nonplain_case_arrays':[e['id']for e in entries if not e['plain_case_strings']],'case_placement_qualifications':[e['id']for e in entries if not e['case_placement']],'literal_check_failures':[e['id']for e in entries if not e['literal_checks']['all_structure_and_declared_source_spans_valid']],'outside_assigned_base_path_attempts':external,'limits':'Per-entry delivery is exact LF transport evidence, not semantic adequacy. Current saved selection checked against pre-composition window; later narrow mechanical revisions are separately inspectable in complete call projections.'}
report['history_qualifications']='Initial oversized question responses and bounded repair history, syntactic compound-map rows, A grouped repair/revisit sequencing and incomplete deviation notes remain as established by this agent’s two earlier audits. None is a factual score cap.'
report['method_limits']='Literal source slicing/hash/serialization and explicit manually supplied per-entry clause/case text are allowed. No private reasoning/messages retained. Append detection is syntactic and all unresolved receipt/parse cases require technical qualification rather than invented success.'
put('prefix-audit.json',report)
print(json.dumps({r:{k:v for k,v in report['readers'][r].items()if k in ['available_prefix','all_contexts_luna_high','new_question_counts_by_turn','questions_without_exact_reread','unit_receipt_gaps','source_blocks_over_45','source_record_alignment_failures','case_placement_qualifications','literal_check_failures','outside_assigned_base_path_attempts']}for r in 'a'},indent=2))
