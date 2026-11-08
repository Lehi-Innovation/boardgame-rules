"""Bind heterogeneous current04 grading citations to only the same raw entry."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,re,hashlib
B=Path(__file__).resolve().parent
D=B.parents[4]/'docs/quality/summary-qa/new-angeles'/B.name/'expanded-luna-iteration-04'
J=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
scope={x['id']:x for x in J(D.parent/'expanded-candidate-v11/asked-clause-map.json')}
refs=[];vectors=0;diagnostics=[];styles=Counter()
def pointer(v,path):
    for bit in path.split('/')[1:]:
        bit=bit.replace('~1','/').replace('~0','~');v=v[int(bit)] if isinstance(v,list) else v[bit]
    return v
def dot(v,path):
    path=path.removeprefix('$.').removeprefix('$').lstrip('.')
    binding=re.match(r'[A-Za-z_]\w*(?:(?:\.[A-Za-z_]\w*)|\[\d+\])*',path)
    assert binding
    suffix=path[binding.end():]
    assert not suffix or suffix.startswith(',') or suffix.startswith(' ('),path
    path=binding[0]
    for field,index in re.findall(r'([^\.\[\]]+)|\[(\d+)\]',path):v=v[field] if field else v[int(index)]
    return v
def walk(value,pack,entry,who,ident):
    if isinstance(value,dict):
        quote=value.get('quote',value.get('text'))
        if isinstance(quote,str) and any(isinstance(value.get(k),str) for k in ['entry_json_pointer','location','path']):
            path=value.get('entry_json_pointer',value.get('location',value.get('path')))
            if 'entry_json_pointer' in value:
                text=pointer(entry,path);style='relative_json_pointer'
            elif path.startswith('/complete_raw_reader_entries/'):
                parts=path.split('/');assert parts[2]==who
                assert pack['complete_raw_reader_entries'][who][int(parts[3])]['id']==ident
                text=pointer(pack,path);style='full_pack_json_pointer'
            elif path.startswith('complete_raw_reader_entries.'):
                match=re.fullmatch(r'complete_raw_reader_entries\.([ab])\[(id=Q\d+|\d+)\]\.(.*)',path)
                assert match and match[1]==who
                if match[2].startswith('id='):assert match[2][3:]==ident
                else:assert pack['complete_raw_reader_entries'][who][int(match[2])]['id']==ident
                text=dot(entry,match[3]);style='full_pack_dot_path'
            else:
                text=dot(entry,path);style='relative_dot_path'
            assert isinstance(text,str) and quote in text,(who,ident,path)
            if 'field_unicode_range' in value:
                a,z=value['field_unicode_range'];assert text[a:z]==quote
            refs.append({'reader':who,'id':ident,'path':path,'quote':quote});styles[style]+=1
        for child in value.values():walk(child,pack,entry,who,ident)
    elif isinstance(value,list):
        for child in value:walk(child,pack,entry,who,ident)
for task in J(D/'grading/input-manifest.json')['blocks']:
    pack=J(Path(task['pack']));report=J(Path(task['output']))
    raw={w:{x['id']:x for x in pack['complete_raw_reader_entries'][w]} for w in 'ab'}
    for rec in report.get('records',report.get('grades')):
        who,ident=rec['reader'],rec['id'];assessments=rec['asked_fact_assessments']
        actual=[x['asked_fact'] for x in assessments]
        if actual!=scope[ident]['asked_facts']:diagnostics.append({'reader':who,'id':ident,'fixed':scope[ident]['asked_facts'],'actual':actual})
        assert rec['label']=='Correct' and not rec['material_wrong_claims'] and not rec['genuine_omissions']
        assert all(x['assessment'].lower() in ['satisfied','correct'] for x in assessments)
        walk(rec,pack,raw[who][ident],who,ident);vectors+=len(assessments)
assert vectors==544 and refs and not diagnostics
counts=Counter((x['reader'],x['id']) for x in refs)
assert len(counts)==188
proof={'verified':True,'checked_at_utc':datetime.now(timezone.utc).isoformat(),'complete_entries_with_exact_support_citations':len(counts),'exact_same_entry_citations':refs,'citation_schema_counts':dict(styles),'all544_asked_fact_texts_exact_fixed_map_order':True,'all544_fact_assessments_positive':True,'all188_original_correct_labels_without_omissions_or_wrong_claims':True,'raw_hashes':{w:H(D/('reader-'+w+'.json')) for w in 'ab'},'scope_annotation':'Q30 phase remains an actual literal asked procedure, not a phantom given. Predeclared annotation preserved.','limits':['Extends the earlier current04 primary integrity proof, whose old citation-schema parser matched zero current04 citation forms. That zero was a parser limitation, not missing evidence.','No cross-answer or other-reader borrowing; every actual path resolves within the same full original entry, and every supplied exact field range is checked.','No complete-core, SG01 resolution, stamp or publication approval.']}
out=B/'coordinator-checks/new-angeles-expanded04-exact-same-entry-citation-binding.json';assert not out.exists();out.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'verified':True,'entries':len(counts),'fixed_vectors':vectors,'exact_citations':len(refs),'styles':dict(styles),'proof':str(out)}))
