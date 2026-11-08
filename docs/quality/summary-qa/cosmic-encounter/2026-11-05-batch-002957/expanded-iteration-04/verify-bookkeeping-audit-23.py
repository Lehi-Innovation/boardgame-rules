#!/usr/bin/env python3
"""Independent technical audit. Standard library only; imports no project code.
Writes only bookkeeping-audit-23.json next to this script. Does not regrade gameplay.
"""
import collections, datetime, hashlib, json, re
from pathlib import Path

IT = Path(__file__).resolve().parent
ROOT = IT.parent
COUNTS = collections.Counter()
FAILURES = []
FILES = {}
ROWS = collections.defaultdict(list)

def sha(v):
    return hashlib.sha256(v.encode('utf-8') if isinstance(v, str) else v).hexdigest()

def canonical(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def nh(v): return sha(canonical(v))

def check(condition, category, context):
    COUNTS[category] += 1
    if not condition: FAILURES.append({'category': category, 'context': context})
    return bool(condition)

def read(path):
    path = Path(path).resolve()
    # Exclude assessment inputs and findings; only named technical evidence is read.
    assert not any(t in path.name for t in ['neutral21', 'neutral-assess', 'bookkeeping-audit-22'])
    raw = path.read_bytes()
    FILES[str(path)] = {'bytes': len(raw), 'sha256': sha(raw)}
    return raw.decode('utf-8')

def doc(path): return json.loads(read(path))

def esc(s): return str(s).replace('~', '~0').replace('/', '~1')

def ptr(value, pointer):
    for k in pointer.split('/')[1:]:
        k = k.replace('~1', '/').replace('~0', '~')
        value = value[int(k)] if isinstance(value, list) else value[k]
    return value

class RawJSON:
    """Traverse original text independently, retaining exact token spans by RFC6901 pointer."""
    def __init__(self, path):
        self.path = Path(path).resolve()
        self.text = read(self.path)
        self.raw = self.text.encode('utf-8')
        self.spans = {}
        self.decoder = json.JSONDecoder()
        self.value, end = self.parse(self.white(0), '')
        check(self.white(end) == len(self.text), 'raw_json_eof', str(path))
        check(self.value == json.loads(self.text), 'raw_json_independent_parse', str(path))
        self.byte = [0]
        for c in self.text: self.byte.append(self.byte[-1] + len(c.encode('utf-8')))
    def white(self, i):
        while i < len(self.text) and self.text[i] in ' \t\r\n': i += 1
        return i
    def parse(self, i, pointer):
        start = i
        if self.text[i] == '{':
            value = {}; i = self.white(i+1)
            while self.text[i] != '}':
                key, i = self.decoder.raw_decode(self.text, i)
                check(key not in value, 'duplicate_json_key_absent', str(self.path)+pointer+'/'+str(key))
                i = self.white(i); assert self.text[i] == ':'
                v, i = self.parse(self.white(i+1), pointer+'/'+esc(key)); value[key] = v
                i = self.white(i)
                if self.text[i] != ',': break
                i = self.white(i+1)
            assert self.text[i] == '}'; i += 1
        elif self.text[i] == '[':
            value = []; i = self.white(i+1)
            while self.text[i] != ']':
                v, i = self.parse(i, pointer+'/'+str(len(value))); value.append(v)
                i = self.white(i)
                if self.text[i] != ',': break
                i = self.white(i+1)
            assert self.text[i] == ']'; i += 1
        else: value, i = self.decoder.raw_decode(self.text, i)
        self.spans[pointer] = (start, i)
        return value, i
    def info(self, pointer):
        a,b = self.spans[pointer]; x,y = self.byte[a],self.byte[b]
        return {'json_pointer': pointer, 'start_char': a, 'end_char': b,
                'start_byte': x, 'end_byte': y, 'raw_sha256': sha(self.raw[x:y]),
                'normalized_sha256': nh(ptr(self.value,pointer))}

def walk(value, path=''):
    yield path,value
    if isinstance(value,dict):
        for k,v in value.items(): yield from walk(v,path+'/'+esc(k))
    elif isinstance(value,list):
        for i,v in enumerate(value): yield from walk(v,path+'/'+str(i))

def ref_paths(entry):
    refs = collections.defaultdict(list)
    for path,v in walk(entry):
        # All explicit scalar evidence references, wherever placed in the original entry.
        if isinstance(v,(str,int)) and re.search(r'/evidence_refs/\d+$',path):
            refs[str(v)].append((path,v))
    return refs

AUDIT_INSTRUCTIONS=read(IT/'bookkeeping-audit-instructions-v1.txt')
QDOC=doc(IT/'questions.json'); Q=QDOC['questions']; IDS=[q['id'] for q in Q]; N=len(IDS)
KEYDOC=doc(IT/'answer-key.json'); KEYS=KEYDOC['answers']; KM={k['id']:k for k in KEYS}
SCOPE=doc(IT/'actual-question-scope.json'); SM={r['id']:r for r in SCOPE['questions']}
SUMMARY=read(IT/'summary-snapshot.md')
check(len(set(IDS))==N,'ordered_question_ids_unique',IDS)
check([k['id'] for k in KEYS]==IDS,'key_order_equals_questions',None)
check(list(SM)==IDS,'scope_order_equals_questions',None)
for name,field in [('questions.json','questions'),('answer-key.json','answers')]:
    candidate=doc(ROOT/'expanded-candidate-16'/name)
    check(doc(IT/name)[field]==candidate[field],'candidate16_complete_records',name)
# Current canonical map is a technical literal-scope artifact, not a new source reading.
canonical_map=ROOT/'source-review/literal-scope-map-14-v5.json'
if canonical_map.exists():
    cm=doc(canonical_map)
    check(SCOPE==cm,'current_canonical_scope_whole_file',str(canonical_map))
for q in Q:
    ident=q['id']; k=KM[ident]; s=SM[ident]
    check(s['question_record_exact']==q,'canonical_question_record',ident)
    check(s['key_record_exact']==k,'canonical_key_record',ident)
    check(s['literal_question']==q['question'] and s['question_utf8_sha256']==sha(q['question']),'canonical_literal_question',ident)
    check(s['key_record_canonical_json_sha256']==nh(k),'canonical_key_hash',ident)
    check([f['raw_required_fact'] for f in s['fact_classifications']]==k['required_facts'],'canonical_raw_fact_records',ident)
RAW_FACT_N=sum(len(k['required_facts']) for k in KEYS)
READERS={r:RawJSON(IT/f'reader-{r}.json') for r in 'ab'}
for r,raw in READERS.items():
    check([e['id'] for e in raw.value['answers']]==IDS,'raw_reader_order',r)

# Check both wrappers against independently located original tokens, not against each other only.
ALL_BLOCK_IDS=[]; PACKETS={}; FACT_REFS={}
for block in range(1,10):
    oldp=IT/f'grading-inputs/block-{block:02}.json'; newp=IT/f'grading-inputs-v2/block-{block:02}.json'
    old,new=doc(oldp),doc(newp); block_ids=[e['id'] for e in new['entries']]
    ALL_BLOCK_IDS.extend(block_ids)
    check(block_ids==new['expected_ids']==old['expected_ids'],'block_ids',block)
    check([e['id'] for e in old['entries']]==block_ids,'intermediate_block_ids',block)
    check(new['original_bundle_path']==str(oldp) and new['original_bundle_sha256']==FILES[str(oldp)]['sha256'],'original_bundle_binding',block)
    for bundle,kind in [(old,'intermediate'),(new,'materialized')]:
        check(bundle['complete_summary_path']==str(IT/'summary-snapshot.md') and bundle['summary_sha256']==sha(SUMMARY),'packet_summary_binding',{'block':block,'kind':kind})
        for entry in bundle['entries']:
            ident=entry['id']; idx=IDS.index(ident); q=Q[idx]; k=KM[ident]
            check(entry['literal_question']==q,'packet_literal_question',{'id':ident,'kind':kind})
            check(entry['key']==k,'packet_key_record',{'id':ident,'kind':kind})
            check(entry['validated_actual_scope']==SM[ident],'packet_actual_scope_exact_current',{'id':ident,'kind':kind})
            check(entry['key_entry_sha256']==nh(k) and entry['question_entry_sha256']==nh(q),'packet_key_question_hashes',{'id':ident,'kind':kind})
            expectedrefs=[{'id':f'{ident}-F{i+1:02}','index':i,'sha256':sha(f)} for i,f in enumerate(k['required_facts'])]
            check(entry['raw_key_fact_refs']==expectedrefs,'packet_raw_key_refs',{'id':ident,'kind':kind})
            FACT_REFS[ident]=expectedrefs
            for r,raw in READERS.items():
                w=entry['readers'][r]; pointer=f'/answers/{idx}'; info=raw.info(pointer); original=ptr(raw.value,pointer)
                context={'reader':r,'id':ident,'kind':kind}
                check(w['complete_original_entry']==original,'complete_original_entry_all_fields',context)
                check(w['id']==ident and w['raw_file_path']==str(raw.path) and w['raw_file_sha256']==sha(raw.raw),'entry_original_file_binding',context)
                for name in ['start_char','end_char','start_byte','end_byte']:
                    check(w[name]==info[name],'entry_exact_'+name,context)
                check(w['raw_entry_sha256']==info['raw_sha256'],'entry_raw_utf8_sha256',context)
                check(w['normalized_entry_sha256']==info['normalized_sha256'],'entry_normalized_hash',context)
                check(json.loads(raw.raw[w['start_byte']:w['end_byte']])==original,'entry_raw_byte_slice_decodes_exactly',context)
                check(json.loads(raw.text[w['start_char']:w['end_char']])==original,'entry_raw_unicode_slice_decodes_exactly',context)
                if kind=='materialized':
                    PACKETS[(r,ident)]=w
                    ROWS['raw_entries'].append(dict(context,raw_file=str(raw.path),**info))
                    pool=raw.value['evidence_units']; refs=ref_paths(original)
                    attached=w['explicitly_referenced_shared_evidence']
                    check(attached['raw_reader_path']==str(raw.path) and attached['raw_reader_sha256']==sha(raw.raw),'reference_pool_file_binding',context)
                    check(attached['pool_field']=='/evidence_units' and attached['complete_pool_normalized_sha256']==nh(pool),'reference_complete_pool_hash',context)
                    units=attached['resolved_units']
                    check([u['reference'] for u in units]==list(refs),'all_and_only_explicit_same_entry_references',context)
                    for u in units:
                        ref=u['reference']; origin=refs[ref]
                        if isinstance(pool,dict): key=ref; value=pool[key]
                        else:
                            candidates=[(j,x) for j,x in enumerate(pool) if str(x.get('id',j))==ref]
                            assert len(candidates)==1; key,value=candidates[0]
                        up='/evidence_units/'+esc(key); ui=raw.info(up)
                        c=dict(context,reference=ref,pointer=up)
                        check(u['original_unit']==value,'reference_unit_all_fields',c)
                        check(u['original_unit_sha256']==nh(value),'reference_unit_normalized_hash',c)
                        us=u['original_raw_unit_span']
                        check(us['collection_key']==key and all(us[k]==v for k,v in ui.items()),'reference_unit_exact_pointer_spans_hashes',c)
                        check(u['explicit_reference_paths_in_original_entry']==[p for p,v in origin],'reference_all_originating_paths',c)
                        check(u['original_entry_reference_value']==origin[0][1],'reference_original_scalar_value',c)
                        for path,v in origin: check(ptr(original,path)==v and str(v)==ref,'reference_origin_pointer_resolves',dict(c,path=path))
                        check(json.loads(raw.raw[ui['start_byte']:ui['end_byte']])==value,'reference_raw_byte_span_decodes_exactly',c)
                        # Diagnostics are measured, never prerequisites for packaging or grade caps.
                        quote=value.get('text',''); occurs=quote in SUMMARY
                        source_span=SUMMARY[value.get('start',0):value.get('end',0)]==quote
                        check(u['unit_text_matches_frozen_summary']==occurs,'reference_quote_diagnostic_truth',c)
                        check(u['declared_source_span_matches_text']==source_span,'reference_source_span_diagnostic_truth',c)
                        if 'sha256' in value: check(value['sha256']==sha(quote),'reference_declared_quote_hash',c)
                        ROWS['reference_units'].append(dict(c,**{k:v for k,v in ui.items() if k!='json_pointer'},origin_paths=[p for p,v in origin],quote_occurs_in_summary=occurs,declared_summary_span_matches=source_span))
    # Existing intermediate reader wrappers must be unchanged after materialization.
    for a,b in zip(old['entries'],new['entries']):
        for r in 'ab':
            x=dict(b['readers'][r]);x.pop('explicitly_referenced_shared_evidence',None)
            check(a['readers'][r]==x,'intermediate_wrapper_unchanged',{'block':block,'id':a['id'],'reader':r})
check(ALL_BLOCK_IDS==IDS,'nine_disjoint_blocks_exact_ordered_partition',None)
check(len(set(ALL_BLOCK_IDS))==N,'nine_disjoint_blocks_no_overlap',None)

# All 34 fixed snapshots: exact prefixes and preserved earlier entries/pool values.
SCHEDULE=doc(IT/'fixed-blind-batch-schedule.json'); schedule=SCHEDULE['schedule']
check(len(schedule)==(N+9)//10,'fixed_snapshot_count_derived_from_N',None)
for i,b in enumerate(schedule):
    check(b=={'batch':i+1,'start_record_index':i*10,'end_record_index_exclusive':min((i+1)*10,N)},'fixed_schedule_exact_boundaries',i+1)
cont=read(IT/'generic-continuation-message.txt')
check(cont.strip()==SCHEDULE['identical_generic_continuation_message'],'saved_constant_continuation_schedule',None)
for r,raw in READERS.items():
    prev=None
    for b in schedule:
        path=IT/f"reader-{r}-batch-{b['batch']:02}.json"; s=doc(path);end=b['end_record_index_exclusive']
        check([e['id'] for e in s['answers']]==IDS[:end],'snapshot_exact_id_prefix',{'reader':r,'batch':b['batch']})
        check(s['answers']==raw.value['answers'][:end],'snapshot_exact_final_answer_prefix',{'reader':r,'batch':b['batch']})
        check(s['continuation']['completed_count']==end and s['continuation']['next_record_index_zero_based']==end and s['continuation']['bank_complete']==(end==N),'snapshot_continuation_metadata',{'reader':r,'batch':b['batch']})
        pool=s['evidence_units']; previous_entries=0;previous_units=0
        if prev:
            previous_entries=len(prev['answers']);previous_units=len(prev['evidence_units'])
            check(s['answers'][:previous_entries]==prev['answers'],'snapshot_earlier_answers_unchanged',{'reader':r,'batch':b['batch']})
            for k,v in prev['evidence_units'].items(): check(pool[k]==v,'snapshot_earlier_dictionary_value_unchanged',{'reader':r,'batch':b['batch'],'key':k})
            for k in ['instructions_read','inputs_read','method_code_sha256']:
                check(s[k]==prev[k],'snapshot_frozen_receipts_unchanged',{'reader':r,'batch':b['batch'],'field':k})
        for k,v in pool.items(): check(raw.value['evidence_units'][k]==v,'snapshot_dictionary_exact_final_value',{'reader':r,'batch':b['batch'],'key':k})
        for e,q in zip(s['answers'],Q):
            check(e['id']==q['id'],'snapshot_id_question_order',{'reader':r,'batch':b['batch'],'id':e['id']})
            # A literal mismatch is recorded as reader data, not changed or converted to a grade.
            ROWS['literal_bindings'].append({'reader':r,'batch':b['batch'],'id':e['id'],'literal_matches_current_question':e.get('literal_question')==q['question'],'actual_literal_sha256':sha(e.get('literal_question','')),'expected_literal_sha256':sha(q['question'])})
            for ref in ref_paths(e): check(ref in pool,'snapshot_reference_available',{'reader':r,'batch':b['batch'],'id':e['id'],'reference':ref})
        ROWS['snapshots'].append({'reader':r,'batch':b['batch'],'path':str(path),'sha256':FILES[str(path)]['sha256'],'answer_count':end,'dictionary_unit_count':len(pool),'earlier_answers_preserved':previous_entries,'earlier_dictionary_values_preserved':previous_units,'literal_mismatch_ids':[e['id'] for e,q in zip(s['answers'],Q) if e.get('literal_question')!=q['question']]})
        prev=s
    check(prev==raw.value,'final_snapshot_complete_raw_equivalence',r)
    check(FILES[str(IT/f'reader-{r}-batch-{len(schedule):02}.json')]['sha256']==sha(raw.raw),'final_snapshot_exact_bytes',r)

# Frozen input and embedded code/process hashes. No source approval follows from this.
manifest=doc(IT/'input-manifest-final.json')
for path,digest in manifest['sha256'].items():
    check(sha(read(path))==digest,'frozen_manifest_file_hash',path)
RQ=doc(IT/'reader-questions-final.json'); process=RQ['reader_process'];code=read(IT/'generic-method-code.py')
check(RQ['questions']==Q,'reader_question_records_exact',None)
check(process['instructions_sha256']==sha(process['instructions']),'embedded_process_hash',None)
check(process['method_code_sha256']==sha(code) and manifest['generic_code_sha256']==sha(code),'embedded_method_code_hash',None)
check(code in process['instructions'],'embedded_exact_method_code_body',None)

# Original grade indexing is lossless by immutable report hash + resolving original pointer.
AGG=doc(IT/'original-grades-aggregate.json'); totals={}; flag_rows=[]; grade_ids={r:[] for r in 'ab'}; fact_ids={r:[] for r in 'ab'}
GRADE_DOCS={}
for b in range(1,10):
    path=IT/f'grades-{b:02}.json';g=doc(path);GRADE_DOCS[b]=g
    rp=AGG['original_reports'][b-1]; bid=[e['id'] for e in doc(IT/f'grading-inputs-v2/block-{b:02}.json')['entries']]
    check(rp['block']==b and rp['path']==str(path) and rp['sha256']==FILES[str(path)]['sha256'] and rp['expected_ids']==bid,'aggregate_original_report_binding',b)
    check(g['exact_assigned_ids']==bid,'grader_exact_assigned_ids',b)
    for r in 'ab':
        es=g['readers'][r]['entries'];check([e['id'] for e in es]==bid,'grader_entry_ids_partition',{'block':b,'reader':r})
        gt=collections.Counter(e['grade'] for e in es)
        check(all(g['readers'][r]['totals'].get(k,0)==gt[k] for k in ['correct','partial','incorrect']),'original_grader_totals',{'block':b,'reader':r})
        for total_key in ['total','assigned']:
            if total_key in g['readers'][r]['totals']:
                check(g['readers'][r]['totals'][total_key]==len(es),'original_grader_assigned_total',{'block':b,'reader':r,'field':total_key})
        for j,e in enumerate(es):
            ident=e['id'];grade_ids[r].append(ident);packet=PACKETS[r,ident]
            wrappers=[v for v in e.values() if isinstance(v,dict) and 'complete_original_entry' in v and 'raw_entry_sha256' in v]
            check(len(wrappers)==1 and wrappers[0]==packet,'grade_lossless_complete_packet',{'reader':r,'id':ident})
            check(e['observed_raw_entry_hash']==packet['raw_entry_sha256'],'grade_observed_raw_hash',{'reader':r,'id':ident})
            if 'observed_normalized_entry_hash' in e:check(e['observed_normalized_entry_hash']==packet['normalized_entry_sha256'],'grade_observed_normalized_hash',{'reader':r,'id':ident})
            fcs=e['fact_checks'];expected=FACT_REFS[ident];fids=[f.get('fact_id',f.get('id')) for f in fcs]
            fact_ids[r].extend(fids)
            check(fids==[v['id'] for v in expected],'all_raw_facts_exactly_once',{'reader':r,'id':ident})
            for i,(fc,rf) in enumerate(zip(fcs,expected)):
                ctx={'reader':r,'id':ident,'fact':rf['id']};sid=f'{ident}.RF{i+1:03}'
                check(fc.get('validated_scope_fact_id',fc.get('scope_fact_id',sid))==sid,'fact_assessment_scope_id',ctx)
                for k in ['raw_key_fact','raw_required_fact','raw_fact_text']:
                    if k in fc:check(fc[k]==KM[ident]['required_facts'][i],'fact_assessment_exact_raw_text',dict(ctx,field=k))
                for k in ['raw_key_fact_sha256','raw_fact_sha256']:
                    if k in fc:check(fc[k]==rf['sha256'],'fact_assessment_raw_text_hash',dict(ctx,field=k))
                if 'raw_key_fact_ref' in fc:check(fc['raw_key_fact_ref']==rf,'fact_assessment_raw_ref',ctx)
                check(any(k in fc for k in ['classification','status']),'fact_assessment_present',ctx)
                ROWS['fact_assessments'].append(dict(ctx,report_path=str(path),json_pointer=f'/readers/{r}/entries/{j}/fact_checks/{i}',assessment_sha256=nh(fc),scope_fact_id=sid))
            # Canonical scope rows are already exact in every packet; grade clause labels are
            # assessed for identity where supplied, not schema-capped or semantically regraded.
            clauses=SM[ident]['clauses'];cc=e.get('clause_checks',[])
            for c in cc:
                if 'clause_id' in c:
                    cs=next((x for x in clauses if x['clause_id']==c['clause_id']),None)
                    check(cs is not None,'grade_clause_ref_current_scope',{'reader':r,'id':ident,'clause_id':c['clause_id']})
                    if cs and 'asked_clause' in c:check(c['asked_clause']==cs['asked_clause'],'grade_asked_clause_exact_current_scope',{'reader':r,'id':ident,'clause_id':c['clause_id']})
            flags={k:e.get(k,[]) for k in ['unsupported_correct_claims','material_contradictions','missing_asked_facts']}
            if any(flags.values()):flag_rows.append({'reader':r,'id':ident,'grade':e['grade'],'report_path':str(path),'json_pointer':f'/readers/{r}/entries/{j}',**flags})
            ar=[x for x in AGG['readers'][r] if x['id']==ident]
            check(len(ar)==1,'aggregate_exactly_one_grade_index',{'reader':r,'id':ident})
            if ar:
                ar=ar[0];point=f'/readers/{r}/entries/{j}'
                check(ar['report_path']==str(path) and ar['report_sha256']==FILES[str(path)]['sha256'] and ar['json_pointer']==point,'aggregate_immutable_lossless_grade_pointer',{'reader':r,'id':ident})
                check(ptr(g,ar['json_pointer'])==e and ar['grade']==e['grade'] and ar['original_grade_retained'] is True,'aggregate_original_grade_retained',{'reader':r,'id':ident})
                check(ar['unsupported_claim_flags']==len(flags['unsupported_correct_claims']),'aggregate_unsupported_flags_not_hidden',{'reader':r,'id':ident})
for r in 'ab':
    check(grade_ids[r]==IDS and len(set(grade_ids[r]))==N,'all_original_grade_ids_once',r)
    expected=[x['id'] for ident in IDS for x in FACT_REFS[ident]]
    check(fact_ids[r]==expected and len(set(fact_ids[r]))==RAW_FACT_N,'all_raw_fact_assessments_once_per_reader',r)
    totals[r]=dict(collections.Counter(e['grade'] for b in range(1,10) for e in GRADE_DOCS[b]['readers'][r]['entries']))
    check(AGG['totals'][r]==totals[r],'aggregate_totals_recomputed',r)
    check([e['id'] for e in AGG['readers'][r]]==IDS,'aggregate_ordered_ids',r)
check(AGG['question_count']==N and AGG['raw_key_record_count_per_reader']==RAW_FACT_N,'aggregate_current_bank_counts',None)
unsupported=sum(len(x['unsupported_correct_claims']) for x in flag_rows)
check(AGG['unsupported_correct_claim_count']==unsupported,'aggregate_unsupported_count',None)
check(AGG['primary_all_correct_by_grade']==all(totals[r].get('correct',0)==N for r in 'ab'),'aggregate_all_correct_flag_truth',None)
ROWS['original_grade_flags']=flag_rows

# Actual external runtime evidence. Decode only PUBLIC tool result text and tool
# call arguments required for input delivery/settings; never emit encrypted bodies.
def result_texts(output, depth=0):
    if depth>8:return []
    if isinstance(output,list):
        return [t for x in output for t in result_texts(x,depth+1)]
    if isinstance(output,dict):
        return [t for k,v in output.items() if k in ['text','output','content','value'] for t in result_texts(v,depth+1)]
    if not isinstance(output,str):return []
    result=[output]
    candidates=[output.strip()]
    for marker in ['Output:\n\n','Output:\n']:
        if marker in output:candidates.append(output.split(marker,1)[1].strip())
    for s in candidates:
        if s.startswith(('{','[')):
            try:
                decoded=result_texts(json.loads(s),depth+1)
                if decoded: return decoded
            except (ValueError,TypeError):pass
    return result

def runtime(path):
    raw=Path(path).read_bytes(); lines=raw.splitlines(keepends=True)
    # Runtime files are append-only external evidence and are not copied.
    records=[json.loads(x) for x in lines]
    return {'path':str(path),'bytes_observed':len(raw),'observed_prefix_sha256':sha(raw),'lines':lines,'records':records}

def record_proof(rt,i):
    return {'runtime_path':rt['path'],'record_ordinal_zero_based':i,'timestamp':rt['records'][i].get('timestamp'),'record_sha256_including_lf':sha(rt['lines'][i])}

def outputs(rt):
    result=[]
    for i,o in enumerate(rt['records']):
        p=o.get('payload',{})
        if o.get('type')=='response_item' and p.get('type') in ['custom_tool_call_output','function_call_output']:
            ts=result_texts(p.get('output'))
            result.append((i,ts))
    return result

def receipt_chunks(receipt):
    chunks=receipt.get('chunks',receipt.get('actual_delivered_chunks',[]))
    result=[]
    for c in chunks:
        start=c.get('start',c.get('start_char',c.get('start_char_inclusive')))
        end=c.get('end',c.get('end_char_exclusive'))
        digest=c.get('sha256',c.get('utf8_chunk_sha256',c.get('sha256_utf8')))
        result.append((start,end,digest))
    return result

def delivery(receipt,rt,outs,before,role):
    path=Path(receipt['path']);text=read(path);chunks=receipt_chunks(receipt);position=0; proofs=[]
    ctx={'task':role,'path':str(path)}
    check(receipt.get('bytes',len(text.encode()))==len(text.encode()) and receipt.get('characters',len(text))==len(text),'receipt_file_size',ctx)
    check(receipt.get('sha256',receipt.get('full_file_sha256'))==sha(text),'receipt_file_hash',ctx)
    for a,b,h in chunks:
        cc=dict(ctx,start=a,end=b)
        check(a==position and isinstance(b,int) and a<b<=len(text),'receipt_contiguous_full_ranges',cc);position=b
        chunk=text[a:b]
        check(h==sha(chunk),'receipt_chunk_hash_recomputed',cc)
        # Require exact plaintext availability within an actual delivered tool result,
        # and before the first write for the initial complete two-file proof.
        found=[i for i,ts in outs if i<before and any(chunk in t for t in ts)]
        check(bool(found),'actual_public_payload_exact_chunk_before_write',cc)
        bound=len(chunk)<=6000
        check(bound,'individual_declared_display_chunk_max6000',cc)
        proofs.append({'start':a,'end':b,'utf8_sha256':sha(chunk),'characters':len(chunk),'actual_runtime_outputs':[record_proof(rt,i) for i in found]})
    check(position==len(text) and bool(chunks),'receipt_full_eof_nonvacuous',ctx)
    return dict(ctx,characters=len(text),bytes=len(text.encode()),sha256=sha(text),declared_chunks=len(chunks),first_write_ordinal=before,full_eof=position==len(text),chunks=proofs)

PROV=doc(ROOT/'model-provenance.json'); agents={a['task']:a for a in PROV['agents']}
root_rt=runtime(agents['/root']['runtime_source_path'])
spawns={}; followups=collections.defaultdict(list); snapshot_calls=collections.defaultdict(list)
for i,o in enumerate(root_rt['records']):
    p=o.get('payload',{});name=p.get('name','')
    if p.get('type') in ['function_call','custom_tool_call']:
        if name in ['spawn_agent','followup_task']:
            try:args=json.loads(p.get('arguments',p.get('input','')))
            except ValueError:continue
            if name=='spawn_agent' and args.get('task_name','').startswith(('expanded4_reader_','expanded4_grader_')):
                spawns['/root/'+args['task_name']]={'settings':{k:v for k,v in args.items() if k!='message'},**record_proof(root_rt,i)}
            elif name=='followup_task' and args.get('target','').startswith('/root/expanded4_reader_'):
                followups[args['target']].append(record_proof(root_rt,i))
        if name=='exec':
            s=p.get('input','')
            for r in 'ab':
                if f'snapshot_blind_batch.py expanded-iteration-04 {r}' in s or ('snapshot_blind_batch.py expanded-iteration-04 ${c}' in s and "['a','b'].map" in s):
                    snapshot_calls[r].append(dict(record_proof(root_rt,i),timestamp=o.get('timestamp')))

selected=[f'/root/expanded4_reader_{r}' for r in 'ab']+[f'/root/expanded4_grader_{b:02}' for b in range(1,10)]
for task in selected:
    a=agents[task];rt=runtime(a['runtime_source_path']);outs=outputs(rt);reader='reader_' in task
    expected_model='gpt-6-luna' if reader else 'gpt-6.1-sol';turn_n=len(schedule) if reader else 1
    meta=rt['records'][0]['payload']
    check(meta.get('id')==a['identity'] and meta.get('parent_thread_id')==agents['/root']['identity'],'actual_runtime_identity_parent',task)
    check(meta.get('agent_path')==task,'actual_runtime_task_identity',task)
    turns=[(i,o) for i,o in enumerate(rt['records']) if o.get('type')=='turn_context']
    check(len(turns)==turn_n,'actual_model_turn_count',task)
    turn_rows=[]
    for i,o in turns:
        z=o['payload'];check(z.get('model')==expected_model and z.get('effort')=='high','actual_model_effort_each_turn',{'task':task,'ordinal':i})
        turn_rows.append(dict(record_proof(rt,i),timestamp=o.get('timestamp'),turn_id=z.get('turn_id'),actual_model=z.get('model'),actual_effort=z.get('effort')))
    check(len({x['turn_id'] for x in turn_rows})==turn_n,'distinct_actual_turn_ids',task)
    spawn=spawns.get(task)
    check(bool(spawn),'actual_root_spawn_exists',task)
    if spawn:
        ss=spawn['settings'];check(ss.get('fork_turns')=='none' and ss.get('model')==expected_model and ss.get('reasoning_effort')=='high','actual_root_requested_fresh_model_effort',task)
    writes=[]
    for i,o in enumerate(rt['records']):
        z=o.get('payload',{});s=z.get('input',z.get('arguments',''))
        if z.get('type') in ['custom_tool_call','function_call'] and isinstance(s,str) and any(t in s for t in ['write_text(','write_bytes(']):
            writes.append(i)
    check(bool(writes),'runtime_output_write_observed',task)
    before=min(writes) if writes else len(rt['records'])
    receipts=READERS[task[-1]].value['inputs_read'] if reader else [GRADE_DOCS[int(task[-2:])]['instructions_read']]+GRADE_DOCS[int(task[-2:])]['inputs_read']
    expected_paths=[str(IT/'summary-snapshot.md'),str(IT/'reader-questions-final.json')] if reader else [str(IT/f'grader-{int(task[-2:]):02}-instructions.txt'),str(IT/'summary-snapshot.md'),str(IT/f'grading-inputs-v2/block-{int(task[-2:]):02}.json')]
    check([x['path'] for x in receipts]==expected_paths,'actual_required_full_input_paths',task)
    for receipt in receipts:ROWS['runtime_deliveries'].append(delivery(receipt,rt,outs,before,task))
    # Transport events reflect actual wrappers, not occurrences of words in the game text.
    diagnostics=[];oversized=[]
    for i,ts in outs:
        truncated=any(re.search(r'Warning: truncated output|[\u2026.]\s*\d+\s+tokens truncated',t) for t in ts)
        errors=[]
        for t in ts:
            if 'command not found' in t:errors.append('command_not_found')
            if 'Traceback (most recent call last):' in t:errors.append('python_traceback')
        if truncated or errors:diagnostics.append(dict(record_proof(rt,i),truncated=truncated,error_types=sorted(set(errors))))
        # Only decoded innermost command output; multi-block large responses counted
        # separately from the maximum individual declared chunk size.
        if ts and max(map(len,ts))>6500:oversized.append(dict(record_proof(rt,i),maximum_public_text_characters=max(map(len,ts))))
    if reader:
        r=task[-1]
        check(len(followups[task])==len(schedule)-1,'actual_root_reader_continuation_count',task)
        check(len(snapshot_calls[r])==len(schedule),'actual_root_snapshot_capture_count',task)
        # Each snapshot capture and subsequent continuation occurs after the respective
        # reader turn begins; encrypted continuation text itself is unavailable.
        for j,capture in enumerate(snapshot_calls[r]):
            start=turns[j][1].get('timestamp') if j<len(turns) else None
            check(start is not None and capture['timestamp']>=start,'snapshot_capture_after_actual_turn_start',{'task':task,'batch':j+1})
            end_ordinal=turns[j+1][0] if j+1<len(turns) else len(rt['records'])
            turn_writes=[k for k in writes if turns[j][0]<k<end_ordinal]
            check(bool(turn_writes),'actual_reader_each_turn_output_write',{'task':task,'batch':j+1})
            if turn_writes:
                check(rt['records'][turn_writes[-1]]['timestamp']<=capture['timestamp'],'snapshot_capture_after_actual_turn_write',{'task':task,'batch':j+1})
            if j<len(followups[task]):
                follow=followups[task][j]
                check(capture['record_ordinal_zero_based']<follow['record_ordinal_zero_based'],'snapshot_capture_before_next_root_continuation',{'task':task,'batch':j+1})
                check(follow['timestamp']<=turns[j+1][1]['timestamp'],'actual_continuation_before_next_same_identity_turn',{'task':task,'batch':j+1})
    ROWS['runtime_identities'].append({'task':task,'identity':a['identity'],'runtime_path':rt['path'],'runtime_bytes_observed':rt['bytes_observed'],'runtime_observed_prefix_sha256':rt['observed_prefix_sha256'],'session_record':record_proof(rt,0),'actual_turns':turn_rows,'requested_spawn':spawn,'first_write_ordinal':before,'all_write_ordinals':writes,'actual_root_continuation_records':followups.get(task,[]),'actual_root_snapshot_capture_records':snapshot_calls.get(task[-1],[]) if reader else [],'transport_events':diagnostics,'responses_over6500_characters':oversized,'runtime_fork_context_field':None,'encrypted_initial_and_continuation_plaintext_equality':None})

# Discrepancies in original data stay separate from failed technical integrity checks.
literal_mismatches=[{'reader':r,'id':e['id'],'actual_literal_question':e.get('literal_question'),'expected_literal_question':q['question']} for r,raw in READERS.items() for e,q in zip(raw.value['answers'],Q) if e.get('literal_question')!=q['question']]
quote_diagnostics=[u for u in ROWS['reference_units'] if not u['quote_occurs_in_summary'] or not u['declared_summary_span_matches']]
# Verify every original data file read by this implementation stayed byte-identical.
for path,meta in list(FILES.items()):
    check(sha(Path(path).read_bytes())==meta['sha256'],'original_evidence_unchanged_during_audit',path)
SCRIPT_HASH=sha(Path(__file__).read_bytes())
report={
 'verification_script':{'path':str(Path(__file__).resolve()),'sha256':SCRIPT_HASH},
 'audit':'Independent technical bookkeeping audit 23',
 'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'iteration':str(IT),'technical_pass':not FAILURES,'technical_verdict':'PASS' if not FAILURES else 'FAIL',
 'scope':'Bookkeeping, transport and runtime identity proof only. No gameplay regrading, source-authority approval, new source vote, global readiness or stamping approval.',
 'independence':'Fresh standard-library implementation; no parent materializer/verifier/aggregator code imported, executed or used as an oracle. Original reader JSON and nine original grades directly parsed. Parent technical validation summaries not used as proof. Separate neutral assessment inputs/findings excluded.',
 'derived_counts':{'question_count':N,'ordered_ids':IDS,'raw_key_records_per_reader':RAW_FACT_N,'raw_fact_assessments_verified':len(ROWS['fact_assessments']),'whole_original_entries_verified':len(ROWS['raw_entries']),'entry_wrapper_checks':COUNTS['complete_original_entry_all_fields'],'original_entry_raw_spans_verified':len(ROWS['raw_entries']),'referent_raw_span_attachments_verified':len(ROWS['reference_units']),'distinct_raw_entry_and_referent_spans_verified':len(ROWS['raw_entries'])+len({(u['reader'],u['pointer']) for u in ROWS['reference_units']}),'same_entry_reference_unit_attachments_verified':len(ROWS['reference_units']),'distinct_raw_reference_units_verified':len({(u['reader'],u['pointer']) for u in ROWS['reference_units']}),'originating_reference_paths_verified':COUNTS['reference_origin_pointer_resolves'],'snapshots_verified':len(ROWS['snapshots']),'literal_question_bindings_examined_across_snapshots':len(ROWS['literal_bindings']),'actual_identities_verified':len(ROWS['runtime_identities']),'actual_reader_turns_verified':sum(len(x['actual_turns']) for x in ROWS['runtime_identities'] if 'reader_' in x['task']),'actual_grader_turns_verified':sum(len(x['actual_turns']) for x in ROWS['runtime_identities'] if 'grader_' in x['task']),'actual_input_files_verified':len(ROWS['runtime_deliveries']),'actual_declared_chunks_verified':sum(x['declared_chunks'] for x in ROWS['runtime_deliveries'])},
 'executed_assertions_total':sum(COUNTS.values()),'executed_assertions_by_category':dict(COUNTS),'failed_checks':FAILURES,
 'original_grade_totals_recomputed':totals,'original_grade_flags':flag_rows,
 'preserved_reader_data_diagnostics':{'literal_question_mismatches_final':literal_mismatches,'same_entry_quote_or_declared_source_span_mismatches':quote_diagnostics,'policy':'Observed original answer/question or quotation diagnostics are preserved and reported as data, not automatic gameplay grades or packaging failures.'},
 'limitations':[
  'Runtime task/continuation bodies are encrypted and plaintext is unavailable. No encrypted body is exposed, decrypted, or asserted equal to a saved prompt/constant. Actual same-identity turn ordering, requested root settings, saved constant schedule, and public input payloads are separately verified.',
  'fork_turns:none is independently observed in actual submitted root spawn arguments. External child runtime metadata does not expose a fork-context field; no independent runtime fresh-context field is claimed.',
  'Public delivered input availability and exact bytes/characters do not prove semantic comprehension or correctness. No gameplay judgments were changed and no confidence, schema, locator, process, source-wide or unasked-background caps were imposed.',
  'Questions/key compared in full to candidate16; old167/seed20 preservation was not separately recertified in this audit. This audit performs no new primary source reading.',
  'Root runtime is append-only and may continue growing; reported whole-file hash is the observed prefix at read time. Exact relevant record hashes including line LF are stable evidence.',
  'Original aggregate uses immutable report hashes and original resolving pointers rather than embedding every assessment field. Missing/contradiction flags remain losslessly reachable through those original pointers and are explicitly inventoried here.'
 ],
 'raw_span_convention':'Zero-based half-open Unicode codepoint and UTF-8 byte offsets independently parsed from original tokens. Normalized hashes use compact sorted-key ensure_ascii=false JSON. Every originating reference path is RFC6901 and resolves inside the same original answer entry.',
 'data_files':FILES,'evidence':dict(ROWS)
}
# Avoid accidentally replacing an already completed audit without explicit invocation.
out=IT/'bookkeeping-audit-23.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'output':str(out),'technical_pass':report['technical_pass'],'checks':sum(COUNTS.values()),'failures':len(FAILURES),'counts':report['derived_counts'],'first_failures':FAILURES[:12]},ensure_ascii=False))
