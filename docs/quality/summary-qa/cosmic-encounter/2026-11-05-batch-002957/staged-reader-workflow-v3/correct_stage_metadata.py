"""Append a continuation-only correction to a failed scheduled stage archive.

The same reader must author the corrected work file. This tool only archives
and verifies metadata; it changes no reader work file and sends no messages.
"""
import argparse
import copy
import json
import re
import sys
from pathlib import Path
from staged_common import (Context, archives, changes, check_doc, checked_archives,
                           closed_draft, encoded, input_history, load,
                           draft_fence_errors, metadata_changes, report_path, same, sha, write_new)

FIELDS = ('completed_count', 'next_record_index_zero_based', 'bank_complete')


def correction_paths(original, attempt):
    return (original.with_name(original.stem + '-metadata-corrected-' + format(attempt, '02') + '.json'),
            original.with_name(original.stem + '-metadata-resolution-' + format(attempt, '02') + '.json'))


def correction_attempts(original):
    prefix = original.stem + '-metadata-'
    found = set()
    for path in original.parent.glob(prefix + '*.json'):
        match = re.fullmatch(re.escape(prefix) + r'(?:corrected|resolution)-(\d+)\.json', path.name)
        if match:
            found.add(int(match[1]))
    return sorted(found)


def continuation_change(original, corrected, expected):
    errors, changed = [], []
    if not isinstance(original, dict) or not isinstance(corrected, dict):
        return ['Original and corrected documents must be objects'], [], None
    before = {k: v for k, v in original.items() if k != 'continuation'}
    after = {k: v for k, v in corrected.items() if k != 'continuation'}
    if not same(before, after):
        errors.append('Non-continuation JSON values changed')
    old = original.get('continuation', {})
    new = corrected.get('continuation')
    if not isinstance(old, dict) or not isinstance(new, dict):
        return errors + ['Continuation must be an object or originally absent'], [], None
    old_unknown = {k: v for k, v in old.items() if k not in FIELDS}
    new_unknown = {k: v for k, v in new.items() if k not in FIELDS}
    if not same(old_unknown, new_unknown):
        errors.append('Unknown continuation fields changed')
    for key in FIELDS:
        if key not in new or not same(new[key], expected[key]):
            errors.append('Incorrect corrected continuation field: ' + key)
        if (key in old) != (key in new) or (key in old and key in new and not same(old[key], new[key])):
            changed.append('/continuation/' + key)
    if not changed:
        errors.append('No permitted continuation value was corrected')
    return errors, changed, sha(encoded({'outside_continuation': before, 'unknown_continuation': old_unknown}))


