#!/usr/bin/env python3
"""Validate delivery/reuse evidence only; write one separate validation JSON."""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
from PIL import Image

B = Path(__file__).resolve().parent
OUT = B / 'working-sweeps39-40-delivery-validation.json'
EXPECTED = {
    'working-source-sweeps-39-40.json': '428e4f5fe301869c7419deadfda9cb9da4f6125cca698be88ba8764dc1fdeda3',
    'working-source-sweeps-39-40-read-ledger.json': '7ed3821cb67400a7f5faccd8f2f7da626275a90019f122b80e3c4a672bf9c25f',
}
checks = []
disclosures = []

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def read(path):
    return json.loads(Path(path).read_text())

def canon(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())

def check(ok, name, **details):
    checks.append({'check': name, 'passed': bool(ok), **details})

def contiguous(ranges, length):
    ranges = sorted(set(map(tuple, ranges)))
    return bool(ranges) and ranges[0][0] == 0 and ranges[-1][1] == length and all(
        ranges[i][1] == ranges[i + 1][0] for i in range(len(ranges) - 1)
    )

def text_row(row, label, number):
    original = Path(row['path'])
    path = original
    if sha(path) != row['original_byte_sha256']:
        saved = row.get('historical_original_preserved_at')
        if saved and Path(saved).is_file() and sha(saved) == row['original_byte_sha256']:
            path = Path(saved)
            item = {'kind': 'historical_README_version_resolved', 'ledger': label, 'original_path': str(original), 'preserved_original_path': str(path), 'sha256': sha(path)}
            if item not in disclosures:
                disclosures.append(item)
    raw = path.read_bytes()
    text = raw.decode('utf-8')
    start, end = row['range']
    valid = (
        digest(raw) == row['original_byte_sha256']
        and len(text) == row['character_length']
        and 0 <= start < end <= len(text)
        and end - start <= 6000
        and row['max_output_tokens'] >= 4000
        and digest(text[start:end].encode()) == row['slice_utf8_sha256']
    )
    successful = row.get('delivery_status') != 'attempted_blank_tool_output_not_counted_as_delivered'
    if successful:
        valid = valid and 'no tool truncation observed' in row['truncation_check'].lower()
    check(valid, 'text_bytes_unicode_length_slice_hash_bounds_cap_and_delivery_record', ledger=label, row=number, path=str(original), range=[start, end], counted_as_successful=successful)
    return len(text)

def text_groups(rows, label, require_complete=False):
    groups = defaultdict(list)
    for i, row in enumerate(rows, 1):
        length = text_row(row, label, i)
        groups[(row['path'], row['original_byte_sha256'], length)].append(row['range'])
    results = []
    for (path, version, length), ranges in groups.items():
        full = contiguous(ranges, length)
        if require_complete:
            check(full, 'prior_complete_text_version_contiguity', ledger=label, path=path, sha256=version)
        results.append({'path': path, 'sha256': version, 'character_length': length, 'ranges': ranges, 'complete_contiguous': full})
    return results

def image_row(row, label):
    path = Path(row['path'])
    with Image.open(path) as picture:
        dimensions = list(picture.size)
        picture.verify()
    recorded = row.get('native_dimensions', row.get('dimensions'))
    if 'full_view_region_xyxy' in row:
        regions = [row['full_view_region_xyxy']]
    elif 'viewed_region' in row:
        regions = [row['viewed_region']]
    else:
        regions = [item['bounds_xyxy'] for item in row.get('viewed_regions', [])]
    marked_full = row.get('fully_viewed_this_sweep', row.get('inspection_complete', row.get('fully_viewed', False)))
    check(sha(path) == row['original_byte_sha256'] and dimensions == recorded and [0, 0, *dimensions] in regions and marked_full,
          'native_image_bytes_decode_dimensions_fullbounds_and_fullview_record', ledger=label, path=str(path), dimensions=dimensions)

