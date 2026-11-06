"""Coordinator checks of original runtime-bound inputs; never copies private contexts."""
from pathlib import Path
import ast
import hashlib
import json
import re
import shlex
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[4]
RUN = REPO / 'docs/quality/summary-qa/john-company-second-edition' / BASE.name
IT = RUN / 'expanded-v13-complete-requested-scope/luna-iteration-03'
load = lambda p: json.loads(p.read_text())
H = lambda b: hashlib.sha256(b).hexdigest()


def strings(v):
    if isinstance(v, str):
        yield v
    elif isinstance(v, dict):
        for value in v.values():
            yield from strings(value)
    elif isinstance(v, list):
        for value in v:
            yield from strings(value)


def bind_projection(path):
    """Rebind every projected physical record, call and visible output to originals."""
    p = load(path)
    original = Path(p['original_runtime_path']).read_bytes()[:p['prefix_bytes']]
    assert H(original) == p['prefix_sha256']
    lines = original.splitlines(keepends=True)
    bindings = p.get('physical_records', p.get('records'))
    assert len(lines) == len(bindings)
    records = {}
    for n, (line, binding) in enumerate(zip(lines, bindings), 1):
        assert binding['physical_record'] == n
        assert binding['sha256'] == H(line) and binding['bytes'] == len(line)
        records[n] = json.loads(line)
    for c in p['tool_calls']:
        r = records[c['physical_record']]
        assert r['type'] == 'response_item'
        v = r['payload']
        assert v['call_id'] == c['call_id'] and v['name'] == c['name']
        assert v.get('input', v.get('arguments')) == c['input']
    for o in p['tool_outputs']:
        r = records[o['physical_record']]
        assert r['type'] == 'response_item' and r['payload']['call_id'] == o['call_id']
        visible = list(strings(r['payload']['output']))
        projected = o.get('text_blocks', o.get('visible_text_blocks'))
        assert projected and all(s in visible for s in projected)
    return p, len(lines)


def body(o):
    return ''.join(o.get('text_blocks', o.get('visible_text_blocks'))[1:])


def decoder(s):
    try:
        return json.JSONDecoder().raw_decode(s.lstrip())[0]
    except ValueError:
        return None


def question_seen(q, text):
    if q['question'] + '\n' in text:
        return True
    return any(decoder(text[m.start():]) == q for m in re.finditer(r'\{', text))


summary_path = IT / 'summary-snapshot.md'
summary = summary_path.read_text()
source_lines = summary.splitlines(keepends=True)
questions = load(IT / 'questions.json')['questions']
assert len(questions) == 116
assert summary_path.read_bytes() == (REPO / 'rules/john-company-second-edition.md').read_bytes()
report = {'at_utc': datetime.now(timezone.utc).isoformat(), 'summary_sha256': H(summary_path.read_bytes()),
          'readers': [], 'graders': [], 'private_contexts_retained': False}
physical_count = 0

for role in ('a', 'b'):
    folder = IT / f'full-reader-method-audit-01/terminal-{role}-01'
    p, count = bind_projection(folder / f'prefix-reader-{role}-runtime-projection.json')
    physical_count += count
    outputs = {o['physical_record']: body(o) for o in p['tool_outputs']}
    methods = load(folder / f'prefix-reader-{role}-per-entry-method.json')
    assert [m['id'] for m in methods] == [q['id'] for q in questions]
    receipts = 0
    for q, m in zip(questions, methods):
        write = m['first_successful_composition_append_call']
        assert write and m['exact_question_reread_output_records']
        assert all(n < write and question_seen(q, outputs[n])
                   for n in m['exact_question_reread_output_records'])
        for u in m['source_unit_receipts']:
            assert u['complete_receipt'] and not u['missing_physical_lines']
            whole = ''.join(source_lines[u['start_line'] - 1:u['end_line']])
            assert H(whole.encode()) == u['full_unit_sha256']
            covered = set()
            for c in u['exact_received_chunks']:
                n = c['output_record']
                assert n < write
                first, last = c['source_physical_first'], c['source_physical_last']
                literal = ''.join(source_lines[first - 1:last])
                assert H(literal.encode()) == c['exact_slice_sha256']
                assert literal in outputs[n]
                covered.update(range(first, last + 1))
                receipts += 1
            for c in u['numbered_lossless_line_receipts']:
                n = c['output_record']
                assert n < write
                for physical in c['exact_full_LF_lines_after_removing_only_visible_number_prefix']:
                    literal = source_lines[physical - 1]
                    assert f'{physical}:{literal}' in outputs[n] or f'{physical}: {literal}' in outputs[n]
                    covered.add(physical)
            # Parent records blank-line extension beside exact substantive slices.
            for physical in range(u['start_line'], u['end_line'] + 1):
                if physical not in covered:
                    assert not source_lines[physical - 1].strip()
        assert m['source_record_same_entry_alignment']
    terminal = load(folder / 'terminal-assessment.json')
    assert terminal['qualified_full_final_response_fact_grading_admission']
    assert terminal['final_exact_ordered_unique_116_ids']
    report['readers'].append({'role': role, 'original_runtime_sha256': p['prefix_sha256'],
        'physical_records': count, 'questions_reread_before_composition': 116,
        'literal_unit_chunk_receipts_verified': receipts,
        'qualification': 'Original method/format/history qualifications retained; no factual cap.'})

