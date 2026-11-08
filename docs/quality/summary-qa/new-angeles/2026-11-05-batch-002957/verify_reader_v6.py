"""Technical V6 verification; semantic adequacy remains a whole-entry grading task."""
from pathlib import Path
import argparse,ast,collections,hashlib,json,sys
sys.dont_write_bytecode=True
B=Path(__file__).parent.resolve()
parser=argparse.ArgumentParser();parser.add_argument('readers',nargs='?',default='ab');parser.add_argument('--iteration',default='expanded-luna-iteration-03');args=parser.parse_args()
I=(B/args.iteration).resolve();assert I.is_relative_to(B)
iteration_number=int(I.name.rsplit('-',1)[-1])
q=json.loads((I/'questions.json').read_text());s=(I/'summary-snapshot.md').read_text()
ns={};code=q['generic_reader_process']['source_extractor_python']
assert hashlib.sha256(code.encode()).hexdigest()==q['generic_reader_process']['source_extractor_sha256']
exec(compile(code,'<frozen-embedded-extractor>','exec'),ns)
questions={x['id']:x['question'] for x in q['questions']}
meta=json.loads((B/'runtime-provenance.json').read_text())
def sha(raw):return hashlib.sha256(raw).hexdigest()
def strings(x):
    if isinstance(x,str):
        yield x
        # Some tools displayed complete records with Python repr, whose escaped
        # newlines remain model-visible. Decode only those literal dictionaries.
        for line in x.splitlines():
            if line.startswith("{'kind':"):
                try:yield from strings(ast.literal_eval(line))
                except (ValueError,SyntaxError):pass
        if x[:1] in ['{','[']:
            try:yield from strings(json.loads(x))
            except (ValueError,TypeError):pass
    elif isinstance(x,list):
        for v in x:yield from strings(v)
    elif isinstance(x,dict):
        for k,v in x.items():
            if k not in ['encrypted_content','internal_chat_message_metadata_passthrough']:yield from strings(v)
report={'scope':'Technical structure/exact units only; no factual score or semantic completeness conclusion.','readers':{}}
for letter in args.readers:
    assert letter in 'ab'
    path=I/f'reader-{letter}.json';r=json.loads(path.read_text());m=next(x for x in meta if x['task']==f'/root/expanded{iteration_number}_reader_'+letter)
    outputs=[]
    for ordinal,line in enumerate(Path(m['runtime_log_path']).open(),1):
        obj=json.loads(line);p=obj.get('payload',{})
        if obj['type']=='response_item' and p.get('type')=='custom_tool_call_output':
            outputs.append(({'record_ordinal':ordinal,'record_sha256':sha(line.encode())},list(strings(p.get('output')))))
    ids=[x['id'] for x in r['answers']];complete=collections.Counter(ids)==collections.Counter(list(questions))
    entries=[];errors=[]
    for answer in r['answers']:
        ident=answer['id'];literal=questions[ident];checks=[]
        for index,e in enumerate(answer['evidence']):
            try:ns['validate_record'](s,e);valid=True
            except Exception as err:valid=False;errors.append({'id':ident,'evidence':index,'error':str(err)})
            units=[e['header'],e['row']] if e['kind']=='table' else [e['unit']]
            text='\n'.join(u['text'] for u in units)
            pieces=[u['text'][i:i+5500] for u in units for i in range(0,len(u['text']),5500)]
            matches=[[rec for rec,values in outputs if any(part in v for v in values)] for part in pieces]
            long_units=[]
            for u in units:
                if len(u['text'])<=5500:continue
                parts=[u['text'][i:i+5500] for i in range(0,len(u['text']),5500)]
                full=[rec for rec,values in outputs if any(u['text'] in v for v in values)]
                oversized_ordinals={v['record_ordinal'] for v in full}
                ordered=[];previous=-1
                for part in parts:
                    hits=[rec for rec,values in outputs if rec['record_ordinal']>previous and rec['record_ordinal'] not in oversized_ordinals and any(part in v for v in values)]
                    if not hits:break
                    hit=min(hits,key=lambda v:v['record_ordinal']);ordered.append(hit);previous=hit['record_ordinal']
                long_units.append({'native_characters':len(u['text']),'whole_unit_found_in_single_output':full,'distinct_ordered_bounded_piece_receipts':ordered,'complete_bounded_span_delivery_verified':len(ordered)==len(parts),'bounded_display_verified':not full and len(ordered)==len(parts)})
            checks.append({'index':index,'exact_extractor_record':valid,'text_chars':len(text),'unit_sha256':sha(text.encode()),'actual_model_visible_piece_receipts':matches,'all_pieces_found':all(matches),'long_unit_rendering_checks':long_units})
        clauses=[]
        for c in answer['clauses']:
            required=['asked_text','asked_start','asked_end','queries','mode','result','evidence_indices']
            ok=all(k in c for k in required)
            if ok:ok=(literal[c['asked_start']:c['asked_end']]==c['asked_text'] and c['mode'] in ['lookup','case'] and bool(c['queries']) and bool(c['result']) and bool(c['evidence_indices']) and all(isinstance(i,int) and 0<=i<len(checks) for i in c['evidence_indices']))
            clauses.append({'literal_span_exact_and_fields_valid':ok,'asked_start':c.get('asked_start'),'asked_end':c.get('asked_end'),'mode':c.get('mode')})
            if not ok:errors.append({'id':ident,'error':'Clause span/fields/evidence indices invalid.'})
        if not answer['answer'] or not clauses:errors.append({'id':ident,'error':'Empty answer/clauses.'})
        mechanical=answer['answer']==' '.join(c['result'] for c in answer['clauses'])
        if not mechanical:errors.append({'id':ident,'error':'Answer differs from mechanical clause-result join.'})
        entries.append({'id':ident,'raw_entry_sha256':sha(json.dumps(answer,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()),'evidence':checks,'clauses':clauses,'answer_is_exact_mechanical_clause_result_join':mechanical})
    report['readers'][letter]={'raw_output_path':str(path),'raw_output_sha256':sha(path.read_bytes()),'answer_count':len(ids),'all94_ids_exactly_once':complete,'generic_evidence_count':sum(len(x['evidence']) for x in entries),'clause_count':sum(len(x['clauses']) for x in entries),'errors':errors,'entries':entries,'all_exact_evidence_validated':all(e['exact_extractor_record'] for x in entries for e in x['evidence']),'all_selected_unit_text_found_in_actual_outputs':all(e['all_pieces_found'] for x in entries for e in x['evidence']),'all_long_selected_units_have_bounded_display_proof':all(u['bounded_display_verified'] for x in entries for e in x['evidence'] for u in e['long_unit_rendering_checks']),'technical_clause_fields_valid':not errors}
if (I/'protocol-diagnostics.json').exists():
    report['protocol_conformance']='Technical record/unit validity PASS; full rendering conformance has a preserved deviation in protocol-diagnostics.json.'
    report['protocol_diagnostics_path']=str(I/'protocol-diagnostics.json')
(I/'v6-technical-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:{f:v[f] for f in ['answer_count','all94_ids_exactly_once','generic_evidence_count','clause_count','all_exact_evidence_validated','all_selected_unit_text_found_in_actual_outputs','technical_clause_fields_valid']} for k,v in report['readers'].items()}))
assert all(v['all94_ids_exactly_once'] and v['all_exact_evidence_validated'] and v['technical_clause_fields_valid'] for v in report['readers'].values())
