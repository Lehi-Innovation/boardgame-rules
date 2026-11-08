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
PRESERVED_ARCHIVE_HASHES={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [IT.parent/'expanded-iteration-04/bookkeeping-audit-23.json',IT.parent/'expanded-iteration-04/verify-bookkeeping-audit-23.py',IT/'initial-transport-technical-audit-23.json',IT/'verify-initial-transport-technical-audit-23.py']}

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
    assert not any(t in path.name.lower() for t in ['neutral', 'bookkeeping-audit-22'])
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

AUDIT_INSTRUCTIONS=read(IT/'bookkeeping-audit-instructions-v2.txt')
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
REPAIR=doc(IT/'reader-a-transport-repair-01.json')
INITIALS={r:doc(IT/f'reader-{r}-batch-01.json') for r in 'ab'}
for k in ['answers','evidence_units','instructions_read','method_code_sha256','continuation']:
    check(REPAIR[k]==INITIALS['a'][k],'transport_archive_preserves_initial_values',k)
check(REPAIR['initial_inputs_read']==INITIALS['a']['inputs_read'],'transport_archive_preserves_raw_initial_receipts',None)
check(READERS['a'].value['initial_inputs_read']==INITIALS['a']['inputs_read'],'final_A_preserves_initial_receipts',None)
check(REPAIR['inputs_read']==READERS['a'].value['inputs_read'],'transport_repair_final_receipts_equal',None)
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
                expected=REPAIR[k] if r=='a' and b['batch']==2 else prev[k]
                check(s[k]==expected,'snapshot_frozen_receipts_unchanged_or_exact_documented_repair',{'reader':r,'batch':b['batch'],'field':k})
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

# Exact clause associations are metadata diagnostics, never automatic gameplay caps.
for r,raw in READERS.items():
    for i,(entry,q) in enumerate(zip(raw.value['answers'],Q)):
        for j,c in enumerate(entry['clauses']):
            a,b=c.get('question_start'),c.get('question_end')
            valid=isinstance(a,int) and isinstance(b,int) and 0<=a<b<=len(q['question']) and q['question'][a:b]==c.get('literal_ask')
            ROWS['clause_literal_bindings'].append({'reader':r,'id':entry['id'],'json_pointer':f'/answers/{i}/clauses/{j}','question_start':a,'question_end':b,'literal_ask_sha256':sha(c.get('literal_ask','')),'exact_current_question_substring':valid})
# Frozen input and embedded code/process hashes. No source approval follows from this.
manifest=doc(IT/'input-manifest-final.json')
for path,digest in manifest['sha256'].items():
    check(sha(read(path))==digest,'frozen_manifest_file_hash',path)
RQ=doc(IT/'reader-questions-final.json'); process=RQ['reader_process'];code=read(IT/'generic-method-code.py')
check(RQ['questions']==Q,'reader_question_records_exact',None)
check(process['instructions_sha256']==sha(process['instructions']),'embedded_process_hash',None)
check(process['method_code_sha256']==sha(code) and manifest['generic_code_sha256']==sha(code),'embedded_method_code_hash',None)
check(code in process['instructions'],'embedded_exact_method_code_body',None)
for r,raw in READERS.items():
    metadata=raw.value['instructions_read']
    records=[metadata['question_file_process_metadata']] if isinstance(metadata,dict) else [x for x in metadata if isinstance(x,dict)]
    for rec in records:
        target=ptr(RQ,rec['json_pointer']);actual_digest=sha(target) if rec['json_pointer'].endswith('/instructions') else target
        check(rec['path']==str(IT/'reader-questions-final.json') and rec.get('instructions_sha256',rec.get('sha256'))==actual_digest,'reader_instruction_digest_alias_resolves_exactly',{'reader':r,'pointer':rec['json_pointer']})
    check(raw.value['method_code_sha256']==sha(code),'reader_declared_method_code_digest_exact',r)


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
            fcs=e['fact_checks'];expected=FACT_REFS[ident];fids=[f.get('fact_id',f.get('id',f.get('key_fact_id'))) for f in fcs]
            fact_ids[r].extend(fids)
            check(fids==[v['id'] for v in expected],'all_raw_facts_exactly_once',{'reader':r,'id':ident})
            for i,(fc,rf) in enumerate(zip(fcs,expected)):
                ctx={'reader':r,'id':ident,'fact':rf['id']};sid=f'{ident}.RF{i+1:03}'
                check(fc.get('validated_scope_fact_id',fc.get('scope_fact_id',sid))==sid,'fact_assessment_scope_id',ctx)
                for k in ['raw_key_fact','raw_required_fact','raw_fact_text','raw_key_fact_exact']:
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
                if 'clause_id' in c or 'id' in c:
                    c=dict(c,clause_id=c.get('clause_id',c.get('id')))
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
    chunks=receipt.get('chunks',receipt.get('actual_delivered_chunks',receipt.get('actual_chunks',[])))
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



