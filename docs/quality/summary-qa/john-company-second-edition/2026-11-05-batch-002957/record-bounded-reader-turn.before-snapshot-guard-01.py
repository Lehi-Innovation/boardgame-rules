"""Snapshot an actually completed partial reader turn; never grade or dispatch."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import sys

ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'expanded-v13-complete-requested-scope/luna-iteration-03'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(role, turn):
    if role not in ['a', 'b']:
        raise ValueError('Expected role a or b')
    turn = int(turn)
    progress_path = ROOT / 'progress.json'
    progress = json.loads(progress_path.read_text())
    state = progress['bounded_turn_progress'][role]
    if state['turns_dispatched'] != turn:
        raise ValueError('Turn differs from current dispatched state')
    questions = json.loads((RUN / 'questions.json').read_text())['questions']
    expected = [row['id'] for row in questions]
    draft_path = RUN / f'reader-{role}-draft.json'
    check_path = RUN / f'reader-{role}-self-check.json'
    answers = json.loads(draft_path.read_text())['answers']
    ids = [row['id'] for row in answers]
    count = len(ids)
    if ids != expected[:count] or not 0 <= count <= len(expected):
        raise ValueError('Draft is not an exact original ordered prefix')
    if not 0 <= count - state['completed_prefix'] <= 10:
        raise ValueError('Turn added more than ten questions or lost a prefix')
    check = json.loads(check_path.read_text())
    lists = [value for value in check.values() if isinstance(value, list)]
    if not any(all(isinstance(row, dict) for row in value)
               and [row.get('id') for row in value] == ids for value in lists):
        raise ValueError('No matching ordered per-ID source-check records')
    if count < len(expected) and (RUN / f'reader-{role}.json').exists():
        raise ValueError('Partial final file requires explicit procedural review')
    folder = RUN / 'bounded-turn-history' / f'reader-{role}-turn-{turn:02d}'
    folder.mkdir(parents=True, exist_ok=False)
    for source in [draft_path, check_path]:
        shutil.copyfile(source, folder / source.name)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    next_id = expected[count] if count < len(expected) else None
    manifest = dict(completed_at_utc=now, actor=f'/root/v13_i3_blind_reader_{role}',
        turn=turn, ordered_prefix=count, source_records=count,
        next_unfinished_id=next_id, full_bank_N=len(expected),
        caller_confirmed_actual_turn_terminal=True,
        source_only_same_context=True, facts_not_graded=True,
        files={path.name: digest(path) for path in folder.iterdir()},
        next_generic_continuation=str(RUN / 'reader-continuation-template.json'))
    with (folder / 'manifest.json').open('x') as handle:
        json.dump(manifest, handle, indent=2)
        handle.write('\n')
    state.update(turns_dispatched=turn + 1, completed_prefix=count,
        source_records=count, next_unfinished_id=next_id,
        state='next_generic_continuation_queued')
    progress['current_reader_partial_counts'] = progress['bounded_turn_progress']
    progress['updated_at_utc'] = now
    progress_path.write_text(json.dumps(progress, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(role=role, saved_turn=turn, prefix=count,
        full_bank_N=len(expected), next_id=next_id,
        next_turn_queued=turn + 1, no_semantic_grade_or_reader_edit=True)))


if __name__ == '__main__':
    main(*sys.argv[1:])
