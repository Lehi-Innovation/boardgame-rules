"""Check C28 physical evidence and explicit prior reuse; no semantic vote."""
from pathlib import Path
import hashlib
import json
from PIL import Image

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
load = lambda p: json.loads(Path(p).read_text())
H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
source = lambda p: (ROOT / p).resolve()
checks = []

def check(ok, name):
    assert ok, name
    checks.append(name)

rp = B / 'source-audit15-current-body-C28-followup.json'
lp = B / 'source-audit15-current-body-C28-followup-read-view-ledger.json'
r, l = load(rp), load(lp)
freeze = load(B / 'source-audit15-C28-followup-original-completed/original-freeze.json')
for row in freeze['originals']:
    check(H(row['path']) == H(row['immutable_copy']) == row['sha256'], 'entire original frozen ' + Path(row['path']).name)
current = B / 'source-candidate-28.md'
prior = B / 'source-candidate-27.md'
check(r['candidate_sha256'] == H(current) == H(ROOT / 'rules/spirit-island.md'), 'exact current canonical C28')
check(r['candidate_character_length'] == len(current.read_text()) == 55813 and r['candidate_byte_length'] == current.stat().st_size == 56017, 'exact character and byte lengths')
check(r['prior_candidate_sha256'] == H(prior), 'own completely read prior C27')
check(r['whole_current_body_read'] and r['verdict'] == 'PASS' and not r['findings'] and r['unresolved_current_guide_findings'] == 0 and not r['unverified_current_guide_concerns'], 'reported zero current concerns; semantic adoption separate')
check(r['new_source_delivery'] == l['actual_new_text_deliveries'] and r['new_views'] == l['actual_new_views'], 'two reports agree on all new deliveries and views')
for row in l['actual_new_text_deliveries']:
    p = source(row['path']); s = p.read_text(); a, z = row['start'], row['end']
    check(H(p) == row['source_sha256'] and len(s) == row['character_length'], 'new source identity ' + str([row['path'], a, z]))
    check(0 <= a < z <= len(s) and z-a <= 6000 and hashlib.sha256(s[a:z].encode()).hexdigest() == row['slice_sha256'] and row['output_cap'] >= 4000 and not row['truncated'], 'new exact bounded range ' + str([row['path'], a, z]))
for row in l['reused_own_evidence_artifacts']:
    check(H(source(row['path'])) == row['source_sha256'], 'own evidence unchanged ' + row['path'])
old_l = load(B / 'source-audit15-current-body-C27-followup-read-view-ledger.json')
for key in ['reused_complete_text_perceptions', 'reused_visual_perceptions', 'reused_source_manifest_and_supplement_reconciliation']:
    check(l[key] == old_l[key], 'exact explicitly reused prior array ' + key)
for row in l['reused_complete_text_perceptions']:
    p = source(row['path'])
    check(H(p) == row['source_sha256'] and len(p.read_text()) == row['character_length'] and row['hash_verified_unchanged'], 'reused whole text exact ' + row['path'])
for row in l['reused_visual_perceptions']:
    p = source(row['path'])
    check(H(p) == row['source_sha256'] and list(Image.open(p).size) == row['dimensions'] and row['hash_verified_unchanged'], 'reused native visual exact ' + row['path'])
expected = load(B / 'expanded-iteration-09/input-manifest.json')['source_hashes']
pins = {str(source(row['path'])): row['source_sha256'] for row in l['reused_source_manifest_and_supplement_reconciliation']}
check(len(pins) == len(expected) == 79 and pins == {str(source(p)): h for p, h in expected.items()}, 'all79 unchanged primary and locator pins')
for row in l['reused_source_manifest_and_supplement_reconciliation']:
    check(H(source(row['path'])) == row['source_sha256'] and row['hash_verified_unchanged'], 'reused source pin exact ' + row['path'])
original_delivery = load(B / 'source-audit15-original-actual-delivery-validation.json')
check(original_delivery['verified'] and original_delivery['text_sources'] == 16 and original_delivery['actual_distinct_text_range_deliveries'] == 92 and original_delivery['unique_visual_sources'] == original_delivery['public_image_blocks'] == 57 and original_delivery['record_cutoff_exclusive'] == 653, 'original completed authority perception evidence remains bounded and verified')
old = load(B / 'source-audit-final-15.json')
check(len(r['checked_current_scope']) == len(old['checked_groups']) == 23, 'all23 current scope groups')
old_refs = old_visual_refs = 0
for row, previous in zip(r['checked_current_scope'], old['checked_groups']):
    check(row['group'] == previous['group'] and row['primary_sources'] == previous['sources'] and row['visual_source_references'] == previous['visual_sources'], 'exact old reference arrays ' + row['group'])
    old_visual_refs += len(row['visual_source_references'])
    for ref in row['primary_sources']:
        p = source(ref['path'])
        check(H(p) == ref['source_sha256'] and p.read_text()[ref['start']:ref['end']] == ref['passage'], 'exact reused literal primary span ' + row['group'])
        old_refs += 1
