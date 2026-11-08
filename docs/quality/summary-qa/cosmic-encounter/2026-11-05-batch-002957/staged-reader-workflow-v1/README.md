# Generic staged reader metadata tools

These standard-library tools preserve a predeclared input-readiness → complete
draft → complete own-review workflow. They generate no answers, select no
questions, and perform no factual or semantic grading. No existing protocol,
generic helper, or real reader data was changed while implementing them.

Run with existing Python and bytecode disabled:

```text
python3 -B snapshot_stage.py ITERATION a input
python3 -B snapshot_stage.py ITERATION a draft
python3 -B begin_review.py ITERATION a
python3 -B snapshot_stage.py ITERATION a review
python3 -B validate_staged_history.py ITERATION
python3 -B verify_review_payloads.py ITERATION a
python3 -B -m unittest -v test_staged_workflow.py
```

`ITERATION` is a directory path, absolute or relative to the invoking working
directory. Labels are `a` and `b`. The parent invokes each stage snapshot after
the corresponding reader turn. CLI structural/delivery failures return nonzero.
`begin_review.py` and `verify_review_payloads.py` are production entry points:
their runtime/provenance reads occur only when explicitly invoked. Neither
dispatches tools nor sends continuations. The parent must save a successful
review-start fence before sending the first generic review continuation.

## Manifest and path roles

`ITERATION/input-manifest-final.json` declares:

```json
{
  "question_count": 23,
  "generic_code_sha256": "<SHA256 of trusted generic-method-code.py>",
  "sole_game_data_files": [
    "/synthetic/iteration/summary-snapshot.md",
    "/synthetic/iteration/reader-questions-final.json"
  ],
  "reader_tasks": {
    "a": "/root/expanded6_reader_a",
    "b": "/root/expanded6_reader_b"
  },
  "reader_work_paths": {
    "a": {"draft": "/synthetic/iteration/a-draft.json", "final": "/synthetic/iteration/a-final.json"},
    "b": {"draft": "/synthetic/iteration/b-draft.json", "final": "/synthetic/iteration/b-final.json"}
  },
  "stage_schedule": {"draft_batch_size": 10, "review_batch_size": 20},
  "model_provenance_path": "/synthetic/parent/model-provenance.json"
}
```

All work/data/provenance paths are absolute. Work paths must be distinct. The
explicit provenance path supports parent capture outside the iteration; when
omitted, the locator defaults to `ITERATION/model-provenance.json`. It expects
`agents` entries with `task` and absolute `runtime_source_path`.

`ITERATION/questions.json` is the frozen grading bank and is not a declared
reader input. `ITERATION/reader-questions-final.json` is the reader input with
process metadata. Its complete ordered question records must exactly equal the
grading bank records, including unknown fields; IDs may have arbitrary gaps.
`ITERATION/generic-method-code.py` is the trusted generic v15 copy, verified
against the manifest before execution. The tools freeze hashes of the manifest,
both question files, and generic code in every stage report. The metadata tools
do not open the summary data file. Input delivery declarations are checked for
shape/coverage only; the parent must establish actual input delivery separately.

The reader's `reader` value must explicitly be `a` or `b`. Work documents retain
all original fields. They require unchanged `inputs_read`, `instructions_read`,
`method_code_sha256`, exact current question/clause bindings, and continuation
counts. Input readiness has `stage="inputs_ready"`, `answers=[]`, and
`evidence_units={}`. Draft stages are `drafting`/`draft_complete`; review stages
are `reviewing`/`review_complete`. Review counts and receipt prefixes are stored
in `self_review`, including bank-ordered `revised_ids` derived by comparison with
the original draft entries.

## Immutable artifacts

`snapshot_stage` archives the actual live file bytes using exclusive creation
before inspecting output defects, including malformed JSON. It writes the paired
`-structure.json` report afterward. Existing archives and reports are never
replaced.

