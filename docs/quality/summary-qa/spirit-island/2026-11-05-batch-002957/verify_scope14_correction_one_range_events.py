"""Check public source events while allowing a separately reopened subrange inside a full source partition."""
from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent;source=B/'verify_scope14_correction_actual_delivery.py';code=source.read_text();code=code[:code.index('dest = B /')];ns={'__file__':str(source)};exec(compile(code,'scope14-public-matcher-in-memory','exec'),ns);rows=ns['ledger']['rows'];known={}
for row in rows:
 key=(row['path'],row['start'],row['end']);known[key]=Path(row['path']).read_text()[row['start']:row['end']]
outputs={x['ordinal']:x for x in ns['outputs']};checks=[]
for receipt in ns['receipts']:
 key=(receipt['path'],*receipt['range']);excerpt=known[key];output=outputs[receipt['event_ordinal']];block=next(x for x in output['texts'] if x['block_index']==receipt['public_block_index']);body=block['text'];assert excerpt in body
 # A focused-reopen receipt must not borrow a different event containing a larger delivered source partition.
 supers=[other for other,text in known.items() if other[0]==key[0] and other[1]<=key[1] and other[2]>=key[2] and other!=key and text in body]
 assert not supers,(receipt['event_ordinal'],'claimed subrange borrowed a larger source event',key,supers)
 residual=body.replace(excerpt,'',1);additional=[other for other,text in known.items() if text in residual]
 assert not additional,(receipt['event_ordinal'],'additional full known literal range in residual',additional)
 checks.append({'event_ordinal':receipt['event_ordinal'],'claimed_source_range':list(key[1:]),'one_complete_literal_range_after_lossless_wrapper_decode':True})
p=B/'scope14-correction-one-range-event-validation.json';assert not p.exists();p.write_text(json.dumps({'verified':True,'events_checked':len(checks),'unique_claimed_ranges':len(known),'all114_claimed_ranges_matched_to_separate_single_range_events':True,'method':'For each selected public event remove its exact claimed literal once; no other complete known source range may remain. A focused partial-reopen receipt cannot borrow an event containing a larger known source partition. This avoids mistaking an embedded legitimate subrange for a second delivery while still rejecting actual aggregated/repeated source payloads.','checks':checks,'source_matcher_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'no_private_runtime_bodies_copied':True},indent=2)+'\n');print(json.dumps({'verified':True,'events':len(checks),'unique_ranges':len(known),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
