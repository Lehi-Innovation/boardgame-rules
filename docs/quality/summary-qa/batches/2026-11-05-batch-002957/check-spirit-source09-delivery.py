"""Verify an independent Spirit Island source audit without exporting private context."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument('--audit', required=True)
ap.add_argument('--auditor', required=True)
args = ap.parse_args()
assert args.audit == 'source-audit-final-09-completed', 'Initial09 omitted an assigned publisher source and is preserved as incomplete; verify only the separate completed artifact.'
base = Path(__file__).resolve().parent
repo = base.parents[4]
run = repo / 'docs/quality/summary-qa/spirit-island' / base.name
read = lambda p: json.loads(p.read_text())
def sha(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for piece in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(piece)
    return value.hexdigest()
resolve = lambda s: (repo / s).resolve()
audit_path = run / (args.audit + '.json')
audit = read(audit_path)
ledger = read(run / (args.audit + '-read-ledger.json'))
visual = read(run / (args.audit + '-visual-manifest.json'))
candidate = resolve(audit['candidate_path'])
assert audit['verdict'] == 'PASS' and not audit['findings']
# Exact current candidate bytes independently prove preservation despite schema alias.
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
        if value.get('type') in ('input_image', 'image'):
            return
        for v in value.values():
            yield from strings(v, depth + 1)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v, depth + 1)


def literal_image_paths(code):
    """Resolve literal strings/arrays/templates only; never execute tool code."""
    quoted = r'"(?:\\.|[^"\\])*"'
    constants = {m[1]: json.loads(m[2]) for m in re.finditer(r'const\s+(\w+)\s*=\s*(' + quoted + r')\s*;', code)}
    environments = [constants]
    for m in re.finditer(r'for\s*\(\s*const\s+(\w+)\s+of\s+(\[[^\]]*\])\s*\)', code):
        values = json.loads(m[2])
        assert all(isinstance(v, (str, int)) for v in values)
        environments += [dict(constants, **{m[1]: value}) for value in values]
    paths = {json.loads(m[1]) for m in re.finditer(r'path\s*:\s*(' + quoted + r')\s*[,}]', code)}
    for env in environments:
        for m in re.finditer(r'path\s*:\s*(\w+)\s*\+\s*(\w+)\s*[,}]', code):
            if isinstance(env.get(m[1]), str) and isinstance(env.get(m[2]), str):
                paths.add(env[m[1]] + env[m[2]])
        for m in re.finditer(r'path\s*:\s*(\w+)\s*[,}]', code):
            if isinstance(env.get(m[1]), str):
                paths.add(env[m[1]])
        for m in re.finditer(r'path\s*:\s*`([^`]+)`', code):
            value = m[1]
            for name, replacement in env.items():
                value = value.replace('${' + name + '}', str(replacement))
                if isinstance(replacement, int):
                    value = re.sub(r'\$\{String\(' + re.escape(name) + r'\)\.padStart\(2,[\x27\x22]0[\x27\x22]\)\}', f'{replacement:02d}', value)
            if '${' not in value:
                paths.add(value)
    return {str(resolve(path)) for path in paths}
runtime = runtime_path(args.auditor)
calls, outputs, images, contexts, cutoffs, terminal = {}, [], [], [], [], []
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
    elif record.get('type') == 'event_msg' and p.get('type') == 'task_complete':
        terminal.append(ordinal)
    elif record.get('type') == 'response_item':
        typ = p.get('type')
        if typ in ['function_call', 'custom_tool_call']:
            body = p.get('arguments', p.get('input', ''))
            calls[p.get('call_id')] = {'ordinal': ordinal, 'body': body}
            assert not any(t in body for t in ('questions.json', 'answer-key.json', 'reader-a.json', 'reader-b.json', 'source-audit-final-08.json', 'coverage-review-12.json'))
            assert not any(t in p.get('name', '') for t in ('collaboration', 'thread'))
            if (isinstance(body, str) and audit_path.stem in body and 'PASS' in body
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
assert terminal and max(terminal) > cutoff, 'Auditor final integrity/terminal completion still pending'

reads, ranges, lengths = [], {}, {}
receipt_fields = ('path', 'start', 'end', 'source_sha256', 'slice_sha256', 'truncated')
# Report receipts omit only size/output-cap metadata retained in the ledger.
assert [tuple(e[k] for k in receipt_fields) for e in ledger['source_delivery']] == [tuple(e[k] for k in receipt_fields) for e in audit['source_delivery']]
assert len(ledger['source_delivery']) == len(audit['source_delivery'])
for e in ledger['source_delivery']:
    path = resolve(e['path'])
    assert sha(path) == e['source_sha256'], str(path)
    data = path.read_bytes().decode('utf-8')
    choices = [data, path.read_text()]
    start, end = e['start'], e['end']
    choices = [t for t in choices if len(t) == e['character_length']
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
assert len(ranges) == len(ledger['text_inputs'])
assert len(reads) == len(ledger['source_delivery'])
for e in visual['images']:
    path = resolve(e['path'])
    assert sha(path) == e['sha256']
    if 'source_pdf' in e:
        assert sha(resolve(e['source_pdf'])) == e['source_pdf_sha256']
delivered_images = [x for x in images if x['ordinal'] < cutoff]
assert len(delivered_images) >= len(visual['images'])
grouped = Counter(x['call_id'] for x in delivered_images)
named_images = []
for call_id, count in grouped.items():
    paths = literal_image_paths(calls[call_id]['body'])
    assert len(paths) == count, (calls[call_id]['ordinal'], count, sorted(paths))
    named_images.extend({'path': path, 'call_ordinal': calls[call_id]['ordinal'], 'output_ordinals': [x['ordinal'] for x in delivered_images if x['call_id'] == call_id]} for path in paths)
assert {str(resolve(e['path'])) for e in visual['images']} <= {e['path'] for e in named_images}
assert sha(candidate) == audit['candidate_sha256']
assert audit['checked_groups']

out = base / 'coordinator-checks' / ('spirit-' + args.audit + '-actual-delivery.json')
assert not out.exists(), 'Preserve earlier checks; version a new proof before rerunning'
proof = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
         'checker_script_sha256': sha(Path(__file__)), 'audit_path': str(audit_path),
         'audit_sha256': sha(audit_path), 'summary_sha256': sha(candidate),
         'auditor': identity, 'actual_turn_contexts_minimal': contexts,
         'actual_initial_spawn': dispatches[0], 'runtime_path': str(runtime),
         'runtime_sha256_at_check': sha(runtime), 'first_report_creation_ordinal': cutoff,
         'complete_actual_pre_report_text_reads': reads, 'text_file_count': len(ranges),
         'native_image_receipts': len(visual['images']),
         'actual_pre_report_image_outputs': delivered_images,
         'individually_named_pre_report_images': named_images,
         'actual_terminal_event_ordinals': terminal,
         'verdict': audit['verdict'], 'findings': audit['findings'],
         'limits': ['No blind-reader, coverage-stopping or publication approval is granted.',
                    'Full source-only task boundaries and semantic inspection are reviewed separately; this checks actual delivery and minimal model/fork provenance.',
                    'No private session, permission, profile or instruction bodies are copied into this proof.']}
out.write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps({'verified': True, 'proof': str(out), 'text_files': len(ranges),
                  'text_slices': len(reads), 'native_image_outputs': len(delivered_images)}))
