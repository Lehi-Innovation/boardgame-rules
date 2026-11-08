"""Strict NEW own-C28 source text delivery only; prior evidence is explicitly reused."""
from pathlib import Path
import base64, hashlib, json, re
B=Path(__file__).resolve().parent
ROOT=B.parents[4]
H=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_text())
profile=load(B/'runtime/final_source_audit_15-C28-followup-final-completed-projection.json')
assert profile['confirmed_settings']==[{'model':'gpt-6.1-sol','effort':'high'}]*4
assert profile['requested_spawn']['fields']['fork_turns']=='none'
rawledger=load(B/'source-audit15-current-body-C28-followup-read-view-ledger.json')
ledger={'deliveries':rawledger['actual_new_text_deliveries']}
freeze=load(B/'source-audit15-C28-followup-original-completed/original-freeze.json')
boundary={'session_path':freeze['external_runtime_path'],'record_count':freeze['runtime_records_at_completed_freeze'],'new_record_start_inclusive':811}
assert profile['session_path']==boundary['session_path']
def public_strings(value):
    if isinstance(value,str):return [value]
    if isinstance(value,dict):return [s for x in value.values() for s in public_strings(x)]
    if isinstance(value,list):return [s for x in value for s in public_strings(x)]
    return []
calls, outputs, images = {}, [], []
for ordinal, line in enumerate(Path(profile['session_path']).open('rb')):
    if ordinal>=boundary['record_count']:break
    if ordinal<boundary['new_record_start_inclusive']:continue
    record = json.loads(line)
    if record.get('type') != 'response_item':
        continue
    p = record.get('payload', {})
    if p.get('type') == 'custom_tool_call':
        code = p.get('input', '')
        caps = [int(x) for x in re.findall(r'''max_output_tokens["'\s]*[:=]\s*(\d+)''', code)] if isinstance(code, str) else []
        calls[p.get('call_id', p.get('id'))] = {'ordinal': ordinal, 'record_sha256': H(line), 'numeric_cap_candidates': caps}
    elif p.get('type') == 'custom_tool_call_output':
        raw = p.get('output')
        blocks = [{'type': 'input_text', 'text': raw}] if isinstance(raw, str) else raw if isinstance(raw, list) else []
        texts = []
        for index, block in enumerate(blocks):
            if not isinstance(block, dict):
                continue
            if block.get('type') == 'input_image':
                url = block.get('image_url')
                assert isinstance(url, str) and url.startswith('data:') and ';base64,' in url
                encoded = url.split(';base64,', 1)[1]
                payload = base64.b64decode(encoded, validate=True)
                images.append({'event_ordinal': ordinal, 'record_sha256': H(line), 'public_block_index': index, 'displayed_bytes_sha256': H(payload), 'displayed_bytes': len(payload), 'detail': block.get('detail')})
                continue
            if block.get('type') != 'input_text' or not isinstance(block.get('text'), str):
                continue
            text = block['text']
            original_sha = H(text.encode())
            decoded_layers = []
            other_public_string_fields=[]
            for unused in range(4):
                try:
                    obj = json.loads(text)
                except (ValueError, TypeError):
                    break
                if isinstance(obj, dict) and obj.get('status') == 'fulfilled' and isinstance(obj.get('value'), dict):
                    other_public_string_fields.extend(public_strings({k:v for k,v in obj.items() if k!='value'}))
                    obj = obj['value']
                    decoded_layers.append('public fulfilled/value result')
                if isinstance(obj,dict):
                    primary='output' if isinstance(obj.get('output'),str) and {'chunk_id','exit_code'}.issubset(obj) else 'text' if isinstance(obj.get('text'),str) else 'content' if isinstance(obj.get('content'),str) and isinstance(obj.get('range'),list) else None
                    if primary:other_public_string_fields.extend(public_strings({k:v for k,v in obj.items() if k!=primary}))
                    if primary=='content':obj={**obj,'text':obj['content']}
                if isinstance(obj, dict) and isinstance(obj.get('output'), str) and {'chunk_id', 'exit_code'}.issubset(obj):
                    text = obj['output']
                    decoded_layers.append('public exec result output')
                elif isinstance(obj, dict) and isinstance(obj.get('text'), str):
                    text = obj['text']
                    decoded_layers.append('public source text field')
                else:
                    break
            texts.append({'block_index': index, 'original_block_sha256': original_sha, 'decoded_layers': decoded_layers, 'text': text, 'other_public_string_fields':other_public_string_fields})
        outputs.append({'ordinal': ordinal, 'record_sha256': H(line), 'call_id': p.get('call_id'), 'texts': texts})

