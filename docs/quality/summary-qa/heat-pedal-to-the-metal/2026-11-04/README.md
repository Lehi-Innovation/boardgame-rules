# Heat summary question-answer evaluation — November 4, 2026

This pilot tests whether a reader can answer table questions using only the collection's Heat: Pedal to the Metal summary. The scope is the core game, excluding advanced modules and expansions.

## Results

| Reader | Fully correct | Partial / unresolved | Incorrect |
|---|---:|---:|---:|
| A | 7/20 (35%) | 12/20 (60%) | 1/20 (5%) |
| B | 8/20 (40%) | 11/20 (55%) | 1/20 (5%) |
| Total answer attempts | 15/40 (37.5%) | 23/40 (57.5%) | 2/40 (5%) |

Both readers made the same material error: they permitted Slipstream across the final finish line. The summary prohibits Slipstream only **after** crossing, while the source additionally prohibits crossing that line with Slipstream. This omission produced an affirmative wrong answer from both readers, each labeling its answer supported.

Most other failures were explicit abstentions on missing details. These percentages measure complete answers to this specific multi-part test, not a general claim that only 35–40% of the summary's rules are accurate. Some abstentions also reflect reader conservatism: B correctly deduced that an empty Engine cannot pay for Boost and that Stress flips resume after a reshuffle, while A declined to make those deductions. A correctly combined Cluttered Hand with generic cleanup, while B left the covering Heat cards' cleanup unresolved.

## Comparison of all 20 questions

The complete question wording, expected answers and raw answers are in the linked artifacts below. This table captures the material comparison; source references are line numbers in the frozen authoritative extraction, not PDF page numbers.

| # | Topic and expected ruling | A | B | Missing or misleading detail |
|---|---|---|---|---|
| 1 | Initial deck: 12 Speed + 3 upgrades + 3 Stress; 6 Heat in Engine; 1st gear; draw 7 | Correct | Correct | None |
| 2 | May stay in gear; two-position shift costs 1 Heat immediately, Engine → discard | Partial | Partial | Staying put and precise payment timing |
| 3 | 3rd gear requires exactly 3 face-down cards | Correct | Correct | None |
| 4 | Steps 1–2 simultaneous; then each player finishes 3–9; Race Line breaks position ties | Partial | Partial | Whole-turn sequencing and positional tie rule |
| 5 | May pass cars; a full destination pushes placement back to first free space, preferring Race Line | Correct | Correct | None |
| 6 | Flipped Heat/upgrade go to discard; Speed 3 joins played Stress in Play Area; resolve before Adrenaline | Partial | Partial | Destinations of flipped cards |
| 7 | Last two of five get +1 speed and Cooldown 1; speed may precede/follow Boost; cannot save | Partial | Partial | Timing flexibility and no carryover |
| 8 | May Cooldown 1 into Engine, then spend that Heat on Boost | Partial | Partial | React symbols may resolve in any order |
| 9 | Boost at most once, costs 1 Engine Heat; cannot pay from empty Engine; flip for Speed; counts for corners | Partial | Correct | A abstains on empty Engine |
| 10 | Optional two-space Slipstream across corner: speed stays 6; pay 2 Heat at limit 4 | Correct | Correct | None |
| 11 | At speed 8 check limits 6 then 4 separately; pay 2 + 4 = 6 Heat | Partial | Partial | Check every corner in crossing order |
| 12 | Pay remaining 2 Heat, spin out before corner, take 2 Stress **into hand**, set 1st gear | Partial | Partial | New Stress destination |
| 13 | May discard Speed, never Stress/Heat; nobody browses discard piles; only top card public | Partial | Partial | Discard visibility and inspection |
| 14 | Discard Play Area; refill hand to 7 | Correct | Correct | None |
| 15 | Immediately reshuffle discard excluding Play Area; resume required Stress flips | Partial | Correct | A abstains on continuation |
| 16 | Paid Heat: Engine → discard → deck → hand; Cooldown returns it; normally cannot play/discard | Correct | Correct | None |
| 17 | Commit 2 playable + 2 Heat; move 0; 1st gear; discard commitment; skip React | Correct | Partial | B abstains on covering Heat cleanup |
| 18 | Furthest same-round finisher wins; Race Line breaks tie; remove finishers at round end | Partial | Partial | Removal timing |
| 19 | Cannot Slipstream across or after final finish line; ignore corners beyond it | Incorrect | Incorrect | Both incorrectly permit crossing via Slipstream |
| 20 | Six starters means last two receive Adrenaline, even with only two left | Partial | Partial | Use starting field size |

