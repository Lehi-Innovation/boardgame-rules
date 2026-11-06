#!/usr/bin/env python3
"""Read-only evidence validator; writes only its separate validation JSON."""
from pathlib import Path
from collections import defaultdict
import hashlib
import json
from PIL import Image

B = Path(__file__).resolve().parent
OUT = B / 'working-sweeps37-38-delivery-validation.json'
EXPECTED = {
    'working-source-sweeps-37-38.json': 'c828d4256d4a52e837868637e128222c9bc236badeb85717d89e6285b4ed856a',
    'working-source-sweeps-37-38-read-ledger.json': 'fd56b054edc356c3470d637978ba9f23b6b042cc51a69c8e77cfa4863ef7594e',
}
checks = []
exceptions = []

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def sha(path):
    return digest(Path(path).read_bytes())

def read(path):
    return json.loads(Path(path).read_text())

def require(condition, label, **details):
    checks.append({'check': label, 'passed': bool(condition), **details})

def complete(ranges, length):
    ranges = sorted(set(map(tuple, ranges)))
    return bool(ranges) and ranges[0][0] == 0 and ranges[-1][1] == length and all(
        ranges[i][1] == ranges[i + 1][0] for i in range(len(ranges) - 1)
    )

def validate_text_rows(rows, label, allow_partial=False):
    groups = defaultdict(list)
    summaries = []
    for number, row in enumerate(rows, 1):
        original_path = Path(row['path'])
        path = original_path
        if sha(path) != row['original_byte_sha256']:
            saved = row.get('historical_original_preserved_at')
            if saved and Path(saved).is_file() and sha(saved) == row['original_byte_sha256']:
                path = Path(saved)
                item = {
                    'kind': 'historical_source_version_resolved',
                    'ledger': label,
                    'original_path': str(original_path),
                    'preserved_original_path': str(path),
                    'original_sha256': row['original_byte_sha256'],
                    'note': 'README was appended after its initial read; original bytes remain preserved. No hash substitution.',
                }
                if item not in exceptions:
                    exceptions.append(item)
        raw = path.read_bytes()
        text = raw.decode('utf-8')
        start, end = row['range']
        valid = (
            digest(raw) == row['original_byte_sha256']
            and len(text) == row['character_length']
            and 0 <= start < end <= len(text)
            and end - start <= 6000
            and row['max_output_tokens'] >= 4000
            and digest(text[start:end].encode('utf-8')) == row['slice_utf8_sha256']
            and bool(row.get('truncation_check'))
        )
        require(valid, 'text_row_hash_length_range_cap_slice_and_truncation_record', ledger=label, row=number, path=str(original_path), range=[start, end])
        groups[(str(original_path), row['original_byte_sha256'], len(text))].append([start, end])
    for (path, version, length), ranges in groups.items():
        is_complete = complete(ranges, length)
        if not allow_partial:
            require(is_complete, 'complete_contiguous_text_version', ledger=label, path=path, sha256=version, character_length=length)
        summaries.append({'path': path, 'sha256': version, 'character_length': length, 'slice_count': len(ranges), 'ranges': ranges, 'complete_contiguous': is_complete})
    return summaries

def validate_image(row, label):
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
        regions = [region['bounds_xyxy'] for region in row.get('viewed_regions', [])]
    full = [0, 0, *dimensions]
    marked_full = row.get('fully_viewed_this_sweep', row.get('inspection_complete', row.get('fully_viewed', False)))
    require(
        sha(path) == row['original_byte_sha256'] and dimensions == recorded and full in regions and marked_full,
        'image_hash_decodable_dimensions_full_view_record', ledger=label, path=str(path), dimensions=dimensions, recorded_regions=regions,
    )

report_path = B / 'working-source-sweeps-37-38.json'
ledger_path = B / 'working-source-sweeps-37-38-read-ledger.json'
for name, expected in EXPECTED.items():
    require(sha(B / name) == expected, 'original_working_artifact_hash', path=str(B / name), expected_sha256=expected, actual_sha256=sha(B / name))
report = read(report_path)
ledger = read(ledger_path)
require(report['read_ledger']['original_byte_sha256'] == sha(ledger_path), 'report_binds_exact_read_ledger')

current_text = validate_text_rows(ledger['text_reads'], str(ledger_path), allow_partial=True)
prior = {}
prior_text = []
for binding in ledger['explicit_reuse']['completed_ledger_bindings']:
    path = Path(binding['path'])
    require(sha(path) == binding['original_byte_sha256'], 'immutable_reused_ledger_hash', **binding)
    value = read(path)
    prior[str(path)] = value
    prior_text.append({'ledger_path': str(path), 'ledger_sha256': sha(path), 'text_version_summaries': validate_text_rows(value.get('text_reads', []), str(path))})

