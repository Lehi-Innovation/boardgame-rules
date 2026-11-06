from pathlib import Path
import copy
import hashlib
import json

D = Path(__file__).resolve().parent
P = D.parent
def read(path): return json.loads(path.read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
summary = (D/'summary-snapshot.md').read_text()
questions = read(D/'questions.json')['questions']
keys = {x['id']: x for x in read(P/'expanded-v9/answer-key.json')['answers']}
scope_data = read(P/'expanded-v9/grading-scope.json')
scope = {x['id']: x for x in scope_data['questions']}
raw = {who: read(D/f'reader-{who}.json') for who in ['a', 'b']}
ids = [x['id'] for x in questions]
readers = {}
for who, obj in raw.items():
    assert [x['id'] for x in obj['answers']] == ids
    readers[who] = {x['id']: x for x in obj['answers']}
records = []
quote_count = 0
for q in questions:
    id = q['id']
    sp = scope[id]
    rec = {'id': id, 'question': q['question'], 'fixed_expected_answer': keys[id]['expected_answer'],
           'source_references': sp['source_references'],
           'required_facts': [{'fact_id': x['fact_id'], 'expected_fact': x['expected_fact']} for x in sp['required_facts']],
           'contextual_exclusions': sp['contextual_exclusions'], 'semantic_notes': sp['semantic_notes'], 'readers': {}}
    for who in ['a', 'b']:
        entry = copy.deepcopy(readers[who][id])
        quotes = entry.pop('verbatim_passages')
        spans = []
        for text in quotes:
            start = summary.index(text)
            end = start + len(text)
            assert summary[start:end] == text
            spans.append({'start': start, 'end': end, 'sha256_utf8': hashlib.sha256(text.encode()).hexdigest()})
            quote_count += 1
        entry['attached_verbatim_passage_spans'] = spans
        rec['readers']['reader-'+who] = entry
    records.append(rec)
paths = [D/'summary-snapshot.md', D/'questions.json', D/'reader-a.json', D/'reader-b.json',
         P/'expanded-v9/answer-key.json', P/'expanded-v9/grading-scope.json']
package = {'description': 'Lossless grading transport: every original reader entry field is retained; only verbatim_passages strings are replaced by exact start:end Unicode character spans in the separately supplied complete summary. Each span belongs exclusively to its own answer. No omitted reader content, answer edits, or parent grades.',
           'inputs': [{'path': str(path), 'sha256': sha(path)} for path in paths],
           'rubric': scope_data['rubric'], 'global_constraints': scope_data['global_constraints'],
           'question_count': len(records), 'required_fact_count_per_reader': sum(len(r['required_facts']) for r in records),
           'attached_quote_count': quote_count, 'questions': records}
(D/'grading-input.json').write_text(json.dumps(package, ensure_ascii=False, separators=(',',':'))+'\n')
proof = {'all_original_reader_fields_preserved_except_lossless_quote_encoding': True, 'all_quotes_exact_summary_substrings': True,
         'question_count': len(records), 'attached_quote_count': quote_count, 'package_sha256': sha(D/'grading-input.json'),
         'raw_reader_hashes': {who: sha(D/f'reader-{who}.json') for who in ['a','b']}}
# Reconstruct each original entry and compare the entire object, not just its answer.
for record in records:
    for who in ['a', 'b']:
        entry = copy.deepcopy(record['readers']['reader-'+who])
        spans = entry.pop('attached_verbatim_passage_spans')
        entry['verbatim_passages'] = [summary[x['start']:x['end']] for x in spans]
        assert entry == readers[who][record['id']]
proof['full_entry_reconstruction_equality'] = True
(D/'grading-input-losslessness.json').write_text(json.dumps(proof, indent=2)+'\n')
print(json.dumps(proof))
