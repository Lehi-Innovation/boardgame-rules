from pathlib import Path
import ast, collections, copy, fnmatch, hashlib, io, json, posixpath, types

REAL_ROOT = Path(__file__).resolve().parent.parent
OWN = Path(__file__).resolve().parent
ALLOWED = [
    'single-reader-grading-tools.py', 'prove-single-reader-grading-delivery.py',
    'block-grading-tools.py', 'prove-bounded-delivery.py',
    'expanded-v12-complete-requested-scope/luna-iteration-05/single-reader-grading-dispatch-template.json',
    'expanded-v12-complete-requested-scope/luna-iteration-05/grading-dispatch-template.json',
]
SOURCES = {name: (REAL_ROOT / name).read_bytes() for name in ALLOWED}
INPUT_HASHES = {name: hashlib.sha256(value).hexdigest() for name, value in SOURCES.items()}
STORE, DIRS, WRITES, READS = {}, set(), [], []
CASES = []


class Writer(io.StringIO):
    def __init__(self, path):
        super().__init__()
        self.path = path
    def close(self):
        if not self.closed:
            STORE[self.path] = self.getvalue()
        super().close()


class MP:
    def __init__(self, path): self.path = str(path)
    def __str__(self): return self.path
    def __lt__(self, other): return self.path < str(other)
    def __truediv__(self, child): return MP(posixpath.join(self.path, str(child)))
    @property
    def name(self): return posixpath.basename(self.path)
    def exists(self): return self.path in STORE or self.path in DIRS
    def is_dir(self): return self.path in DIRS
    def mkdir(self, exist_ok=False):
        if self.exists() and not exist_ok: raise FileExistsError(self.path)
        DIRS.add(self.path)
    def read_text(self):
        READS.append(self.path)
        if self.path not in STORE: raise FileNotFoundError(self.path)
        return STORE[self.path]
    def read_bytes(self): return self.read_text().encode()
    def write_text(self, text):
        WRITES.append(self.path)
        STORE[self.path] = text
    def open(self, mode='r'):
        if mode == 'x':
            if self.exists(): raise FileExistsError(self.path)
            WRITES.append(self.path)
            STORE[self.path] = ''
            return Writer(self.path)
        if mode == 'r': return io.StringIO(self.read_text())
        raise AssertionError('Unexpected synthetic mode: ' + mode)
    def glob(self, pattern):
        prefix = self.path.rstrip('/') + '/'
        return [MP(p) for p in set(STORE) | DIRS
                if p.startswith(prefix) and '/' not in p[len(prefix):]
                and fnmatch.fnmatch(p[len(prefix):], pattern)]


def load_functions(name, bindings):
    module = types.ModuleType(name)
    module.__dict__.update(Path=MP, ROOT=MP('/synthetic'), collections=collections,
                           copy=copy, hashlib=hashlib, json=json, **bindings)
    tree = ast.parse(SOURCES[name])
    body = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    exec(compile(ast.Module(body=body, type_ignores=[]), name, 'exec'), module.__dict__)
    return module


PAIRED = load_functions('block-grading-tools.py', {})
BOUNDED = load_functions('prove-bounded-delivery.py', {})
SINGLE = load_functions('single-reader-grading-tools.py', {'base': PAIRED})
PROOF = load_functions('prove-single-reader-grading-delivery.py', {'base': BOUNDED})
# Every global used by imported functions points at the SAME virtual root/path class.
for module in [PAIRED, BOUNDED, SINGLE, PROOF]:
    module.ROOT = MP('/synthetic')
    module.Path = MP
assert SINGLE.base is PAIRED and PROOF.base is BOUNDED

RUN = '/synthetic/bank/run'
SUMMARY = '## Synthetic summary\nShared context alpha.\nShared context beta.\n'


def put(path, value): STORE[path] = json.dumps(value, ensure_ascii=False)
def get(path): return json.loads(STORE[path])
def sha(path): return hashlib.sha256(STORE[path].encode()).hexdigest()
def snapshot(): return copy.deepcopy((STORE, DIRS, WRITES, READS))
def restore(s):
    STORE.clear(); STORE.update(copy.deepcopy(s[0]))
    DIRS.clear(); DIRS.update(copy.deepcopy(s[1]))
    WRITES[:] = copy.deepcopy(s[2]); READS[:] = copy.deepcopy(s[3])
def case(name, **detail): CASES.append(dict(case=name, **detail))


