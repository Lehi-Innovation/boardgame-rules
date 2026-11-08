"""Bind ONE neutral21 to four whole original entries and actual complete inputs."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import hashlib,json,re
B=Path(__file__).resolve().parent;ROOT=B.parents[4]
D=ROOT/'docs/quality/summary-qa/cosmic-encounter'/B.name/'expanded-iteration-04'
J=lambda p:json.loads(p.read_text());H=lambda b:hashlib.sha256(b).hexdigest()
packet_path=D/'neutral21-case-input.json';packet=J(packet_path)
rp=D/'neutral21-adjudication.json';report=J(rp);delivery=J(D/'neutral21-delivery.json')
assert H(packet_path.read_bytes())==report['selected_case_input_sha256']
body=(D/'summary-snapshot.md').read_text();assert H((D/'summary-snapshot.md').read_bytes())==report['frozen_guide_sha256']
case_map={}
for index,case in enumerate(packet['cases']):
    origin=Path(case['origin_block_path']);assert H(origin.read_bytes())==case['origin_block_sha256']
    e=next(x for x in J(origin)['entries'] if x['id']==case['case']['id'])
    assert all(e[k]==v for k,v in case['case'].items())
    assert case['complete_original_reader_entries_and_explicit_referents']==e['readers']
    case_map[e['id']]=(index,e)
assert set(case_map)=={'Q094','Q136'}
actor='01a1b61c-b305-75b1-a68a-a5156dc41836'
runtime=next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/07').glob('*'+actor+'.jsonl'))
def strings(v,depth=0):
    if depth>9:return
    if isinstance(v,str):
        yield v
        try:child=json.loads(v)
        except (ValueError,TypeError):return
        if child!=v:yield from strings(child,depth+1)
    elif isinstance(v,dict):
        if v.get('type') in ('input_image','image'):return
        for child in v.values():yield from strings(child,depth+1)
    elif isinstance(v,list):
        for child in v:yield from strings(child,depth+1)
outputs=[];ends=[];contexts=[]
for n,line in enumerate(runtime.open(),1):
    row=json.loads(line);p=row.get('payload',{})
    if row.get('type')=='turn_context':contexts.append((p.get('model'),p.get('effort')))
    if row.get('type')=='event_msg' and p.get('type')=='task_complete':ends.append(n)
    if row.get('type')=='event_msg' and p.get('type')=='item_completed':
        item=p.get('item',{})
        if item.get('type')=='CommandExecution':outputs.append((n,H(line.encode()),list(strings(item.get('aggregated_output','')))))
assert ends and contexts and all(c==('gpt-6.1-sol','high') for c in contexts)
reads=[]
for f in delivery['text_input_proofs']:
    p=Path(f['path']);t=p.read_text();assert H(p.read_bytes())==f['full_file_sha256'] and len(t)==f['unicode_character_count'] and f['contiguous_complete_coverage'];cursor=0
    for c in f['chunks']:
        a,z=c['start_char'],c['end_char_exclusive'];assert a==cursor and a<z<=len(t) and H(t[a:z].encode())==c['utf8_chunk_sha256']
        matched=[{'record':n,'record_sha256':h} for n,h,vals in outputs if n<max(ends) and any(t[a:z] in value for value in vals)]
        assert matched,(str(p),a,z)
        reads.append({'path':str(p),'start':a,'end':z,'sha256':c['utf8_chunk_sha256'],'actual_outputs':matched});cursor=z
    assert cursor==len(t)
assert {f['path'] for f in delivery['text_input_proofs']}=={str(D/'summary-snapshot.md'),str(packet_path),str(D/'neutral21-instructions.txt')}
def pointer(v,path):
    for bit in path.split('/')[1:]:
        bit=bit.replace('~1','/').replace('~0','~');v=v[int(bit)] if isinstance(v,list) else v[bit]
    return v
def atoms(v):
    result=set()
    if isinstance(v,dict):
        for key,child in v.items():
            if isinstance(child,str) and re.fullmatch(r'Q\d+\.RF\d+\.A\d+',child):result.add(child)
            if isinstance(child,(list,dict)):result.update(atoms(child))
    elif isinstance(v,list):
        for child in v:result.update(atoms(child))
    return result
refs=[]
def quotes(v,index,who):
    if isinstance(v,dict):
        if 'input_json_pointer' in v and 'quote' in v:
            path=v['input_json_pointer'];assert path.startswith('/cases/'+str(index)+'/complete_original_reader_entries_and_explicit_referents/'+who+'/')
            assert v['quote'] in pointer(packet,path);refs.append({'reader':who,'path':path,'quote':v['quote']})
        if all(k in v for k in ['guide_path','start_char','end_char_exclusive','quote']):
            assert Path(v['guide_path'])==D/'summary-snapshot.md' and body[v['start_char']:v['end_char_exclusive']]==v['quote']
        for child in v.values():quotes(child,index,who)
    elif isinstance(v,list):
        for child in v:quotes(child,index,who)
totals={'a':Counter(correct=163,partial=5,incorrect=0),'b':Counter(correct=166,partial=2,incorrect=0)};seen=set();assessment_counts=[]
for a in report['assessments']:
    ident,who=a['question_id'],a['reader_label'];index,e=case_map[ident];m=e['readers'][who]
    assert (who,ident) not in seen;seen.add((who,ident))
    assert a['original_raw_entry_sha256']==m['raw_entry_sha256'] and a['original_normalized_entry_sha256']==m['normalized_entry_sha256']
    assert a['original_raw_file_sha256_as_supplied']==m['raw_file_sha256'] and a['literal_question']==e['literal_question']['question']
    covered={i for row in a['actual_scope_assessment'] for i in row['asked_atom_ids']};assert covered==atoms(e['validated_actual_scope'])
    for item in a['same_entry_explicit_referent_audit']:
        original=next(x for x in m['explicitly_referenced_shared_evidence']['resolved_units'] if str(x['reference'])==str(item['reference']))
        assert sorted(item['explicit_reference_paths_in_original_entry'])==sorted(original['explicit_reference_paths_in_original_entry'])
    quotes(a,index,who)
    old='partial' if ident=='Q094' or who=='b' else 'correct'
    totals[who][old]-=1;totals[who][a['grade']]+=1
    assessment_counts.append({'reader':who,'id':ident,'asked_atoms':len(covered),'grade':a['grade']})
assert seen=={(w,i) for w in 'ab' for i in ['Q094','Q136']}
scores={w:{k:c[k] for k in ['correct','partial','incorrect']} for w,c in totals.items()}
assert scores=={'a':{'correct':164,'partial':4,'incorrect':0},'b':{'correct':167,'partial':1,'incorrect':0}}
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'actor':actor,'runtime_path':str(runtime),'runtime_sha256':H(runtime.read_bytes()),'report_path':str(rp),'report_sha256':H(rp.read_bytes()),'input_sha256':H(packet_path.read_bytes()),'actual_complete_input_reads':reads,'all4_whole_original_entries_and_only_same_entry_explicit_referents_exact':True,'asked_atom_assessments':assessment_counts,'literal_same_entry_citations':refs,'semantic_acceptance':{'Q094_both':'Correct: in context of the literal future-promise question, unenforceability allows making promises while denying enforceable future obligations. Whole operative deal quotation and answers do not prohibit them. No demand for duplicate permission wording.','Q136_a':'Correct: Super-enabled ally role is supplied by the literal case, so answer need not independently prove its existence. Direct applicable win/eradication outcome and all exceptions supplied.','Q136_b':'Partial: expressly leaves actual supplied ally outcome unresolved, absent from entire entry/referents. Support label itself is not a cap.','Q064_to_Q067_a':'Four wrong-alien entries remain Partial: explicit correct different-alien statements are not reassigned to the requested actor to invent contradictions, and cannot supply that actor’s missing outcomes.'},'primary_scores_preserved':{'a':[163,5,0],'b':[166,2,0]},'one_neutral_effective_scores':scores,'pair_verdict':'FAIL','limits':['Exactly ONE fresh neutral for this borderline set; all nine primary reports preserved.','No cross-answer or unreferenced-pool borrowing, unasked permissions/name/rephrasing gate, or transport cap.','Current whole168 repair/new pair and essential FAQ authority gap remain separate.']}
out=B/'coordinator-checks/cosmic-expanded04-one-neutral-acceptance.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'cases':4,'complete_input_ranges':len(reads),'same_entry_exact_citations':len(refs),'effective':scores,'proof':str(out)}))
