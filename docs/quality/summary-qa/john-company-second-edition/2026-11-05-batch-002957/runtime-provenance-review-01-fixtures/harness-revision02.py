from pathlib import Path
import json,hashlib,ast,copy,sys
ROOT=Path(__file__).resolve().parent.parent
OWN=Path(__file__).resolve().parent
SOURCE=(ROOT/'runtime-provenance-all-dates.py').read_bytes()
ns={'__name__':'generic_review','__file__':str(ROOT/'runtime-provenance-all-dates.py')}
exec(compile(SOURCE,'<authorized generic helper>','exec'),ns)
collect=ns['collect'];CASES=[];PARENT='synthetic-parent'
def meta(actor='/root/a',sid='s1',parent=PARENT):return {'type':'session_meta','payload':{'id':sid,'source':{'subagent':{'thread_spawn':{'parent_thread_id':parent,'agent_path':actor}}}}}
def ctx(model='model-a',effort='high'):return {'type':'turn_context','payload':{'model':model,'effort':effort}}
def fixture(name,files):
 root=OWN/name
 if root.exists():
  for rel,events in files.items():
   expected=''.join((json.dumps(e) if not isinstance(e,str) else e)+'\n' for e in events)
   assert (root/rel).read_text()==expected
  return root
 root.mkdir()
 for rel,events in files.items():
  p=root/rel;p.parent.mkdir(parents=True,exist_ok=True)
  p.write_text(''.join((json.dumps(e) if not isinstance(e,str) else e)+'\n' for e in events))
 return root
root=fixture('valid-across-dates',{'2026/11/05/a.jsonl':[meta(),ctx(),ctx('model-b','low')],'2026/11/06/b.jsonl':[meta('/root/b','s2'),ctx('model-a','medium')],'2026/11/07/unrelated.jsonl':[meta('/root/other','s3','other-parent'),ctx()]})
r=collect(root,PARENT);assert len(r['records'])==2
assert r['records'][0]['settings']==[{'model':'model-a','effort':'high'},{'model':'model-b','effort':'low'}]
assert [x['line'] for x in r['records'][0]['all_contexts_at_snapshot']]==[2,3]
for x in r['records']:
 b=Path(x['runtime_source']).read_bytes();assert x['runtime_snapshot_sha256']==hashlib.sha256(b).hexdigest() and x['runtime_snapshot_bytes']==len(b)
CASES.append({'name':'all dates matched; unrelated parent excluded; every context including later mismatch retained with exact snapshot hashes','passed':True})
# Confirmation means actual observed setting strings present, NOT agreement with requested model.
assert all(x['confirmed'] for x in r['records'])
CASES.append({'name':'later different model/effort retained, not falsely collapsed to first context; confirmed is not expected-setting equality','passed':True})
for label,events in [('missing-context',[meta()]),('missing-model',[meta(),{'type':'turn_context','payload':{'effort':'high'}}]),('missing-effort',[meta(),{'type':'turn_context','payload':{'model':'model-a'}}]),('numeric-model',[meta(),ctx(7)]),('empty-effort',[meta(),ctx(effort='')]),('malformed-line',[meta(),ctx(),'{bad json'])]:
 f=fixture(label,{'a.jsonl':events});a=collect(f,PARENT);assert len(a['records'])==1 and not a['records'][0]['confirmed']
 if label=='malformed-line':assert a['records'][0]['parse_issues']==[{'line':3,'issue':'unparsed snapshot event'}]
 CASES.append({'name':label+' does not certify confirmed','passed':True})
f=fixture('duplicates',{'date1/a.jsonl':[meta(),ctx()],'date2/b.jsonl':[meta(),ctx()]});a=collect(f,PARENT);assert a['duplicate_agents']==['/root/a'] and a['duplicate_session_ids']==['s1']
CASES.append({'name':'duplicate actors and sessions surfaced across date directories','passed':True})
f=fixture('bad-first-events',{'a.jsonl':['{bad'],'b.jsonl':[ctx()]});a=collect(f,PARENT);assert len(a['discovery_issues'])==2 and not a['records']
CASES.append({'name':'malformed initial JSON and missing session_meta disclosed as discovery issues','passed':True})
crashes=[]
for label,events in [
 ('nonobject-first-event',[[]]),('null-session-payload',[{'type':'session_meta','payload':None}]),
 ('nonobject-subagent',[{'type':'session_meta','payload':{'source':{'subagent':[]}}}]),
 ('null-thread-spawn',[{'type':'session_meta','payload':{'source':{'subagent':{'thread_spawn':None}}}}]),
 ('nonobject-later-event',[meta(),ctx(),[]]),('null-context-payload',[meta(),{'type':'turn_context','payload':None}]),
 ('unhashable-actor',[meta(actor=[]),ctx()]),('unhashable-session-id',[meta(sid={}),ctx()])]:
 f=fixture(label,{'a.jsonl':events})
 a=collect(f,PARENT)
 assert a['discovery_issues'] or any(x['parse_issues'] for x in a['records'])
 assert all(not x['confirmed'] for x in a['records'])
 crashes.append({'fixture':label,'resolved':True})
 CASES.append({'name':label+' disclosed without crashing or confirmation','passed':True})
