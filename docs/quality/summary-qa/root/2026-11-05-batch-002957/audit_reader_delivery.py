from build_evidence import *
import re,sys
from difflib import SequenceMatcher
D=R/'delivery-audit';D.mkdir(exist_ok=True)
runtime=json.loads((R/'runtime-model-provenance.json').read_text())['records'];reports=[]
for rec in runtime:
 task=rec['agent_path'].split('/')[-1];m=re.fullmatch(r'(seed|expanded)(\d*)_reader_([ab])',task)
 if not m:continue
 kind,num,side=m.groups();num=int(num or 1);I=R/f'{kind}-iteration-{num:02}'
 if not I.exists() or (len(sys.argv)>1 and sys.argv[1]!='all' and I.name!=sys.argv[1]):continue
 raw_path=I/f'reader-{side}.json'
 if not raw_path.exists():continue
 try:
  raw=json.loads(raw_path.read_text());expected=[q['id'] for q in json.loads((I/'questions.json').read_text())['questions']];actual=[q['id'] for q in raw['answers']]
  if len(actual)!=len(expected) or set(actual)!=set(expected):continue
 except (ValueError,KeyError):continue
 calls={};blocks=[];records=[]
 for line in Path(rec['runtime_path']).open():
  event=json.loads(line);p=event.get('payload',{});typ=p.get('type');inp=p.get('input',p.get('arguments',''))
  if not isinstance(inp,str):inp=json.dumps(inp)
  if typ in ['custom_tool_call','function_call'] and re.search(r'[\"\']?cmd[\"\']?\s*:\s*\"(?:cat (?!>)|sed (?!-i\b)|wc |head |tail |nl |rg )',inp):calls[p.get('call_id')]=(event,p,inp)
  if typ not in ['custom_tool_call_output','function_call_output'] or p.get('call_id') not in calls:continue
  output=p.get('output','')
  if isinstance(output,str):
   try:output=json.loads(output)
   except ValueError:output=[{'text':output}]
  body='\n'.join(x.get('text','') for x in output) if isinstance(output,list) else json.dumps(output)
  call,cp,code=calls[p['call_id']];name=f'{I.name}-reader-{side}-call-{call.get("ordinal",0):04}.txt';path=D/name;path.write_text(body)
  normalized=[];comparison_body=body
  if re.search(r'\bnl\s+-ba\b',code):comparison_body=re.sub(r'(?m)^[ \t]*[0-9]+\t','',comparison_body);normalized.append('nl -ba line-number/tab prefixes')
  if re.search(r'\brg\s+[^\n]*?(?:-n\b|--line-number\b)',code):comparison_body=re.sub(r'(?m)^[0-9]+[:-]','',comparison_body);normalized.append('rg -n line-number/colon-or-dash prefixes')
  blocks.append(comparison_body)
  records.append({'call_id':p['call_id'],'call_ordinal':call.get('ordinal'),'output_ordinal':event.get('ordinal'),'tool':cp.get('name'),'actual_call_input':code,'output_path':str(path),'output_sha256':sha(path),'truncation_marker_present':bool(re.search('truncated',body,re.I)),'comparison_normalization':normalized,'actual_output_preserved_verbatim':True})
 input_results=[]
 for filename in ['summary-snapshot.md','questions.json']:
  path=I/filename;lines=path.read_text().splitlines();missing=[i for i,line in enumerate(lines,1) if line.strip() and not any(line in b for b in blocks)]
  ordered=set();ranges=[]
  for index,body in enumerate(blocks):
   for a,b,n in SequenceMatcher(None,lines,body.splitlines(),autojunk=False).get_matching_blocks():
    if n:ordered.update(range(a+1,a+n+1));ranges.append({'read_index':index+1,'source_lines':[a+1,a+n],'output_lines':[b+1,b+n]})
  ordered_missing=[i for i,line in enumerate(lines,1) if line.strip() and i not in ordered]
  input_results.append({'path':str(path),'sha256':sha(path),'total_lines':len(lines),'nonempty_lines':sum(bool(x.strip()) for x in lines),'unmatched_nonempty_lines':missing,'all_nonempty_lines_present_in_actual_read_outputs':not missing,'ordered_exact_matching_ranges':ranges,'unmatched_nonempty_lines_in_ordered_blocks':ordered_missing,'all_nonempty_lines_in_ordered_exact_blocks':not ordered_missing,'full_input_literal_present_in_one_read_output':any(path.read_text().strip() in b for b in blocks)})
 result={'iteration':I.name,'side':side,'agent_path':rec['agent_path'],'runtime_path':rec['runtime_path'],'method':'Read-call/output pairs only, never generated-answer output. Exact complete source-line text and ordered exact contiguous line blocks matched against actually delivered tool text, including recovery reads; blank lines do not carry facts. This establishes delivery, not cognitive attention. Whole-file and contiguous-chunk literal checks supplement line coverage where applicable.','read_calls':records,'inputs':input_results,'line_coverage_status':'ALL_NONEMPTY_INPUT_LINES_DELIVERED' if blocks and all(not x['unmatched_nonempty_lines_in_ordered_blocks'] for x in input_results) else 'DELIVERY_NOT_FULLY_PROVEN'}
 if I.name=='expanded-iteration-06':
  lines=(I/'summary-snapshot.md').read_text().splitlines();cut=99 if side=='a' else 84
  result['strict_contiguous_summary_delivery']={'ranges':[[1,cut],[cut+1,len(lines)]],'each_entire_contiguous_range_literal_present_in_actual_output':all(any('\n'.join(part).strip() in b for b in blocks) for part in [lines[:cut],lines[cut:]])}
  result['strict_questions_delivery']=input_results[1]['full_input_literal_present_in_one_read_output']
 save(I/f'reader-{side}-delivery-audit.json',result);reports.append(result)
save(R/'reader-delivery-audit.json',{'trigger':'Coordinator requested actual delivery/truncation/gap verification; no scores changed by delivery audit.','reports':reports,'summary':{k:sum(x['line_coverage_status']==k for x in reports) for k in ['ALL_NONEMPTY_INPUT_LINES_DELIVERED','DELIVERY_NOT_FULLY_PROVEN']}})
print(json.dumps({'reports':len(reports),'not_fully_proven':[(r['iteration'],r['side'],[(Path(i['path']).name,i['unmatched_nonempty_lines']) for i in r['inputs'] if i['unmatched_nonempty_lines']]) for r in reports if r['line_coverage_status']!='ALL_NONEMPTY_INPUT_LINES_DELIVERED'],'latest_strict_checks':[(r['side'],r.get('strict_contiguous_summary_delivery'),r.get('strict_questions_delivery')) for r in reports if r['iteration']=='expanded-iteration-06']},indent=2))
