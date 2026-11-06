from pathlib import Path
import copy
import hashlib
import json

D = Path(__file__).resolve().parent
P = D.parent
def read(path): return json.loads(path.read_text())
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
summary = (D/'summary-snapshot.md').read_text()
def encode_quote(original):
    metadata = None
    if isinstance(original, dict):
        metadata = copy.deepcopy(original)
        text = metadata.pop('text')
    else:
        text = original
    start = summary.index(text)
    assert summary[start:start+len(text)] == text
    return {'start':start,'end':start+len(text),'sha256_utf8':hashlib.sha256(text.encode()).hexdigest(),
            'original_quote_type':'object' if metadata is not None else 'string','original_quote_metadata':metadata}
def decode_quote(span):
    text = summary[span['start']:span['end']]
    if span['original_quote_type'] == 'object':
        result = copy.deepcopy(span['original_quote_metadata'])
        result['text'] = text
        return result
    return text
questions = read(D/'questions.json')['questions']
keys = {x['id']: x for x in read(P/'expanded-v11/answer-key.json')['answers']}
scope_data = read(P/'expanded-v11/grading-scope.json')
scope = {x['id']: x for x in scope_data['questions']}
raw = {who: read(D/f'reader-{who}.json') for who in ['a', 'b']}
ids = [x['id'] for x in questions]
readers = {}
for who, obj in raw.items():
    assert [x['id'] for x in obj['answers']] == ids
    readers[who] = {x['id']: x for x in obj['answers']}
records = []
quote_count = 0
answer_quote_count = 0
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
        for original_quote in quotes:
            quote_metadata = None
            if isinstance(original_quote, dict):
                quote_metadata = copy.deepcopy(original_quote)
                text = quote_metadata.pop('text')
            else:
                text = original_quote
            start = summary.index(text)
            end = start + len(text)
            assert summary[start:end] == text
            spans.append({'start': start, 'end': end, 'sha256_utf8': hashlib.sha256(text.encode()).hexdigest(),
                          'original_quote_type': 'object' if quote_metadata is not None else 'string',
                          'original_quote_metadata': quote_metadata})
            quote_count += 1
        entry['attached_verbatim_passage_spans'] = spans
        if 'answer_quotations' in entry:
            answer_quotes = entry.pop('answer_quotations')
            entry['answer_quotation_spans'] = [encode_quote(q) for q in answer_quotes]
            answer_quote_count += len(answer_quotes)
            joined = '\n\n'.join(q['text'] if isinstance(q,dict) else q for q in answer_quotes)
            if entry.get('answer') == joined:
                entry.pop('answer')
                entry['answer_transport'] = {'mode':'join_answer_quotations','separator':'\n\n'}
        rec['readers']['reader-'+who] = entry
    records.append(rec)
paths = [D/'summary-snapshot.md', D/'questions.json', D/'reader-a.json', D/'reader-b.json',
         P/'expanded-v11/answer-key.json', P/'expanded-v11/grading-scope.json']
package = {'description': 'Lossless grading transport: every original reader entry field is retained. Source text in verbatim_passages and answer_quotations is encoded as exact start:end Unicode character spans in the separately supplied complete summary, retaining original string/object representation and metadata. When answer is exactly its answer_quotations joined by blanklines, answer_transport records that exact join instead of duplicating text. Reconstruct answer_quotations from answer_quotation_spans, then reconstruct answer using the separator. Case results/numerical applications remain original literals. Every entire original entry is reconstructed and equality-checked. Each span belongs only to its own entry. No omitted content, answer edits or parent grades.',
           'inputs': [{'path': str(path), 'sha256': sha(path)} for path in paths],
           'rubric': scope_data['rubric'], 'global_constraints': scope_data['global_constraints'],
           'question_count': len(records), 'required_fact_count_per_reader': sum(len(r['required_facts']) for r in records),
           'attached_quote_count': quote_count, 'answer_quote_count':answer_quote_count, 'questions': records}
(D/'grading-input.json').write_text(json.dumps(package, ensure_ascii=False, separators=(',',':'))+'\n')
proof = {'all_original_reader_fields_preserved_except_lossless_quote_encoding': True, 'all_quotes_exact_summary_substrings': True,
         'question_count': len(records), 'attached_quote_count': quote_count, 'package_sha256': sha(D/'grading-input.json'),
         'answer_quote_count':answer_quote_count,
         'raw_reader_hashes': {who: sha(D/f'reader-{who}.json') for who in ['a','b']}}
# Reconstruct each original entry and compare the entire object, not just its answer.
for record in records:
    for who in ['a', 'b']:
        entry = copy.deepcopy(record['readers']['reader-'+who])
        spans = entry.pop('attached_verbatim_passage_spans')
        entry['verbatim_passages'] = []
        for x in spans:
            text = summary[x['start']:x['end']]
            if x['original_quote_type'] == 'object':
                quote = copy.deepcopy(x['original_quote_metadata'])
                quote['text'] = text
            else:
                quote = text
            entry['verbatim_passages'].append(quote)
        if 'answer_quotation_spans' in entry:
            answer_spans = entry.pop('answer_quotation_spans')
            entry['answer_quotations'] = [decode_quote(x) for x in answer_spans]
        if 'answer_transport' in entry:
            transport = entry.pop('answer_transport')
            assert transport['mode'] == 'join_answer_quotations'
            entry['answer'] = transport['separator'].join(q['text'] if isinstance(q,dict) else q for q in entry['answer_quotations'])
        assert entry == readers[who][record['id']]
proof['full_entry_reconstruction_equality'] = True
(D/'grading-input-losslessness.json').write_text(json.dumps(proof, indent=2)+'\n')
print(json.dumps(proof))
