"""Freeze both complete original drafts without inspecting factual content."""
from pathlib import Path
import collections
import hashlib
import json
import shutil
import sys

B = Path(__file__).resolve().parent
D = B / sys.argv[1]
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
load = lambda p: json.loads(p.read_text())
ids = [q['id'] for q in load(D / 'questions.json')['questions']]
assert len(ids) == 173 and len(set(ids)) == len(ids)
rows = []
for r in 'ab':
    raw = D / f'reader-{r}.json'
    data = load(raw)
    assert data['stage'] == 'draft_ready'
    assert collections.Counter(a['id'] for a in data['answers']) == collections.Counter(ids)
    assert data['inputs_read'] and data['method_execution']
    copy = D / f'reader-{r}-original-draft.json'
    receipt = D / f'reader-{r}-original-draft-freeze.json'
    assert not copy.exists() and not receipt.exists()
    rows.append((raw, copy, receipt))
for raw, copy, receipt in rows:
    shutil.copyfile(raw, copy)
    assert raw.read_bytes() == copy.read_bytes()
    receipt.write_text(json.dumps({
        'path': str(raw), 'sha256': H(raw), 'immutable_copy': str(copy),
        'immutable_copy_sha256': H(copy), 'stage': 'draft_ready',
        'answer_count': 173, 'entire_original_fields_preserved': True,
        'parent_factual_diagnostics_not_started': True,
        'this_is_not_a_completed_reader_trial': True,
    }, indent=2) + '\n')
out = {
    'both_full_original_drafts_frozen': True,
    'parent_factual_diagnostics_or_grading_feedback_supplied': False,
    'question_count': 173,
    'drafts': {raw.name: {'sha256': H(copy), 'copy': str(copy), 'receipt': str(receipt)} for raw, copy, receipt in rows},
    'same_stage3_technical_resume_required_for_both_original_actors': True,
    'resampling_or_completed_original_repair': False,
}
p = D / 'both-drafts-technical-checkpoint.json'
assert not p.exists()
p.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out))
