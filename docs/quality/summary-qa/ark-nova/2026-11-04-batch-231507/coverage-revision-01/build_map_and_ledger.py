import copy
from build_revision import HERE,QA,DRAFT,BASE,read,write,oldq,olda,oldmap,oldfacts,oldledger,challenge,reject,new,sc01,primary_ref_fixes

q=read(HERE/'questions.json');a=read(HERE/'answer-key.json')
qids={x['id'] for x in q['questions']}
assert {r['id'] for r in new}<=qids

# Every inherited primary passage remains in the new map. Rejected question IDs
# are replaced by the earliest real questions that actually contain the branch.
remap={qid:item['covered_by'] for qid,item in reject.items()}
coverage=copy.deepcopy(oldmap)
coverage['authoring_role']='Question-bank author revision after independent source challenge; fresh independent acceptance pending.'
coverage['revision']='coverage-revision-01'
coverage['baseline_benchmark']='benchmark-v1.1 / explicit source-key correction SC01'
coverage['source_boundaries']['component_numeric_supplement']='Matching original publisher Spielzene.jpg and Back_arche_nova.jpg original German component artwork supplement obscured Animals II numeric cells and tiny reputation-track numerals only. Original English prose and edition remain authority. The third-party 2022 German card review photo is corroborating research history only and is not authority.'
coverage['source_boundaries']['icon_overview']='Official original English base Icon Overview from Capstone original product page; local primary PDF table-source-check/capstone-icon-overview.pdf. Not a strategy guide.'
coverage['source_boundaries']['source_reports_not_required_as_authority']=True
for p in coverage['passages']:
    oldids=p['question_ids']
    updated=[]
    for qid in oldids:
        updated.extend(remap.get(qid,[qid]))
    p['question_ids']=sorted(set(updated),key=lambda x:int(x[1:]))
    removed=[qid for qid in oldids if qid in reject]
    if removed:
        p['revision_note']='Rejected duplicate candidate(s) '+', '.join(removed)+' remapped to earlier existing branches; no source passage removed.'

byid={p['passage_id']:p for p in coverage['passages']}
def fix(pid,source,passage,ids,note):
    p=byid[pid]
    p.update(source=source,passage=passage,question_ids=ids,revision_note=note)
    p.pop('note',None)
def add(pid,source,passage,ids,note):
    coverage['passages'].append({'passage_id':pid,'source':source,'passage':passage,'disposition':'covered','question_ids':ids,'revision_note':note})

fix('M02c','Main p2 Zoo-card component illustrations; Main p7 Zoo Cards','Science Lab Sponsor illustration and Sea Cave release-project illustration',['Q61','Q16','Q17'],
    'F07 corrects the erroneous Reptiles identity. Sea Cave is a release project; corrected Q17 covers its depicted size bands. Species Diversity receives its own passage record below.')
add('M02g','Main p2 base-project Species Diversity illustration; Main p7 Species Diversity illustration','Count different categories, not duplicate icons; 5/4/3 categories give 5/3/2 conservation',['Q135'],
    'ADD01/F01: distinct counting rule and complete printed table; not a numerical permutation of ordinary icon count.')
fix('M09c','Main p9 reputation/display paragraphs','Same/lower folders, one-time bonuses, maximum15 conversion, refill by ordered compaction/deck fill and no discard-pile search',['Q06','Q07','Q134'],
    'Q06 remains exact and tests timing. New Q134 explicitly tests the ordered refill execution; Q42 remains exact.')
add('M09f','Main p9 The Reputation Track and the Display','Higher-folder cards shift down into lower gaps preserving relative order; then deck fills remaining folders',['Q134'],
    'F07 requested the previously unasked preservation-of-order procedure; no extra novelty credit for refill timing.')
byid['M10a']['question_ids'].append('Q137')
byid['M10a']['revision_note']='F03: new Q137 now actually asks standard-enclosure empty starting face and once-only placement bonus; the earlier map overclaim is corrected.'
add('M10d','Main p10 Build I empty-side/placement-bonus paragraphs; Main p6 placement bonus','New standard enclosure empty-side up; each covered bonus immediately once; resolve each building bonuses before next building',['Q137','Q10'],
    'ADD03: Q137 covers the previously unasked state and once-only activation. Q10 supplies existing sequential funding context without new novelty credit.')
add('M13e','Main p13 Crested Porcupine illustrated Digging2 text; Glossary p2 Digging','Two selections from display-discard/refill or hand-discard/deck-draw; choice-by-choice decisions and immediate refill',['Q133','Q42','Q134'],
    'F04: Q133 adds only the previously unasked base choices. Q42 wording and answer remain exact; compaction details map to Q134.')
