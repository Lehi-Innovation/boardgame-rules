"""Record explicitly confirmed dispatches and captured model checkpoints only."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import sys

B = Path(__file__).resolve().parent
D = B / 'expanded-iteration-09'
P = D / 'grading/dispatch-log.json'
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
state = load(P)
for argument in sys.argv[1:]:
    operation, number = argument.split(':')
    n = int(number)
    assert 1 <= n <= 9
    task = f'expanded9_grade_{n:02}'
    if operation == 'dispatch':
        assert not any(x['block'] == n for x in state['dispatch_events'])
        prompt = D / 'grading' / f'block-{n:02}' / 'grader-prompt.txt'
        assert len(prompt.read_text()) == 5940
        state['dispatch_events'].append({
            'block': n, 'task': '/root/' + task,
            'requested_model': 'gpt-6.1-sol', 'requested_effort': 'high',
            'fork_turns': 'none', 'creation_confirmed': True,
            'whole_native5940_prepared_message_sent_including_LF_parent_attestation': True,
            'prompt_sha256': H(prompt),
            'opaque_runtime_not_claimed_to_prove_plaintext_equality': True,
        })
    elif operation in ['initial', 'final-completed']:
        src = B / 'runtime' / f'{task}-metadata.json'
        dst = B / 'runtime' / f'{task}-{operation}-projection.json'
        assert not dst.exists()
        meta = load(src)
        assert meta['confirmed_settings'] == [{'model': 'gpt-6.1-sol', 'effort': 'high'}]
        assert meta['requested_spawn']['fields']['fork_turns'] == 'none'
        if operation == 'final-completed':
            block = D / 'grading' / f'block-{n:02}'
            assert H(block / 'grades.json') == H(block / 'grades-original-completed.json') == load(block / 'original-freeze.json')['sha256']
        shutil.copyfile(src, dst)
        state.setdefault('subsequent_captured_profiles', []).append({
            'task': task, 'path': str(dst), 'sha256': H(dst),
            'actual_contexts': 1, 'epoch': operation,
            'no_pre_first_draft_chronology_claim': True,
        })
    else:
        raise AssertionError(operation)
dispatched = {x['block'] for x in state['dispatch_events']}
frozen = {n for n in dispatched if (D / 'grading' / f'block-{n:02}' / 'original-freeze.json').exists()}
state.update(
    all9_dispatched=dispatched == set(range(1, 10)),
    pending_blocks=sorted(set(range(1, 10)) - dispatched),
    completed_original_frozen_blocks=sorted(frozen),
    active_blocks=sorted(dispatched - frozen),
    updated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
)
P.write_text(json.dumps(state, indent=2) + '\n')
print(json.dumps({k: state[k] for k in ['all9_dispatched', 'pending_blocks', 'completed_original_frozen_blocks', 'active_blocks']}))
