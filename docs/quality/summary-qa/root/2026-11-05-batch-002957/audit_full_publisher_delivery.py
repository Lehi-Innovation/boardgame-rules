"""Prove actual source delivery without reading benchmark questions or keys.

The completed source-audit report must exist before this script runs. Inputs and
prior proofs are immutable. Only the requested evidence directory is written.
"""
from pathlib import Path
from difflib import SequenceMatcher
import argparse
import base64
import hashlib
import json
import re

ROOT = Path('/home/jonny/projects/boardgame-rules')
R = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, indent=2) + '\n'
    if path.exists() and path.read_text() != text:
        raise RuntimeError(f'Refusing to overwrite different evidence: {path}')
    if not path.exists():
        path.write_text(text)


def delivered_texts(output):
    if isinstance(output, str):
        try:
            output = json.loads(output)
        except ValueError:
            return [(output, 'plain tool text')]
    if isinstance(output, dict):
        return [(output['output'], 'JSON output field decoded')] if isinstance(output.get('output'), str) else []
    blocks = []
    for item in output if isinstance(output, list) else []:
        body = item.get('text', '')
        try:
            parsed = json.loads(body)
        except ValueError:
            parsed = None
        if isinstance(parsed, dict) and isinstance(parsed.get('output'), str):
            blocks.append((parsed['output'], 'JSON output field decoded'))
        else:
            blocks.append((body, 'plain tool text'))
    return blocks


def collect(runtime, out):
    calls, blocks, records, images = {}, [], [], []
    for line in runtime.open():
        event = json.loads(line)
        p = event.get('payload', {})
        kind = p.get('type')
        inp = p.get('input', p.get('arguments', ''))
        code = inp if isinstance(inp, str) else json.dumps(inp)
        if kind in ('custom_tool_call', 'function_call'):
            is_image = bool(re.search(r'tools\.view_image\s*\(', code))
            is_read = bool(re.search(r'[\"\']?cmd[\"\']?\s*:', code)) and any(x in code for x in ('sed ', 'cat ', 'nl ', 'get_text(', 'read_text(', 'print('))
            is_write = bool(re.search(r'cat\s*>|sed\s+-i\b|\.write_text\(|\.write_bytes\(', code))
            if is_image or (is_read and not is_write):
                calls[p.get('call_id')] = (event, code, is_image)
        if kind not in ('custom_tool_call_output', 'function_call_output') or p.get('call_id') not in calls:
            continue
        call, code, is_image = calls[p['call_id']]
        raw = out / 'delivery-raw' / f'call-{call.get("ordinal", 0):04}.json'
        save(raw, {'actual_call': call, 'actual_output': event})
        pair = {'call_id': p['call_id'], 'call_ordinal': call.get('ordinal'), 'output_ordinal': event.get('ordinal'), 'raw_path': str(raw), 'raw_sha256': sha(raw)}
        if is_image:
            images.append({**pair, 'input': code})
        for index, (body, transport) in enumerate(delivered_texts(p.get('output', ''))):
            normalizations = []
            if re.search(r'\bnl\s+-ba\b', code):
                body = re.sub(r'(?m)^[ \t]*[0-9]+\t', '', body)
                normalizations.append('declared nl -ba line-number/tab prefix removed')
            if re.search(r'\brg\s+[^\n]*?(?:-n\b|--line-number\b)', code):
                body = re.sub(r'(?m)^[0-9]+[:-]', '', body)
                normalizations.append('declared rg line-number prefix removed')
            if re.search(r"print\(f[\"']\{i\+1\}: \{(?:a|lines|ls)\[i\]\}", code):
                body = re.sub(r'(?m)^[0-9]+: ', '', body)
                normalizations.append('declared Python i+1 colon-space line-number prefix removed')
            record = {**pair, 'read_index': len(blocks) + 1, 'content_index': index, 'transport': transport, 'comparison_normalization': normalizations, 'truncation_marker_present': bool(re.search('truncated', body, re.I))}
            records.append(record)
            blocks.append({'body': body, 'code': code, 'record': record})
    return blocks, records, images


