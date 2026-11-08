"""Bind the single current neutral assessment to complete original evidence."""
from pathlib import Path
from collections import Counter
import hashlib
import json

R = Path(__file__).parent.resolve()
IT = R / 'expanded-iteration-05'
OUT = IT / 'neutral25-case-integrity-validation.json'
assert not OUT.exists()
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
source = read(IT / 'neutral25-case-input.json')
report = read(IT / 'neutral25-adjudication.json')
guide_path = IT / 'summary-snapshot.md'
guide = guide_path.read_text()
assert read(IT / 'neutral25-runtime-delivery-validation.json')['pass']
assert report['frozen_guide_sha256'] == sha(guide_path)
assert report['case_input_sha256'] == sha(IT / 'neutral25-case-input.json')
cases, checks, quotes = {}, 0, []


def pointer(value, path):
    for part in path.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def check_quotes(value, original):
    global checks
    if isinstance(value, list):
        for item in value:
            check_quotes(item, original)
    elif isinstance(value, dict):
        if 'quote' in value and 'original_entry_json_pointer' in value:
            text = pointer(original, value['original_entry_json_pointer'])
            assert isinstance(text, str) and value['quote'] in text
            quotes.append({'kind': 'exact_original_field_substring', 'pointer': value['original_entry_json_pointer'],
                           'quote_sha256': hashlib.sha256(value['quote'].encode()).hexdigest()})
            checks += 1
        if 'quote' in value and 'path' in value and 'start_char' in value:
            assert value['path'] == str(guide_path)
            assert guide[value['start_char']:value['end_char_exclusive']] == value['quote']
            quotes.append({'kind': 'exact_guide_span', 'start': value['start_char'],
                           'end': value['end_char_exclusive'],
                           'quote_sha256': hashlib.sha256(value['quote'].encode()).hexdigest()})
            checks += 1
        for item in value.values():
            check_quotes(item, original)


for selected in source['cases']:
    path = Path(selected['origin_block_path'])
    assert sha(path) == selected['origin_block_sha256']
    original = next(e for e in read(path)['entries'] if e['id'] == selected['case']['id'])
    assert selected['case'] == {k: v for k, v in original.items() if k != 'readers'}
    assert 'grade' not in selected and 'grade' not in selected['case']
    for label, wrapper in selected['complete_original_reader_entries_and_explicit_referents'].items():
        assert wrapper == original['readers'][label]
        cases[(original['id'], label)] = (selected['case'], wrapper)
    checks += 4
assert Counter((e['case_id'], e['reader_label']) for e in report['results']) == Counter(cases.keys())
for result in report['results']:
    case, wrapper = cases[(result['case_id'], result['reader_label'])]
    assert result['original_raw_entry_sha256'] == wrapper['raw_entry_sha256']
    assert result['original_normalized_entry_sha256'] == wrapper['normalized_entry_sha256']
    assert result['original_raw_file_sha256'] == wrapper['raw_file_sha256']
    assert pointer(source, result['original_entry_input_json_pointer']) == wrapper['complete_original_entry']
    expected = Counter(a['atom_id'] for a in case['validated_actual_scope']['required_atoms'])
    assessed = Counter(a for f in result['actual_scope_fact_assessment'] for a in f['required_atom_ids'])
    assert expected == assessed
    assert result['whole_entry_and_all_explicit_referents_reviewed'] is True
    units = wrapper['explicitly_referenced_shared_evidence']['resolved_units']
    assert Counter(u['reference'] for u in units) == Counter(u['reference'] for u in result['explicit_referents_reviewed'])
    for unit in result['explicit_referents_reviewed']:
        original = next(u for u in units if u['reference'] == unit['reference'])
        span = original['original_raw_unit_span']
        assert unit['original_reader_json_pointer'] == span['json_pointer']
        assert unit['raw_unit_sha256'] == span['raw_sha256']
        assert unit['normalized_unit_sha256'] == span['normalized_sha256']
        assert unit['all_reference_paths'] == original['explicit_reference_paths_in_original_entry']
        assert pointer(source, unit['input_json_pointer']) == original['original_unit']
        checks += 5
    assert not result['key_scope_ambiguities']
    assert result['grade'] == 'incorrect' and result['material_contradictions']
    check_quotes(result, wrapper['complete_original_entry'])
    checks += 8

agent = next(a for a in read(R / 'model-provenance.json')['agents']
             if a['task'] == '/root/expanded5_neutral_adjudicator_25')
turns, public_calls = [], []
for n, line in enumerate(Path(agent['runtime_source_path']).open()):
    row = json.loads(line)
    payload = row.get('payload', {})
    proof = {'ordinal': row.get('ordinal', n), 'record_sha256': hashlib.sha256(line.encode()).hexdigest()}
    if row.get('type') == 'turn_context':
        assert payload['model'] == 'gpt-6.1-sol' and payload.get('effort', payload.get('reasoning_effort')) == 'high'
        turns.append(proof)
    if payload.get('type') == 'custom_tool_call':
        assert payload['name'] == 'exec'
        public_calls.append({**proof, 'tool': 'exec', 'public_input_sha256': hashlib.sha256(payload['input'].encode()).hexdigest()})
    if payload.get('type') == 'function_call':
        assert payload['name'] == 'send_message'
        args = json.loads(payload['arguments'])
        assert args['target'] == '/root'
        public_calls.append({**proof, 'tool': 'send_message', 'target': '/root',
                             'arguments_sha256': hashlib.sha256(payload['arguments'].encode()).hexdigest(),
                             'message_contents_not_exposed_or_copied': True})
assert len(turns) == 1
assert all(sha(Path(p['path'])) == p['sha256'] for p in read(IT / 'original-grades-aggregate.json')['original_reports'])
OUT.write_text(json.dumps({'pass': True, 'checks_executed': checks, 'complete_original_entries': len(cases),
                          'complete_case_key_scope_and_wrappers_exact': True, 'all_asked_atoms_assessed_once': True,
                          'exact_quote_bindings': quotes, 'all_explicit_referent_bindings_exact': True,
                          'actual_full_delivery_proof': str(IT / 'neutral25-runtime-delivery-validation.json'),
                          'actual_Sol_high_contexts': turns, 'public_tool_call_bindings': public_calls,
                          'original_primary_reports_unchanged': True,
                          'case_input_sha256': sha(IT / 'neutral25-case-input.json'),
                          'neutral_report_sha256': sha(IT / 'neutral25-adjudication.json'),
                          'neutral_flag_metadata_preserved': [e['unsupported_correct_claim_flags'] for e in report['results']],
                          'confidence_label_diagnostics_not_independent_factual_caps': True,
                          'no_additional_neutral_vote_authorized': True}, indent=2) + '\n')
print({'pass': True, 'checks': checks, 'whole_original_entries': len(cases), 'exact_quotes': len(quotes)})
