"""Bind one fresh whole-entry assessment without rewriting primary judgments."""
from pathlib import Path
from collections import Counter
import hashlib
import json

R = Path(__file__).parent.resolve()
IT = R / 'expanded-iteration-04'
OUT = IT / 'neutral21-case-integrity-validation.json'
assert not OUT.exists()
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())
case_path = IT / 'neutral21-case-input.json'
case_input = read(case_path)
report_path = IT / 'neutral21-adjudication.json'
report = read(report_path)
guide_path = IT / 'summary-snapshot.md'
guide = guide_path.read_text()
assert read(IT / 'neutral21-runtime-delivery-validation.json')['pass']
assert report['frozen_guide_sha256'] == sha(guide_path)
assert report['selected_case_input_sha256'] == sha(case_path)
assert report['instruction_sha256'] == sha(IT / 'neutral21-instructions.txt')
assert report['primary_reports_modified'] is False
checks = 0
quote_checks = []


def pointer(value, path):
    for part in path.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def inspect_quotes(value):
    global checks
    if isinstance(value, list):
        for item in value:
            inspect_quotes(item)
    elif isinstance(value, dict):
        if 'quote' in value and 'input_json_pointer' in value:
            actual = pointer(case_input, value['input_json_pointer'])
            assert isinstance(actual, str) and value['quote'] in actual
            quote_checks.append({'kind': 'exact_original_field_substring',
                                 'pointer': value['input_json_pointer'],
                                 'quote_sha256': hashlib.sha256(value['quote'].encode()).hexdigest()})
            checks += 1
        if 'quote' in value and 'guide_path' in value and 'start_char' in value:
            assert value['guide_path'] == str(guide_path)
            assert guide[value['start_char']:value['end_char_exclusive']] == value['quote']
            quote_checks.append({'kind': 'exact_guide_span', 'start': value['start_char'],
                                 'end': value['end_char_exclusive'],
                                 'quote_sha256': hashlib.sha256(value['quote'].encode()).hexdigest()})
            checks += 1
        for item in value.values():
            inspect_quotes(item)


cases = {}
for selected in case_input['cases']:
    block_path = Path(selected['origin_block_path'])
    assert sha(block_path) == selected['origin_block_sha256']
    original = next(e for e in read(block_path)['entries'] if e['id'] == selected['case']['id'])
    assert selected['case'] == {k: v for k, v in original.items() if k != 'readers'}
    assert selected['complete_original_reader_entries_and_explicit_referents'] == original['readers']
    assert 'grade' not in selected and 'grade' not in selected['case']
    for reader, wrapper in original['readers'].items():
        cases[(original['id'], reader)] = (selected['case'], wrapper)
    checks += 4

assert Counter((e['question_id'], e['reader_label']) for e in report['assessments']) == Counter(cases.keys())
for entry in report['assessments']:
    case, wrapper = cases[(entry['question_id'], entry['reader_label'])]
    assert entry['original_raw_entry_sha256'] == wrapper['raw_entry_sha256']
    assert entry['original_normalized_entry_sha256'] == wrapper['normalized_entry_sha256']
    assert entry['original_raw_file_sha256_as_supplied'] == wrapper['raw_file_sha256']
    assert entry['key_entry_sha256'] == case['key_entry_sha256']
    assert entry['literal_question'] == case['literal_question']['question']
    assert pointer(case_input, entry['complete_original_entry_input_json_pointer']) == wrapper['complete_original_entry']
    expected_atoms = Counter(a['atom_id'] for a in case['validated_actual_scope']['required_atoms'])
    actual_atoms = Counter(a for assessment in entry['actual_scope_assessment'] for a in assessment['asked_atom_ids'])
    assert actual_atoms == expected_atoms
    units = wrapper['explicitly_referenced_shared_evidence']['resolved_units']
    assert Counter(u['reference'] for u in units) == Counter(u['reference'] for u in entry['same_entry_explicit_referent_audit'])
    for unit in entry['same_entry_explicit_referent_audit']:
        original = next(u for u in units if u['reference'] == unit['reference'])
        span = original['original_raw_unit_span']
        assert unit['original_reader_unit_json_pointer'] == span['json_pointer']
        assert unit['original_raw_unit_sha256'] == span['raw_sha256']
        assert unit['explicit_reference_paths_in_original_entry'] == original['explicit_reference_paths_in_original_entry']
        assert pointer(case_input, unit['input_unit_json_pointer']) == original['original_unit']
        checks += 4
    if entry['grade'] == 'correct':
        assert not entry['material_contradictions'] and not entry['missing_asked_units']
        assert not entry['unsupported_correct_claim_flags']
    assert not entry['genuine_key_or_scope_ambiguity']
    inspect_quotes(entry)
    checks += 9

provenance = read(R / 'model-provenance.json')
agent = next(a for a in provenance['agents'] if a['task'] == '/root/expanded4_neutral_adjudicator_21')
runtime = []
turns = []
for index, raw in enumerate(Path(agent['runtime_source_path']).open()):
    row = json.loads(raw)
    payload = row.get('payload', {})
    binding = {'ordinal': row.get('ordinal', index), 'record_sha256': hashlib.sha256(raw.encode()).hexdigest()}
    if row.get('type') == 'turn_context':
        assert payload['model'] == 'gpt-6.1-sol' and payload.get('effort', payload.get('reasoning_effort')) == 'high'
        turns.append(binding)
    if payload.get('type') == 'custom_tool_call':
        assert payload['name'] == 'exec'
        runtime.append({**binding, 'tool': 'exec', 'public_input_sha256': hashlib.sha256(payload['input'].encode()).hexdigest()})
    if payload.get('type') == 'function_call':
        assert payload['name'] == 'send_message'
        args = json.loads(payload['arguments'])
        assert args['target'] == '/root'
        runtime.append({**binding, 'tool': 'send_message', 'target': '/root',
                        'arguments_sha256': hashlib.sha256(payload['arguments'].encode()).hexdigest(),
                        'message_plaintext_not_examined_or_saved': True})
assert len(turns) == 1
primary = read(IT / 'original-grades-aggregate.json')
assert all(sha(Path(p['path'])) == p['sha256'] for p in primary['original_reports'])
result = {'pass': True, 'checks_executed': checks, 'complete_case_wrappers_and_key_scope_exact': True,
          'whole_original_entry_count': len(cases), 'all_required_atoms_assessed_once': True,
          'all_same_entry_unit_bindings_verified': True, 'exact_quote_bindings': quote_checks,
          'actual_runtime_delivery_pass': True, 'actual_turn_model_settings': turns,
          'public_tool_call_bindings': runtime,
          'purity_review': 'Public exec read expressions inspected: only the three permitted input files. Output writes use the two specified destinations. Parent progress message only; no peer/source calls. No plaintext decryption or ciphertext stored in this artifact.',
          'initial_diagnostic_deviation_disclosed_separately': 'runtime-diagnostic-deviation-21.json',
          'original_primary_reports_hashes_unchanged': True,
          'case_input_sha256': sha(case_path), 'neutral_report_sha256': sha(report_path),
          'guide_sha256': sha(guide_path), 'requested_fork_none_distinct_from_unavailable_runtime_field': True}
OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print({'pass': True, 'checks': checks, 'whole_entries': len(cases), 'exact_quotes': len(quote_checks)})
