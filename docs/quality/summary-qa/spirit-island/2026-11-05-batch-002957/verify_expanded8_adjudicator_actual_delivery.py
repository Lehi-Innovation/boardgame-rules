"""Verify public full-slice delivery without copying privileged runtime bodies."""
from pathlib import Path
import hashlib
import json
import re

B = Path(__file__).resolve().parent
D = B / 'expanded-iteration-08'
H = lambda x: hashlib.sha256(x).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
def pairs(item):
    return [(x.get('start',x.get('start_inclusive')),x.get('end',x.get('end_exclusive'))) if isinstance(x,dict) else tuple(x) for x in item['read_ranges']]
proof = {'adjudicators': [], 'private_runtime_bodies_copied': False,
         'limitations': 'Exact public tool-output matching proves recorded delivery, not cognition. Filesystem and declared read ledgers are separate checks. Only safe event references, hashes, numeric caps and source ranges are retained. Notify caps are literal public per-range metadata rather than a separately enforced per-event tool cap.'}
for number in [0]:
    task = 'expanded8_adjudication_01'
    profile = load(B / 'runtime' / f'{task}-final-completed-projection.json')
    assert profile['confirmed_settings'] and all(x=={'model':'gpt-6.1-sol','effort':'high'} for x in profile['confirmed_settings'])
    assert profile['requested_spawn']['fields']['fork_turns']=='none'
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
                if isinstance(obj,dict) and isinstance(obj.get('content'),str) and isinstance(obj.get('range'),list):
                    value['other_public_string_fields']=[v for k,v in obj.items() if isinstance(v,str) and k!='content']
                    obj={**obj,'text':obj['content']}
                if isinstance(obj, dict) and isinstance(obj.get('text'), str) and isinstance(obj.get('range'), list):
                    value['other_public_string_fields']=[v for k,v in obj.items() if isinstance(v,str) and k not in ['text','content']]
                    value.update(text=obj['text'], decoded_notify_json=True, declared_range=obj['range'], declared_cap=obj.get('output_cap_tokens'), declared_truncated=obj.get('truncated'))
                elif isinstance(obj, dict) and isinstance(obj.get('output'), str) and {'chunk_id', 'wall_time_seconds', 'exit_code'}.issubset(obj):
                    value.update(text=obj['output'], decoded_exec_result_json=True)
                    try:
                        inner = json.loads(obj['output'])
                    except (ValueError, TypeError):
                        inner = None
                    if isinstance(inner,dict) and isinstance(inner.get('content'),str) and isinstance(inner.get('range'),list):
                        value['other_public_string_fields']=[v for k,v in inner.items() if isinstance(v,str) and k!='content']
                        inner={**inner,'text':inner['content']}
                    if isinstance(inner, dict) and isinstance(inner.get('text'), str) and isinstance(inner.get('range', inner.get('read_range')), list):
                        value['other_public_string_fields']=[v for k,v in inner.items() if isinstance(v,str) and k not in ['text','content']]
                        value.update(text=inner['text'], decoded_notify_json=True, declared_range=inner.get('range', inner.get('read_range')), declared_cap=inner.get('output_cap_tokens'), declared_truncated=inner.get('truncated'))
                decoded.append(value)
            outputs.append({'ordinal': ordinal, 'record_sha256': H(line), 'call_id': p.get('call_id'), 'blocks': decoded})
    gpath = D / 'adjudication-01' / 'adjudication.json'
    grade = load(gpath)
    expected_paths={str(Path(p).resolve()) for p in load(gpath.parent/'input-manifest.json')['inputs']}
    assert len(grade['inputs_read'])==5 and {str(Path(i['path']).resolve()) for i in grade['inputs_read']}==expected_paths
    row = {'agent': '/root/' + task, 'grade_sha256': H(gpath.read_bytes()), 'inputs': []}
    event_ranges = {}
    known_snippets=[]
    for declared in grade['inputs_read']:
        text=Path(declared['path']).read_text()
        known_snippets.extend(text[a:z] for a,z in pairs(declared))
    for inp in grade['inputs_read']:
        path = Path(inp['path']).resolve()
        assert path == (D / 'summary-snapshot.md').resolve() or path.parent == (D / 'adjudication-01').resolve()
        source = path.read_text()
        assert H(path.read_bytes()) == inp['sha256']
        slices = []
        for start, end in pairs(inp):
            excerpt = source[start:end]
            choices = []
            for event in outputs:
                if event['ordinal'] in event_ranges:
                    continue
                for block in event['blocks']:
                    if excerpt not in block['text']:
                        continue
                    # The selected literal must be the only complete source range outside itself.
                    residual=[b['text'].replace(excerpt,'',1) for b in event['blocks']]+[t for b in event['blocks'] for t in b.get('other_public_string_fields',[])]
                    if any(s in t for s in known_snippets for t in residual):
                        continue
                    if any(excerpt in s and s != excerpt and s in b['text'] for s in known_snippets for b in event['blocks']):
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
    proof['adjudicators'].append(row)
proof['all_actual_source_slices_verified'] = True
dest = D / 'adjudication-01' / 'adjudicator-actual-delivery-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'proof': str(dest), 'sha256': H(dest.read_bytes()), 'all_actual_source_slices_verified': True, 'adjudicators': [{'agent': r['agent'], 'slices': sum(len(x['slices']) for x in r['inputs'])} for r in proof['adjudicators']], 'private_runtime_bodies_copied': False}))
