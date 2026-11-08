"""Index complete corrected grades without changing any factual disposition."""
from collections import Counter
import hashlib
import json
from pathlib import Path

R = Path(__file__).parent.resolve()
IT = R / 'expanded-iteration-02'
OUT = IT / 'corrected-grades-aggregate-v2.json'
assert not OUT.exists()


def read(p):
    return json.loads(p.read_bytes())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


manifest = read(IT / 'grading-inputs-v2/manifest.json')
expected = [q['id'] for q in read(IT / 'questions.json')['questions']]
assert read(IT / 'materialized-reference-integrity-validation-02.json')['pass']
readers = {c: [] for c in 'ab'}
reports, diagnostics, changes = [], [], []
fact_count = {c: 0 for c in 'ab'}
for n, block in enumerate(manifest['blocks'], 1):
    tag = f'{n:02}'
    bundle_path = Path(block['path'])
    assert sha(bundle_path) == block['sha256']
    bundle = read(bundle_path)
    path = IT / f'grades-{tag}-v2.json'
    doc = read(path)
    proof_path = IT / f'grader-{tag}-v2-runtime-delivery-validation.json'
    assert read(proof_path)['pass'], ('Actual complete delivery missing', tag)
    old_path = IT / f'grades-{tag}.json'
    old = read(old_path) if old_path.exists() else None
    assert doc['exact_assigned_ids'] == block['expected_ids']
    for c in readers:
        entries = doc['readers'][c]['entries']
        assert [e['id'] for e in entries] == block['expected_ids']
        old_entries = {e['id']: e for e in old['readers'][c]['entries']} if old else {}
        for index, (e, source) in enumerate(zip(entries, bundle['entries'])):
            assert e['grade'] in ('correct', 'partial', 'incorrect')
            ids = [f.get('fact_id', f.get('key_fact_id', f.get('id'))) for f in e['fact_checks']]
            assert ids == [f['id'] for f in source['raw_key_fact_refs']], (tag, c, e['id'])
            fact_count[c] += len(ids)
            wrapper = source['readers'][c]
            observed = e['observed_raw_entry_hash']
            if observed != wrapper['raw_entry_sha256']:
                diagnostics.append({'block': tag, 'reader': c, 'id': e['id'],
                                    'kind': 'observed_hash_metadata',
                                    'matches_normalized_entry': observed == wrapper['normalized_entry_sha256'],
                                    'original_raw_entry_sha256': wrapper['raw_entry_sha256']})
            if e['grade'] == 'correct' and (e['missing_asked_facts'] or e['material_contradictions']):
                diagnostics.append({'block': tag, 'reader': c, 'id': e['id'],
                                    'kind': 'correct_with_nonempty_failure_fields'})
            prior = old_entries.get(e['id'])
            if prior and prior['grade'] != e['grade']:
                changes.append({'block': tag, 'reader': c, 'id': e['id'],
                                'original_grade': prior['grade'], 'corrected_grade': e['grade'],
                                'original_report_path': str(old_path), 'original_report_sha256': sha(old_path),
                                'corrected_report_path': str(path),
                                'corrected_json_pointer': f'/readers/{c}/entries/{index}'})
            readers[c].append({'id': e['id'], 'grade': e['grade'],
                               'report_path': str(path), 'report_sha256': sha(path),
                               'json_pointer': f'/readers/{c}/entries/{index}',
                               'unsupported_claim_flags': len(e['unsupported_correct_claims']),
                               'raw_entry_sha256': wrapper['raw_entry_sha256']})
    reports.append({'block': tag, 'path': str(path), 'sha256': sha(path),
                    'runtime_delivery_path': str(proof_path),
                    'original_provisional_path': str(old_path) if old else None,
                    'same_original_grader_continuation': bool(old)})

for c in readers:
    assert [e['id'] for e in readers[c]] == expected
    assert len(set(e['id'] for e in readers[c])) == len(expected) == 167
    assert fact_count[c] == 544
totals = {c: {g: Counter(e['grade'] for e in entries)[g]
              for g in ('correct', 'partial', 'incorrect')} for c, entries in readers.items()}
report = {'iteration': IT.name, 'question_count': len(expected), 'reports': reports,
          'status': 'Corrected original assessments; all provisional reports remain preserved. No adjudications applied.',
          'readers': readers, 'totals': totals, 'changed_dispositions': changes,
          'integrity_diagnostics': diagnostics, 'all_ids_once_per_reader': True,
          'all544_raw_key_records_checked_once_per_reader': True,
          'explicit_evidence_reference_integrity_proof': str(IT / 'materialized-reference-integrity-validation-02.json'),
          'all_current_grader_actual_delivery_verified': True,
          'independent_coordinator_bookkeeping_acceptance': False,
          'final_scope_readiness': False, 'adjudications_applied': False}
OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
print(totals)
print('Metadata/consistency diagnostics:', len(diagnostics))
