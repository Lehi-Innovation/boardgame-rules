from pathlib import Path
import json,hashlib,sys,shutil,difflib
P=Path(__file__).resolve().parent
ROOT=Path('/home/jonny/projects/boardgame-rules')
bank,iteration=sys.argv[1:3]
D=P/iteration;D.mkdir()
shutil.copyfile(ROOT/'rules/dune-imperium.md',D/'summary-snapshot.md');shutil.copyfile(P/bank/'questions.json',D/'questions.json')
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
inputs=[D/'summary-snapshot.md',D/'questions.json',P/bank/'answer-key.json',ROOT/'extracted/dune-imperium-rules.txt',ROOT/'source_pdfs/dune-imperium-rules.pdf',ROOT/'source_pdfs/dune-imperium-official-faq-2025-01-13.pdf']

for extra in ['publisher-house-hagal-harvest-spice-2020.jpg']:
 if (P/extra).exists():inputs.append(P/extra)
(D/'input-manifest.json').write_text(json.dumps({'hashes':{str(p):h(p) for p in inputs},'requested_model':'gpt-6-luna','reasoning_effort':'high','prompt_version':'guide-plus-self-check-v2-bounded-reads'},indent=2))
for r in 'ab':
 prompt=f'''You are an independent rules-summary reader in a blind evaluation.

Read ONLY these two input files:
{D}/summary-snapshot.md
{D}/questions.json

Read the two inputs separately in bounded chunks (for example, no more than 60 lines per tool call). Do not combine both whole files into one output. Inspect each result for truncation; if any output is truncated, reread the missing ranges in smaller chunks until you have seen both complete files before answering.

Do not read any authoritative rulebook, extracted text, answer key,
manifest, prior responses, other files, parent history or web links.
Do not browse. Use only the supplied summary as evidence, not prior
game knowledge. Do not communicate with other readers.

Answer every question in the input file, including every requested part. If a requested
fact is absent, explicitly identify that part as unsupported; do not guess.

For every question include:
- id
- answer
- support: supported, partial or unsupported
- evidence: a short quote or section from the summary

Before writing final JSON, reread every question and review your draft answer on your own; explicitly resolve every requested part from the supplied summary, including requested quantities, timing, costs, destinations and exceptions; do not borrow a missing fact from another answer; identify unsupported parts instead of guessing; check volunteered rulings for contradictions with the summary.

Save valid JSON to {D}/reader-{r}.json with
top-level fields reader, inputs_read and answers (an array).
You may read only the two allowed inputs and write only your assigned
output. Do not evaluate or improve the summary.
'''
 (D/f'reader-{r}-prompt.txt').write_text(prompt)
(D/'summary-changes.patch').write_text(''.join(difflib.unified_diff((P/'baseline-summary.md').read_text().splitlines(True),(D/'summary-snapshot.md').read_text().splitlines(True),fromfile='baseline-summary.md',tofile='summary-snapshot.md')))
s=json.loads((P/'game-status.json').read_text());s.update(phase='blind-readers',question_count=len(json.loads((D/'questions.json').read_text())['questions']));s['iterations'].append(iteration);(P/'game-status.json').write_text(json.dumps(s,indent=2))
print(D)
