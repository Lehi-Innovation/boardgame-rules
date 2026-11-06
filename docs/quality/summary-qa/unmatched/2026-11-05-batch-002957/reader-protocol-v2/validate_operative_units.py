"""Mechanical complete-unit gate. Does not grade game rulings or modify readers."""
from pathlib import Path
import re,json,sys,hashlib
KINDS={'paragraph','list_item','list','subsection','table_header','table_row'}
def trim(text,start,end):
 while start<end and text[start].isspace():start+=1
 while end>start and text[end-1].isspace():end-=1
 return start,end

def catalog(text):
 valid={k:set() for k in KINDS};row_headers={};fm=re.match(r'\A---\n.*?\n---\n',text,re.S);body_start=fm.end() if fm else 0
 heads=list(re.finditer(r'(?m)^(#{1,6})[ \t]+[^\n]+',text))
 for i,h in enumerate(heads):
  if len(h.group(1))<2:continue  # The title must not license a whole-summary dump.
  next_any=heads[i+1].start() if i+1<len(heads) else len(text)
  valid['subsection'].add(trim(text,h.start(),next_any))
 bounds=[];start=0
 for m in re.finditer(r'\n[ \t]*\n',text):bounds.append((start,m.start()));start=m.end()
 bounds.append((start,len(text)))
 for left,right in bounds:
  left,right=trim(text,left,right)
  if left>=right or left<body_start:continue
  value=text[left:right];lines=[];pos=left
  for line in text[left:right].splitlines(keepends=True):lines.append((pos,pos+len(line),line));pos+=len(line)
  if value.startswith('|'):
   if len(lines)<2 or not re.fullmatch(r'\|[ |:\-]+\|',lines[1][2].strip()):continue
   header=trim(text,lines[0][0],lines[1][1]);valid['table_header'].add(header)
   for a,b,line in lines[2:]:
    if line.strip().startswith('|') and line.strip().endswith('|'):
     row=trim(text,a,b);valid['table_row'].add(row);row_headers[row]=header
  elif re.match(r'(?:[-*+]|\d+[.)])[ \t]+',value):
   valid['list'].add((left,right));markers=[]
   for a,b,line in lines:
    marker=re.match(r'([ ]*)(?:[-*+]|\d+[.)])[ \t]+',line)
    if marker:markers.append((a,len(marker.group(1))))
   for i,(a,indent) in enumerate(markers):
    end=next((b for b,other_indent in markers[i+1:] if other_indent<=indent),right);valid['list_item'].add(trim(text,a,end))
  elif not value.startswith('#'):valid['paragraph'].add((left,right))
 return valid,row_headers

def unit_error(text,unit,valid,row_headers,lookup):
 kind=unit.get('kind');start=unit.get('start');end=unit.get('end')
 if kind not in KINDS:return 'unknown evidence kind'
 if type(start) is not int or type(end) is not int or not 0<=start<end<=len(text):return 'invalid character bounds'
 if unit.get('text')!=text[start:end]:return 'quote is not exact original summary[start:end]'
 span=trim(text,start,end)
 if span not in valid[kind]:return 'selection is not a complete permitted Markdown operative unit'
 if kind=='table_row':
  header=lookup.get(unit.get('header_id'))
  if not header or header.get('kind')!='table_header':return 'table row lacks its same-entry complete header'
  actual_header=trim(text,header['start'],header['end']);expected_header=row_headers[span]
  # Identical complete headers may be shared across same-entry table rows;
  # their column meaning is unchanged even when the source repeats the header.
  if actual_header!=expected_header and text[actual_header[0]:actual_header[1]]!=text[expected_header[0]:expected_header[1]]:return 'table row references different table columns'
 return None

def validate(summary,questions,raw):
 text=summary.read_text();valid,row_headers=catalog(text);data=json.loads(raw.read_text());q=json.loads(questions.read_text())['questions'];answers=data['answers'];ids=[x['id'] for x in q]
 errors=[];checks=[]
 if [a.get('id') for a in answers]!=ids:errors.append({'id':None,'reason':'Missing, duplicate or unordered question IDs'})
 for a in answers:
  evidence=a.get('evidence');clauses=a.get('clauses');clause_checks=a.get('clause_checks')
  if not isinstance(evidence,list) or not isinstance(clauses,list) or not isinstance(clause_checks,list):errors.append({'id':a.get('id'),'reason':'Missing v2 evidence/clauses/clause_checks arrays'});continue
  lookup={u.get('unit_id'):u for u in evidence};seen=set();local=[]
  if len(lookup)!=len(evidence):local.append('duplicate evidence unit IDs')
  for u in evidence:
   err=unit_error(text,u,valid,row_headers,lookup)
   if err:local.append(str(u.get('unit_id'))+': '+err);continue
   span=trim(text,u['start'],u['end'])
   if span in seen:local.append(str(u.get('unit_id'))+': duplicate same-entry source text under another label')
   seen.add(span)
  if [x.get('clause_index') for x in clause_checks]!=list(range(len(clauses))):local.append('clause check indices must cover each own clause once in order')
  for x in clause_checks:
   refs=x.get('evidence_unit_ids',[])
   if any(ref not in lookup for ref in refs):local.append('clause references missing same-entry evidence')
   if x.get('supported') is True and not refs:local.append('supported clause has no operative evidence reference')
  checks.append({'id':a.get('id'),'clause_count':len(clauses),'unit_count':len(evidence),'complete_operative_units':not local})
  errors.extend({'id':a.get('id'),'reason':reason} for reason in local)
 return {'method':'Exact character spans plus complete Markdown paragraph/list/list-item/subsection/table-row-with-header boundaries. No semantic ruling grade is inferred. Raw reader file unchanged.','summary_sha256':hashlib.sha256(summary.read_bytes()).hexdigest(),'questions_sha256':hashlib.sha256(questions.read_bytes()).hexdigest(),'raw_reader_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'expected_question_count':len(ids),'answers':checks,'errors':errors,'pass':not errors}

if __name__=='__main__':
 if len(sys.argv)!=5:raise SystemExit('usage: validate_operative_units.py SUMMARY QUESTIONS RAW_READER OUTPUT_VALIDATION')
 result=validate(*map(Path,sys.argv[1:4]));Path(sys.argv[4]).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS' if result['pass'] else 'FAIL',len(result['errors']),'boundary/schema errors');raise SystemExit(0 if result['pass'] else 1)
