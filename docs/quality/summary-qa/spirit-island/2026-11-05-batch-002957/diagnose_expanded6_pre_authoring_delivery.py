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
H = lambda data: hashlib.sha256(data).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
diagnostics=[]
proof = {'readers': [], 'private_runtime_bodies_copied': False,
         'limitations': 'Exact public tool payload matching establishes recorded full source delivery, not cognition. Only public source-output text is inspected; safe event references, hashes, decoded wrapper types and numeric public call caps are retained.'}
for letter in 'ab':
    profile_suffix = 'delivery-ready' if pre_authoring else 'completed'
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
    freeze_suffix = 'delivery-ready-freeze' if pre_authoring else 'original-freeze'
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
    rows=[]
    for path,start,end,excerpt in known:
        matches=[]
        for output in outputs:
            if any(excerpt in block['text'] for block in output['blocks']):
                call=calls.get(output['call_id'],{});caps=call.get('numeric_cap_candidates',[]);matches.append({'event_ordinal':output['ordinal'],'record_sha256':output['record_sha256'],'caps':caps,'aggregated_event':output['ordinal'] in bad_events,'truncated_marker':any('Warning: truncated output' in block['text'] for block in output['blocks'])})
        rows.append({'path':path,'range':[start,end],'slice_sha256':H(excerpt.encode()),'public_full_literal_matches':matches})
    diagnostics.append({'reader':letter,'source_ranges':rows,'aggregated_events':bad_events})
p=D/'pre-authoring-first-actual-source-match-diagnostic.json';assert not p.exists();p.write_text(json.dumps({'diagnostic_only':True,'unchanged_source_checker_sha256':H((B/'verify_staged_reader_actual_delivery.py').read_bytes()),'readers':diagnostics,'no_private_bodies_copied':True,'no_factual_scores_or_authoring_authorization':True},indent=2)+'\n')
print(json.dumps({'diagnostic':str(p),'noneligible_ranges':[{'reader':r['reader'],'range':x['range'],'path':x['path'],'matches':x['public_full_literal_matches']} for r in diagnostics for x in r['source_ranges'] if not any(m['caps'] and min(m['caps'])>=4000 and not m['aggregated_event'] and not m['truncated_marker'] for m in x['public_full_literal_matches'])]},indent=2))
