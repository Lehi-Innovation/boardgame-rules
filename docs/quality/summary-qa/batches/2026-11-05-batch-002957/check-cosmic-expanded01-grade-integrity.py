"""Rebind all initial expanded grades to complete original entries and fixed inputs."""
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
D = ROOT / 'docs/quality/summary-qa/cosmic-encounter' / B.name / 'expanded-iteration-01'
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
HB = lambda b: hashlib.sha256(b).hexdigest()
questions = {x['id']: x for x in load(D / 'questions.json')['questions']}
key = {x['id']: x for x in load(D / 'answer-key.json')['answers']}
scope = {x['id']: x for x in load(D / 'actual-question-scope.json')['questions']}
raw_paths = {w: D / ('reader-' + w + '.json') for w in 'ab'}
raw = {w: {x['id']: x for x in load(p)['answers']} for w, p in raw_paths.items()}
raw_bytes = {w: p.read_bytes() for w, p in raw_paths.items()}
seen = {w: [] for w in 'ab'}
totals = {w: Counter() for w in 'ab'}
fact_totals = {w: 0 for w in 'ab'}
classification_counts = Counter()
reports = []
aliases = ['complete_original_entry', 'raw_reader_record', 'raw_reader_record_preserved',
           'preserved_raw_reader_record']
plan = load(D / 'grading-dispatch-plan.json')
for task in plan['graders']:
    bundle_path, report_path = Path(task['bundle_path']), Path(task['output_path'])
    assert H(bundle_path) == task['bundle_sha256']
    bundle, report = load(bundle_path), load(report_path)
    assert bundle['summary_sha256'] == H(D / 'summary-snapshot.md')
    assert bundle['expected_ids'] == task['expected_ids']
    bundled = {x['id']: x for x in bundle['entries']}
    assert list(bundled) == task['expected_ids']
    for ident, entry in bundled.items():
        assert entry['literal_question'] == questions[ident]
        assert entry['key'] == key[ident]
        assert entry['validated_actual_scope'] == scope[ident]
        assert len(entry['raw_key_fact_refs']) == len(key[ident]['required_facts'])
        for who in 'ab':
            saved = entry['readers'][who]
            assert saved['complete_original_entry'] == raw[who][ident]
            assert saved['raw_file_sha256'] == H(raw_paths[who])
            fragment = raw_bytes[who][saved['start_byte']:saved['end_byte']]
            assert HB(fragment) == saved['raw_entry_sha256']
            assert json.loads(fragment) == raw[who][ident]
    for who in 'ab':
        entries = report['readers'][who]['entries']
        assert [x['id'] for x in entries] == task['expected_ids']
        for entry in entries:
            ident = entry['id']
            original = raw[who][ident]
            full = [entry[n] for n in aliases if n in entry]
            full = [x.get('complete_original_entry', x) for x in full]
            assert full and all(x == original for x in full), (report_path, who, ident)
            assert entry['observed_raw_entry_hash'] == bundled[ident]['readers'][who]['raw_entry_sha256']
            fact_ids = [f.get('id', f.get('fact_id', f.get('key_fact_id'))) for f in entry['fact_checks']]
            expected = [f['id'] for f in bundled[ident]['raw_key_fact_refs']]
            assert fact_ids == expected and len(fact_ids) == len(set(fact_ids))
            states = [f.get('classification', f.get('asked_portion_status')) for f in entry['fact_checks']]
            assert all(s in ['matched', 'missing', 'background-only', 'contradicted'] for s in states)
            classification_counts.update(states)
            if entry['material_contradictions'] or 'contradicted' in states:
                assert entry['grade'] == 'incorrect', (who, ident, entry['grade'])
            if entry['grade'] == 'correct':
                assert not entry['missing_asked_facts'] and 'missing' not in states
            assert entry['grade'] in ['correct', 'partial', 'incorrect']
            totals[who][entry['grade']] += 1
            fact_totals[who] += len(fact_ids)
            seen[who].append(ident)
    reports.append({'path': str(report_path), 'sha256': H(report_path),
                    'bundle_path': str(bundle_path), 'bundle_sha256': H(bundle_path),
                    'ids': task['expected_ids']})
assert all(seen[w] == list(questions) and fact_totals[w] == 544 for w in 'ab')
aggregate = load(D / 'original-grades-aggregate.json')
assert aggregate['totals'] == {w: dict(totals[w]) for w in 'ab'}
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'N': len(questions), 'original_entries': sum(len(x) for x in seen.values()),
          'raw_fact_assessments': fact_totals, 'fact_classifications': dict(classification_counts),
          'primary_totals': {w: dict(totals[w]) for w in 'ab'}, 'reports': reports,
          'aggregate_sha256': H(D / 'original-grades-aggregate.json'),
          'raw_outputs': {w: {'path': str(p), 'sha256': H(p)} for w, p in raw_paths.items()},
          'limits': 'Independent completeness, exact original byte-span/object and frozen question/key/scope binding, primary aggregate arithmetic, and material-contradiction label checks. Does not replace semantic grading or a fresh neutral adjudication. Primary grades remain unchanged. Fixed-set preliminary full-bank regression only; global authority choices remain pending.'}
out = B / 'coordinator-checks/cosmic-expanded01-primary-grade-integrity.json'
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'entries': result['original_entries'],
                  'fact_assessments': sum(fact_totals.values()), 'totals': result['primary_totals'],
                  'report': str(out)}))
