# V7 hierarchical tools review — revision 01

**PASS within the declared protocol/checker contract.** All three previous findings are resolved.

The checker now accounts for the entire reserved marker namespace and requires the exact declared begin/end token set. Unknown, extra, dangling, malformed and nested attachment cases were rejected. Valid identified blocks are masked before checking for unmarked complete-unit copies, so duplicate volume is rejected while distinct disjoint IDs with identical source text remain valid.

Raw question IDs, selected unit IDs, fact-source IDs, reference IDs and their relevant containers are checked before unsafe lookups. Invalid raw entries produce structured diagnostics; malformed source question IDs receive deliberate format-review exceptions. Synthetic inputs remained unchanged, and no format error became a content score or cap.

Independent tests also reconfirmed nested/skipped/repeated headings, level1 closure, Unicode character offsets, physical LF lines, exact untrimmed hashes, EOF/trailing whitespace, overlapping aliases, source order, cropped/mislabeled/duplicate blocks, false quotes/source references, and honest unsupported clauses without guessed sections.

V7 remains generic, identical except role/path and blind, with one-question-at-a-time manual semantic selection. Structural/literal results still do not establish relevance, asked-fact completeness, calculations or factual correctness. No question, key or substantive grading change is required.

Only the two authorized files were read. All test data were synthetic and in memory; no parent tests, real banks, readers, grades, results, histories, statuses or scores were accessed or inferred. The original review and all existing files were preserved.

## Input hashes

- `blind-reader-protocol-user-scope-v7.txt`: `02f4adf3a1e9ca4655964014f711a35dbd55a651f2e65842748de1406645ca25`
- `summary-hierarchical-section-check.py`: `fec4ed84e1d1993ff0763cc584144a4b2e58627260bcc38455626c1ea812e0f2`
