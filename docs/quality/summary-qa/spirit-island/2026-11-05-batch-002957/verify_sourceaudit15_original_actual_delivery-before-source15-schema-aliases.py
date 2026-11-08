"""Match only public source-delivery payloads; never retain private runtime bodies."""
from pathlib import Path
import base64
import hashlib
import json
import re

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
H = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
profile = load(B / 'runtime/final_source_audit_15-initial-projection.json')
ledger = load(B / 'source-audit-final-15-read-ledger.json')
visual = load(B / 'source-audit-final-15-visual-manifest.json')
# Lossless in-memory field aliases only; original frozen artifacts are unchanged.
ledger={**ledger,'deliveries':ledger['source_delivery'],'source_files':ledger['files']}
visual={**visual,'visual_sources':visual['observations']}
def public_strings(value):
    if isinstance(value,str):return [value]
    if isinstance(value,dict):return [s for x in value.values() for s in public_strings(x)]
    if isinstance(value,list):return [s for x in value for s in public_strings(x)]
    return []
calls, outputs, images = {}, [], []
boundary=load(B/'source-audit15-original-completed-runtime-boundary.json')
with Path(boundary['session_path']).open('rb') as stream:
    assert H(stream.read(boundary['prefix_bytes']))==boundary['prefix_sha256']
assert profile['session_path']==boundary['session_path']
for ordinal, line in enumerate(Path(profile['session_path']).open('rb')):
    if ordinal>=boundary['record_count']:break
    record = json.loads(line)
    if record.get('type') != 'response_item':
        continue
    p = record.get('payload', {})
    if p.get('type') == 'custom_tool_call':
        code = p.get('input', '')
        caps = [int(x) for x in re.findall(r'''max_output_tokens["'\s]*[:=]\s*(\d+)''', code)] if isinstance(code, str) else []
        calls[p.get('call_id', p.get('id'))] = {'ordinal': ordinal, 'record_sha256': H(line), 'numeric_cap_candidates': caps}
    elif p.get('type') == 'custom_tool_call_output':
        raw = p.get('output')
        blocks = [{'type': 'input_text', 'text': raw}] if isinstance(raw, str) else raw if isinstance(raw, list) else []
        texts = []
        for index, block in enumerate(blocks):
            if not isinstance(block, dict):
                continue
            if block.get('type') == 'input_image':
                url = block.get('image_url')
                assert isinstance(url, str) and url.startswith('data:') and ';base64,' in url
                encoded = url.split(';base64,', 1)[1]
                payload = base64.b64decode(encoded, validate=True)
                images.append({'event_ordinal': ordinal, 'record_sha256': H(line), 'public_block_index': index, 'displayed_bytes_sha256': H(payload), 'displayed_bytes': len(payload), 'detail': block.get('detail')})
                continue
            if block.get('type') != 'input_text' or not isinstance(block.get('text'), str):
                continue
            text = block['text']
            original_sha = H(text.encode())
            decoded_layers = []
            other_public_string_fields=[]
            for unused in range(4):
                try:
                    obj = json.loads(text)
                except (ValueError, TypeError):
                    break
                if isinstance(obj, dict) and obj.get('status') == 'fulfilled' and isinstance(obj.get('value'), dict):
                    other_public_string_fields.extend(public_strings({k:v for k,v in obj.items() if k!='value'}))
                    obj = obj['value']
                    decoded_layers.append('public fulfilled/value result')
                if isinstance(obj,dict):
                    primary='output' if isinstance(obj.get('output'),str) and {'chunk_id','exit_code'}.issubset(obj) else 'text' if isinstance(obj.get('text'),str) else 'content' if isinstance(obj.get('content'),str) and isinstance(obj.get('range'),list) else None
                    if primary:other_public_string_fields.extend(public_strings({k:v for k,v in obj.items() if k!=primary}))
                    if primary=='content':obj={**obj,'text':obj['content']}
                if isinstance(obj, dict) and isinstance(obj.get('output'), str) and {'chunk_id', 'exit_code'}.issubset(obj):
                    text = obj['output']
                    decoded_layers.append('public exec result output')
                elif isinstance(obj, dict) and isinstance(obj.get('text'), str):
                    text = obj['text']
                    decoded_layers.append('public source text field')
                else:
                    break
            texts.append({'block_index': index, 'original_block_sha256': original_sha, 'decoded_layers': decoded_layers, 'text': text, 'other_public_string_fields':other_public_string_fields})
        outputs.append({'ordinal': ordinal, 'record_sha256': H(line), 'call_id': p.get('call_id'), 'texts': texts})

