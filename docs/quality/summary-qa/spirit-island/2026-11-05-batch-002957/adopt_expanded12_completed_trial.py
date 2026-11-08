"""Adopt the fully verified trial without assuming a passing or failing outcome."""
from pathlib import Path
import collections
import copy
import hashlib
import json

B = Path(__file__).resolve().parent
D = B / 'expanded-iteration-12'
A = D / 'adjudication-01'
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
original = load(D / 'results.json')
report = load(A / 'adjudication.json')
manifest = load(A / 'input-manifest.json')
validation = load(A / 'structural-reference-validation.json')
actual = load(A / 'adjudicator-actual-delivery-validation.json')
parent = load(A / 'parent-review-receipt.json')
assert validation['all_passed']
assert validation['complete_cases'] == manifest['case_count']
assert validation['complete_fact_assessments'] == manifest['requested_fact_assessment_count']
assert actual['all_actual_source_slices_verified']
assert parent['all_human_fields_read'] and all(x['parent_agrees_with_adjudicated_grade'] for x in parent['decisions'])
assert {(r['reader'], r['id']) for r in parent['decisions']} == {(r['reader'], r['id']) for r in report['adjudications']}
assert not report['unresolved_adjudications'] and not report['genuine_key_or_map_findings']
assert all(not r['unresolved'] for r in report['adjudications'])
assert H(A / 'adjudication.json') == H(A / 'adjudication-original-completed.json') == load(A / 'adjudication-original-freeze.json')['sha256']
assert parent['original_report_sha256'] == H(A / 'adjudication.json')
assert parent['human_view_sha256'] == H(A / 'parent-complete-semantic-view.json')
profile = B / 'runtime/expanded12_adjudication_01-final-completed-projection.json'
meta = load(profile)
assert meta['confirmed_settings'] == [{'model': 'gpt-6.1-sol', 'effort': 'high'}]
assert meta['requested_spawn']['fields']['fork_turns'] == 'none'
primary = load(D / 'grader-actual-delivery-validation.json')
assert primary['all_actual_source_slices_verified'] and len(primary['graders']) == 9
assert load(D / 'grader-delivery-validation.json')['all_passed']
assert load(D / 'primary-grading-structural-validation.json')['all_structure_and_identity_checks_passed']
read_delivery = load(D / 'reader-actual-delivery-validation.json')
assert read_delivery['all_actual_source_slices_verified'] and read_delivery['strict_delivery_protocol_pass']
for r in 'ab':
    assert H(D / f'reader-{r}.json') == H(D / f'reader-{r}-original-completed.json') == load(D / f'reader-{r}-original-freeze.json')['sha256']
    m = load(B / 'runtime' / f'expanded12_reader_{r}-final-completed-projection.json')
    assert m['confirmed_settings'] == [{'model': 'gpt-6-luna', 'effort': 'high'}] * {'a': 3, 'b': 3}[r]
    assert m['requested_spawn']['fields']['fork_turns'] == 'none'

effective = copy.deepcopy(original)
replacement = {(r['reader'], r['id']): r for r in report['adjudications']}
for reader, data in effective['readers'].items():
    for grade in data['grades']:
        if (reader, grade['id']) not in replacement:
            continue
        row = replacement[reader, grade['id']]
        grade['complete_original_grader_proposal'] = copy.deepcopy(grade)
        grade['original_grade'] = grade['grade']
        grade['grade'] = row['adjudicated_grade']
        for k in ['requested_part_assessment', 'reason', 'missing_requested_material_facts', 'contradictions', 'unsupported_guesses']:
            grade[k] = copy.deepcopy(row[k])
        grade['borderline_adjudication_needed'] = False
        grade['complete_independent_adjudication'] = copy.deepcopy(row)
        grade['independent_adjudication_report_sha256'] = H(A / 'adjudication.json')
    counts = collections.Counter(g['grade'] for g in data['grades'])
    data['totals'] = {k: counts[k] for k in ['correct', 'partial', 'incorrect']}
    data['unsupported_guess_count'] = sum(bool(g['unsupported_guesses']) for g in data['grades'])
    assert data['totals'] == validation['adjudicated_totals_pending_semantic_adoption'][reader]
