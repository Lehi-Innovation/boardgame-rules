"""Record structural literal-span checks only, never gameplay assessments."""
from pathlib import Path
import hashlib
import json
import sys

R = Path(__file__).parent.resolve()
IT = (R / sys.argv[1]).resolve()
assert IT.is_relative_to(R)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())
manifest = read(IT / 'input-manifest-final.json')
method = IT / 'generic-method-code.py'
assert sha(method) == manifest['generic_code_sha256']
namespace = {}
exec(compile(method.read_text(), str(method), 'exec'), namespace)
questions = read(IT / 'questions.json')
out = IT / 'clause-binding-diagnostics'
out.mkdir(exist_ok=True)
new = []
for label in 'ab':
    for path in sorted(IT.glob(f'reader-{label}-batch-[0-9][0-9].json')):
        batch = int(path.stem.rsplit('-', 1)[1])
        destination = out / f'{label}-{batch:02}.json'
        if destination.exists():
            assert read(destination)['snapshot_sha256'] == sha(path)
            continue
        doc = read(path)
        diagnostic = None
        try:
            namespace['validate_clause_bindings'](questions, doc['answers'],
                                                  complete=len(doc['answers']) == len(questions['questions']))
        except (ValueError, KeyError, TypeError) as error:
            diagnostic = str(error)
        result = {'reader': label, 'batch': batch, 'snapshot_path': str(path),
                  'snapshot_sha256': sha(path), 'method_sha256': sha(method),
                  'completed_records': len(doc['answers']),
                  'structural_literal_span_pass': diagnostic is None,
                  'diagnostic': diagnostic, 'gameplay_graded': False,
                  'coverage_or_correctness_certified': False,
                  'factual_grade_cap_applied': False}
        destination.write_text(json.dumps(result, indent=2) + '\n')
        new.append({k: result[k] for k in ['reader', 'batch', 'completed_records', 'structural_literal_span_pass']})
print(json.dumps(new))
