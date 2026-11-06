"""Verify the scoped source auditor's actual delivered text and native images."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

ap = argparse.ArgumentParser()
ap.add_argument('--audit', required=True)
ap.add_argument('--auditor', required=True)
args = ap.parse_args()
base = Path(__file__).resolve().parent
repo = base.parents[4]
run = repo / 'docs/quality/summary-qa/john-company-second-edition' / base.name
directory = run / args.audit
assert directory.parent == run
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
report_path = directory / 'source-audit.json'
report = read(report_path)
receipt = read(directory / 'source-read-record.json')
provenance = read(run / 'model-provenance.json')
actor = next(x for x in provenance['records'] if x['session_id'] == args.auditor)
runtime = Path(actor['runtime_source'])

def strings(value, depth=0):
    if depth > 9:
        return
    if isinstance(value, str):
        yield value
        try:
            parsed = json.loads(value)
        except (ValueError, TypeError):
            return
        if parsed != value:
            yield from strings(parsed, depth + 1)
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings(v, depth + 1)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v, depth + 1)

calls, outputs, image_outputs, forbidden = {}, [], [], []
cutoffs = []
for ordinal, line in enumerate(runtime.open(), 1):
    record = json.loads(line)
    p = record.get('payload')
    if record.get('type') != 'response_item' or not isinstance(p, dict):
        continue
    typ = p.get('type')
    if typ in ['function_call', 'custom_tool_call']:
        body = p.get('arguments', p.get('input', ''))
        calls[p.get('call_id')] = ordinal
        if not isinstance(body, str):
            continue
        for name in ['questions.json', 'answer-key.json', 'reader-a.json',
                     'reader-b.json', 'grades.json', 'results.json']:
            if name in body:
                forbidden.append({'ordinal': ordinal, 'filename': name})
        if ('source-audit.json' in body and 'verdict' in body
                and any(x in body for x in ['write_text', 'writeFile', 'apply_patch'])):
            cutoffs.append(ordinal)
    elif typ in ['function_call_output', 'custom_tool_call_output']:
        outputs.append((ordinal, p.get('call_id'), list(strings(p.get('output')))))
        blocks = p.get('output')
        if isinstance(blocks, list):
            image_outputs.extend({'ordinal': ordinal, 'call_id': p.get('call_id')}
                                 for block in blocks if isinstance(block, dict)
                                 and block.get('type') == 'input_image')
assert cutoffs, 'No source report creation boundary found'
cutoff = min(cutoffs)
assert not forbidden, forbidden

manifest = read(directory / 'manifest.json')
checked_hashes = []
for e in manifest['entries']:
    path = Path(e['path'])
    assert sha(path) == e['sha256'], str(path)
    checked_hashes.append({'path': str(path), 'sha256': e['sha256']})

actual_reads, covered = [], {}
for e in receipt['text_reads']:
    path = Path(e['path'])
    assert sha(path) == e['sha256']
    lines = path.read_bytes().decode('utf-8').split('\n')
    start, end = e['start_physical_LF'], e['end_physical_LF']
    assert len(lines) == e['physical_LF_lines']
    assert 1 <= start <= end <= len(lines)
    expected = '\n'.join(f'{n}: {lines[n-1]}' for n in range(start, end + 1))
    matches = [(o, call) for o, call, values in outputs if o < cutoff
               and call in calls and calls[call] < o
               and any(expected in v for v in values)]
    assert matches, (str(path), start, end)
    covered.setdefault(str(path), set()).update(range(start, end + 1))
    actual_reads.append({'path': str(path), 'sha256': e['sha256'],
                         'start_physical_LF': start, 'end_physical_LF': end,
                         'runtime_ordinals': [o for o, _ in matches],
                         'complete_claimed_text_delivered_before_report': True})

snapshot = directory / 'summary-snapshot.md'
assert set(range(1, len(snapshot.read_bytes().decode('utf-8').split('\n')) + 1)) <= covered[str(snapshot)]
rules = repo / 'extracted/john-company-second-edition-rules.txt'
assert set(range(1, 3017)) <= covered[str(rules)], 'Complete multiplayer core text required'
assert set(range(3252, 3307)) <= covered[str(rules)], 'Edition-identification text required'
images = receipt['native_visual_reads']
for image in images:
    assert image['visually_checked'] is True
    if 'source' in image:
        assert sha(Path(image['source'])) == image['source_sha256']
        assert sha(Path(image['derivative'])) == image['derivative_sha256']
    else:
        assert sha(Path(image['path'])) == image['sha256']
delivered_images = [x for x in image_outputs if x['ordinal'] < cutoff]
assert len(delivered_images) >= len(images), (len(delivered_images), len(images))
assert report['snapshot_sha256'] == sha(snapshot) == manifest['candidate_sha256']
verdicts = report['machine_verdicts']
assert verdicts['official_claims'] == verdicts['human_interpretation_fidelity'] == 'PASS'
assert verdicts['overall_scoped_result'] == 'PASS' and verdicts['scoped_signoff'] is True
assert verdicts['unqualified_independently_verified_official_core_signoff'] is False
assert verdicts['publisher_email_independently_verified'] is False
assert not report['findings']

out = base / 'coordinator-checks' / f'john-{args.audit}-actual-delivery.json'
assert not out.exists(), 'Preserve the prior proof; choose a new version before rerunning'
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'checker_script_sha256': sha(Path(__file__)), 'audit_path': str(report_path),
          'audit_sha256': sha(report_path), 'auditor_id': args.auditor,
          'summary_sha256': sha(snapshot), 'runtime_path': str(runtime),
          'runtime_sha256_at_check': sha(runtime), 'first_report_creation_ordinal': cutoff,
          'actual_text_reads': actual_reads, 'source_and_artifact_hashes': checked_hashes,
          'actual_native_image_outputs': delivered_images,
          'expected_native_visual_receipts': len(images),
          'machine_verdicts': verdicts,
          'limits': ['Scope includes the explicitly accepted user interpretation; publisher email not independently verified.',
                     'Model, initial fresh-context request and source-only task delivery require separate checks.',
                     'The native-image count and hashed derivative lineage corroborate the independent semantic inspection; they do not replace it.',
                     'No blind-reader or publication approval is granted by this source-delivery check.']}
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'proof': str(out), 'text_reads': len(actual_reads),
                  'native_image_outputs': len(delivered_images), 'scope': 'user-qualified'}))
