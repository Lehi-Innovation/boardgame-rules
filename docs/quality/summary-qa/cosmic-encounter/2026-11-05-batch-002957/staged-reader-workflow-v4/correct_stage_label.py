"""Archive and resolve only an incorrect top-level stage label.

The same reader authors corrected bytes. Original failed artifacts remain
immutable. Continuation-only resolution definitions are deliberately unchanged.
"""
import argparse
import copy
import json
import re
import sys
from staged_common import (Context, archives, changes, check_doc, checked_archives,
                           closed_draft, draft_fence_errors, encoded, input_history,
                           load, metadata_changes, report_path, same, sha, write_new)


def correction_paths(original, attempt):
    return (original.with_name(original.stem + '-stage-label-corrected-' + format(attempt, '02') + '.json'),
            original.with_name(original.stem + '-stage-label-resolution-' + format(attempt, '02') + '.json'))


def correction_attempts(original):
    prefix = original.stem + '-stage-label-'
    attempts = set()
    for path in original.parent.glob(prefix + '*.json'):
        match = re.fullmatch(re.escape(prefix) + r'(?:corrected|resolution)-(\d+)\.json', path.name)
        if match:
            attempts.add(int(match[1]))
    return sorted(attempts)


def build_label_resolution(ctx, label, stage, number, original_path, corrected_path, attempt, previous=None):
    """Deterministic independent stage-label verification, with no old defaults."""
    size = 10 if stage == 'draft' else 20
    expected = min(number * size, ctx.n)
    expected_label = (('draft_complete' if expected == ctx.n else 'drafting') if stage == 'draft' else
                      ('review_complete' if expected == ctx.n else 'reviewing'))
    raw, fixed_raw = original_path.read_bytes(), corrected_path.read_bytes()
    original_structure_path = report_path(original_path)
    result = {'resolution_type': 'stage_label_only', 'reader': label, 'stage': stage,
              'sequence': number, 'correction_attempt': attempt, 'expected_records': expected,
              'expected_stage_label': expected_label, 'frozen_inputs': ctx.frozen(),
              'original_snapshot_path': str(original_path), 'original_snapshot_sha256': sha(raw),
              'original_failed_report_path': str(original_structure_path),
              'original_failed_report_sha256': sha(original_structure_path.read_bytes()),
              'corrected_snapshot_path': str(corrected_path), 'corrected_snapshot_sha256': sha(fixed_raw),
              'permitted_change_fields': ['/stage'], 'errors': [],
              'structural_diagnostics_only': True, 'factual_grades_or_automatic_caps': False,
              'new_blind_vote_or_resampling': False, 'no_factual_changes': False}
    try:
        original, corrected = load(original_path), load(corrected_path)
        structure = load(original_structure_path)
        result['original_structure_pass'] = structure.get('pass')
        result['original_structure_errors'] = structure.get('errors')
        if (structure.get('pass') is not False or structure.get('errors') != ['Incorrect stage label']
                or check_doc(ctx, label, stage, original, expected) != ['Incorrect stage label']):
            result['errors'].append('Original failure must concern the stage label only')
        if (structure.get('raw_snapshot_sha256') != sha(raw) or structure.get('frozen_inputs') != ctx.frozen()
                or structure.get('reader') != label or structure.get('stage') != stage or structure.get('sequence') != number):
            result['errors'].append('Original failed report association/hash/frozen pins mismatch')
        if stage not in ('draft', 'review') or not 1 <= number <= (ctx.n + size - 1) // size:
            result['errors'].append('Not a scheduled draft/review boundary')
        if not isinstance(original, dict) or not isinstance(corrected, dict):
            raise ValueError('Original and corrected documents must be objects')
        before = {key: value for key, value in original.items() if key != 'stage'}
        after = {key: value for key, value in corrected.items() if key != 'stage'}
        result['unchanged_nonstage_values_sha256'] = sha(encoded(before))
        if not same(before, after):
            result['errors'].append('Non-stage JSON values changed')
        if corrected.get('stage') != expected_label or original.get('stage') == corrected.get('stage'):
            result['errors'].append('Only the exact expected top-level stage label may be corrected')
        result['errors'].extend(check_doc(ctx, label, stage, corrected, expected))
        ready, ready_errors = input_history(ctx, label)
        if ready_errors or ready is None or metadata_changes(ready, corrected):
            result['errors'].append('Original readiness/process receipts must remain valid and unchanged')
        if number > 1:
            if previous is None:
                result['errors'].append('Previous effective scheduled stage is required')
            else:
                answer_changes, pool_changes = changes(previous, corrected)
                if answer_changes or pool_changes or metadata_changes(previous, corrected):
                    result['errors'].append('Earlier completed values changed within stage')
        effective = copy.deepcopy(structure)
        effective.update({'raw_snapshot_path': str(corrected_path), 'raw_snapshot_sha256': sha(fixed_raw),
                          'errors': [], 'pass': True})
        if stage == 'review':
            from snapshot_stage import review_diff
            draft_path, draft = closed_draft(ctx, label)
            fence = load(ctx.root / ('reader-' + label + '-review-start.json'))
            result['errors'].extend(draft_fence_errors(ctx, label, fence))
            if (fence.get('draft_sha256') != sha(draft_path.read_bytes()) or fence.get('frozen_inputs') != ctx.frozen()
                    or fence.get('reader') != label or fence.get('task') != ctx.manifest['reader_tasks'][label]):
                result['errors'].append('Review fence does not bind frozen reader/draft')
            if metadata_changes(draft, corrected):
                result['errors'].append('Original draft input/process metadata changed')
            effective['draft_to_review_diff'] = review_diff(draft, corrected)
            if corrected.get('self_review', {}).get('revised_ids') != effective['draft_to_review_diff']['changed_answer_ids']:
                result['errors'].append('revised_ids differs from complete original-entry diff')
        if not result['errors']:
            result['no_factual_changes'] = True
            result['effective_stage_report'] = effective
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
        result['errors'].append(type(exc).__name__ + ': ' + str(exc))
    result['pass'] = not result['errors']
    return result


