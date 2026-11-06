from pathlib import Path
import ast,json,re,hashlib,shlex,io,contextlib,posixpath,collections
O=Path(__file__).resolve().parent;M=json.loads((O/'input-hashes.json').read_text());orig={x['snapshot_file']:x['original_path'] for x in M['inputs']};base=str(O.parent);S=(O/'summary-snapshot.md').read_text();Q=json.loads((O/'questions.json').read_text())['questions'];QM={q['id']:q for q in Q};F=json.loads((O/'reader-b.json').read_text());es=[json.loads(x) for x in (O/'runtime-snapshot.jsonl').read_bytes().splitlines()];cs=[(n+1,e['payload']) for n,e in enumerate(es) if e.get('payload',{}).get('type')=='custom_tool_call'];outs={e['payload'].get('call_id'):(n+1,e['payload']['output']) for n,e in enumerate(es) if e.get('payload',{}).get('type')=='custom_tool_call_output'}
fs={base+'/'+n:(O/n).read_text() for n in ['summary-snapshot.md','questions.json']}
for n in ['reader-b.json','reader-b-self-check.json','reader-b-draft.json']:fs[base+'/'+n]=(O/('reader-b-method-precompletion-01--'+n)).read_text()
reads=set();writepaths=set();events=[];activewrites=set()
class VP:
 def __init__(self,p):self.p=str(p)
 def __truediv__(self,p):return VP(posixpath.join(self.p,p))
 def __str__(self):return self.p
 def read_text(self):reads.add(self.p);return fs[self.p]
 def write_text(self,v):assert self.p in [base+'/reader-b.json',base+'/reader-b-self-check.json'];fs[self.p]=v;activewrites.add(self.p);writepaths.add(self.p);return len(v)
class VF(io.StringIO):
 def __init__(self,p,mode):
  self.p=str(p);self.mode=mode
  if mode=='r':reads.add(self.p)
  else:assert self.p in [base+'/reader-b.json',base+'/reader-b-self-check.json'];writepaths.add(self.p);activewrites.add(self.p)
  super().__init__(fs[self.p] if mode in ['r','a'] else '')
  if mode=='w':fs[self.p]=''
  if mode=='a':self.seek(0,2)
 def write(self,v):r=super().write(v);fs[self.p]=self.getvalue();return r
def vopen(p,mode='r',*a,**kw):return VF(p,mode)
for k,(ln,p) in enumerate(cs[57:],58):
 got=''.join(x.get('text','') for x in outs[p['call_id']][1][1:]);rec=dict(call=k,line=ln,output_line=outs[p['call_id']][0],call_id=p['call_id'],visible=got);events.append(rec);cmd=json.JSONDecoder().raw_decode(p['input'].split('cmd:',1)[1])[0];rec['command_sha256']=hashlib.sha256(cmd.encode()).hexdigest();activewrites=set();before=json.loads(fs[base+'/reader-b-self-check.json'])['checks']
 try:
  if re.match(r"^python3(?: -)? <<'PY'\n",cmd):src=cmd.split('\n',1)[1].rsplit('\nPY',1)[0]
  else:a=shlex.split(cmd);assert a[:2]==['python3','-c'];src=a[2]
  t=ast.parse(src)
  for n in ast.walk(t):
   if isinstance(n,ast.Import):assert all(x.name in ['json','re','hashlib','os'] for x in n.names)
   if isinstance(n,ast.ImportFrom):assert n.module in ['pathlib','collections']
  t.body=[n for n in t.body if not isinstance(n,(ast.Import,ast.ImportFrom))];b=io.StringIO()
  with contextlib.redirect_stdout(b):exec(compile(t,'<virtual B continuation>','exec'),dict(Path=VP,open=vopen,json=json,re=re,hashlib=hashlib,Counter=collections.Counter))
  rec['stdout_matches']=b.getvalue()==got
 except Exception as ex:rec['exception']=type(ex).__name__;rec['error']=str(ex)[:120]
 after=json.loads(fs[base+'/reader-b-self-check.json'])['checks'];changed=[a['id'] for a,b in zip(after,before) if a!=b];rec['changed_selfcheck_ids']=changed
 if len(changed)==1:rec['changed_check']=after[next(i for i,x in enumerate(after) if x['id']==changed[0])]
 rec['write_paths']=sorted(activewrites)
