"""Verify public full-slice delivery without copying privileged runtime bodies."""
from pathlib import Path
import hashlib
import json
import re

B = Path(__file__).resolve().parent
D = B / 'expanded-iteration-03'
H = lambda x: hashlib.sha256(x).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
proof = {'graders': [], 'private_runtime_bodies_copied': False,
         'limitations': 'Exact public tool-output matching proves recorded delivery, not cognition. Filesystem and declared read ledgers are separate checks. Only safe event references, hashes, numeric caps and source ranges are retained. Notify caps are literal public per-range metadata rather than a separately enforced per-event tool cap.'}
for number in [0]:
    task = 'expanded3_adjud_01'
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
                if isinstance(obj, dict) and obj.get('status') == 'fulfilled' and isinstance(obj.get('value'), dict) and {'chunk_id', 'wall_time_seconds', 'exit_code', 'output'}.issubset(obj['value']):
                    obj = obj['value']
                    value['decoded_fulfilled_public_result_json'] = True
                if isinstance(obj, dict) and isinstance(obj.get('text'), str) and isinstance(obj.get('range'), list):
                    value.update(text=obj['text'], decoded_notify_json=True, declared_range=obj['range'], declared_cap=obj.get('output_cap_tokens'), declared_truncated=obj.get('truncated'))
                elif isinstance(obj, dict) and isinstance(obj.get('output'), str) and {'chunk_id', 'wall_time_seconds', 'exit_code'}.issubset(obj):
                    value.update(text=obj['output'], decoded_exec_result_json=True)
                    try:
                        inner = json.loads(obj['output'])
                    except (ValueError, TypeError):
                        inner = None
                    if isinstance(inner, dict) and isinstance(inner.get('text'), str) and isinstance(inner.get('range'), list):
                        value.update(text=inner['text'], decoded_notify_json=True, declared_range=inner['range'], declared_cap=inner.get('output_cap_tokens'), declared_truncated=inner.get('truncated'))
                decoded.append(value)
            outputs.append({'ordinal': ordinal, 'record_sha256': H(line), 'call_id': p.get('call_id'), 'blocks': decoded})
    gpath = D / 'adjudication-01' / 'adjudication.json'
    grade = load(gpath)
    row = {'agent': '/root/' + task, 'grade_sha256': H(gpath.read_bytes()), 'inputs': []}
    event_ranges = {}
    for inp in grade['inputs_read']:
        path = Path(inp['path']).resolve()
        assert path == (D / 'summary-snapshot.md').resolve() or path in {(D / 'adjudication-01' / n).resolve() for n in ['questions.json', 'answer-key.json', 'asked-facts.json', 'raw-cases.json']}
        source = path.read_text()
        assert H(path.read_bytes()) == inp['sha256']
        slices = []
        for part in inp['read_ranges']:
            start, end = part['start'], part['end']
            excerpt = source[start:end]
            choices = []
            for event in outputs:
                if event['ordinal'] in event_ranges:
                    continue
                for block in event['blocks']:
                    if excerpt not in block['text']:
                        continue
                    if block['decoded_notify_json'] and block['declared_range'] != [start, end]:
                        continue
                    call = calls.get(event['call_id'], {})
                    caps = call.get('numeric_cap_candidates', [])
                    if block['decoded_notify_json']:
                        cap = block['declared_cap']
                        if cap is not None and (not isinstance(cap, int) or cap < 4000):
                            continue
                        if block['declared_truncated'] is not None and block['declared_truncated'] is not False:
                            continue
                        if (not caps or min(caps) < 4000) and (not isinstance(cap, int) or cap < 4000):
                            continue
                    elif not caps or min(caps) < 4000:
                        continue
                    if any(x in block['text'] for x in ['Warning: truncated output', 'Output exceeded the available model context', 'Output exceeded available model context']):
                        continue
                    choices.append({'range': [start, end], 'slice_sha256': H(excerpt.encode()), 'event_ordinal': event['ordinal'], 'record_sha256': event['record_sha256'], 'public_block_index': block['index'], 'public_block_sha256': block['block_sha256'], 'decoded_notify_json_losslessly': block['decoded_notify_json'], 'decoded_exec_result_json_losslessly': block.get('decoded_exec_result_json', False), 'associated_public_call': call, 'notify_declared_cap': block.get('declared_cap')})
            assert choices, (task, str(path), start, end)
            choice = choices[0]
            assert 0 < end - start <= 6000
            event_ranges.setdefault(choice['event_ordinal'], set()).add((str(path), start, end))
            slices.append(choice)
        assert slices[0]['range'][0] == 0 and slices[-1]['range'][1] == len(source)
        assert all(x['range'][1] == y['range'][0] for x, y in zip(slices, slices[1:]))
        chronological = [x['event_ordinal'] for x in slices] == sorted(x['event_ordinal'] for x in slices)
        row['inputs'].append({'path': str(path), 'sha256': H(path.read_bytes()), 'characters': len(source), 'slices': slices, 'all_exact_source_slices_delivered': True, 'source_range_order_is_runtime_chronological': chronological})
    assert len(row['inputs']) == 5
    assert all(len(v) == 1 for v in event_ranges.values()), (task, 'more than one source range per output event')
    row['one_source_range_per_recorded_output_event'] = True
    proof['graders'].append(row)
proof['all_actual_source_slices_verified'] = True
dest = D / 'adjudication-01' / 'adjudicator-actual-delivery-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'proof': str(dest), 'sha256': H(dest.read_bytes()), 'all_actual_source_slices_verified': True, 'graders': [{'agent': r['agent'], 'slices': sum(len(x['slices']) for x in r['inputs'])} for r in proof['graders']], 'private_runtime_bodies_copied': False}))
