"""Preserve complete selected original inputs for actual parent review."""
from pathlib import Path
import copy
import hashlib
import json

B = Path(__file__).resolve().parent
D = B / 'expanded-iteration-10'
A = D / 'adjudication-01'
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
cases = load(A / 'raw-cases.json')
manifest = load(A / 'input-manifest.json')
assert all(H(Path(p)) == meta['sha256'] for p, meta in manifest['inputs'].items())
ids = {x['id'] for x in cases['requested_cases']}
view = {
    'requested_cases': copy.deepcopy(cases['requested_cases']),
    'readers': copy.deepcopy(cases['readers']),
    'all_original_entry_fields_preserved': True,
    'both_readers_for_every_selected_question': True,
    'no_deduplication_or_quotation_elision': True,
}
for r, value in view['readers'].items():
    original = load(D / (r + '.json'))
    assert H(D / (r + '.json')) == cases['original_raw_output_sha256'][r]
    assert value['answers'] == [x for x in original['answers'] if x['id'] in ids]
    assert {x['id'] for x in value['answers']} == ids
questions = {
    name: load(A / name)
    for name in ['questions.json', 'answer-key.json', 'asked-facts.json']
}
outputs = {
    'parent-selected-complete-original-entries.json': view,
    'parent-complete-questions-key-map-view.json': questions,
}
receipts = []
for name, value in outputs.items():
    p = A / name
    assert not p.exists()
    p.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')
    receipts.append({'path': str(p), 'sha256': H(p), 'characters': len(p.read_text())})
receipt = {
    'inputs': {str(A / n): H(A / n) for n in ['raw-cases.json', 'questions.json', 'answer-key.json', 'asked-facts.json']},
    'outputs': receipts,
    'full_original_entries': sum(len(v['answers']) for v in view['readers'].values()),
    'selected_questions': len(ids),
    'exact_original_objects_preserved': True,
    'actual_parent_delivery_and_semantic_review_pending': True,
}
p = A / 'parent-selected-inputs-preparation.json'
assert not p.exists()
p.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
