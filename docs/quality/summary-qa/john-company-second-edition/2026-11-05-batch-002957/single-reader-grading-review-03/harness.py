from pathlib import Path
import ast,collections,contextlib,copy,fnmatch,hashlib,io,json,posixpath,shlex,types

REAL=Path(__file__).resolve().parent.parent
OWN=Path(__file__).resolve().parent
NAMES=['single-reader-grading-tools.py','prove-single-reader-grading-delivery.py',
 'prove-single-reader-grading-delivery-revision-02.py','block-grading-tools.py','prove-bounded-delivery.py',
 'expanded-v12-complete-requested-scope/luna-iteration-05/single-reader-grading-dispatch-template.json',
 'expanded-v12-complete-requested-scope/luna-iteration-05/single-reader-grading-dispatch-template-initial.json']
SOURCES={n:(REAL/n).read_bytes() for n in NAMES}
assert hashlib.sha256(SOURCES[NAMES[1]]).hexdigest()=='72face89f06420bbd65671c3fb475a04a94c100a8dc6243ca8fc72e148ecea63'
prior1=REAL/'single-reader-grading-review-01/harness.py'
prior2=REAL/'single-reader-grading-review-02/harness.py'
STORE,DIRS,WRITES,READS,CASES={},set(),[],[],[]
RUN='/synthetic/bank/run'
SUMMARY=''.join(('\n' if i==46 else f'Line {i}: café λ value {i}.'+('  \t' if i==45 else '')+'\n')
 for i in range(1,96))+'Final Ω without LF'
utility={'Writer','MP','load_functions','put','get','sha','snapshot','restore','case','raw_entry',
 'setup','add_role','write_reports','reject'}
tree=ast.parse(prior1.read_bytes())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef))
 and n.name in utility],type_ignores=[]),'<own virtual utilities>','exec'),globals())
PAIRED=load_functions('block-grading-tools.py',{})
BOUNDED=load_functions('prove-bounded-delivery.py',{})
SINGLE=load_functions('single-reader-grading-tools.py',{'base':PAIRED})
PROOF=load_functions('prove-single-reader-grading-delivery.py',{'base':BOUNDED,'shlex':shlex})
OLD=load_functions('prove-single-reader-grading-delivery-revision-02.py',{'base':BOUNDED,'shlex':shlex})
for name,module in [(NAMES[1],PROOF),(NAMES[2],OLD)]:
 for node in ast.parse(SOURCES[name]).body:
  if isinstance(node,ast.Assign):
   for target in node.targets:
    if isinstance(target,ast.Name) and target.id in ['READ_SCRIPT','WRITE_MARKER']:
     setattr(module,target.id,ast.literal_eval(node.value))
for module in [PAIRED,BOUNDED,SINGLE,PROOF,OLD]:module.ROOT=MP('/synthetic');module.Path=MP
assert PROOF.READ_SCRIPT==OLD.READ_SCRIPT
FOREIGN=dict(id='FOREIGN_SYNTHETIC',question_entry={'question':'Foreign synthetic prompt'},
 key_entry={'expected_answer':'Foreign synthetic content'},reader_b_entry={'answer':'Foreign synthetic content'})
tree=ast.parse(prior2.read_bytes())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)
 and n.name in ['read_value','fixture','event_call','event_output','logs']],type_ignores=[]),
 '<own synthetic source and trace generators>','exec'),globals())

attempt=0
def trace_edit(fn):
 records=get('/synthetic/model-provenance.json')['records']
 for record in records:
  events=[json.loads(x) for x in STORE[record['runtime_source']].splitlines()]
  events=fn(events)
  STORE[record['runtime_source']]='\n'.join(json.dumps(e,ensure_ascii=False) for e in events)+'\n'

def call_index(events,mode,index):
 body=PROOF.read_call(MP(RUN+'/summary-snapshot.md'),MP(RUN+'/grading-reader-a/block-01/packet.json'),mode,index)
 return next(i for i,e in enumerate(events) if e['payload']['type']=='custom_tool_call'
  and PROOF.call_body(e['payload']['input'])==body)

