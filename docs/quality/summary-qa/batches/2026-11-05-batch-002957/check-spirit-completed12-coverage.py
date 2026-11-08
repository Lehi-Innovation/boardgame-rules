"""Check current v22 confirmation and accurately bind its own-source reuse."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import re

B = Path(__file__).resolve().parent
REPO = B.parents[4]
R = REPO / 'docs/quality/summary-qa/spirit-island' / B.name
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_text())
AP = R / 'coverage-review-12-completed.json'
LP = R / 'scope-coverage-12-completed-read-ledger.json'
C, L = load(AP), load(LP)
K = load(R / 'question-key-scope-review-12-completed.json')
old = load(R / 'scope-coverage-12-read-ledger.json')
prior_path = B / 'coordinator-checks/spirit-coverage-review12-actual-delivery-v2.json'
prior = load(prior_path)
assert prior['verified'] and H(Path(prior['coverage_report_path'])) == prior['coverage_report_sha256']
assert all(C[k] == 'PASS' for k in ('verdict', 'fixed_key_verdict', 'asked_fact_mapping_verdict', 'scope_verdict', 'coverage_verdict', 'stopping_verdict'))
assert C['remaining_gap_count'] == 0 and not C['remaining_gaps'] and not C['unresolved_stopping_findings']
assert C['checked_question_count'] == 172 and C['checked_required_fact_count'] == 507
assert C['read_evidence']['sha256'] == K['read_evidence']['sha256'] == H(LP)
for k in ('fixed_key_findings', 'asked_fact_mapping_findings', 'scope_findings', 'missing_truly_asked_facts_in_map', 'missing_truly_asked_facts_in_fixed_key'):
    assert not C[k] and not K[k]
runtime = Path(prior['runtime_path'])
tree = ast.parse((B / 'check-spirit-source09-delivery.py').read_text())
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ('strings', 'literal_image_paths')]
ns = {'json': json, 're': re, 'resolve': lambda p: Path(p) if Path(p).is_absolute() else REPO / p}
exec(compile(ast.Module(body=functions, type_ignores=[]), '<literal-data-parsers>', 'exec'), ns)
raw = runtime.read_bytes().splitlines(keepends=True)
calls, outputs, contexts, writers = {}, [], [], []
for n, line in enumerate(raw, 1):
    row = json.loads(line); p = row.get('payload', {})
    if row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ('function_call', 'custom_tool_call'):
        t = p.get('input', p.get('arguments', ''))
        assert isinstance(t, str)
        assert not any(x in t for x in ('rules/spirit-island.md', 'source-candidate-', 'reader-a.json', 'reader-b.json',
            'source-audit-final-', 'working-map-adjudication-16.json', 'list_agents', 'read_thread', 'wait_threads'))
        calls[p['call_id']] = (n, t)
        if AP.name in t and any(x in t for x in ('write_text', 'writeFile', 'apply_patch', 'json.dump(')):
            writers.append(n)
    elif p.get('type') in ('function_call_output', 'custom_tool_call_output'):
        outputs.append((n, p, list(ns['strings'](p.get('output')))))
assert contexts and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in contexts)
assert writers
boundary = min(writers)
manifest_text = (R / 'scope12-currentmap-input-manifest.json').read_text()
starts = [n for n, _, vals in outputs if n < boundary and any(manifest_text in v for v in vals)]
assert starts
start = min(starts)
text_checks = []
for path, f in L['new_text_inputs'].items():
    p = Path(path); t = p.read_text(); cursor = 0; parts = []
    assert H(p) == f['full_byte_sha256'] and len(t) == f['character_length']
    for c in f['slices']:
        a, z = c['start'], c['end']
        assert a == cursor and a < z <= len(t) and HB(t[a:z].encode()) == c['utf8_sha256']
        matches = [n for n, _, vals in outputs if start <= n < boundary and any(t[a:z] in v or json.dumps(t[a:z], ensure_ascii=False)[1:-1] in v for v in vals)]
        assert matches, (path, a, z)
        parts.append({'start': a, 'end': z, 'slice_sha256': c['utf8_sha256'], 'actual_output_records': matches})
        cursor = z
    assert cursor == len(t)
    text_checks.append({'path': path, 'sha256': H(p), 'complete': True, 'parts': parts})
source_reopens = []
for f in L['new_source_reopens']:
    p = Path(f['path']); t = p.read_text(); a, z = f['character_range']
    assert H(p) == f['full_byte_sha256'] and HB(t[a:z].encode()) == f['slice_utf8_sha256']
    matches = [n for n, _, vals in outputs if start <= n < boundary and any(t[a:z] in v for v in vals)]
    assert matches
    source_reopens.append({'path': str(p), 'start': a, 'end': z, 'actual_output_records': matches})
reused_text = []
for f in L['reused_primary_text_inputs']:
    p = Path(f['path']); original = old['text_inputs'][str(p)]
    assert H(p) == f['full_byte_sha256'] == original['full_byte_sha256'] and f['slices'] == original['slices']
    assert f['new_delivery'] is False
    reused_text.append({'path': str(p), 'sha256': H(p), 'own_original_actual_delivery_reference': str(prior_path)})
old_images = {x['path']: x for x in old['images']}
prior_images = {x['path']: x for x in prior['native_checks']}
for f in L['reused_images']:
    assert H(Path(f['path'])) == f['sha256'] == old_images[f['path']]['sha256'] == prior_images[f['path']]['sha256']
    assert f['new_visual_delivery'] is False
    for k in ('fully_viewed', 'view_detail', 'regions', 'observations'):
        assert f[k] == old_images[f['path']][k]
native = []
for n, p, vals in outputs:
    if not start <= n < boundary or not isinstance(p.get('output'), list):
        continue
    count = sum(isinstance(v, dict) and v.get('type') == 'input_image' for v in p['output'])
    if not count:
        continue
    cn, t = calls[p['call_id']]; paths = ns['literal_image_paths'](t)
    assert start <= cn < n < boundary and len(paths) == count
    native.extend({'path': path, 'sha256': H(Path(path)), 'call_record': cn, 'output_record': n} for path in sorted(paths))
assert {x['path']: x['sha256'] for x in native} == {x['path']: x['sha256'] for x in L['new_visual_reopens']}
assert len(text_checks) == 5 and sum(len(x['parts']) for x in text_checks) == 91
assert len(reused_text) == 12 and len(L['reused_images']) == 54 and len(native) == 3
current_map = load(R / 'expanded-v22/asked-fact-map.json')
facts = [(x['id'], fact) for x in current_map['questions'] for clause in x['requested_clauses'] for fact in clause['required_facts']]
assert len(facts) == len(C['required_fact_checks']) == 507
for i, (identity, fact) in enumerate(facts):
    f = C['required_fact_checks'][i]
    assert f['fact_index'] == i and f['question_id'] == identity and f['required_fact'] == fact
    assert f['required_fact_utf8_sha256'] == HB(fact.encode())
    assert all(f[k] == 'PASS' for k in ('actual_ask_check', 'source_correctness', 'present_in_fixed_key'))
for f in C['question_checks']:
    assert f['fixed_key'] == f['asked_fact_mapping'] == 'PASS' and f['all_requested_material_facts_checked']
    assert not f['finding_ids'] and f['missing_asked_fact_count'] == 0 and f['unasked_context_graded'] is False
for path, digest in C['input_hashes'].items():
    assert H(Path(path)) == digest
delta = load(B / 'coordinator-checks/spirit-v22-exact-map-delta.json')
assert delta['verified'] and H(REPO / 'rules/spirit-island.md') == delta['summary_sha256']
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'N': 172,
    'required_facts': 507, 'coverage_report_path': str(AP), 'coverage_report_sha256': H(AP),
    'ledger_sha256': H(LP), 'runtime_path': str(runtime), 'runtime_sha256_at_check': H(runtime),
    'actual_initial_spawn': prior['actual_initial_spawn'], 'actual_contexts': contexts,
    'current_manifest_delivery_record': start, 'completed_report_creation_boundary': boundary,
    'new_text_checks': text_checks, 'precise_source_reopens': source_reopens, 'new_native_checks': native,
    'reused_complete_primary_texts': reused_text, 'reused_native_image_count': 54,
    'original_actual_delivery_proof': str(prior_path), 'original_actual_delivery_proof_sha256': H(prior_path),
    'exact_map_delta_proof': str(B / 'coordinator-checks/spirit-v22-exact-map-delta.json'),
    'all507_actual_ask_source_and_fixed_key_checks_PASS': True,
    'qualification': 'Same initially fresh independent reviewer continued its own review. New current bank delivery and renewed decisions are separately verified; 12 complete primary texts and54 native observations are own-history reuse after exact hash/binding checks, not another fresh context or another54 new views. Original FAIL reports remain unchanged.',
    'limits': 'Current coverage/key/map/scope and stopping confirmation only. Full expanded blind-reader results, source audit, stamping and publication remain separate gates.'}
out = B / 'coordinator-checks/spirit-v22-completed12-current-coverage.json'
assert not out.exists()
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'N': 172, 'facts': 507, 'new_text_slices': 91, 'new_native_views': len(native), 'reused_primary_texts': 12, 'reused_native_views': 54, 'report': str(out)}))
