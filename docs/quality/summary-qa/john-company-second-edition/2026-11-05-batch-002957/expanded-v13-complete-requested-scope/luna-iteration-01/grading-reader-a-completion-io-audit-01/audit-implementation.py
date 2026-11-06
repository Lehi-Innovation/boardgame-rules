from pathlib import Path
import json,ast,re,shlex,hashlib,posixpath,io,contextlib,datetime,collections
O=Path(__file__).resolve().parent;I=O.parent;R=I.parent.parent
H=[]
def read(p,copyname=None):
 b=p.read_bytes();H.append(dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 if copyname:(O/copyname).write_bytes(b)
 return b
proof=json.loads(read(I/'grading-reader-a-input-delivery-proof.json','initial-delivery-proof.json'));pv=json.loads(read(I/'grader-a-terminal-all-date-runtime-provenance.json'))
actors={f'/root/v13_i1_grade_a_{n:02d}' for n in range(1,7)};records={x['agent']:x for x in pv['records'] if x['agent'] in actors};assert set(records)==actors
manifest=json.loads(read(I/'grading-reader-a/packet-manifest.json','packet-manifest.json'));rawb=read(I/'reader-a.json','reader-a.json');raw=json.loads(rawb)['answers'];rawmap={x['id']:x for x in raw};assert len(rawmap)==len(raw)==116
summary=read(I/'summary-snapshot.md','summary-snapshot.md')
for n in ['single-reader-grading-tools.py','block-grading-tools.py','prove-single-reader-grading-delivery.py','prove-single-reader-grading-delivery-literal-equivalent.py']:read(R/n)
results=[];programs=[];allids=[]
for block in manifest['blocks']:
 bid=block['block_id'];dp=proof[bid];v=records[dp['actor']];lp=Path(dp['runtime_source']);assert str(lp)==v['runtime_source'];log=read(lp,bid+'--runtime.jsonl');es=[json.loads(x) for x in log.splitlines()]
 assert hashlib.sha256(log[:v['runtime_snapshot_bytes']]).hexdigest()==v['runtime_snapshot_sha256']
 contexts=[dict(line=n+1,model=e['payload'].get('model'),effort=e['payload'].get('effort')) for n,e in enumerate(es) if e.get('type')=='turn_context'];assert contexts and all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in contexts)
 first=es[0]['payload'];spawn=first['source']['subagent']['thread_spawn'];assert spawn['agent_path']==dp['actor'] and spawn['parent_thread_id']==pv['parent_thread_id']
 folder=I/'grading-reader-a'/bid;pb=read(folder/'packet.json',bid+'--packet.json');packet=json.loads(pb);rb=read(folder/'grades-same-entry.json',bid+'--grades-same-entry.json');report=json.loads(rb)
 assert hashlib.sha256(pb).hexdigest()==block['packet_sha256']==dp['packet_sha256'];assert packet['reader_role']=='reader-a' and packet['block_id']==bid
 assert packet['summary_sha256']==hashlib.sha256(summary).hexdigest();assert [e['id'] for e in packet['entries']]==block['ids'];allids+=block['ids']
 for entry in packet['entries']:
  qid=entry['id'];assert entry['reader_a_entry']==rawmap[qid] and 'reader_b_entry' not in entry
  assert hashlib.sha256(json.dumps(rawmap[qid],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==block['complete_raw_entry_sha256s'][qid]
 assert dp['complete_input_delivery_confirmed'] and not dp['unapproved_pre_boundary_tool_calls'] and not dp['status_or_other_agent_calls'] and not dp['unexpected_packet_shaped_inputs']
 calls=[(n+1,e['payload']) for n,e in enumerate(es) if e.get('payload',{}).get('type') in ['custom_tool_call','function_call']];assert all(p.get('name')=='exec' for _,p in calls)
 boundary=next(j for j,(ln,p) in enumerate(calls) if p['call_id']==dp['first_possible_artifact_write_boundary']['call_id']);assert len(calls[boundary:])==1
 initialpaths=set()
 for ln,p in calls[:boundary]:
  code=p['input'];expr=code.split('cmd: ',1)[1].split(', max_output_tokens:',1)[0]
  dec=json.JSONDecoder();part,end=dec.raw_decode(expr);cmd=part
  if end<len(expr):assert expr[end:end+3]==' + ';tail,e=dec.raw_decode(expr[end+3:]);assert end+3+e==len(expr);cmd+=tail
  a=shlex.split(cmd);assert a[:2]==['python3','-c'];assert len(a)==7
  assert a[3]==str(I/'summary-snapshot.md') and a[4]==str(folder/'packet.json');assert a[5] in ['summary','metadata','entry'];initialpaths|={a[3],a[4]}
 ln,p=calls[boundary];code=p['input'];(O/(bid+'--artifact-call.js')).write_text(code)
 if bid!='block-05':cmd=json.JSONDecoder().raw_decode(code.split('cmd:',1)[1].lstrip())[0]
 else:
  output=json.JSONDecoder().raw_decode(code.split('const output =',1)[1].strip())[0]
  decisions,end=json.JSONDecoder().raw_decode(code.split('const decisions =',1)[1].strip())
  data={'block_id':'block-05','readers':{'reader-a':{'grades':[dict(id=x[0],grade=x[1],reason=x[2],material_parts=[dict(requirement=y[0],status=y[1],reader_quotes=y[2:]) for y in x[3]],unsupported_guesses=[],summary_issue_if_any=None) for x in decisions]}}}
  payload=json.dumps(data,ensure_ascii=False,indent=2)
  expr=code.split('const cmd =',1)[1].split(';\nconst r',1)[0].strip();cmd=''
  while expr:
   if expr.startswith('"'):part,end=json.JSONDecoder().raw_decode(expr)
   elif expr.startswith('JSON.stringify(payload)'):part=json.dumps(payload,ensure_ascii=False);end=len('JSON.stringify(payload)')
   elif expr.startswith('output'):part=output;end=6
   else:raise AssertionError('Unexpected JS expression')
   cmd+=part;expr=expr[end:].strip()
   if expr:assert expr.startswith('+');expr=expr[1:].strip()
 assert cmd.startswith("python3 - <<'PY'\n");src=cmd.split('\n',1)[1].rsplit('\nPY',1)[0];(O/(bid+'--artifact-program.py')).write_text(src)
 tree=ast.parse(src)
 for n in ast.walk(tree):
  if isinstance(n,ast.Import):assert all(x.name in ['json','hashlib'] for x in n.names)
  if isinstance(n,ast.ImportFrom):assert n.module=='pathlib'
 fs={str(folder/'packet.json'):pb};reads=[];writes=[]
 class VP:
  def __init__(self,p):self.p=str(p)
  def __truediv__(self,p):return VP(posixpath.join(self.p,p))
  def __str__(self):return self.p
  def read_text(self):reads.append(self.p);assert self.p in fs;return fs[self.p].decode()
  def read_bytes(self):reads.append(self.p);assert self.p in fs;return fs[self.p]
  def write_text(self,v):assert self.p==str(folder/'grades-same-entry.json');writes.append(self.p);fs[self.p]=v.encode();return len(v)
 tree.body=[n for n in tree.body if not isinstance(n,(ast.Import,ast.ImportFrom))];buf=io.StringIO()
 with contextlib.redirect_stdout(buf):exec(compile(tree,'<isolated grader artifact transport>','exec'),dict(Path=VP,json=json,hashlib=hashlib))
 assert fs[str(folder/'grades-same-entry.json')]==rb;assert writes==[str(folder/'grades-same-entry.json')]
 outs=[e['payload'] for e in es if e.get('payload',{}).get('type')=='custom_tool_call_output' and e['payload'].get('call_id')==p['call_id']];assert len(outs)==1
 actual=''.join(x.get('text','') for x in outs[0]['output'][1:]);assert actual==buf.getvalue()
 grades=report['readers']['reader-a']['grades'];assert [g['id'] for g in grades]==block['ids'];atoms=0
 for g,entry in zip(grades,packet['entries']):
  parts=g['material_parts'];assert [x['requirement'] for x in parts]==entry['requested_fact_scope_entry']['material_requested_facts'];atoms+=len(parts)
  r=entry['reader_a_entry'];fields=[r['answer']]+[x['supported_fact_or_case_result'] for x in r['clause_ledger']]+r['case_conclusions']+[x['quote'] for x in r['evidence']]
  for part in parts:
   assert part['status'] in ['covered','omitted','contradicted'];assert all(isinstance(q,str) and q.strip() and any(q in f for f in fields) for q in part['reader_quotes'])
   if part['status']=='covered':assert part['reader_quotes']
 results.append(dict(block_id=bid,actor=dp['actor'],question_count=len(grades),material_parts=atoms,total_calls=len(calls),pre_boundary_calls=boundary,post_boundary_calls=1,boundary_call_id=p['call_id'],boundary_log_line=ln,contexts=contexts,initial_allowed_read_paths=sorted(initialpaths),post_boundary_read_paths=reads,post_boundary_write_paths=writes,report_sha256=hashlib.sha256(rb).hexdigest(),packet_sha256=hashlib.sha256(pb).hexdigest(),runtime_sha256=hashlib.sha256(log).hexdigest(),raw_entries_exact_original_and_canonical_hashes=True,virtual_output_byte_identical=True,stdout_path_count_hash_only=True))
 programs.append(dict(block_id=bid,js_file=bid+'--artifact-call.js',python_file=bid+'--artifact-program.py',command_sha256=hashlib.sha256(cmd.encode()).hexdigest(),python_sha256=hashlib.sha256(src.encode()).hexdigest()))
assert allids==[x['id'] for x in raw] and len(allids)==len(set(allids))==116
record=dict(blocks=results,code_inventory=programs,all116_disjoint_complete_ids=True,inputs=H)
with (O/'execution-proof.json').open('x') as f:json.dump(record,f,indent=2);f.write('\n')
print(json.dumps(dict(blocks=len(results),questions=sum(x['question_count'] for x in results),atoms=sum(x['material_parts'] for x in results),all_outputs_byte_identical=True)))
