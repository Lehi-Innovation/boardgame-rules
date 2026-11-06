from pathlib import Path
import json,ast,re,hashlib,shlex,contextlib,io,posixpath,collections
O=Path(__file__).resolve().parent;M=json.loads((O/'input-hashes.json').read_text());orig={x['snapshot_file']:x['original_path'] for x in M['inputs']};s=(O/'summary-snapshot.md').read_text();qs=json.loads((O/'questions.json').read_text())['questions'];draft=json.loads((O/'reader-a-first-observed-complete-draft.json').read_text());es=[json.loads(x) for x in (O/'runtime-prefix.jsonl').read_bytes().splitlines()];cs=[(n+1,e['payload']) for n,e in enumerate(es) if e.get('payload',{}).get('type')=='custom_tool_call'];oo={e['payload'].get('call_id'):(n+1,e['payload']['output']) for n,e in enumerate(es) if e.get('payload',{}).get('type')=='custom_tool_call_output'}
fs={orig['summary-snapshot.md']:s,orig['questions.json']:(O/'questions.json').read_text()};writes=[];reads=set();rs=[];programs=[]
class VP:
 def __init__(self,p):self.p=str(p)
 def __truediv__(self,p):return VP(posixpath.join(self.p,p))
 def __str__(self):return self.p
 def read_text(self):reads.add(self.p);assert self.p in fs;return fs[self.p]
 def write_text(self,v):assert self.p==orig['reader-a-draft.json'];fs[self.p]=v;writes.append((k,json.loads(v)));return len(v)
def vopen(p,mode='r',*a,**kw):
 assert mode=='r';name=str(p);reads.add(name);assert name in fs;return io.StringIO(fs[name])
for k,(ln,p) in enumerate(cs[:422],1):
 got=''.join(z.get('text','') for z in oo[p['call_id']][1][1:]);r=dict(call=k,line=ln,output_line=oo[p['call_id']][0],call_id=p['call_id'],stdout=got);rs.append(r)
 cmd=json.JSONDecoder().raw_decode(p['input'].split('cmd:',1)[1])[0];programs.append(dict(call=k,line=ln,call_id=p['call_id'],sha256=hashlib.sha256(cmd.encode()).hexdigest()))
 try:
  if cmd.startswith("python3 - <<'PY'\n"):src=cmd[len("python3 - <<'PY'\n"):].rsplit('\nPY',1)[0]
  else:a=shlex.split(cmd);assert a[:2]==['python3','-c'] and len(a)==3;src=a[2]
  t=ast.parse(src)
  for z in ast.walk(t):
   if isinstance(z,ast.Import):assert all(x.name in ['json','re','hashlib'] for x in z.names)
   if isinstance(z,ast.ImportFrom):assert z.module=='pathlib' and [x.name for x in z.names]==['Path']
  t.body=[z for z in t.body if not isinstance(z,(ast.Import,ast.ImportFrom))];buf=io.StringIO()
  with contextlib.redirect_stdout(buf):exec(compile(t,'<virtual replay>','exec'),dict(Path=VP,open=vopen,re=re,json=json,hashlib=hashlib))
  r['stdout_matches']=buf.getvalue()==got
 except (ValueError,StopIteration,TypeError,KeyError,NameError) as e:r['exception']=type(e).__name__
assert len(writes)==116 and [len(d['answers']) for k,d in writes]==list(range(1,117))
assert all(d['answers'][:-1]==writes[j-1][1]['answers'] for j,(k,d) in enumerate(writes) if j)
assert json.loads(fs[orig['reader-a-draft.json']])==draft and writes[-1][0]==422
ns=dict(re=re,hashlib=hashlib,json=json);t=ast.parse((O/'summary-hierarchical-section-check-v8.py').read_bytes());exec(compile(ast.Module(body=[z for z in t.body if isinstance(z,(ast.Assign,ast.FunctionDef))],type_ignores=[]),'<checker>','exec'),ns)
structure=ns['check_data'](s,qs,draft,'a');by={x['id']:x for x in structure['checks']};prev=31;per=[]
for write,data in writes:
 e=data['answers'][-1];idx=int(e['id'][1:])-1;qr=[];ds=[]
 for r in rs:
  if not prev<r['call']<write:continue
  txt=r['stdout']
  try:j=json.loads(txt)
  except ValueError:j=None
  if j==qs[idx]:qr.append({k:r[k] for k in ['call','call_id','line','output_line']})
  if isinstance(j,dict) and isinstance(j.get('text'),str):txt=j['text']
  if txt and txt in s:ds.append((s.index(txt),s.index(txt)+len(txt),r,len(txt.splitlines()),hashlib.sha256(txt.encode()).hexdigest()))
  # Exact literal source inside an identified multi-unit response still proves transport.
  for selected in e['operative_sections']:
   exact=s[selected['start_offset']:selected['end_offset']]
   if exact in txt:ds.append((selected['start_offset'],selected['end_offset'],r,len(txt.splitlines()),hashlib.sha256(exact.encode()).hexdigest()))
  if re.match(r'^LINES [0-9]+\n',txt):
   body=txt.split('\n',1)[1]
   if body and body in s:ds.append((s.index(body),s.index(body)+len(body),r,len(txt.splitlines()),hashlib.sha256(body.encode()).hexdigest()))
 details=[]
 for u in e['operative_sections']:
  chunks=[d for d in ds if d[0]>=u['start_offset'] and d[1]<=u['end_offset']];cursor=u['start_offset']
  for a,b,r,l,h in sorted(chunks,key=lambda d:(d[0],d[1])):
   if a<=cursor:cursor=max(cursor,b)
  details.append(dict(section_id=u['section_id'],start_offset=u['start_offset'],end_offset=u['end_offset'],sha256=u['sha256'],complete=cursor>=u['end_offset'],bounded=all(l<=45 for a,b,r,l,h in chunks),chunks=[dict(call=r['call'],call_id=r['call_id'],line=r['line'],output_line=r['output_line'],start=a,end=b,physical_lines=l,sha256=h) for a,b,r,l,h in chunks]))
 per.append(dict(id=e['id'],question_rereads=qr,units=details,write={k:rs[write-1][k] for k in ['call','call_id','line','output_line']},one_entry_append_preserves_prior=True,clause_count=len(e['clause_ledger']),format_result=by[e['id']]))
 prev=write
issues=[p['id'] for p in per if not p['question_rereads'] or any(not u['complete'] or not u['bounded'] for u in p['units'])]
proof=dict(per_id=per,transport_issues=issues,observed_read_paths=sorted(reads),successful_stdout_mismatches=[r['call'] for r in rs if r.get('stdout_matches')==False],recovered_exceptions=[{k:r[k] for k in ['call','exception']} for r in rs if 'exception' in r],programs=programs,first_full_call=422,first_full_output_line=rs[421]['output_line'],first_full_call_id=rs[421]['call_id'],contexts=[dict(line=n+1,model=e['payload'].get('model'),effort=e['payload'].get('effort')) for n,e in enumerate(es) if e.get('type')=='turn_context' and n+1<=cs[421][0]])
with (O/'composition-proof.json').open('x') as f:json.dump(proof,f,ensure_ascii=False,indent=2);f.write('\n')
cut=b''.join((O/'runtime-prefix.jsonl').read_bytes().splitlines(keepends=True)[:rs[421]['output_line']]);(O/'runtime-through-first-full-draft.jsonl').write_bytes(cut)
print(json.dumps({k:v for k,v in proof.items() if k not in ['per_id','programs']}))
