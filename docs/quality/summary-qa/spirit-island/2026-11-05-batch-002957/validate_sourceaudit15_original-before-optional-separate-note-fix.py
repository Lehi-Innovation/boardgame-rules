"""Verify original source15 identity, full delivery, references and source pixels."""
from pathlib import Path
from functools import lru_cache
import collections
import hashlib
import json
import fitz
from PIL import Image
from bs4 import BeautifulSoup

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
load = lambda p: json.loads(Path(p).read_text())
@lru_cache(None)
def H(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
checks = []
def ck(ok, label):
    assert ok, label
    checks.append({'check': label, 'pass': True})

r = load(B / 'source-audit-final-15.json')
l = load(B / 'source-audit-final-15-read-ledger.json')
v = load(B / 'source-audit-final-15-visual-manifest.json')
freeze = load(B / 'source-audit15-original-freeze.json')
actual = load(B / 'source-audit15-original-actual-delivery-validation.json')
profile = load(B / 'runtime/final_source_audit_15-final-completed-projection.json')
primary = load(B / 'source-manifest.json')['paths_and_sha256']
supp = load(B / 'supplemental-source-manifest-v4.json')['source_records']
ck(r['candidate_sha256'] == H(ROOT / r['candidate_path']) == H(B / 'source-candidate-26.md') == H(ROOT / 'rules/spirit-island.md') == 'ce8f1d645f466686ae2e75fcd29130fa89cbb1c4963d981090e3768a526a6fd1', 'exact C26 candidate binding')
for name, row in freeze['files'].items():
    ck(H(B / name) == row['sha256'] == H(row['original_completed_copy']), 'entire frozen original unchanged ' + name)
ck(profile['confirmed_settings'] == [{'model': 'gpt-6.1-sol', 'effort': 'high'}] and profile['requested_spawn']['fields']['fork_turns'] == 'none', 'one actual initially fresh proper model context')
ck(actual['verified'] and actual['candidate_sha256'] == r['candidate_sha256'] and actual['text_sources'] == 16 and actual['actual_distinct_text_range_deliveries'] == 92 and actual['unique_visual_sources'] == actual['public_image_blocks'] == 57 and actual['one_source_range_per_matched_output_event'], 'strict actual original-prefix16/92/57 public delivery proof')
ck(actual['record_cutoff_exclusive'] == 653 and actual['original_boundary_sha256'] == H(B / 'source-audit15-original-completed-runtime-boundary.json'), 'fixed original completed runtime boundary')
allowed = {(ROOT / p).resolve() for p in primary} | {(ROOT / row['path']).resolve() for row in supp}
allowed |= {(B / name).resolve() for name in ['source-manifest.json', 'supplemental-source-manifest-v4.json', 'source-candidate-26.md']}
for path, digest in primary.items():
    ck(H(ROOT / path) == digest, 'original manifest primary hash ' + Path(path).name)
for row in supp:
    ck(H(ROOT / row['path']) == row['sha256'], 'supplemental primary hash ' + Path(row['path']).name)

derived = l['derived_prose']
source = (ROOT / derived['source']).resolve()
target = (ROOT / derived['derived_path']).resolve()
ck(source in allowed and H(source) == derived['source_sha256'], 'independent publisher prose primary identity')
soup = BeautifulSoup(source.read_text(), 'html.parser')
for element in soup(['script', 'style', 'noscript', 'template']):
    element.decompose()
prose = soup.get_text('\n', strip=True)
ck(prose == target.read_text() and len(prose) == derived['chars'] == 4329 and H(target) == derived['sha256'], 'documented complete publisher visible prose independently reproduced')
ck(target.is_relative_to(B) and target.exists(), 'derived prose permanently within owned evidence')
allowed.add(target)

parts = collections.defaultdict(list)
for item in l['source_delivery']:
    p = (ROOT / item['path']).resolve()
    text = p.read_text()
    a, z = item['start'], item['end']
    ck(p in allowed and H(p) == item['source_sha256'] and len(text) == item['character_length'], 'allowed exact whole text identity ' + p.name)
    ck(isinstance(a, int) and isinstance(z, int) and 0 <= a < z <= len(text) and z - a <= 6000 and hashlib.sha256(text[a:z].encode()).hexdigest() == item['slice_sha256'], 'literal bounded source slice ' + p.name + str([a, z]))
    ck(isinstance(item['output_cap'], int) and item['output_cap'] >= 4000 and item['truncated'] is False, 'declared sufficient cap and no truncation ' + p.name)
    parts[item['path']].append(item)
ck(len(parts) == len(l['sources']) == 16 and len(l['source_delivery']) == 92, 'all16 complete source files and92 ranges')
ck({Path(p).name for p in parts} == {'source-manifest.json', 'supplemental-source-manifest-v4.json', 'source-candidate-26.md', 'spirit-island-rules.txt', 'living-faq-core-game.txt', 'living-faq-setup.txt', 'what-do-range-boosts-affect.txt', 'range-in-text-of-powers-that-target-spirits.txt', 'core-second-printing.txt', 'audit15-publisher-branch-claw-visible.txt', 'README.md', 'panel-download-map.json', 'download-integrity.json', 'independent-printed-photo-corroboration.json', 'novelty11-publisher-updates.txt', 'provenance.json'}, 'exact complete mandatory text inventory plus original source provenance')
for path, rows in parts.items():
    rows = sorted(rows, key=lambda row: row['start'])
    p = (ROOT / path).resolve()
    ck(rows[0]['start'] == 0 and rows[-1]['end'] == len(p.read_text()) and all(a['end'] == z['start'] for a, z in zip(rows, rows[1:])), 'whole contiguous source file ' + p.name)
    entry = next(row for row in l['sources'] if row['path'] == path)
    ck(entry['source_sha256'] == H(p) and entry['character_length'] == len(p.read_text()) and entry['slices'] == len(rows) and entry['contiguous_complete'] and entry['unicode_exact_decode'] and entry['truncation_checked'], 'declared full file identity ' + p.name)
ck(r['source_delivery'] == [{key: row[key] for key in ['path', 'start', 'end', 'source_sha256', 'slice_sha256', 'truncated']} for row in l['source_delivery']], 'report exact flat original source-delivery ledger')

images = v['images']
visual_by_path = {row['path']: row for row in images}
ck(len(visual_by_path) == len(images) == 57, 'all57 distinct original source views')
for image in images:
    p = (ROOT / image['path']).resolve()
    dimensions = list(Image.open(p).size)
    ck(H(p) == image['source_sha256'] and dimensions == image['dimensions'] and image['detail'] == 'original' and image['fully_received'] and bool(image['observations']) and bool(image['region']), 'whole original-detail image and observation ' + p.name)
panels = [row for row in images if '/original-spirit-panels/' in row['path'] and row['path'].endswith(('-front.png', '-back.png'))]
faces = [row for row in images if '/card-scope-source/' in row['path'] and row['path'].endswith('.jpg')]
ck(len(panels) == 16 and all(row['dimensions'] == [2697, 1797] and (ROOT / row['path']).stat().st_size == 19419092 for row in panels), 'all16 complete native unresized panels')
ck(len(faces) == 33 and v['printed_face_count'] == 33 and v['core_printed_face_count'] == 31 and v['excluded_BC_exemplar_count'] == 2, 'all33 printed faces31core2excluded exemplars')
ck(v['native_panel_count'] == 16 and v['all_images_forwarded_detail'] == 'original', 'declared mandatory native visual counts')
ck(bool(v['delivery_issue_resolved']), 'initial IPC failure and individual original-byte retransmission explicitly disclosed')
renders = sorted(v['pdf_render_provenance'], key=lambda row: row['render_order'])
ck([row['page_one_based'] for row in renders] == [6, 7, 17, 32] and [row['render_order'] for row in renders] == [1, 2, 3, 4], 'all four required independent CORE renders ordered')
with fitz.open(ROOT / renders[0]['pdf_path']) as document:
    for row in renders:
        ck(H(ROOT / row['pdf_path']) == row['pdf_sha256'] == primary['source_pdfs/spirit-island-rules.pdf'] and row['matrix_scale'] == [2, 2] and 'shared' in row['method'], 'exact documented original PDF matrix and shared-document method')
        pix = document[row['page_one_based'] - 1].get_pixmap(matrix=fitz.Matrix(*row['matrix_scale']), alpha=False)
        ck(hashlib.sha256(pix.tobytes('png')).hexdigest() == row['image_sha256'] == H(ROOT / row['path']) and [pix.width, pix.height] == [row['width'], row['height']], 'independent exact PNG byte reproduction page ' + str(row['page_one_based']))
        ck(row['path'] in visual_by_path, 'independently rendered CORE image actually in full visual ledger')

textrefs = visualrefs = exactrefs = withinrefs = 0
for group in r['checked_groups']:
    ck(bool(group['group']) and bool(group['scope_checked']) and bool(group['result']) and bool(group['sources'] or group['visual_sources']), 'explicit checked group scope and observations ' + group['group'])
    for ref in group['sources']:
        p = (ROOT / ref['path']).resolve()
        text = p.read_text()
        a, z = ref['start'], ref['end']
        ck(p in allowed and str(p.relative_to(ROOT)) in parts and H(p) == ref['source_sha256'], 'reference to fully read allowed primary source')
        ck(0 <= a < z <= len(text) and bool(ref['passage']) and ref['passage'] in text[a:z], 'literal cited primary passage and exact range')
        exactrefs += text[a:z] == ref['passage']
        withinrefs += text[a:z] != ref['passage']
        textrefs += 1
    for ref in group['visual_sources']:
        ck(ref['path'] in visual_by_path and H(ROOT / ref['path']) == ref['source_sha256'] and bool(ref['region']), 'reference to actual full native visual')
        visualrefs += 1
ck(len(r['checked_groups']) == 23 and textrefs == 97 and visualrefs == 65, 'all23 checked groups97text65visual references individually verified')

reconciled = r['supplemental_record_reconciliation']
ck(len(reconciled) == 72 and {row['record_index'] for row in reconciled} == set(range(72)), 'all72 supplemental records exactly indexed once')
for row in reconciled:
    original = supp[row['record_index']]
    ck((ROOT / row['path']).resolve() == (ROOT / original['path']).resolve() and row['source_sha256'] == original['sha256'] == H(ROOT / row['path']) and row['manifest_hash_matches'] and bool(row['disposition']) and bool(row['note']), 'exact supplemental identity and explicit disposition ' + str(row['record_index']))
ck(len(r['original_source_manifest_reconciliation']) == len(primary) == 7, 'all seven original manifest sources reconciled')
for row in r['original_source_manifest_reconciliation']:
    ck(row['path'] in primary and row['source_sha256'] == primary[row['path']] == H(ROOT / row['path']) and row['manifest_hash_matches'] and bool(row['role']), 'original primary manifest identity and role ' + Path(row['path']).name)

out = {
    'all_passed': True, 'counts': {'checks': len(checks), 'blocking_failed_checks': 0, 'text_files': 16, 'text_slices': 92, 'original_detail_views': 57, 'native_panels': 16, 'printed_faces': 33, 'checked_groups': 23, 'primary_text_references': textrefs, 'visual_references': visualrefs, 'supplemental_records': 72, 'exact_reproduced_CORE_renders': 4},
    'checks': checks,
    'frozen_artifact_sha256': {name: row['sha256'] for name, row in freeze['files'].items()},
    'original_transport_proof_sha256': H(B / 'source-audit15-original-actual-delivery-validation.json'),
    'source_reference_exact_range_matches': exactrefs, 'source_reference_quotations_within_larger_ranges': withinrefs,
    'actual_completed_model_profile': {'path': str(B / 'runtime/final_source_audit_15-final-completed-projection.json'), 'sha256': H(B / 'runtime/final_source_audit_15-final-completed-projection.json')},
    'candidate_sha256': r['candidate_sha256'], 'semantic_adoption': False,
    'limitations': 'Identity, exact transport, literal references and source-pixel reproduction are distinct from interpretation and cognition. All human observations/scopes/dispositions and semantic judgment require separate complete review; no source finding or original artifact changed.'
}
p = B / 'source-audit15-original-evidence-validation.json'
assert not p.exists()
p.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({key: value for key, value in out.items() if key != 'checks'}))
