"""Validate frozen case coverage and literal reference bindings; no rescoring."""
from pathlib import Path
import collections
import hashlib
import json

B = Path(__file__).resolve().parent
D = B / 'expanded-iteration-02'
A = D / 'adjudication-01'
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
report = load(A / 'adjudication.json')
manifest = load(A / 'input-manifest.json')
cases = load(A / 'raw-cases.json')
maps = {x['id']: x for x in load(A / 'asked-facts.json')['questions']}
original = load(D / 'results.json')
expected = {(x['reader'], x['id']) for x in cases['requested_cases']}
rows = report['adjudications']
assert len(rows) == len(expected) == 12
assert {(x['reader'], x['id']) for x in rows} == expected
assert {(x['reader'], x['id']) for x in report['expected_cases']} == expected
checks = []
def check(label, condition):
    assert condition, label
    checks.append(label)

input_paths = {str((D / 'summary-snapshot.md').resolve())} | {str((A / x).resolve()) for x in ['questions.json', 'answer-key.json', 'asked-facts.json', 'raw-cases.json']}
check('exactly five declared input paths', {x['path'] for x in report['inputs_read']} == input_paths)
for inp in report['inputs_read']:
    p = Path(inp['path'])
    text = p.read_text()
    check('input hash ' + p.name, inp['sha256'] == H(p))
    check('input character length ' + p.name, inp['unicode_character_length'] == len(text))
    check('input byte length ' + p.name, inp['byte_length'] == p.stat().st_size)
    position = 0
    for part in inp['read_ranges']:
        check('contiguous bounded literal input range', part['start'] == position and 0 < part['end'] - part['start'] <= 6000 and part['output_cap_tokens'] >= 4000 and part['truncated'] is False and part['exit_code'] == 0)
        position = part['end']
    check('complete input ' + p.name, position == len(text))

def pointer(value, path):
    for part in path.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value

reference_count = 0
def references(value, reader, qid):
    global reference_count
    if isinstance(value, dict):
        if 'quotation' in value and 'path' in value:
            path = Path(value['path'])
            check('reference uses an allowed input', str(path.resolve()) in input_paths)
            if 'json_pointer' in value:
                scope = pointer(cases, '/readers/' + reader + '/answers')
                index = next(i for i, entry in enumerate(scope) if entry['id'] == qid)
                check('citation belongs to same complete original entry', value['json_pointer'].startswith(f'/readers/{reader}/answers/{index}/'))
                field = pointer(cases, value['json_pointer'])
                start, end = value['unicode_range_within_field']
            else:
                field = path.read_text()
                start, end = value['unicode_range']
            check('literal reference span', isinstance(field, str) and field[start:end] == value['quotation'])
            reference_count += 1
        for nested in value.values():
            references(nested, reader, qid)
    elif isinstance(value, list):
        for nested in value:
            references(nested, reader, qid)

fact_count = 0
for row in rows:
    reader, qid = row['reader'], row['id']
    old = next(x for x in original['readers'][reader]['grades'] if x['id'] == qid)
    check('original grade preserved ' + reader + qid, row['original_grade'] == old['grade'])
    mapping = maps[qid]
    check('literal actual question ' + qid, row['actual_question'] == mapping['question'])
    parts = row['requested_part_assessment']
    check('every mapped clause once ' + reader + qid, len(parts) == len(mapping['requested_clauses']) and {x['clause_id'] for x in parts} == {x['clause_id'] for x in mapping['requested_clauses']})
    for part in parts:
        clause = next(x for x in mapping['requested_clauses'] if x['clause_id'] == part['clause_id'])
        facts = part['fact_assessments']
        check('every mapped fact index once ' + reader + qid, len(facts) == len(clause['required_facts']) and {x['fact_index'] for x in facts} == set(range(1, len(clause['required_facts']) + 1)))
        for fact in facts:
            check('fixed mapped expected fact ' + reader + qid, fact['expected'] == clause['required_facts'][fact['fact_index'] - 1])
            fact_count += 1
    scope = row['entry_scope_checked']
    entry = pointer(cases, scope['json_pointer'])
    check('whole original entry identified ' + reader + qid, entry['id'] == qid and set(scope['all_original_fields_examined']) == set(entry) and scope['entire_attached_quotations_examined'] is True and scope['other_reader_or_entry_used_to_fill_facts'] is False)
    check('case resolved ' + reader + qid, row['unresolved'] is False)
    references(row, reader, qid)
check('decision counts', dict(collections.Counter(x['adjudicated_grade'] for x in rows)) == {k: v for k, v in report['decision_counts'].items() if v})
check('no unresolved adjudications', report['unresolved_adjudications'] == [] and report['unresolved_count'] == 0)
check('no genuine key or map findings', report['genuine_key_or_map_findings'] == [])
overlay = {}
for reader, data in original['readers'].items():
    replacements = {x['id']: x['adjudicated_grade'] for x in rows if x['reader'] == reader}
    overlay[reader] = dict(collections.Counter(replacements.get(x['id'], x['grade']) for x in data['grades']))
proof = {'all_passed': True, 'checks': len(checks), 'check_labels': checks, 'complete_cases': len(rows), 'complete_fact_assessments': fact_count, 'literal_same_entry_and_summary_references_checked': reference_count, 'original_report_sha256': H(A / 'adjudication.json'), 'original_results_sha256': H(D / 'results.json'), 'adjudicated_totals': overlay, 'limitation': 'Filesystem/reference/declared-delivery proof only. Actual recorded transport, actual model settings and parent semantic review are separate.'}
dest = A / 'structural-reference-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps({k: v for k, v in proof.items() if k != 'check_labels'}))