def raw_entry(qid, role):
    return dict(id=qid, answer=f'Answer fact {role} {qid}.',
        clause_ledger=[dict(requested_clause='Synthetic requested phrase',
            supported_fact_or_case_result=f'Ledger fact {role} {qid}.')],
        case_conclusions=[f'Case result {role} {qid}.'],
        evidence=[dict(summary_location='Synthetic location', quote=f'Evidence fact {role} {qid}.')],
        support='supported', custom_opaque=dict(role=role, nested=['preserve', qid, {'unicode': 'λ'}]))


def setup(n=53, roles='a'):
    STORE.clear(); DIRS.clear(); WRITES.clear(); READS.clear()
    DIRS.update(['/synthetic', '/synthetic/bank', RUN])
    ids = [f'SYN{i:03}' for i in range(1, n + 1)]
    questions = [dict(id=qid, question='State four synthetic facts.') for qid in ids]
    put('/synthetic/bank/questions.json', dict(scope='Synthetic normative scope', questions=questions))
    put('/synthetic/bank/answer-key.json', dict(grading_standard='Synthetic standard', answers=[
        dict(id=qid, expected_answer='Synthetic expected content.', source_references='Synthetic reference') for qid in ids]))
    put('/synthetic/bank/requested-fact-scope-reviewed.json', dict(questions=[
        dict(id=qid, material_requested_facts=[f'Required atom {i} {qid}' for i in range(4)]) for qid in ids]))
    put('/synthetic/bank/grading-scope.json', dict(policy='Synthetic same-entry content policy'))
    STORE[RUN + '/summary-snapshot.md'] = SUMMARY
    for role in roles:
        put(RUN + f'/reader-{role}.json', dict(answers=[raw_entry(qid, role) for qid in ids]))
    return ids


def add_role(ids, role):
    put(RUN + f'/reader-{role}.json', dict(answers=[raw_entry(qid, role) for qid in ids]))


def write_reports(role):
    manifest = get(RUN + f'/grading-reader-{role}/packet-manifest.json')
    for b in manifest['blocks']:
        grades = []
        for qid in b['ids']:
            e = raw_entry(qid, role)
            quotes = [e['answer'], e['clause_ledger'][0]['supported_fact_or_case_result'],
                      e['case_conclusions'][0], e['evidence'][0]['quote']]
            grades.append(dict(id=qid, grade='Correct', reason='Synthetic classification only.',
                material_parts=[dict(requirement=f'Required atom {i} {qid}', status='covered', reader_quotes=[quote])
                                for i, quote in enumerate(quotes)], unsupported_guesses=[], summary_issue_if_any=None))
        put(RUN + f'/grading-reader-{role}/' + b['block_id'] + '/grades-same-entry.json',
            dict(block_id=b['block_id'], readers={f'reader-{role}': dict(grades=grades)}))


def reject(name, fn, expected=(AssertionError, ValueError, FileNotFoundError, FileExistsError, KeyError, TypeError)):
    original_readers = {p: t for p, t in STORE.items() if p.endswith(('reader-a.json', 'reader-b.json'))}
    original_results = STORE.get(RUN + '/results.json')
    try: fn()
    except expected as ex:
        assert original_readers == {p: t for p, t in STORE.items() if p.endswith(('reader-a.json', 'reader-b.json'))}
        assert STORE.get(RUN + '/results.json') == original_results
        case(name, rejected=True, exception=type(ex).__name__)
        return
    raise AssertionError('Unexpected acceptance: ' + name)


# Dispatch comparison is generic text only; no runtime data is loaded.
old = json.loads(SOURCES[ALLOWED[-1]])
new = json.loads(SOURCES[ALLOWED[-2]])
assert hashlib.sha256(old['template'].encode()).hexdigest() == old['template_sha256']
assert hashlib.sha256(new['template'].encode()).hexdigest() == new['template_sha256']
adapted = old['template']
for a, b in new['replacements'].items():
    assert a in adapted
    adapted = adapted.replace(a, b)
assert adapted == new['template']
case('dispatch semantic text unchanged except the four declared role/scheduling replacements', passed=True)

setup(113)
sizes = SINGLE.prepare('bank', 'run', 'a')
assert len(sizes) == 6 and sum(n for _, n in sizes) == 113 and all(15 <= n <= 20 for _, n in sizes)
case('synthetic 113-entry bank partitions into six complete 15–20 entry blocks', passed=True)