def resolve_label_archive(ctx, label, stage, number, original_path, current, previous=None):
    """Layer label resolution over the unchanged continuation resolver result."""
    numbers = correction_attempts(original_path)
    if not numbers:
        return current, []
    attempts, errors, accepted = [], [], []
    for expected_attempt, attempt in enumerate(numbers, 1):
        corrected_path, resolution_path = correction_paths(original_path, attempt)
        try:
            result = load(resolution_path)
            if attempt != expected_attempt:
                errors.append('Stage-label correction attempt numbering gap')
            binding = {'resolution_type': 'stage_label_only', 'reader': label, 'stage': stage,
                       'sequence': number, 'correction_attempt': attempt, 'frozen_inputs': ctx.frozen(),
                       'original_snapshot_path': str(original_path),
                       'original_snapshot_sha256': sha(original_path.read_bytes()),
                       'original_failed_report_path': str(report_path(original_path)),
                       'original_failed_report_sha256': sha(report_path(original_path).read_bytes()),
                       'corrected_snapshot_path': str(corrected_path),
                       'corrected_snapshot_sha256': sha(corrected_path.read_bytes())}
            if any(not same(result.get(key), value) for key, value in binding.items()):
                errors.append('Stage-label correction immutable binding mismatch')
            if result.get('pass'):
                recomputed = build_label_resolution(ctx, label, stage, number, original_path,
                                                    corrected_path, attempt, previous)
                if not recomputed['pass'] or not same(recomputed, result):
                    errors.append('Successful stage-label resolution failed independent recomputation')
                else:
                    accepted.append((corrected_path, load(corrected_path), result['effective_stage_report']))
            attempts.append({'attempt': attempt, 'resolution_path': str(resolution_path),
                             'resolution_sha256': sha(resolution_path.read_bytes()),
                             'corrected_snapshot_path': str(corrected_path),
                             'corrected_snapshot_sha256': sha(corrected_path.read_bytes()),
                             'reported_pass': result.get('pass'), 'errors': result.get('errors', [])})
        except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
            errors.append('Stage-label correction artifact error: ' + str(exc))
    if len(accepted) > 1:
        errors.append('Multiple accepted stage-label resolutions for one scheduled stage')
    if len(accepted) == 1 and not errors and current[0] != original_path:
        errors.append('A stage-label-only fix cannot replace another effective correction')
    path, doc, report = accepted[0] if len(accepted) == 1 and not errors else current
    report = copy.deepcopy(report)
    # Preserve original raw failure disclosure and the existing continuation
    # resolver fields only in the in-memory history, never its saved reports.
    for key, value in current[2].items():
        if key.startswith('_'):
            report[key] = copy.deepcopy(value)
    report['_stage_label_correction_attempts'] = attempts
    report['_stage_label_resolution_status'] = ('stage_label_only_resolved' if accepted and not errors else 'unresolved')
    if accepted and not errors:
        report['_metadata_resolution_status'] = 'stage_label_only_resolved'
    return (path, doc, report), errors


def correct_stage_label(iteration, label, stage, number):
    ctx = Context(iteration)
    if stage not in ('draft', 'review') or type(number) is not int or number < 1:
        raise ValueError('Specify a scheduled draft/review batch number')
    history = archives(ctx, label, stage)
    if not history or history[-1][0] != number:
        raise ValueError('Correct only the latest archived scheduled stage')
    original = history[-1][1]
    prior, prior_errors = checked_archives(ctx, label, stage, before_number=number)
    if prior_errors:
        raise ValueError('Earlier stages must already be valid or resolved')
    attempts = correction_attempts(original)
    for attempt in attempts:
        _, path = correction_paths(original, attempt)
        if path.exists() and load(path).get('pass'):
            raise FileExistsError('Preserve the existing successful stage-label resolution')
    attempt = max(attempts, default=0) + 1
    corrected_path, resolution_path = correction_paths(original, attempt)
    raw = ctx.work(label, 'final' if stage == 'review' else 'draft').read_bytes()
    with corrected_path.open('xb') as handle:
        handle.write(raw)
    result = build_label_resolution(ctx, label, stage, number, original, corrected_path, attempt,
                                    prior[-1][1] if prior else None)
    write_new(resolution_path, result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('iteration')
    parser.add_argument('label', choices=['a', 'b'])
    parser.add_argument('stage', choices=['draft', 'review'])
    parser.add_argument('batch_number', type=int)
    args = parser.parse_args()
    result = correct_stage_label(args.iteration, args.label, args.stage, args.batch_number)
    print(json.dumps({key: result[key] for key in ('reader', 'stage', 'sequence', 'correction_attempt',
                                                   'pass', 'errors', 'expected_stage_label',
                                                   'corrected_snapshot_path', 'corrected_snapshot_sha256')}))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
