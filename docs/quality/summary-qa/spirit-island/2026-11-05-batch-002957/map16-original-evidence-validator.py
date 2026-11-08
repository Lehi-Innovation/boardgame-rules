"""Safe post-freeze proof: bytes/objects plus separately labeled attestations."""
import copy
import hashlib
import json
from pathlib import Path
from PIL import Image

B=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/spirit-island/2026-11-05-batch-002957')
FROZEN=Path('/tmp/map-adjudication16-frozen-hashes.json')
PROOF=Path('/tmp/map-adjudication16-evidence-proof.json')
checks=[];counts={}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def hs(s):return hashlib.sha256(s.encode()).hexdigest()
def obj(p):return json.loads(Path(p).read_text())
def check(name,condition,kind='filesystem_object',detail=None):
    row=dict(check=name,kind=kind,ok=bool(condition))
    if detail is not None:row['detail']=detail
    checks.append(row)
def slices(row,label):
    p=Path(row['path']);text=p.read_text();check(label+':file_hash',sha(p)==row['original_byte_sha256']);check(label+':unicode_length',len(text)==row['character_length']);end=0
    for i,part in enumerate(row['slices']):
        a,z=part['range'];check(f'{label}:{i}:contiguous_bounds',a==end and 0<=a<z<=len(text) and z-a<=6000);check(f'{label}:{i}:slice_hash',hs(text[a:z])==part['slice_utf8_sha256']);check(f'{label}:{i}:recorded_cap_truncation',part['output_cap_tokens']>=4000 and part['truncated'] is False,'historical_receipt_attestation');end=z
    check(label+':complete',end==len(text) and row['contiguous_complete'] is True)
    return len(row['slices'])
def covered(a,z,intervals):
    end=a
    for lo,hi in sorted(intervals):
        if hi<=end:continue
        if lo>end:return False
        end=hi
        if end>=z:return True
    return False