- `reader-a-input-ready-01.json`: readiness attempt number; later attempts may
  supersede failed readiness attempts, whose original bytes remain preserved.
- `reader-a-draft-batch-01.json`: cumulative scheduled prefixes of 10, then 20,
  through the derived full bank size (including a shorter final batch).
- `reader-a-review-batch-01.json`: cumulative scheduled prefixes of 20 through
  full bank size, after the complete original draft is closed.
- `reader-a-review-start.json`: closed draft SHA, frozen-input hashes, runtime
  path, original runtime prefix byte count/hash, record count, and maximum
  `after_ordinal`. Exclusive creation prevents changing this fence.

Each scheduled draft/review snapshot consumes the next archive number. A failed
draft/review snapshot remains a structural history defect; a later snapshot
does not erase it or silently reuse the same boundary. Earlier completed answer
objects and shared evidence values cannot change within either stage. Declared
draft-to-review corrections are allowed. Reports retain every changed original
answer ID, original/revised hashes, changed JSON paths, pool changes, and hashes
of changed unknown top-level fields. The closed live draft must equal the final
draft snapshot byte for byte, and the final live output must equal the last
review snapshot. History validation recomputes these checks rather than using a
factual score or cap.

History and delivery validation runs create numbered, immutable
`staged-history-validation-NN.json` and
`reader-a-review-payload-validation-NN.json` reports.

## Actual review-payload proof

For every frozen question, the verifier calls the pinned v15
`review_display_record(question, original_closed_draft_entry, original_pool)`.
The final document declares:

```json
{"self_review": {"receipts": [{
  "id": "neutral/gapped-id",
  "payload_sha256": "<full canonical payload SHA256>",
  "chunks": [{"start": 0, "end": 1234, "sha256": "<whole piece UTF8 SHA256>"}]
}]}}
```

All chunks must cover the entire canonical payload contiguously in Unicode
character coordinates, with each range nonempty and at most 2900 characters.
Original reference values, types, JSON paths, unknown fields, and complete
explicitly referenced evidence come from the trusted helper without rewriting.
Unreferenced units and other answer records are not attached. Revised final
entries never replace original draft entries for this calculation.

The runtime must extend the exact saved prefix, with strictly increasing integer
ordinals (the JSONL line index is the fallback when an ordinal is absent).
Only public `payload.type="custom_tool_call_output"` outputs strictly after
`after_ordinal` qualify. JSON-wrapped public text is decoded without examining
instruction/message bodies. Every whole declared piece must occur in a distinct
actual output, in bank/chunk order. A piece cut out of a larger actual display of
the same contiguous payload is rejected. Proof reports retain ordinal and
record/public-text hashes rather than text. Recognizable model/effort context
fields are recorded separately, without copying instructions or ciphertext.

## API and verification limits

Importable APIs: `snapshot(iteration,label,stage)`,
`begin_review(iteration,label)`, `validate_history(iteration)`,
`verify_production(iteration,label)`. Tests use
`make_start(ctx,label,runtime_path,injected_bytes)` and
`verify_payloads(ctx,label,runtime_path,injected_bytes)` so production provenance
and runtime files are never opened. Test temporary directories are confined to
this tool directory and removed afterward.

The synthetic suite covers a 23-record bank with gapped IDs, Unicode ranges,
unknown fields, typed references, permitted cross-stage corrections, two complete
readers, computed-only receipts, pre-fence/private outputs, revised-record
substitution, overlarge-display subdivision, path/prefix/ordinal mismatches,
malformed-byte archival, within-stage changes, final-byte mismatches, partial
review rejection, and distinct reader/grading/provenance path roles.

The proof establishes exact text availability after a saved fence. It does not
establish comprehension, factual correctness, output token budget, the time of
the parent's first continuation, or delivery before a particular final-file
write. Model-context metadata is not independent identity attestation, and this
manifest contains no expected model/effort contract. Production runtime access
has not been exercised by this implementation's tests.