byid['GAB.digging']['source']='Glossary p2 Digging; Main p13 Crested Porcupine illustrated effect'
byid['GAB.digging']['passage']='Digging options and two selections; choose next option after each result; display discard refills immediately using ordered compaction'
byid['GAB.digging']['question_ids']=['Q42','Q133','Q134']
byid['GAB.digging']['revision_note']='Previously covered timing alone; actual options now requested separately without changing Q42.'
add('M18d','Main pp4–5 setup-board appeal/income diagrams; Main p18 step5a','Complete appeal-to-money payoff table, separate from additional kiosk and activated income',['Q136','Q19'],
    'ADD02/F02: one whole payoff-table question; Q19 continues to cover break order and other income.')

# Replace remapping mechanically broad groups with exact earlier atom coverage.
for pid in ['GF.004','GF.006']:
    byid[pid]['question_ids']=['Q09','Q34','Q104']
    byid[pid]['revision_note']='Q109 rejected: building-space exclusion, connected definition and empty upgrade spaces are earlier branches; no unsupplied final-card scoring table is invented.'
byid['GF.005']['question_ids']=['Q16','Q66']
byid['GF.005']['revision_note']='Q110 rejected: missing support tokens and discarded-project token destination are already requested by Q66 and Q16.'

coverage['shared_ability_parameterization']=[
 {'primary_source':'Official English base Icon Overview p2 Pouch X; Glossary p3 Pouch; Glossary p5 Expert on Australia212',
  'generic_source_fact':'Up to X hand cards tuck beneath the animal for2 appeal each; tucked cards cease functioning and are discarded on release without reversing earned appeal.',
  'covered_by':['Q55','Q72'],'rejected_duplicate_question':'Q126','reason':'Pouch1 already establishes the per-card reward/source; formal X adds no distinct branch.'},
 {'primary_source':'Official English base Icon Overview p2 Perception X; Glossary p6 Barred Owl Hut249',
  'generic_source_fact':'DrawX deck cards, keep half, discard the rest.','covered_by':['Q95'],'rejected_duplicate_question':'Q126','reason':'Perception2 already requests the same draw/keep/discard rule; no extra rounding rule is supplied or invented.'},
 {'primary_source':'Official English base Icon Overview p2 Sunbathing X; Glossary p6 Sea Turtle Tank250; Glossary p3 Sunbathing',
  'generic_source_fact':'Sell up toX hand cards for4 money each and discard the sold cards.','covered_by':['Q55','Q96'],'rejected_duplicate_question':'Q126','reason':'Changing2 to formalX creates no new source/destination/choice branch.'}
]
coverage['source_key_corrections']=[{'id':'SC01','question_id':'Q17','baseline':'benchmark-v1.1','rule':'Match depicted 2−/3/4+ bands: printed1/2,3,4/5 respectively. Actual enclosure and special capacity do not set the band.','primary_sources':['Main p15 release bands','Glossary p1 Release condition as shown','FAQ pp1–2'],'correction_record':'SC01-source-key-correction.json'}]

assert len({p['passage_id'] for p in coverage['passages']})==len(coverage['passages'])
assert all(set(p['question_ids'])<=qids for p in coverage['passages'])
mapped={qid for p in coverage['passages'] for qid in p['question_ids']}
assert qids<=mapped, qids-mapped
write('coverage-map.json',coverage)

facts={}
for answer in a['answers']:
    qid=answer['id']
    if qid in oldfacts:
        facts[qid]=copy.deepcopy(oldfacts[qid])
    else:
        facts[qid]={'origin':'revision01-new-source-procedure'}
    facts[qid]['source_references']=answer['source_references']
    facts[qid]['material_requested_facts']=answer.get('material_requested_facts',[x.strip() for x in answer['expected_answer'].split(';') if x.strip()])
    if qid=='Q17':
        facts[qid]['origin']='benchmark-v1.1 explicit SC01 source/key correction'
        facts[qid]['material_requested_facts']=[
            'Depicted2− accepts printed standard requirement1 or2; depicted3 requires exactly3; depicted4+ accepts4 or5.',
            'Actual occupied enclosure size and special-enclosure capacity do not set the release band.',
            'Lose printed appeal before conservation reward; discard the animal and its icons; retain ability-earned appeal, reputation/conservation and past effects.',
            'Prefer removing indicated special tokens if eligible and possible; otherwise free the smallest occupied standard meeting all requirements, then size-only, then none if none fits.',
            'The freeing procedure also applies to flock animals.'
        ]
write('material-requested-facts.json',facts)

accepted=[copy.deepcopy(r) for r in oldledger['accepted_candidates'] if r['id'] not in reject]
for r in accepted:
    if r['id'] in primary_ref_fixes:r['source_references']=primary_ref_fixes[r['id']]
