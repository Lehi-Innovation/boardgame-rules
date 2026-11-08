"""Verify revision04 focused source reading/native refresh and exact complete-file delta."""
import ast
import difflib
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
A = ROOT / 'docs/quality/summary-qa/new-angeles' / B.name / 'current-text-source-auditor'
V = A / 'revision-04'
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
resolve = lambda s: Path(s) if Path(s).is_absolute() else ROOT / s
prior_path = B / 'coordinator-checks/new-angeles-source02-original-and-localized-followup-delivery.json'
prior = load(prior_path)
audit_path = V / 'source-audit.json'
audit = load(audit_path)
assert audit['result']['source_supported_text'] == 'PASS'
assert audit['result']['complete_core_scope_readiness'] == 'NOT_READY'
assert audit['result']['essential_scope_limit'] == 'SG01'
assert not audit['result']['unqualified_approval']
for previous in audit['prior_audits_preserved']:
    assert H(resolve(previous['path'])) == previous['sha256']
old, new = A / 'revision-03/snapshot-new-angeles.md', V / 'snapshot-new-angeles.md'
delta = audit['complete_exact_diff']
assert H(old) == delta['old_sha256'] and H(new) == delta['new_sha256'] == audit['snapshot']['sha256']
assert H(V / delta['own_diff']) == delta['own_diff_sha256']
old_lines, new_lines = old.read_text().splitlines(keepends=True), new.read_text().splitlines(keepends=True)
old_offsets, new_offsets = [0], [0]
for line in old_lines:
    old_offsets.append(old_offsets[-1] + len(line))
for line in new_lines:
    new_offsets.append(new_offsets[-1] + len(line))
changes = [x for x in difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False).get_opcodes() if x[0] != 'equal']
assert len(changes) == len(delta['change_groups']) == 3
for (tag, a0, a1, b0, b1), group in zip(changes, delta['change_groups']):
    assert tag == group['operation']
    assert [old_offsets[a0], old_offsets[a1]] == group['old_unicode_range']
    assert [new_offsets[b0], new_offsets[b1]] == group['new_unicode_range']
runtime = Path(prior['runtime_path'])
lines = runtime.read_bytes().splitlines(keepends=True)
old_records = []
for f in prior['initial_full_text_inputs'] + prior['new_focused_followup_inputs']:
    old_records.extend(f['actual_output_records'])
for f in prior['native_original_images']:
    old_records.extend({'record': x['record'], 'sha256': x['record_sha256']} for x in f['actual_deliveries'])
for record in old_records:
    assert HB(lines[record['record'] - 1]) == record['sha256']
for source in prior['sources']:
    assert H(Path(source['checked_path'])) == source['sha256']
old_images = {x['path']: x for x in prior['native_original_images']}
for path, image in old_images.items():
    assert H(Path(path)) == image['sha256']
tree = ast.parse((B / 'check-spirit-source09-delivery.py').read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'strings')
ns = {'json': json}
exec(compile(ast.Module(body=[fn], type_ignores=[]), '<public-tool-strings>', 'exec'), ns)
previous03_path = B / 'coordinator-checks/new-angeles-source02-revision03-actual-addendum.json'
previous03 = load(previous03_path)
for f in previous03['new_focused_text_ranges']:
    for record in f['actual_records']:
        assert HB(lines[record['record']-1]) == record['sha256']
for f in previous03['new_original_native_refreshes']:
    for record in f['new_actual_original_deliveries']:
        assert HB(lines[record['record']-1]) == record['record_sha256']
lower = previous03['current_completion_record']
outputs, deliveries, contexts, terminals, calls = [], [], [], [], []
for n, line in enumerate(lines, 1):
    row = json.loads(line)
    p = row.get('payload', {})
    if row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if n <= lower:
        continue
    if row.get('type') == 'event_msg' and p.get('type') == 'task_complete':
        terminals.append(n)
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ['function_call', 'custom_tool_call']:
        text = p.get('input', p.get('arguments', ''))
        assert not re.search(r'(?:get_agent_info|list_agents|read_thread|wait_threads|web__run)\s*\(', text)
        assert not any(s in text for s in ['questions.json', 'answer-key.json', 'asked-clause-map.json',
            'reader-a.json', 'reader-b.json', 'fresh-borderline-adjudication.json'])
        calls.append({'record': n, 'name': p.get('name'), 'sha256': HB(line)})
    elif p.get('type') in ['function_call_output', 'custom_tool_call_output']:
        outputs.append((n, list(ns['strings'](p.get('output')))))
        if isinstance(p.get('output'), list):
            import base64
            for i, image in enumerate(p['output']):
                if not isinstance(image, dict) or image.get('type') != 'input_image':
                    continue
                url = image.get('image_url')
                url = url.get('url') if isinstance(url, dict) else url
                payload = base64.b64decode(url.split(';base64,', 1)[1], validate=True)
                deliveries.append({'record': n, 'block': i, 'sha256': HB(payload),
                                   'detail': image.get('detail'), 'record_sha256': HB(line)})
