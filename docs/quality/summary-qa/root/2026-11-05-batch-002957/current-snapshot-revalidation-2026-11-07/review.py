"""Display full applications and fixed key; bind exact quoted guide spans."""
from evidence import *

def show(side, start, end):
    raw = json.loads((I / f'reader-{side}.json').read_text())
    questions = {x['id']: x['question'] for x in json.loads((I / 'questions.json').read_text())['questions']}
    keys = {x['id']: x for x in json.loads((I / 'answer-key.json').read_text())['answers']}
    guide = (I / 'summary-snapshot.md').read_text()
    for entry in raw['answers'][start - 1:end]:
        qid = entry['id']
        selected = []
        for passage in entry.get('source_passages', []):
            quote = passage['quotation']
            assert quote and quote in guide
            a = guide.index(quote)
            selected.append({**{k: v for k, v in passage.items() if k != 'quotation'}, 'verbatim_quotation_lines_in_fully_read_guide': [guide.count('\n', 0, a) + 1, guide.count('\n', 0, a + len(quote)) + 1], 'quote_sha256': hashlib.sha256(quote.encode()).hexdigest(), 'boundary_quotes': [quote[:100], quote[-100:]]})
        view = {**entry, 'source_passages': selected}
        print(json.dumps({'reader': side, 'question': questions[qid], 'key': keys[qid], 'complete_original_entry': view}, ensure_ascii=False))

def grade(side, reasons):
    raw = json.loads((I / f'reader-{side}.json').read_text())
    questions = {x['id']: x for x in json.loads((I / 'questions.json').read_text())['questions']}
    keys = {x['id']: x for x in json.loads((I / 'answer-key.json').read_text())['answers']}
    entries = {x['id']: x for x in raw['answers']}
    guide = (I / 'summary-snapshot.md').read_text()
    for qid, decision in reasons.items():
        entry = entries[qid]
        grade, reason = decision
        assert grade in ['correct', 'partial', 'incorrect', 'borderline']
        record = {'reviewer': '/root', 'reader': side, 'id': qid, 'grade': grade, 'reason': reason, 'question': questions[qid], 'expected': keys[qid], 'observed_original_entry': entry, 'observed_entry_sha256': hashlib.sha256(js(entry).encode()).hexdigest(), 'every_substantive_field_reviewed': True, 'whole_entry_policy': True, 'quote_fidelity': all(p['quotation'] and p['quotation'] in guide for p in entry['source_passages']), 'unsupported_guess': False if grade == 'correct' else None, 'unresolved_requested_fact': False if grade == 'correct' else None}
        save(I / 'primary-grades' / f'{side}-{qid}.json', record)
    print(json.dumps({'reader': side, 'saved_primary_decisions': list(reasons)}))

if __name__ == '__main__':
    if sys.argv[1] == 'show':
        show(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]))