assert json.loads(fs[base+'/reader-b.json'])==F
assert json.loads(fs[base+'/reader-b-self-check.json'])==json.loads((O/'reader-b-self-check.json').read_text())
# Source transport is matched as exact literal source slices; question JSON can precede source.
for ev in events:
 txt=ev['visible'];ev['exact_question_id']=None
 try:
  obj,end=json.JSONDecoder().raw_decode(txt)
  if isinstance(obj,dict) and obj.get('id') in QM and obj==QM[obj['id']]:ev['exact_question_id']=obj['id'];ev['source_tail']=txt[end:].lstrip('\n')
 except ValueError:pass
starts=[]
for ev in events:
 qid=ev['exact_question_id']
 if qid and (not starts or starts[-1][0]!=qid):starts.append((qid,ev['call']))
per=[]
for qid in QM:
 begins=[k for q,k in starts if q==qid]
 if not begins:per.append(dict(id=qid,question_reread=False));continue
 begin=begins[0];nexts=[k for q,k in starts if k>begin and q!=qid];end=min(nexts) if nexts else 401
 episode=[e for e in events if begin<=e['call']<end];manual=[e for e in episode if e['changed_selfcheck_ids']==[qid]];last=manual[-1] if manual else None
 delivs=[]
 for e in episode:
  if last and e['call']>last['call']:continue
  txt=e.get('source_tail',e['visible']);candidates=[txt]
  if re.match(r'^LINES [0-9]+\n',txt):candidates.append(txt.split('\n',1)[1])
  for text in candidates:
   if text and text in S:delivs.append((S.index(text),S.index(text)+len(text),e,len(text.splitlines())))
  for u in F['answers'][list(QM).index(qid)]['operative_sections']:
   exact=S[u['start_offset']:u['end_offset']]
   if exact in txt:delivs.append((u['start_offset'],u['end_offset'],e,len(txt.splitlines())))
 units=[]
 for u in F['answers'][list(QM).index(qid)]['operative_sections']:
  chunks=[(max(d[0],u['start_offset']),min(d[1],u['end_offset']),d[2],d[3]) for d in delivs if d[0]<u['end_offset'] and d[1]>u['start_offset']];cursor=u['start_offset']
  for a,b,e,l in sorted(chunks,key=lambda x:(x[0],x[1])):
   if a<=cursor:cursor=max(cursor,b)
  units.append(dict(section_id=u['section_id'],complete=cursor>=u['end_offset'],bounded=all(l<=45 for a,b,e,l in chunks),chunks=[dict(call=e['call'],line=e['line'],output_line=e['output_line'],start=a,end=b,physical_lines=l,sha256=hashlib.sha256(S[a:b].encode()).hexdigest()) for a,b,e,l in chunks]))
 per.append(dict(id=qid,question_reread=True,start_call=begin,next_question_call=end,manual_selfcheck_calls=[e['call'] for e in manual],manual_comparison_before_next_question=bool(manual),selected_units=units,last_manual_check=last.get('changed_check') if last else None))
proof=dict(per_id=per,question_chronology=starts,read_paths=sorted(reads),write_paths=sorted(writepaths),exceptions=[{k:e[k] for k in ['call','exception','error']} for e in events if 'exception' in e],stdout_mismatches=[e['call'] for e in events if e.get('stdout_matches')==False],programs=[{k:e[k] for k in ['call','line','output_line','call_id','command_sha256','changed_selfcheck_ids','write_paths']} for e in events],terminal_replay_equals_frozen_files=True)
with (O/'continuation-proof.json').open('x') as f:json.dump(proof,f,ensure_ascii=False,indent=2);f.write('\n')
print('QUESTIONS',len(starts),'last',starts[-5:]);print('EXCEPTIONS',proof['exceptions']);print('STDOUT mismatches',proof['stdout_mismatches']);print('ISSUES',[(p['id'],p.get('start_call'),p.get('manual_selfcheck_calls'),[(u['section_id'],u['complete'],u['bounded']) for u in p.get('selected_units',[]) if not u['complete'] or not u['bounded']]) for p in per if not p.get('question_reread') or not p.get('manual_comparison_before_next_question') or any(not u['complete'] or not u['bounded'] for u in p.get('selected_units',[]))])
