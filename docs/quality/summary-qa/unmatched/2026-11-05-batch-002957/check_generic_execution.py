from pathlib import Path
import json,sys,re,ast,hashlib,copy
P=Path(__file__).resolve().parent;I=P/sys.argv[1];binding=json.loads((I/'generic-extraction-proof.json').read_text());D=next(Path(path).parent for path in binding['files'] if Path(path).name=='source_units.py')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def normalized(node):
 node=copy.deepcopy(node)
 if node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):node.body=node.body[1:]
 return ast.dump(node,include_attributes=False)
original={n.name:normalized(n) for n in ast.parse((D/'source_units.py').read_text()).body if isinstance(n,ast.FunctionDef)}
class Calls(ast.NodeVisitor):
 def __init__(self):self.names=set()
 def visit_FunctionDef(self,node):pass
 def visit_AsyncFunctionDef(self,node):pass
 def visit_Call(self,node):
  f=node.func
  if isinstance(f,ast.Name):self.names.add(f.id)
  elif isinstance(f,ast.Attribute):self.names.add(f.attr)
  elif isinstance(f,ast.Subscript) and isinstance(f.slice,ast.Constant) and isinstance(f.slice.value,str):self.names.add(f.slice.value)
  self.generic_visit(node)
def calls(nodes):
 v=Calls()
 for node in nodes:v.visit(node)
 return v.names
actors=[];prov=read(P/'model-provenance.json')['agents']
for r in ['a','b']:
 task='/root/'+I.name.replace('-','_')+'_reader_'+r;a=next(x for x in prov if x['task']==task);events=[];outputs={}
 for ordinal,line in enumerate(Path(a['runtime_source_path']).open()):
  d=json.loads(line);v=d.get('payload',{})
  if d.get('type')!='response_item':continue
  typ=v.get('type');cid=v.get('call_id')
  if typ=='custom_tool_call_output':
   value=v.get('output');flat=value if isinstance(value,str) else json.dumps(value)
   exits=[int(x) for x in re.findall(r'\?"exit_code\?"\s*:\s*(-?\d+)',flat)]
   if 'Process exited with code 0' in flat:exits.append(0)
   outputs[cid]={'ordinal':ordinal,'record_sha256':hashlib.sha256(line.encode()).hexdigest(),'reported_exit_codes':exits}
  if typ not in ['custom_tool_call','function_call']:continue
  code=v.get('input',v.get('arguments',''));code=code if isinstance(code,str) else json.dumps(code);scripts=[]
  for match in re.finditer(r'(?:"cmd"|cmd)\s*:\s*("(?:\\.|[^"\\])*")',code,re.S):
   try:cmd=json.loads(match.group(1))
   except ValueError:continue
   if "<<'PY'\n" not in cmd:continue
   py=cmd.split("<<'PY'\n",1)[1].rsplit('\nPY',1)[0]
   try:tree=ast.parse(py)
   except SyntaxError:continue
   defs={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))};roots=calls(tree.body);graph={name:calls(node.body) for name,node in defs.items()};reachable=set(roots);pending=list(roots)
   while pending:
    for name in graph.get(pending.pop(),set()):
     if name not in reachable:reachable.add(name);pending.append(name)
   methods=sorted(set(original)&reachable);adapted=sorted(set(defs)&reachable&{'hi','heads','hs','span','unit','section','sec'});matched=sorted(name for name,node in defs.items() if name in original and normalized(node)==original[name])
   if methods or matched or adapted:scripts.append({'heredoc_command_first_line':cmd.splitlines()[0],'heredoc_script_execution_after_definition':cmd.rsplit('\nPY',1)[1].strip() if cmd.lstrip().startswith('cat ') else None,'python_sha256':hashlib.sha256(py.encode()).hexdigest(),'generic_method_call_sites_reachable_from_module':methods,'provided_function_ast_matches':matched,'reader_adapted_function_call_sites':adapted,'reader_adapted_function_ast_sha256':{name:hashlib.sha256(normalized(defs[name]).encode()).hexdigest() for name in adapted},'code_loaded_from_prebound_instruction_marker':'BEGIN GENERIC SOURCE UNIT HELPER' in py})
  if scripts:events.append({'runtime_input_ordinal':ordinal,'runtime_input_sha256':hashlib.sha256(line.encode()).hexdigest(),'call_id':cid,'scripts':scripts})
 for event in events:event['actual_tool_output']=outputs.get(event['call_id'])
 assert events and any(e['actual_tool_output'] and any(s['generic_method_call_sites_reachable_from_module'] or s['reader_adapted_function_call_sites'] for s in e['scripts']) for e in events),(task,'No actual generic extraction execution trace found')
 actors.append({'reader':r,'task':task,'actual_id':a['identity'],'runtime_source_path':a['runtime_source_path'],'prebound_instruction_path':str(I/f'reader-{r}-prompt.txt'),'prebound_instruction_sha256':sha(I/f'reader-{r}-prompt.txt'),'provided_function_calls_observed':any(s['generic_method_call_sites_reachable_from_module'] for e in events for s in e['scripts']),'reader_adapted_function_calls_observed':any(s['reader_adapted_function_call_sites'] for e in events for s in e['scripts']),'generic_extraction_tool_events':events})
proof=read(I/'generic-extraction-proof.json');assert all(sha(Path(path))==value for path,value in proof['files'].items())
out={'method':'Hash-bind the identical supplied neutral-tested helper/instructions and record actual original runtime Python tool invocations and their paired outputs. Statically identify generic method call sites reachable from module code and exact AST matches to supplied functions (ignoring docstrings), without copying rules, questions or answers.','provided_helper_sha256':sha(D/'source_units.py'),'generic_neutral_test_proof':str(I/'generic-extraction-proof.json'),'same_prebound_generic_method_supplied_to_both':True,'actors':actors,'limits':['Call-site reachability is static execution provenance, not branch-level instrumentation or proof that every unit used every function. Actual full source spans, complete asked facts and case outcomes are separately graded and validated.','Reader-adapted generic code is retained in original runtime; exact matching supplied function definitions are identified, not assumed. Named adapted section/heading/span functions are separately recorded with original AST hashes; adaptation is not claimed to be execution of the supplied public API.']}
(I/'generic-extraction-execution-provenance.json').write_text(json.dumps(out,indent=2)+'\n');print('Both readers: instruction/helper hashes and actual supplied/adapted extraction traces recorded separately.')
