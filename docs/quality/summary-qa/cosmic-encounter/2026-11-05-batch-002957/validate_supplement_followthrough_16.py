"""Check new audit/challenge payloads and reversible selected source records."""
from pathlib import Path
import base64
import hashlib
import json
import subprocess

R = Path(__file__).parent.resolve()
prov = json.loads((R / 'model-provenance.json').read_bytes())


def sha(b):
    return hashlib.sha256(b).hexdigest()


def texts(x):
    if isinstance(x, str):
        yield x
        try:
            y = json.loads(x)
            if isinstance(y, (dict, list)):
                yield from texts(y)
        except ValueError:
            for line in x.splitlines():
                if line.startswith(('{', '[')):
                    try:
                        yield from texts(json.loads(line))
                    except ValueError:
                        pass
    elif isinstance(x, dict):
        for y in x.values():
            yield from texts(y)
    elif isinstance(x, list):
        for y in x:
            yield from texts(y)


def runtime(task):
    agent = next(a for a in prov['agents'] if a['task'] == task)
    assert agent['settings_verified']
    records, images = [], []
    for index, line in enumerate(Path(agent['runtime_source_path']).open()):
        row = json.loads(line)
        p = row.get('payload', {})
        if p.get('type') != 'custom_tool_call_output':
            continue
        proof = {'ordinal': row.get('ordinal', index), 'record_sha256_including_lf': sha(line.encode())}
        output = p.get('output')
        records.append((proof, list(texts(output))))
        for im in output if isinstance(output, list) else []:
            if not isinstance(im, dict) or im.get('type') != 'input_image':
                continue
            url = im.get('image_url', '')
            if not url.startswith('data:') or ';base64,' not in url:
                continue
            data = base64.b64decode(url.split(';base64,', 1)[1], validate=True)
            if data.startswith(b'\x89PNG\r\n\x1a\n'):
                images.append({**proof, 'sha256': sha(data), 'bytes': len(data),
                               'dimensions': [int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')],
                               'detail': im.get('detail')})
    return agent, records, images


def visible(piece, records):
    found = [p for p, strings in records if any(piece in s for s in strings)]
    assert found
    return found


def image_proof(path, images):
    data = path.read_bytes()
    dimensions = [int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')]
    found = [i for i in images if i['sha256'] == sha(data) and i['bytes'] == len(data)
             and i['dimensions'] == dimensions and i['detail'] == 'original']
    assert found
    return {'path': str(path), 'sha256': sha(data), 'bytes': len(data),
            'dimensions': dimensions, 'actual_original_detail_payloads': found}


scope = json.loads((R / 'source-review/source-scope-16.json').read_bytes())
for path, pin in scope['pins'].items():
    p = Path(path)
    assert sha(p.read_bytes()) == pin['sha256'] and p.stat().st_size == pin['bytes']
image_path = Path(scope['supplement']['native_page_capture_path'])
agent, records, images = runtime('/root/source_only_auditor_15')
receipt = json.loads((R / 'source-review/source-only-delivery-15-freeze16.json').read_bytes())
assert json.loads((R / 'source-review/source15-freeze16-runtime-delivery-validation-01.json').read_bytes())['pass']
page = receipt['new_native_pdf_text_delivery']
native = subprocess.check_output([
    str(R.parents[4] / '.venv/bin/python'), '-c',
    'import fitz,sys;d=fitz.open(sys.argv[1]);sys.stdout.write(d[int(sys.argv[2])-1].get_text())',
    page['path'], str(page['printed_page'])]).decode()
assert len(native) == page['chars'] and sha(native.encode()) == page['sha256']
source_proof = {'pass': True, 'task': agent['task'], 'identity': agent['identity'],
                'new_full_text_input_proof': str(R / 'source-review/source15-freeze16-runtime-delivery-validation-01.json'),
                'native_pdf_p16_text': {'extractor': 'PyMuPDF/Fitz in existing workspace venv',
                                        'sha256': page['sha256'], 'actual_visible_proof': visible(native, records)},
                'native_p16_png': image_proof(image_path, images),
                'all_active_scope_pins_match': True,
                'own_original_source_and_fifty_native_reuse': 'Explicit own completed readings; no new50-image inspection or independent vote.',
                'original_full_source_native_proof': str(R / 'source-review/source15-runtime-delivery-validation-01.json'),
                'original_pins_integrity': str(R / 'validation-in-progress-11.json'),
                'source_adoption_or_publication_approval_inferred_from_delivery': False}
assert json.loads((R / 'source-review/source15-runtime-delivery-validation-01.json').read_bytes())['pass']
p = R / 'source-review/source15-freeze16-full-new-input-reuse-validation.json'
assert not p.exists()
p.write_text(json.dumps(source_proof, indent=2) + '\n')

agent, records, images = runtime('/root/supplement_source_coverage_20')
D = R / 'source-review/supplement-coverage-20'
receipt = json.loads((D / 'delivery-receipt.json').read_bytes())
full = []
for f in receipt['complete_inputs_actually_delivered'].values():
    p = Path(f['path'])
    value = p.read_text()
    assert sha(p.read_bytes()) == f['sha256']
    cursor, checks = 0, []
    for c in f['chunks']:
        start, end = c['start'], c['end']
        piece = value[start:end]
        assert start == cursor and 0 < end-start <= 6000
        assert sha(piece.encode()) == c['utf8_sha256']
        checks.append({'start': start, 'end': end, 'actual_visible_proof': visible(piece, records)})
        cursor = end
    assert cursor == len(value) == f['chars']
    full.append({'path': str(p), 'complete': True, 'chunks': checks})
selected = []
for f in receipt['selected_complete_record_deliveries']:
    value = json.loads(Path(f['source_path']).read_bytes())
    for part in f['pointer'].split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    assert value['id'] == f['id'] and sha(canonical.encode()) == f['canonical_sha256']
    assert len(canonical) == f['canonical_chars']
    cursor, checks = 0, []
    for c in f['chunks']:
        start, end = c['start'], c['end']
        piece = canonical[start:end]
        assert start == cursor and 0 < end-start <= 6000
        assert sha(piece.encode()) == c['utf8_sha256']
        checks.append({'start': start, 'end': end, 'actual_visible_proof': visible(piece, records)})
        cursor = end
    assert cursor == len(canonical)
    selected.append({'source_path': f['source_path'], 'pointer': f['pointer'],
                     'canonical_sha256': f['canonical_sha256'], 'all_record_fields_retained': True, 'chunks': checks})
policy = receipt['source_scope_delivery']
policy_value = Path(policy['path']).read_text()
assert policy['full_visible_delivery'] and policy['chunks'] == 1 and len(policy_value) <= 6000
assert sha(policy_value.encode()) == policy['sha256']
out = {'pass': True, 'task': agent['task'], 'identity': agent['identity'], 'full_text_inputs': full,
       'selected_complete_records': selected, 'selected_records_not_called_whole_files': True,
       'normative_policy_actual_full_display': visible(policy_value, records),
       'native_p16_png': image_proof(image_path, images),
       'no_new_full_original_corpus_or_fifty_alien_inspection_claim': True,
       'no_coverage_or_publication_verdict_inferred_from_delivery': True}
dest = D / 'actual-delivery-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(out, indent=2) + '\n')
print('PASS:source15 new24textchunks/nativep16/ownreuse; fresh20 full29chunks/6exact selectedrecords/nativep16')