reused_sources = ledger['explicit_reuse']['reused_complete_text_sources']
source_paths = {source['path'] for source in reused_sources}
for source in reused_sources:
    path = Path(source['path'])
    require(sha(path) == source['original_byte_sha256'], 'reused_original_source_bytes', path=str(path))
    actual_rows = []
    for binding in source['completed_delivery_ledger_refs']:
        require(sha(binding['path']) == binding['original_byte_sha256'], 'source_to_complete_ledger_binding', source=str(path), ledger=binding['path'])
        actual_rows.extend(row for row in prior[binding['path']]['text_reads'] if row['path'] == str(path) and row['original_byte_sha256'] == source['original_byte_sha256'])
    actual_ranges = sorted({tuple(row['range']) for row in actual_rows})
    require(actual_ranges == sorted(set(map(tuple, source['completed_ranges']))) and complete(actual_ranges, len(path.read_text())), 'reused_ranges_exactly_match_actual_complete_delivery_rows', path=str(path), actual_ranges=actual_ranges)

for group in current_text:
    if group['path'] not in source_paths:
        require(group['complete_contiguous'], 'new_text_input_delivered_completely', path=group['path'])
    elif not group['complete_contiguous']:
        exceptions.append({'kind': 'intentional_targeted_reread', 'path': group['path'], 'ranges': group['ranges'], 'note': 'Not a new whole-file delivery. Complete immutable original delivery is verified separately.'})

prior_image_rows = []
for path, value in prior.items():
    for row in value.get('image_reads', []):
        validate_image(row, path)
        prior_image_rows.append(row)
for row in ledger['explicit_reuse']['reused_full_image_delivery_rows']:
    require(row in prior_image_rows, 'reused_image_row_exactly_matches_immutable_original_ledger', path=row['path'])
require(len(ledger['image_reads']) == 11 and len({row['path'] for row in ledger['image_reads']}) == 11, 'eleven_unique_current_full_image_records')
for row in ledger['image_reads']:
    validate_image(row, str(ledger_path))

locator = ledger['derived_locator']
source = Path(locator['source_path']).read_text()
position = 0
derived = []
for line in source.splitlines(keepends=True):
    if '?' in line:
        derived.append(f'{position}: {line}')
    position += len(line)
require(''.join(derived).encode() == Path(locator['path']).read_bytes() and sha(locator['path']) == locator['original_byte_sha256'] and sha(locator['source_path']) == locator['source_sha256'], 'derived_locator_exactly_reproduces_source_lines_and_offsets', question_mark_lines=len(derived))

