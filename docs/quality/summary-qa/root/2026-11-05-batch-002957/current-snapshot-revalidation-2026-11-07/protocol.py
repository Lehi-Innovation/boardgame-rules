"""Actual role/model/read-call checks, separate from factual grades."""
from evidence import *
import re

def main():
    data = runtime()
    pair = I.name
    checks = []
    actors = []
    def check(label, condition, detail=None):
        checks.append({'check': label, 'passed': bool(condition), 'detail': detail})
    check('Canonical and this pair exact current bytes', (ROOT / 'rules/root.md').read_bytes() == (I / 'summary-snapshot.md').read_bytes())
    for side in 'ab':
        task = READER_PREFIX + '_reader_' + side
        rec = next(x for x in data['records'] if x['agent_path'] == '/root/' + task)
        spawn = [x for x in data['dispatches'] if x['arguments_without_message'].get('task_name') == task]
        check(task + ' one explicit new none spawn', len(spawn) == 1 and spawn[0]['arguments_without_message'].get('fork_turns') == 'none')
        check(task + ' requested model/effort', spawn[0]['arguments_without_message'].get('model') == 'gpt-6-luna' and spawn[0]['arguments_without_message'].get('reasoning_effort') == 'high')
        check(task + ' all9 actual turns Luna/high', len(rec['turns']) == 9 and all(t['model'] == 'gpt-6-luna' and t['effort'] == 'high' for t in rec['turns']))
        check(task + ' actual child parent identity', rec['session_meta']['payload']['parent_thread_id'] == PARENT)
        forbidden = []
        call_rows = []
        for line in Path(rec['runtime_path']).open():
            event = json.loads(line)
            p = event.get('payload', {})
            if p.get('type') not in ('custom_tool_call', 'function_call'):
                continue
            code = p.get('input', p.get('arguments', ''))
            code = code if isinstance(code, str) else json.dumps(code)
            patterns = r'tools\.(?:web|mcp|list_mcp|get_goal)|collaboration\.|ALL_TOOLS|answer-key\.json|source_pdfs/|extracted/root|progress\.json|source-audit|benchmark-v\d|git\s+status|(?:read|wait|list)_threads|/\.codex/sessions'
            hits = re.findall(patterns, code)
            peer = 'b' if side == 'a' else 'a'
            for forbidden_path in (f'reader-{peer}.json', 'rules/root.md', 'README.md', 'CLAUDE.md', 'input-manifest.json', 'working-state.json', 'results-primary.json'):
                if forbidden_path in code:
                    hits.append(forbidden_path)
            if hits:
                forbidden.append({'ordinal': event.get('ordinal'), 'matches': hits})
            call_rows.append({'ordinal': event.get('ordinal'), 'call_id': p.get('call_id'), 'name': p.get('name'), 'code': code})
        check(task + ' no observed source/key/status/peer/web tool calls', not forbidden, forbidden)
        actors.append({**rec, 'spawn_evidence': spawn, 'actual_tool_calls': call_rows, 'restriction_review_limits': 'Runtime code scanned for source/key/status/peer/web operations and retained for inspection. This is instruction-based isolation with actual calls, not filesystem jailing or proof against prior model knowledge.'})
        delivery = json.loads((I / ('reader-' + side + '-delivery-completed/delivery-audit.json')).read_text())
        check(task + ' final actual complete literal inputs delivered', delivery['status'] == 'PASS')
        check(task + ' raw actual delivery pairs intact', all(sha(x['raw_path']) == x['raw_sha256'] for x in delivery['read_calls']))
    check('New independent reader identities', len({r['session_id'] for r in actors}) == 2)
    freeze = json.loads((I / 'raw-output-manifest.json').read_text())
    if pair == 'iteration-02':
        check('Both full originals before ANY semantic grading', freeze['existing_primary_count'] == 0)
    else:
        check('Initial early grading chronology fully disclosed/preserved', freeze['existing_primary_count'] == 90 and (I / 'grading-chronology-deviation.json').exists())
    for task in ('current18_pure_source_auditor', 'current18_neutral'):
        rec = next(x for x in data['records'] if x['agent_path'] == '/root/' + task)
        spawn = next(x for x in data['dispatches'] if x['arguments_without_message'].get('task_name') == task)
        check(task + ' new none spawn', spawn['arguments_without_message'].get('fork_turns') == 'none')
        check(task + ' actual Sol6.1/high', all(t['model'] == 'gpt-6.1-sol' and t['effort'] == 'high' for t in rec['turns']))
    check('Parent actual current Sol6.1/high contexts', bool(data['parent_current_turn_contexts']) and all(t['model'] == 'gpt-6.1-sol' and t['effort'] == 'high' for t in data['parent_current_turn_contexts']))
    note = {'pair': pair, 'status': 'PASS' if all(x['passed'] for x in checks) else 'REVIEW', 'passed': sum(x['passed'] for x in checks), 'total': len(checks), 'checks': checks, 'actors': actors, 'runtime_dispatch_provenance': data, 'prompt_provenance_limit': 'Initial plaintext copies prospectively frozen. Runtime encrypts message bodies; retain exact ciphertext hashes and clear dispatch fields without claiming independently computed plaintext/ciphertext equality. Actual iteration02 B adds one redundant access restriction sentence; prompt-repetition-disclosure.json records it; operative instructions and rule data identical, byte-identical actual messages not claimed.'}
    save(I / 'protocol-validation.json', note)
    print(json.dumps({'status': note['status'], 'passed': note['passed'], 'total': note['total'], 'failures': [x for x in checks if not x['passed']]}))

if __name__ == '__main__':
    main()
