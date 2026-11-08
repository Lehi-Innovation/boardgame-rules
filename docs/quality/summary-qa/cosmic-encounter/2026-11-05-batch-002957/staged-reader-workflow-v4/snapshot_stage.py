"""Archive actual stage bytes before returning structural diagnostics."""
import argparse
import json
import sys
from staged_common import (Context, archives, changes, check_doc, checked_archives, closed_draft, draft_fence_errors, encoded,
                           load, metadata_changes, report_path, same, sha, write_new)


def value_diff(old, new, pointer=''):
    """Every changed leaf/path, with original/new hashes and presence flags."""
    if same(old, new):
        return []
    if isinstance(old, dict) and isinstance(new, dict):
        result = []
        for key in sorted(set(old) | set(new)):
            path = pointer + '/' + key.replace('~', '~0').replace('/', '~1')
            if key in old and key in new:
                result.extend(value_diff(old[key], new[key], path))
            else:
                result.append({'path': path, 'draft_present': key in old, 'review_present': key in new,
                               'draft_sha256': sha(encoded(old[key])) if key in old else None,
                               'review_sha256': sha(encoded(new[key])) if key in new else None})
        return result
    if isinstance(old, list) and isinstance(new, list) and len(old) == len(new):
        return [change for index, (a, b) in enumerate(zip(old, new))
                for change in value_diff(a, b, pointer + '/' + str(index))]
    return [{'path': pointer, 'draft_present': True, 'review_present': True,
             'draft_sha256': sha(encoded(old)), 'review_sha256': sha(encoded(new))}]


def review_diff(original, reviewed):
    prefix = len(reviewed.get('answers', []))
    answer_diffs = []
    for old, new in zip(original['answers'], reviewed.get('answers', [])):
        paths = value_diff(old, new)
        if paths:
            answer_diffs.append({'id': old['id'], 'original_answer_sha256': sha(encoded(old)),
                                 'reviewed_answer_sha256': sha(encoded(new)), 'changes': paths})
    return {'reviewed_prefix_count': prefix,
            'changed_answer_ids': [d['id'] for d in answer_diffs], 'answers': answer_diffs,
            'evidence_pool_changes': value_diff(original.get('evidence_units', {}), reviewed.get('evidence_units', {}), '/evidence_units'),
            'other_field_changes': value_diff({k: v for k, v in original.items() if k not in ('answers', 'evidence_units')},
                                              {k: v for k, v in reviewed.items() if k not in ('answers', 'evidence_units')})}


def snapshot(iteration, label, stage):
    ctx = Context(iteration)
    source = ctx.work(label, 'final' if stage == 'review' else 'draft')
    history = archives(ctx, label, stage)
    sequence = history[-1][0] + 1 if history else 1
    term = {'input': 'input-ready', 'draft': 'draft-batch', 'review': 'review-batch'}[stage]
    target = ctx.root / ('reader-' + label + '-' + term + '-' + format(sequence, '02') + '.json')
    structure = report_path(target)
    if structure.exists():
        raise FileExistsError('Preserve existing structure archive')
    raw = source.read_bytes()
    # No output parsing/validation occurs before immutable raw-byte archival.
    with target.open('xb') as handle:
        handle.write(raw)
    report = {'reader': label, 'stage': stage, 'sequence': sequence,
              'raw_snapshot_path': str(target), 'raw_snapshot_sha256': sha(raw),
              'source_work_path': str(source), 'frozen_inputs': ctx.frozen(),
              'errors': [], 'structural_diagnostics_only': True,
              'factual_grades_or_automatic_caps': False,
              'actual_input_delivery_verified': False}
    try:
        doc = load(target)
        expected = 0 if stage == 'input' else min(sequence * (10 if stage == 'draft' else 20), ctx.n)
        report['expected_records'] = expected
        report['errors'].extend(check_doc(ctx, label, stage, doc, expected))
        if stage != 'input' and sequence > (ctx.n + (9 if stage == 'draft' else 19)) // (10 if stage == 'draft' else 20):
            report['errors'].append('Unexpected extra stage snapshot')
        if stage != 'input':
            ready = archives(ctx, label, 'input')
            if not ready:
                report['errors'].append('Input-readiness archive required before drafting')
            else:
                ready_path = ready[-1][1]
                if not load(report_path(ready_path)).get('pass') or metadata_changes(load(ready_path), doc):
                    report['errors'].append('Missing valid original readiness metadata')
            if history:
                prior, prior_errors = checked_archives(ctx, label, stage, before_number=sequence)
                if prior_errors:
                    report['errors'].append('Earlier scheduled history has unresolved structural defects')
                if not prior:
                    raise ValueError('Previous effective scheduled snapshot is unavailable')
                previous_path, previous, previous_report = prior[-1]
                report['previous_effective_snapshot_path'] = str(previous_path)
                report['previous_effective_snapshot_sha256'] = sha(previous_path.read_bytes())
                report['previous_metadata_resolution_status'] = previous_report.get('_metadata_resolution_status', 'not_required')
                changed, pool_changed = changes(previous, doc)
                report['earlier_answer_values_changed_ids'] = changed
                report['earlier_evidence_values_changed_paths'] = pool_changed
                report['earlier_metadata_changed_fields'] = metadata_changes(previous, doc)
                if changed or pool_changed or report['earlier_metadata_changed_fields']:
                    report['errors'].append('Earlier completed values changed within stage')
        if stage == 'review':
            draft_path, draft = closed_draft(ctx, label)
            start = load(ctx.root / ('reader-' + label + '-review-start.json'))
            report['errors'].extend(draft_fence_errors(ctx, label, start))
            if start.get('draft_sha256') != sha(draft_path.read_bytes()) or start.get('frozen_inputs') != ctx.frozen() or start.get('reader') != label:
                report['errors'].append('Review start does not bind this closed draft')
            report['closed_draft_path'] = str(draft_path)
            report['closed_draft_sha256'] = sha(draft_path.read_bytes())
            report['draft_to_review_diff'] = review_diff(draft, doc)
            revised = report['draft_to_review_diff']['changed_answer_ids']
            if doc.get('self_review', {}).get('revised_ids') != revised:
                report['errors'].append('revised_ids differs from complete original-entry diff')
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
        report['errors'].append(type(exc).__name__ + ': ' + str(exc))
    report['pass'] = not report['errors']
    write_new(structure, report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('iteration')
    parser.add_argument('label', choices=['a', 'b'])
    parser.add_argument('stage', choices=['input', 'draft', 'review'])
    args = parser.parse_args()
    result = snapshot(args.iteration, args.label, args.stage)
    print(json.dumps({k: result[k] for k in ('reader', 'stage', 'sequence', 'raw_snapshot_path', 'raw_snapshot_sha256', 'pass', 'errors')}))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
