"""Verify actual original-source delivery for the independently audited stamp."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

B = Path(__file__).resolve().parent
REPO = B.parents[4]
R = REPO / 'docs/quality/summary-qa/john-company-second-edition' / B.name
D = R / 'final-stamped-source-audit-01'
IT = R / 'expanded-v13-complete-requested-scope/luna-final-stamped-iteration-01'
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text())
audit_path = D / 'source-audit.json'
audit, reads, manifest = load(audit_path), load(D / 'source-read-record.json'), load(D / 'manifest.json')
assert audit['verdict'] == 'PASS' and not audit['findings'] and not audit['unresolved_findings']
assert audit['machine_verdicts'] == {'official_claims': 'PASS', 'human_interpretation_fidelity': 'PASS',
    'overall_scoped_result': 'PASS', 'scoped_signoff': True}
assert audit['authority_qualification']['publisher_email_independently_inspected'] is False
assert audit['authority_qualification']['unqualified_independently_verified_official_only_signoff'] is False
candidate = Path(manifest['candidate']['path'])
assert H(candidate) == audit['candidate_sha256'] == manifest['candidate']['sha256']
assert candidate.read_bytes() == (REPO / 'rules/john-company-second-edition.md').read_bytes()
for entry in manifest['originals']:
    p = Path(entry['path'])
    assert H(p) == entry['sha256'] and p.stat().st_size == entry['bytes']
actor = next(x for x in load(IT / 'reader-and-source-dispatch-record.json')['actors']
             if x['session_id'] == '01a1b17d-ec85-7a01-8175-22d4430ab94b')
runtime = Path(actor['runtime_source'])


def strings(value, depth=0):
    if depth > 10:
        return
    if isinstance(value, str):
        yield value
        try:
            v = json.loads(value)
        except ValueError:
            return
        if v != value:
            yield from strings(v, depth + 1)
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings(v, depth + 1)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v, depth + 1)


outputs, images, calls, terminal, contexts = [], [], [], [], []
for n, line in enumerate(runtime.open(), 1):
    row = json.loads(line); p = row.get('payload', {})
    if row.get('type') == 'turn_context':
        contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    if row.get('type') == 'event_msg' and p.get('type') == 'task_complete':
        terminal.append(n)
    if row.get('type') != 'response_item':
        continue
    if p.get('type') in ('custom_tool_call', 'function_call'):
        text = p.get('input', p.get('arguments', ''))
        assert isinstance(text, str)
        assert not any(s in text for s in ('questions.json', 'answer-key.json', 'reader-a.json', 'reader-b.json',
            'grading-results.json', 'grades-same-entry.json', 'source-audit-18/source-audit.json'))
        calls.append({'record': n, 'name': p.get('name'), 'call_id': p['call_id'],
                      'input_sha256': hashlib.sha256(text.encode()).hexdigest(),
                      'nested_tools': sorted(set(re.findall(r'tools\.([\w]+)', text)))})
    elif p.get('type') in ('custom_tool_call_output', 'function_call_output'):
        outputs.append((n, list(strings(p.get('output')))))
        images.extend({'record': n, 'call_id': p['call_id']} for block in p.get('output', [])
                      if isinstance(block, dict) and block.get('type') == 'input_image')
assert terminal and contexts and all(c['model'] == 'gpt-6.1-sol' and c['effort'] == 'high' for c in contexts)
end = max(terminal)
receipts, coverage = [], {}
for e in reads['reads']:
    path = Path(e['path'])
    assert H(path) == e['sha256']
    # The auditor's disclosed read_text transport normalizes CRLF, with raw-byte SHA retained.
    lines = path.read_text().split('\n')
    assert len(lines) == e['total_lf']
    a, z = e['start_lf'], e['end_lf']
    literal = '\n'.join(f'{i}: {lines[i - 1]}' for i in range(a, z + 1))
    found = [n for n, values in outputs if n < end and any(literal in text for text in values)]
    assert found, (str(path), a, z)
    coverage.setdefault(str(path), set()).update(range(a, z + 1))
    receipts.append({'path': str(path), 'start_lf': a, 'end_lf': z, 'actual_output_records': found,
                     'sha256': e['sha256'], 'complete_claimed_text_received': True})
assert set(range(1, 500)) <= coverage[str(candidate)]
assert set(range(1, 3016)) <= coverage[str(REPO / 'extracted/john-company-second-edition-rules.txt')]
assert set(range(3290, 3307)) <= coverage[str(REPO / 'extracted/john-company-second-edition-rules.txt')]
for e in reads['native_renders']:
    assert H(Path(e['original'])) == e['original_sha256']
    assert H(Path(e['derivative'])) == e['derivative_sha256']
for e in reads['visual_inspections']:
    assert H(Path(e['original'])) == e['original_sha256']
    assert H(Path(e['derivative'])) == e['derivative_sha256']
assert len(images) >= len(reads['visual_inspections'])
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
    'audit_path': str(audit_path), 'audit_sha256': H(audit_path), 'report_version': audit['report_version'],
    'summary_sha256': H(candidate), 'auditor_id': actor['session_id'], 'runtime_path': str(runtime),
    'runtime_sha256_at_check': H(runtime), 'actual_contexts': contexts, 'terminal_record': end,
    'actual_text_reads': receipts, 'actual_native_image_outputs': images,
    'native_visual_inspection_receipts': len(reads['visual_inspections']), 'native_render_lineage_checks': len(reads['native_renders']),
    'authority_qualification': audit['authority_qualification'], 'tool_call_hash_projection': calls,
    'rendering_environment': reads['rendering_environment'],
    'limits': ['Final source report supersedes its preserved v1; text and image completion is bound to actual terminal audit, not falsely to an earlier draft report.',
               'Scope is explicitly user-qualified, without independently verified publisher email.',
               'Initial fresh spawn and actual models are independently checked in the stamped-source model checkpoint.',
               'Literal transport and hashed native derivatives corroborate the independent semantic verdict; no reader or publication signoff is granted.']}
out = B / 'coordinator-checks/john-final-stamped-source-audit-01-actual-delivery.json'
assert not out.exists()
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'text_reads': len(receipts), 'native_outputs': len(images), 'report': str(out)}))
