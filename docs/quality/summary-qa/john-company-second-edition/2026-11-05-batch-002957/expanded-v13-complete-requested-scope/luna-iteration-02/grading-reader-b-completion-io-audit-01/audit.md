# Reader B completion IO audit 01

**Qualified actual-delivery/IO PASS for all six original actors.** Every full original summary chunk, own-packet metadata value and complete assigned entry reached a matched call-ID output before the first possible write. All six reports reproduce byte for byte in a replay using in-memory writes. All actual contexts are `gpt-6.1-sol` / `high`, with the original actor and parent IDs confirmed.

| Block | Preserved strict proof | Delivered chunks / metadata / entries | Failed reads before IO | Byte-identical report replay |
|---|---|---|---|---|
| block-01 | false | 11 / 1 / 20 | 0 | yes |
| block-02 | PASS | 11 / 1 / 20 | 0 | yes |
| block-03 | false | 11 / 1 / 19 | 1 | yes |
| block-04 | PASS | 11 / 1 / 19 | 0 | yes |
| block-05 | PASS | 11 / 1 / 19 | 0 | yes |
| block-06 | false | 11 / 1 / 19 | 1 | yes |

B01 has 32 outer-JavaScript whitespace departures; all 32 fixed shell read commands are identical to the permitted commands. B03 has 32 unrecognized calls: 31 successful fixed reads with outer-JavaScript whitespace differences and one malformed call missing the summary path. B06 has one extra malformed call missing that path. Each malformed call raises `ValueError: not enough values to unpack (expected 4, got 3)` at argument unpacking, before the first file read. Later successful calls supply the missing chunks. The strict false findings remain false, and the checker and frozen proof remain unchanged.

Every post-boundary shell and Python statement was inspected before extraction/replay. Python reads only its own packet and, where used, its own report after writing it; it writes only its own `grades-same-entry.json`. B01 additionally writes, executes and deletes its own `/tmp/grade_b01.py` source helper. That temporary artifact is an explicit qualification to block-directory-only IO. No other agent/status calls or foreign-data reads occur in the submitted programs.

Grades, per-atom statuses, selected quotes, reasons and issues originate in literal model-authored decision declarations. Loops insert packet IDs and required-fact text, validate counts and literal quote membership, assemble JSON and hash it. None of these programs performs semantic grading. This audit does not assess whether the selected gameplay decisions are correct.

`delivery/` records each actual call and output ordinal/hash, exact deep JSON equality and exact UTF-8 JSON serialization equality. Summary chunk text additionally matches original source bytes; concatenating all chunks matches the complete source SHA. `replay/` records the static program review, literal decision dataflow, constrained IO operations, actual output SHA and exact report reproduction. `programs/` contains only the six safety-reviewed original report programs; `replayed/` contains audit-owned reproduced reports. `projections/` contains explicit minimal runtime projections with original path, prefix length/SHA, physical record ordinals/hashes and needed tool fields. Every other runtime record is hash-only; private, incoming-task, message, reasoning, world-state and encrypted bodies are omitted.

`input-hashes.json` verifies that every original permitted file and runtime remained unchanged. `read-records.json` states the permitted reads and their purpose. No other reader, source rulebook, external key/question/scope file, audit history, web source or agent/status tool was consulted. The provenance document is used only for the six named actor entries.

The finding concerns recorded command/output delivery and explicit submitted-program IO. It does not supply a historical OS syscall trace or prove model attention. No content-score cap, gameplay regrading, source-authority cap or new key is introduced.
