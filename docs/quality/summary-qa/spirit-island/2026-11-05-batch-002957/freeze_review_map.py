from pathlib import Path
import json,hashlib,sys
B=Path(__file__).parent;idx=sys.argv[1];j=json.loads((B/'coverage-ledger.json').read_text());compact={k:j[k] for k in ['benchmark','question_count','source_hierarchy','novelty_policy','stopping_rule','book_passages','faq_rulings','precise_clause_mappings']};aliases={}
# Supply the required stopping protocol, not prior review outcomes or author saturation claims.
compact['stopping_rule']={'required_consecutive_zero_addition_passes':2,'fresh_independent_challenge_required':True,'no_forced_pass_or_discovery_quota':True}
compact['working_base_scope_credit']={'path':str((B/j['benchmark']/'core-scope-credit.json').resolve()),'interpretation':'Independently validate this working clause-level metadata. Historical mappings can retain source-correct generalized/unverified regressions without granting current-base novelty or making every broad Core-labelled FAQ row a saturation requirement. Zero credit never waives regression grading.'}
def walk(x):
 if isinstance(x,dict):
  x=dict(x)
  for old,new in [('path','file'),('original_byte_sha256','file_sha256'),('passage_utf8_sha256','passage_sha256'),('full_native_bounds_xyxy','visual_region_xyxy'),('region','label')]:
   if old in x and new not in x:x[new]=x[old]
  out={}
  for k,v in x.items():
   if k in ['url','source_url','reason','coverage_credit_limit']:continue
   if k in ['file','source_file','primary_file'] and isinstance(v,str):
    full=str(Path(v).resolve());a=next((a for a,p in aliases.items() if p==full),None)
    if a is None:a=f'source{len(aliases)+1}';aliases[a]=full
    out[k]=a
   elif k=='source_refs':out[k]=[walk({a:s[a] for a in ['file','path','source_file','primary_file','entry_anchor','anchor','label','region','full_native_bounds_xyxy','character_range','anchor_character_range','passage_sha256','passage_utf8_sha256','source_passage_sha256','file_sha256','original_byte_sha256','visual_region_xyxy','transcribed_passage','transcription','transcription_sha256','relevant_region','image_region_coordinates'] if a in s}) if isinstance(s,dict) else s for s in v]
   else:out[k]=walk(v)
  return out
 if isinstance(x,list):return [walk(v) for v in x]
 return x
compact=walk(compact);compact['source_aliases']=aliases;assert all(Path(v).exists() for v in aliases.values());mp=B/f'coverage-map-for-review-{idx}.json';assert not mp.exists();mp.write_text(json.dumps(compact,ensure_ascii=False,separators=(',',':'))+'\n');bank=B/j['benchmark'];files=[bank/'questions.json',bank/'answer-key.json',mp,B/'supplemental-source-manifest-v4.json',Path('extracted/spirit-island-rules.txt'),Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/spirit-island/living-faq-core-game.txt'),Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/spirit-island/living-faq-setup.txt')]
if (bank/'asked-fact-map.json').exists():files.append(bank/'asked-fact-map.json')
if (bank/'core-scope-credit.json').exists():files.append(bank/'core-scope-credit.json')
files += [B/'source-manifest.json',B/'scope-reachability-steering-2026-11-05.txt']
p=B/f'coverage-review-{idx}-input-manifest.json';assert not p.exists();p.write_text(json.dumps({'benchmark':j['benchmark'],'question_count':j['question_count'],'sha256':{str(x.resolve()):hashlib.sha256(x.read_bytes()).hexdigest() for x in files},'blind_to':['summary','readers','grades','earlier review/adjudication conclusions']},indent=2)+'\n');print('Map frozen:',mp,len(mp.read_text()),'chars')