def build_resolution(ctx, label, stage, number, original_path, corrected_path, attempt, previous=None):
    """Deterministic verification of preserved original and corrected archives."""
    expected = min(number * (10 if stage == 'draft' else 20), ctx.n)
    raw, fixed_raw = original_path.read_bytes(), corrected_path.read_bytes()
    original_report_path = report_path(original_path)
    report = {'reader': label, 'stage': stage, 'sequence': number, 'correction_attempt': attempt,
              'expected_records': expected, 'frozen_inputs': ctx.frozen(),
              'original_snapshot_path': str(original_path), 'original_snapshot_sha256': sha(raw),
              'original_failed_report_path': str(original_report_path),
              'original_failed_report_sha256': sha(original_report_path.read_bytes()),
              'corrected_snapshot_path': str(corrected_path), 'corrected_snapshot_sha256': sha(fixed_raw),
              'permitted_change_fields': ['/continuation/' + key for key in FIELDS],
              'errors': [], 'structural_diagnostics_only': True,
              'factual_grades_or_automatic_caps': False, 'new_blind_vote_or_resampling': False,
              'no_factual_changes': False}
    try:
        original, corrected, structure = load(original_path), load(corrected_path), load(original_report_path)
        original_errors = check_doc(ctx, label, stage, original, expected)
        report['original_structure_pass'] = structure.get('pass')
        report['original_structure_errors'] = structure.get('errors')
        if structure.get('pass') is not False or structure.get('errors') != ['Incorrect continuation metadata'] or original_errors != ['Incorrect continuation metadata']:
            report['errors'].append('Original failure must concern continuation metadata only')
        if (structure.get('raw_snapshot_sha256') != sha(raw) or structure.get('frozen_inputs') != ctx.frozen()
                or structure.get('reader') != label or structure.get('stage') != stage or structure.get('sequence') != number):
            report['errors'].append('Original failed report association/hash/frozen pins mismatch')
        if stage not in ('draft', 'review') or not 1 <= number <= (ctx.n + (9 if stage == 'draft' else 19)) // (10 if stage == 'draft' else 20):
            report['errors'].append('Not a scheduled draft/review boundary')
        if stage == 'review':
            own_review = original.get('self_review', {})
            required = {'completed_count': own_review.get('reviewed_count'),
                        'next_record_index_zero_based': own_review.get('next_record_index_zero_based'),
                        'bank_complete': own_review.get('complete')}
        else:
            required = {'completed_count': expected, 'next_record_index_zero_based': expected,
                        'bank_complete': expected == ctx.n}
        errors, changed, unchanged_hash = continuation_change(original, corrected, required)
        report['errors'].extend(errors)
        report['changed_fields'] = changed
        report['unchanged_noncontinuation_values_sha256'] = unchanged_hash
        report['errors'].extend(check_doc(ctx, label, stage, corrected, expected))
        ready, ready_errors = input_history(ctx, label)
        if ready_errors or ready is None or metadata_changes(ready, corrected):
            report['errors'].append('Original readiness/process receipts must remain valid and unchanged')
        if number > 1:
            if previous is None:
                report['errors'].append('Previous effective scheduled stage is required')
            else:
                answer_changes, pool_changes = changes(previous, corrected)
                if answer_changes or pool_changes or metadata_changes(previous, corrected):
                    report['errors'].append('Earlier completed values changed within stage')
        effective = copy.deepcopy(structure)
        effective.update({'raw_snapshot_path': str(corrected_path), 'raw_snapshot_sha256': sha(fixed_raw),
                          'errors': [], 'pass': True})
        if stage == 'review':
            from snapshot_stage import review_diff
            draft_path, draft = closed_draft(ctx, label)
            start = load(ctx.root / ('reader-' + label + '-review-start.json'))
            report['errors'].extend(draft_fence_errors(ctx, label, start))
            if (start.get('draft_sha256') != sha(draft_path.read_bytes()) or start.get('frozen_inputs') != ctx.frozen()
                    or start.get('reader') != label or start.get('task') != ctx.manifest['reader_tasks'][label]):
                report['errors'].append('Review fence does not bind frozen reader/draft')
            if metadata_changes(draft, corrected):
                report['errors'].append('Original draft input/process metadata changed')
            effective['draft_to_review_diff'] = review_diff(draft, corrected)
            if corrected.get('self_review', {}).get('revised_ids') != effective['draft_to_review_diff']['changed_answer_ids']:
                report['errors'].append('revised_ids differs from complete original-entry diff')
        if not report['errors']:
            report['effective_stage_report'] = effective
            report['no_factual_changes'] = True
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
        report['errors'].append(type(exc).__name__ + ': ' + str(exc))
    report['pass'] = not report['errors']
    return report


