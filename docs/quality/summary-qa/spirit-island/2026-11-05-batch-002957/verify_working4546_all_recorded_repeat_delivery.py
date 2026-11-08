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
profile = load(B / 'runtime/working45_46-final-completed-projection.json')
boundary=load(B/'novelty-adjudication-18/completed-runtime-boundary.json')
raw_ledger=load(B/'working-source-sweeps-45-46-read-ledger.json')
rows=[]
for file in raw_ledger['new_delivered_text_files']:
 seen=set()
 for r in file['slices']:
  seen.add(tuple(r['range']))
  rows.append({'path':file['path'],'source_sha256':file['full_byte_sha256'],'start':r['range'][0],'end':r['range'][1],'slice_sha256':r['slice_utf8_sha256']})
ledger={'rows':rows,'complete_sources':[x for x in raw_ledger['new_delivered_text_files'] if x['complete_new_delivery']],'candidate_sha256':None}
raw_visual=load(B/'working-source-sweeps-45-46-visual-manifest.json')
visual={'visuals':[{'id':str(i),'path':r['path'],'source_sha256':r['sha256'],'dimensions':r['dimensions'],'kind':'original-core-panel-native' if r['dimensions']==[2697,1797] else 'primary-image'} for i,r in enumerate(raw_visual['images']) if r.get('newly_viewed')]}
calls, outputs, images = {}, [], []
for ordinal, line in enumerate(Path(profile['session_path']).open('rb')):
    record = json.loads(line)
    if ordinal < 549:continue
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
            for unused in range(4):
                try:
                    obj = json.loads(text)
                except (ValueError, TypeError):
                    break
                if isinstance(obj, dict) and obj.get('status') == 'fulfilled' and isinstance(obj.get('value'), dict):
                    obj = obj['value']
                    decoded_layers.append('public fulfilled/value result')
                if isinstance(obj, dict) and isinstance(obj.get('output'), str) and {'chunk_id', 'exit_code'}.issubset(obj):
                    text = obj['output']
                    decoded_layers.append('public exec result output')
                elif isinstance(obj, dict) and isinstance(obj.get('text'), str):
                    text = obj['text']
                    decoded_layers.append('public source text field')
                else:
                    break
            texts.append({'block_index': index, 'original_block_sha256': original_sha, 'decoded_layers': decoded_layers, 'text': text})
        outputs.append({'ordinal': ordinal, 'record_sha256': H(line), 'call_id': p.get('call_id'), 'texts': texts})

used, receipts = set(), []
for row in ledger['rows']:
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
                choices.append({'path': row['path'], 'range': [start, end], 'slice_sha256': row['slice_sha256'], 'event_ordinal': output['ordinal'], 'record_sha256': output['record_sha256'], 'public_block_index': block['block_index'], 'original_public_block_sha256': block['original_block_sha256'], 'losslessly_decoded_public_layers': block['decoded_layers'], 'associated_public_call': call})
    assert choices, (row['path'], start, end)
    chosen = choices[-1]
    used.add(chosen['event_ordinal'])
    receipts.append(chosen)

image_receipts = []
for view in visual['visuals']:
    path = ROOT / view['path']
    digest = H(path.read_bytes())
    assert digest == view['source_sha256']
    matches = [x for x in images if x['displayed_bytes_sha256'] == digest and x['detail']=='original']
    assert matches, (view['id'], view['path'], 'original image bytes absent from public deliveries')
    if view['kind'].startswith('original-core-panel-'):
        assert path.stat().st_size == 19419092 and view['dimensions'] == [2697, 1797]
    image_receipts.append({'id': view['id'], 'path': view['path'], 'source_sha256': digest, 'source_bytes': path.stat().st_size, 'dimensions': view['dimensions'], 'original_source_bytes_delivered_without_reencoding': True, 'public_image_deliveries': matches})

assert len(receipts) == 201 and len(used) == 201
assert len(image_receipts) == 46
proof = {'verified': True, 'candidate_sha256': ledger['candidate_sha256'], 'text_sources': len(ledger['complete_sources']), 'actual_distinct_text_range_deliveries': len(receipts), 'one_source_range_per_matched_output_event': True, 'text_deliveries': receipts, 'unique_visual_sources': len(image_receipts), 'public_image_blocks': len(images), 'visuals': image_receipts, 'no_private_runtime_bodies_copied': True, 'limitations': 'Only public custom-tool source text/image payloads and numeric public call caps are inspected; safe hashes and event references are retained. Exact delivered original source bytes prove recorded transport, not cognition or semantic correctness. This scans only public working-phase records with ordinal at least549. The six own earlier whole texts and eight earlier original images are separately bound to the immutable original-phase proof; they are not counted as new delivery. All201 recorded range rows, including each of twelve repeats, are matched to separate actual events. The earlier189-range proof still selects the last relied copy per unique range.'}
dest = B / 'working45-46-all-recorded-repeat-delivery-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps({'proof': str(dest), 'sha256': H(dest.read_bytes()), 'verified': True, 'text_sources': proof['text_sources'], 'text_ranges': len(receipts), 'visual_sources': len(image_receipts), 'public_image_blocks': len(images), 'private_runtime_bodies_copied': False}))
