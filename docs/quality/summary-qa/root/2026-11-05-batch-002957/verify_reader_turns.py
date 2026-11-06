from build_evidence import *
import sys
I=R/sys.argv[1]
provenance=json.loads((I/'model-provenance.json').read_text())
records=[]
for reader in provenance['readers']:
 contexts=[]
 for line in Path(reader['runtime_path']).open():
  event=json.loads(line)
  if event.get('type')=='turn_context':
   payload=event['payload'];contexts.append({'timestamp':event['timestamp'],'ordinal':event.get('ordinal'),'turn_id':payload.get('turn_id'),'model':payload.get('model'),'effort':payload.get('effort')})
 records.append({'agent_path':reader['agent_path'],'session_id':reader['session_id'],'runtime_path':reader['runtime_path'],'turn_contexts':contexts,'all_turn_settings_confirmed':bool(contexts) and all(x['model']=='gpt-6-luna' and x['effort']=='high' for x in contexts)})
save(I/'reader-turn-provenance.json',{'status':'PASS' if len(records)==2 and all(x['all_turn_settings_confirmed'] for x in records) else 'UNCONFIRMED','method':'All actual turn_context records from the two reader sessions, including operational resumptions. No message or reasoning content used.','readers':records})
print([(r['agent_path'],len(r['turn_contexts']),r['all_turn_settings_confirmed']) for r in records])
