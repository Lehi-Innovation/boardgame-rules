"""Reconcile owned working-state metadata; never adopt grades or mutate inputs."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil

B = Path(__file__).resolve().parent
D = B / 'expanded-iteration-08'
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
dispatch = load(D / 'grading/dispatch-log.json')
sent = {row['block'] for row in dispatch['dispatch_events']}
frozen = []
for n in sorted(sent):
    p = D / 'grading' / f'block-{n:02}'
    if (p / 'original-freeze.json').exists():
        receipt = load(p / 'original-freeze.json')
        assert H(p / 'grades.json') == H(p / 'grades-original-completed.json') == receipt['sha256']
        frozen.append(n)
active = sorted(sent - set(frozen))
pending = sorted(set(range(1, 10)) - sent)
dispatch.update(completed_original_frozen_blocks=frozen, active_blocks=active,
                pending_blocks=pending, all9_dispatched=len(sent) == 9,
                recorded_utc=now)
(D / 'grading/dispatch-log.json').write_text(json.dumps(dispatch, indent=2) + '\n')
stage = {'dispatch_log': str(D / 'grading/dispatch-log.json'),
         'completed_original_frozen_blocks': frozen, 'active_blocks': active,
         'pending_blocks': pending, 'results_adopted': False,
         'all346_entries_and1012_facts_required_before_adoption': True}
blocking = (
    f'C27 current source PASS and complete08 reader actual transport/models accepted. '
    f'Primary originals frozen {frozen}; dispatched but not frozen {active}; undispatched {pending}. '
    'Collect all9 originals, verify all45 whole grader inputs and actual models, and complete '
    'all346/1012 assessments before ONE full-original complete-set neutral and result adoption. '
    'Actual stamp authorization, NEW exact-stamped173 pair plus pure own-current-body followup, '
    'final integrity/privacy/report and explicit completion authorization remain pending.'
)
steps = [
    'Finish all9 primary blocks and freeze each entire completed original before semantic review; capture completed actual models.',
    'Verify all45 whole grader inputs and all346 originals/all1012 facts; aggregate once after the entire primary set closes.',
    'Select every noncorrect/flag/finding/noncorrect-fact/nonempty-extra case for ONE fresh full-original neutral; if none, preserve honest zero-case closure.',
    'Adopt full08 result. After eventual PASS and actual stamp authorization, run NEW exact-stamped173 pair and pure current-body followup, final integrity/privacy/report and obtain explicit completion authorization.',
]
profiles = len(load(B / 'model-provenance.json'))
edges = len(load(B / 'provenance-metadata-update-chain.json')['updates'])
for name in ['progress.json', 'pending-work-state.json', 'final-report-rewrite-requirements.json']:
    p = B / name
    backup = p.with_name(p.name + '.before-current08-primary-phase-synchronization')
    if not backup.exists():
        shutil.copyfile(p, backup)
    x = load(p)
    x.update(phase=f'C27-pair08-primary-{len(frozen)}-of9-originals-frozen',
             active_agents=[f'/root/expanded8_grade_{n:02}' for n in active],
             updated_utc=now, blocking_reason=blocking, next_steps=steps,
             pair08_primary_grading=stage,
             runtime_privacy_current_verified=False,
             actual_model_profiles_currently=profiles,
             working_report_refresh_needed_after_pair08_final_freeze=True)
    x['verification'] = {**x.get('verification', {}),
                         'current_actual_model_profiles': profiles,
                         'current_metadata_update_edges': edges,
                         'current_DEFAULT_privacy_not_yet_renewed': True,
                         'actual_model_capture_epoch': 'Current08 primary grading; exact frozen profiles retained per actor.'}
    p.write_text(json.dumps(x, indent=2) + '\n')
receipt = {'updated_utc': now, 'current_canonical_sha256': H(B.parents[4] / 'rules/spirit-island.md'),
           'C27_source_PASS_adoption': str(B / 'source-audit15-C27-own-current-body-semantic-adoption.json'),
           'source_acceptance_is_not_reader_performance_acceptance': True,
           'reader_originals_frozen': True, 'primary': stage,
           'current_profile_count': profiles, 'current_metadata_update_edges': edges,
           'runtime_privacy_current_verified': False,
           'all_older_continuations_are_historical': True,
           'next_steps': steps, 'goal_status': 'active',
           'stamp_or_completion_authorized': False}
(B / 'continuation-C27-current08-primary.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(stage))
