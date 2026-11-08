"""Verify complete frozen case coverage and literal references; semantic adoption is separate."""
from pathlib import Path
import collections,hashlib,json
B=Path(__file__).resolve().parent;D=B/'expanded-iteration-05';A=D/'adjudication-01';load=lambda p:json.loads(p.read_text());H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();report=load(A/'adjudication.json');cases=load(A/'raw-cases.json');manifest=load(A/'input-manifest.json');maps={x['id']:x for x in load(A/'asked-facts.json')['questions']};original=load(D/'results.json');checks=[]
def ck(ok,label):
 assert ok,label
 checks.append(label)
def pointer(value,path):
 for key in path.strip('/').split('/'):
  key=key.replace('~1','/').replace('~0','~');value=value[int(key)] if isinstance(value,list) else value[key]
 return value
def strings(value):
 if isinstance(value,str):return [value]
 if isinstance(value,dict):return [s for v in value.values() for s in strings(v)]
 if isinstance(value,list):return [s for v in value for s in strings(v)]
 return []
allowed={Path(p).resolve() for p in manifest['inputs']};byname={p.name:p for p in allowed}
def resolve(raw):
 p=Path(raw);return p.resolve() if p.is_absolute() else byname[p.name]
expected={(x['reader'],x['id']) for x in cases['requested_cases']};rows=report['adjudications'];ck(len(rows)==len(expected)==manifest['case_count'] and {(x['reader'],x['id']) for x in rows}==expected,'all selected cases exactly once');ck({(x['reader'],x['id']) for x in report['expected_cases']}==expected,'declared complete expected cases');ck({resolve(x['path']) for x in report['inputs_read']}==allowed and len(report['inputs_read'])==5,'exact five declared inputs')
for inp in report['inputs_read']:
 p=resolve(inp['path']);s=p.read_text();ck(inp['sha256']==H(p) and inp['unicode_character_length']==len(s) and inp['utf8_byte_length']==p.stat().st_size,'exact input identity '+p.name);pos=0
 for part in inp['read_ranges']:
  start,end=part['start_inclusive'],part['end_exclusive'];ck(start==pos and 0<end-start<=6000 and part['unicode_character_count']==end-start and part['output_cap_tokens']>=4000 and part['exit_code']==0 and not part['truncated'] and part['complete_literal_range_delivered'],'declared contiguous bounded literal '+p.name+str([start,end]));pos=end
 ck(pos==len(s) and inp['caps_and_truncation_check']['ranges_contiguous_complete'],'whole input declared '+p.name)
for r,data in cases['readers'].items():
 raw=load(D/(r+'.json'));by={x['id']:x for x in raw['answers']};ck(H(D/(r+'.json'))==cases['original_raw_output_sha256'][r],'whole original reader binding '+r)
 for entry in data['answers']:ck(entry==by[entry['id']],'entire original entry unchanged '+r+entry['id'])
guide=(D/'summary-snapshot.md').read_text();facts=samerefs=summaryrefs=exactrange=withinrange=derived=negative=literal_expected=0
for row in rows:
 r,q=row['reader'],row['id'];old=next(x for x in original['readers'][r]['grades'] if x['id']==q);ck(row['original_grade']==old['grade'],'exact original grade '+r+q);parts=row['requested_part_assessment'];mapping=maps[q]['requested_clauses'];ck(len(parts)==len(mapping) and {p['clause_id'] for p in parts}=={p['clause_id'] for p in mapping},'all mapped clauses once '+r+q);index=next(i for i,x in enumerate(cases['readers'][r]['answers']) if x['id']==q);prefix=f'/readers/{r}/answers/{index}'
 for part in parts:
  clause=next(c for c in mapping if c['clause_id']==part['clause_id']);ck(part['actual_requested_clause']==clause['actual_requested_clause'],'literal actual ask '+r+q);fs=part['fact_assessments'];ck(len(fs)==len(clause['required_facts']) and {f['fact_index'] for f in fs}==set(range(1,len(fs)+1)),'all mapped facts once '+r+q)
  for fact in fs:
   facts+=1;ck(isinstance(fact['expected'],str) and bool(fact['expected']),'expected fact present');literal_expected+=fact['expected']==clause['required_facts'][fact['fact_index']-1]
   for ref in fact['same_entry_references']:
    ck(resolve(ref['input_path'])==(A/'raw-cases.json').resolve() and (ref['json_pointer']==prefix or ref['json_pointer'].startswith(prefix+'/')),'reference to same entire entry');node=pointer(cases,ref['json_pointer']);ck(isinstance(ref['quotation'],str) and bool(ref['quotation']) and any(ref['quotation'] in text for text in strings(node)),'literal same-entry quotation');samerefs+=1
   for ref in fact['summary_support']:
    ck(resolve(ref['path'])==(D/'summary-snapshot.md').resolve(),'support references frozen summary');quote=ref.get('quotation');span=ref.get('character_range')
    if isinstance(quote,str) and quote:
     ck(quote in guide,'literal support quotation present');summaryrefs+=1
     if span is None:derived+=1
     else:
      if isinstance(span,dict):start=span.get('start',span.get('start_inclusive'));end=span.get('end',span.get('end_exclusive'))
      else:start,end=span
      ck(isinstance(start,int) and isinstance(end,int) and 0<=start<end<=len(guide) and quote in guide[start:end],'quoted text within declared summary range');exactrange+=guide[start:end]==quote;withinrange+=guide[start:end]!=quote
    else:negative+=1
 ck(row['adjudicated_grade'] in ['correct','partial','incorrect'] and isinstance(row['unresolved'],bool),'valid semantic decision fields '+r+q)
ck(facts==manifest['requested_fact_assessment_count'],'complete mapped fact assessments');ck(dict(collections.Counter(x['adjudicated_grade'] for x in rows))=={k:v for k,v in report['decision_counts'].items() if v},'all decision counts agree');ck(H(A/'adjudication.json')==load(A/'adjudication-original-freeze.json')['sha256']==H(A/'adjudication-original-completed.json'),'entire original adjudication frozen unchanged')
overlay={}
for r,data in original['readers'].items():
 replacements={x['id']:x['adjudicated_grade'] for x in rows if x['reader']==r};c=collections.Counter(replacements.get(x['id'],x['grade']) for x in data['grades']);overlay[r]={k:c[k] for k in ['correct','partial','incorrect']}
out={'all_passed':True,'checks':len(checks),'check_labels':checks,'complete_cases':len(expected),'complete_fact_assessments':facts,'literal_same_entry_references':samerefs,'literal_summary_references':summaryrefs,'summary_quotations_equal_exact_range':exactrange,'summary_quotations_within_larger_range':withinrange,'summary_quotations_verified_without_declared_span':derived,'negative_or_interpretive_support_claims_not_literal_quotes':negative,'expected_strings_exact_map_matches':literal_expected,'adjudicated_totals_pending_semantic_adoption':overlay,'unresolved_case_count':sum(x['unresolved'] for x in rows),'unresolved_adjudications':report['unresolved_adjudications'],'genuine_key_or_map_findings':report['genuine_key_or_map_findings'],'original_report_sha256':H(A/'adjudication.json'),'original_results_sha256':H(D/'results.json'),'limitations':'Literal/structure checks do not prove interpretation or cognition. Negative source-support claims and expected-fact paraphrases require separate parent semantic review. No grading threshold or original output modified.'};p=A/'structural-reference-validation.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='check_labels'}))
