"""Parent evidence checks and gate normalization; no new semantic audit verdict."""
from pathlib import Path
import hashlib
import json

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
COORD = ROOT / 'docs/quality/summary-qa/batches/2026-11-05-batch-002957/coordinator-checks'
H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
resolve = lambda p: (ROOT / p).resolve()
expected = {
    'source-audit-final-09-completed.json': '5f886e52b3e1ca62d3f4cf3b991578e88414a018c0a078d0acdfb0206b968b3d',
    'source-audit-final-09-completed-read-ledger.json': '6b2a4500019e9838cc16763452ed2fce1b9aa6cc1f99c4fabf09a94cada7b93f',
    'source-audit-final-09-completed-visual-manifest.json': '74bf4e9a241e8a4ed180e4151ca3aad575c55a67479d7601987b626a15aad5cd',
    'source-candidate-20.md': '63da3a8f472025ad10028eba03c11ec1ad00b2455cb3e70a08bafa6ae90bdb24',
    'source-audit09-completed-evidence-validator.py': '8631ce835cbca4665d1df9604b83bd1051d52ea74638cfaccd59abb5c3896484',
    'source-audit09-completed-evidence-proof.json': 'fc937e51240c7bec37d6e2b10338226db1fd49cffc032eb1b71c18e5abe7dcca',
}
coordinator_expected = {
    'spirit-source-audit-final-09-completed-actual-delivery.json': 'cd61156de39f8ff66c50d007291671f0dfe8a1195644613404026596a43e8302',
    'spirit-completed09-publisher-prose-lineage.json': '42d479c1f3f7875a36e47679d8c2b59e7a82fb1459a9c5a575dd85fe6fe7f266',
    'spirit-completed09-mandatory-inventory-and-render-lineage.json': '4a023bf3d662b21d3bcbd5f50378165e8ac9da3a26f4bf461b1d7470f5ab9423',
}
checks = []


def check(name, passed, kind='filesystem_or_object'):
    checks.append({'name': name, 'passed': bool(passed), 'kind': kind})
    assert passed, name


for name, digest in expected.items():
    check('frozen artifact ' + name, H(B / name) == digest)
for name, digest in coordinator_expected.items():
    check('frozen independent evidence ' + name, H(COORD / name) == digest)
a = load(B / 'source-audit-final-09-completed.json')
l = load(B / 'source-audit-final-09-completed-read-ledger.json')
v = load(B / 'source-audit-final-09-completed-visual-manifest.json')
p = load(B / 'source-audit09-completed-evidence-proof.json')
c = load(COORD / 'spirit-source-audit-final-09-completed-actual-delivery.json')
lineage = load(COORD / 'spirit-completed09-mandatory-inventory-and-render-lineage.json')
publisher = load(COORD / 'spirit-completed09-publisher-prose-lineage.json')
check('all333 original evidence checks preserved and passing', p['passed'] and not p['errors']
      and len(p['checks']) == 333 and all(x['pass'] for x in p['checks']))
check('original proof binds exact current completed artifacts',
      all(p['completed_artifact_sha256'][str((B / n).resolve())] == expected[n]
          for n in list(expected)[:3]))
check('parent original-helper rerun identical bytes',
      load(B / 'source-audit09-completed-root-rerun.json')['same_exact_proof_sha256']
      == expected['source-audit09-completed-evidence-proof.json'])
check('reported semantic PASS and no unresolved findings', a['verdict'] == 'PASS'
      and a['findings'] == [] and a['finding_counts'] == {'MAJOR': 0, 'MINOR': 0},
      'existing_auditor_semantic_verdict_not_new_parent_audit')
candidate = B / 'source-candidate-20.md'
check('candidate path and canonical exact bytes', resolve(a['candidate_path']) == candidate.resolve()
      and candidate.read_bytes() == (ROOT / 'rules/spirit-island.md').read_bytes()
      and a['candidate_sha256'] == H(candidate) and a['candidate_characters'] == 52388
      and a['candidate_bytes'] == 52590 and p['canonical_bytes_only']['equal'])
for group in a['checked_groups']:
    for ref in group['source_references']:
        source = resolve(ref['path'])
        check('exact primary anchor ' + group['group'] + ':' + str(ref['start']),
              H(source) == ref['source_sha256']
              and source.read_text()[ref['start']:ref['end']] == ref['passage'])
rows = l['source_delivery']
inventory = {resolve(x['path']): x for x in l['text_inputs']}
check('complete16-input inventory matches merged91 delivery rows',
      len(inventory) == 16 and len(rows) == 91
      and set(inventory) == {resolve(x['path']) for x in rows})
for path, item in inventory.items():
    check('complete text metadata ' + path.name, item['source_sha256'] == H(path)
          and item['character_length'] == len(path.read_text())
          and item['bytes'] == path.stat().st_size and item['complete'])
key = lambda x: (str(resolve(x['path'])), x['start'], x['end'],
                 x['source_sha256'], x['slice_sha256'])
