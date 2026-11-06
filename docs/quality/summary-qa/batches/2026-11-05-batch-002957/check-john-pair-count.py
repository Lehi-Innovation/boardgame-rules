"""Reconcile unique actual Luna dispatches with saved paired trials and results."""
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
import hashlib
import json
import subprocess

B = Path(__file__).resolve().parent
R = B.parents[4] / 'docs/quality/summary-qa/john-company-second-edition' / B.name
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
parent_id = '01a1aaa2-7c89-7c92-bca8-a89efc3fe4d7'
provenance = R / 'expanded-v13-complete-requested-scope/luna-final-stamped-iteration-01/source-auditor-terminal-runtime-provenance.json'
actors = [a for a in load(provenance)['records']
          if any(s.get('model') == 'gpt-6-luna' for s in a.get('settings', []))]
assert len({a['session_id'] for a in actors}) == len(actors)
paths = subprocess.run(['rg', '--files', '/mnt/c/Users/jonny/.codex/sessions'],
                       check=True, capture_output=True, text=True).stdout.splitlines()
parent = next(Path(p) for p in paths if p.endswith(parent_id + '.jsonl'))
dispatches = {}
for n, line in enumerate(parent.open(), 1):
    row = json.loads(line); p = row.get('payload', {})
    if row.get('type') == 'response_item' and p.get('type') == 'function_call' and p.get('name', '').endswith('spawn_agent'):
        a = p.get('arguments'); a = json.loads(a) if isinstance(a, str) else a
        if a.get('model') == 'gpt-6-luna':
            assert a['task_name'] not in dispatches
            dispatches[a['task_name']] = {'record': n, **{k: a.get(k) for k in ('task_name', 'model', 'reasoning_effort', 'fork_turns')}}
groups, model_checks = defaultdict(list), []
for actor in actors:
    runtime = Path(actor['runtime_source']); task = actor['agent'].rsplit('/', 1)[-1]
    contexts, identity = [], None
    for n, line in enumerate(runtime.open(), 1):
        row = json.loads(line); p = row.get('payload', {})
        if row.get('type') == 'session_meta':
            identity = {k: p.get(k) for k in ('id', 'agent_path', 'parent_thread_id')}
        elif row.get('type') == 'turn_context':
            contexts.append({'record': n, 'model': p.get('model'), 'effort': p.get('effort')})
    assert identity == {'id': actor['session_id'], 'agent_path': actor['agent'], 'parent_thread_id': parent_id}
    assert contexts and all(c['model'] == 'gpt-6-luna' and c['effort'] == 'high' for c in contexts)
    spawn = dispatches[task]
    assert spawn['reasoning_effort'] == 'high' and spawn['fork_turns'] == 'none'
    assert task.endswith(('_a', '_b'))
    groups[task.rsplit('_', 1)[0]].append({'side': task[-1], 'session_id': actor['session_id']})
    model_checks.append({'task': task, 'identity': identity, 'actual_contexts': contexts,
                         'actual_spawn': spawn, 'runtime_path': str(runtime), 'runtime_sha256_at_check': H(runtime)})
assert len(dispatches) == len(actors)
assert all(sorted(a['side'] for a in values) == ['a', 'b'] for values in groups.values())
pairs, fingerprints = [], set()
for a in sorted(R.rglob('reader-a.json')):
    b = a.with_name('reader-b.json')
    if not b.exists():
        continue
    result = a.with_name('results.json')
    fingerprint = (H(a), H(b))
    assert fingerprint not in fingerprints, 'Do not count archival copies as another trial'
    fingerprints.add(fingerprint)
    pairs.append({'directory': str(a.parent), 'raw_a_sha256': fingerprint[0], 'raw_b_sha256': fingerprint[1],
                  'results_present': result.exists(), 'results_sha256': H(result) if result.exists() else None})
completed = sum(p['results_present'] for p in pairs)
now = datetime.now(timezone.utc)
result = {'verified': True, 'checked_at_utc': now.isoformat(), 'actual_distinct_luna_readers': len(actors),
    'actual_paired_dispatches': len(groups), 'unique_saved_raw_pairs': len(pairs), 'saved_scored_pairs': completed,
    'paired_dispatches_not_yet_matched_by_saved_results': len(groups) - completed,
    'actual_reader_task_groups': dict(groups), 'actual_model_and_fresh_spawn_checks': model_checks,
    'unique_raw_result_pairs': pairs,
    'limits': 'Trial count reconciles actual unique paired Luna task stems, distinct raw pairs and saved result documents; it does not regrade historical answers. Live readers are checked only through this timestamp. Final exact-byte result/model/goal checks remain separate.'}
assert 0 <= completed <= len(pairs) <= len(groups)
out = B / 'coordinator-checks' / ('john-pair-count-' + now.strftime('%Y%m%dT%H%M%S%f') + '.json')
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ('verified', 'actual_distinct_luna_readers', 'actual_paired_dispatches',
                 'unique_saved_raw_pairs', 'saved_scored_pairs', 'paired_dispatches_not_yet_matched_by_saved_results')} | {'report': str(out)}))
