"""Bind saved prompt requests to runtime spawn settings; task bodies are encrypted."""
from pathlib import Path
import hashlib
import json
import sys

R = Path(__file__).parent.resolve()
it = (R / sys.argv[1]).resolve()
assert it.is_relative_to(R)
assert not (it / 'dispatch-bindings.json').exists()
provenance = json.loads((R / 'model-provenance.json').read_text())
root = next(a for a in provenance['agents'] if a['task'] == '/root')
iteration_number = int(it.name.rsplit('-', 1)[1])
active_manifest = json.loads((it / 'input-manifest-final.json').read_text())
requested_tasks = {letter: f'expanded{iteration_number}_reader_{letter}'
                   for letter in ['a', 'b']}
found = {letter: [] for letter in requested_tasks}


def sha(value):
    return hashlib.sha256(value).hexdigest()


for ordinal, raw in enumerate(Path(root['runtime_source_path']).open()):
    row = json.loads(raw)
    p = row.get('payload', {})
    if p.get('type') != 'function_call' or p.get('name') != 'spawn_agent':
        continue
    arguments = p.get('arguments')
    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except ValueError:
            continue
    if not isinstance(arguments, dict):
        continue
    for letter, task in requested_tasks.items():
        if arguments.get('task_name') != task:
            continue
        prompt = Path(active_manifest['active_dispatch_prompt_paths'][letter])
        runtime_message = arguments['message']
        assert arguments['model'] == 'gpt-6-luna'
        assert arguments['reasoning_effort'] == 'high'
        assert arguments['fork_turns'] == 'none'
        found[letter].append({
            'label': letter, 'task': '/root/' + task,
            'output_path': str(it / f'reader-{letter}.json'),
            'prompt_path': str(prompt),
            'submitted_prompt_sha256': sha(prompt.read_bytes()),
            'fork_turns': 'none', 'requested_model': arguments['model'],
            'requested_effort': arguments['reasoning_effort'],
            'actual_parent_spawn_settings_verified': True,
            'actual_prompt_plaintext_comparison': None,
            'request_proof': {
                'runtime_source_path': root['runtime_source_path'],
                'record_ordinal': row.get('ordinal', ordinal),
                'record_sha256': sha(raw.encode()),
                'runtime_message_characters': len(runtime_message),
                'saved_literal_characters': len(prompt.read_text()),
                'saved_literal_equals_actual_spawn_message': None,
            },
            'runtime_fork_context_field': None,
            'limit': 'Parent requested task/fork/model/effort are verified from '
                     'actual function-call arguments. The runtime task message is '
                     'encrypted, so its plaintext cannot be independently compared '
                     'with the saved literal prompt. Child actual model/effort and '
                     'input payloads are checked separately. No encrypted task '
                     'body, hidden instructions or account data copied.',
        })
assert all(len(value) == 1 for value in found.values()), 'Exactly one actual spawn request per fresh reader required'
readers = [found[letter][0] for letter in ['a', 'b']]
normalized = [Path(x['prompt_path']).read_text().replace(x['output_path'], 'OUTPUT_PATH')
              for x in readers]
assert normalized[0] == normalized[1]
report = {'readers': readers, 'saved_submitted_prompts_identical_except_output_path': True,
          'actual_runtime_prompt_plaintext_comparison': None,
          'method': 'Saved literal protocol and actual requested settings/root record bindings. Task-message plaintext is encrypted and unavailable; only opaque whole-record hashes and ordinals are retained.'}
(it / 'dispatch-bindings.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
print('Saved prompts identical apart from output; actual settings/fork requests verified. Runtime message plaintext unavailable.')
