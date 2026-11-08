"""Independently verify original entries, linked shared quotations and all corrected grades."""
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
D = ROOT / 'docs/quality/summary-qa/cosmic-encounter' / B.name / 'expanded-iteration-02'
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
canonical = lambda value: HB(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                      separators=(',', ':')).encode())
questions = {x['id']: x for x in load(D / 'questions.json')['questions']}
key = {x['id']: x for x in load(D / 'answer-key.json')['answers']}
scope = {x['id']: x for x in load(D / 'actual-question-scope.json')['questions']}
paths = {w: D / ('reader-' + w + '.json') for w in 'ab'}
docs = {w: load(p) for w, p in paths.items()}
data = {w: p.read_bytes() for w, p in paths.items()}
raw = {w: {x['id']: x for x in doc['answers']} for w, doc in docs.items()}
body = (D / 'summary-snapshot.md').read_text()
aggregate_path = D / 'corrected-grades-aggregate-v2.json'
aggregate = load(aggregate_path)
totals, facts, seen = {w: Counter() for w in 'ab'}, {w: 0 for w in 'ab'}, {w: [] for w in 'ab'}
pool = {x['number']: x for x in docs['b']['evidence_units']}
assert len(pool) == len(docs['b']['evidence_units']) == 72
reference_checks, reports, states = [], [], Counter()

def pointer(value, path):
    for part in path.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value

def contains_scalar(value, expected):
    if isinstance(value, dict):
        return any(contains_scalar(v, expected) for v in value.values())
    if isinstance(value, list):
        return any(contains_scalar(v, expected) for v in value)
    return value == expected

def references(value, path=''):
    found = defaultdict(list)
    if isinstance(value, dict):
        for name, child in value.items():
            escaped = name.replace('~', '~0').replace('/', '~1')
            if name == 'evidence' and isinstance(child, list):
                for index, item in enumerate(child):
                    if isinstance(item, int):
                        found[item].append(path + '/' + escaped + '/' + str(index))
            for number, paths_seen in references(child, path + '/' + escaped).items():
                found[number].extend(paths_seen)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            for number, paths_seen in references(child, path + '/' + str(index)).items():
                found[number].extend(paths_seen)
    return found

aliases = ['complete_original_entry', 'raw_reader_record', 'raw_reader_entry',
           'raw_reader_record_preserved', 'preserved_raw_reader_record',
           'preserved_complete_original_entry']
