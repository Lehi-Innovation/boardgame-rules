"""Approve only a fully evidenced Root candidate; publication is a separate gate."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import Counter
import argparse
import hashlib
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--iteration', required=True)
parser.add_argument('--runtime-proof', required=True)
parser.add_argument('--phase', choices=['pre-stamp', 'complete'], required=True)
args = parser.parse_args()
base = Path(__file__).parent
root = base.parents[4]
run = root / 'docs/quality/summary-qa/root' / base.name
iteration = run / args.iteration
assert iteration.parent == run
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sys.path.insert(0, str(root))
from scripts.validate import validate_rules_file

manifest = read(base / 'manifest.json')
game = next(x for x in manifest['games'] if x['slug'] == 'root')
assert game.get('coordinator_source_gap', {}).get('status') != 'open'
frozen = read(iteration / 'input-manifest.json')
benchmark = run / frozen['benchmark']
questions = read(iteration / 'questions.json')['questions']
key = read(benchmark / 'answer-key.json')['answers']
assert questions == read(benchmark / 'questions.json')['questions']
ids = [x['id'] for x in questions]
n = len(ids)
assert n >= 20 and len(set(ids)) == n and ids == [x['id'] for x in key]
question_by_id = {x['id']: x for x in questions}
key_by_id = {x['id']: x for x in key}
hash_checks = []

def verify_hashes(values):
    if isinstance(values, list):
        normalized = {entry['path']: entry['sha256'] for entry in values}
        assert len(normalized) == len(values)
        values = normalized
    for filename, expected in values.items():
        path = Path(filename)
        if not path.is_absolute():
            path = root / path
        expected_hash = expected['sha256'] if isinstance(expected, dict) else expected
        assert sha(path) == expected_hash, filename
        hash_checks.append(str(path))

initial = read(run / 'input-manifest.json')['hashes']
for filename, expected in initial.items():
    path = run / 'baseline-summary.md' if filename.endswith('/rules/root.md') else Path(filename)
    assert sha(path) == expected, filename

previous_questions = previous_key = None
for bank in sorted(run.glob('benchmark-v*'), key=lambda p: int(p.name.split('-v')[-1])):
    q = read(bank / 'questions.json')['questions']
    k = read(bank / 'answer-key.json')['answers']
    assert len(q) == len(k) == len({x['id'] for x in q})
    assert [x['id'] for x in q] == [x['id'] for x in k]
    if previous_questions is not None:
        assert q[:len(previous_questions)] == previous_questions
        changed = {old['id']: (old, new) for old, new in zip(previous_key, k) if old != new}
        corrections_path = bank / 'key-corrections.json'
        declared = {x['id']: x for x in read(corrections_path)['corrections']} if corrections_path.exists() else {}
        assert set(changed) == set(declared), bank
        for ident, (old, new) in changed.items():
            assert old == declared[ident]['old_entry'] and new == declared[ident]['new_entry']
            assert declared[ident]['source_references']
            assert (bank / declared[ident]['independent_evidence'].split('#')[0]).resolve().exists()
    verify_hashes(read(bank / 'input-manifest.json')['hashes'])
    previous_questions, previous_key = q, k

verify_hashes(frozen['hashes'])
verify_hashes(frozen['prompt_hashes'])
results = read(iteration / 'results.json')
independent_path = iteration / 'independent-grades.json'
independent_grades = read(independent_path) if independent_path.exists() else None
if independent_grades and isinstance(independent_grades.get('readers'), dict):
    verify_hashes(independent_grades['input_hashes'])
scores = {}
for who in ['a', 'b']:
    raw = read(iteration / ('reader-' + who + '.json'))['answers']
    answers = {x['id']: x for x in raw}
    grades = results[who]['grades']
    if independent_grades and 'reader-' + who in independent_grades.get('readers', {}):
        original = independent_grades['readers']['reader-' + who]
        original_by_id = {entry['id']: entry for entry in original['grades']}
        assert Counter(entry['id'] for entry in original['grades']) == Counter(ids)
        assert original['totals'] == {'correct': n, 'partial': 0, 'incorrect': 0}
        assert all(grade[field] == original_by_id[grade['id']][field] for grade in grades for field in ['grade', 'reason', 'unsupported_guess', 'requested_fact_checklist'])
    assert Counter(x['id'] for x in raw) == Counter(ids)
    assert Counter(x['id'] for x in grades) == Counter(ids)
    for grade in grades:
        ident = grade['id']
        assert grade['observed'] == answers[ident]
        assert grade['question'] == question_by_id[ident]['question']
        assert grade['expected_answer'] == key_by_id[ident]['expected_answer']
        assert grade['grade'] == 'correct' and grade['unsupported_guess'] is False
        assert grade.get('requested_fact_checklist')
        assert all(x['status'] in ['satisfied', 'resolved', 'context_not_requested', 'context-not-requested', 'satisfied/resolved', 'contextual not_requested'] for x in grade['requested_fact_checklist'])
    assert results[who]['totals'] == {'correct': n, 'partial': 0, 'incorrect': 0}
    scores[who] = {**results[who]['totals'], 'unresolved': 0, 'unsupported_guesses': 0}
    delivery = read(iteration / ('reader-' + who + '-delivery-audit.json'))
    assert delivery['line_coverage_status'] == 'ALL_NONEMPTY_INPUT_LINES_DELIVERED'
    assert delivery['read_calls'] and delivery['inputs']

prompt_a = (iteration / 'reader-a-prompt.txt').read_text().replace('/reader-a.json', '/reader-{reader}.json')
prompt_b = (iteration / 'reader-b-prompt.txt').read_text().replace('/reader-b.json', '/reader-{reader}.json')
assert prompt_a == prompt_b
models = read(Path(args.runtime_proof))
assert models['verified'] and models['slug'] == 'root' and models['game_chat_id'] == game['thread_id']
reader_ids = {x['session_id'] for x in read(iteration / 'model-provenance.json')['readers']}
assert len(reader_ids) == 2 and reader_ids == {x['session_id'] for x in models['records'] if x['role'] == 'reader'}
auditors = [x for x in models['records'] if x['role'] == 'source-auditor']
assert len(auditors) == 1

canonical = root / 'rules/root.md'
assert canonical.read_bytes() == (iteration / 'summary-snapshot.md').read_bytes()
audit_path = iteration / 'source-audit.json'
audit = read(audit_path)
assert audit['verdict'] == 'PASS' and not audit['findings']
assert auditors[0]['identity']['agent_path'].endswith('/' + audit['auditor'])
if 'input_hashes' in audit:
    audit_hashes = audit['input_hashes']
else:
    assert audit['inputs'] and audit['final_input_hash_check']
    audit_hashes = {entry['path']: entry['sha256'] for entry in audit['inputs']}
    assert audit_hashes == audit['final_input_hash_check']
    assert not audit['material_unresolved_findings']
source_delivery_path = iteration / 'source-auditor-delivery-audit.json'
if source_delivery_path.exists():
    source_delivery = read(source_delivery_path)
    assert source_delivery['line_coverage_status'] == 'ALL_SOURCE_AND_SUMMARY_NONEMPTY_LINES_DELIVERED'
    assert source_delivery['inputs'] and source_delivery['read_calls']
    assert all(entry['all_nonempty_lines_in_ordered_exact_blocks'] and not entry['unmatched_nonempty_lines_in_ordered_blocks'] for entry in source_delivery['inputs'])
    assert source_delivery['image_delivery_validation']['passed']
    assert source_delivery['completed_source_audit']['sha256'] == sha(Path(source_delivery['completed_source_audit']['path'])) == sha(audit_path)
verify_hashes(audit_hashes)
assert sha(canonical) in json.dumps(audit_hashes)
for path in game['source_paths']:
    assert sha(Path(path)) in json.dumps(audit_hashes)

coverage = read(run / 'coverage-status.json')
assert coverage['verdict'] == 'PASS' and coverage['bank'] == frozen['benchmark'] and coverage['question_count'] == n
verify_hashes(coverage['hashes'])
ledger = read(run / 'coverage-ledger.json')
assert all(x['count'] == 0 and x['all_core_procedural_passages_mapped'] for x in ledger['passes'][-2:])
assert len(ledger['passes']) >= 2 and all(x['questions'] for x in ledger['coverage_map'])
review = read(run / 'coverage-review.json')
assert review.get('verdict', review.get('status')) == 'PASS'
for path in [benchmark / 'questions.json', benchmark / 'answer-key.json', run / 'coverage-ledger.json']:
    assert sha(path) in json.dumps(review)
validation = read(run / 'validation.json')
assert validation['status'] == 'PASS' and validation['passed'] == validation['total'] and all(x['pass'] for x in validation['checks'])
assert not validate_rules_file(str(canonical))

if args.iteration == 'expanded-iteration-10':
    assert read(iteration / 'q04-fresh-adjudication.json')['decision'] == 'correct'
    assert (iteration / 'results-before-q04-fresh-adjudication.json').exists()
    quotation = read(iteration / 'quotation-disposition-independent.json')
    assert quotation['total_reviewed_count'] == 18 and quotation['material_findings_count'] == quotation['unresolved_count'] == 0
    assert read(iteration / 'quotation-review-validation.json')['status'] == 'PASS'

approvals_path = base / 'coordinator-approvals.json'
old_approvals = approvals_path.read_text()
approvals = json.loads(old_approvals)
prior = approvals.get('root')
if args.phase == 'complete' and prior and prior.get('phase') == 'pre-stamp':
    if prior['summary_sha256'] != sha(canonical):
        assert not reader_ids.intersection(prior['reader_session_ids'])
    assert auditors[0]['session_id'] != prior['source_auditor_session_id']
now = datetime.now(ZoneInfo('America/Phoenix'))
report = {'game': 'Root', 'checked_at': now.isoformat(), 'approved': True, 'phase': args.phase, 'question_count': n, 'final_reader_scores': scores, 'summary_sha256': sha(canonical), 'final_snapshot_path': str(iteration / 'summary-snapshot.md'), 'source_audit_verdict': 'PASS', 'source_audit_path': str(audit_path), 'reader_session_ids': sorted(reader_ids), 'source_auditor_session_id': auditors[0]['session_id'], 'independent_runtime_proof': args.runtime_proof, 'historical_questions_preserved_and_key_changes_explicitly_versioned': True, 'final_ids_once_and_grade_raw_key_correspondence_verified': True, 'complete_reader_input_delivery_checked': True, 'same_saved_reader_instructions_except_output_path': True, 'coverage_stopping_and_independent_challenge_inspected': True, 'novelty_accounting': coverage['novelty'], 'worker_integrity_checks_passed': validation['total'], 'canonical_equals_final_snapshot': True, 'structural_validation_passed': True, 'frozen_hash_checks': len(hash_checks), 'publication_gate': 'Sequential source-audit recording, stamping, targeted catalog update and stamp-byte verification remain coordinator actions.'}
out = base / 'coordinator-checks' / ('root-' + args.phase + '-' + now.strftime('%Y%m%dT%H%M%S%f') + '.json')
out.write_text(json.dumps(report, indent=2) + '\n')
report['coordinator_validation_path'] = str(out)
approvals['root'] = report
assert approvals_path.read_text() == old_approvals
approvals_path.write_text(json.dumps(approvals, indent=2) + '\n')
print(json.dumps({'approved': True, 'phase': args.phase, 'questions': n, 'scores': scores, 'summary_sha256': report['summary_sha256'], 'report': str(out)}))
