"""Parent binding check of already independently inspected grader IO evidence.

Never executes a grader program or decides a gameplay grade. The post-write
command decoder accepts only two constant exec/forward wrappers. It does not
change either original initial-delivery proof or the adopted normalizer.
"""
from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'expanded-v13-complete-requested-scope/luna-iteration-03'
role = sys.argv[1]
assert role in ['a', 'b']
AUDIT = RUN / f'grading-reader-{role}-completion-io-audit-01'
spec = importlib.util.spec_from_file_location('postwrite_literal_grammar', ROOT / 'literal-read-js-format-proposal-01/read_call_format_proposal.py')
grammar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grammar)
WS = grammar._WS
direct = re.compile(
    rf'\A{WS}text{WS}\({WS}await[ \t\r\n\v\f]+tools{WS}\.{WS}exec_command'
    rf'{WS}\({WS}\{{{WS}(?:cmd|"cmd"){WS}:{WS}(?P<command>{grammar._STRING})'
    rf'{WS},{WS}(?:max_output_tokens|"max_output_tokens"){WS}:{WS}24000'
    rf'{WS}\}}{WS}\){WS}\){WS};{WS}\Z')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(name):
    return json.loads((AUDIT / name).read_text())


freeze = read('freeze-manifest.json')
for name, binding in freeze['input_file_bindings'].items():
    data = (RUN / name).read_bytes()
    assert len(data) == binding['bytes'] and sha(data) == binding['sha256'], name

records = calls = outputs = 0
programs = []
assessment = read('audit.json')
for number in range(1, 7):
    block = f'{number:02d}'
    projection = read(f'{block}-runtime-projection.json')
    data = Path(projection['original_runtime_path']).read_bytes()[:projection['prefix_bytes']]
    assert sha(data) == projection['prefix_sha256']
    lines = data.splitlines(keepends=True)
    assert len(lines) == len(projection['physical_records'])
    actual = {}
    for ordinal, (line, binding) in enumerate(zip(lines, projection['physical_records']), 1):
        item = json.loads(line)
        payload = item.get('payload', {})
        actual[ordinal] = item
        assert set(binding) == {'physical_record', 'ordinal', 'sha256', 'bytes', 'type', 'payload_type'}
        assert binding == dict(physical_record=ordinal, ordinal=ordinal - 1,
            sha256=sha(line), bytes=len(line), type=item.get('type'), payload_type=payload.get('type'))
        records += 1
    for call in projection['tool_calls']:
        assert set(call) == {'physical_record', 'name', 'call_id', 'input'}
        item = actual[call['physical_record']]
        payload = item['payload']
        assert item['type'] == 'response_item' and payload['type'] in ['function_call', 'custom_tool_call']
        assert call['name'] == payload['name'] and call['call_id'] == payload['call_id']
        assert call['input'] == payload.get('input', payload.get('arguments'))
        calls += 1
    for output in projection['tool_outputs']:
        assert set(output) == {'physical_record', 'call_id', 'text_blocks'}
        payload = actual[output['physical_record']]['payload']
        assert payload['type'] in ['function_call_output', 'custom_tool_call_output']
        assert payload['call_id'] == output['call_id']
        value = payload['output']
        texts = [value] if isinstance(value, str) else [part['text'] for part in value
            if part.get('type') in ['text', 'input_text']]
        assert texts == output['text_blocks']
        outputs += 1
    for metadata in projection['actual_metadata']:
        payload = actual[metadata['physical_record']]['payload']
        if 'model' in metadata:
            assert set(metadata) == {'physical_record', 'model', 'effort'}
            assert metadata['model'] == payload['model'] == 'gpt-6.1-sol'
            assert metadata['effort'] == payload['effort'] == 'high'
        else:
            assert set(metadata) == {'physical_record', 'agent_path', 'parent_thread_id'}
            assert metadata['agent_path'] == payload['agent_path'] == f'/root/v13_i3_grade_{role}_{block}'
            assert metadata['parent_thread_id'] == payload['parent_thread_id'] == '01a1aaa2-7c89-7c92-bca8-a89efc3fe4d7'
    for event in projection['events']:
        assert set(event) == {'physical_record', 'event'}
        assert actual[event['physical_record']]['payload']['type'] == event['event']
    assert projection['events'][-1]['event'] == 'task_complete'
    report = RUN / f'grading-reader-{role}/block-{block}/grades-same-entry.json'
    replay = read(f'{block}-isolated-replay.json')
    assert replay['replay_sha256'] == replay['original_report_sha256'] == sha(report.read_bytes())
    assert (AUDIT / f'{block}-grades-same-entry.json').read_bytes() == report.read_bytes()
    boundary = assessment['runs'][f'block-{block}']['first_mutation_record']
    call = next(item for item in projection['tool_calls'] if item['physical_record'] == boundary)
    body = call['input'].strip()
    if body.startswith('// @exec:'):
        body = body.split('\n', 1)[1].strip()
    assert body.startswith('// QA_ARTIFACT_WRITE_V1\n')
    body = body.split('\n', 1)[1].strip()
    match = grammar._CALL.fullmatch(body)
    if match:
        command = json.loads(match.group('first'))
        if match.group('second'):
            command += json.loads(match.group('second'))
    else:
        match = direct.fullmatch(body)
        assert match is not None, block
        command = json.loads(match.group('command'))
    program = (AUDIT / f'{block}-program-{boundary}.py').read_text()
    assert sha(program.encode()) == replay['program_sha256']
    candidates = ["python3 - <<'PY'\n" + program + ending for ending in ['\nPY', 'PY']]
    if role == 'a' and block == '02':
        candidates += ["cat > /tmp/qa-block02-write.py <<'PY'\n" + program + ending
            + '\npython3 /tmp/qa-block02-write.py' for ending in ['\nPY', 'PY']]
    assert command.strip() in [value.strip() for value in candidates], block
    programs.append(dict(block=f'block-{block}', actual_program_matches_retained_inspected_source=True,
        report_sha256=sha(report.read_bytes())))

result = dict(at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), reader=role,
    all_six_original_runtime_prefixes_and_every_record_hash_verified=True,
    physical_record_bindings=records, actual_tool_call_bindings=calls,
    actual_visible_tool_output_bindings=outputs, only_allowlisted_projection_fields=True,
    all_model_contexts_and_terminal_events_bound_to_originals=True,
    all_inspected_programs_bound_to_actual_first_write_commands=programs,
    all_six_report_copy_and_replay_hashes_match_originals=True,
    source_packet_reader_and_proof_bindings_unchanged=True,
    independent_qualified_technical_assessment=str(AUDIT / 'audit.json'), factual_grades_unchanged=True,
    original_strict_and_normalized_false_results_preserved=True,
    parent_only_postwrite_decoder='Constant wrappers with harmless whitespace; no initial proof/parser/helper modification or grader-program execution.',
    limits='Parent original-record/program/report binding verification; independent manual decision-code inspection is not repeated or replaced.')
with (RUN / f'reader-{role}-grading-completion-verification.json').open('x') as handle:
    json.dump(result, handle, indent=2)
    handle.write('\n')
print(json.dumps(dict(reader=role, records=records, calls=calls, outputs=outputs,
    programs=len(programs), bindings='PASS')))
