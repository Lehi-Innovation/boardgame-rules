"""Freeze the whole168 bank, supplemented scope and generic literal-binding method."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

R = Path(__file__).parent.resolve()
IT = R / 'expanded-iteration-06'
C = R / 'expanded-candidate-16'
assert not IT.exists()


def read(p):
    return json.loads(p.read_bytes())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


assert read(R / 'expanded-iteration-05/adjudicated-grades-aggregate.json')['both_readers_all_correct'] is False
assert read(R / 'expanded-iteration-05/bookkeeping-audit-23.json')['technical_pass']
assert read(R / 'expanded-iteration-05/neutral25-case-integrity-validation.json')['pass']
assert read(R / 'source-review/freeze17-unchanged-168-scope-coverage-continuity.json')['pass']
assert read(R / 'generic-staged-v7-v15-coordinator-acceptance.json')['accepted']
assert read(R / 'source-review/source-only-audit-15-freeze17.json')['verdict'] == 'PASS'
assert read(R / 'source-review/source15-freeze17-full-new-input-own-reuse-validation.json')['pass']
assert read(R / 'source-review/literal14-v5-bank16-integrity-validation.json')['pass']
assert read(R / 'source-review/literal14-v5-runtime-delta-delivery-validation.json')['pass']
assert read(R / 'source-review/supplement-coverage-20/actual-delivery-validation.json')['pass']
assert read(R / 'source-review/supplement-coverage-20/coverage-challenge.json')['bounded_verdict']['new_gap_count'] == 0
assert read(C / 'targeted-coverage-passes-renewed-16.json')['renewed_pass27']['new_qualifying_groups'] == 0
assert read(C / 'targeted-coverage-passes-renewed-16.json')['renewed_pass28']['new_qualifying_groups'] == 0
gate = read(R / 'pre-reader-gate-decision-03.json')
assert gate['pending_dependent_source_choices'] == [] and not gate['final_scope_readiness']
snapshot = R / 'repair-freeze-17.md'
assert sha(snapshot) == '787b88677123fc93751d1605a99e4c724faadaa891f1b0c103bcb296075952b9'
assert snapshot.read_bytes() == (R.parents[4] / 'rules/cosmic-encounter.md').read_bytes()
questions, key = read(C / 'questions.json'), read(C / 'answer-key.json')
assert len(questions['questions']) == len(key['answers']) == 168
assert sum(len(a['required_facts']) for a in key['answers']) == 547
assert questions['questions'][:-1] == read(R / 'expanded-iteration-03/questions.json')['questions']
assert key['answers'][:-1] == read(R / 'expanded-iteration-03/answer-key.json')['answers']
assert questions['questions'][:20] == read(R / 'seed-v1/questions.json')['questions']
assert key['answers'][:20] == read(R / 'seed-v1/answer-key.json')['answers']
method = R / 'reader-method-v15/source_units.py'
assert read(R / 'reader-method-v15/validation.json')['neutral_tests_passed']
assert sha(method) == read(R / 'reader-method-v15/validation.json')['source_code_sha256']
IT.mkdir()
shutil.copyfile(snapshot, IT / 'summary-snapshot.md')
supplement_scope = (' Single specifically attributed later FFG revised-rulebook p16 '
                    'chosen-alien reveal instruction is included; all other revised content remains excluded.')
for name, doc in [('questions.json', questions), ('answer-key.json', key)]:
    doc['scope'] += supplement_scope
    (IT / name).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + '\n')
shutil.copyfile(R / 'source-review/literal-scope-map-14-v5.json', IT / 'actual-question-scope.json')
shutil.copyfile(R / 'pre-reader-gate-decision-03.json', IT / 'pre-reader-gate-decision.json')
shutil.copyfile(R / 'source-review/source-scope-16.json', IT / 'source-scope.json')
shutil.copyfile(method, IT / 'generic-method-code.py')
reader_questions = IT / 'reader-questions-final.json'
process = ((R / 'full-bank-reader-protocol-template-v7.txt').read_text()
           .replace('SUMMARY_PATH', str(IT / 'summary-snapshot.md'))
           .replace('QUESTIONS_PATH', str(reader_questions))
           .replace('METHOD_CODE_SHA256', sha(method))
           .replace('METHOD_CODE', method.read_text().rstrip('\n')))
assert 'METHOD_CODE' not in process
assert str(R / 'expanded-iteration-03') not in process
reader_doc = read(IT / 'questions.json')
reader_doc['reader_process'] = {'kind': 'generic_process_only_no_rules_answers_or_question_routing',
                                'instructions': process,
                                'instructions_sha256': hashlib.sha256(process.encode()).hexdigest(),
                                'method_code_sha256': sha(method)}
reader_questions.write_text(json.dumps(reader_doc, indent=2, ensure_ascii=False) + '\n')
assert read(reader_questions)['questions'] == questions['questions']
acceptance = read(R / 'generic-staged-v7-v15-coordinator-acceptance.json')
assert sha(method) == acceptance['method_sha256']
assert sha(R / 'full-bank-reader-protocol-template-v7.txt') == acceptance['template_sha256']
prospective = Path(acceptance['proof_path'])
assert sha(prospective) == acceptance['proof_sha256']
reader_work_paths = {c: {'draft': str(IT / f'reader-{c}-draft.json'),
                         'final': str(IT / f'reader-{c}.json')} for c in 'ab'}
for c in 'ab':
    prompt = ((R / 'reader-input-bootstrap-template-v7.txt').read_text()
              .replace('SUMMARY_PATH', str(IT / 'summary-snapshot.md'))
              .replace('QUESTIONS_PATH', str(reader_questions))
              .replace('DRAFT_PATH_VALUE', reader_work_paths[c]['draft'])
              .replace('FINAL_PATH_VALUE', reader_work_paths[c]['final']))
    prompt += f'\nYour reader label for the work-file reader field is "{c}".\n'
    (IT / f'reader-{c}-prompt.txt').write_text(prompt)
normalized = []
for c in 'ab':
    value = (IT / f'reader-{c}-prompt.txt').read_text()
    value = value.replace(reader_work_paths[c]['draft'], 'DRAFT_PATH_VALUE')
    value = value.replace(reader_work_paths[c]['final'], 'FINAL_PATH_VALUE')
    value = value.replace(f'field is "{c}"', 'field is "READER_LABEL"')
    normalized.append(value)
assert normalized[0] == normalized[1]
schedules = {}
for stage, size in [('draft', 10), ('review', 20)]:
    text = (R / f'staged-{stage}-continuation-message-v7.txt').read_text()
    (IT / f'generic-{stage}-continuation-message.txt').write_text(text)
    schedules[stage] = [{'batch': i+1, 'start_record_index': start,
                         'end_record_index_exclusive': min(start+size,168)}
                        for i,start in enumerate(range(0,168,size))]
(IT / 'fixed-staged-schedule.json').write_text(json.dumps({
    'schedule_fixed_before_readers': True, 'input_only_first_turn': True,
    'same_initially_fresh_identities_across_all_stages': True,
    'no_factual_feedback_or_targeted_retries': True,
    'closed_complete_draft_preserved': True,
    'schedule': schedules}, indent=2)+'\n')
manifest = {'created_at_utc': datetime.now(timezone.utc).isoformat(),
            'purpose': 'Complete preliminary168-bank regression; no finalglobal source/publication approval.',
            'full_bank_freeze_authorized': True, 'independent_actual_scope_validated': True,
            'question_count': 168, 'raw_key_fact_count': 547, 'required_semantic_unit_count': 696,
            'bank_version': 'expanded-candidate-16', 'expected_ids': [q['id'] for q in questions['questions']],
            'question_key_records_exact_candidate16': True,
            'wrapper_scope_only_updated_to_state_authorized_supplement': True,
            'all_prior167_and_original20_records_preserved': True,
            'source_scope_manifest': str(R / 'source-review/source-scope-16.json'),
            'source_audit_path': str(R / 'source-review/source-only-audit-15-freeze17.json'),
            'source_audit_limit': 'Exactfreeze17 sourcePASS after11newfullchunks/164selectedchars; ownunchangedoriginalsource/50image reuse explicit; oneessentialFAQconflict remains.',
            'coverage_stopping_closure': str(C / 'coverage-stopping-closure.json'),
            'unresolved_global_authority_topics': gate['unresolved_global_authority_topics'],
            'pending_dependent_source_choices': [], 'final_scope_freeze': False,
            'completion_readiness': False, 'human_interpretation_adopted': False,
            'reader_protocol_version': 7, 'generic_code_sha256': sha(method),
            'generic_code_neutral_validation': str(R / 'reader-method-v15/validation.json'),
            'prospective_generic_method_review': str(prospective),
            'prospective_review_limit': 'Genericprocess/code preflight only; actual newmodel/input/originalgrading checks stillrequired.',
            'process_and_code_embedded_in_question_file_metadata': True,
            'external_process_files_authorized_for_readers': [],
            'sole_game_data_files': [str(IT / 'summary-snapshot.md'), str(reader_questions)],
            'active_dispatch_prompt_paths': {c: str(IT / f'reader-{c}-prompt.txt') for c in 'ab'},
            'reader_tasks': {c: '/root/expanded6_reader_' + c for c in 'ab'},
            'reader_work_paths': reader_work_paths,
            'model_provenance_path': str(R / 'model-provenance.json'),
            'stage_schedule': {'draft_batch_size': 10, 'review_batch_size': 20},
            'fixed_draft_batch_count': 17, 'fixed_review_batch_count': 9,
            'fixed_stage_schedule': str(IT / 'fixed-staged-schedule.json'),
            'grading_only_after_both_complete_review': True,
            'no_question_specific_routing_or_failed_facts_supplied': True,
            'sha256': {str(p): sha(p) for p in IT.iterdir() if p.is_file()},
            'no_readers_dispatched_by_this_script': True}
(IT / 'input-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
shutil.copyfile(IT / 'input-manifest.json', IT / 'input-manifest-final.json')
print('Frozen168/547/696; readiness+17draft+9review; readerdatacharacters:',
      len((IT / 'summary-snapshot.md').read_text()), len(reader_questions.read_text()))