passes = all(
    rr['totals'] == {'correct': 173, 'partial': 0, 'incorrect': 0}
    and all(g['grade'] == 'correct' and not g['missing_requested_material_facts'] and not g['contradictions'] and not g['unsupported_guesses'] for g in rr['grades'])
    for rr in effective['readers'].values()
)
status = 'COMPLETED_DELIVERY_QUALIFIED_FACTUAL_PASS' if passes else 'COMPLETED_DELIVERY_QUALIFIED_FACTUAL_FAILURE'
effective.update(
    unresolved_adjudications=[],
    original_results={'path': str(D / 'results.json'), 'sha256': H(D / 'results.json')},
    complete_independent_adjudication={'path': str(A / 'adjudication.json'), 'sha256': H(A / 'adjudication.json'), 'case_count': len(replacement), 'fact_assessment_count': validation['complete_fact_assessments'], 'decision_counts': report['decision_counts']},
    passes_full_bank=passes, trial_status=status,
    all173_questions_and506_active_required_facts_per_reader_preserved=True,
)
p = D / 'results-adjudicated.json'
assert not p.exists()
p.write_text(json.dumps(effective, indent=2, ensure_ascii=False) + '\n')

files = [
    'adjudication.json', 'adjudication-original-completed.json', 'adjudication-original-freeze.json',
    'input-manifest.json', 'questions.json', 'answer-key.json', 'asked-facts.json', 'raw-cases.json',
    'adjudicator-prompt.txt', 'dispatch-manifest.json', 'adjudicator-actual-delivery-validation.json',
    'structural-reference-validation.json', 'parent-review-receipt.json',
    'parent-view-reconstruction-validation.json', 'parent-complete-semantic-view.json',
    'parent-technical-input-delivery-sidecar.json',
]
adoption = {
    'adopted': True, 'semantic_verdict': 'COMPLETE_ADJUDICATION_ACCEPTED',
    'unresolved': 0, 'complete_case_count': len(replacement),
    'complete_fact_assessments': validation['complete_fact_assessments'],
    'actual_source_ranges': sum(len(i['slices']) for a in actual['adjudicators'] for i in a['inputs']),
    'literal_same_entry_references': validation['literal_same_entry_references'],
    'literal_summary_spans': validation['literal_summary_references'],
    'structural_reference_checks': validation['checks'],
    'genuine_key_or_map_findings': [],
    'actual_model': 'gpt-6.1-sol/high', 'actual_contexts': 1, 'initial_fork_turns': 'none',
    'adjudicated_totals': validation['adjudicated_totals_pending_semantic_adoption'],
    'evidence': {name: H(A / name) for name in files},
    'completed_model_profile': {'path': str(profile), 'sha256': H(profile)},
    'original_results_sha256': H(D / 'results.json'),
    'adjudicated_results_sha256': H(D / 'results-adjudicated.json'),
    'parent_review_scope': f"All {len(replacement)} selected cases, all {validation['complete_fact_assessments']} fact assessments and every human field actually read in full, including repeated complete quotations. Other {346-len(replacement)} primary entries entrusted to qualified fresh full-input graders; no claimed parent regrade.",
    'no_reader_bank_summary_or_threshold_change': True,
    'full_pair_factual_PASS': passes,
    'stamp_publication_or_goal_completion_authorized': False,
}
p = A / 'adoption.json'
assert not p.exists()
p.write_text(json.dumps(adoption, indent=2) + '\n')
owned = ['input-manifest.json', 'reader-a.json', 'reader-b.json', 'reader-a-original-freeze.json', 'reader-b-original-freeze.json', 'reader-pre-authoring-delivery-validation.json', 'reader-actual-delivery-validation.json', 'operative-unit-boundary-validation.json', 'grader-delivery-validation.json', 'grader-actual-delivery-validation.json', 'primary-grading-structural-validation.json', 'results.json', 'results-adjudicated.json', 'adjudication-01/adoption.json']
whole = {
    'trial_status': status, 'benchmark': 'expanded-v24', 'summary_sha256': H(D / 'summary-snapshot.md'),
    'question_count': 173, 'required_facts_per_reader': 506, 'full_original_entries': 346,
    'complete_primary_fact_assessments': 1012,
    'full_pair_factual_PASS': passes, 'adjudicated_totals': adoption['adjudicated_totals'],
    'fresh_primary_graders': 9,
    'actual_primary_source_ranges': sum(len(i['slices']) for g in primary['graders'] for i in g['inputs']),
    'complete_set_adjudication': {'cases': len(replacement), 'facts': validation['complete_fact_assessments'], 'actual_source_ranges': adoption['actual_source_ranges'], 'unresolved': 0},
    'evidence': {name: H(D / name) for name in owned},
    'all_originals_preserved': True, 'bank_key_map_scope_and_summary_changed_during_evaluation': False,
    'no_threshold_change_or_reader_resampling': True,
    'stamp_publication_or_goal_completion_authorized': False,
}
p = D / 'completed-trial-adoption.json'
assert not p.exists()
p.write_text(json.dumps(whole, indent=2) + '\n')
print(json.dumps({'trial_status': status, 'totals': whole['adjudicated_totals'], 'completed_trial_adoption_sha256': H(p), 'full_pair_factual_PASS': passes}))
