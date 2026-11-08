"""Bind the one Q117 neutral to the unchanged whole entry and actual reads."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json

B=Path(__file__).resolve().parent;R=B.parents[4]
D=R/'docs/quality/summary-qa/cosmic-encounter'/B.name/'expanded-iteration-03'
load=lambda p:json.loads(p.read_text());H=lambda b:hashlib.sha256(b).hexdigest()
packet_path=D/'neutral19-case-input.json';packet=load(packet_path);rp=D/'neutral19-adjudication.json';report=load(rp);delivery=load(D/'neutral19-delivery.json')
assert report['case_id']=='Q117' and report['grade']=='correct' and not report['material_contradictions'] and not report['unresolved_asked_material_facts']
origin=Path(packet['origin_block_path']);assert H(origin.read_bytes())==packet['origin_block_sha256']
e=next(x for x in load(origin)['entries'] if x['id']=='Q117')
for k in ['id','literal_question','key','validated_actual_scope']:assert packet['case'][k]==e[k]
assert packet['complete_original_reader_entry_and_explicit_referents']==e['readers']['a']
assert len(e['readers']['a']['explicitly_referenced_shared_evidence']['resolved_units'])==1
assert [x['raw_key_fact_ref_id'] for x in report['clause_and_raw_fact_coverage']]==[x['id'] for x in e['raw_key_fact_refs']]
actor='01a1b596-77f5-7b40-8182-c009010fb680';runtime=next(Path('/mnt/c/Users/jonny/.codex/sessions/2026/11/07').glob('*'+actor+'.jsonl'))
def strings(v,depth=0):
    if depth>8:return
    if isinstance(v,str):
        yield v
        try:c=json.loads(v)
        except (ValueError,TypeError):return
        if c!=v:yield from strings(c,depth+1)
    elif isinstance(v,dict):
        if v.get('type') in ('input_image','image'):return
        for x in v.values():yield from strings(x,depth+1)
    elif isinstance(v,list):
        for x in v:yield from strings(x,depth+1)
outputs=[];ends=[];contexts=[]
for n,line in enumerate(runtime.open(),1):
    d=json.loads(line);v=d.get('payload',{})
    if d.get('type')=='turn_context':contexts.append((v.get('model'),v.get('effort')))
    elif d.get('type')=='event_msg' and v.get('type')=='task_complete':ends.append(n)
    elif d.get('type')=='event_msg' and v.get('type')=='item_completed':
        it=v.get('item',{})
        if it.get('type')=='CommandExecution':outputs.append((n,H(line.encode()),list(strings(it.get('aggregated_output','')))))
assert ends and contexts and all(c==('gpt-6.1-sol','high') for c in contexts)
reads=[]
for f in delivery['inputs']:
    p=Path(f['path']);t=p.read_text();assert H(p.read_bytes())==f['sha256'] and len(t)==f['unicode_characters'] and f['read_end_to_end'];cursor=0
    for c in f['chunks']:
        a,z=c['start_char'],c['end_char'];assert a==cursor and a<z<=len(t) and H(t[a:z].encode())==c['utf8_sha256']
        m=[{'ordinal':n,'raw_record_sha256':h} for n,h,vals in outputs if n<max(ends) and any(t[a:z] in val for val in vals)]
        assert m,(str(p),a,z);reads.append({'path':str(p),'start':a,'end':z,'slice_sha256':c['utf8_sha256'],'actual_public_outputs':m});cursor=z
    assert cursor==len(t)
assert {Path(f['path']).resolve() for f in delivery['inputs']}=={(D/'summary-snapshot.md').resolve(),packet_path.resolve()}
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'actor':actor,'runtime_path':str(runtime),'runtime_sha256':H(runtime.read_bytes()),'report_path':str(rp),'report_sha256':H(rp.read_bytes()),'input_sha256':H(packet_path.read_bytes()),'four_raw_fact_vectors_bound':True,'complete_original_entry_and_only_explicit_E35_preserved':True,'actual_complete_input_reads':reads,'semantic_acceptance':'The imprecise that-arrival sentence is reasonably the actual-loss-and-Healer-return sequence in the literal question and whole entry, disambiguated by its own operative E35 reference. It does not expressly create an independent warp-entry Remora trigger or earlier timing window. This is contextual interpretation, not erasing a definite false claim with a correct quote. All four actual requested outcomes are supplied.','primary_scores_preserved':{'a':[166,0,1],'b':[165,1,1]},'one_neutral_effective_scores':{'a':[167,0,0],'b':[165,1,1]},'pair_verdict':'FAIL','limits':['Exactly one fresh neutral for this one borderline entry. No other label changed.','Wrong-question BQ115 and false CosmicZap mechanism BQ146 retained; no cross-answer borrowing or extra paraphrase/name requirement.','No new-source/applicability or publication approval.']}
out=B/'coordinator-checks/cosmic-expanded03-one-neutral-acceptance.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'whole_input_slices':len(reads),'effective':proof['one_neutral_effective_scores'],'verdict':'FAIL','proof':str(out)}))
