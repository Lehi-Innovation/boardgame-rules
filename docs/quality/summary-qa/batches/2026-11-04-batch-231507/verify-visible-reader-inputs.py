"""Check actual visible reader tool outputs for every frozen question and summary line.

Use with verify-runtime.py output. This supplements manual review of tool boundaries;
it is not a claim of filesystem isolation or recovery of encrypted task prompts.
"""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('runtime_check', type=Path)
p.add_argument('iteration', type=Path)
a = p.parse_args()
runtime = json.loads(a.runtime_check.read_text())
summary = (a.iteration/'summary-snapshot.md').read_text().splitlines()
questions = json.loads((a.iteration/'questions.json').read_text())['questions']


def visible_text(value):
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except (ValueError, TypeError):
            return [value]
        if isinstance(parsed, dict) and 'output' in parsed:
            return visible_text(parsed['output'])
        return [value]
    if isinstance(value, list):
        return [s for item in value for s in visible_text(item)]
    if isinstance(value, dict) and value.get('type') in ['input_text', 'text']:
        return visible_text(value['text'])
    return []


readers = []
for agent in runtime['agents']:
    contexts = agent['actual_contexts']
    if not all(c['model'] == 'gpt-6-luna' for c in contexts):
        continue
    events = [json.loads(s)['payload'] for s in Path(agent['runtime_path']).read_text().split('\n') if s]
    calls = {e['call_id']: e.get('input', e.get('arguments', '')) for e in events
             if e.get('type') in ['custom_tool_call', 'function_call'] and 'call_id' in e}
    chunks = []
    call_ids = []
    excluded_writers = []
    for event in events:
        if event.get('type') not in ['custom_tool_call_output', 'function_call_output']:
            continue
        call_id = event.get('call_id')
        call = calls.get(call_id, '')
        if any(s in call for s in ['cat >', 'write_text(', 'write_bytes(', 'writeFile', 'apply_patch']):
            excluded_writers.append(call_id)
            continue
        chunks.extend(visible_text(event.get('output', [])))
        call_ids.append(call_id)
    text = '\n'.join(chunks)
    missing_questions = [q['id'] for q in questions
                         if q['question'] not in text
                         and json.dumps(q['question'], ensure_ascii=False)[1:-1] not in text
                         and json.dumps(q['question'], ensure_ascii=True)[1:-1] not in text]
    missing_lines = [i for i, line in enumerate(summary, 1) if line.strip() and line not in text]
    readers.append({'task': agent['task'], 'runtime_path': agent['runtime_path'],
                    'missing_question_ids': missing_questions, 'missing_summary_lines': missing_lines,
                    'all_question_texts_visible': not missing_questions,
                    'all_nonblank_summary_lines_visible': not missing_lines,
                    'examined_output_call_ids': call_ids, 'excluded_writer_call_ids': excluded_writers})
assert len(readers) == 2, 'Pass a runtime check containing exactly the two final readers plus any nonreader auditors'
result = {'iteration': str(a.iteration), 'question_count': len(questions), 'readers': readers,
          'actual_visible_inputs_complete': all(r['all_question_texts_visible'] and
                                               r['all_nonblank_summary_lines_visible'] for r in readers),
          'limit': 'Presence check supplements manual review of actual tool read ranges, truncation, boundary and timing. It does not prove that no other evidence was read.'}
print(json.dumps(result, indent=2))
assert result['actual_visible_inputs_complete'], 'Some frozen input was not found in actual nonwriter tool outputs; investigate rather than claim complete input'