ids = setup()
blocks = SINGLE.prepare('bank', 'run', 'a')
assert len(blocks) == 3 and all(15 <= n <= 20 for _, n in blocks)
manifest = get(RUN + '/grading-reader-a/packet-manifest.json')
assert [x for b in manifest['blocks'] for x in b['ids']] == ids
assert not any('/reader-b.json' in p for p in READS)
for b in manifest['blocks']:
    packet = get(RUN + '/grading-reader-a/' + b['block_id'] + '/packet.json')
    for e in packet['entries']:
        assert e['reader_a_entry'] == raw_entry(e['id'], 'a') and 'reader_b_entry' not in e
case('A preparation uses only A, preserves full raw fields, and makes complete disjoint 15–20 blocks', passed=True)
write_reports('a')
before = copy.deepcopy((STORE, DIRS, WRITES))
r = SINGLE.validate_role('bank', 'run', 'a')
assert r['full_requested_atom_count'] == 4 * len(ids)
assert (STORE, DIRS, WRITES) == before
case('role validation is read-only and validates every atom across all four substantive fields', passed=True)
SINGLE.collect('bank', 'run', 'a')
reject('collection cannot overwrite an existing frozen collection', lambda: SINGLE.collect('bank', 'run', 'a'))
reject('full pair cannot combine before B is available', lambda: SINGLE.combine('bank', 'run'))
BASE_A = snapshot()

def first_report(): return RUN + '/grading-reader-a/block-01/grades-same-entry.json'
def mutate_report(fn):
    p = first_report(); report = get(p); fn(report); put(p, report)

for label, change in [
    ('missing requested atom', lambda g: g['material_parts'].pop()),
    ('duplicated requested atom', lambda g: g['material_parts'].append(copy.deepcopy(g['material_parts'][0]))),
    ('wrong requirement', lambda g: g['material_parts'][0].update(requirement='Unrequested synthetic atom')),
    ('empty evidence quote', lambda g: g['material_parts'][0].update(reader_quotes=[''])),
    ('metadata-only evidence quote', lambda g: g['material_parts'][0].update(reader_quotes=['Synthetic location'])),
    ('other-role evidence quote', lambda g: g['material_parts'][0].update(reader_quotes=['Answer fact b SYN001.'])),
    ('cross-question evidence quote', lambda g: g['material_parts'][0].update(reader_quotes=['Answer fact a SYN002.'])),
    ('Correct with an omitted atom', lambda g: g['material_parts'][0].update(status='omitted', reader_quotes=[])),
    ('invalid material status', lambda g: g['material_parts'][0].update(status='invalid')),
]:
    restore(BASE_A); mutate_report(lambda report, change=change: change(report['readers']['reader-a']['grades'][0]))
    reject(label + ' rejected', lambda: SINGLE.validate_role('bank', 'run', 'a'))

for label, change in [
    ('missing grade ID', lambda rv: rv['grades'].pop()),
    ('duplicated grade ID', lambda rv: rv['grades'].append(copy.deepcopy(rv['grades'][0]))),
    ('reordered grade IDs', lambda rv: rv['grades'].reverse()),
    ('unknown grade ID', lambda rv: rv['grades'][0].update(id='UNKNOWN_SYNTHETIC')),
]:
    restore(BASE_A); mutate_report(lambda report, change=change: change(report['readers']['reader-a']))
    reject(label + ' rejected', lambda: SINGLE.validate_role('bank', 'run', 'a'))

restore(BASE_A)
mutate_report(lambda report: report['readers'].update({'reader-b': copy.deepcopy(report['readers']['reader-a'])}))
reject('role report cannot include a second reader', lambda: SINGLE.validate_role('bank', 'run', 'a'))
restore(BASE_A); mutate_report(lambda report: report.update(block_id='WRONG'))
reject('role report wrong block identity rejected', lambda: SINGLE.validate_role('bank', 'run', 'a'))

for label, path, mutate in [
    ('raw', RUN + '/reader-a.json', lambda v: v['answers'][0].update(answer='Tampered raw text.')),
    ('question input', '/synthetic/bank/questions.json', lambda v: v['questions'][0].update(question='Changed wording.')),
    ('key input', '/synthetic/bank/answer-key.json', lambda v: v['answers'][0].update(expected_answer='Changed key.')),
    ('scope input', '/synthetic/bank/requested-fact-scope-reviewed.json', lambda v: v['questions'][0]['material_requested_facts'].append('Changed atom')),
]:
    restore(BASE_A); v = get(path); mutate(v); put(path, v)
    reject(label + ' tampering rejected', lambda: SINGLE.validate_role('bank', 'run', 'a'))

