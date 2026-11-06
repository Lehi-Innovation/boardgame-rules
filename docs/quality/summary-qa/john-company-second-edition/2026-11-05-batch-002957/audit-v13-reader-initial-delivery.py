"""Actual initial-call inspection, not a semantic grader or hostile-code proof."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import re
import shlex

ROOT = Path(__file__).resolve().parent
RUN = ROOT / 'expanded-v13-complete-requested-scope/luna-iteration-01'
SUMMARY, QUESTIONS = RUN / 'summary-snapshot.md', RUN / 'questions.json'
LINES = SUMMARY.read_text().splitlines(keepends=True)
QMAP = {q['id']: q for q in json.loads(QUESTIONS.read_text())['questions']}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_values(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from text_values(item)
    elif isinstance(value, dict) and isinstance(value.get('text'), str):
        yield value['text']


def question_objects(value):
    if isinstance(value, dict):
        if set(value) == {'id', 'question'}:
            yield value
        else:
            for item in value.values():
                yield from question_objects(item)
    elif isinstance(value, list):
        for item in value:
            yield from question_objects(item)


results = {}
for record in json.loads((RUN / 'dispatch-runtime-provenance.json').read_text())['records']:
    if 'blind_reader' not in record['agent']:
        continue
    calls, outputs, contexts = [], {}, []
    for line in Path(record['runtime_source']).open():
        event = json.loads(line)
        payload = event.get('payload', {})
        if event.get('type') == 'turn_context':
            contexts.append({k: payload.get(k) for k in ['model', 'effort']})
        if event.get('type') != 'response_item':
            continue
        kind = payload.get('type')
        if kind in ['custom_tool_call', 'function_call']:
            calls.append(payload)
        elif kind in ['custom_tool_call_output', 'function_call_output']:
            outputs[payload['call_id']] = list(text_values(payload.get('output')))
    covered, seen, audited, chunks, deviations = set(), {}, [], [], []
    for call in calls:
        cid = call['call_id']
        assert call['name'] == 'exec', ('foreign initial tool', cid)
        code = call.get('input', call.get('arguments', ''))
        match = re.search(r'(?<![A-Za-z_])(?:"cmd"|cmd)\s*:\s*("(?:[^"\\]|\\.)*")', code)
        assert match, ('unparsed command', cid)
        args = shlex.split(json.loads(match.group(1)))
        assert len(args) == 3 and args[:2] == ['python3', '-c'], ('shell program', cid)
        body, out = args[2], outputs.get(cid, [])
        tree = ast.parse(body)
        assert not any(isinstance(n, (ast.FunctionDef, ast.Lambda, ast.With, ast.For,
                                     ast.While, ast.Delete, ast.AugAssign)) for n in ast.walk(tree)), cid
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert node.module == 'pathlib' and all(a.name == 'Path' for a in node.names), cid
            elif isinstance(node, ast.Import):
                assert all(a.name == 'json' for a in node.names), cid
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    assert node.func.id in ['Path', 'print', 'len', 'isinstance'], (cid, node.func.id)
                else:
                    assert isinstance(node.func, ast.Attribute) and node.func.attr in [
                        'read_text', 'splitlines', 'join', 'loads', 'dumps'], (cid, ast.dump(node.func))
        paths = [node.args[0].value for node in ast.walk(tree) if isinstance(node, ast.Call)
                 and isinstance(node.func, ast.Name) and node.func.id == 'Path']
        assert len(paths) == 1 and paths[0] in [str(SUMMARY), str(QUESTIONS)], (cid, paths)
        audited.append(dict(call_id=cid, program_sha256=hashlib.sha256(body.encode()).hexdigest(),
                            path=paths[0], actual_readonly_program_inspected=True))
        if paths[0] == str(SUMMARY):
            slices = [node.slice for node in ast.walk(tree) if isinstance(node, ast.Subscript)
                      and isinstance(node.slice, ast.Slice)]
            assert len(slices) == 1, ('source slices', cid)
            span = slices[0]
            start = span.lower.value if span.lower else 0
            requested_end = span.upper.value if span.upper else len(LINES)
            assert 0 <= start <= requested_end and requested_end - start <= 45, ('bounds', cid)
            end = min(requested_end, len(LINES))
            if start >= len(LINES):
                deviations.append(dict(call_id=cid, kind='harmless empty EOF probe',
                                       requested_start=start, requested_end=requested_end))
                continue
            expected = ''.join(LINES[start:end])
            exact = expected in out
            chunks.append(dict(call_id=cid, start_line=start + 1, end_line=end,
                               exact_whole_visible_chunk_match=exact,
                               sha256=hashlib.sha256(expected.encode()).hexdigest()))
            if exact:
                covered.update(range(start, end))
        else:
            objects = []
            for text in out:
                raw = text.lstrip()
                try:
                    value, pos = json.JSONDecoder().raw_decode(raw)
                except ValueError:
                    continue
                tail = raw[pos:].strip()
                assert not tail or tail == 'COUNT 116 FINAL_ID Q116', ('unexpected trailing text', cid)
                objects.extend(question_objects(value))
            if len(objects) > 6:
                deviations.append(dict(call_id=cid, kind='oversized attempt excluded', count=len(objects)))
            else:
                for question in objects:
                    assert QMAP.get(question['id']) == question, ('question value mismatch', cid)
                    seen.setdefault(question['id'], []).append(cid)
            if any('truncated' in text.lower() for text in out):
                deviations.append(dict(call_id=cid, kind='truncated attempt excluded; bounded recovery required'))
            if 'd[:6] if isinstance(d,list) else d' in body:
                deviations.append(dict(call_id=cid, kind='unbounded whole-object attempt; excluded from proof'))
        if len(covered) == len(LINES) and set(seen) == set(QMAP):
            break
    assert len(covered) == len(LINES) and set(seen) == set(QMAP), (record['agent'], len(covered), len(seen))
    assert contexts and all(c == dict(model='gpt-6-luna', effort='high') for c in contexts)
    results[record['agent']] = dict(runtime_source=record['runtime_source'],
        initial_calls_audited=audited, all_initial_programs_readonly_two_exact_files=True,
        complete_exact_source_chunks=chunks, all_summary_lines_delivered=len(covered),
        expected_summary_lines=len(LINES), complete_original_question_objects=seen,
        delivery_complete_at_call_id=audited[-1]['call_id'],
        full_delivery_before_any_possible_write_in_actual_audited_prefix=True,
        deviations_and_recovery=deviations, all_observed_contexts=contexts)

report = dict(verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    summary_sha256=sha(SUMMARY), questions_sha256=sha(QUESTIONS), readers=results,
    method='Exact whole source-chunk equality in actual call-ID outputs, including blank lines and whitespace. Complete question-object JSON equality in bounded groups. Actual initial programs inspected as readonly two-file reads and printing.',
    parent_parser_corrections='Two earlier parent attempts stopped without writing any report: valid JSON plus COUNT tail and an empty EOF probe needed explicit handling. No raw inputs or reader answers changed.',
    limits='Initial delivery and readonly prefix only. Attention, later behavior, completion, final settings and semantic correctness remain separate. This inspects actual calls; it is not a general hostile-code security proof.')
with (RUN / 'reader-initial-exact-delivery-audit.json').open('x') as handle:
    json.dump(report, handle, ensure_ascii=False, indent=2)
    handle.write('\n')
print(json.dumps({role: dict(summary_lines=value['all_summary_lines_delivered'],
    exact_questions=len(value['complete_original_question_objects']),
    readonly_calls=len(value['initial_calls_audited'])) for role, value in results.items()}))
