"""Bind Sidereal's pure source audit to actual complete text and image delivery."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess
from PIL import Image

B = Path(__file__).resolve().parent
REPO = B.parents[4]
R = REPO / 'docs/quality/summary-qa/sidereal-confluence' / B.name
AUDITOR = '01a1b131-aa7d-7053-ac4a-46c2ba1c144b'
PARENT = '01a1b0b3-0030-70b2-8947-7a940fdf364f'
H = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_text())
audit_path = R / 'source-audit-02/source-audit.json'
audit = load(audit_path)
assert audit['verdict'] == 'PASS' and not audit['findings'] and not audit['unresolved_consequential_source_gaps']
summary = Path(audit['summary']['path'])
assert H(summary.read_bytes()) == audit['summary']['sha256']
assert summary.read_bytes() == (REPO / 'rules/sidereal-confluence.md').read_bytes()
manifest_path = Path(audit['manifest']['path'])
assert H(manifest_path.read_bytes()) == audit['manifest']['sha256']
manifest = load(manifest_path)
for entry in manifest['sources']:
    p = Path(entry['path'])
    assert H(p.read_bytes()) == entry['sha256'] and p.stat().st_size == entry['bytes']
actor = next(x for x in load(R / 'runtime-provenance.json')['records'] if x['identity'] == AUDITOR)
runtime = Path(actor['runtime_source_path'])
records = [json.loads(line) for line in runtime.read_text().splitlines()]
contexts, chunks, images, calls, writes, metadata = [], {}, [], [], [], None
for n, row in enumerate(records, 1):
    p = row.get('payload', {})
    if row.get('type') == 'session_meta':
        metadata = {k: p.get(k) for k in ('id', 'agent_path', 'parent_thread_id')}
    elif row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ('custom_tool_call', 'function_call'):
        text = p.get('input', p.get('arguments', ''))
        assert isinstance(text, str)
        assert not any(name in text for name in ('questions.json', 'answer-key.json', 'scope-map.json',
            'reader-a.json', 'reader-b.json', 'results.json', 'source-audit-01/', 'designer-2017-final-turn-addendum.md'))
        calls.append({'record': n, 'call_id': p['call_id'], 'input_sha256': H(text.encode()),
                      'nested_tool_names': sorted(set(re.findall(r'tools\.([\w]+)', text)))})
        if 'source-audit.json' in text and any(word in text for word in ('write_text', 'writeFile', 'apply_patch')):
            writes.append(n)
    elif p.get('type') in ('custom_tool_call_output', 'function_call_output'):
        for block in p.get('output', []):
            if not isinstance(block, dict):
                continue
            if block.get('type') == 'input_image':
                images.append({'record': n, 'call_id': p['call_id']})
            if block.get('type') == 'input_text':
                try:
                    v = json.loads(block.get('text', ''))
                except ValueError:
                    continue
                if isinstance(v, dict) and 'chunk_id' in v:
                    chunks[v['chunk_id']] = (n, v)
assert metadata == {'id': AUDITOR, 'agent_path': '/root/pure_source_auditor_02', 'parent_thread_id': PARENT}
assert contexts and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in contexts)
assert writes
first_write = min(writes)
receipts = []
for entry in audit['text_delivery_receipts']:
    path = Path(entry['path'])
    assert H(path.read_bytes()) == entry['sha256'] and path.stat().st_size == entry['bytes']
    text = path.read_text()
    assert len(text) == entry['characters']
    assert len(entry['ranges_half_open']) == len(entry['tool_exec_chunk_ids'])
    cursor, slices = 0, []
    for (a, z), chunk_id in zip(entry['ranges_half_open'], entry['tool_exec_chunk_ids']):
        assert a == cursor and a < z <= len(text)
        ordinal, output = chunks[chunk_id]
        assert ordinal < first_write and output['exit_code'] == 0
        assert text[a:z] in output['output']
        assert 'truncated' not in output['output'].lower() or text[a:z].lower().count('truncated') == output['output'].lower().count('truncated')
        slices.append({'start': a, 'end': z, 'actual_output_record': ordinal, 'chunk_id': chunk_id,
                       'literal_slice_sha256': H(text[a:z].encode())})
        cursor = z
    assert cursor == len(text)
    receipts.append({'path': str(path), 'sha256': entry['sha256'], 'complete': True, 'slices': slices})
images_before = [x for x in images if x['record'] < first_write]
assert len(images_before) == 35
assert audit['image_delivery_receipts']['pdf']['directly_viewed_pages'] == list(range(1, 11))
assert len(audit['image_delivery_receipts']['component_images']['paths']) == 25
crop_checks = []
for relative in manifest['accepted_recovered_component_provenance']:
    doc = load(R / relative)
    entries = doc if isinstance(doc, list) else [doc]
    for entry in entries:
        if not isinstance(entry, dict) or not any(k in entry for k in ('bounds_pixels', 'bounds')) or not any(k in entry for k in ('parent_file', 'parent')):
            continue
        parent, crop = Path(entry.get('parent_file', entry.get('parent'))), Path(entry.get('file', entry.get('path', '')))
        assert H(parent.read_bytes()) == entry['parent_sha256']
        if 'sha256' in entry:
            assert H(crop.read_bytes()) == entry['sha256']
        pixels = Image.open(parent).crop(entry.get('bounds_pixels', entry.get('bounds')))
        angle = entry.get('rotation_degrees_counterclockwise', 0)
        if angle:
            pixels = pixels.rotate(angle, expand=True)
        native = Image.open(crop)
        assert pixels.size == native.size and pixels.convert('RGB').tobytes() == native.convert('RGB').tobytes()
        crop_checks.append({'path': str(crop), 'exact_native_parent_pixels': True})
paths = subprocess.run(['rg', '--files', '/mnt/c/Users/jonny/.codex/sessions'], capture_output=True, text=True, check=True).stdout.splitlines()
parent_paths = [Path(p) for p in paths if p.endswith(PARENT + '.jsonl')]
assert len(parent_paths) == 1
spawns = []
for n, line in enumerate(parent_paths[0].open(), 1):
    row = json.loads(line); p = row.get('payload', {})
    if row.get('type') == 'response_item' and p.get('type') == 'function_call' and p.get('name', '').endswith('spawn_agent'):
        args = p.get('arguments'); args = json.loads(args) if isinstance(args, str) else args
        if args.get('task_name') == 'pure_source_auditor_02':
            spawns.append({'record': n, **{k: args.get(k) for k in ('task_name', 'model', 'reasoning_effort', 'fork_turns')}})
assert len(spawns) == 1 and spawns[0]['model'] == 'gpt-6.1-sol' and spawns[0]['reasoning_effort'] == 'high' and spawns[0]['fork_turns'] == 'none'
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'audit_path': str(audit_path), 'audit_sha256': H(audit_path.read_bytes()),
          'summary_sha256': H(summary.read_bytes()), 'auditor_id': AUDITOR, 'actual_metadata': metadata,
          'actual_contexts': contexts, 'actual_initial_spawn': spawns[0],
          'runtime_path': str(runtime), 'runtime_sha256_at_check': H(runtime.read_bytes()),
          'first_report_write_record': first_write, 'text_receipts': receipts,
          'actual_native_image_outputs_before_report': images_before, 'native_crop_lineage': crop_checks,
          'source_hash_bindings': len(manifest['sources']), 'tool_call_hash_projection': calls,
          'limits': 'Actual text slices and native-output count verified before report writing. Semantic source verdict remains the independent auditor conclusion. Filename trace check is not a general sandbox proof. No private context body copied.'}
out = B / 'coordinator-checks/sidereal-source-audit-02-actual-delivery-v2.json'
assert not out.exists()
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'text_files': len(receipts), 'slices': sum(len(x['slices']) for x in receipts),
                  'native_images': len(images_before), 'native_crop_checks': len(crop_checks), 'report': str(out)}))