for report_ref in aggregate['reports']:
    report_path = Path(report_ref['path'])
    assert H(report_path) == report_ref['sha256']
    report = load(report_path)
    old_report = Path(report_ref['original_provisional_path']) if report_ref.get('original_provisional_path') else None
    # Each continuation binds its own previous report; schemas place the
    # binding at different depths rather than always at the top level.
    if old_report:
        assert contains_scalar(report, str(old_report)) and contains_scalar(report, H(old_report))
    bundle_path = D / 'grading-inputs-v2' / ('block-' + report_ref['block'] + '.json')
    bundle = load(bundle_path)
    old_bundle_path = D / 'grading-inputs' / ('block-' + report_ref['block'] + '.json')
    old_bundle = load(old_bundle_path)
    assert bundle['summary_sha256'] == HB(body.encode())
    ids = bundle['expected_ids']
    assert [x['id'] for x in bundle['entries']] == ids
    old_by_id = {x['id']: x for x in old_bundle['entries']}
    by_id = {x['id']: x for x in bundle['entries']}
    for ident, entry in by_id.items():
        assert entry['literal_question'] == questions[ident]
        assert entry['key'] == key[ident] and entry['validated_actual_scope'] == scope[ident]
        assert len(entry['raw_key_fact_refs']) == len(key[ident]['required_facts'])
        for w in 'ab':
            meta = entry['readers'][w]
            assert meta['complete_original_entry'] == raw[w][ident]
            old_meta = old_by_id[ident]['readers'][w]
            assert all(meta[name] == value for name, value in old_meta.items())
            assert meta['raw_file_sha256'] == H(paths[w])
            fragment = data[w][meta['start_byte']:meta['end_byte']]
            assert HB(fragment) == meta['raw_entry_sha256'] and json.loads(fragment) == raw[w][ident]
            if w == 'b':
                linked = meta['explicitly_referenced_shared_evidence']
                assert linked['raw_reader_sha256'] == H(paths[w])
                assert linked['pool_field'].lstrip('/') == 'evidence_units'
                assert linked['complete_pool_normalized_sha256'] == canonical(docs[w]['evidence_units'])
                expected = references(raw[w][ident])
                resolved = {x['reference']: x for x in linked['resolved_units']}
                assert set(resolved) == set(expected)
                for number, proof in resolved.items():
                    unit = pool[number]
                    assert proof['original_unit'] == unit and proof['original_unit_sha256'] == canonical(unit)
                    assert sorted(proof['explicit_reference_paths_in_original_entry']) == sorted(expected[number])
                    assert all(pointer(raw[w][ident], p) == number for p in expected[number])
                    span = proof['original_raw_unit_span']
                    fragment = data[w][span['start_byte']:span['end_byte']]
                    assert HB(fragment) == span['raw_sha256'] and json.loads(fragment) == unit
                    assert pointer(docs[w], span['json_pointer']) == unit
                    assert span['normalized_sha256'] == canonical(unit)
                    a, z = unit['source_span']['start'], unit['source_span']['end']
                    assert body[a:z] == unit['text']
                reference_checks.append({'reader': w, 'id': ident, 'explicit_reference_occurrences': sum(map(len, expected.values())),
                                         'unique_resolved_units': len(resolved), 'all_only_original_same_entry_refs': True})
    for w in 'ab':
        entries = report['readers'][w]['entries']
        assert [x['id'] for x in entries] == ids
        for entry in entries:
            ident = entry['id']
            full = [entry[name] for name in aliases if name in entry and isinstance(entry[name], dict)]
            full = [x.get('complete_original_entry', x) for x in full]
            # Input packets preserve all fields. A grader may bind them by hash
            # without repeating the entire original object in its output.
            assert all(x == raw[w][ident] for x in full)
            assert entry['observed_raw_entry_hash'] == by_id[ident]['readers'][w]['raw_entry_sha256']
            ids_seen = [x.get('id', x.get('fact_id', x.get('key_fact_id'))) for x in entry['fact_checks']]
            assert ids_seen == [x['id'] for x in by_id[ident]['raw_key_fact_refs']]
            statuses = [x.get('classification', x.get('asked_portion_status', x.get('status'))) for x in entry['fact_checks']]
            states.update(statuses)
            if entry['material_contradictions'] or 'contradicted' in statuses:
                assert entry['grade'] == 'incorrect'
            if entry['grade'] == 'correct':
                assert not entry['missing_asked_facts'] and 'missing' not in statuses
            assert entry['grade'] in ['correct', 'partial', 'incorrect']
            totals[w][entry['grade']] += 1
            facts[w] += len(ids_seen)
            seen[w].append(ident)
    reports.append({'path': str(report_path), 'sha256': H(report_path), 'original_provisional_report': str(old_report) if old_report else None,
                    'original_provisional_sha256': H(old_report) if old_report else None, 'complete_bundle': str(bundle_path),
                    'complete_bundle_sha256': H(bundle_path), 'ids': ids})
assert len(reports) == 9
assert all(seen[w] == list(questions) and facts[w] == 544 for w in 'ab')
scores = {w: {s: totals[w][s] for s in ['correct', 'partial', 'incorrect']} for w in 'ab'}
assert scores == aggregate['totals']
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'N': len(questions), 'complete_original_entries': sum(map(len, seen.values())),
          'raw_key_fact_assessments': facts, 'fact_status_counts': dict(states),
          'corrected_primary_scores': scores, 'reports': reports,
          'source_dictionary_units': len(pool), 'same_entry_reference_checks': reference_checks,
          'aggregate_sha256': H(aggregate_path), 'raw_file_sha256': {w: H(p) for w, p in paths.items()},
          'limits': 'Root independently verifies all334 original entry byte spans/parsed fields, fixed Q/key/map objects, all1088 raw fact assessments, preserved provisional report hashes and corrected arithmetic. For B, every and only explicitly linked original shared unit, every reference path, actual original global JSON pointer/raw byte span and literal frozen-summary span checked; no unreferenced or other-answer material is borrowed. Same originally fresh graders continued from their own incomplete packets with restored original data, not new independent votes. Models/input delivery and any fresh neutral remain separate. Pair FAIL, no unqualified source scope/readiness/publication/stamp approval.'}
out = B / 'coordinator-checks/cosmic-expanded02-corrected-primary-and-reference-integrity.json'
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'original_entries': result['complete_original_entries'],
                  'fact_assessments': sum(facts.values()), 'shared_units': len(pool),
                  'scores': result['corrected_primary_scores'], 'proof': str(out)}))
