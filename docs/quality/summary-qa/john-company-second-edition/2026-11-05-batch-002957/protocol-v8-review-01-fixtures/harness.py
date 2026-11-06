from pathlib import Path
import ast,copy,hashlib,json,re
ROOT=Path(__file__).resolve().parent.parent
OWN=Path(__file__).resolve().parent
NAMES=['blind-reader-protocol-user-scope-v8.txt','summary-hierarchical-section-check-v8.py','blind-reader-protocol-user-scope-v7.txt','summary-hierarchical-section-check.py','block-grading-tools.py']
SOURCES={n:(ROOT/n).read_bytes() for n in NAMES}
def load(name):
 tree=ast.parse(SOURCES[name]);ns=dict(re=re,hashlib=hashlib,json=json)
 body=[x for x in tree.body if isinstance(x,ast.FunctionDef) or isinstance(x,ast.Assign)]
 exec(compile(ast.Module(body=body,type_ignores=[]),'<authorized generic checker>','exec'),ns)
 return ns
V=load(NAMES[1]);OLD=load(NAMES[3]);CASES=[]
TEXT='# Root\nPreface.\n## Parent\nShared condition: staff act after approval.  \t\n#### Child\nThe clerk sends two tokens to the reserve after approval.\n###### Deep\nException: wait until morning.\n## Sibling\nOther procedure.\n# New root\nRoot-only text.\n### Last λ\nFinal Ω without LF'
U=V['units'](TEXT)
def uid(heading,prefix='T'):return next(k for k,v in U.items() if v['heading']==heading and k.startswith(prefix))
parent=uid('## Parent');intro=uid('## Parent','I');child=uid('#### Child');deep=uid('###### Deep');sibling=uid('## Sibling');last=uid('### Last λ')
Q=[{'id':'SYN001','question':'Who sends tokens, how many, where and when?'}]
def raw(kind='quote',fact='The clerk sends two tokens to the reserve after approval.',selected=None):
 selected=[child] if selected is None else selected
 units=[U[k] for k in selected]
 return {'answers':[{'id':'SYN001','operative_sections':[{k:v for k,v in x.items() if k!='text'} for x in units],
 'answer':'Applicable summary text\n'+''.join(V['attachment'](x) for x in units),
 'clause_ledger':[{'requested_clause':'Who sends tokens','section_ids':selected,'fact_kind':kind,'fact_source_section':(child if child in selected else selected[0]) if selected else None,'supported_fact_or_case_result':fact}],
 'case_conclusions':[],'support':'supported','evidence':[]}]}
def valid(data,questions=Q,text=TEXT):
 result=V['check_data'](text,questions,data,'a')
 return result['exact_ordered_unique_ids'] and result['all_structure_and_declared_source_spans_valid'],result
def test(name,data=None,want=True,mutate=None,questions=Q,text=TEXT):
 data=copy.deepcopy(raw() if data is None else data)
 if mutate:mutate(data)
 ok,result=valid(data,questions,text)
 assert ok==want,(name,result)
 CASES.append(dict(name=name,expected_valid=want,passed=True))
 return result
def edit_clause(field,value):return lambda d:d['answers'][0]['clause_ledger'][0].__setitem__(field,value)
def edit_entry(field,value):return lambda d:d['answers'][0].__setitem__(field,value)
assert U==OLD['units'](TEXT)
assert U[parent]['text']==TEXT[TEXT.index('## Parent'):TEXT.index('## Sibling')]
assert U[intro]['text']==TEXT[TEXT.index('## Parent'):TEXT.index('#### Child')]
assert U[sibling]['text']==TEXT[TEXT.index('## Sibling'):TEXT.index('# New root')]
assert U[last]['text'].endswith('Final Ω without LF')
assert U[deep]['parent_section_id']==child and U[deep]['ancestor_headings']==['## Parent','#### Child']
for unit in U.values():
 assert TEXT[unit['start_offset']:unit['end_offset']]==unit['text']
 assert unit['sha256']==hashlib.sha256(unit['text'].encode()).hexdigest()
 assert unit['start_line']==TEXT[:unit['start_offset']].count('\n')+1
CASES.append(dict(name='nested/skipped headings, root closure, Unicode character offsets, EOF and untrimmed hashes match original',passed=True))
test('literal quote accepted')
p=raw('paraphrase','Once approved, a clerk transfers 2 tokens into the reserve.')
res=test('faithful nonliteral paraphrase structurally accepted',p)
assert res['checks'][0]['fact_quote_checks'][0]['paraphrase_meaning_requires_independent_grading']
test('same nonliteral wording rejected as quote',raw('quote',p['answers'][0]['clause_ledger'][0]['supported_fact_or_case_result']),False)
res=test('false paraphrase structurally allowed for independent semantic rejection',raw('paraphrase','The manager pays nine tokens before approval.'))
assert res['checks'][0]['fact_quote_checks'][0]['paraphrase_meaning_requires_independent_grading']
test('honest unsupported needs no guessed section',raw('unsupported','The requested fact is absent; relevant contexts checked.',[]))
test('unsupported with actual attached context allowed',raw('unsupported','This source leaves the requested amount unknown.'))
for kind in ['quote','paraphrase','unsupported']:
 for fact in ['', '  \t',None,{},[]]:test(kind+' rejects empty/nontext '+repr(fact),raw(kind),False,edit_clause('supported_fact_or_case_result',fact))
