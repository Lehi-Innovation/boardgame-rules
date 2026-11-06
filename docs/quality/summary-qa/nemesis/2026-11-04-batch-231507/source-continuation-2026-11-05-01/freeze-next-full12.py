"""Freeze only after an explicit, reviewable source/coverage gate decision exists."""
from pathlib import Path
import copy, datetime, hashlib, json, sys

R = Path(__file__).resolve().parent
ROOT = R.parents[5]
def read(p):
    return json.loads(p.read_text())
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, value):
    with p.open('x') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')

gate_path = (R/sys.argv[1]).resolve()
assert gate_path.parent == R
gate = read(gate_path)
assert gate['allow_reader_freeze'] is True
benchmark = R/gate['benchmark_version']
q = read(benchmark/'questions.json')
k = read(benchmark/'answer-key.json')
n = len(q['questions'])
ids = [x['id'] for x in q['questions']]
assert n == gate['question_count'] == len(k['answers']) == len(set(ids))
assert ids == [x['id'] for x in k['answers']]
assert {'Q109', 'Q124'}.isdisjoint(ids)
coverage_manifest_path = R/gate['coverage_manifest']
cm = read(coverage_manifest_path)
assert sha(benchmark/'questions.json') == cm['question_sha256']
assert sha(benchmark/'answer-key.json') == cm['key_sha256']
assert sha(Path(cm['author_coverage_map'])) == cm['author_coverage_map_sha256']
for path, digest in cm['source_files'].items():
    assert sha(Path(path)) == digest, path
coverage_report_path = R/gate['coverage_report']
assert sha(coverage_report_path) == gate['coverage_report_sha256']
source_report_path = R/gate['source_audit']
source_report = read(source_report_path)
assert source_report['source_fidelity_rating'] == 'PASS'
summary_bytes = (ROOT/'rules/nemesis.md').read_bytes()
summary_hash = hashlib.sha256(summary_bytes).hexdigest()
assert summary_hash == gate['summary_sha256'] == source_report['summary_sha256']
rubric_path = R/gate['rubric_file']
assert read(rubric_path)['benchmark_version'] == gate['benchmark_version']
assert read(rubric_path)['source_unresolved_question_ids'] == []
prior = read(R/'full-iteration-08/input-manifest.json')
assert (benchmark/'questions.json').read_bytes() == (R/'full-iteration-08/questions.json').read_bytes()
assert sha(benchmark/'answer-key.json') == prior['hashes'][str(benchmark/'answer-key.json')]
assert sha(rubric_path) == prior['hashes'][str(rubric_path)]

d = R/'full-iteration-12'
d.mkdir()
(d/'summary-snapshot.md').write_bytes(summary_bytes)
(d/'questions.json').write_bytes((benchmark/'questions.json').read_bytes())
now = datetime.datetime.now(datetime.timezone.utc).isoformat()
hashes = {str(d/'summary-snapshot.md'):summary_hash,
          str(d/'questions.json'):sha(d/'questions.json'),
          str(benchmark/'answer-key.json'):sha(benchmark/'answer-key.json'),
          str(rubric_path):sha(rubric_path), str(gate_path):sha(gate_path),
          str(coverage_manifest_path):sha(coverage_manifest_path),
          str(coverage_report_path):sha(coverage_report_path),
          str(Path(cm['author_coverage_map'])):cm['author_coverage_map_sha256'],
          str(source_report_path):sha(source_report_path),
          **cm['source_files']}
for name in gate['scope_and_provenance_files']:
    hashes[str(R/name)] = sha(R/name)
write(d/'input-manifest.json', {'created_utc':now,'benchmark_version':gate['benchmark_version'],
      'question_count':n,'requested_model':'gpt-6-luna','requested_effort':'high',
      'fork_turns':'none','hashes':hashes,'coverage_gate_decision':str(gate_path),
      'pre_reader_source_audit':str(source_report_path),
      'pre_reader_source_audit_exact_same_summary_bytes':True,
      'source_fidelity_is_not_complete_core_pass':True})
premise = " Treat each question as an independent scenario unless it explicitly says otherwise; use only that question's own stated premises. Check numerical inferences against its listed inputs and the supporting rule, and reconcile the final ruling with the calculation."
prompts=[]
for old in read(R/'full-iteration-11/reader-prompts.json')['records']:
    prompt=old['prompt'].replace('full-iteration-11','full-iteration-12')
    prompt=prompt.replace('Answer ALL125 questions from summary.', 'Across preplanned batches, answer the entire125-question bank from the summary. In THIS turn, answer only the first up-to10 question objects in original array order; save those substantive answers before stopping. Later preplanned continuations will cover the remaining questions in this same context.'+premise)
    prompt=prompt.replace('For EACH question,','For EACH question in this batch,')
    prompt=prompt.replace('Save valid JSON {reader,inputs_read,answers:[...]}', 'Stop after this batch is saved. Save valid JSON {reader,inputs_read,answers:[...]} containing only the answered prefix, with no unanswered placeholder entries,')
    prompts.append({'reader':old['reader'],'prompt':prompt,'sha256':hashlib.sha256(prompt.encode()).hexdigest(),'requested_model':'gpt-6-luna','requested_effort':'high','fork_turns':'none'})
