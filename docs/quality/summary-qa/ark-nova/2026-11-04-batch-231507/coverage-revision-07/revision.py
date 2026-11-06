import copy
import hashlib
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent;QA=HERE.parent;PRIOR=QA/'coverage-revision-06'
def read(path):return json.loads(path.read_text())
def write(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
FROZEN=['questions.json','answer-key.json','material-requested-facts.json','shared-source-lookup-facts.json','novelty-rejection-ledger.json']

if sys.argv[1]=='prepare':
    for name in FROZEN+['question-bank.md','answer-key.md']:
        (HERE/name).write_bytes((PRIOR/name).read_bytes())
    (HERE/'scope-qualifications-revision06.json').write_bytes((PRIOR/'scope-qualifications.json').read_bytes())
    prior_scope=read(PRIOR/'scope-qualifications.json')
    scope98={'qualification_id':'Q98-building-placement-context','affected_existing_id':'Q98',
        'old_key_and_material_object_unchanged':True,'source_accurate_extra_key_clause':'Place its unique building adjacent to at least 1 rock.',
        'literally_requested_by_old_prompt':False,
        'grading_scope':'The placement sentence is source-accurate context, not a requestedQ98grading part. Q98 requests Hunter reveal/select/discard, icon count and duplicate-icon sequential use. Keep its entire frozen key and material object unchanged.',
        'actual_requested_procedures':[{'question_ids':['Q98'],'procedure':'Hunter trigger/count, reveal/select/discard and duplicate-icon sequential use.'}],
        'shared_placement_procedure_question_ids':['Q35'],'shared_terrain_adjacency_question_ids':['Q31'],
        'named_source_context_without_new_credit':'Spotted Hyena Compound252 requires its unique building adjacent to at least1rock. This card identity and exact minimum remain source context/lookup, not a claim that Q35/Q31 ask this named threshold.',
        'source':'Glossary p7 Sponsor252 placement sentence','finding':'C07-P01'}
    scope99={'qualification_id':'Q99-building-placement-context','affected_existing_id':'Q99',
        'old_key_and_material_object_unchanged':True,'source_accurate_extra_key_clause':'Place its unique building',
        'literally_requested_by_old_prompt':False,
        'grading_scope':'Only the unique-building placement clause is source-accurate context, not a requestedQ99grading part. The following instruction to put3personal-supply tokens ON the card remains requested and required; token gain/spend, Sponsor play, immediate self-trigger, money cost and hand source remain requested. Keep the full frozen key and composite first material sentence unchanged.',
        'actual_requested_procedures':[{'question_ids':['Q99'],'procedure':'ThreeON-cardtokens, token gain/spend, Sponsor hand source/level cost, immediate self-trigger and limited uses.'}],
        'shared_placement_procedure_question_ids':['Q35'],
        'explicitly_requested_token_setup':'Put3player tokens from your personal supply on the Okapi Stable card, not on the unique building.',
        'source':'Glossary p7 Sponsor253 placement and token-setup sentences','finding':'C07-P01'}
    write('scope-qualifications.json',{'revision':'coverage-revision-07','scope':'External requested/context qualifications only; frozen bank objects unchanged.',
        'prior_Q20_qualification_preserved_exact':True,'prior_exact_file':'scope-qualifications-revision06.json',
        'qualifications':[prior_scope,scope98,scope99]})
    m=read(PRIOR/'coverage-map.json')
    for r in m['passages']:
        if r['passage_id']=='GSP.252':
            r['question_ids']=['Q31','Q35','Q98']
            r['clause_coverage']=[
                {'clause':'Hunter trigger, count, reveal/select/discard and sequential double-icon use','question_ids':['Q98'],'classification':'actually_requested'},
                {'clause':'General unique-building placement procedure','question_ids':['Q35'],'classification':'shared_procedure_only'},
                {'clause':'Meaning of required terrain adjacency','question_ids':['Q31'],'classification':'shared_procedure_only'},
                {'clause':'Named Sponsor252 building adjacent to at least1rock','question_ids':[],'classification':'source_accurate_named_context_lookup_not_a_Q98grading_part_or_new_credit'}]
            r['requested_context_caution']='Q98 asks Hunter/icon handling, not placement. Q35 supplies general unique-building placement and Q31 terrain-adjacency procedure; neither is claimed to ask the named Sponsor252 minimum1rock. Preserve the named sentence as context in the frozen key/facts and external scope qualification.'
            r['scope_qualification']='scope-qualifications.json: Q98-building-placement-context'
        if r['passage_id']=='GSP.253':
            r['question_ids']=['Q35','Q99']
            r['clause_coverage']=[
                {'clause':'General unique-building placement procedure','question_ids':['Q35'],'classification':'shared_procedure_only_and_contextual_for_Q99'},
                {'clause':'Place3personal-supply tokens ON the Sponsor card','question_ids':['Q99'],'classification':'actually_requested_token_setup'},
                {'clause':'Token gain/spend, Sponsor from hand for level-cost money, immediate self-trigger and limited uses','question_ids':['Q99'],'classification':'actually_requested'}]
            r['requested_context_caution']='Only Place its unique building is unrequestedQ99context. The three-token ON-card setup remains requested. Q35 covers general placement procedure; it is not claimed to request the named Okapi Stable effect. Frozen key/facts remain exact.'
            r['scope_qualification']='scope-qualifications.json: Q99-building-placement-context'
    # Inherited metadata remains exact; this manifest identifies the narrow revision07 delta.
    write('coverage-map.json',m)
    print('Prepared only externalQ98/Q99scope qualifications and two clause-level map records; frozen bank files unchanged. Terminal passes pending.')
    sys.exit(0)

assert sys.argv[1]=='seal'
q=read(HERE/'questions.json')['questions'];a=read(HERE/'answer-key.json')['answers'];f=read(HERE/'material-requested-facts.json')
lookups=read(HERE/'shared-source-lookup-facts.json');ledger=read(HERE/'novelty-rejection-ledger.json')
m=read(HERE/'coverage-map.json');m0=read(PRIOR/'coverage-map.json');scope=read(HERE/'scope-qualifications.json')
active={r['id'] for r in q}
assert len(q)==len(a)==len(f)==len(active)==95
assert len(m['passages'])==233 and len(lookups)==42
assert m['shared_source_lookup_facts']==lookups
checks={}
for name in FROZEN+['question-bank.md','answer-key.md']:
    assert (HERE/name).read_bytes()==(PRIOR/name).read_bytes()
    checks[name]={'old_sha256':sha(PRIOR/name),'current_sha256':sha(HERE/name),'bytes_identical':True}
assert scope['qualifications'][0]==read(PRIOR/'scope-qualifications.json')
assert (HERE/'scope-qualifications-revision06.json').read_bytes()==(PRIOR/'scope-qualifications.json').read_bytes()
assert len(scope['qualifications'])==3
assert q[:94]==read(QA/'coverage-revision-05/questions.json')['questions']
assert a[:94]==read(QA/'coverage-revision-05/answer-key.json')['answers']
assert {x:r for x,r in f.items() if x!='Q141'}==read(QA/'coverage-revision-05/material-requested-facts.json')
assert q[:20]==read(QA/'benchmark-v1.2/questions.json')['questions']
assert a[:20]==read(QA/'benchmark-v1.2/answer-key.json')['answers']
assert ledger==read(PRIOR/'novelty-rejection-ledger.json')
changed=[]
assert {k:v for k,v in m.items() if k!='passages'}=={k:v for k,v in m0.items() if k!='passages'}
for r,s in zip(m['passages'],m0['passages']):
    assert r['passage_id']==s['passage_id']
    if r!=s:
        assert r['passage_id'] in ['GSP.252','GSP.253']
        assert {k:v for k,v in r.items() if k not in ['question_ids','clause_coverage','requested_context_caution','scope_qualification']}=={k:v for k,v in s.items() if k!='question_ids'}
        changed.append({'passage_id':r['passage_id'],'old_question_ids':s['question_ids'],'new_question_ids':r['question_ids'],'new_clause_coverage':r['clause_coverage']})
assert len(changed)==2
edge_keys={'question_ids','covered_by','procedure_covered_by','procedure_covered_by_active_ids','active_procedure_covering_ids','policy_question_ids','permission_question_ids',
    'actual_requested_coverage','shared_placement_procedure_question_ids','shared_terrain_adjacency_question_ids'}
lookup_ids={r.get('lookup_id',r.get('id')) for r in lookups};edge_count=0;lookup_count=0
def edges(obj):
    global edge_count,lookup_count
    if isinstance(obj,list):
        for v in obj:edges(v)
    elif isinstance(obj,dict):
        for k,v in obj.items():
            if k in edge_keys and isinstance(v,list):assert set(v)<=active,(k,v);edge_count+=len(v)
            elif k=='lookup_fact_ids':assert set(v)<=lookup_ids;lookup_count+=len(v)
            else:edges(v)
edges(m);edges(scope)
assert active<={x for r in m['passages'] for x in r['question_ids']}
assert len(ledger['accepted_candidates'])==75 and len(ledger['all_rejected_historical_ids'])==46
write('frozen-bank-byte-preservation.json',{'files':checks,'all95question_key_material_objects_exact':True,
    'all42lookup_objects_and_bytes_exact':True,'old94prefix_identity_to_revision05_exact':True,
    'Q20_qualification_object_exact':True,'Q20_prior_scope_file_bytes_exact':True,'Q99_three_ON_card_tokens_remain_requested':True})

immut=read(PRIOR/'prior-artifact-immutability-check.json');count=0
for folder,items in immut.items():
    for name,rec in items.items():assert sha(QA/folder/name)==rec['sealed_sha256'];count+=1
immut['coverage-revision-06']={}
for name,digest in read(PRIOR/'artifact-hashes.json').items():
    observed=sha(PRIOR/name);assert observed==digest
    immut['coverage-revision-06'][name]={'sealed_sha256':digest,'observed_sha256':observed,'unchanged':True};count+=1
assert sha(PRIOR/'sealed-manifest.json')=='13cd9ab0ed178155ee2dc3b1acc103253a65a27e0ec9ac6a5c3d7da650c6aff7'
write('prior-artifact-immutability-check.json',immut)
report=read(QA/'coverage-challenge-07/report.json')
assert report['counts']['new_distinct_procedural_gaps']==report['counts']['source_key_contradictions']==report['counts']['remaining_novelty_inflation']==0
write('precision-resolution.json',{'finding':'C07-P01','source_report':'../coverage-challenge-07/report.json','report_sha256':sha(QA/'coverage-challenge-07/report.json'),
    'external_context_qualifications_added':['Q98-building-placement-context','Q99-building-placement-context'],
    'Q20_qualification_preserved_exact':True,'frozen_true_key_and_material_objects_unchanged':True,
    'requested_Q99_token_setup_retained':'Put3personal-supply tokens ON the card.',
    'source_context_without_new_credit':'Sponsor252 exact minimum1rock remains in frozen source facts and explicit external context; general placement mapsQ35, terrain-adjacency procedureQ31.',
    'exact_changed_map_records':changed,'all_other_map_content_exact':True,
    'review_basis':'Same reviewer07 finite delta and exact bank-identity check after the completed full95 substantive source-first review; no new fresh-context full review claimed.'})
passes=[{'pass':1,'new_question_additions':0,'map_records_checked':233,'final_map_complete_before_pass':True,
    'target':'Whole final source-to-prompt map sweep after two per-clause placement/context repairs; use unchanged full33-page inventory and reread Glossaryp7 Sponsor252/253.',
    'result':'No distinct gap. Q98Hunter andQ99token/Sponsorhandling retain actual requests; placement is sharedQ35procedure, rock-adjacency meaning sharedQ31, named minimum source context only. Q99threeON-cardtokens remain asked.'},
    {'pass':2,'new_question_additions':0,'map_records_checked':233,'final_map_complete_before_pass':True,
    'target':'Reverse complete233-record map/95prompt/42lookup check, exact unchanged bank and old94prefix identity, priorQ20qualification and no-dead destinations.',
    'result':'Zero additions. All existing branch/lookup evidence retained, no novelty or definition change, context classification external only; no further source-to-actual-prompt omission identified.'}]
write('terminal-author-passes.json',{'terminal_zero_addition_passes':2,'passes':passes,'map_sha256':sha(HERE/'coverage-map.json'),
    'all_passage_ids_checked':[r['passage_id'] for r in m['passages']],
    'unchanged_raw_source_inventory':'../coverage-revision-06/source-reading-report.json; packet1898splitlines/1897LF unchanged',
    'ledger_preservation':'Frozen novelty ledger copied byte for byte; new revision07 terminal author passes recorded externally.'})
validation={'status':'pass','active_questions':95,'highest_historical_id':'Q141','source_passage_records':233,'lookup_records':42,'historical_retired_ids':46,
    'new_question_or_retirement_changes':0,'changed_map_records':['GSP.252','GSP.253'],'all_other_map_content_exact':True,
    'five_bank_json_files_byte_identical':True,'readable_banks_byte_identical':True,'all95question_key_material_objects_exact':True,
    'old94prefix_identity_preserved':True,'original20Q_key_exact_benchmark_v1_2':True,'all42lookups_bytes_exact':True,
    'prior_Q20_scope_qualification_exact':True,'prior_Q20_scope_file_bytes_preserved':True,'Q98_placement_context_external_only':True,
    'Q99_only_placement_prefix_context_external':True,'Q99_three_ON_card_tokens_requested':True,
    'live_map_and_scope_question_edges_checked':edge_count,'lookup_edges_checked':lookup_count,'no_dead_destinations':True,
    'all95active_ids_retain_map_coverage':True,'prior_sealed_artifacts_unchanged':count,'revision06_manifest_unchanged':True,
    'terminal_author_zero_addition_passes':2,'independent_status':'Full95substantive challenge07 supplies basis; same reviewer07 precise repaired delta/identity acceptance pending.'}
write('validation-report.json',validation)
inputs=[]
for path in [QA/'coverage-challenge-07/report.json',PRIOR/'sealed-manifest.json',PRIOR/'scope-qualifications.json']+[PRIOR/name for name in FROZEN+['coverage-map.json']]:
    inputs.append({'path':str(path.relative_to(QA)),'sha256':sha(path)})
write('input-provenance.json',{'revision':'coverage-revision-07','inputs':inputs,
    'scope':'Source-only context precision; no canonical summary, reader outputs, grades or repair history read. All95bank objects/42lookups and novelty ledger unchanged.',
    'primary_targeted_reread':'Complete Glossaryp7 Sponsor252 and253 source paragraphs including distinct placement, Hunter effect,3ON-cardtokens and token-funded Sponsor play.',
    'unchanged_source_inventory':'Complete original English basev1.2 packet33PDFpages,1898splitlines/1897LF including unterminated footer3; original publisher photos numeric-only; solo/MW/strategy guide and unsupplied text excluded.',
    'review_scope':'Same reviewer07 exact finite delta check, not a new fresh-context substantive review.'})
(HERE/'coverage-report.md').write_text('''# Ark Nova context precision revision07

All95 question/key/material-fact objects,42lookup objects and bytes, the novelty ledger and both readable banks are byte-identical to revision06. Counts remain95/233/42, stable IDs throughQ141 and46 historical retirements. No question, rule definition, correction, novelty decision or retirement changes. All earlier seals remain unchanged.

The sole independent finding C07-P01 is resolved with two external scope qualifications and two clause-level sponsor-map notes. Q98's accurate sentence placing its unique building adjacent to at least1rock is unrequested context; the actual question asks Hunter/icon handling. General unique-building placement maps toQ35 and terrain-adjacency procedure toQ31. Neither prompt is claimed to ask this named Sponsor252 threshold; the exact named minimum remains source context without new credit. Q99's accurate Place its unique building prefix is likewise context. Its following three personal-supply tokens ON the card remain requested, along with token spending, Sponsor hand source, money cost and immediate self-trigger. No frozen true key or composite material sentence is edited.

The new scope-qualifications.json wraps three qualification entries. The existing Q20 fallback entry is retained as an exactly equal object, and its old file bytes are separately preserved as scope-qualifications-revision06.json. The new Q98/Q99 entries guide requested grading scope externally. GSP.252 andGSP.253 now assign each procedure/context clause separately; their top-level ID union is not a claim that each prompt requests every clause. All other map content is exact prior content, including inherited metadata and embedded42lookup objects. This directory and manifest identify revision07.

The unchanged full primary inventory is reused, and the complete Glossaryp7 Sponsor252/253 paragraphs were reread. Two terminal whole-map author passes after the precision repair found zero additions and validated all233records,95actual prompts,42lookups, old94prefix identity and live destinations. The frozen novelty ledger is unchanged; these new author passes are recorded separately.

Fresh reviewer07's completed full95source-first substantive review found no distinct procedural gap, contradiction or novelty inflation, with this one scope precision finding. The same reviewer will check only this repaired delta and exact bank identity. This author does not claim a new fresh-context full review or the pending independent delta acceptance. No summary, readers or grades were read.
''')
(HERE/'author-prompt-provenance.md').write_text('''# Coordinator task — revision07

> Fresh07FINAL report.json ready, C07-P01 only; no distinctgaps/sourcecontradictions/noveltyinflation. PleasecompleteSMALLnewcoverage-revision-07 preservingALL95question/key/materialfactobjects and42lookupbytes EXACT; alloldsealsunchanged. ApplyexternalcontextqualificationsforQ98rock-buildingplacement andQ99unique-buildingplacement ONLY (Q99threeON-cardtokensisasked). RetainQ20fallbackqualificationexact. Nevereditoldtruekey/materialobjects to'remove'context. MapGSP.252/.253 clause-leveldistinction: Q98HuntervsQ99token/Sponsoractualaskedparts; placementsharedprocedureQ35, rockadjacencyQ31; namedrockvalueisretainedsourcecontext/lookup, notnovelcredit. Addclear per-clausecoverage notes/edges soaddingQ35/Q31doesn'tclaimallpromptsaskeveryclause. Newscopequal file maywrap3qualifications; preservepriorQ20entryandoldfileversion. Complete all95/233/42 integrity/no-dead-ID/prefix94preservation and2terminalwholemapzero-additionpassesafterprecisionfix; nodefinition/newquestion/retirementchanges. Recordfiniteexactdelta+hashseal/readablebanks unchanged ifsamebytes. Source07sameindependentreviewerwillcheckrepaireddelta+exactbankidentity; no newfreshfullcontextclaim. Reportpaths/hasheswhenready. Remainsource-only no summary/readers/grades.
''')
hashes={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name not in {'artifact-hashes.json','sealed-manifest.json'}}
write('artifact-hashes.json',hashes)
core=FROZEN+['coverage-map.json','scope-qualifications.json','scope-qualifications-revision06.json','validation-report.json']
write('sealed-manifest.json',{'status':'sealed_context_precision_delta_for_same_reviewer07_check','revision':'coverage-revision-07',
    'active_question_count':95,'highest_historical_id':'Q141','source_passage_records':233,'lookup_records':42,'historical_retired_count':46,
    'new_question_ids':[],'new_retired_ids':[],'all95bank_objects_exact':True,'lookup_file_bytes_exact':True,'novelty_ledger_bytes_exact':True,
    'changed_map_records':['GSP.252','GSP.253'],'new_external_context_qualifications':['Q98','Q99'],'Q20_qualification_object_and_old_bytes_exact':True,
    'terminal_author_zero_addition_passes':2,'independent_delta_acceptance':'pending same reviewer07; prior full95substantive review supplies basis',
    'core_sha256':{x:hashes[x] for x in core},'all_artifact_hashes_sha256':sha(HERE/'artifact-hashes.json')})
print(json.dumps({'validation':validation,'sealed_manifest_sha256':sha(HERE/'sealed-manifest.json'),'core_sha256':{x:hashes[x] for x in core}},indent=2))
