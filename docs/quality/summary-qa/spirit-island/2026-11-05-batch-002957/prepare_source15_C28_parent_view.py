"""Lossless SOURCE-parent view with explicit exact prior-reference reuse only."""
from pathlib import Path
import copy
import hashlib
import json

B = Path(__file__).resolve().parent
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
object_hash = lambda v: hashlib.sha256(json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
rp = B / 'source-audit15-current-body-C28-followup.json'
lp = B / 'source-audit15-current-body-C28-followup-read-view-ledger.json'
freeze = load(B / 'source-audit15-C28-followup-original-completed/original-freeze.json')
for row in freeze['originals']:
    assert H(Path(row['path'])) == H(Path(row['immutable_copy'])) == row['sha256']
original = {'report': load(rp), 'ledger': load(lp)}
view = copy.deepcopy(original)
prior_report = B / 'source-audit-final-15.json'
prior_ledger = B / 'source-audit15-current-body-C27-followup-read-view-ledger.json'
old = load(prior_report)
old_l = load(prior_ledger)
references = {}

def pointer(value, path):
    for key in path.strip('/').split('/'):
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value

def ref(value, path, ptr, reason):
    target = pointer(load(path), ptr)
    assert target == value
    name = f'r{len(references):02}'
    references[name] = {'path': str(path), 'source_sha256': H(path), 'json_pointer': ptr,
                        'exact_object_sha256': object_hash(value), 'reason': reason}
    return {'$exact_source_parent_reference': name}

for i, (row, prior) in enumerate(zip(view['report']['checked_current_scope'], old['checked_groups'])):
    assert row['group'] == prior['group']
    row['primary_sources'] = ref(row['primary_sources'], prior_report, f'/checked_groups/{i}/sources',
                                 'Exact unchanged prior literal sources: parent originally read all97 within full131096-character human review.')
    row['visual_source_references'] = ref(row['visual_source_references'], prior_report, f'/checked_groups/{i}/visual_sources',
                                         'Exact unchanged prior visual references; original human observations and later own-note correction remain retained.')

for key in ['reused_complete_text_perceptions', 'reused_visual_perceptions', 'reused_source_manifest_and_supplement_reconciliation']:
    assert view['ledger'][key] == old_l[key]
    view['ledger'][key] = ref(view['ledger'][key], prior_ledger, '/' + key,
                              'Unchanged technical identity/perception-reuse metadata; machine-reverified, not newly perceived or claimed newly human-read.')

for key, prior_key in [('complete_text_perceptions', 'reused_complete_text_perceptions'), ('visual_perceptions', 'reused_visual_perceptions')]:
    value = view['report']['reused_original_evidence'][key]
    assert value == old_l[prior_key]
    view['report']['reused_original_evidence'][key] = ref(value, prior_ledger, '/' + prior_key,
                                                        'Same exact unchanged technical reuse metadata as ledger; no current human judgment removed.')

assert view['ledger']['actual_new_views'] == original['report']['new_views']
view['ledger']['actual_new_views'] = ref(view['ledger']['actual_new_views'], rp, '/new_views',
                                       'Exact duplicate of new human observations retained in full in this report view; SOURCE-parent only.')

def restore(value):
    if isinstance(value, dict) and set(value) == {'$exact_source_parent_reference'}:
        r = references[value['$exact_source_parent_reference']]
        path = Path(r['path'])
        assert H(path) == r['source_sha256']
        target = pointer(load(path), r['json_pointer'])
        assert object_hash(target) == r['exact_object_sha256']
        return target
    if isinstance(value, dict):
        return {k: restore(v) for k, v in value.items()}
    if isinstance(value, list):
        return [restore(v) for v in value]
    return value

assert restore(view) == original
prior_read = load(B / 'source-audit15-parent-semantic-read-progress.json')
assert prior_read['full_parent_read_complete'] and prior_read['actual_parent_read_contiguous_end'] == prior_read['total_characters'] == 131096
assert prior_read['exact_primary_text_references_physically_verified'] == 97
p = B / 'source-audit15-C28-parent-current-human-semantic-view.json'
s = B / 'source-audit15-C28-parent-exact-reference-sidecar.json'
v = B / 'source-audit15-C28-parent-view-reconstruction-and-prior-reuse.json'
assert not any(x.exists() for x in [p, s, v])
p.write_text(json.dumps({'original_report_sha256': H(rp), 'original_ledger_sha256': H(lp),
                         'all_current_human_judgments_and_new_citations': view}, ensure_ascii=False, separators=(',', ':')) + '\n')
s.write_text(json.dumps({'exact_references': references}, ensure_ascii=False, indent=2) + '\n')
v.write_text(json.dumps({'report_sha256': H(rp), 'ledger_sha256': H(lp), 'view_sha256': H(p), 'sidecar_sha256': H(s),
                        'exact_both_original_objects_reconstructed': True,
                        'all_new_current_scope_observations_changed_blocks_new_text_visual_citations_qualifications_and_limits_retained': True,
                        'only_exact_prior_literal_reference_arrays_and_unchanged_technical_reuse_arrays_and_one_SOURCE_parent_duplicate_referenced': True,
                        'prior_actual_parent_full_read': {'path': str(B / 'source-audit15-parent-semantic-read-progress.json'),
                                                         'sha256': H(B / 'source-audit15-parent-semantic-read-progress.json'),
                                                         'characters': 131096, 'exact_primary_references': 97},
                        'not_an_input_to_auditor_or_any_reader_grader_neutral': True,
                        'no_reader_grader_or_neutral_data_deduplicated': True,
                        'current_parent_actual_read_not_yet_claimed': True}, indent=2) + '\n')
print(json.dumps({'current_human_view_characters': len(p.read_text()), 'sha256': H(p),
                  'exact_reference_pointers': len(references), 'entire_report_and_ledger_reconstruction': True,
                  'current_parent_full_read_pending': True}))
