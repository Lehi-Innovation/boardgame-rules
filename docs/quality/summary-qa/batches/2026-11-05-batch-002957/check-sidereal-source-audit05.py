"""Independently rebind audit05 to actual source reads, image calls and settings."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
import re
import subprocess

B = Path(__file__).resolve().parent
REPO = B.parents[4]
R = REPO / 'docs/quality/summary-qa/sidereal-confluence' / B.name
D = R / 'source-audit-05'
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_text())
audit_path = D / 'source-audit.json'
audit, manifest = load(audit_path), load(D / 'source-manifest.json')
assert audit['verdict'] == 'PASS' and not audit['findings'] and not audit['important_missing_core_procedural_content']
summary = Path(audit['summary_snapshot_path'])
assert H(summary) == audit['summary_snapshot_sha256']
assert summary.read_bytes() == (REPO / 'rules/sidereal-confluence.md').read_bytes()
assert H(Path(audit['source_manifest_path'])) == audit['source_manifest_sha256']
for entry in manifest['sources']:
    p = Path(entry['path'])
    assert H(p) == entry['sha256'] and p.stat().st_size == entry['bytes']
parent_text = load(D / 'runtime-text-delivery.json')
parent_native = load(D / 'runtime-native-delivery.json')
runtime = Path(parent_text['runtime_source_path'])
raw = runtime.read_bytes().splitlines(keepends=True)
rows = {n: json.loads(line) for n, line in enumerate(raw, 1)}


def strings(value, depth=0):
    if depth > 10:
        return
    if isinstance(value, str):
        yield value
        try:
            decoded = json.loads(value)
        except ValueError:
            return
        if decoded != value:
            yield from strings(decoded, depth + 1)
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item, depth + 1)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item, depth + 1)


def literal_view_paths(text):
    """Resolve literal path lists and the observed bounded PDF-number templates."""
    string = r'"(?:\\.|[^"\\])*"'
    constants = {m[1]: json.loads(m[2]) for m in
                 re.finditer(r'const\s+(\w+)\s*=\s*(' + string + r')\s*;', text)}
    paths = set()
    for m in re.finditer(r'view_image\(\{path:\s*(' + string + r')\s*[,}]', text):
        paths.add(json.loads(m[1]))
    for m in re.finditer(r'view_image\(\{path:\s*(\w+)\s*\+\s*(' + string + r')\s*[,}]', text):
        paths.add(constants[m[1]] + json.loads(m[2]))
    for loop in re.finditer(r'for\(const (\w+) of (\[[^\]]*\])\)\{(.*?)\n?\}', text, re.S):
        name, values, body = loop[1], json.loads(loop[2]), loop[3]
        assert isinstance(values, list) and all(isinstance(v, str) for v in values)
        pattern = r'path:\s*(' + string + r'|\w+)\s*\+\s*' + re.escape(name) + r'(?:\s*\+\s*(' + string + r'))?'
        for m in re.finditer(pattern, body):
            prefix = json.loads(m[1]) if m[1].startswith('"') else constants[m[1]]
            suffix = json.loads(m[2]) if m[2] else ''
            paths.update(prefix + v + suffix for v in values)
    for loop in re.finditer(r'for\(const (\w+) of (\[[^\]]*\])\)', text):
        name, values = loop[1], json.loads(loop[2])
        assert isinstance(values, list) and all(isinstance(v, str) for v in values)
        for match in re.finditer(r'path:\s*(\w+)\s*\+\s*' + re.escape(name) + r'\s*[,}]', text):
            paths.update(constants[match[1]] + value for value in values)
    for loop in re.finditer(r'for\(let (\w+)=(\d+);\1<=(\d+);\1\+\+\)', text):
        name, first, last = loop[1], int(loop[2]), int(loop[3])
        assert 1 <= first <= last <= 10
        for match in re.finditer(r'path:\s*`([^`]+)`', text):
            template = match[1]
            for number in range(first, last + 1):
                value = template.replace('${' + name + '}', str(number))
                value = value.replace('${String(' + name + ").padStart(2,'0')}", f'{number:02d}')
                assert '${' not in value
                paths.add(value)
    return paths


outputs, calls, contexts, cutoffs = [], [], [], []
for n, row in rows.items():
    p = row.get('payload', {})
    if row.get('type') == 'session_meta':
        assert p['id'] == '01a1b275-4822-7e33-88f6-cd4ac317b5f0'
        assert p['parent_thread_id'] == '01a1b0b3-0030-70b2-8947-7a940fdf364f'
        assert p['agent_path'] == '/root/pure_source_auditor_05'
    if row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ('custom_tool_call', 'function_call'):
        text = p.get('input', p.get('arguments', ''))
        assert isinstance(text, str)
        assert not any(s in text for s in ('questions.json', 'answer-key.json', 'asked-facts.json', 'coverage-map',
            'reader-a.json', 'reader-b.json', 'results.json', 'source-audit-02/', 'source-audit-03/', 'source-audit-04/'))
        calls.append({'record': n, 'call_id': p['call_id'], 'input_sha256': HB(text.encode())})
        if 'source-audit.json' in text and any(s in text for s in ('write_text', 'writeFile', 'apply_patch')):
            cutoffs.append(n)
    elif p.get('type') in ('custom_tool_call_output', 'function_call_output'):
        outputs.append((n, list(strings(p.get('output')))))
assert cutoffs and contexts and all(c['model'] == 'gpt-6.1-sol' and c['effort'] == 'high' for c in contexts)
boundary = min(cutoffs)
assert boundary == parent_native['all_native_views_before_first_report_write_ordinal']
text_checks = []
for receipt in audit['text_read_receipts']:
    p = Path(receipt['path']); text = p.read_text()
    assert H(p) == receipt['sha256'] and len(text) == receipt['character_count']
    cursor, parts = 0, []
    for a, z in receipt['ranges']:
        assert a == cursor and a < z <= len(text)
        found = [n for n, values in outputs if n < boundary and any(text[a:z] in v for v in values)]
        assert found, (str(p), a, z)
        parts.append({'start': a, 'end': z, 'actual_output_records': found, 'slice_sha256': HB(text[a:z].encode())})
        cursor = z
    assert cursor == len(text)
    text_checks.append({'path': str(p), 'sha256': receipt['sha256'], 'complete': True, 'parts': parts})
native_checks, grouped = [], Counter()
for binding in parent_native['bindings']:
    path = Path(binding['path']); x = binding['native_output_binding']
    assert H(path) == binding['sha256']
    assert HB(raw[x['ordinal'] - 1]) == x['record_sha256']
    assert HB(raw[x['call_ordinal'] - 1]) == x['call_record_sha256']
    out, call = rows[x['ordinal']]['payload'], rows[x['call_ordinal']]['payload']
    assert out['call_id'] == call['call_id'] == x['call_id']
    assert x['call_ordinal'] < x['ordinal'] < boundary
    text = call.get('input', call.get('arguments', ''))
    assert 'view_image' in text and str(path) in literal_view_paths(text), (str(path), x['call_ordinal'])
    count = sum(isinstance(v, dict) and v.get('type') == 'input_image' for v in out['output'])
    assert count == x['native_image_count']
    grouped[x['ordinal']] += 1
    native_checks.append({'path': str(path), 'sha256': binding['sha256'], 'call_record': x['call_ordinal'],
                          'output_record': x['ordinal'], 'native_count': count})
for n, count in grouped.items():
    assert count == sum(isinstance(v, dict) and v.get('type') == 'input_image' for v in rows[n]['payload']['output'])
assert len(native_checks) == len(audit['native_view_receipts']) == 41
paths = subprocess.run(['rg', '--files', '/mnt/c/Users/jonny/.codex/sessions'], capture_output=True, text=True, check=True).stdout.splitlines()
parent = next(Path(p) for p in paths if p.endswith('01a1b0b3-0030-70b2-8947-7a940fdf364f.jsonl'))
spawns = []
for n, line in enumerate(parent.open(), 1):
    row = json.loads(line); p = row.get('payload', {})
    if row.get('type') == 'response_item' and p.get('type') == 'function_call' and p.get('name', '').endswith('spawn_agent'):
        a = p.get('arguments'); a = json.loads(a) if isinstance(a, str) else a
        if a.get('task_name') == 'pure_source_auditor_05':
            spawns.append({'record': n, **{k: a.get(k) for k in ('task_name', 'model', 'reasoning_effort', 'fork_turns')}})
assert len(spawns) == 1 and spawns[0]['model'] == 'gpt-6.1-sol' and spawns[0]['reasoning_effort'] == 'high' and spawns[0]['fork_turns'] == 'none'
prior = B / 'coordinator-checks/sidereal-source-audit-02-actual-delivery-v2.json'
lineage = load(prior)
for x in lineage['native_crop_lineage']:
    assert x['exact_native_parent_pixels']
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'audit_path': str(audit_path), 'audit_sha256': H(audit_path), 'summary_sha256': H(summary),
    'auditor_id': '01a1b275-4822-7e33-88f6-cd4ac317b5f0', 'actual_contexts': contexts,
    'actual_initial_spawn': spawns[0], 'runtime_path': str(runtime), 'runtime_sha256_at_check': H(runtime),
    'first_report_write_record': boundary, 'text_checks': text_checks, 'native_checks': native_checks,
    'unchanged_crop_pixel_lineage_reference': {'path': str(prior), 'sha256': H(prior), 'checks': 15},
    'source_hashes': manifest['sources'], 'tool_call_hash_projection': calls,
    'limits': 'Actual complete text and individually named native-image delivery before report verified. Semantic source signoff remains the independent auditor verdict. No question/key/reader/publication signoff.'}
out = B / 'coordinator-checks/sidereal-source-audit-05-actual-delivery.json'
assert not out.exists()
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'text_files': len(text_checks), 'text_slices': sum(len(x['parts']) for x in text_checks),
                  'native_images': len(native_checks), 'report': str(out)}))