report_path = B / 'working-source-sweeps-39-40.json'
ledger_path = B / 'working-source-sweeps-39-40-read-ledger.json'
for name, expected in EXPECTED.items():
    check(sha(B / name) == expected, 'working_original_exact_hash', path=str(B / name), expected_sha256=expected, actual_sha256=sha(B / name))
report = read(report_path)
ledger = read(ledger_path)
check(report['read_ledger']['sha256'] == sha(ledger_path), 'report_exact_read_ledger_binding')
current_groups = text_groups(ledger['text_reads'], str(ledger_path))
check(len(ledger['text_reads']) == 16, 'sixteen_successful_current_text_records')

prior = {}
prior_summaries = []
for binding in ledger['immutable_reuse_bindings']:
    path = Path(binding['path'])
    check(sha(path) == binding['sha256'], 'immutable_own_reuse_ledger_hash', path=str(path), sha256=binding['sha256'])
    value = read(path)
    prior[str(path)] = value
    # Working37/38 intentionally includes targeted rereads; other earlier ledgers
    # completely delivered each source version appearing in their text_reads.
    full = path.name != 'working-source-sweeps-37-38-read-ledger.json'
    prior_summaries.append({'ledger_path': str(path), 'sha256': sha(path), 'text_versions': text_groups(value.get('text_reads', []), str(path), full)})

sources = ledger['complete_reused_text_source_bindings']
source_paths = {source['path'] for source in sources}
for source in sources:
    path = Path(source['path'])
    text = path.read_bytes().decode('utf-8')
    check(sha(path) == source['sha256'] and len(text) == source['character_length'], 'complete_reused_source_byte_and_length_identity', path=str(path))
    rows = []
    for binding in source['full_original_rows_in']:
        check(sha(binding['path']) == binding['original_byte_sha256'], 'complete_source_original_ledger_hash', source=str(path), ledger=binding['path'])
        value = prior.get(binding['path']) or read(binding['path'])
        rows.extend(row for row in value['text_reads'] if row['path'] == str(path) and row['original_byte_sha256'] == source['sha256'])
    for i, row in enumerate(rows, 1):
        text_row(row, 'bound original source rows: ' + str(path), i)
    ranges = [row['range'] for row in rows]
    check(contiguous(ranges, len(text)) and len(set(map(tuple, ranges))) == source['slice_count'] and source['complete_range'] == [0, len(text)],
          'complete_reuse_bound_to_actual_contiguous_original_rows', path=str(path), original_slice_count=source['slice_count'])

for group in current_groups:
    if group['path'] not in source_paths:
        check(group['complete_contiguous'], 'new_input_complete_contiguous_delivery', path=group['path'])
    elif not group['complete_contiguous']:
        disclosures.append({'kind': 'intentional_targeted_primary_reread', 'path': group['path'], 'ranges': group['ranges'], 'note': 'Prior complete source delivery verified through exact original ledger rows, hashes, caps and contiguity; no new whole-file claim.'})

exceptions = ledger.get('delivery_exceptions', [])
check(len(exceptions) == 1, 'exactly_one_recorded_blank_payload_attempt')
recovery = []
for i, attempt in enumerate(exceptions, 1):
    text_row(attempt, 'failed attempts, not deliveries', i)
    matches = [row for row in ledger['text_reads'] if row['path'] == attempt['path'] and row['range'] == attempt['range'] and row['slice_utf8_sha256'] == attempt['slice_utf8_sha256'] and row['original_byte_sha256'] == attempt['original_byte_sha256']]
    ok = (attempt['delivery_status'] == 'attempted_blank_tool_output_not_counted_as_delivered'
          and attempt not in ledger['text_reads'] and attempt['resolved'] and len(matches) == 1
          and 'no tool truncation observed' in matches[0]['truncation_check'].lower())
    check(ok, 'blank_attempt_excluded_exact_interval_successfully_redelivered_once', path=attempt['path'], range=attempt['range'])
    recovery.append({'path': attempt['path'], 'range': attempt['range'], 'slice_sha256': attempt['slice_utf8_sha256'], 'failed_chunk_id': attempt['tool_chunk_id'], 'successful_chunk_id_from_agent_transport_attestation': '019f09', 'excluded_from_successful_count': True, 'matching_successful_records': len(matches)})
