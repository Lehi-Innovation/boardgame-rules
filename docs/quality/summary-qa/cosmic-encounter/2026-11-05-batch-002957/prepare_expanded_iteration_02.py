"""Freeze the unchanged bank with source repair13 and generic process v3."""
from pathlib import Path
import hashlib
import json
import shutil
from datetime import datetime, timezone

R = Path(__file__).parent.resolve()
OLD, IT = R / 'expanded-iteration-01', R / 'expanded-iteration-02'
assert not IT.exists()


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


previous = read(OLD / 'adjudicated-grades-aggregate.json')
assert previous['question_count'] == 167 and previous['factual_pair_pass'] is False
assert read(OLD / 'borderline16-runtime-delivery-validation-02.json')['pass'] is True
for i in range(1, 10):
    assert read(OLD / f'grader-{i:02}-runtime-delivery-validation.json')['pass'] is True
snapshot = R / 'repair-freeze-13.md'
assert sha(snapshot) == 'a7476044204b670b4b2e906ca64a659487e6d5bab891cfe6340fc379b90b81a0'
assert snapshot.read_bytes() == (R.parents[4] / 'rules/cosmic-encounter.md').read_bytes()
audit = R / 'source-review/source-only-audit-15-freeze13.json'
assert read(audit)['verdict'] == 'PASS'
assert read(R / 'source-review/source15-freeze13-runtime-delivery-validation-01.json')['pass'] is True
choices_path = R.parents[1] / 'batches/2026-11-05-batch-002957/coordinator-checks/cosmic-pending-human-scope-choice.json'
assert read(choices_path)['human_answer_received'] is False
questions = read(OLD / 'questions.json')['questions']
key = read(OLD / 'answer-key.json')['answers']
assert len(questions) == 167
assert sum(len(a['required_facts']) for a in key) == 544
assert questions[:20] == read(R / 'seed-v1/questions.json')['questions']
assert key[:20] == read(R / 'seed-v1/answer-key.json')['answers']
method = R / 'reader-method-v11/source_units.py'
assert read(R / 'reader-method-v11/validation.json')['neutral_tests_passed'] is True
assert sha(method) == read(R / 'reader-method-v11/validation.json')['source_code_sha256']

IT.mkdir()
shutil.copyfile(snapshot, IT / 'summary-snapshot.md')
for name in ['questions.json', 'answer-key.json', 'actual-question-scope.json',
             'pre-reader-gate-decision.json']:
    shutil.copyfile(OLD / name, IT / name)
template = (R / 'full-bank-reader-protocol-template-v3.txt').read_text()
instructions = (template.replace('SUMMARY_PATH', str(IT / 'summary-snapshot.md'))
                .replace('QUESTIONS_PATH', str(IT / 'questions.json'))
                .replace('METHOD_CODE_SHA256', sha(method))
                .replace('METHOD_CODE', method.read_text().rstrip('\n')))
assert len(instructions) <= 11600
(IT / 'reader-process-instructions.txt').write_text(instructions)
shutil.copyfile(method, IT / 'generic-method-code.py')
for letter in ['a', 'b']:
    prompt = (
        'You are a new independent blind reader. Your OUTPUT_PATH is ' +
        str(IT / f'reader-{letter}.json') + '. Read the complete shared process '
        'instructions at ' + str(IT / 'reader-process-instructions.txt') +
        ' in actual visible blocks of at most 5800 characters, clamping the final '
        'remainder. Then follow those instructions. That file contains only '
        'generic process/code; the two game-data files named inside are your '
        'sole rules authority. Do not read any other files except your own '
        'partial output. Do not browse, use prior game knowledge, delegate or '
        'communicate with other readers. The same shared instructions apply '
        'to each reader; only OUTPUT_PATH differs. Complete the entire question '
        'bank and save only your assigned output.'
    )
    (IT / f'reader-{letter}-prompt.txt').write_text(prompt)
assert ((IT / 'reader-a-prompt.txt').read_text().replace(str(IT / 'reader-a.json'), 'OUTPUT_PATH')
        == (IT / 'reader-b-prompt.txt').read_text().replace(str(IT / 'reader-b.json'), 'OUTPUT_PATH'))
for name in ['questions.json', 'answer-key.json', 'actual-question-scope.json']:
    assert (IT / name).read_bytes() == (OLD / name).read_bytes()
files = [p for p in IT.iterdir() if p.is_file()]
manifest = {
    'created_at_utc': datetime.now(timezone.utc).isoformat(),
    'purpose': 'Preliminary complete fixed167-bank repair regression; no final global scope or publication approval.',
    'full_bank_freeze_authorized': True,
    'independent_actual_scope_validated': True,
    'pending_dependent_source_choices': [],
    'unresolved_global_authority_topics': read(OLD / 'input-manifest.json')['unresolved_global_authority_topics'],
    'final_scope_freeze': False, 'completion_readiness': False,
    'question_count': 167, 'raw_key_fact_count': 544,
    'expected_ids': [a['id'] for a in questions],
    'bank_version': 'expanded-candidate-15',
    'questions_key_scope_byte_identical_to_iteration01': True,
    'original_twenty_preserved_verbatim': True,
    'summary_source_repair': str(R / 'source-review/source-corrections-13.json'),
    'source_audit_path': str(audit), 'source_audit_sha256': sha(audit),
    'source_audit_limit': 'Source verdict PASS with two documented authority gaps; not coordinator/publication approval.',
    'reader_protocol_version': 3,
    'shared_instruction_file': str(IT / 'reader-process-instructions.txt'),
    'shared_instruction_characters': len(instructions),
    'instructions_are_process_only_not_additional_rule_data': True,
    'generic_code_sha256': sha(method),
    'generic_code_neutral_validation': str(R / 'reader-method-v11/validation.json'),
    'generic_code_coordinator_approval_claimed': False,
    'new_protocol_limit': 'Readers still choose and interpret passages themselves; no question map, failed IDs, keys, old responses or expected facts are provided.',
    'sha256': {str(p): sha(p) for p in files},
    'no_readers_dispatched_by_this_script': True,
}
(IT / 'input-manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
print('Frozen unchanged167/544 bank; shared process instruction chars', len(instructions))
print((IT / 'reader-a-prompt.txt').read_text())
