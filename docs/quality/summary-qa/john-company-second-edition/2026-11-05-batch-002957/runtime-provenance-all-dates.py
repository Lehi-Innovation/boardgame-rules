"""Read actual child-session metadata across dates; never infer terminal status."""
from collections import Counter
from pathlib import Path
import datetime
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parent
SESSION_ROOT = Path('/mnt/c/Users/jonny/.codex/sessions')
PARENT_ID = '01a1aaa2-7c89-7c92-bca8-a89efc3fe4d7'


def collect(session_root=SESSION_ROOT, parent_id=PARENT_ID):
    records, discovery_issues = [], []
    for path in sorted(Path(session_root).rglob('*.jsonl')):
        try:
            with path.open('rb') as handle:
                first = handle.readline()
            initial = json.loads(first)
        except (OSError, ValueError) as error:
            discovery_issues.append(dict(path=str(path), issue='metadata unreadable', error_type=type(error).__name__))
            continue
        if not isinstance(initial, dict):
            discovery_issues.append(dict(path=str(path), issue='first event is not a JSON object'))
            continue
        if initial.get('type') != 'session_meta':
            discovery_issues.append(dict(path=str(path), issue='first event is not session_meta'))
            continue
        meta = initial.get('payload', {})
        if not isinstance(meta, dict):
            discovery_issues.append(dict(path=str(path), issue='session metadata payload is not an object'))
            continue
        source = meta.get('source', {})
        if isinstance(source, str):
            continue  # Non-child sessions may name the host directly, e.g. "cli".
        if not isinstance(source, dict):
            discovery_issues.append(dict(path=str(path), issue='session source metadata is not an object or host string'))
            continue
        subagent = source.get('subagent', {})
        if not isinstance(subagent, dict):
            discovery_issues.append(dict(path=str(path), issue='subagent metadata is not an object'))
            continue
        spawn = subagent.get('thread_spawn', {})
        if not isinstance(spawn, dict):
            discovery_issues.append(dict(path=str(path), issue='thread_spawn metadata is not an object'))
            continue
        if spawn.get('parent_thread_id') != parent_id:
            continue
        if any(not isinstance(value, str) or not value.strip()
               for value in [spawn.get('agent_path'), meta.get('id')]):
            discovery_issues.append(dict(path=str(path), issue='matched child has an invalid actor or session identifier',
                                         matched_parent=True))
            continue
        try:
            data = path.read_bytes()
        except OSError as error:
            discovery_issues.append(dict(path=str(path), issue='matched child snapshot unreadable', error_type=type(error).__name__))
            continue
        settings, contexts, issues = [], [], []
        for number, line in enumerate(data.splitlines(), 1):
            try:
                event = json.loads(line)
            except ValueError:
                issues.append(dict(line=number, issue='unparsed snapshot event'))
                continue
            if not isinstance(event, dict):
                issues.append(dict(line=number, issue='snapshot event is not a JSON object'))
                continue
            if event.get('type') != 'turn_context':
                continue
            payload = event.get('payload', {})
            if not isinstance(payload, dict):
                issues.append(dict(line=number, issue='turn_context payload is not an object'))
                continue
            actual = {key: payload.get(key) for key in ['model', 'effort']}
            settings.append(actual)
            contexts.append(dict(line=number, **actual))
            if any(not isinstance(actual[key], str) or not actual[key].strip() for key in actual):
                issues.append(dict(line=number, issue='missing actual model or effort'))
        records.append(dict(agent=spawn.get('agent_path'), session_id=meta.get('id'),
            runtime_source=str(path), parent_thread_id=parent_id, settings=settings,
            confirmed=bool(settings) and not issues, all_contexts_at_snapshot=contexts,
            runtime_snapshot_bytes=len(data), runtime_snapshot_sha256=hashlib.sha256(data).hexdigest(),
            parse_issues=issues))
    actors = Counter(record['agent'] for record in records)
    sessions = Counter(record['session_id'] for record in records)
    return dict(snapshot_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        parent_thread_id=parent_id, session_root=str(session_root), records=records,
        discovery_issues=discovery_issues,
        duplicate_agents=[name for name, count in actors.items() if count > 1],
        duplicate_session_ids=[name for name, count in sessions.items() if count > 1],
        limits='Actual settings for every parsed context in each captured child-session snapshot across all dates. No terminal-state, input-isolation, fork-setting, instruction-content, attention or correctness inference. Recheck complete terminal traces; resolve duplicate actors and relevant parse/discovery issues explicitly. Incoming task text may be encrypted.')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: runtime-provenance-all-dates.py NEW_RUN_LOCAL_OUTPUT.json')
    output = (ROOT / sys.argv[1]).resolve()
    if not output.is_relative_to(ROOT):
        raise SystemExit('Output must remain inside this run directory')
    result = collect()
    with output.open('x') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    print(json.dumps(dict(output=str(output), matched_children=len(result['records']),
        duplicate_agents=result['duplicate_agents'], discovery_issues=len(result['discovery_issues']),
        unconfirmed=[record['agent'] for record in result['records'] if not record['confirmed']])))
