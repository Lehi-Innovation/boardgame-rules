"""Technical whole-section format only. No rules, keys, expected facts or grades."""
from pathlib import Path
import json,re,sys,hashlib
P=Path(__file__).resolve().parent;D=P/sys.argv[1];who=sys.argv[2];s=(D/'summary-snapshot.md').read_text();rawpath=D/f'reader-{who}.json';r=json.loads(rawpath.read_text());headings=list(re.finditer(r'^(#{2,6}) (.+)\n',s,re.M));sections={}
for n,m in enumerate(headings):
 end=next((z.start() for z in headings[n+1:] if len(z[1])<=len(m[1])),len(s));sections[m[2]]=s[m.start():end].rstrip()
errors=[];checked=0
for entry in r['answers']:
 if int(D.name.rsplit('-',1)[1])>=12 and 'numeric_application' in entry and 'case_result' in entry:
  errors.append({'id':entry['id'],'reason':'Numerical entry must have one computed numeric_application, without a duplicate case_result calculation.'})
 valid=[]
 for n,q in enumerate(entry.get('verbatim_passages',[])):
  checked+=1
  if not isinstance(q,dict) or 'section' not in q or 'text' not in q:errors.append({'id':entry['id'],'field':f'verbatim_passages[{n}]','reason':'Require object section/text with exact Markdown heading label and full section text.'});continue
  expected=sections.get(q['section'])
  if expected is None or q['text'].rstrip()!=expected:errors.append({'id':entry['id'],'field':f'verbatim_passages[{n}]','reason':'Text is not the entire named ##/### section through its next equal-or-higher heading.'})
  else:valid.append(expected)
 if not valid:errors.append({'id':entry['id'],'reason':'No complete controlling section supplied.'})
 for n,q in enumerate(entry.get('answer_quotations',[])):
  t=q.get('text',q.get('verbatim')) if isinstance(q,dict) else q
  if not any(t in section for section in valid):errors.append({'id':entry['id'],'field':f'answer_quotations[{n}]','reason':'Answer excerpt must belong within an attached complete named section.'})
out={'status':'PASS' if not errors else 'FORMAT_INCOMPLETE','scope':'Technical format and literal section coverage only; no rule/case/semantic grading. No raw edits.','raw_sha256':hashlib.sha256(rawpath.read_bytes()).hexdigest(),'sections_checked':checked,'errors':errors};(D/f'reader-{who}.section-format-validation.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],'sections',checked,'format_errors',len(errors))
