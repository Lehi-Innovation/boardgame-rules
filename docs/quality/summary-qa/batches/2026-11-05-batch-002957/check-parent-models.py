"""Retain actual game-chat model evidence without copying unrelated runtime data."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import subprocess

base = Path(__file__).parent
manifest = json.loads((base / 'manifest.json').read_text())
session_root = Path('/mnt/c/Users/jonny/.codex/sessions')
paths = subprocess.run(['rg', '--files', str(session_root)], check=True, capture_output=True, text=True).stdout.splitlines()
records = []
for game in manifest['games']:
    ident = game.get('thread_id')
    if not ident:
        continue
    matches = [Path(p) for p in paths if p.endswith(ident + '.jsonl')]
    assert len(matches) == 1, (game['slug'], 'expected one runtime record', len(matches))
    identity = None
    contexts = []
    for line_no, line in enumerate(matches[0].open(), 1):
        row = json.loads(line)
        payload = row.get('payload', {})
        if row.get('type') == 'session_meta':
            identity = {k: payload.get(k) for k in ['id', 'parent_thread_id', 'agent_path', 'model_provider']}
        elif row.get('type') == 'turn_context':
            contexts.append({'line': line_no, 'timestamp': row.get('timestamp'), 'model': payload.get('model'), 'effort': payload.get('effort')})
    assert identity and identity['id'] == ident
    assert contexts and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in contexts), (game['slug'], contexts)
    records.append({'game': game['game'], 'thread_id': ident, 'host_id': game['host_id'], 'session_path': str(matches[0]), 'session_metadata': identity, 'actual_turn_contexts': contexts, 'verified': True})
now = datetime.now(ZoneInfo('America/Phoenix'))
report = {'checked_at': now.isoformat(), 'scope': 'Actual game-chat parent model and effort. Reader and reviewer provenance is retained separately in each game evidence directory. Only identity/model fields were copied.', 'game_chats': records}
out = base / 'parent-model-provenance'
out.mkdir(exist_ok=True)
target = out / (now.strftime('%Y%m%dT%H%M%S%f') + '.json')
target.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'path': str(target), 'verified_game_chats': len(records), 'all_requested_models_and_efforts': True}))
