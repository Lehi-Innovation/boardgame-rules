"""Parent-only lossless delivery proof for independently scheduled reader grades."""
from pathlib import Path
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('bounded_delivery', ROOT / 'prove-bounded-delivery.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def packet_entries(value, role):
    if isinstance(value, dict):
        if all(k in value for k in ['id', 'question_entry', 'key_entry', 'requested_fact_scope_entry', f'reader_{role}_entry']):
            yield value
        for child in value.values():
            yield from packet_entries(child, role)
    elif isinstance(value, list):
        for child in value:
            yield from packet_entries(child, role)


def prove(bank_name, iteration, role, prefix, output_name=None):
    if role not in ['a', 'b']:
        raise ValueError('Expected role a or b')
    run = ROOT / bank_name / iteration
    records = base.read(ROOT / 'model-provenance.json')['records']
    summary = (run / 'summary-snapshot.md').read_text().splitlines()
    result = {}
    for folder in sorted((run / f'grading-reader-{role}').glob('block-*')):
        if not folder.is_dir():
            continue
        actor = f'/root/{prefix}_{folder.name.replace("block-", "")}'
        record = next(x for x in records if x['agent'] == actor)
        outputs, calls, status_calls = base.visible(record)
        text = '\n'.join(outputs)
        missing_lines = [n for n, line in enumerate(summary, 1) if line.strip() and not base.text_present(line, text)]
        packet = base.read(folder / 'packet.json')
        assert packet['reader_role'] == f'reader-{role}'
        metadata = {k: v for k, v in packet.items() if k != 'entries'}
        metadata_delivered, observed = False, {}
        for output in outputs:
            for value in base.decoded_objects(output):
                if base.canonical(value) == base.canonical(metadata):
                    metadata_delivered = True
                for entry in packet_entries(value, role):
                    observed.setdefault(entry['id'], set()).add(base.canonical(entry))
        checks = {e['id']: base.canonical(e) in observed.get(e['id'], set()) for e in packet['entries']}
        result[folder.name] = dict(actor=actor, runtime_source=record['runtime_source'],
            packet_sha256=__import__('hashlib').sha256((folder / 'packet.json').read_bytes()).hexdigest(),
            missing_nonblank_summary_lines=missing_lines, complete_packet_entry_checks=checks,
            complete_grading_metadata_delivered=metadata_delivered, status_or_other_agent_calls=status_calls,
            truncated_outputs=sum('Warning: truncated output' in output for output in outputs),
            complete_input_delivery_confirmed=not missing_lines and all(checks.values()) and metadata_delivered and not status_calls,
            read_calls=calls, limits='Exact full entry/metadata delivery before first output write; not semantic grading proof.')
    manifest = base.read(run / f'grading-reader-{role}/packet-manifest.json')
    assert set(result) == {b['block_id'] for b in manifest['blocks']}
    out = run / (output_name or f'grading-reader-{role}-input-delivery-proof.json')
    with out.open('x') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    return {name: {k: v for k, v in item.items() if k not in ['read_calls', 'runtime_source']} for name, item in result.items()}


if __name__ == '__main__':
    print(json.dumps(prove(*sys.argv[1:]), indent=2))
