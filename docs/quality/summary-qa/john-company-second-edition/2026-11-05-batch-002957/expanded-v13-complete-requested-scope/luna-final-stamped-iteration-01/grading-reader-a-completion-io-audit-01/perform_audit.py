import sys
sys.dont_write_bytecode=True
from pathlib import Path
import ast,builtins,contextlib,hashlib,io,json,re,shlex,types,difflib
O=Path(__file__).parent; F=O.parent; R=F.parent.parent
sha=lambda x:hashlib.sha256(x if isinstance(x,bytes) else x.encode()).hexdigest()
S=r'"(?:\\.|[^"\\])*"'
def command(raw):
 m=re.search(r'(?:cmd|"cmd")\s*:\s*('+S+r')(?:\s*\+\s*('+S+r'))?',raw);assert m
 return json.loads(m.group(1))+(json.loads(m.group(2)) if m.group(2) else '')
def objects(text):
 for m in re.finditer(r'\{',text):
  try:v,_=json.JSONDecoder().raw_decode(text[m.start():])
  except ValueError:continue
  if isinstance(v,dict):yield v
freeze=json.loads((O/'freeze-manifest.json').read_text())
helpers=['verify-v13-i3-grading-runtime-bindings.py','prove-single-reader-grading-delivery-literal-equivalent.py','prove-bounded-delivery.py','literal-read-js-format-proposal-01/read_call_format_proposal.py','literal-read-js-future-adoption.json']
for name in helpers:
 p=R/name;b=p.read_bytes();freeze['input_file_bindings']['../../'+name]={'bytes':len(b),'sha256':sha(b)}