def resolve_archive(ctx, label, stage, number, original_path, original_doc, original_report, previous=None):
    """Return effective tuple + diagnostics; disclose every immutable attempt."""
    attempts, failures, accepted = [], [], []
    for expected_attempt, attempt in enumerate(correction_attempts(original_path), 1):
        corrected_path, resolution_path = correction_paths(original_path, attempt)
        try:
            resolution = load(resolution_path)
            if attempt != expected_attempt:
                failures.append('Metadata correction attempt numbering gap')
            binding = {'reader': label, 'stage': stage, 'sequence': number,
                       'correction_attempt': attempt, 'frozen_inputs': ctx.frozen(),
                       'original_snapshot_path': str(original_path),
                       'original_snapshot_sha256': sha(original_path.read_bytes()),
                       'original_failed_report_path': str(report_path(original_path)),
                       'original_failed_report_sha256': sha(report_path(original_path).read_bytes()),
                       'corrected_snapshot_path': str(corrected_path),
                       'corrected_snapshot_sha256': sha(corrected_path.read_bytes())}
            if any(not same(resolution.get(key), value) for key, value in binding.items()):
                failures.append('Metadata correction immutable binding mismatch')
            if resolution.get('pass'):
                recomputed = build_resolution(ctx, label, stage, number, original_path, corrected_path, attempt, previous)
                if not recomputed['pass'] or not same(recomputed, resolution):
                    failures.append('Successful metadata resolution failed independent recomputation')
                else:
                    accepted.append((corrected_path, load(corrected_path), resolution['effective_stage_report']))
            attempts.append({'attempt': attempt, 'resolution_path': str(resolution_path),
                             'resolution_sha256': sha(resolution_path.read_bytes()),
                             'corrected_snapshot_path': str(corrected_path),
                             'corrected_snapshot_sha256': sha(corrected_path.read_bytes()),
                             'reported_pass': resolution.get('pass'), 'errors': resolution.get('errors', [])})
        except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
            failures.append('Metadata correction artifact error: ' + str(exc))
    if len(accepted) > 1:
        failures.append('Multiple accepted metadata resolutions for one scheduled stage')
    path, doc, report = accepted[0] if len(accepted) == 1 and not failures else (original_path, original_doc, original_report)
    report = copy.deepcopy(report)
    report['_original_snapshot_path'] = str(original_path)
    report['_original_snapshot_sha256'] = sha(original_path.read_bytes())
    report['_original_structure_sha256'] = sha(report_path(original_path).read_bytes())
    report['_original_structure_pass'] = original_report.get('pass')
    report['_original_structure_errors'] = original_report.get('errors', [])
    report['_metadata_correction_attempts'] = attempts
    report['_metadata_resolution_status'] = ('continuation_metadata_only_resolved' if accepted and not failures else
                                             'unresolved' if original_report.get('pass') is False else 'not_required')
    return (path, doc, report), failures


def correct_metadata(iteration, label, stage, number):
    ctx = Context(iteration)
    if stage not in ('draft', 'review') or type(number) is not int or number < 1:
        raise ValueError('Specify a scheduled draft/review batch number')
    history = archives(ctx, label, stage)
    if not history or history[-1][0] != number:
        raise ValueError('Correct only the latest archived scheduled stage')
    original_path = history[-1][1]
    prior, prior_errors = checked_archives(ctx, label, stage, before_number=number)
    if prior_errors:
        raise ValueError('Earlier scheduled stages must already be valid or resolved')
    attempts = correction_attempts(original_path)
    for attempt in attempts:
        _, resolution_path = correction_paths(original_path, attempt)
        if resolution_path.exists() and load(resolution_path).get('pass'):
            raise FileExistsError('Preserve the existing successful metadata resolution')
    attempt = max(attempts, default=0) + 1
    corrected_path, resolution_path = correction_paths(original_path, attempt)
    source = ctx.work(label, 'final' if stage == 'review' else 'draft')
    raw = source.read_bytes()
    # Preserve every proposed correction before inspecting its JSON values.
    with corrected_path.open('xb') as handle:
        handle.write(raw)
    resolution = build_resolution(ctx, label, stage, number, original_path, corrected_path, attempt,
                                  prior[-1][1] if prior else None)
    write_new(resolution_path, resolution)
    return resolution


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('iteration')
    parser.add_argument('label', choices=['a', 'b'])
    parser.add_argument('stage', choices=['draft', 'review'])
    parser.add_argument('batch_number', type=int)
    args = parser.parse_args()
    result = correct_metadata(args.iteration, args.label, args.stage, args.batch_number)
    print(json.dumps({key: result[key] for key in ('reader', 'stage', 'sequence', 'correction_attempt',
                                                   'pass', 'errors', 'original_snapshot_sha256',
                                                   'corrected_snapshot_path', 'corrected_snapshot_sha256')}))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
