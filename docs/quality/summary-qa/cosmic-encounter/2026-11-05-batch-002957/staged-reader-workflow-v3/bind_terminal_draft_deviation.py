"""Bind one preserved complete terminal draft deviation without curing it.

Only earlier answer objects may be revised; prior evidence values stay exact.
This operation reads frozen and own archived/work inputs. It rewrites no data
or reader work files, accesses no runtime, generates no answers, and dispatches
no tools or messages.
"""
import argparse
import json
from pathlib import Path
from staged_common import (Context, archives, changes, check_doc, checked_archives,
                           encoded, input_history, load, metadata_changes,
                           pool_values, report_path, same, sha, write_new)

FAILURE = 'Earlier completed values changed within stage'


def binding_path(ctx, label):
    return ctx.root / ('reader-' + label + '-terminal-draft-deviation.json')


def evaluate_deviation(ctx, label, terminal_path, document, structure, previous_items, previous_errors):
    """Deterministic narrow binding; raises on every unassigned defect."""
    count = (ctx.n + 9) // 10
    history = archives(ctx, label, 'draft')
    if count < 2 or len(history) != count or history[-1] != (count, terminal_path):
        raise ValueError('Only the original full-bank terminal scheduled draft may be bound')
    if previous_errors or len(previous_items) != count - 1:
        raise ValueError('Every earlier scheduled draft must pass')
    if any(item[2].get('_original_structure_pass', item[2].get('pass')) is not True
           or item[2].get('_terminal_draft_deviation') for item in previous_items):
        raise ValueError('Every prior raw draft structure report must pass')
    if terminal_path.name != 'reader-' + label + '-draft-batch-' + format(count, '02') + '.json':
        raise ValueError('Bind the original terminal raw archive, never a selected alternative')
    raw = terminal_path.read_bytes()
    if (structure.get('pass') is not False or structure.get('errors') != [FAILURE]
            or structure.get('reader') != label or structure.get('stage') != 'draft'
            or structure.get('sequence') != count or structure.get('raw_snapshot_sha256') != sha(raw)
            or structure.get('frozen_inputs') != ctx.frozen()):
        raise ValueError('The sole preserved terminal failure must be earlier-answer immutability')
    if check_doc(ctx, label, 'draft', document, ctx.n):
        raise ValueError('Terminal draft must have exact full-bank bindings and valid source/process/count metadata')
    if ctx.work(label, 'draft').read_bytes() != raw:
        raise ValueError('Closed live draft must equal the exact preserved terminal raw bytes')
    if list(terminal_path.parent.glob(terminal_path.stem + '-metadata-*.json')):
        raise ValueError('A terminal deviation cannot select or replace a metadata correction')
    previous_path, previous, _ = previous_items[-1]
    changed, pool_changes = changes(previous, document)
    if not changed or pool_changes or type(previous.get('evidence_units', {})) is not type(document.get('evidence_units', {})):
        raise ValueError('Only earlier answer objects may change; every prior shared-pool value must stay exact')
    if (structure.get('earlier_answer_values_changed_ids') != changed
            or structure.get('earlier_evidence_values_changed_paths') != []
            or structure.get('earlier_metadata_changed_fields') != []):
        raise ValueError('Original terminal change diagnostics do not match actual preserved values')
    stable_before = {k: v for k, v in previous.items() if k not in ('answers', 'stage', 'continuation', 'evidence_units')}
    stable_after = {k: v for k, v in document.items() if k not in ('answers', 'stage', 'continuation', 'evidence_units')}
    if not same(stable_before, stable_after) or metadata_changes(previous, document):
        raise ValueError('Input/process/pool/unknown metadata must remain exact')
    old_continuation, new_continuation = previous['continuation'], document['continuation']
    known = ('completed_count', 'next_record_index_zero_based', 'bank_complete')
    if not same({k: v for k, v in old_continuation.items() if k not in known},
                {k: v for k, v in new_continuation.items() if k not in known}):
        raise ValueError('Unknown continuation metadata changed')
    ready, ready_errors = input_history(ctx, label)
    if ready_errors or ready is None or metadata_changes(ready, document):
        raise ValueError('Original readiness pins and process receipts must remain valid and unchanged')
    # Resolve explicit references against this same unchanged pool, retaining
    # original values/types/paths. This checks transport structure, not facts.
    for question, answer in zip(ctx.questions, document['answers']):
        ctx.method['review_display_record'](question, answer, document.get('evidence_units', {}))
    from snapshot_stage import value_diff
    differences = []
    for old, new in zip(previous['answers'], document['answers']):
        if not same(old, new):
            differences.append({'id': old['id'], 'earlier_answer_sha256': sha(encoded(old)),
                                'terminal_answer_sha256': sha(encoded(new)),
                                'changed_paths_and_hashes': value_diff(old, new)})
    return {'binding_version': 1, 'reader': label, 'task': ctx.manifest['reader_tasks'][label],
            'binding_verified': True, 'question_count': ctx.n, 'terminal_draft_sequence': count,
            'frozen_inputs': ctx.frozen(), 'terminal_draft_path': str(terminal_path),
            'terminal_draft_sha256': sha(raw), 'original_structure_path': str(report_path(terminal_path)),
            'original_structure_sha256': sha(report_path(terminal_path).read_bytes()),
            'original_structure_pass': False, 'original_structure_errors': [FAILURE],
            'previous_draft_path': str(previous_path), 'previous_draft_sha256': sha(previous_path.read_bytes()),
            'preserved_prior_drafts': [{'path': str(path), 'sha256': sha(path.read_bytes()),
                                       'structure_sha256': sha(report_path(path).read_bytes())}
                                      for path, _, _ in previous_items],
            'earlier_answer_values_changed_ids': changed, 'earlier_answer_differences': differences,
            'unchanged_prior_pool_sha256': sha(encoded(previous.get('evidence_units', {}))),
            'terminal_pool_sha256': sha(encoded(document.get('evidence_units', {}))),
            'appended_evidence_paths': sorted(set(pool_values(document)) - set(pool_values(previous))),
            'unchanged_process_input_and_unknown_values_sha256': sha(encoded(stable_after)),
            'content_integrity_pass': True, 'immutable_prefix_pass': False,
            'workflow_conformance_pass': False, 'content_completion_pass': False,
            'whole_bank_own_review_still_required': True,
            'factual_grading_question_count': ctx.n, 'workflow_deviation_factual_grade_cap': False,
            'new_blind_vote_or_resampling': False, 'publication_readiness_assessed': False,
            'limit': 'Binds the exact preserved complete draft as own-review input; does not cure its immutability failure or certify factual accuracy, actual reading, or publication readiness.'}


