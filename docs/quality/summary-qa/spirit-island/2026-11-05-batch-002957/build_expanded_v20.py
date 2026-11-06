"""Consolidate the complete source-only adjudication14 set; never edit history."""
from pathlib import Path
from collections import Counter
import copy
import hashlib
import json

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
OLD = B / 'expanded-v19'
NEW = B / 'expanded-v20'
H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
T = lambda s: hashlib.sha256(s.encode()).hexdigest()
L = lambda p: json.loads(Path(p).read_text())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


r = L(B / 'working-novelty-adjudication-14.json')
v = L(B / 'novelty14-delivery-validation.json')
assert v['status'] == 'VALID_FOR_RECORDED_EVIDENCE' and not v['exceptions']
assert v['check_count'] == 888 and all(x['ok'] for x in v['checks'])
assert all(H(B / n) == h for n, h in v['immutable_expected_sha256'].items())
assert r['decision_counts'] == {'ACCEPT': 3, 'REFINE': 1, 'REJECT': 0}
assert not NEW.exists()
canonical_sha = H(ROOT / 'rules/spirit-island.md')
assert canonical_sha == H(B / 'source-candidate-19.md') == 'c705923bc215d598f756af6a6fd6dd5c246e762ff7a304dfdc2bdf124ae1463e'
original = {n: L(OLD / n) for n in ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']}
q, k, f, sc = [copy.deepcopy(original[n]) for n in original]
a = r['coverage_decisions'][0]
s = r['scope_decisions'][0]
e1, e2 = r['source_transcription_decisions']
assert a['verdict'] == 'REFINE' and a['minimum_new_required_fact_count'] == 1
assert s['verdict'] == e1['verdict'] == e2['verdict'] == 'ACCEPT'
assert sc['questions'][35] == s['complete_old_scope_entry']
sc['questions'][35] = copy.deepcopy(s['complete_proposed_scope_entry'])
sc['questions'][35].update(
    current_base_novelty_credit_for_numeric_Move_arrow=0,
    unverified_required_fact_indices=[1],
    base_supported_required_fact_indices=[2, 3, 4],
    all_four_conditional_grading_facts_retained=True,
)

old_cost_ref = copy.deepcopy(sc['questions'][163]['primary_sources'][2])
cost_ref = sc['questions'][163]['primary_sources'][2]
old_text = cost_ref['transcribed_passage']
assert old_text.count(e1['exact_old_fragment']) == 1
cost_ref['transcribed_passage'] = old_text.replace(e1['exact_old_fragment'], e1['exact_corrected_fragment'])
cost_ref['transcription_sha256'] = T(cost_ref['transcribed_passage'])
assert cost_ref['transcribed_passage'] == e1['own_prior_transcription_correction']['exact_proposed_corrected_full_transcription']
assert cost_ref['transcription_sha256'] == e1['own_prior_transcription_correction']['corrected_full_transcription_utf8_sha256']

refs = []
for source in a['source_backed_original_core_producer']['source_refs']:
    path = Path(source['path'])
    assert H(path) == source['original_byte_sha256']
    ref = {'file': str(path), 'file_sha256': H(path), 'label': source.get('locator', 'Whole original-core Powerstorm face; explicit Repeat instruction')}
    if 'character_range' in source:
        lo, hi = source['character_range']
        passage = path.read_text()[lo:hi]
        assert passage == source['complete_operative_passage'] and T(passage) == source['passage_utf8_sha256']
        ref.update(character_range=[lo, hi], passage_sha256=T(passage))
    else:
        # The adjudication's cost-corner focus concerns E11-01; the producer
        # instruction is supported by its actually viewed complete native face.
        assert source['full_native_view'] and source['viewed_region_xyxy'] == [0, 0, 300, 420]
        ref.update(visual_region_xyxy=source['viewed_region_xyxy'],
                   full_native_view_region_xyxy=source['viewed_region_xyxy'],
                   transcribed_passage=source['complete_native_transcription'],
                   transcription_sha256=source['transcription_sha256'])
    refs.append(ref)
labels = [x['file'] + ' | ' + x['label'] + ' | SHA256 ' + x['file_sha256'] for x in refs]
novelty = {
    'id': 'Q171', 'question': a['literal_surviving_pretest_question'],
    'answer': a['source_correct_answer'], 'source_refs': labels,
    'exact_source_refs': refs,
    'new_coverage': a['source_defined_distinct_procedure'],
    'why_not_previously_requested': a['why_not_just_repeated_payload'],
    'base_reachability': {'status': 'ESTABLISHED', 'reason': a['source_backed_original_core_producer']},
    'current_base_novelty_credit': True, 'proposal_id': 'G11-01',
    'adjudication_decision': 'REFINE',
    'origin': 'Complete fresh challenge11 set, independently source-adjudicated14 before any expanded readers',
}
q['questions'].append({'id': 'Q171', 'question': novelty['question']})
k['answers'].append({'id': 'Q171', 'answer': novelty['answer'], 'source_refs': labels})
mapping = copy.deepcopy(a['minimal_asked_only_map'])
mapping.update(id='Q171', question=novelty['question'])
for index, clause in enumerate(mapping['requested_clauses'], 1):
    clause['clause_id'] = 'Q171.' + str(index)
f['questions'].append(mapping)
sc['questions'].append({'id': 'Q171', 'scope_result': 'base_supported',
                        'base_reachability': novelty['base_reachability'],
                        'primary_sources': refs, 'current_base_novelty_credit': True})
assert q['questions'][:170] == original['questions.json']['questions']
assert k['answers'][:170] == original['answer-key.json']['answers']
assert f['questions'][:170] == original['asked-fact-map.json']['questions']
assert [x['id'] for x, old in zip(sc['questions'][:170], original['core-scope-credit.json']['questions']) if x != old] == ['Q36', 'Q164']
q['benchmark_version'] = k['benchmark_version'] = 'expanded-v20'
f.update(benchmark='expanded-v20', question_count=171,
         required_fact_count=sum(len(c['required_facts']) for x in f['questions'] for c in x['requested_clauses']))
assert f['required_fact_count'] == 506
sc.update(benchmark='expanded-v20', question_count=171)
overlay = sc['working_scope_credit_overlay']
prior_overlay = copy.deepcopy(overlay)
for number in [154, 163, 169, 170, 171]:
    cohort = Counter(x['scope_result'] for x in sc['questions'][:number])
    assert set(cohort) <= {'base_supported', 'mixed_supported_and_noncredited', 'noncredited_pending_base_proof'}
    overlay['working_question_counts_for' + str(number)] = {
        'base_supported': cohort['base_supported'],
        'mixed_supported_and_noncredited': cohort['mixed_supported_and_noncredited'],
        'noncredited_only': cohort['noncredited_pending_base_proof'],
    }
for name, counts in list(overlay.items()):
    if name.startswith('working_audited_clause_counts'):
        counts['base_supported'] -= 1
        counts['unverified_base_reachability'] += 1
counts = copy.deepcopy(overlay['working_audited_clause_counts_after_bringer_limit'])
counts['base_supported'] += 1
overlay['working_audited_clause_counts_after_explicit_element_grant'] = counts
assert counts == {'base_supported': 484, 'unverified_base_reachability': 26, 'generalized_engine_regression': 1}
assert overlay['working_question_counts_for171'] == {'base_supported': 154, 'mixed_supported_and_noncredited': 14, 'noncredited_only': 3}
sc['scope_revision_v20'] = {
    'Q36_first_asked_fact_only_loses_base_novelty_credit': True,
    'all505_prior_grading_facts_retained': True,
    'prior_v19_working_overlay_preserved_here_as_history': prior_overlay,
    'historical_baseline_fields_notice': 'classification_counts_for_original154 and scope_only_subclauses_for_original154 retain the original baseline audit, before explicit Q71/Q36 overlays; current row-derived cohort counts are in working_scope_credit_overlay.',
    'audited_clause_total': 511, 'required_grading_fact_total': 506,
    'five_scope_premises_are_not_extra_grading_requirements': True,
}
corrections = {
    'source_only_before_expanded_readers': True,
    'adjudication': {'path': str(B / 'working-novelty-adjudication-14.json'), 'sha256': H(B / 'working-novelty-adjudication-14.json')},
    'Q36_scope': {'old': s['complete_old_scope_entry'], 'new': sc['questions'][35],
                  'question_key_map_unchanged': True, 'all4_facts_fully_graded': True},
    'Powerstorm_scope_source_reference': {'old': old_cost_ref, 'new': cost_ref,
                                        'no_question_key_map_or_required_fact_change': True},
    'transcription_decisions': r['source_transcription_decisions'],
    'raw_prior_reports_ledgers_frozen_maps_and_acceptance_history_not_rewritten': True,
}
NEW.mkdir()
for name, value in [('questions.json', q), ('answer-key.json', k), ('core-scope-credit.json', sc),
                    ('novelty.json', [novelty]), ('metadata-corrections.json', corrections)]:
    write(NEW / name, value)
f['creator_provenance'] = {
    'role': 'Root pre-test consolidation of the complete adjudication14 finding set',
    'prior_map': str(OLD / 'asked-fact-map.json'), 'prior_map_sha256': H(OLD / 'asked-fact-map.json'),
    'all170_prior_map_entries_exact': True, 'all170_prior_questions_and_keys_exact': True,
    'summary_seen': True, 'historical_seed_answers_known': True,
    'no_expanded_reader_outputs_exist': True, 'required_new_fresh_whole_corpus_scope_validation': True,
}
f['input_hashes'] = {str(path): H(path) for path in [NEW / 'questions.json', NEW / 'answer-key.json',
    NEW / 'metadata-corrections.json', OLD / 'asked-fact-map.json', B / 'working-novelty-adjudication-14.json']}
write(NEW / 'asked-fact-map.json', f)
write(NEW / 'input-manifest.json', {
    'question_count': 171, 'required_fact_count': 506, 'prior_version': 'expanded-v19',
    'all_prior170_questions_keys_and_map_entries_exact': True,
    'prior_scope_rows_changed_only_Q36_credit_and_Q164_source_transcription': True,
    'complete_surviving_set': ['G11-01 refined positive branch'], 'new_questions': 1, 'new_required_facts': 1,
    'scope_and_transcription_corrections_add_no_grading_facts': True,
    'original20_prompts_preserved': q['questions'][:20] == L(B / 'seed-v1/questions.json')['questions'],
    'all_versioned_Q18_Q157_Q71_Q84_corrections_retained': True,
    'expanded_readers_dispatched_before_freeze': False,
    'canonical_candidate': 'source-candidate-19.md', 'canonical_sha256': canonical_sha,
    'sha256': {str(path): H(path) for path in [NEW / n for n in ['questions.json', 'answer-key.json',
        'asked-fact-map.json', 'core-scope-credit.json', 'metadata-corrections.json']]
        + [OLD / n for n in ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']]
        + [B / 'working-novelty-adjudication-14.json', B / 'working-novelty-adjudication-14-read-ledger.json',
           B / 'novelty14-delivery-validation.json', B / 'supplemental-source-manifest-v4.json']},
})
(NEW / 'question-bank.md').write_text('# Spirit Island expanded bank v20\n\n'
    '171 retained questions and506 required-fact entries. All170 prior questions, keys and asked-map entries remain exact. '
    'One independently refined positive Element-text grant branch is appended. Q36 current-base novelty credit and two supporting source transcriptions are explicitly corrected; all original hard regressions remain fully graded. '
    'Two new actual zero-addition passes and a NEW fresh whole-corpus challenge are required. No expanded reader outputs or current coverage PASS.\n\n'
    + '\n\n'.join(f"## {x['id']}\n\n{x['question']}\n\n**Expected:** {y['answer']}\n\n**Sources:** {'; '.join(y['source_refs'])}" for x, y in zip(q['questions'], k['answers'])) + '\n')
assert H(ROOT / 'rules/spirit-island.md') == canonical_sha
write(B / 'build-status-v20.json', {'bank_files_complete': True, 'questions': 171, 'required_facts': 506,
    'prior170_q_key_map_exact': True, 'complete4_findings_consolidated': True,
    'summary_body_unchanged_C19': True, 'source_audit08_reusable_only_exact_C19': True,
    'new_working_two_zero_and_fresh_challenge_required': True, 'expanded_readers_dispatched': False})
print(json.dumps({'bank': 'expanded-v20', 'questions': 171, 'facts': 506,
                  'all170_q_key_map_entries_exact': True, 'scope_counts': overlay['working_question_counts_for171'],
                  'canonical_unchanged': canonical_sha}))
