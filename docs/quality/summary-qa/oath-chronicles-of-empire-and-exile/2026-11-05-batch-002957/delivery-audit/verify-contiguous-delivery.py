"""Verify actual model-visible text chunks from this task's runtime records."""
import hashlib
import json
from pathlib import Path
import re
import sys

EVIDENCE = Path(__file__).resolve().parent.parent
TARGETS = sys.argv[1:] or ["expanded03_reader_a", "expanded03_reader_b", "final_source_auditor_03"]
FILES = [EVIDENCE / "expanded-iteration-03/summary-snapshot.md",
         EVIDENCE / "expanded-iteration-03/questions.json",
         Path('/home/jonny/projects/boardgame-rules/extracted/oath-current-law.txt'),
         Path('/home/jonny/projects/boardgame-rules/extracted/oath-current-playbook.txt'),
         EVIDENCE / 'errata.txt', EVIDENCE / 'expanded-v5/answer-key.json',
         EVIDENCE / 'coverage-ledger.json', EVIDENCE / 'expanded-iteration-03/grading-input.json']
BASE_INPUTS = {p.name: (p, p.read_text()) for p in FILES}
for session in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*.jsonl'):
    with session.open() as f:
        meta = json.loads(f.readline()).get('payload', {})
    if meta.get('parent_thread_id') != '01a1aad5-d462-7b90-9cb0-ed14a110aee7':
        continue
    agent = meta.get('agent_path', '').split('/')[-1]
    if agent == 'coverage_challenge_08':
        if 'coverage_challenge_08__v9' in TARGETS:
            agent = 'coverage_challenge_08__v9'
        elif 'coverage_challenge_08__v8' in TARGETS:
            agent = 'coverage_challenge_08__v8'
    if agent not in TARGETS:
        continue
    INPUTS = dict(BASE_INPUTS)
    if agent == 'coverage_challenge_06':
        p = EVIDENCE/'coverage-ledger-reviewed-06.json'
        INPUTS['coverage-ledger.json'] = (p, p.read_text())
    if agent == 'coverage_challenge_07':
        for p in [EVIDENCE/'expanded-v6/questions.json', EVIDENCE/'expanded-v6/answer-key.json', EVIDENCE/'coverage-ledger-reviewed-07.json']:
            INPUTS[p.name] = (p, p.read_text())
    if agent == 'coverage_challenge_08':
        for p in [EVIDENCE/'expanded-v7/questions.json', EVIDENCE/'expanded-v7/answer-key.json', EVIDENCE/'coverage-ledger-reviewed-08.json']:
            INPUTS[p.name] = (p, p.read_text())
    if agent == 'coverage_challenge_08__v8':
        for p in [EVIDENCE/'expanded-v8/questions.json', EVIDENCE/'expanded-v8/answer-key.json', EVIDENCE/'coverage-ledger-reviewed-08-v8.json']:
            INPUTS[p.name] = (p, p.read_text())
    if agent == 'coverage_challenge_08__v9':
        for p in [EVIDENCE/'expanded-v9/questions.json', EVIDENCE/'expanded-v9/answer-key.json', EVIDENCE/'coverage-ledger-reviewed-08-v9.json']:
            INPUTS[p.name] = (p, p.read_text())
    if agent == 'coverage_challenge_10':
        for p in [EVIDENCE/'expanded-v11/questions.json', EVIDENCE/'expanded-v11/answer-key.json', EVIDENCE/'coverage-ledger-reviewed-10.json']:
            INPUTS[p.name] = (p, p.read_text())
    if agent == 'scope_adjudicator_09':
        for p in [EVIDENCE/'expanded-iteration-08/summary-snapshot.md', EVIDENCE/'expanded-iteration-08/scope-review-packet-09.json']:
            INPUTS[p.name] = (p, p.read_text())
    block_match = re.fullmatch(r'block(\d+)_grader_(\d+)',agent)
    if block_match:
        num,blocknum=map(int,block_match.groups())
        for p in [EVIDENCE/f'expanded-iteration-{num:02d}'/'summary-snapshot.md',EVIDENCE/f'expanded-iteration-{num:02d}'/'grading-blocks'/f'block-{blocknum:02d}'/'packet.json']:
            INPUTS[p.name]=(p,p.read_text())
    iteration_match = re.match(r'^(?:expanded(\d+)_|full(\d+)_grader(?:_v\d+)?$|final_source_auditor_(\d+)$)', agent)
    if iteration_match:
        number = next(int(x) for x in iteration_match.groups() if x is not None)
        iteration_dir = EVIDENCE/f'expanded-iteration-{number:02d}'
        for p in [iteration_dir/'summary-snapshot.md', iteration_dir/'questions.json', iteration_dir/'grading-input.json', iteration_dir/'grading-input.v3.json']:
            if p.exists():
                INPUTS[p.name] = (p, p.read_text())
    events = [json.loads(line) for line in session.open()]
    if agent in ['coverage_challenge_08','coverage_challenge_08__v8','coverage_challenge_08__v9']:
        phase_start = next((i for i,e in enumerate(events) if 'Please verify final source-only correction.' in str(e.get('payload', {}))), None)
        v9_start = next((i for i,e in enumerate(events) if 'Final material-fact correction in expanded-v9 is now frozen.' in str(e.get('payload', {}))), None)
        if agent.endswith('__v9') and v9_start is not None:
            events = events[v9_start+1:]
        elif agent.endswith('__v8') and phase_start is not None:
            events = events[phase_start+1:v9_start]
        elif phase_start is not None:
            events = events[:phase_start]
    records, chunks, truncations = [], [], []
    for event in events:
        item = event.get('payload', {})
        if item.get('type') == 'custom_tool_call':
            records.append({'kind': 'call', 'call_id': item['call_id'], 'input': item.get('input')})
        elif item.get('type') == 'custom_tool_call_output':
            texts = [block.get('text', '') for block in item.get('output', []) if block.get('type') == 'input_text']
            records.append({'kind': 'output', 'call_id': item['call_id'], 'texts': texts})
            for text in texts:
                # text(result) serializes the exec result; text(result.output) does not.
                try:
                    wrapper = json.loads(text)
                    if isinstance(wrapper, dict) and isinstance(wrapper.get('output'), str):
                        text = wrapper['output']
                except (ValueError, TypeError):
                    pass
                if re.search(r'Warning: truncated output|tokens truncated|Output exceeded', text):
                    truncations.append(item['call_id'])
                if agent == 'scope_adjudicator_09':
                    for marker in re.finditer(r'^=== (packet|summary) chunk \d+/\d+ chars (\d+):(\d+) ===\n', text, re.M):
                        name = 'scope-review-packet-09.json' if marker[1] == 'packet' else 'summary-snapshot.md'
                        a,b = int(marker[2]),int(marker[3])
                        expected = INPUTS[name][1]
                        actual = text[marker.end():marker.end()+(b-a)]
                        chunks.append({'file':name,'start':a,'end':b,'total':len(expected),'exact_model_visible_text':actual == expected[a:b],'call_id':item['call_id']})
                for marker in re.finditer(r'^.*\bBEGIN\b[^\n]*\n', text, re.M):
                    line = marker.group()
                    start = re.search(r'\bstart[\"\s]*[=:]\s*(\d+)', line)
                    end = re.search(r'\bend[\"\s]*[=:]\s*(\d+)', line)
                    bracket_range = re.search(r'\bchars\[(\d+):(\d+)\]', line)
                    if bracket_range and not (start and end):
                        start = re.match(r'(\d+)', bracket_range[1])
                        end = re.match(r'(\d+)', bracket_range[2])
                    name = next((name for name in INPUTS if name in line), None)
                    if not (start and end and name):
                        continue
                    a, b = int(start[1]), int(end[1])
                    total = re.search(r'\btotal(?:_length)?[\"\s]*[=:]\s*(\d+)', line)
                    representation = INPUTS[name][1]
                    raw = INPUTS[name][0].read_bytes().decode('utf-8')
                    if total and int(total[1]) == len(raw):
                        representation = raw
                    expected = representation[a:b]
                    actual = text[marker.end():marker.end() + (b-a)]
                    convention = 'zero_based_half_open'
                    if actual != expected and a >= 1:
                        inclusive_actual = text[marker.end():marker.end() + (b-a+1)]
                        inclusive_expected = representation[a-1:b]
                        if inclusive_actual == inclusive_expected:
                            a -= 1
                            actual,expected = inclusive_actual,inclusive_expected
                            convention = 'one_based_inclusive_normalized_to_half_open'
                    chunks.append({'file': name, 'start': a, 'end': b,
                                   'total': len(representation), 'marker_convention':convention,
                                   'exact_model_visible_text': actual == expected,
                                   'call_id': item['call_id']})
    if agent == 'scope_adjudicator_09':
        required = ['summary-snapshot.md','scope-review-packet-09.json']
    elif agent in ['coverage_challenge_08__v8','coverage_challenge_08__v9']:
        required = ['questions.json', 'answer-key.json', 'coverage-ledger-reviewed-08-v9.json' if agent.endswith('__v9') else 'coverage-ledger-reviewed-08-v8.json']
    elif block_match:
        required = ['summary-snapshot.md','packet.json']
    elif agent == 'seed_grader' or re.fullmatch(r'full\d+_grader(?:_v\d+)?', agent):
        required = ['summary-snapshot.md', 'grading-input.v3.json' if agent.endswith('_v3') else 'grading-input.json']
    elif 'reader' in agent:
        required = ['summary-snapshot.md', 'questions.json']
    elif 'coverage' in agent:
        ledger_name = 'coverage-ledger-reviewed-10.json' if agent.endswith('_10') else ('coverage-ledger-reviewed-08.json' if agent.endswith('_08') else ('coverage-ledger-reviewed-07.json' if agent.endswith('_07') else 'coverage-ledger.json'))
        required = ['oath-current-law.txt', 'oath-current-playbook.txt', 'errata.txt', 'questions.json', 'answer-key.json', ledger_name]
    else:
        required = ['summary-snapshot.md', 'oath-current-law.txt', 'oath-current-playbook.txt', 'errata.txt']
    coverage = []
    for name in required:
        path, expected = INPUTS[name]
        totals = {c['total'] for c in chunks if c['file'] == name and c['exact_model_visible_text']}
        raw = path.read_bytes().decode('utf-8')
        if len(raw) in totals:
            expected = raw
        cursor, gaps = 0, []
        ranges = sorted((c['start'], c['end']) for c in chunks if c['file'] == name and c['exact_model_visible_text'])
        for a, b in ranges:
            if a > cursor:
                gaps.append([cursor, a])
            cursor = max(cursor, b)
        if cursor < len(expected):
            gaps.append([cursor, len(expected)])
        coverage.append({'file': name, 'path': str(path), 'characters': len(expected),
                         'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                         'verified_ranges': ranges, 'gaps': gaps, 'complete': not gaps})
    input_chunk_calls = {c['call_id'] for c in chunks}
    report = {'agent': agent, 'session': str(session), 'status': 'PASS' if all(c['complete'] for c in coverage) else 'INCOMPLETE_OR_FAILED',
              'coverage': coverage, 'chunks': chunks, 'truncated_calls': truncations,
              'failed_chunk_attempts': [c for c in chunks if not c['exact_model_visible_text']],
              'truncated_input_chunk_calls': [c for c in truncations if c in input_chunk_calls],
              'other_truncated_calls': [c for c in truncations if c not in input_chunk_calls],
              'criterion': 'Every required input character is proven present in exact model-visible chunks; failed attempts do not count toward coverage and may be replaced by complete exact redelivery. Other truncated draft/debug output is retained separately; it does not remove already delivered input characters.'}
    (EVIDENCE / 'delivery-audit' / (agent + '.actual-tool-records.json')).write_text(json.dumps(records, indent=2))
    (EVIDENCE / 'delivery-audit' / (agent + '.verified-delivery.json')).write_text(json.dumps(report, indent=2))
    print(agent, report['status'], [(c['file'], c['gaps']) for c in coverage], 'truncated', len(truncations))
