"""Verify new neutral case/quote bindings; never assign or alter factual grades."""
from pathlib import Path
from collections import Counter
import hashlib,json
R=Path(__file__).parent.resolve();IT=R/'expanded-iteration-06'
def read(p):return json.loads(p.read_bytes())
def sha(raw):return hashlib.sha256(raw).hexdigest()
def objsha(x):return sha(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
def ptr(x,p):
    for key in p.split('/')[1:]:
        key=key.replace('~1','/').replace('~0','~')
        x=x[int(key)] if isinstance(x,list) else x[key]
    return x
checks=[];quotes=[]
def check(name,value):checks.append({'check':name,'pass':bool(value)})
packet=read(IT/'neutral28-case-input.json');audit=read(IT/'neutral28-adjudication.json');ledger=read(IT/'neutral28-case-selection-and-source-bindings.json');guide=(IT/'summary-snapshot.md').read_text();deliver=read(IT/'neutral28-runtime-delivery-validation.json')
check('actual complete three-file delivery/model',deliver['pass'])
check('guide exact hash',audit['frozen_guide']['sha256']==sha((IT/'summary-snapshot.md').read_bytes()))
check('input exact hash',audit['assigned_input']['sha256']==sha((IT/'neutral28-case-input.json').read_bytes())==ledger['case_input_sha256'])
check('all cases once in original order',[x['case_id'] for x in audit['assessments']]==[x['case_id'] for x in packet['cases']])
for index,(case,result,binding) in enumerate(zip(packet['cases'],audit['assessments'],ledger['whole_case_bindings'])):
    name=case['case_id'];source=read(Path(binding['source_bundle_path']));entry=next(x for x in source['entries'] if x['id']==case['id']);label=case['reader_label'];wrapper=case['original_reader_entry'];raw=Path(wrapper['raw_file_path']).read_bytes()
    check(name+' source bundle hash',sha(Path(binding['source_bundle_path']).read_bytes())==binding['source_bundle_sha256'])
    for field in ('literal_question','key','validated_actual_scope','raw_key_fact_refs'):
        check(name+' exact '+field,objsha(case[field])==objsha(entry[field]))
    check(name+' exact complete raw wrapper/referents',objsha(wrapper)==objsha(entry['readers'][label]))
    check(name+' current frozen raw hash',sha(raw)==wrapper['raw_file_sha256'])
    check(name+' exact raw byte span',sha(raw[wrapper['start_byte']:wrapper['end_byte']])==wrapper['raw_entry_sha256'])
    check(name+' raw parsed entry',objsha(json.loads(raw[wrapper['start_byte']:wrapper['end_byte']]))==objsha(wrapper['complete_original_entry'])==wrapper['normalized_entry_sha256'])
    check(name+' response identity',result['reader_label']==label and result['id']==case['id'])
    check(name+' response raw hashes',result['original_raw_entry_sha256']==wrapper['raw_entry_sha256'] and result['original_normalized_entry_sha256']==wrapper['normalized_entry_sha256'])
    check(name+' reported provenance',all(result['original_raw_entry_provenance'][k]==wrapper[k] for k in result['original_raw_entry_provenance']))
    check(name+' reported Q/key hashes',result['question_entry_sha256']==case['question_entry_sha256'] and result['key_entry_sha256']==case['key_entry_sha256'])
    check(name+' whole entry field list',set(result['complete_entry_fields_reviewed'])==set(wrapper['complete_original_entry']))
    check(name+' valid factual label',result['grade'] in ('correct','partial','incorrect'))
    facts=result['fact_by_fact_actual_scope_assessment'];scope=case['validated_actual_scope']
    check(name+' all actual-scope fact IDs once',Counter(x['fact_id'] for x in facts)==Counter(x['fact_id'] for x in scope['fact_classifications']))
    check(name+' all asked atom IDs once',Counter(a for x in facts for a in x['asked_atom_ids'])==Counter(x['atom_id'] for x in scope['required_atoms']))
    units=wrapper['explicitly_referenced_shared_evidence']['resolved_units'];refs=result['explicit_referents_reviewed']
    check(name+' all exact explicit referents reported',Counter(x['reference'] for x in refs)==Counter(x['reference'] for x in units))
    for ref in refs:
        unit=next(x for x in units if x['reference']==ref['reference']);span=unit['original_raw_unit_span']
        check(name+' exact referent metadata '+str(ref['reference']),ref['original_pool_json_pointer']==span['json_pointer'] and ref['original_raw_unit_sha256']==span['raw_sha256'] and ref['original_unit_sha256']==unit['original_unit_sha256'] and objsha(ref['all_explicit_reference_paths'])==objsha(unit['explicit_reference_paths_in_original_entry']) and set(ref['original_unit_fields_reviewed'])==set(unit['original_unit']))
        check(name+' referent pointer is own complete unit',ref['input_json_pointer'].startswith(f'/cases/{index}/original_reader_entry/explicitly_referenced_shared_evidence/') and objsha(ptr(packet,ref['input_json_pointer']))==objsha(unit['original_unit']))
    for fact in facts:
        for field,expected in [('answer_evidence','complete_original_entry/'),('explicit_same_entry_referent_evidence','explicitly_referenced_shared_evidence/')]:
            for evidence in fact[field]:
                pointer=evidence['json_pointer'];quote=evidence['quote'];value=ptr(packet,pointer)
                valid=pointer.startswith(f'/cases/{index}/original_reader_entry/'+expected) and isinstance(value,str) and quote in value
                check(name+' exact own-field quotation '+pointer,valid);quotes.append({'case_id':name,'kind':field,'json_pointer':pointer,'quote_sha256':sha(quote.encode()),'pass':valid})
        for locator in fact['guide_locators']:
            first,last=locator['start_char'],locator['end_char_exclusive'];quote=locator['quote'];valid=locator['path']==str(IT/'summary-snapshot.md') and guide[first:last]==quote and locator['start_line']==guide[:first].count('\n')+1
            check(name+' exact guide quotation '+str(first),valid);quotes.append({'case_id':name,'kind':'guide','start':first,'end':last,'quote_sha256':sha(quote.encode()),'pass':valid})
for report in read(IT/'original-grades-aggregate.json')['original_reports']:
    check('original primary report unchanged '+str(report['block']),sha(Path(report['path']).read_bytes())==report['sha256'])
report={'pass':all(x['pass'] for x in checks),'checks':checks,'check_count':len(checks),'whole_original_cases':len(packet['cases']),'exact_quote_count':len(quotes),'quotes':quotes,'input_sha256':sha((IT/'neutral28-case-input.json').read_bytes()),'assessment_sha256':sha((IT/'neutral28-adjudication.json').read_bytes()),'actual_delivery_sha256':sha((IT/'neutral28-runtime-delivery-validation.json').read_bytes()),'factual_regrading_or_cap':False,'primary_reports_unchanged':True}
out=IT/'neutral28-case-integrity-validation.json';assert not out.exists();out.write_text(json.dumps(report,indent=2)+'\n')
print({'pass':report['pass'],'checks':len(checks),'whole_cases':len(packet['cases']),'exact_quotes':len(quotes),'failures':[x['check'] for x in checks if not x['pass']]})
