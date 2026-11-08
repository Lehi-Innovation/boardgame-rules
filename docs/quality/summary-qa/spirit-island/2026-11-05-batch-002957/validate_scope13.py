"""Bind the complete review13 PASS/FAIL judgments to actual current inputs."""
from pathlib import Path
import collections
import hashlib
import json
from PIL import Image
from bs4 import BeautifulSoup

B=Path(__file__).resolve().parent
ROOT=B.parents[4]
load=lambda p:json.loads(Path(p).read_text())
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
SH=lambda text:hashlib.sha256(text.encode()).hexdigest()
k,c,l=[load(B/n) for n in ['question-key-scope-review-13.json','coverage-review-13.json','scope-coverage-13-read-ledger.json']]
q,key,f,scope=[load(B/'expanded-v23'/n) for n in ['questions.json','answer-key.json','asked-fact-map.json','core-scope-credit.json']]
checks=[]
def check(label,condition):
    assert condition,label
    checks.append({'name':label,'passed':True})
freeze=load(B/'scope13-original-freeze.json')
for name,data in freeze['files'].items():check('original raw freeze '+name,H(B/name)==data['sha256'])
ids=[x['id'] for x in q['questions']]
for report in [k,c]:
    check('all172 checked IDs and504 facts',report['checked_ids']==ids and report['checked_question_count']==172 and report['required_fact_count_checked']==504)
    check('reported key and map PASS',report['fixed_key_verdict']==report['asked_fact_mapping_verdict']=='PASS' and not report['fixed_key_findings'] and not report['asked_fact_mapping_findings'] and not report['missing_truly_asked_facts_in_map'] and not report['missing_truly_asked_facts_in_fixed_key'])
    check('current asked map hash',report['asked_fact_map_sha256']==H(B/'expanded-v23/asked-fact-map.json'))
    check('exact linked full ledger',report['read_evidence']['sha256']==H(Path(report['read_evidence']['ledger_path']))==H(B/'scope-coverage-13-read-ledger.json'))
    for path,digest in report['input_hashes'].items():check('review input hash '+Path(path).name,H(B/path)==digest)
check('whole corpus and stopping FAIL preserved',c['verdict']==c['coverage_verdict']==c['stopping_verdict']=='FAIL' and c['remaining_gap_count']==len(c['remaining_gaps'])==1 and len(c['coverage_map_classification_findings'])==3)
check('all checked judgments identical in both reports',k['checked_questions']==c['checked_questions'])
maps={x['id']:x for x in f['questions']}
keys={x['id']:x for x in key['answers']}
scopes={x['id']:x for x in scope['questions']}
fact_count=0
for question,row in zip(q['questions'],k['checked_questions']):
    ident=question['id'];check('literal question/key bindings '+ident,row['id']==ident and row['literal_question_sha256']==SH(question['question']) and row['fixed_answer_sha256']==SH(keys[ident]['answer']))
    expected={(clause['clause_id'],i):text for clause in maps[ident]['requested_clauses'] for i,text in enumerate(clause['required_facts'])}
    facts=row['fact_checks']
    check('every required fact once '+ident,len(facts)==row['required_fact_count']==len(expected) and {(x['clause_id'],x['fact_index']) for x in facts}==set(expected))
    for fact in facts:
        check('exact mapped fact hash',fact['fact_sha256']==SH(expected[fact['clause_id'],fact['fact_index']]))
        check('explicit independent per-fact PASS',fact['literal_ask_fit']==fact['primary_source_correctness']==fact['fixed_key_semantic_support']=='PASS');fact_count+=1
    check('question context and scope judgment '+ident,row['fixed_key_verdict']==row['asked_fact_mapping_verdict']=='PASS' and row['context_boundary_checked'] is True and row['scope_result_independently_validated']==scopes[ident]['scope_result'])
check('all504 fact judgments checked',fact_count==504)
check('unchanged155/14/3 eligible question classes',dict(collections.Counter(x['scope_result_independently_validated'] for x in k['checked_questions']))=={'base_supported':155,'mixed_supported_and_noncredited':14,'noncredited_pending_base_proof':3})
by_path=collections.defaultdict(list)
for row in l['text_reads']:
    p=ROOT/row['path'];text=p.read_text();start,end=row['range']
    check('source/range literal hash',H(p)==row['full_byte_sha256'] and len(text)==row['character_length'] and 0<end-start<=6000 and SH(text[start:end])==row['utf8_slice_sha256'] and row['truncation'] is False)
    if row['received_and_read'] and not row['duplicate_not_relied_upon']:by_path[row['path']].append(row)
