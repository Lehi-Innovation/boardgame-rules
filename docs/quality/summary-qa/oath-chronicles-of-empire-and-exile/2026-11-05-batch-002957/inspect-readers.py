from pathlib import Path
import json,hashlib,sys
P=Path(__file__).resolve().parent;D=P/sys.argv[1]
def H(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def text(q):return q.get('text',q.get('verbatim')) if isinstance(q,dict) else q
s=(D/'summary-snapshot.md').read_text();ids=[x['id'] for x in json.loads((D/'questions.json').read_text())['questions']];readers={}
for who in ['a','b']:
 f=D/f'reader-{who}.json';r=json.loads(f.read_text());fail=[];counts={}
 for field in ['answer_quotations','verbatim_passages']:
  n=0
  for x in r['answers']:
   for quote in x.get(field,[]):
    n+=1
    if text(quote) not in s:fail.append([x['id'],field,'not_literal'])
  counts[field]=n
 for x in r['answers']:
  if x['answer']!='\n\n'.join(text(q) for q in x['answer_quotations']):fail.append([x['id'],'answer_join_mismatch'])
 readers['reader-'+who]={'raw_sha256':H(f),'all104_IDs_ordered':[x['id'] for x in r['answers']]==ids,'literal_quote_counts':counts,'failures':fail,'numeric_application_IDs':[x['id'] for x in r['answers'] if 'numeric_application' in x],'case_result_IDs':[x['id'] for x in r['answers'] if 'case_result' in x]}
out={'status':'PASS' if all(v['all104_IDs_ordered'] and not v['failures'] for v in readers.values()) else 'FAIL','summary_sha256':H(D/'summary-snapshot.md'),'questions_sha256':H(D/'questions.json'),'scope':'Technical literal/identity checks only; no semantic grades. dict quote text/verbatim fields preserved by lossless transport.','readers':readers}
(D/'reader-technical-validation.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],readers)
