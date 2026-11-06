# Coordinator prompt for rules summary QA across games

Replace the game list below, then paste the entire text block into a new local Codex chat. The prompt authorizes creating separate game chats and following them through completion. It does not authorize Git commits or pushes.

```text
Coordinate the rules-summary QA process below across these games. Create one
separate local Codex chat per game and work until the selected games reach the
completion criteria. Do the work, rather than stopping after a plan or dispatch.

GAMES:
- <game name or collection slug>
- <game name or collection slug>

SETTINGS:
- Repository: /home/jonny/projects/boardgame-rules
- Maximum active game chats: 3; queue additional games.
- Game-chat model: gpt-6.1-sol, high reasoning effort.
- Blind reader model: gpt-6-luna, high reasoning effort.
- Question/source reviewers: gpt-6.1-sol, high reasoning effort.
- Scope: each game's complete base/core rules. Record excluded optional modes
  and expansions; do not silently omit difficult core sections.
- Initial question target: 20, then expand until meaningful coverage saturates.
- Do not commit or push unless I separately request it.

LOCAL REFERENCES
Read these before dispatching, and give their absolute paths to every game chat:
/home/jonny/projects/boardgame-rules/CLAUDE.md
/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/README.md

Use this completed example for artifacts and methodology, not a question quota:
/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/heat-pedal-to-the-metal/2026-11-04/coverage-expansion-01/README.md

AUTHORIZATION AND CHAT COORDINATION
I explicitly authorize you to create the game chats, launch their reader and
reviewer subagents, and send continuation or corrective messages to the game
chats created for this batch. Use real separate chats for games, not merely
subagents in this coordinator chat. Readers and reviewers within a game should
be subagents of its game chat, not additional sidebar chats.

Use list_projects to identify this repository, then create_thread with that
project, the local environment, the configured model/effort, and a clear title
such as "Rules QA — <game>". Discover and follow the tools' actual schemas.
Use the existing local checkout; do not create worktrees for this request.

Resolve the exact collection slug, edition and authoritative source files before
dispatch. Deduplicate games and do not assign the same summary to two workers.
Check for an existing active owner of a requested game; queue that game rather
than starting a conflicting editor. If a name cannot be resolved uniquely from
the catalog, ask only for the missing identification while continuing other games.

Create a persistent batch goal and have each game chat create a persistent goal
for its assigned objective. Do not set an arbitrary token budget. Keep a batch
manifest under docs/quality/summary-qa/batches/<unique-run-id>/ recording each
game, chat/host IDs, assigned paths, status, question count, final reader scores,
source-audit outcome, report path, and any blocking reason. Reuse recorded chats
when resuming this batch rather than dispatching duplicates.

Creation is asynchronous: wait for actual worker progress. Monitor using compact
wait_threads snapshots with cursors and bounded waits. Inspect a chat in detail
only when necessary. If a worker stops before meeting the criteria, inspect its
evidence and send a targeted continuation when it is idle. Keep processing other
games while one needs source material or user input. Workers should report in
their own chats and files; they do not need to send messages back to this chat.

INCLUDE THIS WORKER BRIEF IN EVERY GAME CHAT
Identify the assigned game, summary, source files and unique output directory
explicitly in its initial prompt, then include all the following requirements.

1. Follow the local QA guide. Read the complete authoritative source for the
   exact edition and scope. Inspect the source PDF when text extraction or
   diagrams are insufficient. Do not invent rules or treat the summary as its
   own authority. If an essential ruling cannot be sourced, record the precise
   gap and what would resolve it; do not quietly skip it or declare success.

2. Prepare an initial bank of 20 meaningful questions with predetermined answers
   and source references before dispatching readers. Reuse an existing larger
   bank as the baseline if one already exists; do not shrink it. If the source
   genuinely supports fewer distinct questions, document that with independent
   coverage review rather than padding the set to reach a number.

3. Run two fresh blind reader subagents using gpt-6-luna/high. Use
   fork_turns="none" and explicitly select the model and reasoning effort.
   Give each only a frozen summary snapshot and question file, using the guide's
   reader prompt. Exclude sources, keys, earlier responses, grades, reviewer
   findings, parent history, browsing and prior game knowledge. Verify actual
   models from runtime metadata; never silently substitute another model.

4. Compare every requested part of every answer against the fixed source-backed
   key. Record correct, partial and incorrect separately, with per-question
   evidence and reasons. Judge the answer, not its confidence/support label.
   Each answer must resolve all its requested parts; do not borrow missing facts
   from another answer to manufacture a pass. Accept equivalent wording, but
   retain material omissions, unsupported guesses, wrong rulings and contradictory
   caveats as findings. Seek fresh independent adjudication if a case is borderline.

5. Repair summary gaps and ambiguities using general source-supported rules,
   not an appended answer key. Freeze the next version and rerun the entire bank
   with two new readers. Keep questions and expected answers fixed throughout
   each repair series. Preserve all failed iterations and raw outputs. Explicitly
   version a genuine source/key correction rather than changing the target silently.
   Continue until both readers answer the initial bank completely and correctly.

6. Expand beyond the initial bank. Map procedural source passages to questions.
   Accept a new question only for a new rule, a rule-defined outcome branch, or
   an interaction where timing, priority or an exception changes the ruling.
   Reject cosmetic rewording, changed numbers within an already covered branch,
   and mechanical recombinations without a distinct timing or exception issue.
   Preserve earlier IDs, wording and answers in each expanded bank version.

7. Keep a coverage map and acceptance/rejection ledger. Continue targeted passes
   until two consecutive passes produce no meaningfully new source-supported
   questions after all core procedural passages have coverage. Then have a fresh
   source/coverage reviewer challenge the bank and key, without seeing the summary
   or reader outputs. If it finds a real gap, add it and repeat the stopping check.
   Twenty is a seed and Heat's 47 is an example; neither is a universal cap or quota.

8. Freeze the complete expanded bank and its key before testing. Run all N
   questions, including the originals, with two fresh Luna readers. Repair and
   rerun until both independently score N/N with zero partial, unresolved or
   incorrect answers and no unsupported guesses replacing summary coverage.
   Do not relax grading, remove hard questions or reuse informed readers to pass.

9. Obtain an independent final source audit from a fresh reviewer that has not
   authored the repairs or seen the questions, key or reader responses. Give it
   only the final summary and authoritative source. Resolve findings before
   claiming PASS. If repairs or audit feedback change the summary after a passing
   pair, rerun the full bank on that exact new text and update the audit as needed.
   If audit feedback reveals an untested core rule, reopen coverage expansion.

10. Save evidence under the assigned unique
    docs/quality/summary-qa/<slug>/<run-id>/ directory: readable question/answer
    bank, separate question and key JSON, source references, coverage/rejection
    ledger, reviewer reports, input hashes, every frozen summary and question
    copy, raw reader responses, detailed grades, actual model provenance, diffs,
    source-audit outcomes, validation results and a readable final report.
    Never overwrite historical runs. Confirm original entries and hashes remain
    intact within their benchmark versions, every expected ID appears once per
    reader, and the final snapshot matches the canonical summary byte for byte.

SHARED WORKTREE RULES
Give each game chat exclusive ownership of rules/<its-slug>.md and its assigned
QA output directory. All workers may read shared documentation and sources.
Workers must not edit another game's files, shared instructions, games.yaml,
games.json, index.md, global audit registries or shared scripts; must not run
global regeneration/stamping jobs; and must not commit, push, switch branches,
reset or discard other work. These constraints override generic shared-file
regeneration steps in the guide. If another process changes an assigned source
or summary unexpectedly, preserve the evidence and coordinate before overwriting.

Keep shared catalog/audit updates in this coordinator chat. After workers finish,
record only the completed games' actual independent source verdicts through the
repository workflow. Stamp only their summaries and handle index/manifest
regeneration sequentially, preserving unrelated changes. If stamping changes the
tested summary bytes, send it back for a final test of that exact version.

Validate each changed summary and its artifacts. Use temporary regenerated files
or targeted comparisons when the checkout contains unrelated work; do not rewrite
shared files blindly. Report a genuine validation problem and its scope instead
of hiding it or attributing another game's failure to a completed worker.

COMPLETION AND REPORTING
A game is complete only when its coverage stopping rule and independent coverage
review hold, both final Luna readers score N/N on the full unchanged bank, the
independent source audit is PASS, and saved evidence verifies the exact canonical
summary, source/key integrity, reader models, and relevant repository checks.
Treat a partial or missing result as incomplete. Mark persistent goals complete
only after inspecting that evidence; use the host's actual blocked-goal rules
when progress genuinely requires external input rather than inventing a pass.

Report a table of game, question count, iterations, both reader scores, source
audit, status, and links to its chat and final report. Include concrete blockers
for unfinished games and a batch report with evidence paths. Describe coverage
as working saturation within each documented source/scope, not a proof of every
conceivable scenario or an exhaustive model-accuracy claim. Keep working until
every game is complete or genuinely awaiting identified external input.
```
