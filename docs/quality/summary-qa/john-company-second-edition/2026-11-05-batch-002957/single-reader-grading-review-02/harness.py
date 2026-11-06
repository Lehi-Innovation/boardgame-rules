from pathlib import Path
import ast, collections, contextlib, copy, fnmatch, hashlib, io, json, posixpath, shlex, types

ROOT_REAL = Path(__file__).resolve().parent.parent
OWN = Path(__file__).resolve().parent
NAMES = ['single-reader-grading-tools.py', 'prove-single-reader-grading-delivery.py',
    'block-grading-tools.py', 'prove-bounded-delivery.py',
    'expanded-v12-complete-requested-scope/luna-iteration-05/single-reader-grading-dispatch-template.json',
    'expanded-v12-complete-requested-scope/luna-iteration-05/single-reader-grading-dispatch-template-initial.json']
SOURCES = {n: (ROOT_REAL / n).read_bytes() for n in NAMES}
prior = ROOT_REAL / 'single-reader-grading-review-01/harness.py'
prior_tree = ast.parse(prior.read_bytes())
utility_names = {'Writer','MP','load_functions','put','get','sha','snapshot','restore','case',
    'raw_entry','setup','add_role','write_reports','reject'}
STORE, DIRS, WRITES, READS, CASES = {}, set(), [], [], []
RUN='/synthetic/bank/run'
SUMMARY=''.join(('\n' if i==46 else f'Line {i}: café λ value {i}.'+('  \t' if i==45 else '')+'\n')
                for i in range(1,96))+'Final Ω without LF'
exec(compile(ast.Module(body=[n for n in prior_tree.body
    if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in utility_names],type_ignores=[]),
    '<reviewer-owned prior virtual utilities>','exec'),globals())
PAIRED=load_functions('block-grading-tools.py',{})
BOUNDED=load_functions('prove-bounded-delivery.py',{})
SINGLE=load_functions('single-reader-grading-tools.py',{'base':PAIRED})
PROOF=load_functions('prove-single-reader-grading-delivery.py',{'base':BOUNDED,'shlex':shlex})
proof_tree=ast.parse(SOURCES['prove-single-reader-grading-delivery.py'])
for node in proof_tree.body:
    if isinstance(node,ast.Assign):
        for target in node.targets:
            if isinstance(target,ast.Name) and target.id in ['READ_SCRIPT','WRITE_MARKER']:
                setattr(PROOF,target.id,ast.literal_eval(node.value))
for module in [PAIRED,BOUNDED,SINGLE,PROOF]:
    module.ROOT=MP('/synthetic');module.Path=MP
assert SINGLE.base is PAIRED and PROOF.base is BOUNDED

FOREIGN=dict(id='FOREIGN_SYNTHETIC',question_entry={'question':'Foreign synthetic prompt'},
    key_entry={'expected_answer':'Foreign synthetic data'},reader_b_entry={'answer':'Foreign synthetic data'})

def read_value(packet_path,mode,index):
    tree=ast.parse(PROOF.READ_SCRIPT)
    body=[n for n in tree.body if not isinstance(n,(ast.Import,ast.ImportFrom))]
    ns=dict(Path=MP,hashlib=hashlib,json=json,
        sys=types.SimpleNamespace(argv=['read-only-script',RUN+'/summary-snapshot.md',packet_path,mode,str(index)]))
    buffer=io.StringIO()
    before=copy.deepcopy((STORE,DIRS,WRITES))
    with contextlib.redirect_stdout(buffer):exec(compile(ast.Module(body=body,type_ignores=[]),'<fixed READ_SCRIPT>','exec'),ns)
    assert (STORE,DIRS,WRITES)==before
    return json.loads(buffer.getvalue())


def fixture(n=1,nested=False):
    ids=setup(n)
    if nested:
        raw=get(RUN+'/reader-a.json');raw['answers'][0]['custom_opaque']['approved_example']=copy.deepcopy(FOREIGN);put(RUN+'/reader-a.json',raw)
        scope=get('/synthetic/bank/grading-scope.json');scope['approved_metadata_example']=copy.deepcopy(FOREIGN);put('/synthetic/bank/grading-scope.json',scope)
        STORE[RUN+'/summary-snapshot.md']+='\nApproved source example: '+json.dumps(FOREIGN)+'\n'
    SINGLE.prepare('bank','run','a')
    return ids


