"""Verify public reader source deliveries; retain hashes, never private runtime bodies."""
from pathlib import Path
import hashlib
import json
import re
import sys

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
D = (B / sys.argv[1]).resolve()
prefix = sys.argv[2]
assert sys.argv[3:] in [['--pre-authoring'], ['--complete']]
pre_authoring = sys.argv[3:] == ['--pre-authoring']
diagnose = False
assert D.parent == B and re.fullmatch(r'expanded\d+_reader', prefix)
assert D.name == 'expanded-iteration-09' and prefix == 'expanded9_reader' and pre_authoring
H = lambda data: hashlib.sha256(data).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
proof = {'readers': [], 'private_runtime_bodies_copied': False,
         'limitations': 'Exact public tool payload matching establishes recorded full source delivery, not cognition. Only public source-output text is inspected; safe event references, hashes, decoded wrapper types and numeric public call caps are retained.'}
for letter in 'ab':
    profile_suffix = 'delivery-ready' if pre_authoring else 'completed'
    if pre_authoring and letter == 'b': profile_suffix = 'delivery-ready-after-technical-retry01'
    profile_path = B / 'runtime' / f'{prefix}_{letter}-{profile_suffix}-projection.json'
    profile = load(profile_path)
    assert profile['confirmed_settings'] and profile['turn_contexts']
    assert all(x == {'model': 'gpt-6-luna', 'effort': 'high'} for x in profile['confirmed_settings'])
    assert profile['requested_spawn']['fields']['fork_turns'] == 'none'
    calls, outputs = {}, []
    for ordinal, line in enumerate(Path(profile['session_path']).open('rb')):
        record = json.loads(line)
        if record.get('type') != 'response_item':
            continue
        p = record.get('payload', {})
        if p.get('type') == 'custom_tool_call':
            code = p.get('input', '')
            caps = [int(x) for x in re.findall(r'''max_output_tokens["'\s]*[:=]\s*(\d+)''', code)] if isinstance(code, str) else []
            calls[p.get('call_id', p.get('id'))] = {'ordinal': ordinal, 'record_sha256': H(line), 'numeric_cap_candidates': caps}
        elif p.get('type') == 'custom_tool_call_output':
            public = p.get('output')
            blocks = [public] if isinstance(public, str) else [x['text'] for x in public if isinstance(x, dict) and x.get('type') == 'input_text' and isinstance(x.get('text'), str)] if isinstance(public, list) else []
            decoded = []
            for index, text in enumerate(blocks):
                original_hash = H(text.encode())
                layers = []
                for unused in range(4):
                    try:
                        value = json.loads(text)
                    except (ValueError, TypeError):
                        break
                    if isinstance(value, dict) and value.get('status') == 'fulfilled' and isinstance(value.get('value'), dict):
                        value = value['value']
                        layers.append('public fulfilled/value result')
                    if isinstance(value, dict) and isinstance(value.get('output'), str) and {'chunk_id', 'exit_code'}.issubset(value):
                        text = value['output']
                        layers.append('public exec result output')
                    elif isinstance(value, dict) and isinstance(value.get('text'), str):
                        text = value['text']
                        layers.append('public source text field')
                    else:
                        break
                decoded.append({'index': index, 'original_block_sha256': original_hash, 'decoded_layers': layers, 'text': text})
            outputs.append({'ordinal': ordinal, 'record_sha256': H(line), 'call_id': p.get('call_id'), 'blocks': decoded})
    answer_suffix = '-delivery-ready' if pre_authoring else ''
    if pre_authoring and letter == 'b': answer_suffix = '-delivery-ready-after-technical-retry01'
    freeze_suffix = 'delivery-ready-freeze' if pre_authoring else 'original-freeze'
    if pre_authoring and letter == 'b': freeze_suffix = 'delivery-ready-after-technical-retry01-freeze'
    answer_path = D / f'reader-{letter}{answer_suffix}.json'
    answer = load(answer_path)
    if pre_authoring:
        assert answer['stage'] == 'delivery_ready' and answer['answers'] == []
    else:
        assert answer['stage'] == 'complete' and len(answer['answers']) == len(load(D/'questions.json')['questions'])
    freeze = load(D / f'reader-{letter}-{freeze_suffix}.json')
    assert H(answer_path.read_bytes()) == freeze['sha256']
    result = {'reader': f'reader-{letter}', 'raw_answer_sha256': freeze['sha256'], 'completed_profile_sha256': H(profile_path.read_bytes()), 'inputs': []}
    # A candidate event itself must contain only one declared complete source slice.
    # Merely selecting a different event for its second slice cannot hide aggregation.
    known = []
    for inp in answer['inputs_read']:
        p = Path(inp['path']); p = p if p.is_absolute() else ROOT/p
        assert p.resolve() in {(D/'summary-snapshot.md').resolve(), (D/'questions.json').resolve()}
        assert H(p.read_bytes()) == inp['sha256']
        text = p.read_text()
        assert all(0 <= start < end <= len(text) and end-start <= 6000 for start,end in inp['read_ranges'])
        known.extend((str(p.resolve()), start, end, text[start:end]) for start,end in inp['read_ranges'])
    bad_events = {}
    for event in outputs:
        matches = {(p,start,end) for p,start,end,text in known if any(text in block['text'] for block in event['blocks'])}
        if len(matches) > 1:
            bad_events[event['ordinal']] = sorted(matches)
    result['excluded_aggregated_source_events'] = [{'event_ordinal': k, 'known_ranges': v} for k,v in bad_events.items()]
    used, event_ranges = set(), {}
    for inp in answer['inputs_read']:
        path = Path(inp['path'])
        path = path if path.is_absolute() else ROOT / path
        path = path.resolve()
        assert path in {(D / 'summary-snapshot.md').resolve(), (D / 'questions.json').resolve()}
        source = path.read_text()
        assert H(path.read_bytes()) == inp['sha256']
        assert inp['character_length'] == len(source) and inp['output_cap_tokens'] >= 4000
        position, slices = 0, []
        for start, end in inp['read_ranges']:
            assert start == position and 0 < end - start <= 6000
            excerpt = source[start:end]
            choices = []
            for output in outputs:
                if output['ordinal'] in bad_events or (output['ordinal'] in used and not diagnose):
                    continue
                call = calls.get(output['call_id'], {})
                caps = call.get('numeric_cap_candidates', [])
                if not caps or min(caps) < 4000:
                    continue
                for block in output['blocks']:
                    if excerpt in block['text'] and not any(x in block['text'] for x in ['Warning: truncated output', 'Output exceeded the available model context', 'Output exceeded available model context']):
                        choices.append({'range': [start, end], 'slice_sha256': H(excerpt.encode()), 'event_ordinal': output['ordinal'], 'record_sha256': output['record_sha256'], 'public_block_index': block['index'], 'original_public_block_sha256': block['original_block_sha256'], 'losslessly_decoded_public_layers': block['decoded_layers'], 'associated_public_call': call})
            assert choices, (letter, str(path), start, end)
            choice = choices[0]
            used.add(choice['event_ordinal'])
            event_ranges.setdefault(choice['event_ordinal'], []).append({'path': str(path), 'range': [start, end]})
            slices.append(choice)
            position = end
        assert position == len(source)
        result['inputs'].append({'path': str(path), 'sha256': inp['sha256'], 'characters': len(source), 'slices': slices, 'complete_exact_recorded_delivery': True})
    assert len(result['inputs']) == 2
    result['one_source_range_per_matched_output_event'] = all(len(v) == 1 for v in event_ranges.values())
    result['actual_distinct_tool_output_events'] = len(used)
    result['multi_range_output_events'] = [{'event_ordinal': k, 'source_ranges': v, 'combined_known_source_characters': sum(x['range'][1] - x['range'][0] for x in v)} for k, v in event_ranges.items() if len(v) > 1]
    if not diagnose:
        assert result['one_source_range_per_matched_output_event']
    proof['readers'].append(result)
