"""Rebind terminal reader receipt evidence to original records without copying contexts."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
IT = REPO / 'docs/quality/summary-qa/john-company-second-edition' / BASE.name / 'expanded-v13-complete-requested-scope/luna-final-stamped-iteration-01'
AUDIT = IT / 'full-reader-method-audit-01/terminal-final-method-supplement-01'
H = lambda value: hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()
load = lambda path: json.loads(path.read_text())
summary = (IT / 'summary-snapshot.md').read_text()
lines = summary.splitlines(keepends=True)
questions = load(IT / 'questions.json')['questions']
ids = [q['id'] for q in questions]
assert len(ids) == len(set(ids)) == 116
assert (IT / 'summary-snapshot.md').read_bytes() == (REPO / 'rules/john-company-second-edition.md').read_bytes()


def texts(value):
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [x.get('text', '') for x in value if isinstance(x, dict) and x.get('type') in ('input_text', 'text')]
    return []


def contains_question(value, question):
    for match in re.finditer(r'[\[{]', value):
        try:
            decoded = json.JSONDecoder().raw_decode(value[match.start():])[0]
        except ValueError:
            continue
        pending = [decoded]
        while pending:
            item = pending.pop()
            if item == question:
                return True
            if isinstance(item, dict):
                pending.extend(item.values())
            elif isinstance(item, list):
                pending.extend(item)
    return False


proof = {'at_utc': datetime.now(timezone.utc).isoformat(), 'summary_sha256': H(summary),
         'question_count': len(ids), 'readers': [], 'private_contexts_retained': False}
for role in ('a', 'b'):
    folder = AUDIT / f'final-{role}'
    evidence_path = folder / f'reader-{role}-method-evidence.json'
    evidence = load(evidence_path)
    admission = load(folder / 'admission.json')
    binding = evidence['runtime_read_binding']
    with Path(binding['path']).open('rb') as stream:
        original = stream.read(binding['snapshot_bytes'])
    assert H(original) == binding['snapshot_sha256']
    records = original.splitlines(keepends=True)
    bound = load(folder / f'reader-{role}-physical-record-bindings.json')
    assert len(records) == binding['complete_physical_records']
    # The saved narrow ledger deliberately omits private body records. The full
    # prefix hash binds them without copying or displaying their contents.
    runtime = {n: json.loads(raw) for n, raw in enumerate(records, 1)}
    bound_ordinals = set()
    for item in bound:
        ordinal = item['ordinal']
        raw = records[ordinal - 1]
        assert ordinal not in bound_ordinals and item['bytes'] == len(raw) and item['sha256'] == H(raw)
        bound_ordinals.add(ordinal)
    calls, visible = {}, {}
    for call in evidence['tool_call_records']:
        ordinal = call['ordinal']
        assert ordinal in bound_ordinals
        raw = runtime[ordinal]
        payload = raw['payload']
        assert raw['type'] == 'response_item' and payload['call_id'] == call['call_id'] and payload['name'] == call['name']
        code = payload.get('input', payload.get('arguments'))
        assert H(code) == call['input_sha256'] and len(code) == call['input_chars']
        calls[ordinal] = call
        if call.get('output_ordinal') is None:
            continue
        output = runtime[call['output_ordinal']]
        assert call['output_ordinal'] in bound_ordinals
        assert output['type'] == 'response_item' and output['payload']['call_id'] == payload['call_id']
        blocks = texts(output['payload']['output'])
        assert H(json.dumps(blocks, ensure_ascii=False, sort_keys=True, separators=(',', ':'))) == call['visible_output_sha256']
        assert sum(map(len, blocks)) == call['visible_output_chars']
        visible[ordinal] = ''.join(blocks)
    contexts = [(r['payload'].get('model'), r['payload'].get('effort')) for r in runtime.values() if r['type'] == 'turn_context']
    assert contexts and all(c == ('gpt-6-luna', 'high') for c in contexts)
    seen = set()
    first_composition = min(m['composition_call_ordinal'] for m in evidence['per_entry_method_records'])

    def verify_span(span, boundary):
        ordinal = span['call_ordinal']
        assert ordinal < span['output_ordinal'] < boundary
        assert calls[ordinal]['output_ordinal'] == span['output_ordinal']
        left, right = span['start_line'], span['end_line']
        literal = ''.join(lines[left - 1:right])
        assert H(literal) == span['slice_sha256'] and literal in visible[ordinal]
        assert span['start_offset'] == sum(map(len, lines[:left - 1]))
        assert span['end_offset'] == span['start_offset'] + len(literal)
        return set(range(left, right + 1))

    for span in evidence['initial_summary_receipts']:
        seen.update(verify_span(span, first_composition))
    assert all(i in seen or not line.strip() for i, line in enumerate(lines, 1))
    methods = evidence['per_entry_method_records']
    assert [m['id'] for m in methods] == ids
    unit_count = span_count = 0
    for question, method in zip(questions, methods):
        boundary = method['composition_call_ordinal']
        assert boundary in calls and method['question_sha256'] == H(question['question'])
        qcalls = method['exact_question_reread_call_ordinals']
        assert qcalls and all(q < calls[q]['output_ordinal'] < boundary and contains_question(visible[q], question) for q in qcalls)
        for unit in method['source_units']:
            receipt = unit['actual_individual_work_receipt']
            assert receipt['complete']
            unit_lines = set(range(unit['start_line'], unit['end_line'] + 1))
            assert H(''.join(lines[unit['start_line'] - 1:unit['end_line']])) == unit['slice_sha256']
            delivered = set()
            for span in receipt['spans']:
                delivered.update(verify_span(span, boundary))
                span_count += 1
            assert unit_lines <= delivered
            unit_count += 1
    raw = load(IT / f'reader-{role}.json')
    assert [a['id'] for a in raw['answers']] == ids
    assert admission['qualified_full116_response_grading_admitted'] and admission['root_original_whole_task_terminal_confirmed']
    for name, item in admission['terminal_raw_file_bindings'].items():
        assert item['matches'] and item['actual_sha256'] == item['replay_sha256'] == H((IT / name).read_bytes())
    assert admission['final_answer_count'] == admission['final_source_record_count'] == 116
    assert admission['final_suffix_individual_question_and_bounded_unit_receipt_verified']
    proof['readers'].append({'role': role, 'runtime_path': binding['path'], 'runtime_prefix_sha256': binding['snapshot_sha256'],
        'physical_records_rebound': len(records), 'tool_calls_rebound': len(calls), 'model_contexts': len(contexts),
        'complete_initial_summary_before_composition': True, 'complete_question_objects_before_each_composition': len(methods),
        'complete_selected_units_before_composition': unit_count, 'literal_source_spans_before_composition': span_count,
        'final_raw_sha256': H((IT / f'reader-{role}.json').read_bytes()), 'method_evidence_sha256': H(evidence_path.read_bytes()),
        'qualified_not_clean_method': True, 'retained_method_qualifications': admission['historical_qualifications_retained']})
proof.update(verified=True, limits='Original physical record hashes, complete literal model-visible question/source receipts and frozen raw bindings. No gameplay grade, source-completeness verdict or publication approval. Method timing, batching and format deviations remain disclosed. Fresh spawn/model and source-only mechanical replay are separately evidenced.')
out = BASE / 'coordinator-checks/john-stamped-i1-actual-reader-inputs.json'
assert not out.exists()
out.write_text(json.dumps(proof, indent=2) + '\n')
print(json.dumps({'verified': True, 'readers': len(proof['readers']), 'records': sum(r['physical_records_rebound'] for r in proof['readers']), 'proof': str(out)}))
