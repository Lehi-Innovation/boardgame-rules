# Single-reader grading tools review 02

**Changes requested: two delivery-proof edge cases remain.** The four original mechanisms have been repaired under the new explicit read interface. Forty-two independent synthetic cases were run; the unchanged single-reader adapter again matched the original paired validator exactly.

The fixed read program is read-only and per-invocation. Unknown early commands, alternate writes/stdout helpers, cached commands and missing/early boundaries fail. Exact tagged45-LF-line chunks preserve ranges, source quantities, whitespace, Unicode and EOF. Frozen input/packet/original canonical hashes and role/block identity reject tampering. Complete approved nested metadata and entries are distinguished from separately supplied foreign packets. The five substantive grading/output paragraphs remain unchanged.

Two concrete cases still need attention:

1. **Outputs are not bound to recorded reads.** Removing every read-call event while retaining the approved-value output events and declared write boundary still certifies delivery. Retain output call IDs and count data only when bound to an approved recorded pre-boundary mode/index call; an orphaned trace is insufficient proof.
2. **Recovered truncation can be falsely rejected.** A legitimate nested packet-shaped example inside a frozen original entry is accepted in a full read. If that entry’s output truncates just after the nested example and a complete approved retry follows before the boundary, the nested fragment is wrongly treated as foreign input and the proof fails. Match fragments against the expected response for their approved call, credit only the complete value, and keep genuinely additional foreign objects rejected.

These findings concern trace proof and recovery, not content scores or gameplay. No actual reader, grade or runtime was read. Post-boundary calls are retained for a separate permitted-path/isolation audit, and the proof correctly avoids claiming arbitrary later code is vetted.

All tests used in-memory source/question/entry/runtime data. Both adapter and imported base globals pointed at the same virtual root. The original helpers, templates, reviews and tests remain untouched; no grader was dispatched. The authorized `single-reader-grading-review-02` folder retains the new harness and synthetic results.

## Input hashes

- `single-reader-grading-tools.py`: `74cf5e82b263576a200ba9837dcbf90844310e35194d0e789be073e39f189ccb`
- `prove-single-reader-grading-delivery.py`: `fb09a0d296aca178bdc4bbc4d61f163dfe32b8ce235a45d39e8d5b231eecd65b`
- `block-grading-tools.py`: `f9df66b622d264975923fb85877a3c559898d0b0db4f233dc49b6c3f0f05a9f6`
- `prove-bounded-delivery.py`: `5f95d57189dbf3c449d47ad375e35cbf32b83bfb2bd00bb876f27f40ab857318`
- `expanded-v12-complete-requested-scope/luna-iteration-05/single-reader-grading-dispatch-template.json`: `65cf97d5036f321a10b040a63c6a492b04b8ff4f73bf6189feb1037c6bb68e63`
- `expanded-v12-complete-requested-scope/luna-iteration-05/single-reader-grading-dispatch-template-initial.json`: `70f6bb52dc209a16e3e7c11ae7af215ac7aa084d258a4fdbca806ed50a643e7b`

The JSON review contains all cases, exact reviewer-artifact hashes and review limits.