assert contexts and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in contexts)
assert terminals
upper = max(terminals)
texts, covered_new_body = [], []
for receipt in audit['new_focused_text_reading']['receipts']:
    path = new if receipt['path'] == 'rules/new-angeles.md' else resolve(receipt['path'])
    text = path.read_text()
    assert H(path) == receipt['sha256'] and len(text) == receipt['total_chars']
    a, z = receipt['start_inclusive'], receipt['end_exclusive']
    part = text[a:z]
    assert 0 <= a < z <= len(text) and HB(part.encode()) == receipt['chunk_sha256']
    matches = [n for n, values in outputs if n < upper and any(
        part in value or json.dumps(part, ensure_ascii=False)[1:-1] in value for value in values)]
    assert matches
    texts.append({'path': str(path), 'start': a, 'end': z, 'sha256': receipt['chunk_sha256'],
                  'actual_records': [{'record': n, 'sha256': HB(lines[n-1])} for n in matches]})
    if path == new:
        covered_new_body.append((a, z))
for _, _, _, b0, b1 in changes:
    start, end = new_offsets[b0], new_offsets[b1]
    assert any(a <= start and z >= end for a, z in covered_new_body)
native = []
import fitz
from PIL import Image
import io
assert H(V / audit['new_focused_native_reading']['manifest']) == audit['new_focused_native_reading']['manifest_sha256']
for receipt in load(V / audit['new_focused_native_reading']['manifest']):
    path = resolve(receipt.get('crop', receipt.get('render')))
    digest = receipt.get('crop_sha256', receipt.get('render_sha256'))
    assert H(path) == digest
    if str(path) in old_images:
        original = old_images[str(path)]
        assert digest == original['sha256']
        lineage = {'kind':'previously verified exact native image','prior_native_kind':original['native_kind']}
    else:
        source = resolve(receipt['source']); assert H(source) == receipt['source_sha256']
        with fitz.open(source) as doc:
            pix = doc[receipt['page_1based']-1].get_pixmap(matrix=fitz.Matrix(*receipt['matrix']))
            reproduced = pix.tobytes('png')
        assert HB(reproduced) == digest
        with Image.open(io.BytesIO(reproduced)) as image:
            dimensions = list(image.size)
        lineage = {'kind':'new PDF native page independently reproduced','source':str(source),'source_sha256':H(source),'page_1based':receipt['page_1based'],'matrix':receipt['matrix'],'dimensions':dimensions,'independently_reproduced_png_sha256':HB(reproduced)}
    matches = [x for x in deliveries if x['record'] < upper and x['sha256'] == digest and x['detail'] == 'original']
    assert matches
    native.append({'path':str(path),'sha256':digest,'lineage':lineage,'new_actual_original_deliveries':matches})
assert len(native) == 5
result = {'verified_delivery_only': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'auditor': prior['source_auditor'], 'runtime': str(runtime), 'runtime_sha256_at_check': H(runtime),
          'all_current_contexts': contexts, 'prior_revision03_proof': str(previous03_path), 'prior_revision03_proof_sha256':H(previous03_path), 'prior_verified_source_union': str(prior_path),
          'prior_verified_source_union_sha256': H(prior_path), 'old_actual_records_rechecked': len(old_records),
          'all_old_source_and85_native_hashes_current': True, 'current_snapshot_sha256': H(new),
          'exact_change_groups_independently_reproduced': len(changes), 'changed_text_covered_in_new_readings': True,
          'new_focused_text_ranges': texts, 'new_original_native_refreshes': native,
          'prior_completion_record': lower, 'current_completion_record': upper, 'new_public_call_trace': calls,
          'audit_path': str(audit_path), 'audit_sha256': H(audit_path),
          'limits': 'Same initially fresh pure02 own-source continuation. Initial complete corpus and original85 native lineage, revision02 and revision03 evidence reused honestly, exact historical records rechecked. Three changed groups covered by14 new focused ranges and five actual original-detail images: three reused original images plus two newly independently reproduced RR pages. Accuracy PASS exact930 only; SG01 still NOT_READY and four source limits remain. No human interpretation, new fresh vote, full-core, reader score, publication or stamp approval.'}
out = B / 'coordinator-checks/new-angeles-source02-revision04-actual-addendum.json'
assert not out.exists()
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified_delivery_only': True, 'changed_groups': len(changes), 'new_text_ranges': len(texts),
                  'new_original_image_refreshes': len(native), 'old_actual_records_rechecked': len(old_records), 'proof': str(out)}))
