"""Verify the new clean v8 coverage challenge against original runtime delivery."""
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
import ast
import hashlib
import json
import re

B = Path(__file__).resolve().parent
REPO = B.parents[4]
R = REPO / 'docs/quality/summary-qa/lords-of-vegas' / B.name
AP = R / 'source-only-v8-review.json'
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_text())
d = load(AP)
assert d['verdict'] == 'PASS' and not d['findings'] and not d['proposed_additional_questions']
assert d['stopping_check']['status'] == 'PASS'
rp = Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/06/rollout-2026-11-06T16-04-44-01a1b31b-796c-74b3-9ab5-189bc599f664.jsonl')
tree = ast.parse((B / 'check-spirit-source09-delivery.py').read_text())
definitions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ('strings', 'literal_image_paths')]


class LiteralJSON:
    @staticmethod
    def loads(value):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            try:
                return ast.literal_eval(value)
            except (SyntaxError, ValueError) as exc:
                raise ValueError('Not a JSON or literal value') from exc


ns = {'json': LiteralJSON, 're': re, 'resolve': lambda p: Path(p) if Path(p).is_absolute() else REPO / p}
exec(compile(ast.Module(body=definitions, type_ignores=[]), '<literal-data-parsers>', 'exec'), ns)


def named_image_paths(code):
    paths = ns['literal_image_paths'](code)
    quoted = r'"(?:\\.|[^"\\])*"'
    for loop in re.finditer(r'for\s*\(\s*const\s+(\w+)\s+of\s+(\[[^\]]*\])\s*\)', code):
        name, values = loop[1], LiteralJSON.loads(loop[2])
        for m in re.finditer(r'path\s*:\s*(' + quoted + r')\s*\+\s*' + re.escape(name) + r'\s*}', code):
            paths.update(json.loads(m[1]) + str(value) for value in values)
    for loop in re.finditer(r'for\s*\(\s*let\s+(\w+)\s*=\s*(\d+);\s*\1\s*<=\s*(\d+);\s*\1\+\+\s*\)', code):
        name, first, last = loop[1], int(loop[2]), int(loop[3])
        assert 1 <= first <= last <= 16
        for m in re.finditer(r'path\s*:\s*(' + quoted + r')\s*\+\s*' + re.escape(name) + r'\s*\+\s*(' + quoted + r')', code):
            paths.update(json.loads(m[1]) + str(value) + json.loads(m[2]) for value in range(first, last+1))
    return paths


raw = rp.read_bytes().splitlines(keepends=True)
calls, outputs, contexts, writes = {}, [], [], []
for n, line in enumerate(raw, 1):
    row = json.loads(line); p = row.get('payload', {})
    if row.get('type') == 'session_meta':
        assert p['id'] == '01a1b31b-796c-74b3-9ab5-189bc599f664' and p['parent_thread_id'] == '01a1b2c1-d5d1-7333-8948-72708b3d1f3e'
        assert p['agent_path'] == '/root/source_only_v8_review'
    if row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ('custom_tool_call', 'function_call'):
        t = p.get('input', p.get('arguments', ''))
        assert isinstance(t, str)
        assert not any(x in t for x in ('rules/lords-of-vegas.md', 'summary-snapshot.md', 'reader-a.json', 'reader-b.json',
            'results.json', 'source-audit.json', 'case-scope-adjudication.json', 'list_agents', 'read_thread', 'wait_threads'))
        calls[p['call_id']] = (n, t)
        if AP.name in t and any(x in t for x in ('write_text', 'writeFile', 'apply_patch')):
            writes.append(n)
    elif p.get('type') in ('custom_tool_call_output', 'function_call_output'):
        outputs.append((n, p, list(ns['strings'](p.get('output')))))
assert contexts and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in contexts)
assert writes
boundary = min(writes)
grouped = defaultdict(list)
for c in d['complete_delivery_receipts']:
    p = Path(c['path']); t = p.read_text(); a, z = c['start'], c['end']
    assert len(t) == c['total'] and t[a:z] == c['exact_full_content'] and HB(t[a:z].encode()) == c['chunkSHA256']
    matches = [n for n, _, vals in outputs if n < boundary and any(t[a:z] in x for x in vals)]
    assert matches, (str(p), a, z)
    grouped[str(p)].append({'start': a, 'end': z, 'slice_sha256': c['chunkSHA256'], 'actual_output_records': matches})
text_checks = []
for path, parts in grouped.items():
    cursor = 0
    for c in parts:
        assert c['start'] == cursor and c['end'] > cursor
        cursor = c['end']
    assert cursor == len(Path(path).read_text())
    text_checks.append({'path': path, 'sha256': H(Path(path)), 'complete': True, 'parts': parts})
assert len(text_checks) == 9 and sum(len(x['parts']) for x in text_checks) == 39
native = []
for n, p, vals in outputs:
    out = p.get('output')
    if not isinstance(out, list):
        continue
    count = sum(isinstance(x, dict) and x.get('type') == 'input_image' for x in out)
    if not count:
        continue
    cn, t = calls[p['call_id']]
    paths = named_image_paths(t)
    assert cn < n < boundary and len(paths) == count
    native.extend({'path': path, 'sha256': H(Path(path)), 'call_record': cn, 'output_record': n} for path in sorted(paths))
assert len(native) == 7
assert {x['path']: x['sha256'] for x in native} == {x['path']: x['sha256'] for x in d['native_image_delivery_receipts']}
v = R / 'expanded-v8'
qs = load(v / 'questions.json')['questions']; ks = load(v / 'grading-key.json')['answers']; ss = load(v / 'scope-map.json')['entries']
ids = [x['id'] for x in qs]
assert len(ids) == len(set(ids)) == 38 and [x['id'] for x in ks] == [x['id'] for x in ss] == ids
assert qs == load(R / 'expanded-v6/questions.json')['questions']
assert load(v / 'answer-key.json')['answers'] == load(R / 'expanded-v6/answer-key.json')['answers']
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'N': 38,
    'coverage_report_path': str(AP), 'coverage_report_sha256': H(AP), 'runtime_path': str(rp),
    'runtime_sha256_at_check': H(rp), 'actual_contexts': contexts, 'report_creation_boundary_record': boundary,
    'text_checks': text_checks, 'native_checks': native, 'stopping_rule': d['stopping_check'],
    'all38_original_question_and_baseline_key_records_preserved': True,
    'bank_hashes': {name: H(v / name) for name in ('questions.json', 'answer-key.json', 'grading-key.json', 'scope-map.json', 'bank-freeze-manifest.json')},
    'limits': 'New independent source-only current-bank review and exact original delivery verified; initial fresh settings are checked in the separate critical-actor model proof. Does not accept blind-reader factual results, summary stamp or publication. Opaque runtime dispatch plaintext is not reconstructed.'}
out = B / 'coordinator-checks/lords-v8-current-coverage.json'
assert not out.exists()
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'N': 38, 'text_files': len(text_checks), 'text_slices': 39, 'native_images': len(native), 'report': str(out)}))
