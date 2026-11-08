from pathlib import Path
import copy,hashlib,json
B=Path(__file__).resolve().parent;ROOT=B.parents[4];H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();load=lambda p:json.loads(p.read_text());r=load(B/'source-audit-final-12.json');l=load(B/'source-audit-final-12-read-ledger.json');v=load(B/'source-audit-final-12-visual-manifest.json');side=[];citations=[]
def stash(obj,kind,label=None):
 i=len(side);side.append(copy.deepcopy(obj));return {'$technical':i,'kind':kind,**({'label':label} if label else {})}
obj={'report':copy.deepcopy(r),'ledger':copy.deepcopy(l),'visual_manifest':copy.deepcopy(v)}
for g in obj['report']['checked_groups']:
 for i,ref in enumerate(g['source_references']):
  if 'passage' not in ref:continue
  assert set(ref)=={'path','source_sha256','anchor','start','end','passage','delivery_ranges'}
  p=ROOT/ref['path'];text=p.read_text();assert H(p)==ref['source_sha256'] and text[ref['start']:ref['end']]==ref['passage'] and ref['passage']
  citations.append({'path':ref['path'],'range':[ref['start'],ref['end']],'passage_sha256':hashlib.sha256(ref['passage'].encode()).hexdigest()})
  g['source_references'][i]=stash(ref,'verified literal primary citation',ref['anchor'])
obj['report']['source_delivery']=stash(obj['report']['source_delivery'],'exact original flat source-delivery rows')
for key in ['entries','coverage']:
 obj['ledger'][key]=stash(obj['ledger'][key],'exact recorded '+key)
# Technical source identities remain bound in the sidecar; every human observation/result/limit remains visible.
def encode(x):
 if isinstance(x,dict):
  if '$technical' in x:return x
  tech={k:value for k,value in x.items() if k in ['path','source_sha256','dimensions','original_pdf_sha256','matrix_scale','render_order','shared_document_method','render_provenance']}
  result={k:encode(value) for k,value in x.items() if k not in tech}
  if tech:
   result['$metadata']=stash(tech,'source identity and render metadata')
   if 'path' in tech:result['source_filename']=Path(tech['path']).name
  return result
 if isinstance(x,list):return [encode(y) for y in x]
 return x
projection=encode(obj)
def restore(x):
 if isinstance(x,dict):
  if '$technical' in x:return copy.deepcopy(side[x['$technical']])
  result={k:restore(value) for k,value in x.items() if k not in ['$metadata','source_filename']}
  if '$metadata' in x:result.update(restore(x['$metadata']))
  return result
 if isinstance(x,list):return [restore(y) for y in x]
 return x
assert restore(projection)=={'report':r,'ledger':l,'visual_manifest':v}
for name,data in [('source-audit12-root-semantic-projection.json',projection),('source-audit12-root-technical-sidecar.json',side),('source-audit12-verified-primary-citations.json',citations)]:
 p=B/name;assert not p.exists();p.write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n');print(json.dumps({'path':str(p),'characters':len(p.read_text()),'sha256':H(p)}))
print(json.dumps({'exact_full_reconstruction':True,'literal_primary_citations_verified':len(citations),'all_new_checked_groups':len(r['checked_groups']),'all_new_roles':len(r['supplemental_source_reconciliation']),'all_new_visual_observations':len(v['images'])}))
