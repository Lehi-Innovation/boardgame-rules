"""Neutral syntactic characterization only; no semantic routing or grading."""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent


def load(version):
    spec = importlib.util.spec_from_file_location(version, ROOT / ('summary-hierarchical-section-check-' + version + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v8, v9 = load('v8'), load('v9')
TEXT = '# Root\n## Shared\nOnly blue labels apply.\n### Alpha\nPlace one token in tray A.\n### Beta\nPlace two tokens in tray B.\n## Other\nKeep labels dry.  \n'
QUESTIONS = [{'id': 'N1', 'question': 'Which tray receives Alpha, and how many tokens?'}]
INDEX = v9.units(TEXT)
CASES = []


def entry(selected=('I002', 'T004')):
    return {'id': 'N1', 'clause_ledger': [
        {'requested_clause': 'Which tray receives Alpha', 'section_ids': list(selected), 'fact_kind': 'lookup'},
        {'requested_clause': 'how many tokens', 'section_ids': list(selected), 'fact_kind': 'lookup'}],
        'case_conclusions': [], 'operative_sections': [{k: v for k, v in INDEX[uid].items() if k != 'text'} for uid in selected],
        'answer': 'Applicable summary text\n' + '\n'.join(v9.attachment(INDEX[uid]) for uid in selected),
        'support': 'supported', 'evidence': [{'summary_location': '### Alpha', 'quote': '### Alpha'}]}


def mutate(fn, selected=('I002', 'T004')):
    e = entry(selected)
    fn(e)
    return {'answers': [e]}


def check(raw=None, text=TEXT, questions=QUESTIONS):
    return v9.check_data(text, questions, raw if raw is not None else {'answers': [entry()]}, 'neutral')


def probe(name, category, fn, expected):
    try:
        value = fn()
        actual = {'returned': value}
    except Exception as exc:
        actual = {'exception': type(exc).__name__, 'message': str(exc)}
    ok = expected(actual)
    CASES.append({'name': name, 'category': category, 'characterization_matches': ok, 'observed': actual})


def valid(x):
    return 'returned' in x and x['returned']['all_structure_and_declared_source_spans_valid']


def invalid(x):
    return 'returned' in x and not x['returned']['all_structure_and_declared_source_spans_valid']


def is_exception(x):
    return x.get('exception') == 'ValueError'


probe('lookup_without_paraphrase', 'supported-mechanism', check, valid)
probe('adjacent_intro_and_child', 'boundary', check, lambda x: valid(x) and INDEX['I002']['end_offset'] == INDEX['T004']['start_offset'])
probe('unit_engine_unchanged', 'comparison', lambda: v8.units(TEXT) == INDEX, lambda x: x.get('returned') is True)
for name in ('units', 'start_marker', 'end_marker', 'attachment'):
    def same_ast(name=name):
        trees = [ast.parse((ROOT / ('summary-hierarchical-section-check-' + v + '.py')).read_text()) for v in ('v8', 'v9')]
        return len({ast.dump(next(n for n in t.body if isinstance(n, ast.FunctionDef) and n.name == name), include_attributes=False) for t in trees}) == 1
    probe('unchanged_ast_' + name, 'comparison', same_ast, lambda x: x.get('returned') is True)
probe('crop_final_condition', 'boundary', lambda: check(mutate(lambda e: e.update(answer=e['answer'].replace('Only blue labels apply.\n', '')))), invalid)
probe('trim_trailing_whitespace', 'boundary', lambda: check(mutate(lambda e: e.update(answer=e['answer'].replace('Keep labels dry.  \n', 'Keep labels dry.\n')), ('T008',))), invalid)
probe('wrong_hash', 'hash', lambda: check(mutate(lambda e: e['operative_sections'][0].update(sha256='0'*64))), invalid)
probe('wrong_offset', 'boundary', lambda: check(mutate(lambda e: e['operative_sections'][0].update(end_offset=0))), invalid)
probe('wrong_kind', 'boundary', lambda: check(mutate(lambda e: e['operative_sections'][0].update(kind='subtree'))), invalid)
probe('wrong_heading', 'boundary', lambda: check(mutate(lambda e: e['operative_sections'][0].update(heading='Shared'))), invalid)
probe('reverse_attachment_order', 'order', lambda: check(mutate(lambda e: e.update(answer=v9.attachment(INDEX['T004'])+'\n'+v9.attachment(INDEX['I002'])))), invalid)
probe('parent_child_overlap', 'overlap', lambda: check({'answers': [entry(('T002','T004'))]}), invalid)
probe('intro_subtree_leaf_alias_overlap', 'overlap', lambda: check({'answers': [entry(('I004','T004'))]}), invalid)
probe('duplicate_selected_id', 'overlap', lambda: check({'answers': [entry(('T004','T004'))]}), invalid)
probe('unmarked_duplicate_answer', 'attachment', lambda: check(mutate(lambda e: e.update(answer=e['answer']+INDEX['T004']['text']))), invalid)
probe('duplicate_marked_attachment', 'attachment', lambda: check(mutate(lambda e: e.update(answer=e['answer']+v9.attachment(INDEX['T004'])))), invalid)
probe('unknown_marker', 'attachment', lambda: check(mutate(lambda e: e.update(answer=e['answer']+'<!-- qa-unit:T999:begin -->\nextra<!-- qa-unit:T999:end -->'))), invalid)
probe('dangling_marker', 'attachment', lambda: check(mutate(lambda e: e.update(answer=e['answer']+'<!-- qa-unit:unfinished'))), invalid)
probe('nonliteral_clause', 'clause', lambda: check(mutate(lambda e: e['clause_ledger'][0].update(requested_clause='different request'))), invalid)
probe('unselected_clause_reference', 'clause', lambda: check(mutate(lambda e: e['clause_ledger'][0].update(section_ids=['T008']))), invalid)
probe('empty_lookup_references', 'clause', lambda: check(mutate(lambda e: e['clause_ledger'][0].update(section_ids=[]))), invalid)
probe('nontext_reference', 'clause', lambda: check(mutate(lambda e: e['clause_ledger'][0].update(section_ids=[4]))), invalid)
probe('lookup_duplicate_fact_field', 'clause', lambda: check(mutate(lambda e: e['clause_ledger'][0].update(supported_fact_or_case_result='Tray A.'))), invalid)
probe('lookup_separate_fact_source', 'clause', lambda: check(mutate(lambda e: e['clause_ledger'][0].update(fact_source_section='T004'))), invalid)
probe('v8_quote_kind_rejected', 'comparison', lambda: check(mutate(lambda e: e['clause_ledger'][0].update(fact_kind='quote'))), invalid)
probe('unsupported_nonempty', 'unsupported-structure', lambda: check(mutate(lambda e: e['clause_ledger'][0].update(fact_kind='unsupported', section_ids=[], supported_fact_or_case_result='The requested tray cannot be determined from checked text.'))), valid)
probe('unsupported_blank', 'unsupported-structure', lambda: check(mutate(lambda e: e['clause_ledger'][0].update(fact_kind='unsupported', supported_fact_or_case_result=' \n'))), invalid)
probe('unsupported_number', 'unsupported-structure', lambda: check(mutate(lambda e: e['clause_ledger'][0].update(fact_kind='unsupported', supported_fact_or_case_result=7))), invalid)
probe('fenced_source_rejected', 'unsupported-input', lambda: v9.units('```\n## Literal\n```\n'), is_exception)
probe('reserved_source_marker_rejected', 'unsupported-input', lambda: v9.units('## Alpha\n<!-- qa-unit:T001:begin -->'), is_exception)
probe('missing_case_field_accepted', 'schema-gap', lambda: check(mutate(lambda e: e.pop('case_conclusions'))), valid)
probe('nonarray_case_field_accepted', 'schema-gap', lambda: check(mutate(lambda e: e.update(case_conclusions={'result': 'Two tokens.'}))), valid)
probe('invalid_support_label_accepted', 'schema-gap', lambda: check(mutate(lambda e: e.update(support='arbitrary'))), valid)
probe('invalid_evidence_type_accepted', 'schema-gap', lambda: check(mutate(lambda e: e.update(evidence=17))), valid)
probe('missing_inputs_read_accepted', 'schema-gap', check, valid)
probe('float_metadata_accepted', 'schema-gap', lambda: check(mutate(lambda e: e['operative_sections'][0].update(level=2.0))), valid)
probe('text_in_metadata_accepted', 'schema-gap', lambda: check(mutate(lambda e: e['operative_sections'][0].update(text=INDEX['I002']['text']))), valid)
probe('duplicate_unit_other_field_accepted', 'schema-gap', lambda: check(mutate(lambda e: e.update(extra=INDEX['T004']['text']))), valid)
probe('missing_applicable_text_label_accepted', 'format-gap', lambda: check(mutate(lambda e: e.update(answer=e['answer'].replace('Applicable summary text\n','')))), valid)
probe('empty_answer_bank_has_true_structure_flag', 'aggregation-limit', lambda: check({'answers': []}), lambda x: valid(x) and x['returned']['exact_ordered_unique_ids'] is False)
probe('compound_unsplit_ledger_accepted', 'semantic-limit', lambda: check(mutate(lambda e: e.update(clause_ledger=[{'requested_clause': QUESTIONS[0]['question'], 'section_ids': ['T004'], 'fact_kind': 'lookup'}]))), valid)
probe('omitted_clause_accepted', 'semantic-limit', lambda: check(mutate(lambda e: e['clause_ledger'].pop())), valid)
probe('unrelated_selected_unit_accepted', 'semantic-limit', lambda: check({'answers': [entry(('T008',))]}), valid)
probe('unsupported_guess_accepted_structurally', 'semantic-limit', lambda: check(mutate(lambda e: e['clause_ledger'][0].update(fact_kind='unsupported', supported_fact_or_case_result='The tray is probably purple.'))), valid)
probe('wrong_extra_prose_accepted_structurally', 'semantic-limit', lambda: check(mutate(lambda e: e.update(answer='Use tray Z.\n'+e['answer']))), valid)
probe('contradictory_case_accepted_structurally', 'semantic-limit', lambda: check(mutate(lambda e: e.update(case_conclusions=['Use tray Z.']))), valid)


def boundaries():
    text = '# R\n## P\nintro\n### C\nchild\n# Stop\noutside\n'
    index = v9.units(text)
    assert index['I002']['text'] == '## P\nintro\n'
    assert index['T002']['text'] == '## P\nintro\n### C\nchild\n'
    assert index['T004']['parent_section_id'] == 'T002'
    assert all(u['start_line'] not in (1, 6) for u in index.values())
    assert all(text[u['start_offset']:u['end_offset']] == u['text'] for u in index.values())
    assert all(hashlib.sha256(u['text'].encode()).hexdigest() == u['sha256'] for u in index.values())
    return True


probe('level1_closure_exact_boundaries_hashes', 'boundary', boundaries, lambda x: x.get('returned') is True)


def disjoint_identical():
    text = '## Repeat\nSame.\n## Repeat\nSame.\n'
    idx = v9.units(text)
    e = entry()
    e['operative_sections'] = [{k:v for k,v in idx[u].items() if k!='text'} for u in ('T001','T003')]
    e['answer'] = '\n'.join(v9.attachment(idx[u]) for u in ('T001','T003'))
    e['clause_ledger'] = [{'requested_clause':'Which tray receives Alpha', 'section_ids':['T001','T003'], 'fact_kind':'lookup'}]
    return check({'answers':[e]},text)


probe('identical_disjoint_units_allowed', 'attachment', disjoint_identical, valid)


def unicode_crlf():
    text = '😀 e\u0301\r\n## Alpha\r\nDetail.  \r\n'
    u = v9.units(text)['T002']
    assert u['start_offset'] == 6 and u['text'] == text[6:] and u['heading'] == '## Alpha\r'
    assert u['end_line'] == 3 and u['sha256'] == hashlib.sha256(text[6:].encode()).hexdigest()
    return True


probe('unicode_crlf_direct_string_exactness', 'encoding-limit', unicode_crlf, lambda x:x.get('returned') is True)



def wrapper_crlf():
    root = ROOT / 'neutral-crlf-wrapper'
    root.mkdir(exist_ok=True)
    text = '## Alpha\r\nDetail.  \r\n'
    u = v9.units(text)['T001']
    e = entry()
    e['operative_sections'] = [{k:v for k,v in u.items() if k != 'text'}]
    e['clause_ledger'] = [{'requested_clause': 'Which tray receives Alpha', 'section_ids': ['T001'], 'fact_kind': 'lookup'}]
    e['answer'] = 'Applicable summary text\n' + v9.attachment(u)
    (root/'summary-snapshot.md').write_bytes(text.encode())
    (root/'questions.json').write_text(json.dumps({'questions':QUESTIONS}))
    (root/'reader-a.json').write_text(json.dumps({'answers':[e]}))
    return v9.check(root, 'a')


probe('wrapper_normalizes_crlf_rejects_raw_crlf_spans', 'encoding-limit', wrapper_crlf, invalid)


def boundary_check_prefix_unchanged():
    prefixes = []
    for version in ('v8','v9'):
        tree = ast.parse((ROOT/('summary-hierarchical-section-check-'+version+'.py')).read_text())
        function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'check_data')
        loop = next(n for n in function.body if isinstance(n, ast.For) and isinstance(n.target, ast.Name) and n.target.id == 'original')
        prefix = []
        for node in loop.body:
            if isinstance(node, ast.Assign) and any(isinstance(t,ast.Name) and t.id == 'ledger' for t in node.targets): break
            prefix.append(ast.dump(node,include_attributes=False))
        prefixes.append(prefix)
    return prefixes[0] == prefixes[1]


probe('unchanged_boundary_attachment_checks_ast', 'comparison', boundary_check_prefix_unchanged, lambda x:x.get('returned') is True)


probe('duplicate_answer_id_requires_id_flag', 'aggregation-limit', lambda:check({'answers':[entry(),entry()]}), lambda x:valid(x) and x['returned']['exact_ordered_unique_ids'] is False)
probe('nonobject_entry_rejected', 'schema-detected', lambda:check({'answers':[7]}), invalid)
probe('nonlist_answers_rejected', 'schema-detected', lambda:check({'answers':{}}), is_exception)
probe('empty_ledger_rejected', 'schema-detected', lambda:check(mutate(lambda e:e.update(clause_ledger=[]))), invalid)
probe('lookup_empty_legacy_fields_accepted', 'schema-tolerance', lambda:check(mutate(lambda e:e['clause_ledger'][0].update(supported_fact_or_case_result=None, fact_source_section=''))), valid)



def uncovered_top_level():
    text = 'Preamble qualifier.\n# Root\nGlobal qualifier.\n## Alpha\nLocal detail.\n'
    idx = v9.units(text)
    assert idx['T004']['text'] == '## Alpha\nLocal detail.\n'
    assert all('Preamble qualifier.' not in u['text'] and 'Global qualifier.' not in u['text'] for u in idx.values())
    return True


probe('preamble_and_level1_body_unselectable', 'source-precondition', uncovered_top_level, lambda x:x.get('returned') is True)
probe('blockquote_fence_not_rejected', 'source-precondition', lambda:v9.units('## Alpha\n> ```\n> Literal.\n> ```\n'), lambda x:'returned' in x and 'T001' in x['returned'])


if __name__ == '__main__':
    result = {'purpose':'Neutral structural characterization only; accepted semantic errors are documented limits, not graded facts.',
              'python_version':sys.version, 'source_fixture':TEXT, 'question_fixture':QUESTIONS,
              'count':len(CASES), 'matches':sum(c['characterization_matches'] for c in CASES), 'cases':CASES}
    (ROOT/'neutral-results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'count':result['count'],'matches':result['matches']}))
    for c in CASES:
        if not c['characterization_matches']: print(json.dumps(c,ensure_ascii=False))
    raise SystemExit(0 if result['count']==result['matches'] else 1)