for kind in ['quote','paraphrase']:
 for source in [None,[],{},42,'T999','## Child',U[child]['text']]:
  test(kind+' rejects invalid fact source '+repr(source)[:20],raw(kind),False,edit_clause('fact_source_section',source))
 test(kind+' requires source in own clause refs',raw(kind),False,edit_clause('section_ids',[]))
 test(kind+' rejects whole unit as individual fact',raw(kind,U[child]['text']),False)
for refs in [None,{},[{}],[child,'T999']]:test('invalid refs '+repr(refs),p,False,edit_clause('section_ids',refs))
for kind in [None,'literal',[],{}]:test('invalid fact kind '+repr(kind),want=False,mutate=edit_clause('fact_kind',kind))
test('nonquestion clause rejected',want=False,mutate=edit_clause('requested_clause','Unasked condition'))
test('parent subtree with overlapping child rejected',raw(selected=[parent,child]),False)
test('leaf intro/subtree aliases rejected',raw(selected=[deep,uid('###### Deep','I')]),False)
test('disjoint intro and child union accepted',raw(selected=[intro,child]))
test('disjoint sibling sources accepted',raw(selected=[child,sibling]))
test('attachments reverse source order rejected',raw(selected=[sibling,child]),False)
test('duplicate selected ID rejected',raw(selected=[child,child]),False)
for field in ['kind','heading','level','start_offset','end_offset','start_line','end_line','sha256']:
 def corrupt(d,f=field):d['answers'][0]['operative_sections'][0][f]='WRONG'
 test('metadata '+field+' mismatch rejected',want=False,mutate=corrupt)
for label,change in [
 ('crop',lambda a:a.replace('Exception: wait until morning.','Exception:')),
 ('trailing whitespace',lambda a:a.replace('approval.\n','approval.  \n')),
 ('mislabeled',lambda a:a.replace('qa-unit:'+child,'qa-unit:T999')),
 ('duplicate identified',lambda a:a+V['attachment'](U[child])),
 ('duplicate unmarked',lambda a:a+U[child]['text']),
 ('unknown marker',lambda a:a+'<!-- qa-unit:T999:begin -->\n'),
 ('malformed marker',lambda a:a+'<!-- qa-unit:garbled -->'),
 ('unterminated marker',lambda a:a+'<!-- qa-unit:broken'),
]:
 test(label+' rejected',want=False,mutate=lambda d,c=change:d['answers'][0].__setitem__('answer',c(d['answers'][0]['answer'])))
for x in [[],{},None,7]:test('nontext question ID '+repr(x),want=False,mutate=edit_entry('id',x))
for x in [None,{},['T999'],[{}]]:test('malformed selected metadata '+repr(x),want=False,mutate=edit_entry('operative_sections',x))
test('unknown question ID rejected',want=False,mutate=edit_entry('id','UNKNOWN'))
test('missing answer rejected by ordered full-bank flag',{'answers':[]},False)
d=raw();d['answers']*=2;test('duplicate answer IDs rejected',d,False)
for text in ['## A\n```\n## Fake\n```','## A\n~~~code','## A\n<!-- qa-unit:source']:
 try:V['units'](text)
 except ValueError:pass
 else:raise AssertionError('fence/marker allowed')
 CASES.append(dict(name='reserved fence/marker source rejected: '+repr(text),passed=True))
repeat='## Same\nIdentical body.\n## Same\nIdentical body.\n';ru=V['units'](repeat);chosen=[v for k,v in ru.items() if k.startswith('T')]
d=raw();d['answers'][0]['operative_sections']=[{k:v for k,v in u.items() if k!='text'} for u in chosen]
d['answers'][0]['answer']='Applicable summary text\n'+''.join(V['attachment'](u) for u in chosen)
c=d['answers'][0]['clause_ledger'][0];c.update(section_ids=[chosen[0]['section_id']],fact_source_section=chosen[0]['section_id'],supported_fact_or_case_result='Identical body.')
test('disjoint ID-distinct identical source units accepted',d,text=repeat)
for q in [[{'id':[],'question':'Text'}],Q+Q]:
 try:valid(raw(),q)
 except ValueError:pass
 else:raise AssertionError('malformed source IDs not rejected')
 CASES.append(dict(name='malformed/duplicate question source IDs raise format-review error',passed=True))
# No selected-unit algorithm changed; v8 changes only fact type handling and limits.
for name in ['units','start_marker','end_marker','attachment']:
 a=next(n for n in ast.parse(SOURCES[NAMES[1]]).body if isinstance(n,ast.FunctionDef) and n.name==name)
 b=next(n for n in ast.parse(SOURCES[NAMES[3]]).body if isinstance(n,ast.FunctionDef) and n.name==name)
 assert ast.dump(a)==ast.dump(b)
tree=ast.parse(SOURCES['block-grading-tools.py'])
fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='substantive_strings')
ns={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<generic same-entry string collector>','exec'),ns)
d=raw('paraphrase','A faithful synthetic restatement.')['answers'][0]
d['case_conclusions']=['Actual synthetic case conclusion.'];d['evidence']=[{'quote':'Operative evidence.'}]
strings=ns['substantive_strings'](d)
assert d['clause_ledger'][0]['supported_fact_or_case_result'] in strings
assert d['answer'] in strings and d['case_conclusions'][0] in strings and d['evidence'][0]['quote'] in strings
assert d['clause_ledger'][0]['requested_clause'] not in strings
CASES.append(dict(name='same-entry collector includes paraphrases and all substantive fields without requested-label proof',passed=True))
result=dict(input_hashes={n:hashlib.sha256(b).hexdigest() for n,b in SOURCES.items()},synthetic_only=True,case_count=len(CASES),cases=CASES)
with (OWN/'synthetic-test-results.json').open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'case_count':len(CASES),'all_passed':True}))
