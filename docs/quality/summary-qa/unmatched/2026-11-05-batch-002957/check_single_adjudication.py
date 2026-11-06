from pathlib import Path
import hashlib, json, sys

P = Path(__file__).resolve().parent
I = P / sys.argv[1]
D = I / 'adjudication'
assessment = D / sys.argv[2]
pack_path = D / sys.argv[3]
task = '/root/' + sys.argv[4]
def read(path): return json.loads(path.read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def entry_sha(entry): return hashlib.sha256(json.dumps(entry, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()

a, pack = read(assessment), read(pack_path)
raw_path = I / ('reader-' + pack['reader'] + '.json')
entry = next(x for x in read(raw_path)['answers'] if x['id'] == pack['question']['id'])
assert pack['raw_reader_entry'] == entry
assert pack['original_raw_file_sha256'] == a['original_raw_file_sha256'] == sha(raw_path)
assert pack['raw_entry_canonical_sha256'] == a['raw_entry_canonical_sha256'] == entry_sha(entry)
assert a['id'] == pack['question']['id'] and a['reader'] == pack['reader']
assert [x['fact_index'] for x in a['facts']] == list(range(len(pack['frozen_scope']['required_answer_facts'])))
assert a['grade'] in ['correct', 'partial', 'incorrect']
if a['grade'] == 'correct':
    assert all(x['assessment'] == 'satisfied' for x in a['facts']) and not a['unsupported_correct_guess']
assert a['input_hashes']['summary_sha256'] == sha(I / 'summary-snapshot.md')
assert a['input_hashes']['pack_sha256'] == sha(pack_path)
agent = next(x for x in read(P / 'model-provenance.json')['agents'] if x['task'] == task)
assert agent['confirmed'] and agent['parent'] == '01a1ad02-d3f0-7083-bb2c-847ca80bb819'
assert agent['turns'] and all(x['model'] == 'gpt-6.1-sol' and x['effort'] == 'high' for x in agent['turns'])
review = next(x for x in read(P / 'actual-reviewer-input-delivery-validation.json')['reviewers'] if x['task'] == task)
assert {Path(x['path']).resolve() for x in review['verified_text_inputs']} == {(I / 'summary-snapshot.md').resolve(), pack_path.resolve()}
writes = []
for ordinal, line in enumerate(Path(agent['runtime_source_path']).open()):
    record = json.loads(line)
    value = record.get('payload', {})
    if record.get('type') != 'response_item' or value.get('type') not in ['custom_tool_call', 'function_call']:
        continue
    code = value.get('input', value.get('arguments', ''))
    code = code if isinstance(code, str) else json.dumps(code)
    if assessment.name in code and any(x in code for x in ['write_text', 'write_bytes', 'json.dump', '*** Add File']):
        writes.append({'ordinal': ordinal, 'record_sha256': hashlib.sha256(line.encode()).hexdigest()})
assert writes, 'Inspect actual runtime: no direct assessment write identified'
first = min(x['ordinal'] for x in writes)
inputs = []
for source in review['verified_text_inputs']:
    assert sha(Path(source['path'])) == source['sha256'] and source['complete_contiguous']
    slices = []
    for part in source['slices']:
        before = [x for x in part['runtime_output_record_ordinals'] if x < first]
        assert before
        slices.append({'start': part['start'], 'end': part['end'], 'actual_delivery_records_before_first_write': before})
    inputs.append({'path': source['path'], 'sha256': source['sha256'], 'complete_original_text_before_first_assessment_write': True, 'slices': slices})
out = {'task': task, 'actual_id': agent['identity'], 'runtime_source_path': agent['runtime_source_path'], 'actual_requested_fresh_model_confirmed': True, 'complete_original_text_before_first_assessment_write': True, 'first_assessment_write': next(x for x in writes if x['ordinal'] == first), 'verified_inputs': inputs, 'assessment_path': str(assessment), 'assessment_sha256': sha(assessment), 'pack_sha256': sha(pack_path), 'all_original_entry_fields_preserved': True, 'all_required_fact_indices_once': True, 'grade': a['grade'], 'grade_accepted_by_coordinator': False}
(D / 'actual-delivery-validation.json').write_text(json.dumps(out, indent=2) + '\n')
print('Fresh assessment: complete original inputs before first write; requested model/effort and lossless entry verified. Grade:', a['grade'])
