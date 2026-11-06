# Independent protocol v4 review — revision 01

**PASS within the declared protocol and structural-checker scope.** V4 remains generic, identical except role/path, blind and complete-bank. It requires actual clause facts/results and minimal explicit numerical/legal conclusions.

Both concrete checker failures are fixed. Complete selected source text, allowing only omitted trailing whitespace, must now occur exactly once in the answer. Unknown question IDs produce structured row errors through safe lookup instead of aborting validation.

Nine independent synthetic in-memory cases passed their expected outcomes: valid once, permitted trailing-whitespace omission, cropped content, duplicate body copy, unknown question ID, explicit unsupported clause without sections, wrong hash, wrong boundary and duplicate metadata ID. Nested-heading boundaries and EOF without newline also match the protocol’s exact algorithm and hashes.

The checker remains structural: it does not establish requested-fact correctness or section relevance, and unsupported clauses need not invent a source section. It identifies sections through metadata/ledger references; it does not independently parse answer-body ID attachment blocks. Body labeling remains a protocol/self-check requirement, not a stronger parser guarantee.

No remaining issue was found within that stated scope. The original review was preserved. Only the two authorized inputs were read; no real reader files, grades, results, histories or scores were accessed or inferred, and no fixture files were written.

Read hashes:

- `blind-reader-protocol-user-scope-v4.txt`: `38b1354b73561b1b160cacc845ebc4b738dfb69a88b1bd1e332f70988985a654`
- `summary-section-check.py`: `60d4c7b0768041e2ad735d5cbec71871516b4fa47fd7dc5a3a4dbb19298242fc`
