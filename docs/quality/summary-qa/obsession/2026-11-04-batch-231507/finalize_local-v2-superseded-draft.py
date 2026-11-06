from qa_tools import *
from validate_evidence import run
import subprocess,re

def main():
 v=run();assert not v['errors'],v['errors']
 I=P/'expanded-iteration-07';f=ROOT/'rules/obsession.md';q=P/'expanded-v2/questions.json';k=P/'expanded-v2/answer-key.json';A=P/'final-source-audit-07/source-audit.json';r=json.loads((I/'results.json').read_text());a=json.loads(A.read_text())
 assert f.read_bytes()==(I/'summary-snapshot.md').read_bytes()==(P/'final-source-audit-07/summary-snapshot.md').read_bytes()
 assert a['verdict']=='PASS' and not a.get('findings',[])
 for w in ['a','b']:
  assert all(r['readers'][w][x]==n for x,n in [('correct',60),('partial',0),('incorrect',0),('unsupported_guesses',0)])
 assert json.loads((P/'coverage-challenge-02.json').read_text())['verdict']=='PASS_NO_DISTINCT_ADDITIONS_FOUND'
 ledger=json.loads((P/'coverage-ledger.json').read_text());assert [x['new_count'] for x in ledger['passes'][-2:]]==[0,0]
 checks=[]
 for cmd in [[str(ROOT/'.venv/bin/python'),'-m','scripts.validate','rules/obsession.md'],['git','diff','--check','--','rules/obsession.md',str(P.relative_to(ROOT))]]:
  cp=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True);checks.append({'command':cmd,'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr});assert cp.returncode==0
 dump(P/'repository-checks.json',{'targeted_checks':checks,'coordinator_owned_pending':['semantic audit recording','targeted verification stamping','index and manifest regeneration','final catalog/repository checks and explicit integration follow-up'],'no_shared_registry_or_generated_file_edits_by_this_game_chat':True})
 total_answers=total_grades=0;iterations=[]
 names=[f'seed-iteration-{i:02}' for i in range(1,4)]+[f'expanded-iteration-{i:02}' for i in range(1,8)]
 for name in names:
  it=P/name;rr=json.loads((it/'results.json').read_text());n=len(json.loads((it/'questions.json').read_text())['questions']);entry={'path':name,'bank':rr['benchmark_version'],'question_count':n,'summary_sha256':sha(it/'summary-snapshot.md'),'results_path':str(it/'results.json')}
  for w in ['a','b']:
   raw=json.loads((it/f'reader-{w}.json').read_text());total_answers+=len(raw['answers']);total_grades+=len(rr['readers'][w]['grades']);entry[f'reader_{w}']={x:rr['readers'][w][x] for x in ['correct','partial','incorrect','unsupported_guesses']}
  iterations.append(entry)
 assert total_answers==total_grades==960
 # Verify explicit actual runtime provenance for every one of the20 fresh readers.
 prov=provenance();reader_tasks={f'/root/obs_seed_{i:02}_{w}' for i in range(1,4) for w in ['a','b']}|{f'/root/obs_expanded_{i:02}_{w}' for i in range(1,8) for w in ['a','b']}
 actual={x['task']:x for x in prov};assert reader_tasks<=actual.keys()
 for task in reader_tasks:
  assert actual[task]['contexts'] and all(c['model']=='gpt-6-luna' and c['effort']=='high' for c in actual[task]['contexts'])
 for x in prov:
  if x['task'] not in reader_tasks:assert x['contexts'] and all(c['model']=='gpt-6.1-sol' and c['effort']=='high' for c in x['contexts'])
 manifest={'benchmark_version':'expanded-v2','question_count':60,'reader_snapshot':str(I/'summary-snapshot.md'),'canonical_summary':str(f),'source_audit':str(A),'inputs':[{'path':str(x),'sha256':sha(x)} for x in [f,I/'summary-snapshot.md',q,k,ROOT/'extracted/obsession-rules.txt',ROOT/'source_pdfs/obsession-universal-rules.pdf',ROOT/'source_pdfs/obsession-corrigendum-1.0.pdf',P/'publisher-fr-base-rules.pdf',P/'publisher-fr-base-rules.txt',A,P/'coverage-challenge-02.json',I/'reader-a.json',I/'reader-b.json',I/'results.json',P/'grading-audit-07.json']]};dump(P/'final-input-manifest.json',manifest)
 proof={'local_result':'PASS','coordinator_integration':'pending explicit follow-up; goal remains active','question_count':60,'benchmark_version':'expanded-v2','all_procedural_passage_groups_mapped':len(ledger['coverage']),'two_final_zero_addition_passes':[x['pass'] for x in ledger['passes'][-2:]],'independent_coverage_verdict':'PASS','final_source_audit':'PASS','final_audit_snapshot_matches_reader_and_canonical':True,'canonical_summary_sha256':sha(f),'every_benchmark_input_hash_matches':True,'original_seed_questions_preserved':True,'original_seed_keys_preserved_except_explicit_Q09_version_correction':True,'expanded_original56_question_wording_preserved':v['expanded_question_prefix_preserved'],'all_reader_ids_and_grade_ids_exactly_once':True,'every_grade_matches_original_question_fixed_key_and_raw_answer':True,'saved_reader_answer_count':total_answers,'saved_grade_count':total_grades,'fresh_blind_reader_count':len(reader_tasks),'all_actual_reader_models_and_efforts_confirmed':True,'actual_reviewer_models_and_efforts_confirmed':True,'readers':{w:{x:r['readers'][w][x] for x in ['correct','partial','incorrect','unsupported_guesses']} for w in ['a','b']},'targeted_repository_checks':'PASS','errors':[]};dump(P/'final-validation.json',proof)
 scores='\n'.join('| '+e['path']+' | '+e['bank']+' | '+str(e['question_count'])+' | '+' / '.join(str(e['reader_a'][x]) for x in ['correct','partial','incorrect'])+' | '+' / '.join(str(e['reader_b'][x]) for x in ['correct','partial','incorrect'])+' |' for e in iterations)
 perlinks='\n'.join(f'- {e["path"]}: [summary]({e["path"]}/summary-snapshot.md), [questions]({e["path"]}/questions.json), [reader A]({e["path"]}/reader-a.json), [reader B]({e["path"]}/reader-b.json), [detailed grades]({e["path"]}/results.json), [input hashes]({e["path"]}/input-manifest.json).' for e in iterations)
 report=f'''# Obsession summary QA — 2026-11-04 batch 231507

**Local PASS: both final readers answered all 60 questions correctly, with zero partial, incorrect or unsupported answers. Status: ready for coordinator.** Work performed November 5, 2026 (America/Phoenix). The persistent goal remains active until explicit integration follow-up and final repository checks for this game.

Read the [complete 60-question bank and source-backed answers](expanded-v2/question-bank.md), [final tested summary](expanded-iteration-07/summary-snapshot.md), [final grades](expanded-iteration-07/results.json) and [validation proof](final-validation.json).

## Source and scope

Dan Hallagan / Kayenta **Obsession, BGG 231733**, second-edition **base/core 2–4-player standard 16-round multiplayer**, using the publisher Universal Rules Compendium (2025-12-17) plus Corrigendum 1.0 (2026-10-06), and the base objective deck. The canonical frontmatter now uses the correct BGG ID, source_pdf `obsession-universal-rules.pdf`, extracted_date `2026-11-04`, and an explicit rulebook/scope description.

The earlier third-party condensed 2.2E reference has been replaced explicitly. Its [coordinator-retained original](../../batches/2026-11-04-batch-231507/source-discovery/obsession-original-condensed-rules.txt) and original summary remain preserved; see [historical fingerprints](historical-source-preservation.json). This chat preserved its own [initial summary](baseline/obsession.md), full upgraded source/PDF copies and [pre-work hashes](input-manifest.json). The assigned live authoritative sources remain byte-identical to those initial fingerprints.

The only supplemental source is the [official French publisher base rulebook](publisher-fr-base-rules.pdf), used **only** for the unchanged reputation objective: PDF p.14 explicitly uses maximum reputation *level*, identified by the Max counter, and p.7 maps Max to standard level 7. Its component counts and identical objective artwork establish narrow compatibility. See [download provenance](supplemental-source-provenance.json), [original ambiguity finding](source-review-01/source-audit.json) and [independent resolution](source-review-01/supplemental-resolution.json). No older general flow rules were imported.

Excluded: all marked Upstairs, Downstairs, Characters, Wessex, promotional/backer components and mechanics; supplemental/second-chance servants; replacement objective decks; expanded drafts; extended game; 5–6 players; solo/AI/estate challenge; tableau/teams/co-op; friendly mode; low-VP monuments; milestones; distinguished family; alternate Charles; Costume Ball; starting hall boy; intensive service; closed courtship; Queen Victoria/Charles Dickens variants; other optional variants, including hiring when passing. The **new default full seasonal Market refresh is included**, as required by the compendium and corrigendum. The [coverage ledger](coverage-ledger.json) records exclusions by source passage.

## Bank growth and stopping check

The source was read before building the initial fixed 20-question bank. The evaluator had seen the original summary before source-first question design; this is documented, not a held-out study.

The bank grew from 20 to 56 through distinct setup, procedure, timing, resource, guest, tile, objective and scoring branches. Two targeted passes added none. A [fresh independent coverage reviewer](coverage-challenge-01.json), who saw source/bank/key but no summary or reader outputs, then found four real gaps: unlimited hand/discard size; public/select-any Reserve; voluntary versus mandatory passing; and separate Market refresh methods. These became Q57–Q60. Two renewed targeted passes added none, followed by a [second fresh independent coverage challenge](coverage-challenge-02.json): **PASS, no further distinct additions or material key corrections**.

The [coverage/rejection ledger](coverage-ledger.json) maps {len(ledger['coverage'])} procedural passage/reference groups and records accepted novelty, rejected cosmetic/number substitutions, excluded modes and unsupported extreme exhaustion candidates. This establishes working saturation within the supplied base source and novelty criterion, not enumeration of every conceivable game situation. Ordinary component-number swaps and mechanical recombinations without a distinct exception were not counted as new questions.

All original Q01–Q20 wording remains identical. Q09’s original key specified immediate Expended placement but omitted the explicitly asked service-availability timing. A [fresh adjudicator](adjudication-01/report.json) retained both reader omissions as partial and identified the key defect. [seed-v2](seed-v2/question-bank.md) explicitly adds normal second-rotation availability and earlier refresh mechanisms. Historical seed-v1 and expanded-v1 remain intact. The expanded-v2 bank inherits that documented correction; Q21–Q56 question wording remains unchanged, and their compressed draft answers were rendered into readable prose without changing targets. See [version corrections](benchmark-corrections.json). The entire expanded-v2 question/key files remained unchanged throughout all seven expanded reader iterations.

## Reader results

All readers were fresh **gpt-6-luna / high**, forked with no parent history. Each saw only its frozen summary and question copy, with instructions excluding source, key, previous answers, grades, browsing, prior game knowledge and communication with other readers. The full intended reader prompts are retained as `reader-*-prompt.txt`. Parent spawn settings establish requested `fork_turns=none`, model and effort; child runtime turn contexts establish actual model/effort. **Runtime NEW_TASK/spawn message payloads are encrypted and were not decrypted or recovered.** Visible user-role runtime messages contain environment context only. Legacy `reader-*-dispatched-prompt.json` files are env-only captures, not full task prompts; the accurately named `reader-*-runtime-environment-user-messages.json` files and [inspection-limit disclosure](provenance-interpretation.json) make this distinction explicit. [Runtime metadata and turn contexts](model-provenance.json) confirm every requested reader model/effort and each **gpt-6.1-sol / high** source, coverage, grading and adjudication reviewer. Isolation was prompt/context based; no stronger filesystem barrier is claimed.

Scores below are **correct / partial / incorrect**, graded by requested material rulings, not support labels. Each answer is judged independently; missing facts are not borrowed from another answer.

| Iteration | Bank | N | Reader A C / P / I | Reader B C / P / I |
|---|---|---:|---|---|
{scores}

Iteration 1’s reader B also has one correct ruling with an unsupported gender assumption, separately flagged. Iteration 4 B and iteration 5 A have unsupported-guess flags associated with their wrong rulings. The final pair has **none**.

Repairs add general source rules and clearer organization: complete setup; fixed reputation screening; servant origins/destinations/substitutions; mandatory favours and payments; Market refill/reserve/refresh and fixed multi-buy prices; courtship/final scoring; family-by-gender eligibility; underbutler uniqueness/availability; Fairchild genders/dismissal and admirer interaction; named objective sets; VP-card timing; recovered gentry’s immediate use; last-player marker advancement; event order; and monuments retaining their category for both objective types.

Expanded iteration 6 tested exactly the iteration-5 text without a repair because the latest clear failure was a self-contradictory Charles ruling despite explicit summary coverage; its valid [source-audit reuse](expanded-iteration-06/source-audit-reuse.json) records identical bytes. Both iteration-6 readers then omitted the suites’ category-objective eligibility, and one again contradicted itself about Charles. The final wording makes those general interactions explicit.

### Grading safeguards and corrections

The [full independent grading audits 3](grading-audit-03.json), [4](grading-audit-04.json), [5](grading-audit-05.json), [6](grading-audit-06.json), and [7](grading-audit-07.json) preserve all raw answers, reasons, source evidence and requested-fact boundaries. They distinguish genuinely requested procedure, timing, quantities, destinations and comparisons from incidental explanation in the key.

[Adjudication 2](adjudication-02/report.json) accepted iteration-2 B’s Q32/Q50 despite partial support labels because its actual answers resolve the requested rulings. A later grading audit caught missing marker advancement in iteration-2 B Q02; its corrected score is 59/60 with one partial, not the provisional 60. [Grading corrections](grading-corrections.json) preserve original grade JSON and hashes beside the corrected records. The [cross-case Q44 adjudication](adjudication-03/report.json) consistently retains missing ordinary-rotation movement as partial across iterations 1, 3 and 4; iteration-4 A’s parent result uses this stricter adjudication although grading audit 4 alone accepted that answer. No raw response or fixed key was changed to improve a score.

Final reader A Q05 uses awkward money-penalty wording while stating the mandatory positive-before-negative rule and the complete payment ruling. The fresh final grader records it as nonmaterial wording: it does not retract an asked ruling, assert a wrong permission or leave a requested fact unresolved. All **120 final answers** are independently confirmed complete/correct with no unsupported guesses.

## Independent source audit and validation

The [fresh final source audit](final-source-audit-07/source-audit.json) returned **PASS, no findings**, checking the full relevant core/FAQ/base references and authorized localized objective clarification. Its author had not written repairs and saw no questions, keys, reader responses, grades or earlier reviews. Its [audited snapshot](final-source-audit-07/summary-snapshot.md), final reader snapshot and canonical summary are byte-for-byte identical.

Final summary SHA-256: `{sha(f)}`.

The [final proof](final-validation.json), [all iteration checks](validation.json), [final input manifest](final-input-manifest.json) and [targeted repository checks](repository-checks.json) confirm:

- All **960 saved reader answers and 960 grade records** contain their expected IDs exactly once; every grade matches its original question, fixed key and raw answer.
- Original benchmark entries, all frozen input hashes and assigned authoritative source fingerprints remain intact; only the explicit Q09 key version correction differs.
- All 20 fresh blind-reader runtime models/efforts and all reviewer settings are confirmed.
- Both final readers are 60 correct / 0 partial / 0 incorrect / 0 unsupported guesses.
- Final source audit and independent coverage challenge pass, two final targeted passes add zero, and exact canonical/snapshot/audited-byte equality holds.
- Targeted `scripts.validate rules/obsession.md` and path-scoped `git diff --check` pass. Report links are checked below during finalization.

The coordinator owns semantic audit recording, verification stamping, index/manifest regeneration and final catalog/repository checks. These remain pending explicit integration follow-up for this game. If stamping changes any summary bytes, the exact new text must be frozen and the full 60-question bank retested; this chat’s persistent goal remains active. This report claims local fixed-regression-set passage, not batch completion, held-out accuracy or general model equivalence.

## Complete iteration evidence

{perlinks}

Additional evidence: [source-reading/PDF inspection log](source-reading-log.json), [line-numbered source](source-numbered.txt), [initial independent source review](source-review-01/source-audit.json), [source audits 1](final-source-audit-01/source-audit.json), [2](final-source-audit-02/source-audit.json), [3](final-source-audit-03/source-audit.json), [4](final-source-audit-04/source-audit.json), [5](final-source-audit-05/source-audit.json), [7](final-source-audit-07/source-audit.json), [machine-readable progress](game-status.json). Each iteration retains summary diffs, frozen inputs, raw outputs, detailed grades, full intended prompt files, env-only runtime captures and per-reader runtime provenance with the stated payload-inspection limit.
'''
 (P/'README.md').write_text(report)
 # Local relative report/bank links, excluding the deliberate publisher web URL.
 broken=[]
 for doc in [P/'README.md',P/'expanded-v2/question-bank.md',P/'seed-v1/question-bank.md',P/'seed-v2/question-bank.md']:
  for dest in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',doc.read_text()):
   if '://' in dest or dest.startswith('#'):continue
   if not (doc.parent/dest.split('#')[0]).exists():broken.append({'document':str(doc),'target':dest})
 assert not broken,broken
 proof['report_links_resolve']=True;proof['report_sha256']=sha(P/'README.md');dump(P/'final-validation.json',proof)
 status={'game':'Obsession','slug':'obsession','bgg_id':231733,'phase':'local-qa-passed-awaiting-coordinator-integration','status':'ready-for-coordinator','question_count':60,'question_bank_version':'expanded-v2','iterations':iterations,'final_reader_scores':proof['readers'],'source_audit':{'verdict':'PASS','path':str(A),'snapshot_path':str(P/'final-source-audit-07/summary-snapshot.md'),'summary_sha256':sha(f)},'coverage_review':{'verdict':'PASS','path':str(P/'coverage-challenge-02.json'),'zero_addition_passes':[6,7]},'report_path':str(P/'README.md'),'blocking_reason':None,'integration_required':'Wait for explicit game-specific coordinator audit-recording/stamping/repository-check follow-up; retest complete bank if exact bytes change; goal intentionally remains active.','final_snapshot_path':str(I/'summary-snapshot.md'),'source_paths':[str(ROOT/'extracted/obsession-rules.txt'),str(ROOT/'source_pdfs/obsession-universal-rules.pdf'),str(ROOT/'source_pdfs/obsession-corrigendum-1.0.pdf'),str(P/'publisher-fr-base-rules.pdf'),str(P/'publisher-fr-base-rules.txt')],'hashes':{'canonical_summary':sha(f),'final_snapshot':sha(I/'summary-snapshot.md'),'source':sha(ROOT/'extracted/obsession-rules.txt'),'questions':sha(q),'answer_key':sha(k),'source_pdf':sha(ROOT/'source_pdfs/obsession-universal-rules.pdf'),'corrigendum':sha(ROOT/'source_pdfs/obsession-corrigendum-1.0.pdf'),'supplemental_pdf':sha(P/'publisher-fr-base-rules.pdf'),'report':sha(P/'README.md')},'validation_path':str(P/'final-validation.json'),'actual_models_verified':True,'persistent_goal_status':'active'};dump(P/'game-status.json',status)
 print(json.dumps({'status':status['status'],'scores':proof['readers'],'summary_sha256':sha(f),'total_answers':total_answers,'total_grades':total_grades,'errors':proof['errors'],'report':status['report_path']}))
if __name__=='__main__':main()
