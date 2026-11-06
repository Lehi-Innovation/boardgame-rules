from pathlib import Path
import json, re, hashlib

q = Path(__file__).resolve().parent

def normalized(text):
    for _ in range(3):
        old = text
        text = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m[1], 16)), text)
        text = text.replace(r'\n', '\n').replace(r'\r', '\r').replace(r'\t', '\t').replace(r'\"', '"').replace('\\\\', '\\')
        # Nested tool-output JSON may leave one escape before a decoded newline.
        text = text.replace(chr(92) + chr(10), chr(10))
        if old == text:
            break
    return text

for m in json.loads((q / 'model-provenance.json').read_text()):
    match = re.fullmatch(r'expanded(\d+)_full_grader', m['agent_path'].split('/')[-1])
    if not match:
        continue
    d = q / ('expanded-iteration-' + match[1])
    calls, reads = {}, []
    for line in Path(m['session_path']).open():
        p = json.loads(line).get('payload', {})
        typ = p.get('type')
        if typ in ['custom_tool_call', 'function_call']:
            calls[p.get('call_id', p.get('id'))] = str(p.get('input', p.get('arguments', '')))
        if typ not in ['custom_tool_call_output', 'function_call_output']:
            continue
        code = calls.get(p.get('call_id'), '')
        output = p.get('output', '')
        if isinstance(output, list):
            output = '\n'.join(x.get('text', '') for x in output if isinstance(x, dict))
        else:
            output = str(output)
        if not any(x in code for x in ['cat ', 'tail ', 'head ', 'sed ', 'nl -', 'print(']):
            continue
        if 'write_text' in code or 'json.dump(' in code or 'independent-full-grading.json' in code:
            continue
        reads.append({'input': code, 'visible_output': output, 'truncated': 'truncated output' in output.lower()})
    checks = []
    summary = d / 'summary-snapshot.md'
    visible = normalized('\n'.join(x['visible_output'] for x in reads if summary.name in x['input']))
    missing = [i for i, line in enumerate(summary.read_text().splitlines(), 1) if line.strip() and line not in visible]
    checks.append({'file': str(summary), 'missing_nonempty_lines': missing, 'complete_visible': not missing})
    benchmark = q / json.loads((d / 'input-manifest.json').read_text())['benchmark']
    for f, array, fields in [(benchmark / 'questions.json', 'questions', ['question']), (benchmark / 'answer-key.json', 'answers', ['expected_answer'])] + [(d / ('reader-' + r + '.json'), 'answers', ['answer', 'evidence']) for r in 'ab']:
        visible = normalized('\n'.join(x['visible_output'] for x in reads if f.name in x['input']))
        data = json.loads(f.read_text())[array]
        absent = []
        for item in data:
            for field in fields:
                value = item[field]
                if isinstance(value, (dict, list)):
                    value = json.dumps(value, ensure_ascii=False)
                if normalized(str(value)) not in visible:
                    absent.append({'id': item['id'], 'field': field})
        checks.append({'file': str(f), 'sha256': hashlib.sha256(f.read_bytes()).hexdigest(), 'entry_count': len(data), 'missing_fields': absent, 'complete_visible': not absent})
    report = {'agent': m['agent_path'], 'session': m['session_path'], 'checks': checks, 'all_summary_questions_key_rulings_and_both_answers_evidence_visible': all(x['complete_visible'] for x in checks), 'read_records': reads, 'method': 'Actual model-visible reads, JSON-escape-normalized complete nonempty summary lines and full question/expected-answer/reader-answer/evidence strings. Own report writes, report validation and hash-only reads excluded. No completeness inferred merely from claimed ranges or hashes.'}
    (d / 'independent-grader-input-read-integrity.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print({'grader': m['agent_path'], 'complete': report['all_summary_questions_key_rulings_and_both_answers_evidence_visible'], 'missing': [{k: v for k, v in x.items() if k in ['file', 'missing_nonempty_lines', 'missing_fields']} for x in checks if not x['complete_visible']]})
