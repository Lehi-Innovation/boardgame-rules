"""Recompute structural stage history without evaluating any answer fact."""
import argparse
import json
import sys
from staged_common import (Context, archives, checked_archives, closed_draft, load,
                           input_history, metadata_changes, report_path, sha, write_new)
from snapshot_stage import review_diff


def validate_history(iteration):
    ctx = Context(iteration)
    report = {'frozen_inputs': ctx.frozen(), 'question_count': ctx.n, 'readers': [],
              'structural_diagnostics_only': True, 'factual_grades_or_automatic_caps': False,
              'review_payload_delivery_certified': False}
    for label in ('a', 'b'):
        errors, stages = [], {}
        for stage in ('input', 'draft', 'review'):
            items, stage_errors = checked_archives(ctx, label, stage)
            stages[stage] = items
            # Failed input attempts are preserved, and a later valid readiness
            # attempt may supersede them before drafting begins.
            if stage == 'input':
                _, input_errors = input_history(ctx, label)
                errors.extend(input_errors)
            else:
                errors.extend(stage_errors)
        draft, review = stages['draft'], stages['review']
        if len(draft) != (ctx.n + 9) // 10 or len(review) != (ctx.n + 19) // 20:
            errors.append('Incomplete scheduled stage history')
        try:
            draft_path, original = closed_draft(ctx, label)
            start = load(ctx.root / ('reader-' + label + '-review-start.json'))
            if start.get('draft_sha256') != sha(draft_path.read_bytes()) or start.get('frozen_inputs') != ctx.frozen() or start.get('task') != ctx.manifest['reader_tasks'][label]:
                errors.append('Review fence does not bind frozen reader/draft')
            for path, doc, structure in review:
                diff = review_diff(original, doc)
                if diff != structure.get('draft_to_review_diff') or doc.get('self_review', {}).get('revised_ids') != diff['changed_answer_ids']:
                    errors.append('Original draft-to-review diff mismatch: ' + path.name)
                if metadata_changes(original, doc):
                    errors.append('Original input/process metadata changed during review')
            if not review or ctx.work(label, 'final').read_bytes() != review[-1][0].read_bytes():
                errors.append('Final work file differs from last review archive')
        except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
            errors.append(str(exc))
        report['readers'].append({'reader': label, 'pass': not errors, 'errors': errors,
            'stages': {stage: [{'path': str(path), 'sha256': sha(path.read_bytes()),
                               'reported_pass': structure.get('pass')} for path, _, structure in items]
                       for stage, items in stages.items()}})
    report['pass'] = all(item['pass'] for item in report['readers'])
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('iteration')
    args = parser.parse_args()
    result = validate_history(args.iteration)
    # Immutable validation attempts; an incomplete check never replaces history.
    root = Context(args.iteration).root
    number = 1
    while (root / ('staged-history-validation-' + format(number, '02') + '.json')).exists():
        number += 1
    write_new(root / ('staged-history-validation-' + format(number, '02') + '.json'), result)
    print(json.dumps(result))
    return 0 if result['pass'] else 1


if __name__ == '__main__':
    sys.exit(main())
