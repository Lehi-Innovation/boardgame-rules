"""Verify the clean final38 source/key challenge and frozen bank preservation."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import re

B = Path(__file__).resolve().parent
REPO = B.parents[4]
R = REPO / 'docs/quality/summary-qa/lords-of-vegas' / B.name
AP = R / 'clean-final-coverage-review.json'
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
d = load(AP)
assert d['verdict'] == 'PASS' and not d['findings'] and not d['required_changes']
assert d['stopping_rule_assessment']['satisfactory'] and not d['accepted_new_candidates']
runtime = Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/06/rollout-2026-11-06T15-30-07-01a1b2fb-c7dd-71f2-8f0c-ee87c40778a0.jsonl')
tree = ast.parse((B / 'check-spirit-source09-delivery.py').read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'strings')
ns = {'json': json}
exec(compile(ast.Module(body=[fn], type_ignores=[]), '<literal-string-walker>', 'exec'), ns)
strings = ns['strings']
raw = runtime.read_bytes().splitlines(keepends=True)
rows = {i: json.loads(v) for i, v in enumerate(raw, 1)}
calls, outputs, contexts, boundaries = {}, [], [], []
for n, row in rows.items():
    p = row.get('payload', {})
    if row.get('type') == 'session_meta':
        assert p['id'] == '01a1b2fb-c7dd-71f2-8f0c-ee87c40778a0' and p['parent_thread_id'] == '01a1b2c1-d5d1-7333-8948-72708b3d1f3e'
        assert p['agent_path'] == '/root/clean_final_coverage'
    if row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ('function_call', 'custom_tool_call'):
        t = p.get('input', p.get('arguments', ''))
        assert isinstance(t, str)
        assert not any(x in t for x in ('rules/lords-of-vegas.md', 'summary-snapshot.md', 'reader-a.json',
            'reader-b.json', 'results.json', 'source-audit.json', 'q31-scope-adjudication.json', 'list_agents', 'read_thread', 'wait_threads'))
        calls[p['call_id']] = (n, p, t)
        if 'clean-final-coverage-review.json' in t and any(x in t for x in ('write_text', 'writeFile', 'apply_patch')):
            boundaries.append(n)
    elif p.get('type') in ('function_call_output', 'custom_tool_call_output'):
        outputs.append((n, p, list(strings(p.get('output')))))
assert contexts and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in contexts)
assert boundaries
boundary = min(boundaries)
checks = []
for f in d['delivery_receipts']:
    p = Path(f['path']); t = p.read_text(); cursor = 0; parts = []
    assert H(p) == f['sha256'] and len(t) == f['characters']
    for c in f['chunks']:
        a, z = c['start_character_inclusive'], c['end_character_exclusive']
        assert a == cursor and a < z <= len(t) and HB(t[a:z].encode()) == c['chunk_sha256_utf8']
        matches = [n for n, _, vals in outputs if n < boundary and any(t[a:z] in x for x in vals)]
        assert matches, (str(p), a, z)
        parts.append({'start': a, 'end': z, 'slice_sha256': c['chunk_sha256_utf8'], 'actual_output_records': matches})
        cursor = z
    assert cursor == len(t)
    checks.append({'path': str(p), 'sha256': H(p), 'complete': True, 'parts': parts})
u = B / 'source-preflight/lords-of-vegas/unified-2022'
for p in [u / 'provenance.json', u / 'publisher-downloads-visible.txt']:
    t = p.read_text()
    matches = [n for n, _, vals in outputs if n < boundary and any(t in x for x in vals)]
    assert matches
    checks.append({'path': str(p), 'sha256': H(p), 'complete': True,
        'parts': [{'start': 0, 'end': len(t), 'actual_output_records': matches}]})
native = []
for n, p, vals in outputs:
    out = p.get('output')
    if not isinstance(out, list):
        continue
    count = sum(isinstance(v, dict) and v.get('type') == 'input_image' for v in out)
    if count:
        cn, call, t = calls[p['call_id']]
        paths = re.findall(r'path:\s*"([^"\n]+)"', t)
        assert cn < n < boundary and len(paths) == count
        native.extend({'path': path, 'sha256': H(Path(path)), 'call_record': cn, 'output_record': n} for path in paths)
assert len(native) == 1 and Path(native[0]['path']).name == 'original-rulebook-p4.png'
v = R / 'expanded-v6'
q, k, g, scope = (load(v / name) for name in ('questions.json', 'answer-key.json', 'grading-key.json', 'scope-map.json'))
ids = [x['id'] for x in q['questions']]
assert len(ids) == len(set(ids)) == 38
assert [x['id'] for x in k['answers']] == [x['id'] for x in g['answers']] == [x['id'] for x in scope['entries']] == ids
seedq, seedk = (load(R / 'seed-iteration-01' / name) for name in ('questions.json', 'answer-key.json'))
assert q['questions'][:20] == seedq['questions'] and k['answers'][:20] == seedk['answers']
q35, k35 = (load(R / 'expanded-iteration-03' / name) for name in ('questions.json', 'answer-key.json'))
assert q['questions'][:35] == q35['questions'] and k['answers'][:35] == k35['answers']
ledger = load(R / 'coverage-ledger-v6.json')
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'N': 38, 'coverage_report_path': str(AP), 'coverage_report_sha256': H(AP),
    'runtime_path': str(runtime), 'runtime_sha256_at_check': H(runtime), 'actual_contexts': contexts,
    'report_creation_boundary_record': boundary, 'text_checks': checks, 'native_checks': native,
    'original20_and_prior35_question_and_baseline_key_entries_preserved': True,
    'bank_hashes': {name: H(v / name) for name in ('questions.json', 'answer-key.json', 'grading-key.json', 'scope-map.json', 'bank-freeze-manifest.json')},
    'stopping_rule': d['stopping_rule_assessment'],
    'independence_qualification': 'Current permitted ledger includes references to preserving former grades/adjudication, without reader answers or grade results. Original prompt is opaque; actual source-only tool trace excludes summary, readers, prior reports, grade files and peer status. Explicit initially fresh settings are independently checked in the critical-actor model proof.',
    'limits': 'Source/key coverage and original-entry preservation only. Independent source audit, blind-reader factual results, exact summary, stamp and publication remain separate gates.'}
target = B / 'coordinator-checks/lords-clean-final38-coverage.json'
assert not target.exists()
target.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'N': 38, 'text_files': len(checks), 'text_slices': sum(len(x['parts']) for x in checks), 'native_images': len(native), 'report': str(target)}))
