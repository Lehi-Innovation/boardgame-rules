from pathlib import Path
import sys,json,hashlib,shutil,difflib
P=Path(__file__).parent; name=sys.argv[1]; bank=sys.argv[2];D=P/name;D.mkdir(exist_ok=False)
shutil.copyfile('rules/orl-ans.md',D/'summary-snapshot.md');shutil.copyfile(P/bank/'questions.json',D/'questions.json')
paths=[D/'summary-snapshot.md',D/'questions.json',P/bank/'answer-key.json',P/'authoritative-source.txt',P/'matching-rulebook.pdf']
if (P/'base-clarification-invasion-2015.pdf').exists(): paths += [P/'base-clarification-invasion-2015.pdf',P/'base-clarification-invasion-extraction.txt']
(D/'input-manifest.json').write_text(json.dumps({'sha256':{str(x.resolve()):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths},'benchmark_version':bank,'requested_model':'gpt-6-luna','reasoning_effort':'high'},indent=2)+'\n')
(D/'summary-changes.patch').write_text(''.join(difflib.unified_diff((P/'original-summary.md').read_text().splitlines(True),(D/'summary-snapshot.md').read_text().splitlines(True),fromfile='original-summary.md',tofile=name+'/summary-snapshot.md')))
s=json.loads((P/'game-status.json').read_text());s.update(phase='blind-readers',question_count=len(json.loads((D/'questions.json').read_text())['questions']));s['iterations'].append(name);(P/'game-status.json').write_text(json.dumps(s,indent=2)+'\n')
