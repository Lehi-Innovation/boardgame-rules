"""Preserve primary judgments and bind one neutral overlay/source continuation."""
from pathlib import Path
from collections import Counter
import json
import hashlib

R = Path(__file__).parent.resolve()
IT = R / 'expanded-iteration-04'
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
overlay_path = IT / 'adjudicated-grades-aggregate.json'
source_path = R / 'source-review/source15-freeze17-full-new-input-own-reuse-validation.json'
assert not overlay_path.exists() and not source_path.exists()
assert read(IT / 'neutral21-case-integrity-validation.json')['pass']
assert read(IT / 'bookkeeping-audit-23.json')['technical_pass']
primary = read(IT / 'original-grades-aggregate.json')
neutral = read(IT / 'neutral21-adjudication.json')
assess = {(x['question_id'], x['reader_label']): (i, x) for i, x in enumerate(neutral['assessments'])}
rows, overlays = {}, []
for label, entries in primary['readers'].items():
    rows[label] = []
    for entry in entries:
        value = {'id': entry['id'], 'primary_grade': entry['grade'], 'effective_grade': entry['grade'],
                 'primary_report_path': entry['report_path'], 'primary_report_sha256': entry['report_sha256'],
                 'primary_json_pointer': entry['json_pointer'],
                 'primary_unsupported_claim_flags': entry['unsupported_claim_flags'],
                 'effective_unsupported_claim_flags': entry['unsupported_claim_flags']}
        if (entry['id'], label) in assess:
            n, assessment = assess[(entry['id'], label)]
            value.update(effective_grade=assessment['grade'],
                         effective_unsupported_claim_flags=len(assessment['unsupported_correct_claim_flags']),
                         neutral_json_pointer=f'/assessments/{n}')
            overlays.append({'reader': label, **value,
                             'neutral_report_path': str(IT / 'neutral21-adjudication.json'),
                             'neutral_report_sha256': sha(IT / 'neutral21-adjudication.json')})
        rows[label].append(value)
totals = {label: dict(Counter(e['effective_grade'] for e in entries)) for label, entries in rows.items()}
assert totals == {'a': {'correct': 164, 'partial': 4}, 'b': {'correct': 167, 'partial': 1}}
overlay = {'iteration': IT.name, 'question_count': 168,
           'original_primary_aggregate_path': str(IT / 'original-grades-aggregate.json'),
           'original_primary_aggregate_sha256': sha(IT / 'original-grades-aggregate.json'),
           'primary_totals': primary['totals'], 'totals': totals, 'readers': rows, 'overlays': overlays,
           'neutral_count': 1, 'neutral_original_whole_entries': 4,
           'neutral_case_integrity_path': str(IT / 'neutral21-case-integrity-validation.json'),
           'independent_bookkeeping_audit_path': str(IT / 'bookkeeping-audit-23.json'),
           'independent_bookkeeping_scope': 'Complete primary bookkeeping only; neutral excluded from that audit and separately validated.',
           'unsupported_correct_claim_count': sum(e['effective_unsupported_claim_flags'] for v in rows.values() for e in v),
           'original_primary_reports_and_flags_preserved': True, 'originals_modified': False,
           'all_ids_once_per_reader': True, 'both_readers_all_correct': False, 'final_scope_readiness': False,
           'remaining_substantive_cases': [{'reader': label, 'id': e['id'], 'grade': e['effective_grade']}
                                         for label, entries in rows.items() for e in entries if e['effective_grade'] != 'correct'],
           'source_wide_or_background_caps_applied': False}

receipt = read(R / 'source-review/source-only-delivery-15-freeze17.json')
reuse = receipt['own_unchanged_source_reuse']
policy = read(R / 'source-review/source-scope-16.json')
full_proof = R / 'source-review/source15-freeze17-runtime-delivery-validation-01.json'
spot_proof = R / 'source-review/source15-freeze17-selected-spot-validation-01.json'
prior = R / 'source-review/source15-freeze16-full-new-input-reuse-validation.json'
initial = R / 'source-review/source15-runtime-delivery-validation-01.json'
assert all(read(p)['pass'] for p in [full_proof, spot_proof, prior, initial])
assert reuse['fresh_independent_vote'] is False
for key in ['own_prior_completed_source_receipt', 'own_original_receipt_binding']:
    item = reuse[key]
    assert sha(Path(item['path'])) == item['sha256']
pins = []
for name, pin in policy['pins'].items():
    path = Path(name)
    assert sha(path) == pin['sha256'] and path.stat().st_size == pin['bytes']
    pins.append({'path': name, **pin, 'matches': True})
manifest = next(Path(p) for p in policy['pins'] if p.endswith('original-alien-sheet-provenance.json'))
assets = read(manifest)['assets']
visuals = reuse['reused_original50_payload_visuals']
assert len(assets) == len(visuals) == 50
images = []
for asset in assets:
    item = next(x for x in visuals if x['alien'] == asset['alien'])
    path = Path(asset['original_file'])
    assert str(path) == item['path']
    assert sha(path) == asset['original_sha256'] == item['returned_decoded_sha256'] == item['current_file_sha256']
    assert path.stat().st_size == asset['expected_size'] == item['returned_decoded_bytes']
    assert item['returned_dimensions'] == [asset['width'], asset['height']]
    assert item['forwarded_detail'] == 'original' and item['inspection_reused'] is True and item['newly_transported'] is False
    images.append({'alien': asset['alien'], 'path': str(path), 'sha256': sha(path),
                   'bytes': path.stat().st_size, 'dimensions': item['returned_dimensions'],
                   'own_original_verified_payload_reused': True})
for item in reuse['reused_original_texts'].values():
    assert sha(Path(item['path'])) == item['sha256']
item = reuse['reused_later_publisher_text']
assert sha(Path(item['path'])) == item['sha256']
item = reuse['reused_later_p16_payload_visual']
assert sha(Path(item['path'])) == item['returned_decoded_sha256']
assert Path(item['path']).stat().st_size == item['returned_decoded_bytes']
audit = read(R / 'source-review/source-only-audit-15-freeze17.json')
assert audit['source_verdict'] == 'PASS' and audit['summary']['sha256'] == sha(R / 'repair-freeze-17.md')
assert len(audit['all_50_alien_mapping']) == 50
source = {'pass': True, 'task': '/root/source_only_auditor_15', 'new_full_text_inputs': 2,
          'new_actual_full_text_chunks': 11, 'new_selected_primary_spot_characters': 164,
          'new_full_input_proof_path': str(full_proof), 'selected_spot_proof_path': str(spot_proof),
          'prior_own_union_proof_path': str(prior), 'prior_own_union_proof_sha256': sha(prior),
          'original_full_source_and_fifty_actual_native_payload_proof': str(initial),
          'original_proof_sha256': sha(initial), 'all_scope_pins': pins,
          'fifty_unchanged_original_payload_reuse': images,
          'fresh_independent_vote': False, 'new_fifty_native_inspection_claimed': False,
          'audit_sha256': sha(R / 'source-review/source-only-audit-15-freeze17.json'),
          'guide_sha256': sha(R / 'repair-freeze-17.md'),
          'source_scope_sha256': sha(R / 'source-review/source-scope-16.json'),
          'publication_or_global_qa_approval_inferred': False}
overlay_path.write_text(json.dumps(overlay, indent=2) + '\n')
source_path.write_text(json.dumps(source, indent=2) + '\n')
print({'effective_totals': totals, 'source17_own_reuse_pass': True, 'originals_modified': False})
