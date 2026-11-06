"""Exact visible-delivery audit. No semantic coverage adjudication."""
import hashlib,json,pathlib,re
O=pathlib.Path(__file__).parent
I=O.parent
H=lambda b:hashlib.sha256(b).hexdigest()
summary=(I/'summary-snapshot.md').read_text()
questions=json.loads((I/'questions.json').read_text())['questions']
namespace={}
exec(compile((I/'source-unit-checker.py').read_text(),str(I/'source-unit-checker.py'),'exec'),namespace)
units=namespace['units'](summary)
def put(name,value):
    (O/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def decode(text):
    try:return json.JSONDecoder().raw_decode(text.lstrip())[0]
    except (ValueError,TypeError):return None
def command(call):
    m=re.search(r'(?:"cmd"|cmd)\s*:\s*("(?:\\.|[^"\\])*")',call['input'])
    return json.loads(m[1]) if m else None
manifest=json.loads((O/'freeze-manifest.json').read_text())
audit={'scope':'First frozen ten-entry turn only; no gameplay grading, source adequacy adjudication, or repairs.',
       'freeze_manifest':'freeze-manifest.json','question_count':len(questions),'final_bank_id':questions[-1]['id'],
       'readers':{},'limits':['Exact output equality establishes delivery, not private attention or comprehension.',
       'Exact attachments and literal ledger references do not establish relevance, governing-rule completeness, or correct gameplay conclusions.',
       'No content scores or score caps assigned. Initial over-limit delivery history cannot be erased by later recovery.'],
       'privacy':'Only allowlisted tool-call inputs, visible tool outputs, narrow model/effort/agent/parent values, and physical record hashes retained. All other runtime record bodies are hash-only.'}
compound_rows={
 'a':{'Q001':[3],'Q002':[4],'Q003':[1],'Q004':[1],'Q005':[4],'Q010':[3]},
 'b':{'Q001':[3],'Q005':[4],'Q010':[3]}}
write_records={'a':[246,260,274,288,302,316,330,344,358,372],
               'b':[263,284,303,322,341,367,386,405,424,449]}
for role in 'ab':
    runtime=json.loads((O/f'reader-{role}-runtime-projection.json').read_text())
    draft=json.loads((O/f'reader-{role}-draft.json').read_text())
    sc=json.loads((O/f'reader-{role}-self-check.json').read_text())
    checks=sc.get('checks',sc.get('records'))
    outputs=runtime['tool_outputs']
    for out in outputs:
        out['text']=''.join(out['visible_text_blocks'][1:])
    firstwrite=write_records[role][0]
    initial=[o for o in outputs if o['physical_record']<firstwrite]
    initial_summary=[]
    lines=summary.splitlines(keepends=True)
    for offset in range(0,len(lines),45):
        text=''.join(lines[offset:offset+45])
        matches=[o['physical_record'] for o in initial if text in o['text']]
        initial_summary.append({'start_line':offset+1,'end_line':min(offset+45,len(lines)),
          'full_LF_text_sha256':H(text.encode()),'exact_contiguous_output_records':matches})
    qdeliveries=[]
    for out in initial:
        decoded=decode(out['text'])
        objects=decoded.get('questions') if isinstance(decoded,dict) and isinstance(decoded.get('questions'),list) else decoded
        if isinstance(objects,list) and objects and all(isinstance(q,dict) and 'id' in q and 'question' in q for q in objects):
            exact=all(q in questions for q in objects)
            qdeliveries.append({'output_record':out['physical_record'],'object_count':len(objects),
              'ids':[q['id'] for q in objects],'complete_original_object_equality':exact,
              'within_six':len(objects)<=6,'output_sha256':H(out['text'].encode())})
    bounded_ids={qid for d in qdeliveries if d['within_six'] and d['complete_original_object_equality'] for qid in d['ids']}
    all_ids={qid for d in qdeliveries if d['complete_original_object_equality'] for qid in d['ids']}
    entries=[]
    lower=219 if role=='a' else 238
    for q,entry,sourcecheck,write in zip(questions,draft['answers'],checks,write_records[role]):
        between=[o for o in outputs if lower<o['physical_record']<write]
        rereads=[o['physical_record'] for o in between if decode(o['text'])==q]
        received=[]
        for meta in entry['operative_sections']:
            u=units[meta['section_id']]
            records=[o['physical_record'] for o in between if u['text'] in o['text']]
            received.append({'section_id':u['section_id'],'start_line':u['start_line'],'end_line':u['end_line'],
              'physical_line_count':len(u['text'].splitlines(keepends=True)),
              'unit_text_sha256':u['sha256'],'exact_full_text_output_records':records,
              'bounded_full_unit_receipt_before_entry':bool(records) and len(u['text'].splitlines(keepends=True))<=45})
        mapped=sourcecheck.get('clause_map',sourcecheck.get('clause_to_unit_map'))
        literal=namespace['check_data'](summary,questions,{'answers':[entry]},role)['checks'][0]
        entries.append({'id':entry['id'],'composition_and_append_call_record':write,
          'question_object_exact_reread_output_records':rereads,'source_unit_receipts':received,
          'manual_selection_evidence':'Literal single-question clause/source choices in the cited call; no code-generated coverage selection.',
          'during_work_selfcheck_written_in_same_call':True,
          'sourcecheck_exact_question':sourcecheck['question']==q['question'],
          'sourcecheck_map_equals_entry':mapped==entry['clause_ledger'],
          'sourcecheck_metadata_equals_entry':sourcecheck['selected_source_metadata']==entry['operative_sections'],
          'literal_attachment_and_phrase_check':literal,
          'syntactically_compound_map_row_numbers':compound_rows[role].get(entry['id'],[]),
          'case_conclusion_present':bool(entry['case_conclusions']),
          'case_conclusion_at_answer_start':not entry['case_conclusions'] or entry['answer'].startswith(entry['case_conclusions'][0])})
        lower=next(o['physical_record'] for o in outputs if o['call_id']==next(c['call_id'] for c in runtime['tool_calls'] if c['physical_record']==write))
    calls=[{'physical_record':c['physical_record'],'tool':c['name'],'command':command(c)} for c in runtime['tool_calls']]
    put(f'reader-{role}-exact-delivery-records.json',{'initial_source_chunks':initial_summary,
      'initial_question_objects':qdeliveries,'per_entry':entries,'tool_method_records':calls})
    actual_initial=[o['physical_record'] for o in initial if re.search(r'truncat(?:ed|ion)',o['text'],re.I)]
    result={'actual_metadata':runtime['actual_metadata'],'first_write_call_record':firstwrite,
      'terminal_first_turn':runtime['task_events'][-1]['event']=='task_complete',
      'answer_count':len(draft['answers']),'ordered_unique_prefix':[a['id'] for a in draft['answers']]==[q['id'] for q in questions[:10]],
      'selfcheck_count':len(checks),'no_partial_final_file':manifest['readers'][role]['files']['final'].get('exists') is False,
      'initial_summary_all_492_full_LF_lines_received_in_11_separate_bounded_outputs':all(d['exact_contiguous_output_records'] for d in initial_summary),
      'all_116_complete_original_objects_received_before_first_write':all_ids=={q['id'] for q in questions},
      'all_objects_also_received_in_bounded_at_most_six_outputs':bounded_ids=={q['id'] for q in questions},
      'not_received_in_bounded_question_outputs':[q['id'] for q in questions if q['id'] not in bounded_ids],
      'oversized_question_delivery_outputs':[d for d in qdeliveries if not d['within_six']],
      'initial_output_truncation_records':actual_initial,
      'every_current_question_exactly_reread_before_entry':all(e['question_object_exact_reread_output_records'] for e in entries),
      'every_selected_unit_completely_received_in_bounded_output_before_entry':all(u['bounded_full_unit_receipt_before_entry'] for e in entries for u in e['source_unit_receipts']),
      'literal_final_prefix_structure_and_attachments_valid':all(e['literal_attachment_and_phrase_check']['all_structure_and_declared_source_spans_valid'] for e in entries),
      'syntactically_compound_map_rows':compound_rows[role],
      'case_format_deviation_ids':[e['id'] for e in entries if not e['case_conclusion_at_answer_start']],
      'per_entry_source_records_present_during_work':all(e['sourcecheck_exact_question'] and e['sourcecheck_map_equals_entry'] and e['sourcecheck_metadata_equals_entry'] for e in entries),
      'selfcheck_flag_qualification':'Per-entry mechanical flags are literal True assignments. Unit boundaries and hashes are actually computed and attachments assembled from those slices. The auditor independently tested exact metadata/text equality; it did not accept the flags as proof. Reader A additionally ran comparisons in call 381; no separate Reader B comparison validator is visible.',
      'method_inspection':'Every visible call inspected: only assigned frozen summary/questions and own draft/self-check paths; source-only heading/slice/hash/serialization operations, one new entry per successful call. No question-to-unit router, ranking, default source, automated semantic grading, unsupported fallback, prefilled ten/whole-bank map, or other-agent/status/web call observed.',
      'next_procedural_disposition':'Current prefix has procedural work outstanding. Do not treat generic next-ID continuation alone as completing the original protocol. Preserve history and originals; source-neutral procedural completion/replay is needed before treating this prefix as method-complete.'}
    audit['readers'][role]=result
audit['historical_notes']={
 'a':['Initial question-list slice failed (call 97/output 100); next call dumped all 116 objects (104/107), over the six-object limit. All 116 were subsequently redelivered in 20 bounded outputs, ending output 219 before first write 246.',
      'An initial question/source reread (232/235) printed a Python list representation rather than raw LF text. Recovered with full exact source text and exact question object in 239/242 before write 246.',
      'A nonliteral Q003 map phrase was written in call 274, then repaired mechanically in call 381. Frozen phrase checks pass; sourcecheck procedural_deviations remains empty.',
      'Q003 has an explicit case conclusion and during-work case reasoning, but the conclusion is absent from the start of answer. No judgment of the conclusion or its arithmetic is made.'],
 'b':['Initial question-list slice failed (95/98); shape inspection (102/105) recovered it. Final initial question response 235/238 delivered eight objects (Q109–Q116); no <=6-object redelivery of those eight occurred before first write 263.',
      'A Q006 append attempt (360/363) failed shell quoting before execution. Retry 367/370 saved the one entry and its sourcecheck; no duplicated entry resulted.']}
audit['syntactic_map_qualification']='Compound-row findings concern visible co-ordinated requested fields/conditions retained in one map row. They do not establish a missing rule, incorrect answer, or gameplay coverage failure. Source IDs and question IDs use the expected padded format.'
audit['auditor_technical_qualification']='The first checker load used importlib SourceFileLoader before switching this reproducible script to compile/exec without bytecode caching. That loader may have generated a Python bytecode cache outside the audit directory; no cache path was inspected or removed, and no original permitted input was edited. This possible auxiliary-file side effect is disclosed separately from reader method findings.'
put('audit.json',audit)
print(json.dumps({r:{k:v for k,v in audit['readers'][r].items() if k in ['answer_count','initial_summary_all_492_full_LF_lines_received_in_11_separate_bounded_outputs','all_116_complete_original_objects_received_before_first_write','all_objects_also_received_in_bounded_at_most_six_outputs','every_current_question_exactly_reread_before_entry','every_selected_unit_completely_received_in_bounded_output_before_entry','literal_final_prefix_structure_and_attachments_valid','case_format_deviation_ids']} for r in 'ab'},indent=2))
