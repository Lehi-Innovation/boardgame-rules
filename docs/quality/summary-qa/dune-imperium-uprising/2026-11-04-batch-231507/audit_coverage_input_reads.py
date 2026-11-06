from pathlib import Path
import json, re, hashlib

q = Path(__file__).resolve().parent
metadata = json.loads((q / 'model-provenance.json').read_text())

def normalize(text):
    # Flatten nested JSON string escaping before decoding Unicode escapes.
    # Decoding Unicode first leaves a stray backslash before curly punctuation.
    for _ in range(8):
        old = text
        text = text.replace('\\\\', '\\').replace(r'\"', '"')
        text = text.replace(r'\n', '\n').replace(r'\r', '\r').replace(r'\t', '\t')
        if old == text:
            break
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m[1], 16)), text)

reports = []
for m in metadata:
    name = m['agent_path'].split('/')[-1]
    if not name.startswith('coverage_final_independent_v'):
        continue
    version = name.rsplit('_', 1)[1]
    bank = q / ('benchmark-' + version)
    calls, reads = {}, []
    for line in Path(m['session_path']).open():
        p = json.loads(line).get('payload', {})
        typ = p.get('type')
        if typ in ['custom_tool_call', 'function_call']:
            calls[p.get('call_id', p.get('id'))] = str(p.get('input', p.get('arguments', '')))
        if typ not in ['custom_tool_call_output', 'function_call_output']:
            continue
        code = calls.get(p.get('call_id'), '')
        out = p.get('output', '')
        if isinstance(out, list):
            out = '\n'.join(x.get('text', '') for x in out if isinstance(x, dict))
        else:
            out = str(out)
        if not any(x in code for x in ['cat ', 'tail ', 'head ', 'sed ', 'nl -', 'print(']):
            continue
        if 'write_text' in code or 'json.dump(' in code:
            continue
        reads.append({'input': code, 'visible_output': out, 'truncated': 'truncated output' in out.lower()})
    checks = []
    files = [Path('/home/jonny/projects/boardgame-rules/extracted/dune-imperium-uprising-rules.txt')]
    files += [q / f for f in ['dune-imperium-uprising-rules.txt', 'dune-imperium-uprising-supplements.txt', 'dune-imperium-official-faq-2025-01-13.txt']]
    if int(version[1:]) >= 14:
        files += [q / 'shaddam-original-2023-leader-transcription.txt', q / 'shaddam-source-origin-metadata.json']
    for f in files:
        identifier = 'extracted/' + f.name if f.parent.name == 'extracted' else f.name
        visible = normalize('\n'.join(x['visible_output'] for x in reads if identifier in x['input']))
        missing = [i for i, line in enumerate(f.read_text().splitlines(), 1) if line.strip() and line not in visible]
        checks.append({'path': str(f), 'sha256': hashlib.sha256(f.read_bytes()).hexdigest(), 'missing_nonempty_lines': missing, 'complete_visible': not missing})
    for file, field, textfield in [('questions.json', 'questions', 'question'), ('answer-key.json', 'answers', 'expected_answer')]:
        visible = normalize('\n'.join(x['visible_output'] for x in reads if file in x['input']))
        entries = json.loads((bank / file).read_text())[field]
        missing = [x['id'] for x in entries if x[textfield] not in visible]
        checks.append({'path': str(bank / file), 'entry_count': len(entries), 'missing_entry_texts': missing, 'complete_visible': not missing})
    report = {'agent': m['agent_path'], 'session': m['session_path'], 'files': checks, 'all_authorized_sources_and_bank_key_visible': all(x['complete_visible'] for x in checks), 'read_records': reads, 'method': 'JSON-escape-normalized exact nonempty source-line and full question/expected-answer matching in actual model-visible read outputs. Report writes and hash-only commands excluded. This checks observable completeness, not an inference from claimed ranges.'}
    (bank / 'coverage-input-read-integrity.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    reports.append({k: v for k, v in report.items() if k != 'read_records'})
(q / 'coverage-input-read-integrity.json').write_text(json.dumps(reports, indent=2, ensure_ascii=False) + '\n')
print([{x['agent']: x['all_authorized_sources_and_bank_key_visible']} for x in reports])
