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
    answer = load(D / f'reader-{letter}-delivery-ready.json')
    known = []
    for inp in answer['inputs_read']:
        p = Path(inp['path']); p = p if p.is_absolute() else ROOT/p
        source = p.read_text()
        assert H(p.read_bytes()) == inp['sha256']
        known.extend((str(p.resolve()), a, z, source[a:z]) for a,z in inp['read_ranges'])
    event_matches = {o['ordinal']: [(p,a,z) for p,a,z,t in known if any(t in v['text'] for v in o['blocks'])] for o in outputs}
    row={'reader':letter,'range_count':len(known),'proper_ranges':[],'failed_ranges':[]}
    for path,a,z,t in known:
        candidates=[];proper=[]
        for o in outputs:
            exact=any(t in v['text'] for v in o['blocks'])
            near=any(t[:128] in v['text'] or t[-128:] in v['text'] or t.rstrip() in v['text'] for v in o['blocks'])
            if not (exact or near):continue
            cap=calls.get(o['call_id'],{}).get('numeric_cap_candidates',[])
            trunc=any(any(marker in v['text'] for marker in ['Warning: truncated output','Output exceeded the available model context','Output exceeded available model context']) for v in o['blocks'])
            candidate={'event_ordinal':o['ordinal'],'record_sha256':o['record_sha256'],'associated_public_call':calls.get(o['call_id'],{}),'exact_literal_range_found':exact,'known_complete_ranges_in_event':[{'path':p,'range':[x,y]} for p,x,y in event_matches[o['ordinal']]],'truncation_marker_seen':trunc,'only_terminal_whitespace_differs':not exact and any(t.rstrip() in v['text'] for v in o['blocks']),'prefix128_matched':any(t[:128] in v['text'] for v in o['blocks']),'suffix128_matched':any(t[-128:] in v['text'] for v in o['blocks'])}
            candidates.append(candidate)
            if exact and cap and min(cap)>=4000 and not trunc and len(event_matches[o['ordinal']])==1:proper.append(candidate)
        value={'path':path,'range':[a,z],'expected_sha256':H(t.encode()),'candidate_metadata':candidates}
        row['proper_ranges' if proper else 'failed_ranges'].append(value)
    proof['readers'].append(row)
proof.update(diagnostic_only=True,strict_delivery_protocol_pass=all(not r['failed_ranges'] for r in proof['readers']),no_actual_delivery_criterion_relaxed=True,initial_strict_checker_failed_before_any_authoring=True)
p=D/'reader-first-empty-actual-delivery-diagnostic.json'
assert not p.exists()
p.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'diagnostic':str(p),'strict_delivery_protocol_pass':proof['strict_delivery_protocol_pass'],'readers':[{'reader':r['reader'],'proper':len(r['proper_ranges']),'failures':r['failed_ranges']} for r in proof['readers']],'private_runtime_bodies_copied':False}))
