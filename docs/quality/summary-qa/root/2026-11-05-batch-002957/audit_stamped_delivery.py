"""Check actual delivered tool text, decoding JSON transport without changing rules."""
from build_evidence import *
from difflib import SequenceMatcher
import re,sys

I=R/(sys.argv[1] if len(sys.argv)>1 else 'expanded-iteration-12')
number=int(I.name.rsplit('-',1)[1])
include_incomplete='--include-incomplete' in sys.argv
runtime=json.loads((R/'runtime-model-provenance.json').read_text())['records']
D=I/'delivery-raw';D.mkdir(exist_ok=True)

def delivered_texts(output):
 if isinstance(output,str):
  try:output=json.loads(output)
  except ValueError:return [(output,'plain tool text')]
 if isinstance(output,dict):
  if isinstance(output.get('output'),str):return [(output['output'],'JSON output field decoded')]
  return []
 out=[]
 for item in output if isinstance(output,list) else []:
  body=item.get('text','')
  try:parsed=json.loads(body)
  except ValueError:parsed=None
  if isinstance(parsed,dict) and isinstance(parsed.get('output'),str):out.append((parsed['output'],'JSON output field decoded'))
  else:out.append((body,'plain tool text'))
 return out

def collect(rec):
 calls={};blocks=[];records=[];images=[]
 for line in Path(rec['runtime_path']).open():
  event=json.loads(line);p=event.get('payload',{});typ=p.get('type');inp=p.get('input',p.get('arguments',''))
  code=inp if isinstance(inp,str) else json.dumps(inp)
  if typ in ['custom_tool_call','function_call']:
   if re.search(r'tools\.view_image\s*\(',code):images.append({'ordinal':event.get('ordinal'),'input':code})
   if re.search(r'[\"\']?cmd[\"\']?\s*:',code) and any(x in code for x in ['sed ','cat ','nl ','get_text(','read_text(','print(']):
    original_input_read=('_reader_' not in rec['agent_path']) or any(name in code for name in ['summary-snapshot.md','questions.json'])
    if original_input_read and not re.search(r'cat\s*>|sed\s+-i\b',code) and ('.write_text(' not in code or 'get_text(' in code):calls[p.get('call_id')]=(event,p,code)
  if typ not in ['custom_tool_call_output','function_call_output'] or p.get('call_id') not in calls:continue
  call,cp,code=calls[p['call_id']]
  raw=D/(rec['agent_path'].split('/')[-1]+f'-call-{call.get("ordinal",0):04}.json')
  save(raw,{'actual_call':call,'actual_output':event})
  for idx,(body,transport) in enumerate(delivered_texts(p.get('output',''))):
   normalization=[]
   if re.search(r'\bnl\s+-ba\b',code):body=re.sub(r'(?m)^[ \t]*[0-9]+\t','',body);normalization.append('declared nl -ba line-number/tab prefix removed')
   if re.search(r'\brg\s+[^\n]*?(?:-n\b|--line-number\b)',code):body=re.sub(r'(?m)^[0-9]+[:-]','',body);normalization.append('declared rg line-number prefix removed')
   blocks.append({'body':body,'code':code,'read_index':len(blocks)+1})
   records.append({'call_id':p['call_id'],'call_ordinal':call.get('ordinal'),'output_ordinal':event.get('ordinal'),'content_index':idx,'raw_path':str(raw),'raw_sha256':sha(raw),'transport':transport,'comparison_normalization':normalization,'truncation_marker_present':bool(re.search('truncated',body,re.I))})
 return blocks,records,images

def coverage(path,blocks,text_value=None):
 text_value=path.read_text() if text_value is None else text_value
 lines=text_value.splitlines();covered=set();ranges=[]
 for block in blocks:
  for a,b,n in SequenceMatcher(None,lines,block['body'].splitlines(),autojunk=False).get_matching_blocks():
   if n:covered.update(range(a+1,a+n+1));ranges.append({'read_index':block['read_index'],'source_lines':[a+1,a+n],'output_lines':[b+1,b+n]})
 missing=[n for n,line in enumerate(lines,1) if line.strip() and n not in covered]
 return {'path':str(path),'sha256':sha(path),'total_lines':len(lines),'nonempty_lines':sum(bool(x.strip()) for x in lines),'unmatched_nonempty_lines_in_ordered_blocks':missing,'all_nonempty_lines_in_ordered_exact_blocks':not missing,'ordered_exact_matching_ranges':ranges}

