"""Record read-only coordinator integration verification; never write shared files."""
from pathlib import Path
import datetime, hashlib, json, shutil
import yaml
from scripts.catalog import validate_catalog
from scripts.generate_manifest import build_manifest
from scripts.generate_index import parse_frontmatter, format_row
P=Path(__file__).parent
assert not (P/'coordinator-final-validation.json').exists(), 'One-shot completion receipt already exists; preserve it.'
B=P.parents[1]/'batches/2026-11-04-batch-231507'
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
write=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
for name in ['README.md','game-status.json','validation.json','evidence-hashes.json']:
 dest=P/('pre-integration-'+name)
 if not dest.exists():shutil.copyfile(P/name,dest)
paths=[B/'orl-ans-coordinator-validation.json',B/'orl-ans-stamped-coordinator-iteration-check.json',B/'orl-ans-coordinator-stamped-review.json',B/'recording/orl-ans-20261105-013301/validation.json',B/'publication/20261105-013352/validation.json']
co,mechanical,review,stamp,pub=[read(p) for p in paths]
sha=h('rules/orl-ans.md')
registry=[g for g in yaml.safe_load(Path('games.yaml').read_text())['games'] if g.get('bgg_id')==164928]
manifest=[g for g in read('games.json')['games'] if g.get('slug')=='orl-ans']
expected=[g for g in build_manifest(Path('rules'))['games'] if g.get('slug')=='orl-ans']
fm=parse_frontmatter(Path('rules/orl-ans.md').read_text());fm['slug']='orl-ans'
index_rows=[line for line in Path('index.md').read_text().splitlines() if '(rules/orl-ans/)' in line]
audit=yaml.safe_load(Path('docs/quality/semantic-audit-results.yaml').read_text())['orl-ans']
errors=validate_catalog(Path('.'))
target_errors=[e for e in errors if 'orl-ans' in e or '164928' in e]
checks={
 'canonical_equals_final_snapshot':sha==h(P/'stamped-iteration-03/summary-snapshot.md'),
 'coordinator_exact_sha':sha==co['canonical_sha256']==review['summary_sha256']==stamp['summary_sha256_before']==stamp['summary_sha256_after'],
 'coordinator_integrity_pass':mechanical['mechanical_checks_pass'] and all(mechanical['checks'].values()) and all(mechanical['input_hash_checks'].values()),
 'coordinator_source_audit_and_models_confirmed':review['worker_current_integrity_checks_pass'] and co['runtime_models_independently_verified_from_original_sessions'] and co['source_audit'].startswith('PASS'),
 'stamping_idempotent':not co['stamping_changed_tested_bytes'] and not stamp['stamping_changed_tested_bytes'] and not stamp['requires_full_bank_retest'],
 'recorded_current_audit_pass':audit['verdict']=='PASS' and sha in audit['reason'],
 'unrelated_entries_preserved':stamp['unrelated_audit_verdicts_preserved'] and stamp['global_audit_manifest_unchanged'] and pub['non_selected_index_lines_preserved'] and pub['non_selected_manifest_entries_preserved'],
 'current_registry_verified':len(registry)==1 and registry[0]['status']=='verified',
 'current_manifest_matches_regeneration':len(manifest)==1 and manifest==expected and manifest[0]['verification']=='verified',
 'current_index_matches_regeneration':index_rows==[format_row(fm)],
 'target_catalog_no_errors':not target_errors and not co['target_catalog_errors'],
 'coordinator_structural_diff_checks_pass':co['structural_validation']=='PASS' and co['targeted_git_diff_check']=='PASS',
}
result={'game':'orl-ans','observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'summary_sha256':sha,'checks':checks,'assigned_game_integration_pass':all(checks.values()),'coordinator_evidence':[{'path':str(p.resolve()),'sha256':h(p)} for p in paths],'current_registry_entry':registry,'current_manifest_entry':manifest,'current_index_row':index_rows,'current_recorded_audit':audit,'coordinator_catalog_errors_at_its_check':co['global_catalog_errors'],'current_global_catalog_errors':errors,'current_target_catalog_errors':target_errors,'scope_note':'Current global findings concern other games and are preserved explicitly; assigned Orléans integration passes. This does not claim batch or repository completion.','source_limit':'Cross-round retention after partial Town Hall use is not expressly ruled by selected sources; no invented answer is assigned. See source-gap-resolution.json.'}
assert result['assigned_game_integration_pass'],checks
write(P/'coordinator-final-validation.json',result)
inventory=read(P/'evidence-hashes.json')
assert all(h(P/f)==v for f,v in inventory.items())
inventory['coordinator-final-validation.json']=h(P/'coordinator-final-validation.json')
write(P/'evidence-hashes.json',inventory)
status=read(P/'game-status.json')
status.update(status='complete',phase='assigned-game-complete',coordinator_pending=[],persistent_goal='achieved; final goal status recorded after validation',coordinator_integration_path=str((P/'coordinator-final-validation.json').resolve()),coordinator_integration_pass=True,evidence_hash_count=len(inventory),current_global_catalog_errors=errors,completion_scope='Assigned Orléans only; whole batch/repository completion is not claimed.')
write(P/'game-status.json',status)
print(json.dumps({'assigned_game_integration_pass':True,'summary_sha256':sha,'current_global_catalog_errors':errors},indent=2))
