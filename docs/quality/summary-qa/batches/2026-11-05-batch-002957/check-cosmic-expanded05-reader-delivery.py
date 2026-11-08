"""Bind final whole inputs and immutable prefixes without rewriting initial timing."""
import ast
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

B = Path(__file__).resolve().parent
R = B.parents[4]
D = R / 'docs/quality/summary-qa/cosmic-encounter' / B.name / 'expanded-iteration-05'
J = lambda p: json.loads(p.read_text())
HB = lambda v: hashlib.sha256(v).hexdigest()
H = lambda p: HB(p.read_bytes())
tree = ast.parse((B/'check-spirit-source09-delivery.py').read_text())
fn = next(x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == 'strings')
ns = {'json': json}
exec(compile(ast.Module(body=[fn], type_ignores=[]), '<strings>', 'exec'), ns)
ids = [x['id'] for x in J(D/'questions.json')['questions']]
assert len(ids) == 168 and len(set(ids)) == 168
actors = {'a': '01a1b631-46ad-77b2-81e8-2e7e1beeea8d',
          'b': '01a1b631-9145-74f1-9f2e-e08898cd27c1'}
initial = J(D/'initial-transport-technical-audit-23.json')
checks = []
for who, actor in actors.items():
    rawpath = D/f'reader-{who}.json'
    raw = J(rawpath)
    assert [x['id'] for x in raw['answers']] == ids
    prefixes = []
    for i in range(1, 18):
        path = D/f'reader-{who}-batch-{i:02}.json'
        old = J(path)
        n = min(i*10, 168)
        assert old['answers'] == raw['answers'][:n]
        prefixes.append({'path': str(path), 'sha256': H(path), 'answers': n})
    runtime = next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/07').glob('*'+actor+'.jsonl'))
    lines = runtime.read_bytes().splitlines(keepends=True)
    received, writes, contexts, terminals, calls = [], [], [], [], []
    for n, line in enumerate(lines, 1):
        row = json.loads(line)
        p = row.get('payload', {})
        if row.get('type') == 'session_meta':
            assert p['id'] == actor and p['parent_thread_id'] == '01a1b3c7-0daa-70f1-9158-0e75d24cbb22'
        if row.get('type') == 'turn_context':
            contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
        if row.get('type') == 'event_msg' and p.get('type') == 'task_complete':
            terminals.append(n)
        if row.get('type') == 'response_item':
            if p.get('type') in ['function_call_output', 'custom_tool_call_output']:
                received.append((n, list(ns['strings'](p.get('output')))))
            if p.get('type') in ['function_call', 'custom_tool_call']:
                code = p.get('input', p.get('arguments', ''))
                assert not any(x in code for x in ['answer-key.json', 'grading-key.json',
                    'scope-map.json', 'asked-facts.json', 'source_pdfs/', 'extracted/',
                    'read_thread', 'wait_threads', 'web__run', 'list_agents',
                    f'reader-{"b" if who == "a" else "a"}.json'])
                calls.append({'record': n, 'name': p.get('name'), 'record_sha256': HB(line)})
                if rawpath.name in code and any(x in code for x in ['write_text', 'write_bytes', 'writeFile', 'apply_patch']):
                    writes.append(n)
        if row.get('type') == 'event_msg' and p.get('type') == 'item_completed':
            item = p.get('item', {})
            if item.get('type') == 'CommandExecution':
                received.append((n, list(ns['strings'](item.get('aggregated_output', '')))))
    assert writes and terminals and max(terminals) > max(writes)
    assert contexts and all(x['model'] == 'gpt-6-luna' and x['effort'] == 'high' for x in contexts)
    first, last = min(writes), max(writes)
    files = []
    for receipt in raw['inputs_read']:
        path = Path(receipt['path'])
        assert path in [D/'summary-snapshot.md', D/'reader-questions-final.json']
        text = path.read_text()
        data = path.read_bytes()
        assert receipt['sha256'] == H(path) and receipt['characters'] == len(text) and receipt['bytes'] == len(data)
        char_mode = all(HB(text[c['start']:c['end']].encode()) == c['sha256'] for c in receipt['chunks'])
        byte_mode = all(HB(data[c['start']:c['end']]) == c['sha256'] for c in receipt['chunks'])
        assert char_mode or byte_mode
        cursor, parts = 0, []
        for span in receipt['chunks']:
            a, z = span['start'], span['end']
            assert a == cursor and a < z
            part = text[a:z] if char_mode else data[a:z].decode('utf-8')
            matched = [{'record': n, 'record_sha256': HB(lines[n-1])}
                for n, values in received if n < last and any(part in value.replace('\r\n','\n') for value in values)]
            assert matched, (who, path.name, a, z)
            parts.append({'start': a, 'end': z, 'sha256': HB(part.encode()),
                'actual_outputs_before_final_writer': matched,
                'also_received_before_first_writer': any(x['record'] < first for x in matched)})
            cursor = z
        assert cursor == (len(text) if char_mode else len(data))
        files.append({'path': str(path), 'sha256': H(path), 'offset_unit': 'unicode_characters' if char_mode else 'utf8_bytes',
            'all_literal_input_received_before_final_writer': True, 'parts': parts})
    assert len(files) == 2
    original = next(x for x in initial['reader_results'] if x['reader'] == who)
    initial_findings = [{'path': f['path'],
        'actual_initial_visible_char_ranges': f['measured_raw_source_visible_ranges_including_oversized_survivors'],
        'actual_initial_missing_char_ranges': f['missing_raw_source_char_ranges_after_measured_survivors']}
        for f in original['files']]
    checks.append({'reader': who, 'actor': actor, 'runtime': str(runtime), 'runtime_sha256': H(runtime),
        'raw_sha256': H(rawpath), 'contexts': contexts, 'first_writer_record': first, 'final_writer_record': last,
        'last_completed_turn_record': max(terminals), 'actual_input_files': files, 'unchanged_original_prefixes': prefixes,
        'initial_transport_verdict': original['technical_transport_verdict'], 'initial_transport_finding': initial_findings,
        'public_call_trace': calls})
assert H(D/'summary-snapshot.md') == H(R/'rules/cosmic-encounter.md')
proof = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'N': 168, 'complete_original_answers': 336, 'immutable_fixed_batch_prefixes': 34,
    'readers': checks, 'initial_audit23_path': str(D/'initial-transport-technical-audit-23.json'),
    'initial_audit23_sha256': H(D/'initial-transport-technical-audit-23.json'),
    'chronology_qualification': 'A saved the first10 before complete rule-data delivery. Its later complete reread is bound before the final writer, never relabeled pre-first-save. B complete initial bounded input is retained with byte-coordinate metadata normalization. All first10 and later prefix answer values remain exact.',
    'limits': ['This proves actual whole final inputs, model contexts, and immutable originals. Initial A protocol deviation remains explicit.',
        'No factual grading cap, factual feedback, discarded completed output, or score resampling is inferred from the transport defect.',
        'Fresh spawn requests, generic method review, original full-output freeze, factual grades, source audit and external authority gates are separate.']}
out = B/'coordinator-checks/cosmic-expanded05-complete-reader-actual-delivery.json'
assert not out.exists()
out.write_text(json.dumps(proof, indent=2)+'\n')
print(json.dumps({'verified': True, 'N': 168, 'prefixes': 34,
    'actual_input_ranges': sum(len(f['parts']) for x in checks for f in x['actual_input_files']), 'proof': str(out)}))
