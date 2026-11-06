from pathlib import Path
import json,hashlib,sys,shutil,difflib
P=Path(__file__).resolve().parent
ROOT=P.parents[4]
def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,d):Path(p).write_text(json.dumps(d,indent=2)+'\n')
def effective_results(d):
 versions=sorted(Path(d).glob('results-adjudicated-v*.json'),key=lambda x:int(x.stem.split('-v')[-1]))
 return versions[-1] if versions else Path(d)/'results.json'
def integrity():
 m=json.loads((P/'input-manifest.json').read_text())
 for x,sha in m['hashes'].items():
  if x.startswith(('extracted/','source_pdfs/')): assert h(ROOT/x)==sha,(x,'unexpected source mutation')
def freeze(name,bank='.'):
 integrity(); dest=P/name;dest.mkdir(exist_ok=False);bank=P/bank
 for n in ['questions.json','answer-key.json']:shutil.copyfile(bank/n,dest/n)
 shutil.copyfile(ROOT/'rules/scythe.md',dest/'summary-snapshot.md')
 files={n:h(dest/n) for n in ['summary-snapshot.md','questions.json','answer-key.json']}
 save(dest/'input-manifest.json',{'hashes':files,'source_hashes':json.loads((P/'input-manifest.json').read_text())['hashes'],'requested_model':'gpt-6-luna','reasoning_effort':'high'})
 for reader in ['a','b']:
  prompt=f'''You are an independent rules-summary reader in a blind evaluation.\n\nRead ONLY these two input files:\n{dest}/summary-snapshot.md\n{dest}/questions.json\n\nDo not read any authoritative rulebook, extracted text, answer key, manifest, prior responses, other files, parent history or web links. Do not browse. Use only the supplied summary as evidence, not prior game knowledge. Do not communicate with other readers.\n\nAnswer every question in the input file, including every requested part. Include every requested procedural quantity, timing, cost and destination within each answer. If a requested fact is absent, explicitly identify that part as unsupported; do not guess.\n\nFor every question include id, answer, support (supported, partial or unsupported), evidence (a short quote or section from the summary).\n\nSave valid JSON to {dest}/reader-{reader}.json with top-level fields reader, inputs_read and answers (an array). You may read only the two allowed inputs and write only your assigned output. Do not evaluate or improve the summary.\n'''
  if name.startswith('integrated-iteration-') or (name.startswith('expanded-iteration-') and int(name.split('-')[-1])>=9):
   old='Answer every question in the input file, including every requested part. Include every requested procedural quantity, timing, cost and destination within each answer. If a requested fact is absent, explicitly identify that part as unsupported; do not guess.'
   new="Answer every question in the input file, including every requested part. Treat compound questions as checklists and explicitly cover every requested procedural quantity, timing, cost and destination within that question's answer. Do not rely on answers to other questions. Before saving, check each answer against its question and use a separate clause for each requested part. If a requested fact is absent, explicitly identify that part as unsupported; do not guess."
   prompt=prompt.replace(old,new+'\n'+json.loads((P/'prompt-version-change.json').read_text())['exact_addition']).replace('\n\n','\n').rstrip('\n')
  (dest/f'reader-{reader}-prompt.txt').write_text(prompt)
 (dest/'summary-changes.patch').write_text(''.join(difflib.unified_diff((P/'baseline-summary.md').read_text().splitlines(True),(dest/'summary-snapshot.md').read_text().splitlines(True),fromfile='baseline',tofile=name)))
 s=json.loads((P/'game-status.json').read_text());s['phase']=name;s['question_count']=len(json.loads((dest/'questions.json').read_text())['questions']);s['iterations'].append(name);save(P/'game-status.json',s)
if __name__=='__main__':freeze(*sys.argv[1:])