# Actual runtimes, including initial failure, later transport-only reread and compaction.
def compact_ranges(ranges):
    result=[]
    for a,b in sorted(ranges):
        if result and a<=result[-1][1]:result[-1][1]=max(result[-1][1],b)
        else:result.append([a,b])
    return result

def uncovered(ranges,n):
    result=[];at=0
    for a,b in compact_ranges(ranges):
        if a>at:result.append([at,a])
        at=max(at,b)
    if at<n:result.append([at,n])
    return result

def actual_delivery(receipt,rt,outs,lo,hi,role,require_complete=True,reader_protocol=False,keep=True):
    path=Path(receipt['path']);text=read(path);raw=text.encode();chunks=receipt_chunks(receipt)
    char_ok=[0<=a<b<=len(text) and sha(text[a:b])==h for a,b,h in chunks]
    byte_ok=[0<=a<b<=len(raw) and sha(raw[a:b])==h for a,b,h in chunks]
    mode='Unicode_characters' if all(char_ok) else ('UTF8_bytes' if all(byte_ok) else 'inconsistent')
    ctx={'task':role,'path':str(path)}
    check(mode!='inconsistent','receipt_coordinate_mode_independently_resolved',ctx)
    check(receipt.get('bytes',len(raw))==len(raw) and receipt.get('characters',len(text))==len(text),'actual_receipt_file_sizes',ctx)
    check(receipt.get('sha256',receipt.get('full_file_sha256'))==sha(raw),'actual_receipt_file_hash',ctx)
    rows=[];at=0;seen=[];bounded_seen=[]
    for a,b,h in chunks:
        if mode=='UTF8_bytes':
            chunk=raw[a:b].decode();ca=len(raw[:a].decode());cb=len(raw[:b].decode());ba,bb=a,b
        else:chunk=text[a:b];ca,cb=a,b;ba=len(text[:a].encode());bb=len(text[:b].encode())
        c=dict(ctx,original_start=a,original_end=b,unit=mode)
        check(a==at,'actual_receipt_original_ranges_contiguous',c);at=b
        check(h==sha(chunk),'actual_receipt_exact_chunk_hash',c)
        check(raw[ba:bb].decode()==text[ca:cb]==chunk,'byte_unicode_normalization_one_to_one',c)
        matches=[i for i,ts in outs if lo<=i<hi and any(chunk in t for t in ts)]
        bounded=[i for i,ts in outs if lo<=i<hi and any(chunk in t and len(t)<=6500 and 'Warning: truncated output' not in t and not re.search(r'\d+ tokens truncated',t) for t in ts) and len(chunk)<=5800]
        if require_complete:
            check(bool(matches),'actual_exact_payload_available_in_assigned_time_window',c)
            if reader_protocol:check(bool(bounded),'actual_reader_original_response_bounded_before_save',c)
        if matches:seen.append([ca,cb])
        if bounded:bounded_seen.append([ca,cb])
        rows.append({'original_start':a,'original_end':b,'start_char':ca,'end_char':cb,'start_byte':ba,'end_byte':bb,'characters':len(chunk),'sha256':h,'exact_public_payloads':[record_proof(rt,i) for i in matches],'original_bounded_reader_payloads':[record_proof(rt,i) for i in bounded],'declared_digest_printed_in_same_public_result':any(h in t for i,ts in outs if i in matches for t in ts)})
    check(at==(len(raw) if mode=='UTF8_bytes' else len(text)) and bool(chunks),'actual_receipt_original_unit_eof',ctx)
    result=dict(ctx,window_start_inclusive=lo,window_end_exclusive=hi,original_offset_unit=mode,characters=len(text),bytes=len(raw),sha256=sha(raw),declared_chunks=len(rows),actually_matched_chunks=sum(bool(x['exact_public_payloads']) for x in rows),original_bounded_chunks=sum(bool(x['original_bounded_reader_payloads']) for x in rows),exact_raw_source_visible_ranges=compact_ranges(seen),bounded_reader_visible_ranges=compact_ranges(bounded_seen),missing_exact_declared_raw_source_ranges=uncovered(seen,len(text)),missing_bounded_reader_ranges=uncovered(bounded_seen,len(text)),chunks=rows)
    if keep:ROWS['runtime_deliveries'].append(result)
    return result

