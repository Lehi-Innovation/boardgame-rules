"""Extract public tool-delivery receipts only; never copy private runtime records."""
from pathlib import Path
import hashlib
import json
import re

B = Path(__file__).resolve().parent
D = B / 'expanded-iteration-02'
ROOT = B.parents[4]
H = lambda data: hashlib.sha256(data).hexdigest()


def load(path):
    return json.loads(Path(path).read_text())


result = {'readers': [], 'private_runtime_bodies_copied': False,
          'scope': 'Only exact public tool-output slice matching, safe event references/hashes and numeric cap fields. No private messages, instructions, permission/account payloads or complete runtime records are retained.'}
for letter in 'ab':
    profile = load(B / f'runtime/expanded2_reader_{letter}-completed-projection.json')
    runtime = Path(profile['session_path'])
    calls = {}
    outputs = []
    for ordinal, line in enumerate(runtime.open('rb')):
        record = json.loads(line)
        if record.get('type') != 'response_item':
            continue
        payload = record.get('payload', {})
        if payload.get('type') == 'custom_tool_call':
            # Reader-authored public tool code is inspected only for numeric caps.
            # The code and all other fields are discarded, never printed/copied.
            code = payload.get('input', '')
            caps = [int(x) for x in re.findall(r'max_output_tokens["\s]*:\s*(\d+)', code)] if isinstance(code, str) else []
            calls[payload.get('call_id', payload.get('id'))] = {
                'record_ordinal': ordinal, 'record_sha256': H(line),
                'numeric_max_output_tokens_values': caps,
            }
        elif payload.get('type') == 'custom_tool_call_output':
            # Whitelist public input_text blocks only; do not traverse passthrough metadata.
            blocks = [x['text'] for x in payload.get('output', [])
                      if isinstance(x, dict) and x.get('type') == 'input_text'
                      and isinstance(x.get('text'), str)]
            outputs.append({'ordinal': ordinal, 'record_sha256': H(line),
                            'call_id': payload.get('call_id'), 'blocks': blocks})
    answer = load(D / f'reader-{letter}.json')
    reader = {'reader': f'reader-{letter}', 'runtime_path': str(runtime),
              'raw_answer_sha256': H((D / f'reader-{letter}.json').read_bytes()),
              'inputs': [], 'limitations': 'Matching exact public tool outputs proves recorded delivery of the full source slices. It does not prove cognition. Numeric cap candidates are extracted only from associated public reader-authored tool code; original reader declarations remain separate.'}
    for inp in answer['inputs_read']:
        path = Path(inp['path'])
        if not path.is_absolute():
            path = ROOT / path
        assert path.resolve() in {(D / 'summary-snapshot.md').resolve(), (D / 'questions.json').resolve()}
        text = path.read_text()
        digest = H(path.read_bytes())
        matches = []
        for start, end in inp['read_ranges']:
            excerpt = text[start:end]
            candidates = []
            for out in outputs:
                for block_index, block in enumerate(out['blocks']):
                    if excerpt in block:
                        caps = calls.get(out['call_id'], {})
                        candidates.append({'start': start, 'end': end,
                            'slice_utf8_sha256': H(excerpt.encode()),
                            'runtime_record_ordinal': out['ordinal'],
                            'runtime_record_sha256': out['record_sha256'],
                            'public_output_block_index': block_index,
                            'public_output_block_sha256': H(block.encode()),
                            'whole_requested_slice_occurs_in_public_output': True,
                            'wrapper_truncation_notice': any(z in block for z in ['Warning: truncated output', 'Output exceeded available model context']),
                            'associated_public_tool_call': caps})
            assert candidates, (letter, str(path), start, end)
            # Source slices are unique in these public read results.
            chosen = candidates[0]
            assert not chosen['wrapper_truncation_notice']
            assert 0 < end - start <= 6000
            numeric_caps = chosen['associated_public_tool_call'].get('numeric_max_output_tokens_values', [])
            assert numeric_caps and min(numeric_caps) >= 4000, (letter, start, numeric_caps)
            matches.append(chosen)
        assert matches[0]['start'] == 0 and matches[-1]['end'] == len(text)
        assert all(a['end'] == z['start'] for a, z in zip(matches, matches[1:]))
        assert [x['runtime_record_ordinal'] for x in matches] == sorted(x['runtime_record_ordinal'] for x in matches)
        reader['inputs'].append({'path': str(path.resolve()), 'actual_sha256': digest,
            'characters': len(text), 'original_declared_sha256': inp['sha256'],
            'declared_sha256_matches_actual': inp['sha256'] == digest,
            'reader_declared_output_cap_tokens': inp['output_cap_tokens'],
            'complete_exact_recorded_tool_delivery': True, 'slices': matches})
    result['readers'].append(reader)
result['all_actual_source_slices_verified'] = True
out = D / 'reader-actual-delivery-validation.json'
assert not out.exists()
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'proof': str(out), 'sha256': H(out.read_bytes()),
    'all_actual_source_slices_verified': True,
    'readers': [{'reader': x['reader'], 'slice_count': sum(len(z['slices']) for z in x['inputs']),
                'declared_digest_mismatches': [z['path'] for z in x['inputs'] if not z['declared_sha256_matches_actual']]}
               for x in result['readers']], 'private_runtime_bodies_copied': False}))
