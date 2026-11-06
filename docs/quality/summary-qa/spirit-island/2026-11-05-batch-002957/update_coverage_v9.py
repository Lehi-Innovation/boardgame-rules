from pathlib import Path
import json,hashlib,shutil,copy
B=Path(__file__).parent;P=B/'coverage-ledger.json';backup=B/'coverage-ledger-before-review03-resolution.json'
if backup.exists():raise RuntimeError('Refuse overwrite historical state')
shutil.copyfile(P,backup);j=json.loads(P.read_text());r=json.loads((B/'coverage-review-03.json').read_text());new=json.loads((B/'expanded-v8/novelty.json').read_text())+json.loads((B/'expanded-v9/novelty.json').read_text());j['benchmark']='expanded-v9';j['question_count']=123
for a in new:j['acceptance_ledger'].append({**a,'bank':'expanded-v8' if int(a['id'][1:])<123 else 'expanded-v9','decision':'accepted','origin':'fresh review03 / independent clause adjudication / linked primary source completion'})
refs={a['id']:a['source_refs'] for a in new}
for c in r['remaining_gaps']:refs['Q'+str(115+int(c['candidate_id'][1:]))]=c['source_refs']
for n,i in [('03','Q118'),('04','Q121'),('05','Q122'),('06','Q123')]:refs[i]=json.loads((B/f'coverage-novelty-adjudication-{n}.json').read_text())['source_refs']
for i,n in [('Q119','what-do-range-boosts-affect.txt'),('Q120','range-in-text-of-powers-that-target-spirits.txt')]:
 p=(B/'card-scope-source'/n).resolve();s=p.read_text();refs[i]=[{'file':str(p),'label':n,'character_range':[0,len(s)],'passage_sha256':hashlib.sha256(s.encode()).hexdigest()}]+refs[i]
for a in new:
 j['precise_clause_mappings'].append({'topic':a['new_coverage'],'source_refs':refs[a['id']],'question_ids':[a['id']],'tested_clause':a['question'],'coverage_credit_limit':a.get('coverage_credit_limit','Only source-defined new branch, not repeated arithmetic or already-tested auxiliary clauses.')})
 j['faq_rulings'].append({'ruling_id':'review03-resolution-'+a['id'],'rule':a['answer'],'source_refs':refs[a['id']],'question_ids':[a['id']],'scope':'included','reason':'New actual requested clause, explicitly frozen before expanded readers.'})
for x in j['faq_rulings']:
 if x['ruling_id']=='challenge01-C02':
  x['rule']="General Power Range boosts can affect printed numeric Range arrows in targeting and effect text, obeying restrictions; they do not boost a Range boost or another Spirit's actions. Shadows changes targeting Range only. Excluded Sky example removed in v6. Linked precise primary source qualifies old broad wording explicitly in v8/Q105 key-corrections.json."
  x['source_refs']+=refs['Q119'][:1]
 if x['ruling_id']=='blight-cascade':x['rule']='Each addition of one or more Blight destroys one Presence of every Spirit there, not one per token; separate additions destroy Presence again. Cascades remain within the original action tree.';x['question_ids']+=['Q116']
 if x['ruling_id']=='innate-single':x['question_ids']+=['Q123']
 if x['ruling_id']=='concealing-dahan-only':x['question_ids']+=['Q117','Q118']
 if x['ruling_id']=='defend-both':x['question_ids']+=['Q118','Q122']
extra={'Invader eligibility and Ravage':['Q122'],'Blight cascade and Presence sidebar':['Q116'],'Innates':['Q123'],'Blight':['Q116'],'Damage tracking':['Q122'],'Thresholds / Instead':['Q123'],'Forego Power / fewer Elements':['Q121','Q123'],'Power anatomy Range/Target':['Q119','Q120'],'Defend':['Q118','Q122']}
for row in j['book_passages']:row['question_ids']=list(dict.fromkeys(row['question_ids']+extra.get(row['passage'],[])))
j['source_key_precision_corrections']={'path':'expanded-v8/key-corrections.json','ids':['Q105'],'questions_unchanged':True,'expanded_readers_before_correction':False}
j['independent_challenge_history'].append({'report':'coverage-review-03.json','verdict':r['verdict'],'key_verdict':r['fixed_key_audit'],'accepted_additions':2,'resolved_by_ids':['Q116','Q117'],'further_source_clause_acceptances':['Q118','Q119','Q120','Q121','Q122','Q123'],'prior_zero_pass_claim_revoked':True})
j['passes'] += [
 {'pass':15,'focus':'Fresh review03 independently rejects previous stopping claim; simultaneous Blight and protection boundaries','new_questions':2,'ids':['Q116','Q117'],'review':'coverage-review-03.json'},
 {'pass':16,'focus':'Reopened exact clause comparisons, independent novelty adjudications03–06, two linked primary Range entries','new_questions':6,'ids':['Q118','Q119','Q120','Q121','Q122','Q123']},
 {'pass':17,'focus':'Complete core procedural map and actual123 prompts: setup, tracks, Growth, resources, targeting, play, Elements, thresholds, Repeat, movement, retained effects; compare positive/negative permissions','new_questions':0,'method':'Source passages already fully read; renewed complete69-row book map,149-row prior FAQ map and all123 actual question prompts; focused linked Range entries reread in full. No credit for extra unrequested key text.'},
 {'pass':18,'focus':'Core exceptions and temporal outcomes: all eight original Spirits,33 primary card faces/scope legend, Fear/Blight/Ravage/Defend/Dahan, action trees and victory/defeat; recheck new clauses and reject recombinations','new_questions':0,'method':'Complete mapped source-clause sweep after Q123 freeze, actual question clauses compared, explicit protection/Range ownership and origin boundaries. Earlier primary face checks retained; no excluded examples imported.'}]