whole_texts = {str(source(row['path'])): row['source_sha256'] for row in l['reused_complete_text_perceptions']}
available_visuals = {str(source(row['path'])): row['source_sha256'] for row in l['reused_visual_perceptions'] + l['actual_new_views']}
diff = load('/tmp/audit15-C28-derived-diff.json')
check(r['comparison']['source_only_derived_diff'] == diff and r['comparison']['exact_changed_blocks'] == len(diff['changes']) == 4 and r['comparison']['net_character_change'] == 667 and r['comparison']['otherwise_textually_unchanged'], 'exact independently reproduced four-block comparison')
check(load(B / 'source-audit15-C28-derived-diff-independent-reproduction.json')['complete_JSON_bytes_reproduced'], 'independent exact derived JSON byte reproduction')
new_refs = new_visual_refs = 0
cur, prev = current.read_text(), prior.read_text()
for row, change in zip(r['changed_material'], diff['changes']):
    check(not row['findings'] and row['candidate_start'] == change['current_start'] and row['candidate_end'] == change['current_end'] and row['prior_start'] == change['prior_start'] and row['prior_end'] == change['prior_end'], 'changed block exact offsets ' + row['change_id'])
    check(cur[row['candidate_start']:row['candidate_end']] == change['current_text'] and prev[row['prior_start']:row['prior_end']] == change['prior_text'], 'changed block literal before and after ' + row['change_id'])
    for ref in row['primary_citations']:
        p = source(ref['path']); a, z = ref['start'], ref['end']
        check(H(p) == ref['source_sha256'] and 0 <= a < z <= len(p.read_text()) and p.read_text()[a:z] == ref['passage'], 'newly applied literal primary citation ' + row['change_id'])
        # Prior complete perception is explicitly allowed; no invented new-reopen quota.
        check(whole_texts.get(str(p)) == ref['source_sha256'] or any(source(x['path']) == p and x['start'] <= a < z <= x['end'] for x in l['actual_new_text_deliveries']), 'citation has honest original complete or new perception ' + row['change_id'])
        new_refs += 1
    for ref in row['primary_visual_citations']:
        p = source(ref['path'])
        check(H(p) == ref['source_sha256'] == available_visuals.get(str(p)), 'changed visual citation has exact native original/new perception ' + row['change_id'])
        new_visual_refs += 1
check(old_refs == 97 and old_visual_refs == 65 and new_refs == 7 and new_visual_refs == 4, 'all observed97 old plus7 current primary and65 old plus4 current visual references')
for row in l['actual_new_views']:
    p = source(row['path'])
    check(H(p) == row['source_sha256'] and list(Image.open(p).size) == row['dimensions'] and row['requested_detail'] == row['forwarded_detail'] == 'original' and row['entire_image_actually_received'], 'new full native image exact ' + row['path'])
qual = r['dissolve_prior_evidence_qualification']
check(H(source(qual['addendum_path'])) == qual['addendum_sha256'], 'own earlier note correction unchanged')
check(qual['corrected_printed_replacements'] == [{'source_piece':'City','source_count':1,'destination_piece':'Explorer','destination_count':2}, {'source_piece':'Town','source_count':1,'destination_piece':'Explorer','destination_count':1}, {'source_piece':'Dahan','source_count':1,'destination_piece':'Explorer','destination_count':1}], 'honest corrected payload qualification retained')
actual_path = B / 'source-audit15-C28-followup-actual-delivery-validation.json'
actual = load(actual_path)
check(actual['verified'] and actual['new_record_interval'] == [811, 904] and actual['actual_distinct_text_range_deliveries'] == 13 and actual['new_candidate_whole_contiguous'] and actual['new_views'] == 2 and len(actual['actual_new_native_image_deliveries']) == 2, 'strict actual13 text plus2 native outputs in only new completed phase')
profile_path = B / 'runtime/final_source_audit_15-C28-followup-final-completed-projection.json'
profile = load(profile_path)
check(profile['confirmed_settings'] == [{'model':'gpt-6.1-sol','effort':'high'}] * 4 and profile['requested_spawn']['fields']['fork_turns'] == 'none', 'same initially fresh pure actor actual4 contexts')
counts = {'checks':len(checks), 'blocking_failed_checks':0, 'new_exact_single_range_deliveries':13,
          'new_whole_candidate_slices':10, 'new_primary_reopen_windows':1,
          'new_whole_own_derived_diff':1, 'new_own_derived_diff_ranges':2, 'new_images':2,
          'reused_whole_texts':16, 'reused_native_views':57, 'reused_authority_and_locator_pins':79,
          'current_scope_groups':23, 'exact_reused_primary_references':old_refs,
          'exact_changed_primary_references':new_refs, 'visual_references':old_visual_refs,
          'changed_visual_references':new_visual_refs, 'actual_total_same_auditor_contexts':4}
out = {'all_passed':True, 'counts':counts, 'checks':[{'check':x,'passed':True} for x in checks],
       'candidate_sha256':H(current), 'frozen_artifact_sha256':{rp.name:H(rp),lp.name:H(lp)},
       'actual_delivery_proof_sha256':H(actual_path), 'completed_model_profile_sha256':H(profile_path),
       'original_authority_perception_proof_sha256':H(B / 'source-audit15-original-actual-delivery-validation.json'),
       'semantic_adoption':False, 'same_original_pure_auditor_not_new_fresh_vote':True,
       'prior_exact_authority_perception_honestly_reused_not_claimed_anew':True,
       'parent_full_current_human_review_and_coordinator_current_semantic_acceptance_separate':True}
p = B / 'source-audit15-C28-followup-physical-evidence-validation.json'
assert not p.exists()
p.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'all_passed':True, 'checks':len(checks), 'exact_primary_references':old_refs+new_refs,
                  'changed_visual_references':new_visual_refs, 'semantic_adoption':False, 'sha256':H(p)}))
