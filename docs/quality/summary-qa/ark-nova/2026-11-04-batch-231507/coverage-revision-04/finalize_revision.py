import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
QA = HERE.parent
PRIOR = QA/'coverage-revision-03'
BASE = QA/'benchmark-v1.2'
def read(path): return json.loads(path.read_text())
def write(name,value): (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

q = read(HERE/'questions.json')['questions']; a = read(HERE/'answer-key.json')['answers']
f = read(HERE/'material-requested-facts.json'); m = read(HERE/'coverage-map.json')
q0 = read(PRIOR/'questions.json')['questions']; a0 = read(PRIOR/'answer-key.json')['answers']
f0 = read(PRIOR/'material-requested-facts.json'); m0 = read(PRIOR/'coverage-map.json')
qd = {r['id']:r for r in q}; ad = {r['id']:r for r in a}
oqd = {r['id']:r for r in q0}; oad = {r['id']:r for r in a0}
active = set(qd)
assert len(q) == len(a) == len(f) == len(active) == 94
assert [r['id'] for r in q] == [r['id'] for r in a]
assert active == set(oqd)-{'Q47'} == set(f)
assert all(qd[x]==oqd[x] for x in active)
assert all(ad[x]==oad[x] for x in active-{'Q116','Q133'})
assert all(f[x]==f0[x] for x in active-{'Q07','Q116','Q133'})
assert q[:20] == read(BASE/'questions.json')['questions']
assert a[:20] == read(BASE/'answer-key.json')['answers']
for x,name in [('Q133','source-key-correction-SC03.json'),('Q116','source-key-precision-SC04.json')]:
    correction = read(QA/name)
    assert ad[x] == correction['corrected_entry']
    assert oad[x] == correction['old_entry']
    assert f[x]['material_requested_facts'] == correction['corrected_entry']['material_requested_facts']
assert ad['Q07'] == oad['Q07']
assert 'Track bonuses immediate once.' not in ' '.join(f['Q07']['material_requested_facts'])
assert f['Q07']['contextual_source_facts_not_requested'] == ['Track bonuses immediate once.']
assert len(m['passages']) == 232
assert [r['passage_id'] for r in m['passages']] == [r['passage_id'] for r in m0['passages']]
assert active <= {x for r in m['passages'] for x in r['question_ids']}

lookups = read(HERE/'shared-source-lookup-facts.json')
assert m['shared_source_lookup_facts'] == lookups
assert len(lookups) == 42
assert lookups[:41] == read(PRIOR/'shared-source-lookup-facts.json')
lookup_ids = {r.get('lookup_id',r.get('id')) for r in lookups}
assert len(lookup_ids) == 42
byid = {r['passage_id']:r for r in m['passages']}
assert byid['GSP.255']['lookup_fact_ids'] == byid['GSP.256']['lookup_fact_ids'] == ['lookup255_256']
assert 'lookup_uni3' in byid['M06d']['lookup_fact_ids']
assert 'Q138 immediate capped aggregate' not in byid['M12c']['novelty_credit']
assert 'one whole payoff-table question' not in byid['M18d']['revision_note']
assert 'not a numerical permutation' not in byid['M02g']['revision_note']
edge_keys = {'question_ids','covered_by','procedure_covered_by','procedure_covered_by_active_ids',
    'active_procedure_covering_ids','policy_question_ids','permission_question_ids'}
edge_count = 0; lookup_edge_count = 0
def edges(obj):
    global edge_count,lookup_edge_count
    if isinstance(obj,list):
        for v in obj: edges(v)
    elif isinstance(obj,dict):
        for k,v in obj.items():
            if k in edge_keys and isinstance(v,list):
                assert set(v)<=active,(k,v)
                edge_count += len(v)
            elif k=='lookup_fact_ids':
                assert set(v)<=lookup_ids,(k,v)
                lookup_edge_count += len(v)
            else: edges(v)
edges(m)
remap = read(HERE/'transitive-retirement-map.json')
assert len(remap)==38 and all(ids and set(ids)<=active for ids in remap.values())
arc = read(HERE/'rejected-candidate-entries.json')['new_retirements']
assert len(arc)==1 and arc[0]['id']=='Q47'
assert arc[0]['historical_question']==oqd['Q47']
assert arc[0]['historical_answer']==oad['Q47']
assert arc[0]['historical_material_fact_entry']==f0['Q47']
assert lookups[-1]['all_printed_or_contextual_facts_preserved']==f0['Q47']['material_requested_facts']
assert len(lookups[-1]['four_example_policy_and_permission_edges'])==4

challenge = read(QA/'coverage-challenge-05/report.json')
repairs = read(HERE/'mapping-precision-resolutions.json')
assert len(repairs)==14
for r in repairs:
    assert r['status']=='applied'
    for x in r['passage_ids']:
        assert set(r.get('remove_question_edges',[])).isdisjoint(byid[x]['question_ids'])
        assert set(r.get('retain_question_edges',[]))<=set(byid[x]['question_ids'])

immut = read(PRIOR/'prior-artifact-immutability-check.json')
count = 0
for folder,entries in immut.items():
    for name,rec in entries.items():
        assert sha(QA/folder/name)==rec['sealed_sha256']
        count += 1
rev03hashes=read(PRIOR/'artifact-hashes.json')
immut['coverage-revision-03']={}
for name,digest in rev03hashes.items():
    observed=sha(PRIOR/name)
    assert observed==digest
    immut['coverage-revision-03'][name]={'sealed_sha256':digest,'observed_sha256':observed,'unchanged':True}
    count += 1
assert sha(PRIOR/'sealed-manifest.json')=='9341886eca2c16ea3ffb18a487ff6828d62b12a4aa13e7de6dd744cb2121a699'
write('prior-artifact-immutability-check.json',immut)

closure=[
    {'pass':2,'addition_count':0,'new_ids':[],
     'target':'Complete final source-to-question sweep after all14 map groups, SC03/SC04, Q07 context classification, Q47 lookup and stale table-credit notes were repaired.',
     'records_examined':232,'result':'No new distinct procedure gap. Setup, actions, tracks/diagrams, breaks/endgame, all glossary abilities/sponsors/maps/final-scoring clarifiers, every baseFAQ and the full icon overview remain represented. Optional Digging maximum and named Map5 alternatives correct; numerical data remain lookup.',
     'complete_final_map_preceded_pass':True},
    {'pass':3,'addition_count':0,'new_ids':[],
     'target':'Second complete final map sweep in reverse prompt/lookup direction, including all232 records, all94 active prompts, all42 lookup records, scope exclusions and requested/context distinction.',
     'records_examined':232,'result':'No new distinct procedure or exception. Q47 examples only instantiate Q46 plus ordinary permissions; no additional question credit. All live question and lookup destinations resolve; frozen Q07 bonus context is not a requested grading part.',
     'complete_final_map_preceded_pass':True}
]
ledger=read(HERE/'novelty-rejection-ledger.json')
assert len(ledger['accepted_candidates'])==74
assert {r['id'] for r in ledger['accepted_candidates']}==active-{r['id'] for r in q[:20]}
assert len(ledger['all_rejected_historical_ids'])==46
ledger['closure_passes']=closure;ledger['terminal_zero_addition_passes']=2
ledger['adjudication_verdict']='Challenge05: zero new distinct gaps; retire Q47 direct policy instantiation, apply SC03/SC04 and requested/context plus map precision repairs. Fresh final challenge pending.'
ledger['next_step']='Sealed94-question author candidate ready for fresh independent challenge; two author zero passes are not independent acceptance.'
write('novelty-rejection-ledger.json',ledger)

reread=read(PRIOR/'source-reading-report.json')
reread['status']='Reuse complete unchanged33-page primary inventory; targeted SC03/SC04 source reinspection and two complete final map passes performed in revision04.'
reread['reused_inventory']='../coverage-revision-03/source-reading-report.json; original PDFs and primary renders unchanged'
reread['revision04_targeted_primary_checks']=[
    {'source':'Main English v1.2 p13 lower hand-fan Crested Porcupine','asset':'../coverage-challenge-05/renders/digging-card.png','finding':'Choose up to2x, optional maximum.'},
    {'source':'OfficialFAQ p2 Map5 glyph; main pp2/12 and IconOverviewp1 special-enclosure identity key','asset':'../pre-expanded-source-repairs/faq-p2-map5.png','finding':'Reptile House or Large Bird Aviary, choose one free before upgrade, normal placement.'},
    {'source':'Glossary pp2–3 Hypnosis four examples','finding':'Direct copied-card side policy examples; full original facts and four per-example policy/permission links preserved.'}]
reread['terminal_author_passes']=closure
root=Path('/home/jonny/projects/boardgame-rules')
for r in reread['pdfs']:
    assert sha(root/r['file'])==r['sha256']
write('source-reading-report.json',reread)

trace={'scope':'Complete final map after all revisions, both terminal author passes; no independent acceptance claim.',
    'map_sha256':sha(HERE/'coverage-map.json'),'zero_addition_passes':closure,
    'forward_pass_records':[{'passage_id':r['passage_id'],'question_ids':r['question_ids'],'lookup_fact_ids':r.get('lookup_fact_ids',[]),'disposition':r['disposition']} for r in m['passages']],
    'reverse_pass_prompt_records':[{'question_id':r['id'],'question':r['question'],
        'passage_ids':[s['passage_id'] for s in m['passages'] if r['id'] in s['question_ids']]} for r in q],
    'no_prompt_scope_records':[r for r in m['passages'] if not r['question_ids']]}
write('terminal-pass-evidence.json',trace)
validation={'status':'pass','active_questions':94,'highest_historical_id':'Q140','original_baseline_questions':20,
    'accepted_additions':74,'new_questions_in_revision04':0,'current_retirements':1,'current_retired_id':'Q47',
    'historical_retirements':46,'source_passage_records':232,'retained_lookup_records':42,
    'live_question_edge_occurrences_checked':edge_count,'lookup_edge_occurrences_checked':lookup_edge_count,
    'transitive_retirement_destinations_checked':len(remap),'mapping_precision_groups_checked':14,
    'all94_question_objects_unchanged':True,'all92_other_surviving_key_objects_unchanged':True,
    'all91_other_surviving_fact_objects_unchanged':True,'Q116_exact_SC04_corrected_entry':True,'Q133_exact_SC03_corrected_entry':True,
    'original20_question_and_key_objects_exact_benchmark_v1_2':True,'Q07_frozen_key_unchanged_context_not_required':True,
    'Q06_Q42_unchanged':True,'all_prior232_passage_ids_preserved':True,'all_previous41_lookup_records_exact':True,
    'Q47_full_historical_objects_and_four_examples_preserved':True,'no_dead_live_question_or_lookup_edges':True,
    'prior_sealed_artifacts_unchanged':count,'revision03_manifest_hash_unchanged':True,'terminal_zero_addition_author_passes':2,
    'independent_final_saturation':'pending fresh coordinator challenge'}
write('validation-report.json',validation)

inputs=[]
for path in [PRIOR/'sealed-manifest.json',PRIOR/'questions.json',PRIOR/'answer-key.json',PRIOR/'coverage-map.json',
    PRIOR/'material-requested-facts.json',QA/'coverage-challenge-05/report.json',QA/'source-key-correction-SC03.json',
    QA/'source-key-precision-SC04.json',BASE/'questions.json',BASE/'answer-key.json']:
    inputs.append({'path':str(path.relative_to(QA)),'sha256':sha(path)})
provenance=read(PRIOR/'input-provenance.json')
provenance['revision']='coverage-revision-04';provenance['inputs']=inputs
provenance['immutable_prior_artifact_count']=count
provenance['scope_of_revision']='No new questions. Only Q47 retirement; exact SC03/SC04 keys/facts; Q07 facts context classification; all14 challenge05 map repairs and stale lookup credit clarification.'
write('input-provenance.json',provenance)

questions=['# Ark Nova original base — revision04 question bank','','94 active stable IDs through Q140. All question objects unchanged; retired IDs are archived and never reused.','']
answers=['# Ark Nova original base — revision04 answer key','','Original20 key objects exactly match benchmark-v1.2. Q116 and Q133 inherit exact versioned SC04/SC03 entries; Q47 is archived. Q07 bonus timing is source context, not a requested grading part.','']
for r in q:
    x=r['id'];ans=ad[x]
    questions += [f'## {x}','',r['question'],'']
    answers += [f'## {x}','',r['question'],'',ans['expected_answer'],'','Material requested facts:','']
    answers += ['- '+str(v) for v in f[x]['material_requested_facts']]
    if f[x].get('contextual_source_facts_not_requested'):
        answers += ['','Context only — not requested and not a grading requirement:','']
        answers += ['- '+v for v in f[x]['contextual_source_facts_not_requested']]
    refs=ans['source_references']
    answers += ['','Primary source references:','']+['- '+str(v) for v in (refs if isinstance(refs,list) else [refs])]+['']
(HERE/'question-bank.md').write_text('\n'.join(questions))
(HERE/'answer-key.md').write_text('\n'.join(answers))
(HERE/'coverage-report.md').write_text('''# Ark Nova source coverage revision04

The sealed author candidate contains94 active questions, stable historical IDs throughQ140,232 source-passage records and42 lookup records. This revision authors no new questions: the independent challenge05 found zero new distinct procedural gaps. It retires onlyQ47 as a direct application of the Q46 Hypnosis side policy to ordinary permissions already requested elsewhere. Its full historical question, key and facts remain archived; lookup-Q47 preserves all four source examples with separate policy and permission references. There are46 retired historical IDs in total.

SC03 installs the exact corrected Q133 entry: Digging permits up to2 optional selections, rather than requiring two. The English mainp13 lower hand-fan Crested Porcupine crop was visually checked. Both choices, choice-by-choice timing and immediate ordered display refill remain covered without changing Q42. SC04 installs the exact corrected Q116 entry, naming one Reptile House or one Large Bird Aviary for the Map5 free special-enclosure bonus, even before Build upgrade, choosing one and obeying normal placement restrictions. The officialFAQp2 glyph was rechecked against the supplied component identities.

All original20 question and key objects remain exact benchmark-v1.2, including the explicit SC01 bands and SC02 mandatory special-enclosure priority in Q17. Q07's frozen key is unchanged. Its source-supported sentence “Track bonuses immediate once.” is separately classified as unrequested context in the material-facts index and readable key; it is not a required Q07 grading part. Every other surviving question/key/fact object remains exact except the documented Q116/Q133 corrections and Q07 fact classification.

All14 challenge05 mapping groups are repaired: setup and printed-kiosk edges, Pouch/Perception versus Sunbathing, Polar Bear end timing, bonus-origin upgrade gates, actual Playground lookup255_256, university lookup_uni3, and obsolete Q138/payoff-table credit notes. The stale Species Diversity whole-table note is likewise clarified as retained lookup without standalone credit. Numeric tables, named card amounts and the four Hypnosis examples remain evidence; live prompt references do not imply those prompts literally request every printed cell. All live question and lookup destinations resolve.

The complete unchanged primary-source inventory is reused: main20, glossary8, FAQ3 and official base IconOverview2 pages. The corrected passages were checked directly and the whole final232-record map received two terminal zero-addition author passes after all repairs were complete. The packet still includes all base procedures, listed sponsors, advanced-map clarifiers, final-scoring clarifiers, FAQ restrictions and printed card effects present in those sources. Solo passages are scope-classified and excluded; no Marine Worlds, strategy guide, absent Sponsor223/Map3 text or unsupplied deck text is inferred. Original German publisher photographs supplement only obscured numeric component art. The third-party2022 German-card review photograph is corroborating history, not firsthand user or English-card evidence.

Validation confirms exact frozen-object preservation, all prior232 passage IDs, all previous41 lookup entries, full Q47 archive, live transitive references, and unchanged prior sealed artifacts. No canonical summary, reader outputs or grades were read. These are source-only author checks; fresh independent acceptance remains pending.
''')
(HERE/'author-prompt-provenance.md').write_text('''# Coordinator author task — revision04

> Challenge05 FINAL report coverage-challenge-05/report.json ready. Create new coverage-revision-04 ONLY, preserveallsealedrev03 andearlier. Reportfinds ZERO newdistinctquestiongaps. Resolveall4findings/14mappinggroups: retireQ47 asdirectQ46side-policy instantiation (fullfourexamplespreservedlookup, transitiveactualpermissionsrefs); applySC03Q133 up-to2optionalmaximum key+facts+ledger/map; applySC04Q116 named ReptileHouseORLargeBirdAviary alternatives/keyfactsnormalplacement. Rootstored exactold/correctedentries in source-key-correction-SC03.json andsource-key-precision-SC04.json, visuallyverified primarysources; useexactcorrectedentries. Original20question/keyobjects remainexactbenchmark-v1.2, other19keyspreserved. Q07source-supported 'Trackbonusesimmediateonce' is UNREQUESTEDcontext, NOT a requestedgradingpart: preservefrozenoriginalQ07keyentry; reclassifythatclause inmaterialfactsindexascontextual (recordexplicitrequested/contextdistinction,no silentlydemandingit). Thisisgradingprecision,notkeyweakening/sourcecorrection. Fixall14mapgroups exactlyreport, includingactuallookup255_256,lookup_uni3, staleQ138noveltycredit, stalewholetablenotes, unrelatededges. RetireQ47onlynewretirement=>94active,stableIDsthroughQ140;46historicalretired. Preserveallotherquestion/key/factobjects exceptdocumentedQ07factclassification,Q116,Q133corrections, fullQ47history. Rebuildallmap/lookup/ledgerswithnodeadIDs, retainnumericfactswithoutautomaticquestioncredit. Complete twoterminalzero-additionpasses AFTERfinalmapcomplete, preservation/edgechecks, exactimmutablehashseal/readablebanks/report. Youmayreuseyourcompleteprimaryreread inventory for unchangedrawsources whilecheckingcorrectedpassagesandwholefinalsource-map twice; don'tneeddownload/rerenderunchangedassets. Nonewquestionauthorship needed. Noreaders/summary/grades. Rootwillprovidefreshindependentchallengeaftersealedrev04. Sendprogressandfinalpaths/hashes.

Earlier author prompts and candidates remain immutable in their original revision directories. This author role does not claim independent saturation acceptance.
''')
hashes={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name not in {'artifact-hashes.json','sealed-manifest.json'}}
write('artifact-hashes.json',hashes)
core=['questions.json','answer-key.json','material-requested-facts.json','coverage-map.json','shared-source-lookup-facts.json','novelty-rejection-ledger.json','validation-report.json']
write('sealed-manifest.json',{'status':'sealed_author_candidate_for_fresh_independent_challenge','revision':'coverage-revision-04',
    'active_question_count':94,'highest_historical_id':'Q140','source_passage_records':232,'lookup_records':42,
    'new_question_ids':[],'current_retired_ids':['Q47'],'historical_retired_count':46,
    'baseline':'benchmark-v1.2 exact original20; SC03 Q133 and SC04 Q116 expanded-key corrections',
    'terminal_author_zero_addition_passes':2,'independent_saturation_accepted':False,
    'core_sha256':{x:hashes[x] for x in core},'all_artifact_hashes_sha256':sha(HERE/'artifact-hashes.json')})
print(json.dumps({'validation':validation,'sealed_manifest_sha256':sha(HERE/'sealed-manifest.json'),
    'core_sha256':{x:hashes[x] for x in core}},indent=2))
