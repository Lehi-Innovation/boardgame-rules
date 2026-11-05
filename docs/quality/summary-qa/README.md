# Rules summary question answering workflow

Use this workflow to test whether an assistant can answer table questions from a game's summary alone, then repair gaps against the authoritative rules. Each run uses a fixed set of 20 questions and two independent readers. Continue until both readers answer all 20 completely and correctly from the exact final summary.

This complements the repository's [semantic audit](../../../CLAUDE.md#semantic-audit): source auditing checks the summary's rules, while this test checks whether readers can recover and apply them. A passing question set does not replace an independent source audit.

## Roles and access

| Role | Inputs | Responsibility |
|---|---|---|
| Evaluator | Authoritative rules, questions, fixed answer key, summary and reader outputs | Prepare the key, grade every requested part and retain evidence |
| Reader A | Frozen summary and questions only | Independently answer all 20 questions |
| Reader B | The same frozen summary and questions only | Independently answer all 20 questions |
| Repairer | Summary, source, key and findings | Correct the summary using source-supported rules |
| Source auditor | Revised summary and authoritative source | Independently check the final rules without seeing reader answers or the key |

The evaluator may also perform repairs and compare answers with the fixed key, as in the Heat pilot. The repairer must not be the independent source auditor. The two readers must not inherit the evaluator's chat or communicate with one another.

## Prepare the source and answer key

1. Select a game with both `rules/<slug>.md` and authoritative source material, usually `extracted/<slug>-rules.txt`. Read the complete relevant source. Identify the edition and scope, such as the core game without expansions. If the extraction is incomplete or a diagram is essential, inspect the source PDF before writing the key.
2. Write 20 questions covering routine play and consequential edge cases. Include timing, legal actions, card or component destinations, resource costs, exceptions, scoring and end conditions. Use concrete scenarios where they expose ambiguity. Keep every question within the chosen source's scope.
3. Write the expected answers before dispatching readers. Include every material fact requested by each question and exact source references. Label extraction line numbers as such; they are not PDF page numbers. Prefer source-first question design; record whether the evaluator also saw the summary when selecting questions.
4. Fix the grading standard before seeing reader answers. Save questions separately from the key, and fingerprint both plus the source with SHA-256. Do not disclose the key to readers.

Keep the 20 questions and key unchanged throughout a repair series. If a genuine source or key error is discovered, record the correction as a new benchmark version rather than silently changing the target to get a pass.

## Freeze each iteration

Use `docs/quality/summary-qa/<slug>/<date>/` for the evidence. Keep the initial baseline and every later iteration; do not overwrite failed responses.

| Artifact | Contents |
|---|---|
| `questions.json` | Game, scope and 20 numbered questions, without answers |
| `answer-key.json` | Predetermined answers, material facts and source references |
| `input-manifest.json` | Original input paths and hashes |
| `<iteration>/summary-snapshot.md` | Byte-for-byte copy of the tested summary |
| `<iteration>/questions.json` | Unchanged question copy supplied to readers |
| `<iteration>/input-manifest.json` | Snapshot, question, key and source hashes; requested model and reasoning effort |
| `<iteration>/reader-a.json` and `reader-b.json` | Original reader responses, support labels and summary evidence |
| `<iteration>/results.json` | Per-question grades, reasons, expected and observed answers, and totals |
| `<iteration>/model-provenance.json` | Actual model and reasoning settings, reader identities and runtime evidence |
| `<iteration>/source-audit.json` | Independent source verdict, findings and source references when audited |
| `<iteration>/summary-changes.patch` | Changes from the baseline or previous revision when applicable |
| `<iteration>/validation.json` | Input integrity, counts, model verification and repository checks |
| Run report | Iteration scores, changes, source-audit outcome and links to evidence |

Iteration names may include the model, such as `luna-iteration-01`. Record the exact model in metadata; a directory name does not establish which model ran.

