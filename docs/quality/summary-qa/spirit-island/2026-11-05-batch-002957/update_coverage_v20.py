from pathlib import Path
import copy
import hashlib
import json

B = Path(__file__).resolve().parent
H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
T = lambda s: hashlib.sha256(s.encode()).hexdigest()
L = lambda p: json.loads(Path(p).read_text())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


bank = B / 'expanded-v20'
manifest = L(bank / 'input-manifest.json')
assert all(H(p) == h for p, h in manifest['sha256'].items())
path = B / 'coverage-ledger.json'
backup = B / 'coverage-ledger-before-novelty14-resolution.json'
assert not backup.exists()
ledger = L(path)
assert ledger['benchmark'] == 'expanded-v19'
adjudication = L(B / 'working-novelty-adjudication-14.json')
novelty = L(bank / 'novelty.json')[0]
fixes = adjudication['source_transcription_decisions']
patches = []
for collection in ['faq_rulings', 'precise_clause_mappings']:
    for index, entry in enumerate(ledger[collection]):
        for ri, ref in enumerate(entry.get('source_refs', [])):
            if not isinstance(ref, dict):
                continue
            for key in ['transcription', 'transcribed_passage']:
                if key not in ref:
                    continue
                for fix in fixes:
                    old, new = fix['exact_old_fragment'], fix['exact_corrected_fragment']
                    if old not in ref[key]:
                        continue
                    previous = copy.deepcopy(ref)
                    assert ref[key].count(old) == 1
                    ref[key] = ref[key].replace(old, new)
                    ref['transcription_sha256'] = T(ref[key])
                    patches.append({'finding_id': fix['finding_id'],
                                    'pointer': f'/{collection}/{index}/source_refs/{ri}',
                                    'old': previous, 'new': copy.deepcopy(ref)})
assert [x['finding_id'] for x in patches].count('E11-01') == 2
assert [x['finding_id'] for x in patches].count('E11-02') == 1
growth = next(x for x in ledger['faq_rulings'] if x['ruling_id'] == 'growth-move-v-add')
old_growth = copy.deepcopy(growth)
growth.update(scope='Mixed: Add/reposition original-base; numeric Growth Move arrow conditional/unverified',
              scope_annotation=adjudication['scope_decisions'][0]['coverage_annotation_proposed'],
              numeric_Move_arrow_current_base_novelty_credit=0,
              add_reposition_current_base_supported=True,
              full_conditional_regression_grading_retained=True)
ledger.setdefault('source_transcription_corrections', []).append({
    'bank': 'expanded-v20', 'adjudication': 'working-novelty-adjudication-14.json',
    'adjudication_sha256': H(B / 'working-novelty-adjudication-14.json'),
    'working_source_refs_before_after': patches,
    'core_scope_credit_Q164_before_after': 'expanded-v20/metadata-corrections.json',
    'historical_acceptance_entries_not_rewritten': [
        '/acceptance_ledger/129/exact_source_refs/0/transcription',
        '/acceptance_ledger/143/exact_source_refs/2/transcribed_passage',
        '/acceptance_ledger/143/raw_source_refs/2/transcription',
    ],
    'history_disposition': 'These raw acceptance records preserve original claims. The explicit E11-01/02 errata control current source interpretation; frozen reports/ledgers/v19 remain unchanged.',
    'question_key_map_or_required_fact_delta': 0,
})
ledger.setdefault('source_scope_credit_corrections_v20', []).append({
    'bank': 'expanded-v20', 'id': 'Q36', 'finding': 'S11-01',
    'metadata_correction': 'expanded-v20/metadata-corrections.json',
    'old_coverage_annotation': old_growth, 'new_coverage_annotation': copy.deepcopy(growth),
    'unsupported_asked_fact_index': 1, 'base_novelty_credit_for_that_fact': 0,
    'all4_original_grading_facts_retained': True,
})
ledger['acceptance_ledger'].append({**novelty, 'bank': 'expanded-v20',
    'decision': 'REFINE: complete challenge11 set independently source-adjudicated14; positive grant branch only'})
ledger['precise_clause_mappings'].append({
    'topic': novelty['new_coverage'], 'source_refs': novelty['exact_source_refs'],
    'question_ids': ['Q171'], 'tested_clause': novelty['question'],
    'base_reachability': novelty['base_reachability'],
})
ledger['faq_rulings'].append({
    'ruling_id': 'challenge11-Q171', 'rule': novelty['answer'],
    'source_refs': novelty['exact_source_refs'], 'question_ids': ['Q171'],
    'scope': 'Verified original-core Elemental Boon/Powerstorm positive explicit Element-grant branch',
    'current_base_novelty_credit': True,
})
for record in ledger['independent_challenge_history']:
    if record.get('report') == 'coverage-review-11.json':
        record.update(adjudication='working-novelty-adjudication-14.json',
                      accepted_ids=['Q171'], survivors=1, new_required_facts=1,
                      scope_metadata_corrections=['Q36'],
                      source_transcription_corrections=['E11-01', 'E11-02'],
                      prior_zero_pass_claim_revoked=True,
                      all170_prior_q_key_map_entries_exact=True)
