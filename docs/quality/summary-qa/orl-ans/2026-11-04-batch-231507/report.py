from pathlib import Path
import json,hashlib,sys
P=Path(__file__).parent;final=sys.argv[1] if len(sys.argv)>1 else 'stamped-iteration-03';H=hashlib.sha256((P/final/'summary-snapshot.md').read_bytes()).hexdigest()
its=['seed-iteration-01','seed-iteration-02','seed-iteration-03','expanded-iteration-02','expanded-iteration-03','expanded-iteration-04','expanded-iteration-05','stamped-iteration-01','stamped-iteration-02','stamped-iteration-03']
rows=[];evidence=[];answers=0
for it in its:
 d=P/it
 if not (d/'results.json').exists():continue
 r=json.loads((d/'results.json').read_text());n=len(json.loads((d/'questions.json').read_text())['questions']);answers+=2*n
 score=lambda who:' / '.join(str(r['readers'][who]['counts'][k]) for k in ['correct','partial','incorrect'])
 rows.append(f'| [{it}]({it}/results.json) | {n} | {score("a")} | {score("b")} |')
 links=[f'[summary]({it}/summary-snapshot.md)',f'[questions]({it}/questions.json)',f'[hashes]({it}/input-manifest.json)',f'[reader A]({it}/reader-a.json)',f'[reader B]({it}/reader-b.json)',f'[grades]({it}/results.json)',f'[actual models]({it}/model-provenance.json)',f'[validation]({it}/validation.json)']
 for path,label in [('source-audit.json','source audit'),('summary-changes.patch','baseline diff'),('repair-from-previous.patch','repair diff'),('adjudication.json','adjudication'),('reader-prompt-record.json','exact prompts')]:
  if (d/path).exists():links.append(f'[{label}]({it}/{path})')
 evidence.append(f'- **{it}:** '+', '.join(links)+'.')
