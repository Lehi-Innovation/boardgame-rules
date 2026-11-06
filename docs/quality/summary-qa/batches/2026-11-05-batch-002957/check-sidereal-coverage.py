"""Check the clean closing coverage review, its frozen scope and actual inputs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

B = Path(__file__).resolve().parent
R = B.parents[4] / 'docs/quality/summary-qa/sidereal-confluence' / B.name
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text())


def visible_strings(value, depth=0):
    if depth > 10:
        return
    if isinstance(value, str):
        yield value
        try:
            decoded = json.loads(value)
        except ValueError:
            return
        if decoded != value:
            yield from visible_strings(decoded, depth + 1)
    elif isinstance(value, dict):
        for item in value.values():
            yield from visible_strings(item, depth + 1)
    elif isinstance(value, list):
        for item in value:
            yield from visible_strings(item, depth + 1)
bank = R / 'expanded-v5'
review_path = bank / 'clean-coverage-scope-review.json'
review = load(review_path)
assert all(v['verdict'] == 'PASS' for v in review['verdicts'].values())
assert all(not v.get('findings') for v in review['verdicts'].values())
assert not review['verdicts']['coverage_stopping']['genuine_new_additions']
assert not review['verdicts']['coverage_stopping']['corrections']
for name, expected in load(bank / 'freeze.json')['hashes'].items():
    assert H(bank / name) == expected
q = load(bank / 'questions.json')['questions']
key = load(bank / 'answer-key.json')['answers']
scope = load(bank / 'asked-facts.json')['questions']
assert len(q) == len(key) == len(scope) == len(review['per_question_checks']) == 76
assert sum(len(s['required_facts']) for s in scope) == 248
for question, answer, s, checked in zip(q, key, scope, review['per_question_checks']):
    assert question['id'] == answer['id'] == s['id'] == checked['id']
    assert question['question'] == s['question']
    assert checked['source_key_verdict'] == checked['exact_asked_scope_verdict'] == 'PASS'
    assert checked['checked_fact_ids'] == [f['id'] for f in s['required_facts']]
assert [p['result'] for p in review['source_passes']] == ['ZERO_ADDITIONS'] * 3
actor = next(x for x in load(R / 'runtime-provenance.json')['records']
             if x['identity'] == '01a1b163-6440-72f1-9d60-7955a1c1f770')
runtime = Path(actor['runtime_source_path'])
outputs, image_outputs, calls, writes, contexts = [], [], [], [], []
for n, line in enumerate(runtime.open(), 1):
    row = json.loads(line); p = row.get('payload', {})
    if row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ('custom_tool_call', 'function_call'):
        text = p.get('input', p.get('arguments', ''))
        assert isinstance(text, str)
        assert not any(s in text for s in ('summary-snapshot.md', 'rules/sidereal-confluence.md',
            'reader-a.json', 'reader-b.json', 'results.json', 'source-audit-01/', 'source-audit-02/'))
        assert not any(s in p.get('name', '') for s in ('collaboration', 'thread'))
        nested = sorted(set(re.findall(r'tools\.([\w]+)', text)))
        assert set(nested) <= {'exec_command', 'view_image'}
        calls.append({'record': n, 'input_sha256': hashlib.sha256(text.encode()).hexdigest(), 'nested_tools': nested})
        if 'clean-coverage-scope-review.json' in text and any(s in text for s in ('write_text', 'writeFile', 'apply_patch')):
            writes.append(n)
    elif p.get('type') in ('custom_tool_call_output', 'function_call_output'):
        for block in p.get('output', []):
            if not isinstance(block, dict):
                continue
            if block.get('type') == 'input_image':
                image_outputs.append(n)
            if block.get('type') == 'input_text':
                text = block.get('text', '')
                outputs.extend((n, value) for value in visible_strings(text))
assert contexts and all(c['model'] == 'gpt-6.1-sol' and c['effort'] == 'high' for c in contexts)
assert writes
boundary = min(writes)
inputs, binary_inputs = [], []
for receipt in review['delivery_receipts']:
    path = Path(receipt['path'])
    assert H(path) == receipt['sha256'] and path.stat().st_size == receipt['bytes']
    if 'ranges' not in receipt or receipt['ranges'] is None:
        assert path.suffix.lower() in ('.pdf', '.png', '.jpg', '.jpeg')
        binary_inputs.append({'path': str(path), 'sha256': receipt['sha256']})
        continue
    text = path.read_text()
    assert len(text) == receipt['characters']
    cursor, slices = 0, []
    for a, z in receipt['ranges']:
        assert a == cursor and a < z <= len(text)
        found = [n for n, visible in outputs if n < boundary and text[a:z] in visible]
        assert found, (str(path), a, z)
        slices.append({'start': a, 'end': z, 'actual_output_records': found})
        cursor = z
    assert cursor == len(text)
    inputs.append({'path': str(path), 'sha256': receipt['sha256'], 'complete': True, 'slices': slices})
assert len(binary_inputs) == 26 and len([n for n in image_outputs if n < boundary]) >= 35
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'review_path': str(review_path), 'review_sha256': H(review_path), 'questions': 76, 'facts': 248,
    'three_current_zero_addition_passes_or_challenges': True, 'all_frozen_hashes_match': True,
    'all_reviewed_fact_ids_exact': True, 'reviewer_id': actor['identity'], 'runtime_path': str(runtime),
    'runtime_sha256_at_check': H(runtime), 'actual_contexts': contexts, 'first_report_write_record': boundary,
    'inputs': inputs, 'binary_input_hash_bindings': binary_inputs,
    'native_image_outputs_before_report': [n for n in image_outputs if n < boundary],
    'tool_call_hash_projection': calls,
    'limits': 'Actual complete text delivery and allowed-tool/known-forbidden-path trace checked; semantic coverage verdict belongs to independent reviewer. Initial fresh spawn is checked with final model provenance. Working saturation is within declared original-base corpus.'}
out = B / 'coordinator-checks/sidereal-expanded-v5-clean-coverage.json'
assert not out.exists()
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'questions': 76, 'facts': 248, 'text_files': len(inputs),
    'text_slices': sum(len(x['slices']) for x in inputs), 'native_images': len(result['native_image_outputs_before_report']), 'report': str(out)}))
