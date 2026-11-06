"""Preserve the first observed complete draft without changing reader outputs."""
from pathlib import Path
from collections import Counter
import datetime
import hashlib
import json
import os
import time

ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'expanded-v13-complete-requested-scope/luna-iteration-02'
QUESTIONS = RUN / 'questions.json'
EXPECTED = [q['id'] for q in json.loads(QUESTIONS.read_text())['questions']]


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save_new(path, value):
    with path.open('x') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


save_new(RUN / 'first-complete-draft-watch-start.json', dict(
    started_at_utc=now(), process_id=os.getpid(), script_sha256=sha(Path(__file__).read_bytes()),
    questions_sha256=sha(QUESTIONS.read_bytes()), expected_count=len(EXPECTED),
    poll_seconds=1, action='Read only own two reader draft paths; exclusively preserve each first observed complete draft and a hash record.',
    limit='Polling establishes first observed complete bytes, not an unobserved earlier filesystem event. Reader must also preserve its first complete draft unchanged.'))
pending = set('ab')
print(json.dumps(dict(started=True, process_id=os.getpid(), expected_count=len(EXPECTED))), flush=True)
while pending:
    for role in sorted(pending):
        source = RUN / f'reader-{role}-draft.json'
        try:
            data = source.read_bytes()
            value = json.loads(data)
            ids = [row['id'] for row in value['answers']]
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError):
            continue
        if Counter(ids) != Counter(EXPECTED):
            continue
        target = RUN / f'reader-{role}-first-observed-complete-draft.json'
        with target.open('xb') as handle:
            handle.write(data)
        assert target.read_bytes() == data
        record = dict(observed_at_utc=now(), role=role, source=str(source), preserved_copy=str(target),
                      sha256=sha(data), bytes=len(data), count=len(ids), unique_ids=len(set(ids)),
                      all_expected_ids_once=True, ordered=ids == EXPECTED,
                      original_reader_file_not_modified=True)
        save_new(RUN / f'reader-{role}-first-observed-complete-draft-record.json', record)
        print(json.dumps(record), flush=True)
        pending.remove(role)
    if pending:
        time.sleep(1)
print(json.dumps(dict(complete=True, finished_at_utc=now())), flush=True)
