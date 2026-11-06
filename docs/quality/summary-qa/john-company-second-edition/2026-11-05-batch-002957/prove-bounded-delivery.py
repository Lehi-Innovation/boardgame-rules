"""Prove complete visible inputs before first output write; never edits raw runs."""
from pathlib import Path
import hashlib, json, sys

ROOT = Path(__file__).resolve().parent

def read(p):
    return json.loads(p.read_text())

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def strings(value, depth=0):
    if depth > 5:
        return []
    if isinstance(value, dict):
        return [s for v in value.values() for s in strings(v, depth + 1)]
    if isinstance(value, list):
        return [s for v in value for s in strings(v, depth + 1)]
    if isinstance(value, str):
        out = [value]
        try:
            decoded = json.loads(value)
            if decoded != value:
                out += strings(decoded, depth + 1)
        except ValueError:
            pass
        return out
    return []

def visible(record):
    outputs, calls, status_calls = [], [], []
    for line in Path(record['runtime_source']).open():
        item = json.loads(line)
        payload = item.get('payload', {})
        if item.get('type') != 'response_item':
            continue
        kind = payload.get('type')
        if kind in ['custom_tool_call', 'function_call']:
            code = payload.get('input', payload.get('arguments', ''))
            name = payload.get('name', '')
            if name in ['list_agents', 'wait_agent', 'send_message', 'followup_task', 'spawn_agent']:
                status_calls.append(name)
            if any(token in code for token in ['write_text', 'cat >', 'json.dump(', "open(output"]):
                break
            calls.append(dict(name=name, call_id=payload.get('call_id'), input=code))
        elif kind in ['custom_tool_call_output', 'function_call_output']:
            outputs += strings(payload.get('output', ''))
    return outputs, calls, status_calls

def text_present(needle, text):
    return any(x in text for x in [needle, json.dumps(needle, ensure_ascii=False)[1:-1],
                                  json.dumps(needle, ensure_ascii=True)[1:-1]])

def decoded_objects(text):
    decoder = json.JSONDecoder()
    position = 0
    while position < len(text):
        if text[position] not in '[{':
            position += 1
            continue
        try:
            value, end = decoder.raw_decode(text, position)
            yield value
            position = end
        except ValueError:
            position += 1

def packet_entries(value):
    if isinstance(value, dict):
        if all(k in value for k in ['id', 'question_entry', 'key_entry', 'reader_a_entry', 'reader_b_entry']):
            yield value
        for v in value.values():
            yield from packet_entries(v)
    elif isinstance(value, list):
        for v in value:
            yield from packet_entries(v)

def main(mode, bank_name, iteration, prefix):
    run = ROOT / bank_name / iteration
    records = read(ROOT / 'model-provenance.json')['records']
    summary = (run / 'summary-snapshot.md').read_text().splitlines()
    jobs = [(role, f'/root/{prefix}_reader_{role}', None) for role in 'ab'] if mode == 'readers' else [
        (p.name, f'/root/{prefix}_{p.name.replace("block-", "")}', p)
        for p in sorted((run / 'grading-blocks').glob('block-*')) if p.is_dir()]
    result = {}
    for label, actor, folder in jobs:
        record = next(x for x in records if x['agent'] == actor)
        outputs, calls, status_calls = visible(record)
        text = '\n'.join(outputs)
        missing_lines = [n for n, line in enumerate(summary, 1) if line.strip() and not text_present(line, text)]
        entry_checks = {}
        metadata_delivered = None
        if mode == 'readers':
            missing = [q['id'] for q in read(run / 'questions.json')['questions'] if not text_present(q['question'], text)]
        else:
            packet = read(folder / 'packet.json')
            metadata = {k: v for k, v in packet.items() if k != 'entries'}
            metadata_delivered = False
            expected = {e['id']: canonical(e) for e in packet['entries']}
            observed = {}
            for output in outputs:
                for value in decoded_objects(output):
                    if canonical(value) == canonical(metadata):
                        metadata_delivered = True
                    for entry in packet_entries(value):
                        observed.setdefault(entry['id'], set()).add(canonical(entry))
            entry_checks = {qid: encoded in observed.get(qid, set()) for qid, encoded in expected.items()}
            missing = [qid for qid, ok in entry_checks.items() if not ok]
        truncated = sum('Warning: truncated output' in output for output in outputs)
        complete = not missing_lines and not missing and not status_calls and metadata_delivered is not False
        result[label] = dict(actor=actor, runtime_source=record['runtime_source'], summary_lines=len(summary),
            missing_nonblank_summary_lines=missing_lines, missing_questions_or_complete_packet_entries=missing,
            complete_packet_entry_checks=entry_checks, status_or_other_agent_calls=status_calls,
            complete_grading_metadata_delivered=metadata_delivered,
            truncated_outputs=truncated, any_truncation_recovered=bool(truncated and complete),
            complete_input_delivery_confirmed=complete, read_calls=calls,
            limits='Exact text/JSON-equivalent delivery before first output write; not proof of attention or correctness.')
    path = run / ('input-delivery-proof.json' if mode == 'readers' else 'grading-input-delivery-proof.json')
    assert not path.exists(), 'Preserve earlier proof attempts; use a new filename for any amended analysis'
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({label: {k: v for k, v in value.items() if k not in ['read_calls', 'runtime_source', 'limits']}
                      for label, value in result.items()}, indent=2))

if __name__ == '__main__':
    main(*sys.argv[1:5])
