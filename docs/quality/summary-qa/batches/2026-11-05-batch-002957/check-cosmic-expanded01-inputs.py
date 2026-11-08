"""Independent original-runtime delivery check; no factual grading or approval."""
import ast
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
D = ROOT / 'docs/quality/summary-qa/cosmic-encounter' / B.name / 'expanded-iteration-01'
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_text())
manifest = load(D / 'input-manifest.json')
for name, digest in manifest['sha256'].items():
    assert H(Path(name)) == digest, name
assert manifest['question_count'] == 167
assert manifest['completion_readiness'] is False and manifest['final_scope_freeze'] is False
questions = load(D / 'questions.json')['questions']
ids = [q['id'] for q in questions]
assert len(ids) == 167 and len(set(ids)) == 167
tree = ast.parse((B / 'check-spirit-source09-delivery.py').read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'strings')
ns = {'json': json}
exec(compile(ast.Module(body=[fn], type_ignores=[]), '<public-tool-output-strings>', 'exec'), ns)
strings = ns['strings']
records = []
for who, ident in [('a', '01a1b4c2-c9a5-79b2-a02f-1261ccde54c6'),
                   ('b', '01a1b4c3-2539-7ae2-b640-1d9660b1fa58')]:
    runtime = next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/06').glob('*' + ident + '.jsonl'))
    raw = D / ('reader-' + who + '.json')
    answer = load(raw)
    assert [a['id'] for a in answer['answers']] == ids
    lines = runtime.read_bytes().splitlines(keepends=True)
    contexts, outputs, calls, writes = [], [], [], []
    for n, line in enumerate(lines, 1):
        row = json.loads(line)
        p = row.get('payload', {})
        if row.get('type') == 'session_meta':
            assert p['id'] == ident and p['parent_thread_id'] == '01a1b3c7-0daa-70f1-9158-0e75d24cbb22'
        if row.get('type') == 'turn_context':
            contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
        if row.get('type') != 'response_item':
            continue
        if p.get('type') in ['function_call', 'custom_tool_call']:
            text = p.get('input', p.get('arguments', ''))
            assert isinstance(text, str)
            assert not any(bad in text for bad in ['answer-key.json', 'actual-question-scope.json',
                'source-only-audit', 'source_pdfs/', 'coverage-review', 'list_agents',
                'get_agent_info', 'read_thread', 'wait_threads', 'web__', 'search_query',
                'reader-' + ('b' if who == 'a' else 'a') + '.json'])
            calls.append({'record': n, 'name': p.get('name'), 'input_sha256': HB(text.encode()),
                          'original_record_sha256': HB(line)})
            if raw.name in text and any(v in text for v in ['write_text', 'writeFile', 'apply_patch']):
                writes.append(n)
        elif p.get('type') in ['function_call_output', 'custom_tool_call_output']:
            outputs.append((n, list(strings(p.get('output')))))
    assert contexts and all(c['model'] == 'gpt-6-luna' and c['effort'] == 'high' for c in contexts)
    assert writes
    boundary = min(writes)
    checks = []
    for receipt in answer['inputs_read']:
        path = Path(receipt['path'])
        assert path.parent == D and path.name in ['summary-snapshot.md', 'questions.json']
        text = path.read_text()
        assert receipt['sha256'] == H(path)
        assert receipt['bytes'] == len(path.read_bytes()) and receipt['characters'] == len(text)
        cursor, parts = 0, []
        for chunk in receipt['chunks']:
            a, z = chunk['start'], chunk['end']
            assert a == cursor and a < z <= len(text)
            digest = HB(text[a:z].encode())
            assert chunk['sha256'] == digest
            matches = [n for n, vals in outputs if n < boundary and any(
                text[a:z] in v or json.dumps(text[a:z], ensure_ascii=False)[1:-1] in v for v in vals)]
            assert matches, (who, path.name, a, z)
            parts.append({'start': a, 'end': z, 'sha256': digest,
                          'original_output_records': [{'record': n, 'sha256': HB(lines[n-1])} for n in matches]})
            cursor = z
        assert cursor == len(text)
        checks.append({'path': str(path), 'sha256': H(path), 'complete_before_first_write': True,
                       'characters': len(text), 'declared_parts_rebound_to_actual_original_outputs': parts})
    assert {Path(c['path']).name for c in checks} == {'summary-snapshot.md', 'questions.json'}
    records.append({'reader': who, 'identity': ident, 'raw_output_sha256': H(raw),
                    'runtime': str(runtime), 'runtime_sha256_at_check': H(runtime), 'contexts': contexts,
                    'first_saved_answer_writer_record': boundary, 'input_checks': checks,
                    'public_tool_call_trace': calls})
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'question_count': 167, 'input_manifest_sha256': H(D / 'input-manifest.json'),
          'summary_sha256': H(D / 'summary-snapshot.md'), 'readers': records,
          'canonical_body_matches_at_check': (D / 'summary-snapshot.md').read_bytes() == (ROOT / 'rules/cosmic-encounter.md').read_bytes(),
          'transport_diagnostic_path': str(D / 'actual-transport-slice-validation-02.json'),
          'transport_diagnostic_sha256': H(D / 'actual-transport-slice-validation-02.json'),
          'limits': 'Checks complete actual frozen input delivery before the first saved-answer write, raw IDs and forbidden source-access markers. This is not factual grading, an authoring-time claim based only on saved files, final scope readiness, or publication approval. A separate original-spawn check verifies explicit freshness. A complete oversized original question block is retained as a transport deviation without a factual cap. Task ciphertext is not claimed to equal plaintext.'}
out = B / 'coordinator-checks/cosmic-expanded01-original-reader-inputs.json'
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'readers': len(records), 'N': 167, 'report': str(out)}))
