"""Bind the fresh 86-question source/key challenge to its actual complete inputs."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
import re
import subprocess

B = Path(__file__).resolve().parent
R = B.parents[4] / 'docs/quality/summary-qa/sidereal-confluence' / B.name
D = R / 'expanded-v12'
H = lambda value: hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()
load = lambda path: json.loads(path.read_text())
audit = load(D / 'clean-coverage-scope-review.json')
assert all(v['status'] == 'PASS' for v in audit['verdicts'].values()) and not audit['findings']
assert audit['counts']['new_questions_proposed'] == 0
freeze = load(D / 'freeze.json')
for name, expected in freeze['hashes'].items():
    assert H((D / name).read_bytes()) == expected
q = load(D / 'questions.json')['questions']
key = load(D / 'answer-key.json')['answers']
scope = load(D / 'asked-facts.json')['questions']
assert len(q) == len(key) == len(scope) == len(audit['per_question_checks']) == 86
assert sum(len(s['required_facts']) for s in scope) == 256
assert q[:85] == load(R / 'expanded-v11/questions.json')['questions']
for question, answer, asked, checked in zip(q, key, scope, audit['per_question_checks']):
    assert question['id'] == answer['id'] == asked['id'] == checked['id']
    assert asked['question'] == question['question']
    assert checked['source_key'] == checked['exact_asked_scope'] == 'PASS'
    assert [x['id'] for x in checked['atom_checks']] == [x['id'] for x in asked['required_facts']]
    assert all(x['source_supported'] and x['actually_asked'] for x in checked['atom_checks'])
closure = load(D / 'coverage-closure.json')
assert closure['root_zero_addition_passes'] == [34, 35] and closure['question_count'] == 86 and closure['required_facts'] == 256
parent_text = load(D / 'reviewer-runtime-text-delivery.json')
parent_native = load(D / 'runtime-native-delivery.json')
runtime = Path(parent_text['runtime_source_path'])
raw = runtime.read_bytes().splitlines(keepends=True)
rows = {n: json.loads(line) for n, line in enumerate(raw, 1)}
actor = parent_text['identity']


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
    elif isinstance(value, (list, dict)):
        for child in (value.values() if isinstance(value, dict) else value):
            yield from strings(child, depth + 1)


def image_paths(code):
    """Only enumerate literal arrays/ranges and substitute their literal templates."""
    quoted = r'"(?:\\.|[^"\\])*"'
    constants = {m[1]: json.loads(m[2]) for m in re.finditer(r'const\s+(\w+)\s*=\s*(' + quoted + r')\s*;', code)}
    environments = [constants]
    for m in re.finditer(r'for\s*\(const\s+(\w+)\s+of\s+(\[[^\]]*\])\)', code):
        values = json.loads(m[2])
        assert all(isinstance(v, str) for v in values)
        environments += [dict(constants, **{m[1]: value}) for value in values]
    for m in re.finditer(r'for\s*\(let\s+(\w+)=(\d+);\1<=(\d+);\1\+\+\)', code):
        assert 1 <= int(m[2]) <= int(m[3]) <= 10
        environments += [dict(constants, **{m[1]: value}) for value in range(int(m[2]), int(m[3]) + 1)]
    paths = {json.loads(m[1]) for m in re.finditer(r'path:\s*(' + quoted + r')\s*[,}]', code)}
    for m in re.finditer(r'path:\s*`([^`]+)`', code):
        for env in environments:
            value = m[1]
            for name, replacement in env.items():
                value = value.replace('${' + name + '}', str(replacement))
                if isinstance(replacement, int):
                    value = re.sub(r'\$\{String\(' + re.escape(name) + r'\)\.padStart\(2,[\x27\x22]0[\x27\x22]\)\}', f'{replacement:02d}', value)
            if '${' not in value:
                paths.add(value)
    return paths


outputs, contexts, writes, calls = [], [], [], []
for n, row in rows.items():
    p = row.get('payload', {})
    if row['type'] == 'session_meta':
        assert p['id'] == actor['id'] and p['parent_thread_id'] == actor['parent'] and p['agent_path'] == actor['task']
    if row['type'] == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if row['type'] != 'response_item':
        continue
    if p.get('type') in ('custom_tool_call', 'function_call'):
        code = p.get('input', p.get('arguments', ''))
        assert not any(t in code for t in ('summary-snapshot.md', 'rules/sidereal-confluence.md', 'reader-a.json', 'reader-b.json', 'results.json', 'source-audit-04/', 'source-audit-05/'))
        assert not any(t in p.get('name', '') for t in ('collaboration', 'thread'))
        nested = sorted(set(re.findall(r'tools\.([\w]+)', code)))
        assert set(nested) <= {'exec_command', 'view_image'}
        calls.append({'record': n, 'input_sha256': H(code), 'nested_tools': nested})
        if 'clean-coverage-scope-review.json' in code and any(t in code for t in ('write_text', 'writeFile', 'apply_patch')):
            writes.append(n)
    elif p.get('type') in ('custom_tool_call_output', 'function_call_output'):
        outputs.append((n, list(strings(p.get('output')))))
assert contexts and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in contexts)
boundary = min(writes)
assert boundary == parent_native['all_native_views_before_first_report_write_ordinal']
text_checks = []
for receipt in audit['text_read_receipts']:
    path = Path(receipt['path'])
    text = path.read_text()
    assert H(path.read_bytes()) == receipt['sha256'] and len(text) == receipt['character_count']
    cursor, slices = 0, []
    for start, end in receipt['contiguous_half_open_ranges']:
        assert start == cursor and start < end <= len(text)
        literal = text[start:end]
        # text(r) delivered a JSON-serialized exec result. One host truncation
        # prevented parsing its outer object; complete escaped source slices
        # remain lossless receipts. The missing middle slice was reread.
        encoded = json.dumps(literal, ensure_ascii=False)[1:-1]
        found = [n for n, values in outputs if n < boundary and any(literal in value or encoded in value for value in values)]
        assert found, (str(path), start, end)
        slices.append({'start': start, 'end': end, 'actual_output_records': found,
            'literal_or_exact_single_JSON_string_encoding': True})
        cursor = end
    assert cursor == len(text)
    text_checks.append({'path': str(path), 'sha256': receipt['sha256'], 'complete': True, 'slices': slices})
native_checks, grouped = [], Counter()
for binding in parent_native['bindings']:
    path = Path(binding['path'])
    x = binding['native_output_binding']
    assert H(path.read_bytes()) == binding['sha256'] and H(raw[x['ordinal'] - 1]) == x['record_sha256'] and H(raw[x['call_ordinal'] - 1]) == x['call_record_sha256']
    call, output = rows[x['call_ordinal']]['payload'], rows[x['ordinal']]['payload']
    assert call['call_id'] == output['call_id'] == x['call_id'] and x['call_ordinal'] < x['ordinal'] < boundary
    assert str(path) in image_paths(call.get('input', call.get('arguments', ''))), (str(path), x['call_ordinal'])
    grouped[x['ordinal']] += 1
    native_checks.append({'path': str(path), 'sha256': binding['sha256'], 'call_record': x['call_ordinal'], 'output_record': x['ordinal']})
assert len(native_checks) == len(audit['native_view_receipts']) == 39
for n, count in grouped.items():
    assert count == sum(isinstance(v, dict) and v.get('type') == 'input_image' for v in rows[n]['payload']['output'])
parent_paths = subprocess.run(['rg', '--files', '/mnt/c/Users/jonny/.codex/sessions'], capture_output=True, text=True, check=True).stdout.splitlines()
parent_path = next(Path(p) for p in parent_paths if p.endswith(actor['parent'] + '.jsonl'))
spawns = []
for n, line in enumerate(parent_path.open(), 1):
    row = json.loads(line)
    p = row.get('payload', {})
    if row['type'] == 'response_item' and p.get('type') == 'function_call' and p.get('name', '').endswith('spawn_agent'):
        a = json.loads(p['arguments']) if isinstance(p['arguments'], str) else p['arguments']
        if a.get('task_name') == actor['task'].rsplit('/', 1)[-1]:
            spawns.append({'record': n, **{k: a.get(k) for k in ('task_name', 'model', 'reasoning_effort', 'fork_turns')}})
assert len(spawns) == 1 and spawns[0]['model'] == 'gpt-6.1-sol' and spawns[0]['reasoning_effort'] == 'high' and spawns[0]['fork_turns'] == 'none'
out = B / 'coordinator-checks/sidereal-expanded-v12-clean-coverage.json'
assert not out.exists()
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'review_path': str(D / 'clean-coverage-scope-review.json'), 'review_sha256': H((D / 'clean-coverage-scope-review.json').read_bytes()), 'questions': 86, 'facts': 256, 'first85_question_objects_unchanged': True, 'all_frozen_hashes_match': True, 'all_reviewed_fact_ids_exact': True, 'actual_initial_spawn': spawns[0], 'actual_contexts': contexts, 'runtime_path': str(runtime), 'runtime_sha256_at_check': H(runtime.read_bytes()), 'first_report_write_record': boundary, 'inputs': text_checks, 'native_image_bindings': native_checks, 'tool_call_hash_projection': calls, 'qualification': 'Current coverage map embeds historical stopping metadata; reviewer explicitly ignored it and conducted a new whole-source challenge. Truncated map segment was reread completely before report. Working saturation within documented original-base scope; no reader or publication approval.'}
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'questions': 86, 'facts': 256, 'complete_text_files': len(text_checks), 'native_images': len(native_checks), 'proof': str(out)}))
