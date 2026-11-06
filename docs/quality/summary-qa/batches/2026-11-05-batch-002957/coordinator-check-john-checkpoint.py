"""Verify the preserved incomplete checkpoint without authorizing publication."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

base = Path(__file__).resolve().parent
repo = base.parents[4]
game = repo / 'docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957'
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
checkpoint = read(game / 'checkpoint.json')
iteration = Path(checkpoint['checkpoint_snapshot_path']).parent
checks = {}
checks['canonical_matches_checkpoint_snapshot'] = sha(repo / 'rules/john-company-second-edition.md') == sha(Path(checkpoint['checkpoint_snapshot_path'])) == checkpoint['hashes']['canonical_and_checkpoint_and_audit12']
inputs = read(iteration / 'input-manifest.json')['inputs']
checks['all_frozen_inputs_unchanged'] = all(sha(Path(p)) == h for p, h in inputs.items())
immutable = read(game / 'checkpoint-immutable-artifact-hashes.json')['hashes']
checks['all_immutable_artifacts_unchanged'] = all(sha(game / p) == h for p, h in immutable.items())
questions = read(iteration / 'questions.json')['questions']
key = read(iteration.parent / 'answer-key.json')['answers']
qmap = {x['id']: x for x in questions}
kmap = {x['id']: x for x in key}
checks['bank_has_all_87_unique_questions_and_keys'] = len(qmap) == len(questions) == len(kmap) == len(key) == 87 and qmap.keys() == kmap.keys()
results = read(iteration / 'results.json')
scores = {}
for reader in ['a', 'b']:
    name = f'reader-{reader}'
    raw = read(iteration / f'{name}.json')['answers']
    grades = read(iteration / f'grades-{name}.json')['grades']
    enriched = results['readers'][name]['grades']
    rawmap = {x['id']: x for x in raw}
    checks[f'{name}_exact_complete_ids'] = len(raw) == len(rawmap) == len(grades) == len(enriched) == 87 and rawmap.keys() == qmap.keys() == {x['id'] for x in grades} == {x['id'] for x in enriched}
    counts = {g: sum(x['grade'] == g for x in grades) for g in ['Correct', 'Partial', 'Incorrect']}
    scores[name] = counts
    checks[f'{name}_scores_86_correct_1_partial'] = counts == {'Correct': 86, 'Partial': 1, 'Incorrect': 0} and [x['id'] for x in grades if x['grade'] != 'Correct'] == ['Q015']
    checks[f'{name}_enriched_observations_match_raw_and_key'] = all(x['observed_answer'] == rawmap[x['id']]['answer'] and x['question'] == qmap[x['id']]['question'] and x['expected_answer'] == kmap[x['id']]['expected_answer'] for x in enriched)
    checks[f'{name}_no_unsupported_correct_guesses'] = not any(x.get('unsupported_correct_guess') for x in enriched)
delivery = read(iteration / 'input-delivery-validation.json')
checks['both_complete_nontruncated_input_deliveries'] = all(delivery[x]['complete_input_delivery_confirmed'] and delivery[x]['truncated_responses'] == 0 and not delivery[x]['nonblank_summary_lines_not_visible'] and not delivery[x]['question_texts_not_visible'] for x in ['a', 'b'])
audit = read(game / 'source-audit-12/source-audit.json')
checks['source_audit_is_major_on_exact_checkpoint'] = audit['verdict'] == 'MAJOR' and audit['complete_core_signoff'] is False and audit['known_sourced_claims_verdict'] == 'PASS' and audit['summary_sha256'] == sha(Path(checkpoint['checkpoint_snapshot_path']))
checks['coverage_remains_open'] = checkpoint['coverage']['final_coverage_closed'] is False
blocking = read(game / 'goal-blocking-audit.json')
checks['actual_three_turn_goal_block_confirmed'] = blocking['goal_status_returned'] == 'blocked' and blocking['consecutive_turns_with_same_source_dependency'] >= 3 and blocking['three_consecutive_goal_turn_threshold_established']
runtime = sorted((base / 'coordinator-runtime-model-checks').glob('john-company-second-edition-blocked-checkpoint-*.json'))[-1]
runtime_data = read(runtime)
checks['independent_actual_model_check_passed'] = runtime_data.get('verified') is True
checks['worker_checkpoint_validation_has_no_failures'] = read(game / 'checkpoint-validation.json')['failures'] == []
findings = read(game / 'checkpoint-findings.json')
checks['known_reader_omissions_retained_separately_from_source_gap'] = findings['reader_a']['kind'] == 'source_gap_only' and findings['reader_b']['kind'] == 'source_gap_plus_reader_omissions' and len(findings['reader_b']['omitted_known_facts']) == 2
checks['unverified_unpublished_incomplete'] = checkpoint['ready_for_verification_or_publication'] is False and checkpoint['complete_core_PASS'] is False and checkpoint['formal_bank_PASS'] is False and checkpoint['publication_or_stamping_performed'] is False
report = {
    'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'checkpoint_integrity_verified': all(checks.values()),
    'approved_for_publication': False,
    'complete_core_PASS': False,
    'source_audit_verdict': 'MAJOR',
    'status': 'awaiting-external-input',
    'question_count': 87,
    'iterations_preserved': 20,
    'reader_scores': scores,
    'checks': checks,
    'immutable_artifacts_checked': len(immutable),
    'runtime_model_proof': str(runtime),
    'checkpoint': str(game / 'checkpoint.json'),
    'remaining_findings': str(game / 'checkpoint-findings.json'),
    'external_input_needed': 'Verified publisher/designer ruling on strength-2 local alliance defending strength-1 Crisis, including exhaustion, success and excess-strength counting.',
    'reader_b_known_omissions': 'Q015 omits the printed non-equality result and alliance contribution constraints, and does not acknowledge unresolved excess counting. These remain Partial; they are not excused by the authority gap.'
}
target = base / 'coordinator-checks/john-company-second-edition-blocked-checkpoint.json'
target.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'integrity_verified': report['checkpoint_integrity_verified'], 'approved_for_publication': False, 'failed_checks': [k for k, v in checks.items() if not v], 'report': str(target)}))
assert report['checkpoint_integrity_verified']