accepted += [{'id':r['id'],'decision':'add_distinct_previously_unasked_source_procedure','new_requested_facts':r['material_requested_facts'],'source_references':r['source_references'],'novelty_reason':r['distinct_novelty']} for r in new]
ledger={'game':'Ark Nova','revision':'coverage-revision-01','baseline':'benchmark-v1.1 corrected original20','active_question_count':len(qids),
        'highest_historical_question_id':'Q137','historical_candidate_count':137,'rejected_historical_ids':sorted(reject,key=lambda x:int(x[1:])),
        'id_renumbering':False,'original_draft_immutable':True,'baseline_question_objects_unchanged':True,'baseline_answer_objects_unchanged':True,
        'frozen_Q06_Q42_question_and_answer_objects_unchanged':True,
        'prior_author_closure':{'file':'../coverage-draft/novelty-rejection-ledger.json','status':'overturned_by_fresh_independent_coverage_challenge','reason':'Independent challenge found3 source gaps,2 missing requested procedures and4 novelty overclaims. Original draft and old stopping claim remain historical evidence, not proof of saturation.'},
        'source_corrections':[sc01],
        'accepted_candidates':accepted,
        'novelty_rejections':list(reject.values()),
        'historical_entries_file':'rejected-candidate-entries.json',
        'proposed_amendment_dispositions':[
          {'target':'Q42','challenge_proposal':'Extend question with actual Digging choices','decision':'preserve_Q42_exact_add_Q133','reason':'Parent requires earlier question/key immutable. Actual source/destination choices are genuinely unasked; no repeated timing credit.'},
          {'target':'Q06','challenge_proposal':'Extend question with ordered compaction','decision':'preserve_Q06_exact_add_Q134','reason':'Parent requires original question/key immutable. Relative-order preservation and final deck filling are genuinely unasked.'},
          {'target':'Q17','challenge_proposal':'Clarify depicted size bands','decision':'inherit_explicit_benchmark_v1.1_SC01','reason':'Genuine source/key clarification authorized independently of reader performance; original question unchanged and historical old key retained.'},
          {'target':'Q131/Q132','challenge_proposal':'Primary-source reference cleanup','decision':'replace_derived_report_citation_with_raw_primary_diagrams_and_icon_overview','reason':'A future reviewer can verify actual diagrams without trusting a prior report.'}],
        'rejected_extra_proposals':[
          {'candidate':'Separate Jumping-trigger question','decision':'reject','covered_by':['Q05'],'reason':'Ordinary break endpoint procedure, no exception.'},
          {'candidate':'Separate PouchX/PerceptionX/SunbathingX numerical parameter variants','decision':'reject','covered_by':['Q55','Q72','Q95','Q96'],'reason':'Generic forms retained as source facts, but named X substitutions are not novel procedures.'},
          {'candidate':'One question per appeal value or Species Diversity tier','decision':'reject','covered_by':['Q135','Q136'],'reason':'One complete table covers all tiers; separate examples would inflate counts.'},
          {'candidate':'Extra repeat-choice/refill-timing facts in Q133 as new novelty','decision':'reject_duplicate_credit','covered_by':['Q42'],'reason':'Q133 only adds the actual Digging options and printed number of selections.'},
          {'candidate':'Separate sequential bonus-funding question in Q137','decision':'reject_duplicate_credit','covered_by':['Q10'],'reason':'New facts are empty starting face and once-only activation; existing funding rule is context.'}],
        'revision_passes':[
          {'pass':1,'target':'Primary-source gap resolution and SC01 baseline','addition_ids':['Q135','Q136','Q137'],'addition_count':3,'other_changes':'Archive four duplicate candidates without renumbering; preserve old entries; inherit corrected Q17. Printed Species tiers, appeal income bands, and empty-face/once-only rules verified.'},
          {'pass':2,'target':'Unasked Digging choices and ordered compaction; full inherited source map correction','addition_ids':['Q133','Q134'],'addition_count':2,'other_changes':'Keep Q06/Q42 exact. Correct Sea Cave/Species identities, atom-level coverage and primary references. Map all rejected entries to earlier real branches.'}],
        'source_map_complete_after_revision_pass':2,'open_source_gaps':[],
        'closure_passes':[],'terminal_zero_addition_passes':0,
        'reader_results_used':False,'independent_final_audit_claimed':False,'next_step':'Two author closure passes after complete revised source map, then a fresh independent source/coverage challenge.'}
write('novelty-rejection-ledger.json',ledger)
print(f'{len(coverage["passages"])} full source-map records; {len(qids)} active questions; no rejected IDs active or mapped; two addition passes recorded.')
