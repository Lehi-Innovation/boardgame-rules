"""Verify an independent Spirit Island source audit without exporting private context."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument('--audit', required=True)
ap.add_argument('--auditor', required=True)
args = ap.parse_args()
base = Path(__file__).resolve().parent
repo = base.parents[4]
run = repo / 'docs/quality/summary-qa/spirit-island' / base.name
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
resolve = lambda s: (repo / s).resolve()
audit_path = run / (args.audit + '.json')
audit = read(audit_path)
ledger = read(resolve(audit['artifacts']['read_ledger']))
visual = read(resolve(audit['artifacts']['visual_manifest']))
candidate = resolve(audit['candidate'])
assert audit['verdict'] == 'PASS' and not audit['findings']
assert audit['candidate_preserved'] is True
assert sha(candidate) == audit['candidate_sha256']
assert candidate.read_bytes() == (repo / 'rules/spirit-island.md').read_bytes()

paths = subprocess.run(['rg', '--files', '/mnt/c/Users/jonny/.codex/sessions'],
                       check=True, capture_output=True, text=True).stdout.splitlines()
def runtime_path(ident):
    matches = [Path(p) for p in paths if p.endswith(ident + '.jsonl')]
    assert len(matches) == 1
    return matches[0]

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

runtime = runtime_path(args.auditor)
calls, outputs, images, contexts, cutoffs = {}, [], [], [], []
identity = None
for ordinal, line in enumerate(runtime.open(), 1):
    record = json.loads(line)
    p = record.get('payload')
    if not isinstance(p, dict):
        continue
    if record.get('type') == 'session_meta':
        identity = {k: p.get(k) for k in ['id', 'parent_thread_id', 'agent_path']}
    elif record.get('type') == 'turn_context':
        contexts.append({'ordinal': ordinal, 'model': p.get('model'), 'effort': p.get('effort')})
    elif record.get('type') == 'response_item':
        typ = p.get('type')
        if typ in ['function_call', 'custom_tool_call']:
            body = p.get('arguments', p.get('input', ''))
            calls[p.get('call_id')] = {'ordinal': ordinal, 'body': body}
            if (isinstance(body, str) and audit_path.name in body and 'PASS' in body
                    and any(x in body for x in ['write_text', 'writeFile', 'apply_patch'])):
                cutoffs.append(ordinal)
        elif typ in ['function_call_output', 'custom_tool_call_output']:
            outputs.append((ordinal, p.get('call_id'), list(strings(p.get('output')))))
            blocks = p.get('output')
            if isinstance(blocks, list):
                images.extend({'ordinal': ordinal, 'call_id': p.get('call_id')}
                              for block in blocks if isinstance(block, dict)
                              and block.get('type') == 'input_image')
assert identity and identity['id'] == args.auditor
parent = '01a1ac01-c763-7bb1-901e-7458891630b8'
assert identity['parent_thread_id'] == parent
assert contexts and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in contexts)
task = identity['agent_path'].rsplit('/', 1)[-1]
dispatches = []
for ordinal, line in enumerate(runtime_path(parent).open(), 1):
    record = json.loads(line)
    p = record.get('payload', {})
    if (record.get('type') != 'response_item' or not isinstance(p, dict)
            or p.get('type') != 'function_call' or not p.get('name', '').endswith('spawn_agent')):
        continue
    options = p.get('arguments', {})
    options = json.loads(options) if isinstance(options, str) else options
    if options.get('task_name') == task:
        dispatches.append({k: options.get(k) for k in ['task_name', 'model', 'reasoning_effort', 'fork_turns']})
assert len(dispatches) == 1
assert dispatches[0] == {'task_name': task, 'model': 'gpt-6.1-sol', 'reasoning_effort': 'high', 'fork_turns': 'none'}
assert cutoffs, 'No source-report creation boundary found'
cutoff = min(cutoffs)

reads, ranges, lengths = [], {}, {}
assert ledger['source_delivery'] == audit['source_delivery']
assert len(ledger['reads']) == len(audit['source_delivery'])
for e in ledger['reads']:
    path = resolve(e['path'])
    assert sha(path) == e['source_sha256'], str(path)
    data = path.read_bytes().decode('utf-8')
    choices = [data, path.read_text()]
    start, end = e['start'], e['end']
    choices = [t for t in choices if len(t) == e['characters']
               and hashlib.sha256(t[start:end].encode()).hexdigest() == e['slice_sha256']]
    assert choices and e['truncated'] is False
    text = choices[0]
    assert 0 <= start < end <= len(text)
    expected = text[start:end]
    matches = [o for o, call, values in outputs if o < cutoff and call in calls
               and calls[call]['ordinal'] < o and any(expected in v for v in values)]
    assert matches, (str(path), start, end)
    ranges.setdefault(str(path), []).append((start, end))
    lengths[str(path)] = len(text)
    reads.append({'path': str(path), 'source_sha256': e['source_sha256'],
                  'start': start, 'end': end, 'slice_sha256': e['slice_sha256'],
                  'actual_pre_report_output_ordinals': matches})
for name, intervals in ranges.items():
    cursor = 0
    for start, end in sorted(intervals):
        assert start <= cursor, (name, cursor, start)
        cursor = max(cursor, end)
    assert cursor == lengths[name], (name, cursor, lengths[name])
assert len(ranges) == ledger['totals']['text_files']
assert len(reads) == ledger['totals']['slices']
for e in visual['visual_sources']:
    path = resolve(e['path'])
    if 'source_path' in e:
        assert sha(resolve(e['source_path'])) == e['source_sha256']
        assert sha(path) == e['sha256']
    else:
        assert sha(path) == e['source_sha256']
delivered_images = [x for x in images if x['ordinal'] < cutoff]
assert len(delivered_images) >= len(visual['visual_sources'])
assert visual['candidate_sha256'] == sha(candidate)
assert len(audit['checked_groups']) == 14

out = base / 'coordinator-checks' / ('spirit-' + args.audit + '-actual-delivery.json')
assert not out.exists(), 'Preserve earlier checks; version a new proof before rerunning'
proof = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
         'checker_script_sha256': sha(Path(__file__)), 'audit_path': str(audit_path),
         'audit_sha256': sha(audit_path), 'summary_sha256': sha(candidate),
         'auditor': identity, 'actual_turn_contexts_minimal': contexts,
         'actual_initial_spawn': dispatches[0], 'runtime_path': str(runtime),
         'runtime_sha256_at_check': sha(runtime), 'first_report_creation_ordinal': cutoff,
         'complete_actual_pre_report_text_reads': reads, 'text_file_count': len(ranges),
         'native_image_receipts': len(visual['visual_sources']),
         'actual_pre_report_image_outputs': delivered_images,
         'verdict': audit['verdict'], 'findings': audit['findings'],
         'limits': ['No blind-reader, coverage-stopping or publication approval is granted.',
                    'Full source-only task boundaries and semantic inspection are reviewed separately; this checks actual delivery and minimal model/fork provenance.',
                    'No private session, permission, profile or instruction bodies are copied into this proof.']}
out.write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps({'verified': True, 'proof': str(out), 'text_files': len(ranges),
                  'text_slices': len(reads), 'native_image_outputs': len(delivered_images)}))
