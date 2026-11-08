"""Accept exact C26 with the original auditor's preserved, explicit note correction."""
from pathlib import Path
from collections import Counter
import hashlib
import io
import json
from PIL import Image

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
load = lambda p: json.loads(Path(p).read_text())
H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
r = load(B / 'source-audit-final-15.json')
add = load(B / 'source-audit15-own-source-dissolve-addendum.json')
ledger = load(B / 'source-audit15-own-source-dissolve-addendum-read-view-ledger.json')
physical = load(B / 'source-audit15-original-evidence-validation.json')
original_transport = load(B / 'source-audit15-original-actual-delivery-validation.json')
new_transport = load(B / 'source-audit15-own-source-addendum-actual-delivery-validation.json')
parent = load(B / 'source-audit15-parent-semantic-read-progress.json')
root_path = ROOT / 'docs/quality/summary-qa/batches/2026-11-05-batch-002957/coordinator-checks/spirit-C26-source15-own-correction-and-semantic-acceptance.json'
root = load(root_path)
candidate = B / 'source-candidate-26.md'
assert r['candidate_sha256'] == H(candidate) == H(ROOT / 'rules/spirit-island.md') == root['summary_sha256'] == 'ce8f1d645f466686ae2e75fcd29130fa89cbb1c4963d981090e3768a526a6fd1'
assert r['verdict'] == root['verdict'] == 'PASS' and not r['findings'] and r['unresolved_findings'] == 0
assert physical['all_passed'] and physical['counts']['blocking_failed_checks'] == 0
assert original_transport['verified'] and new_transport['verified']
assert new_transport['text_sources'] == 1 and new_transport['actual_distinct_text_range_deliveries'] == 7 and new_transport['unique_visual_sources'] == new_transport['public_image_blocks'] == 2
for freeze_name, copy_key in [('source-audit15-original-freeze.json', 'original_completed_copy'), ('source-audit15-own-source-addendum-original-freeze.json', 'immutable_copy')]:
    for name, row in load(B / freeze_name)['files'].items():
        assert H(B / name) == row['sha256'] == H(row[copy_key])
original_model = load(B / 'runtime/final_source_audit_15-final-completed-projection.json')
completed_model = load(B / 'runtime/final_source_audit_15-own-source-dissolve-completed-projection.json')
assert original_model['confirmed_settings'] == [{'model': 'gpt-6.1-sol', 'effort': 'high'}]
assert completed_model['confirmed_settings'] == [{'model': 'gpt-6.1-sol', 'effort': 'high'}] * 2
assert completed_model['requested_spawn']['fields']['fork_turns'] == 'none'
assert original_model['thread_id'] == completed_model['thread_id']
assert parent['full_parent_read_complete'] and parent['actual_parent_read_contiguous_end'] == 131096
assert parent['view_sha256'] == H(B / 'source-audit15-parent-all-human-semantic-view.json')
assert root['verified'] and root['original_three_file_freeze_rechecked'] and root['addendum_original_freeze_rechecked'] and root['all23_groups_and57_original_visual_notes_read'] and root['all72_exact_supplemental_members_reconciled']
assert root['original_audit_sha256'] == H(B / 'source-audit-final-15.json') and root['addendum_sha256'] == H(B / 'source-audit15-own-source-dissolve-addendum.json')
assert len(root['new_actual_text_ranges']) == 7 and len(root['new_original_and_diagnostic_views']) == 2 and root['diagnostic_pixels_independently_reproduced_6x_nearest']
local_refs = Counter((str((ROOT / x['path']).resolve()), x['source_sha256'], x['start'], x['end']) for g in r['checked_groups'] for x in g['sources'])
root_refs = Counter((str(Path(x['path']).resolve()), x['sha256'], x['start'], x['end']) for x in root['exact_primary_checked_group_passages'])
assert local_refs == root_refs and sum(local_refs.values()) == 97

source = ROOT / add['primary_source']['path']
assert H(source) == add['primary_source']['source_sha256'] == '92a29d653e305f8fa839c822d8b92b1298298f721c4de787ca9a017d399cedd9'
assert add['reconciliation_status'] == 'CORRECTED_OWN_OBSERVATION'
expected = [
    {'source_piece': 'City', 'source_count': 1, 'destination_piece': 'Explorer', 'destination_count': 2},
    {'source_piece': 'Town', 'source_count': 1, 'destination_piece': 'Explorer', 'destination_count': 1},
    {'source_piece': 'Dahan', 'source_count': 1, 'destination_piece': 'Explorer', 'destination_count': 1},
]
assert add['precise_printed_replacements'] == expected
visual_path = B / 'source-audit-final-15-visual-manifest.json'
visual = load(visual_path)
old = add['original_observation']
assert old['literal'] == visual['images'][41]['observations'] == visual_path.read_text()[old['start']:old['end']]
assert old['source_sha256'] == H(visual_path)
assert add['impact']['candidate_sha256'] == H(candidate)
assert 'evidentiary error' in add['impact']['checked_group_verdict']
assert add['artifact_preservation']['original_artifacts_unchanged']
assert add['artifact_preservation']['candidate_unchanged'] and add['artifact_preservation']['canonical_file_not_opened_or_modified']
completion = ledger['source_completion']
assert completion['source_sha256'] == H(visual_path) and completion['ranges_received'] == 7 and completion['contiguous_zero_based_unicode']
pos = 0
for item in ledger['source_delivery']:
    assert item['start'] == pos and 0 < item['end'] - item['start'] <= 6000 and item['output_cap'] >= 4000 and not item['truncated']
    assert item['slice_sha256'] == hashlib.sha256(visual_path.read_text()[item['start']:item['end']].encode()).hexdigest()
    pos = item['end']
