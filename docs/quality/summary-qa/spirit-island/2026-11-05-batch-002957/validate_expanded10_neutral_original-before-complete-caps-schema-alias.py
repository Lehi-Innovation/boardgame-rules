"""Validate the original neutral schema without rewriting its report or findings."""
from pathlib import Path
import collections
import hashlib
import json

B = Path(__file__).resolve().parent
D = B / 'expanded-iteration-10'
A = D / 'adjudication-01'
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
report = load(A / 'adjudication.json')
cases = load(A / 'raw-cases.json')
manifest = load(A / 'input-manifest.json')
maps = {q['id']: q for q in load(A / 'asked-facts.json')['questions']}
original = load(D / 'results.json')
checks = []

def check(ok, label):
    assert ok, label
    checks.append(label)

def pointer(value, path):
    for k in path.strip('/').split('/'):
        k = k.replace('~1', '/').replace('~0', '~')
        value = value[int(k)] if isinstance(value, list) else value[k]
    return value

def strings(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in strings(v)]
    return []

allowed = {Path(p).resolve() for p in manifest['inputs']}
expected = {(x['reader'], x['id']) for x in cases['requested_cases']}
rows = report['adjudications']
check(collections.Counter((x['reader'], x['id']) for x in rows) == collections.Counter(expected), 'all selected cases exactly once')
check(collections.Counter((x['reader'], x['id']) for x in report['expected_cases']) == collections.Counter(expected), 'exact declared case set')
check(len(rows) == manifest['case_count'], 'manifest case count')
check(len(report['inputs_read']) == 5 and {Path(x['path']).resolve() for x in report['inputs_read']} == allowed, 'exact five whole declared inputs')
declared_ranges = 0
for inp in report['inputs_read']:
    p = Path(inp['path'])
    text = p.read_text()
    check(inp['sha256'] == H(p) and inp['unicode_character_length'] == len(text) and inp['byte_length'] == p.stat().st_size, 'exact input identity ' + p.name)
    pos = 0
    for part in inp['read_ranges']:
        start, end = part.get('start', part.get('start_inclusive')), part.get('end', part.get('end_exclusive'))
        check(start == pos and 0 < end - start <= 6000 and part.get('characters', end-start) == end - start and isinstance(part.get('tool_output_cap_tokens',part.get('max_output_tokens',part.get('output_cap_tokens'))), int) and part.get('tool_output_cap_tokens',part.get('max_output_tokens',part.get('output_cap_tokens'))) >= 4000 and not part['truncated'], 'declared contiguous bounded range ' + p.name + str([start, end]))
        check(bool(part.get('truncation_check', inp.get('truncation_check',inp.get('coverage_check')))) and part.get('complete_literal_range_delivered', True), 'original complete-range/truncation declaration; actual record identifiers independently verified')
        pos = end
        declared_ranges += 1
    check(pos == len(text) and (inp.get('complete_contiguous_read',inp.get('contiguous_complete_coverage')) is True or bool(inp.get('coverage_check')) or (inp.get('coverage_complete') is True and inp.get('contiguous') is True)), 'whole declared input ' + p.name)

for r, data in cases['readers'].items():
    raw = load(D / (r + '.json'))
    by = {e['id']: e for e in raw['answers']}
    check(H(D / (r + '.json')) == cases['original_raw_output_sha256'][r], 'whole original reader hash ' + r)
    for entry in data['answers']:
        check(entry == by[entry['id']], 'entire original entry unchanged ' + r + entry['id'])