Freeze inputs before dispatch. Readers should read the snapshot rather than a live file that may change during the run. Record the user's local date for the report and use timestamps when useful to establish ordering.

## Run two independent readers

Launch two new subagents for each iteration, each answering all 20 questions. In this environment, use `fork_turns: "none"` so neither inherits the parent chat. Set the requested model explicitly and keep reasoning effort consistent across comparisons. The Heat runs used `gpt-6.1-sol` and then `gpt-6-luna`, both at `high` effort.

Give each reader the same instructions, changing only its output path. Allow access only to its summary snapshot and question file. Exclude authoritative sources, the answer key, prior answers, grades, audit findings, browsing and prior game knowledge. Save the raw output before grading or giving feedback.

Verify the actual model and effort from runtime metadata when available. Distinguish requested settings from confirmed settings if runtime evidence is unavailable. In the Heat pilot, local session metadata and `turn_context` records confirmed both. Fresh contexts and instructions provide context isolation; stronger filesystem isolation was not used in that pilot.

### Reader prompt template

```text
You are an independent rules-summary reader in a blind evaluation.

Read ONLY these two input files:
<absolute path to summary-snapshot.md>
<absolute path to questions.json>

Do not read any authoritative rulebook, extracted text, answer key,
manifest, prior responses, other files, parent history or web links.
Do not browse. Use only the supplied summary as evidence, not prior
game knowledge. Do not communicate with other readers.

Answer all 20 questions, including every requested part. If a requested
fact is absent, explicitly identify that part as unsupported; do not guess.

For every question include:
- id
- answer
- support: supported, partial or unsupported
- evidence: a short quote or section from the summary

Save valid JSON to <absolute path to your assigned reader output> with
top-level fields reader, inputs_read and answers (an array).
You may read only the two allowed inputs and write only your assigned
output. Do not evaluate or improve the summary.
```

## Grade every requested part

The evaluator reads all 40 answers and compares them with the fixed key. Reader confidence and support labels are evidence to inspect, not grades to accept automatically.

| Grade | Definition |
|---|---|
| Correct | All requested material facts match the key, with no unresolved part or contradictory ruling |
| Partial | At least one requested fact is missing or explicitly unresolved, with no material contradiction |
| Incorrect | At least one material ruling contradicts the source, even if other parts are correct |

Treat an explicit abstention as partial rather than a wrong rule. Flag correct claims without summary support separately: a lucky guess does not demonstrate that the summary contains the answer. Record each gap or contradiction with the relevant source reference and reader evidence.

For compound questions, require every requested part for full credit. Report correct, partial and incorrect counts separately for each reader; do not hide omissions in a fractional score. These are complete-answer scores for the chosen questions, not the percentage of all rules in the game that are accurate.

## Repair and retest

1. For every partial or incorrect answer, check the authoritative source to determine whether the summary omits a rule, states it incorrectly or presents it ambiguously. Some abstentions reflect overly conservative reading; distinguish those from missing content in the report.
2. Update the canonical summary with general, source-supported rules. Preserve the game's terminology and explain timing, destinations and exceptions where needed. Avoid appending the answer key or rules invented solely to satisfy a scenario.
3. Have a separate source auditor check the revised summary. The auditor sees the source and summary, but no key or reader answers. Repair material findings and resolve any remaining findings before treating the summary as independently passed. If the summary changes after a passing reader pair, freeze and test the new text again.
4. Freeze the next iteration and launch two new readers with the same model, questions and instructions. Do not reuse the earlier readers: they have already seen the test and might have received additional context.
5. Compare all 40 new answers with the same key. Repeat until both readers score 20/20 with no partial, unresolved or incorrect answers and no unsupported guesses standing in for summary coverage.

If the first pair passes, no repair is needed. A prior independent source audit can be reused when the tested summary and source are byte-identical to the audited inputs; identify that evidence rather than claiming a new audit.

### Source auditor prompt template

