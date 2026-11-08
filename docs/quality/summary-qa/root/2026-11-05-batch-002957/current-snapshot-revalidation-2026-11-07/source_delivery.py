"""Actual current auditor source delivery, including native render lineage."""
from evidence import *
import base64
import fitz

def main():
    audit = N / 'source-only-audit/source-audit.json'
    assert audit.exists(), 'Require completed original independent audit'
    json.loads(audit.read_text())
    out = N / (sys.argv[1] if len(sys.argv) > 1 else 'source-delivery-final')
    spec = importlib.util.spec_from_file_location('source_helper', R / 'audit_full_publisher_delivery.py')
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    rec = next(x for x in runtime()['records'] if x['agent_path'] == '/root/current18_pure_source_auditor')
    blocks, calls, images = h.collect(Path(rec['runtime_path']), out)
    b = ROOT / 'docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/root'
    pdf = ROOT / 'source_pdfs/root-recovery.pdf'
    paths = [I / 'summary-snapshot.md', ROOT / 'extracted/root-rules.txt', b / 'publisher-rules-library-p16.txt']
    inputs = [h.coverage(p, blocks, selector=lambda code, p=p: p.name in code) for p in paths]
    doc = fitz.open(pdf)
    pdf_blocks = [x for x in blocks if 'native-page-' in x['code'] and '.txt' in x['code']]
    pages = [{**h.coverage(pdf, pdf_blocks, page.get_text()), 'physical_page': n} for n, page in enumerate(doc, 1)]
    native = N / 'source-only-audit/native-render-manifest.json'
    lineage = json.loads(native.read_text())
    assert lineage['pdf_sha256'] == sha(pdf)
    render_rows = []
    pngs = {}
    for row in lineage['pages']:
        path = Path(row['render'])
        assert sha(path) == row['png_sha256']
        page = doc[row['physical_page'] - 1]
        # The auditor declared Matrix(2,2). Independently reproduce its bytes.
        fresh = page.get_pixmap(matrix=fitz.Matrix(2, 2)).tobytes('png')
        digest = hashlib.sha256(fresh).hexdigest()
        assert digest == sha(path), path
        render_rows.append({'physical_page': row['physical_page'], 'path': str(path), 'sha256': digest, 'width': row['pixel_width'], 'height': row['pixel_height'], 'independently_reproduced_native_pdf_render_bytes_match': True})
        pngs.setdefault(digest, []).append(render_rows[-1])
    delivered, covered = [], set()
    for image_call in images:
        raw = json.loads(Path(image_call['raw_path']).read_text())
        for item in raw['actual_output']['payload'].get('output', []):
            if item.get('type') != 'input_image':
                continue
            url = item.get('image_url', '')
            assert url.startswith('data:image/png;base64,')
            digest = hashlib.sha256(base64.b64decode(url.split(',', 1)[1], validate=True)).hexdigest()
            matches = pngs.get(digest, [])
            covered.update(x['physical_page'] for x in matches)
            delivered.append({'call_ordinal': image_call['call_ordinal'], 'output_ordinal': image_call['output_ordinal'], 'raw_path': image_call['raw_path'], 'raw_sha256': image_call['raw_sha256'], 'delivered_png_sha256': digest, 'matching_native_pdf_renders': matches, 'actual_payload_bytes_match_native_render': bool(matches)})
    required = {1, 5, 9, 10, 24, 27, 28}
    image_ok = required.issubset(covered) and bool(delivered) and all(x['actual_payload_bytes_match_native_render'] for x in delivered)
    publisher = b / 'publisher-rules-library-p16.json'
    result = json.loads(publisher.read_text())['results'][0]
    metadata = {k: v for k, v in result.items() if k not in ('text', 'links')}
    metadata_matches = [x['record']['read_index'] for x in blocks if publisher.name in x['code'] for obj in h.json_objects(x['body']) if obj == metadata]
    text_equal = result['text'] + '\n' == paths[-1].read_text()
    raw_coverage = h.coverage(publisher, blocks, selector=lambda code: publisher.name in code)
    raw_lines = publisher.read_text().splitlines()
    escaped_text_lines = [n for n, line in enumerate(raw_lines, 1) if line.lstrip().startswith('"text":')]
    assert len(escaped_text_lines) == 1
    missing_nontext = sorted(set(raw_coverage['unmatched_nonempty_lines_in_ordered_blocks']) - set(escaped_text_lines))
    metadata_ok = bool(metadata_matches) or not missing_nontext
    passed = all(x['all_nonempty_lines_in_ordered_exact_blocks'] for x in inputs + pages) and len(pages) == 32 and image_ok and metadata_ok and text_equal
    proof = {'status': 'PASS' if passed else 'INCOMPLETE', 'agent_path': rec['agent_path'], 'runtime_path': rec['runtime_path'], 'completed_source_audit': {'path': str(audit), 'sha256': sha(audit)}, 'read_calls': calls, 'inputs': inputs, 'pdf_sha256': sha(pdf), 'pdf_pages': pages, 'render_manifest': {'path': str(native), 'sha256': sha(native), 'declared_renderer': lineage['renderer'], 'matrix': [2, 2], 'render_rows': render_rows}, 'image_delivery': {'required_physical_pages': sorted(required), 'covered_physical_pages': sorted(covered), 'missing_required_pages': sorted(required - covered), 'actual_image_payloads': delivered, 'status': 'PASS' if image_ok else 'INCOMPLETE'}, 'publisher_representation': {'raw_json_path': str(publisher), 'raw_json_sha256': sha(publisher), 'rendered_text_plus_newline_equals_complete_txt': text_equal, 'complete_metadata_object_actual_delivery_read_indices': metadata_matches, 'metadata_fields': sorted(metadata) if metadata_matches else [], 'raw_json_serialization_fully_delivered': not raw_coverage['unmatched_nonempty_lines_in_ordered_blocks'], 'raw_nontext_line_coverage': raw_coverage, 'long_escaped_text_property_line': escaped_text_lines[0], 'missing_nontext_lines': missing_nontext, 'raw_nontext_metadata_and_link_array_actually_delivered': not missing_nontext}, 'method': 'Original auditor actual runtime call/output pairs only; JSON transport decoded, declared line-number prefixes removed only, otherwise exact ordered contiguous source lines. Native PDF text comparisons use only reads of this auditor native-page text extractions. All rendered PNGs independently reproduced from unchanged PDF and actual image payload bytes matched. Complete publisher Law+FAQ rendered text plus exact native JSON text-value equivalence. Metadata proven either by complete parsed object or every exact serialized nontext source line, including links; escaped text line delivery remains separately disclosed. No QA inputs or grades used.'}
    save(out / 'source-delivery-audit.json', proof)
    print(json.dumps({'status': proof['status'], 'inputs_missing': [(Path(x['path']).name, len(x['unmatched_nonempty_lines_in_ordered_blocks'])) for x in inputs], 'pdf_missing': [(x['physical_page'], len(x['unmatched_nonempty_lines_in_ordered_blocks'])) for x in pages if not x['all_nonempty_lines_in_ordered_exact_blocks']], 'images': proof['image_delivery']['status'], 'metadata_matches': metadata_matches, 'missing_nontext_lines': missing_nontext}))

if __name__ == '__main__':
    main()
