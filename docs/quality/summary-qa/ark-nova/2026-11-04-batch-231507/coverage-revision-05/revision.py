import copy
import hashlib
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
QA=HERE.parent
PRIOR=QA/'coverage-revision-04'
def read(path): return json.loads(path.read_text())
def write(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
FROZEN=['questions.json','answer-key.json','material-requested-facts.json','shared-source-lookup-facts.json','novelty-rejection-ledger.json']
CHANGES={'M06a':['Q140'],'IO.sizes':['Q85'],'IO.pilfer':['Q125']}

if sys.argv[1]=='prepare':
    for name in FROZEN+['question-bank.md','answer-key.md']:
        (HERE/name).write_bytes((PRIOR/name).read_bytes())
    m=read(PRIOR/'coverage-map.json')
    for r in m['passages']:
        if r['passage_id'] in CHANGES:
            r['question_ids']=CHANGES[r['passage_id']]
    # The map metadata is intentionally inherited. Only the three documented
    # passage question_ids fields change; the revision05 manifest identifies this delta.
    write('coverage-map.json',m)
    print('Prepared only three map fields; five bank JSON files and both readable banks copied byte for byte.')
    sys.exit(0)

assert sys.argv[1]=='seal'
q=read(HERE/'questions.json')['questions']
a=read(HERE/'answer-key.json')['answers']
f=read(HERE/'material-requested-facts.json')
lookups=read(HERE/'shared-source-lookup-facts.json')
ledger=read(HERE/'novelty-rejection-ledger.json')
m=read(HERE/'coverage-map.json')
m0=read(PRIOR/'coverage-map.json')
active={r['id'] for r in q}
assert len(q)==len(a)==len(f)==len(active)==94
assert len(lookups)==42 and len(m['passages'])==232
assert m['shared_source_lookup_facts']==lookups
frozen_checks={}
for name in FROZEN+['question-bank.md','answer-key.md']:
    assert (HERE/name).read_bytes()==(PRIOR/name).read_bytes()
    frozen_checks[name]={'prior_sha256':sha(PRIOR/name),'current_sha256':sha(HERE/name),'bytes_identical':True}
assert q[:20]==read(QA/'benchmark-v1.2/questions.json')['questions']
assert a[:20]==read(QA/'benchmark-v1.2/answer-key.json')['answers']

expected=copy.deepcopy(m0)
diffs=[]
for old,r,e in zip(m0['passages'],m['passages'],expected['passages']):
    x=r['passage_id']
    if x in CHANGES:
        e['question_ids']=CHANGES[x]
        diffs.append({'passage_id':x,'old_question_ids':old['question_ids'],'new_question_ids':r['question_ids']})
assert m==expected
assert len(diffs)==3
assert ledger==read(PRIOR/'novelty-rejection-ledger.json')
lookup_ids={r.get('lookup_id',r.get('id')) for r in lookups}
edge_keys={'question_ids','covered_by','procedure_covered_by','procedure_covered_by_active_ids','active_procedure_covering_ids','policy_question_ids','permission_question_ids'}
edge_count=0;lookup_count=0
def check_edges(obj):
    global edge_count,lookup_count
    if isinstance(obj,list):
        for v in obj: check_edges(v)
    elif isinstance(obj,dict):
        for k,v in obj.items():
            if k in edge_keys and isinstance(v,list):
                assert set(v)<=active,(k,v)
                edge_count+=len(v)
            elif k=='lookup_fact_ids':
                assert set(v)<=lookup_ids
                lookup_count+=len(v)
            else: check_edges(v)
check_edges(m)
assert active<={x for r in m['passages'] for x in r['question_ids']}
assert next(r for r in m['passages'] if r['passage_id']=='IO.sizes')['lookup_fact_ids']==['lookup-Q87']
assert 'Q54' in next(r for r in m['passages'] if r['passage_id']=='GAB.pilfering_payment_repeat')['question_ids']

immut=read(PRIOR/'prior-artifact-immutability-check.json')
prior_count=0
for folder,items in immut.items():
    for name,rec in items.items():
        assert sha(QA/folder/name)==rec['sealed_sha256']
        prior_count+=1
immut['coverage-revision-04']={}
for name,digest in read(PRIOR/'artifact-hashes.json').items():
    observed=sha(PRIOR/name)
    assert observed==digest
    immut['coverage-revision-04'][name]={'sealed_sha256':digest,'observed_sha256':observed,'unchanged':True}
    prior_count+=1
assert sha(PRIOR/'sealed-manifest.json')=='9ea8dfddff079966ee8dc3d95a590a6742d1085e22275ff44b7723656462fe14'
write('prior-artifact-immutability-check.json',immut)
write('frozen-bank-byte-preservation.json',frozen_checks)

findings=read(QA/'coverage-challenge-06/findings.json')
assert not findings['new_procedural_gaps'] and not findings['answer_contradictions'] and not findings['new_novelty_rejections']
write('mapping-precision-resolutions.json',{'input_findings_sha256':sha(QA/'coverage-challenge-06/findings.json'),
    'resolutions':[
        {'finding':'C06-P01','passage_id':'M06a','live_question_ids':['Q140'],'decision':'RemoveQ03 andQ19 as normal-gameplay coverage; no optional context edge retained.'},
        {'finding':'C06-P02','passage_id':'IO.sizes','live_question_ids':['Q85'],'decision':'RemoveQ11/Q20/Q33; preserve lookup-Q87 unchanged; no optional context edges retained.'},
        {'finding':'C06-P03','passage_id':'IO.pilfer','live_question_ids':['Q125'],'decision':'RemoveQ54 from target-selection passage; Q54 remains on separate payment/repetition passage. No optionalQ53 context edge added.'}],
    'exact_map_field_deltas':diffs,'map_metadata_inherited_from_revision04':True,'other_map_content_exact':True})

passes=[
    {'pass':1,'new_question_additions':0,'source_map_complete_before_pass':True,'map_records_checked':232,
     'method':'Forward final-map sweep using unchanged complete33-page source inventory; compare every final record to prior map, check the three actual prompt destinations and source scope; no bank/key/fact/lookup changes.',
     'result':'No new distinct rule, outcome, timing or exception. Only the three documented live-edge removals were needed.'},
    {'pass':2,'new_question_additions':0,'source_map_complete_before_pass':True,'map_records_checked':232,
     'method':'Reverse full-map and prompt/lookup sweep; check all94 active IDs have live passage coverage, all42 lookups unchanged, no dead destinations, and all previously mapped primary-source records remain represented.',
     'result':'Zero additions. Normal play maps onlyQ140; size definitions onlyQ85; Pilfering target selection onlyQ125. Separate Q54 payment passage retained.'}]
write('terminal-author-passes.json',{'revision':'coverage-revision-05','terminal_zero_addition_passes':2,
    'passes':passes,'full_source_inventory_reused':'../coverage-revision-04/source-reading-report.json',
    'frozen_ledger_note':'The novelty ledger is copied byte for byte as required. These new revision05 author passes are recorded separately rather than mutating the accepted ledger.',
    'map_sha256':sha(HERE/'coverage-map.json'),
    'all_passage_ids_checked':[r['passage_id'] for r in m['passages']]})
validation={'status':'pass','active_questions':94,'source_passage_records':232,'lookup_records':42,
    'highest_historical_id':'Q140','historical_retirements':46,'new_questions':0,'new_retirements':0,
    'changed_map_records':list(CHANGES),'only_three_question_ids_fields_changed':True,
    'five_bank_json_files_byte_identical_to_revision04':True,'readable_banks_byte_identical':True,
    'original20_question_and_key_objects_exact_benchmark_v1_2':True,'embedded_lookup_exact':True,
    'live_question_edge_occurrences_checked':edge_count,'lookup_edge_occurrences_checked':lookup_count,
    'all_active_ids_still_have_map_coverage':True,'no_dead_live_question_or_lookup_edges':True,
    'all_prior232_source_records_retained':True,'prior_sealed_artifacts_unchanged':prior_count,
    'revision04_manifest_unchanged':True,'terminal_author_zero_addition_passes':2,
    'independent_bank_status':'Challenge06 accepted saturation, requested-answer accuracy and strict novelty on identical94-question bank.',
    'independent_map_delta_status':'Pending same reviewer06 check of this precise three-field delta and byte identity.'}
write('validation-report.json',validation)

inputs=[]
for path in [PRIOR/'sealed-manifest.json',QA/'coverage-challenge-06/findings.json',QA/'coverage-challenge-06/report.md']+[PRIOR/x for x in FROZEN+['coverage-map.json']]:
    inputs.append({'path':str(path.relative_to(QA)),'sha256':sha(path)})
write('input-provenance.json',{'revision':'coverage-revision-05','inputs':inputs,
    'source_inventory':'Unchanged complete English basev1.2 primary packet:33PDFpages; same authorized original publisher numeric-art supplements and boundaries.',
    'scope':'Only three map question_ids fields changed. All five bankJSON files and both readable banks copied byte for byte. No summary, reader outputs or grades read.',
    'neutral_metadata_note':'coverage-map.json internal revision metadata deliberately remains inherited revision04 to make its entire structural delta exactly the three documented question_ids lists. This directory and sealed manifest identify revision05.'})
(HERE/'coverage-report.md').write_text('''# Ark Nova coverage revision05

This is a three-field map repair over the unchanged94-question revision04 bank. There are232 source-passage records and42 lookup records. The questions, answer key, material-facts index, lookup file and novelty ledger are byte-identical to revision04. Both readable banks are copied unchanged. No questions, key facts, lookups, novelty decisions or historical IDs changed.

The three exact live-coverage corrections are M06a→Q140 only, IO.sizes→Q85 only and IO.pilfer→Q125 only. Q19 break administration is not retained as a normal-gameplay request. Generic accommodation/scoring/syntax prompts are not treated as requests for small/large definitions. Q54 stays linked to the separate Pilfering payment/repetition passage. No optional contextual edges are added; lookup-Q87 remains unchanged. All other map content, including metadata and embedded lookup data, is exact prior content. The inherited internal map revision field is retained deliberately so that only the three documented question_ids lists differ; this directory and manifest identify revision05.

The complete unchanged33-page primary-source inventory is reused. Two terminal author zero-addition passes after the repaired map checked all232 records and forward/reverse live destinations. Their records are separate in terminal-author-passes.json so the frozen novelty ledger remains byte-identical. All94 active IDs retain coverage, and live question/lookup references resolve. Prior seals remain unchanged.

Independent challenge06 accepted saturation, requested-answer accuracy and strict novelty on this identical94-question bank, with zero new gaps, contradictions or rejections. Its remaining findings were these three map precision groups. The same independent reviewer must still verify the repaired map delta and exact bank identity. The author does not claim that pending independent delta acceptance.
''')
(HERE/'author-prompt-provenance.md').write_text('''# Coordinator task — revision05

> Challenge06 complete: coverage-challenge-06/findings.json +report.md accept saturation/keyaccuracy/strictnovelty onALL94unchanged questions, ZEROnewgaps/contradictions/rejections. Only3mapedgegroups remain. Create smallnewcoverage-revision-05 preservingALL94question/key/materialfact/42lookup/noveltyledger objects exact (copybytes). CorrectONLY documentedmapgroups: M06a liveQ140only fornormalgameplay; removeQ03, putQ19separatecontext ifretained. IO.sizes liveQ85only; removeQ11/Q20/Q33 tooptionalcontext, preservelookupQ87. IO.pilfer liveQ125 (+Q53onlyqualifiedself/tiecontextifdesired); removeQ54fromtargetselection (remainsseparatepaymentpassage). Preservealloldseals/history. Recomputeparentmap/lookupcopiesneeded (no semanticlookupchanges), no deadIDs; newtwoauthorzero-additionpasses aftermapcomplete (existingrawsourcefullread inventory unchanged). Recordthreeprecisionresolutions/allbankbytesunchanged, finalhashseal andcorecounts232/94/42. Priorfreshchallenge06full94bankacceptance remainsvalidonidenticalQ/key/facts; rootwillaskSAMEindependentreviewer06 tocheck repairedmapdelta andexactbankidentity, no needre-authorquestionsorreadotherreports. Finishfinite3fixes/reports/checks, don'taddunrelatedchanges. Sendsealedpaths+hashes.
''')
hashes={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name not in {'artifact-hashes.json','sealed-manifest.json'}}
write('artifact-hashes.json',hashes)
core=FROZEN+['coverage-map.json','validation-report.json']
write('sealed-manifest.json',{'status':'sealed_map_delta_pending_same_independent_reviewer06_check','revision':'coverage-revision-05',
    'active_question_count':94,'highest_historical_id':'Q140','source_passage_records':232,'lookup_records':42,
    'new_question_ids':[],'new_retired_ids':[],'historical_retired_count':46,'byte_identical_bank_base':'coverage-revision-04',
    'only_three_map_question_ids_lists_changed':list(CHANGES),'terminal_author_zero_addition_passes':2,
    'independent_bank_acceptance':'challenge06 on exact same94questions/keys/facts/lookups/ledger',
    'independent_map_delta_acceptance':'pending','core_sha256':{x:hashes[x] for x in core},
    'all_artifact_hashes_sha256':sha(HERE/'artifact-hashes.json')})
print(json.dumps({'validation':validation,'sealed_manifest_sha256':sha(HERE/'sealed-manifest.json'),'core_sha256':{x:hashes[x] for x in core}},indent=2))
