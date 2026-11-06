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

d = R/'full-iteration-10'
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
old_prompts = read(R/'full-iteration-09/reader-prompts.json')
prompts = []
for old in old_prompts['records']:
    prompt = old['prompt'].replace('full-iteration-09','full-iteration-10')
    prompt = prompt.replace('then give an answer string with separate numbered rulings for every one of those clauses.',
        'using one entry per independently requested clause rather than copying the whole question. Then give an answer string with separate numbered rulings aligned with those entries.')
    prompt = prompt.replace('No brevity requirement;',
        'Before saving, check each affirmative ruling, quantity and inference against its cited rule and resolve any internal contradiction. Include the requested facts and necessary reasons without adding unrelated rulings. No brevity requirement;')
    prompt = prompt.replace('reader-a.json','reader-a-draft.json').replace('reader-b.json','reader-b-draft.json')
    prompts.append({'reader':old['reader'],'prompt':prompt,
                    'sha256':hashlib.sha256(prompt.encode()).hexdigest(),
                    'requested_model':'gpt-6-luna','requested_effort':'high','fork_turns':'none'})
normalized=[p['prompt'].replace('reader-a-draft.json','reader-X-draft.json').replace('reader-b-draft.json','reader-X-draft.json') for p in prompts]
assert len(set(normalized)) == 1
write(d/'reader-prompts.json', {'protocol_version':'full10-preplanned-unconditional-two-pass-v4',
      'records':prompts,'only_protocol_changes':'Frozen paths plus neutral individual-clause enumeration and ruling/quote consistency self-check. Identical for both. No game facts, question IDs, failure examples or feedback. Schema/blind inputs/fixed bank/key/rubric unchanged.'})
second_prompts = []
for side in 'ab':
    prompt = (f"Unconditional second pass of the preplanned blind-reader procedure. Read ONLY {d/'summary-snapshot.md'}, {d/'questions.json'}, and your own {d/('reader-'+side+'-draft.json')}. Reread the COMPLETE frozen summary and EVERY question, then review every literal requested clause in your own draft for omissions or contradictions. You have no sources, key, other readers, grades, findings, browsing or outside game knowledge; do not consult any other files or communicate with anyone. Do not infer any particular answer from this generic instruction. For each question, enumerate individual requested clauses, give separate numbered factual rulings and short factual Summary quotations supporting each clause; for a derived outcome quote the rule and state the inference. Check quantities, destinations, timing, exceptions, reasons and consistency when requested. A section/topic label alone supplies no fact, and quotations must be accurate. Fill any missing requested facts that the summary supports, resolve contradictions, and explicitly state when the summary lacks a fact. Never guess. Save the COMPLETE bank of ALL125 answers, including unchanged answers, as valid JSON {{reader,inputs_read,answers:[...]}} with fields id, requested_parts, answer, support(supported/partial/unsupported), evidence(string with factual quotations and any inference). Preserve the first draft. Write ONLY {d/('reader-'+side+'.json')}. Do not evaluate or improve the summary. No brevity requirement; use multiple writes if needed.")
    second_prompts.append({'reader':side,'prompt':prompt,'sha256':hashlib.sha256(prompt.encode()).hexdigest(),'same_reader_context_required':True,'requested_model':'gpt-6-luna','requested_effort':'high','fork_turns':'none-at-initial-spawn'})
assert second_prompts[0]['prompt'].replace('reader-a','reader-X') == second_prompts[1]['prompt'].replace('reader-b','reader-X')
write(d/'reader-second-pass-prompts.json',{'protocol_version':'full10-preplanned-unconditional-two-pass-v4','records':second_prompts,'unconditional_for_both':True,'planned_before_any_current_reader_output':True,'no_current_grading_before_both_final_responses':True,'only_inputs':'Frozen summary/questions and own preserved first draft; no other information.'})
grading = read(R/'full-iteration-09/grading-prompts.json')
grading['created_utc'] = now
grading['fixed_before_any_reader_output'] = True
grading['base_protocol_source'] = str(R/'full-iteration-09/grading-prompts.json')
grading['base_protocol_sha256'] = sha(R/'full-iteration-09/grading-prompts.json')
grading['grading_standard_unchanged'] = True
grading['no_dispatch_until_both_final_responses'] = True
for rec in grading['records']:
    for key in ['prompt','dispatch_message']:
        if key in rec:
            rec[key] = rec[key].replace('full-iteration-09','full-iteration-10')
    rec['sha256'] = hashlib.sha256(rec['prompt'].encode()).hexdigest()
write(d/'grading-prompts.json',grading)
sm = read(R/'source-candidate-14/input-manifest.json')
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
