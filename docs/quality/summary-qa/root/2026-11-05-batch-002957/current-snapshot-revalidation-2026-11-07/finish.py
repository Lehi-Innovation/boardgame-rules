from evidence import *
import collections

def freeze():
    ids = [x['id'] for x in json.loads((I / 'questions.json').read_text())['questions']]
    readers, draft_differences = {}, []
    for side in 'ab':
        path = I / f'reader-{side}.json'
        raw = json.loads(path.read_text())
        assert len(raw['answers']) == 81
        assert [x['id'] for x in raw['answers']] == ids
        backup = I / 'originals' / f'reader-{side}.json'
        backup.parent.mkdir(exist_ok=True)
        if backup.exists():
            assert backup.read_bytes() == path.read_bytes()
        else:
            backup.write_bytes(path.read_bytes())
        readers[side] = {'path': str(path), 'sha256': sha(path), 'bytes': path.stat().st_size, 'exact_original_copy': str(backup), 'copy_sha256': sha(backup), 'answer_count': 81}
        for checkpoint in sorted((I / 'checkpoints').glob(f'reader-{side}-*.json')):
            earlier = json.loads(checkpoint.read_text())['answers']
            if len(earlier) % 10 == 0 or len(earlier) == 81:
                assert earlier == raw['answers'][:len(earlier)], 'Completed-turn original changed'
            elif earlier != raw['answers'][:len(earlier)]:
                draft_differences.append({'reader': side, 'mid_turn_checkpoint': str(checkpoint), 'checkpoint_sha256': sha(checkpoint), 'changes': [{'id': a['id'], 'draft': a, 'complete_original': b} for a, b in zip(earlier, raw['answers']) if a != b]})
    prior = sorted((I / 'primary-grades').glob('*.json'))
    report = {'frozen_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'readers': readers, 'hashes': {str(I / name): sha(I / name) for name in ('summary-snapshot.md', 'questions.json', 'answer-key.json')}, 'both_full_originals_before_remaining_grading': True, 'existing_prefix_primary_labels_preserved': {str(p): sha(p) for p in prior}, 'existing_primary_count': len(prior), 'chronology_deviation': 'iteration-01/grading-chronology-deviation.json' if prior else None, 'no_factual_feedback_to_readers': True}
    save(I / 'raw-output-manifest.json', report)
    save(I / 'mid-turn-draft-review.json', {'differences': draft_differences, 'completed_turn_entries_unchanged': True, 'disposition': 'Mid-turn drafts are preserved separately; complete-turn originals are immutable. No factual feedback was supplied. These draft/receipt diagnostics do not cap factual scores. Any substantive final entry is graded against the fixed key.'})
    print(json.dumps({'full_originals_frozen': {s: r['sha256'] for s, r in readers.items()}, 'existing_primary_decisions': len(prior)}))

def results():
    ids = [x['id'] for x in json.loads((I / 'questions.json').read_text())['questions']]
    frozen = json.loads((I / 'raw-output-manifest.json').read_text())
    readers, primary_readers = {}, {}
    adjud_path = I / 'neutral-adjudication.json'
    adjud = json.loads(adjud_path.read_text()) if adjud_path.exists() else None
    adjud_cases = {x['case_id']: x for x in adjud['cases']} if adjud else {}
    for side in 'ab':
        assert sha(I / f'reader-{side}.json') == frozen['readers'][side]['sha256']
        raw = json.loads((I / f'reader-{side}.json').read_text())
        grades = [json.loads((I / 'primary-grades' / f'{side}-{qid}.json').read_text()) for qid in ids]
        assert [g['observed_original_entry'] for g in grades] == raw['answers']
        primary_counts = collections.Counter(g['grade'] for g in grades)
        primary_readers[side] = {'totals': {k: primary_counts[k] for k in ('correct', 'partial', 'incorrect', 'borderline')}, 'grades': grades, 'original_sha256': frozen['readers'][side]['sha256']}
        effective = []
        for g in grades:
            if g['grade'] == 'borderline':
                decision = adjud_cases[side + '-' + g['id']]
                assert decision['grade'] in ('correct', 'partial', 'incorrect')
                g = {**g, 'primary_grade': 'borderline', 'primary_reason': g['reason'], 'grade': decision['grade'], 'reason': decision['reasoning'], 'neutral_adjudication': {'path': str(adjud_path), 'sha256': sha(adjud_path), 'case_id': decision['case_id']}, 'unsupported_guess': False if decision['grade'] == 'correct' else None, 'unresolved_requested_fact': False if decision['grade'] == 'correct' else None}
            effective.append(g)
        counts = collections.Counter(g['grade'] for g in effective)
        readers[side] = {'totals': {k: counts[k] for k in ('correct', 'partial', 'incorrect')}, 'grades': effective, 'original_sha256': frozen['readers'][side]['sha256']}
    report = {'benchmark': 'benchmark-v10', 'question_count': 81, 'summary_sha256': sha(I / 'summary-snapshot.md'), 'key_sha256': sha(I / 'answer-key.json'), 'readers': readers, 'regression_status': 'PASS' if all(x['totals']['correct'] == 81 for x in readers.values()) else 'FAIL', 'adjudication': {'path': str(adjud_path), 'sha256': sha(adjud_path), 'one_fresh_neutral': True, 'cases': sorted(adjud_cases)} if adjud else 'None: no genuine unresolved whole-entry borderline. Primary and effective grades identical.', 'limits': 'Fixed regression bank, no exhaustive rule-coverage or held-out/general-model claim. Metadata/transport is not a factual-score cap.'}
    save(I / 'results-primary.json', {**report, 'readers': primary_readers, 'regression_status': 'PASS' if all(x['totals']['correct'] == 81 for x in primary_readers.values()) else 'FAIL_OR_PENDING_BORDERLINE', 'grade_label_note': 'borderline is a preserved unresolved primary semantic label, not a fractional factual score. Effective grades resolve only those labels using the one fresh neutral.'})
    save(I / 'results.json', report)
    print(json.dumps({'regression_status': report['regression_status'], 'scores': {s: x['totals'] for s, x in readers.items()}}))

if __name__ == '__main__':
    {'freeze': freeze, 'results': results}[sys.argv[1]]()
