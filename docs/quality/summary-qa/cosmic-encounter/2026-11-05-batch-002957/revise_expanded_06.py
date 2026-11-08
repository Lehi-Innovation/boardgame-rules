"""Version independent source/key corrections; never replace earlier candidates."""
from pathlib import Path
import copy
import hashlib
import json

R = Path(__file__).parent
OLD = R / 'expanded-candidate-05'
OUT = R / 'expanded-candidate-06'
assert not OUT.exists(), 'Historical candidates are immutable'
OUT.mkdir()

def read(path):
    return json.loads(path.read_text())

def write(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

q = read(OLD / 'questions.json')
k = read(OLD / 'answer-key.json')
q['benchmark_version'] = k['benchmark_version'] = OUT.name
questions = {x['id']: x for x in q['questions']}
answers = {x['id']: x for x in k['answers']}
ledger = read(OLD / 'acceptance-rejection-ledger.json')
changes = []

def record(ident, finding, action):
    changes.append({'question_id': ident, 'independent_finding': finding,
                    'action': action, 'before_question': copy.deepcopy(questions.get(ident)),
                    'before_key': copy.deepcopy(answers.get(ident))})

record('Q026', 'CKS-07', 'Make the already-asked use/non-use distinction explicit.')
answers['Q026']['required_facts'].append('Placing a citadel does not require power use; activating the citadels does.')
record('Q073', 'CKS-06', 'Restore the omitted source qualification for sent ships.')
answers['Q073']['required_facts'][1] = 'Lost ships actually go to the warp involuntarily; sent ships go because of a specific action/effect, sometimes voluntarily, are not directly involved in the encounter, and count as lost.'
record('Q078', 'CKS-02/P01', 'Explicitly ask the previously untested reclamation ship cap and sources.')
questions['Q078']['question'] += ' How many ships may be placed on that empty home planet, and from which holdings may they come?'
answers['Q078']['required_facts'] += ['May place up to four ships.', 'Ships come from the player\'s other existing colonies; this rule does not permit direct retrieval from the warp.']
answers['Q078']['source_references'] += ['Original rulebook p7 extraction lines549–553; p12 lines974–979']
record('Q086', 'CKS-08', 'Withdraw unproved reachable current-core scenario, preserving its original ID and artifacts.')
withdrawn = {'id': 'Q086', 'question': questions.pop('Q086'), 'key': answers.pop('Q086'),
             'reason': 'The literal FAQ conditional remains authoritative context, but the present scenario does not establish a positively sourced reachable original-base state before ordinary victory. No excluded enabling mechanism is assumed.',
             'independent_adjudication': 'source-review/coverage-key-scope-review-01.json CKS-08',
             'id_reused': False, 'tested_coverage_credit': False}
record('Q098', 'CKS-05', 'Separate Wild access from permission to replay an already-played flare.')
questions['Q098']['question'] = 'A player has already played its Super flare, and the power use enabled by it is Cosmic Zapped. Must the flare be discarded or its Wild used immediately? While the power is zapped, which effect would apply to a legal flare play, and does the zap permit that already-played flare to be played a second time in the same encounter?'
answers['Q098']['required_facts'] = ['Neither discard nor immediate Wild play is required; the flare remains in hand.', 'While the power is zapped only Wild is available for an otherwise legal play.', 'Canceling the enabled power does not cancel or undo the already-played flare; ordinary per-player and per-flare once-per-encounter limits still prevent a second play absent an explicit exception.']
answers['Q098']['source_references'] += ['Original rulebook p13 Flare Cards; 2018 FAQ p6 extraction lines525–537']
record('Q123', 'CKS-03/P02', 'Explicitly ask Reserve Wild eligibility and card destination, beyond duration.')
questions['Q123']['question'] += ' While Reserve Wild remains active, whose discarded cards of what type may its user take, and where do those cards go?'
answers['Q123']['required_facts'] += ['Whenever another player discards a reinforcement card during the remaining encounter, Reserve Wild\'s user may take it.', 'Add the taken reinforcement to the user\'s own hand; this does not grant retrieval of the user\'s own reinforcement discards.']
questions['Q156'] = {'id': 'Q156', 'question': 'When Mobius Tubes releases a player\'s ships and those ships are placed on that player\'s existing colonies, do the ships land simultaneously or one ship at a time?'}
answers['Q156'] = {'id': 'Q156', 'required_facts': ['The ships land on colonies simultaneously.'], 'contextual_background': ['No Saboteur trap, token or revelation commitment rule is imported.'], 'source_references': ['2018 FAQ p19 extraction lines1796–1797: general simultaneous-landing statement explicitly illustrated by base Mobius Tubes.']}
changes.append({'question_id': 'Q156', 'independent_finding': 'CKS-04/P03', 'action': 'Add distinct original-base arrival timing rule.', 'before_question': None, 'before_key': None})
q['questions'] = list(questions.values())
k['answers'] = list(answers.values())
for c in changes:
    ident = c['question_id']
    c['after_question'] = questions.get(ident)
    c['after_key'] = answers.get(ident)
    ledger.append({'candidate': c['independent_finding'], 'question_id': ident, 'decision': c['action'], 'source_review': 'source-review/coverage-key-scope-review-01.json'})
seedq, seedk = read(R/'seed-v1/questions.json'), read(R/'seed-v1/answer-key.json')
assert q['questions'][:20] == seedq['questions']
assert k['answers'][:20] == seedk['answers']
assert len(questions) == len(answers) == 155
assert set(questions) == set(answers)
write('questions.json', q)
write('answer-key.json', k)
write('acceptance-rejection-ledger.json', ledger)
write('versioned-corrections.json', {'parent_version': OLD.name, 'changes': changes, 'original_twenty_preserved_verbatim': True, 'prior_bank_blind_test_dispatched': False})
write('withdrawn-question-ledger.json', [withdrawn])
cm = read(OLD/'candidate-question-map.json')
cm['FAQC020'] = None
cm['CKS-P01'], cm['CKS-P02'], cm['CKS-P03'] = 'Q078', 'Q123', 'Q156'
write('candidate-question-map.json', cm)
scope = read(R/'source-review/coverage-key-scope-map-01.json')
scope.update(version='parent-proposed-scope-overlay-06', bank_version=OUT.name,
             status='Independent overlay inherited for unchanged questions; changed questions require renewed independent validation. No blind test or final freeze authorized.',
             question_count=155, candidate_fact_record_count=sum(len(a['required_facts']) for a in k['answers']))
scope['questions'] = [e for e in scope['questions'] if e['id'] in questions]
changed = {c['question_id'] for c in changes} - {'Q086'}
for e in scope['questions']:
    if e['id'] in changed:
        e['updated_literal_question'] = questions[e['id']]['question']
        e['updated_candidate_required_facts'] = answers[e['id']]['required_facts']
        e['scoring_ready'] = False
        e['renewed_validation_required'] = True
scope['new_question_awaiting_mapping'] = questions['Q156']
scope['equivalence_policy_pending_review'] = 'Q001 asks flare membership; all dealt flares including rejected aliens plus random extras to total ten is a complete equivalent to six-plus-four, without separately worked arithmetic.'
write('question-scope-map-candidate.json', scope)
coverage = read(OLD/'coverage-map.json')
coverage.update(bank_version=OUT.name, question_count=155, status='Versioned independent findings incorporated; renewed saturation check and independent validation pending.')
for row in coverage['applicable_2018_faq']:
    if row.get('source_id') == 'FAQ-Q038':
        row.update(question_ids=[], counted_tested_coverage=False, disposition='withdrawn-unproved-current-core-scenario', independent_finding='CKS-08')
coverage['applicable_2018_faq'].append({'source_id':'FAQ-SABOTEUR-GENERAL-LANDING', 'pdf_pages':[19], 'lines':[1796,1797], 'question_ids':['Q156'], 'counted_tested_coverage':True, 'disposition':'accepted-in-part-explicit-base-Mobius-example', 'excluded':'All trap/token/revelation mechanics'})
coverage['scope_challenges'] = []
coverage['documentary_conditionals'] = [{'question_id': i, 'reachable_core_branch_credit':False, 'basis':'Explicit original printed source conditional only; no enabling expansion/copying effect assumed.'} for i in ['Q054','Q143']]
coverage['asked_scope_overlay'] = 'question-scope-map-candidate.json; only actually asked content counts, never entire referenced paragraphs or key-only background.'
write('coverage-map.json', coverage)
passes = read(OLD/'review-inputs/targeted-coverage-passes.json')
passes['status'] = 'Counter reset after independent challenge; new zero-addition passes pending.'
passes['passes'].append({'pass':7,'focus':'Independent challenge CKS-02/03/04','new_question_ids':['Q156'],'extended_questions_with_distinct_new_rules':['Q078','Q123'],'withdrawn_unproved_scenarios':['Q086'],'qualifying_rule_additions':3,'stopping_counter_reset':True})
write('targeted-coverage-passes.json', passes)
(OUT/'question-bank.md').write_text('# Expanded candidate 06 — renewed review pending\n\n'+'\n\n'.join(f"## {x['id']}\n\n{x['question']}\n\n"+'\n'.join('- '+f for f in answers[x['id']]['required_facts']) for x in q['questions'])+'\n')
write('input-manifest.json', {'frozen_for_review_only':True,'question_count':155,'raw_key_fact_records':sum(len(a['required_facts']) for a in k['answers']),'original_twenty_preserved_verbatim':True,'sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir() if p.is_file()}})
print(OUT.name, len(questions), sum(len(a['required_facts']) for a in k['answers']))
