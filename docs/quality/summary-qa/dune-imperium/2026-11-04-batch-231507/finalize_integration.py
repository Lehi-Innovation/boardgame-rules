from pathlib import Path
import datetime, hashlib, json, re, subprocess, sys
import yaml

P = Path(__file__).resolve().parent
R = Path('/home/jonny/projects/boardgame-rules')
B = R / 'docs/quality/summary-qa/batches/2026-11-04-batch-231507'
REC = B / 'recording/dune-imperium-20261105-070246'
PUB = B / 'publication/20261105-070303'
REG = B / 'registry/dune-imperium-20261105-070304'
D = P / 'expanded-iteration-05'
A = P / 'source-audit-final-05'
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
checks = {}
def require(name, value):
    checks[name] = bool(value)
    assert value, name

def entry(doc):
    matches = [g for g in doc['games'] if g.get('slug') == 'dune-imperium']
    assert len(matches) == 1
    return matches[0]

def row(path):
    rows = [x for x in path.read_text().splitlines() if '](rules/dune-imperium/)' in x]
    assert len(rows) == 1
    return rows[0]

run = subprocess.run([sys.executable, str(P/'validate_evidence.py'), D.name, A.name], cwd=R, text=True, capture_output=True)
require('full_local_evidence_validation', run.returncode == 0 and read(P/'validation.json')['status'] == 'PASS')
sys.path.insert(0, str(R))
from scripts.catalog import validate_catalog
catalog_errors = validate_catalog(R)
require('current_global_catalog_errors_empty', not catalog_errors)
coordinator = read(B/'dune-imperium-coordinator-validation.json')
recording = read(REC/'validation.json')
publication = read(PUB/'validation.json')
mechanical = read(B/'dune-imperium-expanded05-coordinator-iteration-check.json')
semantic = read(B/'dune-imperium-expanded05-root-preliminary-review.json')
runtime = read(B/'dune-imperium-expanded05-runtime-check.json')
require('coordinator_exact_summary', coordinator['canonical_sha256'] == sha(R/'rules/dune-imperium.md') == sha(D/'summary-snapshot.md') == sha(A/'summary-snapshot.md'))
require('stamping_byte_idempotent', not recording['stamping_changed_tested_bytes'] and not recording['requires_full_bank_retest'] and not coordinator['stamping_changed_tested_bytes'] and all(sha(x) == sha(D/'summary-snapshot.md') for x in [REC/'summary-before.md', REC/'summary-after.md']))
require('recording_preserved_unrelated_audits', recording['unrelated_audit_verdicts_preserved'] and recording['global_audit_manifest_unchanged'])
require('current_audit_record_matches', yaml.safe_load((R/'docs/quality/semantic-audit-results.yaml').read_text())['dune-imperium'] == recording['recorded_verdict'])
require('publication_flags_pass', all(publication[k] for k in ['non_selected_index_lines_preserved','non_selected_manifest_entries_preserved','selected_manifest_entries_match_regeneration','selected_index_rows_match_regeneration']))
before, targeted, regenerated = [read(PUB/n) for n in ['before-games.json','targeted-games.json','regenerated-games.json']]
require('unrelated_manifest_entries_preserved', [x for x in before['games'] if x['slug'] != 'dune-imperium'] == [x for x in targeted['games'] if x['slug'] != 'dune-imperium'])
require('unrelated_index_rows_preserved', [x for x in (PUB/'before-index.md').read_text().splitlines() if '](rules/dune-imperium/)' not in x] == [x for x in (PUB/'targeted-index.md').read_text().splitlines() if '](rules/dune-imperium/)' not in x])
require('current_target_manifest_matches_regeneration', entry(read(R/'games.json')) == entry(targeted) == entry(regenerated))
require('current_target_index_matches_regeneration', row(R/'index.md') == row(PUB/'targeted-index.md') == row(PUB/'regenerated-index.md'))
registry = [g for g in yaml.safe_load((R/'games.yaml').read_text())['games'] if g['bgg_id'] == 316554]
require('current_registry_verified_exact_target', len(registry) == 1 and registry[0] == read(REG/'target-after.json') and registry[0]['status'] == 'verified')
require('coordinator_mechanical_checks', mechanical['mechanical_checks_pass'] and all(mechanical['checks'].values()))
require('coordinator_semantic_scores', not semantic['material_findings'] and all(x == {'correct':76,'partial':0,'incorrect':0,'unsupported_guesses':0} for x in semantic['semantic_scores'].values()))
require('coordinator_actual_runtime_settings', len(runtime['agents']) == 3 and all(a['parent_spawn']['fork_turns'] == 'none' and all(c['model'] == ('gpt-6.1-sol' if a['task'] == 'final_source_audit_05' else 'gpt-6-luna') and c['effort'] == 'high' for c in a['actual_contexts']) for a in runtime['agents']))
coverage, ledger = read(P/'coverage-review-11.json'), read(P/'coverage-ledger.json')
require('coverage_saturated', coverage['verdict'] == 'saturated_within_reviewed_scope' and not coverage.get('findings') and not coverage.get('proposed_questions') and [x['pass'] for x in ledger['passes'][-2:]] == [32,33] and all(not x['accepted_ids'] for x in ledger['passes'][-2:]))
audit = read(A/'source-audit.json')
require('final_source_audit_36_groups', audit['verdict'] == 'PASS' and not audit['findings'] and len(audit['checked_claims']) == 36)
executed = sorted(x.name for x in P.glob('*iteration-*') if (x/'results.json').exists() and all((x/f'reader-{r}.json').exists() for r in 'ab'))
prepared = sorted(x.name for x in P.glob('*iteration-*') if (x/'not-dispatched.json').exists())
require('nine_executed_pairs', len(executed) == 9 and len([x for x in executed if x.startswith('seed')]) == 6 and len([x for x in executed if x.startswith('expanded')]) == 3 and set(executed) == set(coordinator['executed_iterations']))
require('prepared_history_preserved', prepared == ['expanded-iteration-01','expanded-iteration-02'] and all(not (P/x/'results.json').exists() for x in prepared))
proofs = [B/'dune-imperium-coordinator-validation.json', B/'dune-imperium-expanded05-root-preliminary-review.json', B/'dune-imperium-expanded05-runtime-check.json', B/'dune-imperium-expanded05-coordinator-iteration-check.json', REC/'validation.json', PUB/'validation.json', REG/'target-before.json', REG/'target-after.json']
report = {'status':'PASS','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'canonical_sha256':sha(R/'rules/dune-imperium.md'),'executed_iteration_count':9,'executed_iterations':executed,'prepared_not_dispatched':prepared,'source_audit_claim_groups':36,'stamping_changed_tested_bytes':False,'full_bank_retest_required':False,'current_global_catalog_errors':catalog_errors,'coordinator_proof_paths':[str(x) for x in proofs],'coordinator_proof_sha256':{str(x):sha(x) for x in proofs},'local_validation_output':run.stdout,'remaining_requirements':[]}
old = P/'integration-validation.json'
if not (P/'integration-wait-history.json').exists():
    (P/'integration-wait-history.json').write_bytes(old.read_bytes())
old.write_text(json.dumps(report,indent=2)+'\n')
s = read(P/'game-status.json')
s['iteration_directories'] = sorted(set(s['iterations']) | set(executed) | set(prepared))
s['iterations'] = executed
s['executed_iteration_count'] = 9
s['prepared_iterations'] = prepared
s['historical_status_scores'] = {k:s[k] for k in ['last_reader_scores','last_pair_scores'] if k in s}
s.update(status='complete',phase='coordinator-integration-validated',blocking_reason=None,coordinator_integration=report,last_reader_scores=s['final_reader_scores'],last_pair_scores=s['final_reader_scores'])
s['source_audit']['checked_claim_groups'] = 36
(P/'game-status.json').write_text(json.dumps(s,indent=2)+'\n')
text = (P/'README.md').read_text()
text = text.replace('# Dune: Imperium — local summary QA PASS, ready for coordinator','# Dune: Imperium — summary QA and coordinator integration complete')
text = text.replace('A new, final-only gpt-6.1-sol/high source auditor returned **PASS with no findings**', 'A new, final-only gpt-6.1-sol/high source auditor returned **PASS across 36 grouped claim checks, with no findings**')
text = text.replace('Local validation passed. Coordinator audit recording, targeted stamping and final repository integration remain pending; the persistent goal is active. This is not batch completion.', 'Local and coordinator integration validation passed. Audit recording, byte-idempotent stamping, targeted publication and BGG 316554 registry verification are complete. This assigned game is complete; the wider batch is coordinated separately.')
text = text.replace('## Readers, grading and repairs\n', '## Readers, grading and repairs\n\n**Nine reader pairs were executed: six seed pairs and three expanded pairs.** Prepared expanded iterations 01 and 02 were never dispatched and remain preserved separately.\n')
text = text.replace('## Validation and handoff','## Validation and integration')
text = text.replace('No shared registry, global stamp/regeneration, commit, push or branch operation was performed.', 'This worker performed no shared registry, stamp/regeneration, commit, push or branch operation; the coordinator completed the targeted shared integration documented below.')
a = text.index('[Machine status](game-status.json) is `ready-for-coordinator`.')
text = text[:a] + '''[Machine status](game-status.json) is `complete`. The [integration validation](integration-validation.json) confirms the coordinator’s completed recording, byte-idempotent stamp, targeted publication and verified registry entry. Current catalog errors are empty. Canonical, tested, audited, pre-stamp and post-stamp hashes match, so a new reader test was unnecessary.

Actual coordinator evidence: [recording](../../batches/2026-11-04-batch-231507/recording/dune-imperium-20261105-070246/validation.json), [publication](../../batches/2026-11-04-batch-231507/publication/20261105-070303/validation.json), [registry](../../batches/2026-11-04-batch-231507/registry/dune-imperium-20261105-070304/target-after.json), [coordinator validation](../../batches/2026-11-04-batch-231507/dune-imperium-coordinator-validation.json), [complete semantic review](../../batches/2026-11-04-batch-231507/dune-imperium-expanded05-root-preliminary-review.json), [runtime verification](../../batches/2026-11-04-batch-231507/dune-imperium-expanded05-runtime-check.json), and [iteration integrity](../../batches/2026-11-04-batch-231507/dune-imperium-expanded05-coordinator-iteration-check.json).

The earlier helper count of 11 included two undispatched preparations; both machine status files now count nine executed pairs and name the actual proof paths. The earlier wait/block record is preserved as [history](integration-wait-history.json). See the [complete evidence inventory](evidence-index.md).
'''
(P/'README.md').write_text(text)
files = sorted(x for x in P.rglob('*') if x.is_file() and x.name != 'evidence-index.md')
(P/'evidence-index.md').write_text('# Evidence inventory\n\n'+''.join(f'- [{x.relative_to(P)}]({x.relative_to(P).as_posix()})\n' for x in files))
for name in ['README.md','evidence-index.md']:
    for target in re.findall(r'\]\(([^)]+)\)',(P/name).read_text()):
        if not target.startswith(('http','/','#')):
            require('link:'+name+':'+target,(P/target.split('#')[0]).exists())
print(json.dumps({'status':'complete','checks':len(checks),'executed_pairs':9,'source_audit_claim_groups':36,'hash':report['canonical_sha256']}))
