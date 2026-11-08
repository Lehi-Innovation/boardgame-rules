"""Freeze unchanged bank; initial-prompt-only generic process; fixed batch turns."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil

R = Path(__file__).parent.resolve()
OLD = R / 'expanded-iteration-02'
IT = R / 'expanded-iteration-03'
assert not IT.exists()


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


previous = read(OLD / 'corrected-grades-aggregate-v2.json')
assert previous['question_count'] == 167
assert any(previous['totals'][c]['correct'] < 167 for c in 'ab')
assert read(OLD / 'bookkeeping-audit-17.json')['pass'] is True
for n in range(1, 10):
    assert read(OLD / f'grader-{n:02}-v2-runtime-delivery-validation.json')['pass']
snapshot = R / 'repair-freeze-14.md'
assert sha(snapshot) == '0020b1a20e385dfcc45e9d2bb68cc20ed185267d99f9be0088a6453170e04edc'
assert snapshot.read_bytes() == (R.parents[4] / 'rules/cosmic-encounter.md').read_bytes()
audit = R / 'source-review/source-only-audit-15-freeze14.json'
assert read(audit)['verdict'] == 'PASS'
assert read(R / 'source-review/source15-freeze14-reuse-chain-validation-01.json')['pass']
choices = R.parents[1] / 'batches/2026-11-05-batch-002957/coordinator-checks/cosmic-pending-human-scope-choice.json'
assert read(choices)['human_answer_received'] is False
method = R / 'reader-method-v12/source_units.py'
assert read(R / 'reader-method-v12/validation.json')['neutral_tests_passed']
assert sha(method) == read(R / 'reader-method-v12/validation.json')['source_code_sha256']
questions = read(OLD / 'questions.json')['questions']
key = read(OLD / 'answer-key.json')['answers']
assert len(questions) == 167 and sum(len(a['required_facts']) for a in key) == 544
assert questions[:20] == read(R / 'seed-v1/questions.json')['questions']
assert key[:20] == read(R / 'seed-v1/answer-key.json')['answers']
IT.mkdir()
shutil.copyfile(snapshot, IT / 'summary-snapshot.md')
for name in ('questions.json', 'answer-key.json', 'actual-question-scope.json',
             'pre-reader-gate-decision.json'):
    shutil.copyfile(OLD / name, IT / name)
    assert (IT / name).read_bytes() == (OLD / name).read_bytes()
shutil.copyfile(method, IT / 'generic-method-code.py')
template = (R / 'full-bank-reader-protocol-template-v4.txt').read_text()
base = (template.replace('SUMMARY_PATH', str(IT / 'summary-snapshot.md'))
        .replace('QUESTIONS_PATH', str(IT / 'questions.json'))
        .replace('METHOD_CODE_SHA256', sha(method))
        .replace('METHOD_CODE', method.read_text().rstrip('\n')))
for c in 'ab':
    prompt = base.replace('OUTPUT_PATH', str(IT / f'reader-{c}.json'))
    (IT / f'reader-{c}-prompt.txt').write_text(prompt)
assert ((IT / 'reader-a-prompt.txt').read_text().replace(str(IT / 'reader-a.json'), 'OUTPUT_PATH')
        == (IT / 'reader-b-prompt.txt').read_text().replace(str(IT / 'reader-b.json'), 'OUTPUT_PATH'))
continuation = ('Continue your original blind task under the unchanged initial instructions. '
                'Complete exactly the next ten question records in original bank order, or all '
                'remaining records if fewer than ten remain. Preserve the original earlier entries '
                'and input receipts in your cumulative output. Use only the same two frozen data '
                'files and your own partial output. No rule, answer, key or grade feedback is supplied. '
                'Save your cumulative checked output, then stop this turn at the fixed batch boundary.')
(IT / 'generic-continuation-message.txt').write_text(continuation)
schedule = [{'batch': n + 1, 'start_record_index': start,
             'end_record_index_exclusive': min(start + 10, len(questions))}
            for n, start in enumerate(range(0, len(questions), 10))]
(IT / 'fixed-blind-batch-schedule.json').write_text(json.dumps({
    'schedule_fixed_before_readers': True, 'schedule': schedule,
    'identical_generic_continuation_message': continuation,
    'same_initially_fresh_identities_across_all_batches': True,
    'parent_checks_only_prefix_ids_and_unchanged_earlier_bytes_or_values': True,
    'no_factual_feedback_or_targeted_retries': True}, indent=2) + '\n')
manifest = {
    'created_at_utc': datetime.now(timezone.utc).isoformat(),
    'purpose': 'Preliminary full unchanged167 bank regression; no final global scope/publication approval.',
    'full_bank_freeze_authorized': True, 'independent_actual_scope_validated': True,
    'question_count': 167, 'raw_key_fact_count': 544,
    'bank_version': 'expanded-candidate-15', 'expected_ids': [q['id'] for q in questions],
    'questions_key_scope_byte_identical_to_iterations01_02': True,
    'original_twenty_preserved_verbatim': True,
    'unresolved_global_authority_topics': read(OLD / 'input-manifest.json')['unresolved_global_authority_topics'],
    'pending_dependent_source_choices': [], 'final_scope_freeze': False,
    'completion_readiness': False, 'human_choices_adopted': False,
    'source_corrections_path': str(R / 'source-review/source-corrections-14.json'),
    'source_audit_path': str(audit), 'source_audit_sha256': sha(audit),
    'source_audit_limit': 'Own isolated auditor15 continuation; documented2authoritygaps; not new vote/publication approval.',
    'reader_protocol_version': 4, 'process_and_code_embedded_only_in_initial_prompt': True,
    'external_process_files_authorized_for_readers': [],
    'sole_game_data_files': [str(IT / 'summary-snapshot.md'), str(IT / 'questions.json')],
    'generic_code_sha256': sha(method),
    'generic_code_neutral_validation': str(R / 'reader-method-v12/validation.json'),
    'generic_code_coordinator_approval_claimed': False,
    'fixed_batch_count': len(schedule), 'fixed_batch_schedule': str(IT / 'fixed-blind-batch-schedule.json'),
    'no_question_specific_routing_or_failed_facts_supplied': True,
    'sha256': {str(p): sha(p) for p in IT.iterdir() if p.is_file()},
    'no_readers_dispatched_by_this_script': True}
(IT / 'input-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print('Frozen unchanged167/544;17fixed turns each; initial prompt characters:', len(prompt))
