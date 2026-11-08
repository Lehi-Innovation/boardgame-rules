"""Verify336 whole original answers, their exact references and1094 fact checks."""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime,timezone
import argparse,hashlib,json

B=Path(__file__).resolve().parent;ROOT=B.parents[4]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--iteration',required=True,type=int)
args=parser.parse_args()
assert args.iteration>=6
label=f'{args.iteration:02d}'
D=ROOT/'docs/quality/summary-qa/cosmic-encounter'/B.name/('expanded-iteration-'+label)
load=lambda p:json.loads(p.read_text())
HB=lambda b:hashlib.sha256(b).hexdigest()
H=lambda p:HB(p.read_bytes())
canonical=lambda v:HB(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
questions={x['id']:x for x in load(D/'questions.json')['questions']}
key={x['id']:x for x in load(D/'answer-key.json')['answers']}
scope={x['id']:x for x in load(D/'actual-question-scope.json')['questions']}
paths={w:D/f'reader-{w}.json' for w in 'ab'};docs={w:load(p) for w,p in paths.items()};data={w:p.read_bytes() for w,p in paths.items()}
raw={w:{x['id']:x for x in docs[w]['answers']} for w in 'ab'};body=(D/'summary-snapshot.md').read_text()
plan=load(D/'grading-inputs-v2/manifest.json');totals={w:Counter() for w in 'ab'};facts={w:0 for w in 'ab'};seen={w:[] for w in 'ab'};references_checked=[];reports=[];quote_diagnostics=[]
def pointer(v,path):
    for part in path.split('/')[1:]:
        part=part.replace('~1','/').replace('~0','~');v=v[int(part)] if isinstance(v,list) else v[part]
    return v
def references(v,path=''):
    found=defaultdict(list)
    if isinstance(v,dict):
        for name,child in v.items():
            escaped=name.replace('~','~0').replace('/','~1')
            if name in ('evidence','evidence_refs') and isinstance(child,list):
                for i,item in enumerate(child):
                    if isinstance(item,(str,int)):found[item].append(path+'/'+escaped+'/'+str(i))
            for ident,occurrences in references(child,path+'/'+escaped).items():found[ident].extend(occurrences)
    elif isinstance(v,list):
        for i,child in enumerate(v):
            for ident,occurrences in references(child,path+'/'+str(i)).items():found[ident].extend(occurrences)
    return found
for index,item in enumerate(plan['blocks'],1):
    pp=Path(item['path']);assert H(pp)==item['sha256'];pack=load(pp);ids=pack['expected_ids']
    assert pack['summary_sha256']==HB(body.encode()) and [e['id'] for e in pack['entries']]==ids
    old=load(D/'grading-inputs'/f'block-{index:02d}.json');old_by_id={e['id']:e for e in old['entries']};by_id={e['id']:e for e in pack['entries']}
    for i,e in by_id.items():
        assert e['literal_question']==questions[i] and e['key']==key[i] and e['validated_actual_scope']==scope[i]
        assert len(e['raw_key_fact_refs'])==len(key[i]['required_facts'])
        for w in 'ab':
            m=e['readers'][w];assert m['complete_original_entry']==raw[w][i]
            assert all(m[k]==v for k,v in old_by_id[i]['readers'][w].items())
            assert m['raw_file_sha256']==H(paths[w])
            fragment=data[w][m['start_byte']:m['end_byte']]
            assert HB(fragment)==m['raw_entry_sha256'] and json.loads(fragment)==raw[w][i] and m['normalized_entry_sha256']==canonical(raw[w][i])
            link=m['explicitly_referenced_shared_evidence'];assert link['raw_reader_sha256']==H(paths[w])
            assert link['pool_field']=='/evidence_units' and link['complete_pool_normalized_sha256']==canonical(docs[w]['evidence_units'])
            original_refs=references(raw[w][i]);expected=defaultdict(list)
            for ref,occurrences in original_refs.items():expected[str(ref)].extend(occurrences)
            resolved={x['reference']:x for x in link['resolved_units']};assert len(resolved)==len(link['resolved_units']) and set(resolved)==set(expected),(w,i,list(raw[w][i]),sorted(resolved),sorted(expected))
            for ref,pf in resolved.items():
                u=pf['original_unit'];assert pf['original_unit_sha256']==canonical(u)
                assert sorted(pf['explicit_reference_paths_in_original_entry'])==sorted(expected[ref])
                assert all(str(pointer(raw[w][i],p))==ref for p in expected[ref])
                assert all(pointer(raw[w][i],p) in original_refs for p in expected[ref])
                sp=pf['original_raw_unit_span'];fragment=data[w][sp['start_byte']:sp['end_byte']]
                assert HB(fragment)==sp['raw_sha256'] and json.loads(fragment)==u and pointer(docs[w],sp['json_pointer'])==u and sp['normalized_sha256']==canonical(u)
                if isinstance(docs[w]['evidence_units'],dict): assert docs[w]['evidence_units'][str(ref)]==u
                else: assert str(u['number'])==ref
                source=u.get('source_span',u);a,z=source.get('start',source.get('source_start')),source.get('end',source.get('source_end'))
                assert isinstance(a,int) and isinstance(z,int)
                if body[a:z]!=u['text']:quote_diagnostics.append({'reader':w,'id':i,'reference':ref,'reader_quote_mismatch_preserved':True})
            references_checked.append({'reader':w,'id':i,'unique_original_references':len(resolved),'explicit_occurrences':sum(map(len,expected.values())),'all_and_only_same_entry_references':True})
    rp=D/f'grades-{index:02d}.json';report=load(rp)
    for w in 'ab':
        entries=report['readers'][w]['entries'];assert [x['id'] for x in entries]==ids
        local=Counter()
        for x in entries:
            i=x['id'];assert x['observed_raw_entry_hash']==by_id[i]['readers'][w]['raw_entry_sha256']
            ids_seen=[a.get('key_fact_id',a.get('id',a.get('fact_id'))) for a in x['fact_checks']]
            assert ids_seen==[a['id'] for a in by_id[i]['raw_key_fact_refs']]
            states=[a.get('classification',a.get('asked_portion_status',a.get('status'))) for a in x['fact_checks']]
            if x['material_contradictions'] or 'contradicted' in states:assert x['grade']=='incorrect'
            if x['grade']=='correct':assert not x['missing_asked_facts'] and 'missing' not in states
            assert x['grade'] in ['correct','partial','incorrect'];totals[w][x['grade']]+=1;local[x['grade']]+=1;facts[w]+=len(ids_seen);seen[w].append(i)
        declared=report['readers'][w]['totals'];assert all(local[k]==declared.get(k,0) for k in ['correct','partial','incorrect'])
    reports.append({'report':str(rp),'sha256':H(rp),'complete_packet':str(pp),'packet_sha256':H(pp),'ids':ids})
assert len(reports)==9 and all(seen[w]==list(questions) and facts[w]==547 for w in 'ab')
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'N':len(questions),'complete_original_entries':len(references_checked),'raw_key_fact_assessments':facts,'primary_scores':{w:{s:totals[w][s] for s in ['correct','partial','incorrect']} for w in 'ab'},'reports':reports,'same_entry_reference_checks':references_checked,'quote_mismatch_diagnostics':quote_diagnostics,'pool_counts':{w:len(docs[w]['evidence_units']) for w in 'ab'},'raw_file_sha256':{w:H(p) for w,p in paths.items()},'limits':['Original numeric raw references retain their type; string-keyed JSON pool lookup is normalized only for exact correspondence, with every raw pointer/value rechecked.','Fixed original questions/key/scope; no unasked background penalty, cross-answer reference borrowing or transport cap.','This is primary grade and original reference integrity, not a new semantic adjudication vote.','Any genuine whole-entry borderline case may receive ONE neutral; retained primary grades remain immutable.','All168 current asks include the attributed later setup instruction. No full-core/stamp/publication approval.']}
out=B/'coordinator-checks'/('cosmic-expanded'+label+'-primary-and-reference-integrity.json');assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'entries':len(references_checked),'facts':facts,'primary':proof['primary_scores'],'pools':proof['pool_counts'],'quote_diagnostics':len(quote_diagnostics),'proof':str(out)}))
