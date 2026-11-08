"""Version final evidence after the sole historical Q22 neutral decision."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p): return {'path':str(p),'sha256':sha(p)}
def write(name,x):
    p=ROOT/name
    assert not p.exists(),p
    p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')

now=datetime.now(timezone.utc).isoformat()
canonical=ROOT.parents[4]/'rules/sidereal-confluence.md'
assert sha(canonical)=='eb091e5288b379afe914cb89f64d9590c6c9242f05e0843d34cd347311fe348f'
neutral_dir=ROOT/'historical-full5-q22-neutral-01'
runtime=next(r for r in read(ROOT/'runtime-provenance.json')['records'] if r['task']=='/root/full5_q22_neutral_scope_whole_entry')
assert runtime['request']['requested_fork_turns']=='none'
assert runtime['request']['requested_model']=='gpt-6.1-sol' and runtime['request']['requested_effort']=='high'
assert runtime['turn_context_records'] and all(r['actual_model']=='gpt-6.1-sol' and r['actual_effort']=='high' for r in runtime['turn_context_records'])
write('historical-full5-q22-neutral-01/runtime-model-fork-proof.json',runtime)
assert read(neutral_dir/'validation.json')['only_Q22_effective_decisions_changed'] is True
inventory=read(ROOT/'completed-output-grade-inventory-after-q22.json')
assert inventory['complete_outputs']==26 and inventory['complete_entry_records']==1820
ledger=[]
for prefix,count in [('seed',3),('full',9)]:
    for n in range(1,count+1):
        d=ROOT/f'{prefix}-iteration-{n:02}'
        authority=d/'results.json';x=read(authority)
        scores=x.get('reader_scores',x.get('historical_reader_scores'))
        primary=scores;effective=scores;note='Primary and effective scores agree.'
        primary_authority=authority;effective_authority=authority
        if prefix=='full' and n==1:
            primary_authority=d/'results-before-adjudication.json'
            primary=read(primary_authority)['reader_scores']
            note='One earlier authorized Q13 whole-entry adjudication: b Partial to Correct; primary pre-adjudication retained. Historical Q36 key was later genuinely source-corrected in v12; these remain their own historical-target scores.'
        if prefix=='full' and n==5:
            effective_authority=neutral_dir/'effective-results-v1.json'
            effective=read(effective_authority)['reader_scores']
            note='One fresh neutral Q22 operational-equivalence/scope decision: both Partial to Correct. b Q63 remains Incorrect. Primary raw/key/map/grades untouched; pair still fails.'
        if prefix=='seed' and n==2:
            note='Frozen seed-v2 primary historical scores; subsequent genuine scope correction created seed-v3, without retroactively changing this pair.'
        ledger.append({'pair':d.name,'primary_scores':primary,'effective_scores':effective,'primary_authority':bind(primary_authority),'effective_authority':bind(effective_authority),'effective_pair_pass':all(v['correct']==(20 if prefix=='seed' else 76 if n==1 else 86) for v in effective.values()),'note':note})
assert len(ledger)==12
extras=read(ROOT/'complete-attempt-accounting-01/validation.json')
write('scored-pair-history-after-q22.json',{'scored_pairs':12,'pair_output_sets':24,'additional_complete_attempts':2,'all_complete_output_sets':26,'all_complete_entry_records':1820,'scores_are_correct_partial_incorrect':True,'pairs':ledger,'two_extra_attempts_authority':bind(ROOT/'complete-attempt-accounting-01/results.json'),'two_extra_attempts_validation':bind(ROOT/'complete-attempt-accounting-01/validation.json'),'all_complete_output_inventory':bind(ROOT/'completed-output-grade-inventory-after-q22.json'),'no_cross_round_pair_mixing':True})
combined=read(ROOT/'validation-stamped-full9-with-output-accounting.json')
combined['status']='EXACT_STAMPED_QA_COMPLETE_OUTPUT_ACCOUNTING_AND_ONE_HISTORICAL_NEUTRAL_PASS_PENDING_COORDINATOR'
combined['checked_at_utc']=now
combined.pop('remaining_historical_review')
combined['historical_Q22_neutral']={'status':'ADOPTED_VERSIONED_SCOPE_EQUIVALENCE_CORRECTION','validation':bind(neutral_dir/'validation.json'),'runtime_model_fork_proof':bind(neutral_dir/'runtime-model-fork-proof.json'),'scope_correction':bind(neutral_dir/'scope-correction-v1.json'),'primary_scores':read(neutral_dir/'validation.json')['primary_scores'],'effective_scores':read(neutral_dir/'validation.json')['effective_scores'],'historical_pair_still_fails':True,'current_full09_frozen_bank_and_scores_unchanged':True}
combined['all_complete_outputs']['inventory_path']=str(ROOT/'completed-output-grade-inventory-after-q22.json')
combined['all_complete_outputs']['inventory_sha256']=sha(ROOT/'completed-output-grade-inventory-after-q22.json')
combined['scored_pair_history']=bind(ROOT/'scored-pair-history-after-q22.json')
combined['coordinator_final_acceptance']='PENDING final evidence check; coordinator independently accepted source09, full09 and historical two extra factual-accounting results'
write('validation-final-after-q22.json',combined)

requirements=read(ROOT/'acceptance-requirements-after-complete-attempt-accounting.json')
requirements.update({'status':combined['status'],'updated_at_utc':now,'canonical_sha256':sha(canonical),'selected_reader_tasks':{'a':'/root/full9_reader_a','b':'/root/full9_reader_b'},'pure_source_audit':'source-audit-09 PASS exact stamped canonical bytes','final_gate':'validation-final-after-q22.json','coordinator_stamp_verification':'APPLIED by coordinator; NEW exact-byte full09/pure09 QA PASS','all_completed_output_count':26,'all_completed_entry_record_count':1820,'completed_output_accounting':'completed-output-grade-inventory-after-q22.json','selected_full8_pair_replaced_or_regraded':False,'consolidated_validation':'validation-final-after-q22.json','coordinator_status':'Final acceptance and explicit completion authorization pending','scored_pair_history':'scored-pair-history-after-q22.json','historical_Q22_effective_adjudication':'historical-full5-q22-neutral-01/validation.json','no_frozen_benchmark_or_primary_grade_mutation':True})
write('acceptance-requirements-final-after-q22.json',requirements)

progress=read(ROOT/'progress.json')
progress.update({'status':'all_worker_evidence_pass_pending_coordinator_final_acceptance_and_completion_authorization','phase':'coordinator_final_evidence_inspection','current_consolidated_validation':'validation-final-after-q22.json'})
progress['historical_full5_q22_neutral'].update({'status':'COMPLETE_ADOPTED_VERSIONED_SCOPE_EQUIVALENCE_CORRECTION','validation':'historical-full5-q22-neutral-01/validation.json','primary_scores':read(neutral_dir/'validation.json')['primary_scores'],'effective_scores':read(neutral_dir/'validation.json')['effective_scores'],'historical_pair_still_fails':True})
progress['all_completed_outputs']={'count':26,'entry_records':1820,'inventory':'completed-output-grade-inventory-after-q22.json','scored_pairs':12,'additional_complete_attempts':2}
(ROOT/'progress.json').write_text(json.dumps(progress,indent=2,ensure_ascii=False)+'\n')

def fmt(v): return f"{v['correct']}/{v['partial']}/{v['incorrect']}"
rows='\n'.join(f"| {r['pair']} | {fmt(r['primary_scores']['a'])} | {fmt(r['primary_scores']['b'])} | {fmt(r['effective_scores']['a'])} | {fmt(r['effective_scores']['b'])} | {'PASS' if r['effective_pair_pass'] else 'FAIL'} |" for r in ledger)
report=f'''# Exact stamped QA and historical accounting pass; coordinator authorization pending

The current canonical summary covers Original 2017 WizKids base Sidereal Confluence, all nine base species. Remastered, expansions and optional variants are excluded. Its exact SHA-256 is `{sha(canonical)}` (32,068 Unicode characters). The coordinator applied verification `verified`/`2026-11-06` and the standard banner. The worker kept those bytes unchanged during all final and historical work.

The selected NEW full09 Luna/high/fork-none readers both score **86 Correct, 0 Partial, 0 Incorrect**, with no unsupported guessing, on the unchanged frozen v12 bank (86 questions/256 asked facts). All 172 original entries and 512 paired fact checks pass; seven extra output-level numeric claims independently pass without healing any entry omission. Actual process/rules-data delivery before first answer writing and actual original-helper API execution are verified (A 88/B 121 complete source records). Initial no-output turns were technically continued with the same actors, without factual feedback.

NEW pure source audit09 passes on these exact stamped bytes. Actual delivery proves 16 complete texts/53 bounded slices/41 native images before report writing. All 34 source hashes and 15 crop-parent bindings pass. One complete 5,024-character provenance slice survived JSON-escaped within a larger truncated wrapper; strict complete encoded matching and exact decode roundtrip prove its actual delivery, without inferring missing text. The coordinator independently accepted source09 and current full09. Independent source/key, literal asked-scope and coverage verdicts all pass; zero-addition whole-source rewalks 34/35 and all 15 frozen bank versions remain preserved.

All **26 complete submitted outputs, containing 1,820 original entry records**, have factual grades against their own frozen summaries and targets. Twelve scored pairs account for 24 outputs; two extra complete process-deviation attempts are counted separately below. Incomplete or duplicate-ID working checkpoints remain retained and are not complete submitted sets. Process deviations never substitute for factual grades.

Scores below are **Correct / Partial / Incorrect**. Primary and effective records remain distinct.

| Scored pair | Primary A | Primary B | Effective A | Effective B | Effective pair |
| --- | --- | --- | --- | --- | --- |
{rows}

Full01 effective scores include the single earlier authorized Q13 adjudication; pre-adjudication primary grades remain in `full-iteration-01/results-before-adjudication.json`. Its later source-corrected Q36 key is preserved as historical, not promoted to current truth. Seed02 remains graded against its original seed-v2 target; the genuine later scope change created seed-v3 rather than rewriting that history.

For full05 Q22, the coordinator requested **ONE** fresh Sol6.1/high/fork-none neutral decision, given only the clean no-grade packet, the complete exact historical summary, and original 2017 authority. Actual delivery verifies all three complete texts (14 bounded slices) and four native images before the report. The reviewer judged both complete entries Correct: selecting the complete six-player colony and five-player research configurations, plus six actual-five-player Confluence cards, answers the selection question. A separate explicit tally of printed bid spaces was an unasked extra omission gate. The source-correct six/five descriptions remain valid equivalents. `historical-full5-q22-neutral-01/scope-correction-v1.json` explicitly versions this genuine scope/equivalence clarification; `effective-results-v1.json` changes only effective Q22 decisions and retains each original primary grade record. Full05 B Q63 remains Incorrect with its original unsupported-guess assessment, so that historical pair still fails. All frozen question/key/map files, raw outputs and primary grades remain unchanged. Current full09 already passes the original stricter five Q22 facts, including explicit six/five descriptions; it remains the sole selected final pair.

The two extra complete attempts were independently graded by five fresh Sol6.1/high/fork-none graders against each attempt's own full summary, with complete actual model-visible input delivery verified. Original full07 reader B scores **85/0/1** (Q23 falsely makes ordinary resources nontradable and face down). Original full08 reader A scores **85/0/1** (Q80 falsely gives each Kjas half two later actions). Accurate quoted evidence cannot heal either wrong direct assertion. Their process deviations remain separately documented; no complete raw is excluded from factual accounting.

Final evidence is bound by `validation-final-after-q22.json`, `validation-stamped-full9.json`, `completed-output-grade-inventory-after-q22.json`, `scored-pair-history-after-q22.json`, and `historical-full5-q22-neutral-01/validation.json`. Prior raw outputs, failures, grades, freezes, reports and validations remain retained. These are known fixed-set, tool-assisted regression results, not held-out accuracy or OS sandbox guarantees. Full05 B's earlier helper-equivalence proof also remains disclosed as lacking proof of actual original-API execution; that old pair is not selected.

**Goal ACTIVE.** All worker evidence is ready. Coordinator final evidence signoff and explicit completion authorization remain pending. No worker stamp, registry/catalog publication, commit, push, branch/worktree change or cross-chat outgoing message was made. Any later canonical-byte change requires a new full reader pair and new pure source audit on those exact changed bytes.
'''
for name in ['report.md','README.md','STATE.md']:
    old=ROOT/name
    archive=ROOT/(name.removesuffix('.md')+'-history-before-q22-adoption.md')
    assert not archive.exists()
    archive.write_bytes(old.read_bytes())
    old.write_text(report)
print(json.dumps({'status':combined['status'],'scored_pairs':len(ledger),'complete_outputs':26,'entry_records':1820,'canonical_sha256':sha(canonical)}))
