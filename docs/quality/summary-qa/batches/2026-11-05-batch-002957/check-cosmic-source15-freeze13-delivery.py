"""Check cumulative own-source delivery and exact freeze13 rereading, not scope approval."""
import ast
import base64
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image
from pypdf import PdfReader
import pypdf

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
G = ROOT / 'docs/quality/summary-qa/cosmic-encounter' / B.name
A = G / 'source-review'
RT = Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/06/rollout-2026-11-06T22-38-45-01a1b484-32a9-7370-b67f-9ec0c9f64f9f.jsonl')
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_text())
audit = load(A / 'source-only-audit-15-freeze13.json')
initial = load(A / 'source-only-delivery-15.json')
assert audit['source_verdict'] == 'PASS' and len(audit['unresolved_sources']) == 2
assert not audit['demonstrated_errors'] and not audit['omissions'] and not audit['new_findings']
assert not audit['continuation_and_isolation']['fresh_independent_vote']
summary = Path(audit['summary']['path'])
assert H(summary) == audit['summary']['sha256']
assert H(Path(audit['source_census']['original_receipt_ledger']['path'])) == audit['source_census']['original_receipt_ledger']['sha256']
tree = ast.parse((B / 'check-spirit-source09-delivery.py').read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'strings')
ns = {'json': json}
exec(compile(ast.Module(body=[fn], type_ignores=[]), '<public-tool-strings>', 'exec'), ns)
lines = RT.read_bytes().splitlines(keepends=True)
outputs, images, contexts, terminals, calls = [], [], [], [], []
for n, line in enumerate(lines, 1):
    row = json.loads(line)
    p = row.get('payload', {})
    if row.get('type') == 'session_meta':
        assert p['id'] == '01a1b484-32a9-7370-b67f-9ec0c9f64f9f'
        assert p['parent_thread_id'] == '01a1b3c7-0daa-70f1-9158-0e75d24cbb22'
        assert p['agent_path'] == '/root/source_only_auditor_15'
    if row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if row.get('type') == 'event_msg' and p.get('type') == 'task_complete':
        terminals.append(n)
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ['function_call', 'custom_tool_call']:
        text = p.get('input', p.get('arguments', ''))
        assert not any(x in text for x in ['get_agent_info', 'list_agents', 'read_thread',
            'wait_threads', 'web__', 'search_query', 'questions.json', 'answer-key.json',
            'reader-a.json', 'reader-b.json', 'actual-question-scope.json'])
        calls.append({'record': n, 'name': p.get('name'), 'sha256': HB(line)})
    elif p.get('type') in ['function_call_output', 'custom_tool_call_output']:
        outputs.append((n, list(ns['strings'](p.get('output')))))
        if isinstance(p.get('output'), list):
            for i, image in enumerate(p['output']):
                if not isinstance(image, dict) or image.get('type') != 'input_image':
                    continue
                url = image.get('image_url')
                url = url.get('url') if isinstance(url, dict) else url
                data = base64.b64decode(url.split(';base64,', 1)[1], validate=True)
                images.append({'record': n, 'block': i, 'sha256': HB(data),
                               'detail': image.get('detail'), 'record_sha256': HB(line)})
assert contexts and all(c['model'] == 'gpt-6.1-sol' and c['effort'] == 'high' for c in contexts)
assert len(terminals) >= 2
end, previous_end = terminals[-1], terminals[-2]

def matches(part, lower=0):
    result = [n for n, values in outputs if lower < n < end and any(
        part in value or json.dumps(part, ensure_ascii=False)[1:-1] in value for value in values)]
    assert result
    return [{'record': n, 'sha256': HB(lines[n-1])} for n in result]

texts = []
for name, current in [('normalized-source-only-delivery-15.json', False),
                      ('normalized-source-only-delivery-15-freeze13.json', True)]:
    for receipt in load(A / name)['text_receipts']:
        path = Path(receipt['path'])
        assert H(path) == receipt['sha256']
        text, cursor, parts = path.read_text(), 0, []
        for chunk in receipt['chunks']:
            a, z = chunk['start'], chunk['end_exclusive']
            assert a == cursor and a < z <= len(text)
            assert HB(text[a:z].encode()) == chunk['sha256_utf8']
            parts.append({'start': a, 'end': z, 'sha256': chunk['sha256_utf8'],
                          'actual_output_records': matches(text[a:z], previous_end if current else 0)})
            cursor = z
        assert cursor == len(text)
        texts.append({'path': str(path), 'sha256': H(path), 'fresh_freeze13_read': current,
                      'parts': parts})
