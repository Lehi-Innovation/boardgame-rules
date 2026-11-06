from qa_tools import *
final=sys.argv[1];bank=sys.argv[2];audit=sys.argv[3] if len(sys.argv)>3 else 'source-audit-05.json'
completed=(P/'completion-audit.json').exists() and json.loads((P/'completion-audit.json').read_text()).get('all_requirements_pass',False)
opening_status='QA and coordinator integration complete' if completed else 'Local QA PASS — ready for coordinator integration'
res=json.loads(effective_results(P/final).read_text());n=len(json.loads((P/bank/'questions.json').read_text())['questions']);assert all(v['totals']=={'correct':n,'partial':0,'incorrect':0} for v in res['readers'].values())
rows=[]
order=['seed-iteration-01','seed-iteration-02','seed-iteration-03','seed-iteration-04','expanded-iteration-01','seed-iteration-05']+[x.name for x in sorted(P.glob('expanded-iteration-*')) if x.name!='expanded-iteration-01']+[x.name for x in sorted(P.glob('integrated-iteration-*'))]
for name in order:
 d=P/name
 if not (d/'results.json').exists():continue
 report=effective_results(d).name;r=json.loads((d/report).read_text());count=len(json.loads((d/'questions.json').read_text())['questions'])
 score=lambda v:'/'.join(str(v[x]) for x in ['correct','partial','incorrect'])
 rows.append(f"| [{name}]({name}/{report}) | {count} | {score(r['readers']['a']['totals'])} | {score(r['readers']['b']['totals'])} |")
iterations=[]
for name in order:
 d=P/name
 if not (d/'reader-a.json').exists():continue
 report=effective_results(d).name
 iterations.append(f"- **{name}:** [snapshot]({name}/summary-snapshot.md), [questions]({name}/questions.json), [key]({name}/answer-key.json), [A]({name}/reader-a.json), [B]({name}/reader-b.json), [grades]({name}/{report}), [input hashes]({name}/input-manifest.json), [model provenance]({name}/model-provenance.json), [exact prompts]({name}/dispatch-prompts.json), [diff]({name}/summary-changes.patch).")
audit_history=', '.join(f'[{x.name}]({x.name})' for x in sorted(P.glob('source-audit-*.json')) if x.name!=audit and x.stem.removeprefix('source-audit-').isdigit())
audit_dispatch=audit.removesuffix('.json')+'-dispatch.json'
if not (P/audit_dispatch).exists():audit_dispatch='audit-dispatch-11-12.json'
adjudications=', '.join(f'[{x.name}]({x.name})' for x in sorted(P.glob('*adjudication.json')))
sha=h(P/final/'summary-snapshot.md');assert (P/final/'summary-snapshot.md').read_bytes()==(ROOT/'rules/scythe.md').read_bytes()
v4_used=(final.startswith('expanded-iteration-') and int(final.split('-')[-1])>=9) or final.startswith('integrated-iteration-')
prompt_change=('The final pair used the new generic self-check reminder, recorded as `generic-self-check-v4`.' if v4_used else 'The current pair was already dispatched when the new generic self-check reminder was requested; that reminder is reserved for the next fresh pair.')+' The [prompt-version record](prompt-version-change.json) preserves its exact text and timing. It asks readers to review each answer independently for completeness and contradictions, without supplying question-specific facts, keys or prior grading feedback. Old prompts and iterations remain preserved; omissions still count as failures.'
integration_note=('The coordinator recorded and stamped the pre-integration version, changing only verification metadata and the managed banner. The gameplay body is identical. This report covers a new full reader pair and fresh source audit on the exact stamped bytes, as requested in the [integration handoff](coordinator-integration-request.json). The [pre-integration report](README-pre-integration.md) and [stamp diff]('+final+'/stamp-changes.patch) preserve that boundary. Idempotent final recording/stamping and shared catalog integration remain coordinator-owned.' if final.startswith('integrated-iteration-') else '')
if completed:
 integration_note='The coordinator accepted all 126 stamped-version answers, the fresh exact-hash source audit, actual models and fresh contexts. Final audit recording, an idempotent second stamp, the Scythe-only registry update, and targeted index/manifest publication are complete. The gameplay body is unchanged from the pre-stamp pass. See the [completion audit](completion-audit.json), [coordinator validation](../../batches/2026-11-04-batch-231507/scythe-coordinator-validation.json), and [publication preservation checks](../../batches/2026-11-04-batch-231507/publication/20261105-042325/validation.json). The [pre-integration report](README-pre-integration.md) and [stamp diff]('+final+'/stamp-changes.patch) remain preserved.'