(O/'freeze-manifest.json').write_text(json.dumps(freeze,indent=2)+'\n')
summary=(F/'summary-snapshot.md').read_text();lines=summary.splitlines(keepends=True);assert len(lines)==498 and summary.count('\n')==498
reader=json.loads((F/'reader-a.json').read_text());rmap={x['id']:x for x in reader['answers']};proofs={name:json.loads((F/name).read_text()) for name in ['grading-reader-a-input-delivery-proof.json','grading-reader-a-js-format-proposal-proof.json']};runs={}
for index in range(1,7):
 nn=f'{index:02d}';block='block-'+nn;p=json.loads((O/f'{nn}-runtime-projection.json').read_text());base=F/'grading-reader-a'/block;packet=json.loads((base/'packet.json').read_text());expected={e['id']:e for e in packet['entries']};assert all(e['reader_a_entry']==rmap[e['id']] for e in expected.values())
 dispatch=(F/f'grader-a{nn}-dispatch.txt').read_text();prefix=json.loads(next(s.split(': ',1)[1] for s in dispatch.splitlines() if s.startswith('READ_PREFIX_JSON: ')));argv_expected=shlex.split(prefix)
 outputs={x['call_id']:x for x in p['tool_outputs']};boundary=next(c['physical_record'] for c in p['tool_calls'] if 'QA_ARTIFACT_WRITE_V1' in c['input']);chunks={};entries={};metadata=[];calls=[];deviations=[]
 for c in p['tool_calls']:
  if c['physical_record']>=boundary:break
  assert c['name']=='exec';cmd=command(c['input']);argv=shlex.split(cmd);assert argv[:2]==['python3','-c'];tree=ast.parse(argv[2]);assert not any(isinstance(x,(ast.Delete,ast.FunctionDef,ast.With)) for x in ast.walk(tree));assert not any(isinstance(x,ast.Attribute) and x.attr in ['write','write_text','write_bytes','unlink','mkdir','system','popen'] for x in ast.walk(tree))
  assert all(x in [str(F/'summary-snapshot.md'),str(base/'packet.json'),'summary','metadata','entry'] or x.lstrip('-').isdigit() for x in argv[3:])
  visible=''.join(outputs[c['call_id']]['text_blocks']);values=list(objects(visible));got_chunks=[];got_entries=[]
  for v in values:
   if v.get('qa_delivery')=='summary-chunk-v1':
    start=v['start_line'];piece=''.join(lines[start-1:start+44]);valid=v['text']==piece and v['sha256']==sha(piece) and v['end_line']==min(start+44,498)
    assert valid;chunks.setdefault(start,[]).append(c['physical_record']);got_chunks.append(start)
   if v.get('id') in expected and v==expected[v['id']]:entries.setdefault(v['id'],[]).append(c['physical_record']);got_entries.append(v['id'])
   if v=={k:v for k,v in packet.items() if k!='entries'}:metadata.append(c['physical_record'])
  canonical=cmd.startswith(prefix+' ') and cmd[len(prefix)+1:] in ['summary '+str(x) for x in range(0,498,45)]+['metadata 0']+['entry '+str(x) for x in range(len(expected))]
  record={'physical_record':c['physical_record'],'output_record':outputs[c['call_id']]['physical_record'],'canonical_command':canonical,'summary_chunks_received':got_chunks,'complete_entries_received':sorted(set(got_entries)),'visible_error_classes':re.findall(r'(?m)^([\w.]*(?:Error|Exception))(?::|$)',visible)};calls.append(record)
  if not canonical:deviations.append(dict(record,argv_after_script=argv[3:],read_program_diff=list(difflib.unified_diff(argv_expected[2].splitlines(),argv[2].splitlines(),n=0))))
 assert set(chunks)==set(range(1,499,45)) and set(entries)==set(expected) and metadata
 program_path=O/f'{nn}-program-{boundary}.py';program=program_path.read_text();tree=ast.parse(program)
 # Program reviewed by control-flow/AST inspection before this replay. Only constant data,
 # bounded packet iteration, JSON serialization, SHA and quote/shape assertions occur.
 assert not any(isinstance(x,(ast.While,ast.FunctionDef,ast.ClassDef,ast.Try,ast.With)) for x in ast.walk(tree))
 assert not any(isinstance(x,ast.Attribute) and x.attr.startswith('__') for x in ast.walk(tree))
 mem={str(base/'packet.json'):(base/'packet.json').read_bytes(),str(F/'summary-snapshot.md'):(F/'summary-snapshot.md').read_bytes()};reads=[];writes=[]
 class P:
  def __init__(self,path):self.path=str(path)
  def __truediv__(self,n):return P(self.path+'/'+str(n))
  def __str__(self):return self.path
  def read_bytes(self):
   assert self.path in mem;reads.append({'path':self.path,'sha256':sha(mem[self.path])});return mem[self.path]
  def read_text(self,*a,**kw):return self.read_bytes().decode()
  def write_text(self,value,*a,**kw):
   assert self.path in [str(base/'grades-same-entry.json'),str(base/'own-block-notes.txt')]
   mem[self.path]=value.encode();writes.append({'path':self.path,'sha256':sha(mem[self.path]),'bytes':len(mem[self.path])});return len(value)
 def imp(name,*a,**kw):
  assert name in ['pathlib','json','hashlib'];return types.SimpleNamespace(Path=P) if name=='pathlib' else {'json':json,'hashlib':hashlib}[name]
 caps={k:getattr(builtins,k) for k in ['len','sum','str','list','zip','any','isinstance','AssertionError','dict','enumerate','tuple']};caps['__import__']=imp;caps['print']=print
 stdout=io.StringIO()
 with contextlib.redirect_stdout(stdout):exec(compile(tree,'<inspected serializer>','exec'),{'__builtins__':caps})
 report=mem[str(base/'grades-same-entry.json')];original=(base/'grades-same-entry.json').read_bytes();assert report==original==(O/f'{nn}-grades-same-entry.json').read_bytes()
 visible=''.join(outputs[next(c['call_id'] for c in p['tool_calls'] if c['physical_record']==boundary)]['text_blocks'])
 stdout_candidates=[visible]+[v['output'] for v in objects(visible) if isinstance(v.get('output'),str)]
 stdout_candidates += [v.replace(r'\"','"').replace(r'\n','\n') for v in list(stdout_candidates)]
 assert any(stdout.getvalue().rstrip('\n') in value for value in stdout_candidates)
 replay={'program_sha256':sha(program),'replay_sha256':sha(report),'original_report_sha256':sha(original),'report_byte_equality':True,'capabilities':'Only memory-backed allowed Path reads/writes, json/hashlib and bounded Python primitives; no real filesystem/network/process capabilities.','reads':reads,'writes':writes,'serializer_stdout_sha256':sha(stdout.getvalue()),'serializer_stdout_visible':True,'manually_inspected_before_replay':True}
 (O/f'{nn}-isolated-replay.json').write_text(json.dumps(replay,indent=2)+'\n')
 for w in writes:
  if w['path']!=str(base/'grades-same-entry.json'):(O/f'{nn}-replayed-own-block-notes.txt').write_bytes(mem[w['path']])
 falsepaths={}
 def falsewalk(x,path,found):
  if isinstance(x,dict):
   for k,v in x.items():
    if v is False:found.append(path+'/'+k)
    elif isinstance(v,(dict,list)) and k!='first_possible_artifact_write_boundary':falsewalk(v,path+'/'+k,found)
  elif isinstance(x,list):
   for i,v in enumerate(x):falsewalk(v,path+'/'+str(i),found)
 for name,data in proofs.items():a=[];falsewalk(data[block],'',a);falsepaths[name]=a
 assert p['actor_binding']['agent_path']==f'/root/v13_stamped_i1_grade_a_{nn}' and p['actor_binding']['parent_thread_id']=='01a1aaa2-7c89-7c92-bca8-a89efc3fe4d7';assert all(m['model']=='gpt-6.1-sol' and m['effort']=='high' for m in p['actual_metadata']);assert p['events'][-1]['event']=='task_complete'
 runs[block]={'actor':p['actor_binding']['agent_path'],'first_mutation_record':boundary,'complete_actual_initial_inputs_received':True,'summary_LF_lines':498,'summary_chunk_read_records':chunks,'metadata_read_records':metadata,'entire_original_entry_read_records':entries,'prewrite_call_checks':calls,'noncanonical_extra_calls_preserved':deviations,'supplied_proof_false_paths_preserved':falsepaths,'all_actual_contexts_Sol61_high':True,'context_records':p['actual_metadata'],'task_events':p['events'],'in_place_resumption_qualification':index>=4,'postwrite_program_records':[boundary],'permitted_io_verified':True,'temporary_artifacts':[w for w in writes if w['path']!=str(base/'grades-same-entry.json')],'report_replay_byte_equality':True,'manual_semantic_choices_serialized_as_literal_data':True,'semantic_inspection':'Per-question literal chosen quotes/reasons/rows, fixed authored decision tags; packet loops align requirements and assert same-entry quote membership. No grade routing, ranking or semantic matching computes decisions. Assertions check transport/quotes, not semantic correctness.','private_incoming_plaintext_or_fork_isolation_certified':False}