assert prompts[0]['prompt'].replace('reader-a','reader-X')==prompts[1]['prompt'].replace('reader-b','reader-X')
write(d/'reader-prompts.json',{'protocol_version':'full12-preplanned-small-batches-complete-rule-evidence-v6','records':prompts,'first_turn_batch_size':10,'only_protocol_changes':'Original-order batches about10 plus generic independent-premise and numerical-inference checks. Same complete-rule evidence and no outside feedback. Both same fresh identities cover all125. No game facts, failure examples or selected IDs supplied; fixed bank/key/rubric unchanged.'})
continuations=[]
for side in 'ab':
    prompt=(f"Preplanned blind-reader batch continuation. Remain in your original reader context. Read ONLY {d/'summary-snapshot.md'}, {d/'questions.json'}, and your own cumulative {d/('reader-'+side+'-draft.json')}. Continue with the next unanswered batch of up to10 question objects in the original frozen array order. Append substantive answers to your own cumulative draft, preserving all earlier saved answers unchanged; save the batch before stopping. Do not create entries for questions you have not answered. Across these continuations you will answer the entire125 bank before the preplanned full-bank final review. No source/key, other files, other reader/reviewer contact, browsing, prior game knowledge, rule/grade/finding feedback or parent history. Parent contact is file/processing status only."+premise+" For each question in this batch, enumerate its individual literal requested clauses, provide separate numbered factual rulings, and evidence containing complete supporting operative Summary sentence(s) with relevant conditions, exceptions and outcomes. For an inference, quote its complete supporting rule and identify the inference. Resolve every requested part the summary supports; if it lacks a fact, state that explicitly and never guess. Check your rulings against their cited rules and resolve internal contradictions before saving. Schema remains {reader,inputs_read,answers:[...]} with each object id, requested_parts(array), answer(string), support(supported/partial/unsupported), evidence(string). Keep numbered rulings and evidence aligned to requested parts. Write ONLY the assigned cumulative draft; preserve frozen inputs. Stop after this saved batch and report processing/file status. No brevity requirement; use multiple writes if needed. Do not evaluate or improve the summary.")
    continuations.append({'reader':side,'prompt':prompt,'sha256':hashlib.sha256(prompt.encode()).hexdigest(),'same_original_reader_context_required':True,'requested_model':'gpt-6-luna','requested_effort':'high','fork_turns':'none-at-initial-spawn'})
assert continuations[0]['prompt'].replace('reader-a','reader-X')==continuations[1]['prompt'].replace('reader-b','reader-X')
write(d/'reader-batch-continuation-prompts.json',{'protocol_version':'full12-preplanned-small-batches-complete-rule-evidence-v6','records':continuations,'planned_before_any_output':True,'same_generic_continuation_for_every_next_batch':True,'batch_size':10,'no_factual_feedback_or_grading':True})
second=[]
for old in read(R/'full-iteration-11/reader-second-pass-prompts.json')['records']:
    prompt=old['prompt'].replace('full-iteration-11','full-iteration-12')
    prompt=prompt.replace('Do not infer any particular answer from this generic instruction.', 'Do not infer any particular answer from this generic instruction.'+premise)
    second.append({'reader':old['reader'],'prompt':prompt,'sha256':hashlib.sha256(prompt.encode()).hexdigest(),'same_reader_context_required':True,'requested_model':'gpt-6-luna','requested_effort':'high','fork_turns':'none-at-initial-spawn'})
assert second[0]['prompt'].replace('reader-a','reader-X')==second[1]['prompt'].replace('reader-b','reader-X')
write(d/'reader-second-pass-prompts.json',{'protocol_version':'full12-preplanned-small-batches-complete-rule-evidence-v6','records':second,'unconditional_for_both_after_all125_first_draft_answers':True,'planned_before_any_current_output':True,'no_current_grading_before_both_final_banks':True})
grading=read(R/'full-iteration-11/grading-prompts.json')
grading['created_utc']=now
grading['fixed_before_any_reader_output']=True
grading['base_protocol_source']=str(R/'full-iteration-11/grading-prompts.json')
grading['base_protocol_sha256']=sha(R/'full-iteration-11/grading-prompts.json')
grading['grading_standard_unchanged']=True
grading['no_dispatch_until_both_final_responses']=True
for rec in grading['records']:
    for key in ['prompt','dispatch_message']:
        if key in rec:rec[key]=rec[key].replace('full-iteration-11','full-iteration-12')
    rec['sha256']=hashlib.sha256(rec['prompt'].encode()).hexdigest()
write(d/'grading-prompts.json',grading)
write(d/'batch-plan.json',{'created_utc':now,'protocol_version':'full12-preplanned-small-batches-complete-rule-evidence-v6','batch_size':10,'total_questions':125,'order':'Original array order','same_two_fresh_contexts_for_entire_bank':True,'every_continuation_luna_high_required':True,'save_each_batch_before_next':True,'preserve_each_cumulative_prefix_snapshot':True,'parent_checks_structural_only':True,'unconditional_complete_input_and_bank_final_review_for_both':True,'no_grading_before_both_final_banks':True,'source_key_or_factual_feedback_forbidden':True})
sm = read(R/'source-candidate-16/input-manifest.json')
sm['summary_file'] = str(d/'summary-snapshot.md')
sm['summary_sha256'] = summary_hash
sm['previous_source_only_audit'] = str(source_report_path)
sm['previous_source_only_audit_sha256'] = sha(source_report_path)
write(d/'source-audit-input-manifest.json',sm)
write(d/'freeze-record.json', {'created_utc':now,'question_count':n,
      'benchmark_version':gate['benchmark_version'],'summary_sha256':summary_hash,
      'canonical_matches_snapshot':True,'all_supplied_source_hashes_verified':True,
      'gates_settled_before_reader_dispatch':True,'gate_decision':str(gate_path),
      'requested_parts_rubric':str(rubric_path),'no_reader_outputs_exist_at_freeze':True,
      'fresh_luna_high_required':True,'final_exact_byte_source_correspondence_check_pending':True,
      'complete_core_pass':False,'no_stamping':True})
print(json.dumps({'frozen_directory':str(d),'questions':n,'summary_sha256':summary_hash}))
