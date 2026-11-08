"""Verify source02 actual public delivery and its explicit localized own-reading reuse."""
import ast
import base64
import hashlib
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import fitz
from PIL import Image

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
G = ROOT / 'docs/quality/summary-qa/new-angeles' / B.name
A = G / 'current-text-source-auditor'
V = A / 'revision-02'
RT = Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/07/rollout-2026-11-07T00-35-38-01a1b4ef-3792-7613-a57c-63fc42e4c7e0.jsonl')
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_text())
resolve = lambda s: Path(s) if Path(s).is_absolute() else ROOT / s
audit, follow = load(A / 'source-audit.json'), load(V / 'source-audit.json')
old, new = A / 'snapshot-new-angeles.md', V / 'snapshot-new-angeles.md'
assert H(old) == audit['snapshot']['sha256']
assert H(new) == follow['snapshot']['sha256']
assert audit['result']['source_supported_text'] == 'FAIL'
assert follow['result']['source_supported_text'] == 'PASS'
assert follow['result']['complete_core_scope_readiness'] == 'NOT_READY'
assert follow['result']['unqualified_approval'] is False
assert H(A / 'source-audit.json') == follow['prior_audit']['sha256']
change = follow['complete_exact_diff']
assert old.read_text().count(change['old_text']) == 1
assert old.read_text().replace(change['old_text'], change['new_text']) == new.read_text()
assert H(V / change['file']) == change['sha256']
source_checks = []
for source in audit['sources']:
    p = old if source['path'] == 'rules/new-angeles.md' else resolve(source['path'])
    assert H(p) == source['sha256']
    source_checks.append({'declared_path': source['path'], 'checked_path': str(p), 'sha256': H(p)})

tree = ast.parse((B / 'check-spirit-source09-delivery.py').read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'strings')
ns = {'json': json}
exec(compile(ast.Module(body=[fn], type_ignores=[]), '<public-tool-strings>', 'exec'), ns)
lines = RT.read_bytes().splitlines(keepends=True)
outputs, delivered, contexts, terminals, calls = [], [], [], [], []
for n, line in enumerate(lines, 1):
    row = json.loads(line)
    p = row.get('payload', {})
    if row.get('type') == 'session_meta':
        assert p['id'] == '01a1b4ef-3792-7613-a57c-63fc42e4c7e0'
        assert p['parent_thread_id'] == '01a1b3fc-466c-7322-8413-9e59ff041286'
        assert p['agent_path'] == '/root/current_text_source_auditor'
    if row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if row.get('type') == 'event_msg' and p.get('type') == 'task_complete':
        terminals.append(n)
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ['function_call', 'custom_tool_call']:
        text = p.get('input', p.get('arguments', ''))
        assert not any(s in text for s in ['get_agent_info', 'list_agents', 'read_thread',
            'wait_threads', 'web__', 'search_query', 'answer-key.json', 'raw-cases.json',
            'reader-a.json', 'reader-b.json'])
        calls.append({'record': n, 'name': p.get('name'), 'sha256': HB(line)})
    elif p.get('type') in ['function_call_output', 'custom_tool_call_output']:
        outputs.append((n, list(ns['strings'](p.get('output')))))
        if isinstance(p.get('output'), list):
            for i, image in enumerate(p['output']):
                if not isinstance(image, dict) or image.get('type') != 'input_image':
                    continue
                url = image.get('image_url')
                url = url.get('url') if isinstance(url, dict) else url
                assert isinstance(url, str) and ';base64,' in url
                data = base64.b64decode(url.split(';base64,', 1)[1], validate=True)
                delivered.append({'record': n, 'block': i, 'sha256': HB(data),
                                  'detail': image.get('detail'), 'record_sha256': HB(line)})
assert contexts and all(c['model'] == 'gpt-6.1-sol' and c['effort'] == 'high' for c in contexts)
assert len(terminals) >= 2
first_end, final_end = min(terminals), max(terminals)

def check_receipts(receipts, phase):
    checked, coverage = [], defaultdict(list)
    for receipt in receipts:
        name = receipt['path']
        path = (old if phase == 'initial' else new) if name == 'rules/new-angeles.md' else resolve(name)
        text = path.read_text()
        assert H(path) == receipt['sha256'] and len(text) == receipt['total_chars']
        a, z = receipt['start_inclusive'], receipt['end_exclusive']
        part = text[a:z]
        assert 0 <= a < z <= len(text) and HB(part.encode()) == receipt['chunk_sha256']
        lower, upper = (0, first_end) if phase == 'initial' else (first_end, final_end)
        matches = [n for n, values in outputs if lower < n < upper and any(
            part in value or json.dumps(part, ensure_ascii=False)[1:-1] in value for value in values)]
        assert matches, (phase, name, a, z)
        coverage[name].append((a, z))
        checked.append({'path': str(path), 'start': a, 'end': z, 'sha256': HB(part.encode()),
                        'actual_output_records': [{'record': n, 'sha256': HB(lines[n-1])} for n in matches]})
    if phase == 'initial':
        for name, ranges in coverage.items():
            cursor = 0
            for a, z in sorted(ranges):
                assert a <= cursor
                cursor = max(cursor, z)
            path = old if name == 'rules/new-angeles.md' else resolve(name)
            assert cursor == len(path.read_text())
        assert len(coverage) == 6  # summary, three authorities, two source-provenance files
    return checked

