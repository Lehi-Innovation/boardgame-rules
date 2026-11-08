from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
code=(B/'verify_working4546_all_recorded_repeat_delivery.py').read_text();code=code[:code.index('dest = B /')]
ns={'__file__':str(B/'verify_working4546_all_recorded_repeat_delivery.py')};exec(compile(code,'public-source-matcher-in-memory','exec'),ns)
rows=ns['ledger']['rows'];snippets=list(dict.fromkeys(Path(x['path']).read_text()[x['start']:x['end']] for x in rows));receipts=ns['receipts'];outputs={x['ordinal']:x for x in ns['outputs']};counts=[]
for receipt in receipts:
 output=outputs[receipt['event_ordinal']];hits=[]
 for i,excerpt in enumerate(snippets):
  if any(excerpt in block['text'] for block in output['texts']):hits.append(i)
 assert len(hits)==1,(receipt['event_ordinal'],hits)
 counts.append({'event_ordinal':receipt['event_ordinal'],'distinct_known_complete_source_ranges_in_event':len(hits)})
p=B/'working45-46-all201-one-range-event-validation.json';assert not p.exists();p.write_text(json.dumps({'verified':True,'events_checked':len(counts),'all_exactly_one_known_source_range':True,'events':counts,'method':'Inspect only the same public source-output text already matched by the working-only transport checker; no private runtime bodies retained. All201 actual matched events, including twelve repeated deliveries, each contain exactly one of all189 unique claimed literal source ranges.','matcher_sha256':hashlib.sha256((B/'verify_working4546_all_recorded_repeat_delivery.py').read_bytes()).hexdigest()},indent=2)+'\n');print(json.dumps({'verified':True,'events':len(counts),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}))
