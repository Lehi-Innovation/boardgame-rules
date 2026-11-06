from pathlib import Path
import json
import datetime

D = Path(__file__).resolve().parent
load = lambda p: json.loads(p.read_text())
questions = load(D / 'questions.json')['questions']
key = load(D / 'answer-key.json')['answers']
ids = [q['id'] for q in questions]
out = {
    'compiled_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'benchmark_version': 'expanded-v9',
    'protocol_version': 'generic-small-batch-v5',
    'grading_method': 'Two new independent Sol/high/fork-none graders assessed only each final all63 reader output. All staged drafts retained; no semantic evaluator feedback between reader stages. Original grader reports remain unchanged.',
    'readers': {},
}
for side in ['a', 'b']:
    reader = load(D / f'reader-{side}.json')['answers']
    raw = {r['id']: r for r in reader}
    report = load(D / f'grader-{side}.json')
    grades = report['grades']
    by_id = {g['id']: g for g in grades}
    assert len(grades) == len(by_id) == len(reader) == len(raw) == 63
    assert set(by_id) == set(raw) == set(ids)
    for question, expected in zip(questions, key):
        grade = by_id[question['id']]
        actual = raw[question['id']]
        assert grade.get('question', grade.get('literal_question')) == question['question'], (side, question['id'], 'question')
        assert grade['expected_answer'] == expected['expected_answer'], (side, question['id'], 'key')
        assert grade['source_references'] == expected['source_references'], (side, question['id'], 'references')
        assert grade['observed_answer'] == actual['answer'], (side, question['id'], 'answer')
        assert grade['reader_evidence'] == actual['evidence'], (side, question['id'], 'evidence')
        assert grade['reader_support'] == actual['support'], (side, question['id'], 'support')
        assert grade['grade'] in ['correct', 'partial', 'incorrect']
        assert isinstance(grade['unsupported_guess'], bool)
        assert grade['requested_parts'] and grade['reason']
    counts = {kind: sum(g['grade'] == kind for g in grades) for kind in ['correct', 'partial', 'incorrect']}
    assert counts == report['totals']
    out['readers'][side] = {'totals': counts, 'grades': grades, 'independent_grader_report': str(D / f'grader-{side}.json')}
destination = D / 'results.json'
assert not destination.exists(), destination
destination.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({s: v['totals'] for s, v in out['readers'].items()}, indent=2))
