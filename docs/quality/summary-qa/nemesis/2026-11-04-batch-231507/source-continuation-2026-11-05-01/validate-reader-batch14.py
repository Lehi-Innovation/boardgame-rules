"""Preserve every submitted batch, including structural failures, without grading."""
from pathlib import Path
import datetime, hashlib, json, sys

R = Path(__file__).resolve().parent
D = R / 'full-iteration-14'
side = sys.argv[1]
assert side in ['a', 'b']

def read(p):
    return json.loads(p.read_text())

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def new(p, value):
    with p.open('x') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')

p = D / ('reader-' + side + '-draft.json')
questions = read(D / 'questions.json')['questions']
ids = [q['id'] for q in questions]
progress_path = D / ('batch-progress-' + side + '.json')
old = read(progress_path) if progress_path.exists() else {'reader': side, 'saved_answer_count': 0, 'batches': []}
folder = D / ('draft-batches-' + side)
folder.mkdir(exist_ok=True)
step = len(old['batches']) + 1
snapshot = folder / ('step-' + str(step).zfill(3) + '.json')
with snapshot.open('xb') as f:
    f.write(p.read_bytes())
deviations = []
try:
    raw = read(snapshot)
    answers = raw['answers']
    actual = [a['id'] for a in answers]
    schema_valid = bool(answers) and all(
        isinstance(a.get('requested_parts'), list) and bool(a['requested_parts'])
        and isinstance(a.get('answer'), str) and isinstance(a.get('evidence'), str)
        and a.get('support') in ['supported', 'partial', 'unsupported']
        for a in answers)
except (ValueError, KeyError, TypeError):
    answers, actual, schema_valid = [], [], False
count = len(actual)
prefix_valid = 1 <= count <= len(ids) and actual == ids[:count]
unique_valid_ids = len(set(actual)) == count and set(actual).issubset(ids)
changes, missing_previous = [], []
if old['batches']:
    prev = old['batches'][-1]
    assert sha(Path(prev['snapshot'])) == prev['sha256']
    before = read(Path(prev['snapshot']))['answers']
    current_by_id = {a['id']: a for a in answers}
    missing_previous = [a['id'] for a in before if a['id'] not in current_by_id]
    changes = [a['id'] for a in before if a['id'] in current_by_id and a != current_by_id[a['id']]]
previous = old['saved_answer_count']
if not schema_valid:
    deviations.append('Submitted output failed the field/schema check; exact bytes preserved.')
if not prefix_valid:
    deviations.append('Submitted IDs are not the contiguous original-array prefix; exact bytes preserved without factual feedback.')
if changes or missing_previous:
    deviations.append('Earlier saved answer objects changed or disappeared; compared by ID and exact earlier bytes preserved.')
if count - previous > 10:
    deviations.append('Submitted batch exceeded planned up-to10 size; actual bytes preserved.')
if count <= previous:
    deviations.append('Submitted output did not increase the saved answer count.')
record = {
    'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'reader': side, 'step': step, 'previous_count': previous,
    'saved_answer_count': count, 'new_answer_count': count - previous,
    'remaining': len(ids) - count, 'snapshot': str(snapshot), 'sha256': sha(snapshot),
    'schema_valid': bool(schema_valid), 'original_order_prefix_ids_valid': prefix_valid,
    'unique_valid_bank_ids': unique_valid_ids,
    'prior_answer_objects_unchanged_by_id': not changes and not missing_previous,
    'prior_answer_ids_changed': changes, 'prior_answer_ids_missing': missing_previous,
    'protocol_deviations': deviations, 'structural_checks_only': True,
    'no_rule_grade_or_finding_feedback': True,
}
new(folder / ('step-' + str(step).zfill(3) + '-validation.json'), record)
old.update(saved_answer_count=count, remaining=len(ids)-count)
old['batches'].append(record)
progress_path.write_text(json.dumps(old, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: record[k] for k in ['reader', 'step', 'saved_answer_count', 'new_answer_count', 'remaining', 'schema_valid', 'original_order_prefix_ids_valid', 'protocol_deviations']}))
if not schema_valid or not prefix_valid:
    sys.exit(2)
