"""Check original session metadata and parent fresh-context spawn settings."""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('parent')
p.add_argument('agents', nargs='+', help='session-id=model')
a = p.parse_args()
root = Path('/mnt/c/Users/jonny/.codex/sessions')
def events(session):
    files = list(root.rglob('*' + session + '.jsonl'))
    assert len(files) == 1, (session, files)
    # JSONL records are separated by LF. Unicode NEL/U+2028 may occur inside
    # valid JSON strings and must not be treated as record boundaries.
    return files[0], [json.loads(line) for line in files[0].read_text().split('\n') if line]
parent_path, parent = events(a.parent)
spawns = []
for e in parent:
    d = e.get('payload', {})
    if d.get('type') == 'function_call' and d.get('name') == 'spawn_agent':
        z = json.loads(d['arguments'])
        spawns.append({k: z.get(k) for k in ['task_name', 'model', 'reasoning_effort', 'fork_turns']})
out = []
for spec in a.agents:
    session, model = spec.split('=')
    path, ev = events(session)
    meta = next(e['payload'] for e in ev if e['type'] == 'session_meta')
    source = meta['source']['subagent']['thread_spawn']
    assert source['parent_thread_id'] == a.parent
    task = source['agent_path'].rsplit('/', 1)[-1]
    settings = [s for s in spawns if s['task_name'] == task]
    assert len(settings) == 1, (task, settings)
    assert settings[0]['fork_turns'] == 'none'
    assert settings[0]['model'] == model and settings[0]['reasoning_effort'] == 'high'
    contexts = [e['payload'] for e in ev if e['type'] == 'turn_context']
    assert contexts and all(c.get('model') == model and c.get('effort') == 'high' for c in contexts)
    calls = []
    for e in ev:
        d = e.get('payload', {})
        if d.get('type') in ['function_call', 'custom_tool_call']:
            # Record executable tool inputs, excluding encrypted task payloads.
            if d.get('name') in ['exec', 'exec_command', 'functions.exec', 'functions.exec_command']:
                calls.append({'name': d['name'], 'input': d.get('input', d.get('arguments'))})
    out.append({'session_id': session, 'runtime_path': str(path), 'task': task,
                'actual_contexts': [{'model': c['model'], 'effort': c['effort']} for c in contexts],
                'parent_spawn': settings[0], 'executable_tool_calls': calls})
print(json.dumps({'parent_runtime_path': str(parent_path), 'agents': out,
 'limit': 'Task bodies are encrypted; no claim to recover delivered prompts. Context isolation is prompt-based, not OS enforcement.'}, indent=2))
