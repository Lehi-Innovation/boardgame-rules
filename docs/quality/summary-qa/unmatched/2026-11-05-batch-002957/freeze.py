from pathlib import Path
import sys,json,shutil,hashlib,difflib
P=Path(__file__).resolve().parent;I=P/sys.argv[1];B=P/sys.argv[2];I.mkdir(exist_ok=False)
shutil.copyfile(P.parents[4]/'rules/unmatched.md',I/'summary-snapshot.md')
shutil.copyfile(B/'questions.json',I/'questions.json')
for r in ['a','b']:
 text=(P/'seed-iteration-01'/f'reader-{r}-prompt.txt').read_text().replace(str(P/'seed-iteration-01'),str(I))
 (I/f'reader-{r}-prompt.txt').write_text(text)
 if (P/'actual-reader-protocol.txt').exists():
  actual=(P/'actual-reader-protocol.txt').read_text().format(summary=I/'summary-snapshot.md',questions=I/'questions.json',output=I/f'reader-{r}.json')
  (I/f'reader-{r}-actual-dispatch-prompt.txt').write_text(actual)
manifest={'benchmark':B.name,'requested_model':'gpt-6-luna','requested_effort':'high','hashes':{str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in [I/'summary-snapshot.md',I/'questions.json',B/'answer-key.json',I/'reader-a-prompt.txt',I/'reader-b-prompt.txt']}}
(I/'input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if (I/'reader-a-actual-dispatch-prompt.txt').exists():
 (I/'actual-dispatch-prompts.json').write_text(json.dumps({'note':'Exact common dispatch protocol rendered before readers; pair differs only in assigned output filename.','sha256':{str(I/f'reader-{r}-actual-dispatch-prompt.txt'):hashlib.sha256((I/f'reader-{r}-actual-dispatch-prompt.txt').read_bytes()).hexdigest() for r in ['a','b']}},indent=2)+'\n')
print(I)