used, receipts = set(), []
known_snippets=[(ROOT/x['path']).read_text()[x['start']:x['end']] for x in ledger['deliveries']]
for row in ledger['deliveries']:
    path = (ROOT / row['path']).resolve()
    source = path.read_text()
    assert H(path.read_bytes()) == row['source_sha256']
    start, end = row['start'], row['end']
    excerpt = source[start:end]
    assert 0 < end - start <= 6000 and H(excerpt.encode()) == row['slice_sha256']
    choices = []
    for output in outputs:
        if output['ordinal'] in used:
            continue
        call = calls.get(output['call_id'], {})
        caps = call.get('numeric_cap_candidates', [])
        if not caps or min(caps) < 4000:
            continue
        for block in output['texts']:
            if excerpt in block['text'] and not any(x in block['text'] for x in ['Warning: truncated output', 'Output exceeded the available model context', 'Output exceeded available model context']):
                residual=[x['text'].replace(excerpt,'',1) for x in output['texts']]+[s for x in output['texts'] for s in x.get('other_public_string_fields',[])]
                if any(snippet in text for snippet in known_snippets for text in residual):continue
                if any(excerpt in snippet and snippet!=excerpt and snippet in x['text'] for snippet in known_snippets for x in output['texts']):continue
                choices.append({'path': row['path'], 'range': [start, end], 'slice_sha256': row['slice_sha256'], 'event_ordinal': output['ordinal'], 'record_sha256': output['record_sha256'], 'public_block_index': block['block_index'], 'original_public_block_sha256': block['original_block_sha256'], 'losslessly_decoded_public_layers': block['decoded_layers'], 'associated_public_call': call})
    assert choices, (row['path'], start, end)
    chosen = choices[-1]
    used.add(chosen['event_ordinal'])
    receipts.append(chosen)

image_receipts = []
for visual_index, view in enumerate(visual['visual_sources']):
    path = ROOT / view['path']
    digest = H(path.read_bytes())
    assert digest == view.get('source_sha256',view.get('sha256'))
    matches = [x for x in images if x['displayed_bytes_sha256'] == digest and x['detail']=='original']
    assert matches, (visual_index, view['path'], 'original image bytes absent from public deliveries')
    if view['dimensions'] == [2697,1797]:
        assert path.stat().st_size == 19419092 and view['dimensions'] == [2697, 1797]
    image_receipts.append({'id': visual_index, 'path': view['path'], 'source_sha256': digest, 'source_bytes': path.stat().st_size, 'dimensions': view['dimensions'], 'original_source_bytes_delivered_without_reencoding': True, 'public_image_deliveries': matches})

assert len(receipts)==len(ledger['deliveries'])==len(used)
assert len(image_receipts)==len(visual['visual_sources'])
proof = {'verified': True, 'candidate_sha256': load(B/'source-audit-final-15.json')['candidate_sha256'], 'text_sources': len(ledger['source_files']), 'record_cutoff_exclusive':boundary['record_count'], 'original_boundary_sha256':H((B/'source-audit15-original-completed-runtime-boundary.json').read_bytes()), 'actual_distinct_text_range_deliveries': len(receipts), 'one_source_range_per_matched_output_event': True, 'text_deliveries': receipts, 'unique_visual_sources': len(image_receipts), 'public_image_blocks': len(images), 'visuals': image_receipts, 'no_private_runtime_bodies_copied': True, 'limitations': 'Only public custom-tool source text/image payloads and numeric public call caps are inspected; safe hashes and event references are retained. Exact delivered original source bytes prove recorded transport, not cognition or semantic correctness. This proof scans only the fixed original completed runtime prefix; filesystem and semantic checks remain separate.'}
dest = B / 'source-audit15-original-actual-delivery-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps({'proof': str(dest), 'sha256': H(dest.read_bytes()), 'verified': True, 'text_sources': proof['text_sources'], 'text_ranges': len(receipts), 'visual_sources': len(image_receipts), 'public_image_blocks': len(images), 'private_runtime_bodies_copied': False}))
