"""Independent transport/IO audit. No gameplay decisions; no original writes.

Runtime retention is an explicit allowlist, never a raw session copy.
"""
from pathlib import Path
import ast, builtins, hashlib, io, json, re, shlex, subprocess, contextlib, sys
sys.dont_write_bytecode = True

OUT = Path(__file__).resolve().parent
I = OUT.parent
R = I.parent.parent
ACTORS = [f'/root/v13_i2_grade_a_{n:02d}' for n in range(1, 7)]
READS = []

def sha(b):
    return hashlib.sha256(b).hexdigest()

def canon(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def read(p):
    b = p.read_bytes()
    READS.append({'path': str(p), 'bytes': len(b), 'sha256': sha(b)})
    return b

def load(p):
    return json.loads(read(p))

def save(name, v):
    p = OUT / name
    with p.open('w') as f:
        f.write(json.dumps(v, ensure_ascii=False, indent=2) + '\n')
    return {'path': str(p), 'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())}

def visible_text(v):
    if isinstance(v, list):
        return [x['text'] for x in v if isinstance(x, dict) and x.get('type') in ['input_text', 'text'] and isinstance(x.get('text'), str)]
    if isinstance(v, str):
        return [v]
    raise ValueError('Unexpected tool-output representation')

def objects(v):
    if isinstance(v, str):
        dec = json.JSONDecoder()
        pos = 0
        while pos < len(v):
            if v[pos] not in '{[':
                pos += 1
                continue
            try:
                obj, end = dec.raw_decode(v, pos)
            except ValueError:
                pos += 1
                continue
            yield obj
            yield from objects(obj)
            pos = end
    elif isinstance(v, dict):
        for x in v.values():
            yield from objects(x)
    elif isinstance(v, list):
        for x in v:
            yield from objects(x)

NODE_CAPTURE = r'''
const vm = require('node:vm');
let data = ''; process.stdin.setEncoding('utf8');
process.stdin.on('data', x => data += x);
process.stdin.on('end', async () => {
 const calls=[];
 const context=vm.createContext({text:()=>{}, tools:{exec_command:async arg=>{calls.push(arg);return {output:''};}}});
 try { await new vm.Script('(async()=>{'+data+'\n})()').runInContext(context,{timeout:2000});
 process.stdout.write(JSON.stringify(calls)); }
 catch(e){process.stderr.write(String(e));process.exitCode=1;}
});
'''

def capture(code):
    # All outer programs were inspected: literals/template construction plus one
    # awaited exec_command and text forwarding. Python text remains inert here.
    assert code.count('tools.exec_command(') == 1
    assert not re.search(r'\b(process|require|fetch|eval|globalThis|import)\s*[.(]', code)
    p = subprocess.run(['node', '-e', NODE_CAPTURE], input=code, capture_output=True, text=True, check=True)
    calls = json.loads(p.stdout)
    assert len(calls) == 1 and set(calls[0]) <= {'cmd', 'max_output_tokens'}
    return calls[0]

def project(r):
    data = read(Path(r['runtime_source']))
    prefix = data[:r['runtime_snapshot_bytes']]
    assert sha(prefix) == r['runtime_snapshot_sha256']
    result = {'actor': r['agent'], 'runtime_path': r['runtime_source'],
              'prefix_bytes': len(prefix), 'prefix_sha256': sha(prefix),
              'current_bytes': len(data), 'current_sha256': sha(data),
              'records': [], 'tools': [], 'contexts': [], 'settings': [], 'identity': []}
    for ordinal, raw in enumerate(data.splitlines(keepends=True), 1):
        x = json.loads(raw)
        y = x.get('payload', {})
        kind = x.get('type')
        anchor = {'physical_ordinal': ordinal, 'record_sha256': sha(raw)}
        # Nonessential record bodies are neither retained nor printed.
        result['records'].append(dict(anchor, record_type=kind))
        if kind == 'session_meta':
            spawn = y.get('source', {}).get('subagent', {}).get('thread_spawn', {})
            result['identity'].append(dict(anchor, agent=y.get('agent_path'), parent_thread_id=y.get('parent_thread_id'),
                source_agent=spawn.get('agent_path'), source_parent_thread_id=spawn.get('parent_thread_id')))
        if kind == 'turn_context':
            result['contexts'].append(dict(anchor, model=y.get('model'), effort=y.get('effort')))
        if kind == 'event_msg' and y.get('type') == 'thread_settings_applied':
            # The event body is not retained. Its literal serialization is only
            # checked for the precise settings already exposed by turn_context.
            settings = y.get('thread_settings', {})
            narrow = {k:settings[k] for k in ['model', 'reasoning_effort'] if k in settings}
            result['settings'].append(dict(anchor, **narrow))
        if kind == 'response_item' and y.get('type') in ['custom_tool_call', 'function_call']:
            result['tools'].append(dict(anchor, kind='call', name=y.get('name'), call_id=y.get('call_id'),
                input=y.get('input', y.get('arguments', ''))))
        if kind == 'response_item' and y.get('type') in ['custom_tool_call_output', 'function_call_output']:
            result['tools'].append(dict(anchor, kind='output', call_id=y.get('call_id'),
                visible_text_fields=visible_text(y.get('output'))))
    assert result['identity'] and all(x['agent'] == r['agent'] and x['source_agent'] == r['agent'] and
           x['parent_thread_id'] == r['parent_thread_id'] == x['source_parent_thread_id'] for x in result['identity'])
    assert result['contexts'] and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in result['contexts'])
    assert result['settings'] and all(x['model'] == 'gpt-6.1-sol' and x['reasoning_effort'] == 'high' for x in result['settings'])
    return result

class MemoryPath:
    files = {}
    events = []
    def __init__(self, path): self.path = str(path)
    def __truediv__(self, rhs): return MemoryPath(self.path + '/' + rhs)
    def __str__(self): return self.path
    def read_bytes(self):
        self.events.append({'operation':'read_bytes', 'path':self.path})
        assert self.path in self.files, 'Disallowed read: ' + self.path
        return self.files[self.path]
    def read_text(self): return self.read_bytes().decode()
    def write_bytes(self, value):
        self.events.append({'operation':'write_bytes', 'path':self.path, 'bytes':len(value), 'sha256':sha(value)})
        assert self.path.endswith('/grades-same-entry.json') and self.path.rsplit('/',1)[0] == self.allowed_base
        self.files[self.path] = value
        return len(value)
    def write_text(self, value): return self.write_bytes(value.encode())

def replay(src, packet_path, packet_bytes):
    # AST was reviewed before replay. Enforce the complete capability boundary
    # again at runtime: imports only stdlib JSON/hashlib and substituted Path;
    # no filesystem, shell, network, dynamic eval, or original writes available.
    tree = ast.parse(src)
    imports=[]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports += [a.name for a in node.names]
            assert all(a.name in ['json', 'hashlib'] for a in node.names)
        if isinstance(node, ast.ImportFrom):
            assert node.module == 'pathlib' and [a.name for a in node.names] == ['Path']
        if isinstance(node, ast.Name):
            assert not node.id.startswith('__') and node.id not in ['open','eval','exec','compile','globals','locals','getattr','setattr','delattr','input']
        if isinstance(node, ast.Attribute): assert not node.attr.startswith('__')
    def imp(name, *args, **kw):
        if name == 'pathlib':
            class M: Path = MemoryPath
            return M
        assert name in ['json','hashlib']
        return {'json':json,'hashlib':hashlib}[name]
    safe = {k:getattr(builtins,k) for k in ['len','range','zip','sum','str','list','any','all','dict','enumerate']}
    safe['__import__'] = imp
    stdout = io.StringIO()
    safe['print'] = lambda *a, **kw: print(*a, file=stdout, **kw)
    with contextlib.redirect_stdout(stdout):
        exec(compile(tree, '<inspected-audit-memory-replay>', 'exec'), {'__builtins__':safe})
    return {'program_sha256':sha(src.encode()), 'imports':imports,
            'stdout_sha256':sha(stdout.getvalue().encode()), 'stdout':stdout.getvalue()}

def main():
    provenance = load(I/'grader-a-terminal-all-date-runtime-provenance.json')
    records = [next(r for r in provenance['records'] if r.get('agent') == actor) for actor in ACTORS]
    strict = load(I/'grading-reader-a-input-delivery-proof.json')
    manifest = load(I/'grading-reader-a/packet-manifest.json')
    raw_reader = load(I/'reader-a.json')
    freeze = load(I/'reader-a-terminal-freeze.json')
    assert freeze['files'][str(I/'reader-a.json')]['sha256'] == sha((I/'reader-a.json').read_bytes())
    assert manifest['exact_disjoint_ids'] == [e['id'] for e in raw_reader['answers']]
    assert len(by_ids := [e['id'] for e in raw_reader['answers']]) == len(set(by_ids))
    summary = read(I/'summary-snapshot.md').decode()
    lines = summary.splitlines(keepends=True)
    chunks = [dict(qa_delivery='summary-chunk-v1', start_line=i+1, end_line=min(i+45,len(lines)), text=''.join(lines[i:i+45]), sha256=sha(''.join(lines[i:i+45]).encode())) for i in range(0,len(lines),45)]
    # Read only the generic fixed reader definition; do not import its broader
    # workflow or follow manifest paths beyond the explicit input allowlist.
    helper_src = read(R/'prove-single-reader-grading-delivery-literal-equivalent.py').decode()
    for generic in ['prove-bounded-delivery.py','single-reader-grading-tools.py','block-grading-tools.py']:
        read(R/generic)
    for path in [I/'summary-snapshot.md', I/'reader-a.json']:
        assert sha(path.read_bytes()) == manifest['input_hashes'][str(path)]
    helper_ast = ast.parse(helper_src)
    fixed_reader = next(ast.literal_eval(n.value) for n in helper_ast.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='READ_SCRIPT' for t in n.targets))
    by_id = {e['id']:e for e in raw_reader['answers']}
    all_results=[]
    for n,r in enumerate(records,1):
        block=f'block-{n:02d}'
        folder=I/'grading-reader-a'/block
        packet_bytes=read(folder/'packet.json'); packet=json.loads(packet_bytes)
        original=read(folder/'grades-same-entry.json')
        integrity=load(folder/'parent-grade-integrity.json')
        mb=next(b for b in manifest['blocks'] if b['block_id']==block)
        assert sha(packet_bytes)==mb['packet_sha256']
        assert sha(original)==integrity['original_grade_report_sha256']
        assert [e['id'] for e in packet['entries']]==mb['ids']
        assert all(canon(e['reader_a_entry'])==canon(by_id[e['id']]) and sha(canon(e['reader_a_entry']).encode())==mb['complete_raw_entry_sha256s'][e['id']] for e in packet['entries'])
        assert all('reader_b_entry' not in e for e in packet['entries'])
        assert packet['summary_sha256']==sha(summary.encode()) and packet['reader_role']=='reader-a'
        metadata={k:v for k,v in packet.items() if k!='entries'}
        expected={'summary:'+str(c['start_line']-1):c for c in chunks}
        expected['metadata:0']=metadata
        expected.update({'entry:'+str(j):e for j,e in enumerate(packet['entries'])})
        proj=project(r)
        projhash=save(block+'-runtime-projection.json',proj)
        calls={}; outputs={}; deliveries=[]; pre=[]; post=[]; boundary=None; unmatched=[]
        for t in proj['tools']:
            if t['kind']=='call':
                assert t['call_id'] and t['call_id'] not in calls
                assert t['name']=='exec'
                captured=capture(t['input']); cmd=captured['cmd']
                entry=dict(t,command_sha256=sha(cmd.encode()))
                if 'QA_ARTIFACT_WRITE_V1' in t['input'] and boundary is None:
                    boundary=t['physical_ordinal']
                entry['before_boundary']=boundary is None
                if boundary is None:
                    args=shlex.split(cmd)
                    assert args[:2]==['python3','-c'] and args[2]==fixed_reader
                    good=(len(args)==7 and args[3]==str(I/'summary-snapshot.md') and args[4]==str(folder/'packet.json'))
                    if good:
                        key=args[5]+':'+args[6]; assert key in expected
                        entry.update(approved_actual_read=True,expected_key=key)
                    else:
                        # A03's malformed extra invocation has only its own
                        # packet path and fails unpacking before any Path read.
                        assert n==3 and args[3:]==[str(folder/'packet.json'),'summary','225']
                        entry.update(approved_actual_read=True,expected_key=None,behavior='argument unpacking error before filesystem read')
                    pre.append({k:v for k,v in entry.items() if k!='input'})
                else:
                    assert cmd.startswith("python3 - <<'PY'\n") and cmd.endswith('\nPY')
                    src=cmd[len("python3 - <<'PY'\n"):-len('\nPY')]
                    post.append((entry,src))
                calls[t['call_id']]=entry
            else:
                assert t['call_id'] not in outputs
                outputs[t['call_id']] = t
                c=calls.get(t['call_id'])
                if c is None: unmatched.append(t['call_id']);continue
                if c['before_boundary']:
                    key=c['expected_key']
                    if key:
                        found=any(canon(v)==canon(expected[key]) for text in t['visible_text_fields'] for v in objects(text))
                        deliveries.append({'expected_key':key,'call_id':t['call_id'],
                            'call_ordinal':c['physical_ordinal'],'call_record_sha256':c['record_sha256'],
                            'output_ordinal':t['physical_ordinal'],'output_record_sha256':t['record_sha256'],
                            'expected_canonical_sha256':sha(canon(expected[key]).encode()),'exact_deep_json_equal':found,
                            'output_before_write_boundary':t['physical_ordinal']<boundary if boundary else True})
                    else:
                        assert any('ValueError: not enough values to unpack (expected 4, got 3)' in text for text in t['visible_text_fields'])
        assert boundary and not unmatched
        assert set(calls)==set(outputs)
        assert all(d['exact_deep_json_equal'] and d['output_ordinal']<boundary for d in deliveries)
        assert {d['expected_key'] for d in deliveries}==set(expected)
        MemoryPath.files={str(folder/'packet.json'):packet_bytes}
        MemoryPath.events=[];MemoryPath.allowed_base=str(folder)
        replay_proofs=[]
        for entry,src in post:
            proof=replay(src,folder/'packet.json',packet_bytes)
            proof.update(call_id=entry['call_id'],physical_ordinal=entry['physical_ordinal'],record_sha256=entry['record_sha256'])
            original_output = outputs[entry['call_id']]
            assert any(canon(v)==canon(json.loads(proof['stdout'])) for text in original_output['visible_text_fields'] for v in objects(text))
            proof.update(actual_call_bound_stdout_matches_replay=True,
                         output_physical_ordinal=original_output['physical_ordinal'],
                         output_record_sha256=original_output['record_sha256'])
            replay_proofs.append(proof)
        reproduced=MemoryPath.files[str(folder/'grades-same-entry.json')]
        assert reproduced==original
        replay_output=save(block+'-replayed-grades.json',json.loads(reproduced))
        assert sha(Path(replay_output['path']).read_bytes())==sha(original)
        result={'actor':r['agent'],'block':block,'runtime_projection':projhash,
            'frozen_strict_confirmed':strict[block]['complete_input_delivery_confirmed'],
            'frozen_strict_unapproved_call_count':len(strict[block]['unapproved_pre_boundary_tool_calls']),
            'actual_complete_source_metadata_all_opaque_entries_delivered_before_write':True,
            'delivery_checks':deliveries,'pre_boundary_commands':pre,'first_write_boundary_ordinal':boundary,
            'all_actual_contexts_sol_high_and_actor_parent_confirmed':True,
            'all_post_boundary_programs_inspected_and_memory_replayed':True,'post_boundary_program_count':len(post),
            'replay_proofs':replay_proofs,'memory_IO_events':MemoryPath.events,
            'only_own_packet_and_own_output_actual_postboundary_IO':True,
            'cleanup_paths':[],'literal_model_selected_decisions_only':True,
            'byte_for_byte_report_reproduction':True,'original_report_sha256':sha(original),'replay_report':replay_output,
            'limitations':'Technical delivery, construction and IO proof only; no gameplay regrading, correctness inference, factual score cap or authority cap.'}
        all_results.append(result)
    # Verify inspected original files and all six runtimes stayed unchanged.
    unchanged=[]
    for rec in READS:
        assert sha(Path(rec['path']).read_bytes())==rec['sha256']
        unchanged.append({'path':rec['path'],'sha256':rec['sha256'],'unchanged':True})
    save('input-read-records.json',READS)
    save('originals-unchanged.json',unchanged)
    audit={'audit_kind':'independent actual IO/settings/transport; not gameplay grading',
        'actors':all_results,'strict_results_preserved':True,'original_files_unchanged':True,
        'privacy_policy':'Only allowlisted tool-call input and model-visible textual tool-output fields, narrow model/effort/actor/parent fields, physical ordinals and hashes retained. No raw runtime copies or message/reasoning/session-context bodies.',
        'scope_deviation':'Initial provenance-key discovery accidentally printed narrow runtime path/model/effort metadata for all provenance records before filtering. No other runtime was opened; no message, reasoning, account, profile, task, or context body was printed or retained. Subsequent processing and retained projections are restricted to the six actors.',
        'decision_code_inspection':'All grades, reasons, quote selections and covered status are model-written literals or literal constructions. Loops only attach fixed requested atoms in order, repeat/assemble selected quotes, assert exact substring membership/count/ID consistency and serialize. No code selects semantic coverage from answer text. A01 has one literal quote-addition follow-up. No cleanup or auxiliary file path exists.',
        'qualifications':[
            'A03 strict false is unchanged. One additional malformed fixed-reader invocation raises during sys.argv unpacking before Path read; later retry delivers exact source chunk.',
            'A05 strict false is unchanged. All 31 rejected outer calls have the identical fixed reader shell argv and exact call-bound input values; outer JavaScript whitespace differs from strict templates.',
            'Frozen packets preserve complete reader-a opaque entries and match manifest hashes. Key/scope source files named inside packet metadata were not independently opened under this audit scope.',
            'Proof demonstrates observed complete model-visible delivery, restricted program IO and literal-decision reproduction; it does not prove attention or factual correctness.']}
    save('audit.json',audit)
    md=['# Reader A completion IO audit 01','',
        'All six actors received the complete source, metadata and every complete assigned opaque entry before their first report write. All contexts are gpt-6.1-sol/high with the expected actor and parent. All six primary reports reproduce byte for byte using inspected programs with filesystem operations replaced by an in-memory allowlist. Originals are unchanged.','',
        '| Block | Frozen strict | Actual input delivery | Report byte replay |','|---|---|---|---|']
    md += [f"| {x['block']} | {'PASS' if x['frozen_strict_confirmed'] else 'FALSE (preserved)'} | Complete | Exact |" for x in all_results]
    md += ['', 'A03’s extra fixed-reader call fails argument unpacking before any file read; the valid retry delivers the missing chunk. A05 uses identical fixed shell commands with outer JavaScript whitespace differences. These actual findings do not change either frozen strict false result.', '',
        'Post-boundary programs read only their own packet and, for A01’s follow-up and A06’s hash, their own report. They write only their own report. Every grade, coverage status, reason and quote selection is literal model-selected material; the code only checks identity, counts and literal substrings and assembles the report. No cleanup path, semantic coverage algorithm, factual score cap or authority cap was found.', '',
        'Replay executes inspected Python only with substituted in-memory Path and restricted imports/builtins. The original shell and original write paths are never executed by this audit. The saved replay files have the exact original report SHA-256 values.', '',
        'Retained evidence contains only allowlisted tool fields, narrow settings/identity metadata, original physical ordinals and record hashes. No raw sessions or prohibited message/context/reasoning bodies are copied. Initial provenance discovery accidentally printed narrow runtime path/model/effort metadata for other provenance records; no other runtime was opened, and none of that metadata is retained here.', '',
        'This is a technical delivery/IO audit, not gameplay regrading or proof of attention/correctness. Key and scope files referenced inside packet metadata were not opened.', '',
        'Evidence: `audit.json`, `input-read-records.json`, `originals-unchanged.json`, and six minimal runtime projections plus six exact replayed reports.']
    with (OUT/'audit.md').open('w') as f:f.write('\n'.join(md)+'\n')
    print(json.dumps({'actors':len(all_results),'complete_actual_delivery':all(x['actual_complete_source_metadata_all_opaque_entries_delivered_before_write'] for x in all_results),'exact_replays':len(all_results),'output':str(OUT)}))

if __name__=='__main__':main()
