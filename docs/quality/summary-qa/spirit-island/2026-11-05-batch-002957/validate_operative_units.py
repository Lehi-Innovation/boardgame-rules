"""Check exact same-entry quotations and whole source-unit boundaries, not semantics.

Run after blind outputs are saved, before grading. Diagnostics preserve the
original output; never repair or rewrite a reader's answer. Boundary-format
findings are separate from factual grading, per pre-reader coordinator steering.
"""
from pathlib import Path
import re,json,hashlib,sys
D=Path(sys.argv[1]).resolve();s=(D/'summary-snapshot.md').read_text();H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# A paragraph/list item/table is a complete blank-line-delimited Markdown block.
# Trim blank edges only; actual quoted text and all internal newlines stay exact.
blocks=set()
for m in re.finditer(r'\S(?:[\s\S]*?)(?=\n[ \t]*\n|\Z)',s):
 a,z=m.span()
 while z>a and s[z-1] in '\r\n':z-=1
 blocks.add((a,z))
# Complete Markdown list items may be adjacent without blank separators.
items=set();lines=s.splitlines(keepends=True);offsets=[];offset=0
for line in lines:offsets.append(offset);offset+=len(line)
for n,line in enumerate(lines):
 m=re.match(r'^([ \t]*)(?:[-*+]|\d+\.)[ \t]+',line)
 if not m:continue
 indent=len(m.group(1));last=n+1
 while last<len(lines):
  nxt=lines[last]
  if not nxt.strip():break
  next_indent=len(nxt)-len(nxt.lstrip(' \t'))
  if next_indent<=indent:break
  last+=1
 a=offsets[n];z=offsets[last] if last<len(lines) else len(s)
 while z>a and s[z-1].isspace():z-=1
 items.add((a,z))
heads=list(re.finditer(r'^#{1,6} .*(?:\n|$)',s,re.M));sections=set()
for n,h in enumerate(heads):
 level=len(h.group().split(' ')[0]);z=len(s)
 for later in heads[n+1:]:
  if len(later.group().split(' ')[0])<=level:z=later.start();break
 while z>h.start() and s[z-1].isspace():z-=1
 sections.add((h.start(),z))
checks=[]
for r in 'ab':
 p=D/f'reader-{r}.json';out=json.loads(p.read_text());entries=[]
 for x in out['answers']:
  units=x.get('evidence',[]);errors=[];seen=set()
  if not isinstance(units,list):errors.append('evidence is not a list of operative-unit objects');units=[]
  if x.get('support')=='supported' and not units:errors.append('supported answer has no attached units')
  for n,u in enumerate(units):
   if not isinstance(u,dict):errors.append(f'unit{n}: not object');continue
   a,z=u.get('start'),u.get('end');typ=u.get('unit_type');span=(a,z)
   if not isinstance(a,int) or not isinstance(z,int) or not 0<=a<z<=len(s):errors.append(f'unit{n}: invalid offsets');continue
   if u.get('text')!=s[a:z]:errors.append(f'unit{n}: text differs from frozen summary')
   if span in seen:errors.append(f'unit{n}: duplicate unit within entry')
   seen.add(span)
   if typ in ['paragraph','list_item','table']:
    if span not in (blocks|items):errors.append(f'unit{n}: incomplete source unit')
    if typ=='table' and not all(line.lstrip().startswith('|') for line in s[a:z].splitlines()):errors.append(f'unit{n}: table unit contains non-table lines')
   elif typ=='subsection':
    if span not in sections:errors.append(f'unit{n}: incomplete heading-bounded subsection')
   else:errors.append(f'unit{n}: unsupported unit_type')
  entries.append({'id':x['id'],'unit_count':len(units),'pass':not errors,'errors':errors})
 checks.append({'reader':f'reader-{r}','raw_output_sha256':H(p),'entries':entries,'pass':all(x['pass'] for x in entries)})
report={'protocol':'same-entry-operative-units-v2-format-diagnostics','validation_completed':True,'grading_may_proceed':True,'format_diagnostics_only':True,'summary_sha256':H(D/'summary-snapshot.md'),'checks':checks,'all_passed':all(x['pass'] for x in checks),'scope':'Mechanical quote integrity and complete unit boundaries only; diagnostic all_passed is not a factual score gate. Independent graders inspect the entire same entry and count all correctly supplied requested facts. A technical crop alone cannot fail an otherwise complete correct answer; actual missing facts, unsupported guesses and contradictions retain their substantive grading threshold. Raw outputs remain unchanged.'};p=D/'operative-unit-boundary-validation.json';assert not p.exists();p.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'validation_completed':True,'format_diagnostics_only':True,'all_passed':report['all_passed'],'failures':[{ 'reader':r['reader'],'entries':[x for x in r['entries'] if not x['pass']]} for r in checks if not r['pass']]}))
