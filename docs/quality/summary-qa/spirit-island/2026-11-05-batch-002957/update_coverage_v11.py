from pathlib import Path
import json,hashlib,shutil
B=Path(__file__).parent;P=B/'coverage-ledger.json';backup=B/'coverage-ledger-before-review05-resolution.json'
if backup.exists():raise RuntimeError('Refuse historical overwrite')
shutil.copyfile(P,backup);j=json.loads(P.read_text());r=json.loads((B/'coverage-review-05.json').read_text());new=json.loads((B/'expanded-v11/novelty.json').read_text());j['benchmark']='expanded-v11';j['question_count']=127
for a in new:
 s=a['exact_source_refs'][0];refs=[{'file':s['reading_file'],'label':s['entry_anchor'],'character_range':s['character_range_half_open'],'passage_sha256':s['passage_sha256']},{'file':s['primary_file'],'label':s['entry_anchor'],'character_range':s['primary_character_range_half_open'],'passage_sha256':s['primary_passage_sha256']}];j['acceptance_ledger'].append({**a,'bank':'expanded-v11','decision':'accepted before any expanded readers'});j['precise_clause_mappings'].append({'topic':a['new_coverage'],'source_refs':refs,'question_ids':[a['id']],'tested_clause':a['question']});j['faq_rulings'].append({'ruling_id':'review05-resolution-'+a['id'],'rule':a['answer'],'source_refs':refs,'question_ids':[a['id']],'scope':'included','reason':a['why_not_previously_requested']})
for x in j['book_passages']:
 if x['passage']=='Repeat':x['question_ids'].append('Q126')
 if x['passage']=='Presence and Sacred Sites':x['question_ids'].append('Q127')
for x in j['faq_rulings']:
 if x['ruling_id']=='repeat-option':x['rule']+=' The chosen card may enter play after the once-this-turn permission was granted; it is a Spirit permission rather than a grant-time card snapshot.';x['question_ids'].append('Q126')
 if x['ruling_id']=='presence-stack':x['rule']='No standard per-land stacking limit applies to any piece. Many Presence of one Spirit still count as one Sacred Site in that land.';x['question_ids'].append('Q127')
j['novelty_disputes'][0].update(status='Fresh independent review05 adjudicates distinct printed-Power target permission; geometric within-Range fact not counted again. Dissenting source-only08 remains historical.',independent_resolution=r['novelty_notes'][2])
j['independent_challenge_history'].append({'report':'coverage-review-05.json','verdict':r['verdict'],'key_verdict':r['fixed_key_verdict'],'accepted_ids':['Q126','Q127'],'prior_zero_pass_claim_revoked':True,'Q125_overlap_classification':r['novelty_notes'][2]})
j['passes'] += [
 {'pass':22,'focus':'Fresh review05 temporal eligible-card set and per-land capacity limits','new_questions':2,'ids':['Q126','Q127'],'review':'coverage-review-05.json'},
 {'pass':23,'focus':'Complete current procedure map and127 actual prompts: setup/Growth/resources/card gain-play-Forget/Repeat timing and eligibility/Presence and all per-land versus physical-supply limits','new_questions':0,'method':'All new exact source clauses and actual prompts compared; retained named-operation coverage distinguished from surplus key facts. Later-entering eligibility and default stacking now explicitly requested.'},
 {'pass':24,'focus':'Complete temporal/exception/outcome sweep: Invader/Fear/Blight/Dahan, eight original Spirits, primary-verified named cards, Damage/Health/protection, action trees and all outcomes; reject mere combinations','new_questions':0,'method':'Previously fully read primary corpus plus exact new clause ranges, whole current map and all127 actual prompts; no imported excluded producer or changed-number novelty.'}]
