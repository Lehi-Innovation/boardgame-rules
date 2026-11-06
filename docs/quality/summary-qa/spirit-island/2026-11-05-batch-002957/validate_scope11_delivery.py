#!/usr/bin/env python3
"""Validate challenger11 frozen delivery artifacts, without rules re-review.

Reads only the three completed challenger11 artifacts and their allowed original
inputs. Writes only scope11-delivery-validation.json beside this script.
Filesystem assertions do not prove past tool delivery or human/model perception.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
SOURCE = ROOT / 'docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/spirit-island'
PANELS = SOURCE / 'original-spirit-panels'
OUTPUT = B / 'scope11-delivery-validation.json'
FROZEN_ARTIFACTS = {
    'scope-coverage-11-read-ledger.json': '9fdaa1b5eed6ba0e32937518666ef41a4254a930bb3f9b8e092f2f78f48308f2',
    'question-key-scope-review-11.json': '0c917b322a6c7eae6de0967fd966cf3480eff41a402d5998ca36b11832d3c3c8',
    'coverage-review-11.json': '211723bc87dd06586fd490f4c8dc060b288fa6cee63e971abc70f1ca958a1506',
}
FROZEN_BENCHMARK = {
    'expanded-v19/questions.json': 'ad9065e9c817b110a5e3af50ca55c5e2fa59d00be4bf4c9f06b40b3cf7be70d0',
    'expanded-v19/answer-key.json': '1e1ec9944988051b047007d6ab321174d5a007048b3ab5a6002e0df901428bae',
    'expanded-v19/asked-fact-map.json': '2af755fe28efebcd578103985e23f0770e39bc3bcc2b3c628e23c00767a95a22',
    'expanded-v19/core-scope-credit.json': '42b6fa386ac0362fb8de19717cfc399e7195494995516be59ab8be6bb5e551fc',
    'coverage-map-for-review-11.json': '21f5733fbfbd972743387fdb11f49982401c806320112e3002182d2804825f68',
}
EXPECTED_TEXTS = {
    *(str(B / n) for n in [
        'scope-and-coverage-11-prompt.txt', 'coverage-review-11-input-manifest.json',
        'source-manifest.json', 'supplemental-source-manifest-v4.json',
        'scope-reachability-steering-2026-11-05.txt', 'coverage-map-for-review-11.json',
        'expanded-v19/questions.json', 'expanded-v19/answer-key.json',
        'expanded-v19/asked-fact-map.json', 'expanded-v19/core-scope-credit.json',
        'card-scope-source/what-do-range-boosts-affect.txt',
        'card-scope-source/range-in-text-of-powers-that-target-spirits.txt',
        'card-scope-source/core-second-printing.txt',
        'novelty11-source-scratch/novelty11-publisher-updates.txt',
    ]),
    str(ROOT / 'extracted/spirit-island-rules.txt'),
    str(SOURCE / 'living-faq-core-game.txt'), str(SOURCE / 'living-faq-setup.txt'),
    *(str(PANELS / n) for n in ['README.md', 'panel-download-map.json',
        'download-integrity.json', 'independent-printed-photo-corroboration.json']),
}
EXPECTED_IDS = [f'Q{i:02}' for i in range(1, 171)]
checks, failures, text_results, image_results, hash_results = [], [], [], [], []

def check(label, condition, details=None, evidence='filesystem'):
    result = {'check': label, 'passed': bool(condition), 'evidence_type': evidence}
    if details is not None:
        result['details'] = details
    checks.append(result)
    if not condition:
        failures.append(result)
    return bool(condition)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def file_hash(path):
    return digest(Path(path).read_bytes())

def read_json(path):
    return json.loads(Path(path).read_bytes().decode('utf-8'))

def verify_slice(path, text, item, label, primary=False):
    bounds = item.get('range')
    valid_bounds = (isinstance(bounds, list) and len(bounds) == 2
        and all(type(v) is int for v in bounds)
        and 0 <= bounds[0] < bounds[1] <= len(text)
        and bounds[1] - bounds[0] <= 6000)
    check(label + ': bounds/6000 cap', valid_bounds, {'path': path, 'range': bounds})
    if valid_bounds:
        check(label + ': UTF8 slice hash', digest(text[bounds[0]:bounds[1]].encode('utf-8')) == item.get('slice_sha256'))
    cap = item.get('max_output_tokens')
    check(label + ': explicit recorded output cap', type(cap) is int and cap >= 4000,
          cap, 'recorded_tool_attestation')
    check(label + ': recorded no truncation', item.get('truncation') is False,
          evidence='recorded_tool_attestation')
    if primary:
        check(label + ': recorded one slice per response', item.get('one_slice_per_tool_response') is True,
              evidence='recorded_tool_attestation')
    return valid_bounds

try:
    before = {name: file_hash(B / name) for name in FROZEN_ARTIFACTS}
    for name, expected in FROZEN_ARTIFACTS.items():
        check('frozen completed artifact: ' + name, before[name] == expected,
              {'expected_sha256': expected, 'actual_sha256': before[name]})
    ledger = read_json(B / 'scope-coverage-11-read-ledger.json')
    reports = {n: read_json(B / n) for n in FROZEN_ARTIFACTS if n != 'scope-coverage-11-read-ledger.json'}
    texts, images = ledger['texts'], ledger['images']
    text_paths, image_paths = [x['path'] for x in texts], [x['path'] for x in images]
    check('exact21 text inventory', len(texts) == 21 and len(set(text_paths)) == 21
          and set(text_paths) == EXPECTED_TEXTS, {'missing': sorted(EXPECTED_TEXTS - set(text_paths)), 'unexpected': sorted(set(text_paths) - EXPECTED_TEXTS)})
    check('ledger text/image count declarations', ledger.get('text_input_count') == 21
          and ledger.get('native_image_count') == 54, evidence='recorded_tool_attestation')
    manifest = read_json(B / 'supplemental-source-manifest-v4.json')
    records = manifest['source_records']
    primary_roles = {'primary printed card face', 'primary printed original-base Spirit panel facsimile'}
    expected_primary = {x['path']: x['sha256'] for x in records if x.get('role') in primary_roles}
    check('manifest33 card and16 panel inventory',
          sum(x.get('role') == 'primary printed card face' for x in records) == 33
          and sum(x.get('role') == 'primary printed original-base Spirit panel facsimile' for x in records) == 16)
    extra_images = {str(PANELS / n) for n in ['corroborating-all-spirits-2017.jpg',
        'corroborating-river-2018.jpg', 'corroborating-2017-bringer-track-crop.png']}
    extra_images |= {str(B / 'card-scope-source' / n) for n in
        ['branch-claw-rulebook-p6.png', 'all-named-card-title-corner-strips.jpg']}
    expected_images = set(expected_primary) | extra_images
    check('exact54 image inventory', len(images) == len(set(image_paths)) == 54
          and set(image_paths) == expected_images,
          {'missing': sorted(expected_images - set(image_paths)), 'unexpected': sorted(set(image_paths) - expected_images)})
    allowed_inputs = EXPECTED_TEXTS | expected_images
    check('exact75 unique allowed frozen inputs', len(allowed_inputs) == 75
          and set(text_paths).isdisjoint(image_paths))
    ledger_hashes = {x['path']: x['sha256'] for x in texts + images}
    check('ledger75 hash inventory', len(ledger_hashes) == 75 and set(ledger_hashes) == allowed_inputs)
    # Do not follow any other manifest targets, metadata_path, identity_proof,
    # report/runtime/history references, or module/catalog code.
    for path in sorted(allowed_inputs):
        expected = ledger_hashes.get(path)
        actual = file_hash(path)
        good = expected == actual
        check('frozen input hash: ' + path, good)
        hash_results.append({'path': path, 'expected_sha256': expected, 'actual_sha256': actual, 'passed': good})
        if path in expected_primary:
            check('original permitted manifest image hash: ' + path, actual == expected_primary[path])
    for rel, expected in FROZEN_BENCHMARK.items():
        check('independently pinned benchmark hash: ' + rel, file_hash(B / rel) == expected,
              {'expected_sha256': expected, 'actual_sha256': file_hash(B / rel)})
    for index, entry in enumerate(texts):
        path = entry['path']
        if path not in EXPECTED_TEXTS:
            continue
        data = Path(path).read_bytes()
        text = data.decode('utf-8')  # Unicode code points; preserve original CR/LF bytes.
        check('Unicode character length: ' + path, len(text) == entry.get('character_length'))
        cursor, valid = 0, True
        for number, part in enumerate(entry.get('slices', [])):
            bounds_ok = verify_slice(path, text, part, f'text{index}/slice{number}', primary=True)
            contiguous = bounds_ok and part['range'][0] == cursor
            check(f'text{index}/slice{number}: contiguous', contiguous)
            valid &= contiguous
            if bounds_ok:
                cursor = part['range'][1]
        full = valid and cursor == len(text) and bool(entry.get('slices'))
        check('complete reconstructed text inventory: ' + path, full)
        check('recorded complete delivery: ' + path, entry.get('complete_contiguous_delivery') is True,
              evidence='recorded_tool_attestation')
        for number, part in enumerate(entry.get('additional_complete_or_targeted_redeliveries', [])):
            verify_slice(path, text, part, f'text{index}/redelivery{number}')
        text_results.append({'path': path, 'unicode_character_length': len(text),
            'utf8_byte_length': len(data), 'primary_slice_count': len(entry.get('slices', [])),
            'redelivery_record_count': len(entry.get('additional_complete_or_targeted_redeliveries', [])),
            'contiguous_full_inventory': full})
    for entry in images:
        path = entry['path']
        if path not in expected_images:
            continue
        with Image.open(path) as im:
            dimensions = list(im.size)
            fmt = im.format
            im.verify()
        full_region = [0, 0, *dimensions]
        check('native image dimensions/full region: ' + path,
              entry.get('visual_region_xyxy') == full_region,
              {'actual_dimensions': dimensions, 'declared_region': entry.get('visual_region_xyxy'), 'expected_region': full_region})
        check('recorded full native view: ' + path, entry.get('native_view_completed') is True,
              evidence='recorded_perception_attestation')
        check('recorded image no truncation: ' + path, entry.get('truncation') is False,
              evidence='recorded_tool_attestation')
        check('recorded image observation: ' + path,
              isinstance(entry.get('observation'), str) and bool(entry['observation'].strip()),
              evidence='recorded_perception_attestation')
        image_results.append({'path': path, 'format': fmt, 'dimensions': dimensions,
            'file_integrity_checked': True, 'full_native_region': full_region,
            'declared_region_matches_dimensions': entry.get('visual_region_xyxy') == full_region,
            'native_view_declaration': entry.get('native_view_completed'),
            'actual_past_perception_independently_proven': False})
    questions = read_json(B / 'expanded-v19/questions.json')['questions']
    answers = read_json(B / 'expanded-v19/answer-key.json')['answers']
    asked = read_json(B / 'expanded-v19/asked-fact-map.json')
    mapped = asked['questions']
    credit = read_json(B / 'expanded-v19/core-scope-credit.json')
    compact = read_json(B / 'coverage-map-for-review-11.json')
    for label, rows in [('questions', questions), ('answers', answers), ('asked map', mapped), ('scope credit', credit['questions'])]:
        check('exact ordered170 IDs: ' + label, [x['id'] for x in rows] == EXPECTED_IDS)
    check('literal question/map strings unchanged and equal',
          [x['question'] for x in questions] == [x['question'] for x in mapped])
    fact_counts = [sum(len(c['required_facts']) for c in row['requested_clauses']) for row in mapped]
    check('exact505 mapped grading facts', sum(fact_counts) == 505 and asked.get('required_fact_count') == 505,
          {'actual': sum(fact_counts), 'declared': asked.get('required_fact_count')})
    check('all mapped grading facts nonempty strings', all(isinstance(f, str) and bool(f.strip())
          for row in mapped for clause in row['requested_clauses'] for f in clause['required_facts']))
    check('scope-credit and compact170 declarations', credit.get('question_count') == compact.get('question_count') == 170)
    for name, report in reports.items():
        check('report ordered170 IDs: ' + name,
              report.get('checked_question_ids') == EXPECTED_IDS and report.get('checked_question_count') == 170)
        check('report75 frozen input hash bindings: ' + name, report.get('input_hashes') == ledger_hashes)
        expected_link = {'ledger_path': str(B / 'scope-coverage-11-read-ledger.json'),
                         'sha256': file_hash(B / 'scope-coverage-11-read-ledger.json')}
        check('report to ledger path/hash: ' + name, report.get('read_evidence') == expected_link)
        check('report asked-map hash: ' + name,
              report.get('asked_fact_map_sha256') == file_hash(B / 'expanded-v19/asked-fact-map.json'))
        if 'question_checks' in report:
            check('per-question170/505 review inventory: ' + name,
                  [x['id'] for x in report['question_checks']] == EXPECTED_IDS
                  and [x['required_fact_count'] for x in report['question_checks']] == fact_counts)
    after = {name: file_hash(B / name) for name in FROZEN_ARTIFACTS}
    check('three completed artifacts preserved byte-for-byte', before == after and after == FROZEN_ARTIFACTS)
except Exception as exc:
    check('validator completed without unhandled input/decoding errors', False,
          {'exception_type': type(exc).__name__, 'message': str(exc)})

result = {
    'benchmark': 'expanded-v19',
    'validation_scope': 'Evidence structure, frozen bytes, delivery metadata and inventory only; no semantic rules re-review.',
    'generated_utc': datetime.now(timezone.utc).isoformat(),
    'validator_path': str(Path(__file__).resolve()),
    'validator_sha256': file_hash(__file__),
    'validation_verdict': 'FAIL' if failures else 'PASS',
    'actual_failures': failures,
    'checked_counts': {'frozen_input_hashes': len(hash_results), 'text_inputs': len(text_results),
        'primary_text_slices': sum(x['primary_slice_count'] for x in text_results),
        'redelivery_records': sum(x['redelivery_record_count'] for x in text_results),
        'native_images': len(image_results), 'questions': len(EXPECTED_IDS),
        'mapped_grading_facts': sum(fact_counts) if 'fact_counts' in globals() else None,
        'checks': len(checks)},
    'proof_boundary': {
        'filesystem_proven': ['All75 current input byte hashes against the frozen ledger and report bindings',
            'The three completed artifacts retain their independently pinned completion hashes',
            'Exact21 text inventory, UTF8 decoding, Unicode lengths, primary slice bounds/contiguity/coverage and slice hashes',
            'Exact54 permitted image inventory, hashes, readable image integrity/dimensions and declared full-region equality',
            'Exact ordered170 IDs, literal question/map equality,505 mapped fact inventory, and report/ledger hash bindings'],
        'recorded_attestations_only': ['Explicit max_output_tokens>=4000 in historical tool requests',
            'One slice actually delivered in each past tool response', 'Past tool output was not truncated',
            'Model actually received/read every slice and fully perceived each native image'],
        'filesystem_cannot_prove': 'The historical tool/perception claims are explicitly recorded in the frozen ledger and checked for consistency here. This validator does not access runtime/private histories, reconstruct past tool responses, or independently certify past perception.',
        'semantic_report_verdicts_unchanged': True,
        'validation_PASS_meaning': 'All executed filesystem and metadata-consistency assertions passed; it is not independent proof of historical delivery/perception or a rules/coverage PASS.'},
    'frozen_completed_artifacts': FROZEN_ARTIFACTS,
    'frozen_benchmark_inputs': FROZEN_BENCHMARK,
    'input_hash_results': hash_results,
    'text_inventory_results': text_results,
    'native_image_results': image_results,
    'checks': checks,
    'access_boundaries': {'only_completed_own_artifacts_and_original_allowed_inputs_read': True,
        'no_summary_reader_grade_history_other_agent_runtime_private_instruction_or_module_access': True,
        'three_completed_reports_ledger_not_written': True,
        'only_new_validator_and_validation_json_written': True},
}
OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'validation_verdict': result['validation_verdict'],
    'actual_failure_count': len(failures), 'checked_counts': result['checked_counts'],
    'validation_path': str(OUTPUT), 'validator_path': str(Path(__file__).resolve())}))
for failure in failures:
    print(json.dumps(failure, ensure_ascii=False))
raise SystemExit(1 if failures else 0)
