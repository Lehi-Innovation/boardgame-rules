# Heat summary test with gpt-6-luna — November 4, 2026

Both fresh **gpt-6-luna** readers answered all 20 original questions correctly on the first attempt. No further summary changes were needed.

| Reader | Fully correct | Partial / unresolved | Incorrect |
|---|---:|---:|---:|
| Luna A | **20/20** | **0** | **0** |
| Luna B | **20/20** | **0** | **0** |
| Combined | **40/40** | **0** | **0** |

## Controls and grading

The test used the exact summary that passed the previous gpt-6.1-sol retest, without changing its contents. The original [20 questions](questions.json), [answer key](answer-key.json), and authoritative extracted rulebook are unchanged, confirmed against their original SHA-256 hashes.

Two new subagents were explicitly launched with gpt-6-luna and high reasoning effort. Local session metadata confirms those actual model settings for each reader. Both had fresh contexts with no parent chat history and were instructed to read only the frozen summary and questions, without the rulebook, answer key, previous answers, grading results, browsing or prior game knowledge. The reader prompts retained the same instructions as the Sol test, with only the input/output paths changed. Isolation relies on fresh contexts and tool-use instructions, not separate filesystem permissions.

The parent evaluator read all 40 raw answers and compared every requested part against the original source-backed key. Fully correct requires all requested material facts with no unresolved part or contradictory ruling. The results do not merely count each reader's own support labels.

Both readers correctly handled the previously troublesome finish-line rule: Slipstream is forbidden across the final finish line as well as after crossing it. Both also resolved all timing, card destination, corner payment, discard visibility, Cluttered Hand and Adrenaline questions.

## Source and summary integrity

The frozen Luna summary is byte-identical to both the current canonical `rules/heat-pedal-to-the-metal.md` and the final [Sol snapshot](iteration-02/summary-snapshot.md). That same text received an independent [source audit PASS](iteration-02/source-audit.json) in the previous run. No new source audit was necessary for this unchanged text, and no new source audit is claimed here.

The conditional repair loop stopped after the first pair: neither reader produced a partial, unresolved or incorrect answer, so this run makes no additional rules edits.

## Evidence

- [Frozen summary](luna-iteration-01/summary-snapshot.md), [question copy](luna-iteration-01/questions.json), and [input hashes](luna-iteration-01/input-manifest.json).
- [Raw reader A answers](luna-iteration-01/reader-a.json) and [raw reader B answers](luna-iteration-01/reader-b.json).
- [All 40 graded answers and expected answers](luna-iteration-01/results.json).
- [Actual model provenance](luna-iteration-01/model-provenance.json).
- [Validation results](luna-iteration-01/validation.json).
- [Previous Sol repair and retest report](retest-report.md).

## Validation and limits

Artifact checks verify all 20 IDs per reader, all 40 saved answers and grades, original input hashes, actual model settings, report links, and equality of the tested and canonical summary. The summary also passes the repository's structural validator.

This is a regression test on the known 20-question set. It is not a held-out or exhaustive accuracy measurement, and does not establish that Luna and Sol perform equally on other questions.
