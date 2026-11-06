"""Exact, frozen, parent-only delivery proof with a declared read-only interface."""
from pathlib import Path
import hashlib
import importlib.util
import json
import shlex
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('bounded_delivery', ROOT / 'prove-bounded-delivery.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

# This fixed program only reads the two approved inputs and prints one JSON value.
READ_SCRIPT = '''from pathlib import Path
import hashlib,json,sys
summary_path,packet_path,mode,index=sys.argv[1:]
index=int(index)
if mode=="summary":
 text=Path(summary_path).read_text()
 pieces=text.split("\\n")
 lines=[line+"\\n" for line in pieces[:-1]]
 if pieces[-1]: lines.append(pieces[-1])
 chunk="".join(lines[index:index+45])
 value={"qa_delivery":"summary-chunk-v1","start_line":index+1,"end_line":min(index+45,len(lines)),"text":chunk,"sha256":hashlib.sha256(chunk.encode()).hexdigest()}
elif mode=="metadata":
 packet=json.loads(Path(packet_path).read_text())
 value={key:item for key,item in packet.items() if key!="entries"}
elif mode=="entry":
 packet=json.loads(Path(packet_path).read_text())
 value=packet["entries"][index]
else: raise ValueError("unknown read mode")
print(json.dumps(value,ensure_ascii=False))'''
WRITE_MARKER = '// QA_ARTIFACT_WRITE_V1\n'


def physical_lines(text):
    pieces = text.split('\n')
    return [line + '\n' for line in pieces[:-1]] + ([pieces[-1]] if pieces[-1] else [])


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_prefix(summary, packet):
    return shlex.join(['python3', '-c', READ_SCRIPT, str(summary), str(packet)])


def read_call(summary, packet, mode, index):
    return ('const r = await tools.exec_command({cmd: ' + json.dumps(read_prefix(summary, packet)) + ' + '
            + json.dumps(' ' + mode + ' ' + str(index))
            + ', max_output_tokens: 24000});\ntext(r.output);')


def call_body(code):
    code = code.strip()
    if code.startswith('// @exec:'):
        code = code.split('\n', 1)[1].strip()
    return code


def session_delivery(record, permitted_calls):
    """Only exact known read-only calls may precede the first possible mutation."""
    outputs, calls, unknown, status, post_calls, unmatched = [], [], [], [], [], []
    recorded_calls = {}
    boundary = None
    for line in Path(record['runtime_source']).open():
        item = json.loads(line)
        if item.get('type') != 'response_item':
            continue
        payload = item.get('payload', {})
        kind = payload.get('type')
        if kind in ['custom_tool_call', 'function_call']:
            name = payload.get('name', '')
            code = payload.get('input', payload.get('arguments', ''))
            if name in ['list_agents', 'wait_agent', 'send_message', 'followup_task', 'spawn_agent']:
                status.append(name)
            call = dict(name=name, call_id=payload.get('call_id'), input=code)
            body = call_body(code)
            call_id = call['call_id']
            approved = boundary is None and name == 'exec' and body in permitted_calls
            if not call_id or call_id in recorded_calls:
                unknown.append(dict(call, trace_error='Missing or duplicate call ID'))
                approved = False
            recorded_calls[call_id] = dict(approved_read=approved,
                expected_value=permitted_calls.get(body) if approved else None)
            if boundary is None:
                if name == 'exec' and body.startswith(WRITE_MARKER):
                    boundary = call
                else:
                    calls.append(call)
                    if name != 'exec' or body not in permitted_calls:
                        unknown.append(call)
            else:
                post_calls.append(call)
        elif kind in ['custom_tool_call_output', 'function_call_output']:
            call_id = payload.get('call_id')
            source = recorded_calls.get(call_id)
            if source is None:
                unmatched.append(dict(call_id=call_id, before_boundary=boundary is None))
            outputs.append(dict(before_boundary=boundary is None, call_id=call_id,
                approved_read=bool(source and source['approved_read']),
                expected_value=source['expected_value'] if source else None,
                value=payload.get('output', '')))
    return outputs, calls, unknown, status, boundary, post_calls, unmatched


def walk_visible(value, approved, found, unexpected, expected=None, fragments=None):
    """Stop at approved objects, including any packet-like nested original fields."""
    if isinstance(value, (dict, list)):
        canonical = base.canonical(value)
        if canonical in approved:
            found.add(canonical)
            return
    if isinstance(value, dict):
        if ('entries' in value and 'reader_role' in value) or (
            all(key in value for key in ['id', 'question_entry', 'key_entry'])
            and any(key in value for key in ['reader_a_entry', 'reader_b_entry'])):
            unexpected.append(value)
            return
        for child in value.values():
            walk_visible(child, approved, found, unexpected, expected, fragments)
    elif isinstance(value, list):
        for child in value:
            walk_visible(child, approved, found, unexpected, expected, fragments)
    elif isinstance(value, str):
        # A known read may be truncated inside its original opaque fields.
        # Ignore only an exact serialized prefix of THAT call's expected value;
        # leave it uncredited and still examine material after the warning.
        warning = '\nWarning: truncated output'
        if expected is not None and warning in value:
            fragment, _, tail = value.partition(warning)
            candidate = fragment.strip()
            serializations = [json.dumps(expected, ensure_ascii=ascii_mode) for ascii_mode in [False, True]]
            if candidate and any(s.startswith(candidate) and s != candidate for s in serializations):
                if fragments is not None:
                    fragments.append(dict(prefix_characters=len(candidate)))
                walk_visible(tail, approved, found, unexpected, None, fragments)
                return
        # Parse maximal objects and then recurse; never independently scan the
        # nested text of an already approved original entry or source chunk.
        for child in base.decoded_objects(value):
            walk_visible(child, approved, found, unexpected, expected, fragments)


def frozen_packets(run, role):
    target = run / f'grading-reader-{role}'
    manifest = base.read(target / 'packet-manifest.json')
    assert manifest['reader_role'] == f'reader-{role}'
    for path, expected in manifest['input_hashes'].items():
        assert sha(Path(path)) == expected, 'Frozen input differs: ' + path
    originals = base.read(run / f'reader-{role}.json')['answers']
    ids = [entry['id'] for entry in originals]
    assert ids == manifest['exact_disjoint_ids'] and len(ids) == len(set(ids))
    by_id = {entry['id']: entry for entry in originals}
    assigned, packets = [], []
    for block in manifest['blocks']:
        folder = target / block['block_id']
        packet_path = folder / 'packet.json'
        assert sha(packet_path) == block['packet_sha256'], 'Frozen packet differs'
        packet = base.read(packet_path)
        assert packet['reader_role'] == f'reader-{role}' and packet['block_id'] == block['block_id']
        assert packet['summary_path'] == str(run / 'summary-snapshot.md')
        assert packet['summary_sha256'] == sha(run / 'summary-snapshot.md')
        assert [entry['id'] for entry in packet['entries']] == block['ids']
        for entry in packet['entries']:
            original = by_id[entry['id']]
            assert entry[f'reader_{role}_entry'] == original
            assert hashlib.sha256(base.canonical(original).encode()).hexdigest() == block['complete_raw_entry_sha256s'][entry['id']]
            assert f'reader_{"b" if role == "a" else "a"}_entry' not in entry
        assigned += block['ids']
        packets.append((folder, packet))
    assert assigned == ids
    return manifest, packets


def prove(bank_name, iteration, role, prefix, output_name=None):
    if role not in ['a', 'b']:
        raise ValueError('Expected role a or b')
    run = ROOT / bank_name / iteration
    manifest, packets = frozen_packets(run, role)
    records = base.read(ROOT / 'model-provenance.json')['records']
    summary_path = run / 'summary-snapshot.md'
    lines = physical_lines(summary_path.read_text())
    chunks = []
    for start in range(0, len(lines), 45):
        text = ''.join(lines[start:start + 45])
        chunks.append(dict(qa_delivery='summary-chunk-v1', start_line=start + 1,
            end_line=min(start + 45, len(lines)), text=text,
            sha256=hashlib.sha256(text.encode()).hexdigest()))
    result = {}
    for folder, packet in packets:
        actor = f'/root/{prefix}_{folder.name.replace("block-", "")}'
        record = next(x for x in records if x['agent'] == actor)
        metadata = {key: value for key, value in packet.items() if key != 'entries'}
        approved_values = chunks + [metadata] + packet['entries']
        approved = {base.canonical(value) for value in approved_values}
        permitted = {read_call(summary_path, folder / 'packet.json', 'summary', chunk['start_line'] - 1): chunk for chunk in chunks}
        permitted[read_call(summary_path, folder / 'packet.json', 'metadata', 0)] = metadata
        permitted.update({read_call(summary_path, folder / 'packet.json', 'entry', n): entry for n, entry in enumerate(packet['entries'])})
        outputs, calls, unknown, status, boundary, post_calls, unmatched = session_delivery(record, permitted)
        found, extra_initial, extra_all, fragments = set(), [], [], []
        for output in outputs:
            visible, unexpected = set(), []
            expected = output['expected_value'] if output['approved_read'] else None
            walk_visible(output['value'], approved, visible, unexpected, expected, fragments)
            if output['before_boundary']:
                if output['approved_read'] and base.canonical(expected) in visible:
                    found.add(base.canonical(expected))
                extra_initial += unexpected
            extra_all += unexpected
        chunk_checks = {str(chunk['start_line']): base.canonical(chunk) in found for chunk in chunks}
        entry_checks = {entry['id']: base.canonical(entry) in found for entry in packet['entries']}
        metadata_seen = base.canonical(metadata) in found
        complete = (all(chunk_checks.values()) and all(entry_checks.values()) and metadata_seen
            and boundary is not None and not unknown and not status and not extra_all and not unmatched)
        result[folder.name] = dict(actor=actor, runtime_source=record['runtime_source'],
            frozen_input_packet_and_original_role_binding_confirmed=True,
            packet_sha256=sha(folder / 'packet.json'), complete_summary_chunk_checks=chunk_checks,
            complete_packet_entry_checks=entry_checks, complete_grading_metadata_delivered=metadata_seen,
            unapproved_pre_boundary_tool_calls=unknown, status_or_other_agent_calls=status,
            unmatched_tool_outputs=unmatched, ignored_consistent_transport_fragments=fragments,
            unexpected_packet_shaped_inputs=extra_all, initial_unexpected_packet_shaped_inputs=extra_initial,
            first_possible_artifact_write_boundary=boundary, read_calls=calls,
            post_boundary_tool_calls_for_separate_protocol_audit=post_calls,
            complete_input_delivery_confirmed=complete,
            limits='Exact frozen initial input delivery before a declared first possible mutation, with only whitelisted read-only calls before it. Later arbitrary write code still requires separate permitted-path/isolation audit. Content grades are separate.')
    assert set(result) == {block['block_id'] for block in manifest['blocks']}
    out = run / (output_name or f'grading-reader-{role}-input-delivery-proof.json')
    with out.open('x') as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    return {name: {key: value for key, value in item.items() if key not in [
        'read_calls', 'runtime_source', 'first_possible_artifact_write_boundary',
        'post_boundary_tool_calls_for_separate_protocol_audit']} for name, item in result.items()}


if __name__ == '__main__':
    print(json.dumps(prove(*sys.argv[1:]), indent=2))
