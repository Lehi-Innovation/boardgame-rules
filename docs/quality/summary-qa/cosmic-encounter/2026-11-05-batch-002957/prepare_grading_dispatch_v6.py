"""Prepare fresh strict graders only after the full raw pair and referent checks."""
from pathlib import Path
import hashlib
import json
import sys

R = Path(__file__).parent.resolve()
IT = (R / sys.argv[1]).resolve()
assert IT.is_relative_to(R)
iteration_number = int(IT.name.rsplit('-', 1)[1])
assert not (IT / 'grading-dispatch-plan.json').exists()


def read(p):
    return json.loads(p.read_bytes())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


expected = [q['id'] for q in read(IT / 'questions.json')['questions']]
assert len(expected) == read(IT / 'input-manifest-final.json')['question_count']
history=read(IT / 'staged-history-validation-01.json')
assert history['pass']
delivery=read(IT / 'delivery-validation-v6.json')
assert delivery['pass']
for c in 'ab':
    delivered=next(x for x in delivery['readers'] if x['reader']==c)
    assert delivered['raw_output_sha256']==sha(IT / f'reader-{c}.json')
    assert [a['id'] for a in read(IT / f'reader-{c}.json')['answers']] == expected
    final=read(IT / f'reader-{c}.json')
    assert final['stage']=='review_complete' and final['self_review']['complete'] is True
    history_reader=next(x for x in history['readers'] if x['reader']==c)
    terminal=history_reader['effective_terminals']['review']
    assert terminal['sha256']==sha(IT / f'reader-{c}.json')
    assert terminal['original_structure_pass'] or terminal['metadata_resolution_status']=='continuation_metadata_only_resolved'
    assert read(IT / f'reader-{c}-review-payload-validation-01.json')['pass']
assert read(IT / 'staged-history-validation-01.json')['pass']
assert read(IT / 'delivery-validation-v6.json')['pass']
assert read(IT / 'materialized-reference-integrity-validation.json')['pass']
manifest = read(IT / 'grading-inputs-v2/manifest.json')
template = (R / 'full-bank-grader-protocol-template-v4.txt').read_text()
plan = []
for n, block in enumerate(manifest['blocks'], 1):
    tag = f'{n:02}'
    instructions = (template.replace('SUMMARY_PATH', str(IT / 'summary-snapshot.md'))
                    .replace('BUNDLE_PATH', block['path'])
                    .replace('OUTPUT_PATH', str(IT / f'grades-{tag}.json')))
    path = IT / f'grader-{tag}-instructions.txt'
    assert not path.exists()
    path.write_text(instructions)
    request = (f'Read and follow {path} completely. Read its characters0–5800 '
               f'and5800–{len(instructions)} in separate actual tool responses, with hashes; '
               'do not cat the whole process file in one oversized display. Then read the '
               'entire frozen summary and entire assigned materialized packet in actual '
               'contiguous chunks of at most6000characters, and perform the complete '
               'independent assessment. No desired verdict is supplied. Do not open peer '
               'grades, original reader files, repair authoring or primary sources. '
               'Preserve process and data delivery receipts, all raw fields and all same-entry referents.')
    request_path = IT / f'grader-{tag}-request.txt'
    request_path.write_text(request)
    plan.append({'task': f'expanded{iteration_number}_grader_{tag}', 'model': 'gpt-6.1-sol',
                 'reasoning_effort': 'high', 'fork_turns': 'none',
                 'instructions_path': str(path), 'instructions_sha256': sha(path),
                 'request_path': str(request_path), 'request_sha256': sha(request_path),
                 'expected_ids': block['expected_ids'], 'bundle_path': block['path'],
                 'bundle_sha256': block['sha256'], 'output_path': str(IT / f'grades-{tag}.json')})
(IT / 'grading-dispatch-plan.json').write_text(json.dumps({
    'all_original_answers_per_reader_complete_before_any_grading': True, 'question_count': len(expected),
    'all_same_entry_referents_materialized_before_first_grading_dispatch': True,
    'fresh_independent_grader_count': len(plan), 'plan': plan}, indent=2) + '\n')
print('Prepared9 NEW strict graders; no dispatch by this script')
