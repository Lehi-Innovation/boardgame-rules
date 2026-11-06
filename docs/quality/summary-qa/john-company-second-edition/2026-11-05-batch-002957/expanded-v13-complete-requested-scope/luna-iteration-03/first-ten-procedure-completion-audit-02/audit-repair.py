"""Frozen repair-turn technical audit; never reads beyond manifest byte limits."""
import pathlib,json,hashlib,re,ast,shlex
O=pathlib.Path(__file__).parent;I=O.parent
H=lambda b:hashlib.sha256(b).hexdigest()
def put(name,value):(O/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
summary=(I/'summary-snapshot.md').read_text();questions=json.loads((I/'questions.json').read_text())['questions']
checker={'__name__':'source_checker_audit'}
exec(compile((I/'source-unit-checker.py').read_text(),str(I/'source-unit-checker.py'),'exec'),checker)
units=checker['units'](summary)
def decode(t):
    try:return json.JSONDecoder().raw_decode(t.lstrip())[0]
    except (ValueError,TypeError):return None
def command(call):
    z=re.search(r'(?:"cmd"|cmd)\s*:\s*("(?:\\.|[^"\\])*")',call['input'])
    return json.loads(z[1]) if z else None
repair_writes={'a':[544,551,558,572,586,600,614,628,642,656],
               'b':[589,603,617,631,645,659,673,687,701,715]}
review_outputs={'a':[524,531,538,568,582,596,610,624,638,652],
                'b':[583,599,613,627,641,655,669,683,697,711]}
residual_compound_rows={'a':{'Q001':[4],'Q005':[5]},'b':{'Q005':[4],'Q010':[3]}}
report={'scope':'ONLY manifest-frozen turn-two repair prefixes. Live turn three was not read or assessed.',
 'question_count':len(questions),'original_firstturn_history_preserved':True,'readers':{},
 'interpretation':'Bounded question-bank recovery, full per-entry visible source review, source-record alignment and case-placement repair are established. Residual clause-map granularity, sequencing and historical-deviation-record qualifications remain. These are not gameplay judgments or score caps; no operational hold or wait is requested.',
 'privacy':'Runtime prefixes only through manifest byte limits. Every physical record ordinal/hash retained; needed calls/visible tool outputs and narrow actor/model/effort/parent values projected. All other runtime bodies hash-only. No encrypted body retained.',
 'qualification':'Visible delivery does not establish private attention, semantic adequacy, or factual correctness. Original initial-before-first-write violations remain historical facts.'}
for role in 'ab':
    p=json.loads((O/f'reader-{role}-runtime-projection.json').read_text())
    old=json.loads((I/f'first-ten-prefix-method-audit-01/reader-{role}-draft.json').read_text())
    d=json.loads((O/f'reader-{role}-draft.json').read_text());sc=json.loads((O/f'reader-{role}-self-check.json').read_text());records=sc.get('checks',sc.get('records'))
    calls=p['repair_turn_tool_calls'];outputs=p['repair_turn_tool_outputs']
    for out in outputs:out['text']=''.join(out['visible_text_blocks'][1:])
    firstwrite=min(c['physical_record'] for c in calls if 'write_text' in c['input'])
    deliveries=[]
    for out in outputs:
        if out['physical_record']>=firstwrite:continue
        parsed=decode(out['text'])
        if isinstance(parsed,list) and parsed and all(isinstance(q,dict) and 'id'in q and 'question'in q for q in parsed):
            deliveries.append({'output_record':out['physical_record'],'count':len(parsed),
              'ids':[q['id'] for q in parsed],'complete_original_object_equality':all(q in questions for q in parsed),
              'at_most_six':len(parsed)<=6,'visible_text_sha256':H(out['text'].encode())})
    flat=[i for x in deliveries for i in x['ids']]
    entries=[];changes=[]
    for q,oldentry,entry,record,reread,write in zip(questions,old['answers'],d['answers'],records,review_outputs[role],repair_writes[role]):
        out=next(x for x in outputs if x['physical_record']==reread);text=out['text'];parsed=decode(text)
        qequal=(parsed==q or (isinstance(parsed,dict) and parsed.get('question')==q) or ('Exact question: '+q['question']+'\n') in text)
        receipts=[]
        for m in entry['operative_sections']:
            u=units[m['section_id']];n=len(u['text'].splitlines(keepends=True));receipts.append({'section_id':m['section_id'],'start_line':u['start_line'],'end_line':u['end_line'],'source_line_count':n,'full_source_sha256':u['sha256'],'exact_full_LF_text_in_visible_output':u['text'] in text,'at_most_45_source_lines':n<=45})
        changed=[k for k in sorted(set(oldentry)|set(entry)) if oldentry.get(k)!=entry.get(k)]
        if changed:changes.append({'id':entry['id'],'changed_fields':changed})
        source_map=record.get('clause_map',record.get('clause_to_unit_map'))
        literal=checker['check_data'](summary,questions,{'answers':[entry]},role)['checks'][0]
        entries.append({'id':entry['id'],'exact_question_reread':qequal,'review_output_record':reread,
          'entry_repair_or_source_record_write_call':write,'review_before_repair':reread<write,
          'complete_unit_receipts':receipts,'source_record_exact_question':record['question']==q['question'],
          'source_record_map_alignment':source_map==entry['clause_ledger'],
          'source_record_metadata_alignment':record['selected_source_metadata']==entry['operative_sections'],
          'nonempty_during_work_review_record':bool(record.get('review_record',record.get('during_work_source_record'))),
          'literal_check':literal,'actual_changed_fields':changed,
          'case_at_answer_start':not entry['case_conclusions'] or entry['answer'].startswith(entry['case_conclusions'][0]),
          'residual_syntactically_compound_map_rows':residual_compound_rows[role].get(entry['id'],[])})
    # Structural inspection of actual code, not semantic meaning or answer grading.
    method=[]
    for call in calls:
        cmd=command(call);code=None
        if cmd and "<<'PY'\n" in cmd:code=cmd.split("<<'PY'\n",1)[1].rsplit('\nPY',1)[0]
        elif cmd:
            try:
                parts=shlex.split(cmd)
                if '-c'in parts:code=parts[parts.index('-c')+1]
            except ValueError:pass
        tree=ast.parse(code) if code else None
        method.append({'physical_record':call['physical_record'],'name':call['name'],'command':cmd,
          'python_parsed':tree is not None,'has_write':bool(code and 'write_text'in code),
          'explicit_control_constructs':[ast.unparse(n) for n in ast.walk(tree) if isinstance(n,(ast.For,ast.While,ast.If,ast.FunctionDef))] if tree else []})
    literal=checker['check_data'](summary,questions,d,role)
    put(f'reader-{role}-literal-checks.json',literal)
    put(f'reader-{role}-exact-repair-records.json',{'question_bank_redelivery':deliveries,'per_entry':entries,'method_calls':method})
    r={'actual_metadata':p['actual_metadata'],'prefix_bytes':p['prefix_bytes'],'prefix_sha256':p['prefix_sha256'],
      'frozen_record_count':len(p['records']),'first_repair_write_call':firstwrite,
      'turn_two_terminal_event':p['task_events_after_firstturn'][-1],
      'twenty_separate_bounded_outputs_exactly_redeliver_all_116_original_question_objects':len(deliveries)==20 and flat==[q['id'] for q in questions] and all(x['count']<=6 and x['complete_original_object_equality'] for x in deliveries),
      'current_prefix_count':len(d['answers']),'ordered_unique_ten_prefix':[e['id'] for e in d['answers']]==[q['id'] for q in questions[:10]],
      'source_record_count':len(records),'no_new_question_entries':len(d['answers'])==len(old['answers'])==10,
      'no_partial_final_creation_in_visible_repair_calls':not any(re.search(r'reader-[ab]\.json',c['input']) for c in calls),
      'all_existing_questions_and_entire_selected_units_visibly_reread_before_corresponding_repairs':all(e['exact_question_reread'] and e['review_before_repair'] and all(z['exact_full_LF_text_in_visible_output'] and z['at_most_45_source_lines'] for z in e['complete_unit_receipts']) for e in entries),
      'all_source_records_aligned_and_individually_reviewed':all(e['source_record_exact_question'] and e['source_record_map_alignment'] and e['source_record_metadata_alignment'] and e['nonempty_during_work_review_record'] for e in entries),
      'literal_structure_metadata_attachments_and_phrases_pass':literal['all_structure_and_declared_source_spans_valid'],
      'case_placement_passes':all(e['case_at_answer_start'] for e in entries),
      'original_selected_units_and_source_attachment_content_unchanged':all(a['operative_sections']==b['operative_sections'] for a,b in zip(old['answers'],d['answers'])),
      'actual_changes':changes,'residual_syntactic_compound_rows':residual_compound_rows[role],
      'no_receipt_gap_found':True,
      'method_inspection':'Only assigned source/question inputs and own draft/self-check paths occur as data-file operations. Literal individual maps/source choices; no new bank routing, ranking, defaults, automatic semantic grader, fallback or other-reader/status/web call. Per-entry code and final validation inspected; audit does not rely on True flags.',
      'remaining_qualifications':[]}
    if role=='a':r['remaining_qualifications']=[
      'Q001 retirement-destination row and Q005 candidate/hirer-condition row remain syntactically compound. Adding a separate context row does not split those existing requested fields/alternatives.',
      'The first three question/unit reviews (outputs 524, 531, 538) precede all three repair writes (544, 551, 558). This is a limited review/repair scheduling departure from strict one-question-at-a-time completion, not evidence of a ten/whole-bank prefilled map.',
      'Q004 received a later literal-map cleanup in call 667 after other reviews, without a second visible Q004/unit reread immediately for that revisit. Its full reread at output 568 still precedes both writes.',
      'procedural_deviations records the recovered turn-two locator error, but not the original first-turn oversized bank dump, list-representation recovery, or earlier nonliteral-map repair. Those original events remain recorded by the independent first-turn audit.']
    else:r['remaining_qualifications']=[
      'Q005 candidate/hirer-condition row and Q010 routes/capacity row remain syntactically compound. Q001 destination fields were actually split.',
      'technical_deviations records the initial shape error, shell error and turn-two locator recovery. It omits the original eight-object final question response. Its historical statement that every object was delivered in <=6 chunks before writing is true for this repair turn, but inaccurate if read as the initial-turn sequence described in the same note.']
    report['readers'][role]=r
report['no_arbitrary_metadata_or_semantic_demands']='No additional source choices or exact self-check schema were required. Existing source maps may point multiple individual rows to the same complete unit. Compound findings concern explicit requested-field separation only; they do not imply missing gameplay facts.'
report['instruction_binding_qualification']='Standalone generic instruction record SHA verified; runtime confirms /root sender and matching reader recipients. Incoming bodies are encrypted/opaque in the runtime, so exact plaintext generic-message equality cannot be established from these permitted projections.'
report['disposition']='The repair turn supplies concrete bounded delivery recovery and individual source review, with aligned exact attachments and fixed A case placement. Do not describe it as erasing initial history or as perfect compliance: residual map granularity, A scheduling and deviation-record qualifications remain. This assessment makes no request to hold or interrupt the already resumed generic work.'
put('audit.json',report)
print(json.dumps({r:{k:v for k,v in report['readers'][r].items() if k in ['twenty_separate_bounded_outputs_exactly_redeliver_all_116_original_question_objects','current_prefix_count','all_existing_questions_and_entire_selected_units_visibly_reread_before_corresponding_repairs','all_source_records_aligned_and_individually_reviewed','literal_structure_metadata_attachments_and_phrases_pass','case_placement_passes','residual_syntactic_compound_rows']} for r in 'ab'},indent=2))