assert pos == len(visual_path.read_text()) == 38161
im = Image.open(source)
diag = im.resize((im.width * 6, im.height * 6), Image.Resampling.NEAREST)
output = io.BytesIO()
diag.save(output, format='PNG')
diagnostic = Path(ledger['image_delivery'][1]['path'])
assert output.getvalue() == diagnostic.read_bytes()
assert H(diagnostic) == ledger['image_delivery'][1]['source_sha256']
reused = ledger['reused_original_readings'][0]
assert reused['source_sha256'] == H(candidate)
assert reused['slice_sha256'] == hashlib.sha256(candidate.read_text()[reused['start']:reused['end']].encode()).hexdigest()
assert any(x['path'] == reused['path'] and x['range'] == [reused['start'], reused['end']] and x['slice_sha256'] == reused['slice_sha256'] for x in original_transport['text_deliveries'])

read_receipt = {
    'both_complete_new_original_documents_actually_parent_read': True,
    'new_addendum_characters': 8289, 'new_ledger_characters': 8030,
    'events': [
        {'file': 'addendum', 'range': [0, 6000], 'slice_sha256': 'b602b55a66e20fcafc96ed6e9cc8ce5eb479684db81df7399329723e41681842'},
        {'file': 'addendum', 'range': [6000, 8289], 'slice_sha256': '24db756c51149a369ed4c6bf6081a5adc5dcd8149b75d9525d45048f9e6fdfc5'},
        {'file': 'ledger', 'range': [0, 6000], 'slice_sha256': '471d5e47ddc920024dccf552cc1ce142ddbe4cf69be2af2be9bc0373b35bc695'},
        {'file': 'ledger', 'range': [6000, 8030], 'slice_sha256': '55ac94e10434f8b5370a75bc274eebb11cf571e7a12c26f412a965580f748aeb'},
    ],
    'one_range_per_actual_notify_event_cap4000_no_truncation': True,
    'parent_agrees_precise_mapping_and_honest_qualification_of_original_group': True,
    'original_three_artifacts_and_original_note_not_rewritten': True,
    'root_semantic_acceptance_and_limits_selected1172_characters_actually_read': '4e65ea',
    'full37147_character_Root_transport_proof_not_claimed_as_human_read': True,
}
(B / 'source-audit15-own-source-addendum-parent-read-and-acceptance.json').write_text(json.dumps(read_receipt, indent=2) + '\n')
files = [
    'source-audit-final-15.json', 'source-audit-final-15-read-ledger.json', 'source-audit-final-15-visual-manifest.json',
    'source-audit15-original-freeze.json', 'source-audit15-original-evidence-validation.json',
    'source-audit15-original-actual-delivery-validation.json',
    'source-audit15-parent-semantic-read-progress.json', 'source-audit15-parent-view-reconstruction-validation.json',
    'source-audit15-own-source-dissolve-addendum.json', 'source-audit15-own-source-dissolve-addendum-read-view-ledger.json',
    'source-audit15-own-source-addendum-original-freeze.json',
    'source-audit15-own-source-addendum-actual-delivery-validation.json',
    'source-audit15-own-source-addendum-parent-read-and-acceptance.json',
]
adoption = {
    'semantic_verdict': 'PASS', 'candidate_sha256': H(candidate), 'unresolved_findings': 0,
    'original_reported_verdict': 'PASS', 'original_reported_findings': 0,
    'original_audit_one_actual_context': True,
    'same_original_pure_auditor_total_actual_contexts': 2,
    'actual_model': 'gpt-6.1-sol/high', 'initial_fork_turns': 'none',
    'not_a_new_fresh_source_vote': True,
    'explicit_resolved_auditor_note_error': {'image_index': 41, 'incorrect_replacement_clauses': 2, 'corrected_mappings': expected, 'affected_group': 'Core card special procedures', 'original_group_evidence_qualified_not_silently_revalidated': True, 'canonical_rule_finding_or_body_edit': False},
    'original_exact_delivery': {'text_files': 16, 'ranges': 92, 'original_detail_images': 57},
    'own_source_new_exact_delivery': {'own_note_text_ranges': 7, 'original_JPEG_and_diagnostic_views': 2, 'prior_source_reading_reuse_explicit': True},
    'original_physical_reference_checks': physical['counts'],
    'parent_original_all_human_fields_actually_read_characters': 131096,
    'evidence': {name: H(B / name) for name in files},
    'coordinator_semantic_acceptance': {'path': str(root_path), 'sha256': H(root_path), 'all97_reference_bindings_equal_local': True},
    'same_pure_auditor_completed_context_profile': {'path': str(B / 'runtime/final_source_audit_15-own-source-dissolve-completed-projection.json'), 'sha256': H(B / 'runtime/final_source_audit_15-own-source-dissolve-completed-projection.json')},
    'full_new173_reader_pair_required': True,
    'stamp_publication_or_goal_completion_authorized': False,
}
p = B / 'source-audit15-original-with-own-source-correction-semantic-adoption.json'
assert not p.exists()
p.write_text(json.dumps(adoption, indent=2) + '\n')
print(json.dumps({'semantic_verdict': 'PASS', 'candidate_sha256': H(candidate), 'unresolved_guide_findings': 0, 'resolved_original_audit_note_errors': 1, 'adoption_sha256': H(p), 'no_new_source_vote_or_canonical_edit': True}))
