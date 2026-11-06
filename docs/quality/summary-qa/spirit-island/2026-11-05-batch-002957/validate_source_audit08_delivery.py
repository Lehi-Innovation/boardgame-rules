#!/usr/bin/env python3
"""Validate audit08 evidence files; does not perform or change a rules verdict.
Run from any directory with this repository's .venv/bin/python.
Only the named evidence files, permitted source files, own script, and an
explicitly authorized canonical byte comparison are read. No directory search.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from hashlib import sha256
import json
import io
from pathlib import Path
import re

import fitz
from PIL import Image

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
PREFIX = str(B.relative_to(ROOT))
PREFLIGHT = 'docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/spirit-island'
PANELS = PREFLIGHT + '/original-spirit-panels'
CARD = PREFIX + '/card-scope-source'
EXPECTED = {
    'source-candidate-19.md': 'c705923bc215d598f756af6a6fd6dd5c246e762ff7a304dfdc2bdf124ae1463e',
    'source-audit-final-08.json': 'a9e9493a0321fbed19bda2c290dc938d22f7b7c3f8087238a87117dc68009f4f',
    'source-audit-final-08-read-ledger.json': '1e3d8ded57c6ff50bb7dd45c5673efe633cb649cae31e968718ae5af91f84c7b',
    'source-audit-final-08-visual-manifest.json': '6e690d0ca0b27f0220b0aba38e8841c0523e57d5e230ed4f25c64c3448dc0a75',
}
PDF_SHA = '64012c21460d3aee0f5c2c0d1048811a4dd4b4aebd03284ee4706a6a1f8e630e'
PROMPT_SHA = '3f91a2adbde549f372c566e339dc2c6fa2dfa2a1ba5443be68f40c0ad913a7d3'
ALLOWED_TEXT = {
    PREFIX + '/' + n for n in [
        'final-source-audit-08-prompt.txt', 'source-manifest.json',
        'supplemental-source-manifest-v4.json', 'source-candidate-19.md',
        'novelty11-source-scratch/novelty11-publisher-updates.txt',
    ]
} | {
    'extracted/spirit-island-rules.txt',
    PREFLIGHT + '/living-faq-core-game.txt',
    PREFLIGHT + '/living-faq-setup.txt',
    PREFLIGHT + '/provenance.json',
    CARD + '/what-do-range-boosts-affect.txt',
    CARD + '/range-in-text-of-powers-that-target-spirits.txt',
    CARD + '/core-second-printing.txt',
    PANELS + '/README.md', PANELS + '/panel-download-map.json',
    PANELS + '/download-integrity.json',
    PANELS + '/independent-printed-photo-corroboration.json',
    '../../../../tmp/si_audit08_publisher_branch_claw.txt',
}
checks = []
errors = []
diagnostics = []
read_access = []

def check(name, condition, details=None, kind='filesystem'):
    row = {'name': name, 'passed': bool(condition), 'kind': kind}
    if details is not None:
        row['details'] = details
    checks.append(row)
    if not condition:
        if kind == 'nonblocking_render_diagnostic':
            diagnostics.append(name)
        else:
            errors.append(name)


def read(path, purpose):
    path = path.resolve()
    data = path.read_bytes()
    read_access.append({'path': str(path), 'purpose': purpose,
                        'sha256': sha256(data).hexdigest(), 'bytes': len(data)})
    return data


def read_json(path, purpose):
    return json.loads(read(path, purpose).decode('utf-8'))


def digest(data):
    return sha256(data).hexdigest()


def project(row):
    return {k: row[k] for k in ['path', 'start', 'end', 'source_sha256',
                              'slice_sha256', 'truncated']}


artifact_bytes = {n: read(B / n, 'frozen audit artifact validation') for n in EXPECTED}
for name, expected in EXPECTED.items():
    check('frozen hash: ' + name, digest(artifact_bytes[name]) == expected,
          {'expected': expected, 'actual': digest(artifact_bytes[name])})
audit = json.loads(artifact_bytes['source-audit-final-08.json'])
ledger = json.loads(artifact_bytes['source-audit-final-08-read-ledger.json'])
visual = json.loads(artifact_bytes['source-audit-final-08-visual-manifest.json'])
candidate = artifact_bytes['source-candidate-19.md']
check('candidate character count', len(candidate.decode('utf-8')) == 52164)
check('report candidate identity', audit['candidate'] == PREFIX + '/source-candidate-19.md'
      and audit['candidate_sha256'] == EXPECTED['source-candidate-19.md']
      and visual['candidate_sha256'] == EXPECTED['source-candidate-19.md'])

# This is byte comparison only: canonical is not newly delivered rules prose.
canonical_path = ROOT / 'rules/spirit-island.md'
canonical = read(canonical_path, 'authorized hash/byte comparison only; no fresh model text delivery')
check('candidate canonical exact bytes', canonical == candidate,
      {'canonical_path': str(canonical_path), 'canonical_sha256': digest(canonical),
       'candidate_sha256': digest(candidate), 'same_bytes': canonical == candidate})

reads = ledger['reads']
check('exactly 92 successful recorded text slices', len(reads) == 92)
by_path = defaultdict(list)
for row in reads:
    by_path[row['path']].append(row)
check('consulted text input allowlist exactly matches', set(by_path) == ALLOWED_TEXT,
      {'unexpected': sorted(set(by_path) - ALLOWED_TEXT),
       'missing': sorted(ALLOWED_TEXT - set(by_path)), 'files': len(by_path)})
text_inventory = []
for path, slices in sorted(by_path.items()):
    raw = read(ROOT / path, 'machine validation of previously delivered text input')
    text = raw.decode('utf-8')
    # The original helper used read_text(), which normalizes CRLF; none are expected.
    check('text has no newline normalization ambiguity: ' + path, '\r' not in text)
    cursor = 0
    for row in sorted(slices, key=lambda x: x['start']):
        start, end = row['start'], row['end']
        check('slice bounds/hash: ' + path + ':' + str(start),
              isinstance(start, int) and isinstance(end, int)
              and start == cursor and 0 <= start < end <= len(text)
              and end - start <= 6000 and row['characters'] == len(text)
              and row['bytes'] == len(raw) and row['source_sha256'] == digest(raw)
              and row['slice_sha256'] == digest(text[start:end].encode('utf-8')))
        check('recorded transport cap/no truncation: ' + path + ':' + str(start),
              row['output_cap'] >= 4000 and row['truncated'] is False,
              'Checks recorded fields only; actual tool delivery is an auditor attestation.',
              'record_validation_of_transport_attestation')
        cursor = end
    check('complete contiguous text coverage: ' + path, cursor == len(text))
    text_inventory.append({'path': path, 'sha256': digest(raw), 'characters': len(text),
                           'bytes': len(raw), 'slices': len(slices),
                           'complete_contiguous_range': [0, cursor]})
check('prompt expected hash', digest((ROOT / (PREFIX + '/final-source-audit-08-prompt.txt')).read_bytes()) == PROMPT_SHA)
expected_flat = [project(row) for row in reads]
check('report flat source_delivery exactly matches read ledger', audit['source_delivery'] == expected_flat)
check('ledger flat source_delivery exactly matches detailed rows', ledger['source_delivery'] == expected_flat)
check('ledger recorded totals', ledger['totals'] == {
    'text_files': 17, 'slices': 92, 'truncated_slices': 0,
    'failed_reads': 0, 'rereads_required': 0})

# Validate the publisher prose derivative against allowed primary transport.
from bs4 import BeautifulSoup
publisher_raw = read(ROOT / CARD / 'publisher-branch-claw.html',
                     'machine-only reconstruction of prior complete visible-prose derivative')
soup = BeautifulSoup(publisher_raw.decode('utf-8'), 'html.parser')
for node in soup(['script', 'style']):
    node.decompose()
expected_prose = soup.get_text('\n', strip=True)
check('publisher visible-prose derivative reproducible',
      expected_prose.encode('utf-8') == (Path('/tmp/si_audit08_publisher_branch_claw.txt')).read_bytes())

manifest = read_json(B / 'supplemental-source-manifest-v4.json',
                     'machine validation against permitted source inventory; no reviewer links followed')
card_records = [x for x in manifest['source_records'] if x.get('role') == 'primary printed card face']
panel_records = [x for x in manifest['source_records'] if x.get('native_inspection_required') is True]
card_names = {Path(x['path']).name for x in card_records}
panel_names = {Path(x['path']).name for x in panel_records}
check('allowed manifest has exactly 33 distinct faces and 16 native panels',
      len(card_records) == len(card_names) == 33 and len(panel_records) == len(panel_names) == 16)
visual_rows = visual['visual_sources']
check('56 distinct recorded visual sources', len(visual_rows) == 56
      and len({x['path'] for x in visual_rows}) == 56)
check('all 33 allowed card faces represented', card_names <= {Path(x['path']).name for x in visual_rows})
check('all 16 allowed panels represented', panel_names <= {Path(x['path']).name for x in visual_rows})
allowed_visual = {str(Path(x['path']).relative_to(ROOT)) for x in card_records + panel_records}
allowed_visual |= {PANELS + '/corroborating-all-spirits-2017.jpg',
                   PANELS + '/corroborating-2017-bringer-track-crop.png',
                   CARD + '/branch-claw-rulebook-p6.png'}
allowed_visual |= {PREFIX + '/pdf-inspection/audit08/audit08-core-p' + str(p).zfill(2) + '.png'
                   for p in [6, 7, 17, 32]}
check('visual input allowlist exactly matches', {x['path'] for x in visual_rows} == allowed_visual)
visual_inventory = []
by_visual = {Path(x['path']).name: x for x in visual_rows}
for row in visual_rows:
    p = ROOT / row['path']
    raw = read(p, 'machine image hash/dimension validation; not a new visual inspection')
    with Image.open(p) as im:
        width, height = im.size
        im.verify()
    expected_hash = row['sha256'] if row.get('direct_render_and_inspection') else row['source_sha256']
    check('image hash and decode: ' + row['path'], digest(raw) == expected_hash)
    if 'dimensions' in row:
        check('recorded dimensions: ' + row['path'], row['dimensions'] == [width, height])
    if p.name in panel_names:
        check('native panel dimensions: ' + p.name, [width, height] == [2697, 1797])
    if p.name in card_names | panel_names:
        check('native inspection declaration: ' + p.name, row.get('native_inspection') is True
              and ('entire' in row['region']), kind='record_validation_of_visual_attestation')
    visual_inventory.append({'path': row['path'], 'sha256': digest(raw),
        'native_dimensions': [width, height], 'full_file_bounds_xyxy': [0, 0, width, height],
        'recorded_inspected_region': row['region'],
        'actual_full_source_view_attestation': True,
        'bounds_basis': 'Filesystem dimensions establish full file bounds; actual delivery of the full source image is attested from the audit tool calls. A region in the report may restrict use, especially the photo left/middle columns.'})
for rec in card_records + panel_records:
    check('primary manifest image identity: ' + Path(rec['path']).name,
          by_visual[Path(rec['path']).name]['source_sha256'] == rec['sha256'])
check('31 core and 2 excluded card faces', Counter(by_visual[n]['scope'] for n in card_names)
      == {'original core': 31, 'excluded B&C exemplar': 2})
photo = read_json(ROOT / PANELS / 'independent-printed-photo-corroboration.json',
                  'machine validation of allowed dated photo provenance')
check('dated 2017 physical-photo identity provenance', any(
    x['image_id'] == 3635658 and x['postdate'] == '2017-07-15T04:08:20+00:00'
    and x['sha256'] == by_visual['corroborating-all-spirits-2017.jpg']['source_sha256']
    for x in photo['sources']),
    'Verifies recorded provenance and source identity, not the independent truth of the historical publication date.')
check('photo use restricted to original eight',
      'left/middle eight' in by_visual['corroborating-all-spirits-2017.jpg']['region'],
      kind='record_validation_of_visual_attestation')

pdf_raw = read(ROOT / 'source_pdfs/spirit-island-rules.pdf', 'original PDF hash/render provenance verification')
check('original CORE PDF exact hash', digest(pdf_raw) == PDF_SHA)
doc = fitz.open(stream=pdf_raw, filetype='pdf')
check('CORE has 32 physical pages', len(doc) == 32)
for page in [6, 7, 17, 32]:
    row = by_visual['audit08-core-p' + str(page).zfill(2) + '.png']
    regenerated = doc[page - 1].get_pixmap(matrix=fitz.Matrix(1.7, 1.7)).tobytes('png')
    check('direct PDF render reproducible: printed ' + str(page),
          digest(regenerated) == row['sha256'] and row['source_sha256'] == PDF_SHA
          and row['source_path'] == 'source_pdfs/spirit-island-rules.pdf'
          and row['page'] == page and row['direct_render_and_inspection'] is True)
    labels = [line.strip() for line in doc[page - 1].get_text().splitlines() if line.strip().isdigit()]
    if page != 32:
        check('printed page numeral present: ' + str(page), str(page) in labels,
              'Machine text extraction checks the printed numeral; full-page visual reading remains an attestation.')
    else:
        check('back-cover printed-page-32 position and headings', len(doc) == 32
              and 'ICONOGRAPHY' in doc[31].get_text() and 'TURN ORDER' in doc[31].get_text(),
              'Back cover has no printed 32 numeral. Identified as physical page 32 after numbered page 31; complete render matches exact preserved hash.')
legend_pdf = read(B / 'card-scope-source/branch-claw-rulebook.pdf', 'publisher legend PDF source hash verification')
legend = by_visual['branch-claw-rulebook-p6.png']
check('publisher legend original PDF hash/page',
      digest(legend_pdf) == legend['source_pdf_sha256'] and legend['page'] == 6)
legend_doc = fitz.open(stream=legend_pdf, filetype='pdf')
legend_render = legend_doc[5].get_pixmap(matrix=fitz.Matrix(1.4, 1.4)).tobytes('png')
with Image.open(io.BytesIO(legend_render)) as rendered, Image.open(ROOT / legend['path']) as supplied:
    check('publisher legend dimensions and membership region exactly reproduce',
          rendered.size == supplied.size and rendered.convert('RGB').crop((0, 0, rendered.width, 600)).tobytes()
          == supplied.convert('RGB').crop((0, 0, supplied.width, 600)).tobytes(),
          'Top 600 pixels include the expansion-symbol membership legend and reproduce exactly.')
    from PIL import ImageChops, ImageStat
    difference = ImageChops.difference(rendered.convert('RGB'), supplied.convert('RGB'))
    check('publisher legend complete PNG byte reproducibility', digest(legend_render) == legend['source_sha256'],
          {'supplied_png_sha256': legend['source_sha256'], 'regenerated_png_sha256': digest(legend_render),
           'decoded_difference_bbox': difference.getbbox(),
           'mean_absolute_channel_difference': ImageStat.Stat(difference).mean,
           'assessment': 'Nonblocking reproducibility diagnostic: original supplied source hash and PDF hash are correct; dimensions and expansion-symbol prose region match exactly. Tiny differences occur only in the lower illustrative component image, outside the membership legend. Original is preserved.'},
          'nonblocking_render_diagnostic')

for group in audit['checked_groups']:
    for ref in group['sources']:
        raw = (ROOT / ref['path']).read_bytes()
        txt = raw.decode('utf-8')
        check('checked-group anchor exact: ' + group['group'] + ':' + str(ref['start']),
              digest(raw) == ref['source_sha256']
              and txt[ref['start']:ref['end']] == ref['passage'])
check('zero unresolved source findings recorded', audit['verdict'] == 'PASS'
      and audit['findings'] == [] and audit['finding_counts'] == {'MAJOR': 0, 'MINOR': 0, 'total': 0},
      'Validates existing report state only; this is not a new rules verdict.')
check('independence declarations match', audit['independence_statement'] == ledger['independence_statement'])
for declaration in ['no repair authorship', 'No question bank', 'No delegation',
                    'identity_proof reviewer link', 'Candidate and canonical were not edited']:
    check('independence declaration: ' + declaration,
          declaration in audit['independence_statement'], kind='record_validation_of_independence_attestation')
# Exact frozen bytes after every machine check ensure this validator preserved inputs.
for name in EXPECTED:
    check('artifact preserved: ' + name, (B / name).read_bytes() == artifact_bytes[name])
check('canonical preserved', canonical_path.read_bytes() == canonical)
result = {
    'purpose': 'Evidence-validation follow-up only; no repair, new rules review, or new source verdict.',
    'prior_execution_notes': ['Initial validator run stopped on an incorrect repository-root calculation before a nonexistent canonical path could be opened. Corrected root from B.parents[5] to B.parents[4]; no input or audit artifacts were modified.', 'First complete validation run reported 511 checks with two failures: absent back-cover numeral 32, and nonidentical full legend PNG regeneration. Back-cover position is now checked explicitly; legend mismatch remains a disclosed nonblocking diagnostic with exact membership-region comparison.'],
    'validation_status': 'FAIL' if errors else ('PASS_WITH_EXCEPTION' if diagnostics else 'PASS'),
    'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'validator': {'path': str(Path(__file__).resolve()),
                  'sha256': digest(Path(__file__).read_bytes())},
    'frozen_artifact_sha256': {n: digest(data) for n, data in artifact_bytes.items()},
    'counts': {'checks': len(checks), 'failed_checks': sum(not x['passed'] for x in checks),
               'blocking_failed_checks': len(errors), 'nonblocking_diagnostics': len(diagnostics),
               'successful_text_slices': len(reads), 'text_inputs': len(by_path),
               'visual_sources': len(visual_rows), 'card_faces': len(card_names),
               'native_spirit_panels': len(panel_names)},
    'exceptions': errors + diagnostics,
    'attestation_limits': [
        'Filesystem checks prove exact bytes, hashes, UTF8 slice coverage, bounds, dimensions, records, reproducible renders and named input inventory.',
        'Actual historical tool output caps, absence of transport truncation, one slice per response, receiving/reading the text, and full native visual display are audit-session attestations. This validator checks their recorded fields and does not claim filesystem proof of human/model perception or transport.',
        'Independence and absence of unrecorded prohibited consultation are auditor declarations, not facts this filesystem validator can prove. No runtime logs, other-agent results, questions, keys, maps, readers, grades or history were accessed for validation.',
        'The canonical was machine-compared as bytes only and is not claimed as a fresh model-delivered rules text input. Own artifacts and sources were machine-parsed for validation, not newly read as rules authority.',
        'The physical photograph was displayed as a whole image, but only its left/middle original-eight panels were used. The crop corroborates the original Bringer track. Exact fine print comes from the native panels and official sources.',
    ],
    'checks': checks, 'text_inventory': text_inventory,
    'visual_inventory': visual_inventory, 'machine_read_access': read_access,
    'render_provenance': {'library': 'PyMuPDF ' + fitz.VersionBind,
                          'core_matrix': [1.7, 1.7], 'core_pages_one_based': [6, 7, 17, 32],
                          'legend_matrix': [1.4, 1.4], 'legend_page_one_based': 6,
                          'method': 'Full page get_pixmap, PNG bytes compared exactly to preserved artifact hash.'},
}
output = B / 'source-audit08-delivery-validation.json'
output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'validation_status': result['validation_status'], 'counts': result['counts'],
                  'exceptions': errors + diagnostics, 'output': str(output)}))
raise SystemExit(bool(errors))