reports=[]
for who in ['a','b']:
 task=f'/root/expanded{number}_reader_{who}';rec=next((x for x in runtime if x['agent_path']==task),None)
 if not rec or not (I/f'reader-{who}.json').exists():continue
 try:
  raw=json.loads((I/f'reader-{who}.json').read_text());expected=json.loads((I/'questions.json').read_text())['questions']
  if len(raw['answers'])!=len(expected) and not include_incomplete:continue
 except (ValueError,KeyError):continue
 blocks,calls,_=collect(rec);inputs=[coverage(I/f,blocks) for f in ['summary-snapshot.md','questions.json']]
 result={'iteration':I.name,'side':who,'agent_path':task,'runtime_path':rec['runtime_path'],'method':'Actual read-call/output pairs only; JSON transport output fields decoded, declared line-number prefixes removed, otherwise exact contiguous line blocks. Generated answer output is excluded. Establishes delivery, not cognitive attention.','read_calls':calls,'inputs':inputs,'line_coverage_status':'ALL_NONEMPTY_INPUT_LINES_DELIVERED' if blocks and all(x['all_nonempty_lines_in_ordered_exact_blocks'] for x in inputs) else 'DELIVERY_NOT_FULLY_PROVEN'}
 result['answer_count_at_audit']=len(raw['answers']);result['expected_answer_count']=len(expected);result['reader_output_complete']=len(raw['answers'])==len(expected)
 save(I/f'reader-{who}-delivery-audit.json',result);reports.append(result)

rec=next((x for x in runtime if x['agent_path']=='/root/stamped_source_auditor_01'),None)
if rec and I.name=='expanded-iteration-12':
 blocks,calls,images=collect(rec)
 inputs=[coverage(path,blocks) for path in [I/'summary-snapshot.md',ROOT/'extracted/root-rules.txt']]
 import fitz
 pdf=ROOT/'source_pdfs/root-recovery.pdf';doc=fitz.open(pdf)
 pdf_blocks=[b for b in blocks if ('source-only-audit' in b['code'] and '.txt' in b['code']) or ('root-recovery.pdf' in b['code'] and 'get_text' in b['code'])]
 pages=[]
 for n,page in enumerate(doc,1):
  result=coverage(pdf,pdf_blocks,page.get_text())
  result['physical_page']=n;pages.append(result)
 passed=all(x['all_nonempty_lines_in_ordered_exact_blocks'] for x in inputs+pages)
 result={'agent_path':rec['agent_path'],'runtime_path':rec['runtime_path'],'method':'Actual read-call/output pairs with decoded JSON transport; exact contiguous source-line blocks. PDF comparisons use independently extracted fitz text for every physical page and only PDF/PDF-text read calls, excluding original extracted-source reads. Images must additionally be reviewed against the auditor report.','read_calls':calls,'inputs':inputs,'pdf_sha256':sha(pdf),'pdf_pages':pages,'pdf_read_blocks':len(pdf_blocks),'image_inspection_calls':images,'line_coverage_status':'ALL_SOURCE_AND_SUMMARY_NONEMPTY_LINES_DELIVERED' if passed else 'DELIVERY_NOT_FULLY_PROVEN'}
 save(I/'source-auditor-delivery-audit.json',result)
 print(json.dumps({'auditor_delivery':result['line_coverage_status'],'source_missing_counts':[(Path(x['path']).name,len(x['unmatched_nonempty_lines_in_ordered_blocks'])) for x in inputs],'pdf_missing_counts':[(x['physical_page'],len(x['unmatched_nonempty_lines_in_ordered_blocks'])) for x in pages if not x['all_nonempty_lines_in_ordered_exact_blocks']],'image_calls':len(images)}))
print(json.dumps({'readers':[(r['side'],r['line_coverage_status']) for r in reports]}))
