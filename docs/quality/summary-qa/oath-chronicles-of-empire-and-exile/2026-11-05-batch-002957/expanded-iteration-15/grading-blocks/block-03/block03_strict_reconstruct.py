from pathlib import Path
import json,hashlib,copy
D=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957/expanded-iteration-15');B=D/'grading-blocks/block-03'
p=json.loads((B/'packet.json').read_text());s=(D/'summary-snapshot.md').read_text()
def sha(b): return hashlib.sha256(b).hexdigest()
def deref(v):
 if isinstance(v,dict):
  if set(v)=={'$ref'}:return copy.deepcopy(p['shared_values'][v['$ref']])
  return {k:deref(x) for k,x in v.items()}
 if isinstance(v,list):return [deref(x) for x in v]
 return v
p=deref(p)
def quote(i):
 start,end,typ,meta=p['quote_span_table'][i];txt=s[start:end]
 if typ=='string':return txt
 out=copy.deepcopy(meta);field=out.pop('__transport_text_field__','text');out[field]=txt
 if 'sha256_utf8' in out:out['sha256_utf8']=sha(txt.encode())
 return out
def reconstruct(e):
 e=copy.deepcopy(e)
 for transport,raw in [('attached_verbatim_passage_spans_ids','verbatim_passages'),('answer_quotation_spans_ids','answer_quotations')]:e[raw]=[quote(i) for i in e.pop(transport)]
 t=e.pop('answer_transport');assert t['mode']=='join_answer_quotations'
 e['answer']=t['separator'].join(x if isinstance(x,str) else x.get('text',x.get('verbatim')) for x in e['answer_quotations'])
 return e
entries={r:[reconstruct(q['readers'][r]) for q in p['questions']] for r in ['reader-a','reader-b']}
def find(obj,id):
 if isinstance(obj,dict):
  if obj.get('id')==id:return obj
  for v in obj.values():
   f=find(v,id)
   if f is not None:return f
 elif isinstance(obj,list):
  for v in obj:
   f=find(v,id)
   if f is not None:return f
 return None
raw_equality={};rawhash={}
for r,es in entries.items():
 rawbytes=(D/(r+'.json')).read_bytes();rawhash[r]=sha(rawbytes);obj=json.loads(rawbytes)
 raw_equality[r]={e['id']:e==find(obj,e['id']) for e in es}
 assert all(raw_equality[r].values()),raw_equality
if __name__=='__main__':
 print(json.dumps({'raw_equality':raw_equality,'raw_hashes':rawhash,'extra_fields':{r:{e['id']:{k:v for k,v in e.items() if k not in ['id','support','support_label','evidence','verbatim_passages','answer','answer_quotations']} for e in es} for r,es in entries.items()}},ensure_ascii=False,indent=2))
