# V5 protocol and same-entry tools — revision 01

**PASS within the stated protocol/tool scope.** All four earlier findings are resolved.

- Supporting quotes must be non-whitespace strings; empty/nontext quotes and covered parts without quotes are rejected.
- `case_conclusions` is explicitly a plain-string array. Nested metadata produces a format-review error while preserving the complete raw input; it is neither counted as support nor converted into a score cap.
- Same-entry quotation validation is unconditional across answer, ledger facts, case conclusions and operative evidence quotes.
- Original ordered IDs/count/uniqueness are checked before indexing in preparation and merge. Merge also compares complete packet entries with the original raw entries.

Independent synthetic tests also verified heading boundaries and hashes, exact source spans, once-only full section copies, explicit unsupported clauses without invented sections, exclusion of labels/locations/confidence, cross-entry isolation, lossless normal packet contents, preferred same-entry report selection and preservation of originals. The new `validate` path made no writes even with existing results; ordinary merge still refused to overwrite results.

V5 remains generic, identical except role/path, blind and complete-bank, with individual short exact facts, minimal requested case computations, complete sections and necessary cross-reference following. Structural/source-literal checks remain separate from semantic requested-fact grading. No question, key or asked-fact change is needed.

All tests used in-memory synthetic data and filesystem objects. Only the four authorized files were read; no actual bank, reader, grade, result, prior report, history or score was accessed or inferred. Prior reviews remain untouched.

Input hashes:

- `blind-reader-protocol-user-scope-v5.txt`: `0cdf7c426ae55deff4e8939226b9e0b1b3197ee6fea913fb9fbfd5fcda479e39`
- `summary-section-check.py`: `60d4c7b0768041e2ad735d5cbec71871516b4fa47fd7dc5a3a4dbb19298242fc`
- `summary-section-fact-check.py`: `b2c0e3cfc80a674a2a03585adc384ca443abdda5b094bfc3b000df257368c0c0`
- `block-grading-tools.py`: `f9df66b622d264975923fb85877a3c559898d0b0db4f233dc49b6c3f0f05a9f6`
