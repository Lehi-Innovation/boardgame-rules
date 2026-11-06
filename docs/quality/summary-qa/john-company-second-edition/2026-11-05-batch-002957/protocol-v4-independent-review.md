# Independent protocol v4 review

**Changes requested in the checker.** V4 itself remains generic, identical between readers except role/path, blind, and complete-bank. It requires actual per-clause facts/results and minimal explicit case conclusions while avoiding duplicated long extracts.

The section boundary, line, hash and full-literal-presence algorithms match the protocol. Unsupported clauses can correctly have no supporting section. The checker explicitly makes no semantic correctness or relevance claim.

Two concrete issues were reproduced using synthetic in-memory inputs only:

1. A complete selected section duplicated twice in the answer body still passes with one metadata entry. The checker checks presence, not the required exactly-once identified attachment. It also does not bind the source copy to its answer-body section ID. Define an unambiguous attachment format and verify one complete attachment per selected ID if this is to be mechanically certified.
2. An unknown question ID raises `KeyError` instead of recording an invalid-ID error, aborting the validation run. Guard that lookup and continue collecting structural errors.

Keep these repairs structural. Unsupported clauses must remain able to use empty section lists; semantic relevance and requested-fact correctness require independent review. The checker CLI reads both readers’ outputs and therefore must remain a coordinator-side check, not an expansion of blind-reader access.

Only the two assigned inputs were read; no actual reader files, grades, results, histories or scores were accessed or inferred. No fixture files were written.

Read hashes:

- `blind-reader-protocol-user-scope-v4.txt`: `38b1354b73561b1b160cacc845ebc4b738dfb69a88b1bd1e332f70988985a654`
- `summary-section-check.py`: `c1c593998895c52ea651020d3b6a1ae2c142f2a899c1265f825a9e53585aeb34`