def output_index(events,cid):
 return next(i for i,e in enumerate(events) if e['payload']['type']=='custom_tool_call_output'
  and e['payload'].get('call_id')==cid)

def verify(name,mode='normal',expected=True,mutate=None,engine=None):
 global attempt
 engine=engine or PROOF;logs(mode)
 if mutate:trace_edit(mutate)
 attempt+=1;out=f'proof-attempt-{attempt:02}.json'
 result=engine.prove('bank','run','a','review_a',out)
 actual=all(r['complete_input_delivery_confirmed'] for r in result.values())
 assert actual==expected,(name,actual,result)
 case(name,expected_behavior_verified=True,delivery_complete=actual)
 return get(RUN+'/'+out)

# The old failures and new fixes are exercised against identical frozen fixtures/traces.
fixture();baseline=snapshot()
verify('normal frozen approved delivery')
restore(baseline);verify('revision02 reproduces orphan-output false certification','orphan_outputs',True,engine=OLD)
restore(baseline);r=verify('revision03 rejects orphan outputs without recorded read calls','orphan_outputs',False)
assert r['block-01']['unmatched_tool_outputs']
fixture(nested=True);nested=snapshot()
verify('approved nested source/metadata/original objects remain accepted')
restore(nested);verify('revision02 reproduces recovered nested-prefix false rejection','nested_truncation_recovery',False,engine=OLD)
restore(nested);r=verify('revision03 accepts complete approved retry after nested original prefix','nested_truncation_recovery',True)
assert r['block-01']['ignored_consistent_transport_fragments'] and not r['block-01']['unexpected_packet_shaped_inputs']

# Call provenance and expected mode/index binding.
restore(baseline)
def wrong_output_id(events):
 i=call_index(events,'entry',0);cid=events[i]['payload']['call_id'];j=output_index(events,cid)
 events[j]['payload']['call_id']='ORPHAN_OUTPUT';return events
verify('wrong output call ID rejects delivery',expected=False,mutate=wrong_output_id)
def missing_output_id(events):
 i=call_index(events,'entry',0);j=output_index(events,events[i]['payload']['call_id'])
 events[j]['payload'].pop('call_id');return events
restore(baseline);verify('missing output call ID rejects delivery',expected=False,mutate=missing_output_id)
def missing_read_id(events):
 i=call_index(events,'entry',0);events[i]['payload'].pop('call_id');return events
restore(baseline);verify('missing read call ID rejects delivery',expected=False,mutate=missing_read_id)
def duplicate_read_id(events):
 i=call_index(events,'entry',0);j=call_index(events,'metadata',0)
 events[i]['payload']['call_id']=events[j]['payload']['call_id'];return events
restore(baseline);r=verify('duplicate read call ID rejects delivery',expected=False,mutate=duplicate_read_id)
assert r['block-01']['unapproved_pre_boundary_tool_calls']
def wrong_expected_mode(events):
 i=call_index(events,'entry',0)
 events[i]['payload']['input']=PROOF.read_call(MP(RUN+'/summary-snapshot.md'),MP(RUN+'/grading-reader-a/block-01/packet.json'),'metadata',0)
 return events
restore(baseline);verify('entry output cannot fill a metadata-mode call',expected=False,mutate=wrong_expected_mode)
def known_wrong_output_id(events):
 i=call_index(events,'entry',0);j=output_index(events,events[i]['payload']['call_id']);m=call_index(events,'metadata',0)
 events[j]['payload']['call_id']=events[m]['payload']['call_id'];return events
restore(baseline);verify('entry output under another known read ID is not credited',expected=False,mutate=known_wrong_output_id)
def response_before_call(events):
 i=call_index(events,'entry',0);j=output_index(events,events[i]['payload']['call_id'])
 output=events.pop(j);events.insert(i,output);return events
