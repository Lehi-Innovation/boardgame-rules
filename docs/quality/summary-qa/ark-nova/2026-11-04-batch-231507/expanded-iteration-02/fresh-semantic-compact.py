from pathlib import Path
exec(Path(__file__).with_name('fresh-semantic-read.py').read_text().split('start,end=map')[0])
start,end=map(int,sys.argv[1:])
# Lossless grader templates: all non-default keys remain present below.
def compact(g,side,id):
 g=dict(g);q=M['Q'][id]['question'];assert g.pop('id')==id;assert g.pop('question')==q
 pp=g.pop('requestedparts' if side=='A' else 'requested_parts'); rr=[]
 for n,orig in enumerate(pp):
  r=dict(orig);scope=M['S'][id]['requested_parts'];part=r.pop('part');r['part']='scope['+str(n)+']' if n<len(scope) and scope[n]==part else part
  if side=='A':
   if r.get('observedquote')==M['A'][id]['answer']:r.pop('observedquote')
   if r.get('observedquote_scope')=='current answer only; complete answer quoted where no narrower deficiency excerpt is needed':r.pop('observedquote_scope')
   if r.get('note')=='Individually reviewed against the literal question, answer and cited frozen-summary text.':r.pop('note')
  else:
   if r.get('observed_quote')==M['B'][id]['answer']:r.pop('observed_quote')
   if r.get('explanation')=='This requested proposition is resolved in the quoted answer, with frozen-summary support.':r.pop('explanation')
  rr.append(r)
 g['parts']=rr
 extra=g.get('context_volunteered_ruling_check' if side=='A' else 'context_and_volunteered_ruling_check',{})
 defaults={'checked_complete_answer':True,'unrequested_context_omissions_not_penalized':True,'material_false_or_contradictory_volunteered_rule_found':False,'unsupported_volunteered_rule_found':False,'note':'All affirmative volunteered rulings were checked against the frozen summary. Ordinary descriptive ability language is not treated as an assertion that optional effects are compulsory.'} if side=='B' else {'status':'no_material_false_or_unsupported_volunteered_ruling_found','note':'All volunteered content was reviewed against the cited summary rule; no additional contradictory ruling or source-correct unsupported guess found.'}
 for k,v in defaults.items():
  if extra.get(k)==v:extra.pop(k)
 return g
for i,q in enumerate(files['Q'],1):
 id=q['id'];bundle={k:norm(compact(d[id],k[-1],id) if k in ['GA','GB'] else d[id],id+'.'+k) for k,d in M.items()}
 if start<=i<=end:
  print('POSITION',i,id)
  for k,v in bundle.items():print(k,json.dumps(v,ensure_ascii=False,separators=(',',':')))