check('11 uncertain copies candidly unrelied upon',sum(x['duplicate_not_relied_upon'] and not x['received_and_read'] for x in l['text_reads'])==11)
full_partition_rows=0
for path,rows in by_path.items():
    text=(ROOT/path).read_text();position=0
    while position<len(text):
        choices=[r for r in rows if r['range'][0]==position]
        check('next full contiguous source slice '+Path(path).name,bool(choices))
        selected=max(choices,key=lambda x:x['range'][1]);position=selected['range'][1];full_partition_rows+=1
    check('complete relied range coverage '+Path(path).name,position==len(text))
check('22 complete texts228 relied ranges',len(by_path)==22 and sum(len(x) for x in by_path.values())==228)
actual=load(B/'scope13-actual-delivery-validation.json')
check('actual22 texts228 ranges53 original visuals',actual['verified'] and actual['text_sources']==22 and actual['actual_distinct_text_range_deliveries']==228 and actual['unique_visual_sources']==53)
check('actual public token caps for every relied range',all(x['associated_public_call']['numeric_cap_candidates'] and min(x['associated_public_call']['numeric_cap_candidates'])>=4000 for x in actual['text_deliveries']))
latest=[];native_latest=[]
for row in l['image_reads']:
    p=ROOT/row['path']
    with Image.open(p) as im:check('native source image hash/dimensions',H(p)==row['full_byte_sha256'] and list(im.size)==row['native_dimensions'])
    check('full original image declaration',row['view_detail']=='original' and row['fully_viewed'] is True)
    delivered=next(x for x in actual['visuals'] if (ROOT/x['path']).resolve()==p.resolve())['public_image_deliveries']
    check('later complete native image delivery',bool(delivered) and delivered[-1]['detail']=='original' and delivered[-1]['displayed_bytes_sha256']==row['full_byte_sha256'])
    latest.append(delivered[-1])
    if row['native_dimensions']==[2697,1797]:native_latest.append(delivered[-1])
check('16 full native panels',sum(x['native_dimensions']==[2697,1797] and (ROOT/x['path']).stat().st_size==19419092 for x in l['image_reads'])==16)
check('16 distinct final native-panel delivery events',len({x['event_ordinal'] for x in native_latest})==16)
publisher=Path('/tmp/scope13-publisher-branch-claw-visible.txt')
html=Path(l['protocol']['derived_publisher_visible_prose']['input_path']);soup=BeautifulSoup(html.read_text(),'html.parser')
for tag in soup(['script','style','template']):tag.decompose()
check('complete independent publisher visible prose',soup.get_text('\n',strip=True)==publisher.read_text()==l['protocol']['derived_publisher_visible_prose']['entire_visible_prose'])
proposals=load(B/'novelty-adjudication-18/proposals.json')
for field,value in proposals['proposed_set'].items():check('complete proposal set '+field,c[field]==value)
proof={'all_passed':True,'checks':checks,'counts':{'checks':len(checks),'blocking_failed_checks':0,'questions':172,'mapped_fact_entries':504,'complete_text_sources':22,'relied_literal_ranges':228,'full_contiguous_partition_ranges':full_partition_rows,'additional_focused_source_reopens':228-full_partition_rows,'uncertain_unrelied_duplicate_rows':11,'visual_sources':53,'public_image_blocks':actual['public_image_blocks'],'native_panels':16},'latest_relied_image_event_receipts':latest,'frozen_artifact_sha256':{n:H(B/n) for n in ['question-key-scope-review-13.json','coverage-review-13.json','scope-coverage-13-read-ledger.json','scope13-actual-delivery-validation.json']},'limitations':'Source delivery/reference/structural checks preserve semantic FAIL. They prove recorded transport, not cognition or universal completeness. New procedural gap requires independent adjudication before any bank addition.'}
dest=B/'scope13-structural-reference-validation.json'
assert not dest.exists()
dest.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'all_passed':True,'counts':proof['counts']}))
