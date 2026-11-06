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
 root=OWN/name;root.mkdir()
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
 try:collect(f,PARENT)
 except (AttributeError,TypeError) as e:
  crashes.append({'fixture':label,'exception':type(e).__name__});CASES.append({'name':label+' crashes instead of disclosed issue','finding':'RP-01','observed_exception':type(e).__name__})
 else:raise AssertionError('Expected disclosed bug not reproduced: '+label)
f=fixture('whitespace-context',{'a.jsonl':[meta(),ctx('  ','\t')]});a=collect(f,PARENT);assert a['records'][0]['confirmed']
CASES.append({'name':'whitespace-only actual model/effort incorrectly confirmed','finding':'RP-02'})
# Execute only the CLI guard AST with synthetic collector/root/argv; never default SESSION_ROOT.
tree=ast.parse(SOURCE);main=tree.body[-1];assert isinstance(main,ast.If)
body=ast.Module(body=main.body,type_ignores=[])
cli_root=OWN/'run-local';cli_root.mkdir();calls=[]
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
result={'source_sha256':hashlib.sha256(SOURCE).hexdigest(),'case_count':len(CASES),'cases':CASES,'crash_cases':crashes,'no_real_runtime_inputs':True,'all_collection_roots_explicit_synthetic':True}
with (OWN/'synthetic-results.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'cases':len(CASES),'crash_cases':len(crashes),'findings':['RP-01','RP-02']}))
