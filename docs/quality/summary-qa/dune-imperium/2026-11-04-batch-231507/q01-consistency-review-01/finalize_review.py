from pathlib import Path
import datetime, hashlib, json, re

D = Path(__file__).resolve().parent
P = D.parent
R = Path('/home/jonny/projects/boardgame-rules')
B = P.parents[1]/'batches/2026-11-04-batch-231507'
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
acceptance_path = B/'dune-imperium-q01-consistency-coordinator-review.json'
runtime_path = B/'dune-imperium-q01-consistency-runtime-check.json'
acceptance = read(acceptance_path)
runtime = read(runtime_path)
adjudication = read(D/'adjudication.json')
inputs = read(D/'input-manifest.json')
fingerprints = read(D/'original-evidence-fingerprints.json')
checks = {
    'coordinator_accepts': acceptance['coordinator_decision'].startswith('Accepted:'),
    'completion_hold_resolved': acceptance['completion_hold_resolved'],
    'exact_adjudication_accepted': acceptance['adjudication_sha256'] == sha(D/'adjudication.json'),
    'exact_canonical_accepted': acceptance['canonical_sha256'] == sha(R/'rules/dune-imperium.md') == sha(D/'summary-snapshot.md'),
    'both_answers_remain_correct': len(adjudication['response_judgments']) == 2 and all(x['grade']=='correct' for x in adjudication['response_judgments']),
    'no_confirmed_material_defect': not adjudication['material_omissions_or_contradictions'],
    'all_review_inputs_unchanged': all(sha(Path(path))==value for path,value in inputs.items()),
    'all_original_raw_key_question_summary_unchanged': all(sha(Path(path))==value for path,value in fingerprints['sha256'].items()),
    'original_grades_unchanged': sha(P/'expanded-iteration-05/results.json') == fingerprints['old_grades_sha256'],
    'existing_exact_source_audit_unchanged': sha(P/'source-audit-final-05/source-audit.json') == fingerprints['existing_exact_source_audit_sha256'],
    'actual_input_read_audit_pass': read(D/'input-read-audit.json')['status']=='PASS',
    'one_fresh_sol_high_fork_none': len(runtime['agents'])==1 and runtime['agents'][0]['task']=='q01_consistency_01' and runtime['agents'][0]['parent_spawn']['fork_turns']=='none' and all(x['model']=='gpt-6.1-sol' and x['effort']=='high' for x in runtime['agents'][0]['actual_contexts']),
    'coordinator_read_boundary_verified': acceptance['actual_runtime_model_fork_and_inputs_verified'] and acceptance['all_summary_lines_and_full_raw_cases_visible'] and acceptance['source_images_returned']==2,
    'no_new_reader_or_source_audit_required': not acceptance['new_reader_or_source_audit_required'],
    'existing_integration_validation_pass': read(P/'integration-validation.json')['status']=='PASS' and read(P/'integration-validation.json')['canonical_sha256']==sha(R/'rules/dune-imperium.md'),
}
assert all(checks.values()), checks
report = {
    'status':'complete',
    'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'checks':checks,
    'coordinator_acceptance_path':str(acceptance_path),
    'coordinator_runtime_proof_path':str(runtime_path),
    'coordinator_proof_sha256':{str(x):sha(x) for x in [acceptance_path,runtime_path]},
    'canonical_sha256':sha(R/'rules/dune-imperium.md'),
    'material_defect_confirmed':False,
    'grade_correction_required':False,
    'repeat_full_bank_or_source_audit_required':False,
    'remaining_requirements':[],
}
(D/'completion-validation.json').write_text(json.dumps(report,indent=2)+'\n')
if not (D/'pending-acceptance-README.md').exists():
    (D/'pending-acceptance-README.md').write_bytes((P/'README.md').read_bytes())
    (D/'under-review-game-status.json').write_bytes((P/'game-status.json').read_bytes())
review = read(D/'review-status.json')
review.update(status='complete',coordinator_acceptance='accepted',coordinator_acceptance_path=str(acceptance_path),coordinator_runtime_proof_path=str(runtime_path),qa_completion_hold_resolved=True,updated_at_utc=report['checked_at_utc'])
(D/'review-status.json').write_text(json.dumps(review,indent=2)+'\n')
s = read(D/'before-game-status.json')
s.update(status='complete',phase='coordinator-integration-and-q01-consistency-validated',qa_completion_under_review=False,blocking_reason=None,consistency_review_path=str(D),q01_consistency_review=review)
(P/'game-status.json').write_text(json.dumps(s,indent=2)+'\n')
section = '''## Q01 consistency challenge — resolved

One new Sol/high adjudicator with `fork_turns=none` reviewed only the frozen Q01 question/key, both complete same-response answer/evidence records, exact tested summary and authoritative original rulebook. It found both responses correct, and the coordinator accepted that decision after independently checking actual runtime settings and complete visible inputs.

The fixed question explicitly asks for top-to-bottom construction and unused-card disposal. Both responses supply separate tier shuffling, 1 random I above 5 random II above all 4 shuffled III, and unused cards returned unseen to the box. Ten cards is a necessary consequence of those quantities. Face-down placement remains a true source requirement that both responses omit; it was recorded as outside this fixed composition/disposal question scope, not inferred from either answer or added to the grading requirements after testing. No volunteered contradiction was found.

The [review report](q01-consistency-review-01/README.md), [independent adjudication](q01-consistency-review-01/adjudication.json), [completion checks](q01-consistency-review-01/completion-validation.json), [coordinator acceptance](../../batches/2026-11-04-batch-231507/dune-imperium-q01-consistency-coordinator-review.json) and [coordinator runtime check](../../batches/2026-11-04-batch-231507/dune-imperium-q01-consistency-runtime-check.json) resolve the completion hold. Canonical summary, benchmark, raw answers, grades, source audit and integration evidence are unchanged. No repeat reader pair, audit, recording, stamp or publication was required.

'''
base = (D/'before-README.md').read_text()
assert '## Validation and integration' in base
(P/'README.md').write_text(base.replace('## Validation and integration',section+'## Validation and integration',1))
r = (D/'README.md').read_text().replace('# Q01 consistency review — both responses correct, acceptance pending','# Q01 consistency review — both responses correct, accepted')
r = r.replace('**Coordinator acceptance is pending.** The full QA completion claim remains under review, and the new persistent goal remains active.', '**Coordinator accepted the scope decision.** The completion hold is resolved; [acceptance](../../../batches/2026-11-04-batch-231507/dune-imperium-q01-consistency-coordinator-review.json), [runtime verification](../../../batches/2026-11-04-batch-231507/dune-imperium-q01-consistency-runtime-check.json) and [completion validation](completion-validation.json) preserve that evidence. The full QA completion status is restored without changing any tested input or grade.')
(D/'README.md').write_text(r)
files = sorted(x for x in P.rglob('*') if x.is_file() and x.name!='evidence-index.md')
(P/'evidence-index.md').write_text('# Evidence inventory\n\n'+''.join(f'- [{x.relative_to(P)}]({x.relative_to(P).as_posix()})\n' for x in files))
for file in [P/'README.md',D/'README.md',P/'evidence-index.md']:
    for target in re.findall(r'\]\(([^)]+)\)',file.read_text()):
        if not target.startswith(('http','/','#')):
            assert (file.parent/target.split('#')[0]).exists(), (file,target)
assert len(s['iterations']) == s['executed_iteration_count'] == 9
assert s['source_audit']['checked_claim_groups'] == 36
print(json.dumps({'status':'complete','checks':checks,'canonical_sha256':report['canonical_sha256']},indent=2))
