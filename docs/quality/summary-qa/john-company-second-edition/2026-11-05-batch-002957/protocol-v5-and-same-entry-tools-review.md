# V5 protocol and same-entry tools review

**Changes requested in the block tools.** V5 itself passes: it stays generic, identical except role/path, blind and complete-bank. It requires individual request ledgers, short exact ordinary facts, minimal concrete case computations, full selected source sections and necessary cross-reference following. The two source checkers correctly remain structural/literal rather than semantic graders.

Four concrete edge cases were independently reproduced in memory:

1. `reader_quotes: [""]` passes as support for a covered material part. Require non-whitespace quotation strings before literal matching.
2. Recursive `case_conclusions` flattening includes nested confidence/location labels. A confidence-only quote was accepted. Constrain conclusion shape or extract factual leaves while excluding metadata; retain the raw entry intact.
3. Even with `grades-same-entry.json` selected, quotes outside `answer` are rejected unless a separate clarification-marker file exists. Activate v5’s declared same-entry policy explicitly, or validate a recorded policy version rather than silently falling back to answer-only.
4. `prepare` silently collapses duplicate raw IDs into a dictionary, discarding an earlier complete entry while claiming losslessness. Validate original ordered IDs/counts/uniqueness before indexing them.

Positive tests confirmed exact source-span validation, rejection of invented/unselected/whole-section fact quotes, unsupported clauses without forced source sections, normal full-entry preservation, preference for `grades-same-entry.json`, preservation of original grade files, and rejection of results overwrites.

Only the four authorized files were read. All test source/question/answer/grader data and filesystem operations were synthetic and in memory. No actual reader, bank, grade, result, report history or score was accessed or inferred. These findings require no question, key or asked-fact change.

Input hashes:

- `blind-reader-protocol-user-scope-v5.txt`: `1f59353a5a996ffc1635e9b964cab7068860ef224da48e0991cce23297ed5458`
- `summary-section-check.py`: `60d4c7b0768041e2ad735d5cbec71871516b4fa47fd7dc5a3a4dbb19298242fc`
- `summary-section-fact-check.py`: `b2c0e3cfc80a674a2a03585adc384ca443abdda5b094bfc3b000df257368c0c0`
- `block-grading-tools.py`: `3f976f65468e3530c77eb6186aac78255b7eb39218b413c6f0d5d9b28ef99bba`
