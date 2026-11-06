"""Lossless full-entry packets and disjoint grading; no source-status score cap."""
from pathlib import Path
import collections, copy, hashlib, json, sys

ROOT = Path(__file__).resolve().parent

def read(p):
    return json.loads(p.read_text())

def save(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def entry_sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()

def scope_entries(value):
    if isinstance(value, list) and value and all(isinstance(x, dict) and 'id' in x for x in value):
        return value
    if isinstance(value, dict):
        for field in ['questions', 'entries', 'scopes', 'requested_facts', 'per_question', 'checklist']:
            if field in value:
                result = scope_entries(value[field])
                if result:
                    return result
        if value and all(k.startswith('Q') and isinstance(v, dict) for k, v in value.items()):
            return [dict(id=k, **v) for k, v in value.items()]
    return []

def prepare(bank_name, iteration):
    bank = ROOT / bank_name
    run = bank / iteration
    target = run / 'grading-blocks'
    target.mkdir(exist_ok=False)
    questions = read(bank / 'questions.json')['questions']
    key_path = bank / 'answer-key.json'
    revision = run / 'grading-key-revision.json'
    if revision.exists():
        key_path = Path(read(revision)['answer_key_source'])
    keys = {x['id']: x for x in read(key_path)['answers']}
    scope_path = bank / 'requested-fact-scope-reviewed.json'
    if not scope_path.exists():
        scope_path = bank / 'requested-fact-scope.json'
    scopes = {x['id']: x for x in scope_entries(read(scope_path))}
    ids = [x['id'] for x in questions]
    assert len(scopes) == len(ids) and set(scopes) == set(ids)
    raw = {role: {x['id']: x for x in read(run / f'reader-{role}.json')['answers']}
           for role in 'ab'}
    assert all(set(v) == set(ids) for v in raw.values())
    manifests, assigned = [], []
    block_count = (len(ids) + 19) // 20
    base, extra = divmod(len(ids), block_count)
    start = 0
    for index in range(block_count):
        size = base + (index < extra)
        block_id = f'block-{index + 1:02d}'
        folder = target / block_id
        folder.mkdir()
        entries = []
        for q in questions[start:start + size]:
            qid = q['id']
            entry = dict(id=qid, question_entry=q, key_entry=keys[qid],
                         requested_fact_scope_entry=scopes[qid],
                         reader_a_entry=raw['a'][qid], reader_b_entry=raw['b'][qid])
            assert entry['reader_a_entry'] == raw['a'][qid]
            assert entry['reader_b_entry'] == raw['b'][qid]
            entries.append(entry)
            assigned.append(qid)
        packet = dict(benchmark_version=bank_name, iteration=iteration, block_id=block_id,
                      normative_scope=read(bank / 'questions.json')['scope'],
                      grading_scope=read(bank / 'grading-scope.json'),
                      requested_fact_scope_source=str(scope_path),
                      answer_key_source=str(key_path),
                      grading_standard=read(bank / 'answer-key.json')['grading_standard'],
                      summary_path=str(run / 'summary-snapshot.md'),
                      summary_sha256=sha(run / 'summary-snapshot.md'), entries=entries)
        save(folder / 'packet.json', packet)
        manifests.append(dict(block_id=block_id, ids=[e['id'] for e in entries],
                              packet_sha256=sha(folder / 'packet.json'),
                              complete_raw_entry_sha256s={role: {e['id']: entry_sha(e[f'reader_{role}_entry'])
                                                               for e in entries} for role in 'ab'},
                              no_fields_removed=True, quotation_deduplication='none'))
        start += size
    assert assigned == ids and len(set(assigned)) == len(ids)
    save(target / 'packet-manifest.json', dict(blocks=manifests, exact_disjoint_ids=ids,
         input_hashes={str(p): sha(p) for p in [bank / 'questions.json', bank / 'answer-key.json', key_path,
             bank / 'grading-scope.json', scope_path,
             run / 'summary-snapshot.md', run / 'reader-a.json', run / 'reader-b.json']},
         complete_raw_entries_losslessly_preserved=True,
         quotation_deduplication='none; original parsed JSON entries retained in full'))
    return [(m['block_id'], len(m['ids'])) for m in manifests]

def substantive_strings(entry):
    def values(value):
        if isinstance(value, str): return [value]
        if isinstance(value, list): return [s for x in value for s in values(x)]
        if isinstance(value, dict): return [s for x in value.values() for s in values(x)]
        return []
    strings = values(entry.get('answer', '')) + values(entry.get('case_conclusions', []))
    strings += [s for clause in entry.get('clause_ledger', [])
                for s in values(clause.get('supported_fact_or_case_result', ''))]
    strings += [s for evidence in entry.get('evidence', []) for s in values(evidence.get('quote', ''))]
    return strings

def merge(bank_name, iteration):
    bank = ROOT / bank_name
    run = bank / iteration
    target = run / 'grading-blocks'
    manifest = read(target / 'packet-manifest.json')
    for p, expected in manifest['input_hashes'].items():
        assert sha(Path(p)) == expected, p
    ids = manifest['exact_disjoint_ids']
    all_grades = {'reader-a': [], 'reader-b': []}
    for block in manifest['blocks']:
        folder = target / block['block_id']
        packet = read(folder / 'packet.json')
        assert sha(folder / 'packet.json') == block['packet_sha256']
        report_path = folder / ('grades-same-entry.json' if (folder / 'grades-same-entry.json').exists() else 'grades.json')
        report = read(report_path)
        entries = {x['id']: x for x in packet['entries']}
        for role in all_grades:
            rv = report['readers'][role]
            grades = rv['grades'] if isinstance(rv, dict) else rv
            assert collections.Counter(x['id'] for x in grades) == collections.Counter(block['ids'])
            for g in grades:
                z = copy.deepcopy(g)
                z['grade'] = z['grade'].capitalize()
                assert z['grade'] in ['Correct', 'Partial', 'Incorrect']
                e = entries[z['id']]
                raw = e['reader_a_entry' if role == 'reader-a' else 'reader_b_entry']
                parts = z.get('material_parts', [])
                required = e['requested_fact_scope_entry']['material_requested_facts']
                assert collections.Counter(p['requirement'] for p in parts) == collections.Counter(required), z['id']
                for part in parts:
                    assert part['status'].lower() in ['covered', 'omitted', 'contradicted']
                    quote_fields = substantive_strings(raw) if (run / 'same-entry-grading-clarification.json').exists() else [raw['answer']]
                    assert all(any(quote in field for field in quote_fields) for quote in part.get('reader_quotes', [])), z['id']
                    if part['status'].lower() == 'covered':
                        assert part.get('reader_quotes'), z['id']
                if z['grade'] == 'Correct':
                    assert all(p['status'].lower() == 'covered' for p in parts), z['id']
                z.update(question=e['question_entry']['question'], expected_answer=e['key_entry']['expected_answer'],
                         observed_answer=raw['answer'], complete_raw_entry=raw,
                         requested_fact_scope=e['requested_fact_scope_entry'],
                         source_references=e['key_entry']['source_references'], block_id=block['block_id'], source_grade_report=str(report_path))
                all_grades[role].append(z)
    readers = {}
    for role, grades in all_grades.items():
        assert collections.Counter(x['id'] for x in grades) == collections.Counter(ids)
        by_id = {x['id']: x for x in grades}
        ordered = [by_id[qid] for qid in ids]
        readers[role] = dict(grades=ordered, counts={s: sum(x['grade'] == s for x in ordered)
                                                   for s in ['Correct', 'Partial', 'Incorrect']})
    passed = all(v['counts']['Correct'] == len(ids) and
                 all(not g.get('unsupported_guesses') and not g.get('unsupported_correct_guesses')
                     for g in v['grades']) for v in readers.values())
    result = dict(benchmark_version=bank_name, iteration=iteration, status='PASS' if passed else 'FAILED',
                  scope_qualified=True, normative_scope=read(bank / 'questions.json')['scope'],
                  grading_policy=read(bank / 'grading-scope.json'), readers=readers,
                  source_audit_and_reader_correctness_independent=True,
                  answer_key_source=packet['answer_key_source'],
                  independently_verified_publisher_email=False, complete_goal_achieved=False,
                  same_entry_grading_clarification=str(run / 'same-entry-grading-clarification.json') if (run / 'same-entry-grading-clarification.json').exists() else None)
    output = run / 'results.json'
    assert not output.exists(), 'Preserve original results'
    save(output, result)
    return {role: v['counts'] for role, v in readers.items()}

if __name__ == '__main__':
    command, bank_name, iteration = sys.argv[1:4]
    assert command in ['prepare', 'merge']
    print(json.dumps(prepare(bank_name, iteration) if command == 'prepare' else merge(bank_name, iteration), indent=2))
