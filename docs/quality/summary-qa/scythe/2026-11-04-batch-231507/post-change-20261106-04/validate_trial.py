from pathlib import Path
import datetime
import hashlib
import json
import re
import subprocess

D = Path(__file__).resolve().parent
P = D.parent
ROOT = P.parents[4]
ONE = P / 'post-change-20261106-01'
read = lambda p: json.loads(Path(p).read_text())
h = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
checks = {}
manifest = read(D / 'input-manifest.json')
sha = h(D / 'summary-snapshot.md')
checks['canonical_exact_frozen_bytes'] = h(ROOT / 'rules/scythe.md') == sha == manifest['summary_sha256']
before_clarity = (P / 'post-change-20261106-03/before-clarity-summary.md').read_bytes()
current_summary = (D / 'summary-snapshot.md').read_bytes()
checks['resumed_metadata_preserved_by_clarity_repair'] = before_clarity.split(b'---', 2)[:2] == current_summary.split(b'---', 2)[:2]
banner = lambda b: b.split(b'<!-- verification:begin -->', 1)[1].split(b'<!-- verification:end -->', 1)[0]
checks['machine_managed_verification_banner_unchanged'] = banner(before_clarity) == banner(current_summary)
checks['all_initial_inputs_and_predeclared_stage_prompts_intact'] = all(h(p) == v['sha256'] for p, v in manifest['inputs'].items())
old = read(ONE / 'historical-preservation-manifest.json')['sha256']
checks['all_385_historical_files_preserved'] = len(old) == 385 and all((P / p).exists() and h(P / p) == v for p, v in old.items())
prior = read(D / 'prior-post-change-trial-manifest.json')['files']
checks['all_prior_postchange_files_preserved'] = all(Path(p).exists() and h(p) == v['sha256'] for p, v in prior.items())
checks['all_later_trial03_supplements_preserved'] = all(Path(p).exists() and h(p) == v['sha256'] for p, v in read(D / 'prior-supplement-preservation.json')['files'].items())
checks['prior_postchange_trials_exact_raw_key_grade_linkage'] = read(D / 'prior-trial-integrity.json')['all_pass']
checks['primary_source_hashes_unchanged'] = all(h(ROOT / p) == v for p, v in read(P / 'input-manifest.json')['hashes'].items() if p.startswith(('extracted/', 'source_pdfs/')))
questions = read(D / 'questions.json')['questions']
key = read(D / 'answer-key.json')['answers']
ids = [q['id'] for q in questions]
checks['all_63_ids_unique_and_key_linked'] = ids == [f'Q{i:02}' for i in range(1, 64)] == [q['id'] for q in key]
checks['full_bank_and_key_byte_unchanged'] = all((D / f).read_bytes() == (P / 'expanded-v9' / f).read_bytes() for f in ['questions.json', 'answer-key.json'])
checks['seed20_objects_unchanged'] = questions[:20] == read(P / 'questions.json')['questions'] and key[:20] == read(P / 'answer-key.json')['answers']
checks['neutral_subsets_exactly_partition_full_bank'] = all(read(D / f'questions-part-{i}.json')['questions'] == questions[(i - 1) * 21:i * 21] for i in range(1, 4))
checks['grading_policy_byte_unchanged'] = (D / 'grading-policy.md').read_bytes() == (ONE / 'grading-policy.md').read_bytes()
plan = read(D / 'protocol-plan.json')
checks['protocol_declared_four_stages_and_unconditional_review'] = plan['protocol_version'] == 'generic-small-batch-v5' and plan['stages'] == 4 and plan['declared_before_any_reader_output']
config = read(D / 'dispatch-records.json')['agents']
config.update(read(D / 'grader-dispatch-records.json')['agents'])
checks['fresh_grader_prompts_unchanged'] = all(h(p) == v['sha256'] for p, v in read(D / 'grader-prompt-manifest.json')['inputs'].items())
provenance = read(D / 'model-provenance-final.json')
checks['all_actual_models_high_and_original_forknone'] = provenance['actual_required_settings_verified'] and set(config) == set(provenance['agents'])
for role, record in provenance['agents'].items():
    request = config[role]
    spawn = provenance['parent_spawn_proof'][role]
    expected_turns = 4 if role.endswith(('_04_a', '_04_b')) else 1
    checks['all_actual_models_high_and_original_forknone'] &= len(record['contexts']) == expected_turns and all(c['model'] == request['model'] and c['effort'] == 'high' for c in record['contexts']) and spawn['fork_turns'] == 'none' and spawn['model'] == request['model'] and spawn['reasoning_effort'] == 'high'
