"""Local, run-owned evidence helpers. Never edit shared registries or scripts."""
from pathlib import Path
import datetime
import difflib
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]

def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def provenance(agents, destination):
    records = []
    for p in Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/05').glob('*.jsonl'):
        meta = None
        for line in p.open():
            item = json.loads(line)
            if item.get('type') == 'session_meta':
                meta = item['payload']
                if meta.get('agent_path') not in agents or meta.get('parent_thread_id') != '01a1ab26-bd68-7da0-a839-5f50c7d304ef':
                    break
            if item.get('type') == 'turn_context' and meta:
                tc = item['payload']
                record = {'agent': meta['agent_path'], 'session_id': meta['id'],
                          'parent_thread_id': meta.get('parent_thread_id'),
                          'runtime_path': str(p), 'runtime_sha256': digest(p),
                          'actual_model': tc.get('model'), 'actual_effort': tc.get('effort'),
                          'runtime_timestamp': item['timestamp'],
                          'requested_model': agents[meta['agent_path']], 'requested_effort': 'high'}
                record['confirmed'] = record['actual_model'] == record['requested_model'] and record['actual_effort'] == 'high'
                records.append(record)
                break
    assert len(records) == len(agents), (agents, records)
    write(destination, {'runtime_verification': records, 'all_confirmed': all(x['confirmed'] for x in records),
                        'isolation': 'Fresh context, fork_turns=none; reader file access restricted by prompt, not OS sandbox.'})
    return records

def freeze(name, benchmark, previous=None):
    dest = ROOT / name
    dest.mkdir()
    shutil.copy2(REPO/'rules/dead-last.md', dest/'summary-snapshot.md')
    shutil.copy2(ROOT/benchmark/'questions.json', dest/'questions.json')
    paths = [dest/'summary-snapshot.md', dest/'questions.json', ROOT/benchmark/'answer-key.json',
             REPO/'extracted/dead-last-rules.txt', REPO/'source_pdfs/dead-last-rules.pdf']
    write(dest/'input-manifest.json', {'frozen_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'requested_model': 'gpt-6-luna', 'reasoning_effort': 'high',
          'hashes': {str(p): digest(p) for p in paths}})
    for letter in ['a','b']:
        template = (ROOT/'seed-iteration-01'/f'reader-{letter}-prompt.txt').read_text()
        prompt=template.replace(str(ROOT/'seed-iteration-01'), str(dest))
        policy=ROOT/'prompt-policy.json'
        if policy.exists() and json.loads(policy.read_text()).get('version2_used'):
            paragraph=json.loads(policy.read_text())['new_generic_paragraph']
            prompt=prompt.replace('For every question include:',paragraph+'\n\nFor every question include:')
            write(dest/'prompt-version.json',{'version':'blind-v2-self-check','paragraph':paragraph,'change':'Coordinator-authorized generic self-check, no question-specific hints.'})
        (dest/f'reader-{letter}-prompt.txt').write_text(prompt)
    if previous:
        old=(ROOT/previous/'summary-snapshot.md').read_text().splitlines(True)
        new=(dest/'summary-snapshot.md').read_text().splitlines(True)
        (dest/'summary-changes.patch').write_text(''.join(difflib.unified_diff(old,new,fromfile=previous,tofile=name)))
    return dest

def grade(name, benchmark, partials=None, incorrect=None, notes=None):
    partials = partials or {}; incorrect = incorrect or {}; notes = notes or {}
    dest=ROOT/name
    q=json.loads((dest/'questions.json').read_text())['questions']
    key=json.loads((ROOT/benchmark/'answer-key.json').read_text())['answers']
    kd={a['id']:a for a in key}; ids=[a['id'] for a in q]
    results={'benchmark': benchmark, 'standard':'All requested material parts, independently per answer. Grade the ruling, not support labels.', 'readers':{}}
    for reader in ['a','b']:
        raw=json.loads((dest/f'reader-{reader}.json').read_text())
        answers={a['id']:a for a in raw['answers']}
        assert len(answers)==len(raw['answers'])==len(ids) and set(answers)==set(ids)
        rows=[]
        for question in q:
            id=question['id']; index=(reader,id)
            g='partial' if id in partials.get(reader,{}) else 'incorrect' if id in incorrect.get(reader,{}) else 'correct'
            reason=partials.get(reader,{}).get(id) or incorrect.get(reader,{}).get(id) or notes.get(index)
            assert reason, ('Explicit per-answer evaluation reason required',reader,id)
            rows.append({'id':id,'question':question['question'],'expected_answer':kd[id]['answer'],
                'source_references':kd[id]['source_references'],'observed_answer':answers[id]['answer'],
                'reader_support':answers[id]['support'],'reader_evidence':answers[id]['evidence'],
                'grade':g,'reason':reason,'unsupported_guess':False})
        results['readers'][reader]={'grades':rows,'totals':{g:sum(a['grade']==g for a in rows) for g in ['correct','partial','incorrect']}}
    write(dest/'results.json',results)
    return results
