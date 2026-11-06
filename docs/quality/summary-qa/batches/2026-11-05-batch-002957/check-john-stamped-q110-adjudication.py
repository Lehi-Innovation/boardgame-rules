"""Verify the single neutral whole-entry adjudication without altering primary grades."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

B = Path(__file__).resolve().parent
R = B.parents[4] / 'docs/quality/summary-qa/john-company-second-edition' / B.name
BANK = R / 'expanded-v13-complete-requested-scope'
IT = BANK / 'luna-final-stamped-iteration-01'
D = IT / 'independent-q110-whole-entry-adjudication-01'
load = lambda path: json.loads(path.read_text())
H = lambda value: hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()
canon = lambda value: json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, (list, dict)):
        for child in (value.values() if isinstance(value, dict) else value):
            yield from strings(child)


def objects(value):
    if isinstance(value, (dict, list)):
        yield canon(value)
        for child in (value.values() if isinstance(value, dict) else value):
            yield from objects(child)
    elif isinstance(value, str):
        for match in re.finditer(r'[\[{]', value):
            try:
                decoded = json.JSONDecoder().raw_decode(value[match.start():])[0]
            except ValueError:
                continue
            yield from objects(decoded)


packet = load(D / 'packet.json')
assert len(packet['entries']) == 1
entry = packet['entries'][0]
assert entry['id'] == 'Q110'
q = next(x for x in load(BANK / 'questions.json')['questions'] if x['id'] == 'Q110')
key = next(x for x in load(BANK / 'answer-key.json')['answers'] if x['id'] == 'Q110')
scope = next(x for x in load(BANK / 'requested-fact-scope-reviewed.json')['questions'] if x['id'] == 'Q110')
raw = next(x for x in load(IT / 'reader-b.json')['answers'] if x['id'] == 'Q110')
assert entry['question_entry'] == q and entry['key_entry'] == key and entry['requested_fact_scope_entry'] == scope and entry['reader_b_entry'] == raw
assert 'reader_a_entry' not in entry
primary_path = IT / 'grading-reader-b/block-06/grades-same-entry.json'
primary = next(x for x in load(primary_path)['readers']['reader-b']['grades'] if x['id'] == 'Q110')
assert primary['grade'] == 'Partial'
report_path = D / 'adjudication.json'
report = load(report_path)
grade, = report['readers']['reader-b']['grades']
assert grade['id'] == 'Q110' and grade['grade'] == 'Correct' and not grade['unsupported_guesses']
assert [p['requirement'] for p in grade['material_parts']] == scope['material_requested_facts']
for part in grade['material_parts']:
    assert part['status'] == 'covered' and part['reader_quotes']
    assert all(any(quote in s for s in strings(raw)) for quote in part['reader_quotes'])
projection = load(D / 'parent-runtime-projection.json')
with Path(projection['original_runtime_path']).open('rb') as stream:
    original = stream.read(projection['prefix_bytes'])
assert H(original) == projection['prefix_sha256']
physical = original.splitlines(keepends=True)
rows = {n: json.loads(line) for n, line in enumerate(physical, 1)}
for item in projection['physical_records']:
    n = item['physical_record']
    assert H(physical[n - 1]) == item['sha256'] and len(physical[n - 1]) == item['bytes']
for call in projection['tool_calls']:
    p = rows[call['physical_record']]['payload']
    assert p['call_id'] == call['call_id'] and p['name'] == call['name'] and p.get('input', p.get('arguments')) == call['input']
for output in projection['tool_outputs']:
    p = rows[output['physical_record']]['payload']
    assert p['call_id'] == output['call_id']
    actual = list(strings(p['output']))
    assert all(piece in actual for piece in output.get('text_blocks', output.get('visible_text_blocks')))
contexts = [(row['payload'].get('model'), row['payload'].get('effort')) for row in rows.values() if row['type'] == 'turn_context']
assert contexts and all(x == ('gpt-6.1-sol', 'high') for x in contexts)
validation = load(D / 'parent-initial-delivery-and-report-validation.json')
boundary = validation['first_possible_mutation_record']
seen = set()
for n, row in rows.items():
    if n < boundary and row['type'] == 'response_item' and row['payload'].get('type') in ('custom_tool_call_output', 'function_call_output'):
        seen.update(objects(row['payload']['output']))
summary_path = IT / 'summary-snapshot.md'
lines = summary_path.read_text().splitlines(keepends=True)
for start in range(0, len(lines), 45):
    text = ''.join(lines[start:start + 45])
    assert canon({'qa_delivery': 'summary-chunk-v1', 'start_line': start + 1, 'end_line': min(start + 45, len(lines)), 'text': text, 'sha256': H(text)}) in seen
assert canon({k: v for k, v in packet.items() if k != 'entries'}) in seen and canon(entry) in seen
assert validation['actual_terminal_event']['event'] == 'task_complete'
assert validation['two_actual_writer_checks'][-1]['successful_literal_only_reconstruction_byte_equal']
assert validation['two_actual_writer_checks'][-1]['report_sha256'] == H(report_path.read_bytes())
out = B / 'coordinator-checks/john-stamped-q110-neutral-acceptance.json'
assert not out.exists()
proof = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'question': 'Q110', 'reader': 'b', 'primary_grade': 'Partial', 'primary_report_path': str(primary_path), 'primary_report_sha256': H(primary_path.read_bytes()), 'neutral_grade': 'Correct', 'neutral_report_path': str(report_path), 'neutral_report_sha256': H(report_path.read_bytes()), 'all_four_frozen_requested_atoms_resolved': True, 'original_complete_raw_entry_and_key_scope_unchanged': True, 'actual_complete_summary_chunks_before_first_write': len(range(0, len(lines), 45)), 'actual_complete_original_packet_before_first_write': True, 'actual_runtime_path': projection['original_runtime_path'], 'actual_runtime_prefix_sha256': projection['prefix_sha256'], 'physical_records_rebound': len(physical), 'actual_contexts_Sol61_high': True, 'first_possible_write_record': boundary, 'root_semantic_disposition': 'Accept equivalent contextual wording: the whole entry makes further Deploys conditional on normal targeting, effect, exhaustion and check rules while able. The question asks whether ordinary restrictions continue; it does not separately ask a worked zero-dice example. All four unchanged requested facts are resolved without a contrary ruling. This agrees with the single fresh neutral review and the earlier coordinator whole-entry spot-check; no vote or new key is used.', 'qualification': validation['qualification'], 'separate_remaining_gates': ['Initial fresh-spawn/model proof', 'Complete paired primary/effective aggregate integrity', 'Independent exact-byte source and coverage gates', 'Coordinator final stamping/publication authorization']}
out.write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps({'verified': True, 'adjudicated_grade': 'Correct', 'atoms': 4, 'proof': str(out)}))
