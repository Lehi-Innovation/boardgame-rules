from pathlib import Path
import json,re,ast,shlex,hashlib,io,contextlib,posixpath,types
O=Path(__file__).resolve().parent;I=O.parent;R=I.parent.parent;H=[]
def read(p,name=None):
 b=p.read_bytes();H.append(dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 if name:(O/name).write_bytes(b)
 return b
proof=json.loads(read(I/'grading-reader-b-input-delivery-proof.json','original-strict-proof.json'));pv=json.loads(read(I/'grader-b-terminal-all-date-runtime-provenance.json'));wanted={f'/root/v13_i1_grade_b_{n:02d}' for n in range(1,7)};vr=[x for x in pv['records'] if x['agent'] in wanted];assert len(vr)==6;vmap={x['agent']:x for x in vr};manifest=json.loads(read(I/'grading-reader-b/packet-manifest.json','packet-manifest.json'));raw=json.loads(read(I/'reader-b.json','reader-b.json'))['answers'];byraw={x['id']:x for x in raw};summary=read(I/'summary-snapshot.md','summary-snapshot.md')
for n in ['single-reader-grading-tools.py','block-grading-tools.py','prove-single-reader-grading-delivery.py','prove-single-reader-grading-delivery-literal-equivalent.py']:read(R/n)
def command(code):
 expr=re.split(r'cmd:\s*',code,1)[1];dec=json.JSONDecoder();a,end=dec.raw_decode(expr);tail=expr[end:]
 if tail.startswith(' + '):b,end2=dec.raw_decode(tail[3:]);a+=b
 return a
results=[];extra_results=[];allids=[]
for bl in manifest['blocks']:
 bid=bl['block_id'];dp=proof[bid];v=vmap[dp['actor']];assert v['runtime_source']==dp['runtime_source'];log=read(Path(v['runtime_source']),bid+'--runtime.jsonl');assert hashlib.sha256(log[:v['runtime_snapshot_bytes']]).hexdigest()==v['runtime_snapshot_sha256'];es=[json.loads(x) for x in log.splitlines()];cs=[(n+1,e['payload']) for n,e in enumerate(es) if e.get('payload',{}).get('type') in ['custom_tool_call','function_call']];assert all(p.get('name')=='exec' for _,p in cs);outs={e['payload'].get('call_id'):e['payload']['output'] for e in es if e.get('payload',{}).get('type')=='custom_tool_call_output'}
 contexts=[dict(line=n+1,model=e['payload'].get('model'),effort=e['payload'].get('effort')) for n,e in enumerate(es) if e.get('type')=='turn_context'];assert contexts and all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in contexts);meta=es[0]['payload'];spawn=meta['source']['subagent']['thread_spawn'];assert meta['id']==v['session_id'] and spawn['agent_path']==dp['actor'] and spawn['parent_thread_id']==pv['parent_thread_id']
 folder=I/'grading-reader-b'/bid;pb=read(folder/'packet.json',bid+'--packet.json');packet=json.loads(pb);rb=read(folder/'grades-same-entry.json',bid+'--grades-same-entry.json');report=json.loads(rb);assert hashlib.sha256(pb).hexdigest()==bl['packet_sha256']==dp['packet_sha256'];assert packet['summary_sha256']==hashlib.sha256(summary).hexdigest();assert packet['reader_role']=='reader-b';assert [e['id'] for e in packet['entries']]==bl['ids'];allids+=bl['ids']
 for e in packet['entries']:
  assert e['reader_b_entry']==byraw[e['id']] and 'reader_a_entry' not in e
  assert hashlib.sha256(json.dumps(e['reader_b_entry'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()==bl['complete_raw_entry_sha256s'][e['id']]
 boundary=next(j for j,(ln,p) in enumerate(cs) if p['call_id']==dp['first_possible_artifact_write_boundary']['call_id']);unknown={x['call_id'] for x in dp['unapproved_pre_boundary_tool_calls']};assert all(dp['complete_summary_chunk_checks'].values()) and all(dp['complete_packet_entry_checks'].values()) and dp['complete_grading_metadata_delivered']
 fs={str(I/'summary-snapshot.md'):summary,str(folder/'packet.json'):pb};reads=[];writes=[]
 class VP:
  def __init__(self,p):self.p=str(p)
  def __truediv__(self,p):return VP(posixpath.join(self.p,p))
  @property
  def parent(self):return VP(posixpath.dirname(self.p))
  def __str__(self):return self.p
  def read_text(self):reads.append(self.p);assert self.p in fs;return fs[self.p].decode()
  def read_bytes(self):reads.append(self.p);assert self.p in fs;return fs[self.p]
  def write_text(self,t):assert self.p==str(folder/'grades-same-entry.json');fs[self.p]=t.encode();writes.append(dict(path=self.p,sha256=hashlib.sha256(t.encode()).hexdigest()));return len(t)
 delivery=[];initial_inventory=[]
 for k,(ln,p) in enumerate(cs[:boundary],1):
  cmd=command(p['input']);a=shlex.split(cmd);assert a[:2]==['python3','-c'];t=ast.parse(a[2]);t.body=[n for n in t.body if not isinstance(n,(ast.Import,ast.ImportFrom))];reads.clear();b=io.StringIO();error=None
  try:
   with contextlib.redirect_stdout(b):exec(compile(t,'<isolated actual pre-boundary read>','exec'),dict(Path=VP,json=json,hashlib=hashlib,sys=types.SimpleNamespace(argv=['-c']+a[3:])))
  except ValueError as e:error=str(e)
  actual=''.join(x.get('text','') for x in outs[p['call_id']][1:]);assert set(reads)<={str(I/'summary-snapshot.md'),str(folder/'packet.json')};assert not writes
  mode=a[-2];idx=int(a[-1]);rec=dict(call=k,line=ln,call_id=p['call_id'],mode=mode,index=idx,reads=list(reads),argv=a[3:],approved=p['call_id'] not in unknown,error=error)
  if error:assert bid=='block-01' and not reads and 'not enough values to unpack' in actual
  else:
   assert b.getvalue()==actual;val=json.loads(actual)
   if mode=='entry':assert val==packet['entries'][idx]
   elif mode=='metadata':assert val=={k:v for k,v in packet.items() if k!='entries'}
   elif mode=='summary':
    lines=summary.decode().splitlines(keepends=True);text=''.join(lines[idx:idx+45]);assert val==dict(qa_delivery='summary-chunk-v1',start_line=idx+1,end_line=min(idx+45,len(lines)),text=text,sha256=hashlib.sha256(text.encode()).hexdigest())
   delivery.append(rec)
  initial_inventory.append(rec)
  if p['call_id'] in unknown:
   (O/(bid+'--extra-'+str(k)+'.js')).write_text(p['input']);extra_results.append(dict(block=bid,**rec,output_matches_assigned_expected_value=not bool(error),no_io_before_unpack_failure=bool(error) and not reads))
 for ex in [x for x in extra_results if x['block']==bid]:
  retry=next(x for x in delivery if x['approved'] and x['mode']==ex['mode'] and x['index']==ex['index'] and x['call']>ex['call']);ex['correct_approved_later_retry']=dict(call=retry['call'],call_id=retry['call_id'])
 assert {x['index'] for x in delivery if x['approved'] and x['mode']=='summary'}==set(range(0,len(summary.decode().splitlines()),45));assert {x['index'] for x in delivery if x['approved'] and x['mode']=='entry'}==set(range(len(packet['entries'])));assert any(x['approved'] and x['mode']=='metadata' for x in delivery)
 post=[]
 for k,(ln,p) in enumerate(cs[boundary:],boundary+1):
  code=p['input'];(O/(bid+'--call-'+str(k)+'.js')).write_text(code)
  if bid!='block-02':cmd=command(code)
  else:
   selected_text=code.split('const selected =',1)[1].split('\n};',1)[0]+'\n}';reasons_text=code.split('const reasons =',1)[1].split('\n};',1)[0]+'\n}'
   parse=lambda s:json.loads(re.sub(r'(?m)^(Q[0-9]+):',r'"\1":',s.strip()))
   data=json.dumps(dict(selected=parse(selected_text),reasons=parse(reasons_text)),ensure_ascii=False,separators=(',',':'));expr=code.split('const cmd =',1)[1].split(';\nconst r',1)[0].strip();cmd=''
   while expr:
    if expr.startswith('"'):part,end=json.JSONDecoder().raw_decode(expr)
    elif expr.startswith('JSON.stringify(data)'):part=json.dumps(data,ensure_ascii=False);end=len('JSON.stringify(data)')
    else:raise AssertionError('Unexpected JS transport')
    cmd+=part;expr=expr[end:].strip()
    if expr:assert expr[0]=='+';expr=expr[1:].strip()
  assert cmd.startswith("python3 - <<'PY'\n");src=cmd.split('\n',1)[1].rsplit('\nPY',1)[0];(O/(bid+'--call-'+str(k)+'.py')).write_text(src);tree=ast.parse(src)
  for n in ast.walk(tree):
   if isinstance(n,ast.Import):assert all(x.name in ['json','hashlib'] for x in n.names)
   if isinstance(n,ast.ImportFrom):assert n.module=='pathlib'
  tree.body=[n for n in tree.body if not isinstance(n,(ast.Import,ast.ImportFrom))];reads.clear();b=io.StringIO()
  with contextlib.redirect_stdout(b):exec(compile(tree,'<isolated literal report transport>','exec'),dict(Path=VP,json=json,hashlib=hashlib))
  visible=''.join(x.get('text','') for x in outs[p['call_id']][1:])
  if 'text(await tools.exec_command' in code:
   wrapper=json.loads(visible);assert wrapper['exit_code']==0;visible=wrapper['output']
  assert b.getvalue()==visible;assert set(reads)<={str(folder/'packet.json'),str(folder/'grades-same-entry.json')};(O/(bid+'--replayed-report-after-call-'+str(k)+'.json')).write_bytes(fs[str(folder/'grades-same-entry.json')]);post.append(dict(call=k,line=ln,call_id=p['call_id'],read_paths=list(reads),report_sha256=hashlib.sha256(fs[str(folder/'grades-same-entry.json')]).hexdigest(),command_sha256=hashlib.sha256(cmd.encode()).hexdigest(),stdout_exact=True))
 assert fs[str(folder/'grades-same-entry.json')]==rb;grades=report['readers']['reader-b']['grades'];assert [g['id'] for g in grades]==bl['ids'];atoms=0
 for g,e in zip(grades,packet['entries']):
  assert [p['requirement'] for p in g['material_parts']]==e['requested_fact_scope_entry']['material_requested_facts'];atoms+=len(g['material_parts']);r=e['reader_b_entry'];fields=[r['answer']]+[x['supported_fact_or_case_result'] for x in r['clause_ledger']]+r['case_conclusions']+[x['quote'] for x in r['evidence']]
  for p in g['material_parts']:assert p['reader_quotes'] and all(isinstance(q,str) and q.strip() and any(q in s for s in fields) for q in p['reader_quotes'])
 results.append(dict(block=bid,actor=dp['actor'],count=len(grades),atoms=atoms,contexts=contexts,initial_calls=initial_inventory,strict_delivery_proof_complete=dp['complete_input_delivery_confirmed'],post_calls=post,report_writes=writes,packet_sha256=hashlib.sha256(pb).hexdigest(),final_report_sha256=hashlib.sha256(rb).hexdigest(),runtime_sha256=hashlib.sha256(log).hexdigest(),report_replay_byte_identical=True))
assert allids==[r['id'] for r in raw] and len(set(allids))==116
proofout=dict(blocks=results,extras=extra_results,inputs=H,all116_raw_entries_bound=True)
with (O/'execution-proof.json').open('x') as f:json.dump(proofout,f,ensure_ascii=False,indent=2);f.write('\n')
print('contexts',len(results),'questions',sum(x['count'] for x in results),'atoms',sum(x['atoms'] for x in results),'extras',[(x['block'],x['call'],x['reads'],x['correct_approved_later_retry']) for x in extra_results])
