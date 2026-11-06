"""Independently check final QA agents against actual local runtime records."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse
import hashlib
import json
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--slug', required=True)
parser.add_argument('--phase', required=True)
parser.add_argument('--reader', action='append', required=True)
parser.add_argument('--auditor', required=True)
parser.add_argument('--reviewer', action='append', default=[])
args = parser.parse_args()
assert re.fullmatch(r'[a-z0-9_-]+', args.phase)
assert len(args.reader) == 2
requested = [(ident, 'reader', 'gpt-6-luna') for ident in args.reader]
requested += [(args.auditor, 'source-auditor', 'gpt-6.1-sol')]
requested += [(ident, 'reviewer', 'gpt-6.1-sol') for ident in args.reviewer]
assert len({row[0] for row in requested}) == len(requested)
assert all(re.fullmatch(r'[0-9a-f-]{36}', row[0]) for row in requested)
base = Path(__file__).parent
manifest = json.loads((base / 'manifest.json').read_text())
game = next(row for row in manifest['games'] if row['slug'] == args.slug)
paths = subprocess.run(['rg', '--files', '/mnt/c/Users/jonny/.codex/sessions'], check=True, capture_output=True, text=True).stdout.splitlines()

def runtime_path(ident):
    matches = [Path(p) for p in paths if p.endswith(ident + '.jsonl')]
    assert len(matches) == 1, (ident, len(matches))
    return matches[0]

dispatches = []
for line_no, line in enumerate(runtime_path(game['thread_id']).open(), 1):
    row = json.loads(line)
    payload = row.get('payload', {})
    if row.get('type') != 'response_item' or payload.get('type') != 'function_call' or not payload.get('name', '').endswith('spawn_agent'):
        continue
    options = payload.get('arguments', {})
    if isinstance(options, str):
        options = json.loads(options)
    message = options.get('message', '')
    dispatches.append({'line': line_no, 'timestamp': row.get('timestamp'), 'task_name': options.get('task_name'), 'fork_turns': options.get('fork_turns'), 'model': options.get('model'), 'reasoning_effort': options.get('reasoning_effort'), 'message_storage': 'encrypted opaque body' if message.startswith('gAAAAA') else 'plaintext', 'message_sha256': hashlib.sha256(message.encode()).hexdigest()})

records = []
for ident, role, model in requested:
    path = runtime_path(ident)
    metadata = None
    contexts = []
    for line_no, line in enumerate(path.open(), 1):
        row = json.loads(line)
        payload = row.get('payload', {})
        if row.get('type') == 'session_meta':
            metadata = {key: payload.get(key) for key in ['id', 'parent_thread_id', 'agent_path', 'model_provider']}
        elif row.get('type') == 'turn_context':
            contexts.append({'line': line_no, 'timestamp': row.get('timestamp'), 'model': payload.get('model'), 'effort': payload.get('effort')})
    assert metadata and metadata['id'] == ident
    assert metadata['parent_thread_id'] == game['thread_id'], metadata
    assert contexts and all(x['model'] == model and x['effort'] == 'high' for x in contexts), (ident, contexts)
    task_name = metadata['agent_path'].rsplit('/', 1)[-1]
    matches = [x for x in dispatches if x['task_name'] == task_name]
    assert len(matches) == 1, (ident, task_name, matches)
    dispatch = matches[0]
    assert dispatch['fork_turns'] == 'none' and dispatch['model'] == model and dispatch['reasoning_effort'] == 'high', dispatch
    records.append({'session_id': ident, 'role': role, 'runtime_path': str(path), 'runtime_sha256_at_check': hashlib.sha256(path.read_bytes()).hexdigest(), 'identity': metadata, 'actual_turn_contexts': contexts, 'actual_spawn_request': dispatch, 'verified': True})

now = datetime.now(ZoneInfo('America/Phoenix'))
report = {'checked_at': now.isoformat(), 'slug': args.slug, 'phase': args.phase, 'game_chat_id': game['thread_id'], 'distinct_agent_count': len(records), 'verified': True, 'records': records, 'limits': 'This verifies actual model/effort, assigned parent, distinct sessions, and explicit fresh-context spawn requests. It does not grade answers or establish allowed-file delivery. Saved plaintext prompts and delivery evidence are checked separately. Opaque runtime dispatch messages are hashed, without claiming plaintext-to-ciphertext equality.'}
out = base / 'coordinator-runtime-model-checks'
out.mkdir(exist_ok=True)
target = out / (args.slug + '-' + args.phase + '-' + now.strftime('%Y%m%dT%H%M%S%f') + '.json')
target.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'verified': True, 'agents': len(records), 'report': str(target)}))
