"""Check original primary coverage and identity; factual adoption stays separate."""
from pathlib import Path
import collections
import hashlib
import json

B = Path(__file__).resolve().parent
D = B / 'expanded-iteration-06'
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
maps = {q['id']: q for q in load(D / 'asked-fact-map.json')['questions']}
results = load(D / 'results.json')
checks, paraphrases, extras = [], [], []
facts = literal_clauses = omitted_clause_echoes = 0
for n in range(1, 10):
    p = D / 'grading' / f'block-{n:02d}'
    g = load(p / 'grades.json')
    assert H(p / 'grades.json') == H(p / 'grades-original-completed.json') == load(p / 'original-freeze.json')['sha256']
    checks.append(f'frozen entire original block {n}')
    profile = load(B / 'runtime' / f'expanded6_grade_{n:02d}-final-completed-projection.json')
    assert profile['confirmed_settings'] == [{'model': 'gpt-6.1-sol', 'effort': 'high'}]
    assert profile['requested_spawn']['fields']['fork_turns'] == 'none'
    checks.append(f'one fresh actual Sol61 high context {n}')
    for row in g['grades']:
        r, q = row['reader'], row['id']
        clauses = maps[q]['requested_clauses']
        parts = row['requested_part_assessment']
        assert collections.Counter(x['clause_id'] for x in parts) == collections.Counter(x['clause_id'] for x in clauses)
        checks.append('all clauses exactly once ' + r + q)
        for part in parts:
            clause = next(x for x in clauses if x['clause_id'] == part['clause_id'])
            if 'actual_requested_clause' in part:
                assert part['actual_requested_clause'] == clause['actual_requested_clause']
                literal_clauses += 1
            else:
                omitted_clause_echoes += 1
            fs = part['fact_assessments']
            assert collections.Counter(f['fact_index'] for f in fs) == collections.Counter(range(1, len(clause['required_facts']) + 1))
            checks.append('all fact indices once ' + r + q)
            for fact in fs:
                facts += 1
                expected = clause['required_facts'][fact['fact_index'] - 1]
                if fact['expected'] != expected:
                    paraphrases.append({'reader': r, 'id': q, 'clause_id': clause['clause_id'], 'fact_index': fact['fact_index'], 'expected': fact['expected'], 'map': expected})
        if row.get('contextual_extra_observations'):
            extras.append({'reader': r, 'id': q})
assert facts == 1012
assert sum(len(x['grades']) for x in results['readers'].values()) == 346
out = {
    'all_structure_and_identity_checks_passed': True,
    'checks': len(checks), 'check_labels': checks,
    'full_grade_entries': 346, 'mapped_fact_assessments': facts,
    'expected_strings_exact_map_matches': facts - len(paraphrases),
    'expected_paraphrases_requiring_semantic_review': paraphrases,
    'literal_clause_echoes_verified': literal_clauses,
    'clause_echo_not_present_but_clause_identity_and_all_fact_indices_verified': omitted_clause_echoes,
    'nonempty_extra_observation_pairs': extras,
    'original_results_sha256': H(D / 'results.json'),
    'all_actual_source_slices_verified': load(D / 'grader-actual-delivery-validation.json')['all_actual_source_slices_verified'],
    'declared_five_input_delivery_pass': load(D / 'grader-delivery-validation.json')['all_passed'],
    'score_adopted': False,
    'limitations': 'Structure, exact input preservation and actual delivery do not establish interpretation or cognition. Fresh complete-set neutral and parent semantic review pending. A repeated literal clause field is not required by the grader schema; where present it is checked exactly. No original grade modified.'
}
p = D / 'primary-grading-structural-validation.json'
assert not p.exists()
p.write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({k: v for k, v in out.items() if k not in ['check_labels', 'expected_paraphrases_requiring_semantic_review']}))
print('expected paraphrase count', len(paraphrases))
