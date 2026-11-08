"""Consolidate the complete actual-clause source challenge before readers."""
from pathlib import Path
import copy
import hashlib
import json

R = Path(__file__).parent.resolve()
OLD, OUT = R / 'expanded-candidate-14', R / 'expanded-candidate-15'
assert not OUT.exists()


def read(path):
    return json.loads(path.read_text())


def objsha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


for name in ['current14-faq-operative-rechallenge-05.json',
             'ordinary-compensation-selection-novelty-03.json',
             'native-actual-clause-rechallenge-02.json']:
    assert (R / 'source-review' / name).exists()
q, k = read(OLD / 'questions.json'), read(OLD / 'answer-key.json')
old_q, old_k = copy.deepcopy(q), copy.deepcopy(k)
qby = {a['id']: a for a in q['questions']}
kby = {a['id']: a for a in k['answers']}

old_phrase = 'and what happens when another power copies this one and then loses?'
assert old_phrase in qby['Q054']['question']
qby['Q054']['question'] = qby['Q054']['question'].replace(
    old_phrase,
    'and under the original printed copying conditional, which powers may '
    'another alien copy and what happens when that copier loses?')

qby['Q120']['question'] += (
    ' Does the +8 replace the normal +4 or stack with it? After taking +8, '
    'must Human discard the flare to self-Zap, or may it decline that extra step?')
kby['Q120']['required_facts'] += [
    'The +8 replaces the normal +4; the two bonuses do not stack.',
    'After taking +8, Human may decline the additional discard/self-Zap. '
    'Taking the bonus alone does not compel that discard.',
]

qby['Q123']['question'] += (
    ' Is each eligible Reserve Wild pickup compulsory or separately optional; '
    'if the user declines one, may it still take a later eligible discard? '
    'If several otherwise-eligible flares are discarded at the same time while '
    'Vulch Super is active, may its power apply to all of them or only one from that group?')
kby['Q123']['required_facts'] += [
    'Reserve Wild pickup is optional for each eligible discard. Declining one '
    'does not end the encounter-long effect or prevent taking a later eligible discard.',
    'Vulch Super is not capped at one otherwise-eligible flare from a simultaneous '
    'discard group; its effect applies to all otherwise-eligible discarded flares.',
]

qby['Q148']['question'] += (
    ' For each later qualifying deck draw, is interception compulsory or may '
    'the user decide separately?')
kby['Q148']['required_facts'][1] = (
    'For the rest of this encounter, each time that same player must draw a card '
    'from the deck, the user may choose separately whether to draw it instead. '
    "This targets that player's eligible deck draws, not every player's draws "
    'or acquisitions from hands or discard piles.')
kby['Q148']['required_facts'][2] = (
    'For each card it chooses to intercept, the user draws, inspects and gives '
    'the card to that player.')

new = [
    ({'id': 'Q167', 'question':
      'Without a power changing ordinary compensation, how are its cards selected '
      "from the opponent's hand, may the recipient see their faces while selecting, "
      'and is seeing only their backs allowed?'},
     {'id': 'Q167', 'required_facts': [
         'Take compensation cards at random, without seeing their faces while choosing.',
         'The selecting player is allowed to see the card backs.',
     ], 'contextual_background': [
         'No particular shuffle, probability algorithm or expansion deck is supplied '
         'or demanded. The visibility restriction applies during selection.',
     ], 'source_references': [
         'Original2008 rulebook p11 Compensation, extraction887–895.',
         'Official2018 FAQ p5 extraction424–429, original-base random-selection '
         'definition. Repeated p8 extraction785–788 definition does not import a reward deck.',
     ]}),
    ({'id': 'Q168', 'question':
      'After drawing the player-color destiny card that selects the first player, '
      'what happens to that card before play begins, and in which direction do '
      'ordinary turns pass?'},
     {'id': 'Q168', 'required_facts': [
         'Shuffle that drawn player-color card back into the destiny deck before play begins.',
         'Ordinary turns pass to the left.',
     ], 'contextual_background': [], 'source_references': [
         'Original2008 rulebook p6 Setup step7, extraction477–482; '
         'p7 The Turn, extraction487–489.',
     ]}),
]
for qe, ke in new:
    assert qe['id'] not in qby and ke['id'] not in kby
    q['questions'].append(qe)
    k['answers'].append(ke)

q['benchmark_version'] = k['benchmark_version'] = OUT.name
assert len(q['questions']) == 167
assert sum(len(a['required_facts']) for a in k['answers']) == 544
assert q['questions'][:20] == read(R / 'seed-v1/questions.json')['questions']
assert k['answers'][:20] == read(R / 'seed-v1/answer-key.json')['answers']
assert [a['id'] for a in q['questions']] == [a['id'] for a in k['answers']]
OUT.mkdir()


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