restore(baseline);verify('response before its recorded call is rejected',expected=False,mutate=response_before_call)
fixture(n=2)
def wrong_index(events):
 i=call_index(events,'entry',0)
 events[i]['payload']['input']=PROOF.read_call(MP(RUN+'/summary-snapshot.md'),MP(RUN+'/grading-reader-a/block-01/packet.json'),'entry',1)
 return events
verify('entry zero output cannot satisfy entry one call',expected=False,mutate=wrong_index)

# Prefix recovery does not erase actual foreign data.
def append_foreign_tail(events):
 for e in events:
  p=e['payload']
  if p['type']=='custom_tool_call_output' and 'Warning: truncated output' in p.get('output',''):
   p['output']+='\n'+json.dumps(FOREIGN,ensure_ascii=False);break
 return events
restore(nested);verify('foreign object after a consistent prefix warning still rejects','nested_truncation_recovery',False,append_foreign_tail)
def append_wrapped_foreign_tail(events):
 for e in events:
  p=e['payload']
  if p['type']=='custom_tool_call_output' and 'Warning: truncated output' in p.get('output',''):
   p['output']+='\n'+json.dumps({'additional':[FOREIGN]},ensure_ascii=False);break
 return events
restore(nested);verify('wrapped foreign object after warning still rejects','nested_truncation_recovery',False,append_wrapped_foreign_tail)
def foreign_before_warning(events):
 for e in events:
  p=e['payload']
  if p['type']=='custom_tool_call_output' and 'Warning: truncated output' in p.get('output',''):
   p['output']=json.dumps(FOREIGN,ensure_ascii=False)+'\nWarning: truncated output';break
 return events
restore(nested);verify('foreign content before warning cannot use prefix exception','nested_truncation_recovery',False,foreign_before_warning)
def corrupt_prefix(events):
 for e in events:
  p=e['payload']
  if p['type']=='custom_tool_call_output' and 'Warning: truncated output' in p.get('output',''):
   p['output']=p['output'].replace('SYN001','ALTERED_SYNTHETIC',1);break
 return events
restore(nested);verify('inconsistent original prefix is not hidden','nested_truncation_recovery',False,corrupt_prefix)
def no_retry_output(events):
 indexes=[i for i,e in enumerate(events) if e['payload']['type']=='custom_tool_call_output'
  and 'Warning: truncated output' not in e['payload'].get('output','')
  and 'reader_a_entry' in e['payload'].get('output','')]
 events.pop(indexes[-1]);return events
restore(nested);verify('consistent prefix alone never credits complete original entry','nested_truncation_recovery',False,no_retry_output)
def retry_after_boundary(events):
 indexes=[i for i,e in enumerate(events) if e['payload']['type']=='custom_tool_call_output'
  and 'Warning: truncated output' not in e['payload'].get('output','')
  and 'reader_a_entry' in e['payload'].get('output','')]
 complete=events.pop(indexes[-1]);events.append(complete);return events
restore(nested);verify('complete retry arriving after boundary cannot repair initial delivery','nested_truncation_recovery',False,retry_after_boundary)
restore(baseline);verify('ordinary truncation recovery remains valid','truncation_recovery',True)

# All four original findings remain repaired under the declared interface.
for mode in ['alternate_early_write','alternate_stdout','cached_read','unknown_tool','wrong_read_call',
 'changed_quantity','wrong_chunk_range','wrong_chunk_hash','partial_chunk','missing_metadata',
 'wrong_metadata','missing_entry','partial_entry','other_role_only','extra_foreign_initial',
 'post_foreign','missing_boundary','early_boundary']:
 restore(baseline);verify(mode+' remains rejected',mode,False)
restore(baseline);full=verify('later calls retained solely for separate post-boundary audit','post_audit_call')
assert full['block-01']['post_boundary_tool_calls_for_separate_protocol_audit']