PROV=doc(ROOT/'model-provenance.json');agents={a['task']:a for a in PROV['agents']}
root_rt=runtime(agents['/root']['runtime_source_path']);spawns={};followups=collections.defaultdict(list);snapshot_calls=collections.defaultdict(list)
for i,o in enumerate(root_rt['records']):
    z=o.get('payload',{});name=z.get('name','')
    if z.get('type') not in ['function_call','custom_tool_call']:continue
    if name in ['spawn_agent','followup_task']:
        try:a=json.loads(z.get('arguments',z.get('input','')))
        except ValueError:continue
        if name=='spawn_agent' and a.get('task_name','').startswith(('expanded5_reader_','expanded5_grader_')):
            spawns['/root/'+a['task_name']]=dict(record_proof(root_rt,i),settings={k:v for k,v in a.items() if k!='message'})
        elif name=='followup_task' and a.get('target','').removeprefix('/root/').startswith('expanded5_reader_'):
            followups['/root/'+a['target'].removeprefix('/root/')].append(record_proof(root_rt,i))
    if name=='exec':
        src=z.get('input','')
        for r in 'ab':
            if f'snapshot_blind_batch.py expanded-iteration-05 {r}' in src or ('snapshot_blind_batch.py expanded-iteration-05 ${c}' in src and ("['a','b'].map" in src or '["a","b"].map' in src)):
                snapshot_calls[r].append(record_proof(root_rt,i))

