"""Archive completed fixed blind batches; inspect structure, never factual scores."""
from pathlib import Path
import hashlib
import json
import sys
from datetime import datetime, timezone

R = Path(__file__).parent.resolve()
IT = (R / sys.argv[1]).resolve()
assert IT.is_relative_to(R)
label = sys.argv[2]
assert label in ('a', 'b')
path = IT / f'reader-{label}.json'
raw = path.read_bytes()
doc = json.loads(raw)
expected = [q['id'] for q in json.loads((IT / 'questions.json').read_bytes())['questions']]
N = len(expected)
bank_records = json.loads((IT / 'questions.json').read_bytes())['questions']
answers = doc['answers']
count = len(answers)
assert 0 < count <= N
assert count % 10 == 0 or count == N, 'Not at a preplanned fixed boundary'
assert [a['id'] for a in answers] == expected[:count]
batch = (count + 9) // 10
dest = IT / f'reader-{label}-batch-{batch:02}.json'
assert not dest.exists(), 'Preserve immutable completed batch snapshot'
previous = IT / f'reader-{label}-batch-{batch-1:02}.json'
changed, pool_changed = [], []


def pool_values(pool):
    if isinstance(pool, dict):
        return pool
    return {str(u.get('number', u.get('id', i))) if isinstance(u, dict) else str(i): u
            for i, u in enumerate(pool)}


if batch > 1:
    old = json.loads(previous.read_bytes())
    assert len(old['answers']) == min((batch-1)*10, N)
    changed = [a['id'] for a, b in zip(old['answers'], answers) if a != b]
    current_pool = pool_values(doc.get('evidence_units', []))
    pool_changed = [k for k, u in pool_values(old.get('evidence_units', [])).items()
                    if current_pool.get(k) != u]
dest.write_bytes(raw)
report = {'reader': label, 'batch': batch, 'completed_records': count,
          'expected_prefix_ids_match': True, 'bank_complete': count == N,
          'raw_snapshot_path': str(dest), 'raw_snapshot_sha256': hashlib.sha256(raw).hexdigest(),
          'earlier_original_answer_values_changed_ids': changed,
          'earlier_original_dictionary_values_changed_ids': pool_changed,
          'only_structural_checks_no_gameplay_grading': True,
          'literal_question_binding_diagnostic_ids': [a['id'] for a, q in zip(answers, bank_records) if a.get('literal_question') != q['question']],
          'earlier_changes_preserved_not_discarded_or_automatically_capped': True,
          'created_at_utc': datetime.now(timezone.utc).isoformat()}
(IT / f'reader-{label}-batch-{batch:02}-structure.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: report[k] for k in ('reader', 'batch', 'completed_records', 'bank_complete',
                                       'earlier_original_answer_values_changed_ids',
                                       'earlier_original_dictionary_values_changed_ids')}))
