import copy
import hashlib
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent; QA=HERE.parent; PRIOR=QA/'coverage-revision-05'
ROOT=Path('/home/jonny/projects/boardgame-rules')
def read(path): return json.loads(path.read_text())
def write(name,value): (HERE/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

NEWQ={'id':'Q141','question':'If the game ends before any player reaches 10 conservation points, what must all players do with their Final Scoring cards, and when?'}
NEWA={'id':'Q141','expected_answer':'All players must choose and discard one of their Final Scoring cards before end-game scoring begins, before adding those card points to their totals.',
    'material_requested_facts':[
        'The fallback applies if no player reached 10 conservation points before the game ends.',
        'All players must choose and discard one of their Final Scoring cards.',
        'Do this before end-game scoring begins, before adding those card points.'],
    'source_references':['Main English base v1.2 PDF p18, 10-conservation bullet fallback.','Main English base v1.2 PDF p19, Score cards reminder.']}
NEWF={k:copy.deepcopy(NEWA[k]) for k in ['material_requested_facts','source_references']}
NEWF['origin']='revision06 distinct no-player-reaches10 conditional and before-scoring deadline'
NEWC={'id':'Q141','decision':'add_distinct_source_defined_conditional_timing_branch','material_requested_facts':NEWA['material_requested_facts'],
    'source_references':NEWA['source_references'],
    'novelty_reason':'Ending without any player reaching10 creates a separate mandatory discard trigger and before-scoring deadline. The reached10 event does not entail this counterfactual obligation; accurate extra Q20 key context is not a prompt request.',
    'new_credit':1,'no_additional_credit':['discard destination/orientation','ordinary reached10 event','Resistance retained-card rule','per-card conservation cap']}
FALLBACK_ID='M18_M19.no10_final_scoring_fallback'

if sys.argv[1]=='prepare':
    q=read(PRIOR/'questions.json'); a=read(PRIOR/'answer-key.json'); f=read(PRIOR/'material-requested-facts.json')
    for obj in [q,a]: obj['benchmark_version']='coverage-revision-06-SC01-SC02-SC03-SC04'
    q['questions'].append(NEWQ); a['answers'].append(NEWA); f['Q141']=NEWF
    write('questions.json',q);write('answer-key.json',a);write('material-requested-facts.json',f)
    (HERE/'shared-source-lookup-facts.json').write_bytes((PRIOR/'shared-source-lookup-facts.json').read_bytes())
    (HERE/'source-key-corrections.json').write_bytes((QA/'coverage-revision-04/source-key-corrections.json').read_bytes())
    (HERE/'transitive-retirement-map.json').write_bytes((QA/'coverage-revision-04/transitive-retirement-map.json').read_bytes())
    m=read(PRIOR/'coverage-map.json');m['revision']='coverage-revision-06'
    m['authoring_role']='Source-only author adding the independently established no10 fallback prompt; fresh challenge07 pending.'
    for r in m['passages']:
        if r['passage_id'] in ['M18b','M19b']:
            r['question_ids'].append('Q141')
            r['revision06_fallback_scope']='For the conditional where no player reached10 before game end, actual requested coverage is Q141 alone. Q20 remains for its milestone/endgame/scoring requests; its accurate fallback key clause is unrequested context. Q56 does not request this alternative trigger.'
            r['conditional_branches']=[{'condition':'Game ends before any player reaches10 conservation points','question_ids':['Q141'],
                'procedure':'All players choose/discard one Final Scoring card before end-game scoring/card points begin.'}]
    m['passages'].append({'passage_id':FALLBACK_ID,'source':'Main English base v1.2 PDF p18, 10-conservation fallback; p19, Score cards reminder',
        'passage':'If no player reached10 conservation before game ends, all players must choose/discard one Final Scoring card before end-game scoring/card points begin.',
        'disposition':'covered','question_ids':['Q141'],'novelty_credit':'One distinct source-defined conditional discard trigger and deadline; no destination/cap/Resistance credit.',
        'requested_context_distinction':'The unchanged Q20 key/facts contain an accurate fallback sentence but Q20 does not request it. Q141 is the actual prompt coverage.'})
    write('coverage-map.json',m)
    ledger=read(PRIOR/'novelty-rejection-ledger.json')
    ledger['revision']='coverage-revision-06';ledger['active_question_count']=95;ledger['highest_historical_id']='Q141'
    ledger['accepted_candidates'].append(NEWC)
    ledger['inherited_revision04_current_retirement']={'count':ledger['current_retirement_count'],'ids':ledger['current_retire_ids'],'finding':ledger.get('current_novelty_rejection')}
    ledger['current_retirement_count']=0;ledger['current_retire_ids']=[];ledger['current_novelty_rejection']=None
    ledger['revision06_prior_ledger_sha256']=sha(PRIOR/'novelty-rejection-ledger.json')
    ledger['revision06_old94_question_key_fact_objects_exact']=True
    ledger['source_scope_qualification']='Q20 fallback key context remains source-accurate and frozen, but is not a requested grading part or literal coverage. NewQ141 asks the distinct conditional branch.'
    ledger['revision06_prior_passes']={'revision_passes':copy.deepcopy(ledger['revision_passes']),'closure_passes':copy.deepcopy(ledger['closure_passes']),
        'revision05_separate_passes':'../coverage-revision-05/terminal-author-passes.json'}
    ledger['revision_passes']=[{'pass':1,'new_ids':['Q141'],'addition_count':1,'target':'One independently confirmed conditional/timing branch; old94objects unchanged; full source map updated.'}]
    ledger['closure_passes']=[];ledger['terminal_zero_addition_passes']=0
    ledger['adjudication_verdict']='Source-only fallback adjudication reopens prior saturation: genuine unasked no10discard trigger, repaired byQ141. Existing94novelty decisions unchanged.'
    ledger['independent_saturation_accepted']=False
    ledger['next_step']='Complete whole final source-to-prompt map and two terminal zero-addition author passes, then fresh independent challenge07.'
    write('novelty-rejection-ledger.json',ledger)
    print('Prepared95questions/233maprecords/42unchangedlookups; onlyQ141new; two terminal passes pending.')
    sys.exit(0)

assert sys.argv[1]=='seal'
q=read(HERE/'questions.json')['questions'];a=read(HERE/'answer-key.json')['answers'];f=read(HERE/'material-requested-facts.json')
q0=read(PRIOR/'questions.json')['questions'];a0=read(PRIOR/'answer-key.json')['answers'];f0=read(PRIOR/'material-requested-facts.json')
assert q[:-1]==q0 and a[:-1]==a0 and q[-1]==NEWQ and a[-1]==NEWA and f['Q141']==NEWF
assert {x:r for x,r in f.items() if x!='Q141'}==f0
assert q[:20]==read(QA/'benchmark-v1.2/questions.json')['questions']
assert a[:20]==read(QA/'benchmark-v1.2/answer-key.json')['answers']
assert len(q)==len(a)==len(f)==95
active={r['id'] for r in q}
assert len(active)==95 and set(f)==active
m=read(HERE/'coverage-map.json');m0=read(PRIOR/'coverage-map.json')
assert len(m['passages'])==233
assert [r['passage_id'] for r in m['passages'][:-1]]==[r['passage_id'] for r in m0['passages']]
for r,s in zip(m['passages'],m0['passages']):
    if s['passage_id'] not in ['M18b','M19b']:assert r==s
assert m['passages'][-1]['passage_id']==FALLBACK_ID and m['passages'][-1]['question_ids']==['Q141']
assert (HERE/'shared-source-lookup-facts.json').read_bytes()==(PRIOR/'shared-source-lookup-facts.json').read_bytes()
lookups=read(HERE/'shared-source-lookup-facts.json');assert len(lookups)==42 and lookups==m['shared_source_lookup_facts']
lookup_ids={r.get('lookup_id',r.get('id')) for r in lookups}
edgekeys={'question_ids','covered_by','procedure_covered_by','procedure_covered_by_active_ids','active_procedure_covering_ids','policy_question_ids','permission_question_ids'}
edge_count=0;lookup_count=0
def edges(obj):
    global edge_count,lookup_count
    if isinstance(obj,list):
        for v in obj:edges(v)
    elif isinstance(obj,dict):
        for k,v in obj.items():
            if k in edgekeys and isinstance(v,list):assert set(v)<=active,(k,v);edge_count+=len(v)
            elif k=='lookup_fact_ids':assert set(v)<=lookup_ids;lookup_count+=len(v)
            else:edges(v)
edges(m)
assert active<={x for r in m['passages'] for x in r['question_ids']}
assert all(set(ids)<=active for ids in read(HERE/'transitive-retirement-map.json').values())
ledger=read(HERE/'novelty-rejection-ledger.json');ledger0=read(PRIOR/'novelty-rejection-ledger.json')
assert ledger['accepted_candidates'][:-1]==ledger0['accepted_candidates'] and ledger['accepted_candidates'][-1]==NEWC
assert len(ledger['accepted_candidates'])==75 and len(ledger['all_rejected_historical_ids'])==46
assert ledger['all_rejected_historical_ids']==ledger0['all_rejected_historical_ids']
assert ledger['source_corrections']==ledger0['source_corrections']

passes=[{'pass':2,'addition_count':0,'new_ids':[],'map_records_examined':233,'final_map_complete_before_pass':True,
    'target':'Full source-to-actual-prompt sweep afterQ141/map completion; all old232records plus explicit no10fallback branch, all source families and printed lookup boundaries.',
    'result':'No further distinct source-defined procedure, timing or exception identified. Q141 alone requests the alternative no10mandatory discard trigger and before-scoring deadline.'},
    {'pass':3,'addition_count':0,'new_ids':[],'map_records_examined':233,'final_map_complete_before_pass':True,
    'target':'Second complete reverse prompt/branch/lookup sweep;95actual prompts,42lookup records, source-scope exclusions and contextual-key qualifiers.',
    'result':'No additional question. Existing94objects remain exact; Q20accurate extra fallback context does not count as a request. No newcredit for destination, ordinary milestone, cap or Resistance.'}]
ledger['closure_passes']=passes;ledger['terminal_zero_addition_passes']=2
ledger['next_step']='Sealed95-question author candidate ready for fresh independent source/coverage challenge07; final acceptance pending.'
write('novelty-rejection-ledger.json',ledger)
write('terminal-author-passes.json',{'revision':'coverage-revision-06','terminal_zero_addition_passes':2,'passes':passes,
    'map_sha256':sha(HERE/'coverage-map.json'),'source_inventory_reused':'../coverage-revision-04/source-reading-report.json',
    'all_passage_ids_examined':[r['passage_id'] for r in m['passages']]})

adjud_path=QA/'coverage-challenge-06/final-scoring-fallback-scope-adjudication.json'
write('scope-qualifications.json',{'qualification_id':'Q20-no10-context','affected_existing_id':'Q20','old_key_and_material_object_unchanged':True,
    'source_accurate_extra_key_clause':'or do before final scoring if never reached10.',
    'literally_requested_by_old_prompt':False,'grading_scope':'This accurate extra clause is contextual inQ20, not a requestedQ20grading part. Preserve the whole old key/material object exactly; use this external qualification instead of weakening or rewriting it.',
    'actual_requested_coverage':['Q141'],'other_noncoverage':{'Q56':'Resistance interaction does not ask the normal no10trigger.','Q139':'The reached10discard destination does not ask the absent-trigger fallback.'},
    'source_only_adjudication':'../coverage-challenge-06/final-scoring-fallback-scope-adjudication.json','source_adjudication_sha256':sha(adjud_path)})
write('gap-resolution.json',{'source_adjudication':str(adjud_path.relative_to(QA)),'source_adjudication_sha256':sha(adjud_path),
    'resolution':'Add onlyQ141 for the genuinely unasked alternative trigger/deadline. Preserve all94oldquestion/key/material objects and42lookupobjects exactly.',
    'new_question_credit':1,'new_question':NEWQ,'new_key':NEWA,'actual_fallback_map_records':['M18b','M19b',FALLBACK_ID],
    'context_qualification_file':'scope-qualifications.json','no_new_retirements':True,'SC01_SC02_SC03_SC04_unchanged':True})

immut=read(PRIOR/'prior-artifact-immutability-check.json');count=0
for folder,items in immut.items():
    for name,rec in items.items():assert sha(QA/folder/name)==rec['sealed_sha256'];count+=1
immut['coverage-revision-05']={}
for name,digest in read(PRIOR/'artifact-hashes.json').items():
    observed=sha(PRIOR/name);assert observed==digest
    immut['coverage-revision-05'][name]={'sealed_sha256':digest,'observed_sha256':observed,'unchanged':True};count+=1
assert sha(PRIOR/'sealed-manifest.json')=='a15345a4c22790a245582d40f8f0207a58cbcac4b6053f259e4d6a3730588d72'
write('prior-artifact-immutability-check.json',immut)
def objhash(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
write('old94-object-preservation.json',{'prior_revision':'coverage-revision-05','all94question_key_fact_objects_exact':True,
    'records':[{'id':r['id'],'question_object_sha256':objhash(r),'answer_object_sha256':objhash(a0[i]),'material_fact_object_sha256':objhash(f0[r['id']]),
        'all_three_current_objects_equal_prior':r==q[i] and a0[i]==a[i] and f0[r['id']]==f[r['id']]} for i,r in enumerate(q0)],
    'lookup_file_bytes_exact':True,'lookup_sha256':sha(HERE/'shared-source-lookup-facts.json'),'all74prior_accepted_candidate_objects_exact':True})

rawpath=ROOT/'extracted/ark-nova-rules.txt';raw=rawpath.read_bytes()
assert len(raw.splitlines())==1898 and raw.count(b'\n')==1897 and not raw.endswith(b'\n') and raw.splitlines()[-1].strip()==b'3'
write('raw-packet-completeness.json',{'path':str(rawpath),'sha256':sha(rawpath),'splitline_count':1898,'LF_count':1897,
    'final_line_terminated':False,'last_logical_line':1898,'last_unterminated_line_content_trimmed':'3','last_line_kind':'FAQ page3 footer only',
    'body_or_source_change':False,'newly_reread_ranges':['1008–1045','1075–1095','1889–1898'],
    'complete_primary_inventory':'Prior full reading of all33PDFpages and full extracted packet; true EOFfooter is now explicitly included. Historical1897LF count is not a full splitline count.'})
reading=read(QA/'coverage-revision-04/source-reading-report.json')
reading['revision06_targeted_reread']={'main_pages_complete':[18,19],'visually_viewed_primary_renders':['primary-main-p18.png','primary-main-p19.png'],
    'raw_packet_ranges':['1008–1045','1075–1095','1889–1898'],'packet_splitlines':1898,'packet_LF_count':1897,'unterminated_footer_line1898':'3'}
reading['status']='Complete unchanged33-page primary inventory reused; fallback source pages fully reread and viewed; true extracted EOFchecked; two terminal233-record source-map passes complete.'
reading['terminal_author_passes']=passes
write('source-reading-report.json',reading)
validation={'status':'pass','active_questions':95,'highest_historical_id':'Q141','source_passage_records':233,'existing_passage_ids_preserved':232,
    'lookup_records':42,'historical_retirements':46,'new_questions':1,'new_question_ids':['Q141'],'new_retirements':0,
    'old94_question_objects_exact':True,'old94_key_objects_exact':True,'old94_material_fact_objects_exact':True,
    'lookup_file_byte_identical':True,'all74prior_accepted_candidate_objects_exact':True,'SC01_SC02_SC03_SC04_exact':True,
    'original20_questions_and_keys_exact_benchmark_v1_2':True,'Q20_key_and_fact_objects_unchanged_context_external':True,
    'live_question_edges_checked':edge_count,'lookup_edges_checked':lookup_count,'no_dead_live_question_or_lookup_edges':True,
    'prior_sealed_artifacts_unchanged':count,'revision05_manifest_unchanged':True,'raw_packet_splitlines':1898,'raw_packet_LF_count':1897,
    'terminal_author_zero_addition_passes':2,'independent_saturation':'reopened for genuine source-to-actual-prompt gap; fresh challenge07 pending'}
write('validation-report.json',validation)

qt=(PRIOR/'question-bank.md').read_text().replace('revision04','revision06',1).replace('94 active stable IDs through Q140. All question objects unchanged; retired IDs are archived and never reused.','95 active stable IDs through Q141. All94existing question objects unchanged; retired IDs remain archived.')
qt+='\n## Q141\n\n'+NEWQ['question']+'\n';(HERE/'question-bank.md').write_text(qt)
at=(PRIOR/'answer-key.md').read_text().replace('revision04','revision06',1)
at+='\n## Q141\n\n'+NEWQ['question']+'\n\n'+NEWA['expected_answer']+'\n\nMaterial requested facts:\n\n'+'\n'.join('- '+x for x in NEWA['material_requested_facts'])+'\n\nPrimary source references:\n\n'+'\n'.join('- '+x for x in NEWA['source_references'])+'\n'
(HERE/'answer-key.md').write_text(at)

inputs=[]
for path in [adjud_path,PRIOR/'sealed-manifest.json']+[PRIOR/x for x in ['questions.json','answer-key.json','material-requested-facts.json','coverage-map.json','shared-source-lookup-facts.json','novelty-rejection-ledger.json']]:
    inputs.append({'path':str(path.relative_to(QA)),'sha256':sha(path)})
write('input-provenance.json',{'revision':'coverage-revision-06','role':'Source-only author; no canonical summary, readers, grades or repair history consulted.',
    'inputs':inputs,'scope':'Original English basev1.2 controlling prose; same33PDFpage source packet and narrowly numeric original publisher art supplements. No solo/MW/strategy guide or unsupplied card/map text.',
    'primary_source_reread':['English mainPDF pp18–19 complete native text and primary renders','Extracted packet1036–1040/1084–1089 with surrounding ranges','True EOFthrough logical1898 footer'],
    'raw_packet_splitlines':1898,'raw_packet_LF_count':1897,'source_body_unchanged':True,'new_credit':1,'all94old_objects_preserved':True})
(HERE/'coverage-report.md').write_text('''# Ark Nova source coverage revision06

The sealed candidate has95 active stable IDs throughQ141,233 source-passage records and42 lookup records. Exactly one question is added. Every one of the94 prior question, answer and material-fact objects remains exact, including the accurate extra fallback context in Q20. All42 lookup objects and their file bytes remain exact. All74 earlier accepted-candidate objects,46 retired historical IDs, and SC01/SC02/SC03/SC04 corrections remain unchanged.

Q141 asks the distinct branch where the game ends before any player reaches10conservation points: all players must choose/discard one Final Scoring card before end-game scoring begins, before adding card points. Both complete primary Mainpp18–19 pages were reread and visually checked. The source-only adjudication explains why an absent10milestone creates a separate obligation and deadline, rather than a direct application of the reached10event. Only that conditional/timing branch earns new credit; destination/orientation, cap and Resistance do not.

Q20's frozen clause “or do before final scoring if never reached10” remains source-accurate. Its actual prompt does not request this fallback. scope-qualifications.json therefore marks the clause unrequested context externally, without editing or weakening the old key or material-fact object. Q56 and Q139 likewise do not literally request the alternative trigger. M18b and M19b now explicitly link the fallback toQ141, and the dedicated M18_M19.no10_final_scoring_fallback record makes this branch's actual prompt coverage explicit. All232 prior map IDs remain present; other prior passage objects are unchanged.

The unchanged complete33-page primary inventory is reused. A whole source-to-actual-prompt map sweep and two terminal zero-addition passes followed the complete new question and map. No further distinct rule, consequential timing, outcome or exception was identified by the author. Those passes are author checks; the fresh independent challenge07 remains pending, and prior blanket saturation acceptance is reopened by the adjudicated omission.

The extracted packet contains1898 splitlines and1897LF characters. Its final unterminated logical line1898 is only the FAQ page3 footer “3”. The true tail was read; no source or body content changed. raw-packet-completeness.json corrects the count explicitly while preserving historical artifacts. Old94 object identities, unchanged lookup bytes, all prior seals and live map references are validated. No canonical summary, reader outputs or grades were read.
''')
(HERE/'author-prompt-provenance.md').write_text('''# Coordinator task — revision06

> ReopencoverageforONEgenuineactualpromptgap independentlyconfirmed in coverage-challenge-06/final-scoring-fallback-scope-adjudication.json. Youremain source-only author: no canonical/readers/grades/repairhistory. Create coverage-revision-06 ONLY, preservealloldsealedfiles. Readsource-onlyadjudication+rawMainpp18–19/packet; no95readerhasstarted. AddQ141focusedquestion forgameendsbeforeanyplayerreaches10: allplayerschoose/discardONEFinalScoringcardBEFOREendgame scoring/cardpoints. Useproposal polishednormalspaces; no destination/cap/Resistanceextra newcredit. ALL94oldquestion/key/materialfact objects and42lookupobjects MUSTstayEXACTincltrueextraQ20context; do notweaken/rewriteoldkeys/facts. AddonlyQ141question/key/facts,95activeIDs through141,46historicalretiredunchanged. MarkQ20fallbackaccurateUNREQUESTEDcontext innewseparatescopequalification/resolution docs WITHOUTeditingoldfrozenQ20key/materialobject; actualcoverageoffallbackisQ141. Updatecomplete232-recordmap preservingallIDs, addexplicitfallbackrecordifneeded(M18/M19 sourcebranch); actualedgesQ141 forpp18–19fallback, olderQ20/56notliteralcoverage ofthisconditional. Maintainother95-questionnovelty/lookup/no-deadID principles. UpdateledgerwithONEnewdistincttimingbranch credit only; preserveallpriorcandidates/history/hashes. Wholefinalsource-to-promptmapcheck and TWOterminalzero-additionpasses AFTERnewquestion+mapcomplete; noquota. Correctrawpacketcompletenesscount:1898splitlines,1897LF;lastunterminatedfooteronly3 (same-reviewerEOFsupplementavailable). Readtruetailasneeded; no source/bodychanges forfooter. Produceexactpreservation/hashseal/readablebanks/report/validation; prior94identityproof andnew95count. Factualkey SC01/02/03/04 unchanged, original20samebenchmarkv1.2. ThenfreshNEWchallenge07willreviewactualfull95bank/source. Sendprogressandsealedpaths/hashes.
''')
hashes={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name not in {'artifact-hashes.json','sealed-manifest.json'}}
write('artifact-hashes.json',hashes)
core=['questions.json','answer-key.json','material-requested-facts.json','coverage-map.json','shared-source-lookup-facts.json','novelty-rejection-ledger.json','scope-qualifications.json','validation-report.json']
write('sealed-manifest.json',{'status':'sealed_author_candidate_for_fresh_independent_challenge07','revision':'coverage-revision-06','active_question_count':95,
    'highest_historical_id':'Q141','source_passage_records':233,'prior_source_passage_ids_preserved':232,'lookup_records':42,'new_question_ids':['Q141'],
    'new_retired_ids':[],'historical_retired_count':46,'old94_question_key_material_objects_exact':True,'lookup_file_bytes_exact':True,
    'terminal_author_zero_addition_passes':2,'independent_saturation_accepted':False,'raw_packet_splitlines':1898,'raw_packet_LF_count':1897,
    'core_sha256':{x:hashes[x] for x in core},'all_artifact_hashes_sha256':sha(HERE/'artifact-hashes.json')})
print(json.dumps({'validation':validation,'sealed_manifest_sha256':sha(HERE/'sealed-manifest.json'),'core_sha256':{x:hashes[x] for x in core}},indent=2))
