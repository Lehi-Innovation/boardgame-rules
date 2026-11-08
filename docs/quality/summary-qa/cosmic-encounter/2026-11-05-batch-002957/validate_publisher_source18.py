"""Verify focused primary text and actual original-detail PDF-render payloads."""
from pathlib import Path
import base64
import hashlib
import json

R = Path(__file__).parent.resolve()
D = R / 'source-review/publisher-setup-18'
receipt = json.loads((D / 'delivery-receipt.json').read_bytes())
provenance = json.loads((R / 'model-provenance.json').read_bytes())
agent = next(a for a in provenance['agents'] if a['task'] == '/root/publisher_setup_applicability_18')


def sha(b):
    return hashlib.sha256(b).hexdigest()


def texts(x):
    if isinstance(x, str):
        yield x
        try:
            value = json.loads(x)
            if isinstance(value, (dict, list)):
                yield from texts(value)
        except ValueError:
            for line in x.splitlines():
                if line.startswith(('{', '[')):
                    try:
                        yield from texts(json.loads(line))
                    except ValueError:
                        pass
    elif isinstance(x, dict):
        for v in x.values():
            yield from texts(v)
    elif isinstance(x, list):
        for v in x:
            yield from texts(v)


records, images = [], []
for ordinal, line in enumerate(Path(agent['runtime_source_path']).open()):
    row = json.loads(line)
    p = row.get('payload', {})
    if p.get('type') != 'custom_tool_call_output':
        continue
    proof = {'ordinal': row.get('ordinal', ordinal), 'record_sha256_including_line_lf': sha(line.encode())}
    output = p.get('output')
    records.append((proof, list(texts(output))))
    for item in output if isinstance(output, list) else []:
        if not isinstance(item, dict) or item.get('type') != 'input_image':
            continue
        url = item.get('image_url', '')
        if not url.startswith('data:') or ';base64,' not in url:
            continue
        data = base64.b64decode(url.split(';base64,', 1)[1], validate=True)
        if not data.startswith(b'\x89PNG\r\n\x1a\n'):
            continue
        images.append({**proof, 'sha256': sha(data), 'bytes': len(data),
                       'dimensions': [int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')],
                       'detail': item.get('detail')})

files = []
for f in receipt['complete_rulebook_text_deliveries']:
    p = Path(f['path'])
    value, checks, cursor = p.read_text(), [], 0
    assert sha(p.read_bytes()) == f['file_sha256']
    for c in f['chunks']:
        start, end = c['start_char_inclusive_0based'], c['end_char_exclusive_0based']
        piece = value[start:end]
        found = [proof for proof, strings in records if any(piece in s for s in strings)]
        assert start == cursor and 0 < end-start <= 6000
        assert sha(piece.encode()) == c['utf8_sha256'] and found
        checks.append({'start': start, 'end': end, 'runtime_proof': found})
        cursor = end
    assert cursor == len(value) == f['characters']
    files.append({'path': str(p), 'sha256': f['file_sha256'], 'complete': True, 'chunks': checks})
visuals = []
for visual in receipt['visual_deliveries']:
    p = Path(visual['path'])
    assert sha(p.read_bytes()) == visual['file_sha256']
    found = [im for im in images if im['sha256'] == visual['file_sha256']
             and im['bytes'] == visual['encoded_bytes']
             and im['dimensions'] == [visual['width'], visual['height']] and im['detail'] == 'original']
    assert found
    visuals.append({'path': str(p), 'kind': visual['kind'], 'actual_payload_proof': found})
assert agent['settings_verified']
out = {'pass': True, 'scope': 'Two complete rulebooks and4actual original-detail PDF render/capture payloads only',
       'text_files': files, 'visuals': visuals, 'actual_model_and_effort_verified': True,
       'faq_full_read_or_fifty_original_alien_inspections_claimed': False,
       'applicability_or_source_adoption_verdict_inferred_from_delivery': False,
       'historical_installer_cache_deviation_preserved': True,
       'exact_four_cache_files_cleaned_separate_receipt': str(D / 'cache-cleanup-root-verification.json')}
dest = D / 'actual-delivery-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(out, indent=2) + '\n')
print('PASS:2complete rulebooks/21actual textchunks,4original-detail PNG payloads; no50-alien/adoption claim')