j['rejection_ledger'] += [
 {'pass':23,'candidate':'A different original-core later-played card under a prior Repeat permission','decision':'rejected','because':'Q126 now directly requests the grant-to-use eligible-card temporal boundary. Different card identities or phase details do not add a rule.'},
 {'pass':23,'candidate':'Separate default stacking-limit questions for Cities, Dahan and Presence','decision':'rejected','because':'Q127 explicitly asks every piece type and otherwise-legal Build/Gather/Presence placement; one general rule, not multiple type or count discoveries.'},
 {'pass':23,'candidate':'Additional Growth mixes, closer Power distances, deck exhaustion counts or threshold numbers','decision':'rejected','because':'Q124/Q125/Q17/Q123 directly request those source procedures/permissions; arithmetic or different presentation alone is not novelty.'},
 {'pass':24,'candidate':'Further Blight/Defend/Ravage totals, Ocean/Bringer/Vengeance chains and alternate protection producers','decision':'rejected','because':'Distinct temporal/source/type boundaries already directly requested. Mechanical recombinations without a new sourced rule are not additional coverage.'},
 {'pass':24,'candidate':'Adversary/Scenario stacking caps, thematic population, optional scoring/difficulty and expansion-only cards/tokens','decision':'excluded','because':'Broad FAQ examples do not expand original standard-core scope.'}]
j['stopping_rule']={'consecutive_zero_addition_passes':[23,24],'all_in_scope_procedural_passages_mapped':True,'independent_challenge':'pending-new-fresh-review06','claim':'Working source-clause saturation within documented original-core sources and actual-prompt novelty, subject to a fresh challenge. All historical rejected stopping claims preserved.'};j['input_hashes']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [B/'expanded-v11/questions.json',B/'expanded-v11/answer-key.json',Path('extracted/spirit-island-rules.txt'),B/'supplemental-source-manifest-v2.json']};P.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
compact={k:j[k] for k in ['benchmark','question_count','source_hierarchy','novelty_policy','stopping_rule','book_passages','faq_rulings','precise_clause_mappings']};compact.update(retained_non_novel_regressions=['Q32','Q100'],last_targeted_passes=j['passes'][-2:],last_rejections=j['rejection_ledger'][-5:]);aliases={}
def walk(x):
 if isinstance(x,dict):
  out={}
  for k,v in x.items():
   if k in ['url','source_url','reason','coverage_credit_limit']:continue
   if k in ['file','source_file'] and isinstance(v,str):
    full=str(Path(v).resolve());a=next((a for a,p in aliases.items() if p==full),None)
    if a is None:a=f'source{len(aliases)+1}';aliases[a]=full
    out[k]=a
   elif k=='source_refs':out[k]=[walk({a:s[a] for a in ['file','entry_anchor','label','character_range','anchor_character_range','passage_sha256','source_passage_sha256'] if a in s}) if isinstance(s,dict) else s for s in v]
   else:out[k]=walk(v)
  return out
 if isinstance(x,list):return [walk(v) for v in x]
 return x
compact=walk(compact);compact['source_aliases']=aliases;assert all(Path(v).exists() for v in aliases.values());mp=B/'coverage-map-for-review-06.json';mp.write_text(json.dumps(compact,ensure_ascii=False,separators=(',',':'))+'\n')
files=[B/'expanded-v11/questions.json',B/'expanded-v11/answer-key.json',mp,B/'supplemental-source-manifest-v2.json',Path('extracted/spirit-island-rules.txt'),Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/spirit-island/living-faq-core-game.txt'),Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/source-preflight/spirit-island/living-faq-setup.txt')];(B/'coverage-review-06-input-manifest.json').write_text(json.dumps({'benchmark':'expanded-v11','question_count':127,'sha256':{str(p.resolve()):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'blind_to':['summary','readers','grades','earlier review/adjudication conclusions']},indent=2)+'\n');p=B/'progress.json';v=json.loads(p.read_text());v.update(phase='expanded-v11-frozen-fresh-coverage06-and-source-audit06',question_count=127);v['coverage_review']={'status':'pending-fresh-review06','benchmark':'expanded-v11','question_count':127,'path':str((B/'coverage-review-06.json').resolve()),'prior_review05_gaps_addressed':['Q126','Q127'],'Q125_overlap':'Fresh review05 independently confirms distinct printed-Power legality, no duplicate geometry credit'};v['coverage_stopping_rule']={'passes':[23,24],'new_questions':[0,0],'independent_challenge':'pending-fresh-review06'};p.write_text(json.dumps(v,indent=2)+'\n');print('Updated v11 map',len(mp.read_text()),'chars. Fresh audit06 pending on candidate10.')