```text
Independently audit <absolute path to revised summary snapshot> against
the complete authoritative source at <absolute source path>.

Check material claims, important omissions, timing, component destinations,
costs, exceptions and end conditions. Do not read the question set, answer
key, reader answers or grades, and do not communicate with the readers.
Do not edit the summary or assume that it should pass.

Save JSON to <assigned audit path> containing verdict (PASS/MINOR/MAJOR),
findings with severity and source references, and checked_claims.
```

## Test another model

Start the next model from the last passing summary, using a new reader pair and a separate iteration directory. Keep the same questions, key and reasoning effort, and record actual model provenance. Apply the same repair loop if the new model exposes a gap. If that repair changes the summary, rerunning earlier models on the new final text provides a regression check.

A model comparison on different summary versions does not isolate the effect of the model. Report the tested summary hashes alongside model results. Both final Heat model tests used the same summary bytes.

## Verify completion and report

Before claiming success, check all of the following against the saved files:

- Both reader outputs and both grade arrays contain IDs 1–20 exactly once, without missing or duplicate questions.
- Every saved grade corresponds to the original question, expected answer and actual reader response.
- Each reader has 20 correct, zero partial and zero incorrect answers, with all requested parts supported by the summary.
- The question, key and source hashes match the frozen originals.
- The final summary snapshot is byte-identical to the current canonical summary.
- Actual reader models and reasoning settings match the intended run, or any unverified settings are disclosed.
- An independent source audit covers the final text; no source-audit findings remain unresolved for a claimed PASS.
- Report links resolve and original responses, failed iterations and changes remain available.

Run the repository checks appropriate to the changes. For a rules edit, use:

```bash
.venv/bin/python -m scripts.validate rules/<slug>.md
.venv/bin/python -m scripts.stamp_verification rules/<slug>.md
.venv/bin/python -m scripts.generate_index
.venv/bin/python -m scripts.generate_manifest
.venv/bin/python -m scripts.catalog
git diff --check
```

Use the existing audit-recording and stamping workflow in [CLAUDE.md](../../../CLAUDE.md#verification--trust-stamping). A question-test pass alone must not overwrite semantic verification status. Stamp before freezing the final snapshot, or verify that stamping leaves it unchanged. In a shared worktree, preserve unrelated changes; generated artifacts can be regenerated in temporary files and compared before replacing live files.

The final report should state the game and source scope, model and effort, per-reader scores by iteration, what changed, source-audit outcome, validation results and evidence links. Describe success as passing the fixed 20-question regression set. Use a separately frozen, previously unseen set for a later held-out evaluation; passing the known set does not establish exhaustive coverage or general model equivalence.

## Heat pilot

The November 4, 2026 pilot used the extracted core rules for **Heat: Pedal to the Metal**. The original summary led both readers to permit Slipstream across the final finish line, an action explicitly forbidden by the source. Most other failures were unresolved details rather than affirmative wrong rulings.

| Summary and model | Reader A correct | Reader B correct | Outcome |
|---|---:|---:|---|
| Original summary, gpt-6.1-sol | 7/20 | 8/20 | Each reader gave one wrong ruling; the remaining non-passes were partial |
| First repaired summary, gpt-6.1-sol | 20/20 | 20/20 | Source auditor found two minor setup omissions |
| Final repaired summary, gpt-6.1-sol | 20/20 | 20/20 | Setup omissions fixed, exact final text retested, source audit PASS |
| Same final summary, gpt-6-luna | 20/20 | 20/20 | First pair passed; no further rules changes needed |

See the [baseline report](heat-pedal-to-the-metal/2026-11-04/README.md), [Sol repair and retest](heat-pedal-to-the-metal/2026-11-04/retest-report.md), and [Luna test](heat-pedal-to-the-metal/2026-11-04/luna-report.md) for the questions, key, raw responses, grades, summary snapshots, model provenance and source audits.
