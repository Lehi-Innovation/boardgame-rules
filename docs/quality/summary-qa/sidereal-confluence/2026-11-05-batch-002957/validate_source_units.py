from pathlib import Path
import json,sys,hashlib
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'reader-protocol-v2'))
from source_units import validate_record
iteration=sys.argv[1];d=ROOT/iteration;s=(d/'summary-snapshot.md').read_text()
for reader in (sys.argv[2:] or ['a','b']):
 x=json.loads((d/f'reader-{reader}.json').read_text());checks=[];duplicates=[]
 for a in x['answers']:
  seen=set()
  for wrapped in a['evidence']:
   e=wrapped.get('record',wrapped)
   validate_record(s,e);u=e.get('unit',e.get('row'));span=(u['start'],u['end']);checks.append({'id':a['id'],'kind':e['kind'],'start':span[0],'end':span[1],'validated':True})
   if span in seen:duplicates.append({'id':a['id'],'span':span})
   seen.add(span)
 out={'reader':reader,'records_checked':len(checks),'all_match_complete_exact_supplied_helper_units':True,'duplicate_correct_literal_units':duplicates,'supplied_helper_sha256':hashlib.sha256((ROOT/'reader-protocol-v2/source_units.py').read_bytes()).hexdigest(),'reader_diagnostics':checks,'boundary':'Format/metadata diagnostics separate from factual grades; original raw output unchanged.'}
 p=d/f'reader-{reader}-source-unit-validation.json';assert not p.exists();p.write_text(json.dumps(out,indent=2)+'\n');print(reader,len(checks),'complete exact helper units PASS')
