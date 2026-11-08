"""Validate the complete independent four-proposal decision set without rewriting it."""
from pathlib import Path
import hashlib
import json
from PIL import Image

B=Path(__file__).resolve().parent
S=B/'novelty-adjudication-18'
load=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
SH=lambda text:hashlib.sha256(text.encode()).hexdigest()
r,l,v=[load(S/n) for n in ['report.json','read-ledger.json','visual-manifest.json']]
proposals=load(S/'proposals.json')['proposed_set']
checks=[]
def check(label,condition):
    assert condition,label
    checks.append({'name':label,'passed':True})
for name,data in load(S/'original-freeze.json')['files'].items():check('raw original freeze '+name,H(S/name)==data['sha256'])
check('complete four decisions',len(r['gap_decisions'])==1 and len(r['classification_decisions'])==3 and r['completion']['all_four_proposals_decided'] is True)
gap=r['gap_decisions'][0]
check('complete literal gap proposal retained',gap['full_literal_proposal']==proposals['remaining_gaps'][0])
check('unchanged approved question and two facts',gap['decision']=='ACCEPT' and gap['approved_minimal_pretest_object']==gap['proposed_question_answer_fact_object'] and gap['question_answer_facts_changed'] is False and gap['approved_minimal_pretest_object']['question']==proposals['remaining_gaps'][0]['proposed_question'] and gap['approved_minimal_pretest_object']['predetermined_answer']==proposals['remaining_gaps'][0]['predetermined_answer'] and len(gap['approved_minimal_pretest_object']['predetermined_answer']['minimum_asked_facts'])==2)
check('proposal gap resolved without new questions by agent',gap['unresolved']==[] and r['completion']['new_questions_created_by_adjudicator']==0 and r['completion']['whole_corpus_stopping_pass'] is False and r['completion']['reader_responses_consulted_or_rescored'] is False)
q,key,f=[load(B/'expanded-v23'/n) for n in ['questions.json','answer-key.json','asked-fact-map.json']]
byq={x['id']:x for x in q['questions']};bykey={x['id']:x for x in key['answers']};byf={x['id']:x for x in f['questions']}
for row,old,ident in zip(r['classification_decisions'],proposals['coverage_map_classification_findings'],['Q172','Q116','Q142']):
    check('complete classification proposal '+ident,row['decision']=='ACCEPT' and row['full_literal_proposal']==old)
    current=row['proposed_vs_approved_question_answer_facts']
    check('no current question key or fact narrowed '+ident,current['approved_question']==byq[ident] and current['approved_predetermined_answer']==bykey[ident] and current['approved_requested_clauses']==byf[ident]['requested_clauses'] and current['changes_to_current_question_key_or_facts'] is None)
    check('concrete replacement '+ident,bool(row['approved_replacement_text']) and bool(row['approved_replacement_object']))
for ident,binding in r['current_question_key_fact_bindings'].items():
    for field,expected in [('question',byq[ident]),('predetermined_answer',bykey[ident]),('asked_fact_object',byf[ident])]:
        item=binding[field]
        check('exact current binding '+ident+field,H(item['path'])==item['full_byte_sha256'] and item['literal_object']==expected)
        text=Path(item['path']).read_text();pos=item['id_locator_unicode_offset']
        locator='"id": '+json.dumps(ident)
        check('ID locator '+ident+field,text[pos:pos+len(locator)]==locator)
        serializations=[json.dumps(expected,ensure_ascii=ascii_mode,sort_keys=sort_mode,separators=separators) for ascii_mode in [False,True] for sort_mode in [False,True] for separators in [(',',':'),None]]
        check('semantic object hash '+ident+field,item['semantic_object_sha256'] in {SH(s) for s in serializations})
for item in r['input_bindings']:
    p=Path(item['path'])
    check('full input hash and lengths '+p.name,H(p)==item['full_byte_sha256'] and p.stat().st_size==item['byte_length'] and len(p.read_text())==item['character_length'])
total=0
for item in l['files']:
    p=Path(item['path']);text=p.read_text();check('ledger full source '+p.name,H(p)==item['full_byte_sha256'] and len(text)==item['character_length'] and item['read_completely'] is True)
    position=0
    for part in item['slices']:
        start,end=part['range']
        check('contiguous complete literal source slice',start==position and 0<end-start<=6000 and SH(text[start:end])==part['slice_utf8_sha256'] and part['truncated'] is False)
        position=end;total+=1
    check('entire source delivered '+p.name,position==len(text))
check('12 whole inputs164 ranges',len(l['files'])==12 and total==l['unique_slice_count']==164 and l['tool_output_cap_tokens']>=4000 and l['truncated_ranges']==[])
for ev in r['evidence']:
    p=Path(ev['path']);start,end=ev['unicode_character_range'];text=p.read_text()
    check('literal primary citation '+ev['id'],H(p)==ev['full_byte_sha256'] and text[start:end]==ev['quotation'] and SH(ev['quotation'])==ev['utf8_passage_sha256'])
for image in v['images']:
    p=Path(image['path'])
    with Image.open(p) as im:check('original image source '+image['id'],H(p)==image['full_byte_sha256'] and list(im.size)==image['native_dimensions']==image['delivered_dimensions'])
    check('entire original image viewed '+image['id'],image['view_detail']=='original' and image['whole_original_delivered'] and image['viewed_region_xyxy']==[0,0,*image['native_dimensions']])
    for transcription in image['transcriptions']:check('normalized transcription hash '+image['id'],SH(transcription['text'])==transcription['utf8_sha256'])
check('both full19419092byte Bringer panels',len([x for x in v['images'] if x['native_dimensions']==[2697,1797] and Path(x['path']).stat().st_size==19419092])==2)
actual=load(S/'actual-delivery-validation.json')
check('actual complete source and visual delivery',actual['verified'] and actual['text_sources']==12 and actual['actual_distinct_text_range_deliveries']==164 and actual['unique_visual_sources']==8 and actual['public_image_blocks']==8)
check('actual per-range token caps',all(x['associated_public_call']['numeric_cap_candidates'] and min(x['associated_public_call']['numeric_cap_candidates'])>=4000 for x in actual['text_deliveries']))
check('preserved reachability/inspection limits',[(x['status']) for x in r['unresolved_issues']]==['UNVERIFIED','UNVERIFIED','NOT_INSPECTED_BY_DESIGN'])
proof={'all_passed':True,'checks':checks,'counts':{'checks':len(checks),'blocking_failed_checks':0,'proposal_decisions':4,'accepted_new_procedures':1,'minimum_new_required_facts':2,'text_sources':12,'literal_ranges':164,'original_visuals':8,'native_panels':2,'literal_primary_citations':len(r['evidence'])},'frozen_artifact_sha256':{n:H(S/n) for n in ['report.json','read-ledger.json','visual-manifest.json','actual-delivery-validation.json']},'limits':'Machine checks bind source references and normalized transcription hashes; they do not independently OCR or verify every transcribed word, cognition, or whole-corpus saturation. Two unsupported producer limits remain candidly unverified and fully graded.'}
dest=S/'structural-reference-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'all_passed':True,'counts':proof['counts']}))
