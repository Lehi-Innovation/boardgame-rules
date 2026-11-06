"""Narrow, read-only original evidence audit; all writes confined to this directory.

Runtime evidence is an explicit projection, never a raw runtime copy. Programs are
replayed only after AST/shell review, against an in-memory Path capability.
"""
from pathlib import Path
import ast
import builtins
import contextlib
import hashlib
import io
import json
import re
import shlex
import types

OUT = Path(__file__).resolve().parent
I = OUT.parent
R = I.parent.parent
ACTORS = [f'/root/v13_i2_grade_b_{n:02d}' for n in range(1, 7)]
PARENT = '01a1aaa2-7c89-7c92-bca8-a89efc3fe4d7'
read_records = []
input_bytes = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canon(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def read(path, reason):
    path = Path(path)
    raw = path.read_bytes()
    input_bytes[str(path)] = raw
    read_records.append(dict(path=str(path), reason=reason, bytes=len(raw), sha256=sha(raw)))
    return raw


def load(path, reason):
    return json.loads(read(path, reason))


def save(name, value):
    p = OUT / name
    assert p.parent.resolve().is_relative_to(OUT)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def command(code, expected_tokens=None, marker=False):
    """Parse the entire outer JS as a single literal shell command + text output.

    This evaluates no JS. The only optional concatenation is two JSON strings.
    """
    body = code.strip()
    if body.startswith('// @exec:'):
        pragma, body = body.split('\n', 1)
        json.loads(pragma.split(':', 1)[1])
        body = body.strip()
    if marker:
        assert body.startswith('// QA_ARTIFACT_WRITE_V1\n')
        body = body.split('\n', 1)[1].strip()
    direct_text = body.startswith('text(await tools.exec_command(')
    head = r'text\(await\s+tools\.exec_command\(\{cmd\s*:\s*' if direct_text else r'const\s+r\s*=\s*await\s+tools\.exec_command\(\{cmd\s*:\s*'
    m = re.match(head, body)
    assert m, 'Unexpected JS head'
    decoder = json.JSONDecoder()
    cmd, end = decoder.raw_decode(body[m.end():])
    assert isinstance(cmd, str)
    rest = body[m.end()+end:].lstrip()
    if rest.startswith('+'):
        rest = rest[1:].lstrip()
        suffix, end = decoder.raw_decode(rest)
        assert isinstance(suffix, str)
        cmd += suffix
        rest = rest[end:].lstrip()
    tail = r',\s*max_output_tokens\s*:\s*(\d+)\s*\}\)\);' if direct_text else r',\s*max_output_tokens\s*:\s*(\d+)\s*\}\);\s*text\(r\.output\);'
    m = re.fullmatch(tail, rest)
    assert m, 'Unexpected JS tail'
    if expected_tokens is not None:
        assert int(m[1]) == expected_tokens
    return cmd


def texts(output):
    # Runtime outputs are explicit input_text transport blocks. No incoming
    # messages, reasoning, world_state, or encrypted data enter this function.
    assert isinstance(output, list)
    assert all(isinstance(x, dict) and x.get('type') == 'input_text' and isinstance(x.get('text'), str) for x in output)
    return [x['text'] for x in output]


def decoded_output(output):
    out = []
    for text in texts(output):
        try:
            value = json.loads(text)
            if isinstance(value, dict) and {'chunk_id', 'wall_time_seconds', 'exit_code', 'output'} <= set(value):
                assert value['exit_code'] == 0 and isinstance(value['output'], str)
                out.append((value['output'].strip(), json.loads(value['output'])))
            else:
                out.append((text.strip(), value))
        except ValueError:
            pass
    return out


allowed_direct = {'Path', 'dict', 'enumerate', 'len', 'print', 'str', 'sum', 'zip',
                  'all', 'any', 'isinstance', 'range', 'set', 'tuple', 'list',
                  'choose', 'add', 'C', 'O', 'X'}
allowed_attrs = {'append', 'dumps', 'encode', 'get', 'hexdigest', 'loads',
                 'read_text', 'read_bytes', 'sha256', 'write_bytes', 'write_text'}


def prove_program_safety(py, block):
    """Conservative AST gate plus recorded manual dataflow/shell review.

    These exact six programs have been inspected statement by statement. This
    gate supplements that review; it is not a general Python sandbox theorem.
    """
    tree = ast.parse(py)
    imports, direct, attrs, file_ops = [], set(), set(), []
    for node in ast.walk(tree):
        assert not isinstance(node, (ast.With, ast.AsyncWith, ast.ClassDef, ast.Lambda,
                                     ast.Try, ast.Raise, ast.Delete, ast.Global,
                                     ast.Nonlocal, ast.Await, ast.Yield, ast.YieldFrom))
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name in {'json', 'hashlib'} and alias.asname is None
                imports.append(alias.name)
        if isinstance(node, ast.ImportFrom):
            assert node.module == 'pathlib' and [(a.name, a.asname) for a in node.names] == [('Path', None)]
            imports.append('pathlib.Path')
        if isinstance(node, ast.Attribute):
            attrs.add(node.attr)
            assert node.attr in allowed_attrs
        if isinstance(node, ast.Name):
            assert not node.id.startswith('__')
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                direct.add(node.func.id)
                assert node.func.id in allowed_direct
                if node.func.id == 'Path':
                    assert len(node.args) == 1 and ast.literal_eval(node.args[0]) == str(I / 'grading-reader-b' / block)
            else:
                assert isinstance(node.func, ast.Attribute)
                if node.func.attr in {'read_text', 'read_bytes', 'write_text', 'write_bytes'}:
                    file_ops.append(dict(line=node.lineno, operation=node.func.attr, receiver=ast.unparse(node.func.value)))
    # Actual source-to-output paths are simple base/path assignments, reviewed
    # below and enforced independently by the replay Path capability.
    return dict(imports=sorted(set(imports)), direct_calls=sorted(direct),
                attribute_names=sorted(attrs), file_operations=file_ops,
                no_dynamic_execution_or_network_or_process_api=True,
                manual_all_statements_and_shell_review=True,
                safety_proven_before_extraction_and_replay=True)


def replay(py, packet_path, original_output, packet_raw):
    """Run original Python bytes without filesystem writes or ambient Path reads."""
    memory = {}
    operations = []

    class MemoryPath:
        def __init__(self, path):
            self.path = str(path)

        def __truediv__(self, child):
            return MemoryPath(self.path + '/' + child)

        def __str__(self):
            return self.path

        def read_bytes(self):
            if self.path == str(packet_path):
                data = packet_raw
                origin = 'frozen-own-packet'
            else:
                assert self.path == str(original_output) and self.path in memory, self.path
                data = memory[self.path]
                origin = 'own-replayed-output-after-write'
            operations.append(dict(operation='read_bytes', path=self.path, origin=origin, bytes=len(data), sha256=sha(data)))
            return data

        def read_text(self):
            return self.read_bytes().decode()

        def write_bytes(self, data):
            assert self.path == str(original_output), self.path
            assert isinstance(data, bytes)
            memory[self.path] = data
            operations.append(dict(operation='write_bytes_in_memory', path=self.path, bytes=len(data), sha256=sha(data)))
            return len(data)

        def write_text(self, text):
            self.write_bytes(text.encode())
            return len(text)

    def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        assert level == 0
        if name == 'pathlib':
            assert tuple(fromlist) == ('Path',)
            return types.SimpleNamespace(Path=MemoryPath)
        assert name in {'json', 'hashlib'}
        return {'json': json, 'hashlib': hashlib}[name]

    b = {name: getattr(builtins, name) for name in allowed_direct if hasattr(builtins, name)}
    b.update(__import__=safe_import, AssertionError=AssertionError)
    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        exec(compile(py, '<original-audited-program>', 'exec'), {'__builtins__': b})
    assert set(memory) == {str(original_output)}
    return memory[str(original_output)], operations, captured.getvalue()


def main():
    summary_raw = read(I / 'summary-snapshot.md', 'Frozen sole summary source')
    summary = summary_raw.decode()
    raw_reader = load(I / 'reader-b.json', 'Original terminal reader B; exact packet binding only')
    freeze = load(I / 'reader-b-terminal-freeze.json', 'Terminal frozen reader hash')
    manifest = load(I / 'grading-reader-b/packet-manifest.json', 'Own-role packet boundaries and frozen hashes')
    strict_raw = read(I / 'grading-reader-b-input-delivery-proof.json', 'Preserved strict result and literal-call grammar')
    strict = json.loads(strict_raw)
    provenance_raw = read(I / 'grader-b-terminal-all-date-runtime-provenance.json', 'Select ONLY the six named grading actor records; other entries uninspected')
    provenance = [x for x in json.loads(provenance_raw)['records'] if x.get('agent') in ACTORS]
    assert len(provenance) == 6
    fixed_src = read(R / 'prove-single-reader-grading-delivery-literal-equivalent.py', 'Static fixed read program and strict grammar').decode()
    read(R / 'prove-bounded-delivery.py', 'Referenced transport decoder; static inspection only')
    read(R / 'single-reader-grading-tools.py', 'Static grading assembly/validator contract; never invoked')
    read(R / 'block-grading-tools.py', 'Static substantive-string and integrity contract; never invoked')
    fixed_tree = ast.parse(fixed_src)
    READ_SCRIPT = next(ast.literal_eval(n.value) for n in fixed_tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'READ_SCRIPT' for t in n.targets))
    # This exact code was inspected: only Path(...).read_text, hashing, JSON
    # serialization, and print. Argument unpacking precedes every file read.
    read_tree = ast.parse(READ_SCRIPT)
    assert all(not isinstance(n, ast.Attribute) or n.attr not in {'write_text', 'write_bytes', 'open'} for n in ast.walk(read_tree))
    assert isinstance(read_tree.body[2], ast.Assign)
    assert [t.id for t in read_tree.body[2].targets[0].elts] == ['summary_path', 'packet_path', 'mode', 'index']
    assert ast.unparse(read_tree.body[2].value) == 'sys.argv[1:]'
    lines = summary.splitlines(keepends=True)
    assert ''.join(lines).encode() == summary_raw
    chunks = []
    for start in range(0, len(lines), 45):
        text = ''.join(lines[start:start+45])
        chunks.append(dict(qa_delivery='summary-chunk-v1', start_line=start+1,
                           end_line=min(start+45, len(lines)), text=text, sha256=sha(text.encode())))
    assert len(chunks) == 11
    originals = raw_reader['answers']
    by_id = {e['id']: e for e in originals}
    assert len(by_id) == 116 and [e['id'] for e in originals] == manifest['exact_disjoint_ids']
    assert freeze['files'][str(I / 'reader-b.json')]['sha256'] == sha(input_bytes[str(I / 'reader-b.json')])
    assert manifest['input_hashes'][str(I / 'reader-b.json')] == sha(input_bytes[str(I / 'reader-b.json')])
    assert manifest['input_hashes'][str(I / 'summary-snapshot.md')] == sha(summary_raw)
    blocks = []
    for num, mb in enumerate(manifest['blocks'], 1):
        block = mb['block_id']
        actor = f'/root/v13_i2_grade_b_{num:02d}'
        folder = I / 'grading-reader-b' / block
        packet_path, output_path = folder / 'packet.json', folder / 'grades-same-entry.json'
        packet_raw = read(packet_path, 'Own full-entry packet for delivery equality and safe replay')
        packet = json.loads(packet_raw)
        report_raw = read(output_path, 'Original report bytes; compare only, never execute writes over it')
        integrity = load(folder / 'parent-grade-integrity.json', 'Prior frozen report hash binding; not semantic authority')
        assert sha(packet_raw) == mb['packet_sha256']
        assert sha(report_raw) == integrity['original_grade_report_sha256']
        assert packet['block_id'] == block and packet['reader_role'] == 'reader-b'
        assert packet['summary_path'] == str(I / 'summary-snapshot.md') and packet['summary_sha256'] == sha(summary_raw)
        assert [e['id'] for e in packet['entries']] == mb['ids']
        for e in packet['entries']:
            assert e['reader_b_entry'] == by_id[e['id']]
            assert sha(canon(e['reader_b_entry'])) == mb['complete_raw_entry_sha256s'][e['id']]
            assert 'reader_a_entry' not in e
        metadata = {k: v for k, v in packet.items() if k != 'entries'}
        pr = next(x for x in provenance if x['agent'] == actor)
        runtime_path = Path(pr['runtime_source'])
        # Read original runtime only. Retain raw bytes in memory for hashing;
        # never write those bytes or broad metadata to the audit directory.
        runtime_raw = read(runtime_path, 'Original six-actor runtime: narrow identity/settings and actual tool calls/outputs only')
        prefixbytes = pr['runtime_snapshot_bytes']
        assert sha(runtime_raw[:prefixbytes]) == pr['runtime_snapshot_sha256']
        assert len(runtime_raw) == prefixbytes, 'Any later runtime suffix requires separate inspection'
        projection = dict(actor=actor, original_runtime_path=str(runtime_path),
                          prefixbytes=prefixbytes, prefix_sha256=sha(runtime_raw[:prefixbytes]),
                          original_bytes=len(runtime_raw), original_sha256=sha(runtime_raw),
                          policy='Explicit allowlist: narrow identity/settings; actual tool input/output text only. All other records hash-only; no message/reasoning/encrypted/world_state bodies.', records=[])
        calls, outputs, contexts, identities, setting_events = [], {}, [], [], []
        seen_ids = set()
        offset = 0
        for ordinal, physical in enumerate(runtime_raw.splitlines(keepends=True), 1):
            d = json.loads(physical)
            p = d.get('payload', {})
            rec = dict(physical_record_ordinal=ordinal, byte_offset=offset, physical_bytes=len(physical), physical_record_sha256=sha(physical), type=d.get('type'))
            offset += len(physical)
            if isinstance(p, dict) and isinstance(p.get('type'), str):
                rec['payload_type'] = p['type']
            if d.get('type') == 'session_meta':
                narrow = {k: p.get(k) for k in ['id', 'session_id', 'parent_thread_id', 'agent_path']}
                rec['identity'] = narrow
                identities.append(narrow)
            elif d.get('type') == 'turn_context':
                narrow = {k: p.get(k) for k in ['model', 'effort']}
                rec['settings'] = narrow
                contexts.append(dict(physical_record_ordinal=ordinal, **narrow))
            elif d.get('type') == 'event_msg' and p.get('type') == 'thread_settings_applied':
                s = p.get('thread_settings', {})
                narrow = {k: s.get(k) for k in ['model', 'reasoning_effort']}
                assert narrow == dict(model='gpt-6.1-sol', reasoning_effort='high')
                rec['settings'] = narrow
                setting_events.append(dict(physical_record_ordinal=ordinal, kind='thread_settings_applied', **narrow))
            elif d.get('type') == 'response_item' and p.get('type') == 'configuration_update':
                # This payload is an effort-setting object, not a reasoning
                # message. Project only its single allowed effort field.
                narrow = dict(effort=p.get('reasoning', {}).get('effort'))
                assert narrow == dict(effort='high')
                rec['settings'] = narrow
                setting_events.append(dict(physical_record_ordinal=ordinal, kind='configuration_update', **narrow))
            elif d.get('type') == 'response_item' and p.get('type') in ['custom_tool_call', 'function_call']:
                c = dict(name=p.get('name'), call_id=p.get('call_id'), input=p.get('input', p.get('arguments', '')),
                         physical_record_ordinal=ordinal, physical_record_sha256=sha(physical))
                assert c['call_id'] and c['call_id'] not in seen_ids
                seen_ids.add(c['call_id'])
                calls.append(c)
                rec['tool_call'] = {k:c[k] for k in ['name', 'call_id', 'input']}
            elif d.get('type') == 'response_item' and p.get('type') in ['custom_tool_call_output', 'function_call_output']:
                assert p.get('call_id') in seen_ids and p['call_id'] not in outputs
                # Only literal input_text text is retained. No arbitrary nested
                # metadata from the transport record is copied.
                text_blocks = texts(p.get('output'))
                o = dict(call_id=p['call_id'], physical_record_ordinal=ordinal,
                         physical_record_sha256=sha(physical), text_blocks=text_blocks)
                outputs[p['call_id']] = o
                rec['tool_output'] = dict(call_id=o['call_id'], text_blocks=text_blocks)
            projection['records'].append(rec)
        assert offset == len(runtime_raw)
        assert len(identities) == 1 and identities[0]['agent_path'] == actor
        assert identities[0]['id'] == pr['session_id']
        # In these runtime headers `id` identifies the child rollout, while
        # `session_id` identifies the root chat. Preserve both without conflation.
        assert identities[0]['session_id'] == PARENT
        assert identities[0]['parent_thread_id'] == pr['parent_thread_id'] == PARENT
        assert contexts and all(c['model'] == 'gpt-6.1-sol' and c['effort'] == 'high' for c in contexts)
        assert set(outputs) == seen_ids
        assert all(c['name'] == 'exec' for c in calls)
        boundary_index = next(j for j,c in enumerate(calls) if '// QA_ARTIFACT_WRITE_V1\n' in c['input'])
        boundary = calls[boundary_index]
        assert boundary['call_id'] == strict[block]['first_possible_artifact_write_boundary']['call_id']
        pre = calls[:boundary_index]
        deliveries, errors = [], []
        found = set()
        for c in pre:
            cmd = command(c['input'], expected_tokens=24000)
            argv = shlex.split(cmd)
            assert argv[:2] == ['python3', '-c'] and argv[2] == READ_SCRIPT
            o = outputs[c['call_id']]
            assert c['physical_record_ordinal'] < o['physical_record_ordinal'] < boundary['physical_record_ordinal']
            delivery = dict(call_id=c['call_id'], call_record_ordinal=c['physical_record_ordinal'],
                            output_record_ordinal=o['physical_record_ordinal'],
                            call_record_sha256=c['physical_record_sha256'], output_record_sha256=o['physical_record_sha256'],
                            command_sha256=sha(cmd.encode()), fixed_read_program_sha256=sha(READ_SCRIPT.encode()),
                            output_before_first_possible_write=True)
            if len(argv) == 6:
                assert block in {'block-03', 'block-06'}
                assert argv[3:] == [str(packet_path), 'summary', '225' if num == 3 else '315']
                assert cmd == shlex.join(['python3', '-c', READ_SCRIPT, str(packet_path)]) + ' summary ' + argv[-1]
                assert any('ValueError: not enough values to unpack (expected 4, got 3)' in s for s in o['text_blocks'])
                assert not decoded_output([dict(type='input_text', text=s) for s in o['text_blocks']])
                delivery.update(kind='malformed-read', argv_after_program=argv[3:],
                                result='Argument unpacking ValueError on line 3, before any Path/read call',
                                file_reads=0, writes=0, delivery_credit=False)
                errors.append(delivery)
                continue
            assert len(argv) == 7 and argv[3:5] == [str(I/'summary-snapshot.md'), str(packet_path)]
            mode, index = argv[5], int(argv[6])
            assert cmd == shlex.join(['python3', '-c', READ_SCRIPT, str(I/'summary-snapshot.md'), str(packet_path)]) + f' {mode} {index}'
            if mode == 'summary':
                expected = next(x for x in chunks if x['start_line'] == index+1)
                key = 'summary:' + str(index+1)
            elif mode == 'metadata':
                assert index == 0
                expected, key = metadata, 'metadata'
            else:
                assert mode == 'entry'
                expected = packet['entries'][index]
                key = expected['id']
            candidates = decoded_output([dict(type='input_text', text=s) for s in o['text_blocks']])
            assert len(candidates) == 1
            exact = [(text, value) for text,value in candidates if value == expected and canon(value) == canon(expected)]
            assert len(exact) == 1, (block,key)
            visible_text = exact[0][0]
            expected_serialization = json.dumps(expected, ensure_ascii=False)
            assert visible_text.encode() == expected_serialization.encode(), (block,key,'serialized bytes')
            exact_stdout = [s for s in o['text_blocks'] if s.strip() == visible_text]
            assert exact_stdout == [expected_serialization + '\n']
            assert not any('Warning: truncated output' in s for s in o['text_blocks'])
            found.add(key)
            delivery.update(kind=mode, item=key, exact_deep_json_equal=True,
                            exact_utf8_json_serialization_equal=True,
                            expected_canonical_sha256=sha(canon(expected)),
                            actual_canonical_sha256=sha(canon(exact[0][1])),
                            actual_json_utf8_sha256=sha(visible_text.encode()),
                            expected_json_utf8_sha256=sha(expected_serialization.encode()),
                            actual_json_utf8_bytes=len(visible_text.encode()),
                            full_stdout_including_print_newline_byte_equal=True,
                            full_stdout_utf8_sha256=sha(exact_stdout[0].encode()),
                            permitted_read_paths=[str(I/'summary-snapshot.md')] if mode == 'summary' else [str(packet_path)],
                            writes=0, delivery_credit=True)
            if mode == 'summary':
                assert exact[0][1]['text'].encode() == expected['text'].encode()
                delivery['source_chunk_utf8_sha256'] = sha(expected['text'].encode())
                delivery['source_chunk_utf8_bytes'] = len(expected['text'].encode())
            deliveries.append(delivery)
        expected_keys = {'metadata'} | {f"summary:{c['start_line']}" for c in chunks} | {e['id'] for e in packet['entries']}
        assert found == expected_keys
        assert len(deliveries) == len(expected_keys)
        # Inspect every post-boundary shell program BEFORE extracting or replaying.
        post = calls[boundary_index:]
        shell_proofs, programs, program = [], [], None
        for c in post:
            cmd = command(c['input'], marker=True)
            if cmd == 'rm /tmp/grade_b01.py':
                assert num == 1 and c is post[-1]
                shell_proofs.append(dict(call_id=c['call_id'], shell_command=cmd,
                                         operation='delete only this actor temporary source file',
                                         report_writes=False))
                continue
            if num == 1:
                header = "cat > /tmp/grade_b01.py <<'PY'\n"
                trailer = '\nPY\npython3 /tmp/grade_b01.py'
                assert cmd.startswith(header) and cmd.endswith(trailer)
                py = cmd[len(header):-len(trailer)]
                shell_io = [dict(operation='write-temporary-own-program', path='/tmp/grade_b01.py'),
                            dict(operation='execute-temporary-own-program', path='/tmp/grade_b01.py')]
            else:
                header, trailer = "python3 - <<'PY'\n", '\nPY'
                assert cmd.startswith(header) and cmd.endswith(trailer)
                py = cmd[len(header):-len(trailer)]
                shell_io = []
            assert program is None
            safety = prove_program_safety(py, block)
            program = py
            safety.update(call_id=c['call_id'], call_record_ordinal=c['physical_record_ordinal'],
                          program_utf8_sha256=sha(py.encode()), shell_command_sha256=sha(cmd.encode()),
                          shell_io=shell_io)
            programs.append(safety)
        assert program is not None
        # Saving original tool programs is permitted only after the safety proof.
        (OUT / 'programs').mkdir(exist_ok=True)
        (OUT / 'programs' / f'{block}.py').write_text(program)
        replayed, operations, stdout = replay(program, packet_path, output_path, packet_raw)
        assert replayed == report_raw, (block, 'byte-for-byte reproduction failed')
        # The original actual artifact-call output independently binds the same SHA.
        original_artifact_output = decoded_output([dict(type='input_text', text=s) for s in outputs[boundary['call_id']]['text_blocks']])
        assert len(original_artifact_output) == 1
        original_artifact_value = original_artifact_output[0][1]
        assert original_artifact_value['sha256'] == sha(report_raw)
        assert original_artifact_value['path'] == str(output_path)
        replay_value = json.loads(stdout)
        assert replay_value == original_artifact_value
        (OUT / 'replayed').mkdir(exist_ok=True)
        (OUT / 'replayed' / f'{block}-grades-same-entry.json').write_bytes(replayed)
        report = json.loads(report_raw)
        grades = report['readers']['reader-b']['grades']
        assert [g['id'] for g in grades] == mb['ids']
        selected = [dict(id=g['id'], grade=g['grade'],
                         statuses=[p['status'] for p in g['material_parts']],
                         reason_sha256=sha(g['reason'].encode()),
                         selected_quotes_sha256=sha(canon([p['reader_quotes'] for p in g['material_parts']])) ) for g in grades]
        decision_notes = {
            1: 'quotes/extras/partial are literal dictionaries. Literal partial IDs select Partial/omitted; all other IDs select Correct/covered. Code only inserts requested fact strings and checks selected literal quotes occur.',
            2: 'quotes/reasons are literal dictionaries. Q032 is an explicit literal Partial choice; None in literal selected quotes means omitted, otherwise covered. Quote membership assertions do not choose grades.',
            3: 'chosen/reasons are literal dictionaries; every grade/status is an explicit Correct/covered constant. Code zips selected literal quotes onto requested atoms and checks membership.',
            4: 'choose calls give each ID its literal grade, omitted indices, quotes, reason and issue; default Correct is fixed. Helpers assemble these declarations; assertions only verify selected quote transport.',
            5: 'Each add call explicitly gives ID, grade, reason, and parts; C/O/X construct fixed covered/omitted/contradicted status. Code validates selected quote membership and assembles output; it does not discover decisions.',
            6: 'choices and issues are literal data. Grade/reason/quotes are chosen there; a literal empty quote list marks omitted. Code zips selected data to packet facts and validates membership.'
        }
        save(f'projections/{block}.json', projection)
        save(f'delivery/{block}.json', dict(actor=actor, boundary_call_id=boundary['call_id'],
             boundary_record_ordinal=boundary['physical_record_ordinal'],
             last_required_delivery_output_record_ordinal=max(x['output_record_ordinal'] for x in deliveries),
             full_original_summary_reassembled_sha256=sha(''.join(c['text'] for c in chunks).encode()),
             full_original_summary_byte_equal=True, matched_deliveries=deliveries, failed_calls=errors))
        save(f'replay/{block}.json', dict(actor=actor, inspected_programs=programs, shell_cleanup=shell_proofs,
             literal_model_selected_decisions=selected, decision_dataflow_review=decision_notes[num],
             semantic_grading_automated_by_code=False,
             replay_operations=operations, real_filesystem_writes_during_replay=0,
             original_report_sha256=sha(report_raw), replayed_report_sha256=sha(replayed),
             byte_for_byte_report_equal=True, report_bytes=len(report_raw),
             original_actual_output_value=original_artifact_value,
             replay_stdout_deep_json_equal_original_actual_output=True))
        deviation = ('32 whitespace-different outer JS calls; all 32 exact fixed read commands succeed' if num == 1 else
                     '32 whitespace-different outer JS calls: 31 exact fixed reads succeed; one missing-summary-path call fails before IO' if num == 3 else
                     'One extra missing-summary-path call fails before IO; all 31 exact fixed reads succeed' if num == 6 else
                     'No strict interface departure')
        blocks.append(dict(block_id=block, actor=actor,
             original_runtime_path=str(runtime_path), runtime_prefixbytes=prefixbytes,
             runtime_prefix_sha256=sha(runtime_raw), identity_and_parent_match=True,
             actual_identity=identities[0],
             all_actual_turn_contexts=contexts, all_actual_contexts_sol_high=True,
             narrow_thread_and_configuration_setting_events=setting_events,
             packet_frozen_hash_and_full_original_reader_entries_match=True,
             original_grade_hash_matches_parent_integrity=True,
             strict_frozen_proof_pass=strict[block]['complete_input_delivery_confirmed'],
             strict_unrecognized_preboundary_calls=len(strict[block]['unapproved_pre_boundary_tool_calls']),
             departure=deviation, successful_summary_chunks=11, successful_metadata_values=1,
             successful_complete_entries=len(packet['entries']), failed_read_calls=len(errors),
             all_actual_required_delivery_before_first_possible_write=True,
             preboundary_only_permitted_readonly_or_fail_before_io=True,
             no_other_agent_or_status_tool_calls=True,
             post_boundary_program_count=len(programs), post_boundary_cleanup_calls=len(shell_proofs),
             postboundary_python_reads_only_own_packet_and_own_written_output=True,
             postboundary_python_writes_only_own_report=True,
             temporary_own_code_artifact='/tmp/grade_b01.py (write, execute, delete)' if num == 1 else None,
             literal_decision_assembly_no_semantic_grading_code=True,
             byte_for_byte_report_reproduced=True,
             actual_original_report_output_sha256_matches=True,
             actual_io_finding='QUALIFIED PASS: complete actual delivery and isolated literal report assembly; strict false remains false' if not strict[block]['complete_input_delivery_confirmed'] else 'PASS'))
    # Verify every original source remains byte-for-byte unchanged after analysis.
    unchanged = []
    for path, before in input_bytes.items():
        after = Path(path).read_bytes()
        assert after == before, path
        unchanged.append(dict(path=path, bytes=len(before), sha256=sha(before), unchanged=True))
    save('read-records.json', read_records)
    save('input-hashes.json', unchanged)
    audit = dict(audit_kind='Fresh independent technical actual delivery/settings/transport/IO audit; no gameplay regrading',
                 output_directory=str(OUT), actors=ACTORS,
                 result='QUALIFIED PASS for all six actual delivery/IO completions; original strict false B01/B03/B06 preserved',
                 strict_frozen_proof={'block-01':False,'block-02':True,'block-03':False,'block-04':True,'block-05':True,'block-06':False},
                 blocks=blocks, original_primary_files_and_strict_proof_unchanged=True,
                 privacy='No raw runtime copies. Only allowlisted narrow identity/model/effort, actual tool calls/outputs, and physical-record ordinals/hashes retained; other runtime records hash-only. No message, incoming task, account/profile, reasoning, encrypted or world_state bodies saved.',
                 evidence_scope='Only the explicitly permitted files and original runtime paths of the six named actors. Manifest references to outside key/question/scope files are not opened; their frozen copies inside own packets are used.',
                 limitations=[
                     'Historical command/output evidence and static submitted-program IO are audited; no OS syscall trace exists, so implicit Python imports/shell startup are not a claim of zero OS-level reads.',
                     'This establishes visible complete delivery, not model attention or semantic correctness. No factual grades, score caps, source authority caps, or key changes are made.',
                     'B01 creates, executes and deletes its own /tmp source helper in addition to its sole report output; no unrelated input is read. This is explicitly qualified, not silently treated as strictly block-directory-only IO.',
                     'Frozen manifest hashes referring to disallowed external files are recorded assertions only; this audit verifies only permitted source files and full reader B entry bindings.',
                     'The strict checker is not edited or relaxed; its false results are retained separately from the qualified actual-delivery result.'
                 ])
    save('audit.json', audit)
    rows = '\n'.join(f"| {b['block_id']} | {'PASS' if b['strict_frozen_proof_pass'] else 'false'} | 11 / 1 / {b['successful_complete_entries']} | {b['failed_read_calls']} | yes |" for b in blocks)
    md = f'''# Reader B completion IO audit 01

**Qualified actual-delivery/IO PASS for all six original actors.** Every full original summary chunk, own-packet metadata value and complete assigned entry reached a matched call-ID output before the first possible write. All six reports reproduce byte for byte in a replay using in-memory writes. All actual contexts are `gpt-6.1-sol` / `high`, with the original actor and parent IDs confirmed.

| Block | Preserved strict proof | Delivered chunks / metadata / entries | Failed reads before IO | Byte-identical report replay |
|---|---|---|---|---|
{rows}

B01 has 32 outer-JavaScript whitespace departures; all 32 fixed shell read commands are identical to the permitted commands. B03 has 32 unrecognized calls: 31 successful fixed reads with outer-JavaScript whitespace differences and one malformed call missing the summary path. B06 has one extra malformed call missing that path. Each malformed call raises `ValueError: not enough values to unpack (expected 4, got 3)` at argument unpacking, before the first file read. Later successful calls supply the missing chunks. The strict false findings remain false, and the checker and frozen proof remain unchanged.

Every post-boundary shell and Python statement was inspected before extraction/replay. Python reads only its own packet and, where used, its own report after writing it; it writes only its own `grades-same-entry.json`. B01 additionally writes, executes and deletes its own `/tmp/grade_b01.py` source helper. That temporary artifact is an explicit qualification to block-directory-only IO. No other agent/status calls or foreign-data reads occur in the submitted programs.

Grades, per-atom statuses, selected quotes, reasons and issues originate in literal model-authored decision declarations. Loops insert packet IDs and required-fact text, validate counts and literal quote membership, assemble JSON and hash it. None of these programs performs semantic grading. This audit does not assess whether the selected gameplay decisions are correct.

`delivery/` records each actual call and output ordinal/hash, exact deep JSON equality and exact UTF-8 JSON serialization equality. Summary chunk text additionally matches original source bytes; concatenating all chunks matches the complete source SHA. `replay/` records the static program review, literal decision dataflow, constrained IO operations, actual output SHA and exact report reproduction. `programs/` contains only the six safety-reviewed original report programs; `replayed/` contains audit-owned reproduced reports. `projections/` contains explicit minimal runtime projections with original path, prefix length/SHA, physical record ordinals/hashes and needed tool fields. Every other runtime record is hash-only; private, incoming-task, message, reasoning, world-state and encrypted bodies are omitted.

`input-hashes.json` verifies that every original permitted file and runtime remained unchanged. `read-records.json` states the permitted reads and their purpose. No other reader, source rulebook, external key/question/scope file, audit history, web source or agent/status tool was consulted. The provenance document is used only for the six named actor entries.

The finding concerns recorded command/output delivery and explicit submitted-program IO. It does not supply a historical OS syscall trace or prove model attention. No content-score cap, gameplay regrading, source-authority cap or new key is introduced.
'''
    (OUT / 'audit.md').write_text(md)
    projected = []
    for path in sorted(OUT.rglob('*')):
        if path.is_file() and path.name != 'projection-hashes.json':
            raw = path.read_bytes()
            projected.append(dict(path=str(path.relative_to(OUT)), bytes=len(raw), sha256=sha(raw)))
    save('projection-hashes.json', projected)
    print(json.dumps(dict(output=str(OUT), blocks=[{k:b[k] for k in ['block_id','strict_frozen_proof_pass','successful_complete_entries','failed_read_calls','byte_for_byte_report_reproduced']} for b in blocks]), indent=2))


if __name__ == '__main__':
    main()
