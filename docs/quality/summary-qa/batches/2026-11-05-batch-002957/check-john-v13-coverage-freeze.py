"""Verify the reviewed coverage freeze and retain its exact reuse qualifications."""
from pathlib import Path
import copy
import hashlib
import json
from datetime import datetime, timezone

B = Path(__file__).resolve().parent
R = B.parents[4] / 'docs/quality/summary-qa/john-company-second-edition' / B.name
load = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
proposal = R / 'benchmark-revision13-proposal'
review_dir = proposal / 'independent-review-02'
review = load(review_dir / 'source-key-coverage-review.json')
assert review['verdict'] == 'PASS'
assert not review['independence']['prohibited_inputs_read']
assert review['accounting']['questions'] == 116 and review['accounting']['material_atoms'] == 914
assert review['accounting']['source_supported_atoms'] == 914
assert review['accounting']['actually_requested_or_clear_implication_atoms'] == 914
assert review['accounting']['remaining_meaningful_distinct_questions_required'] == 0
prior = review['prior_complete_review']
assert sha(Path(prior['path'])) == prior['sha256']
assert sha(proposal / 'independent-review-01/source-read-record.json') == prior['source_read_record_sha256']
assert sha(proposal / 'independent-review-01/input-hashes.json') == prior['original_inputs_hash_record_sha256']
checked = []
for version in ('independent-review-01', 'independent-review-02'):
    for entry in load(proposal / version / 'input-hashes.json')['files']:
        p = Path(entry['path'])
        assert sha(p) == entry['sha256'] and p.stat().st_size == entry['bytes'], str(p)
        checked.append(str(p))
passes = load(proposal / 'revision02/coverage-passes-24-26.json')['passes']
assert [p['pass'] for p in passes[-2:]] == [25, 26]
assert all(p['new_count'] == 0 for p in passes[-2:])
assert review['working_saturation']['new_gap_count'] == 0
assert not review['working_saturation']['additional_meaningful_distinct_question_required']
candidate = proposal / 'revision02/bank'
frozen = R / 'expanded-v13-complete-requested-scope'
for name in ('questions.json', 'answer-key.json'):
    a, b = load(candidate / name), load(frozen / name)
    a.pop('status'); b.pop('status')
    assert a == b, name
a, b = load(candidate / 'requested-fact-scope-reviewed.json'), load(frozen / 'requested-fact-scope-reviewed.json')
cleanup = load(review_dir / 'parent-completion-verification.json')['post_review_rationale_cleanup']
row = next(x for x in a['questions'] if x['id'] == cleanup['id'])
assert len(row['fact_justifications']) == cleanup['occurrences'] == 7
for fact in row['fact_justifications']:
    assert fact['requested_scope_rationale'] == cleanup['before']
    fact['requested_scope_rationale'] = cleanup['after']
for field in ('status', 'revision', 'full_scoped_signoff', 'independent_final_review'):
    a.pop(field, None); b.pop(field, None)
assert a == b
a, b = load(candidate / 'grading-scope.json'), load(frozen / 'grading-scope.json')
for field in ('status', 'fixed_before_new_readers'):
    a.pop(field); b.pop(field)
assert a == b
questions = load(frozen / 'questions.json')['questions']
assert questions[:113] == load(R / 'expanded-v12-complete-requested-scope/questions.json')['questions']
scope = load(frozen / 'requested-fact-scope-reviewed.json')['questions']
assert len(scope) == len(questions) == 116
assert sum(len(row['material_requested_facts']) for row in scope) == 914
rows = review['all116_questions_and914_atoms']
for q, s, row in zip(questions, scope, rows):
    assert q['id'] == s['id'] == row['id'] and q['question'] == row['question']
    assert row['verdict'] == 'PASS'
    assert [atom['fact'] for atom in row['atoms']] == s['material_requested_facts']
    assert all(atom['source_truth'] == 'SUPPORTED' and
               atom['asked_scope'] == 'REQUESTED_MATERIAL_OR_CLEAR_IMPLICATION' for atom in row['atoms'])
report = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'review_sha256': sha(review_dir / 'source-key-coverage-review.json'),
          'questions': 116, 'material_asked_facts': 914, 'input_hash_bindings': len(checked),
          'two_zero_addition_passes': [25, 26], 'new_gaps': 0,
          'all113_prior_question_objects_preserved': True,
          'post_review_changes': 'Administrative freeze metadata and exactly seven reviewer-requested Q025 rationale corrections; no question, key or mandatory fact changed.',
          'review_reuse_qualification': review['independence']['prior_review_reuse_explicitly_authorized'],
          'independent_review_context': 'Initially fresh source-only reviewer; review02 is a continuation of its own complete review01 with exact unchanged-input inheritance and a renewed 13-candidate source challenge. Not claimed to be another new context.',
          'Q115_novelty_credit': 0,
          'limits': review['working_saturation']['limits']}
out = B / 'coordinator-checks/john-v13-coverage-freeze.json'
assert not out.exists()
out.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'verified': True, 'questions': 116, 'asked_facts': 914, 'bindings': len(checked), 'report': str(out)}))
