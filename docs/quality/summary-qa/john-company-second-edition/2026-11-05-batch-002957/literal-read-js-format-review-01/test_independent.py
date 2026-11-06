"""Independent neutral prospective tests. Never invokes an actual proof or shell read."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys
from types import SimpleNamespace

sys.dont_write_bytecode = True
OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
PROP = ROOT / 'literal-read-js-format-proposal-01'
SOURCE = PROP / 'read_call_format_proposal.py'
ORIGINALS = [ROOT / 'prove-single-reader-grading-delivery-literal-equivalent.py',
             ROOT / 'prove-bounded-delivery.py']

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

inputs = {str(p): digest(p) for p in sorted(PROP.rglob('*')) if p.is_file()}
inputs.update({str(p): digest(p) for p in ORIGINALS})
(OUT / 'input-hashes.json').write_text(json.dumps(inputs, indent=2) + '\n')

spec = importlib.util.spec_from_file_location('independent_format_proposal', SOURCE)
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
results = []
fixtures = []

def check(name, condition, detail=None, group='parser'):
    results.append(dict(name=name, group=group, passed=bool(condition), detail=detail))

def canonical(command):
    return ('const r = await tools.exec_command({cmd: ' + json.dumps(command)
            + ', max_output_tokens: 24000});\ntext(r.output);')

def body(first, second=None):
    return ('const r = await tools.exec_command({cmd: ' + first
            + ('' if second is None else ' + ' + second)
            + ', max_output_tokens: 24000});\ntext(r.output);')

def accept(name, source, command):
    actual = p.canonical_read_body(source)
    check(name, actual == canonical(command), {'source': source, 'actual': actual})
    fixtures.append(dict(name=name, body=source, expected=canonical(command)))

def reject(name, source):
    actual = p.canonical_read_body(source)
    check(name, actual is None, {'source': source, 'actual': actual})
    fixtures.append(dict(name=name, body=source, expected=None))

plain = canonical('neutral')
accept('one-literal', plain, 'neutral')
accept('two-literals', body('"neu"', '"tral"'), 'neutral')
accept('empty-one-literal', body('""'), '')
accept('empty-two-literals', body('""', '""'), '')
for label, ws in [('space', ' '), ('tab', '\t'), ('LF', '\n'), ('CR', '\r'),
                  ('CRLF', '\r\n'), ('VT', '\v'), ('FF', '\f')]:
    tokens = ['const', 'r', '=', 'await', 'tools', '.', 'exec_command', '(', '{',
              '"cmd"', ':', '"neutral"', ',', '"max_output_tokens"', ':', '24000',
              '}', ')', ';', 'text', '(', 'r', '.', 'output', ')', ';']
    accept('whitespace-' + label, ws + ws.join(tokens) + ws, 'neutral')
accept('compact', 'const r=await tools.exec_command({cmd:"neutral",max_output_tokens:24000});text(r.output);', 'neutral')
accept('quoted-keys', plain.replace('cmd:', '"cmd":').replace('max_output_tokens:', '"max_output_tokens":'), 'neutral')
for name, token, command in [
    ('all-json-escapes', r'"\"\\\/\b\f\n\r\t"', '"\\/\b\f\n\r\t'),
    ('unicode-escape', r'"n\u0065utral"', 'neutral'),
    ('escaped-line-separators', r'"\u2028\u2029"', '\u2028\u2029'),
    ('paired-surrogate', r'"\uD83D\uDE80"', '\U0001f680'),
    ('raw-unicode', '"café 🚀"', 'café 🚀'),
    ('nul-static-data', r'"\u0000"', '\0'),
    ('code-looking-data', json.dumps('"}); text(await tools.exec_command({cmd:"touch sentinel"})); // ${x} `x` ; $(x) /*x*/'), '"}); text(await tools.exec_command({cmd:"touch sentinel"})); // ${x} `x` ; $(x) /*x*/')]:
    accept(name, body(token), command)

negative_literals = [
    ('single-quote', "'neutral'"), ('template', '`neutral`'), ('interpolation', '`${neutral}`'),
    ('variable', 'neutral'), ('call', 'getCommand()'), ('json-parse', 'JSON.parse("neutral")'),
    ('parenthesized', '("neutral")'), ('third-literal', '"ne" + "ut" + "ral"'),
    ('dynamic-concat', '"neutral" + tail'), ('unary', '+"neutral"'),
    ('hex-escape', r'"\x6e"'), ('octal-escape', r'"\156"'), ('unknown-escape', r'"\q"'),
    ('js-nul-escape', r'"\0"'), ('escaped-single-quote', r'"\'"'),
    ('escaped-newline', '"ne\\\nutral"'), ('escaped-crlf', '"ne\\\r\nutral"'),
    ('short-unicode', r'"\u012"'), ('bad-unicode', r'"\uXX00"'),
    ('unicode-codepoint', r'"\u{006e}"'), ('unterminated', '"neutral'),
    ('bare-quote', '"neu"tral"'), ('bare-backslash', '"neutral\\"'),
    ('raw-newline', '"neu\ntral"'), ('raw-tab', '"neu\ttral"'), ('raw-nul', '"neu\0tral"'),
    ('raw-ls', '"neu\u2028tral"'), ('raw-ps', '"neu\u2029tral"'),
    ('lone-high-surrogate', r'"\ud800"'), ('lone-low-surrogate', r'"\udfff"'),
    ('split-surrogate-pair', r'"\ud83d" + "\ude80"'),
    ('raw-surrogate', '"\ud800"'), ('nonstring-null', 'null'), ('array', '["neutral"]')]
for name, token in negative_literals:
    reject(name, body(token))

mutations = {
    'prefix-code': 'void 0; ' + plain,
    'suffix-code': plain + '\ntext("extra");',
    'extra-exec': plain + '\n' + canonical('extra'),
    'extra-semicolon': plain + ';',
    'leading-comment': '// comment\n' + plain,
    'block-comment': '/* comment */' + plain,
    'inline-comment': plain.replace('cmd:', 'cmd: /*comment*/'),
    'line-comment': plain.replace('cmd:', 'cmd: //comment\n'),
    'trailing-comment': plain + '// comment',
    'const-merged': plain.replace('const r', 'constr'),
    'await-merged': plain.replace('await tools', 'awaittools'),
    'let': plain.replace('const r', 'let r'),
    'different-var': plain.replace('const r', 'const result'),
    'extra-declaration': plain.replace('const r =', 'const x = 0, r ='),
    'no-await': plain.replace('await ', ''),
    'wrong-tool': plain.replace('exec_command', 'exec'),
    'computed-tool': plain.replace('.exec_command', '["exec_command"]'),
    'optional-chaining': plain.replace('.exec_command', '?.exec_command'),
    'extra-argument': plain.replace('24000});', '24000}, {});'),
    'extra-key': plain.replace('24000}', '24000, cwd: "/tmp"}'),
    'duplicate-cmd': plain.replace('24000}', '24000, cmd: "extra"}'),
    'duplicate-budget': plain.replace('24000}', '24000, max_output_tokens: 24000}'),
    'prototype': plain.replace('24000}', '24000, __proto__: {}}'),
    'constructor': plain.replace('24000}', '24000, constructor: Object}'),
    'spread': plain.replace('cmd:', '...extra, cmd:'),
    'getter': plain.replace('cmd: "neutral"', 'get cmd(){return "neutral"}'),
    'computed-key': plain.replace('cmd:', '["cmd"]:'),
    'escaped-key': plain.replace('cmd:', r'"\u0063md":'),
    'key-order': 'const r=await tools.exec_command({max_output_tokens:24000,cmd:"neutral"});text(r.output);',
    'trailing-comma': plain.replace('24000}', '24000,}'),
    'missing-first-semi': plain.replace('});\n', '})\n'),
    'missing-final-semi': plain[:-1],
    'wrong-output': plain.replace('r.output', 'r.stdout'),
    'extra-text-argument': plain.replace('text(r.output)', 'text(r.output, 1)'),
    'changed-text': plain.replace('text(', 'other('),
    'html-comment': '<!--\n' + plain,
    'nonascii-inner-whitespace': plain.replace('const r', 'const\u00a0r'),
    'unicode-inner-ls': plain.replace('const r', 'const\u2028r'),
    'unicode-inner-ps': plain.replace('const r', 'const\u2029r'),
    'bom-prefix': '\ufeff' + plain,
    'nbsp-prefix': '\u00a0' + plain,
    'repeated-pragma': '// @exec: {}\n// @exec: {}\n' + plain,
}
for budget in ['24001', '23999', '024000', '24_000', '24000.0', '2.4e4', '0x5dc0',
               '+24000', '"24000"', '24000n', 'Infinity', 'NaN', '24000+0']:
    mutations['budget-' + budget] = plain.replace('24000', budget)
for name, source in mutations.items():
    reject(name, source)
for name, value in [('none', None), ('integer', 1), ('mapping', {}), ('bytes', b'neutral')]:
    check('nonstr-' + name, p.canonical_read_body(value) is None)

rng = random.Random(147092)
alphabet = ['a', ' ', '\t', '\n', '\r', '\0', '"', '\\', '/', 'é', '🚀', '\u2028', '\u2029',
            '${x}', '/* comment */', '$(touch sentinel)', '; text(r.output);', '__proto__']
for i in range(320):
    command = ''.join(rng.choice(alphabet) for _ in range(rng.randrange(18)))
    cut = rng.randrange(len(command) + 1)
    one = body(json.dumps(command[:cut]), json.dumps(command[cut:]))
    accept('generated-static-' + str(i), one, command)
    reject('generated-extra-call-' + str(i), one + 'text("extra");')

# Import the original only through the proposal loader. No prove() call follows.
module = p.load_proposal_proof()
check('root-is-original-parent', module.ROOT == ROOT, group='wrapper')
check('base-root-is-original-parent', module.base.ROOT == ROOT, group='wrapper')
check('embedded-hashes-match', all(inputs[str(ROOT / name)] == expected
                                  for name, expected in p._FROZEN_SOURCE_HASHES.items()), group='wrapper')

# Simulate mismatches in memory; do not alter either frozen source. The loader
# must refuse both cases before invoking the Python source loader.
saved_read_bytes = Path.read_bytes
saved_spec_from_file_location = p.importlib.util.spec_from_file_location
for mismatch_path in ORIGINALS:
    import_attempts = []
    def simulated_bytes(path):
        value = saved_read_bytes(path)
        return value + b'\n# neutral simulated mismatch\n' if path == mismatch_path else value
    def blocked_import(*args, **kwargs):
        import_attempts.append(args)
        raise AssertionError('Import must not happen after hash mismatch')
    Path.read_bytes = simulated_bytes
    p.importlib.util.spec_from_file_location = blocked_import
    try:
        try:
            p.load_proposal_proof()
        except ValueError as exc:
            check('hash-mismatch-rejected-' + mismatch_path.name,
                  mismatch_path.name in str(exc) and not import_attempts, group='wrapper')
        else:
            check('hash-mismatch-rejected-' + mismatch_path.name, False, group='wrapper')
    finally:
        Path.read_bytes = saved_read_bytes
        p.importlib.util.spec_from_file_location = saved_spec_from_file_location

# Direct installer must replace only call_body on a known object.
def fake_original(value):
    return value.strip()
sentinel = object()
stub = SimpleNamespace(call_body=fake_original, prove=sentinel, ROOT=sentinel, other=sentinel)
before = vars(stub).copy()
p.install_on_module(stub)
check('installer-only-call-body', all(getattr(stub, key) is value for key, value in before.items()
                                    if key != 'call_body') and stub.call_body is not fake_original,
      group='wrapper')
check('installer-normalizes-after-original', stub.call_body('  ' + body('"neu"', '"tral"')) == plain,
      group='wrapper')
unknown = '/* no */ ' + plain
check('unknown-retained', module.call_body('  ' + unknown + '  ') == unknown, group='wrapper')
write = module.WRITE_MARKER + 'const arbitrary = "neutral";'
check('write-marker-body-preserved', module.call_body(' \n' + write + '\n') == write, group='wrapper')
check('inherited-pragma', module.call_body('// @exec: {"neutral":true}\n' + plain) == plain, group='wrapper')
check('inherited-pragma-content-ignored', module.call_body('// @exec: arbitrary text\n' + plain) == plain,
      group='wrapper')
check('inherited-outer-strip', module.call_body('\u00a0' + plain + '\u2029') == plain, group='wrapper')
try:
    module.call_body('// @exec: no-newline')
except IndexError:
    check('inherited-malformed-pragma-indexerror', True, group='wrapper')
else:
    check('inherited-malformed-pragma-indexerror', False, group='wrapper')

# Validate prospective API names and forwarding using a stub, never original.prove.
saved_loader = p.load_proposal_proof
forwarded = []
p.load_proposal_proof = lambda: SimpleNamespace(prove=lambda *a, **k: forwarded.append((a, k)) or 'stub-only')
valid_name = 'fresh-independent-js-format-proposal-proof.json'
check('wrapper-forwarding-stub-only', p.prove('neutral-bank', 'neutral-iteration', 'a', 'neutral',
      output_name=valid_name) == 'stub-only' and forwarded == [(
          ('neutral-bank', 'neutral-iteration', 'a', 'neutral'), {'output_name': valid_name})], group='wrapper')
for i, name in enumerate([None, '', 'old.json', '../x-js-format-proposal-proof.json',
                         '/tmp/x-js-format-proposal-proof.json', 'a/b-js-format-proposal-proof.json',
                         'x-js-format-proposal-proof.json\n', 0]):
    count = len(forwarded)
    try:
        p.prove('neutral', 'neutral', 'a', 'neutral', output_name=name)
    except ValueError:
        check('invalid-output-name-' + str(i), len(forwarded) == count, group='wrapper')
    else:
        check('invalid-output-name-' + str(i), False, group='wrapper')
try:
    p.prove('neutral', 'neutral', 'a', 'neutral')
except TypeError:
    check('explicit-output-name-required', True, group='wrapper')
else:
    check('explicit-output-name-required', False, group='wrapper')
p.load_proposal_proof = saved_loader

# Prove source remains exact, including exclusive output creation and original
# completion predicate. Function bytes are checked before/after normalizer install.
fresh_spec = importlib.util.spec_from_file_location('independent_pristine', ORIGINALS[0])
fresh = importlib.util.module_from_spec(fresh_spec)
fresh_spec.loader.exec_module(fresh)
funcs_before = {k: v for k, v in vars(fresh).items() if callable(v)}
p.install_on_module(fresh)
check('all-original-functions-identical-except-call-body', all(getattr(fresh, k) is v
      for k, v in funcs_before.items() if k != 'call_body'), group='wrapper')
tree = ast.parse(ORIGINALS[0].read_text())
prove_ast = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'prove')
check('exclusive-create-still-in-source', any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
      and n.func.attr == 'open' and n.args and isinstance(n.args[0], ast.Constant)
      and n.args[0].value == 'x' for n in ast.walk(prove_ast)), group='wrapper')

# Neutral precomputed allowlist: fixed READ_SCRIPT and exactly these two paths.
summary = Path('/neutral only/summary $(touch sentinel); ${x}.txt')
packet = Path('/neutral only/packet "quoted" 🚀.json')
expected = {'neutral_payload': 'exact value', 'nested': {'id': 'neutral', 'opaque': 'x'}}
approved = {module.base.canonical(expected)}
permitted = {}
for mode, index in [('summary', 0), ('metadata', 0), ('entry', 0), ('entry', 1)]:
    permitted[module.read_call(summary, packet, mode, index)] = expected
    permitted[module.literal_read_call(summary, packet, mode, index)] = expected
approved_body = module.literal_read_call(summary, packet, 'entry', 0)
approved_command = json.loads(approved_body.split('cmd: ', 1)[1].split(', max_output_tokens:', 1)[0])
format_body = approved_body.replace('const r = await ', 'const\tr=await\n').replace('});\ntext', '});\ttext')
check('fixed-command-format-canonicalizes-exactly', module.call_body(format_body) == approved_body,
      group='allowlist')
for i, changed in enumerate([approved_command + ' ', approved_command + '; touch sentinel',
                             approved_command.replace('entry 0', 'entry 2'),
                             approved_command.replace('entry 0', 'metadata 0'),
                             approved_command.replace(str(summary), '/neutral-other'),
                             approved_command.replace('python3', 'python'),
                             approved_command.replace('print(json.dumps', 'print (json.dumps'),
                             approved_command.replace(' entry 0', '  entry 0')]):
    normalized = module.call_body(canonical(changed))
    # metadata 0 is separately approved; it must map to its own exact call.
    should_allow = changed == module.read_prefix(summary, packet) + ' metadata 0'
    check('command-mutation-' + str(i), (normalized in permitted) == should_allow, group='allowlist')
for mode, index in [('summary', 0), ('metadata', 0), ('entry', 0), ('entry', 1)]:
    check('original-two-literals-' + mode + '-' + str(index), module.call_body(
          module.read_call(summary, packet, mode, index)) == module.literal_read_call(summary, packet, mode, index),
          group='allowlist')

def call(cid, source, name='exec'):
    return {'type': 'response_item', 'payload': {'type': 'custom_tool_call', 'name': name,
            'call_id': cid, 'input': source}}

def output(cid, value):
    return {'type': 'response_item', 'payload': {'type': 'custom_tool_call_output',
            'call_id': cid, 'output': value}}

trace_count = 0
def session(items):
    global trace_count
    trace_count += 1
    path = OUT / ('neutral-session-%02d.jsonl' % trace_count)
    path.write_text(''.join(json.dumps(x, ensure_ascii=True) + '\n' for x in items))
    parsed = module.session_delivery({'runtime_source': str(path)}, permitted)
    outputs, calls, unknown, status, boundary, post, unmatched = parsed
    found, extras, fragments = set(), [], []
    for item in outputs:
        seen, unexpected = set(), []
        module.walk_visible(item['value'], approved, seen, unexpected,
                            item['expected_value'] if item['approved_read'] else None, fragments)
        if item['before_boundary'] and item['approved_read'] and module.base.canonical(item['expected_value']) in seen:
            found.add(module.base.canonical(item['expected_value']))
        extras.extend(unexpected)
    return SimpleNamespace(outputs=outputs, calls=calls, unknown=unknown, status=status,
                           boundary=boundary, post=post, unmatched=unmatched, found=found,
                           extras=extras, fragments=fragments)

exact_output = json.dumps(expected)
boundary_call = call('write', write)
s = session([call('read', format_body), output('read', exact_output), boundary_call,
             call('post', 'neutral arbitrary postwrite code')])
check('formatted-read-approved-and-output-exact', bool(s.found) and not s.unknown and not s.unmatched,
      group='session')
check('raw-input-not-rewritten', s.calls[0]['input'] == format_body, group='session')
check('first-write-marker-preserved-and-recorded-post', s.boundary['input'] == write
      and [x['call_id'] for x in s.post] == ['post'], group='session')
s = session([call('read', format_body), boundary_call, output('read', exact_output)])
check('late-output-not-credited', not s.found and not s.outputs[0]['before_boundary'], group='session')
s = session([boundary_call, call('read', format_body), output('read', exact_output)])
check('postwrite-read-unapproved-and-uncredited', not s.found and not s.outputs[0]['approved_read'], group='session')
s = session([call('u', unknown), output('u', exact_output), boundary_call])
check('unknown-body-reported-and-uncredited', len(s.unknown) == 1 and not s.found
      and s.unknown[0]['input'] == unknown, group='session')
s = session([call('r', format_body + 'text("extra");'), output('r', exact_output), boundary_call])
check('extra-exec-body-unapproved', len(s.unknown) == 1 and not s.found, group='session')
s = session([call('r', format_body, 'other'), output('r', exact_output), boundary_call])
check('wrong-tool-name-unapproved', len(s.unknown) == 1 and not s.found, group='session')
s = session([call('status', '{}', 'list_agents'), boundary_call])
check('status-remains-reported', s.status == ['list_agents'] and len(s.unknown) == 1, group='session')
s = session([call(None, format_body), output(None, exact_output), boundary_call])
check('missing-call-id-reported', bool(s.unknown) and not s.found, group='session')
s = session([call('same', format_body), call('same', format_body), output('same', exact_output), boundary_call])
check('duplicate-call-id-reported', bool(s.unknown) and not s.found, group='session')
s = session([output('unmatched', exact_output), boundary_call])
check('unmatched-output-reported', len(s.unmatched) == 1 and not s.found, group='session')
for label, altered in [('changed', {'neutral_payload': 'CHANGED', 'nested': expected['nested']}),
                       ('missing', {'neutral_payload': 'exact value'}),
                       ('extra', {**expected, 'extra': 1})]:
    s = session([call('r', format_body), output('r', json.dumps(altered)), boundary_call])
    check('exact-output-' + label + '-not-credited', not s.found, group='session')
s = session([call('r', format_body), output('r', json.dumps(expected, indent=2, sort_keys=True)), boundary_call])
check('json-object-equality-preserved', bool(s.found), group='session')
unexpected = {'id': 'neutral', 'question_entry': {}, 'key_entry': {}, 'reader_a_entry': {}}
s = session([call('r', format_body), output('r', json.dumps(unexpected)), boundary_call])
check('unexpected-entry-shape-detected', bool(s.extras) and not s.found, group='session')
truncated = exact_output[:20] + '\nWarning: truncated output neutral'
s = session([call('r', format_body), output('r', truncated), boundary_call])
check('truncation-alone-uncredited', not s.found and len(s.fragments) == 1, group='session')
s = session([call('r', format_body), output('r', truncated), call('recovery', format_body),
             output('recovery', exact_output), boundary_call])
check('exact-recovery-credited', bool(s.found) and len(s.fragments) == 1, group='session')
s = session([call('r', format_body), output('r', exact_output)])
check('missing-boundary-stays-missing', bool(s.found) and s.boundary is None, group='session')

after = {path: digest(Path(path)) for path in inputs}
check('all-allowed-inputs-unchanged', inputs == after, group='integrity')
check('no-command-sentinel-written', not (OUT / 'sentinel').exists(), group='integrity')

(OUT / 'neutral-parser-fixtures.json').write_text(json.dumps(fixtures, ensure_ascii=True, indent=2) + '\n')
summary_result = dict(total=len(results), passed=sum(x['passed'] for x in results),
                      failed=sum(not x['passed'] for x in results),
                      by_group={g: {'total': sum(x['group'] == g for x in results),
                                    'failed': sum(x['group'] == g and not x['passed'] for x in results)}
                                for g in sorted({x['group'] for x in results})},
                      neutral_parser_fixtures=len(fixtures), neutral_trace_files=trace_count,
                      seed=147092, actual_proof_invocations=0, results=results)
(OUT / 'neutral-results.json').write_text(json.dumps(summary_result, ensure_ascii=True, indent=2) + '\n')
print(json.dumps({k: v for k, v in summary_result.items() if k != 'results'}, indent=2))
if summary_result['failed']:
    print(json.dumps([x for x in results if not x['passed']], ensure_ascii=True, indent=2))
raise SystemExit(bool(summary_result['failed']))