for label, mutation in [
    ('missing original ID', lambda a: a.pop()),
    ('duplicate original ID', lambda a: a.append(copy.deepcopy(a[0]))),
    ('reordered original IDs', lambda a: a.reverse()),
    ('unknown original ID', lambda a: a[0].update(id='UNKNOWN_SYNTHETIC')),
]:
    setup(); v = get(RUN + '/reader-a.json'); mutation(v['answers']); put(RUN + '/reader-a.json', v)
    reject(label + ' rejected before preparation/indexing', lambda: SINGLE.prepare('bank', 'run', 'a'))
    assert not MP(RUN + '/grading-reader-a').exists()

restore(BASE_A)
packet_path = RUN + '/grading-reader-a/block-01/packet.json'
v = get(packet_path); v['entries'][0]['reader_a_entry']['custom_opaque']['nested'].append('tampered'); put(packet_path, v)
reject('packet tampering rejected by packet hash', lambda: SINGLE.validate_role('bank', 'run', 'a'))
m = get(RUN + '/grading-reader-a/packet-manifest.json'); m['blocks'][0]['packet_sha256'] = sha(packet_path); put(RUN + '/grading-reader-a/packet-manifest.json', m)
reject('packet differs from original even if packet hash is updated', lambda: SINGLE.validate_role('bank', 'run', 'a'))

# Prepare B only after A has been collected; compare final combine with direct paired machinery.
restore(BASE_A); add_role(ids, 'b'); SINGLE.prepare('bank', 'run', 'b'); write_reports('b'); SINGLE.collect('bank', 'run', 'b')
BOTH = snapshot()
collection_path = RUN + '/reader-a-grading-results.json'
v = get(collection_path); v['grades'][0]['reason'] = 'Tampered collection'; put(collection_path, v)
reject('tampered frozen role collection rejected', lambda: SINGLE.combine('bank', 'run'))
restore(BOTH); mutate_report(lambda report: report['readers']['reader-a']['grades'][0].update(reason='Changed original report.'))
reject('grade report changed after collection rejected', lambda: SINGLE.combine('bank', 'run'))
restore(BOTH); original_reports = {p: v for p, v in STORE.items() if p.endswith(('grades-same-entry.json', 'grading-results.json'))}
counts = SINGLE.combine('bank', 'run'); result_combined = get(RUN + '/results.json')
assert all(STORE[p] == v for p, v in original_reports.items())
paired_reports = {p: v for p, v in STORE.items() if '/grading-blocks/' in p and p.endswith('/grades-same-entry.json')}
case('single-reader final combine preserves original reports/collections and both full raw entries', passed=True)
reject('combined results cannot be overwritten', lambda: SINGLE.combine('bank', 'run'))
restore(BOTH); PAIRED.prepare('bank', 'run')
STORE.update(paired_reports); direct_counts = PAIRED.merge('bank', 'run'); direct_result = get(RUN + '/results.json')
assert counts == direct_counts and result_combined == direct_result
case('full role aggregation exactly equals the original paired validator on identical inputs/reports', passed=True)


def call(code, name='exec_command'):
    return dict(type='response_item', payload=dict(type='function_call', name=name, arguments=code, call_id='synthetic'))
def output(text):
    return dict(type='response_item', payload=dict(type='function_call_output', output=text, call_id='synthetic'))


