"""Verify literal inputs arrived before the first saved answer group."""
from evidence import *
import re

def main():
    spec = importlib.util.spec_from_file_location('delivery_helper', R / 'audit_full_publisher_delivery.py')
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    provenance = runtime()
    reports = []
    for side in 'ab':
        rec = next(x for x in provenance['records'] if x['agent_path'] == '/root/' + READER_PREFIX + '_reader_' + side)
        writes = []
        for line in Path(rec['runtime_path']).open():
            event = json.loads(line)
            p = event.get('payload', {})
            code = p.get('input', p.get('arguments', ''))
            code = code if isinstance(code, str) else json.dumps(code)
            if p.get('type') in ('custom_tool_call', 'function_call') and f'reader-{side}.json' in code and re.search(r'\.write_text\(|\.write_bytes\(|json\.dump\(|cat\s*>', code):
                writes.append(event)
        assert writes, 'First saved output call must be observed'
        first = min(writes, key=lambda x: x['ordinal'])
        out = I / ('reader-' + side + '-input-before-first-save')
        blocks, calls, images = h.collect(Path(rec['runtime_path']), out)
        initial = [x for x in blocks if x['record']['output_ordinal'] < first['ordinal']]
        inputs = [h.coverage(I / name, initial, selector=lambda code, name=name: name in code) for name in ('summary-snapshot.md', 'questions.json')]
        report = {'status': 'PASS' if all(x['all_nonempty_lines_in_ordered_exact_blocks'] for x in inputs) else 'INCOMPLETE', 'agent_path': rec['agent_path'], 'runtime_path': rec['runtime_path'], 'first_saved_answer_call_ordinal': first['ordinal'], 'first_saved_answer_call_timestamp': first['timestamp'], 'actual_first_save_call': first, 'inputs': inputs, 'read_calls': [c for c in calls if c['output_ordinal'] < first['ordinal']], 'method': 'Actual input-read output blocks delivered before first saved-answer group. JSON transport decoded; only explicit declared line-number prefixes removed; otherwise exact ordered source lines. Establishes literal availability before first saved output, not cognitive attention or internal reasoning chronology.'}
        save(out / 'delivery-audit.json', report)
        reports.append({'reader': side, 'status': report['status'], 'first_save_ordinal': first['ordinal'], 'missing': [(Path(x['path']).name, len(x['unmatched_nonempty_lines_in_ordered_blocks'])) for x in inputs]})
    print(json.dumps(reports))

if __name__ == '__main__':
    main()
