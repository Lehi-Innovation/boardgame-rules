import sys
sys.dont_write_bytecode=True
import pathlib,json,hashlib,ast,re,shlex,types
O=pathlib.Path(__file__).parent;I=O.parent;B=I.parents[1];H=lambda b:hashlib.sha256(b).hexdigest()
def put(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def command(c):
 m=re.search(r'(?:"cmd"|cmd)\s*:\s*("(?:\\.|[^"\\])*")(?:\s*\+\s*("(?:\\.|[^"\\])*"))?',c['input']);return json.loads(m[1])+(json.loads(m[2])if m[2]else'')if m else None
helper=B/'prove-single-reader-grading-delivery-literal-equivalent.py';ht=ast.parse(helper.read_text());read_script=next(ast.literal_eval(n.value)for n in ht.body if isinstance(n,ast.Assign)and any(isinstance(z,ast.Name)and z.id=='READ_SCRIPT'for z in n.targets))
summary=(I/'summary-snapshot.md').read_text();lines=summary.splitlines(keepends=True);rawreader=json.loads((I/'reader-a.json').read_text());qbank=json.loads((I/'questions.json').read_text())['questions'];strict=json.loads((I/'grading-reader-a-input-delivery-proof.json').read_text());normalized=json.loads((I/'grading-reader-a-js-format-proposal-proof.json').read_text());manifest=json.loads((I/'grading-reader-a/packet-manifest.json').read_text());allids=[];totalatoms=0;result={}
# Reviewed parser has no import-time runtime/data access. Import only canonical function
# through compile/exec, never its proof entrypoint or frozen_packets/path readers.
parser=B/'literal-read-js-format-proposal-01/read_call_format_proposal.py';parserns={'__name__':'isolated_parser_audit','__file__':str(parser)};exec(compile(parser.read_text(),str(parser),'exec'),parserns)
for role in [f'{n:02d}'for n in range(1,7)]:
 block='block-'+role;proj=json.loads((O/f'{role}-runtime-projection.json').read_text());packetraw=(O/f'{role}-packet.json').read_bytes();packet=json.loads(packetraw);reportpath=I/'grading-reader-a'/block/'grades-same-entry.json';packetpath=I/'grading-reader-a'/block/'packet.json';report=(O/f'{role}-grades-same-entry.json').read_bytes();boundary=strict[block]['first_possible_artifact_write_boundary']['call_id'];bc=next(c for c in proj['tool_calls']if c['call_id']==boundary);before=[c for c in proj['tool_calls']if c['physical_record']<bc['physical_record']];outmap={x['call_id']:x for x in proj['tool_outputs']};seen_s={};seen_e={};seen_m=[];errors=[];read_records=[]
 metadata={k:v for k,v in packet.items()if k!='entries'}
 for c in before:
  body=c['input'].strip()
  if body.startswith('// @exec:'):body=body.split('\n',1)[1].strip()
  assert parserns['canonical_read_body'](body) is not None, ('unexpected-whole-wrapper',c['physical_record'])
  cmd=command(c);args=shlex.split(cmd)if cmd else[];out=outmap.get(c['call_id']);text=''.join(out['text_blocks'][1:])if out else'';record={'call_record':c['physical_record'],'output_record':out['physical_record']if out else None,'command_sha256':H((cmd or'').encode())};approved=False
  if len(args)==7 and args[:2]==['python3','-c']and args[2]==read_script and args[3:5]==[str(I/'summary-snapshot.md'),str(packetpath)]:
   mode,index=args[5],int(args[6]);expected=None
   if mode=='summary':
    chunk=''.join(lines[index:index+45]);expected={'qa_delivery':'summary-chunk-v1','start_line':index+1,'end_line':min(index+45,len(lines)),'text':chunk,'sha256':H(chunk.encode())}
   elif mode=='entry':expected=packet['entries'][index]
   elif mode=='metadata':expected=metadata
   try:actual=json.JSONDecoder().raw_decode(text.lstrip())[0]
   except ValueError:actual=None
   approved=actual==expected and expected is not None;record.update(mode=mode,index=index,exact_visible_value_equals_original=approved)
   if approved:
    if mode=='summary':seen_s[index]=out['physical_record']
    elif mode=='entry':seen_e[index]=out['physical_record']
    else:seen_m.append(out['physical_record'])
  else:
   record['exact_fixed_program']=len(args)>=3 and args[2]==read_script;record['argument_count_after_script']=max(0,len(args)-3);record['visible_failure_before_Path_read']=bool(record['exact_fixed_program']and len(args)-3!=4 and 'ValueError: not enough values to unpack' in text);record['visible_output_sha256']=H(text.encode());errors.append(record)
  read_records.append(record)
 # Independent object binding, never decides correctness of any keyed fact.
 binding=next(x for x in manifest['blocks']if x['block_id']==block);assert H(packetraw)==binding['packet_sha256'];rmap={e['id']:e for e in rawreader['answers']};qmap={e['id']:e for e in qbank}
 assert [e['id']for e in packet['entries']]==binding['ids']
 for e in packet['entries']:assert e['reader_a_entry']==rmap[e['id']]and e['question_entry']==qmap[e['id']]
 allids += binding['ids'];totalatoms+=sum(len(e['requested_fact_scope_entry']['material_requested_facts'])for e in packet['entries'])
 post=[c for c in proj['tool_calls']if c['physical_record']>=bc['physical_record']];assert len(post)==1
 body=post[0]['input'].strip()
 if body.startswith('// @exec:'):body=body.split('\n',1)[1].strip()
 assert body.startswith('// QA_ARTIFACT_WRITE_V1\n')
 body=body.split('\n',1)[1].strip()
 assert parserns['canonical_read_body'](body)is not None or re.fullmatch(r'text\(await tools\.exec_command\(\{cmd: '+parserns['_STRING']+r', max_output_tokens: 24000\}\)\);',body)is not None
 codefile=O/f'{role}-program-{bc["physical_record"]}.py';code=codefile.read_text();tree=ast.parse(code);literal_choices=[]
 for n in tree.body:
  if isinstance(n,ast.Assign)and isinstance(n.targets[0],ast.Name)and n.targets[0].id in ['selections','quotes','rows','chosen','choices','reasons']:
   value=ast.literal_eval(n.value);literal_choices.append({'name':n.targets[0].id,'literal_type':type(value).__name__,'items':len(value),'source_fragment_sha256':H(ast.get_source_segment(code,n).encode())})
 # All methods manually inspected before executing these six trusted mechanical serializers.
 allowed_methods={'read_text','read_bytes','write_text','write_bytes','with_name','encode','hexdigest','append','get','dumps','loads','sha256'}
 allowed_functions={'Path','len','str','sum','zip','print','any','all','isinstance','list'}
 for n in ast.walk(tree):
  if isinstance(n,ast.Attribute):assert not n.attr.startswith('_')
  if isinstance(n,ast.Call):assert (isinstance(n.func,ast.Name)and n.func.id in allowed_functions)or(isinstance(n.func,ast.Attribute)and n.func.attr in allowed_methods),ast.unparse(n.func)
  assert not isinstance(n,(ast.FunctionDef,ast.ClassDef,ast.With,ast.Try,ast.Lambda,ast.Delete))
 allowed={str(packetpath):packetraw};memory={};io=[]
 class MemoryPath:
  def __init__(self,value):self.value=str(value)
  def __str__(self):return self.value
  def __truediv__(self,other):return MemoryPath(self.value.rstrip('/')+'/'+str(other))
  def with_name(self,name):return MemoryPath(self.value.rsplit('/',1)[0]+'/'+name)
  def read_bytes(self):
   assert self.value in allowed or self.value in memory,('read-denied',self.value);io.append({'operation':'read','path':self.value});return memory.get(self.value,allowed.get(self.value))
  def read_text(self):return self.read_bytes().decode()
  def write_bytes(self,data):assert self.value==str(reportpath);memory[self.value]=data;io.append({'operation':'write','path':self.value,'bytes':len(data),'sha256':H(data)});return len(data)
  def write_text(self,text):return self.write_bytes(text.encode())
 clean=ast.Module(body=[n for n in tree.body if not isinstance(n,(ast.Import,ast.ImportFrom))],type_ignores=[]);ast.fix_missing_locations(clean)
 env={'__builtins__':{k:v for k,v in vars(__import__('builtins')).items()if k in allowed_functions|{'AssertionError'}},'json':json,'hashlib':hashlib,'Path':MemoryPath,'print':lambda *a,**k:None}
 exec(compile(clean,str(codefile),'exec'),env)
 replay=memory[str(reportpath)];assert replay==report;put(f'{role}-delivery-checks.json',{'before_first_mutation_records':read_records,'summary_chunk_output_records':seen_s,'packet_entry_output_records':seen_e,'metadata_output_records':seen_m,'unapproved_fixed_reader_failures':errors})
 put(f'{role}-isolated-replay.json',{'program_sha256':H(code.encode()),'manual_code_inspected_before_replay':True,'literal_decision_data':literal_choices,'capability_model':'Imports removed after inspection; restricted primitives plus real json/hashlib and MemoryPath. No filesystem/network/process APIs supplied; Path can read only own frozen packet or in-memory report and write only in-memory assigned report.','io':io,'byte_identical_to_original_report':True,'replay_bytes':len(replay),'replay_sha256':H(replay),'original_report_sha256':H(report)})
 result[block]={'actor':proj['actual_metadata'][0],'actual_all_contexts_sol_high':all(m.get('model')=='gpt-6.1-sol'and m.get('effort')=='high'for m in proj['actual_metadata']if'model'in m),'actual_metadata':proj['actual_metadata'],'runtime_prefix_sha256':proj['prefix_sha256'],'runtime_prefix_bytes':proj['prefix_bytes'],'terminal_event':proj['events'][-1],'first_mutation_record':bc['physical_record'],'all_complete_summary_chunks_visible_before_mutation':set(seen_s)==set(range(0,len(lines),45)),'all_complete_own_packet_entries_visible_before_mutation':set(seen_e)==set(range(len(packet['entries']))),'complete_packet_metadata_visible_before_mutation':bool(seen_m),'original_strict_proof':strict[block]['complete_input_delivery_confirmed'],'separate_normalized_proof':normalized[block]['complete_input_delivery_confirmed'],'fixed_reader_failures':errors,'report_bytes':len(report),'report_sha256':H(report),'isolated_byte_identical_replay':True,'post_boundary_semantic_choices':'All per-question selection/reason/quote tables are literal data. Construction attaches frozen atoms and runs literal-presence/equality assertions; these assertions are not semantic grades. Uniform status/grade constants apply the explicit chosen decisions; no text ranking or inferred semantic grade.','post_boundary_data_paths':{'reads':[str(packetpath)]+([str(reportpath)]if any(z['operation']=='read'and z['path']==str(reportpath)for z in io)else[]),'writes':[str(reportpath)]},'scratch_script_qualification':'Actual shell also writes and executes /tmp/qa-block02-write.py; no cleanup command occurs in the six actor trace. Auditor did not read, execute, inspect existence of, or delete that real scratch path.'if role=='02'else None}
assert allids==[q['id']for q in qbank]and len(allids)==116
put('audit.json',{'scope':'Six actual current I3 reader-A graders only. Literal delivery, actual IO/manual-decision construction and isolated report transport; no gameplay regrading.','runs':result,'assigned_questions':len(allids),'assigned_atom_count':totalatoms,'all_full_inputs_actually_visible_before_first_mutation':all(x['all_complete_summary_chunks_visible_before_mutation']and x['all_complete_own_packet_entries_visible_before_mutation']and x['complete_packet_metadata_visible_before_mutation']for x in result.values()),'all_replayed_reports_byte_identical':True,'original_proofs_preserved':True,'factual_cap':None,'audit_own_qualification':'Initial provenance tool display was mistakenly unfiltered, exposing unrelated actor metadata. No non-target runtime was opened or used. Only the six exact target runtime projections are retained; no unrelated bodies copied.'})
print(json.dumps({k:{x:y for x,y in v.items()if x in ['actual_all_contexts_sol_high','all_complete_summary_chunks_visible_before_mutation','all_complete_own_packet_entries_visible_before_mutation','complete_packet_metadata_visible_before_mutation','original_strict_proof','separate_normalized_proof','isolated_byte_identical_replay']}for k,v in result.items()},indent=2));print('questions',len(allids),'atoms',totalatoms)
