Independent METHOD audit of the frozen first-ten reader pair

The frozen ten-entry prefixes have qualified source-only support. Both readers visibly received all 498 physical summary lines and all 116 complete original question objects before their first artifact write. Both prefixes pass the frozen literal checker. This does **not** establish perfect procedural compliance, semantic coverage, factual correctness, or completion of the 116-question task.

| Check | Reader A | Reader B |
|---|---|---|
| Complete initial summary receipt | 498 lines; 12 separate responses, each at most 45 source lines | Same |
| Complete initial question receipt | 116 original objects; 20 responses, each at most 6 | 116 original objects; 19 responses; last response contains 8 |
| Final initial question response: call / output ordinal | 217 / 220 | 216 / 219 |
| First artifact-write call ordinal | 272 | 239 |
| Frozen ordered-ten-prefix flag | true | true |
| Ordered-ID flag against original 116 objects | false: partial prefix | false: partial prefix |
| Literal structure, exact attachments and source spans | true | true |
| Frozen records match exact question, map, metadata and case strings | all ten | all ten |
| Terminal first-turn replay matches frozen draft and self-check bytes | both files | both files |

The summary binding is `26ae8cecaa248b4321b6d6d7f601938e52e702057e9b2e4883910c2111f6a6ab`; the question-file binding is `1174e9455651e923694f030af20d3c04543cb436adc0f969bc8cd37d7f6a02cc`. The protocol and checker match their method-freeze hashes. Stored parent dispatches begin with the identical generic template after role substitution; their suffixes supply only the assigned paths.

Actual actor, parent and model evidence

Reader A is `/root/v13_stamped_i1_blind_reader_a` in session `01a1b17f-1872-7782-85b1-9ebbe7cd6c20`; reader B is `/root/v13_stamped_i1_blind_reader_b` in session `01a1b180-1984-7c62-b190-2d40090f9831`. Both original runtime metadata records name parent `01a1aaa2-7c89-7c92-bca8-a89efc3fe4d7`. Each actor agrees with its frozen manifest. All three actual turn-context records captured in each runtime snapshot declare `gpt-6-luna` and `high` effort: A ordinals 10, 518, 804; B ordinals 10, 437, 672. These are snapshot observations, not a promise about subsequent live work.

Receipt and procedure qualifications

1. A's original question-root slice failed at call 102 / output 105 with a TypeError. Call 109 checked the original input's container shape; call 116 recovered the first complete six objects. The complete original bank arrived before any output write. The failure and recovery remain bound in the evidence; there was no observed initial truncation.
2. A read the first three individual questions at calls 228, 242 and 256 and selected/read their sources at calls 235, 249 and 263 before composing the first entry at call 272. This is actual lookahead contrary to strict one-question-at-a-time scheduling. The scripts contain explicit source choices and individual entry appends; no bank-wide prefill or routing algorithm was observed.
3. A reread its second exact question at call 279 and composed it at 286 without a new source call after the first entry's composition. Its complete selected unit had actually arrived at call 249 during the earlier lookahead, after the earlier exact question read at 242. Thus complete actual source receipt is established, while the required fresh sequential source reread is not. All other frozen entries have a complete selected-unit receipt after their latest exact question reread and before composition. All selected units are shorter than 45 physical source lines.
4. A's initial third-entry ledger contained one nonliteral requested-clause phrase. Call 330 repaired the phrase in both entry and source record while saving the next entry. The original attempt and correction are hash-bound through the replay and original physical records. The frozen prefix passes the literal checker. The terminal declaration added at call 505 explains the lookahead and initial failed slice; both terminal files match the frozen manifest bytes.
5. B's call 216 / output 219 delivered eight complete objects, exceeding the six-object response bound. All eight visibly arrived, and the complete original bank was received before the first write. No truncation or recovery of this overbound response was observed in the first turn.
6. B's ten `contexts_rechecked` arrays are empty despite the visible individual question/source rereads. This limits the detail of that declared record field; it does not erase observed reads. The mechanical true fields in the self-check are not semantic verification.

Source selection and records

Every frozen entry has an exact original-question reread and a manually supplied clause-to-unit map in its original serialization call. The available method evidence is explicit heading constants, source-only slicing and hashing, plain case-string fields, and one-entry writes. There is no observed question-to-unit routing, ranking, fixed default selection, whole-summary answer dump, bank prefill, generated semantic-pass flag, or failure-to-locate fallback in these first turns. Private reasoning and manual intent are not independently observable.

The generic frozen lexer successfully constructs the recognized ATX units. Independent checks establish complete untrimmed attachments, matching metadata/hashes/boundaries, valid attachment markers, source order and nonoverlap, literal clause phrases and selected-unit references for all twenty frozen entries. The case fields are arrays of plain strings. These are literal-structure findings only: clause splitting, source relevance, governing qualifiers, calculations, unsupported assertions and completeness require independent factual assessment.

The original tool inputs and their model-visible textual outputs support use of the original two substantive data files and each reader's own draft/self-check files during these first turns. Only `exec` tool calls were observed. A memory-only replay of their deterministic Python mechanics read no additional substantive path and reproduced both frozen first-turn artifact pairs byte for byte. Library imports, working-directory/path strings, instructions prohibiting keys/history, and the original input's container-shape check are mechanical or procedural details; they do not establish forbidden key/history exposure. No such substantive exposure was observed in the permitted tool evidence.

Scope and limits

The adjudication is the frozen first-ten pair. Later work is live in the same actors and is not admitted as a completed bank. Later turn-context metadata was inspected narrowly for model/effort only; later entry choices and artifacts were not audited. The parent reports unchanged generic continuation; this report does not independently certify continuation message-body equivalence because message/context/reasoning/world/account/profile bodies were excluded from inspection. Stored dispatch/template texts were checked separately.

No source rulebook, key, scope bank, grade, prior audit or other session was read. No gameplay fact, failed-question factual hint, case correction, score inference or score cap is supplied. Labels, metadata, uncertainty and format alone do not cap factual grading. The checker result is never semantic coverage. Qualified source-only prefix admissibility follows from complete actual input receipt, complete actual selected-source receipt, exact attachments and matched records, with the stated scheduling, chunk-bound and record qualifications preserved.

Continue both readers only through the unchanged generic protocol/template. Preserve these findings and avoid issue-specific or factual feedback to either reader. Actual 116-entry finals and whole-task terminal admissibility require a separate later supplement.

Artifacts

- `audit.json`: structured disposition, qualifications, receipt counts and precise limits.
- `input-bindings.json`: hashes and lengths of the permitted frozen files.
- `reader-a-method-evidence.json` and `reader-b-method-evidence.json`: per-entry question/map/source bindings, actual receipt-call ordinals, original failed/recovered attempts, during-work checks and memory-replay file read/write records.
- `reader-a-physical-record-bindings.json` and `reader-b-physical-record-bindings.json`: narrow original-record ordinals, lengths, hashes and permitted labels, with no runtime bodies.
- `audit_method.py`: mechanical extraction/replay implementation; it sets `sys.dont_write_bytecode=True` before importing the frozen checker and uses memory-backed reader paths.

All audit writes are inside this new directory. The original runtimes, reader artifacts and frozen snapshots were untouched. There was no communication with either reader.
