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
previous_q = read(R/'benchmark-v13/questions.json')['questions']
previous_k = read(R/'benchmark-v13/answer-key.json')['answers']
assert q['questions'][:125] == previous_q
assert [a['id'] for a, b in zip(k['answers'][:125], previous_k) if a != b] == ['Q19', 'Q58', 'Q59', 'Q60', 'Q61', 'Q62']
assert [a['id'] for a, b in zip(k['answers'][:125], previous_k) if a['expected_answer'] != b['expected_answer']] == ['Q19']
assert n == 126
for path, digest in cm.get('accepted_scope_files', {}).items():
    assert sha(Path(path)) == digest, path

d = R/'full-iteration-13'
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
protocol = read(R/'reader-protocol-full126-v7.json')
extra = ' '+protocol['new_generic_premise_instruction']+' '+protocol['new_generic_array_instruction']
for name in ['reader-prompts.json','reader-batch-continuation-prompts.json','reader-second-pass-prompts.json']:
    obj = read(R/'full-iteration-12'/name)
    for rec in obj['records']:
        prompt = rec['prompt'].replace('full-iteration-12','full-iteration-13')
        prompt = prompt.replace('125',str(n))
        anchor = "Check numerical inferences against its listed inputs and the supporting rule, and reconcile the final ruling with the calculation."
        assert anchor in prompt
        prompt = prompt.replace(anchor, anchor+extra)
        rec['prompt']=prompt
        rec['sha256']=hashlib.sha256(prompt.encode()).hexdigest()
    for key in list(obj):
        if '125' in key:obj[key.replace('125',str(n))]=obj.pop(key)
    obj['protocol_version']=protocol['version']
    obj['only_protocol_changes']='Same preplanned small batches and unconditional final review. Generic distinction between rule quantities and scenario inputs; select unanswered IDs in actual array order. No game facts or failure examples.'
    records=obj['records']
    assert records[0]['prompt'].replace('reader-a','reader-X')==records[1]['prompt'].replace('reader-b','reader-X')
    write(d/name,obj)
grading = read(R/'full-iteration-12/grading-prompts.json')
grading.update(created_utc=now, fixed_before_any_reader_output=True, base_protocol_source=str(R/'full-iteration-12/grading-prompts.json'),base_protocol_sha256=sha(R/'full-iteration-12/grading-prompts.json'),grading_standard_unchanged=True,no_dispatch_until_both_final_responses=True)
for rec in grading['records']:
    for key in ['prompt','dispatch_message']:
        if key in rec:rec[key]=rec[key].replace('full-iteration-12','full-iteration-13').replace('ALL125',f'ALL{n}')
    rec['sha256']=hashlib.sha256(rec['prompt'].encode()).hexdigest()
write(d/'grading-prompts.json',grading)
plan=read(R/'full-iteration-12/batch-plan.json')
plan.update(created_utc=now,protocol_version=protocol['version'],total_questions=n)
write(d/'batch-plan.json',plan)
sm = read(R/gate['source_audit_manifest'])
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
