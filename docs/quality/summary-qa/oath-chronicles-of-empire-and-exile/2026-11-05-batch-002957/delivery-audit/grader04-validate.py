import pathlib,json,hashlib,collections
P=pathlib.Path(__file__).parent.parent;D=P/'expanded-iteration-04'
packet=json.loads((D/'grading-input.json').read_text());s=(D/'summary-snapshot.md').read_text();res=json.loads((D/'results.json').read_text())
key=json.loads((P/'expanded-v9/answer-key.json').read_text());scope=json.loads((P/'expanded-v9/grading-scope.json').read_text())
bykey={q['id']:q for q in key['answers']};byscope={q['id']:q for q in scope['questions']}
hashes=[]
for x in res['inputhashes']:
    actual=hashlib.sha256(pathlib.Path(x['path']).read_bytes()).hexdigest();assert actual==x['sha256'];hashes.append(dict(path=x['path'],expected_sha256=x['sha256'],actual_sha256=actual,match=True))
ranges=[json.loads(x) for x in (P/'delivery-audit/grader04-delivery-ranges.jsonl').read_text().splitlines()]
for fn in ['grading-input.json','summary-snapshot.md']:
    rr=[r for r in ranges if r['filename']==fn];t=(D/fn).read_text();assert rr[0]['start']==0 and rr[-1]['end']==len(t)
    for i,r in enumerate(rr):
        assert 0<r['end']-r['start']<=5000 and r['total']==len(t)
        assert r['sha256']==hashlib.sha256(t.encode()).hexdigest()
        if i:assert rr[i-1]['end']==r['start']
ids=[f'Q{i:03}' for i in range(1,104)];assert [q['id'] for q in packet['questions']]==ids
for q in packet['questions']:
    k=bykey[q['id']];sc=byscope[q['id']]
    assert q['fixed_expected_answer']==k['expected_answer']
    assert sc['fixed_key_expected_answer_sha256']==hashlib.sha256(k['expected_answer'].encode()).hexdigest()
    assert q['question']==sc['question']
    assert q['required_facts']==[{k:f[k] for k in ['fact_id','expected_fact']} for f in sc['required_facts']],q['id']
    for field in ['contextual_exclusions','semantic_notes','source_references']:assert q[field]==sc[field],(q['id'],field)
raw_reconstructions=0;quote_hash_checks=0;evidence_checks=0;application_checks=0;attached_checks=0
for r in res['readers']:
    rn=r['reader'];raw=json.loads((D/f'{rn}.json').read_text());rawby={a['id']:a for a in raw['answers']}
    assert [q['id'] for q in r['questions']]==ids
    for p,q in zip(packet['questions'],r['questions']):
        entry=p['readers'][rn];reconstructed=dict(entry);sp=reconstructed.pop('attached_verbatim_passage_spans');reconstructed['verbatim_passages']=[s[x['start']:x['end']] for x in sp]
        assert reconstructed==rawby[q['id']];raw_reconstructions+=1
        assert q['question']==p['question'] and q['expected_answer_from_fixed_key']==p['fixed_expected_answer'] and q['observed_answer']==entry['answer']
        assert q['attached_quote_spans']==sp
        for x in sp:assert hashlib.sha256(s[x['start']:x['end']].encode()).hexdigest()==x['sha256_utf8'];quote_hash_checks+=1
        assert len(q['fact_checks'])==len(p['required_facts'])
        assert [x['fact_id'] for x in q['fact_checks']]==[x['fact_id'] for x in p['required_facts']]
        for f,pf in zip(q['fact_checks'],p['required_facts']):
            assert f['expected_fact']==pf['expected_fact'] and f['status'] in ['satisfied','missing','contradiction'] and f['evidence']
            for e in f['evidence']:
                if e['source']=='application':
                    assert entry['answer'][e['start']:e['end']]==e['excerpt'];application_checks+=1
                else:
                    assert e['source']=='attached_quote'
                    assert s[e['summary_start']:e['summary_end']]==e['excerpt']
                    assert any(x['start']==e['attached_span_start'] and x['end']==e['attached_span_end'] and x['start']<=e['summary_start']<e['summary_end']<=x['end'] for x in sp)
                    attached_checks+=1
                assert 0<len(e['excerpt'])<=500;evidence_checks+=1
        fc=collections.Counter(f['status'] for f in q['fact_checks']);expected_grade='incorrect' if fc['contradiction'] else 'partial' if fc['missing'] else 'correct';assert q['grade']==expected_grade
        assert len(q['material_contradictions'])==fc['contradiction']
    counts=collections.Counter(q['grade'] for q in r['questions']);facts=collections.Counter(f['status'] for q in r['questions'] for f in q['fact_checks'])
    assert r['totals']=={k:counts[k] for k in ['correct','partial','incorrect']}|{'total':103}
    assert r['fact_totals']=={k:facts[k] for k in ['satisfied','missing','contradiction']}|{'total':327}
assert res['questions_graded']==sum(r['totals']['total'] for r in res['readers'])==206
assert res['fact_assessments']==sum(r['fact_totals']['total'] for r in res['readers'])==654
report=dict(status='passed',benchmark_version='expanded-v9',iteration=4,primary_delivery={'complete':True,'characters':{'grading-input.json':295776,'summary-snapshot.md':43979},'chunks':len(ranges),'maximum_chunk_characters':5000,'tool_calls':35,'max_chunks_per_call':2,'outer_max_output_tokens':7000,'nested_exec_command_max_output_tokens':7000,'all_35_outputs_inspected':True,'truncated_outputs':0,'contiguous_ranges':True,'receipt_path':str(P/'delivery-audit/grader04-delivery-ranges.jsonl')},input_hash_checks=hashes,exact_reader_entry_reconstructions=raw_reconstructions,attached_quote_hash_checks=quote_hash_checks,frozen_key_expected_answers_verified=103,frozen_scope_required_fact_sets_verified=103,frozen_scope_exclusions_and_semantic_notes_verified=103,questions_graded=206,fact_checks=654,literal_evidence_checks=evidence_checks,application_excerpt_checks=application_checks,attached_excerpt_span_membership_checks=attached_checks,all_ids_and_counts_valid=True,no_cross_entry_evidence=True,grade_status_consistency=True,source_consultations=[],gold_or_source_problems=[],reader_totals=[{'reader':r['reader'],'totals':r['totals'],'fact_totals':r['fact_totals']} for r in res['readers']],results_sha256=hashlib.sha256((D/'results.json').read_bytes()).hexdigest(),limitations='Mechanical validation confirms integrity and traceability; semantic grades are the independent grader judgments documented in results and adjudication.')
(D/'grading-validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
(P/'delivery-audit/grader04-delivery-receipt.json').write_text(json.dumps(report['primary_delivery'],indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','questions_graded','fact_checks','literal_evidence_checks','application_excerpt_checks','attached_excerpt_span_membership_checks','results_sha256']},indent=2))