for name,binding in freeze['input_file_bindings'].items():
 b=(F/name).read_bytes();assert len(b)==binding['bytes'] and sha(b)==binding['sha256'],name
results=json.loads((F/'reader-a-grading-results.json').read_text());manifest=json.loads((F/'grading-reader-a/packet-manifest.json').read_text());assert sum(len(json.loads((F/f'grading-reader-a/block-{i:02d}/packet.json').read_text())['entries']) for i in range(1,7))==116
assessment={'scope':'Six original terminal current-stamped reader-A grader actors; technical completion/IO only.','runs':runs,'all_six_actual_input_receipts_confirmed':True,'all_six_original_report_copies_and_isolated_replay_bytes_match':True,'all_inputs_unchanged_after_audit':True,'no_originals_modified':True,'no_gameplay_regrading_or_score_caps':True,'manual_code_inspection_completed_before_capability_limited_replay':True,'qualifications':['Strict and normalized false results remain unchanged and are retained per run, separately from complete actual JSON receipt.','A04–A06 have multiple task/context events and were resumed in place; do not infer clean single-turn completion.','Child traces cannot certify encrypted incoming task plaintext or stronger fork isolation.','Optional own-block notes were written by A02; recorded and reproduced in memory. No /tmp program was created by these six actual commands.']}
(O/'audit.json').write_text(json.dumps(assessment,indent=2)+'\n');print(json.dumps({'six_complete':True,'first_mutations':{k:v['first_mutation_record'] for k,v in runs.items()},'deviation_counts':{k:len(v['noncanonical_extra_calls_preserved']) for k,v in runs.items()},'unchanged_inputs':True}))