ledger['stopping_rule_history'].append(copy.deepcopy(ledger['stopping_rule']))
ledger.update(benchmark='expanded-v20', question_count=171)
ledger['stopping_rule'] = {
    'consecutive_zero_addition_passes': [], 'all_in_scope_procedural_passages_mapped': False,
    'independent_challenge': 'pending actual working41/42 then NEWfresh whole-corpus12',
    'claim': 'Complete new positive-grant survivor Q171 consolidated; restart genuine two-zero/fresh-challenge cycle. Actual39/40 zero history remains intact; it is not the new stopping streak.',
}
ledger['pretest_asked_fact_mapping'].update(
    path='expanded-v20/asked-fact-map.json', sha256=H(bank / 'asked-fact-map.json'),
    question_count=171, required_fact_count=506,
    scope_review='pending actual working41/42 then NEWfresh whole-corpus12')
ledger['scope_reachability_policy']['retained_regression_credit'] = 'expanded-v20/core-scope-credit.json'
ledger['input_hashes'] = {str(p): H(p) for p in [bank / n for n in
    ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']]
    + [B / 'supplemental-source-manifest-v4.json']}
backup.write_bytes(path.read_bytes())
write(path, ledger)
write(B / 'coverage-v20-source-corrections.json', {
    'working_source_reference_patches': patches, 'Q36_old': old_growth, 'Q36_new': growth,
    'metadata_corrections': {'path': str(bank / 'metadata-corrections.json'), 'sha256': H(bank / 'metadata-corrections.json')},
    'prior_ledger_preserved': {'path': str(backup), 'sha256': H(backup)},
})

Q = L(bank / 'questions.json'); K = L(bank / 'answer-key.json')
F = L(bank / 'asked-fact-map.json'); C = L(bank / 'core-scope-credit.json')
packet = {
    'purpose': 'Complete current171 source-only working-pass delta packet; no summary/readers/grades/peer review verdicts',
    'benchmark': 'expanded-v20', 'question_count': 171, 'required_fact_count': 506,
    'complete_new_question_objects': Q['questions'][170:],
    'complete_new_key_objects': K['answers'][170:],
    'complete_new_asked_map_objects': F['questions'][170:],
    'full_bank_sha256': {n: H(bank / n) for n in ['questions.json', 'answer-key.json', 'asked-fact-map.json', 'core-scope-credit.json']},
    'prior170_equivalence': {'all_question_key_map_objects_exact': True,
        'own_previous_complete_version': 'expanded-v19 reconstructed in working39/40',
        'prior_hashes': {n: H(B / 'expanded-v19' / n) for n in ['questions.json', 'answer-key.json', 'asked-fact-map.json']}},
    'complete_Q36_current_scope_entry': C['questions'][35],
    'Q36_actual_question_key_map': {'question': Q['questions'][35], 'key': K['answers'][35], 'asked_map': F['questions'][35]},
    'scope_credit_current_not_a_coverage_authority': 'Numeric Growth Move-arrow branch has no verified original-eight producer; Add/reposition remains core. Independently check primary sources; all4 conditional grading facts remain. Other generalized/unverified regressions remain fully graded with0base novelty.',
    'current_source_transcription_errata': [{
        'source_file': x['native_source']['path'], 'source_sha256': x['native_source']['original_byte_sha256'],
        'old_fragment': x['exact_old_fragment'], 'current_fragment': x['exact_corrected_fragment'],
        'full_current_native_transcription': x['native_source']['complete_native_transcription'],
        'current_transcription_sha256': x['native_source']['transcription_sha256'],
        'unasked_payload_creates_no_new_grading_fact': True,
    } for x in fixes],
    'new_primary_source_refs': novelty['exact_source_refs'],
    'all_primary_source_versions_unchanged': True,
    'no_source_verdict_or_forced_zero': True,
    'no_expanded_reader_outputs_exist': True,
}
write(B / 'working-pass-v20-supplement.json', packet)
print(json.dumps({'bank': 'expanded-v20', 'questions': 171, 'facts': 506,
                  'current_source_refs_corrected': len(patches), 'Q36_first_fact_credit': 0,
                  'zero_streak_reset': True, 'working_packet_characters': len((B / 'working-pass-v20-supplement.json').read_text())}))
