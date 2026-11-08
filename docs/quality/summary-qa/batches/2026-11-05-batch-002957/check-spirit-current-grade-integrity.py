"""Check complete primary grade bookkeeping against the exact frozen full bank."""
import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--iteration', required=True, type=int)
args = parser.parse_args()
assert args.iteration >= 8
label = f'{args.iteration:02d}'
D = ROOT / 'docs/quality/summary-qa/spirit-island' / B.name / ('expanded-iteration-' + label)
load = lambda p: json.loads(p.read_text())
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
questions = {x['id']: x for x in load(D / 'questions.json')['questions']}
key_path = Path(load(D / 'input-manifest.json')['key_path'])
key = {x['id']: x for x in load(key_path)['answers']}
scope = {x['id']: x for x in load(D / 'asked-fact-map.json')['questions']}
raw_paths = {w: D / (w + '.json') for w in ['reader-a', 'reader-b']}
raw = {w: {x['id']: x for x in load(p)['answers']} for w, p in raw_paths.items()}
seen, totals, fact_counts = {}, {}, {}
for who in raw:
    seen[who], totals[who], fact_counts[who] = [], Counter(), 0
outcomes, reports, diagnostics = Counter(), [], []
for block in sorted((D / 'grading').glob('block-*')):
    manifest = load(block / 'input-manifest.json')
    for name, receipt in manifest['inputs'].items():
        path = Path(name)
        assert H(path) == receipt['sha256'] and len(path.read_text()) == receipt['characters']
    q = load(block / 'questions.json')['questions']
    k = load(block / 'answer-key.json')['answers']
    s = load(block / 'asked-facts.json')['questions']
    ids = manifest['expected_ids']
    assert [x['id'] for x in q] == ids == [x['id'] for x in k] == [x['id'] for x in s]
    assert all(x == questions[x['id']] for x in q)
    assert all(x == key[x['id']] for x in k)
    assert all(x == scope[x['id']] for x in s)
    bundle = load(block / 'raw-answers.json')
    for who in raw:
        assert bundle['readers'][who]['answers'] == [raw[who][ident] for ident in ids]
        assert bundle['full_raw_output_hashes'][who[-1]] == H(raw_paths[who])
    report_path = block / 'grades-original-completed.json'
    report = load(report_path)
    assert H(report_path) == H(block / 'grades.json')
    assert report['expected_ids'] == ids
    block_seen = {w: [] for w in raw}
    block_totals = {w: Counter() for w in raw}
    for entry in report['grades']:
        who, ident = entry['reader'], entry['id']
        assert ident in ids and who in raw
        requested = {c['clause_id']: c for c in scope[ident]['requested_clauses']}
        assessed = entry['requested_part_assessment']
        assert [x['clause_id'] for x in assessed] == list(requested)
        for clause in assessed:
            required = requested[clause['clause_id']]['required_facts']
            facts = clause['fact_assessments']
            assert [x['fact_index'] for x in facts] == list(range(1, len(required) + 1))
            outcomes.update(x['outcome'] for x in facts)
            fact_counts[who] += len(facts)
            for i, fact in enumerate(facts):
                if fact['expected'] != required[i]:
                    diagnostics.append({'kind': 'grader_expected_text_paraphrase', 'reader': who,
                                        'id': ident, 'clause': clause['clause_id'], 'index': i + 1})
        assert entry['grade'] in ['correct', 'partial', 'incorrect']
        if entry.get('contradictions') and entry['grade'] != 'incorrect':
            diagnostics.append({'kind': 'contradiction_label_review', 'reader': who, 'id': ident})
        seen[who].append(ident)
        block_seen[who].append(ident)
        totals[who][entry['grade']] += 1
        block_totals[who][entry['grade']] += 1
    assert all(block_seen[w] == ids for w in raw)
    assert report['totals'] == {w: {k: block_totals[w][k] for k in ['correct', 'partial', 'incorrect']} for w in raw}
    reports.append({'block': block.name, 'original_report_path': str(report_path),
                    'original_report_sha256': H(report_path), 'manifest_sha256': H(block / 'input-manifest.json'),
                    'ids': ids})
assert len(reports) == 9
assert all(seen[w] == list(questions) and fact_counts[w] == 506 for w in raw)
assert not [x for x in diagnostics if x['kind'] == 'contradiction_label_review']
result = {'verified': True, 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'N': len(questions), 'original_entries': sum(len(x) for x in seen.values()),
          'fact_assessments': fact_counts, 'fact_outcomes': dict(outcomes),
          'primary_totals': {w: dict(totals[w]) for w in raw}, 'reports': reports,
          'diagnostics': diagnostics, 'raw_output_sha256': {w: H(p) for w, p in raw_paths.items()},
          'limits': 'Checks exact complete original entries in every grader bundle, actual frozen Q/key/map objects, all346 original answers, all1012 mapped fact assessments and primary arithmetic. Semantic judgments and any one fresh neutral remain separate; no factual upgrade, source/publication approval, or grade cap follows from transport/format metadata.'}
out = B / 'coordinator-checks' / ('spirit-expanded' + label + '-primary-grade-integrity.json')
assert not out.exists(), 'Original completed coordinator proofs remain immutable'
out.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'verified': True, 'entries': result['original_entries'],
                  'facts': sum(fact_counts.values()), 'totals': result['primary_totals'],
                  'diagnostics': len(diagnostics), 'report': str(out)}))
