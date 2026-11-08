from pathlib import Path
import json,re,hashlib,collections
R=Path(__file__).parent
def sha(b):return hashlib.sha256(b).hexdigest()
def objsha(x):return sha(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def reader(x):
 x=x.lower().replace('_','-').replace(' ','-')
 if x in ['a','b']:return x
 if x.endswith('-a'):return 'a'
 if x.endswith('-b'):return 'b'
 raise ValueError(x)
def raw_entries(path):
 text=path.read_text();doc=json.loads(text);dec=json.JSONDecoder();candidates=[]
 for m in re.finditer(r'"answers"\s*:\s*\[',text):
  start=text.index('[',m.start())
  try:arr,end=dec.raw_decode(text,start)
  except ValueError:continue
  if arr==doc['answers']:candidates.append((start,end))
 assert len(candidates)==1
 start,end=candidates[0];pos=start+1;records=[]
 while pos<end:
  while text[pos].isspace() or text[pos]==',':pos+=1
  if text[pos]==']':break
  item,stop=dec.raw_decode(text,pos);raw=text[pos:stop]
  assert item==doc['answers'][len(records)]
  records.append({'id':item['id'],'start_char':pos,'end_char':stop,'start_byte':len(text[:pos].encode()),'end_byte':len(text[:stop].encode()),'raw_entry_sha256':sha(raw.encode()),'normalized_entry_sha256':objsha(item),'all_fields_preserved':True})
  pos=stop
 assert len(records)==len(doc['answers'])
 return doc,records
key=json.loads((R/'seed-v1/answer-key.json').read_text());questions=json.loads((R/'seed-v1/questions.json').read_text());expected=[q['id'] for q in questions['questions']]
for iteration in range(1,4):
 it=R/f'seed-iteration-{iteration:02}';original_path=it/'results.json';original=json.loads(original_path.read_text());grading=[]
 if 'results' in original:grading=original['results']
 else:
  for r in original['readers']:
   for entry in r.get('entries',r.get('answers',[])):grading.append(dict(entry,reader=r['reader']))
 table={}
 for i,e in enumerate(grading):
  rid=reader(e['reader']);qid=e.get('id',e.get('question_id'));grade=e.get('grade',e.get('final_whole_answer_grade')).lower();table[rid,qid]={'original_grade':grade,'grade':grade,'original_grade_record':{'path':str(original_path.resolve()),'flattened_record_index':i,'normalized_record_sha256':objsha(e)},'adjudications':[]}
 assert len(table)==40
 adjud_path=it/'scope-adjudication.json';adjud=json.loads(adjud_path.read_text())
 entries=adjud.get('adjudications',adjud.get('results',adjud.get('reader_results',[])))
 for i,e in enumerate(entries):
  rid=reader(e['reader']);qid=e.get('id',e.get('question_id'));t=table[rid,qid];t['grade']=e['grade'].lower();t['adjudications'].append({'path':str(adjud_path.resolve()),'record_index':i,'normalized_record_sha256':objsha(e),'grade':e['grade'].lower()})
 correction=it/'scope-adjudication-grade-definition-correction.json'
 if correction.exists():
  for i,e in enumerate(json.loads(correction.read_text())['corrected_entries']):
   t=table[reader(e['reader']),e['question_id']];t['grade']=e['corrected_grade'];t['adjudications'].append({'path':str(correction.resolve()),'record_index':i,'normalized_record_sha256':objsha(e),'grade':e['corrected_grade']})
 rawmanifest={'iteration':it.name,'readers':[]};final={'game':'Cosmic Encounter','benchmark_version':'seed-v1','iteration':it.name,'method':'Original detailed grades plus fresh independent scope adjudications; no question/key/reader edits. Full detailed observations remain in linked immutable records.','input_key_sha256':sha((R/'seed-v1/answer-key.json').read_bytes()),'original_grades_sha256':sha(original_path.read_bytes()),'readers':[]}
 for rid in ['a','b']:
  path=it/f'reader-{rid}.json';doc,spans=raw_entries(path);ids=[x['id'] for x in doc['answers']];assert ids==expected
  rawmanifest['readers'].append({'reader':rid,'raw_file_path':str(path.resolve()),'raw_file_sha256':sha(path.read_bytes()),'entries':spans,'all_expected_ids_exactly_once':True})
  out=[]
  for q,k,a,span in zip(questions['questions'],key['answers'],doc['answers'],spans):
   assert q['id']==k['id']==a['id'];x=table[rid,q['id']]
   out.append({'id':q['id'],'question_sha256':objsha(q),'key_entry_sha256':objsha(k),'raw_reader_entry':span,'required_key_fact_refs':[{'fact_index':i,'fact_sha256':sha(f.encode())} for i,f in enumerate(k['required_facts'])],**x})
  totals={g:sum(x['grade']==g for x in out) for g in ['correct','partial','incorrect']};assert sum(totals.values())==20
  final['readers'].append({'reader':rid,'results':out,'totals':totals,'all_expected_ids_exactly_once':True,'key_fact_refs_exactly_once':sum(len(x['required_key_fact_refs']) for x in out)==sum(len(x['required_facts']) for x in key['answers'])})
 final['pass']=all(x['totals']=={'correct':20,'partial':0,'incorrect':0} for x in final['readers'])
 for dest,data in [(it/'raw-entry-manifest.json',rawmanifest),(it/'results-after-independent-adjudication.json',final)]:
  if dest.exists():assert json.loads(dest.read_text())==data,'Never replace differing historical aggregation'
  else:dest.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 print(it.name,[x['totals'] for x in final['readers']],final['pass'])
