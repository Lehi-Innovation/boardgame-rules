from pathlib import Path
import copy
import hashlib
import json

B = Path(__file__).resolve().parent
H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
L = lambda p: json.loads(Path(p).read_text())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


bank = B / 'expanded-v21'
m = L(bank / 'input-manifest.json')
assert all(H(p) == h for p, h in m['sha256'].items())
p = B / 'coverage-ledger.json'
backup = B / 'coverage-ledger-before-novelty15-resolution.json'
assert not backup.exists()
j = L(p)
assert j['benchmark'] == 'expanded-v20'
a = L(bank / 'novelty.json')[0]
r = L(B / 'working-novelty-adjudication-15.json')
j.update(benchmark='expanded-v21', question_count=172)
j['acceptance_ledger'].append({**a, 'bank': 'expanded-v21',
    'decision': 'ACCEPT: complete working41/42 retained set independently source/scope-adjudicated15'})
j['precise_clause_mappings'].append({'topic': a['new_coverage'], 'source_refs': a['exact_source_refs'],
    'question_ids': ['Q172'], 'tested_clause': a['question'], 'base_reachability': a['base_reachability']})
j['faq_rulings'].append({'ruling_id': 'working41-Q172', 'rule': a['answer'],
    'source_refs': a['exact_source_refs'], 'question_ids': ['Q172'],
    'scope': 'Actual ordinary CORE p8 actor permission; not blanket etiquette or an invented timed-game consequence',
    'current_base_novelty_credit': True})
for row in j['passes']:
    if row['pass'] == 41:
        row.update(new_questions_added=1, accepted_ids=['Q172'], adjudication='working-novelty-adjudication-15.json',
            final_disposition='ACCEPT one minimal actor-permission fact, consolidated expanded-v21',
            count_semantics='Original retained count1 preserved; now one independent accepted question is actually appended. No zero-pass claim.')
j['scope_boundary_adjudication15'] = {
    'report': 'working-novelty-adjudication-15.json', 'sha256': H(B / 'working-novelty-adjudication-15.json'),
    'decision': 'ACCEPT explicit operative any-player actor permission only',
    'reason': r['scope_assessment'], 'new_question': 'Q172', 'new_required_facts': 1,
    'no_new_Q55_requirement_or_timer_expiry_rule': True,
    'prior_review_and_pass_opinions_preserved_as_history': True,
}
j['stopping_rule_history'].append(copy.deepcopy(j['stopping_rule']))
j['stopping_rule'] = {'consecutive_zero_addition_passes': [],
    'all_in_scope_procedural_passages_mapped': False,
    'independent_challenge': 'pending actual working43/44 then NEW fresh whole-corpus12',
    'claim': 'Accepted working41 survivor Q172 appended; restart actual zero streak on172. Historical42zero was on prior171 bank. No forced zero, global PASS or universal-exhaustiveness claim.'}
j['pretest_asked_fact_mapping'].update(path='expanded-v21/asked-fact-map.json',
    sha256=H(bank / 'asked-fact-map.json'), question_count=172, required_fact_count=507,
    scope_review='pending actual working43/44 then NEW fresh whole-corpus12')
j['scope_reachability_policy']['retained_regression_credit'] = 'expanded-v21/core-scope-credit.json'
j['input_hashes'] = {str(path): H(path) for path in [bank / n for n in
    ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']]
    + [B / 'supplemental-source-manifest-v4.json']}
backup.write_bytes(p.read_bytes())
write(p, j)
Q = L(bank / 'questions.json'); K = L(bank / 'answer-key.json')
F = L(bank / 'asked-fact-map.json'); C = L(bank / 'core-scope-credit.json')
packet = {
    'purpose': 'Complete current172 source-only working-pass delta; no summary/readers/grades/peer review verdicts',
    'benchmark': 'expanded-v21', 'question_count': 172, 'required_fact_count': 507,
    'complete_new_question_objects': Q['questions'][171:],
    'complete_new_key_objects': K['answers'][171:],
    'complete_new_asked_map_objects': F['questions'][171:],
    'complete_new_scope_entry': C['questions'][171],
    'full_bank_sha256': {n: H(bank / n) for n in ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']},
    'prior171_equivalence': {'all_question_key_map_scope_objects_exact': True,
        'own_previous_complete_version': 'expanded-v20 reconstructed and actual asks freshly delivered in working41/42',
        'prior_hashes': {n: H(B / 'expanded-v20' / n) for n in ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']}},
    'new_primary_source_refs': a['exact_source_refs'],
    'scope_boundary': 'The actual CORE p8 sentence assigns a permitted Spirit Phase action to any player. Keep this specific operative actor permission distinct from surrounding flavour/etiquette and the unspecified-decision fallback. Do not invent a duration, compulsory clock, expiry consequence or permission to override unfinished phase procedures. This does not make all table advice a new gameplay rule.',
    'unchanged_scope_controls': 'All earlier conditional/generalized regressions remain fully graded, with their unchanged separate zero novelty credit where original-base reachability remains unverified. Current metadata is not a coverage authority.',
    'all_primary_authority_versions_unchanged': True,
    'no_source_verdict_or_forced_zero': True,
    'no_expanded_reader_outputs_exist': True,
}
write(B / 'working-pass-v21-supplement.json', packet)
print(json.dumps({'bank': 'expanded-v21', 'questions': 172, 'facts': 507,
    'all171_prior_objects_exact': True, 'zero_streak_reset': True,
    'working_packet_characters': len((B / 'working-pass-v21-supplement.json').read_text())}))
