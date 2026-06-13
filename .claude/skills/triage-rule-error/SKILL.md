---
name: triage-rule-error
description: Use when triaging a user-filed `rule-error` issue — verifies the reported error against the extracted rulebook text and either fixes the summary via PR or replies with evidence. Dispatched by the rule-error-triage GitHub workflow or run manually.
---

# Triage a Reported Rules Error

A user reported that a rules summary gave a wrong answer at the table. Your
job: check the report against the **extracted rulebook text** (the only
source of truth), then either fix the summary or explain why not.

## Step 1 — Parse the report

Read the issue (use `gh issue view <number>` or the provided body). Extract:
- **game** (name or slug — slugify: lowercase, hyphens)
- **claim** (what the summary says)
- **correction** (what the user says the rule actually is)
- **source** (where they checked, if given)

Find the files: `rules/<slug>.md` and `extracted/<slug>*.txt`.

## Step 2 — Verify against the source

**Never use outside knowledge of the game. Never trust the report blindly —
users misremember rules too.** The extracted text decides.

1. Grep the extracted text for the rule in question (try several phrasings;
   OCR text is messy).
2. Read ±20 lines around each match.
3. Reach one of three conclusions:
   - **CONFIRMED** — the source contradicts the summary the way the user says.
   - **REJECTED** — the source supports the summary as written.
   - **UNDETERMINED** — the source doesn't settle it (missing text, ambiguous,
     or no extracted file exists).

## Step 3 — Act on the conclusion

### CONFIRMED
1. Create a branch: `rule-error/<slug>-issue-<number>`.
2. Fix `rules/<slug>.md`: correct the claim everywhere it appears (body,
   Player Reference table). Match the existing style. Do not change anything
   the finding doesn't require.
3. Run `python -m scripts.validate rules/<slug>.md` to confirm structure.
4. Commit, push, and open a PR titled `rules(<slug>): fix <short description>`
   whose body quotes BOTH sides: the old summary text and the source text
   that contradicts it, and closes the issue (`Closes #<number>`).

### REJECTED
Comment on the issue with the exact source quote that supports the summary,
thank the reporter, and close the issue.

### UNDETERMINED
Comment on the issue: state what you searched for, quote the closest source
passage, and label the issue `needs-human` (`gh issue edit <number>
--add-label needs-human`). Do NOT change the rules file. If the user supplied
an authoritative external source (publisher FAQ, designer ruling), note that a
maintainer should verify it — external claims are never merged automatically.

## Hard rules

- The extracted text outranks the user, your training data, and BGG.
- Never edit a rules file based on an UNDETERMINED conclusion.
- Every PR must contain quote-pair evidence (summary vs source).
- One issue = one branch = one PR. Don't batch unrelated fixes.