handoff_status=('Status is **complete**, with details in [game-status.json](game-status.json). All Scythe-specific requirements are satisfied; the exact tested/stamped canonical hash remains unchanged. The coordinator explicitly accepted final integration. This completes the assigned Scythe goal, not the wider batch.' if completed else 'Status is **ready-for-coordinator**, with details in [game-status.json](game-status.json). Coordinator-owned audit recording, targeted stamping, shared index/manifest regeneration and final catalog checks remain. The persistent goal stays active while awaiting the explicit Scythe integration follow-up. If stamped summary bytes change, the complete unchanged bank must be retested on those exact bytes and audit evidence updated before completion.')
catalog_note=('The recorded global read-only catalog check found **no Scythe errors** and three outside-scope discrepancies: Dune: Imperium catalog metadata and player count, and Battle of the Bulge BGG ID. The exact messages are retained in [coordinator validation](../../batches/2026-11-04-batch-231507/scythe-coordinator-validation.json). Unrelated entries were preserved; these are not claimed as global catalog PASS or Scythe failures.' if completed else '')
text=f'''# Scythe base/core multiplayer summary QA

**{opening_status}.** Two fresh `gpt-6-luna` readers at `high` effort each answered **{n}/{n}**, with zero partial or incorrect answers and no unsupported guesses substituting for summary coverage. The exact final text independently passed source audit. **{len(rows)} reader pairs were executed** across the preserved seed, expanded and stamped iterations. This is a fixed regression-bank pass; it is not batch completion or a held-out accuracy study.

Game: **Scythe**, BGG **169786**, slug `scythe`. Report date: **November 5, 2026 (America/Phoenix)**. Scope: the **2016 base/core multiplayer game**, using the recovered full 32-page English publisher-authored [PDF](../../../../../source_pdfs/scythe-recovery.pdf) and [extraction](../../../../../extracted/scythe-rules.txt). Automa, expansions, promo additions and explicit optional variants, including Delay of Game, are excluded. No edition substitution or new source download occurred.

The canonical [summary](../../../../../rules/scythe.md) and [final tested snapshot]({final}/summary-snapshot.md) are byte-identical. Final SHA-256: `{sha}`. [Original input hashes](input-manifest.json) and [source inspection](source-inspection.json) establish the unchanged recovered inputs and preserved baseline.

{integration_note}

## Bank and coverage

Use the readable [{n}-question answer bank]({bank}/question-bank.md), separate [questions]({bank}/questions.json), [key]({bank}/answer-key.json), and [benchmark hashes]({bank}/benchmark-manifest.json). All original 20 seed entries retain identical IDs, wording and expected answers; every expanded version preserves all preceding entries. No source/key correction was needed.

| Version | Questions | Meaningful additions |
|---|---:|---|
| [seed-v1](question-bank.md) | 20 | Predetermined source-backed seed |
| [expanded-v2](expanded-v2/question-bank.md) | 43 | Q21–43, source-wide procedural mapping |
| [expanded-v3](expanded-v3/question-bank.md) | 45 | Q44–45, seating and water geometry |
| [expanded-v4](expanded-v4/question-bank.md) | 46 | Q46, public encounter presentation |
| [expanded-v5](expanded-v5/question-bank.md) | 57 | Q47–57, direct elicitation of limits, lifecycle, timing, choices and mandatory stars |
| [expanded-v6](expanded-v6/question-bank.md) | 59 | Q58–59, default water restriction and recruit immobility |
| [expanded-v7](expanded-v7/question-bank.md) | 60 | Q60, character-only encounter eligibility |
| [expanded-v8](expanded-v8/question-bank.md) | 62 | Q61–62, positive Mill effects and loss of resource-only control |
| [expanded-v9](expanded-v9/question-bank.md) | 63 | Q63, Build/Enlist payment-resource identities |

The [coverage and rejection ledger](coverage-ledger.json) records accepted additions, targeted passes and rejected duplicates/padding. The [effective passage map](source-coverage-map-final.json) maps the final questions to procedural passages; the [original reviewed map](source-coverage-map.json) remains preserved. Coverage requires that a rule be elicited by the question, rather than merely supplied as an unasked key extra.

The final targeted passes **23 and 24 added zero questions** after the latest accepted addition. A fresh source/coverage reviewer then challenged all 63 questions and keys against the complete source, checked the required diagrams, and returned **[PASS with no qualifying additions](coverage-review-08.json)**. Its nonblocking map-precision comment is resolved in [coverage-resolution.json](coverage-resolution.json). This is working saturation under the stated meaningful-rule/branch/timing criteria, not enumeration of every possible scenario.

Earlier independent challenges are preserved: [01](coverage-review-01.json), [02](coverage-review-02.json), [03](coverage-review-03.json), [03 supplement](coverage-review-03-supplement.json), [04](coverage-review-04.json), [05](coverage-review-05.json), [06](coverage-review-06.json), [07](coverage-review-07.json). They prompted real additions instead of lowering the novelty standard or removing questions.

## Reader iterations and grading

Scores below are **correct / partial / incorrect** per complete answer. They are not percentages of the game's rules accurate.

| Iteration | N | Reader A | Reader B |
|---|---:|---:|---:|
{chr(10).join(rows)}

The evaluator compared every requested part against the fixed source-backed key, independently per answer. A missing fact cannot be borrowed from another answer. Confidence/support labels do not decide grades. A correctly resolved answer can retain an appropriate caveat about an unrequested, unspecified value; a contradictory rule remains a finding.

**Historical grading correction:** Q10 asks costs. Its original key includes determining the required amount from the exposed, mat-dependent cost. Early resource-only answers were mistakenly accepted without that amount rule. [grading-correction.json](grading-correction.json) records the correction consistently across affected seed iterations. Original `results.json` files remain unchanged; supplemental `results-adjudicated-v2.json` files supersede those scores. Questions, keys, reader outputs and input hashes did not change. The new seed-05 pair then scored 20/20 each under the corrected standard before full-bank testing resumed.

**Q01 grading correction:** The coordinator challenged whether face-down Factory selection alone resolved the requested setup. A [fresh independent adjudicator](expanded08-q01-adjudication.json) ruled that randomization is material; random selection or shuffling suffices, but neither is implied solely by face-down cards. [q01-grading-correction.json](q01-grading-correction.json) applies that standard consistently to earlier affected answers using supplemental `results-adjudicated-v3.json` reports. All original grades, raw answers, prompts and fixed benchmarks remain preserved. The score table uses the latest authoritative assessment per iteration.

Independent adjudications are preserved: {adjudications}. They distinguish requested omissions from extra key facts. For example, full-bank reader B's overlap answer resolves the requested permission despite a partial label; the unspecified structure-tile amount is not required by Q20. Conversely, missing shore-entry eligibility, mandatory encounter choice, actual-worker Mill output, river continuity, combat-card concealment or a requested cost amount remains a partial answer. Factory-as-one scoring and an unconditional three-territory Mill cap are incorrect rulings despite partial/support labels.

The coordinator's remaining narrow review cases are resolved in [expanded08-scope-supplement.json](expanded08-scope-supplement.json): Q42 asks the normal carried-worker lake-combat rule rather than an inventory of faction exceptions, and Q36B's operative stop/after-combats procedure resolves both requested outcomes despite a stray opening affirmative. Neither ruling borrows another answer. After Q01's material omission, iteration 09 repeats the complete fixed bank on the same independently audited summary bytes with the generic self-check reminder.

The repairs use general source-supported rules: complete setup and control, transport and payment sequence, every faction ability, combat and retreats, encounter/Factory/objective timing, sixth-star interruptions, all scoring tiers and six structure tiles. Later clarity repairs explicitly state shoreline entry, mandatory encounter selection, additive Mill output, exposed Upgrade/Deploy quantities, straight-row river continuity, Factory scoring counts, upgraded Mill totals and combat-card concealment. The information rule is grouped with public hand count to prevent the timing exception being omitted. The final revisions clarify control-independent structure bonuses, Rusviet's prior-turn exception, ordinary/Saxony combat-star awards, worker entry into enemy-worker territory, and the distinction between Nordic Swim and its separate unlockable Riverwalk. The summary contains ordinary rules and reference tables, not an appended answer key.

## Independent source audit and provenance

The final exact text received **[{audit} PASS]({audit})**, with no unresolved findings. This final auditor used a new `fork_turns="none"` context, was separate from the repairer, coverage reviewers and readers, and received only the exact frozen summary and authoritative source, including necessary PDF diagrams. No earlier summaries, reports or repair notes were supplied. The review is tied to the exact final hash; [final audit dispatch]({audit_dispatch}) preserves its source-only instructions. Earlier independent source reviews, including continuing reviews, remain supporting history: {audit_history}.

All readers were fresh contexts with `fork_turns="none"`, `gpt-6-luna`, `high`; all source/coverage/adjudication reviewers used `gpt-6.1-sol`, `high`. **Actual model and effort are confirmed from session metadata**, not inferred from directory names. [Runtime provenance](runtime-provenance.json) records session IDs and turn contexts. [Provenance notes](provenance-notes.json) explain exact dispatch-text records and the separation from encrypted runtime task text. The [final isolation review](final-isolation-review.json) records model metadata and inspection of the final readers' and fresh auditor's actual read calls. Each iteration preserves the exact reader prompts and original raw responses. Isolation was by fresh context and explicit allowed-file instructions; stronger filesystem isolation is not claimed.

{prompt_change}

## Validation and coordinator handoff

[Validation](validation.json) checks source integrity, original benchmark preservation, every historical snapshot/question/key hash, every expected reader/grade ID exactly once per assessment version, exact linkage of grades to question/key/raw answer, all actual model settings, final scores, source audit/coverage status, document links and final canonical/snapshot byte equality. It also records targeted `scripts.validate rules/scythe.md` and scoped `git diff --check` results. Grade correction versions are checked and retained separately.

This game-specific chat changed only `rules/scythe.md` and its unique evidence directory. It did not edit shared instructions/scripts, other games, registries, index or manifest, and did not commit, push, switch branches or reset. Coordinator-owned integration is separate. Pre-existing source recovery metadata/link changes were preserved.

{handoff_status}

{catalog_note}

## Evidence by iteration

{chr(10).join(iterations)}
'''
(P/'README.md').write_text(text)
print('Report written for',final,n,sha)