j['rejection_ledger'] += [
 {'pass':17,'candidate':'Another threshold Element amount or another cannot-cherry-pick example','decision':'rejected','because':'Q123 now asks the genuine positive permission, Q73 the forbidden cherry-pick, Q27 gain/loss/order; amount changes add no rule.'},
 {'pass':17,'candidate':'Reaching Grasp bonus to another named original card or different bonus magnitudes','decision':'rejected','because':'Q105/Q119/Q120 cover targeting/internal eligibility, not-boost-a-boost, ownership, instructed origin and explicit origin override. Different cards/numbers with same conditions add no branch.'},
 {'pass':17,'candidate':'Foregone card refund/discard as additional discoveries','decision':'rejected as novelty','because':'Q16/Q30 already request those facts; Q121 new credit is retained printed Elements only.'},
 {'pass':18,'candidate':'Different defended Ravage totals or third repeated Ravage','decision':'rejected','because':'Q122 specifically asks reusable mitigation and nonstored partial land Damage. Extra arithmetic/occurrences repeat that rule.'},
 {'pass':18,'candidate':'Another Concealing Shadows protected Ravage or another direct-Destruction card','decision':'rejected','because':'Q115 covers protected Ravage, Q117 directDestroy and Q118 nonRavageDamage source boundary; changing producer adds no rule.'},
 {'pass':18,'candidate':'Further Ocean/Vengeance/Bringer trigger chains and alternate simultaneous Blight counts','decision':'rejected','because':'Q89 recursion, Q80/Q81 cleanup, Q113 failedDrownPush, Q116 per-addition Presence unit already explicit. Combining outcomes is not a new sourced exception.'},
 {'pass':18,'candidate':'Expansion examples in new linked Range FAQ, optional difficulty/timeboxing/scoring','decision':'excluded','because':'Only original-core-applicable general procedures and positively established original cards belong to authorized scope.'}]
j['stopping_rule']={'consecutive_zero_addition_passes':[17,18],'all_in_scope_procedural_passages_mapped':True,'independent_challenge':'pending-new-fresh-review04','claim':'Working saturation within documented original-core sources and strict actual-prompt novelty. Prior three rejected stopping claims remain historical; fresh challenge required.'}
j['input_hashes']={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [B/'expanded-v9/questions.json',B/'expanded-v9/answer-key.json',Path('extracted/spirit-island-rules.txt'),B/'supplemental-source-manifest-v2.json']}
P.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
compact=copy.deepcopy({k:j[k] for k in ['benchmark','question_count','source_hierarchy','novelty_policy','stopping_rule','book_passages','faq_rulings','precise_clause_mappings']});compact.update(retained_non_novel_regressions=['Q32','Q100'],explicit_prior_corrections=['expanded-v6/scope-corrections.json','expanded-v8/key-corrections.json'],last_targeted_passes=j['passes'][-2:],last_rejections=j['rejection_ledger'][-7:]);aliases={}
def walk(x):
 if isinstance(x,dict):
  for k,v in list(x.items()):
   if k in ['file','source_file'] and isinstance(v,str):
    full=str(Path(v).resolve());alias=next((a for a,p in aliases.items() if p==full),None)
    if alias is None:alias=f'source{len(aliases)+1}';aliases[alias]=full
    x[k]=alias
   elif k in ['url','source_url']:del x[k]
   else:walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
walk(compact);compact['source_aliases']=aliases
(B/'coverage-map-for-review-04.json').write_text(json.dumps(compact,indent=2,ensure_ascii=False)+'\n')
p=B/'progress.json';v=json.loads(p.read_text());v.update(phase='expanded-v9-frozen-fresh-coverage04-and-source-audit05',question_count=123);v['coverage_review']={'status':'pending-fresh-review04','benchmark':'expanded-v9','question_count':123,'path':str((B/'coverage-review-04.json').resolve()),'prior_review03_gaps_resolved':['Q116','Q117'],'further_clause_additions':['Q118','Q119','Q120','Q121','Q122','Q123']};v['coverage_stopping_rule']={'passes':[17,18],'new_questions':[0,0],'independent_challenge':'pending-new-fresh-review04'};v['source_audit'].update(status='running-fresh-audit05',candidate_path=str((B/'source-candidate-09.md').resolve()));v['hashes']['canonical_summary']=hashlib.sha256(Path('rules/spirit-island.md').read_bytes()).hexdigest();v['source_paths'].append(str((B/'supplemental-source-manifest-v2.json').resolve()));v['technical_protocol']['grader_block_size']='balanced15–20';p.write_text(json.dumps(v,indent=2)+'\n')
print('Map v9:',len((B/'coverage-map-for-review-04.json').read_text()),'characters; working stopping passes17/18 need fresh challenge.')
