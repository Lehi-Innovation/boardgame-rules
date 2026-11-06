"""Independently verify complete raw-entry transport and every requested grade atom.

This reader-evidence check never grants source/model/publication approval by itself.
"""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import argparse
import hashlib
import json

parser = argparse.ArgumentParser()
parser.add_argument('--bank', required=True)
parser.add_argument('--iteration', required=True)
parser.add_argument('--require-complete-pass', action='store_true')
args = parser.parse_args()
assert args.bank == "expanded-v13-complete-requested-scope" and args.iteration == "luna-final-stamped-iteration-01"
base = Path(__file__).resolve().parent
repo = base.parents[4]
run = repo / 'docs/quality/summary-qa/john-company-second-edition' / base.name
bank = run / args.bank
iteration = bank / args.iteration
assert bank.parent == run and iteration.parent == bank
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def check_hashes(values, relative=repo, historical_canonical=None):
    for name, expected in values.items():
        path = Path(name)
        path = path if path.is_absolute() else relative / path
        if path == repo / 'rules/john-company-second-edition.md' and historical_canonical:
            path = historical_canonical
        assert sha(path) == expected, str(path)

freeze = read(bank / 'input-manifest.json')
check_hashes(freeze['hashes'], bank)
inputs = read(iteration / 'input-manifest.json')
snapshot = iteration / 'summary-snapshot.md'
check_hashes(inputs['inputs'], historical_canonical=snapshot)
questions = read(iteration / 'questions.json')['questions']
assert questions == read(bank / 'questions.json')['questions']
ids = [x['id'] for x in questions]
assert len(set(ids)) == len(ids)
qmap = {x['id']: x for x in questions}
key = {x['id']: x for x in read(bank / 'answer-key.json')['answers']}
scope = {x['id']: x for x in read(bank / 'requested-fact-scope-reviewed.json')['questions']}
assert list(key) == list(scope) == ids
atoms = sum(len(scope[i]['material_requested_facts']) for i in ids)
canonical_equal = (repo / 'rules/john-company-second-edition.md').read_bytes() == snapshot.read_bytes()
summary = snapshot.read_text()
readers = {}
for who in ['a', 'b']:
    path = iteration / f'reader-{who}.json'
    if not path.exists():
        readers[who] = {'raw_saved': False, 'full_pass': False}
        continue
    raw = read(path)['answers']
    assert [x['id'] for x in raw] == ids
    original = {x['id']: x for x in raw}
    primary, primary_paths, blocks, requirements_equal = {}, {}, [], True
    for directory in sorted((iteration / f'grading-reader-{who}').glob('block-*')):
        packet_path = directory / 'packet.json'
        if not packet_path.exists():
            continue
        packet = read(packet_path)
        assert packet['reader_role'] == f'reader-{who}'
        assert packet['summary_sha256'] == sha(snapshot)
        for entry in packet['entries']:
            ident = entry['id']
            assert entry['question_entry'] == qmap[ident]
            assert entry['key_entry'] == key[ident]
            assert entry['requested_fact_scope_entry'] == scope[ident]
            assert entry[f'reader_{who}_entry'] == original[ident]
        grade_path = directory / 'grades-same-entry.json'
        if not grade_path.exists():
            continue
        document = read(grade_path)
        assert set(document['readers']) == {f'reader-{who}'}
        grades = document['readers'][f'reader-{who}']['grades']
        assert [g['id'] for g in grades] == [e['id'] for e in packet['entries']]
        for grade in grades:
            ident = grade['id']
            assert ident not in primary
            assert len(grade['material_parts']) == len(scope[ident]['material_requested_facts'])
            requirements_equal &= [p['requirement'] for p in grade['material_parts']] == scope[ident]['material_requested_facts']
            assert grade['grade'] in ['Correct', 'Partial', 'Incorrect'] and grade['reason']
            if grade['grade'] == 'Correct':
                assert all(p['status'] == 'covered' and p['reader_quotes'] for p in grade['material_parts'])
                assert not grade.get('unsupported_guesses')
            primary[ident] = grade
            primary_paths[ident] = str(grade_path)
        blocks.append({'directory': str(directory), 'packet_sha256': sha(packet_path), 'grades_sha256': sha(grade_path), 'ids': [g['id'] for g in grades]})
    aggregate_path = iteration / f'reader-{who}-grading-results.json'
    scores = dict(Counter(g['grade'] for g in primary.values()))
    complete = set(primary) == set(ids)
    if aggregate_path.exists():
        aggregate = read(aggregate_path)
        check_hashes(aggregate['input_hashes'])
        check_hashes(aggregate['grade_report_hashes'])
        assert aggregate['grades'] == [dict(primary[i], original_independent_grade_report=primary_paths[i]) for i in ids]
        assert aggregate['full_requested_atom_count'] == atoms
        assert aggregate['counts'] == {k: scores.get(k, 0) for k in ['Correct', 'Partial', 'Incorrect']}
    primary_scores = dict(scores)
    adjudicated_ids = []
    if who == 'b':
        disposition_path = base / 'coordinator-checks/john-stamped-q110-neutral-acceptance.json'
        disposition = read(disposition_path)
        adjud_path = Path(disposition['neutral_report_path'])
        assert disposition['verified'] and disposition['neutral_grade'] == 'Correct'
        assert sha(adjud_path) == disposition['neutral_report_sha256']
        assert sha(Path(disposition['primary_report_path'])) == disposition['primary_report_sha256']
        adjud, = read(adjud_path)['readers']['reader-b']['grades']
        assert adjud['id'] == 'Q110' and primary['Q110']['grade'] == 'Partial'
        assert [p['requirement'] for p in adjud['material_parts']] == scope['Q110']['material_requested_facts']
        assert all(p['status'] == 'covered' and p['reader_quotes'] for p in adjud['material_parts'])
        assert not adjud['unsupported_guesses']
        primary['Q110'] = adjud
        adjudicated_ids = ['Q110']
        scores = dict(Counter(g['grade'] for g in primary.values()))
    full_pass = complete and scores == {'Correct': len(ids)}
    readers[who] = {'raw_saved': True, 'raw_sha256': sha(path), 'raw_entries_exactly_preserved_in_packets': True, 'graded_questions': len(primary), 'required_atom_count': sum(len(scope[i]['material_requested_facts']) for i in primary), 'all_requested_atom_labels_exactly_equal_frozen_scope': requirements_equal, 'scores': scores, 'primary_scores': primary_scores, 'adjudicated_ids': adjudicated_ids, 'all_ids_graded_once': complete, 'full_pass': full_pass, 'blocks': blocks}
    if args.require_complete_pass:
        assert full_pass and requirements_equal, who
