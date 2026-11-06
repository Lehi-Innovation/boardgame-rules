# V7 hierarchical protocol/tool review

**Changes requested in the checker.** The v7 protocol itself passes: it stays generic, blind, identical except role/path and full-bank, with one-question-at-a-time manual semantic choices and no game hints or forced guesses.

Core hierarchy tests pass. Level1 closes subtrees without becoming selectable; levels2–6 get distinct T/I IDs. Nested, skipped and repeated headings, Unicode character offsets, physical LF lines, exact untrimmed hashes, EOF and trailing whitespace behave as specified. Parent/child overlaps and leaf aliases fail, while adjacent intro/child unions pass. Declared selected blocks reject cropping, wrong labels, duplication and wrong source order. Exact short facts reject invented/wrong-source/whole-unit substitutions; honest unsupported clauses need not invent a section. Reserved source markers and recognized fences are deliberately rejected. Distinct disjoint units with identical literal text remain valid.

Three concrete gaps were reproduced in memory:

1. **Undeclared attachment syntax is ignored.** Unknown/unselected extra blocks and dangling unselected markers pass. Parse the entire reserved marker namespace and require exactly the selected, well-formed blocks, with no extras, unknowns or unmatched tokens.
2. **Unmarked long duplicates still pass.** A complete selected subtree repeated under an unmarked Direct Answer after its valid block is accepted, despite the protocol’s no-duplicate-volume rule. Extend checking or explicitly record a separate no-unmarked-duplicate check. Keep valid ID-distinct identical source units supported.
3. **Some nontext IDs crash.** A None selected ID or list-valued fact source causes TypeError. Validate ID/container types first and record a technical format error or intentional format-review exception while preserving raw input.

These are format-proof issues, not content grades. The checker correctly disclaims semantic relevance/completeness/calculation proof and any automatic content-score cap. No asked facts, keys or substantive grading rules need changing.

Only the two authorized inputs were read. All source/question/entry tests were synthetic and in memory. No real candidate, question bank, reader, key, scope, grade, result, history, status or score was accessed or inferred. Old files/reviews remain untouched.

## Input hashes

- `blind-reader-protocol-user-scope-v7.txt`: `02f4adf3a1e9ca4655964014f711a35dbd55a651f2e65842748de1406645ca25`
- `summary-hierarchical-section-check.py`: `2703d81b2aa6d538ab83d3f574b9f77eb28944aa3be856c66c5953f5964566d6`
