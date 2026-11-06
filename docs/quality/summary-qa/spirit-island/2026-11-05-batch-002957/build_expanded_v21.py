from pathlib import Path
from collections import Counter
import copy
import hashlib
import json

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
OLD, NEW = B / 'expanded-v20', B / 'expanded-v21'
H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
T = lambda s: hashlib.sha256(s.encode()).hexdigest()
L = lambda p: json.loads(Path(p).read_text())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


r = L(B / 'working-novelty-adjudication-15.json')
proof = L(B / 'novelty15-delivery-validation.json')
assert proof['status'] == 'VALID_FOR_RECORDED_EVIDENCE' and proof['check_count'] == 438
assert not proof['exceptions'] and all(x['ok'] for x in proof['checks'])
assert all(H(B / name) == digest for name, digest in proof['immutable_expected_sha256'].items())
assert r['decision_counts'] == {'ACCEPT': 1, 'REFINE': 0, 'REJECT': 0}
a = r['decisions'][0]
assert a['gap_id'] == 'W41-G01' and a['minimum_required_fact_count'] == 1
assert not NEW.exists()
candidate = B / 'source-candidate-20.md'
assert H(candidate) == H(ROOT / 'rules/spirit-island.md') == '63da3a8f472025ad10028eba03c11ec1ad00b2455cb3e70a08bafa6ae90bdb24'
q, k, f, sc = [L(OLD / n) for n in ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']]
before = [copy.deepcopy(x) for x in [q, k, f, sc]]
refs = []
for source in a['primary_sources']:
    path = Path(source['path'])
    lo, hi = source['character_range']
    text = path.read_text()[lo:hi]
    assert H(path) == source['original_byte_sha256']
    assert text == source['complete_operative_passage'] and T(text) == source['passage_utf8_sha256']
    refs.append({'file': str(path), 'file_sha256': H(path), 'label': source['locator'],
                 'character_range': [lo, hi], 'passage_sha256': T(text)})
labels = [x['file'] + ' | ' + x['label'] + ' | SHA256 ' + x['file_sha256'] for x in refs]
new = {
    'id': 'Q172', 'question': a['literal_surviving_pretest_question'],
    'answer': a['predetermined_answer'], 'source_refs': labels, 'exact_source_refs': refs,
    'new_coverage': a['source_defined_distinct_procedure'],
    'why_not_previously_requested': a['closest_existing_actual_ask_comparisons'][0]['actual_ask_difference'],
    'base_reachability': {'status': 'ACTUAL_CORE_PROCEDURE', 'reason': a['scope_assessment']},
    'current_base_novelty_credit': True, 'proposal_id': 'W41-G01',
    'adjudication_decision': 'ACCEPT',
    'origin': 'Complete working41/42 retained set, independently source-adjudicated15 before expanded readers',
}
q['questions'].append({'id': 'Q172', 'question': new['question']})
k['answers'].append({'id': 'Q172', 'answer': new['answer'], 'source_refs': labels})
mapping = copy.deepcopy(a['minimal_asked_only_map'])
mapping.update(id='Q172', question=new['question'])
for number, clause in enumerate(mapping['requested_clauses'], 1):
    clause['clause_id'] = 'Q172.' + str(number)
f['questions'].append(mapping)
sc['questions'].append({'id': 'Q172', 'scope_result': 'base_supported',
    'base_reachability': new['base_reachability'], 'primary_sources': refs,
    'current_base_novelty_credit': True,
    'scope_boundary': 'Explicit ordinary CORE actor permission only; not blanket etiquette, a compulsory timed variant, a duration or an invented expiry consequence.'})
assert q['questions'][:171] == before[0]['questions']
assert k['answers'][:171] == before[1]['answers']
assert f['questions'][:171] == before[2]['questions']
assert sc['questions'][:171] == before[3]['questions']
q['benchmark_version'] = k['benchmark_version'] = 'expanded-v21'
f.update(benchmark='expanded-v21', question_count=172,
    required_fact_count=sum(len(c['required_facts']) for x in f['questions'] for c in x['requested_clauses']))
assert f['required_fact_count'] == 507
sc.update(benchmark='expanded-v21', question_count=172)
counter = Counter(x['scope_result'] for x in sc['questions'])
assert counter == {'base_supported': 155, 'mixed_supported_and_noncredited': 14, 'noncredited_pending_base_proof': 3}
overlay = sc['working_scope_credit_overlay']
overlay['working_question_counts_for172'] = {'base_supported': 155, 'mixed_supported_and_noncredited': 14, 'noncredited_only': 3}
counts = copy.deepcopy(overlay['working_audited_clause_counts_after_explicit_element_grant'])
counts['base_supported'] += 1
assert counts == {'base_supported': 485, 'unverified_base_reachability': 26, 'generalized_engine_regression': 1}
overlay['working_audited_clause_counts_after_time_limit_permission'] = counts
sc['scope_revision_v21'] = {'explicit_core_actor_permission_added': 'Q172',
    'all171_prior_scope_entries_exact': True, 'no_invented_timer_expiry_rule': True,
    'audited_clause_total': 512, 'required_grading_fact_total': 507,
    'five_scope_premises_are_not_extra_grading_requirements': True,
    'earlier_scope_revision_v20_counts_remain_labeled_historical_version_counts': True}
NEW.mkdir()
for name, value in [('questions.json', q), ('answer-key.json', k), ('core-scope-credit.json', sc), ('novelty.json', [new])]:
    write(NEW / name, value)
f['creator_provenance'] = {'role': 'Root pre-test consolidation of complete source-adjudicated15 survivor set',
    'prior_map': str(OLD / 'asked-fact-map.json'), 'prior_map_sha256': H(OLD / 'asked-fact-map.json'),
    'all171_prior_entries_exact': True, 'summary_seen': True, 'historical_seed_answers_known': True,
    'no_expanded_reader_outputs_exist': True, 'required_NEW_fresh_whole_corpus_scope_validation': True}
f['input_hashes'] = {str(p): H(p) for p in [NEW / 'questions.json', NEW / 'answer-key.json',
    OLD / 'asked-fact-map.json', B / 'working-novelty-adjudication-15.json']}
write(NEW / 'asked-fact-map.json', f)
write(NEW / 'input-manifest.json', {
    'question_count': 172, 'required_fact_count': 507, 'prior_version': 'expanded-v20',
    'all_prior171_questions_keys_map_and_scope_entries_exact': True,
    'complete_surviving_set': ['W41-G01'], 'new_questions': 1, 'new_required_facts': 1,
    'existing_Q55_default_decision_facts_unchanged': True,
    'original20_prompts_preserved': q['questions'][:20] == L(B / 'seed-v1/questions.json')['questions'],
    'all_versioned_Q18_Q157_Q71_Q84_Q36_and_transcription_corrections_retained': True,
    'expanded_readers_dispatched_before_freeze': False,
    'canonical_candidate': 'source-candidate-20.md', 'canonical_sha256': H(candidate),
    'new_pure_source_audit09_required_on_C20': True,
    'sha256': {str(p): H(p) for p in [NEW / n for n in ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']]
        + [OLD / n for n in ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']]
        + [B / 'working-novelty-adjudication-15.json', B / 'working-novelty-adjudication-15-read-ledger.json',
           B / 'novelty15-delivery-validation.json', candidate, B / 'supplemental-source-manifest-v4.json']},
})
(NEW / 'question-bank.md').write_text('# Spirit Island expanded bank v21\n\n'
    '172 retained questions and507 required-fact entries. All171 prior question, key, asked-map and scope entries remain exact. '
    'One published ordinary-phase actor permission is appended from the complete working41/42 set after independent source/scope adjudication15. '
    'It adds no timer-expiry penalty, compulsory clock, duration, or extra Q55 grading fact. New actual zero passes, a NEW fresh whole-corpus challenge and a new pure-source C20 audit remain required.\n\n'
    + '\n\n'.join(f"## {x['id']}\n\n{x['question']}\n\n**Expected:** {y['answer']}\n\n**Sources:** {'; '.join(y['source_refs'])}" for x, y in zip(q['questions'], k['answers'])) + '\n')
assert H(ROOT / 'rules/spirit-island.md') == H(candidate)
write(B / 'build-status-v21.json', {'bank_files_complete': True, 'questions': 172, 'required_facts': 507,
    'all171_prior_q_key_map_scope_entries_exact': True, 'complete1_survivor_consolidated': True,
    'canonical_candidate': 'source-candidate-20.md', 'canonical_sha256': H(candidate),
    'sourceaudit08_historical_C19_only': True, 'new_sourceaudit09_REQUIRED': True,
    'actual_working43_44_and_NEWfresh12_required': True, 'expanded_readers_dispatched': False})
print(json.dumps({'bank': 'expanded-v21', 'questions': 172, 'facts': 507,
    'all171_prior_q_key_map_scope_entries_exact': True, 'canonical_C20': H(candidate), 'new_sourceaudit09_required': True}))