CHRONOLOGY={};RT={}
selected=[f'/root/expanded5_reader_{r}' for r in 'ab']+[f'/root/expanded5_grader_{i:02}' for i in range(1,10)]
check(len({agents[t]['identity'] for t in selected})==len(selected),'all_current_reader_and_grader_identities_distinct',None)
for task in selected:
    rt=runtime(agents[task]['runtime_source_path']);RT[task]=rt;outs=outputs(rt);is_reader='reader_' in task;r=task[-1] if is_reader else None
    contexts=[(i,o) for i,o in enumerate(rt['records']) if o.get('type')=='turn_context']
    starts=[(i,o) for i,o in enumerate(rt['records']) if o.get('payload',{}).get('type')=='task_started']
    compacted=[i for i,o in enumerate(rt['records']) if o.get('type')=='compacted']
    expected_tasks=len(schedule)+(1 if r=='a' else 0) if is_reader else 1
    check(len(starts)==expected_tasks,'actual_distinct_task_turn_count',task)
    check(len(contexts)==expected_tasks+(1 if r=='a' else 0),'actual_all_context_record_count',task)
    check(len(compacted)==(1 if r=='a' else 0),'actual_automatic_compaction_count',task)
    expected_model='gpt-6-luna' if is_reader else 'gpt-6.1-sol'
    for i,o in contexts:check(o['payload'].get('model')==expected_model and o['payload'].get('effort')=='high','actual_model_effort_every_context',dict(task=task,ordinal=i))
    context_ids=[o['payload']['turn_id'] for i,o in contexts];task_ids=[o['payload']['turn_id'] for i,o in starts]
    check(set(context_ids)==set(task_ids) and len(set(task_ids))==expected_tasks,'all_contexts_map_to_actual_task_turns',task)
    if r=='a':
        check(len(context_ids)-len(set(context_ids))==1,'A_compaction_repeats_existing_turn_identity',task)
        ci=compacted[0];previous=[o['payload']['turn_id'] for i,o in contexts if i<ci][-1];following=[o['payload']['turn_id'] for i,o in contexts if i>ci][0]
        check(previous==following,'A_compaction_does_not_create_answer_batch',task)
    meta=rt['records'][0]['payload']
    check(meta.get('id')==agents[task]['identity'] and meta.get('agent_path')==task and meta.get('parent_thread_id')==agents['/root']['identity'],'actual_session_identity_task_parent',task)
    spawn=spawns.get(task);check(bool(spawn),'actual_spawn_record_present',task)
    if spawn:check(spawn['settings'].get('fork_turns')=='none' and spawn['settings'].get('model')==expected_model and spawn['settings'].get('reasoning_effort')=='high','actual_spawn_requested_fresh_model_effort',task)
    write_calls=[]
    for i,o in enumerate(rt['records']):
        z=o.get('payload',{});src=z.get('input',z.get('arguments',''))
        if z.get('type') in ['custom_tool_call','function_call'] and isinstance(src,str) and any(w in src for w in ['write_text(','write_bytes(','open(']) and any(w in src for w in ['write_text(','write_bytes(','.write(']):write_calls.append(i)
    check(bool(write_calls),'actual_output_producing_call_observed',task)
    initial_write=min(write_calls)
    if not is_reader:
        check(rt['records'][0]['timestamp']>max(snapshot_calls[r][-1]['timestamp'] for r in 'ab'),'actual_grader_identity_created_after_completed_readers',task)
        g=GRADE_DOCS[int(task[-2:])];receipts=[g['instructions_read']]+g['inputs_read']
        check([x['path'] for x in receipts]==[str(IT/f'grader-{int(task[-2:]):02}-instructions.txt'),str(IT/'summary-snapshot.md'),str(IT/f'grading-inputs-v2/block-{int(task[-2:]):02}.json')],'grader_complete_required_input_assignment',task)
        for receipt in receipts:actual_delivery(receipt,rt,outs,0,initial_write,task)
    else:
        check(len(followups[task])==expected_tasks-1,'actual_reader_followup_task_count',task)
        check(len(snapshot_calls[r])==len(schedule),'actual_fixed_snapshot_capture_calls',task)
        # Answer batches exclude the separately observed transport-only task turn.
        answer_starts=starts[:1]+starts[2:] if r=='a' else starts
        check(len(answer_starts)==len(schedule),'actual_answer_batch_task_count',task)
        for j,capture in enumerate(snapshot_calls[r]):
            start_idx,start=answer_starts[j];next_start=starts[starts.index((start_idx,start))+1][0] if starts.index((start_idx,start))+1<len(starts) else len(rt['records'])
            ws=[i for i in write_calls if start_idx<i<next_start]
            check(bool(ws),'each_actual_answer_task_has_output_write',dict(task=task,batch=j+1))
            check(capture['timestamp']>=start['timestamp'],'snapshot_capture_after_answer_task_start',dict(task=task,batch=j+1))
            if ws:check(rt['records'][ws[-1]]['timestamp']<=capture['timestamp'],'snapshot_capture_after_answer_write',dict(task=task,batch=j+1))
            if j+1<len(answer_starts):check(capture['timestamp']<answer_starts[j+1][1]['timestamp'],'snapshot_capture_before_next_answer_task',dict(task=task,batch=j+1))
        initial=[]
        for receipt in INITIALS[r]['inputs_read']:initial.append(actual_delivery(receipt,rt,outs,0,initial_write,task+'/initial',require_complete=r=='b',reader_protocol=True))
        if r=='b':
            check(all(x['original_offset_unit']=='UTF8_bytes' for x in initial) and sum(x['declared_chunks'] for x in initial)==24,'B_original_24_byte_blocks_not_unicode_offset_claim',None)
            check(READERS[r].value['inputs_read']==INITIALS[r]['inputs_read'],'B_original_byte_receipts_preserved_all_the_way',None)
            CHRONOLOGY['b']={'initial_complete_before_first_write':True,'coordinate_normalization':'Original byte offsets, exact byte hashes and actual public payloads mapped one-to-one to Unicode boundaries, with complete EOF coverage. No original ranges replaced.','initial_write_containing_call':record_proof(rt,initial_write),'initial_files':initial}
        else:
            check(not all(x['actually_matched_chunks']==x['declared_chunks'] for x in initial),'A_initial_material_data_incomplete_observed',None)
            guide=next(x for x in initial if x['path'].endswith('summary-snapshot.md'));question=next(x for x in initial if x['path'].endswith('reader-questions-final.json'))
            check(guide['bounded_reader_visible_ranges']==[[0,5800]] and question['bounded_reader_visible_ranges']==[],'A_initial_bounded_proof_only_guide_first5800',None)
            save_results=[i for i,ts in outs if any(re.search(r'saved\s+10\s+answers',t) for t in ts)]
            check(bool(save_results),'A_actual_initial10_save_success_result_observed',None)
            save_result=min(save_results);save_call_id=rt['records'][save_result]['payload']['call_id']
            save_call=next(i for i,o in enumerate(rt['records']) if o.get('payload',{}).get('call_id')==save_call_id and o.get('payload',{}).get('type') in ['custom_tool_call','function_call'])
            actual_pre_save=[actual_delivery(receipt,rt,outs,0,save_call,task+'/initial_before_actual_successful_save',require_complete=False,reader_protocol=True,keep=False) for receipt in INITIALS[r]['inputs_read']]
            check(not all(x['actually_matched_chunks']==x['declared_chunks'] for x in actual_pre_save),'A_still_materially_incomplete_at_actual_first_successful_write',None)
            check([x['bounded_reader_visible_ranges'] for x in actual_pre_save]==[[[0,5800]],[]],'A_no_later_before_save_bounded_full_input_repair',None)
            survivors=[]
            for i,ts in outs:
                if i>=initial_write:continue
                for payload in ts:
                    if len(payload)<=6500:continue
                    for name in ['summary-snapshot.md','reader-questions-final.json']:
                        source=read(IT/name);prefix=payload.find(source[:200]);suffix=payload.find(source[-200:])
                        if prefix>=0:
                            n=0
                            while n<len(source) and prefix+n<len(payload) and source[n]==payload[prefix+n]:n+=1
                            survivors.append(dict(record_proof(rt,i),path=str(IT/name),start_char=0,end_char=n,payload_start_char=prefix,payload_end_char=prefix+n,qualifies_as_bounded_delivery=False))
                        if suffix>=0:
                            end=suffix+200;n=0
                            while n<len(source) and end-n-1>=0 and source[len(source)-n-1]==payload[end-n-1]:n+=1
                            survivors.append(dict(record_proof(rt,i),path=str(IT/name),start_char=len(source)-n,end_char=len(source),payload_start_char=end-n,payload_end_char=end,qualifies_as_bounded_delivery=False))
            sr={name:compact_ranges([[x['start_char'],x['end_char']] for x in survivors if x['path']==str(IT/name)]) for name in ['summary-snapshot.md','reader-questions-final.json']}
            check(sr['summary-snapshot.md']==[[0,19653]] and sr['reader-questions-final.json']==[[50155,70117]],'A_exact_original_oversized_truncated_survivors',None)
            visible_questions=[q['id'] for q in Q if any(q['question'] in t for i,ts in outs if i<initial_write for t in ts)]
            repair_lo=starts[1][0];repair_hi=min(i for i in write_calls if repair_lo<i<starts[2][0]);repaired=[]
            for receipt in REPAIR['inputs_read']:repaired.append(actual_delivery(receipt,rt,outs,repair_lo,repair_hi,task+'/later_transport_only',reader_protocol=True))
            check(sum(x['declared_chunks'] for x in repaired)==46 and all(x['original_offset_unit']=='Unicode_characters' for x in repaired),'A_later_reread_exact_46_original_unicode_blocks',None)
            check(snapshot_calls[r][0]['timestamp']<rt['records'][repair_lo]['timestamp'],'A_repair_after_initial10_archive',None)
            check(repair_hi<starts[2][0],'A_complete_reread_before_new_answer_task',None)
            check(repair_hi<write_calls[-1],'A_complete_reread_before_final_writer',None)
            check(REPAIR['answers']==INITIALS['a']['answers'] and REPAIR['evidence_units']==INITIALS['a']['evidence_units'],'A_transport_only_archive_no_answers_or_dictionary_rewritten',None)
            CHRONOLOGY['a']={'initial_complete_before_first_write':False,'initial_strict_transport_verdict':'FAIL; material RULE/QUESTION data missing before first10 save','initial_write_containing_call':record_proof(rt,initial_write),'actual_first_successful_reader_output_save_call':record_proof(rt,save_call),'actual_first_successful_reader_output_save_result':record_proof(rt,save_result),'initial_files':initial,'files_verified_before_actual_successful_first_save':actual_pre_save,'original_oversized_result_survivors':survivors,'original_guide_raw_missing_ranges':uncovered(sr['summary-snapshot.md'],len(SUMMARY)),'original_question_file_raw_missing_ranges':uncovered(sr['reader-questions-final.json'],len(read(IT/'reader-questions-final.json'))),'initial_exact_literal_questions_visible':visible_questions,'initial_exact_literal_questions_not_visible':[q['id'] for q in Q if q['id'] not in visible_questions],'later_transport_task_start':record_proof(rt,repair_lo),'later_transport_archive_write_containing_call':record_proof(rt,repair_hi),'later_full_reread_files':repaired,'transport_only_archive_path':str(IT/'reader-a-transport-repair-01.json'),'transport_only_archive_sha256':FILES[str(IT/'reader-a-transport-repair-01.json')]['sha256'],'first10_and_dictionary_and_original_receipts_preserved':True,'retroactive_initial_complete_claim':False}
    diag=[];large=[]
    for i,ts in outs:
        truncated=any(re.search(r'Warning: truncated output|[\u2026.]\s*\d+\s+tokens truncated',t) for t in ts)
        errors=[]
        for t in ts:
            if 'command not found' in t:errors.append('command_not_found')
            if 'Traceback (most recent call last):' in t:errors.append('python_traceback')
        if truncated or errors:diag.append(dict(record_proof(rt,i),truncated=bool(truncated),error_types=sorted(set(errors))))
        if ts and max(map(len,ts))>6500:large.append(dict(record_proof(rt,i),maximum_actual_public_text_characters=max(map(len,ts))))
    ROWS['runtime_identities'].append({'task':task,'identity':agents[task]['identity'],'runtime_path':rt['path'],'runtime_bytes_observed':rt['bytes_observed'],'runtime_observed_prefix_sha256':rt['observed_prefix_sha256'],'session_record':record_proof(rt,0),'actual_turns':[dict(record_proof(rt,i),turn_id=o['payload']['turn_id'],actual_model=o['payload'].get('model'),actual_effort=o['payload'].get('effort')) for i,o in contexts],'actual_task_turns':[dict(record_proof(rt,i),turn_id=o['payload'].get('turn_id')) for i,o in starts],'automatic_compaction_records':[record_proof(rt,i) for i in compacted],'requested_spawn':spawn,'initial_write_containing_call':record_proof(rt,initial_write),'all_write_containing_call_ordinals':write_calls,'root_followup_tasks':followups[task],'fixed_snapshot_capture_calls':snapshot_calls[r] if is_reader else [],'transport_events':diag,'responses_over6500_characters':large,'runtime_fork_context_field':None,'encrypted_initial_and_continuation_plaintext_equality':None})


