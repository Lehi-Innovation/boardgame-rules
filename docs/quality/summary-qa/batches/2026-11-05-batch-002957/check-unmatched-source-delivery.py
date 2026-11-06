#!/usr/bin/env python3
"""Check actual model-visible source slices without copying private runtime metadata."""
from pathlib import Path
import argparse
import datetime
import hashlib
import json

ROOT = Path('/home/jonny/projects/boardgame-rules')
BATCH = ROOT / 'docs/quality/summary-qa/batches/2026-11-05-batch-002957'
RUN = ROOT / 'docs/quality/summary-qa/unmatched/2026-11-05-batch-002957'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--audit', required=True)
    parser.add_argument('--auditor', required=True)
    args = parser.parse_args()
    report_file = RUN / args.audit / 'source-audit.json'
    audit = json.loads(report_file.read_text())
    provenance = json.loads((RUN / 'model-provenance.json').read_text())
    agent = next(a for a in provenance['agents'] if a['identity'] == args.auditor)
    runtime = Path(agent['runtime_source_path'])
    chunks = {}
    images = []
    calls = []
    forbidden_hits = []
    forbidden_names = ['questions.json', 'answer-key.json', 'reader-a.json',
                       'reader-b.json', 'grades.json', 'results.json']
    for ordinal, line in enumerate(runtime.open(), 1):
        record = json.loads(line)
        if not isinstance(record, dict) or record.get('type') != 'response_item':
            continue
        p = record.get('payload')
        if not isinstance(p, dict):
            continue
        if p.get('type') == 'custom_tool_call':
            inp = p.get('input', '')
            if isinstance(inp, str):
                calls.append({'ordinal': ordinal, 'name': p.get('name'),
                              'input_sha256': digest(inp.encode())})
                for name in forbidden_names:
                    if name in inp:
                        forbidden_hits.append({'ordinal': ordinal, 'name': name})
        if p.get('type') != 'custom_tool_call_output':
            continue
        for block_index, block in enumerate(p.get('output', [])):
            if not isinstance(block, dict):
                continue
            if block.get('type') == 'input_image':
                images.append({'ordinal': ordinal, 'call_id': p.get('call_id')})
            if block.get('type') != 'input_text' or not isinstance(block.get('text'), str):
                continue
            direct_key = f'direct-text-output-{ordinal}-{block_index}'
            chunks.setdefault(direct_key, []).append((ordinal, {
                'chunk_id': direct_key, 'direct_model_visible_text': True,
                'output': block['text']}))
            try:
                output = json.loads(block['text'])
            except (ValueError, TypeError):
                continue
            if isinstance(output, dict) and 'chunk_id' in output:
                chunks.setdefault(output['chunk_id'], []).append((ordinal, output))
    receipts = []
    for receipt in audit['full_delivery_receipts']:
        path = Path(receipt.get('parsed_visible_path', receipt['path']))
        text = path.read_text()
        expected_sha = receipt.get('parsed_visible_sha256', receipt['sha256'])
        assert digest(path.read_bytes()) == expected_sha, path
        cursor = 0
        slices = []
        normalized_slices = [dict(start=x[0], end=x[1]) if isinstance(x, list) else x
                             for x in receipt['slices']]
        for part in sorted(normalized_slices, key=lambda x: x['start']):
            start, end = part['start'], part['end']
            assert start == cursor and start < end <= len(text), path
            expected = text[start:end]
            candidates = (chunks.get(part['tool_chunk_id'], []) if 'tool_chunk_id' in part
                          else [entry for group in chunks.values() for entry in group])
            matches = [(ordinal, output) for ordinal, output in candidates
                       if (output.get('exit_code') == 0 or output.get('direct_model_visible_text') is True)
                       and isinstance(output.get('output'), str)
                       and expected in output['output']]
            assert matches, (str(path), start, end, part.get('tool_chunk_id'))
            slices.append({'start': start, 'end': end,
                           'matching_chunk_ids': [x[1]['chunk_id'] for x in matches],
                           'matching_runtime_ordinals': [x[0] for x in matches],
                           'expected_text_sha256': digest(expected.encode()),
                           'actual_complete_text_present': True})
            cursor = end
        assert cursor == len(text), path
        receipts.append({'path': str(path), 'sha256': expected_sha,
                         'characters': len(text), 'slices': slices, 'complete': True})
    counts = audit.get('inspection_counts', audit.get('completeness', {}))
    pdf_receipts = audit.get('pdf_diagram_render_receipts', audit.get('pdf_diagram_receipts'))
    if isinstance(pdf_receipts, dict):
        pdf_receipts = pdf_receipts['pages']
    image_receipts = audit['image_receipts']
    native = image_receipts if isinstance(image_receipts, dict) else {}
    listed_character_count = (sum(not x.get('cells') for x in image_receipts)
                              if isinstance(image_receipts, list) else len(native.get('characters', [])))
    listed_crop_count = (len({c['view_path'] for x in image_receipts for c in x.get('cells', [])})
                         if isinstance(image_receipts, list) else len(native.get('crops', [])))
    characters = counts.get('character_cards', counts.get('original_character_images_inspected',
                                                          listed_character_count))
    crop_count = counts.get('native_resolution_three_cell_crops',
                           len(audit['native_crop_receipts']) if 'native_crop_receipts' in audit
                           else listed_crop_count)
    expected_images = characters + crop_count + len(pdf_receipts)
    assert len(images) >= expected_images, (len(images), expected_images)
    assert not forbidden_hits, forbidden_hits
    result = {
        'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'audit_path': str(report_file), 'audit_sha256': digest(report_file.read_bytes()),
        'checker_script_sha256': digest(Path(__file__).read_bytes()),
        'auditor_id': args.auditor, 'runtime_path': str(runtime),
        'runtime_sha256_at_check': digest(runtime.read_bytes()),
        'verified': True, 'text_receipts': receipts,
        'actual_native_image_outputs': images, 'expected_native_image_outputs': expected_images,
        'tool_calls_minimal_hash_projection': calls,
        'forbidden_known_question_key_reader_grade_filename_hits': forbidden_hits,
        'limits': [
            'Identity/model/fork verified separately by check-agent-models.py.',
            'Initial task body is encrypted in parent spawn metadata; no plaintext-hash equality is claimed.',
            'The filename scan is a trace check of these actual tool calls, not a general sandbox proof.',
            'Images are matched by actual delivered output counts and audit native-inspection receipts; semantic audit remains the independent reviewer verdict.'
        ]
    }
    out = BATCH / 'coordinator-checks' / ('unmatched-' + args.audit + '-actual-delivery.json')
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'verified': True, 'proof': str(out), 'text_files': len(receipts),
                      'text_slices': sum(len(x['slices']) for x in receipts),
                      'native_image_outputs': len(images)}))

if __name__ == '__main__':
    main()
