"""Bind seven source-only native views to actual model-visible image outputs."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re

R = Path(__file__).parent
D = R / 'stamped-iteration-01'
proof = json.loads((R / 'runtime-provenance.json').read_text())
auditor = next(x for x in proof['agents'] if x['task'] == '/root/source_audit_stamped1')
runtime = Path(auditor['runtime_source_path'])
raw = runtime.read_bytes().splitlines()
calls = {}
images = []
report_mtime = (D / 'source-audit.json').stat().st_mtime
for ordinal, line in enumerate(raw):
    record = json.loads(line)
    item = record.get('payload', {})
    if record['type'] != 'response_item':
        continue
    if item.get('type') in ['function_call', 'custom_tool_call']:
        calls[item.get('call_id')] = (ordinal, item.get('arguments', item.get('input', '')))
    if item.get('type') not in ['function_call_output', 'custom_tool_call_output']:
        continue
    if not isinstance(item.get('output'), list):
        continue
    count = sum(isinstance(x, dict) and x.get('type') == 'input_image' for x in item['output'])
    if not count:
        continue
    call_ordinal, code = calls[item['call_id']]
    paths = re.findall(r'[\"\'](/home/[^\"\']+\.png)[\"\']', code)
    # This auditor used one literal const p and one view_image({path:p}) per call.
    assert count == len(paths) == 1
    assert re.search(r'const\s+p\s*=\s*"[^"\n]+\.png"\s*;', code)
    assert 'tools.view_image({path:p})' in code
    timestamp = record['timestamp']
    assert datetime.fromisoformat(timestamp.replace('Z', '+00:00')).timestamp() <= report_mtime
    path = Path(paths[0])
    images.append(dict(path=str(path), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                       actual_model_visible_image_count=count,
                       call_record_ordinal_zero_based=call_ordinal,
                       call_record_sha256=hashlib.sha256(raw[call_ordinal]).hexdigest(),
                       output_record_ordinal_zero_based=ordinal,
                       output_record_sha256=hashlib.sha256(line).hexdigest(),
                       output_timestamp=timestamp))
base = Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/lords-of-vegas').resolve()
expected = {str(base / f'original-rulebook-p{i}.png') for i in range(1, 5)}
expected |= {str(base / 'unified-2022' / f'physical-page-{i:02}.png') for i in [2, 5, 16]}
assert len(images) == 7 and {x['path'] for x in images} == expected
out = dict(verified=True, auditor_task=auditor['task'], auditor_identity=auditor['identity'],
           runtime_source_path=str(runtime), source_audit_sha256=hashlib.sha256((D / 'source-audit.json').read_bytes()).hexdigest(),
           image_count=7, all_expected_distinct_pages_seen=True, all_views_before_report_saved=True,
           images=images, hygiene='Only source paths, timestamps, identities and opaque record hashes retained; no runtime instructions/account metadata or image payloads copied.')
(D / 'native-delivery-proof.json').write_text(json.dumps(out, indent=2) + '\n')
print(dict(verified=True, image_count=7, all_expected_distinct_pages_seen=True))
