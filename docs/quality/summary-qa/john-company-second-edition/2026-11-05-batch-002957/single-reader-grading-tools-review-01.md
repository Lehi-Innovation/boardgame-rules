# Single-reader grading tools review 01

**Changes requested in delivery proofs.** The single-reader adapter’s core scheduling, preservation and aggregation passed the tested contract. Fifty-one synthetic cases were run without reading real runtime or grading data.

The new dispatch template is exactly the previous grading template after its four declared role substitutions. Preparation uses only the assigned reader, validates original IDs before indexing, preserves complete entries and partitions both synthetic53- and113-entry banks into disjoint15–20-entry blocks. Every asked atom and quotations across all four substantive same-entry fields were validated. Missing/duplicated requirements or IDs, wrong-role reports, metadata-only/foreign quotes and input/raw/packet/grade/collection tampering were rejected. Exclusive creation preserved existing collections and reports.

With A collected while B was absent, full combine still required B. Once both synthetic roles were complete, the adapter produced **exactly the same final result as the original paired validator** on identical frozen inputs and reports.

Four concrete delivery-proof risks remain:

1. **First-write heuristics are unsound.** An early `open(..., 'x').write(...)` was missed, allowing later input delivery to count as pre-write. Conversely, `json.dump(..., sys.stdout)` was treated as an artifact write. Use an auditable write boundary that distinguishes transport from mutation.
2. **Extra other-role inputs are ignored.** Wrong-role-only entries fail, but complete own inputs plus an additional opposite-role packet entry still pass. Detect forbidden foreign-role input outside approved original entry content.
3. **Expected packets are not bound to frozen originals inside the proof.** A cropped/tampered packet delivered exactly was certified complete without checking its frozen manifest/raw-entry hashes. The separate role validator did reject it. Bind proof expectations to frozen packet/input/original-entry hashes before certifying delivery.
4. **Summary substring checks accept changed lines.** A frozen synthetic `Value 1` line was falsely satisfied by `Value 10`, with matching preparation hashes. Use exact decoded line/chunk boundaries and source ranges/hashes.

These are generic proof-integrity findings, not judgments about any actual reader or grade. No gameplay fact, key, asked atom or semantic grading rule needs changing. The full workflow must continue treating delivery/format proof separately from factual grading.

Only the six authorized static files and this reviewer’s new synthetic artifacts were read. All bank/reader/grader/provenance/runtime data and helper filesystem writes were virtual. Both the adapter and its imported paired helper, and both delivery modules, were explicitly bound to the same virtual root. No real runtime files, grades, results, statuses or scores were accessed or inferred. Helpers and templates were not edited.

## Input hashes

- `single-reader-grading-tools.py`: `74cf5e82b263576a200ba9837dcbf90844310e35194d0e789be073e39f189ccb`
- `prove-single-reader-grading-delivery.py`: `152a947cca1d02ec2fa04e2e13c3ca105a9d16e0adf58d650b13a34675681d86`
- `block-grading-tools.py`: `f9df66b622d264975923fb85877a3c559898d0b0db4f233dc49b6c3f0f05a9f6`
- `prove-bounded-delivery.py`: `5f95d57189dbf3c449d47ad375e35cbf32b83bfb2bd00bb876f27f40ab857318`
- `expanded-v12-complete-requested-scope/luna-iteration-05/single-reader-grading-dispatch-template.json`: `70f6bb52dc209a16e3e7c11ae7af215ac7aa084d258a4fdbca806ed50a643e7b`
- `expanded-v12-complete-requested-scope/luna-iteration-05/grading-dispatch-template.json`: `f1a78c3714c4d5f07d96c9c4d243e891737b538d2c3cdf0c893a387e9f93ed6f`

The companion JSON contains all synthetic cases, exact artifact hashes and review limits. The authorized `single-reader-grading-review-01` subfolder retains the harness and both synthetic test attempts.
