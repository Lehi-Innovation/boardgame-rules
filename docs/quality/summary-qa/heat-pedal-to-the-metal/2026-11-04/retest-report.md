# Heat summary repair and retest — November 4, 2026

Both fresh readers answered all 20 original questions correctly from the final summary. Each used **gpt-6.1-sol, high reasoning effort**, confirmed from local session logs. A separate source auditor passed the final summary against the complete authoritative extracted core rulebook.

| Version | Reader A fully correct | Reader B fully correct | Partial answers | Incorrect answers | Independent source audit |
|---|---:|---:|---:|---:|---|
| Original baseline | 7/20 | 8/20 | 23 combined | 2 combined | Not part of baseline run |
| Revision 1 | 20/20 | 20/20 | 0 | 0 | MINOR: two setup omissions |
| Final revision 2 | **20/20** | **20/20** | **0** | **0** | **PASS** |

## What changed

The canonical summary at `rules/heat-pedal-to-the-metal.md` now explicitly covers every material gap found in the original test:

- Staying in gear and paying for double shifts immediately from Engine to discard.
- Finishing each player's steps 3–9 before the next player acts, with Race Line position breaking ties.
- Where flipped Stress/Boost cards go, when Stress resolves, and how played Stress is cleaned up.
- Adrenaline timing, no carryover, and use of the starting field size after cars finish.
- React symbols in any order, including cooling Heat before spending it on Boost.
- Required Engine Heat for Boost and its contribution to corner speed.
- Checking every crossed corner separately in crossing order, including corners crossed while Slipstreaming.
- Spin-out Stress going directly into hand.
- Discard-pile inspection restrictions and top-card-only public information.
- Resuming interrupted draws/flips after reshuffling.
- Explicit Cluttered Hand commitment, Heat cleanup, and skipped React.
- Finishers leaving at round end, and no Slipstream **across** or after the final finish line.

The independent auditor additionally identified two small setup omissions in revision 1. Final revision 2 adds the lap count printed on the selected board, the source's optional one-lap USA learning race, and a face-up reserve of spare Stress cards. The auditor then returned PASS with no findings. The final readers saw this exact revision, rather than the earlier passing version.

## Test controls and grading

The original [20 questions](questions.json), [predetermined answer key](answer-key.json), and authoritative extraction were unchanged throughout. SHA-256 checks confirm that the key and source still match the original baseline manifest. Each revision has its own frozen summary, question copy and input manifest.

Each revision used two new reader subagents with empty parent histories, explicitly selecting gpt-6.1-sol/high. Readers were instructed to read only their summary snapshot and question file, avoid prior game knowledge and browsing, and identify unsupported facts. They did not receive the source, answer key, previous answers, grades or audit findings. The source auditor was separate from all four readers and the summary author; it did not see the questions, key or reader responses.

The parent evaluator compared every requested part of all 20 answers per reader against the original key. A fully correct answer requires all requested material facts, with no unresolved part or contradictory ruling. Reader support labels alone were not treated as proof of correctness. Every final answer meets that standard; both readers now prohibit Slipstream across the final finish line.

The final frozen snapshot is byte-identical to the canonical summary. Fresh contexts and tool-use instructions provide context isolation; the files were not protected by separate filesystem access controls. This is a regression test on the known 20-question set, not a held-out or exhaustive accuracy measurement.

## Evidence

- [Original baseline report](README.md), [raw A answers](reader-a.json), [raw B answers](reader-b.json), and [baseline grades](results.json).
- Revision 1: [snapshot](iteration-01/summary-snapshot.md), [raw A answers](iteration-01/reader-a.json), [raw B answers](iteration-01/reader-b.json), [all 40 graded answers](iteration-01/results.json), [source audit](iteration-01/source-audit.json), and [model provenance](iteration-01/model-provenance.json).
- Final revision 2: [snapshot](iteration-02/summary-snapshot.md), [raw A answers](iteration-02/reader-a.json), [raw B answers](iteration-02/reader-b.json), [all 40 graded answers](iteration-02/results.json), [source audit PASS](iteration-02/source-audit.json), [model provenance](iteration-02/model-provenance.json), and [baseline-to-final diff](iteration-02/summary-changes.patch).
- [Final validation checks](iteration-02/validation.json).

## Validation

The summary passes the repository's structural validator. The published catalog check passes for all 1,665 summaries. Regenerated index and manifest content match the existing published artifacts, ignoring the manifest's generation date. Whitespace checks pass. Artifact validation checks all question IDs, all 80 retest answers and grades, input hashes, unchanged original questions/key/source, model provenance, and equality of the final snapshot with the canonical summary.

The source is the same local authoritative extraction used for the original test. This run does not claim a newly downloaded PDF comparison or an accuracy guarantee for untested questions.
