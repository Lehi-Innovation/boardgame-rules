"""Validate archived blind continuation history without judging factual answers."""
from pathlib import Path
import hashlib
import json
import sys

R = Path(__file__).parent.resolve()
IT = (R / sys.argv[1]).resolve()
assert IT.is_relative_to(R)
N = len(json.loads((IT / 'questions.json').read_bytes())['questions'])
batch_count = (N + 9) // 10
proofs = []
for c in 'ab':
    first = json.loads((IT / f'reader-{c}-batch-01.json').read_bytes())
    records = []
    for n in range(1, batch_count + 1):
        path = IT / f'reader-{c}-batch-{n:02}.json'
        doc = json.loads(path.read_bytes())
        rec = json.loads((IT / f'reader-{c}-batch-{n:02}-structure.json').read_bytes())
        assert rec['raw_snapshot_sha256'] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert len(doc['answers']) == min(n * 10, N)
        records.append({'batch': n, 'path': str(path), 'sha256': rec['raw_snapshot_sha256'],
                        'completed_records': len(doc['answers']),
                        'earlier_answer_value_changes': rec['earlier_original_answer_values_changed_ids'],
                        'earlier_dictionary_value_changes': rec['earlier_original_dictionary_values_changed_ids'],
                        'literal_binding_diagnostics': rec.get('literal_question_binding_diagnostic_ids', []),
                        'original_input_receipts_unchanged': doc['inputs_read'] == first['inputs_read'],
                        'original_process_record_unchanged': doc['instructions_read'] == first['instructions_read'],
                        'method_code_hash_unchanged': doc['method_code_sha256'] == first['method_code_sha256']})
    assert (IT / f'reader-{c}.json').read_bytes() == (IT / f'reader-{c}-batch-{batch_count:02}.json').read_bytes()
    proofs.append({'reader': c, 'final_record_count': N, 'batch_count': batch_count, 'history': records})
out = {'pass': True, 'question_count': N, 'readers': proofs,
       'all_original_batch_snapshots_and_final_bytes_preserved': True,
       'changes_or_format_diagnostics_not_automatic_factual_grade_caps': True,
       'no_gameplay_scoring_or_factual_feedback': True,
       'one_initially_fresh_identity_per_label_not_one_vote_per_batch': True}
dest = IT / 'fixed-blind-batch-history-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(out, indent=2) + '\n')
print('PASS: preserved', 2 * batch_count, 'blind snapshots and complete', N, '-record outputs')
