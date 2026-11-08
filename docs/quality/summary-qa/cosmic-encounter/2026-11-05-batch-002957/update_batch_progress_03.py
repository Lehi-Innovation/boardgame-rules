"""Update mutable progress only from immutable structural batch receipts."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

R = Path(__file__).parent.resolve()
IT = R / 'expanded-iteration-03'
p = R / 'progress.json'
progress = json.loads(p.read_bytes())
current = next(i for i in progress['iterations'] if i['id'] == IT.name)
counts, completed, changed = {}, {}, False
for c in 'ab':
    receipts = [json.loads(q.read_bytes()) for q in sorted(IT.glob(f'reader-{c}-batch-??-structure.json'))]
    for rec in receipts:
        snapshot = Path(rec['raw_snapshot_path'])
        assert hashlib.sha256(snapshot.read_bytes()).hexdigest() == rec['raw_snapshot_sha256']
        changed |= bool(rec['earlier_original_answer_values_changed_ids'] or
                        rec['earlier_original_dictionary_values_changed_ids'])
    last = receipts[-1] if receipts else {}
    counts[c] = last.get('batch', 0)
    completed[c] = last.get('completed_records', 0)
current['batch_counts'] = counts
current['completed_question_prefix_counts'] = completed
current['earlier_entry_or_dictionary_value_changes_observed'] = changed
current['complete_raw_pair_archived'] = all(n == 167 for n in completed.values())
progress['updated_at_utc'] = datetime.now(timezone.utc).isoformat()
p.write_text(json.dumps(progress, indent=2) + '\n')
print('Archived blind record prefixes:', completed, '; earlier values changed:', changed)