check(not any(row.get('delivery_status') == 'attempted_blank_tool_output_not_counted_as_delivered' for row in ledger['text_reads']), 'no_failed_attempt_counted_as_successful_text')

for row in ledger['image_reads']:
    image_row(row, str(ledger_path))
check(len(ledger['image_reads']) == len({row['path'] for row in ledger['image_reads']}) == 10, 'ten_unique_current_native_fullview_records')
original_image_rows = []
for path, value in prior.items():
    for row in value.get('image_reads', []):
        image_row(row, path)
        if Path(path).name in ['scope-coverage-10-read-ledger.json', 'original-panel-audit-01-read-ledger.json']:
            original_image_rows.append(row)
image_binding = ledger['reused_image_corpus_binding']
check(len(original_image_rows) == image_binding['row_count'] == 52 and canon(original_image_rows) == image_binding['exact_rows_canonical_sha256'], 'exact_52_row_full_original_image_corpus_binding')
for binding in image_binding['full_original_rows_in']:
    check(sha(binding['path']) == binding['sha256'], 'full_native_image_original_ledger_hash', **binding)

# Rebuild the model-delivered prior169 route, then permit ONLY the explicit Q84
# two-string map precision and the exact newQ170 object for each current file.
v16 = read(B / 'panel-audit-bank-supplement-v16.json')
v18 = read(B / 'working-pass-v18-supplement.json')
v19 = read(B / 'working-pass-v19-supplement.json')
q18 = read(B / 'expanded-v16/key-corrections.json')[0]
q157 = v18['inherited163_equivalence']['Q157_explicit_correction'][0]
schemes = {
    'questions.json': ('questions', 'questions', 'complete6_question_objects', 'complete_new_question_objects'),
    'answer-key.json': ('answers', 'answer_key', 'complete6_key_objects', 'complete_new_key_objects'),
    'asked-fact-map.json': ('questions', 'asked_fact_entries', 'complete6_asked_map_objects', 'complete_new_asked_map_objects'),
}
def differences(left, right, prefix=''):
    if type(left) != type(right):
        return [prefix]
    if isinstance(left, dict):
        if set(left) != set(right):
            return [prefix + '.keys']
        return [p for key in left for p in differences(left[key], right[key], prefix + '.' + key)]
    if isinstance(left, list):
        if len(left) != len(right):
            return [prefix + '.length']
        return [p for i, (a, b) in enumerate(zip(left, right)) for p in differences(a, b, prefix + f'[{i}]')]
    return [] if left == right else [prefix]

