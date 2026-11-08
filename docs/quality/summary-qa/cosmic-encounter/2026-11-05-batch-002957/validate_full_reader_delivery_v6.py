"""Verify full data/process delivery and separately diagnose actual transport bounds."""
from pathlib import Path
import hashlib
import json
import sys
from reader_receipt_offsets_v1 import normalize_offset_receipts

R = Path(__file__).parent.resolve()
IT = (R / sys.argv[1]).resolve()
assert IT.is_relative_to(R)
OUT = IT / 'delivery-validation-v6.json'
assert not OUT.exists()


def sha(value):
    return hashlib.sha256(value).hexdigest()


def read(path):
    return json.loads(path.read_text())


def texts(value):
    if isinstance(value, str):
        yield value
        try:
            parsed = json.loads(value)
        except ValueError:
            parsed = None
        if isinstance(parsed, (dict, list)):
            yield from texts(parsed)
        else:
            for line in value.splitlines():
                if not line.startswith(('{', '[')):
                    continue
                try:
                    parsed = json.loads(line)
                except ValueError:
                    continue
                if isinstance(parsed, (dict, list)):
                    yield from texts(parsed)
    elif isinstance(value, dict):
        for item in value.values():
            yield from texts(item)
    elif isinstance(value, list):
        for item in value:
            yield from texts(item)


manifest = read(IT / 'input-manifest-final.json')
bindings = read(IT / 'dispatch-bindings.json')['readers']
provenance = read(R / 'model-provenance.json')
expected = [q['id'] for q in read(IT / 'questions.json')['questions']]
data_paths = set(manifest['sole_game_data_files'])
question_path = next(Path(p) for p in data_paths if p.endswith('.json'))
question_doc = read(question_path)
assert question_doc['questions'] == read(IT / 'questions.json')['questions']
process_metadata = question_doc['reader_process']
assert sha(process_metadata['instructions'].encode()) == process_metadata['instructions_sha256']
assert process_metadata['method_code_sha256'] == manifest['generic_code_sha256']
code = process_metadata['instructions'].split('```python\n', 1)[1].split('```', 1)[0]
assert sha(code.encode()) == manifest['generic_code_sha256']
instruction_path = manifest.get('shared_instruction_file')
reports = []
for binding in bindings:
    agent = next(a for a in provenance['agents'] if a['task'] == binding['task'])
    doc_path = Path(binding['output_path'])
    doc = read(doc_path)
    records = []
    for index, raw in enumerate(Path(agent['runtime_source_path']).open()):
        row = json.loads(raw)
        payload = row.get('payload', {})
        if payload.get('type') == 'custom_tool_call_output':
            records.append(({'ordinal': row.get('ordinal', index),
                             'record_sha256': sha(raw.encode())},
                            list(set(texts(payload.get('output'))))))
    declarations = [(d, 'game_data') for d in doc['inputs_read']]
    if instruction_path:
        process = doc.get('instructions_read', [])
        process = process if isinstance(process, list) else [process]
        declarations += [(d, 'generic_process_only') for d in process]
    files = []
    for declared, kind in declarations:
        path = Path(declared['path']).resolve()
        allowed = data_paths if kind == 'game_data' else {instruction_path}
        assert str(path) in allowed
        value = path.read_text()
        checks, cursor = [], 0
        coordinates = normalize_offset_receipts(value, declared['chunks'])
        for c in coordinates['chunks']:
            begin, end = c['start'], c['end']
            piece = value[begin:end]
            proofs = [proof for proof, strings in records if any(piece in s for s in strings)]
            checks.append({'start': begin, 'end': end, 'characters': end - begin,
                           'contiguous': begin == cursor, 'declared_bounded_6000': 0 < end - begin <= 6000,
                           'original_declared_start': c['original_start'], 'original_declared_end': c['original_end'],
                           'original_coordinate_unit': coordinates['original_offset_unit'],
                           'sha256': sha(piece.encode()), 'declared_hash_matches': c['sha256'] == sha(piece.encode()),
                           'exact_actual_visible_delivery': bool(proofs), 'runtime_proof': proofs})
            cursor = end
        # Probe actual returned strings, not only the reader's declared boundaries.
        # Extending a matched unique source anchor exposes a coalesced long display.
        anchors = [(i, value[i:i + 160]) for i in range(0, len(value) - 159, 1000)]
        oversized = {}
        for proof, strings in records:
            for s in strings:
                if len(s) <= 6000:
                    continue
                for offset, anchor in anchors:
                    where = s.find(anchor)
                    if where < 0:
                        continue
                    left, right = offset, offset + len(anchor)
                    start, stop = where, where + len(anchor)
                    while left > 0 and start > 0 and value[left - 1] == s[start - 1]:
                        left -= 1
                        start -= 1
                    while right < len(value) and stop < len(s) and value[right] == s[stop]:
                        right += 1
                        stop += 1
                    if right - left > 6000:
                        oversized[(proof['ordinal'], left, right)] = {
                            'source_start': left, 'source_end': right, 'source_characters': right - left,
                            **proof}
        result = {'path': str(path), 'kind': kind, 'sha256': sha(path.read_bytes()),
                  'receipt_coordinate_interpretation': coordinates['original_offset_unit'],
                  'one_original_payload_per_normalized_range': True, 'original_raw_receipt_untouched': True,
                  'frozen_hash_matches': manifest['sha256'][str(path)] == sha(path.read_bytes()),
                  'declared_full_hash_matches': declared['sha256'] == sha(path.read_bytes()),
                  'complete_contiguous_coverage': cursor == len(value) and all(c['contiguous'] for c in checks),
                  'chunks': checks, 'actual_oversized_contiguous_source_displays': list(oversized.values()),
                  'metadata_diagnostics': {'bytes_match': declared.get('bytes') == path.stat().st_size,
                                           'characters_match': declared.get('characters') == len(value)}}
        result['content_delivery_pass'] = (result['frozen_hash_matches'] and result['declared_full_hash_matches']
                                          and result['complete_contiguous_coverage'] and bool(checks)
                                          and all(c['declared_hash_matches'] and c['exact_actual_visible_delivery'] for c in checks))
        result['actual_transport_bounded'] = not oversized
        files.append(result)
    actual_ids = [a['id'] for a in doc['answers']]
    game = [f for f in files if f['kind'] == 'game_data']
    process = [f for f in files if f['kind'] == 'generic_process_only']
    report = {'reader': binding['label'], 'task': binding['task'], 'identity': agent['identity'],
              'actual_model_and_effort_verified': agent['settings_verified'],
              'actual_turn_settings': agent['turn_records'], 'requested_fork_context': binding['fork_turns'],
              'runtime_fork_context_field': None,
              'raw_output_sha256': sha(doc_path.read_bytes()),
              'ids_exactly_once_in_order': actual_ids == expected and len(set(actual_ids)) == len(expected),
              'files': files,
              'only_two_declared_game_data_inputs': len(game) == 2 and {f['path'] for f in game} == data_paths,
              'shared_process_instruction_complete': not instruction_path or len(process) == 1 and process[0]['content_delivery_pass'],
              'method_code_hash_diagnostic': doc.get('method_code_sha256') == manifest.get('generic_code_sha256') if manifest.get('generic_code_sha256') else None,
              'continuation_limit': 'One initially fresh blind identity may finish its own explicitly unfinished work. No additional fresh vote or external rule/grade feedback is claimed.'}
    report['content_and_identity_pass'] = (report['actual_model_and_effort_verified'] and binding['fork_turns'] == 'none'
                                           and report['ids_exactly_once_in_order'] and report['only_two_declared_game_data_inputs']
                                           and report['shared_process_instruction_complete'] and all(f['content_delivery_pass'] for f in files))
    report['actual_transport_bounds_compliant'] = all(f['actual_transport_bounded'] for f in files)
    reports.append(report)
