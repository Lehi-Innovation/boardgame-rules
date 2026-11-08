"""Freeze actual completed checkpoint models, retaining the technical retry lineage."""
from pathlib import Path
import hashlib
import json
import shutil
import sys

B = Path(__file__).resolve().parent
D = B / 'expanded-iteration-12'
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
stage = sys.argv[1]
assert stage in ['draft_ready', 'complete']
steps_after_readiness = 1 if stage == 'draft_ready' else 2
suffixes = ['draft-ready'] if stage == 'draft_ready' else ['completed', 'final-completed']
output = D / ('draft-actual-models.json' if stage == 'draft_ready' else 'completed-reader-models.json')
assert not output.exists()
prepared = []
for letter in 'ab':
    task = f'expanded12_reader_{letter}'
    raw = D / f'reader-{letter}.json'
    assert load(raw)['stage'] == stage and len(load(raw)['answers']) == 173
    frozen = D / f'reader-{letter}-original-{("draft" if stage == "draft_ready" else "completed")}.json'
    assert raw.read_bytes() == frozen.read_bytes()
    ready = load(B / 'runtime' / f'{task}-delivery-ready-projection.json')
    src = B / 'runtime' / f'{task}-metadata.json'
    current = load(src)
    assert current['agent'] == ready['agent'] == '/root/' + task
    assert current['thread_id'] == ready['thread_id']
    assert current['requested_spawn']['fields']['fork_turns'] == 'none'
    actual_contexts = len(current['turn_contexts'])
    assert actual_contexts == len(ready['turn_contexts']) + steps_after_readiness
    assert current['turn_contexts'][:len(ready['turn_contexts'])] == ready['turn_contexts']
    assert current['confirmed_settings'] == [{'model': 'gpt-6-luna', 'effort': 'high'}] * actual_contexts
    assert all(x['fields']['model'] == 'gpt-6-luna' and x['fields']['effort'] == 'high' for x in current['turn_contexts'])
    if stage == 'complete':
        draft = load(B / 'runtime' / f'{task}-draft-ready-projection.json')
        assert current['turn_contexts'][:-1] == draft['turn_contexts']
    destinations = [B / 'runtime' / f'{task}-{suffix}-projection.json' for suffix in suffixes]
    assert all(not p.exists() for p in destinations)
    prepared.append((letter, src, destinations, actual_contexts, H(frozen), len(ready['turn_contexts'])))
rows = []
for letter, src, destinations, contexts, original_hash, readiness_contexts in prepared:
    for dst in destinations:
        shutil.copyfile(src, dst)
        assert dst.read_bytes() == src.read_bytes()
    rows.append({
        'reader': f'reader-{letter}', 'actual_completed_contexts': contexts,
        'readiness_contexts_including_technical_retry': readiness_contexts,
        'all_contexts_actual_Luna_high': True, 'initial_fork_turns': 'none',
        'projections': [{'path': str(p), 'sha256': H(p)} for p in destinations],
        'original_checkpoint_sha256': original_hash,
    })
record = {
    'stage': stage, 'both_completed_models_PASS': True, 'readers': rows,
    'actual_context_counts_verified_without_assuming_equal_A_B': True,
    'same_original_actors_and_prior_context_lineage_verified': True,
    'no_pre_firstwriter_chronology_claim': True,
    'no_parent_factual_review_or_feedback': True,
}
output.write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'stage': stage, 'actual_contexts': {r['reader']: r['actual_completed_contexts'] for r in rows}, 'checkpoint_sha256': H(output)}))
