"""Rebind Lords source audit 01 to original text/image delivery records."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

B = Path(__file__).resolve().parent
REPO = B.parents[4]
R = REPO / 'docs/quality/summary-qa/lords-of-vegas' / B.name
AP = R / 'expanded-iteration-01/source-audit.json'
AUDITOR = '01a1b2d1-3ea7-72d2-ac1d-6c1a825a80c3'
PARENT = '01a1b2c1-d5d1-7333-8948-72708b3d1f3e'
runtime = Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/06/rollout-2026-11-06T14-43-40-' + AUDITOR + '.jsonl')
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
d = json.loads(AP.read_text())
assert d['verdict'] == 'PASS' and not d['findings']
assert not d['omissions']['material_explicit_base_rules_missing']
raw = runtime.read_bytes().splitlines(keepends=True)
rows = {i: json.loads(v) for i, v in enumerate(raw, 1)}


def strings(v):
    if isinstance(v, str):
        yield v
        try:
            w = json.loads(v)
        except ValueError:
            return
        if w != v:
            yield from strings(w)
    elif isinstance(v, dict):
        if v.get('type') in ('input_image', 'image'):
            return
        for x in v.values():
            yield from strings(x)
    elif isinstance(v, list):
        for x in v:
            yield from strings(x)


calls, outputs, contexts, writes, communications = {}, [], [], [], []
for n, row in rows.items():
    p = row.get('payload', {})
    if row.get('type') == 'session_meta':
        assert p['id'] == AUDITOR and p['parent_thread_id'] == PARENT
        assert p['agent_path'] == '/root/source_audit_final'
    if row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ('function_call', 'custom_tool_call'):
        t = p.get('input', p.get('arguments', ''))
        assert isinstance(t, str)
        calls[p['call_id']] = (n, p, t)
        # Generic independence declarations in the report writer are permitted;
        # no actual question/key/answer/status file or peer read is permitted.
        assert not any(x in t for x in ('questions.json', 'answer-key.json', 'grading-key.json',
            'scope-map.json', 'reader-a.json', 'reader-b.json', 'list_agents', 'read_thread',
            'wait_threads', 'coverage-review', 'results.json'))
        if p.get('type') == 'function_call':
            a = json.loads(t)
            assert p.get('name', '').endswith('send_message') and a.get('target') == '/root'
            communications.append({'record': n, 'name': p['name'], 'target': a['target'],
                'argument_sha256': HB(t.encode()), 'kind': 'auditor reporting its own findings to parent'})
        if 'source-audit.json' in t and any(x in t for x in ('write_text', 'writeFile', 'apply_patch')):
            writes.append(n)
    elif p.get('type') in ('function_call_output', 'custom_tool_call_output'):
        outputs.append((n, p, list(strings(p.get('output')))))
assert contexts and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in contexts)
assert writes
cutoff = min(writes)
checks = []
for f in d['input_hashes']:
    p = Path(f['path'])
    assert p.stat().st_size == f['bytes'] and H(p) == f['sha256']
summary = Path(d['delivery_receipt']['complete_text_delivery'][0]['path'])
assert summary.read_bytes() == (REPO / 'rules/lords-of-vegas.md').read_bytes()
for f in d['delivery_receipt']['complete_text_delivery']:
    p = Path(f['path']); t = p.read_text(); cursor = 0; parts = []
    assert len(t) == f['total_characters']
    for c in f['chunks']:
        a, z = c['start'], c['end']
        assert a == cursor and a < z <= len(t) and HB(t[a:z].encode()) == c['sha256']
        matches = [n for n, _, values in outputs if n < cutoff and any(t[a:z] in v for v in values)]
        assert matches, (str(p), a, z)
        parts.append({'start': a, 'end': z, 'slice_sha256': c['sha256'], 'actual_output_records': matches})
        cursor = z
    assert cursor == len(t)
    checks.append({'path': str(p), 'sha256': H(p), 'complete': True, 'parts': parts})
u = B / 'source-preflight/lords-of-vegas/unified-2022'
for p in [u / 'provenance.json', u / 'publisher-downloads-visible.txt']:
    t = p.read_text()
    matches = [n for n, _, values in outputs if n < cutoff and any(t in v for v in values)]
    assert matches, str(p)
    checks.append({'path': str(p), 'sha256': H(p), 'complete': True,
        'parts': [{'start': 0, 'end': len(t), 'slice_sha256': HB(t.encode()), 'actual_output_records': matches}]})
native = []
for n, p, values in outputs:
    out = p.get('output')
    if not isinstance(out, list):
        continue
    count = sum(isinstance(v, dict) and v.get('type') == 'input_image' for v in out)
    if not count:
        continue
    cn, call, t = calls[p['call_id']]
    assert cn < n < cutoff and 'view_image' in t
    base = re.search(r'const base=("(?:\\.|[^"\\])*");', t)
    names = re.search(r'for\(const p of (\[[^\]]*\])\)', t)
    assert base and names
    paths = [Path(json.loads(base[1])) / x for x in json.loads(names[1])]
    assert len(paths) == count
    for path in paths:
        native.append({'path': str(path), 'sha256': H(path), 'call_record': cn,
            'output_record': n, 'call_record_sha256': HB(raw[cn-1]), 'output_record_sha256': HB(raw[n-1])})
assert {x['path'] for x in native} == {x['path'] for x in d['delivery_receipt']['native_page_inspection']}
assert len(native) == 7
for c in d['checked_claims']:
    assert c['status'] == 'supported' and c['exact_summary_claim'] in summary.read_text()
parent_runtime = runtime.parent / ('rollout-2026-11-06T14-26-50-' + PARENT + '.jsonl')
spawns = []
for n, line in enumerate(parent_runtime.open(), 1):
    row = json.loads(line); p = row.get('payload', {})
    if row.get('type') == 'response_item' and p.get('type') == 'function_call' and p.get('name', '').endswith('spawn_agent'):
        a = p.get('arguments'); a = json.loads(a) if isinstance(a, str) else a
        if a.get('task_name') == 'source_audit_final':
            spawns.append({'record': n, **{k: a.get(k) for k in ('task_name', 'model', 'reasoning_effort', 'fork_turns')},
                'message_storage': 'encrypted opaque body' if a.get('message', '').startswith('gAAAAA') else 'plaintext',
                'message_sha256': HB(a.get('message', '').encode())})
assert len(spawns) == 1
assert spawns[0]['model'] == 'gpt-6.1-sol' and spawns[0]['reasoning_effort'] == 'high' and spawns[0]['fork_turns'] == 'none'
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'audit_path': str(AP), 'audit_sha256': H(AP), 'summary_sha256': H(summary),
    'auditor_id': AUDITOR, 'runtime_path': str(runtime), 'runtime_sha256_at_check': H(runtime),
    'actual_initial_spawn': spawns[0], 'actual_contexts': contexts, 'first_report_write_record': cutoff,
    'text_checks': checks, 'native_checks': native, 'source_hashes': d['input_hashes'],
    'communications': communications,
    'method_qualification': 'Original dispatch body is opaque encrypted runtime data. Its hash and explicit fresh-context model settings are verified; no claim of recovered plaintext equality. Actual original tool/output trace contains only assigned source/summary/provenance reads and own-findings communication to parent.',
    'limits': 'Current source-audit delivery and source-only independence verified. Does not accept any question bank, reader grades, coverage stopping claim, stamp or publication.'}
out = B / 'coordinator-checks/lords-source-audit-01-actual-delivery.json'
assert not out.exists()
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'complete_text_files': len(checks), 'actual_slices': sum(len(x['parts']) for x in checks),
    'native_images': len(native), 'summary_sha256': H(summary), 'report': str(out)}))
