from pathlib import Path
from collections import Counter
import copy
import hashlib
import json

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
OLD, NEW = B / 'expanded-v21', B / 'expanded-v22'
H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
L = lambda p: json.loads(Path(p).read_text())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


adopt = L(B / 'map-adjudication16-adoption.json')
proof = L(B / 'map16-delivery-validation.json')
report = L(B / 'working-map-adjudication-16.json')
assert adopt['decisions'] == {'MAP12-01': 'ACCEPT', 'MAP12-02': 'ACCEPT'}
assert proof['status'] == 'VALID_FOR_RECORDED_EVIDENCE'
assert proof['check_count'] == 347 and not proof['exceptions']
assert all(x['ok'] for x in proof['checks'])
assert all(H(p) == h for p, h in proof['frozen_outputs'].items())
assert H(adopt['report']['path']) == adopt['report']['sha256']
assert H(adopt['delivery_validation']['path']) == adopt['delivery_validation']['sha256']
assert H(adopt['actual_runtime']['path']) == adopt['actual_runtime']['sha256']
assert adopt['question_count'] == 172 and adopt['mapped_fact_entry_count'] == 507
assert adopt['new_procedure_questions'] == adopt['scope_changes'] == 0
assert not NEW.exists()
assert H(ROOT / 'rules/spirit-island.md') == H(B / 'source-candidate-20.md') == '63da3a8f472025ad10028eba03c11ec1ad00b2455cb3e70a08bafa6ae90bdb24'
assert not list(B.glob('expanded-iteration-*/reader-?.json'))

q, k, f, sc = [L(OLD / n) for n in ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']]
originals = [copy.deepcopy(x) for x in [q, k, f, sc]]
byid = {x['id']: x for x in f['questions']}
for decision in report['decisions']:
    ident = decision['question_id']
    assert decision['verdict'] == 'ACCEPT'
    assert byid[ident] == decision['complete_old_map_entry']
    new = adopt['approved_new_map_entries'][ident]
    assert new == decision['complete_proposed_new_map_entry']
    index = 3 if ident == 'Q09' else 0
    restored = copy.deepcopy(new)
    restored['requested_clauses'][0]['required_facts'][index] = byid[ident]['requested_clauses'][0]['required_facts'][index]
    restored['key_context_not_required'].pop()
    assert restored == byid[ident]
    f['questions'][next(i for i, x in enumerate(f['questions']) if x['id'] == ident)] = copy.deepcopy(new)

assert q['questions'] == originals[0]['questions'] and k['answers'] == originals[1]['answers']
assert sc['questions'] == originals[3]['questions']
assert [x['id'] for x in f['questions']] == [x['id'] for x in q['questions']]
assert len(q['questions']) == 172
assert sum(len(c['required_facts']) for x in f['questions'] for c in x['requested_clauses']) == 507
changed = [a['id'] for a, z in zip(originals[2]['questions'], f['questions']) if a != z]
assert changed == ['Q09', 'Q65']
assert Counter(x['scope_result'] for x in sc['questions']) == {'base_supported': 155, 'mixed_supported_and_noncredited': 14, 'noncredited_pending_base_proof': 3}
q['benchmark_version'] = k['benchmark_version'] = 'expanded-v22'
f.update(benchmark='expanded-v22', question_count=172, required_fact_count=507)
sc['benchmark'] = 'expanded-v22'
sc['scope_revision_v22'] = {'map_precision_only': ['Q09', 'Q65'], 'all172_scope_entries_exact': True, 'scope_credit_counts_unchanged': True, 'no_new_base_novelty': True}
NEW.mkdir()
for name, value in [('questions.json', q), ('answer-key.json', k), ('core-scope-credit.json', sc), ('novelty.json', [])]:
    write(NEW / name, value)
f['creator_provenance'] = {'role': 'Pre-test consolidation of both independently accepted map16 context corrections', 'prior_map': str(OLD / 'asked-fact-map.json'), 'prior_map_sha256': H(OLD / 'asked-fact-map.json'), 'all172_questions_and_keys_exact': True, 'all170_unaffected_map_entries_exact': True, 'two_existing_required_fact_strings_refined_without_index_deletion': True, 'summary_seen': True, 'historical_seed_answers_known': True, 'no_expanded_reader_outputs_exist': True, 'independent_full_current_map_confirmation_pending': True}
f['input_hashes'] = {str(p): H(p) for p in [NEW / 'questions.json', NEW / 'answer-key.json', OLD / 'asked-fact-map.json', B / 'working-map-adjudication-16.json', B / 'map-adjudication16-adoption.json']}
write(NEW / 'asked-fact-map.json', f)
write(NEW / 'map-corrections.json', {'prior_version': 'expanded-v21', 'new_version': 'expanded-v22', 'reason': 'Genuine pre-test asked-fact over-demand corrections independently accepted16; no reader outputs exist.', 'complete_accepted_set': report['decisions'], 'all172_question_and_key_objects_exact': True, 'all172_scope_objects_exact': True, 'all170_other_map_entries_exact': True, 'required_fact_entries_before_and_after': [507, 507], 'new_questions': 0, 'new_required_fact_entries': 0, 'body_unchanged': True, 'independent_full_current_map_confirmation_pending': True})
write(NEW / 'input-manifest.json', {'question_count': 172, 'required_fact_count': 507, 'prior_version': 'expanded-v21', 'map_only_correction_ids': changed, 'all172_question_key_and_scope_entries_exact': True, 'all170_unaffected_map_entries_exact': True, 'whole_required_fact_entries_deleted': 0, 'new_questions': 0, 'new_required_facts': 0, 'new_context_items': 2, 'original20_prompts_preserved': True, 'all_previous_explicit_source_key_scope_transcription_corrections_retained': True, 'expanded_readers_dispatched_before_freeze': False, 'canonical_candidate': 'source-candidate-20.md', 'canonical_sha256': H(ROOT / 'rules/spirit-island.md'), 'pure_source09_completed_adoption_retained_on_unchanged_C20': True, 'working43_44_are_actual_v21_passes_with_same_all172_question_objects': True, 'independent_full_current_map_confirmation_pending': True, 'sha256': {str(p): H(p) for p in [NEW / n for n in ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json', 'map-corrections.json']] + [B / 'map-adjudication16-adoption.json', B / 'map16-delivery-validation.json', B / 'source-candidate-20.md']}})
lines = ['# Spirit Island expanded-v22 question and answer bank', '', '172 unchanged questions; 507 grading fact entries. Two pre-test map context corrections; no new procedure questions. Questions alone are reader input. Keys/maps/scope are evaluator data.', '']
for question, answer in zip(q['questions'], k['answers']):
    lines.extend(['## ' + question['id'], '', question['question'], '', answer['answer'], '', 'Sources: ' + '; '.join(answer['source_refs']), ''])
(NEW / 'question-bank.md').write_text('\n'.join(lines) + '\n')
write(B / 'build-status-v22.json', {'benchmark': 'expanded-v22', 'questions': 172, 'required_fact_entries': 507, 'changed_map_entries': changed, 'all_questions_keys_scope_entries_exact': True, 'body_unchanged': True, 'independent_full_current_map_confirmation_pending': True})
print(json.dumps({'benchmark': 'expanded-v22', 'question_count': 172, 'required_fact_count': 507, 'changed_map_entries': changed, 'summary_sha256': H(ROOT / 'rules/spirit-island.md'), 'sha256': {n: H(NEW / n) for n in ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']}}))