checks['stage_prompts_frozen_before_first_reader_start'] = all(datetime.datetime.fromisoformat(manifest['created_at_utc']) <= datetime.datetime.fromisoformat(provenance['agents'][role]['started'].replace('Z', '+00:00')) for role in config if role.endswith(('_04_a', '_04_b')))
checks['all_planned_stage_messages_equivalent_between_readers'] = all((D / f'reader-a-stage-{i}-prompt.txt').read_text() == (D / f'reader-b-stage-{i}-prompt.txt').read_text().replace('reader-b', 'reader-a') for i in range(1, 5))
checks['reader_and_grader_settings_confirmed_early'] = read(D / 'model-provenance-early-confirmed.json')['actual_required_settings_verified'] and read(D / 'model-provenance-graders-early-confirmed.json')['actual_required_settings_verified']
checks['parent_inspected_all_runtime_tool_boundaries'] = read(D / 'isolation-review.json')['all_required_boundaries_pass']
results = read(D / 'results.json')
checks['final_readers_and_grader_prompts_preserved_since_pregrading_freeze'] = all(h(p) == v['sha256'] for p, v in read(D / 'final-reader-pregrading-manifest.json')['inputs'].items())
for side in ['a', 'b']:
    raw = read(D / f'reader-{side}.json')['answers']
    ai = {a['id']: a for a in raw}
    grader = read(D / f'grader-{side}.json')
    grade_hashes = grader.get('input_hashes', grader.get('input_hashes_sha256'))
    checks[f'{side}_all_seven_grader_inputs_initial_final_hashes_match'] = len(grade_hashes) == 7 and all(h(p) == v['initial'] == v['final'] for p, v in grade_hashes.items())
    grades = grader['grades']
    gi = {g['id']: g for g in grades}
    checks[f'{side}_raw_and_grades_all63_unique'] = len(raw) == len(ai) == len(grades) == len(gi) == 63 and set(ai) == set(gi) == set(ids)
    checks[f'{side}_exact_question_key_raw_linkage'] = all(gi[q['id']].get('question', gi[q['id']].get('literal_question')) == q['question'] and gi[q['id']]['expected_answer'] == k['expected_answer'] and gi[q['id']]['source_references'] == k['source_references'] and gi[q['id']]['observed_answer'] == ai[q['id']]['answer'] and gi[q['id']]['reader_evidence'] == ai[q['id']]['evidence'] for q, k in zip(questions, key))
    counts = {kind: sum(g['grade'] == kind for g in grades) for kind in ['correct', 'partial', 'incorrect']}
    checks[f'{side}_totals_match_grades_and_export'] = counts == grader['totals'] == results['readers'][side]['totals']
    checks[f'{side}_complete_pass_without_guesses'] = counts == {'correct': 63, 'partial': 0, 'incorrect': 0} and all(not g['unsupported_guess'] for g in grades)
    checks[f'{side}_all_checkpoints_preserved'] = True
    for stage in range(1, 5):
        checkpoint = read(D / f'reader-{side}-stage-{stage}-checkpoint.json')
        checks[f'{side}_all_checkpoints_preserved'] &= all(h(p) == v['sha256'] for p, v in checkpoint['inputs'].items()) and all(checkpoint['checks'].values())
    for stage in [2, 3]:
        previous = read(D / f'reader-{side}-draft-{stage-1}.json')['answers']
        current = read(D / f'reader-{side}-draft-{stage}.json')['answers']
        checks[f'{side}_all_checkpoints_preserved'] &= current[:len(previous)] == previous
    draft = read(D / f'reader-{side}-draft-3.json')['answers']
    changed = [{'id': a['id'], 'draft': a, 'final': b} for a, b in zip(draft, raw) if a != b]
    checks[f'{side}_review_changes_record_exact'] = changed == read(D / f'reader-{side}-review-changes.json')['changes']
reuse = read(D / 'source-audit-reuse.json')
audit = read(reuse['fresh_report'])
checks['fresh_source03_report_unchanged'] = h(reuse['fresh_report']) == reuse['report_sha256']
checks['exact_current_source_audit_PASS_no_findings'] = audit['verdict'] == 'PASS' and not audit['material_findings'] and not audit['important_omission_assessment']['important_omissions_found'] and all(h(v['path']) == v['sha256_initial'] == v['sha256_before_report_creation'] for v in audit['inputs']) and sha == reuse['summary_sha256']
source_proof = read(P / 'post-change-20261106-03/model-provenance-final.json')
checks['fresh_source_auditor_actual_required_settings'] = source_proof['checks']['postchange_20261106_03_source']
coverage = read(P / 'coverage-review-08.json')
ledger = read(P / 'coverage-ledger.json')
checks['coverage_stopping_evidence_unchanged'] = coverage['verdict'] == 'PASS' and not coverage['proposed_additions'] and [v['pass'] for v in ledger['passes'][-2:]] == [23, 24] and all(not v['accepted'] for v in ledger['passes'][-2:])
watch = read(ONE / 'input-watch-state.json')
age = (datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(watch['at_utc'])).total_seconds()
checks['live_watch_recent_and_stable'] = age < 60 and watch['content_stable']
events = [json.loads(line) for line in (ONE / 'input-watch-events.jsonl').read_text().splitlines()]
authorized = [e for e in events if e.get('event') == 'authorized-clarity-repair']
checks['no_unexplained_observed_content_changes'] = all(any(a['path'] == name and a['from_sha256'] == change['expected']['sha256'] and a['to_sha256'] == change['actual'].get('sha256') for a in authorized) for e in events for name, change in e.get('content_changes', {}).items())
commands = []
for command in [['.venv/bin/python', '-m', 'scripts.validate', 'rules/scythe.md'], ['git', 'diff', '--check', '--', 'rules/scythe.md', str(P.relative_to(ROOT))]]:
    done = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    commands.append({'command': command, 'exit_code': done.returncode, 'stdout': done.stdout, 'stderr': done.stderr})
checks['target_structural_and_scoped_diff_checks'] = all(c['exit_code'] == 0 for c in commands)
links = []
for document in [P / 'README.md', D / 'README.md']:
    if not document.exists():
        continue
    for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
        if target.startswith(('https:', 'http:', '#')):
            continue
        path = target.split('#')[0]
        links.append({'document': str(document), 'target': target, 'exists': (document.parent / path).exists()})
checks['report_local_links_resolve'] = bool(links) and all(l['exists'] for l in links)
out = {'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'all_pass': all(checks.values()), 'checks': checks, 'final_summary_sha256': sha, 'scores': {s: results['readers'][s]['totals'] for s in ['a', 'b']}, 'commands': commands, 'report_links': links, 'scope': 'Local exact-byte QA; coordinator audit recording, stamping and targeted publication acceptance remain. Any canonical byte change requires new exact-byte evidence.'}
destination = D / 'validation.json'
assert not destination.exists(), destination
destination.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
assert out['all_pass']
