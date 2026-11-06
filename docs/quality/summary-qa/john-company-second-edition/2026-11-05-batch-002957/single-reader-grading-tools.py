"""Per-reader scheduling adapter; the unchanged paired validator owns final merge."""
from pathlib import Path
import collections
import copy
import importlib.util
import json
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('paired_grading', ROOT / 'block-grading-tools.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def save_new(path, value):
    with path.open('x') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write('\n')


def context(bank_name, iteration, role):
    if role not in ['a', 'b']:
        raise ValueError('Expected role a or b')
    bank, run = ROOT / bank_name, ROOT / bank_name / iteration
    questions = base.read(bank / 'questions.json')['questions']
    ids = [q['id'] for q in questions]
    if not ids or len(ids) != len(set(ids)):
        raise ValueError('Question IDs empty or duplicated')
    key_path = bank / 'answer-key.json'
    revision = run / 'grading-key-revision.json'
    if revision.exists():
        key_path = Path(base.read(revision)['answer_key_source'])
    key_rows = base.read(key_path)['answers']
    if [q['id'] for q in key_rows] != ids:
        raise ValueError('Key IDs/order/count differ')
    scope_path = bank / 'requested-fact-scope-reviewed.json'
    if not scope_path.exists():
        scope_path = bank / 'requested-fact-scope.json'
    scope_rows = base.scope_entries(base.read(scope_path))
    if collections.Counter(q['id'] for q in scope_rows) != collections.Counter(ids):
        raise ValueError('Scope IDs/count differ')
    raw_rows = base.read(run / f'reader-{role}.json')['answers']
    if [q['id'] for q in raw_rows] != ids:
        raise ValueError('Original reader IDs/order/count differ; nothing indexed or dropped')
    return bank, run, questions, ids, key_path, scope_path, {
        q['id']: q for q in key_rows}, {q['id']: q for q in scope_rows}, {
        q['id']: q for q in raw_rows}


def prepare(bank_name, iteration, role):
    bank, run, questions, ids, key_path, scope_path, keys, scopes, raw = context(bank_name, iteration, role)
    target = run / f'grading-reader-{role}'
    if target.exists():
        raise FileExistsError('Preserve existing role packets')
    count = (len(ids) + 19) // 20
    size, extra = divmod(len(ids), count)
    packets, blocks, start = [], [], 0
    for index in range(count):
        length = size + (index < extra)
        block_id = f'block-{index + 1:02d}'
        entries = [dict(id=q['id'], question_entry=q, key_entry=keys[q['id']],
            requested_fact_scope_entry=scopes[q['id']],
            **{f'reader_{role}_entry': raw[q['id']]}) for q in questions[start:start + length]]
        packet = dict(benchmark_version=bank_name, iteration=iteration, block_id=block_id,
            reader_role=f'reader-{role}', normative_scope=base.read(bank / 'questions.json')['scope'],
            grading_scope=base.read(bank / 'grading-scope.json'), requested_fact_scope_source=str(scope_path),
            answer_key_source=str(key_path), grading_standard=base.read(bank / 'answer-key.json')['grading_standard'],
            summary_path=str(run / 'summary-snapshot.md'), summary_sha256=base.sha(run / 'summary-snapshot.md'),
            entries=entries)
        packets.append((block_id, packet))
        blocks.append(dict(block_id=block_id, ids=[q['id'] for q in entries],
            complete_raw_entry_sha256s={q['id']: base.entry_sha(q[f'reader_{role}_entry']) for q in entries},
            no_fields_removed=True, quotation_deduplication='none'))
        start += length
    assert [qid for block in blocks for qid in block['ids']] == ids
    target.mkdir()
    for (block_id, packet), block in zip(packets, blocks):
        folder = target / block_id
        folder.mkdir()
        save_new(folder / 'packet.json', packet)
        block['packet_sha256'] = base.sha(folder / 'packet.json')
    paths = [bank / 'questions.json', bank / 'answer-key.json', key_path,
        bank / 'grading-scope.json', scope_path, run / 'summary-snapshot.md', run / f'reader-{role}.json']
    save_new(target / 'packet-manifest.json', dict(reader_role=f'reader-{role}', blocks=blocks,
        exact_disjoint_ids=ids, input_hashes={str(p): base.sha(p) for p in paths},
        complete_raw_entries_losslessly_preserved=True, quotation_deduplication='none'))
    return [(b['block_id'], len(b['ids'])) for b in blocks]


def validate_role(bank_name, iteration, role):
    bank, run, questions, ids, key_path, scope_path, keys, scopes, raw = context(bank_name, iteration, role)
    target = run / f'grading-reader-{role}'
    manifest = base.read(target / 'packet-manifest.json')
    assert manifest['reader_role'] == f'reader-{role}' and manifest['exact_disjoint_ids'] == ids
    for path, expected in manifest['input_hashes'].items():
        assert base.sha(Path(path)) == expected, path
    grades, report_hashes, assigned = [], {}, []
    qmap = {q['id']: q for q in questions}
    for block in manifest['blocks']:
        folder = target / block['block_id']
        packet = base.read(folder / 'packet.json')
        assert base.sha(folder / 'packet.json') == block['packet_sha256']
        assert packet['reader_role'] == f'reader-{role}'
        assert [e['id'] for e in packet['entries']] == block['ids']
        for entry in packet['entries']:
            qid = entry['id']
            assert entry['question_entry'] == qmap[qid]
            assert entry['key_entry'] == keys[qid] and entry['requested_fact_scope_entry'] == scopes[qid]
            assert entry[f'reader_{role}_entry'] == raw[qid]
            assert base.entry_sha(raw[qid]) == block['complete_raw_entry_sha256s'][qid]
        report_path = folder / 'grades-same-entry.json'
        report = base.read(report_path)
        assert report['block_id'] == block['block_id'] and set(report['readers']) == {f'reader-{role}'}
        block_grades = report['readers'][f'reader-{role}']['grades']
        assert [g['id'] for g in block_grades] == block['ids']
        for grade in block_grades:
            g = copy.deepcopy(grade)
            g['grade'] = g['grade'].capitalize()
            assert g['grade'] in ['Correct', 'Partial', 'Incorrect']
            qid = g['id']
            assert collections.Counter(p['requirement'] for p in g['material_parts']) == collections.Counter(scopes[qid]['material_requested_facts'])
            substantive = base.substantive_strings(raw[qid])
            for part in g['material_parts']:
                assert part['status'].lower() in ['covered', 'omitted', 'contradicted']
                quotes = part.get('reader_quotes', [])
                assert isinstance(quotes, list) and all(isinstance(q, str) and q.strip() for q in quotes)
                assert all(any(q in s for s in substantive) for q in quotes)
                if part['status'].lower() == 'covered':
                    assert quotes
            if g['grade'] == 'Correct':
                assert all(p['status'].lower() == 'covered' for p in g['material_parts'])
            g['original_independent_grade_report'] = str(report_path)
            grades.append(g)
        assigned += block['ids']
        report_hashes[str(report_path)] = base.sha(report_path)
    assert assigned == ids and [g['id'] for g in grades] == ids
    return dict(reader_role=f'reader-{role}', grades=grades,
        counts={s: sum(g['grade'] == s for g in grades) for s in ['Correct', 'Partial', 'Incorrect']},
        input_hashes=manifest['input_hashes'], grade_report_hashes=report_hashes,
        full_requested_atom_count=sum(len(scopes[qid]['material_requested_facts']) for qid in ids),
        limits='Per-reader assessment only; full pair, independent source and final canonical gates remain separate.')


def collect(bank_name, iteration, role):
    result = validate_role(bank_name, iteration, role)
    save_new(ROOT / bank_name / iteration / f'reader-{role}-grading-results.json', result)
    return result['counts']


def combine(bank_name, iteration):
    run = ROOT / bank_name / iteration
    roles = {role: validate_role(bank_name, iteration, role) for role in 'ab'}
    for role in 'ab':
        assert base.read(run / f'reader-{role}-grading-results.json') == roles[role], 'Role collection changed'
    assert not (run / 'grading-blocks').exists() and not (run / 'results.json').exists()
    base.prepare(bank_name, iteration)
    for block in base.read(run / 'grading-blocks/packet-manifest.json')['blocks']:
        folder = run / 'grading-blocks' / block['block_id']
        combined = dict(block_id=block['block_id'], readers={}, per_reader_original_reports={})
        for role in 'ab':
            source = run / f'grading-reader-{role}' / block['block_id']
            single = base.read(source / 'packet.json')
            paired = base.read(folder / 'packet.json')
            assert [e['id'] for e in single['entries']] == block['ids']
            for one, both in zip(single['entries'], paired['entries']):
                assert all(one[k] == both[k] for k in one)
            report = source / 'grades-same-entry.json'
            combined['readers'][f'reader-{role}'] = base.read(report)['readers'][f'reader-{role}']
            combined['per_reader_original_reports'][f'reader-{role}'] = dict(path=str(report), sha256=base.sha(report))
        save_new(folder / 'grades-same-entry.json', combined)
    return base.merge(bank_name, iteration)


if __name__ == '__main__':
    command, bank_name, iteration, *args = sys.argv[1:]
    if command == 'combine':
        result = combine(bank_name, iteration)
    elif command in ['prepare', 'collect', 'validate'] and len(args) == 1:
        result = {'prepare': prepare, 'collect': collect, 'validate': validate_role}[command](bank_name, iteration, args[0])
    else:
        raise ValueError('prepare|collect|validate BANK ITERATION ROLE; combine BANK ITERATION')
    print(json.dumps(result, indent=2))
