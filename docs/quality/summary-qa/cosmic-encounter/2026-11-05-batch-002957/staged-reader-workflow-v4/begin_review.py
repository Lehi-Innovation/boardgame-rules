"""Save a runtime ordinal fence before a parent sends its review continuation.

No dispatch, messages, or production provenance access at import time.
"""
import argparse
import json
from pathlib import Path
from staged_common import (Context, closed_draft, draft_criteria, locate_runtime, runtime_records,
                           sha, write_new)


def make_start(ctx, label, runtime_path, runtime_raw, provenance=None):
    """Purely injected runtime bytes/path for synthetic tests; no provenance IO."""
    draft_path, _ = closed_draft(ctx, label)
    records = runtime_records(runtime_raw)
    report = {'reader': label, 'task': ctx.manifest['reader_tasks'][label],
              'draft_path': str(ctx.work(label, 'draft')), 'draft_snapshot_path': str(draft_path),
              'draft_sha256': sha(draft_path.read_bytes()), 'frozen_inputs': ctx.frozen(),
              **draft_criteria(ctx, label),
              'runtime_path': str(Path(runtime_path).resolve()),
              'runtime_prefix_bytes': len(runtime_raw), 'runtime_prefix_sha256': sha(runtime_raw),
              'runtime_record_count_at_start': len(records),
              'after_ordinal': records[-1][0] if records else -1,
              'provenance': provenance,
              'parent_review_continuation_dispatched': False,
              'chronology_limit': 'Only public outputs after this saved runtime fence are certified. No pre-writer timing claim.'}
    write_new(ctx.root / ('reader-' + label + '-review-start.json'), report)
    return report


def begin_review(iteration, label):
    ctx = Context(iteration)
    # Verify draft BEFORE opening any runtime/provenance source.
    closed_draft(ctx, label)
    path, provenance = locate_runtime(ctx, label)
    return make_start(ctx, label, path, path.read_bytes(), provenance)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('iteration')
    parser.add_argument('label', choices=['a', 'b'])
    args = parser.parse_args()
    print(json.dumps(begin_review(args.iteration, args.label)))


if __name__ == '__main__':
    main()
