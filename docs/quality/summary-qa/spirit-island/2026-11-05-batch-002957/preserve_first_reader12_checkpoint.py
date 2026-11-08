from pathlib import Path
import collections,hashlib,json,shutil,sys
B=Path(__file__).resolve().parent
iteration,reader,stage=sys.argv[1:]
assert iteration=='expanded-iteration-12' and reader in ['a','b'] and stage in ['draft_ready','complete']
D=B/iteration
p=D/f'reader-{reader}.json'
v=json.loads(p.read_text())
assert v['stage']==stage
ids=[x['id'] for x in json.loads((D/'questions.json').read_text())['questions']]
assert len(ids)==173 and collections.Counter(x['id'] for x in v['answers'])==collections.Counter(ids)
folder=D/('drafts-first-completed-originals' if stage=='draft_ready' else 'finals-first-completed-originals')
folder.mkdir(exist_ok=True)
dst=folder/f'reader-{reader}.json'
receipt=folder/f'reader-{reader}-freeze.json'
assert not dst.exists() and not receipt.exists()
shutil.copyfile(p,dst)
assert p.read_bytes()==dst.read_bytes()
r={'path':str(p),'immutable_copy':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'characters':len(dst.read_text()),'stage':stage,'answer_count':173,'first_completed_original_preserved':True,'entire_original_fields_retained':True,'parent_semantic_review_not_started':True,'no_original_mutation_or_factual_diagnostic':True}
receipt.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'reader':reader,'stage':stage,'sha256':r['sha256'],'characters':r['characters'],'preserved':True}))