used, receipts = set(), []
known_snippets=[(ROOT/x['path']).read_text()[x['start']:x['end']] for x in ledger['deliveries']]
for row in ledger['deliveries']:
    path = (ROOT / row['path']).resolve()
    source = path.read_text()
    assert H(path.read_bytes()) == row['source_sha256']
    start, end = row['start'], row['end']
    excerpt = source[start:end]
    assert 0 < end - start <= 6000 and H(excerpt.encode()) == row['slice_sha256']
    choices = []
    for output in outputs:
        if output['ordinal'] in used:
            continue
        call = calls.get(output['call_id'], {})
        caps = call.get('numeric_cap_candidates', [])
        if not caps or min(caps) < 4000:
            continue
        for block in output['texts']:
            if excerpt in block['text'] and not any(x in block['text'] for x in ['Warning: truncated output', 'Output exceeded the available model context', 'Output exceeded available model context']):
                residual=[x['text'].replace(excerpt,'',1) for x in output['texts']]+[s for x in output['texts'] for s in x.get('other_public_string_fields',[])]
                if any(snippet in text for snippet in known_snippets for text in residual):continue
                if any(excerpt in snippet and snippet!=excerpt and snippet in x['text'] for snippet in known_snippets for x in output['texts']):continue
                choices.append({'path': row['path'], 'range': [start, end], 'slice_sha256': row['slice_sha256'], 'event_ordinal': output['ordinal'], 'record_sha256': output['record_sha256'], 'public_block_index': block['block_index'], 'original_public_block_sha256': block['original_block_sha256'], 'losslessly_decoded_public_layers': block['decoded_layers'], 'associated_public_call': call})
    assert choices, (row['path'], start, end)
    chosen = choices[-1]
    used.add(chosen['event_ordinal'])
    receipts.append(chosen)


assert len(receipts)==len(ledger['deliveries'])==13
assert len(used)==13
assert len(images)==len(rawledger['actual_new_views'])==2
image_receipts=[]
image_events=set()
for view in rawledger['actual_new_views']:
    path=(ROOT/view['path']).resolve()
    assert H(path.read_bytes())==view['source_sha256']
    assert view['requested_detail']==view['forwarded_detail']=='original' and view['entire_image_actually_received']
    candidates=[i for i in images if i['displayed_bytes_sha256']==view['source_sha256'] and i['detail']=='original' and i['event_ordinal'] not in image_events]
    assert candidates, ('native full original image not matched',view['path'])
    chosen=candidates[0]
    image_events.add(chosen['event_ordinal'])
    image_receipts.append({'path':view['path'],'source_sha256':view['source_sha256'],'actual_native_payload':chosen})
assert len(image_events)==2
current=[r for r in ledger['deliveries'] if (ROOT/r['path']).resolve()==(B/'source-candidate-28.md').resolve()]
assert len(current)==10 and current[0]['start']==0 and current[-1]['end']==55813 and all(x['end']==y['start'] for x,y in zip(current,current[1:]))
assert all(r['output_cap']>=4000 and not r['truncated'] for r in ledger['deliveries'])
proof={'verified':True,'same_original_pure_auditor_not_fresh_vote':True,'actual_contexts':4,'new_record_interval':[811,boundary['record_count']],'new_candidate_whole_contiguous':True,'new_candidate_slices':10,'new_exact_primary_reopen_windows':1,'new_whole_own_derived_diff':1,'actual_new_text_deliveries':receipts,'actual_distinct_text_range_deliveries':len(used),'one_source_range_per_matched_output_event':True,'new_views':2,'actual_new_native_image_deliveries':image_receipts,'prior_full_authority_perception_not_claimed_anew':True,'frozen_originals':freeze['originals'],'model_profile_sha256':H((B/'runtime/final_source_audit_15-C28-followup-final-completed-projection.json').read_bytes()),'private_runtime_bodies_copied':False,'limitations':'Only new public literal source outputs in completed records [811,N) are matched. Prior whole-authority and image reading is reused explicitly, not reasserted as new delivery. This proves recorded delivery, not cognition or semantic accuracy.'}
p=B/'source-audit15-C28-followup-actual-delivery-validation.json'
assert not p.exists()
p.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'proof':str(p),'sha256':H(p.read_bytes()),'verified':True,'new_candidate_slices':10,'primary_reopens':1,'derived_diff':1,'new_single_range_events':13,'new_views':2,'actual_new_native_image_deliveries':image_receipts,'private_runtime_bodies_copied':False}))