def event_call(code,cid,name='exec'):
    return dict(type='response_item',payload=dict(type='custom_tool_call',name=name,input=code,call_id=cid))
def event_output(value,cid,raw_text=None):
    out=json.dumps(value,ensure_ascii=False) if raw_text is None else raw_text
    return dict(type='response_item',payload=dict(type='custom_tool_call_output',call_id=cid,output=out))


def logs(mode='normal'):
    manifest=get(RUN+'/grading-reader-a/packet-manifest.json');records=[]
    for block in manifest['blocks']:
        packet_path=RUN+'/grading-reader-a/'+block['block_id']+'/packet.json'
        packet=get(packet_path);events=[];seq=0
        def emit(read_mode,index,alter=None):
            nonlocal seq
            seq+=1;cid=f'{block["block_id"]}-{seq}'
            body=PROOF.read_call(MP(RUN+'/summary-snapshot.md'),MP(packet_path),read_mode,index)
            events.append(event_call('// @exec: {"max_output_tokens":24000}\n'+body,cid))
            value=read_value(packet_path,read_mode,index)
            if alter:value=alter(value)
            if mode=='truncation_recovery' and read_mode=='entry' and index==0:
                encoded=json.dumps(value,ensure_ascii=False)
                events.append(event_output(None,cid,raw_text=encoded[:len(encoded)//2]+'\nWarning: truncated output'))
                seq+=1;cid=f'{block["block_id"]}-{seq}'
                events.append(event_call('// @exec: {"max_output_tokens":24000}\n'+body,cid))
            if mode=='nested_truncation_recovery' and read_mode=='entry' and index==0:
                encoded=json.dumps(value,ensure_ascii=False);nested=json.dumps(FOREIGN,ensure_ascii=False)
                end=encoded.index(nested)+len(nested)
                events.append(event_output(None,cid,raw_text=encoded[:end]+'\nWarning: truncated output'))
                seq+=1;cid=f'{block["block_id"]}-{seq}'
                events.append(event_call('// @exec: {"max_output_tokens":24000}\n'+body,cid))
            events.append(event_output(value,cid))
        if mode in ['alternate_early_write','alternate_stdout','cached_read','unknown_tool']:
            body={'alternate_early_write':"open('/synthetic/out','x').write('{}')",
                  'alternate_stdout':'json.dump(value, sys.stdout)',
                  'cached_read':'text(cachedInput)', 'unknown_tool':'text(123)'}[mode]
            events.append(event_call(body,'unapproved',name='clock' if mode=='unknown_tool' else 'exec'))
        starts=list(range(0,len(PROOF.physical_lines(STORE[RUN+'/summary-snapshot.md'])),45))
        for start in starts:
            alter=None
            if start==0 and mode in ['changed_quantity','wrong_chunk_range','wrong_chunk_hash','partial_chunk']:
                def alter(v):
                    v=copy.deepcopy(v)
                    if mode=='changed_quantity':v['text']=v['text'].replace('value 1.','value 10.');v['sha256']=hashlib.sha256(v['text'].encode()).hexdigest()
                    if mode=='wrong_chunk_range':v['end_line']-=1
                    if mode=='wrong_chunk_hash':v['sha256']='0'*64
                    if mode=='partial_chunk':v['text']=v['text'][:-4];v['sha256']=hashlib.sha256(v['text'].encode()).hexdigest()
                    return v
            emit('summary',start,alter)
        if mode!='missing_metadata':emit('metadata',0,lambda v:{**v,'normative_scope':'Wrong metadata'} if mode=='wrong_metadata' else v)
        for index in range(len(packet['entries'])):
            if mode=='missing_entry' and index==0:continue
            def alter_entry(v):
                v=copy.deepcopy(v)
                if mode=='partial_entry':del v['reader_a_entry']['custom_opaque']
                if mode=='other_role_only':v['reader_b_entry']=v.pop('reader_a_entry')
                if mode=='extra_foreign_initial':return [v,copy.deepcopy(FOREIGN)]
                return v
            emit('entry',index,alter_entry)
        if mode=='orphan_outputs':events=[e for e in events if e['payload']['type'].endswith('_output')]
        if mode=='wrong_read_call':
            for e in events:
                if e['payload']['type']=='custom_tool_call':e['payload']['input']+='\ntext("extra code")';break
        if mode=='missing_boundary':pass
        else:events.append(event_call(PROOF.WRITE_MARKER+'text("synthetic output path");','write-boundary'))
        if mode=='post_foreign':events.append(event_output(FOREIGN,'write-boundary'))
        if mode=='post_audit_call':
            events.append(event_call('text("synthetic later code requiring separate audit");','post-call'))
            events.append(event_output({'path':'/synthetic/own-grade.json','hash':'synthetic hash'},'post-call'))
        if mode=='early_boundary':
            boundary=events.pop();events.insert(0,boundary)
        runtime='/synthetic/'+block['block_id']+'-runtime.jsonl'
        STORE[runtime]='\n'.join(json.dumps(e,ensure_ascii=False) for e in events)+'\n'
        records.append(dict(agent='/root/review_a_'+block['block_id'].replace('block-',''),runtime_source=runtime))
    put('/synthetic/model-provenance.json',dict(records=records))


attempt=0
def delivery(name,mode='normal',expected=True,finding=None):
    global attempt
    logs(mode);attempt+=1;output_name=f'review-proof-{attempt:02}.json'
    result=PROOF.prove('bank','run','a','review_a',output_name)
    actual=all(v['complete_input_delivery_confirmed'] for v in result.values())
    assert actual==expected,(name,actual,result)
    case(name,delivery_complete=actual,finding=finding)
    return get(RUN+'/'+output_name)


# Same semantic paragraphs, new technical delivery interface.
old=json.loads(SOURCES[NAMES[-1]]);new=json.loads(SOURCES[NAMES[-2]])
assert hashlib.sha256(new['template'].encode()).hexdigest()==new['template_sha256']
for prefix in ['Grade only {READER}', 'CONTROLLING SAME-ENTRY CLARIFICATION:',
               "Apply the packet's", 'For {READER} and EVERY', 'Save JSON']:
    paragraph=lambda t:next(p for p in t.split('\n\n') if p.startswith(prefix))
    assert paragraph(old['template'])==paragraph(new['template'])
case('semantic grading paragraphs unchanged; technical delivery interface is prospectively explicit',passed=True)

fixture();baseline=snapshot()
lines=PROOF.physical_lines(STORE[RUN+'/summary-snapshot.md']);assert len(lines)==96
packet_path=RUN+'/grading-reader-a/block-01/packet.json'
for start in [0,45,90]:
    value=read_value(packet_path,'summary',start);chunk=''.join(lines[start:start+45])
    assert value==dict(qa_delivery='summary-chunk-v1',start_line=start+1,end_line=min(start+45,96),text=chunk,sha256=hashlib.sha256(chunk.encode()).hexdigest())
assert read_value(packet_path,'summary',90)['text'].endswith('Final Ω without LF')
assert read_value(packet_path,'metadata',0)=={k:v for k,v in get(packet_path).items() if k!='entries'}
assert read_value(packet_path,'entry',0)==get(packet_path)['entries'][0]
assert shlex.split(PROOF.read_prefix(MP("/synthetic/a b'Ω"),MP('/synthetic/$(text).json')))==['python3','-c',PROOF.READ_SCRIPT,"/synthetic/a b'Ω",'/synthetic/$(text).json']
case('fixed READ_SCRIPT is read-only; exact45 LF chunks preserve blanks, tabs, Unicode, EOF and safe literal paths',passed=True)
delivery('normal exact frozen input delivery')
for mode in ['alternate_early_write','alternate_stdout','cached_read','unknown_tool','wrong_read_call',
             'changed_quantity','wrong_chunk_range','wrong_chunk_hash','partial_chunk','missing_metadata',
             'wrong_metadata','missing_entry','partial_entry','other_role_only','extra_foreign_initial',
             'post_foreign','missing_boundary','early_boundary']:
    restore(baseline);delivery(mode,mode,False)
restore(baseline);delivery('standard truncated entry can be recovered by its approved retry','truncation_recovery')
restore(baseline);full=delivery('later arbitrary calls are retained but not certified by initial-delivery scope','post_audit_call')
assert full['block-01']['post_boundary_tool_calls_for_separate_protocol_audit']
case('boundary and post-boundary calls retained with explicit later-audit limitation',passed=True)

# Deep legitimate examples inside approved originals/metadata/source are not foreign reads.
fixture(nested=True);nested_baseline=snapshot()
delivery('nested packet-shaped content within approved source/metadata/original entry is accepted')
delivery('recovered truncation exposes nested approved original example and is falsely rejected',
         'nested_truncation_recovery',False,'SRG2-02')

# A response-only trace currently certifies despite containing no recorded approved reads.
restore(baseline)
delivery('orphan approved-value outputs certify without any recorded read calls','orphan_outputs',True,'SRG2-01')

# Frozen packet/original/source binding regression.
for label,mutation in [
    ('raw input change',lambda:put(RUN+'/reader-a.json',{'answers':[dict(raw_entry('SYN001','a'),answer='Changed')]})),
    ('summary source change',lambda:STORE.__setitem__(RUN+'/summary-snapshot.md','Changed source')),
    ('manifest role change',lambda:put(RUN+'/grading-reader-a/packet-manifest.json',dict(get(RUN+'/grading-reader-a/packet-manifest.json'),reader_role='reader-b'))),
    ('canonical raw-entry hash change',lambda:(lambda m:(m['blocks'][0]['complete_raw_entry_sha256s'].__setitem__('SYN001','0'*64),put(RUN+'/grading-reader-a/packet-manifest.json',m)))(get(RUN+'/grading-reader-a/packet-manifest.json'))),
]:
    restore(baseline);mutation();reject(label+' rejected by frozen_packets',lambda:PROOF.frozen_packets(MP(RUN),'a'))
for label,mutation in [
    ('packet cropping',lambda p:p['entries'][0]['reader_a_entry'].pop('custom_opaque')),
    ('packet role change',lambda p:p.update(reader_role='reader-b')),
    ('packet block change',lambda p:p.update(block_id='WRONG')),
    ('packet summary hash change',lambda p:p.update(summary_sha256='0'*64)),
    ('opposite raw role added to packet entry',lambda p:p['entries'][0].update(reader_b_entry=raw_entry('SYN001','b'))),
]:
    restore(baseline);p=get(packet_path);mutation(p);put(packet_path,p)
    reject(label+' with stale packet hash rejected',lambda:PROOF.frozen_packets(MP(RUN),'a'))
    m=get(RUN+'/grading-reader-a/packet-manifest.json');m['blocks'][0]['packet_sha256']=sha(packet_path);put(RUN+'/grading-reader-a/packet-manifest.json',m)
    reject(label+' still rejected when only packet hash updated',lambda:PROOF.frozen_packets(MP(RUN),'a'))

# Recheck core adapter composition using imported original paired validator.
ids=setup(53);SINGLE.prepare('bank','run','a');write_reports('a');SINGLE.collect('bank','run','a')
assert not any('/reader-b.json' in p for p in READS)
add_role(ids,'b');SINGLE.prepare('bank','run','b');write_reports('b');SINGLE.collect('bank','run','b');before_combine=snapshot()
originals={p:v for p,v in STORE.items() if p.endswith(('grades-same-entry.json','grading-results.json'))}
counts=SINGLE.combine('bank','run');result=get(RUN+'/results.json')
assert all(STORE[p]==v for p,v in originals.items())
reports={p:v for p,v in STORE.items() if '/grading-blocks/' in p and p.endswith('/grades-same-entry.json')}
restore(before_combine);PAIRED.prepare('bank','run');STORE.update(reports);direct=PAIRED.merge('bank','run')
assert counts==direct and result==get(RUN+'/results.json')
case('unchanged adapter preserves original role reports/collections and equals paired full merge',passed=True)
assert all(str(m.ROOT)=='/synthetic' and m.Path is MP for m in [PAIRED,BOUNDED,SINGLE,PROOF])
result=dict(input_hashes={n:hashlib.sha256(v).hexdigest() for n,v in SOURCES.items()},
    prior_utility_source=str(prior),prior_utility_sha256=hashlib.sha256(prior.read_bytes()).hexdigest(),
    synthetic_only=True,all_roots_virtual=True,case_count=len(CASES),cases=CASES)
with (OWN/'synthetic-test-results.json').open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(dict(case_count=len(CASES),remaining_reproduced_findings=sorted({c['finding'] for c in CASES if c.get('finding')}),
    strict_paired_equivalence=True,all_roots_virtual=True),indent=2))