save('questions.json', q)
save('answer-key.json', k)
for name in ['acceptance-rejection-ledger.json', 'versioned-corrections.json',
             'candidate-question-map.json', 'withdrawn-question-ledger.json',
             'targeted-coverage-passes.json', 'targeted-coverage-passes-after-review.json']:
    save(name, read(OLD / name))
changed = ['Q054', 'Q120', 'Q123', 'Q148']
save('source-field-expansion-and-precision-ledger.json', {
    'prior_bank_version': OLD.name, 'bank_version': OUT.name,
    'new_question_ids': ['Q167', 'Q168'], 'extended_existing_ids': changed,
    'old_complete_entries': [{'question': qe, 'key': ke}
                             for qe, ke in zip(old_q['questions'], old_k['answers'])
                             if qe['id'] in changed],
    'five_unique_new_reachable_rule_groups': [
        {'group': 'Active-effect per-event choice', 'ids': ['Q123', 'Q148'],
         'primary': '2018FAQ p19 ReserveWild1784–1789; retained2009MindWildL43–49'},
        {'group': 'Random-selection face visibility', 'ids': ['Q167'],
         'primary': '2018FAQ p5 424–429; originalbookp11 887–895'},
        {'group': 'HumanSuper replacement and optional post-bonus discard', 'ids': ['Q120'],
         'primary': '2018FAQ p15 1420–1424'},
        {'group': 'VulchSuper simultaneous eligible-card cardinality', 'ids': ['Q123'],
         'primary': '2018FAQ p21 2011–2017'},
        {'group': 'First-player destiny restoration and ordinary turn flow', 'ids': ['Q168'],
         'primary': 'Originalbookp6 477–482/p7 487–489'},
    ],
    'documentary_precision_without_reachable_group_credit': {
        'id': 'Q054', 'source': 'Original printed Reincarnator copying conditional',
        'limits': 'No original-base effect creating that copying state is assumed. '
                  'The printed conditional is described; no new reachable-branch credit.',
    },
    'source_review_paths': [str(R / 'source-review' / name) for name in [
        'current14-faq-operative-rechallenge-05.json',
        'ordinary-compensation-selection-novelty-03.json',
        'native-actual-clause-rechallenge-02.json']],
    'all_original_twenty_objects_preserved': True,
    'human_choices_adopted': False,
    'expanded_readers_seen_before_this_correction': False,
})

for prior_version, target, include_key in [
    ('expanded-candidate-14', 'scope-delta-from14.json', True),
    ('expanded-candidate-13', 'scope-and-source-delta-from13.json', True),
    ('expanded-candidate-14', 'question-delta-from14.json', False),
]:
    pq = {x['id']: x for x in read(R / prior_version / 'questions.json')['questions']}
    pk = {x['id']: x for x in read(R / prior_version / 'answer-key.json')['answers']}
    entries, unchanged = [], []
    for qe, ke in zip(q['questions'], k['answers']):
        same = qe['id'] in pq and qe == pq[qe['id']] and (
            not include_key or ke == pk[ke['id']])
        if same:
            unchanged.append({'id': qe['id'], 'question_sha256': objsha(qe),
                              **({'key_sha256': objsha(ke)} if include_key else {})})
        else:
            entries.append({'id': qe['id'], 'question': qe,
                            **({'key': ke} if include_key else {})})
    save(target, {'prior_bank_version': prior_version, 'bank_version': OUT.name,
                  'question_count': 167, 'raw_key_fact_count': 544,
                  'changed_complete_entries': entries,
                  'unchanged_entry_bindings': unchanged})

save('coverage-map.json', {
    'bank_version': OUT.name, 'question_count': 167,
    'status': 'Review candidate: exact current asked map/source closure pending.',
    'retained_prior_map_exact': read(OLD / 'coverage-map.json'),
    'prior_map_limit': 'Historical broad paragraph/key credit is not sufficient. '
                       'Current actual-asked scope and source-field corrections govern.',
    'current_source_field_overlay': str(OUT / 'source-field-expansion-and-precision-ledger.json'),
    'latest_actual_scope_pending': True,
    'no_composite_pass': True,
})
(OUT / 'question-bank.md').write_text(
    '# Expanded candidate15 — consolidated source-field additions\n\n' +
    '\n\n'.join('## ' + qe['id'] + '\n\n' + qe['question'] + '\n\n' +
                  '\n'.join('- ' + f for f in ke['required_facts'])
                  for qe, ke in zip(q['questions'], k['answers'])) + '\n')
save('input-manifest.json', {
    'review_candidate_only': True, 'question_count': 167, 'raw_key_fact_count': 544,
    'original_twenty_preserved_verbatim': True,
    'sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
               for p in OUT.iterdir() if p.is_file()},
})
print('candidate15:167questions/544rawrecords; five unique reachable groups, one documentary precision; no freezePASS')
