from pathlib import Path
import collections,copy,hashlib,json
D=Path(__file__).resolve().parent
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
J=lambda p:json.loads(p.read_text())
original=J(D/'grading-input.json');summary=(D/'summary-snapshot.md').read_text();raw={f'reader-{w}':{x['id']:x for x in J(D/f'reader-{w}.json')['answers']} for w in ['a','b']}
canon=lambda x:json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
blocks=[]
for number,start in enumerate(range(0,104,18),1):
 bd=D/'grading-blocks'/f'block-{number:02d}';bd.mkdir(parents=True,exist_ok=True)
 subset=copy.deepcopy(original);subset['questions']=copy.deepcopy(original['questions'][start:start+18]);subset['question_count']=len(subset['questions']);subset['required_fact_count_per_reader']=sum(len(q['required_facts']) for q in subset['questions']);subset['block_id']=f'block-{number:02d}'
 table=[];lookup={};counts=collections.Counter()
 for q in subset['questions']:
  for entry in q['readers'].values():
   for field in ['attached_verbatim_passage_spans','answer_quotation_spans']:
    refs=[]
    for span in entry.pop(field):
     row=[span['start'],span['end'],span['original_quote_type'],span['original_quote_metadata']];key=canon(row)
     if key not in lookup:lookup[key]=len(table);table.append(row)
     refs.append(lookup[key]);counts[field]+=1
    entry[field+'_ids']=refs
 subset['attached_quote_count']=counts['attached_verbatim_passage_spans'];subset['answer_quote_count']=counts['answer_quotation_spans'];subset['quote_span_table']=table
 subset['description']='Lossless bounded block. Decode every {$ref:N} from shared_values[N] (fully expanded, one lookup). quote_span_table rows: [start,end,original_quote_type,original_quote_metadata]. Each SAME-entry attached_verbatim_passage_spans_ids and answer_quotation_spans_ids references table rows in order; exact quote is full supplied summary[start:end], Unicode half-open. Original object/string metadata retained; __transport_text_field__ names text/verbatim field, remove it on restoration. Span sha256_utf8 reconstructs as SHA256 of exact quote. answer_transport joins restored answer_quotations. All original raw fields/quotes/numeric/case fields reconstruct exactly. No keys or answers outside this fixed block supplied. No cross-entry or cross-reader borrowing.'
 occurrences=collections.Counter()
 def count(x):
  if isinstance(x,(dict,list,str)):
   key=canon(x)
   if len(key)>=40:occurrences[key]+=1
  if isinstance(x,dict):
   for v in x.values():count(v)
  elif isinstance(x,list):
   for v in x:count(v)
 count(subset);pool=[];pool_ids={}
 def encode(x):
  if isinstance(x,(dict,list,str)):
   key=canon(x)
   if len(key)>=40 and occurrences[key]>1:
    if key not in pool_ids:pool_ids[key]=len(pool);pool.append(copy.deepcopy(x))
    return {'$ref':pool_ids[key]}
  if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
  if isinstance(x,list):return [encode(v) for v in x]
  return x
 compact=encode(subset);compact['shared_values']=pool
 (bd/'packet.json').write_text(json.dumps(compact,separators=(',',':'),ensure_ascii=False)+'\n')
 def decode(x):
  if isinstance(x,dict) and set(x)=={'$ref'}:return copy.deepcopy(pool[x['$ref']])
  if isinstance(x,dict):return {k:decode(v) for k,v in x.items()}
  if isinstance(x,list):return [decode(v) for v in x]
  return x
 restored=decode({k:v for k,v in compact.items() if k!='shared_values'});assert restored==subset
 raw_hashes={};record_count=0
 for q in restored['questions']:
  for who,transport in q['readers'].items():
   entry=copy.deepcopy(transport)
   for field,outfield in [('attached_verbatim_passage_spans_ids','verbatim_passages'),('answer_quotation_spans_ids','answer_quotations')]:
    quotes=[]
    for idx in entry.pop(field):
     a,b,t,m=table[idx];text=summary[a:b]
     if t=='object':
      value=copy.deepcopy(m);tf=value.pop('__transport_text_field__','text');value[tf]=text
     else:value=text
     quotes.append(value)
    entry[outfield]=quotes
   if 'answer_transport' in entry:
    tr=entry.pop('answer_transport');entry['answer']=tr['separator'].join(x.get('text',x.get('verbatim')) if isinstance(x,dict) else x for x in entry['answer_quotations'])
   assert entry==raw[who][q['id']]
   raw_hashes[f'{who}:{q["id"]}']=hashlib.sha256(canon(entry).encode()).hexdigest();record_count+=1
 proof={'status':'PASS','packet_sha256':H(bd/'packet.json'),'summary_sha256':H(D/'summary-snapshot.md'),'full_v1_packet_sha256':H(D/'grading-input.json'),'question_ids':[q['id'] for q in subset['questions']],'question_count':subset['question_count'],'required_fact_groups_per_reader':subset['required_fact_count_per_reader'],'both_complete_original_raw_entries_reconstructed_exactly':True,'raw_entry_count':record_count,'raw_entry_hashes':raw_hashes,'no_original_fields_or_quotations_discarded':True,'only_derived_span_hashes_not_serialized':True,'packet_characters':len((bd/'packet.json').read_text()),'actual_input_hashes':{x['path']:H(Path(x['path'])) for x in original['inputs']}}
 (bd/'losslessness.json').write_text(json.dumps(proof,indent=2)+'\n');blocks.append({'block_id':subset['block_id'],'agent_name':f'block{int(D.name.rsplit(chr(45),1)[1]):02d}_grader_{number:02d}','directory':str(bd),'packet_path':str(bd/'packet.json'),'packet_sha256':proof['packet_sha256'],'question_ids':proof['question_ids'],'question_count':proof['question_count'],'required_fact_groups_per_reader':proof['required_fact_groups_per_reader'],'packet_characters':proof['packet_characters']})
assert [id for b in blocks for id in b['question_ids']]==[q['id'] for q in original['questions']]
assert sum(b['required_fact_groups_per_reader'] for b in blocks)==328
manifest={'mode':'disjoint_bounded_fresh_grader_blocks','summary_path':str(D/'summary-snapshot.md'),'summary_sha256':H(D/'summary-snapshot.md'),'question_count':104,'entry_count':208,'required_fact_groups_per_reader':328,'fact_assessments':656,'blocks':blocks,'original_input_hashes':original['inputs'],'block_size':18,'coordinator_instruction':'Each fresh Sol/high none grader receives entire current frozen summary and only its fixed question/key/scope entries plus both full reconstructed raw entries. Aggregate every ID/fact exactly once; no cross-entry borrowing.'}
(D/'grading-block-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
selection=D/'grading-transport-selection.json'
if selection.exists() and not (D/'grading-transport-selection.whole-pair-v3.json').exists():(D/'grading-transport-selection.whole-pair-v3.json').write_bytes(selection.read_bytes())
selection.write_text(json.dumps({'mode':'bounded_blocks','manifest':'grading-block-manifest.json','grader_agents':[b['agent_name'] for b in blocks]},indent=2)+'\n')
print([(b['block_id'],b['question_count'],b['required_fact_groups_per_reader'],b['packet_characters']) for b in blocks])