# Reconstruct ALL question/key/map objects from the model-delivered inputs.
v15 = B / 'expanded-v15'
v16 = read(B / 'panel-audit-bank-supplement-v16.json')
v18 = read(B / 'working-pass-v18-supplement.json')
q18 = read(B / 'expanded-v16/key-corrections.json')[0]
q157 = v18['inherited163_equivalence']['Q157_explicit_correction'][0]
reconstruction = {}
schemes = {
    'questions.json': ('questions', 'questions', 'complete6_question_objects'),
    'answer-key.json': ('answers', 'answer_key', 'complete6_key_objects'),
    'asked-fact-map.json': ('questions', 'asked_fact_entries', 'complete6_asked_map_objects'),
}
def canonical_hash(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8'))

for name, (main, addition16, addition18) in schemes.items():
    base = read(v15 / name)[main]
    objects = base + v16[addition16] + v18[addition18]
    if name != 'questions.json':
        objects = [q18['new_key' if name == 'answer-key.json' else 'new_mapping'] if row['id'] == 'Q18' else row for row in objects]
    if name != 'answer-key.json':
        objects = [q157['new_question' if name == 'questions.json' else 'new_mapping'] if row['id'] == 'Q157' else row for row in objects]
    current_path = B / 'expanded-v18' / name
    current = read(current_path)[main]
    current_hash = sha(current_path)
    require(objects == current and len(current) == 169 and [row['id'] for row in current] == [f'Q{i:02}' for i in range(1, 170)], 'exact_all_fields_169_object_reconstruction_and_ID_order', path=str(current_path))
    require(current_hash == v18['full_bank_sha256'][name] == report['current_input_hashes'][str(current_path)], 'current_full_file_byte_hash_matches_delivered_packet_and_report', path=str(current_path), sha256=current_hash)
    reconstruction[name] = {
        'current_path': str(current_path),
        'current_full_file_sha256': current_hash,
        'reconstructed_object_count': len(objects),
        'exact_all_fields_object_equality': objects == current,
        'reconstructed_objects_canonical_sha256': canonical_hash(objects),
        'current_objects_canonical_sha256': canonical_hash(current),
        'inherited_154': {'count': 154, 'canonical_sha256': canonical_hash(objects[:154]), 'explicit_changes': ['Q18 key/map only'] if name != 'questions.json' else []},
        'inherited_nine': {'count': 9, 'canonical_sha256': canonical_hash(objects[154:163]), 'explicit_changes': ['Q157 question/map wording only'] if name != 'answer-key.json' else []},
        'new_six': {'count': 6, 'canonical_sha256': canonical_hash(objects[163:])},
        'proof_type': 'Programmatic exact JSON-object equivalence plus direct original-file byte hashes. Not a claim of freshly model-delivering whole169 files or reproducing top-level metadata/JSON formatting.',
    }
    if name == 'asked-fact-map.json':
        count = sum(len(clause['required_facts']) for row in current for clause in row['requested_clauses'])
        require(count == 504, 'current_map_exact_504_required_facts', count=count)
        reconstruction[name]['required_fact_count'] = count

credit = B / 'expanded-v18/core-scope-credit.json'
require(sha(credit) == v18['full_bank_sha256'][credit.name], 'scope_credit_byte_hash_only', path=str(credit), sha256=sha(credit))
exceptions.append({'kind': 'disclosed_non_delivery', 'paths': [str(B / 'expanded-v18' / name) for name in schemes], 'note': 'Whole current bank content was checked programmatically, not freshly model-delivered. Fully delivered inherited packets and their exact reconstruction are the authorized reuse route.'})
exceptions.append({'kind': 'scope_credit_content_not_consulted', 'path': str(credit), 'note': 'Byte hash only; no content consultation or false full-read claim.'})

for path, expected in {**report['preservation'], **report['current_input_hashes'], **{str(B / name): expected for name, expected in EXPECTED.items()}}.items():
    require(sha(path) == expected, 'original_input_or_artifact_still_unchanged', path=path, expected_sha256=expected)

output = {
    'task': 'Evidence delivery/reuse and exact-bank-reconstruction validation only',
    'validator_path': str(Path(__file__).resolve()),
    'validator_sha256': sha(__file__),
    'status': 'PASS' if all(check['passed'] for check in checks) else 'FAIL',
    'scope_of_status': 'Evidence validation only. No new working sweep, novelty adjudication, or global independent coverage PASS.',
    'summary': {
        'checks': len(checks),
        'passed': sum(check['passed'] for check in checks),
        'failed': sum(not check['passed'] for check in checks),
        'current_text_records': len(ledger['text_reads']),
        'current_text_paths': len(current_text),
        'complete_new_external_text_inputs': 3,
        'complete_new_scratch_locator_inputs': 1,
        'current_native_full_image_records': len(ledger['image_reads']),
        'reused_immutable_ledgers': len(prior),
        'reused_complete_source_or_bank_text_paths': len(reused_sources),
        'reused_full_image_rows': len(ledger['explicit_reuse']['reused_full_image_delivery_rows']),
        'current_questions': 169,
        'current_required_facts': 504,
    },
    'validated_working_artifacts': [{'path': str(B / name), 'sha256': expected} for name, expected in EXPECTED.items()],
    'current_text_version_summaries': current_text,
    'prior_immutable_ledger_validation': prior_text,
    'exact_bank_reconstruction': reconstruction,
    'delivery_exceptions_and_disclosures': exceptions,
    'machine_validation_limit': 'Hashes, image decoding/dimensions/recorded bounds and full-delivery flags are checked. The original actual one-slice-per-response and native visual-delivery events are attested by this agent’s tool responses; a filesystem validator alone cannot independently replay model visual inspection or infer a missing transport transcript.',
    'checks': checks,
    'preservation': 'Original working report/read-ledger, own prior audits/ledgers, current bank and source bytes remain unchanged. Only this validation JSON is written by this helper.',
}
OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'status': output['status'], 'summary': output['summary'], 'validator_path': str(Path(__file__).resolve()), 'validation_path': str(OUT), 'validation_sha256': sha(OUT), 'failed_checks': [check for check in checks if not check['passed']]}, indent=2))
raise SystemExit(0 if output['status'] == 'PASS' else 1)