## Recommended summary changes

Highest priority: explicitly forbid Slipstream **across** the final finish line, as well as after crossing it (source lines 361–365).

Both readers also exposed these source-backed coverage gaps:

- Allow remaining in the same gear; state that double shifts pay Heat immediately (142–149, 333–346).
- Say that each player completes steps 3–9 before the next starts, and the car nearest the Race Line is ahead for all purposes (156–161, 187–188).
- Explain where Stress/Boost flips go: discard non-Speed cards, add the found Speed to played cards, keep played Stress until cleanup (189–207, 229–235, 249–256, 301–308).
- State Adrenaline's before/after-Boost flexibility, React timing and no carryover; specify that the starting car count governs eligibility after finishers leave (209–218, 366–371).
- Permit React symbols in any order, including Cooldown before Boost (219–228).
- Check every crossed corner separately in crossing order (267–280).
- Put spin-out Stress directly into hand (281–289).
- Forbid browsing any discard pile and state that only its top card is public (290–300).
- Remove finished cars at the end of the round (356–371).

Useful clarifications for the divergent answers: explicitly state that Boost needs available Engine Heat, interrupted draws/flips resume after reshuffling, and all committed Cluttered Hand cards enter discard (309–316, 333–355). These are lower-priority clarity improvements because the existing summary already supports the successful reader's deductions.

No canonical rules edits or verification-status changes were made during this evaluation. Repair and a fresh-question retest would be a separate step, keeping this baseline intact.

## Method

1. The evaluator read the complete authoritative extracted core rulebook at `extracted/heat-pedal-to-the-metal-rules.txt` and the existing summary.
2. The evaluator wrote 20 questions and a source-backed answer key, including exact extraction line references, before dispatching readers.
3. The questions, key, original summary and source were fingerprinted in `input-manifest.json`. A byte-identical summary copy was frozen as `summary-snapshot.md`.
4. Two fresh-context subagents independently received the same 20 questions and summary. Neither inherited this chat. They were instructed to read only those two files, avoid browsing and prior game knowledge, and explicitly identify unsupported answers. Their only permitted output was their assigned response file.
5. The evaluator compares each answer with the predetermined key. The readers receive no corrective feedback before grading.

The authoritative input for this run is the local extracted rulebook, rather than a newly downloaded PDF. A [publisher-hosted core rulebook](https://cdn.svc.asmodee.net/production-daysofwonder/uploads/2024/07/9101-HT-Rules-EN.pdf) was located, but retrieval failed; this run does not claim a fresh PDF-to-extraction comparison.

## Scoring

- **Correct:** all requested material facts match the predetermined answer.
- **Partial:** some requested facts are omitted or explicitly identified as unsupported, with no contradictory ruling.
- **Incorrect:** at least one material ruling contradicts the source, even if other parts are right.

The headline measure is fully answered questions out of 20 for each reader. Compound questions require every requested part; partial answers do not receive fractional credit. Missing information is reported separately from incorrect rulings. Correct claims without summary support are flagged separately because they do not establish summary coverage.

## Artifacts

- [questions.json](questions.json): all 20 questions, without expected answers.
- [answer-key.json](answer-key.json): predetermined answers and source line references (inclusive start/end pairs).
- [summary-snapshot.md](summary-snapshot.md): unchanged summary supplied to both readers.
- [input-manifest.json](input-manifest.json): input SHA-256 hashes and isolation design.
- [reader-a.json](reader-a.json) and [reader-b.json](reader-b.json): independent raw responses and stated support.
- [results.json](results.json): per-question grades and reasons.

## Limits

This is a targeted diagnostic set, mixing routine rules with edge cases, not a random or exhaustive sample of all Heat questions. The evaluator saw the summary when designing it, and two model readers are not a representative user population. Reader isolation is enforced by fresh contexts and tool-use instructions, not separate filesystem permissions. The evaluator is also the answer-key author and grader; raw outputs and source references are retained for review. A summary's existing verification label measures a different property from its ability to answer every requested detail here. This run leaves the canonical summary and catalog metadata unchanged.
