"""Verify public full-slice delivery without copying privileged runtime bodies."""
from pathlib import Path
import hashlib
import json
import re

B = Path(__file__).resolve().parent
D = B / 'expanded-iteration-02'
H = lambda x: hashlib.sha256(x).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
proof = {'graders': [], 'private_runtime_bodies_copied': False,
         'limitations': 'Exact public tool-output matching proves recorded delivery, not cognition. Filesystem and declared read ledgers are separate checks. Only safe event references, hashes, numeric caps and source ranges are retained.'}
for number in range(1, 10):
    task = f'expanded2_grade_{number:02d}'
    profile = load(B / 'runtime' / f'{task}-final-completed-projection.json')
    calls, outputs = {}, []
    for ordinal, line in enumerate(Path(profile['session_path']).open('rb')):
        rec = json.loads(line)
        if rec.get('type') != 'response_item':
            continue
        p = rec.get('payload', {})
        if p.get('type') == 'custom_tool_call':
            # Inspect only reader-authored public tool code for numeric caps.
            code = p.get('input', '')
            caps = [int(x) for x in re.findall(r'''max_output_tokens["'\s]*[:=]\s*(\d+)''', code)] if isinstance(code, str) else []
            calls[p.get('call_id', p.get('id'))] = {'ordinal': ordinal, 'record_sha256': H(line), 'numeric_cap_candidates': caps}
        elif p.get('type') == 'custom_tool_call_output':
            public = p.get('output')
            if isinstance(public, str):
                blocks = [public]
            elif isinstance(public, list):
                blocks = [x['text'] for x in public if isinstance(x, dict) and x.get('type') == 'input_text' and isinstance(x.get('text'), str)]
            else:
                blocks = []
            decoded = []
            for index, block in enumerate(blocks):
                value = {'index': index, 'block_sha256': H(block.encode()), 'text': block, 'decoded_notify_json': False}
                try:
                    obj = json.loads(block)
                except (ValueError, TypeError):
                    obj = None
                if isinstance(obj, dict) and isinstance(obj.get('text'), str) and isinstance(obj.get('range'), list):
                    value.update(text=obj['text'], decoded_notify_json=True, declared_range=obj['range'], declared_cap=obj.get('output_cap_tokens'), declared_truncated=obj.get('truncated'))
                decoded.append(value)
            outputs.append({'ordinal': ordinal, 'record_sha256': H(line), 'call_id': p.get('call_id'), 'blocks': decoded})
    gpath = D / 'grading' / f'block-{number:02d}' / 'grades.json'
    grade = load(gpath)
    row = {'agent': '/root/' + task, 'grade_sha256': H(gpath.read_bytes()), 'inputs': []}
    event_ranges = {}
    for inp in grade['inputs_read']:
        path = Path(inp['path']).resolve()
        assert path == (D / 'summary-snapshot.md').resolve() or path.parent == (D / 'grading' / f'block-{number:02d}').resolve()
        source = path.read_text()
        assert H(path.read_bytes()) == inp['sha256']
        slices = []
        for start, end in inp['read_ranges']:
            excerpt = source[start:end]
            choices = []
            for event in outputs:
                for block in event['blocks']:
                    if excerpt not in block['text']:
                        continue
                    if block['decoded_notify_json'] and block['declared_range'] != [start, end]:
                        continue
                    call = calls.get(event['call_id'], {})
                    caps = call.get('numeric_cap_candidates', [])
                    if block['decoded_notify_json']:
                        cap = block['declared_cap']
                        if not isinstance(cap, int) or cap < 4000 or block['declared_truncated'] is not False:
                            continue
                    elif not caps or min(caps) < 4000:
                        continue
                    if any(x in block['text'] for x in ['Warning: truncated output', 'Output exceeded the available model context', 'Output exceeded available model context']):
                        continue
                    choices.append({'range': [start, end], 'slice_sha256': H(excerpt.encode()), 'event_ordinal': event['ordinal'], 'record_sha256': event['record_sha256'], 'public_block_index': block['index'], 'public_block_sha256': block['block_sha256'], 'decoded_notify_json_losslessly': block['decoded_notify_json'], 'associated_public_call': call, 'notify_declared_cap': block.get('declared_cap')})
            assert choices, (task, str(path), start, end)
            choice = choices[0]
            assert 0 < end - start <= 6000
            event_ranges.setdefault(choice['event_ordinal'], set()).add((str(path), start, end))
            slices.append(choice)
        assert slices[0]['range'][0] == 0 and slices[-1]['range'][1] == len(source)
        assert all(x['range'][1] == y['range'][0] for x, y in zip(slices, slices[1:]))
        assert [x['event_ordinal'] for x in slices] == sorted(x['event_ordinal'] for x in slices)
        row['inputs'].append({'path': str(path), 'sha256': H(path.read_bytes()), 'characters': len(source), 'slices': slices, 'all_exact_source_slices_delivered': True})
    assert len(row['inputs']) == 5
    assert all(len(v) == 1 for v in event_ranges.values()), (task, 'more than one source range per output event')
    row['one_source_range_per_recorded_output_event'] = True
    proof['graders'].append(row)
proof['all_actual_source_slices_verified'] = True
dest = D / 'grader-actual-delivery-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'proof': str(dest), 'sha256': H(dest.read_bytes()), 'all_actual_source_slices_verified': True, 'graders': [{'agent': r['agent'], 'slices': sum(len(x['slices']) for x in r['inputs'])} for r in proof['graders']], 'private_runtime_bodies_copied': False}))
