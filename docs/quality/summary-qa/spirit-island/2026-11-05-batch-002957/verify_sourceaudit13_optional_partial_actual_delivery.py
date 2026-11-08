"""Match only public source-delivery payloads; never retain private runtime bodies."""
from pathlib import Path
import base64
import hashlib
import json
import re

B = Path(__file__).resolve().parent
ROOT = B.parents[4]
H = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(Path(p).read_text())
profile = load(B / 'runtime/final_source_audit_13-initial-projection.json')
archive_ledger=load(B/'source-audit13-optional-partial-read-ledger.json')
ledger={'deliveries':archive_ledger['actual_new_text_deliveries']}
visual={'visual_sources':archive_ledger['new_original_detail_image_views']}
def public_strings(value):
    if isinstance(value,str):return [value]
    if isinstance(value,dict):return [s for x in value.values() for s in public_strings(x)]
    if isinstance(value,list):return [s for x in value for s in public_strings(x)]
    return []
calls, outputs, images = {}, [], []
original_boundary=load(B/'source-audit13-original-completed-runtime-boundary.json')
session=Path(profile['session_path']);assert str(session)==original_boundary['session_path']
with session.open('rb') as stream:
    assert H(stream.read(original_boundary['prefix_bytes']))==original_boundary['prefix_sha256']
prefix=session.read_bytes();boundary={'session_path':str(session),'record_count':len(prefix.splitlines()),'prefix_bytes':len(prefix),'prefix_sha256':H(prefix),'lower_record_boundary_inclusive':original_boundary['record_count']}
for ordinal,line in enumerate(session.open('rb')):
    if ordinal>=boundary['record_count']:break
    if ordinal<boundary['lower_record_boundary_inclusive']:continue
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

image_receipts = [];used_images=set()
for visual_index, view in enumerate(visual['visual_sources']+archive_ledger['extra_diagnostic_derivative_views']):
    path = ROOT / view['path'];digest=H(path.read_bytes())
    assert digest == view.get('source_sha256',view.get('sha256')) if visual_index<len(visual['visual_sources']) else digest==view['sha256']
    matches=[x for x in images if x['displayed_bytes_sha256']==digest and x['detail']=='original' and (x['event_ordinal'],x['public_block_index']) not in used_images]
    assert matches,(visual_index,view['path'],'new original-detail payload absent')
    chosen=matches[0];used_images.add((chosen['event_ordinal'],chosen['public_block_index']))
    image_receipts.append({'id':visual_index,'path':view['path'],'sha256':digest,'diagnostic_derivative':visual_index>=len(visual['visual_sources']),'public_image_delivery':chosen})

assert len(receipts)==len(ledger['deliveries'])==len(used)
assert len(image_receipts)==len(visual['visual_sources'])+1==35
proof={'verified_partial_transport_only':True,'status':'PARTIAL_ADDITIONAL_VERIFICATION_NOT_COMPLETED','completed_additional_audit_or_vote':False,'runtime_boundary':boundary,'original_boundary_excluded':True,'text_ranges':len(receipts),'one_source_range_per_output':True,'text_deliveries':receipts,'original_detail_primary_views':34,'distinct_primary_faces':len({x['path'] for x in visual['visual_sources']}),'diagnostic_derivative_views':1,'image_receipts':image_receipts,'no_private_runtime_bodies_copied':True,'limitations':'Only exact recorded partial deliveries verified. No completed additional source judgment or vote; initial evidence is separately accepted original evidence.'}
dest=B/'source-audit13-optional-partial-actual-delivery-validation.json';assert not dest.exists();dest.write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps({'path':str(dest),'sha256':H(dest.read_bytes()),'text_ranges':len(receipts),'primary_views':34,'diagnostic_views':1,'verified_partial_transport_only':True}))