guide_path = (D / 'summary-snapshot.md').resolve()
guide = guide_path.read_text()
samerefs = summaryrefs = auxiliaryrefs = facts = 0
same_field_refs = 0
exactranges = withinranges = 0
for row in rows:
    r, q = row['reader'], row['id']
    old = next(x for x in original['readers'][r]['grades'] if x['id'] == q)
    check(row['original_grade'] == old['grade'], 'original grade binding ' + r + q)
    index = next(i for i, x in enumerate(cases['readers'][r]['answers']) if x['id'] == q)
    prefix = f'/readers/{r}/answers/{index}'
    parts = row['requested_part_assessment']
    clauses = maps[q]['requested_clauses']
    check(collections.Counter(p['clause_id'] for p in parts) == collections.Counter(c['clause_id'] for c in clauses), 'all mapped clauses exactly once ' + r + q)
    for part in parts:
        clause = next(c for c in clauses if c['clause_id'] == part['clause_id'])
        check(part['actual_requested_clause'] == clause['actual_requested_clause'], 'exact literal ask ' + r + q)
        fs = part['fact_assessments']
        check(collections.Counter(f['fact_index'] for f in fs) == collections.Counter(range(1, len(clause['required_facts']) + 1)), 'all mapped fact indices exactly once ' + r + q)
        for fact in fs:
            facts += 1
            check(fact['expected'] == clause['required_facts'][fact['fact_index'] - 1], 'literal mapped expected fact ' + r + q)
            check(bool(fact['same_entry_references']) and bool(fact['summary_support']) and bool(fact['observed']) and bool(fact['outcome']), 'assessment and evidence fields present ' + r + q)

    # Check all fact, contradiction, omission and unasked-context citations.
    def walk(value, inherited_source=None):
        global samerefs, summaryrefs, auxiliaryrefs, exactranges, withinranges, same_field_refs
        if isinstance(value, list):
            for child in value:
                walk(child, inherited_source)
        elif isinstance(value, dict):
            citation_source = value.get('path', value.get('source', inherited_source))
            if 'json_pointer' in value and citation_source is not None:
                p = Path(citation_source).resolve()
                quote = value.get('quotation',value.get('quote',value.get('text')))
                check(p in allowed, 'allowed exact JSON field reference input')
                node = pointer(load(p), value['json_pointer'])
                if quote is not None:
                    check(isinstance(quote,str) and bool(quote) and any(quote in s for s in strings(node)), 'literal original JSON quotation')
                if p == (A / 'raw-cases.json').resolve():
                    check(value['json_pointer'] == prefix or value['json_pointer'].startswith(prefix + '/'), 'citation belongs to same complete original entry')
                    if quote is None:
                        same_field_refs += 1
                    else:
                        samerefs += 1
                else:
                    check(p.name in ['questions.json', 'answer-key.json', 'asked-facts.json'], 'auxiliary question/key/map citation')
                    auxiliaryrefs += 1
            if ('unicode_character_range' in value or 'range' in value or 'unicode_range_start_inclusive_end_exclusive' in value or ('start' in value and 'end' in value)) and any(k in value for k in ['quotation','quote','text']) and citation_source is not None:
                check(Path(citation_source).resolve() == guide_path, 'citation refers to frozen summary')
                start, end = value.get('unicode_character_range',value.get('range',value.get('unicode_range_start_inclusive_end_exclusive',[value.get('start'),value.get('end')])))
                quote = value.get('quotation',value.get('quote',value.get('text')))
                check(isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(guide) and isinstance(quote, str) and bool(quote) and quote in guide[start:end], 'literal summary quotation within exact declared span')
                summaryrefs += 1
                exactranges += guide[start:end] == quote
                withinranges += guide[start:end] != quote
            for child in value.values():
                walk(child, citation_source)

    walk(row)
    check(row['adjudicated_grade'] in ['correct', 'partial', 'incorrect'] and isinstance(row['unresolved'], bool), 'valid decision fields ' + r + q)

check(facts == manifest['requested_fact_assessment_count'], 'complete mapped fact assessment count')
check(samerefs + same_field_refs >= facts and summaryrefs >= facts, 'original same-entry field/quotation and literal source references actually matched')
check(dict(collections.Counter(r['adjudicated_grade'] for r in rows)) == {k: v for k, v in report['decision_counts'].items() if v}, 'decision counts agree')
check(H(A / 'adjudication.json') == H(A / 'adjudication-original-completed.json') == load(A / 'adjudication-original-freeze.json')['sha256'], 'entire frozen original report unchanged')
overlay = {}
for r, data in original['readers'].items():
    replacements = {x['id']: x['adjudicated_grade'] for x in rows if x['reader'] == r}
    counts = collections.Counter(replacements.get(g['id'], g['grade']) for g in data['grades'])
    overlay[r] = {k: counts[k] for k in ['correct', 'partial', 'incorrect']}
out = {
    'all_passed': True, 'checks': len(checks), 'check_labels': checks,
    'complete_cases': len(rows), 'complete_fact_assessments': facts,
    'declared_complete_source_ranges': declared_ranges,
    'literal_same_entry_references': samerefs,
    'exact_same_entry_field_pointer_references_without_new_quotation': same_field_refs,
    'literal_summary_references': summaryrefs,
    'literal_auxiliary_question_key_map_references': auxiliaryrefs,
    'summary_quotations_equal_exact_range': exactranges,
    'summary_quotations_within_larger_range': withinranges,
    'expected_strings_exact_map_matches': facts,
    'adjudicated_totals_pending_semantic_adoption': overlay,
    'unresolved_case_count': sum(r['unresolved'] for r in rows),
    'unresolved_adjudications': report['unresolved_adjudications'],
    'genuine_key_or_map_findings': report['genuine_key_or_map_findings'],
    'original_report_sha256': H(A / 'adjudication.json'),
    'original_results_sha256': H(D / 'results.json'),
    'limitations': 'Literal structure/reference checks do not prove interpretation, actual delivery or cognition. Actual runtime delivery/model proof and full parent semantic review remain separate gates. No original output or grading criterion changed.'
}
p = A / 'structural-reference-validation.json'
assert not p.exists()
p.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'check_labels'}))
