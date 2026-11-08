"""Make an already-asked exchange-state consequence explicit before testing."""
from pathlib import Path
import copy
import hashlib
import json

R = Path(__file__).parent.resolve()
OLD, OUT = R / 'expanded-candidate-13', R / 'expanded-candidate-14'
assert not OUT.exists()


def read(path):
    return json.loads(path.read_text())


def objsha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


q, k = read(OLD / 'questions.json'), read(OLD / 'answer-key.json')
before = copy.deepcopy(next(a for a in k['answers'] if a['id'] == 'Q144'))
after = next(a for a in k['answers'] if a['id'] == 'Q144')
after['required_facts'][2] = (
    'Only after both selections may Sorcerer switch encounter cards, before '
    "revealing Oracle's originally selected card. If switched, Sorcerer's originally "
    'faceup card is now faceup in front of Oracle; Oracle\'s originally facedown '
    'card is now facedown in front of Sorcerer until the normal reveal. The '
    'physical exchange supplies no additional flip step.'
)
after['source_references'].append(
    'Original2008 rulebook p14 Alien Interactions, extraction1118–1136, '
    'plus original printed Oracle/Sorcerer sheets and ordinary Reveal phase. '
    'Post-exchange locations/orientations are the direct application of '
    'the stated physical exchange, not a separate quoted card effect.'
)
q['benchmark_version'] = k['benchmark_version'] = OUT.name
assert q['questions'] == read(OLD / 'questions.json')['questions']
assert q['questions'][:20] == read(R / 'seed-v1/questions.json')['questions']
assert k['answers'][:20] == read(R / 'seed-v1/answer-key.json')['answers']
assert sum(len(a['required_facts']) for a in k['answers']) == 536
OUT.mkdir()


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


save('questions.json', q)
save('answer-key.json', k)
for name in ['acceptance-rejection-ledger.json', 'versioned-corrections.json',
             'candidate-question-map.json', 'withdrawn-question-ledger.json',
             'targeted-coverage-passes.json', 'targeted-coverage-passes-after-review.json',
             'coverage-map.json']:
    save(name, read(OLD / name))
save('key-precision-correction.json', {
    'prior_bank_version': OLD.name,
    'bank_version': OUT.name,
    'reason': 'Literal Q144 already asks orientations at every step. Make the '
              'post-exchange consequence explicit before any expanded reader, '
              'preserving all original timing and orientation requirements.',
    'old_complete_key_entry': before,
    'new_complete_key_entry': after,
    'all_165_literal_questions_identical': True,
    'raw_fact_record_count_unchanged': 536,
    'new_coverage_rule_group_credit': 0,
    'primary_evidence_adjudication': str(R / 'source-review/oracle-sorcerer-orientation-source-adjudication-02.json'),
    'interpretation_limit': 'Straightforward physical exchange application; no '
                            'invented flip step, timing window or full flare text.',
    'human_choices_adopted': False,
})
save('scope-delta-from13.json', {
    'prior_bank_version': OLD.name,
    'bank_version': OUT.name,
    'question_count': 165,
    'raw_key_fact_count': 536,
    'all_literal_questions_identical': True,
    'changed_complete_entries': [{'id': 'Q144', 'question': next(x for x in q['questions'] if x['id'] == 'Q144'), 'key': after}],
    'unchanged_entry_bindings': [
        {'id': qe['id'], 'question_sha256': objsha(qe), 'key_sha256': objsha(ke)}
        for qe, ke in zip(q['questions'], k['answers']) if qe['id'] != 'Q144'
    ],
})
(OUT / 'question-bank.md').write_text(
    '# Expanded candidate14 — explicit exchange-state key precision\n\n' +
    '\n\n'.join('## ' + qe['id'] + '\n\n' + qe['question'] + '\n\n' +
                  '\n'.join('- ' + f for f in ke['required_facts'])
                  for qe, ke in zip(q['questions'], k['answers'])) + '\n'
)
save('input-manifest.json', {
    'review_candidate_only': True, 'question_count': 165, 'raw_key_fact_count': 536,
    'all_literal_questions_identical_to13': True,
    'original_twenty_preserved_verbatim': True,
    'sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file()},
})
print('candidate14: same165questions/536records; Q144 exchange consequence explicit; no new rule-group credit')