initial_text = check_receipts(audit['text_inspection']['receipts'], 'initial')
follow_text = check_receipts(follow['followup_text_inspection']['receipts'], 'followup')
native = load(A / 'native-receipts.json')
assert H(A / 'native-receipts.json') == audit['native_inspection']['manifest_sha256']
groups, bound, documents, render_checks = defaultdict(list), [], {}, []
for receipt in native:
    source = resolve(receipt['source'])
    assert H(source) == receipt['source_sha256']
    is_crop = 'crop' in receipt
    image_path = resolve(receipt['crop'] if is_crop else receipt['render'])
    expected_hash = receipt['crop_sha256'] if is_crop else receipt['render_sha256']
    assert H(image_path) == expected_hash
    matches = [x for x in delivered if x['sha256'] == expected_hash and x['detail'] == 'original'
               and x['record'] < first_end]
    assert matches, image_path
    with Image.open(image_path) as image:
        pixels, dimensions = image.convert('RGB').tobytes(), list(image.size)
    if is_crop:
        with Image.open(source) as parent:
            assert parent.convert('RGB').crop(tuple(receipt['rect'])).tobytes() == pixels
            groups[str(source)].append((receipt['rect'], list(parent.size)))
    else:
        # Preserve the declared original page-render order and reuse each PDF
        # document, as in the auditor's rendering batch; glyph caches affect pixels.
        if str(source) not in documents:
            documents[str(source)] = fitz.open(source)
        doc = documents[str(source)]
        pix = doc[receipt['page_1based'] - 1].get_pixmap(matrix=fitz.Matrix(*receipt['matrix']))
        assert [pix.width, pix.height] == dimensions and pix.n == 3 and pix.samples == pixels, image_path
        render_checks.append({'source': str(source), 'page_1based': receipt['page_1based'],
                              'matrix': receipt['matrix'], 'pixels_match': True})
    bound.append({'path': str(image_path), 'sha256': expected_hash, 'dimensions': dimensions,
                  'actual_deliveries': matches, 'native_kind': 'source-pixel-equal crop' if is_crop else 'independently reproduced PDF render'})
for source, entries in groups.items():
    width, height = entries[0][1]
    breaks = sorted({0, height} | {v for rect, _ in entries for v in [rect[1], rect[3]]})
    for y0, y1 in zip(breaks, breaks[1:]):
        xs = sorted((r[0], r[2]) for r, _ in entries if r[1] <= y0 and r[3] >= y1)
        cursor = 0
        for x0, x1 in xs:
            assert x0 <= cursor
            cursor = max(cursor, x1)
        assert cursor == width
assert len(groups) == 16 and len(native) == 85 and len(render_checks) == 16
result = {'verified_delivery_only': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'source_auditor': '01a1b4ef-3792-7613-a57c-63fc42e4c7e0',
          'runtime_path': str(RT), 'runtime_sha256_at_check': H(RT), 'actual_contexts': contexts,
          'initial_report_path': str(A / 'source-audit.json'), 'initial_report_sha256': H(A / 'source-audit.json'),
          'followup_report_path': str(V / 'source-audit.json'), 'followup_report_sha256': H(V / 'source-audit.json'),
          'initial_snapshot_sha256': H(old), 'followup_snapshot_sha256': H(new),
          'canonical_body_matches_followup_at_check': (ROOT / 'rules/new-angeles.md').read_bytes() == new.read_bytes(),
          'sources': source_checks, 'initial_full_text_inputs': initial_text,
          'new_focused_followup_inputs': follow_text, 'whole_source_reuse_explicit': True,
          'native_original_images': bound, 'all16_original_atlas_pixels_covered': True,
          'independent_pdf_render_checks': render_checks, 'fitz_version': fitz.VersionBind,
          'initial_terminal_record': first_end, 'final_terminal_record': final_end,
          'public_tool_call_trace': calls,
          'limits': 'Source delivery and localized followup only, not final game acceptance. Original FAIL is preserved; source-supported-text PASS follows exactly one complete-file-proved hand-size substitution, eight new focused readings and explicit reuse of six whole old text inputs (summary, three authorities, two source-provenance files)/85 native images from the same initially fresh pure author. SG01 remains NOT_READY, no unqualified scope/publication/stamp approval. Actual complete frozen93 reader grading and future corrected-body full pair remain independent. Opaque spawn-message plaintext is not claimed available; original fresh/model request verified separately.'}
out = B / 'coordinator-checks/new-angeles-source02-original-and-localized-followup-delivery.json'
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified_delivery_only': True, 'whole_text_files': 6, 'initial_ranges': len(initial_text),
                  'new_focused_ranges': len(follow_text), 'native_images': len(bound),
                  'original_atlases': len(groups), 'pdf_renders': len(render_checks), 'report': str(out)}))