def apply_bound_deviation(ctx, label, terminal_path, doc, structure, previous_items, previous_errors):
    path = binding_path(ctx, label)
    if not path.exists():
        return structure, []
    try:
        recomputed = evaluate_deviation(ctx, label, terminal_path, doc, load(report_path(terminal_path)),
                                        previous_items, previous_errors)
        if not same(recomputed, load(path)):
            raise ValueError('Saved deviation binding differs from independent recomputation')
        result = dict(structure)
        # Keep pass=false and all original failure fields. Separate content
        # acceptance permits review; it is never technical conformance.
        result['_content_integrity_pass'] = True
        result['_immutable_prefix_pass'] = False
        result['_workflow_conformance_pass'] = False
        result['_terminal_draft_deviation'] = {'path': str(path), 'sha256': sha(path.read_bytes()),
                                               'terminal_draft_sha256': recomputed['terminal_draft_sha256']}
        return result, []
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as exc:
        return structure, ['Terminal draft deviation binding rejected: ' + str(exc)]


def bind_terminal_deviation(iteration, label):
    ctx = Context(iteration)
    if (ctx.root / ('reader-' + label + '-review-start.json')).exists() or archives(ctx, label, 'review'):
        raise ValueError('Bind the deviation before beginning own review')
    history = archives(ctx, label, 'draft')
    if not history:
        raise ValueError('No preserved terminal draft archive')
    count = (ctx.n + 9) // 10
    previous, errors = checked_archives(ctx, label, 'draft', before_number=count)
    terminal = history[-1][1]
    result = evaluate_deviation(ctx, label, terminal, load(terminal), load(report_path(terminal)), previous, errors)
    write_new(binding_path(ctx, label), result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('iteration')
    parser.add_argument('label', choices=['a', 'b'])
    args = parser.parse_args()
    result = bind_terminal_deviation(args.iteration, args.label)
    print(json.dumps({key: result[key] for key in ('reader', 'binding_verified', 'terminal_draft_sha256',
                                                  'original_structure_pass', 'immutable_prefix_pass',
                                                  'content_completion_pass', 'workflow_conformance_pass')}))


if __name__ == '__main__':
    main()