precision = v19['explicit_Q84_map_precision']
map_delta = differences(precision['old_map'], precision['new_map'])
check(map_delta == ['.requested_clauses[0].required_facts[0]', '.requested_clauses[0].required_facts[1]'], 'Q84_only_two_explicit_map_string_changes', actual_diff_paths=map_delta)
check(precision['old_question'] == precision['new_question'] and precision['old_key'] == precision['new_key'], 'Q84_question_and_key_unchanged')
reconstruction = {}
for name, (main, add16, add18, add19) in schemes.items():
    base = read(B / 'expanded-v15' / name)[main] + v16[add16] + v18[add18]
    if name != 'questions.json':
        base = [q18['new_key' if name == 'answer-key.json' else 'new_mapping'] if row['id'] == 'Q18' else row for row in base]
    if name != 'answer-key.json':
        base = [q157['new_question' if name == 'questions.json' else 'new_mapping'] if row['id'] == 'Q157' else row for row in base]
    old = read(B / 'expanded-v18' / name)[main]
    check(base == old and len(base) == 169, 'exact_prior169_all_fields_reconstruction', filename=name)
    expected_prefix = base
    if name == 'asked-fact-map.json':
        check(next(row for row in base if row['id'] == 'Q84') == precision['old_map'], 'prior_Q84_map_matches_delivered_old_object')
        expected_prefix = [precision['new_map'] if row['id'] == 'Q84' else row for row in base]
    objects = expected_prefix + v19[add19]
    path = B / 'expanded-v19' / name
    current = read(path)[main]
    check(objects == current and current[:169] == expected_prefix and current[169:] == v19[add19] and len(current) == 170 and [row['id'] for row in current] == [f'Q{i:02}' for i in range(1, 171)], 'exact170_all_fields_prefix_delta_newQ170_and_order', filename=name)
    current_hash = sha(path)
    check(current_hash == v19['full_bank_sha256'][name] == report['current_input_hashes'][str(path)], 'current170_original_byte_hash_matches_delivered_packet_and_report', path=str(path), sha256=current_hash)
    check(canon(objects) == ledger['exact_current_bank_reconstruction'][name]['reconstructed170_canonical_sha256'] == report['exact170_reconstruction_proof'][name]['current170_canonical_sha256'], 'canonical_object_hash_matches_existing_report_ledger_proof', filename=name)
    reconstruction[name] = {'path': str(path), 'current_full_file_sha256': current_hash, 'reconstructed_prior169_canonical_sha256': canon(base), 'reconstructed170_canonical_sha256': canon(objects), 'current170_canonical_sha256': canon(current), 'all_fields_object_equality': objects == current, 'object_count': len(current), 'permitted_prior_delta': map_delta if name == 'asked-fact-map.json' else []}
    if name == 'asked-fact-map.json':
        oldfacts = sum(len(c['required_facts']) for row in old for c in row['requested_clauses'])
        facts = sum(len(c['required_facts']) for row in current for c in row['requested_clauses'])
        newfacts = sum(len(c['required_facts']) for row in v19[add19] for c in row['requested_clauses'])
        check(oldfacts == 504 and facts == 505 and newfacts == 1, '504_to505_only_one_new_Q170_required_fact', old=oldfacts, current=facts, new=newfacts)
        reconstruction[name]['required_fact_count'] = facts

check([p['pass_number'] for p in report['passes']] == [39, 40] and all(p['new_question_count'] == 0 and p['complete_remaining_gaps'] == [] for p in report['passes']), 'both_recorded_actual_working_pass_results_zero_with_empty_gapsets')
check(report['actual_ask_IDs_compared'] == [f'Q{i:02}' for i in range(1, 171)] and all(p['source_families'] for p in report['passes']), '170_ordered_ask_IDs_and_source_family_records_present')
credit = B / 'expanded-v19/core-scope-credit.json'
check(sha(credit) == v19['full_bank_sha256'][credit.name], 'scope_credit_byte_hash_only_no_content_consultation', path=str(credit))
for path, expected in {**report['preserved_inputs'], **report['current_input_hashes'], **{str(B / n): h for n, h in EXPECTED.items()}}.items():
    check(sha(path) == expected, 'original_input_report_or_bank_still_unchanged', path=path, expected_sha256=expected)

source_note_path = B / 'working-sweeps39-40-dread-source-check.json'
source_note = read(source_note_path)
original_image_path = Path(source_note['source']['path'])
aid_path = Path(source_note['inspection_enlargement']['path'])
check(sha(original_image_path) == source_note['source']['original_byte_sha256'] == '4a8523619e8f8ba4ee4791401346b5a019ce904371bff620d820ad194dff848b', 'disputed_source_reinspection_binds_exact_original_native_bytes')
with Image.open(original_image_path) as picture:
    original_pixels = picture.convert('RGB')
with Image.open(aid_path) as picture:
    aid_pixels = picture.convert('RGB')
