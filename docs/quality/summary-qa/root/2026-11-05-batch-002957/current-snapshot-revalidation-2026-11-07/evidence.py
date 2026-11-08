"""Append-only current-byte Root evidence; never edits canonical or old QA."""
from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import os
import sys

N = Path(__file__).resolve().parent
R = N.parent
ROOT = R.parents[4]
PAIR = os.environ.get('ROOT_QA_PAIR', 'iteration-01')
assert PAIR in ('iteration-01', 'iteration-02')
I = N / PAIR
READER_PREFIX = 'current18' if PAIR == 'iteration-01' else 'current19'
PARENT = '01a1aa9d-614e-7493-a3f2-715a8c52e03d'
TASKS = ['current18_reader_a', 'current18_reader_b', 'current18_pure_source_auditor', 'current18_neutral', 'current19_reader_a', 'current19_reader_b']

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def js(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def save(p, v):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    s = json.dumps(v, indent=2, ensure_ascii=False) + '\n'
    if p.exists() and p.read_text() != s:
        raise RuntimeError(f'Immutable evidence exists: {p}')
    if not p.exists():
        p.write_text(s)

def runtime():
    records = []
    for day in ('05', '06', '07', '08'):
        for p in (Path('/mnt/c/Users/jonny/.codex/sessions/2026/11') / day).glob('*.jsonl'):
            with p.open() as f:
                try:
                    first = json.loads(next(f))
                except (StopIteration, ValueError):
                    continue
                m = first.get('payload', {})
                if m.get('agent_path') not in ['/root/' + t for t in TASKS] or m.get('parent_thread_id') != PARENT:
                    continue
                turns = []
                for line in f:
                    d = json.loads(line)
                    if d.get('type') == 'turn_context':
                        turns.append({'timestamp': d.get('timestamp'), 'ordinal': d.get('ordinal'), **{k: d['payload'].get(k) for k in ('turn_id', 'model', 'effort', 'cwd')}})
                meta_excerpt = {'timestamp': first.get('timestamp'), 'ordinal': first.get('ordinal'), 'type': first.get('type'), 'payload': {k: m.get(k) for k in ('id', 'parent_thread_id', 'agent_path', 'thread_source', 'source', 'model_provider')}}
                records.append({'agent_path': m['agent_path'], 'session_id': m['id'], 'runtime_path': str(p), 'session_meta': meta_excerpt, 'turns': turns})
    parent = next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*' + PARENT + '.jsonl'))
    dispatches, parent_turns = [], []
    for line in parent.open():
        d = json.loads(line)
        p = d.get('payload', {})
        if d.get('type') == 'turn_context' and d.get('timestamp', '') >= '2026-11-07':
            parent_turns.append({'timestamp': d.get('timestamp'), 'ordinal': d.get('ordinal'), **{k: p.get(k) for k in ('turn_id', 'model', 'effort', 'cwd')}})
        if p.get('type') != 'function_call' or not any(t in p.get('name', '') for t in ('spawn_agent', 'followup_task')):
            continue
        a = p.get('arguments', {})
        a = json.loads(a) if isinstance(a, str) else a
        if a.get('task_name', '') not in TASKS and not any(a.get('target', '').endswith(t) for t in TASKS):
            continue
        message = a.get('message', '')
        dispatches.append({'timestamp': d.get('timestamp'), 'ordinal': d.get('ordinal'), 'tool': p.get('name'), 'arguments_without_message': {k: v for k, v in a.items() if k != 'message'}, 'message_storage': 'encrypted opaque body' if message.startswith('gAAAAA') else 'plaintext', 'runtime_message_sha256': hashlib.sha256(message.encode()).hexdigest()})
    return {'records': records, 'dispatches': dispatches, 'parent_runtime_path': str(parent), 'parent_current_turn_contexts': parent_turns, 'limits': 'Runtime encrypted message bodies cannot be compared with saved plaintext prompt files. Clear dispatch model/effort/fork settings and actual turn_contexts are independently retained. Instruction isolation, not filesystem jailing.'}

def checkpoint(side):
    p = I / f'reader-{side}.json'
    if not p.exists():
        return {'reader': side, 'count': 0}
    raw = json.loads(p.read_text())
    answers = raw['answers']
    count = len(answers)
    expected = json.loads((I / 'questions.json').read_text())['questions']
    assert [a['id'] for a in answers] == [q['id'] for q in expected[:count]]
    for old in sorted((I / 'checkpoints').glob(f'reader-{side}-*.json')):
        previous = json.loads(old.read_text())['answers']
        # Five-entry checkpoints captured mid-turn are drafts, preserved for
        # transparency. Completed ten-entry turns are immutable originals.
        if len(previous) % 10 == 0 or len(previous) == 81:
            assert answers[:len(previous)] == previous, f'Completed-turn answer changed: {old}'
    cp = I / 'checkpoints' / f'reader-{side}-{count:02}.json'
    save(cp, raw)
    guide = (I / 'summary-snapshot.md').read_text()
    quotes = [s['quotation'] for a in answers for s in a['source_passages']]
    bad = [n for n, q in enumerate(quotes) if not q or q not in guide]
    assert not bad, bad
    return {'reader': side, 'count': count, 'sha256': sha(cp), 'checkpoint': str(cp), 'all_completed_turn_entries_unchanged': True, 'mid_turn_drafts_preserved_separately': True, 'exact_nonempty_quotes': len(quotes)}

def delivery(side, out):
    spec = importlib.util.spec_from_file_location('old_delivery', R / 'audit_full_publisher_delivery.py')
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    rec = next(r for r in runtime()['records'] if r['agent_path'] == '/root/' + READER_PREFIX + '_reader_' + side)
    blocks, calls, images = helper.collect(Path(rec['runtime_path']), out)
    inputs = [helper.coverage(I / name, blocks, selector=lambda code, name=name: name in code) for name in ('summary-snapshot.md', 'questions.json')]
    assert not images
    report = {'agent_path': rec['agent_path'], 'runtime_path': rec['runtime_path'], 'read_calls': calls, 'inputs': inputs, 'status': 'PASS' if all(x['all_nonempty_lines_in_ordered_exact_blocks'] for x in inputs) else 'INCOMPLETE', 'method': 'Actual runtime input-read call/output pairs. JSON output transport decoded; otherwise exact ordered source lines, with only explicit declared line-number prefixes removed. Answer-writing calls excluded. Blank lines not required. Delivery is not cognitive-attention proof.'}
    save(out / 'delivery-audit.json', report)
    return {'reader': side, 'status': report['status'], 'missing': [(Path(x['path']).name, len(x['unmatched_nonempty_lines_in_ordered_blocks'])) for x in inputs]}

if __name__ == '__main__':
    if sys.argv[1] == 'runtime':
        result = runtime()
        if len(sys.argv) > 2:
            save(N / sys.argv[2], result)
        print(json.dumps({'actors': [{'agent': r['agent_path'], 'session': r['session_id'], 'turns': [[t['model'], t['effort']] for t in r['turns']]} for r in result['records']], 'dispatch_count': len(result['dispatches'])}))
    elif sys.argv[1] == 'checkpoint':
        print(json.dumps([checkpoint(s) for s in 'ab']))
    elif sys.argv[1] == 'delivery':
        print(json.dumps([delivery(s, I / ('reader-' + s + '-delivery-' + sys.argv[2])) for s in 'ab']))
