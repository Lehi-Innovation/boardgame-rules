"""Verify original review12 delivery, without changing its two scope findings."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import re
import subprocess

B = Path(__file__).resolve().parent
REPO = B.parents[4]
R = REPO / 'docs/quality/summary-qa/spirit-island' / B.name
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_text())
L = load(R / 'scope-coverage-12-read-ledger.json')
C = load(R / 'coverage-review-12.json')
assert C['coverage_verdict'] == 'PASS' and C['remaining_gap_count'] == 0
assert C['verdict'] == 'FAIL' and C['unresolved_stopping_findings'] == ['MAP12-01', 'MAP12-02']
ident = '01a1b2a4-9845-77f3-b04e-1dad7cb8d501'
parent = '01a1ac01-c763-7bb1-901e-7458891630b8'
paths = subprocess.run(['rg', '--files', '/mnt/c/Users/jonny/.codex/sessions'], check=True, capture_output=True, text=True).stdout.splitlines()
runtime = next(Path(p) for p in paths if p.endswith(ident + '.jsonl'))
# Reuse only this audited data walker definition, never execute another helper's
# top-level statements or any tool command read from a runtime record.
tree = ast.parse((B / 'check-spirit-source09-delivery.py').read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'strings')
ns = {'json': json}
exec(compile(ast.Module(body=[fn], type_ignores=[]), '<literal-string-walker>', 'exec'), ns)
strings = ns['strings']
raw = runtime.read_bytes().splitlines(keepends=True)
rows = {i: json.loads(v) for i, v in enumerate(raw, 1)}
calls, outputs, contexts, writes = {}, [], [], []
for n, row in rows.items():
    p = row.get('payload', {})
    if row.get('type') == 'session_meta':
        assert p['id'] == ident and p['parent_thread_id'] == parent and p['agent_path'] == '/root/scope_and_coverage_12'
    if row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ('custom_tool_call', 'function_call'):
        t = p.get('input', p.get('arguments', ''))
        assert isinstance(t, str)
        assert not any(x in t for x in ('rules/spirit-island.md', 'source-candidate-',
            'reader-a.json', 'reader-b.json', 'source-audit-final-', 'list_agents', 'read_thread', 'wait_threads'))
        calls[p['call_id']] = (n, p, t)
        if (('coverage-review-12.json' in t or 'cat > /tmp/scope12-write-reports.py' in t)
                and any(x in t for x in ('write_text', 'writeFile', 'apply_patch'))):
            writes.append(n)
    elif p.get('type') in ('custom_tool_call_output', 'function_call_output'):
        outputs.append((n, p, list(strings(p.get('output')))))
assert contexts and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in contexts)
assert writes
boundary = min(writes)
text_checks = []
for path, v in L['text_inputs'].items():
    p = Path(path); t = p.read_text(); cursor = 0; slices = []
    assert H(p) == v['full_byte_sha256'] and len(t) == v['character_length']
    for c in v['slices']:
        a, z = c['start'], c['end']
        assert a == cursor and a < z <= len(t) and HB(t[a:z].encode()) == c['utf8_sha256']
        matches = [n for n, _, vals in outputs if n < boundary and any(t[a:z] in x or json.dumps(t[a:z], ensure_ascii=False)[1:-1] in x for x in vals)]
        assert matches, (path, a, z)
        slices.append({'start': a, 'end': z, 'slice_sha256': c['utf8_sha256'], 'actual_output_records': matches})
        cursor = z
    assert cursor == len(t)
    text_checks.append({'path': path, 'sha256': H(p), 'complete': True, 'slices': slices})
manifest_path = R / 'supplemental-source-manifest-v4.json'
card_paths = [x['path'] for x in load(manifest_path)['source_records'] if x.get('role') == 'primary printed card face']
assert len(card_paths) == 33
assert load(Path('/tmp/scope12-card-paths.json')) == card_paths
card_writer = [(n, t) for n, _, t in calls.values() if "Path('/tmp/scope12-card-paths.json').write_text(json.dumps(r))" in t
    and "r=[x['path'] for x in d['source_records'] if x.get('role')=='primary printed card face']" in t]
assert len(card_writer) == 1 and card_writer[0][0] < boundary
assert "r=[x['path'] for x in d['source_records'] if x.get('role')=='primary printed card face']" in card_writer[0][1]
assert 'supplemental-source-manifest-v4.json' in card_writer[0][1]
native_checks = []
for n, p, vals in outputs:
    out = p.get('output')
    if not isinstance(out, list):
        continue
    count = sum(isinstance(x, dict) and x.get('type') == 'input_image' for x in out)
    if not count:
        continue
    cn, call, t = calls[p['call_id']]
    assert cn < n < boundary and 'view_image' in t
    named = re.findall(r'path:\s*"([^"\n]+)"', t)
    if not named:
        r = re.search(r'for\(let i=(\d+);i<(\d+);i\+\+\)', t)
        assert r and ('load("scope12Cards")[i]' in t or 'path:paths[i]' in t)
        named = card_paths[int(r[1]):int(r[2])]
    assert len(named) == count
    for path in named:
        native_checks.append({'path': path, 'sha256': H(Path(path)), 'call_record': cn,
            'output_record': n, 'call_record_sha256': HB(raw[cn-1]), 'output_record_sha256': HB(raw[n-1])})
assert len(native_checks) == 54
assert {x['path']: x['sha256'] for x in native_checks} == {x['path']: x['sha256'] for x in L['images']}
parent_runtime = next(Path(p) for p in paths if p.endswith(parent + '.jsonl'))
spawns = []
for n, line in enumerate(parent_runtime.open(), 1):
    row = json.loads(line); p = row.get('payload', {})
    if row.get('type') == 'response_item' and p.get('type') == 'function_call' and p.get('name', '').endswith('spawn_agent'):
        a = p.get('arguments'); a = json.loads(a) if isinstance(a, str) else a
        if a.get('task_name') == 'scope_and_coverage_12':
            spawns.append({'record': n, **{k: a.get(k) for k in ('task_name', 'model', 'reasoning_effort', 'fork_turns')},
                'message_sha256': HB(a.get('message', '').encode()),
                'message_storage': 'encrypted opaque body' if a.get('message', '').startswith('gAAAAA') else 'plaintext'})
assert len(spawns) == 1 and spawns[0]['model'] == 'gpt-6.1-sol' and spawns[0]['reasoning_effort'] == 'high' and spawns[0]['fork_turns'] == 'none'
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'reviewer_id': ident, 'actual_initial_spawn': spawns[0], 'actual_contexts': contexts,
    'runtime_path': str(runtime), 'runtime_sha256_at_check': H(runtime),
    'coverage_report_path': str(R / 'coverage-review-12.json'), 'coverage_report_sha256': H(R / 'coverage-review-12.json'),
    'conservative_report_creation_boundary_record': boundary, 'text_checks': text_checks, 'native_checks': native_checks,
    'card_path_derivation': {'source': str(manifest_path), 'sha256': H(manifest_path), 'actual_writer_record': card_writer[0][0]},
    'original_semantic_outcome_preserved': {'coverage': C['coverage_verdict'], 'stopping': C['stopping_verdict'], 'remaining_gaps': 0, 'open_scope_findings': C['unresolved_stopping_findings']},
    'boundary_note': 'All inputs precede even the creation of the report-writer helper. The earlier literal-filename-only projection at record1573 is retained as a draft, not used as the earliest report boundary.',
    'limits': 'Actual complete input delivery and explicit initially fresh source-only reviewer settings verified. Original report remains FAIL pending two grading-map findings; this is not final coverage approval. Opaque original dispatch text is not claimed to equal a reconstructed plaintext prompt.'}
target = B / 'coordinator-checks/spirit-coverage-review12-actual-delivery-v2.json'
assert not target.exists()
target.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'text_inputs': len(text_checks), 'slices': sum(len(x['slices']) for x in text_checks),
    'native_images': len(native_checks), 'conservative_report_creation_boundary_record': boundary, 'report': str(target)}))
