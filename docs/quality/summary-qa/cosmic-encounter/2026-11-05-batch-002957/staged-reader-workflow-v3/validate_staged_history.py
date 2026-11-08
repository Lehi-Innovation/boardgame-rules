"""Recompute structural stage history without evaluating any answer fact."""
import argparse
import json
import sys
from staged_common import (Context, archives, checked_archives, closed_draft, load,
                           draft_fence_errors, immutable_prefix_pass, input_history, metadata_changes, report_path, sha, write_new)
from snapshot_stage import review_diff


def validate_history(iteration):
    ctx = Context(iteration)
    report = {'frozen_inputs': ctx.frozen(), 'question_count': ctx.n, 'readers': [],
              'structural_diagnostics_only': True, 'factual_grades_or_automatic_caps': False,
              'review_payload_delivery_certified': False, 'publication_readiness_assessed': False,
              'content_completion_scope': 'Frozen source/process pins, exact complete bank and whole-bank own-review structure; actual payload availability is certified separately.',
              'factual_grading_question_count': ctx.n, 'workflow_deviation_factual_grade_cap': False}
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
            errors.extend(draft_fence_errors(ctx, label, start))
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
        deviations = [structure['_terminal_draft_deviation'] for _, _, structure in draft
                      if structure.get('_terminal_draft_deviation')]
        content_pass = not errors
        workflow_pass = content_pass and not deviations
        report['readers'].append({'reader': label, 'pass': content_pass and workflow_pass, 'errors': errors,
            'content_completion_pass': content_pass, 'workflow_conformance_pass': workflow_pass,
            'immutable_prefix_pass': all(immutable_prefix_pass(structure) for stage in ('draft', 'review')
                                        for _, _, structure in stages[stage]),
            'workflow_deviations': deviations,
            'stages': {stage: [{'path': structure.get('_original_snapshot_path', str(path)),
                               'sha256': structure.get('_original_snapshot_sha256', sha(path.read_bytes())),
                               'reported_pass': structure.get('_original_structure_pass', structure.get('pass')),
                               'original_errors': structure.get('_original_structure_errors', structure.get('errors', [])),
                               'original_structure_sha256': structure.get('_original_structure_sha256'),
                               'effective_path': str(path), 'effective_sha256': sha(path.read_bytes()),
                               'effective_pass': structure.get('pass'),
                               'content_integrity_pass': structure.get('_content_integrity_pass', structure.get('pass')),
                               'immutable_prefix_pass': immutable_prefix_pass(structure),
                               'workflow_conformance_pass': structure.get('_workflow_conformance_pass', structure.get('pass')),
                               'terminal_draft_deviation': structure.get('_terminal_draft_deviation'),
                               'metadata_resolution_status': structure.get('_metadata_resolution_status', 'not_required'),
                               'metadata_correction_attempts': structure.get('_metadata_correction_attempts', [])}
                              for path, _, structure in items]
                       for stage, items in stages.items()},
            'effective_terminals': {stage: {'path': str(items[-1][0]),
                                            'sha256': sha(items[-1][0].read_bytes()),
                                            'metadata_resolution_status': items[-1][2].get('_metadata_resolution_status', 'not_required'),
                                            'original_structure_pass': items[-1][2].get('_original_structure_pass', items[-1][2].get('pass')),
                                            'content_integrity_pass': items[-1][2].get('_content_integrity_pass', items[-1][2].get('pass')),
                                            'workflow_conformance_pass': items[-1][2].get('_workflow_conformance_pass', items[-1][2].get('pass')),
                                            'immutable_prefix_pass': immutable_prefix_pass(items[-1][2]),
                                            'terminal_draft_deviation': items[-1][2].get('_terminal_draft_deviation')}
                                    for stage, items in stages.items() if items}})
    report['content_completion_pass'] = all(item['content_completion_pass'] for item in report['readers'])
    report['workflow_conformance_pass'] = all(item['workflow_conformance_pass'] for item in report['readers'])
    report['pass'] = report['content_completion_pass'] and report['workflow_conformance_pass']
    report['overall_technical_pass'] = report['pass']
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
