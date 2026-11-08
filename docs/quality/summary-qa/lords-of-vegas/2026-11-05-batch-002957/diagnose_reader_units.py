"""Mechanical excerpt/inventory-field diagnostics; does not assign factual grades."""
from pathlib import Path
import json
import re
import sys
from quote_texts import quote_texts

R = Path(__file__).parent
D = R / sys.argv[1]
text = (D / 'summary-snapshot.md').read_text()
headings = [(m.start(), len(m.group(1)), m.group(2))
            for m in re.finditer(r'^(#{1,6}) (.+)$', text, re.M)]
units = {}
for start, level, title in headings:
    if level not in [2, 3]:
        continue
    end = next((s for s, l, _ in headings if s > start and l <= level), len(text))
    units[text[start:end].strip()] = title
result = {'factual_grades_assigned': False, 'readers': {}}
for label in 'ab':
    data = json.loads((D / f'reader-{label}.json').read_text())
    entries = []
    for answer in data['answers']:
        quotes = quote_texts(answer['operative_quotes'])
        entries.append({
            'id': answer['id'],
            'all_quotes_verbatim': all(q in text for q in quotes),
            'all_quotes_complete_heading_units': all(q.strip() in units for q in quotes),
            'heading_titles': [units.get(q.strip()) for q in quotes],
            'all_clauses_have_direct_rulings': all(isinstance(c, dict) and c.get('ruling')
                                                   for c in answer['clauses']),
            'case_check_present': 'case_check' in answer,
            'shared_rendered_result_consistent': (
                isinstance(answer.get('case_check'), dict)
                and answer['case_check'].get('checked_result') == answer['answer']
                and all(c.get('ruling') == answer['answer'] for c in answer['clauses'])
            ),
        })
    result['readers'][label] = entries
(D / 'reader-format-diagnostics.json').write_text(json.dumps(result, indent=2) + '\n')
print({label: {'answers': len(entries),
               'quote_unit_warnings': [e['id'] for e in entries
                                       if not e['all_quotes_complete_heading_units']],
               'missing_case_check': [e['id'] for e in entries if not e['case_check_present']]}
       for label, entries in result['readers'].items()})
