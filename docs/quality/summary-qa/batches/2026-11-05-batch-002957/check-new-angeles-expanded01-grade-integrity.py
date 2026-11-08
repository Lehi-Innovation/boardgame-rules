"""Rebind all186 initial expanded grades to complete originals and frozen v7 data."""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
R = ROOT / 'docs/quality/summary-qa/new-angeles' / B.name
D = R / 'expanded-luna-iteration-01'
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
canonical = lambda obj: hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True,
                                                  separators=(',', ':')).encode()).hexdigest()
questions = {x['id']: x for x in load(D / 'questions.json')['questions']}
key = {x['id']: x for x in load(R / 'expanded-candidate-v7/answer-key.json')['answers']}
scope = {x['id']: x for x in load(R / 'expanded-candidate-v7/asked-clause-map.json')}
raw_paths = {w: D / ('reader-' + w + '.json') for w in 'ab'}
raw = {w: {x['id']: x for x in load(p)['answers']} for w, p in raw_paths.items()}
plan = load(D / 'grading/input-manifest.json')
totals, facts, seen = {w: Counter() for w in 'ab'}, {w: 0 for w in 'ab'}, set()
reports, diagnostics, assessments = [], [], Counter()
for task in plan['blocks']:
    pack_path, report_path = Path(task['pack']), Path(task['output'])
    assert H(pack_path) == task['pack_sha256']
    pack, report = load(pack_path), load(report_path)
    ids = task['ids']
    assert pack['ids'] == ids
    for name, digest in pack['source_file_hashes'].items():
        assert H(Path(name)) == digest
    assert pack['questions'] == [questions[i] for i in ids]
    assert pack['fixed_key'] == [key[i] for i in ids]
    assert pack['asked_clause_map'] == [scope[i] for i in ids]
    for w in 'ab':
        assert pack['complete_raw_reader_entries'][w] == [raw[w][i] for i in ids]
        for ident in ids:
            assert pack['raw_entry_sha256'][w][ident] == canonical(raw[w][ident])
    records = report.get('grades', report.get('records'))
    assert isinstance(records, list) and len(records) == len(ids) * 2
    expected = {(w, ident) for w in 'ab' for ident in ids}
    actual = set()
    for record in records:
        w, ident = record['reader'], record['id']
        assert (w, ident) in expected and (w, ident) not in actual
        assert record['raw_entry_sha256'] == canonical(raw[w][ident])
        actual.add((w, ident))
        clauses = record['asked_fact_assessments']
        required = scope[ident]['asked_facts']
        assert len(clauses) == len(required)
        for index, (clause, requirement) in enumerate(zip(clauses, required), 1):
            if clause['required_clause'] != requirement:
                diagnostics.append({'reader': w, 'id': ident, 'requirement_index': index,
                                    'kind': 'grader_expected_text_paraphrase'})
            assessments[clause['assessment']] += 1
        if record['material_wrong_claims']:
            assert record['label'] == 'Incorrect'
        assert record['label'] in ['Correct', 'Partial', 'Incorrect']
        totals[w][record['label']] += 1
        facts[w] += len(clauses)
    assert actual == expected and not seen.intersection(actual)
    seen.update(actual)
    reports.append({'path': str(report_path), 'sha256': H(report_path),
                    'pack': str(pack_path), 'pack_sha256': H(pack_path), 'ids': ids})
assert len(reports) == 6 and seen == {(w, i) for w in 'ab' for i in questions}
expected_facts = sum(len(x['asked_facts']) for x in scope.values())
assert all(facts[w] == expected_facts for w in 'ab')
result_file = D / 'results.json'
result = load(result_file)
counts = {w: {label: totals[w][label] for label in ['Correct', 'Partial', 'Incorrect']} for w in 'ab'}
assert counts == result['counts']['primary_fixed_v7']
v8q = load(R / 'expanded-candidate-v8/questions.json')['questions']
v8key = load(R / 'expanded-candidate-v8/answer-key.json')['answers']
v8scope = {x['id']: x for x in load(R / 'expanded-candidate-v8/asked-clause-map.json')}
assert v8q == list(questions.values())
key_changes = [x['id'] for x in v8key if x != key[x['id']]]
assert key_changes == ['Q73']
assert all(x['expected_answer'] == key[x['id']]['expected_answer'] for x in v8key)
changed = [i for i in scope if scope[i] != v8scope[i]]
assert changed == ['Q73']
assert key['Q10']['required_facts'] == v8key[9]['required_facts']
assert any('reserve+2' in x for x in key['Q10']['required_facts'])
proof = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
         'N': len(questions), 'complete_original_entries': len(seen),
         'mapped_requirement_vector_assessments': facts, 'requirement_assessment_labels': dict(assessments),
         'primary_fixed_v7_scores': counts, 'reports': reports, 'diagnostics': diagnostics,
         'raw_file_sha256': {w: H(p) for w, p in raw_paths.items()},
         'results_sha256_at_check': H(result_file),
         'versioned_scope_correction': {'questions_and_expected_answers_unchanged': True,
             'key_required_scope_rows_changed_only': key_changes,
             'changed_map_records_only': changed,
             'Q73_literal': questions['Q73']['question'], 'old_required': scope['Q73']['asked_facts'],
             'new_required': v8scope['Q73']['asked_facts'],
             'movement_numeric_rule_still_covered_by_Q10': key['Q10']['required_facts'],
             'original_v7_inputs_retained': True},
         'limits': 'Integrity and literal-scope continuity only. All original answer fields and every mapped requirement vector remain linked to frozen v7 packets, with correct material-error labels. No semantic grade upgrade comes from this bookkeeping. One fresh neutral and source-only Q73 correction are reviewed separately. Q73 asks an upper fixed amount and then only whether movement can increase threat; the latter numerical2 is not another omission gate. The ordinary Root+2 outcome remains expressly asked/keyed in originalQ10. New v8 pair required on the repaired guide; SG01 unresolved; no full-core/publication/stamp approval.'}
out = B / 'coordinator-checks/new-angeles-expanded01-primary-grade-integrity.json'
out.write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps({'verified': True, 'entries': len(seen), 'requirements_per_reader': expected_facts,
                  'primary': counts, 'diagnostics': len(diagnostics), 'report': str(out)}))