assert len(texts) == 6
bound_images = []
assert len(initial['images']) == 50 and len({x['path'] for x in initial['images']}) == 50
for receipt in initial['images']:
    path = Path(receipt['path'])
    digest = H(path)
    assert digest == receipt['returned_decoded_sha256'] == receipt['manifest_sha256']
    assert path.stat().st_size == receipt['manifest_bytes'] == receipt['returned_decoded_bytes']
    with Image.open(path) as image:
        assert list(image.size) == receipt['manifest_dimensions'] == receipt['returned_dimensions']
    found = [x for x in images if x['sha256'] == digest and x['detail'] == 'original' and x['record'] < end]
    assert found, path
    bound_images.append({'alien': receipt['alien'], 'path': str(path), 'sha256': digest,
                         'dimensions': receipt['manifest_dimensions'], 'actual_deliveries': found})
pdf_checks = []
for receipt in initial['native_pdfs']:
    path = Path(receipt['path'])
    assert H(path) == receipt['sha256']
    pdf = PdfReader(path)
    assert len(pdf.pages) == receipt['pages']
    for page in receipt['native_text_deliveries']:
        text = pdf.pages[page['printed_page'] - 1].extract_text()
        assert len(text) == page['chars'] and HB(text.encode()) == page['sha256']
        cursor, parts = 0, []
        for chunk in page['chunks']:
            a, z = chunk['start'], chunk['end']
            assert a == cursor and a < z <= len(text)
            assert HB(text[a:z].encode()) == chunk['chunk_sha256']
            parts.append({'start': a, 'end': z, 'actual_output_records': matches(text[a:z])})
            cursor = z
        assert cursor == len(text)
        pdf_checks.append({'path': str(path), 'pdf_sha256': H(path), 'printed_page': page['printed_page'],
                           'native_text_sha256': page['sha256'], 'parts': parts})
    assert not receipt['raster_pages_inspected']
result = {'verified_delivery_only': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'source_auditor': '01a1b484-32a9-7370-b67f-9ec0c9f64f9f', 'runtime': str(RT),
          'runtime_sha256_at_check': H(RT), 'contexts': contexts,
          'audit_path': str(A / 'source-only-audit-15-freeze13.json'),
          'audit_sha256': H(A / 'source-only-audit-15-freeze13.json'), 'summary_sha256': H(summary),
          'full_text_inputs': texts, 'original_native_alien_images': bound_images,
          'independently_reproduced_native_pdf_text_views': pdf_checks, 'pypdf_version': pypdf.__version__,
          'previous_completion_record': previous_end, 'current_completion_record': end,
          'public_tool_call_trace': calls, 'unresolved_authority_gaps': audit['unresolved_sources'],
          'canonical_body_matches_at_check': summary.read_bytes() == (ROOT / 'rules/cosmic-encounter.md').read_bytes(),
          'limits': 'Cumulative own-source receipt union, all50 original-detail JPEG deliveries and five selected native-PDF text views verified against actual original public payloads and current source bytes. New complete freeze13 body rereading is verified after the previous completed continuation. Initially fresh pure auditor explicitly reuses its own whole authorities and native-sheet reading; no new independent vote or new50-image inspection claimed. Native PDF text is pypdf output, not Fitz output or a raster-image inspection. Historical FAQ exists as complete cached publisher text, not a verified original PDF. Source accuracy PASS has two essential authority gaps (alien reveal; reinforcement/negotiate), so no unqualified complete-core, reader, stamp or publication approval.'}
out = B / 'coordinator-checks/cosmic-source15-freeze13-actual-delivery.json'
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified_delivery_only': True, 'whole_text_files': len(texts),
                  'text_parts': sum(len(x['parts']) for x in texts), 'original_images': len(bound_images),
                  'native_pdf_text_views': len(pdf_checks), 'report': str(out)}))