body=f'''# Orléans summary QA — November 4–5, 2026

**Assigned Orléans QA complete: PASS on bank-v6, 60 questions.** Two fresh, runtime-confirmed **gpt-6-luna/high** readers each scored **60 correct, 0 partial, 0 incorrect** on the exact final summary. A fresh independent **gpt-6.1-sol/high** source audit returned **PASS**, with no findings or essential source gaps. Coordinator integration is verified, including the recorded exact-byte audit, idempotent stamping, registry promotion, index and manifest. This completes the assigned-game goal; it does not claim batch or repository completion.

Final tested summary SHA-256: `{H}`. The [final snapshot]({final}/summary-snapshot.md) is byte-identical to [the canonical summary](../../../../../rules/orl-ans.md). See [machine-readable status](game-status.json), [validation](validation.json), and [immutable evidence fingerprints](evidence-hashes.json).

## Edition and recovered sources

Scope is the **2014 dlp base game for 2–4 players**, English printed pp.12–21, all **20 base Place Tiles** pp.22–23, and components p.24. Optional pregame Place exclusion and every expansion scenario/mode are excluded. Bathhouse follows this booklet's original draw-three, choose-two rule.

The frontmatter PDF was absent locally. The matching publisher [Orleans_EN.pdf](https://www.dlp-games.de/tpl/download/Orleans_EN.pdf) was recovered as [matching-rulebook.pdf](matching-rulebook.pdf). It has fourteen PDF pages: contents/cover then printed pp.12–24. Its complete prose is identical to the authoritative extraction after ignoring whitespace and standalone numerical illustration labels. Its 2014 copyright and four-player component inventory corroborate the edition. Printed action costs absent from prose were inspected on the player-board diagram and every Place illustration, then independently checked by reviewers.

Evidence: [original input fingerprints](input-manifest.json), [original summary](original-summary.md), [frozen authoritative text](authoritative-source.txt), [source provenance](source-provenance.json), [recovered PDF extraction](recovered-extraction.txt), [extraction comparison](source-extraction-comparison.patch), and [enlarged board-cost diagram](player-board-costs-p12.png).

A Town Hall partial-transfer ambiguity led to a narrow supplemental source: the publisher-authored [2015 booklet](base-clarification-invasion-2015.pdf), p.3, explicitly cites base Town Hall as the precedent for resolving placed Followers in the same or separate actions. [Independent source adjudication](town-hall-source-adjudication.json) supports separate same-round action turns before passing. Only that base-game clarification appears in the labeled FAQ; no scenario procedures are adopted. See [supplement provenance](base-clarification-provenance.json), [extraction](base-clarification-invasion-extraction.txt), [page image](base-clarification-invasion-p3.png), and [source-gap resolution](source-gap-resolution.json).

**Evidentiary limit:** the cited texts do not expressly resolve cross-round retention after partial Town Hall use. That scenario is not assigned an invented answer. An explicit matching publisher/designer statement about partial-use round-end cleanup would resolve it if requested. Other speculative unruled cases are recorded in the rejection ledger. This does not remove any expressly stated in-scope procedure from coverage.

One intermediate source audit flagged only that “90 minutes” was absent from the allowed rulebook pages. The official publisher listing corroborates it; [metadata evidence](publisher-duration-metadata.json) resolves that finding. It is used solely for duration, while player count and all mechanics remain based on the 2014 booklet. Final audit has no remaining findings.

## Frozen bank and coverage stopping check

Read the complete [60-question and answer bank](bank-v6/question-bank.md), or use the separate [questions](bank-v6/questions.json), [key](bank-v6/answer-key.json), and [pre-dispatch hashes](bank-v6/benchmark-hashes.json). All earlier entries and their benchmark hashes remain intact. No original prompt or expected answer was removed, relaxed or silently corrected.

| Version | Questions | Additions |
|---|---:|---|
| [v1](bank-v1/question-bank.md) | 20 | Source-backed seed, fixed before initial readers |
| [v2](bank-v2/question-bank.md) | 50 | Setup, printed costs, remaining procedures/events, all 20 Places |
| [v3](bank-v3/question-bank.md) | 55 | Unique final Citizen, Hour Glass preparation/reveal, coin VP, initial values, Development recovery |
| [v4](bank-v4/question-bank.md) | 57 | Own action-order freedom, immediate acquired passive abilities |
| [v5](bank-v5/question-bank.md) | 58 | Selective one-of-two Town Hall transfer |
| [v6](bank-v6/question-bank.md) | 60 | Optional Ship/Wagon pickup, Town Hall separate turns |

The [final coverage/rejection ledger](coverage-ledger-v6.json) preserves all fifteen targeted passes and every accepted addition. Latest passes **14 and 15 added zero** after all procedural source passages were mapped. A fifth fresh independent [source/coverage challenge](coverage-complete-review.json) returned **PASS**, proposing no new question, finding no material key error and no wholly redundant addition. It saw sources and the bank, never summaries or reader responses.

Prior zero-addition claims were actively falsified and repaired; the history remains: [50-question ledger](coverage-ledger.json) and [challenge](coverage-review.json), [55-question ledger](coverage-ledger-v3.json) and [challenge](coverage-review-final.json), [57-question ledger](coverage-ledger-v4.json) and [challenge](coverage-saturation-review.json), [58-question ledger](coverage-ledger-v5.json) and [challenge](coverage-last-review.json). Cosmetic numerical variants, rewording, mechanical recombinations, component trivia, excluded modes and unsupported edge cases were rejected with reasons. Sixty is the resulting bank size, not a quota or cap. This is working saturation for the stated source/novelty standard, not every conceivable scenario.

## Readers, grading and repairs

Every reader used a new context with `fork_turns="none"` and saw only its frozen summary and questions. Sources, keys, other responses, prior grades, audit findings, browsing, parent history and prior game knowledge were excluded. Isolation is by fresh context and explicit read restrictions; stronger filesystem isolation was not used. Runtime session/turn-context records confirm actual models/effort for every reader, source reviewer and adjudicator; see per-iteration evidence and [reviewer provenance](reviewer-model-provenance.json). Final exact dispatch instructions are recorded as [reader A prompt]({final}/reader-a-prompt.txt), [reader B prompt]({final}/reader-b-prompt.txt), and [prompt provenance]({final}/reader-prompt-record.json). These strings were saved before dispatch; model, effort and fresh-context settings are independently confirmed. The earlier pre-stamp final prompt transcription remains preserved in expanded-iteration-05. The [original100-entry fingerprint inventory](evidence-hashes.pre-prompt-record.json) is retained unchanged.

Scores are **correct / partial / incorrect**, requiring all requested material parts independently within each response, with no unresolved requested ruling or material contradiction. A correct support label does not excuse an omission; a partial support label does not make a complete ruling partial. All {answers} raw reader answers and their detailed grades are retained.

| Iteration | N | Reader A | Reader B |
|---|---:|---:|---:|
'''+ '\n'.join(rows)+f'''

[Expanded iteration 1](expanded-iteration-01/iteration-state.json) was a prepared 57-question snapshot superseded before any reader dispatch; it is preserved and is not counted as a reader run. Every executed expanded and stamped iteration tested the complete unchanged bank-v6, including Q01–Q20. Stamped iteration 2 adds a generic completeness reminder to the reader prompt. It gives no question-specific facts or earlier findings; summary and prompt changes mean score differences do not isolate a single cause. Its exact prompts were saved before dispatch.

The initial repair corrected wrong action costs/effects, Census ties/two-player treatment, action rotation/passing/retention, recruitment rewards, Technology constraints, travel/building, exact Deed rules/rewards/destinations, events, bankruptcy, finite stock, Development/scoring, and all base Places. Later source-supported clarifications made Castle's Citizen reward, permanent Deed destinations, randomized goods setup, first Technology's incompatibility with Laboratory, immediate passive acquisition, bag-only torture payments, and Ship/Waterway versus Wagon/Road explicit. All failed iterations remain available.

Borderline answers received fresh independent adjudication. [Seed adjudication](seed-iteration-02/adjudication.json) established strict reward/destination completeness. A later [adjudicator](expanded-iteration-02/adjudication.json) viewed Deed permanence as incidental; the evaluator retained the earlier stricter requirement, and final responses state permanence. The [versioned interpretation note](grading-material-facts-v2.json) corrects overinclusive incidental helper facts while preserving the [original pre-dispatch checklist](grading-material-facts.json) and every bank/key byte. Technology persistence in Q03, after-pass timing in Q06 and the physical stack's board-space location in Q52 are unrequested supporting context, rather than newly imposed answer requirements.

In the pre-stamp passing pair, reader A labels Q16 and Q26 partial, but fully resolves the requested rulings: food types/destination/fallback and Town Hall neutral/no-profession-restriction eligibility. Its caveats concern additional wording, not an unresolved requested answer. A fresh [adjudicator](expanded-iteration-05/adjudication.json) independently confirmed both **correct**. The evaluator did not borrow missing facts from other answers. This differs from retained prior failures: [bag-pool omission](expanded-iteration-03/adjudication.json), [route omission](expanded-iteration-04/adjudication.json), and first-Technology conditional non-answers.

## Evidence by executed iteration

'''+ '\n'.join(evidence)+f'''

The fresh final source auditor saw only the final snapshot and scoped sources, never the bank, keys, readers or grades. [Its PASS]({final}/source-audit.json) covers the exact final summary hash and all 30 printed action/Place entries. Historical audits are preserved; the intermediate metadata-only MINOR remains historical and its finding is resolved by the publisher corroboration in the final audit.

## Validation and completed coordinator integration

[Validation](validation.json) checks all expected IDs exactly once per reader/grade array; grade-to-raw/key/question alignment; all frozen input and original benchmark hashes; exact retained prefixes across six versions; original source integrity; actual model/effort provenance; final 60/60 pair with zero unsupported guesses replacing coverage; two final zero-addition passes and independent coverage PASS; exact source-audit input hashes; report links; and byte equality between final snapshot and canonical summary. Targeted `scripts.validate rules/orl-ans.md` and scoped `git diff --check` pass.

The game evaluator modified no shared registry, audit registry, index, manifest or global scripts, and performed no commit, push, branch switch, reset or discard. The coordinator recorded the pre-stamp independent result and stamped the canonical file. The first stamped pair exposed additional unresolved requested parts; general activation timing, optional goods pickup, Technology placement limits and Town Hall eligibility were clarified while preserving the stamped metadata. A later reader contradicted the correct Pilgrimage phase, so the Phase1 reveal and Phase5 application were distinguished explicitly; that incorrect historical answer is retained.

The coordinator then recorded the new exact-byte independent PASS and confirmed that stamping changed no tested bytes. Its [final validation](../../batches/2026-11-04-batch-231507/orl-ans-coordinator-validation.json), [mechanical iteration checks](../../batches/2026-11-04-batch-231507/orl-ans-stamped-coordinator-iteration-check.json), [independent evidence review](../../batches/2026-11-04-batch-231507/orl-ans-coordinator-stamped-review.json), [audit/stamp recording](../../batches/2026-11-04-batch-231507/recording/orl-ans-20261105-013301/validation.json) and [targeted publication](../../batches/2026-11-04-batch-231507/publication/20261105-013352/validation.json) are retained. Unrelated entries were preserved. The evaluator's [read-only integration verification](coordinator-final-validation.json) checks the current verified registry entry, exact recorded audit hash, regenerated Orléans manifest entry and index row, plus the final snapshot equality.

The coordinator's earlier catalog check had no findings. A later evaluator check during concurrent work observed six global findings: Oath missing from the catalog, aggregate manifest coverage differing from rules files, and manifest BGG-ID mismatches for Cobra, Dirtside II, Don't Drop the Soap and Game of the Generals. Their exact messages and observation time are saved in the integration verification. Orléans has no target catalog error and matches regeneration. These unrelated/global findings are not declared resolved, and no whole-repository completion is claimed.

This is a passing fixed regression set, not a held-out accuracy study or a claim of universal model equivalence.
'''
(P/'README.md').write_text(body)
print('report written',answers,'answers',H)
