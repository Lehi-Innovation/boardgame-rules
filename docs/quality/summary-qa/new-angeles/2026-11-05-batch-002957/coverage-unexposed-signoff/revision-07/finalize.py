from pathlib import Path
import json, hashlib, collections

out=Path(__file__).parent
own=out.parent
base=own.parent
old=base/'expanded-candidate-v10'
new=base/'expanded-candidate-v11'
prev=own/'revision-06'
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d): (out/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
q0,q1=(read(p/'questions.json')['questions'] for p in (old,new))
k0,k1=(read(p/'answer-key.json')['answers'] for p in (old,new))
a0,a1=(read(p/'asked-clause-map.json') for p in (old,new))
ids=[f'Q{i:02}' for i in range(1,95)]
assert [r['id'] for r in q1]==[r['id'] for r in k1]==[r['id'] for r in a1]==ids
assert q0==q1
assert all(x['expected_answer']==y['expected_answer'] for x,y in zip(k0,k1))
assert [x['id'] for x,y in zip(k0,k1) if x!=y]==['Q87']
assert [x['id'] for x,y in zip(a0,a1) if x!=y]==['Q87']
assert k0[-1]==k1[-1] and a0[-1]==a1[-1]
for r in read(out/'reuse-hash-verification.json'): assert sha(Path(r['path']))==r['sha256']
inputs=read(out/'input-hashes.json')
for r in inputs: assert sha(Path(r['path']))==r['sha256']
for n,h in read(new/'input-manifest.json')['hashes'].items():
 if n in [Path(r['path']).name for r in inputs]: assert sha(new/n)==h

coverage={
 'changed_id':'Q87','source':'RR20/64/64.1–64.2, unchanged authoritative text and printed event/action native evidence reused after hashes',
 'literal_question':q1[86]['question'],'actual_asked_facts':a1[86]['asked_facts'],'contextual_background':a1[86]['contextual_background'],
 'source_verdict':'supported','scope_verdict':'The question asks tier identification and absence of inherent production/threat effects. Printed-card references are a correct explanation, not an additional independently asked fact.',
 'lost_procedural_coverage':False,'distinct_qualifying_additions':0,
 'actual_coverage_elsewhere':[
  {'id':'Q71','asked_facts':a1[70]['asked_facts'],'procedure':'Explicit tier3-over-tier2 conditional priority, tier1-only no upper effect, and upper check before placements.'},
  {'id':'Q72','asked_facts':a1[71]['asked_facts'],'procedure':'Explicit required-tier Human First condition and absent-tier alternative movement branch/order.'},
  {'id':'Q60','asked_facts':[a1[59]['asked_facts'][2]],'procedure':'Scorched Earth same-tier target geography, independently asked; no SG01 ruling inferred.'}
 ],
 'locator_precision_advisory':{'candidate_field':'coverage-map.json Q87_context_normalization.card_tier_conditions_actively_asked_elsewhere','overbroad_id':'Q75','explanation':'Q75 asks component/state thresholds and counts, not a tier condition. Do not count Q75 as actual tier-condition coverage. Q71/Q72 directly cover the relevant procedure and Q60 directly covers same-tier targeting, so this overbroad locator introduces no source or procedural gap.'},
 'stopping_impact':'No changed question, fixed outcome, rule procedure, novelty issue or operative coverage. Reuse the two v10 broad zero-addition passes without claiming new passes or increasing count.'
}
write('q87-source-coverage-review.json',coverage)

scope=read(prev/'scope-review.json')
scope['candidate']='expanded-candidate-v11'
scope['qualification']='All94 fixed outcomes remain unchanged and source-supported. Q87 scope now asks only identification/no inherent effect; explicit printed tier procedures are actually asked Q71/Q72/Q60. Complete-core SG01 remains NOT_READY.'
for i,r in enumerate(scope['records']):
 assert r['id']==ids[i]
 r['candidate']='expanded-candidate-v11'
 r['actual_asked_facts']=a1[i]['asked_facts']
 r['scenario_givens']=a1[i].get('scenario_givens',[])
 r['contextual_background']=a1[i].get('contextual_background',[])
 r['recheck_basis']='Exact v10-to-v11 structural comparison: all94 question entries and expected answers unchanged; only Q87 required/context metadata changed. Prior complete source/native and all94 review reused after352 unchanged manifest checks. Q87 focused scope and actual-coverage review in q87-source-coverage-review.json.'
scope['records'][86]['versioned_source_confirmation']={'verdict':'confirmed','evidence':'RR20/64 bar-count identification and RR64.1 no inherent tier effect. RR64.2/printed tier-dependent procedures remain actually asked Q71/Q72; same-tier action scope Q60. Do not credit Q75 as tier-specific.'}
scope['delta_confirmation']={'all94_question_entries_exactly_unchanged':True,'all94_expected_answers_exactly_unchanged':True,'only_changed_key_record':'Q87 required/context','only_changed_clause_record':'Q87 asked/context','Q94_exactly_unchanged':True,'all94_ids_once':True}
assert len(scope['records'])==94 and len(set(r['id'] for r in scope['records']))==94
write('scope-review.json',scope)

source_map=read(prev/'source-map.json')
source_map['candidate']='expanded-candidate-v11'
byid={r['id']:r for r in scope['records']}
for r in source_map['all94_question_source_links']:
 r['asked_facts']=byid[r['id']]['actual_asked_facts']
for r in source_map['core_RR_units']:
 r['actual_asked_evidence']=[{'id':i,'asked_facts':byid[i]['actual_asked_facts']} for i in r['actually_asked_question_ids']]
 if r['source_unit']=='RR64':
  r['actually_asked_question_ids']=['Q60','Q71','Q72','Q87']
  r['operative_procedure']='Tier bar-count identification/no inherent effect Q87; printed tier-dependent conditions/priority/alternative branches Q71/Q72; same-tier action geography Q60. Q75 is not tier-specific.'
  r['actual_asked_evidence']=[{'id':i,'asked_facts':byid[i]['actual_asked_facts']} for i in r['actually_asked_question_ids']]
source_map['Q87_normalization']='q87-source-coverage-review.json'
source_map['reuse']='All other source-unit/procedure links carried from exact hash-verified v10 whole-bank review; no unasked Q87 context credit.'
write('source-map.json',source_map)

stopping=read(prev/'stopping-review.json')
write('stopping-review.json',{
 'candidate':'expanded-candidate-v11','current_question_count':94,
 'reused_review':str((prev/'stopping-review.json').resolve()),'reused_review_sha256':sha(prev/'stopping-review.json'),
 'previous_exact_v10_results':[p['new_qualifying_additions'] for p in stopping['passes']],
 'consecutive_zero_addition_passes':2,'new_broad_passes_claimed_in_this_delta_review':0,
 'delta_challenge':'Q87 context demotion reviewed against literal scope and actually asked printed procedures; no lost coverage or new source-resolvable branch.',
 'new_qualifying_additions_in_delta_review':0,'counter_reset_required':False,
 'verdict':'SATURATED_WITHIN_SUPPORTED_SOURCE_RESOLVABLE_SCOPE','essential_SG01_complete_core_verdict':'NOT_READY',
 'limits':'Current supported bank only; no unqualified complete-core readiness, SG01 interpretation, general impossible-cost or stack/revival ruling.'
})
write('source-limits.json',read(prev/'source-limits.json'))

rs=[json.loads(s) for s in (out/'text-receipts.jsonl').read_text().splitlines()]
groups=collections.defaultdict(list)
for r in rs:
 p=Path(r['path']);s=p.read_text();assert sha(p)==r['file_sha256'];assert hashlib.sha256(s[r['start']:r['end_exclusive']].encode()).hexdigest()==r['chunk_utf8_sha256'];assert r['chunk_chars']<=5500 and r['no_truncation'];groups[r['path']].append(r)
required=[out/(n+'-delta.json') for n in ['questions','answer-key','asked-clause-map','coverage-map','coverage-ledger','input-manifest']]+[new/'version-changes.json',out/'q87-operative-coverage-evidence.json']
delivered=[]
for p in required:
 end=0
 for r in sorted(groups[str(p.resolve())],key=lambda r:r['start']):assert r['start']==end;end=r['end_exclusive']
 assert end==len(p.read_text());delivered.append({'path':str(p.resolve()),'complete_semantic_changed_data_or_focused_evidence':True,'covered_chars':end})
write('receipt-validation.json',{
 'all352_prior_hash_checks_match':True,'all7_final_inputs_and_assigned_manifest_hashes_match':True,
 'all94_question_entries_and_expected_answers_exactly_equal_v10':True,'only_Q87_scope_record_changed':True,'Q94_exactly_preserved':True,
 'all94_scope_records_exactly_once':True,'complete_changed_semantic_delivery':delivered,
 'text_delivery':'One contiguous <=5500-character chunk per result, outer cap6500, exact ranges/chunk/file hashes/end marker; unchanged content reused from complete previous deliveries.',
 'authorities_and_native_reuse':{'complete_source_text':str((own/'text-receipts.jsonl').resolve()),'native_payload_receipts':str((own/'image-payload-receipts.json').resolve()),'fresh_v10_payload_receipts':str((prev/'image-payload-receipts.json').resolve()),'full_pixel_equality':str((own/'full-pixel-equality.json').resolve()),'lineage':str((own/'image-lineage.json').resolve()),'all_required_corporation_sides_and_emergency_faces':'Original complete native deliveries reused only after unchanged source/crop/receipt hashes; no new image delivery claimed.'},
 'new_technical_deviation':None
})
write('provenance.json',{
 'task':'/root/coverage_unexposed_signoff','revision':'revision-07','requested_and_verified_actual_model':'gpt-6.1-sol','requested_and_verified_actual_effort':'high',
 'verified_initial_provenance':str((own/'provenance.json').resolve()),'verified_v10_provenance':str((prev/'provenance.json').resolve()),'verified_v10_provenance_sha256':sha(prev/'provenance.json'),
 'freshness':'Continuation of initially fresh independent source-only review; no claim of a newly blind review after own Q93/Q94 proposals and parent steering.',
 'exposure':'Permitted primary sources, seven v11 candidate JSON files, exact v10 inputs and own source-only artifacts. No optional other-validator report opened. No summary, reader answers, grades, parent QA artifacts, collaboration/status/thread surfaces or web read. Candidate metadata mentioning workflow history was permitted data, not evidence of outcomes.',
 'reuse':'352 exact prior hashes verified before reuse and again at finalization; unchanged complete authorities/native proof and full94 v10 review/two broad passes reused explicitly.',
 'authorship':'No candidate/source repair or edits; writes only own revision-07.'
})
write('coverage-review.json',{
 'game':'New Angeles FFG2016 base4–6 BGG205716','candidate':'expanded-candidate-v11','review_complete':True,
 'supported_bank_saturation':{'verdict':'SATURATED_WITHIN_SUPPORTED_SOURCE_RESOLVABLE_SCOPE','fixed_outcomes_source_supported':94,'actual_asked_scope_records_validated_once':94,'material_false_source_key_claims':0,'all94_question_entries_and_expected_answers_unchanged':True,'Q94_exactly_preserved':True,'new_qualifying_source_resolvable_additions_from_delta':0,'reused_v10_broad_pass_additions':[0,0],'consecutive_zero_addition_passes':2,'new_broad_passes_claimed':0,'reference_only_zero_novelty':['Q68','Q73','Q76']},
 'complete_core_scope':{'verdict':'NOT_READY','SG01':'Essential human/coordinator authority choice pending. No proposed placement/removal priority or impossible-placement interpretation adopted; supported printed Q60 does not resolve it.','SG03':'Explicit cancellation/status/no-refund and Fall Guy bypass only. No generic interrupt stack or categorical earlier-offer revival ruling.'},
 'Q87_delta':{'verdict':'source/scope-supported; no procedural coverage lost','actual_coverage_elsewhere':['Q71','Q72','Q60'],'report':'q87-source-coverage-review.json'},
 'findings':[{'severity':'nonblocking locator precision advisory','field':'coverage-map.json Q87_context_normalization.card_tier_conditions_actively_asked_elsewhere','detail':'Q75 is not tier-specific; rely on directly asked Q71/Q72 and same-tier targeting Q60. No key outcome or procedural coverage gap.'}],
 'scope_review':'scope-review.json','source_map':'source-map.json','stopping_review':'stopping-review.json','source_limits':'source-limits.json','receipts':'receipt-validation.json','exact_inputs':'input-hashes.json','provenance':'provenance.json',
 'history':'All prior v9 NOT_SATURATED/Q94 proposal and v10 whole94/two-zero reports preserved unchanged. No frozen candidate edits.'
})
for r in inputs: assert sha(Path(r['path']))==r['sha256']
outputs=[{'path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(out.rglob('*')) if p.is_file() and p.name!='output-hashes.json']
write('output-hashes.json',outputs)
print(json.dumps({'candidate':'expanded-candidate-v11','outcomes':94,'new_qualifying_additions':0,'reused_two_broad_passes':[0,0],'supported_bank':'SATURATED_WITHIN_SUPPORTED_SOURCE_RESOLVABLE_SCOPE','complete_core_SG01':'NOT_READY','nonblocking_locator':'Q75 is not tier-specific; Q71/Q72/Q60 provide actual coverage','review_sha256':sha(out/'coverage-review.json'),'output_manifest_sha256':sha(out/'output-hashes.json'),'inputs':inputs},indent=2))