f=fixture('whitespace-context',{'a.jsonl':[meta(),ctx('  ','\t')]});a=collect(f,PARENT);assert not a['records'][0]['confirmed']
assert a['records'][0]['settings']==[{'model':'  ','effort':'\t'}]
CASES.append({'name':'whitespace-only settings unconfirmed with raw values retained','passed':True})
# Execute only the CLI guard AST with synthetic collector/root/argv; never default SESSION_ROOT.
tree=ast.parse(SOURCE);main=tree.body[-1];assert isinstance(main,ast.If)
body=ast.Module(body=main.body,type_ignores=[])
cli_root=OWN/'revision02-run-local';cli_root.mkdir();calls=[]
def cli(arg):
 env=dict(ns,ROOT=cli_root,sys=type('Args',(),{'argv':['helper',arg]}),collect=lambda:(calls.append('synthetic collect') or r))
 exec(compile(body,'<synthetic CLI guard>','exec'),env)
cli('new.json');assert (cli_root/'new.json').exists()
CASES.append({'name':'new run-local output written with exclusive creation','passed':True})
b=(cli_root/'new.json').read_bytes()
try:cli('new.json')
except FileExistsError:pass
else:raise AssertionError('overwrote existing')
assert (cli_root/'new.json').read_bytes()==b
CASES.append({'name':'existing output remains byte-identical after rejected exclusive write','passed':True})
for label,arg in [('relative traversal','../escape.json'),('absolute outside',str(OWN/'escape.json'))]:
 before=len(calls)
 try:cli(arg)
 except SystemExit:pass
 else:raise AssertionError('escaped run-local guard')
 assert len(calls)==before
 CASES.append({'name':label+' rejected before collect','passed':True})
(cli_root/'outside-link').symlink_to(OWN,target_is_directory=True)
try:cli('outside-link/escape.json')
except SystemExit:pass
else:raise AssertionError('symlink escape')
CASES.append({'name':'resolved symlink output escape rejected','passed':True})
# New mixed-tree regressions ensure one malformed child cannot hide unaffected records.
newcases=[
 ('first-null',[None]),('first-string',['"not object"']),
 ('source-null',[{'type':'session_meta','payload':{'source':None}}]),
 ('source-list',[{'type':'session_meta','payload':{'source':[]}}]),
 ('spawn-list',[{'type':'session_meta','payload':{'source':{'subagent':{'thread_spawn':[]}}}}]),
 ('blank-actor',[meta(actor='  '),ctx()]),('blank-session',[meta(sid='\t'),ctx()]),
 ('later-null',[meta(),ctx(),None]),('later-scalar',[meta(),ctx(),7]),
 ('context-list',[meta(),ctx(),{'type':'turn_context','payload':[]}]),
 ('context-missing-payload',[meta(),ctx(),{'type':'turn_context'}]),
 ('later-missing-effort',[meta(),ctx(),{'type':'turn_context','payload':{'model':'later'}}]),
]
for name,events in newcases:
 f=fixture('revision02-'+name,{'date1/bad.jsonl':events,'date2/good.jsonl':[meta('/root/good','good-id'),ctx()]})
 a=collect(f,PARENT)
 assert any(x['agent']=='/root/good' and x['confirmed'] for x in a['records'])
 assert a['discovery_issues'] or any(x['parse_issues'] for x in a['records'])
 assert all(x['agent']=='/root/good' or not x['confirmed'] for x in a['records'])
 CASES.append({'name':name+' disclosed while unrelated good matched child remains confirmed','passed':True})
f=fixture('revision02-host-string',{'a.jsonl':[{'type':'session_meta','payload':{'id':'host','source':'cli'}},ctx()],'b.jsonl':[meta('/root/good','good-id'),ctx()]})
a=collect(f,PARENT);assert len(a['records'])==1 and not a['discovery_issues']
CASES.append({'name':'legitimate nonchild host-string session excluded without issue','passed':True})
f=fixture('revision02-valid-raw-spaces',{'a.jsonl':[meta(),ctx(' model-a ',' high ')]})
a=collect(f,PARENT);assert a['records'][0]['confirmed'] and a['records'][0]['settings']==[{'model':' model-a ','effort':' high '}]
CASES.append({'name':'nonblank raw setting strings retained exactly without normalization','passed':True})
result={'source_sha256':hashlib.sha256(SOURCE).hexdigest(),'case_count':len(CASES),'cases':CASES,'resolved_shape_cases':crashes,'no_real_runtime_inputs':True,'all_collection_roots_explicit_synthetic':True}
with (OWN/'synthetic-results-revision02.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'cases':len(CASES),'resolved_original_shape_cases':len(crashes),'RP01_resolved':True,'RP02_resolved':True}))