if args.require_complete_pass:
    assert canonical_equal
out = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS_READER_EVIDENCE_ONLY' if args.require_complete_pass else 'INCOMPLETE_CHECKPOINT', 'bank': args.bank, 'iteration': args.iteration, 'question_count': len(ids), 'required_atoms_per_reader': atoms, 'summary_sha256': sha(snapshot), 'canonical_equals_snapshot_at_check': canonical_equal, 'readers': readers, 'both_full_bank_semantic_pass': all(r['full_pass'] for r in readers.values()), 'requires_separate_checks': ['Actual model/effort/fork and pre-answer/pre-grade complete delivery', 'Fresh pure exact-byte source audit within explicit user scope', 'Working-saturation independent coverage challenge', 'Historical integrity, required repository checks and stamping/publication'], 'no_source_or_publication_approval_granted': True, 'single_neutral_disposition_path': str(base / 'coordinator-checks/john-stamped-q110-neutral-acceptance.json'), 'original_primary_partial_preserved': True}
target = base / 'coordinator-checks' / ('john-adjudicated-' + args.bank + '-' + args.iteration + '-reader-evidence-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '.json')
target.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps({'proof': str(target), 'status': out['status'], 'scores': {w: r.get('scores') for w, r in readers.items()}, 'both_pass': out['both_full_bank_semantic_pass']}))
