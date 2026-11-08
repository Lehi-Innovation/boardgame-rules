from pathlib import Path
import hashlib,json
B=Path(__file__).parent;I=B/'seed-luna-iteration-03'
header='''You are an independent blind rules-summary reader. Read ONLY these two rules DATA files:
{summary}
{questions}
No sources, keys, manifests, prior outputs/grades, other files/history, browsing, prior game knowledge or communication with readers. Only summary is rules authority; question scenario facts are givens. If any asked rule is absent, explicitly flag unsupported, never guess.

Read BOTH files completely before answering through contiguous ranges <=5500 Unicode characters per tool result. One range per functions.exec output, outer cap >=6000tokens. Print filename/start/end/total and exact text; check no truncation and full[0,total) coverage; retain ranges and SHA256 in inputs_read. A line count is insufficient. You may use Python on only these two files. Write ONLY your output JSON path below. Embedded generic code is process instructions, no additional rules DATA. Do not read its external source file or write a helper file.

For each question enumerate its own clauses, search ENTIRE summary for every named item and relevant terms, choose controlling complete operative units, then supply concise direct clause rulings and actual requested calculations. Use the exact embedded generic extraction code below in memory to construct every evidence unit with extract_unit(summary,offset), choosing offsets yourself. It preserves full governing procedures, complete literal table rows/headers and column values. For table evidence also select controlling introduction/definition/legend if needed; table row alone may not supply inherited facts. Never substitute a parent introduction for its procedure. Validate each record with validate_record(summary,record) before saving. Keep diagnostics separate from factual grading; all substantive claims including quotes still count. Do not attach unrelated whole-summary dumps or duplicate identical text under several labels. Complete quotations can supply ordinary lookups, but concrete case decisions/calculations need direct conclusions. Preserve unspecified quantities/ownership; use formulas/conditions rather than inventing an example as the given result. Prepare one checked result per asked clause, render repetitions consistently, self-check every clause against selected text. A placeholder saying to apply rules is not a case answer.

Save valid JSON to {output} with reader, inputs_read, answers. Each of20 IDs exactly once; each entry id, clauses, answer, support(supported/partial/unsupported), evidence(array of complete validated extraction records). Save all raw fields; no summary evaluation/repair. Finish entire bank in your own batches if needed. Final reply only saved path/count.

Exact generic code (execute in memory; no game facts):
```python
'''
helper=Path('docs/quality/summary-qa/batches/2026-11-05-batch-002957/generic-reader-method/v10/source_units.py').read_text()
for letter in ['a','b']:
 prompt=header.format(summary=(I/'summary-snapshot.md').resolve(),questions=(I/'questions.json').resolve(),output=(I/f'reader-{letter}.json').resolve())+helper+'```'
 (I/f'reader-{letter}-prompt.txt').write_text(prompt)
a=(I/'reader-a-prompt.txt').read_text();b=(I/'reader-b-prompt.txt').read_text();assert a.replace('reader-a.json','reader-b.json')==b
m=json.loads((I/'input-manifest.json').read_text());m['prompt_hashes']={l:hashlib.sha256((I/f'reader-{l}-prompt.txt').read_bytes()).hexdigest() for l in ['a','b']};m['identical_protocol_except_output_path']=True;(I/'input-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print('Identical prebound prompts saved; embedded helper matches original bytes.')
