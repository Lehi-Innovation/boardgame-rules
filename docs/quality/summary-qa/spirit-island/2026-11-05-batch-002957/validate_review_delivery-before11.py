from pathlib import Path
import json,hashlib,collections,re
B=Path(__file__).parent.resolve();ROOT=B.parents[4];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[];resolved={}
def lookup(path,digest):
 p=Path(path);p=p if p.is_absolute() else ROOT/p
 if p.exists() and H(p)==digest:return p
 if digest not in resolved:
  candidates=list(B.glob('*.json'))+list(B.glob('source-candidate-*.md'))+list(B.glob('*/summary-snapshot.md'))
  resolved[digest]=next((x for x in candidates if H(x)==digest),None)
 return resolved[digest]
def getrows(d):
 if 'technical_read_log' in d:
  by={x['file']:x.get('sha256') for x in d.get('input_manifest',[])}
  return [{**x,'sha256':by.get(x['file'])} for x in d['technical_read_log']['full_reads']]
 if 'read_audit' in d:return d['read_audit']['full_reads']
 e=d.get('read_evidence',{})
 if isinstance(e,list):return e
 if 'ledger_path' in e:
  ledger=json.loads(Path(e['ledger_path']).read_text())
  if 'text_reads' in ledger:
   by=collections.defaultdict(list)
   for x in ledger['text_reads']:by[x['path']].append(x)
   return [{'path':name,'sha256':rows[0]['original_byte_sha256'],'chunks':[{'range':r['range'],'slice_sha256':r['slice_utf8_sha256']} for r in rows],'output_cap_tokens':min(r['max_output_tokens'] for r in rows),'truncated':False} for name,rows in by.items()]
  return [{**x,'read_ranges':x['delivered_slices_zero_based_half_open'],'output_cap_tokens':int(re.search(r'max_output_tokens=(\d+)',x['delivery']).group(1)),'truncated':False} for x in ledger['text_files']]
 if 'text_files' in e:
  return [{**x,'chunks':[{'range':[c['start'],c['end_exclusive']],'slice_sha256':c['slice_sha256_utf8']} for c in x['complete_contiguous_ranges']],'output_cap_tokens':x['tool_response_cap_tokens'],'truncated':x.get('truncation_detected',False)} for x in e['text_files']]
 for key in ['text_reads','text_inputs','full_reads','inputs','complete_text_reads']:
  if key in e:return e[key]
 raise ValueError('Unrecognized read schema: '+str(d.keys()))
for report in sorted(B.glob('coverage-review-??.json')):
 d=json.loads(report.read_text());rows=getrows(d);out=[]
 for x in rows:
  path=x.get('path',x.get('file'));digest=x.get('sha256',x.get('source_sha256'));full=x.get('complete',x.get('complete_read',x.get('read_completely',x.get('complete_contiguous_read',True))))
  pairs=None;chunks=None
  for key in ['chunks','delivered_chunks']:
   if key in x:chunks=x[key];pairs=[c['range'] for c in chunks];break
  if pairs is None:
   for key in ['read_ranges','complete_read_ranges','ranges','contiguous_read_ranges_half_open','contiguous_half_open_character_ranges','ranges_half_open','read_ranges_zero_based_half_open','complete_read_ranges_zero_based_half_open']:
    if key in x:pairs=x[key];break
  if pairs is None:raise ValueError('No ranges '+str(x.keys()))
  p=lookup(path,digest);s=p.read_text() if p else '';normalized=[(v['start'],v['end']) if isinstance(v,dict) else tuple(v) for v in pairs];length=len(s)
  limits=all(0<b-a<=6000 and 0<=a<b<=length for a,b in normalized)
  contiguous=bool(normalized) and normalized[0][0]==0 and normalized[-1][1]==length and all(a[1]==b[0] for a,b in zip(normalized,normalized[1:]))
  hashes=True
  if chunks:
   for c,(a,b) in zip(chunks,normalized):
    h=next((c[k] for k in ['utf8_sha256','sha256_utf8','slice_sha256','sha256'] if k in c),None)
    if h:hashes=hashes and hashlib.sha256(s[a:b].encode()).hexdigest()==h
  cap=next((x[k] for k in ['max_output_tokens_per_call','output_cap_tokens','tool_output_cap_tokens','per_call_output_cap_tokens'] if k in x),None)
  truncated=any(x.get(k,False) for k in ['source_output_truncated','truncation_observed','truncated'])
  passed=bool(p) and limits and hashes and not truncated and (contiguous if full else True) and (cap>=4000 if cap is not None else True)
  out.append({'original_path':path,'retained_matching_path':str(p) if p else None,'sha256':digest,'full_read':full,'characters':length,'ranges':normalized,'range_limit_ok':limits,'complete_contiguous':contiguous,'per_slice_hashes_match':hashes,'output_cap_when_recorded':cap,'pass':passed})
 checks.append({'report':report.name,'report_sha256':H(report),'linked_read_ledger':({'path':d['read_evidence']['ledger_path'],'sha256':H(Path(d['read_evidence']['ledger_path']))} if isinstance(d.get('read_evidence'),dict) and 'ledger_path' in d['read_evidence'] else None),'text_files':len(out),'chunks':sum(len(x['ranges']) for x in out),'all_passed':all(x['pass'] for x in out),'inputs':out})
p=B/'coverage-delivery-validation.json';p.write_text(json.dumps({'reports':checks,'all_passed':all(x['all_passed'] for x in checks),'note':'Checks reported complete Unicode slice coverage, retained historical file hashes and per-slice hashes where present. Raw per-tool transcripts retain actual delivery and cap evidence; targeted primary HTML reads need not cover the whole HTML when full reading derivative was delivered.'},indent=2)+'\n');print(json.dumps({'reports':len(checks),'all_passed':all(x['all_passed'] for x in checks),'failures':[{'report':x['report'],'inputs':[i for i in x['inputs'] if not i['pass']]} for x in checks if not x['all_passed']]},indent=2))
