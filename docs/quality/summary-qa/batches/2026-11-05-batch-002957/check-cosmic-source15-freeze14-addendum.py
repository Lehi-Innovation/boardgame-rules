"""Bind source15's new freeze14 reading to its previously verified own-source union."""
import ast
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from pypdf import PdfReader

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
A = ROOT / 'docs/quality/summary-qa/cosmic-encounter' / B.name / 'source-review'
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
prior_path = B / 'coordinator-checks/cosmic-source15-freeze13-actual-delivery.json'
prior = load(prior_path)
audit_path, receipt_path = A / 'source-only-audit-15-freeze14.json', A / 'source-only-delivery-15-freeze14.json'
audit, receipt = load(audit_path), load(receipt_path)
assert audit['source_verdict'] == 'PASS' and not audit['demonstrated_errors'] and not audit['omissions']
assert len(audit['unresolved_sources']) == 2
assert audit['continuation_and_isolation']['fresh_independent_vote'] is False
summary = Path(receipt['summary']['path'])
assert H(summary) == receipt['summary']['sha256'] == audit['summary']['sha256']
assert H(A / 'source-only-audit-15-freeze13.json') == prior['audit_sha256']
for f in prior['full_text_inputs']:
    assert H(Path(f['path'])) == f['sha256']
for f in prior['original_native_alien_images']:
    assert H(Path(f['path'])) == f['sha256']
for f in prior['independently_reproduced_native_pdf_text_views']:
    assert H(Path(f['path'])) == f['pdf_sha256']
runtime = Path(prior['runtime'])
lines = runtime.read_bytes().splitlines(keepends=True)
# Recheck old actual payload-record hashes, not only the cached verifier label.
old_records = []
for f in prior['full_text_inputs']:
    for part in f['parts']:
        old_records.extend(part['actual_output_records'])
for f in prior['original_native_alien_images']:
    old_records.extend({'record': x['record'], 'sha256': x['record_sha256']} for x in f['actual_deliveries'])
for f in prior['independently_reproduced_native_pdf_text_views']:
    for part in f['parts']:
        old_records.extend(part['actual_output_records'])
for old in old_records:
    assert HB(lines[old['record'] - 1]) == old['sha256']
tree = ast.parse((B / 'check-spirit-source09-delivery.py').read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'strings')
ns = {'json': json}
exec(compile(ast.Module(body=[fn], type_ignores=[]), '<public-tool-strings>', 'exec'), ns)
lower = prior['current_completion_record']
outputs, terminals, contexts, calls = [], [], [], []
for n, line in enumerate(lines, 1):
    row = json.loads(line)
    p = row.get('payload', {})
    if row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if n <= lower:
        continue
    if row.get('type') == 'event_msg' and p.get('type') == 'task_complete':
        terminals.append(n)
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ['function_call_output', 'custom_tool_call_output']:
        outputs.append((n, list(ns['strings'](p.get('output')))))
    elif p.get('type') in ['function_call', 'custom_tool_call']:
        t = p.get('input', p.get('arguments', ''))
        assert not re.search(r'(?:get_agent_info|list_agents|read_thread|wait_threads|web__run)\s*\(', t)
        assert not any(s in t for s in ['questions.json', 'answer-key.json', 'reader-a.json',
            'reader-b.json', 'actual-question-scope.json', 'source-corrections-14.json'])
        calls.append({'record': n, 'name': p.get('name'), 'sha256': HB(line)})
assert contexts and all(c['model'] == 'gpt-6.1-sol' and c['effort'] == 'high' for c in contexts)
assert terminals
upper = max(terminals)

def actual(part):
    found = [n for n, values in outputs if n < upper and any(
        part in v or json.dumps(part, ensure_ascii=False)[1:-1] in v for v in values)]
    assert found
    return [{'record': n, 'sha256': HB(lines[n-1])} for n in found]

text, cursor, parts = summary.read_text(), 0, []
for chunk in receipt['summary']['chunks']:
    a, z = chunk['start'], chunk['end']
    assert a == cursor and a < z <= len(text) and HB(text[a:z].encode()) == chunk['chunk_sha256']
    parts.append({'start': a, 'end': z, 'sha256': chunk['chunk_sha256'], 'actual_records': actual(text[a:z])})
    cursor = z
assert cursor == len(text) and len(parts) == 10
pdf_views = []
for view in receipt['new_primary_native_text_spot_checks']:
    path = Path(view['path'])
    native = PdfReader(path).pages[view['printed_page'] - 1].extract_text()
    assert len(native) == view['chars'] and HB(native.encode()) == view['sha256']
    a, z = view['start'], view['end']
    assert HB(native[a:z].encode()) == view['chunk_sha256']
    pdf_views.append({'path': str(path), 'pdf_sha256': H(path), 'printed_page': view['printed_page'],
                      'native_text_sha256': view['sha256'], 'start': a, 'end': z,
                      'actual_records': actual(native[a:z])})
assert len(pdf_views) == 1 and pdf_views[0]['printed_page'] == 14
result = {'verified_delivery_only': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'auditor': prior['source_auditor'], 'runtime': str(runtime), 'runtime_sha256_at_check': H(runtime),
          'initially_fresh_model_provenance_reused': True, 'all_current_contexts': contexts,
          'prior_verified_union': str(prior_path), 'prior_verified_union_sha256': H(prior_path),
          'old_actual_public_records_rechecked': len(old_records), 'old_primary_and_native_hashes_current': True,
          'new_full_summary_path': str(summary), 'new_full_summary_sha256': H(summary),
          'new_full_summary_parts': parts, 'new_native_pdf_text_views': pdf_views,
          'prior_completion_record': lower, 'current_completion_record': upper,
          'new_public_tool_call_trace': calls, 'audit_path': str(audit_path), 'audit_sha256': H(audit_path),
          'receipt_path': str(receipt_path), 'receipt_sha256': H(receipt_path),
          'unresolved_authority_gaps': audit['unresolved_sources'],
          'limits': 'Same initially fresh pure author, own-source continuation; not a fresh vote or new50-image inspection. Prior complete sources/50 originals/five selected PDF text views and actual record hashes remain valid; new entire freeze14 body ten ranges and native rulebookp14 text are independently verified after prior completion. No native PDF raster claim. Source accuracy PASS remains scoped by the two reported authority gaps and unanswered human requests. Full reader167 pair03, source readiness, stamping and publication remain separate.'}
out = B / 'coordinator-checks/cosmic-source15-freeze14-actual-addendum.json'
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified_delivery_only': True, 'old_record_bindings': len(old_records),
                  'new_summary_ranges': len(parts), 'new_native_text_pages': len(pdf_views), 'proof': str(out)}))
