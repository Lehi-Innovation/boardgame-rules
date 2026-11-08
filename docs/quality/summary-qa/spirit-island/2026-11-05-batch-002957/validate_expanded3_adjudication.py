"""Check frozen complete adjudication coverage and literal references, without rescoring."""
from pathlib import Path
import collections
import hashlib
import json

B = Path(__file__).resolve().parent
D = B / 'expanded-iteration-03'
A = D / 'adjudication-01'
load = lambda p: json.loads(Path(p).read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
report = load(A / 'adjudication.json')
cases = load(A / 'raw-cases.json')
maps = {x['id']: x for x in load(A / 'asked-facts.json')['questions']}
original = load(D / 'results.json')
checks = []
def check(label, condition):
    assert condition, label
    checks.append(label)

expected = {(x['reader'], x['id']) for x in cases['requested_cases']}
rows = report['adjudications']
check('all 19 cases exactly once', len(rows) == len(expected) == 19 and {(x['reader'], x['id']) for x in rows} == expected)
check('declared expected cases', {(x['reader'], x['id']) for x in report['expected_cases']} == expected)
inputs = {(D / 'summary-snapshot.md').resolve()} | {(A / n).resolve() for n in ['questions.json', 'answer-key.json', 'asked-facts.json', 'raw-cases.json']}
check('exact five input paths', {Path(x['path']).resolve() for x in report['inputs_read']} == inputs)
for inp in report['inputs_read']:
    p = Path(inp['path']); text = p.read_text()
    check('hash ' + p.name, inp['sha256'] == H(p))
    check('lengths ' + p.name, inp['length_unicode_characters'] == len(text) and inp['length_bytes'] == p.stat().st_size)
    pos = 0
    for part in inp['read_ranges']:
        check('bounded declared complete range', part['start'] == pos and 0 < part['end'] - pos <= 6000 and part['returned_literal_range_length'] == part['end'] - pos and part['tool_max_output_tokens'] >= 4000 and part['truncated'] is False and part['truncation_checked'] is True)
        pos = part['end']
    check('complete input ' + p.name, pos == len(text) and inp['complete_contiguous_coverage'] is True and inp['all_range_tool_calls_exit_code'] == 0)

def pointer(value, path):
    for part in path.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value

refs = facts = 0
for reader, data in cases['readers'].items():
    rawpath = D / f'{reader}-raw.json'
    if not rawpath.exists():
        candidates = [p for p in D.glob('*.json') if H(p) == cases['original_raw_output_sha256'][reader]]
        assert len(candidates) == 1, (reader, candidates)
        rawpath = candidates[0]
    raw = load(rawpath)
    check('original reader hash ' + reader, H(rawpath) == cases['original_raw_output_sha256'][reader])
    originals = {x['id']: x for x in raw['answers']}
    for entry in data['answers']:
        check('complete unchanged entry ' + reader + entry['id'], entry == originals[entry['id']])
for row in rows:
    reader, qid = row['reader'], row['id']
    old = next(x for x in original['readers'][reader]['grades'] if x['id'] == qid)
    check('original grade ' + reader + qid, row['original_grade'] == old['grade'])
    mapping = maps[qid]; parts = row['requested_part_assessment']
    check('every clause once ' + reader + qid, len(parts) == len(mapping['requested_clauses']) and {x['clause_id'] for x in parts} == {x['clause_id'] for x in mapping['requested_clauses']})
    index = next(i for i, x in enumerate(cases['readers'][reader]['answers']) if x['id'] == qid)
    for part in parts:
        clause = next(x for x in mapping['requested_clauses'] if x['clause_id'] == part['clause_id'])
        check('literal requested clause', part['actual_requested_clause'] == clause['actual_requested_clause'])
        fs = part['fact_assessments']
        check('every mapped fact once', len(fs) == len(clause['required_facts']) and {x['fact_index'] for x in fs} == set(range(1, len(clause['required_facts']) + 1)))
        for fact in fs:
            check('literal expected fact', fact['expected'] == clause['required_facts'][fact['fact_index'] - 1]); facts += 1
            for ref in fact['same_entry_references']:
                check('reference in same original entry', ref['json_pointer'].startswith(f'/readers/{reader}/answers/{index}/'))
                field = pointer(cases, ref['json_pointer'])
                check('literal same-entry quotation', isinstance(field, str) and bool(ref['quotation']) and ref['quotation'] in field); refs += 1
            for ref in fact['summary_support']['references']:
                p = Path(ref['path']).resolve()
                check('reference in frozen summary', p == (D / 'summary-snapshot.md').resolve())
                check('literal summary span', p.read_text()[ref['start']:ref['end']] == ref['text']); refs += 1
    check('resolved ' + reader + qid, row['unresolved'] is False)
check('decision counts', dict(collections.Counter(x['adjudicated_grade'] for x in rows)) == {k:v for k,v in report['decision_counts'].items() if v})
check('no unresolved cases', report['unresolved_adjudications'] == [])
check('no reported key or map findings', report['genuine_key_or_map_findings'] == [])
overlay = {}
for reader, data in original['readers'].items():
    replacements = {x['id']:x['adjudicated_grade'] for x in rows if x['reader'] == reader}
    overlay[reader] = dict(collections.Counter(replacements.get(x['id'], x['grade']) for x in data['grades']))
proof = {'all_passed':True,'checks':len(checks),'check_labels':checks,'complete_cases':len(rows),'complete_fact_assessments':facts,'literal_references_checked':refs,'original_report_sha256':H(A/'adjudication.json'),'original_results_sha256':H(D/'results.json'),'adjudicated_totals':overlay,'limitation':'Filesystem/reference and declared delivery checks only; actual delivery, model settings and parent semantic review remain separate.'}
dest = A / 'structural-reference-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({k:v for k,v in proof.items() if k != 'check_labels'}))
