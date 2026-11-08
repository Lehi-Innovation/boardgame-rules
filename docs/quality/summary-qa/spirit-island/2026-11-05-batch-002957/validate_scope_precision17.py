"""Bind all focused classifications and proposed corrections to frozen inputs."""
from pathlib import Path
import hashlib
import json

B = Path(__file__).resolve().parent
S = B / 'scope-precision-17'
load = lambda p: json.loads(Path(p).read_text())
H = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
r, ledger, manifest = [load(S / n) for n in ['report.json', 'read-ledger.json', 'input-manifest.json']]
checks = []
def check(label, value):
    assert value, label
    checks.append(label)
for path, digest in manifest['canonical_current_files'].items():
    check('frozen bank input ' + path, H(path) == digest)
q, k, f = [load(B/'expanded-v22'/n) for n in ['questions.json','answer-key.json','asked-fact-map.json']]
byq = {x['id']:x for x in q['questions']}
byk = {x['id']:x for x in k['answers']}
byf = {x['id']:x for x in f['questions']}
focus = load(S/'focused-current-objects.json')['cases']
for case in focus:
    ident = case['question']['id']
    check('complete focused question ' + ident, case['question'] == byq[ident])
    check('complete focused key ' + ident, case['fixed_key'] == byk[ident])
    check('complete focused map ' + ident, case['asked_fact_map'] == byf[ident])
ids = [x['question']['id'] for x in focus]
check('all21 exact cases', len(ids) == len(set(ids)) == 21 and r['checked_question_ids'] == ids and [x['question_id'] for x in r['questions']] == ids)
for path, data in ledger['files'].items():
    p = Path(path); text = p.read_text()
    check('source file hash', H(p) == data['file_sha256'])
    check('source file lengths', p.stat().st_size == data['file_bytes'] and len(text) == data['unicode_characters'])
    pos = 0
    for d in data['deliveries']:
        start,end = d['range']
        check('contiguous bounded literal range', start == pos and 0 < end-start <= 6000)
        check('slice hash', hashlib.sha256(text[start:end].encode()).hexdigest() == d['slice_utf8_sha256'])
        check('slice delivery metadata', d['slice_characters'] == d['actual_received_unicode_characters'] == end-start and d['output_cap_tokens'] >= 4000 and d['truncated'] is False and d['actual_received_matches_literal'] is True)
        pos = end
    check('complete file coverage', pos == len(text))
for ident, ev in r['evidence'].items():
    p = Path(ev['source_path']); text = p.read_text(); start,end = ev['unicode_range']
    check('primary evidence file ' + ident, str(p) in ledger['files'] and H(p) == ev['file_sha256'])
    check('primary evidence literal ' + ident, text[start:end] == ev['passage'] and hashlib.sha256(ev['passage'].encode()).hexdigest() == ev['passage_utf8_sha256'])
facts = 0
for row in r['questions']:
    ident = row['question_id']; old = byf[ident]
    check('literal reviewed question ' + ident, row['literal_question'] == byq[ident]['question'])
    check('complete fixed key ' + ident, row['fixed_key_review']['entire_answer_reviewed'] == byk[ident]['answer'])
    check('all clauses once', len(row['clauses']) == len(old['requested_clauses']) and {x['clause_id'] for x in row['clauses']} == {x['clause_id'] for x in old['requested_clauses']})
    for clause in row['clauses']:
        prev = next(x for x in old['requested_clauses'] if x['clause_id'] == clause['clause_id'])
        check('literal clause', clause['actual_requested_clause'] == prev['actual_requested_clause'])
        check('every original fact index once', len(clause['facts']) == len(prev['required_facts']) and {x['fact_index'] for x in clause['facts']} == set(range(1,len(prev['required_facts'])+1)))
        for fact in clause['facts']:
            text = prev['required_facts'][fact['fact_index']-1]
            check('literal current fact', fact['current_text'] == text)
            pos = 0
            for part in fact['literal_partition']:
                start,end = part['fact_character_range']
                check('exact contiguous classification partition', start == pos and end > start and text[start:end] == part['literal_text'] and part['category'] in ['requested','background','premise','mixed_requested_and_background'])
                if part['category'] == 'mixed_requested_and_background':
                    check('explicit mixed-span explanation', ident == 'Q101' and fact['fact_index'] == 2 and bool(fact['mixed_span_explanation']))
                pos = end
            check('full original fact classified', pos == len(text)); facts += 1
            check('known cited evidence', all(x in r['evidence'] for x in fact['primary_evidence_ids']))
    check('all existing context classified', len(row['existing_key_context_review']) == len(old['key_context_not_required']) and [x['fact'] for x in row['existing_key_context_review']] == [x['fact'] for x in old['key_context_not_required']])
    check('no unresolved row', row['semantic_unresolved_questions'] == [])
for correction in r['consolidated_corrections']:
    ident = correction['question_id']; row = next(x for x in r['questions'] if x['question_id'] == ident)
    check('complete correction matches per-row proposal', correction == row['correction'] and row['decision'] == 'CORRECTION')
    check('no question or key mutation', correction['prompt_change'] is None and correction['fixed_key_answer_change'] is None)
    for clause in correction['requested_clauses']:
        prev = next(x for x in byf[ident]['requested_clauses'] if x['clause_id'] == clause['clause_id'])
        indices = clause['original_index_mapping']
        check('every old correction index accounted', len(indices) == len(prev['required_facts']) and {x['original_fact_index'] for x in indices} == set(range(1,len(prev['required_facts'])+1)))
        check('every replacement index accounted', {x['new_fact_index'] for x in indices if x['new_fact_index'] is not None} == set(range(1,len(clause['required_facts'])+1)))
    before = sum(len(x['required_facts']) for x in byf[ident]['requested_clauses'])
    after = sum(len(x['required_facts']) for x in correction['requested_clauses'])
    check('exact correction count delta', (before,after,after-before) == (correction['fact_count_before'],correction['fact_count_after'],correction['fact_count_delta']))
check('all78 fact entries classified', facts == 78)
check('all11 corrections and net minus3', len(r['consolidated_corrections']) == 11 and sum(x['fact_count_delta'] for x in r['consolidated_corrections']) == -3)
check('no reported key errors or unresolved cases', r['fixed_key_factual_errors'] == [] and r['semantic_unresolved_questions'] == [])
delivery = load(S/'actual-delivery-validation.json')
check('all91 actual literal deliveries independently verified', delivery['all_actual_source_slices_verified'] and sum(len(x['slices']) for x in delivery['graders'][0]['inputs']) == 91)
proof = {'all_passed':True,'check_count':len(checks),'checks':checks,'report_sha256':H(S/'report.json'),'ledger_sha256':H(S/'read-ledger.json'),'fact_entries_classified':facts,'literal_primary_citations':len(r['evidence']),'limitations':'Structural, literal reference and actual public delivery checks are not a substitute for semantic judgment or whole-corpus coverage review.'}
dest = S/'structural-reference-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({k:v for k,v in proof.items() if k != 'checks'}))
