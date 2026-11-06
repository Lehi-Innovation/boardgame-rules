from pathlib import Path
import collections, hashlib, json, sys

R = Path(__file__).resolve().parent

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def combine(iteration, benchmark):
    d = R / iteration
    assert not (d / 'results.json').exists(), 'Preserve sealed results; version any later adjudication explicitly.'
    questions = read(d / 'questions.json')['questions']
    key = read(R / benchmark / 'answer-key.json')['answers']
    expected_ids = [q['id'] for q in questions]
    key_by_id = {a['id']: a for a in key}
    assert len(expected_ids) == len(set(expected_ids)) == len(key)
    result = {
        'benchmark_version': benchmark,
        'question_count': len(questions),
        'summary_sha256': sha(d / 'summary-snapshot.md'),
        'standard': 'Every actual requested part; factual-key matches and strict requested-part completion reported separately. Q18 unasked miss-execution timing is not a penalty. No question/key/raw edits.',
        'source_unresolved_requested_question_ids': ['Q51'],
        'core_playability_limitations_separate_from_question_grades': '../source-gaps-v2.json',
        'complete_core_pass': False,
        'readers': {},
    }
    for label in ['a', 'b']:
        raw = read(d / f'reader-{label}.json')['answers']
        report = read(d / f'grading-review-{label}.json')
        grades = report['reviews']
        assert collections.Counter(x['id'] for x in raw) == collections.Counter(expected_ids)
        assert collections.Counter(x['id'] for x in grades) == collections.Counter(expected_ids)
        raw_by_id = {x['id']: x for x in raw}
        for grade in grades:
            qid = grade['id']
            assert grade['observed_answer'] == raw_by_id[qid]['answer'], (label, qid, 'raw mismatch')
            assert grade['expected_answer'] == key_by_id[qid]['expected_answer'], (label, qid, 'key mismatch')
            assert grade['grade'] in ['correct', 'partial', 'incorrect']
            assert grade['strict_completion_grade'] in ['correct', 'partial', 'incorrect']
            if qid != 'Q51':
                assert grade['grade'] == grade['strict_completion_grade'], (label, qid, 'unasked overlay')
            elif grade['grade'] == 'correct':
                assert grade['strict_completion_grade'] == 'partial'
        factual = {k: sum(g['grade'] == k for g in grades) for k in ['correct', 'partial', 'incorrect']}
        strict = {k: sum(g['strict_completion_grade'] == k for g in grades) for k in ['correct', 'partial', 'incorrect']}
        for field, actual in [('factual_totals', factual), ('strict_completion_totals', strict)]:
            assert all(report[field][k] == actual[k] for k in actual), (label, field)
        result['readers'][label] = {
            'counts': factual,
            'strict_completion_counts': strict,
            'unsupported_guess_count': sum(bool(g.get('unsupported_guess')) for g in grades),
            'factual_non_correct_ids': [g['id'] for g in grades if g['grade'] != 'correct'],
            'strict_non_correct_ids': [g['id'] for g in grades if g['strict_completion_grade'] != 'correct'],
            'grades': grades,
            'independent_review_path': str((d / f'grading-review-{label}.json').resolve()),
        }
    manifest = read(d / 'input-manifest.json')
    checks = {path: Path(path).is_file() and sha(Path(path)) == digest for path, digest in manifest['hashes'].items()}
    assert all(checks.values()), checks
    (d / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    (d / 'grading-integrity.json').write_text(json.dumps({
        'all_ids_once': True,
        'raw_and_fixed_key_correspondence': True,
        'frozen_input_hashes': checks,
        'requested_parts_overlay': 'Q51 only; coordinator clarification retained separately',
        'summary_matches_canonical_now': sha(d / 'summary-snapshot.md') == sha(Path('/home/jonny/projects/boardgame-rules/rules/nemesis.md')),
        'historical_iteration_may_be_superseded': True,
        'complete_core_pass': False,
    }, indent=2) + '\n')
    print(iteration, {label: {k: v for k, v in info.items() if k in ['counts', 'strict_completion_counts']} for label, info in result['readers'].items()})

if __name__ == '__main__':
    combine(*sys.argv[1:])