normalized = [Path(b['prompt_path']).read_text()
              .replace(b['draft_output_path'], 'DRAFT_PATH_VALUE')
              .replace(b['output_path'], 'FINAL_PATH_VALUE')
              .replace('field is \"' + b['label'] + '\"', 'field is \"READER_LABEL\"') for b in bindings]
staged = read(IT / 'staged-history-validation-01.json')
assert staged['pass']
review_proofs = [read(IT / f'reader-{c}-review-payload-validation-01.json') for c in 'ab']
assert all(x['pass'] for x in review_proofs)
for c in 'ab':
    assert read(IT / f'reader-{c}-initial-bounded-actual-validation-02.json')['pass']
input_gates = []
for c in 'ab':
    gates=sorted(IT.glob(f'reader-{c}-input-gate-[0-9][0-9].json'))
    assert gates and read(gates[-1])['pass'] and read(gates[-1])['zero_answers_at_gate']
    input_gates.append(str(gates[-1]))
result = {'iteration': IT.name, 'validator_version': 6,
          'staged_history_validation_path': str(IT / 'staged-history-validation-01.json'),
          'input_only_gates': input_gates,
          'whole_original_draft_review_payloads_verified': True,
          'version_note': 'One-to-one Unicode/UTF8byte receipt normalization requires exact original hashes and EOF. Actual payload matching remains mandatory; original receipts are untouched.',
          'initial_transport_timing_evidence_path': str(IT / 'initial-transport-technical-audit-23.json') if (IT / 'initial-transport-technical-audit-23.json').exists() else None,
          'initial_timing_limit': 'Whole-runtime availability never certifies pre-first-save delivery. Any separately documented initial failure and later transport repair remain explicit.',
          'saved_prompts_identical_except_output': len(normalized) == 2 and normalized[0] == normalized[1],
          'runtime_message_plaintext_comparison': None,
          'question_file_metadata_process_code_hash_verified': True,
          'every_literal_question_record_unchanged': True,
          'process_delivery_basis': 'Complete exact actual question-file delivery includes all generic process metadata/code; no external instruction file is needed.',
          'runtime_message_limit': 'Task messages encrypted; saved requests plus actual visible shared process text and data are verified separately.',
          'readers': reports,
          'pass': all(r['content_and_identity_pass'] for r in reports) and len(reports) == 2,
          'actual_transport_bounds_compliant': all(r['actual_transport_bounds_compliant'] for r in reports),
          'scoring_policy': 'Transport/metadata diagnostics do not change factual grades. Complete original answers are graded normally, with any final readiness limits disclosed separately.'}
OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print('content/model/identity', result['pass'], 'actual transport bounds', result['actual_transport_bounds_compliant'])