proof['all_actual_source_slices_verified'] = True
proof['strict_delivery_protocol_pass'] = all(x['one_source_range_per_matched_output_event'] for x in proof['readers'])
proof['diagnostic_only'] = False
proof['pre_authoring_checkpoint'] = pre_authoring
proof['all_readiness_files_have_no_answers'] = pre_authoring
if not pre_authoring:
    prior = load(D/'reader-pre-authoring-delivery-validation.json')
    assert prior['strict_delivery_protocol_pass'] and prior['pre_authoring_checkpoint'] and prior['all_readiness_files_have_no_answers']
    assert [[(x['path'],x['sha256']) for x in r['inputs']] for r in prior['readers']] == [[(x['path'],x['sha256']) for x in r['inputs']] for r in proof['readers']]
    proof['pre_authoring_validation_sha256'] = H((D/'reader-pre-authoring-delivery-validation.json').read_bytes())
dest = D / ('reader-pre-authoring-delivery-validation.json' if pre_authoring else 'reader-actual-delivery-validation.json')
assert not dest.exists()
dest.write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps({'proof': str(dest), 'sha256': H(dest.read_bytes()), 'all_actual_source_slices_verified': True, 'strict_delivery_protocol_pass': proof['strict_delivery_protocol_pass'], 'diagnostic_only': diagnose, 'readers': [{'reader': x['reader'], 'source_slices': sum(len(y['slices']) for y in x['inputs']), 'actual_tool_output_events': x['actual_distinct_tool_output_events'], 'multi_range_output_events': len(x['multi_range_output_events'])} for x in proof['readers']], 'private_runtime_bodies_copied': False}))
