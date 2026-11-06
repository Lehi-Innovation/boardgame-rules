"""Verify actual nonwriter output visibility; retain calls for boundary review."""
import argparse
import hashlib
import json
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('runtime_check', type=Path)
p.add_argument('session_id')
p.add_argument('files', nargs='+', type=Path)
p.add_argument('--semantic-bank', action='store_true')
a = p.parse_args()
agent = next(x for x in json.loads(a.runtime_check.read_text())['agents']
             if x['session_id'] == a.session_id)
ev = [json.loads(s)['payload'] for s in Path(agent['runtime_path']).read_text().split('\n') if s]
calls = {e['call_id']: e for e in ev if e.get('type') in ['custom_tool_call', 'function_call']}

def visible(v):
    if isinstance(v, str):
        try:
            d = json.loads(v)
        except (ValueError, TypeError):
            return [v]
        if isinstance(d, dict) and 'output' in d:
            return visible(d['output'])
        return [v]
    if isinstance(v, list):
        return [s for item in v for s in visible(item)]
    if isinstance(v, dict) and v.get('type') in ['input_text', 'text']:
        return visible(v['text'])
    return []

chunks = []
images = 0
for e in ev:
    if e.get('type') not in ['custom_tool_call_output', 'function_call_output']:
        continue
    call = calls.get(e.get('call_id'), {})
    code = call.get('input', call.get('arguments', ''))
    if any(x in code for x in ['write_text(', 'write_bytes(', 'writeFile', 'cat >', 'apply_patch']):
        continue
    output = e.get('output', [])
    images += json.dumps(output).count('"type": "input_image"')
    chunks.extend(visible(output))
text = '\n'.join(chunks)
out = []
for f in a.files:
    body = f.read_text()
    if a.semantic_bank and f.suffix == '.json' and f.name in ['questions.json', 'answer-key.json']:
        d = json.loads(body)
        items = d.get('questions', d.get('answers', []))
        required = [(x['id'], x.get('question', x.get('expected_answer'))) for x in items]
    else:
        required = list(enumerate(body.splitlines(), 1))
    missing = [i for i, s in required if s and s.strip() and s not in text
               and json.dumps(s, ensure_ascii=False)[1:-1] not in text
               and json.dumps(s, ensure_ascii=True)[1:-1] not in text]
    out.append({'file': str(f.resolve()), 'sha256': hashlib.sha256(f.read_bytes()).hexdigest(),
                'required_units': len(required), 'missing_units': missing})
result = {'session_id': a.session_id, 'task': agent['task'],
          'actual_contexts': agent['actual_contexts'], 'parent_spawn': agent['parent_spawn'],
          'inputs': out, 'actual_returned_image_blocks': images,
          'all_required_text_visible': all(not x['missing_units'] for x in out),
          'calls_for_boundary_review': [e for e in calls.values()],
          'limit': 'Actual output presence, not OS isolation; manually review calls, ranges, and task boundaries.'}
print(json.dumps(result, indent=2))
assert result['all_required_text_visible'], 'Missing actual visible text; investigate.'