def coverage(path, blocks, text=None, selector=None):
    lines = (path.read_text() if text is None else text).splitlines()
    covered, ranges = set(), []
    for block in blocks:
        if selector and not selector(block['code']):
            continue
        for a, b, n in SequenceMatcher(None, lines, block['body'].splitlines(), autojunk=False).get_matching_blocks():
            if n:
                covered.update(range(a + 1, a + n + 1))
                ranges.append({'read_index': block['record']['read_index'], 'source_lines': [a + 1, a + n], 'output_lines': [b + 1, b + n]})
    missing = [n for n, line in enumerate(lines, 1) if line.strip() and n not in covered]
    return {'path': str(path), 'sha256': sha(path), 'total_lines': len(lines), 'nonempty_lines': sum(bool(x.strip()) for x in lines), 'unmatched_nonempty_lines_in_ordered_blocks': missing, 'all_nonempty_lines_in_ordered_exact_blocks': not missing, 'ordered_exact_matching_ranges': ranges}


def json_objects(body):
    decoder, objects, offset = json.JSONDecoder(), [], 0
    while offset < len(body):
        match = re.search(r'[\[{]', body[offset:])
        if not match:
            break
        start = offset + match.start()
        try:
            value, length = decoder.raw_decode(body[start:])
            objects.append(value)
            offset = start + length
        except ValueError:
            offset = start + 1
    return objects


