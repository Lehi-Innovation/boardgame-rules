from pathlib import Path
import json, hashlib, collections

out=Path(__file__).parent
own=out.parent
base=own.parent
candidate=base/'expanded-candidate-v10'
def read(p): return json.loads(p.read_text())
def write(name,data): (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
q=read(candidate/'questions.json')['questions']
k=read(candidate/'answer-key.json')['answers']
a=read(candidate/'asked-clause-map.json')
ids=[f'Q{i:02}' for i in range(1,95)]
assert [r['id'] for r in q]==ids
assert [r['id'] for r in k]==ids
assert [r['id'] for r in a]==ids
oldq=read(base/'expanded-candidate-v9/questions.json')['questions']
oldk=read(base/'expanded-candidate-v9/answer-key.json')['answers']
olda=read(base/'expanded-candidate-v9/asked-clause-map.json')
assert q[:93]==oldq and k[:93]==oldk and a[:93]==olda
proposal=read(own/'revision-05/proposed-additions.json')[0]
assert q[-1]['question']==proposal['question']
assert k[-1]['expected_answer']==proposal['expected_answer']
assert k[-1]['required_facts']==proposal['asked_facts']==a[-1]['asked_facts']

scope=read(own/'revision-05/scope-review.json')
for i,r in enumerate(scope['records']):
 assert r['id']==ids[i]
 assert r['actual_asked_facts']==a[i]['asked_facts']
 r['candidate']='expanded-candidate-v10'
 r['recheck_basis']='All original93 question/key/clause records match v9 exactly after full structural comparison. Complete prior source/native deliveries reused after unchanged hashes; all94 operative questions/asked facts freshly delivered. Renewed broad passes in stopping-review.json screen actual scope and do not credit background.'
scope['candidate']='expanded-candidate-v10'
scope['qualification']='All94 fixed outcomes and actual asked clauses are source-supported. This current-bank source finding does not approve essential unresolved SG01 complete-core scope. Frozen references Q68/Q73/Q76 receive zero novelty credit.'
scope['ids_exactly_once']=ids
scope['records'].append({
 'id':'Q94','candidate':'expanded-candidate-v10','question':q[-1]['question'],
 'actual_asked_facts':a[-1]['asked_facts'],'scenario_givens':a[-1]['scenario_givens'],
 'contextual_background':a[-1]['contextual_background'],'source_refs':a[-1]['source_refs'],
 'scope_verdict':'Literal actor/beneficiary, sequence and mandatory positive branch confirmed; fixed asset count/capital coefficients are context.',
 'fixed_key_outcome_verdict':'source-supported','source_fact_validation':'supported',
 'material_extra_key_claims_checked':'No material false extra claim. No asset-selector identity beyond the printed resolver instruction or inter-clause trading/interrupt ruling is inferred.',
 'independent_validation':'Fresh original-detail native Vanity Project complete cell and construction atlas match previous verified payload bytes/dimensions. Printed grant followed by Then, discard ... belonging to that player, if possible supports all three actual asked facts.',
 'novelty_credit':'One qualifying branch accepted from v9 proposal; not counted as a further addition in either renewed v10 pass.',
 'recheck_basis':'Exact verbatim proposal comparison plus fresh native payload verification and RR16.5 effect resolution; ordinary discard destination remains separate Q18.'
})
scope['delta_confirmation']={'original93_question_records_exactly_equal_v9':True,'original93_key_records_exactly_equal_v9':True,'original93_clause_records_exactly_equal_v9':True,'Q94_verbatim_own_proposal':True,'all94_ids_once':True}
assert len(scope['records'])==94 and len(set(r['id'] for r in scope['records']))==94
write('scope-review.json',scope)

demotions=[
 ('Q11','Ordinary illness action numerical increment','No procedure lost: action involvement, failed attempts, once-per-action, events/production exclusions remain asked Q11; normal two-threat comparison is also actually asked Q52. Root return/+2 remains Q11/Q10.','Q11 Q52 Q10'),
 ('Q27','Rachel exact one-card draw count','Only a fixed coefficient was demoted. End-of-each-deal timing, zero-hand condition, optionality and topmost type remain asked. No distinct branch follows from changing count.','Q27'),
 ('Q42','Alex exact two-capital cost','Payment timing before an owned-asset swap, permitted targets/self-asset and nonclaim status remain asked. The fixed two-capital coefficient is consultation, not a new cost procedure.','Q42'),
 ('Q46','Jackson exact two-capital gain','Reveal timing, optional exhaust, another-player selection, winning condition and gain actor remain asked. Different payment amount adds no procedure.','Q46'),
 ('Q63','Vanity Project ordinary successful asset discard','The former genuine gap is closed by Q94: after grant, same beneficiary asset, mandatory with eligible asset. Assetless grant/no-discard branch and supporter difference remain Q63.','Q63 Q94'),
 ('Q73','Root numerical magnitude two each','Movement-order/else branch/possibility of threat remain Q73; actual ordinary Root reserve/+2/no-contract procedure is explicitly asked Q10. No new identity substitution credit.','Q73 Q10'),
 ('Q74','Full ordinary blocking/Root result beyond binary applicability','Q74 asks highest-first/two movement instructions and normal blocking/Root applicability. Full cascade, reserve return, +2 and contract exclusion are directly asked Q10, so none is lost.','Q74 Q10'),
 ('Q76','Per-count numerical threat rate','What is counted and pre-placement timing remain asked Q76; generic per-object rate is a printed coefficient, not an added procedure. Related distinct conditional threshold/priority/movement cases remain Q71/Q72/Q74/Q75.','Q76 Q71 Q72 Q74 Q75')
]
write('demoted-context-coverage-review.json',[{'id':i,'demoted_context':c,'actual_coverage_and_novelty_decision':d,'actually_asked_ids':links.split(),'new_qualifying_additions':0} for i,c,d,links in demotions])

def rejection(name,refs,reason,source):
 return {'candidate':name,'actually_asked_ids':refs.split(),'decision':'reject as a further qualifying question','reason':reason,'controlling_source':source,'qualifying_additions':0}
first=[
 rejection('Alternate setup/demand/event instance vectors','Q01 Q15 Q19','The placement-from-list, low-slot fill, demand comparison/reset and ordered event resolution procedures are actually asked; other vectors are consultation.','RR p2 steps1–12; RR18/24/53/67'),
 rejection('Undealt Federalist or another named-rival/tie example','Q01 Q16 Q81','Allocation of the one unused card and strict win tests already determine these outcomes. No new rule-defined procedure.','RR28.3/50/69; LTPp15'),
 rejection('More action-deck depletion, hand checks or secret transfers','Q18 Q78 Q91','Entire-discard redistribution, own-turn-only check and secrecy are directly asked; new deck names or counts merely repeat them.','RR2.2/2.4/2.8/30.2; LTPp14'),
 rejection('Further failed placement/illness/Root variants','Q10 Q11 Q18 Q21 Q52','Failed attempts, capacity, default movement, Root reserve/+2 and one illness increment are actually asked. New quantities or routes do not supply a new exception.','RR10/31/32/35/36/39/42'),
 rejection('Ark Construction title and exact count','Q01 Q18 Q21 Q08','Ordinary development placement/capacity and production effect are already asked. No exceptional target/timing/branch on this native instruction.','Printed Ark Construction; RR19/40/48'),
 rejection('Gurren fixed payment and Bryan discard-to-theft combination','Q25 Q37 Q49 Q07','On-claim own-card discard-before-effect is asked in the claim/discard asset cases, and Bryan emergency-target/state exception is actually Q07. Different fixed payout or their mechanical combination adds no new procedure.','Printed Gurren Imashi, Bryan Stinson, Toshiyuki Sakai, Naoko Watanabe, Hernando Cortez; RR6/9/21.6'),
 rejection('Extra sector/table rows or retained reference questions','Q67 Q69 Q70','Demand gating, cap/total-supply formula, noncumulative bracket lookup and counted objects are actually asked. Remaining coefficients/table rows are consultation. Q68/Q73/Q76 stay frozen zero-novelty references.','Printed twelve investments; FAQ Investments'),
 rejection('Asset reveal read-aloud and component art/frame locations','Q04 Q17 Q60','Revealed faceup public asset and unit/token distinction are asked. Read-aloud presentation and matching frames/art locations add no consequential procedure.','LTPp10; RR40.4–40.5'),
 rejection('Vanity Project positive branch as another new addition','Q63 Q94','Q94 now expressly asks the previously missing beneficiary-linked mandatory follow-on and timing. Do not count its already accepted addition again.','Printed Vanity Project complete native cell; RR16.5'),
]
second=[rejection('Demoted '+i+' context',links,d,'See demoted-context-coverage-review.json; literal current question and printed/RR source') for i,c,d,links in demotions]
second += [
 rejection('Vanity Project chooser elaboration or general impossible-cost rule','Q04 Q94','Effect resolver is already established by Resolution and Q94 addresses resolver skipping the beneficiary-linked discard. A general feasibility, inter-clause trade or interrupt framework is not supplied by assigned text and is not inferred.','Printed Vanity Project; RR16.5; source-limits.json'),
 rejection('Rachel/Coach/Alex/Marco optionality header variants','Q03 Q14 Q27 Q42 Q45 Q47 Q89','End-of-Turn optional/once/owner-order is explicitly asked generally. Printed trigger and may/absence-of-may do not add a new procedure by changing an asset identity. Do not score unasked headers as omissions.','RR6.3–6.6/22; corresponding printed assets'),
 rejection('More zero/tie/threshold complementary branches','Q26 Q44 Q45 Q65 Q67 Q69 Q71 Q72 Q75','Equal-capital failure, zero-resource target exclusion, tied richest selection, collective threshold success/failure, unmet demand, table lower bounds and exclusive conditional branches are actually asked. Replacing the numbers supplies no distinct branch.','Printed Lily/Fumiko/Marco/Information Procurement/investments/events; FAQ Investments'),
 rejection('Other asset acquisition/same-time/newly gained/claim examples','Q13 Q14 Q24 Q37 Q41 Q42 Q49 Q85','Current questions directly ask owner order, active-clockwise multiowner order, readied/exhausted state, trade/steal/swap versus claim, first claim before second, and newly acquired end-turn use. New physical identities only recombine covered procedures.','RR6/9/22/26/56/61/65; FAQ Naoko'),
 rejection('Emergency subtype/return/flip/illness variants','Q07 Q12 Q50 Q58','All six native emergency procedures, target scope, later penalties, player-specific draws, illness exceptions, theft orientation and logo return states are actually asked. Recombining these with ordinary contracts/capacity adds no new issue.','Printed six emergencies and twelve corporation faces; RR11/21; FAQ Contracts'),
 rejection('Further event movement/count/rate cases','Q10 Q19 Q71 Q72 Q73 Q74 Q75 Q76 Q81','All sixteen native event procedures reduce to already asked exclusive conditions, threshold/count definitions, highest-first one/two movement instructions, normal Root handling and immediate ending before lower placements. Lower placement vectors and rates are consultation.','Printed sixteen events; RR24/25/35/36/63/64'),
 rejection('Claim publisher resolution of Arrest Orders or Chief revival/stack','Q30 Q31 Q60 Q79','Source supports the printed instructions and explicit Chief cancellation/status/no-refund/Fall Guy exception only. SG01 remains pending; no adopted priority/impossible-placement ruling and no categorical earlier-offer revival framework. This is a source limit, not a qualifying source-resolvable addition.','Printed Arrest Orders/Chief; LTPp12–13; RR15.8/35.4/42; FAQ Fall Guy')
]

source_map=read(candidate/'coverage-map.json')['current_complete_core_unit_map']
assert len(source_map)==69
byid={r['id']:r for r in scope['records']}
for row in source_map:
 row['validation']='Renewed independently against fresh complete RR delivery and current actual asked facts, including all demotion cautions; no contextual coverage credit.'
 row['actual_asked_evidence']=[{'id':i,'asked_facts':byid[i]['actual_asked_facts']} for i in row['actually_asked_question_ids']]

assets=[
 ('Aaron Marrón','Q28','Other-player proposal payment interception versus own payment/support cleanup'),
 ('Alex Westlund','Q42','In-play swap targets, self/Alex selection, owned-asset payment before exchange and no claim; amount consultation'),
 ('Bernice Mai','Q43','End-turn hand-card transfer, target, cap/per-card gain and emergency exclusion'),
 ('Braintrust','Q23','Double each draw entry, distinct General entries and reduced hand size'),
 ('Bryan Stinson','Q07 Q49','Emergency theft/state/participating-corporation exception Q07; common on-claim own-discard mechanism Q49, no recombination novelty'),
 ('Caprice Nisei','Q20 Q32','Optional exhaust at offer, binding exact declaration and Unorthodox exception'),
 ('Chief Gorman','Q31','Ordinary-hand counteroffer response, optional exhaust/payment, return/status/proposer restriction/no refund; limits preserved'),
 ('Coach Walden','Q47 Q89 Q14','Right-neighbor victory trigger, no exhaust; ordinary mandatory instruction is not a separate named-card procedure'),
 ('Eiko','Q29','Abstention response, exhaust, main support or capital loss'),
 ('Elizabeth Mills','Q40','Transfer first, user chooses recipient discard/draw and recipient topmost type'),
 ('The Fall Guy','Q30','Discard after own main, own counteroffer, immediate Support and Chief exclusion'),
 ('Floyd 2X3A7C','Q24','Claim draw versus owned hand increase and nonclaim trade'),
 ('Fumiko Yamamori','Q44','Nonzero resource eligibility and reduction for capital'),
 ('Gurren Imashi','Q25 Q37 Q49','Common on-claim discard for effect; fixed capital payment consultation, no exceptional procedure'),
 ('Hernando Cortez','Q49','On-claim own discard, alternative steal/capital, exhausted state and nonclaim'),
 ('Isabel McGuire','Q33 Q88','Start Support optional exhaust, deck top/either offer, no supporter status and Locust exception'),
 ('Jackson Howard','Q46','Asset reveal optional exhaust, another target, deal-win condition; fixed award consultation'),
 ('Lily Lockwell','Q26','Other-player start before Refresh, strict richer condition, random hand theft'),
 ('Locust Company','Q33 Q34','Start Support optional exhaust, hand-only counteroffer restriction, main and Isabel unaffected'),
 ('Marco Cubrero','Q45 Q14','Richest/tie alternative theft; End-of-Turn common optionality/timing already Q14'),
 ('Mark Yale','Q36','After proposed offer exhaust, proposer-only capital/asset trade restriction through deal end'),
 ('Midori','Q35','Resolution winner determination only on tie, exhaust and either winner'),
 ('Monica Singh','Q47 Q89','Active-player loss targets countering player, optional no exhaust'),
 ('Mr. Li','Q48','Any/self target, capital loss and mixed-type draw'),
 ('Mr. White','Q48','Another-player hand inspection and optional theft; End-of-Turn'),
 ('Naoko Watanabe','Q37','On-claim own discard, sequential top-two claims, first when-claimed effect before second'),
 ('Rachel Beckmann','Q27','End-each-deal zero-hand condition, optional topmost-type draw, emergencies outside hand; count consultation'),
 ('Saul Eustecio','Q47 Q89','Countering victory optional exhaust, user then active-player gain'),
 ('Sunny LeBeau','Q38','Per-instance threat trigger, topmost draw, optional no exhaust'),
 ('Susan Chen','Q41','Capital before transfer and newly acquired end-turn use'),
 ('Tanaka','Q35','Start Resolution optional discard, select active/countering winner without tie'),
 ('Thomas Haas','Q17 Q84','End-turn under-board inspection/optional own swap, facedown and open swap announcement, no cost'),
 ('Toshiyuki Sakai','Q25','On-claim discard, each-type draw and only-this-turn hand exemption'),
 ('Wong Ya Ching','Q39','Illness-effect threat trigger versus generic threat and capital gain')
]
actions=[
 ('Efficiency Experts','Q52','Android-free any destination, illness waiver versus normal effect'),
 ('High-Risk Investments','Q54','Three chosen recipients, order-linked grants, resolver not compulsory recipient'),
 ('Labor Solutions','Q51','Sequential up-to-three android movement then orgcrime, no illness waiver'),
 ('Liquidation','Q20 Q53 Q93','Strike/outage target exclusion, produce not exploit, ignore orgcrime/apply development/cap, then strike'),
 ('Media Circus','Q57','Unrest reduction then Human First'),
 ('24/7 Live Feeds','Q57 Q82','Orgcrime removal alternative; ordinary one-stage unrest operation already Q82'),
 ('Puff Piece','Q55','Per-player optional chosen type, winning-support branch, active-clockwise'),
 ('Spin Doctors','Q56 Q90','Up-to-two district unrest reductions, credit reduction versus explicit zero alternative'),
 ('Arrest Orders','Q60','Printed placement/removal and unit/token scope only; SG01 pending'),
 ('Full Deployment','Q58 Q07','Another-player target; resolver chooses draw/type or emergency flip'),
 ('Riot Control','Q59','Prisec removal, city-wide enemy removal then eligible unrest penalty; prisec not enemy'),
 ('Scorched Earth','Q60','Not-outage destination and chosen/another same-tier district enemy removal; no universal feasibility claim'),
 ('Ark Construction','Q01 Q18 Q21 Q08','Ordinary development placement/capacity/modifier; no exceptional branch; exact card count consultation'),
 ('Gentrification','Q61','Outage removal, conditional prisec placement, enemy movement/no removal contract'),
 ('Budget Renovations','Q62','Actual removed-outage districts receive subsequent unrest, cannot redirect'),
 ('Vanity Project','Q63 Q94','Support-dependent grant, assetless branch and positive mandatory beneficiary-linked discard after grant'),
 ('Clean Slate','Q64','Illness removal, outage target constrained to actual removal district, immunity'),
 ('Clinical Trials','Q64','Single illness removal and immunity'),
 ('Information Procurement','Q65','Voluntary contributions, player-count aggregate threshold, overpayment allowed; given active-clockwise order is common printed multi-player sequence'),
 ('Unorthodox Knowledge','Q20 Q66','Top-three secret fronts, one bottom/two top chosen order, Caprice exception')
]
event_groups=[
 ('Helium-3 Transport Threatened','Q71','Tier3 priority over tier2, no relevant tier no increase, upper before placement'),
 ('Human First Starts Riot / Beanstalk Beset by Protesters','Q72','Required tier condition versus highest-first one movement each'),
 ('Beanstalk Owned by Mob? / Pistoleros Hit Squads Strike!','Q73 Q10','Fixed tier condition versus movement, Root consequence asked Q10; Q73 zero novelty'),
 ('Activist Cells Awaken','Q74 Q10','Highest-first twice per unit subject to ordinary Root stopping/blocking; full ordinary result Q10'),
 ('Report: Record Unemployment / Average Wage Falls Again / Earthquake Rocks City','Q75','Distinct condition predicates/thresholds and no-effect complement'),
 ('Social Apps Spark Revolution / Welfare Programs Slashed','Q75','Protest-or-strike versus strike-only count'),
 ('Humanity Labor Hosts Union Heads / Gang Wars at All-Time High! / Tri-Maf Leaders Unite! / Crumbling Infrastructure / Rolling Outages Increase','Q76 Q19','Object counts before lower placements; rate and duplicate copies consultation, Q76 zero novelty')
]
write('source-map.json',{
 'candidate':'expanded-candidate-v10','authority':'Official2018 FAQ corrections; RR over LTP; original printed effects. Community module locates original images only.',
 'core_RR_units':source_map,'complete_setup':{'source':'RRp2 steps1–12','actually_asked_ids':['Q01','Q02'],'instance_vectors':'consultation'},
 'authority_question':'Q83','FAQ_every_bullet':read(own/'coverage-review.json')['FAQ_every_bullet'],
 'printed_assets':[{'printed_card':n,'actually_asked_ids':i.split(),'operative_procedure_or_rejection':d} for n,i,d in assets],
 'printed_actions':[{'printed_card':n,'actually_asked_ids':i.split(),'operative_procedure_or_rejection':d} for n,i,d in actions],
 'printed_event_procedure_families':[{'printed_cards':n,'actually_asked_ids':i.split(),'operative_procedure':d} for n,i,d in event_groups],
 'all_six_corporations_both_sides':{'actually_asked_ids':['Q01','Q02','Q12'],'procedure':'Player-count side, all draw vectors/order/General and all contract triggers, limits and exceptions; initial twelve individual original-detail native deliveries reused after unchanged hashes, both atlases freshly delivered.'},
 'all_six_emergencies':{'actually_asked_ids':['Q07','Q50'],'procedure':'Complete six effects in order plus offer/support/return/theft state; initial six full native faces reused after unchanged hashes, complete face atlas freshly delivered.'},
 'all_twelve_investments':{'actually_asked_procedure_ids':['Q15','Q67','Q69','Q70'],'reference_only':['Q68'],'procedure':'Demand gate, total supply/cap, noncumulative table alternatives, district/type counting; remaining coefficients consultation.'},
 'all94_question_source_links':[{'id':r['id'],'asked_facts':r['actual_asked_facts'],'source_refs':r['source_refs']} for r in scope['records']],
 'demoted_context_coverage':'demoted-context-coverage-review.json','scope_limit':'SG01 NOT_READY, not silently treated as covered by Q60 or ordinary movement questions.'
})

write('stopping-review.json',{
 'candidate':'expanded-candidate-v10','count_at_start':94,'counter_reset_after_Q94':0,
 'criterion':'Accept a distinct rule, rule-defined branch or consequential timing/priority/exception. Reject coefficients/vectors/duplicate copies/cosmetic identity changes and mechanical recombinations without a new issue. No unasked context credit.',
 'passes':[
  {'independent_review_pass':'V10-R1','after_acceptance':'Q94','method':'Broad forward source-to-asked-clause audit: complete RR setup and all69 glossary units reread, complete FAQ reread, LTP procedural pages6–15 refreshed; all94 current questions/asked facts freshly delivered. Full prior printed inspection reused after exact hashes, with fresh complete asset/action/event/investment atlas reviews and Q94 native cell.',
   'source_units_screened':['RR Complete Setup1–12','RR1–69','RR Golden Rules','all17 FAQ bullets','LTP procedural pages6–15','all12 corporation sides','all6 emergencies','all34 assets','all20 distinct actions','all12 investments','all16 event fronts','setup/demand/rival consultation boundaries'],
   'candidates_and_rejections':first,'new_qualifying_additions':0,'accepted_ids':[],'consecutive_zero_count_after_pass':1},
  {'independent_review_pass':'V10-R2','after_pass':'V10-R1','method':'Renewed reverse and adversarial branch/actor/timing audit across the same full source families: challenge exact asked clauses and all eight v7–v9 demotions, then positive/negative/zero/tie alternatives, payment-before-effect versus mandatory consequence, optional/exhaust/discard triggers, scope-limited exceptions, event priority and ordering. Reconsider core69/setup/FAQ against source-map rather than treating map labels as coverage.',
   'source_units_screened':['RR1–69 in actor/timing/condition/exception categories','complete setup and authority','all17 FAQ bullets','all printed procedure families in source-map.json','all94 actual asked records','eight demoted contexts'],
   'candidates_and_rejections':second,'new_qualifying_additions':0,'accepted_ids':[],'consecutive_zero_count_after_pass':2}
 ],
 'total_new_qualifying_additions_after_Q94':0,'consecutive_zero_addition_passes':2,
 'supported_current_bank_stopping_verdict':'SATURATED_WITHIN_SUPPORTED_SOURCE_RESOLVABLE_SCOPE',
 'SG01_complete_core_verdict':'NOT_READY','not_a_claim':'No publisher priority resolution, impossible-cost adoption, generic interrupt stack, reader result or complete-core approval is inferred.'
})

limits=read(own/'revision-05/source-limits.json')
write('source-limits.json',limits)
provenance=read(own/'revision-05/provenance.json')
write('provenance.json',{
 'initial_provenance_reused':provenance,'task':'/root/coverage_unexposed_signoff','revision':'revision-06',
 'requested_and_verified_actual_model':'gpt-6.1-sol','requested_and_verified_actual_effort':'high',
 'freshness':'Initially fresh unexposed source-only reviewer. This is a continuation after own Q93/Q94 findings and parent steering, not a newly blind reviewer.',
 'allowed_exposure':'Primary sources, permitted candidate JSON versions and own previous source-only artifacts only. Permitted candidate metadata mentions workflow/scope decisions; no summary body, reader answers, grades, other reviewer reports, collaboration/status/thread surface or web read.',
 'reuse':'347 exact prior manifest checks passed before use. Initial complete source text/native pixel/payload receipts explicitly reused, including all12 corporation sides and all6 emergency faces. Fresh runtime images separately recorded; no claim of repeating every individual native face.',
 'scope':'No repair authorship and no candidate/source edits. All saved changes only in own revision-06.',
 'technical_note':'One diagnostic query asked an absent id_validation field in own prior scope file and exited after showing its schema; actual validation uses ids_exactly_once and explicit94-id assertions. No source delivery or hash verification was lost.'
})

inputs=read(out/'input-hashes.json')
for r in inputs: assert sha(Path(r['path']))==r['sha256']
manifest=read(candidate/'input-manifest.json')['hashes']
for n,h in manifest.items():
 if n in [Path(r['path']).name for r in inputs]: assert sha(candidate/n)==h
for r in read(out/'reuse-hash-verification.json'): assert sha(Path(r['path']))==r['sha256']
receipts=[json.loads(s) for s in (out/'text-receipts.jsonl').read_text().splitlines()]
grouped=collections.defaultdict(list)
for r in receipts:
 p=Path(r['path']);s=p.read_text();assert sha(p)==r['file_sha256'];assert hashlib.sha256(s[r['start']:r['end_exclusive']].encode()).hexdigest()==r['chunk_utf8_sha256'];assert r['chunk_chars']<=5500 and r['no_truncation'];grouped[str(p)].append(r)
required=[out/(n+'-delta.json') for n in ['questions','answer-key','asked-clause-map','coverage-map','coverage-ledger','input-manifest']]+[candidate/'version-changes.json',out/'operative-asked-bank.json',Path('extracted/new-angeles-rules.txt').resolve(),Path('extracted/new-angeles-faq.txt').resolve()]
delivery=[]
for p in required:
 rs=sorted(grouped[str(p.resolve())],key=lambda r:r['start']);end=0
 for r in rs: assert r['start']==end;end=r['end_exclusive']
 assert end==len(p.read_text());delivery.append({'path':str(p.resolve()),'covered_chars':end,'complete':True})
write('receipt-validation.json',{'candidate7inputs_match':True,'manifest_matches_assigned_files':True,'all347_reuse_hash_checks_still_match':True,'all94_ids_once':True,'all_original93_records_unchanged':True,'Q94_exact_verbatim':True,'all_required_changed_semantic_data_delivered_completely':delivery,'all_text_chunks_max5500_actual_ranges_hashes_verified':True,'fresh_LTP_range':[14113,58113],'complete_LTP_reused_from_initial_receipts':True,'outer_cap_tokens':6500,'one_text_chunk_per_result':True,'native_receipts':'image-payload-receipts.json (fresh) plus unchanged original full native/image-lineage/full-pixel-equality receipts','reference_only_zero_novelty':['Q68','Q73','Q76']})

write('coverage-review.json',{
 'game':'New Angeles FFG2016 base4–6 BGG205716','candidate':'expanded-candidate-v10','review_complete':True,
 'supported_bank_saturation':{'verdict':'SATURATED_WITHIN_SUPPORTED_SOURCE_RESOLVABLE_SCOPE','current_question_count':94,'fixed_outcomes_source_supported':94,'material_false_source_claims':0,'Q94_verbatim_source_confirmed':True,'renewed_broad_passes_after_Q94':2,'new_qualifying_additions_per_pass':[0,0],'consecutive_zero_addition_passes':2,'additional_qualifying_source_resolvable_questions_found':0,'proposed_additions':[],'reference_only_zero_novelty':['Q68','Q73','Q76']},
 'complete_core_scope':{'verdict':'NOT_READY','essential_SG01':'Actual human/coordinator authority choice remains pending. No placement/removal priority or impossible-placement interpretation adopted. Q60 is supported printed instruction only.','SG03':'Explicit Chief cancellation/status/no-refund and Fall Guy bypass only; no general interrupt stack or categorical earlier-offer revival ruling.'},
 'findings':[],'history':'Preserves original v4 Q93 gap and v9 NOT_SATURATED/Q94 proposal unchanged. v10 accepts Q94; this review newly conducts two broad zero-addition passes after that reset.',
 'scope_review':'scope-review.json','all94_source_links_and_core_printed_map':'source-map.json','every_v9_demoted_context_delta':'demoted-context-coverage-review.json','two_pass_candidates_rejections_and_stopping':'stopping-review.json','source_limits':'source-limits.json','receipts':'receipt-validation.json','exact_inputs':'input-hashes.json','minimal_provenance':'provenance.json',
 'claim_limit':'Supported-current-bank stopping is distinct from complete-core readiness and from any reader/grader assessment. Unasked key context does not earn procedural coverage or omission caps.'
})

outputs=[]
for p in sorted(out.rglob('*')):
 if p.is_file() and p.name!='output-hashes.json':outputs.append({'path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':sha(p)})
write('output-hashes.json',outputs)
print(json.dumps({'candidate':'expanded-candidate-v10','ids':94,'renewed_passes':[0,0],'supported_bank':'SATURATED_WITHIN_SUPPORTED_SOURCE_RESOLVABLE_SCOPE','complete_core_SG01':'NOT_READY','review_sha256':sha(out/'coverage-review.json'),'output_manifest_sha256':sha(out/'output-hashes.json'),'inputs':inputs},indent=2))
