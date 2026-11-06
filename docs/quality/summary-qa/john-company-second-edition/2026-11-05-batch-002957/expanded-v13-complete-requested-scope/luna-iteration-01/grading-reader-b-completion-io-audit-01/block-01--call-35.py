from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-01/grading-reader-b/block-01')
path=base/'grades-same-entry.json'
data=json.loads(path.read_text())
packet=json.loads((base/'packet.json').read_text())
byid={x['id']:x for x in data['readers']['reader-b']['grades']}
extra={
'Q012':{11:['Turn it region-symbol side up and put it **ABOVE THE ASSOCIATED PRESIDENT\'S BOX**.','Steps 3a–3c form a new Governorship only if the target was not already Company-controlled.']},
'Q014':{8:['Standing reaching leftmost space means Company failure. During Revenue, go immediately to Final Scoring.'],10:['Standing reaching leftmost space means Company failure. During Revenue, go immediately to Final Scoring.']},
'Q015':{5:['normal Invasion/Rebellion attack strength **plus unrest in its target region**.'],6:['normal Invasion/Rebellion attack strength **plus unrest in its target region**.']},
'Q019':{0:['Managers select their strategy simultaneously and secretly:','Trade zone/home port | Commit a secret cash bid from London treasury.'],6:['matching firms reveal strategy and roll one die per committed £1, paying bid to bank.']}
}
for entry in packet['entries']:
 qid=entry['id']
 if qid not in extra: continue
 reader=entry['reader_b_entry']
 candidates=[reader['answer']]+[x['supported_fact_or_case_result'] for x in reader.get('clause_ledger',[])]+reader.get('case_conclusions',[])+[x['quote'] for x in reader.get('evidence',[])]
 for index,quotes in extra[qid].items():
  for quote in quotes:
   assert any(quote in candidate for candidate in candidates),(qid,quote)
   byid[qid]['material_parts'][index]['reader_quotes'].append(quote)
encoded=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
path.write_text(encoded)
print(json.dumps({'path':str(path),'count':len(byid),'sha256':hashlib.sha256(encoded.encode()).hexdigest()}))