actual_rows = c['complete_actual_pre_report_text_reads']
check('independent actual91 pre-completed-report text outputs match exact merged rows',
      c['verified'] and len(actual_rows) == 91
      and sorted(map(key, actual_rows)) == sorted(map(key, rows))
      and all(x['actual_pre_report_output_ordinals']
              and all(n < c['first_report_creation_ordinal'] for n in x['actual_pre_report_output_ordinals'])
              for x in actual_rows), 'independent_actual_runtime_delivery')
check('independent actual delivery binds current audit/body',
      c['audit_sha256'] == expected['source-audit-final-09-completed.json']
      and c['summary_sha256'] == expected['source-candidate-20.md']
      and resolve(c['audit_path']) == (B / 'source-audit-final-09-completed.json').resolve())
check('independent actual source-auditor settings and original fresh fork',
      len(c['actual_turn_contexts_minimal']) == 4
      and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high'
              for x in c['actual_turn_contexts_minimal'])
      and c['actual_initial_spawn'] == {'task_name': 'final_source_audit_09',
          'model': 'gpt-6.1-sol', 'reasoning_effort': 'high', 'fork_turns': 'none'},
      'independent_actual_runtime_model')
images = {str(resolve(x['path'])) for x in v['images']}
named = c['individually_named_pre_report_images']
check('independent actual57 named native image outputs before completed report',
      len(images) == len(named) == c['native_image_receipts'] == 57
      and len(c['actual_pre_report_image_outputs']) == 57
      and {str(resolve(x['path'])) for x in named} == images
      and all(x['call_ordinal'] < c['first_report_creation_ordinal']
              and x['output_ordinals']
              and all(n < c['first_report_creation_ordinal'] for n in x['output_ordinals']) for x in named),
      'independent_actual_runtime_image_delivery')
manifest = load(B / 'supplemental-source-manifest-v4.json')['source_records']
reconciled = a['mandatory_inventory_reconciliation']['records']
check('all72 actual role/path/hash reconciliations exact', len(reconciled) == len(manifest) == 72
      and all(x['path'] == z['path'] and x['sha256'] == z['sha256']
              and x['declared_role'] == (z['role'] if 'role' in z else z['source_type']) for x, z in zip(reconciled, manifest)))
check('independent required inventory and all five render reproductions',
      lineage['verified'] and lineage['audit_sha256'] == c['audit_sha256']
      and lineage['summary_sha256'] == c['summary_sha256']
      and lineage['supplemental_records_all_current_hashes_verified'] == 72
      and lineage['independently_required_text_inputs_exact'] == 16
      and lineage['required33_card_faces_and16_panels_all_present']
      and len(lineage['independent_pdf_render_reproductions']) == 5
      and all(x['byte_equal'] for x in lineage['independent_pdf_render_reproductions']))
check('complete primary publisher prose independently reproduced', publisher['verified']
      and publisher['extraction_exactly_reproduced'] and publisher['no_selective_prose_filtering']
      and publisher['complete_visible_characters'] == 4329
      and publisher['auditor_input_sha256'] == H(publisher['actual_auditor_temporary_input'])
      and publisher['durable_copy_sha256'] == H(publisher['durable_visible_prose_copy']))
check('initial incomplete history and completed chronology preserved',
      lineage['all_initial_incomplete_artifacts_preserved']
      and 'incomplete' in a['chronology']['initial_audit'].lower()
      and all(H(resolve(path)) == digest for path, digest in a['preserved_original_artifact_hashes'].items()))
normalized = [{'name': x['check'], 'passed': x['pass'], 'kind': 'original_auditor_evidence_check'}
              for x in p['checks']] + checks
out = {
    'validation_status': 'PASS',
    'purpose': 'Parent evidence extension and normalization; existing completed auditor verdict only.',
    'counts': {'checks': len(normalized), 'original_auditor_checks': 333,
               'parent_extension_checks': len(checks), 'blocking_failed_checks': 0,
               'nonblocking_diagnostics': 0, 'text_inputs': 16, 'successful_text_slices': 91,
               'visual_sources': 57},
    'frozen_artifact_sha256': expected,
    'independent_coordinator_evidence': {str(COORD / n): h for n, h in coordinator_expected.items()},
    'validator': {'path': str(Path(__file__).resolve()), 'sha256': H(__file__)},
    'checks': normalized,
    'limits': ['Filesystem checks validate bytes, bounds, recorded caps, metadata and exact reproduction.',
               'Coordinator proof independently verifies actual pre-completed-report text/image delivery and model/fork provenance; semantic understanding and perception are auditor attestations.',
               'Original15-input PASS was incomplete and never adopted. All91 required slices predate the completed report; earlier90 and57 views are correctly reused, not new.',
               'No coverage-stopping, blind-reader, publication or completion approval is implied.'],
}
target = B / 'source-audit09-completed-delivery-validation.json'
target.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'validation_status': out['validation_status'], 'counts': out['counts'],
                  'output': str(target), 'sha256': H(target)}))
