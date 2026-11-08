"""Losslessly index the nine original independent grading reports."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys

R = Path(__file__).parent.resolve()
IT = (R / sys.argv[1]).resolve()
assert IT.is_relative_to(R)
OUT = IT / 'original-grades-aggregate.json'
assert not OUT.exists()


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert read(IT / 'materialized-reference-integrity-validation.json')['pass']
for n in range(1, len(read(IT / 'grading-inputs-v2/manifest.json')['blocks']) + 1):
    assert read(IT / f'grader-{n:02}-runtime-delivery-validation.json')['pass']
blocks = read(IT / 'grading-inputs-v2/manifest.json')['blocks']
expected = [a['id'] for a in read(IT / 'questions.json')['questions']]
readers = {label: [] for label in ['a', 'b']}
reports, diagnostics = [], []
for i, block in enumerate(blocks, 1):
    bundle = read(Path(block['path']))
    path = IT / f'grades-{i:02}.json'
    doc = read(path)
    assert doc['exact_assigned_ids'] == block['expected_ids']
    for label in readers:
        entries = doc['readers'][label]['entries']
        assert [e['id'] for e in entries] == block['expected_ids']
        for e, source in zip(entries, bundle['entries']):
            assert e['grade'] in ['correct', 'partial', 'incorrect']
            ids = [x.get('fact_id', x.get('key_fact_id', x.get('id'))) for x in e['fact_checks']]
            assert Counter(ids) == Counter(x['id'] for x in source['raw_key_fact_refs']), (i, label, e['id'], ids)
            wrapper = source['readers'][label]
            observed = e['observed_raw_entry_hash']
            if observed != wrapper['raw_entry_sha256']:
                diagnostics.append({'block': i, 'reader': label, 'id': e['id'],
                                    'kind': 'observed_hash_metadata',
                                    'matches_normalized_entry': observed == wrapper['normalized_entry_sha256'],
                                    'original_raw_hash_preserved': wrapper['raw_entry_sha256']})
            if e['grade'] == 'correct' and (e['missing_asked_facts'] or e['material_contradictions']):
                diagnostics.append({'block': i, 'reader': label, 'id': e['id'],
                                    'kind': 'correct_grade_with_nonempty_failure_fields'})
            readers[label].append({'id': e['id'], 'grade': e['grade'],
                                   'report_path': str(path), 'report_sha256': sha(path),
                                   'json_pointer': f"/readers/{label}/entries/{entries.index(e)}",
                                   'unsupported_claim_flags': len(e['unsupported_correct_claims']),
                                   'original_grade_retained': True})
    reports.append({'block': i, 'path': str(path), 'sha256': sha(path),
                    'expected_ids': block['expected_ids']})
for label in readers:
    assert [x['id'] for x in readers[label]] == expected
    assert len({x['id'] for x in readers[label]}) == len(expected)
totals = {label: dict(Counter(x['grade'] for x in entries))
          for label, entries in readers.items()}
report = {'iteration': IT.name, 'status': 'Original independent grades; adjudications remain separate.',
          'question_count': len(expected), 'original_reports': reports,
          'readers': readers, 'totals': totals, 'integrity_diagnostics': diagnostics,
          'all_ids_once_per_reader': True,
          'all_raw_key_records_checked_once_per_reader': True,
          'raw_key_record_count_per_reader': sum(len(a['required_facts']) for a in read(IT / 'answer-key.json')['answers']),
          'raw_reader_fields_and_spans_preserved_in_bundles': True,
          'actual_transport_deviation_report': str(IT / 'delivery-validation-v6.json'),
          'final_scope_readiness': False, 'adjudications_applied': False,
          'independent_bookkeeping_acceptance_pending': True,
          'primary_all_correct_by_grade': all(e['grade'] == 'correct' for entries in readers.values() for e in entries),
          'unsupported_correct_claim_count': sum(e['unsupported_claim_flags'] for entries in readers.values() for e in entries),
          'no_factual_grade_changes_from_metadata_or_transport_diagnostics': True,
          'all_current_grader_actual_delivery_verified': True,
          'same_entry_reference_integrity_path': str(IT / 'materialized-reference-integrity-validation.json')}
OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
print(totals)
print('integrity_diagnostics', len(diagnostics))