expected_pixels = original_pixels.resize((1200, 1680), Image.Resampling.NEAREST)
check(sha(aid_path) == source_note['inspection_enlargement']['sha256'] and expected_pixels.tobytes() == aid_pixels.tobytes() and original_pixels.tobytes() == aid_pixels.resize(original_pixels.size, Image.Resampling.NEAREST).tobytes(), 'inspection_aid_exact_nearest_neighbor_replication_and_roundtrip_pixel_equality')
check(source_note['preserved_original_artifacts'][str(report_path)] == sha(report_path) and source_note['preserved_original_artifacts'][str(ledger_path)] == sha(ledger_path), 'source_reinspection_note_preserves_raw_report_ledger_hashes')

disclosures.extend([
    {'kind': 'recovered_empty_payload', 'records': recovery, 'note': 'Failed attempt not counted. A matching successful exact-range/slice-hash record exists; actual tool-response delivery is separately agent-attested.'},
    {'kind': 'authorized_whole_bank_reuse', 'note': 'Current170 files checked programmatically; inherited complete model deliveries plus the complete new packet reconstruct all objects. No fresh whole-file model-delivery claim.'},
    {'kind': 'scope_credit_not_consulted', 'note': 'Only its raw-byte hash was checked.'},
])
result = {
    'task': 'Evidence validation only; no source sweep or novelty adjudication',
    'validator_path': str(Path(__file__).resolve()),
    'validator_sha256': sha(__file__),
    'status': 'PASS' if all(row['passed'] for row in checks) else 'FAIL',
    'status_scope': 'Delivery/reuse/object-reconstruction evidence only. No global coverage verdict.',
    'summary': {'checks': len(checks), 'passed': sum(row['passed'] for row in checks), 'failed': sum(not row['passed'] for row in checks), 'successful_current_text_records': len(ledger['text_reads']), 'failed_blank_attempts_excluded': len(exceptions), 'successful_exact_interval_retries': len(recovery), 'complete_new_external_inputs': 2, 'complete_new_input_slices': 4, 'targeted_primary_reread_slices': 12, 'current_native_fullviews': len(ledger['image_reads']), 'own_immutable_reuse_ledgers': len(prior), 'complete_reused_text_bindings': len(sources), 'original_full_image_corpus_rows': len(original_image_rows), 'current_questions': 170, 'current_required_facts': 505, 'pass39_new_questions': 0, 'pass40_new_questions': 0},
    'working_artifact_hashes': EXPECTED,
    'current_text_groups': current_groups,
    'prior_ledger_validation': prior_summaries,
    'exact170_reconstruction': reconstruction,
    'separate_source_annotation_reinspection': {'path': str(source_note_path), 'sha256': sha(source_note_path), 'finding': 'The separate printed1Fear effect was confirmed by native visual reinspection; no false erratum or raw-artifact change. Visual reading is agent-attested; aid pixel equivalence is machine-checked.'},
    'delivery_exceptions_and_disclosures': disclosures,
    'machine_check_limit': 'Filesystem checks validate exact bytes, Unicode slices/caps/contiguity, recorded no-truncation/full-view status, image decode/dimensions/bounds and object equivalence. Actual one-slice-per-response transport and semantic visual inspection are agent tool-history attestations, not independently replayed by this helper. The zero results are validated as accurately recorded, not independently proved as semantic coverage completeness.',
    'transport_attestations': {'blank_failed_chunk': '7211ae', 'successful_exact_interval_chunk': '019f09', 'originals_preserved': True},
    'checks': checks,
    'preservation': 'This helper writes only its separate validation JSON. No original report/ledger, bank, canonical/C19, primary source, or earlier audit is written. Canonical/C19 was not opened.',
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'summary': result['summary'], 'validator_path': result['validator_path'], 'validation_path': str(OUT), 'validation_sha256': sha(OUT), 'failed_checks': [row for row in checks if not row['passed']]}, indent=2))
raise SystemExit(0 if result['status'] == 'PASS' else 1)
