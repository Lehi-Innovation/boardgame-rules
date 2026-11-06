import sys
sys.dont_write_bytecode=True
from pathlib import Path
import ast,builtins,contextlib,hashlib,io,json,re,shlex,types,difflib
O=Path(__file__).parent;F=O.parent;R=F.parent.parent;sha=lambda x:hashlib.sha256(x if isinstance(x,bytes) else x.encode()).hexdigest();S=r'"(?:\\.|[^"\\])*"'
def command(raw):
 m=re.search(r'(?:cmd|"cmd")\s*:\s*('+S+r')(?:\s*\+\s*('+S+r'))?',raw);assert m
 return json.loads(m.group(1))+(json.loads(m.group(2)) if m.group(2) else '')
def objects(text):
 for m in re.finditer(r'\{',text):
  try:v,_=json.JSONDecoder().raw_decode(text[m.start():])
  except ValueError:continue
  if isinstance(v,dict):yield v
stage=int(sys.argv[1]);assert stage in [5,6]
summary=(F/'summary-snapshot.md').read_text();lines=summary.splitlines(keepends=True);assert len(lines)==498 and summary.count('\n')==498
reader=json.loads((F/'reader-b.json').read_text());rmap={e['id']:e for e in reader['answers']};runs={}
for index in range(1,stage+1):
 nn=f'{index:02d}';block='block-'+nn;p=json.loads((O/f'{nn}-runtime-projection.json').read_text());assert p['events'][-1]['event']=='task_complete';base=F/'grading-reader-b'/block;packet=json.loads((base/'packet.json').read_text());expected={e['id']:e for e in packet['entries']};assert all(e['reader_b_entry']==rmap[e['id']] for e in expected.values())
 dispatch=(F/f'grader-b{nn}-dispatch.txt').read_text();prefix=json.loads(next(s.split(': ',1)[1] for s in dispatch.splitlines() if s.startswith('READ_PREFIX_JSON: ')));avexpected=shlex.split(prefix);outs={x['call_id']:x for x in p['tool_outputs']};boundary=next(c['physical_record'] for c in p['tool_calls'] if 'QA_ARTIFACT_WRITE_V1' in c['input']);chunks={};entries={};metadata=[];calls=[];deviations=[]
 for c in p['tool_calls']:
  if c['physical_record']>=boundary:break
  assert c['name']=='exec';cmd=command(c['input']);av=shlex.split(cmd);assert av[:2]==['python3','-c'];tree=ast.parse(av[2]);assert not any(isinstance(n,(ast.Delete,ast.With,ast.FunctionDef)) for n in ast.walk(tree));assert not any(isinstance(n,ast.Attribute) and n.attr in ['write','write_bytes','write_text','unlink','system','popen'] for n in ast.walk(tree));assert all(x in [str(F/'summary-snapshot.md'),str(base/'packet.json'),'summary','entry','metadata'] or x.lstrip('-').isdigit() for x in av[3:])
  visible=''.join(outs[c['call_id']]['text_blocks']);values=list(objects(visible));received_chunks=[];received_entries=[]
  for v in values:
   if v.get('qa_delivery')=='summary-chunk-v1':
    start=v['start_line'];part=''.join(lines[start-1:start+44]);assert v['text']==part and v['sha256']==sha(part) and v['end_line']==min(start+44,498);chunks.setdefault(start,[]).append(c['physical_record']);received_chunks.append(start)
   if v.get('id') in expected and v==expected[v['id']]:entries.setdefault(v['id'],[]).append(c['physical_record']);received_entries.append(v['id'])
   if v=={k:v for k,v in packet.items() if k!='entries'}:metadata.append(c['physical_record'])
  canonical=cmd.startswith(prefix+' ') and cmd[len(prefix)+1:] in ['summary '+str(x) for x in range(0,498,45)]+['metadata 0']+['entry '+str(x) for x in range(len(expected))]
  call={'physical_record':c['physical_record'],'output_record':outs[c['call_id']]['physical_record'],'canonical_fixed_command':canonical,'received_summary_chunks':received_chunks,'received_complete_entry_ids':sorted(set(received_entries)),'visible_error_classes':re.findall(r'(?m)^([\w.]*(?:Error|Exception))(?::|$)',visible)};calls.append(call)
  if not canonical:deviations.append(dict(call,argv_after_script=av[3:],read_program_diff=list(difflib.unified_diff(avexpected[2].splitlines(),av[2].splitlines(),n=0))))
 assert set(chunks)==set(range(1,499,45)) and set(entries)==set(expected) and metadata
 post=[c for c in p['tool_calls'] if c['physical_record']>=boundary];assert len(post)==1
 program_path=O/f'{nn}-program-{boundary}.py';program=program_path.read_text();tree=ast.parse(program)
 # Original control flow and literal decision data inspected before capability-limited replay.
 assert not any(isinstance(n,(ast.While,ast.FunctionDef,ast.ClassDef,ast.With,ast.Try)) for n in ast.walk(tree));assert not any(isinstance(n,ast.Attribute) and n.attr.startswith('__') for n in ast.walk(tree))
 mem={str(base/'packet.json'):(base/'packet.json').read_bytes(),str(F/'summary-snapshot.md'):(F/'summary-snapshot.md').read_bytes()};reads=[];writes=[]
 class P:
  def __init__(self,path):self.path=str(path)
  def __truediv__(self,x):return P(self.path+'/'+str(x))
  def __str__(self):return self.path
  def with_name(self,name):return P(self.path.rsplit('/',1)[0]+'/'+str(name))
  def read_bytes(self):assert self.path in mem;reads.append({'path':self.path,'sha256':sha(mem[self.path])});return mem[self.path]
  def read_text(self,*a,**kw):return self.read_bytes().decode()
  def write_bytes(self,value):
   assert self.path in [str(base/'grades-same-entry.json'),str(base/'own-block-notes.txt')];assert isinstance(value,bytes);mem[self.path]=value;writes.append({'path':self.path,'sha256':sha(value),'bytes':len(value)});return len(value)
  def write_text(self,value,*a,**kw):self.write_bytes(value.encode());return len(value)
 def imp(name,*a,**kw):assert name in ['pathlib','json','hashlib'];return types.SimpleNamespace(Path=P) if name=='pathlib' else {'json':json,'hashlib':hashlib}[name]
 caps={k:getattr(builtins,k) for k in ['len','sum','str','list','zip','any','all','isinstance','AssertionError','dict','enumerate','tuple']};caps['__import__']=imp;caps['print']=print;capture=io.StringIO()
 with contextlib.redirect_stdout(capture):exec(compile(tree,'<inspected grader serializer>','exec'),{'__builtins__':caps})
 report=mem[str(base/'grades-same-entry.json')];assert report==(base/'grades-same-entry.json').read_bytes()==(O/f'{nn}-grades-same-entry.json').read_bytes()
 visible=''.join(outs[post[0]['call_id']]['text_blocks']);candidates=[visible]+[v['output'] for v in objects(visible) if isinstance(v.get('output'),str)];candidates += [s.replace(r'\"','"').replace(r'\n','\n') for s in list(candidates)];assert any(capture.getvalue().rstrip('\n') in s for s in candidates)
 replay={'program_sha256':sha(program),'replay_sha256':sha(report),'original_report_sha256':sha((base/'grades-same-entry.json').read_bytes()),'report_byte_equality':True,'manually_inspected_before_replay':True,'isolated_capabilities':'Only memory-backed own packet/output Path methods, json/hashlib and finite Python primitives; no real filesystem/network/process access.','reads':reads,'writes':writes,'serializer_stdout_sha256':sha(capture.getvalue()),'serializer_stdout_visible':True};(O/f'{nn}-isolated-replay.json').write_text(json.dumps(replay,indent=2)+'\n')
 assert p['actor_binding']['agent_path']==f'/root/v13_stamped_i1_grade_b_{nn}' and p['actor_binding']['parent_thread_id']=='01a1aaa2-7c89-7c92-bca8-a89efc3fe4d7';assert all(c['model']=='gpt-6.1-sol' and c['effort']=='high' for c in p['actual_metadata'])
 runs[block]={'actor':p['actor_binding']['agent_path'],'first_mutation_record':boundary,'complete_actual_inputs_received_before_mutation':True,'source_physical_LF_lines':498,'summary_chunk_records':chunks,'metadata_records':metadata,'entire_original_entry_records':entries,'prewrite_call_checks':calls,'noncanonical_extra_calls':deviations,'all_actual_contexts_Sol61_high':True,'contexts':p['actual_metadata'],'task_events':p['task_event_metadata'],'actual_postwrite_program_records':[boundary],'all_actual_postwrite_calls_inspected':True,'report_copy_and_replay_byte_equality':True,'permitted_io_verified':True,'manual_literal_semantic_decision_serialization_observed':True,'semantic_inspection_limit':'Literal per-question choices/quotes/reasons with constant tags and finite authored repetitions/ID-specific additions. Assertions check atom/quote transport; no semantic matching/ranking computes grades. Private cognitive review not certified.','private_incoming_plaintext_or_stronger_fork_isolation_certified':False}
for name,v in json.loads((O/'stage-01-freeze-manifest.json').read_text())['input_file_bindings'].items():b=(F/name).read_bytes();assert len(b)==v['bytes'] and sha(b)==v['sha256']
assessment={'scope':f'{stage} completed original reader-B grading traces; sixth remains pending unless stage6.','runs':runs,'all_six_technical_audit_complete':stage==6,'originals_unchanged':True,'no_gameplay_regrading_or_factual_format_caps':True};(O/('stage-01-five-run-assessment.json' if stage==5 else 'audit.json')).write_text(json.dumps(assessment,indent=2)+'\n');print(json.dumps({'completed_traces_audited':stage,'actual_complete_inputs_all':True,'all_original_report_byte_replays_equal':True,'noncanonical_counts':{k:len(v['noncanonical_extra_calls']) for k,v in runs.items()}}))