def own_glyph_images(images, directory):
    """Bind this auditor's actual PNG payload bytes to its local PDF renders."""
    required_pages = (1, 5, 9, 10, 24, 27, 28)
    artifacts = {}
    for path in directory.glob('pdf-page-*.png'):
        match = re.fullmatch(r'pdf-page-(\d+)\.png', path.name)
        if match:
            artifacts.setdefault(sha(path), []).append({'path': str(path), 'physical_page': int(match[1]), 'sha256': sha(path)})
    delivered, covered = [], set()
    for call in images:
        raw = json.loads(Path(call['raw_path']).read_text())
        for index, item in enumerate(raw['actual_output']['payload'].get('output', [])):
            if item.get('type') != 'input_image':
                continue
            url = item.get('image_url', '')
            digest = hashlib.sha256(base64.b64decode(url.split(',', 1)[1], validate=True)).hexdigest() if url.startswith('data:image/png;base64,') else None
            matches = artifacts.get(digest, [])
            covered.update(x['physical_page'] for x in matches)
            delivered.append({'call_ordinal': call['call_ordinal'], 'output_ordinal': call['output_ordinal'], 'content_index': index, 'raw_path': call['raw_path'], 'raw_sha256': call['raw_sha256'], 'delivered_png_sha256': digest, 'matching_local_pdf_pngs': matches, 'actual_payload_bytes_match_local_png': bool(matches)})
    missing = sorted(set(required_pages) - covered)
    return {'mode': 'OWN_ACTUAL_RUNTIME_IMAGE_PAYLOADS_ONLY', 'glyph_directory': str(directory), 'required_physical_pages': list(required_pages), 'missing_required_physical_pages': missing, 'actual_png_payloads': delivered, 'all_actual_png_payload_bytes_match_local_pdf_pngs': bool(delivered) and all(x['actual_payload_bytes_match_local_png'] for x in delivered), 'passed': not missing and bool(delivered) and all(x['actual_payload_bytes_match_local_png'] for x in delivered)}


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--agent-path', required=True)
    parser.add_argument('--runtime-path', type=Path)
    parser.add_argument('--summary', required=True, type=Path)
    parser.add_argument('--output-directory', required=True, type=Path)
    parser.add_argument('--audit-report', required=True, type=Path)
    parser.add_argument('--publisher-json', required=True, type=Path)
    parser.add_argument('--publisher-text', required=True, type=Path)
    parser.add_argument('--faq-text', type=Path, help='Optional separately supplied tiny FAQ text; omitted when complete publisher text is the only FAQ input')
    parser.add_argument('--faq-metadata', type=Path, help='Optional metadata for a separately supplied tiny FAQ')
    parser.add_argument('--glyph-directory', type=Path, help='Own pdf-page-NN.png render directory; defaults to completed audit report directory')
    parser.add_argument('--original-proof', type=Path)
    args = parser.parse_args()
    for name, value in vars(args).items():
        if isinstance(value, Path):
            setattr(args, name, value.resolve())
    if not args.output_directory.is_relative_to(R):
        parser.error('Evidence output directory must be inside this authorized batch directory')
    if not args.audit_report.is_file():
        parser.error('Completed source audit report is required; no premature proof may be finalized')
    for optional in (args.faq_text, args.faq_metadata):
        if optional is not None and not optional.is_file():
            parser.error(f'Supplied optional source input must exist: {optional}')
    # This binds delivery to a completed report; its verdict is never interpreted or changed.
    json.loads(args.audit_report.read_text())
    if args.runtime_path is None:
        candidates = []
        for path in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*.jsonl'):
            with path.open() as f:
                first = json.loads(next(f))
            if first.get('payload', {}).get('agent_path') == args.agent_path:
                candidates.append(path)
        if len(candidates) != 1:
            parser.error(f'Expected one runtime for {args.agent_path}, got {len(candidates)}')
        args.runtime_path = candidates[0]
    with args.runtime_path.open() as f:
        meta = json.loads(next(f))['payload']
    if meta.get('agent_path') != args.agent_path:
        parser.error('Runtime agent path does not match requested agent')
    blocks, records, images = collect(args.runtime_path, args.output_directory)
    original_source = ROOT / 'extracted/root-rules.txt'
    pdf = ROOT / 'source_pdfs/root-recovery.pdf'
    paths = [args.summary, original_source, args.publisher_text]
    paths.extend(p for p in (args.faq_text, args.faq_metadata) if p is not None)
    inputs = [coverage(p, blocks, selector=lambda code, p=p: p.name in code) for p in paths]
    reused = None
    if args.original_proof:
        old = json.loads(args.original_proof.read_text())
        original_input = next(x for x in old['inputs'] if x['path'] == str(original_source))
        old_summary = next(x for x in old['inputs'] if Path(x['path']).name == 'summary-snapshot.md')
        reuse_ok = old['agent_path'] == args.agent_path and old['pdf_sha256'] == sha(pdf) and original_input['sha256'] == sha(original_source) and len(old['pdf_pages']) == 32 and all(x['all_nonempty_lines_in_ordered_exact_blocks'] for x in old['pdf_pages']) and original_input['all_nonempty_lines_in_ordered_exact_blocks']
        if not reuse_ok:
            parser.error('Original proof reuse failed exact agent/source/PDF/hash/completeness checks')
        # Hash all prior raw evidence and glyph image artifacts, rather than relying on a status alone.
        prior_raw_ok = all(Path(x['raw_path']).is_file() and sha(x['raw_path']) == x['raw_sha256'] for x in old['read_calls'])
        if not prior_raw_ok:
            parser.error('An original raw read/output pair changed')
        image_artifacts = []
        original_image_ordinals = {x['ordinal'] for x in old['image_inspection_calls']}
        image_call_ids, delivered_images = set(), []
        for line in Path(old['runtime_path']).open():
            event = json.loads(line)
            payload = event.get('payload', {})
            if event.get('ordinal') in original_image_ordinals:
                image_call_ids.add(payload['call_id'])
            if payload.get('type') in ('custom_tool_call_output', 'function_call_output') and payload.get('call_id') in image_call_ids:
                for item in payload.get('output', []):
                    if item.get('type') == 'input_image' and item.get('image_url', '').startswith('data:image/png;base64,'):
                        delivered_images.append({'actual_runtime_output_ordinal': event.get('ordinal'), 'delivered_image_sha256': hashlib.sha256(base64.b64decode(item['image_url'].split(',', 1)[1])).hexdigest()})
        if len(delivered_images) != 7:
            parser.error('Expected seven original actual PNG image payloads')
        for n, delivered_image in zip((1, 5, 9, 10, 24, 27, 28), delivered_images):
            image = args.original_proof.parent / 'source-only-audit' / f'pdf-page-{n:02}.png'
            image_artifacts.append({'path': str(image), 'sha256': sha(image), 'physical_page': n, **delivered_image, 'matches_actual_original_delivered_png_bytes': sha(image) == delivered_image['delivered_image_sha256']})
        if not all(x['matches_actual_original_delivered_png_bytes'] for x in image_artifacts):
            parser.error('Original glyph PNG bytes changed from actual runtime delivery')
        reused = {'path': str(args.original_proof), 'sha256': sha(args.original_proof), 'same_auditor': True, 'source_sha256_matches': True, 'pdf_sha256_matches': True, 'all_prior_raw_pair_hashes_match': prior_raw_ok, 'original_physical_page_count': 32, 'page32_all_nonempty_lines_delivered': old['pdf_pages'][31]['all_nonempty_lines_in_ordered_exact_blocks'], 'image_artifacts_verified_against_actual_original_delivery': image_artifacts, 'all_original_glyph_image_hashes_unchanged': True}
        inputs[1] = {**original_input, 'delivery_proof_reused_from': str(args.original_proof)}
        if old_summary['sha256'] == sha(args.summary) and old_summary['all_nonempty_lines_in_ordered_exact_blocks']:
            inputs[0] = {**old_summary, 'path': str(args.summary), 'delivery_proof_reused_from': str(args.original_proof), 'byte_identical_summary': True}
        pages = old['pdf_pages']
        images = old['image_inspection_calls'] + images
        image_validation = {'mode': 'VERIFIED_SAME_AUDITOR_ORIGINAL_PDF_PROOF', 'passed': True, 'original_proof_sha256': sha(args.original_proof), 'all_original_glyph_image_hashes_unchanged': True}
    else:
        import fitz
        doc = fitz.open(pdf)
        selected = [b for b in blocks if ('get_text(' in b['code'] and '.pdf' in b['code']) or ('pdf' in b['code'].lower() and '.txt' in b['code'])]
        pages = [{**coverage(pdf, selected, page.get_text()), 'physical_page': n} for n, page in enumerate(doc, 1)]
        image_validation = own_glyph_images(images, args.glyph_directory or args.audit_report.parent)
    raw = json.loads(args.publisher_json.read_text())
    result = raw['results'][0]
    metadata = {k: v for k, v in result.items() if k not in ('text', 'links')}
    metadata_blocks = [b for b in blocks if args.publisher_json.name in b['code'] and 'print(' in b['code']]
    metadata_matches = [b['record']['read_index'] for b in metadata_blocks if any(isinstance(obj, dict) and all(obj.get(k, object()) == v for k, v in metadata.items()) for obj in json_objects(b['body']))]
    text_equal = args.publisher_text.read_text() == result['text'] + '\n'
    publisher = {'raw_json_path': str(args.publisher_json), 'raw_json_sha256': sha(args.publisher_json), 'text_path': str(args.publisher_text), 'text_sha256': sha(args.publisher_text), 'parsed_results_0_text_plus_newline_equals_txt': text_equal, 'metadata_fields_actually_delivered': ['results[0].' + k for k in metadata] if metadata_matches else [], 'metadata_matching_read_indices': metadata_matches, 'raw_json_fully_delivered': False, 'representation_note': 'Full rules and embedded FAQ text is proven through exact TXT line delivery and independent JSON text+newline equivalence. Complete raw JSON serialization and links array are not claimed delivered. Metadata is checked against actual parsed-object output, excluding text and links.'}
    passed = len(pages) == 32 and all(x['all_nonempty_lines_in_ordered_exact_blocks'] for x in inputs + pages) and text_equal and bool(metadata_matches) and image_validation['passed']
    proof = {'agent_path': args.agent_path, 'runtime_path': str(args.runtime_path), 'method': 'Actual runtime read-call/output pairs only, JSON output fields decoded and declared line-number prefixes removed (nl -ba or explicit Python i+1 colon-space); otherwise exact ordered contiguous line blocks. Source selector requires the input basename in the read call. Calls writing generated reports are excluded. Establishes delivered text, not cognitive attention or factual correctness.', 'read_calls': records, 'inputs': inputs, 'publisher_json_representation': publisher, 'pdf_sha256': sha(pdf), 'pdf_pages': pages, 'image_inspection_calls': images, 'image_delivery_validation': image_validation, 'reusable_original_pdf_proof': reused, 'completed_source_audit': {'path': str(args.audit_report), 'sha256': sha(args.audit_report), 'verdict_unchanged': True}, 'line_coverage_status': 'ALL_SOURCE_AND_SUMMARY_NONEMPTY_LINES_DELIVERED' if passed else 'DELIVERY_NOT_FULLY_PROVEN', 'limitations': ['No source-audit verdict, semantic grade, benchmark key, question or reader answer is evaluated by this helper.', 'Only the source text and separately inspected metadata fields are delivery claims; neither links-array delivery nor entire raw JSON serialization is claimed.']}
    save(args.output_directory / 'source-delivery-audit.json', proof)
    print(json.dumps({'status': proof['line_coverage_status'], 'input_lines': [[Path(x['path']).name, x['nonempty_lines'], len(x['unmatched_nonempty_lines_in_ordered_blocks'])] for x in inputs], 'pdf_pages': len(pages), 'metadata_matches': metadata_matches, 'read_calls': len(records), 'proof_sha256': sha(args.output_directory / 'source-delivery-audit.json')}))


if __name__ == '__main__':
    main()