# Frozen binding regression, including deliberate rehash of just the altered packet.
packet_path=RUN+'/grading-reader-a/block-01/packet.json'
for label,mutate in [
 ('raw input changed',lambda:put(RUN+'/reader-a.json',{'answers':[dict(raw_entry('SYN001','a'),answer='changed')]})),
 ('summary changed',lambda:STORE.__setitem__(RUN+'/summary-snapshot.md','Changed source')),
 ('manifest role changed',lambda:put(RUN+'/grading-reader-a/packet-manifest.json',dict(get(RUN+'/grading-reader-a/packet-manifest.json'),reader_role='reader-b'))),
]:
 restore(baseline);mutate();reject(label+' cannot pass frozen_packets',lambda:PROOF.frozen_packets(MP(RUN),'a'))
for label,mutate in [('packet original field cropped',lambda p:p['entries'][0]['reader_a_entry'].pop('custom_opaque')),
 ('packet block changed',lambda p:p.update(block_id='WRONG')),
 ('other-role original added',lambda p:p['entries'][0].update(reader_b_entry=raw_entry('SYN001','b')))]:
 restore(baseline);p=get(packet_path);mutate(p);put(packet_path,p)
 reject(label+' fails frozen packet hash',lambda:PROOF.frozen_packets(MP(RUN),'a'))
 m=get(RUN+'/grading-reader-a/packet-manifest.json');m['blocks'][0]['packet_sha256']=sha(packet_path);put(RUN+'/grading-reader-a/packet-manifest.json',m)
 reject(label+' fails even if packet hash is updated',lambda:PROOF.frozen_packets(MP(RUN),'a'))

# Core adapter and semantic dispatch paragraphs are unchanged.
initial=json.loads(SOURCES[NAMES[-1]]);template=json.loads(SOURCES[NAMES[-2]])
for prefix in ['Grade only {READER}','CONTROLLING SAME-ENTRY CLARIFICATION:',"Apply the packet's",'For {READER} and EVERY','Save JSON']:
 paragraph=lambda t:next(x for x in t.split('\n\n') if x.startswith(prefix))
 assert paragraph(initial['template'])==paragraph(template['template'])
case('substantive grading/output paragraphs unchanged',passed=True)
assert hashlib.sha256(SOURCES[NAMES[0]]).hexdigest()=='74cf5e82b263576a200ba9837dcbf90844310e35194d0e789be073e39f189ccb'
ids=setup(53);SINGLE.prepare('bank','run','a');write_reports('a');SINGLE.collect('bank','run','a')
assert not any('/reader-b.json' in p for p in READS)
add_role(ids,'b');SINGLE.prepare('bank','run','b');write_reports('b');SINGLE.collect('bank','run','b');both=snapshot()
originals={p:v for p,v in STORE.items() if p.endswith(('grades-same-entry.json','grading-results.json'))}
counts=SINGLE.combine('bank','run');combined=get(RUN+'/results.json');assert all(STORE[p]==v for p,v in originals.items())
reports={p:v for p,v in STORE.items() if '/grading-blocks/' in p and p.endswith('/grades-same-entry.json')}
restore(both);PAIRED.prepare('bank','run');STORE.update(reports);direct=PAIRED.merge('bank','run')
assert counts==direct and combined==get(RUN+'/results.json')
case('unchanged adapter preserves full entries/reports/collections and equals original paired final merge',passed=True)
assert all(str(m.ROOT)=='/synthetic' and m.Path is MP for m in [PAIRED,BOUNDED,SINGLE,PROOF,OLD])
result=dict(input_hashes={n:hashlib.sha256(b).hexdigest() for n,b in SOURCES.items()},
 reviewer_utility_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [prior1,prior2]},
 synthetic_only=True,all_roots_virtual=True,case_count=len(CASES),cases=CASES)
with (OWN/'synthetic-test-results.json').open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(dict(case_count=len(CASES),two_target_regressions_fixed=True,
 prior_four_fixes_retained=True,strict_paired_equivalence=True,all_roots_virtual=True),indent=2))
