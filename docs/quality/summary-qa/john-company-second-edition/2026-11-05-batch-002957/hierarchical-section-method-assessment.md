# Hierarchical section method assessment

The retrieval risk is real: **v6’s parent unit is an introduction, not the entire procedure beneath that heading.** The checker implements that definition correctly. Passing its boundary/hash check therefore does not establish that descendant procedures, conditions or outcomes were selected. No current reader error or score is inferred.

This assessment is **prospective only, for a future test after the current full pair is graded**. It does not authorize changing the current protocol, checker, raw outputs, key, scope or grades.

## Clear future semantics

- **Introduction:** heading through the character before the next recognized heading, at any level.
- **Subtree:** heading through the character before the next recognized heading of equal or higher level, or EOF. All deeper descendants are included.
- **Explicit union:** separately identified complete intro/subtree slices, such as needed ancestor introductions plus relevant child subtrees. A union omitting siblings must not be represented as a complete parent subtree.

The model should choose the smallest appropriate set supplying the actual requested facts and qualifiers. Code may index, validate and copy that selection; it must not route questions or infer relevance. A broad procedure may warrant the parent subtree. A narrower request may warrant an explicit union plus needed external definitions/exceptions.

## Algorithm and checker recommendations

Build a source-only heading table with level, parent and offsets. For each heading, calculate both next-heading intro end and next-equal/higher-heading subtree end. Give the two kinds distinct future IDs or namespaces and record the method version, source hash, kind, heading, full offsets/lines and exact untrimmed slice hash. Never silently reuse a v6 H-number for a larger range.

Sort selected half-open intervals and require `previous.end <= next.start`. Reject selecting a parent subtree with any overlapping descendant; allow adjacent intro/child units. Copy complete selected slices in source order. Check each short fact quote against its declared selected unit and verify one complete identified attachment block per unit. ID-aware block checks are preferable to free substring counts when text can repeat or occur inside a larger subtree.

Freeze the heading lexer too. Top-level headings should close lower-level subtrees even if not selectable; fenced-code handling, skipped levels, root/preamble text, repeated titles and EOF/newline behavior need explicit decisions. Alternatively, retain the existing lexer to isolate the endpoint change, but describe the rule precisely as equal/higher **recognized** headings and keep its limitations explicit. Broader parsing support is a separate versioned change.

## Risks that hierarchy does not remove

A child can omit shared parent conditions. Exceptions and definitions can live outside its subtree; a common final condition can also be placed under the last child by the document’s layout. Readers must still compare governing procedure/condition, actor and requested result, and follow references. Large subtrees can add unrelated siblings and output pressure. Keep short individual fact quotes and minimal requested case calculations; attachment volume is not substantive correctness.

Synthetic in-memory checks confirmed introduction versus subtree ranges, child/grandchild inclusion, equal/higher-level stops, exact union reconstruction, overlap rejection and full-slice hashes. No real source/question/reader data or fixture files were used.

A future test must freeze the method and checker before giving both fresh readers identical instructions. Preserve the existing pair and its original grading rules. No per-question mappings, retroactive attachments or scoring relaxation are proposed.

## Read hashes

- `blind-reader-protocol-user-scope-v6.txt`: `715ba0eee1f102b06b92a0b1975d30804a8782ac116d685ead63c14852b54019`
- `summary-section-check.py`: `60d4c7b0768041e2ad735d5cbec71871516b4fa47fd7dc5a3a4dbb19298242fc`
