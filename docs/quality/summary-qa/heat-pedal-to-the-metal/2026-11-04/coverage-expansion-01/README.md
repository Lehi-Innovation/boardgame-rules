# Heat core rules coverage expansion

The question bank now contains **47 questions**, up from 20. Questions 21–47 add 27 distinct rules, outcome branches or consequential interactions. The original questions and answers are preserved unchanged. Both final gpt-6-luna readers answered all 47 correctly, and the final summary passed an independent source audit.

Read the complete [question and answer bank](question-bank.md), or use the separate [questions](questions.json) and [answer key](answer-key.json) for another test.

## Why expansion stopped at 47

A question qualifies as new when it tests a source-supported rule that was not asked before, an explicit condition with a different ruling, or an interaction where timing, priority or an exception changes the outcome. Changed numbers, names or phrasing within a covered branch do not qualify. Mechanical combinations of known rules do not qualify unless they introduce such a consequential interaction.

| Review pass | Focus | New questions |
|---|---|---:|
| 1 | Setup, action limits, Stress, movement, payment boundaries, cooling and Adrenaline | 21 (Q21–41) |
| 2 | Movement exceptions, phase order, lap scope, end conditions and conditional failures | 6 (Q42–47) |
| 3 | Challenge with alternate draws, gears, speeds, car counts, payments and finishing outcomes | 0 |
| 4 | Review the procedural source passages again and challenge remaining edge cases | 0 |

These four passes were sequential reviews by the parent evaluator, not independent author samples. A separate fresh source reviewer then checked all additions and their answers, challenged the claimed saturation, and returned **PASS with no findings or proposed additions**. It did not see the summary or reader outputs.

The [coverage ledger](coverage-ledger.json) records why each addition is distinct, maps procedural source passages to question IDs, and lists rejected candidates. For example, another double downshift duplicates Q2 and Q26–27; different corner speeds repeat the same already-tested excess/payment branches; another high-starting-car-count Adrenaline example duplicates Q7 and Q20. Exhaustion cases without an explicit ruling in this source and advanced modules require other authoritative material.

This is working saturation within the extracted core booklet and the stated novelty rule. Advanced play, expansions, component-count trivia and unsupported edge-case answers were excluded. It does not establish that every conceivable question about Heat has been enumerated.

## Coverage added

| Topic | New question IDs |
|---|---|
| Lap selection, board-defined setup quantities, starting grid, Stress reserve and veteran handicap | 21–25 |
| Maximum shift, immediate shift payment and avoiding Cluttered Hand by a legal shift | 26–27, 47 |
| Resolving multiple Stress cards and distinguishing found cards from hand commitments | 28 |
| Exact movement and the difference between blocked distance and corner-check speed | 29–30 |
| Corner-crossing trigger, zero and exact payment, later-corner failure and low-gear spin-out penalty | 31–35 |
| First-gear cooling plus Adrenaline, optional independent benefits and turn-order eligibility | 36–38 |
| Slipstream positions, eligibility after Boost, multiple qualifying cars and occupied landing spaces | 39–42 |
| Pre-finish versus post-finish corners, intermediate laps and continuing after the winner finishes | 43–45 |
| Corner Lines versus Legends Lines in the core game | 46 |

## Expanded test and repairs

Each iteration used two new gpt-6-luna readers at high reasoning effort, with no parent chat history. Each reader received only that iteration's frozen summary and question copy. The source, fixed key, previous answers, grades and reviewer findings were excluded. Actual model settings were confirmed from session metadata in [model-provenance.json](model-provenance.json).

The original 20 entries remain identical to the original benchmark. All 47 questions and expected answers were frozen before reader dispatch and remained unchanged during repairs. The evaluator graded requested material rulings semantically against the key, independently of reader confidence/support labels.

| Iteration | Reader A correct | Reader B correct | Partial answers combined | Incorrect answers combined |
|---|---:|---:|---:|---:|
| Expanded bank against the previous summary | 42/47 | 43/47 | 9 | 0 |
| First repair | 47/47 | 46/47 | 1 | 0 |
| Final repair | **47/47** | **47/47** | **0** | **0** |

The first expanded test exposed missing veteran-handicap and Legends Line rules, plus unresolved starting-grid assignment, exact movement and intermediate-lap behavior. Repairs added those source-supported details and clarified occupied Slipstream destinations. A later reader correctly stated that Adrenaline cooling can be used without extra speed, then called that same choice unsupported. The final repair explicitly separates those benefits, states the single non-stacking Slipstream move, and explains optional cooling up to the allowance.

Grading follows the meaning of each ruling rather than requiring a particular sentence. Final reader A uses Race Line position as shorthand in Q18 and explicitly defines the closest car as ahead in Q4. Final reader B labels Q40 partially supported because there is no worked Boost example, but gives the complete correct eligibility ruling and phase-order evidence. These grading notes are preserved in the final results. Neither answer leaves a requested ruling unresolved. In contrast, the inconsistent unsupported caveat on the requested Adrenaline choice in iteration 2 was counted as partial and repaired.

The final source auditor was separate from the question-bank reviewer, the readers and the repairer. It saw only the summary and complete authoritative extracted rulebook. Both revised snapshots received a source-audit PASS; the final audited snapshot is the exact text given to the final reader pair.

## Evidence

- [Source and novelty review](coverage-review.json), [coverage and rejection ledger](coverage-ledger.json), and [benchmark input hashes](input-manifest.json).
- Iteration 1: [summary](luna-iteration-01/summary-snapshot.md), [reader A](luna-iteration-01/reader-a.json), [reader B](luna-iteration-01/reader-b.json), and [all grades](luna-iteration-01/results.json).
- Iteration 2: [summary](luna-iteration-02/summary-snapshot.md), [reader A](luna-iteration-02/reader-a.json), [reader B](luna-iteration-02/reader-b.json), [all grades](luna-iteration-02/results.json), and [source audit](luna-iteration-02/source-audit.json).
- Final iteration 3: [summary](luna-iteration-03/summary-snapshot.md), [reader A](luna-iteration-03/reader-a.json), [reader B](luna-iteration-03/reader-b.json), [all grades](luna-iteration-03/results.json), [source audit PASS](luna-iteration-03/source-audit.json), and [summary changes](luna-iteration-03/summary-changes.patch).
- [Final validation](validation.json) checks original-entry preservation, all 282 reader answers and grades, hashes, models, source references, document links and equality of the canonical summary with the final tested snapshot.

The source is the same authoritative core-rule extraction used in the original Heat pilot. The question bank is now a regression suite; neither its expansion nor repeated testing is a held-out accuracy study. Earlier reports and their passing snapshots remain historical evidence for their own question-bank versions.
