from pathlib import Path
import json,shutil
q=Path(__file__).resolve().parent
# Runtime task bodies are opaque ciphertext. Preserve them without claiming recovery.
if (q/'prompts').exists() and not (q/'runtime-opaque-task-bodies').exists():shutil.move(q/'prompts',q/'runtime-opaque-task-bodies')
(q/'prompts').mkdir(exist_ok=True)
reader='''You are an independent rules-summary reader in a blind evaluation.
Read ONLY these two input files:
{summary}
{questions}
Do not read any authoritative rulebook, extracted text, answer key, manifest, prior responses, other files, parent history or web links. Do not browse. Use only the supplied summary as evidence, not prior game knowledge. Do not communicate with other readers.
Answer every question in the input file, including every requested part. If a requested fact is absent, explicitly identify that part as unsupported; do not guess.
For every question include id, answer, support (supported, partial or unsupported), evidence (a short quote or section from summary).
Before writing final JSON, reread every question and review your draft answer on your own. Explicitly resolve every requested part from the supplied summary, including requested quantities, timing, costs, destinations and exceptions. Do not borrow a missing fact from another answer. Identify unsupported parts instead of guessing. Check volunteered rulings for contradictions with the summary.
Save valid JSON to {output} with top-level reader, inputs_read, answers (array). You may read only the two allowed inputs and write only your assigned output. Do not evaluate or improve the summary.'''
for d in q.glob('*iteration-*'):
 if not d.is_dir():continue
 for r in ['a','b']:
  body=reader.format(summary=d/'summary-snapshot.md',questions=d/'questions.json',output=d/f'reader-{r}.json')+'\n'
  version=json.loads((d/'input-manifest.json').read_text())['prompt_version']
  if 'v2-' in version:
   body=body.replace('Answer every question in the input file, including every requested part.', 'Operational reading: read the two files separately in bounded chunks, for example at most 30 summary lines or 10 questions per output. Use one chunk per tool invocation, including the outer wrapper. Never rely on truncated output; if a warning appears, reread all missing ranges in smaller chunks until the entire summary and every question have been read. Do not create helper files; write only your assigned output.\nAnswer every question in the input file, including every requested part. Use a separate explicit clause for each requested part; do not compress away rule consequences or exceptions. Lists or tables may be used to keep multi-part answers complete.')
  if d.name.startswith('expanded-iteration-') and int(d.name.rsplit('-',1)[1])>=6:
   body=(d/f'reader-{r}-prompt.txt').read_text()
  (d/f'reader-{r}-intended-dispatch-prompt.txt').write_text(body)
  task=('seed' if d.name.startswith('seed') else 'expanded' if d.name.startswith('expanded') else 'integration')+d.name.rsplit('-',1)[1]+'_'+r
  (q/'prompts'/f'{task}.txt').write_text(body)
audit='''You are a fresh independent final source auditor. Independently audit ONLY this exact frozen summary:
{summary}
against the complete authoritative source packet:
/home/jonny/projects/boardgame-rules/extracted/dune-imperium-uprising-rules.txt
{q}/dune-imperium-uprising-rules.txt
{q}/dune-imperium-uprising-supplements.txt
{q}/dune-imperium-official-faq-2025-01-13.txt
Necessary original PDF assets may be inspected at /home/jonny/projects/boardgame-rules/source_pdfs/dune-imperium-uprising-rules.pdf, dune-imperium-uprising-supplements.pdf and dune-imperium-official-faq-2025-01-13.pdf. Unannotated source rendering for resource icons: {q}/dune-imperium-uprising-supplements-p5.png. Working Python with fitz: /home/jonny/projects/boardgame-rules/.venv/bin/python.
Scope is original English 2023 Uprising v23-10-12, complete standard 2–4-player multiplayer including required standard scoring two-player Rival, plus optional standard base-box CHOAM with its 20 standard contracts. Identify separate 10 Rise of Ix compatibility contracts but exclude cross-game expansions, solo-only rules, optional Rival variants and six-player teams. Relevant general/Uprising official Jan13 2025 FAQ clarifications apply.
Check all material claims and important omissions, all board-space costs/effects/Combat flags, timing, component destinations, exceptions and end conditions. Treat printed cards as rules sources only to the extent supported by supplied text/PDF; do not invent details. Do not read any other summary version, prior audit or repair history, coverage questions, answer key, reader outputs or grades. Do not communicate with readers. Do not assume it should pass and do not edit the summary.
Save JSON ONLY to {output} containing verdict (PASS/MINOR/MAJOR), findings with severity and precise source references, checked_claims, exact summary/source input hashes and independence statement. You may write necessary unannotated PDF renders in that same iteration directory. Your final answer should state verdict and material findings.'''
for d in q.glob('expanded-iteration-*'):
 if (d/'source-audit-reference.json').exists():continue
 body=audit.format(summary=d/'summary-snapshot.md',q=q,output=d/'source-audit.json')+'\n'
 if any(v in json.loads((d/'input-manifest.json').read_text())['prompt_version'] for v in ['v2-','v3-']):
  template='source-audit-final-prompt-v3-template.txt' if int(d.name.rsplit('-',1)[1])>=12 else 'source-audit-final-prompt-v2-template.txt'
  body=(q/template).read_text().format(iteration=d,run=q)
 (d/'source-audit-intended-dispatch-prompt.txt').write_text(body);(q/'prompts'/('final_source_audit'+d.name.rsplit('-',1)[1]+'.txt')).write_text(body)
(q/'prompt-provenance-note.json').write_text(json.dumps({'reader_prompt_versions':['guide-reader-plus-generic-self-check-v1','guide-reader-plus-generic-self-check-v2-bounded-complete-clauses','guide-reader-plus-generic-self-check-v3-complete-input-ids'],'plaintext_intended_prompts':'prompts/ and per-iteration *-intended-dispatch-prompt.txt; retained from the exact messages submitted in this chat, not decrypted from runtime data','runtime_task_bodies':'Opaque encrypted strings in runtime spawn arguments; previous captures preserved in runtime-opaque-task-bodies/. No claim that these or environment-only user messages recover plaintext task bodies.','model_and_effort':'Confirmed independently from turn_context runtime records','fork_turns':'Requested none recorded in spawn arguments; separate unique sessions confirmed','failed_dispatch':'First final_source_audit02 spawn hit concurrency limit; identical intended message was retried successfully after coverage reviewer finalized. Only one actual auditor session exists.'},indent=2)+'\n')