helper = ast.parse((RUN / 'prove-single-reader-grading-delivery-literal-equivalent.py').read_text())
fixed_reader = next(ast.literal_eval(n.value) for n in helper.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'READ_SCRIPT' for t in n.targets))
for role in ('a', 'b'):
    folder = IT / f'grading-reader-{role}-completion-io-audit-01'
    for index in range(1, 7):
        block = f'block-{index:02d}'
        p, count = bind_projection(folder / f'{index:02d}-runtime-projection.json')
        physical_count += count
        checks = load(folder / f'{index:02d}-delivery-checks.json')
        packet_path = IT / f'grading-reader-{role}/{block}/packet.json'
        packet = load(packet_path)
        outputs = {o['physical_record']: o for o in p['tool_outputs']}
        calls = {c['physical_record']: c for c in p['tool_calls']}
        boundary = next(c['physical_record'] for c in p['tool_calls'] if '// QA_ARTIFACT_WRITE_V1' in c['input'])
        summary_seen, entries_seen, metadata_seen = set(), set(), False
        for c in checks['before_first_mutation_records']:
            n = c['output_record']
            assert c['call_record'] < n < boundary
            call = calls[c['call_record']]
            match = re.search(r'(?:"cmd"|cmd)\s*:\s*("(?:\\.|[^"\\])*")(?:\s*\+\s*("(?:\\.|[^"\\])*"))?', call['input'])
            assert match
            command = json.loads(match[1]) + (json.loads(match[2]) if match[2] else '')
            assert H(command.encode()) == c['command_sha256']
            if not c.get('exact_visible_value_equals_original'):
                continue
            args = shlex.split(command)
            assert args[:2] == ['python3', '-c'] and args[2] == fixed_reader
            assert args[3:5] == [str(summary_path), str(packet_path)]
            mode, j = args[5], int(args[6])
            actual = decoder(body(outputs[n]))
            if mode == 'summary':
                literal = ''.join(source_lines[j:j + 45])
                expected = {'qa_delivery': 'summary-chunk-v1', 'start_line': j + 1,
                    'end_line': min(j + 45, len(source_lines)), 'text': literal, 'sha256': H(literal.encode())}
                summary_seen.add(j)
            elif mode == 'entry':
                expected = packet['entries'][j]
                entries_seen.add(j)
            else:
                assert mode == 'metadata'
                expected = {k: v for k, v in packet.items() if k != 'entries'}
                metadata_seen = True
            assert actual == expected
        assert summary_seen == set(range(0, len(source_lines), 45))
        assert entries_seen == set(range(len(packet['entries']))) and metadata_seen
        replay = load(folder / f'{index:02d}-isolated-replay.json')
        grade_path = IT / f'grading-reader-{role}/{block}/grades-same-entry.json'
        assert replay['byte_identical_to_original_report'] and replay['original_report_sha256'] == H(grade_path.read_bytes())
        report['graders'].append({'reader': role, 'block': block, 'physical_records': count,
            'summary_chunks_before_first_mutation': len(summary_seen), 'whole_packet_entries_before_first_mutation': len(entries_seen),
            'metadata_before_first_mutation': True, 'original_strict_false_preserved':
                not load(IT / f'grading-reader-{role}-input-delivery-proof.json')[block]['complete_input_delivery_confirmed'],
            'qualified_extra_call_count': len(checks['unapproved_pre_boundary_calls'] if
                'unapproved_pre_boundary_calls' in checks else checks['unapproved_fixed_reader_failures'])})

report.update(verified=True, total_original_physical_record_bindings=physical_count,
    limits='Actual literal input transport and original record bindings, not another gameplay regrade. '
           'Actual models, semantic grading, source purity and coverage stopping are separately checked. '
           'Original strict false results and technical qualifications remain preserved.')
out = BASE / 'coordinator-checks/john-v13-i3-actual-reader-grader-inputs.json'
assert not out.exists()
out.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'verified': True, 'readers': len(report['readers']), 'graders': len(report['graders']),
                  'original_record_bindings': physical_count, 'report': str(out)}))
