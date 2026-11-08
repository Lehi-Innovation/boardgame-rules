"""Independently bind complete Lords entries, asked facts and actual grader inputs."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
from collections import Counter
import hashlib
import json
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--iteration', required=True)
p.add_argument('--bank', default='expanded-v10')
p.add_argument('--grader', action='append', required=True, help='block-number:actor-id')
p.add_argument('--require-pass', action='store_true')
a = p.parse_args()
B = Path(__file__).resolve().parent
REPO = B.parents[4]
R = REPO / 'docs/quality/summary-qa/lords-of-vegas' / B.name
D = R / a.iteration
assert D.parent == R
load = lambda p: json.loads(p.read_text())
hb = lambda b: hashlib.sha256(b).hexdigest()
h = lambda p: hb(p.read_bytes())
canonical = lambda x: hb(json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
summary = D / 'summary-snapshot.md'
assert summary.read_bytes() == (REPO / 'rules/lords-of-vegas.md').read_bytes()
ids = [x['id'] for x in load(D / 'questions.json')['questions']]
raw = {w: {x['id']: x for x in load(D / ('reader-' + w + '.json'))['answers']} for w in ['a', 'b']}
assert all(list(x) == ids for x in raw.values())
frozen = load(D / 'input-manifest.json')
for name, digest in frozen['inputs'].items():
    assert h(D / name) == digest
for name, digest in frozen['grading_inputs'].items():
    assert h(R / a.bank / name) == digest
keys = {x['id']: x for x in load(R / a.bank / 'grading-key.json')['answers']}
scope = {x['id']: x for x in load(R / a.bank / 'scope-map.json')['entries']}
runtime_paths = subprocess.run(['rg', '--files', '/mnt/c/Users/jonny/.codex/sessions'], check=True, capture_output=True, text=True).stdout.splitlines()

def strings(x):
    if isinstance(x, str):
        yield x
        try:
            y = json.loads(x)
        except ValueError:
            return
        if y != x:
            yield from strings(y)
    elif isinstance(x, dict):
        if x.get('type') in ['image', 'input_image']:
            return
        for y in x.values():
            yield from strings(y)
    elif isinstance(x, list):
        for y in x:
            yield from strings(y)

def first(x, names):
    return next(x[k] for k in names if k in x)

seen = {w: [] for w in raw}
counts = {w: Counter() for w in raw}
facts = {w: 0 for w in raw}
checks = []
for spec in a.grader:
    block, actor = spec.split(':', 1)
    packet_path = D / ('grader-block-' + block + '.json')
    report_path = D / ('grader-block-' + block + '-results.json')
    packet, report = load(packet_path), load(report_path)
    def expand(x):
        if isinstance(x, dict):
            return packet['dictionary'][x['__literal_quote__']] if set(x) == {'__literal_quote__'} else {k: expand(v) for k, v in x.items()}
        return [expand(y) for y in x] if isinstance(x, list) else x
    entries = {x['id']: expand(x) for x in packet['entries']}
    assert list(entries) == packet['ids']
    for qid, x in entries.items():
        assert x['effective_fixed_key'] == keys[qid]
        assert x['asked_scope'] == scope[qid]
        for w in raw:
            assert x['raw_entries'][w] == raw[w][qid]
            assert canonical(raw[w][qid]) == x['original_entry_canonical_sha256'][w]
    reconstructed = report['reconstruction_validation'].get('entries')
    if isinstance(reconstructed, list):
        if reconstructed and 'reconstructed_entry' in reconstructed[0]:
            reconstructed = {w: {x['id']: x['reconstructed_entry'] for x in reconstructed if x['reader'] == w} for w in raw}
        else:
            # Duplicating every raw answer in the report is optional. The full
            # packet is independently reconstructed above and actually delivered
            # below; each individual grade still binds the original entry hash.
            for x in reconstructed:
                if 'computed_sha256' in x:
                    assert x['computed_sha256'] == canonical(raw[x['reader']][x['id']])
            reconstructed = None
    for w in raw:
        grades = report['readers'][w]['grades']
        assert [g['id'] for g in grades] == packet['ids']
        for g in grades:
            qid = g['id']
            if reconstructed is not None:
                assert reconstructed[w][qid] == raw[w][qid]
            assert g['original_entry_canonical_sha256'] == canonical(raw[w][qid])
            required = entries[qid]['asked_scope']['required_answer_facts']
            assert [(f['index'], f['required_fact']) for f in g['required_facts']] == list(enumerate(required))
            field_checks = first(g, ['original_field_assessments', 'original_field_assessment'])
            field_check_text = json.dumps(field_checks)
            assert all(k in field_check_text for k in raw[w][qid] if k not in ['id', 'question'])
            facts[w] += len(required)
            counts[w][g['grade'].lower()] += 1
            seen[w].append(qid)
            if a.require_pass:
                assert g['grade'].lower() == 'correct' and g['unsupported_guess'] is False
                assert all(f['status'] == 'met' for f in g['required_facts'])
    runtime = next(Path(x) for x in runtime_paths if x.endswith(actor + '.jsonl'))
    outputs, writers, contexts = [], [], []
    for n, line in enumerate(runtime.open(), 1):
        row = json.loads(line)
        z = row.get('payload', {})
        if row.get('type') == 'session_meta':
            assert z['id'] == actor and z['parent_thread_id'] == '01a1b2c1-d5d1-7333-8948-72708b3d1f3e'
        if row.get('type') == 'turn_context':
            contexts.append({'record': n, 'model': z.get('model'), 'effort': z.get('effort')})
        if row.get('type') != 'response_item':
            continue
        if z.get('type') in ['custom_tool_call', 'function_call']:
            t = z.get('input', z.get('arguments', ''))
            if report_path.name in t and any(v in t for v in ['write_text', 'writeFile', 'apply_patch', 'json.dump(', '.write(']):
                writers.append(n)
        elif z.get('type') in ['custom_tool_call_output', 'function_call_output']:
            outputs.append((n, list(strings(z.get('output')))))
    assert writers and contexts and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in contexts)
    boundary = min(writers)
    cursors, delivered = {}, []
    receipts = []
    for item in report['delivery_receipts']:
        receipts.extend(item['chunks'] if 'chunks' in item else [item])
    for c in receipts:
        fp = Path(first(c, ['path', 'file_path', 'filename']))
        assert fp in [summary, packet_path]
        text = fp.read_text()
        start = first(c, ['start_unicode_character', 'start_unicode_character_offset', 'start_character_offset', 'start_character', 'start'])
        end = first(c, ['end_unicode_character_exclusive', 'end_unicode_character_offset_exclusive', 'end_character_offset_exclusive', 'end_character_exclusive', 'end'])
        assert first(c, ['total_unicode_characters', 'total_characters', 'total']) == len(text)
        assert start == cursors.get(str(fp), 0) and start < end <= len(text)
        assert hb(text[start:end].encode()) == first(c, ['chunk_sha256', 'chunk_sha256_utf8'])
        assert c.get('exact_full_chunk', c.get('exact_chunk', text[start:end])) == text[start:end]
        actual = [n for n, vals in outputs if n < boundary and any(text[start:end] in v for v in vals)]
        assert actual, (block, str(fp), start, end)
        cursors[str(fp)] = end
        delivered.append({'path': str(fp), 'start': start, 'end': end, 'actual_output_records': actual})
    assert set(cursors) == {str(summary), str(packet_path)}
    assert all(end == len(Path(fp).read_text()) for fp, end in cursors.items())
    checks.append({'block': block, 'actor': actor, 'packet_sha256': h(packet_path), 'report_path': str(report_path), 'report_sha256': h(report_path), 'runtime_path': str(runtime), 'runtime_sha256_at_check': h(runtime), 'contexts': contexts, 'first_writer_record': boundary, 'actual_delivery': delivered})
assert all(sorted(v) == sorted(ids) and len(v) == len(set(v)) for v in seen.values())
assert facts['a'] == facts['b']
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'iteration': a.iteration, 'N': len(ids), 'facts_each': facts['a'], 'summary_sha256': h(summary), 'scores': {w: dict(c) for w, c in counts.items()}, 'require_pass': a.require_pass, 'blocks': checks, 'limits': 'Complete original same-entry reconstruction, asked-fact identities and actual complete grader delivery are independently checked. This integrity proof retains primary grades; it does not replace substantive grading, neutral adjudication, source/coverage review, initial-fork verification, stamping or publication.'}
target = B / 'coordinator-checks' / ('lords-' + a.iteration + '-grading-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '.json')
target.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'N': len(ids), 'facts_each': facts['a'], 'scores': result['scores'], 'report': str(target)}))
