"""New neutral fixtures only. No actual proof, shell read command or runtime is executed."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import sys
from types import SimpleNamespace
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PROPOSAL_DIR = HERE.parent
spec = importlib.util.spec_from_file_location('format_proposal', PROPOSAL_DIR/'read_call_format_proposal.py')
proposal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proposal)


def original_module():
    path = PROPOSAL_DIR.parent/'prove-single-reader-grading-delivery-literal-equivalent.py'
    s = importlib.util.spec_from_file_location('neutral_original_delivery', path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


original = original_module()
wrapped = proposal.load_proposal_proof()
SUMMARY = '/neutral-only/source.md'
PACKET = '/neutral-only/packet.json'
COMMAND = original.read_prefix(SUMMARY, PACKET) + ' summary 0'
CANONICAL = original.literal_read_call(SUMMARY, PACKET, 'summary', 0)
EXPECTED = {'qa_delivery':'summary-chunk-v1','start_line':1,'end_line':2,
            'text':'## Neutral\nA neutral line.\n',
            'sha256':hashlib.sha256('## Neutral\nA neutral line.\n'.encode()).hexdigest()}
PERMITTED = {CANONICAL: EXPECTED, original.read_call(SUMMARY, PACKET, 'summary', 0): EXPECTED}
CASES=[]


def case(name, category, fn, predicate):
    try:
        value=fn();observed={'returned':value}
    except Exception as e:
        observed={'exception':type(e).__name__,'message':str(e)}
    CASES.append({'name':name,'category':category,'matches':bool(predicate(observed)),'observed':observed})


def eq(expected):return lambda x:'returned' in x and x['returned']==expected
def rejected(x):return x.get('returned','not-none') is None


def form(literal, whitespace=' ', keys=('cmd','max_output_tokens')):
    w=whitespace
    return f'const{w}r{w}={w}await{w}tools{w}.{w}exec_command{w}({w}{{{w}{keys[0]}{w}:{w}{literal}{w},{w}{keys[1]}{w}:{w}24000{w}}}{w}){w};{w}text{w}({w}r{w}.{w}output{w}){w};'


case('original_single_literal','positive',lambda:proposal.canonical_read_body(CANONICAL),eq(CANONICAL))
case('original_two_literals','positive',lambda:proposal.canonical_read_body(original.read_call(SUMMARY,PACKET,'summary',0)),eq(CANONICAL))
case('compact_outer_format','positive',lambda:proposal.canonical_read_body('const r=await tools.exec_command({cmd:'+json.dumps(COMMAND)+',max_output_tokens:24000});text(r.output);'),eq(CANONICAL))
for name,ws in [('spaces','   '),('tabs','\t'),('newlines','\n'),('crlf','\r\n'),('mixed',' \t\r\n\v\f')]:
    case('outer_whitespace_'+name,'positive',lambda ws=ws:proposal.canonical_read_body(form(json.dumps(COMMAND),ws)),eq(CANONICAL))
case('quoted_exact_keys','positive',lambda:proposal.canonical_read_body(form(json.dumps(COMMAND),' ',('"cmd"','"max_output_tokens"'))),eq(CANONICAL))
case('mixed_quoted_keys','positive',lambda:proposal.canonical_read_body(form(json.dumps(COMMAND),' ',('cmd','"max_output_tokens"'))),eq(CANONICAL))
case('escaped_slash_same_command','positive',lambda:proposal.canonical_read_body(form(json.dumps(COMMAND).replace('/','\\/'))),eq(CANONICAL))
case('alternate_unicode_escape_same_command','positive',lambda:proposal.canonical_read_body(form(json.dumps(COMMAND).replace('python3','\\u0070ython3',1))),eq(CANONICAL))
case('arbitrary_static_literal_split','positive',lambda:proposal.canonical_read_body(form(json.dumps(COMMAND[:17])+' + '+json.dumps(COMMAND[17:]))),eq(CANONICAL))
case('empty_first_static_literal','positive',lambda:proposal.canonical_read_body(form('"" + '+json.dumps(COMMAND))),eq(CANONICAL))

for name,content in [
    ('code_like','"}); text(r.output); /* comment */ // QA_ARTIFACT_WRITE_V1\n'),
    ('interpolation_like','${throw new Error("not executed")}'),
    ('shell_like','$(touch SHOULD_NOT_EXIST); `not executed`; & | >'),
    ('escaped_controls','one\ntwo\tthree\r'),
    ('unicode','Café e\u0301 😀'),
    ('unicode_line_separator','before\u2028after\u2029end')]:
    expected='const r = await tools.exec_command({cmd: '+json.dumps(content)+', max_output_tokens: 24000});\ntext(r.output);'
    case('literal_data_'+name,'data-not-code',lambda content=content:proposal.canonical_read_body(form(json.dumps(content))),eq(expected))

negative={
 'single_quote_literal':form("'python3'"),
 'template_literal':form('`python3`'),
 'template_interpolation':form('`${command}`'),
 'dynamic_identifier':form('command'),
 'dynamic_concat':form(json.dumps(COMMAND)+' + suffix'),
 'three_literals':form('"" + '+json.dumps(COMMAND)+' + ""'),
 'parenthesized_literal':form('('+json.dumps(COMMAND)+')'),
 'json_parse_expression':form('JSON.parse('+json.dumps(json.dumps(COMMAND))+')'),
 'function_value':form('(()=>'+json.dumps(COMMAND)+')()'),
 'string_raw':form('String.raw`python3`'),
 'malformed_escape':form(r'"bad\x41"'),
 'malformed_unicode':form(r'"bad\u12QQ"'),
 'unterminated_string':form('"unterminated'),
 'raw_newline_string':form('"one\ntwo"'),
 'raw_control_string':form('"one\ttwo"'),
 'raw_unicode_separator':form('"one\u2028two"'),
 'lone_high_surrogate':form(r'"\ud800"'),
 'lone_low_surrogate':form(r'"\udc00"'),
 'ordinary_leading_comment':'// ordinary comment\n'+CANONICAL,
 'block_comment':'/* ordinary */'+CANONICAL,
 'inline_comment':CANONICAL.replace('cmd:', 'cmd: /* injected */'),
 'comment_between_statements':CANONICAL.replace('\ntext','\n// added\ntext'),
 'extra_statement_before':'text("extra");'+CANONICAL,
 'extra_statement_after':CANONICAL+'text("extra");',
 'second_exec_call':CANONICAL+'await tools.exec_command({cmd:"extra",max_output_tokens:24000});',
 'extra_object_field':CANONICAL.replace(', max_output_tokens:', ', env: {}, max_output_tokens:'),
 'prototype_field':CANONICAL.replace(', max_output_tokens:', ', __proto__: {}, max_output_tokens:'),
 'duplicate_cmd_field':CANONICAL.replace(', max_output_tokens:', ', cmd: "extra", max_output_tokens:'),
 'computed_key':CANONICAL.replace('cmd:', '["cmd"]:'),
 'spread_object':CANONICAL.replace('{cmd:', '{...other,cmd:'),
 'object_getter':CANONICAL.replace('{cmd:', '{get cmd(){return "extra"},unused:'),
 'keys_reordered':'const r=await tools.exec_command({max_output_tokens:24000,cmd:'+json.dumps(COMMAND)+'});text(r.output);',
 'escaped_key':CANONICAL.replace('cmd:',r'"\u0063md":'),
 'other_budget':CANONICAL.replace('24000','24001'),
 'string_budget':CANONICAL.replace('24000','"24000"'),
 'float_budget':CANONICAL.replace('24000','24000.0'),
 'expression_budget':CANONICAL.replace('24000','12000+12000'),
 'leading_zero_budget':CANONICAL.replace('24000','024000'),
 'numeric_separator_budget':CANONICAL.replace('24000','24_000'),
 'extra_exec_argument':CANONICAL.replace('24000});','24000}, {});'),
 'trailing_object_comma':CANONICAL.replace('24000});','24000,});'),
 'wrong_variable':CANONICAL.replace('const r','const result'),
 'let_binding':CANONICAL.replace('const r','let r'),
 'missing_const_separator':CANONICAL.replace('const r','constr'),
 'missing_await_separator':CANONICAL.replace('await tools','awaittools'),
 'different_output':CANONICAL.replace('r.output','r.other'),
 'optional_chaining':CANONICAL.replace('r.output','r?.output'),
 'missing_semicolon':CANONICAL[:-1],
 'extra_semicolon':CANONICAL+';',
 'unicode_syntax_whitespace':CANONICAL.replace('const r','const\u00a0r'),
 'async_wrapper':'(async()=>{'+CANONICAL+'})()',
 'return_prefix':'return '+CANONICAL,
}
for name,body in negative.items():
    case('reject_'+name,'negative-syntax',lambda body=body:proposal.canonical_read_body(body),rejected)

case('escaped_valid_surrogate_pair','positive',lambda:proposal.canonical_read_body(form(r'"\ud83d\ude00"')),
     eq('const r = await tools.exec_command({cmd: "\\ud83d\\ude00", max_output_tokens: 24000});\ntext(r.output);'))


def call(code,call_id='read',name='exec'):
    return {'type':'response_item','payload':{'type':'custom_tool_call','name':name,'call_id':call_id,'input':code}}


def output(value=EXPECTED,call_id='read'):
    return {'type':'response_item','payload':{'type':'custom_tool_call_output','call_id':call_id,'output':json.dumps(value,ensure_ascii=False)}}


WRITE=original.WRITE_MARKER+'text("neutral marker only; never executed");'
TRACE_COUNT=0


def session(items, proof=wrapped, permitted=PERMITTED):
    global TRACE_COUNT
    TRACE_COUNT+=1
    path=HERE/f'neutral-trace-{TRACE_COUNT:03}.jsonl'
    path.write_text(''.join(json.dumps(i,ensure_ascii=False)+'\n' for i in items))
    values=proof.session_delivery({'runtime_source':str(path)},permitted)
    outputs,calls,unknown,status,boundary,post,unmatched=values
    return {'outputs':outputs,'calls':calls,'unknown':unknown,'status':status,'boundary':boundary,'post_calls':post,'unmatched':unmatched}


variant=form(json.dumps(COMMAND),'\n',('"cmd"','max_output_tokens'))
case('original_rejects_format_variant','session',lambda:session([call(variant),output(),call(WRITE,'write')],original),
     lambda x:len(x['returned']['unknown'])==1 and not x['returned']['outputs'][0]['approved_read'])
case('proposal_accepts_static_same_command','session',lambda:session([call(variant),output(),call(WRITE,'write')]),
     lambda x:not x['returned']['unknown'] and x['returned']['outputs'][0]['approved_read'] and x['returned']['boundary']['input']==WRITE)
case('raw_call_preserved_for_audit','session',lambda:session([call(variant),output(),call(WRITE,'write')]),
     lambda x:x['returned']['calls'][0]['input']==variant)

for name,cmd in [
 ('different_path',COMMAND.replace('/neutral-only/source.md','/neutral-only/other.md')),
 ('different_mode',COMMAND[:-len('summary 0')]+'entry 0'),
 ('different_index',COMMAND[:-1]+'1'),
 ('different_script',COMMAND.replace('import hashlib,json,sys','import json,sys')),
 ('extra_shell_command',COMMAND+'; touch SHOULD_NOT_EXIST'),
 ('shell_token_equivalent_spacing',COMMAND.replace('python3 -c','python3  -c',1)),
 ('trailing_shell_whitespace',COMMAND+' '),
 ('nul_byte',COMMAND+'\x00')]:
    body=form(json.dumps(cmd))
    case('unapproved_command_'+name,'exact-command',lambda body=body:session([call(body),output(),call(WRITE,'write')]),
         lambda x:len(x['returned']['unknown'])==1 and not x['returned']['outputs'][0]['approved_read'])

case('syntax_rejection_remains_unknown','session',lambda:session([call(negative['extra_statement_after']),output(),call(WRITE,'write')]),
     lambda x:len(x['returned']['unknown'])==1 and not x['returned']['outputs'][0]['approved_read'])
case('ordinary_comment_stays_unknown','session',lambda:session([call(negative['ordinary_leading_comment']),output(),call(WRITE,'write')]),
     lambda x:len(x['returned']['unknown'])==1)
case('inherited_exec_pragma_preserved','legacy-preprocessing',lambda:session([call('// @exec: {"yield_time_ms":10000}\n'+variant),output(),call(WRITE,'write')]),
     lambda x:not x['returned']['unknown'] and x['returned']['outputs'][0]['approved_read'])
case('write_marker_preserved_exactly','boundary',lambda:wrapped.call_body(WRITE),eq(original.call_body(WRITE)))
case('postwrite_read_uncredited','boundary',lambda:session([call(WRITE,'write'),call(variant),output()]),
     lambda x:x['returned']['boundary']['call_id']=='write' and len(x['returned']['post_calls'])==1 and not x['returned']['outputs'][0]['approved_read'] and not x['returned']['outputs'][0]['before_boundary'])
case('late_output_after_write_not_initial','boundary',lambda:session([call(variant),call(WRITE,'write'),output()]),
     lambda x:x['returned']['outputs'][0]['approved_read'] and not x['returned']['outputs'][0]['before_boundary'])
case('unknown_before_marker_retained','boundary',lambda:session([call('text("unknown")','unknown'),call(variant),output(),call(WRITE,'write')]),
     lambda x:len(x['returned']['unknown'])==1 and x['returned']['boundary']['call_id']=='write')
case('status_call_retained','boundary',lambda:session([call('{}','status','list_agents'),call(WRITE,'write')]),
     lambda x:x['returned']['status']==['list_agents'] and len(x['returned']['unknown'])==1)
case('duplicate_call_id_retained','call-binding',lambda:session([call(variant),call(variant),output(),call(WRITE,'write')]),
     lambda x:bool(x['returned']['unknown']) and not x['returned']['outputs'][0]['approved_read'])
case('missing_call_id_retained','call-binding',lambda:session([call(variant,None),output(call_id=None),call(WRITE,'write')]),
     lambda x:bool(x['returned']['unknown']) and not x['returned']['outputs'][0]['approved_read'])
case('unmatched_output_retained','call-binding',lambda:session([output(call_id='unknown'),call(WRITE,'write')]),
     lambda x:bool(x['returned']['unmatched']) and not x['returned']['outputs'][0]['approved_read'])
case('missing_write_boundary_retained','boundary',lambda:session([call(variant),output()]),lambda x:x['returned']['boundary'] is None)


def approved_literal_code_like_path():
    source='/neutral-only/"}); // ${not_executed} $(not_executed) `data` 😀.md'
    packet='/neutral-only/packet with spaces.json'
    command=original.read_prefix(source,packet)+' entry 2'
    literal=original.literal_read_call(source,packet,'entry',2)
    return session([call(form(json.dumps(command),'\t')),output(),call(WRITE,'write')],
                   permitted={literal:EXPECTED})


case('allowlisted_code_like_path_remains_literal_data','exact-command',approved_literal_code_like_path,
     lambda x:not x['returned']['unknown'] and x['returned']['outputs'][0]['approved_read'])
case('marker_plus_extra_read_remains_write_boundary','boundary',lambda:wrapped.call_body(WRITE+'\n'+variant),
     eq(original.call_body(WRITE+'\n'+variant)))


def visible(value,expected=EXPECTED):
    found,unexpected,fragments=set(),[],[]
    approved={original.base.canonical(expected)}
    wrapped.walk_visible(value,approved,found,unexpected,expected,fragments)
    return {'credited_expected':original.base.canonical(expected) in found,'unexpected':unexpected,'fragments':fragments}


case('exact_source_value_required','output-equality',lambda:visible(json.dumps(EXPECTED)),lambda x:x['returned']['credited_expected'])
changed=dict(EXPECTED,text='## Neutral\nAltered.\n')
case('altered_source_value_not_credited','output-equality',lambda:visible(json.dumps(changed)),lambda x:not x['returned']['credited_expected'])
neutral_entry={'id':'NEUTRAL-1','question_entry':{'neutral':'question-shaped fixture'},'key_entry':{'neutral':'synthetic reference'},'reader_a_entry':{'neutral':'synthetic entry'}}
case('exact_neutral_entry_equality_required','output-equality',lambda:visible(json.dumps(neutral_entry),neutral_entry),lambda x:x['returned']['credited_expected'])
altered=copy.deepcopy(neutral_entry);altered['reader_a_entry']['neutral']='altered'
case('altered_neutral_entry_flagged','output-equality',lambda:visible(json.dumps(altered),neutral_entry),lambda x:not x['returned']['credited_expected'] and bool(x['returned']['unexpected']))
truncated=json.dumps(EXPECTED,ensure_ascii=False)[:30]+'\nWarning: truncated output remaining neutral text'
case('consistent_truncated_prefix_not_credited','output-equality',lambda:visible(truncated),lambda x:not x['returned']['credited_expected'] and bool(x['returned']['fragments']))
case('exact_recovery_after_truncation_credited','output-equality',lambda:visible(truncated+'\n'+json.dumps(EXPECTED)),lambda x:x['returned']['credited_expected'])


def only_one_override():
    m=original_module();before=dict(vars(m));proposal.install_on_module(m);after=dict(vars(m))
    changed=[k for k in set(before)|set(after) if before.get(k) is not after.get(k)]
    return changed


case('only_call_body_is_overridden','guard-preservation',only_one_override,eq(['call_body']))


def source_hash_change_rejected_without_edit():
    with patch.object(proposal.Path,'read_bytes',return_value=b'neutral changed source; never imported'):
        return proposal.load_proposal_proof()


case('changed_generic_source_hash_fails_closed','version-binding',source_hash_change_rejected_without_edit,
     lambda x:x.get('exception')=='ValueError' and 'reviewed frozen hash' in x['message'])


def future_api_no_runtime():
    captured=[]
    fake=SimpleNamespace(prove=lambda *a,**kw:captured.append({'args':list(a),'kwargs':kw}) or 'stub-only')
    with patch.object(proposal,'load_proposal_proof',return_value=fake):
        value=proposal.prove('neutral-bank','neutral-iteration','a','neutral-prefix',output_name='neutral-js-format-proposal-proof.json')
    return {'value':value,'captured':captured}


case('future_wrapper_forwards_to_frozen_prove_stub_only','future-api',future_api_no_runtime,
     lambda x:x['returned']['value']=='stub-only' and x['returned']['captured'][0]['kwargs']['output_name']=='neutral-js-format-proposal-proof.json')
for name in ['grading-reader-a-input-delivery-proof.json','../neutral-js-format-proposal-proof.json','/tmp/neutral-js-format-proposal-proof.json','neutral.json']:
    case('reject_output_name_'+name,'future-api',lambda name=name:proposal.prove('neutral','neutral','a','neutral',output_name=name),lambda x:x.get('exception')=='ValueError')


def deterministic_string_properties():
    rng=random.Random(41027)
    alphabet=['a','\\','"','\n','\r','\t','\x00','😀','${','*/','\\u1234',';text(r.output);']
    for _ in range(256):
        value=''.join(rng.choice(alphabet) for _ in range(rng.randrange(40)))
        split=rng.randrange(len(value)+1)
        expression=json.dumps(value[:split])+' + '+json.dumps(value[split:])
        body=form(expression,rng.choice([' ','\t','\n','\r\n']))
        expected='const r = await tools.exec_command({cmd: '+json.dumps(value)+', max_output_tokens: 24000});\ntext(r.output);'
        assert proposal.canonical_read_body(body)==expected
        assert proposal.canonical_read_body(body+';') is None
        assert proposal.canonical_read_body(body+'text("extra");') is None
    return {'seed':41027,'static_literal_cases':256,'extra_syntax_rejections':512}


case('deterministic_literal_data_properties','generated-neutral',deterministic_string_properties,
     eq({'seed':41027,'static_literal_cases':256,'extra_syntax_rejections':512}))


if __name__=='__main__':
    result={'purpose':'Unadopted proposal neutral syntax/guard tests only; no actual runtimes, proof(), shell or JavaScript evaluation.',
            'python_version':sys.version,'count':len(CASES),'matches':sum(x['matches'] for x in CASES),'cases':CASES}
    (HERE/'neutral-results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'count':result['count'],'matches':result['matches']}))
    for c in CASES:
        if not c['matches']:print(json.dumps(c,ensure_ascii=False))
    raise SystemExit(0 if result['count']==result['matches'] else 1)