def build_logs(summary=None, mode='normal'):
    m = get(RUN + '/grading-reader-a/packet-manifest.json'); records = []
    for block in m['blocks']:
        packet = get(RUN + '/grading-reader-a/' + block['block_id'] + '/packet.json')
        metadata = {k: v for k, v in packet.items() if k != 'entries'}
        entries = copy.deepcopy(packet['entries']); log = []
        if mode == 'early_open_write': log.append(call("open('/synthetic/output.json','x').write('{}')"))
        log += [call('read summary'), output(STORE[RUN + '/summary-snapshot.md'] if summary is None else summary)]
        if mode != 'missing_metadata':
            shown = copy.deepcopy(metadata)
            if mode == 'wrong_metadata': shown['normative_scope'] = 'Wrong synthetic metadata'
            log += [call('read complete metadata'), output(json.dumps(shown, ensure_ascii=False))]
        for e in entries:
            if mode == 'partial_entry': del e['reader_a_entry']['custom_opaque']
            if mode == 'other_role_only': e['reader_b_entry'] = e.pop('reader_a_entry')
            reader_code = 'json.dump(entry, sys.stdout, ensure_ascii=False)' if mode == 'stdout_json_dump' else 'print complete entry'
            log += [call(reader_code), output(json.dumps(e, ensure_ascii=False))]
        if mode == 'other_role_extra':
            e = copy.deepcopy(entries[0]); e['reader_b_entry'] = e.pop('reader_a_entry')
            log += [call('print unrelated other-role input'), output(json.dumps(e, ensure_ascii=False))]
        if mode == 'known_early_write':
            log = [call("Path('/synthetic/output.json').write_text('{}')")] + log
        if mode == 'status_call': log.append(call('status request', name='list_agents'))
        log.append(call("Path('/synthetic/output.json').write_text('{}')"))
        runtime = '/synthetic/runtime-' + block['block_id'] + '.jsonl'
        STORE[runtime] = '\n'.join(json.dumps(x, ensure_ascii=False) for x in log) + '\n'
        records.append(dict(agent='/root/synthetic_a_' + block['block_id'].replace('block-', ''), runtime_source=runtime))
    put('/synthetic/model-provenance.json', dict(records=records))


proof_counter = 0
def prove_case(name, mode='normal', summary=None, expected=True, finding=None):
    global proof_counter
    build_logs(summary=summary, mode=mode); proof_counter += 1
    output_name = f'synthetic-proof-{proof_counter:02}.json'
    result = PROOF.prove('bank', 'run', 'a', 'synthetic_a', output_name)
    actual = all(x['complete_input_delivery_confirmed'] for x in result.values())
    assert actual == expected, (name, actual, result)
    case(name, delivery_complete=actual, finding=finding)
    return output_name


restore(BASE_A)
name = prove_case('full summary, all metadata and complete original role entries prove delivery')
reject('delivery proof cannot overwrite a prior proof', lambda: PROOF.prove('bank', 'run', 'a', 'synthetic_a', name))
prove_case('partial original role entry rejected', mode='partial_entry', expected=False)
prove_case('missing metadata rejected', mode='missing_metadata', expected=False)
prove_case('wrong metadata rejected', mode='wrong_metadata', expected=False)
prove_case('other-role-only entry cannot replace assigned reader entry', mode='other_role_only', expected=False)
prove_case('missing summary lines rejected', summary='## Synthetic summary\n', expected=False)
prove_case('recognized first-write pattern prevents late delivery', mode='known_early_write', expected=False)
prove_case('recognized collaboration/status call rejected', mode='status_call', expected=False)
prove_case('unrecognized early open/write wrongly permits post-write input delivery', mode='early_open_write', finding='SRG-01')
prove_case('stdout-only JSON transport wrongly treated as an output-file write', mode='stdout_json_dump', expected=False, finding='SRG-01')
prove_case('extra other-role input is not rejected when own inputs are complete', mode='other_role_extra', finding='SRG-02')
# The proof compares runtime to mutable current packet content, not the frozen manifest/original.
v = get(packet_path); del v['entries'][0]['reader_a_entry']['custom_opaque']; put(packet_path, v)
prove_case('tampered/cropped packet accepted by delivery proof without frozen hash binding', finding='SRG-03')
reject('role validator still rejects the tampered packet', lambda: SINGLE.validate_role('bank', 'run', 'a'))
setup()
STORE[RUN + '/summary-snapshot.md'] = '## Synthetic summary\nValue 1\n'
SINGLE.prepare('bank', 'run', 'a')
prove_case('changed/prefix-only summary line falsely counted as full original line', summary='## Synthetic summary\nValue 10\n', finding='SRG-04')

# No mutating helper ever received a real filesystem path or real ROOT.
assert all(str(m.ROOT) == '/synthetic' and m.Path is MP for m in [PAIRED, SINGLE, BOUNDED, PROOF])
result = dict(input_hashes=INPUT_HASHES, synthetic_only=True, real_runtime_or_reader_inputs_accessed=False,
              roots_all_virtual=True, case_count=len(CASES), cases=CASES)
with (OWN / 'synthetic-test-results-02.json').open('x') as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)
    handle.write('\n')
print(json.dumps(dict(case_count=len(CASES), reproduced_findings=sorted({c['finding'] for c in CASES if c.get('finding')}),
    strict_paired_equivalence=True, all_mutating_roots_virtual=True), indent=2))
