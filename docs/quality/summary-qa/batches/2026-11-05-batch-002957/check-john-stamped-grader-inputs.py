"""Independently rebind complete pre-write JSON delivery for terminal graders."""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import re

parser = argparse.ArgumentParser()
parser.add_argument('--role', choices=['a', 'b'], required=True)
role = parser.parse_args().role
BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
IT = REPO / 'docs/quality/summary-qa/john-company-second-edition' / BASE.name / 'expanded-v13-complete-requested-scope/luna-final-stamped-iteration-01'
FOLDER = IT / f'grading-reader-{role}-completion-io-audit-01'
H = lambda value: hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()
load = lambda path: json.loads(path.read_text())
canon = lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from strings(child)


def objects(value):
    if isinstance(value, (dict, list)):
        yield canon(value)
        children = value.values() if isinstance(value, dict) else value
        for child in children:
            yield from objects(child)
    elif isinstance(value, str):
        for match in re.finditer(r'[\[{]', value):
            try:
                child = json.JSONDecoder().raw_decode(value[match.start():])[0]
            except ValueError:
                continue
            yield from objects(child)


audit = load(FOLDER / 'audit.json')
assert audit['all_six_actual_input_receipts_confirmed']
assert audit['all_six_original_report_copies_and_isolated_replay_bytes_match']
summary_path = IT / 'summary-snapshot.md'
summary_lines = summary_path.read_text().splitlines(keepends=True)
assert summary_path.read_bytes() == (REPO / 'rules/john-company-second-edition.md').read_bytes()
proof = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'reader_role': role,
         'summary_sha256': H(summary_path.read_bytes()), 'technical_audit_sha256': H((FOLDER / 'audit.json').read_bytes()),
         'blocks': [], 'private_contexts_retained': False}
for index in range(1, 7):
    block = f'block-{index:02d}'
    packet = load(IT / f'grading-reader-{role}' / block / 'packet.json')
    projection = load(FOLDER / f'{index:02d}-runtime-projection.json')
    with Path(projection['original_runtime_path']).open('rb') as stream:
        original = stream.read(projection['prefix_bytes'])
    assert H(original) == projection['prefix_sha256']
    physical = original.splitlines(keepends=True)
    rows = {n: json.loads(line) for n, line in enumerate(physical, 1)}
    bindings = projection.get('physical_records', projection.get('records'))
    for item in bindings:
        ordinal = item.get('physical_record', item.get('ordinal'))
        assert H(physical[ordinal - 1]) == item['sha256'] and len(physical[ordinal - 1]) == item['bytes']
    for call in projection['tool_calls']:
        row = rows[call['physical_record']]['payload']
        assert row['call_id'] == call['call_id'] and row['name'] == call['name']
        assert row.get('input', row.get('arguments')) == call['input']
    for output in projection['tool_outputs']:
        row = rows[output['physical_record']]['payload']
        assert row['call_id'] == output['call_id']
        actual = list(strings(row['output']))
        projected = output.get('text_blocks', output.get('visible_text_blocks'))
        assert projected and all(piece in actual for piece in projected)
    contexts = [(row['payload'].get('model'), row['payload'].get('effort')) for row in rows.values() if row['type'] == 'turn_context']
    assert contexts and all(item == ('gpt-6.1-sol', 'high') for item in contexts)
    run = audit['runs'][block]
    boundary = run['first_mutation_record']
    actual_objects = set()
    output_records = []
    for ordinal, row in rows.items():
        if ordinal >= boundary or row['type'] != 'response_item' or row['payload'].get('type') not in ('custom_tool_call_output', 'function_call_output'):
            continue
        actual_objects.update(objects(row['payload']['output']))
        output_records.append(ordinal)
    expected_chunks = []
    for start in range(0, len(summary_lines), 45):
        text = ''.join(summary_lines[start:start + 45])
        expected_chunks.append({'qa_delivery': 'summary-chunk-v1', 'start_line': start + 1,
            'end_line': min(start + 45, len(summary_lines)), 'text': text, 'sha256': H(text)})
    assert all(canon(chunk) in actual_objects for chunk in expected_chunks)
    assert all(canon(entry) in actual_objects for entry in packet['entries'])
    assert canon({k: v for k, v in packet.items() if k != 'entries'}) in actual_objects
    replay = load(FOLDER / f'{index:02d}-isolated-replay.json')
    report = IT / f'grading-reader-{role}' / block / 'grades-same-entry.json'
    assert replay['report_byte_equality'] and replay['replay_sha256'] == replay['original_report_sha256'] == H(report.read_bytes())
    proof['blocks'].append({'block': block, 'original_runtime_path': projection['original_runtime_path'],
        'runtime_prefix_sha256': projection['prefix_sha256'], 'physical_records': len(physical),
        'summary_chunks_before_first_write': len(expected_chunks), 'complete_original_packet_entries_before_first_write': len(packet['entries']),
        'metadata_before_first_write': True, 'first_write_record': boundary, 'actual_model_contexts': len(contexts),
        'grade_report_sha256': H(report.read_bytes()), 'retained_extra_calls': len(run['noncanonical_extra_calls_preserved']),
        'in_place_resumption_qualification': run['in_place_resumption_qualification']})
proof.update(verified=True, qualifications=audit['qualifications'], limits='Complete actual pre-write input delivery and original report bindings only. Independent gameplay grades, initial fresh-spawn verification, source audit, coverage and final publication remain separate gates. Original strict false flags and technical deviations remain unchanged.')
out = BASE / f'coordinator-checks/john-stamped-i1-reader-{role}-actual-grader-inputs.json'
assert not out.exists()
out.write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps({'verified': True, 'role': role, 'blocks': len(proof['blocks']), 'complete_entries': sum(b['complete_original_packet_entries_before_first_write'] for b in proof['blocks']), 'proof': str(out)}))