# Discrepancies in original data stay separate from failed technical integrity checks.
literal_mismatches=[{'reader':r,'id':e['id'],'actual_literal_question':e.get('literal_question'),'expected_literal_question':q['question']} for r,raw in READERS.items() for e,q in zip(raw.value['answers'],Q) if e.get('literal_question')!=q['question']]
quote_diagnostics=[u for u in ROWS['reference_units'] if not u['quote_occurs_in_summary'] or not u['declared_summary_span_matches']]
# Verify every original data file read by this implementation stayed byte-identical.
for path,meta in list(FILES.items()):
    check(sha(Path(path).read_bytes())==meta['sha256'],'original_evidence_unchanged_during_audit',path)
for path,digest in PRESERVED_ARCHIVE_HASHES.items():
    check(sha(Path(path).read_bytes())==digest,'old04_and_initial05_audits_untouched',path)
SCRIPT_HASH=sha(Path(__file__).read_bytes())
report={
 'verification_script':{'path':str(Path(__file__).resolve()),'sha256':SCRIPT_HASH},
 'audit':'Independent technical bookkeeping audit 23; own technical continuation for completed iteration05',
 'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'iteration':str(IT),'technical_pass':not FAILURES,'technical_verdict':'PASS_BOOKKEEPING_WITH_CONFIRMED_INITIAL_A_TRANSPORT_FAILURE' if not FAILURES else 'FAIL_BOOKKEEPING','strict_complete_pre_first_save_input_delivery_pass':False,'initial_delivery_status':'A incomplete; B complete; later A reread is not retroactive initial delivery',
 'scope':'Bookkeeping, transport and runtime identity proof only. No gameplay regrading, source-authority approval, new source vote, global readiness or stamping approval.',
 'independence':'Continuation of this auditor’s own independent standard-library implementation; no parent materializer/verifier/aggregator code imported, executed or used as an oracle. Original reader JSON and nine original grades directly parsed. Parent technical validation summaries not used as proof. Separate neutral assessment inputs/findings excluded.',
 'derived_counts':{'question_count':N,'ordered_ids':IDS,'raw_key_records_per_reader':RAW_FACT_N,'raw_fact_assessments_verified':len(ROWS['fact_assessments']),'whole_original_entries_verified':len(ROWS['raw_entries']),'entry_wrapper_checks':COUNTS['complete_original_entry_all_fields'],'original_entry_raw_spans_verified':len(ROWS['raw_entries']),'referent_raw_span_attachments_verified':len(ROWS['reference_units']),'distinct_raw_entry_and_referent_spans_verified':len(ROWS['raw_entries'])+len({(u['reader'],u['pointer']) for u in ROWS['reference_units']}),'same_entry_reference_unit_attachments_verified':len(ROWS['reference_units']),'distinct_raw_reference_units_verified':len({(u['reader'],u['pointer']) for u in ROWS['reference_units']}),'originating_reference_paths_verified':COUNTS['reference_origin_pointer_resolves'],'snapshots_verified':len(ROWS['snapshots']),'literal_question_bindings_examined_across_snapshots':len(ROWS['literal_bindings']),'final_clause_literal_associations_examined':len(ROWS['clause_literal_bindings']),'final_clause_literal_association_mismatches':sum(not x['exact_current_question_substring'] for x in ROWS['clause_literal_bindings']),'separate_transport_only_archives_verified':1,'actual_identities_verified':len(ROWS['runtime_identities']),'actual_reader_contexts_verified':sum(len(x['actual_turns']) for x in ROWS['runtime_identities'] if 'reader_' in x['task']),'actual_reader_task_turns_verified':sum(len(x['actual_task_turns']) for x in ROWS['runtime_identities'] if 'reader_' in x['task']),'actual_grader_turns_verified':sum(len(x['actual_turns']) for x in ROWS['runtime_identities'] if 'grader_' in x['task']),'declared_input_file_receipts_examined':len(ROWS['runtime_deliveries']),'declared_input_chunks_examined':sum(x['declared_chunks'] for x in ROWS['runtime_deliveries']),'exact_input_chunks_matched_to_actual_runtime':sum(x['actually_matched_chunks'] for x in ROWS['runtime_deliveries']),'input_receipts_with_full_actual_payload_coverage':sum(x['actually_matched_chunks']==x['declared_chunks'] for x in ROWS['runtime_deliveries']),'unmatched_initial_A_declared_chunks':sum(x['declared_chunks']-x['actually_matched_chunks'] for x in CHRONOLOGY['a']['initial_files']),'actual_grader_input_files_verified':sum('grader_' in x['task'] for x in ROWS['runtime_deliveries']),'actual_grader_input_chunks_verified':sum(x['actually_matched_chunks'] for x in ROWS['runtime_deliveries'] if 'grader_' in x['task'])},
 'executed_assertions_total':sum(COUNTS.values()),'executed_assertions_by_category':dict(COUNTS),'failed_checks':FAILURES,
 'original_grade_totals_recomputed':totals,'original_grade_flags':flag_rows,
 'preserved_reader_data_diagnostics':{'literal_question_mismatches_final':literal_mismatches,'same_entry_quote_or_declared_source_span_mismatches':quote_diagnostics,'policy':'Observed original answer/question or quotation diagnostics are preserved and reported as data, not automatic gameplay grades or packaging failures.'},
 'limitations':[
  'Runtime task/continuation bodies are encrypted and plaintext is unavailable. No encrypted body is exposed, decrypted, or asserted equal to a saved prompt/constant. Actual same-identity turn ordering, requested root settings, saved constant schedule, and public input payloads are separately verified.',
  'fork_turns:none is independently observed in actual submitted root spawn arguments. External child runtime metadata does not expose a fork-context field; no independent runtime fresh-context field is claimed.',
  'Initial A delivery was incomplete, B was complete before first write in actual UTF8-byte blocks, and A later received 46 actual Unicode blocks after saving its first10. The later reread does not erase the original missing material RULE/QUESTION data or make those initial answers initially fully informed.',
  'Public delivered input availability and exact bytes/characters do not prove semantic comprehension or correctness. No gameplay judgments were changed and no confidence, schema, locator, process, source-wide or unasked-background caps were imposed.',
  'Questions/key compared in full to candidate16; old167/seed20 preservation was not separately recertified in this audit. This audit performs no new primary source reading.',
  'Root runtime is append-only and may continue growing; reported whole-file hash is the observed prefix at read time. Exact relevant record hashes including line LF are stable evidence.',
  'Original aggregate uses immutable report hashes and original resolving pointers rather than embedding every assessment field. Missing/contradiction flags remain losslessly reachable through those original pointers and are explicitly inventoried here.'
 ],
 'raw_span_convention':'Zero-based half-open Unicode codepoint and UTF-8 byte offsets independently parsed from original tokens. Normalized hashes use compact sorted-key ensure_ascii=false JSON. Every originating reference path is RFC6901 and resolves inside the same original answer entry.',
 'preserved_prior_audit_hashes':PRESERVED_ARCHIVE_HASHES,'data_files':FILES,'evidence':dict(ROWS),'initial_and_repair_chronology':CHRONOLOGY
}
# Avoid accidentally replacing an already completed audit without explicit invocation.
out=IT/'bookkeeping-audit-23.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'output':str(out),'technical_pass':report['technical_pass'],'checks':sum(COUNTS.values()),'failures':len(FAILURES),'counts':report['derived_counts'],'first_failures':FAILURES[:12]},ensure_ascii=False))