def run():
    freeze=obj(FROZEN)
    for path,expected in freeze['outputs'].items():check('frozen_output:'+path,sha(path)==expected)
    for path,expected in freeze['original_inputs'].items():check('preserved_input:'+path,sha(path)==expected)
    check('helper_frozen_hash',sha(__file__)==freeze['helper']['sha256'])
    report=obj(B/'working-map-adjudication-16.json');ledger=obj(B/'working-map-adjudication-16-read-ledger.json');packet=obj(B/'working-map-adjudication16-input.json')
    counts['new_complete_text_files']=len(ledger['new_complete_text_inputs']);counts['new_complete_slices']=sum(slices(x,'new:'+x['path']) for x in ledger['new_complete_text_inputs'])
    original_rows={};old_count=0
    for i,reuse in enumerate(ledger['own_exact_complete_primary_source_delivery_reuse']):
        check(f'reuse{i}:ledger_hash',sha(reuse['original_ledger_path'])==reuse['original_ledger_sha256']=='eca65d91d99ba2a1934cc6e35bed43a7de60e627335a24cf99178bd65c77a546')
        row=reuse['original_complete_delivery_row'];check(f'reuse{i}:exact_original_row',row in obj(reuse['original_ledger_path'])['text_files']);old_count+=slices(row,'reused:'+row['path']);original_rows[row['path']]=row
    counts['reused_complete_source_slices']=old_count
    intervals={}
    for i,row in enumerate(ledger['targeted_primary_rereads']):
        text=Path(row['path']).read_text();a,z=row['range'];check(f'targeted{i}:source_binding',row['path'] in original_rows and sha(row['path'])==row['original_byte_sha256']==original_rows[row['path']]['original_byte_sha256']);check(f'targeted{i}:bounds_hash',0<=a<z<=len(text)==row['character_length'] and z-a<=6000 and hs(text[a:z])==row['slice_utf8_sha256']);check(f'targeted{i}:recorded_cap_truncation',row['output_cap_tokens']>=4000 and row['truncated'] is False,'historical_receipt_attestation');intervals.setdefault(row['path'],[]).append([a,z])
    counts['targeted_primary_slices']=len(ledger['targeted_primary_rereads']);check('total_recorded_slices',ledger['total_successful_text_slices']==counts['new_complete_slices']+counts['targeted_primary_slices'])
    for i,entry in enumerate(ledger['operative_primary_passages']):
        text=Path(entry['path']).read_text();a,z=entry['character_range'];check(f'operative{i}:source_range_text_hash',sha(entry['path'])==entry['original_byte_sha256'] and 0<=a<z<=len(text) and text[a:z]==entry['complete_operative_passage'] and hs(text[a:z])==entry['passage_utf8_sha256']);check(f'operative{i}:freshly_received_range',covered(a,z,intervals[entry['path']]))
    counts['operative_primary_passages']=len(ledger['operative_primary_passages'])
    legend=ledger['own_membership_legend_reuse'];old=obj(legend['original_ledger_path']);check('legend_exact_old_row',sha(legend['original_ledger_path'])==legend['original_ledger_sha256'] and legend['exact_original_image_row'] in old['image_files']);check('legend_immutable_image',sha(legend['exact_original_image_row']['path'])==legend['exact_original_image_row']['original_byte_sha256'])
    for i,image in enumerate(ledger['fresh_native_image_views']):
        w,h=Image.open(image['path']).size;a,b,c,d=image['relevant_region_xyxy'];check(f'image{i}:file_dimensions_bounds',sha(image['path'])==image['original_byte_sha256'] and [w,h]==image['dimensions'] and image['viewed_region_xyxy']==[0,0,w,h] and 0<=a<c<=w and 0<=b<d<=h);check(f'image{i}:transcription_hash',hs(image['complete_printed_transcription'])==image['transcription_utf8_sha256']);check(f'image{i}:full_view_attestation',image['full_native_view'] is True and image['view_detail']=='original','historical_perception_attestation','Hashes/bounds do not independently prove image-tool delivery or glyph recognition.')
    counts['fresh_native_view_records']=len(ledger['fresh_native_image_views'])
    asks=[json.loads(x) for x in Path(ledger['all172_input']['path']).read_text().splitlines() if x.strip()];check('full_projection_hash',sha(ledger['all172_input']['path'])==ledger['all172_input']['sha256']=='da563decae399ab5e21d688d0a4a40f2cb1f4a2930b26523ac271503e7564526');check('all172_ordered_IDs',[x['id'] for x in asks]==[f'Q{i:02d}' for i in range(1,173)]);count=lambda rows:sum(len(c['required_facts']) for q in rows for c in q['requested_clauses']);check('507_original_indices',count(asks)==507)
    byid={x['id']:x for x in asks};selected=packet['selected_complete_objects'];maps={x['id']:x for x in selected['asked-fact-map.json']};qs={x['id']:x for x in selected['questions.json']};ks={x['id']:x for x in selected['answer-key.json']}
    for ident,mapping in maps.items():check('selected_projection_exact:'+ident,byid[ident]['question']==mapping['question']==qs[ident]['question'] and byid[ident]['requested_clauses']==mapping['requested_clauses'])
    edited=copy.deepcopy(asks)
    for i,decision in enumerate(report['decisions']):
        ident=decision['question_id'];oldmap=decision['complete_old_map_entry'];newmap=decision['complete_proposed_new_map_entry'];index=3 if ident=='Q09' else 0;proposal=packet['complete_proposals'][i];check(f'decision{i}:exact_original_proposal',decision['complete_original_proposal']==proposal);check(f'decision{i}:exact_old_map',oldmap==maps[ident]);check(f'decision{i}:key_preserved',decision['complete_old_fixed_key']==decision['complete_proposed_fixed_key']==ks[ident]);check(f'decision{i}:question_preserved',decision['complete_old_question']==decision['complete_proposed_question']==qs[ident]);check(f'decision{i}:exact_proposed_required_string',newmap['requested_clauses'][0]['required_facts'][index]==proposal['correction']['required_fact']);check(f'decision{i}:exact_context_fact',newmap['key_context_not_required'][-1]['fact']==proposal['correction']['move_to_key_context_not_required'])
        restored=copy.deepcopy(newmap);restored['requested_clauses'][0]['required_facts'][index]=oldmap['requested_clauses'][0]['required_facts'][index];restored['key_context_not_required'].pop();check(f'decision{i}:only_target_string_plus_context_edit',restored==oldmap);check(f'decision{i}:fact_index_entry_count_preserved',len(newmap['requested_clauses'][0]['required_facts'])==len(oldmap['requested_clauses'][0]['required_facts']))
        for row in edited:
            if row['id']==ident:row['requested_clauses']=copy.deepcopy(newmap['requested_clauses'])
    counts['questions']=len(asks);counts['fact_index_entries_before']=count(asks);counts['fact_index_entries_after']=count(edited);check('172_507_counts_preserved',len(edited)==172 and count(edited)==507);check('two_separate_proposals',len(report['decisions'])==report['complete_proposal_count']==2);check('declared_no_whole_bank_access',ledger['whole_current_bank_files_opened'] is False,'historical_access_attestation')
    for path,expected in freeze['outputs'].items():check('output_unchanged_after_proof:'+path,sha(path)==expected)
    for path,expected in freeze['original_inputs'].items():check('input_unchanged_after_proof:'+path,sha(path)==expected)
try:run()
except Exception as e:check('helper_exception',False,detail=f'{type(e).__name__}: {e}')
failures=[x for x in checks if not x['ok']]
result=dict(task='Post-freeze source/input/object evidence proof only; no new semantic review',status='VALID_FOR_RECORDED_EVIDENCE' if not failures else 'EVIDENCE_FAILURES',helper_path=__file__,helper_sha256=sha(__file__),frozen_manifest_path=str(FROZEN),frozen_manifest_sha256=sha(FROZEN),frozen_outputs=obj(FROZEN)['outputs'],check_count=len(checks),filesystem_object_checks=sum(x['kind']=='filesystem_object' for x in checks),historical_attestation_checks=sum(x['kind']!='filesystem_object' for x in checks),counts=counts,exceptions=failures,checks=checks,proof_boundary='Byte hashes, ranges, object edits and counts are verified. Historical receipt caps/truncation, source receipt and image viewing/recognition remain explicitly labeled attestations. Whole current bank files were not opened; object equivalence is against the fully received packet/projection only.')
PROOF.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(dict(status=result['status'],checks=len(checks),filesystem_object_checks=result['filesystem_object_checks'],historical_attestation_checks=result['historical_attestation_checks'],exceptions=len(failures),counts=counts,proof_path=str(PROOF),proof_sha256=sha(PROOF),helper_sha256=sha(__file__),frozen_outputs=result['frozen_outputs'])))
raise SystemExit(0 if not failures else 1)
