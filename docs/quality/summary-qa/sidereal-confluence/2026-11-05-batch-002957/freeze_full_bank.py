from pathlib import Path
import json,hashlib,shutil,sys,difflib
ROOT=Path(__file__).resolve().parent
CANONICAL=Path('/home/jonny/projects/boardgame-rules/rules/sidereal-confluence.md')
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
iteration=sys.argv[1];d=ROOT/iteration;d.mkdir(exist_ok=False)
review=ROOT/'expanded-v5/clean-coverage-scope-review.json';audit=ROOT/'source-audit-02/source-audit.json'
assert review.exists() and audit.exists()
assert CANONICAL.read_bytes()==(ROOT/'source-audit-02/summary-snapshot.md').read_bytes()
shutil.copyfile(CANONICAL,d/'summary-snapshot.md')
for n in ['questions.json','answer-key.json','asked-facts.json']:shutil.copyfile(ROOT/'expanded-v5'/n,d/n)
shutil.copyfile(ROOT/'source-manifest.json',d/'source-manifest.json');shutil.copyfile(audit,d/'source-audit.json');shutil.copyfile(review,d/'coverage-scope-review.json')
base=(ROOT/'reader-protocol-v2/dispatched-base.txt').read_text().replace('Do not browse or communicate with others.','Do not browse or communicate with others. Do not call ANY collaboration, agent-status or thread tools, including list_agents; never inspect sibling status.')
helper=(ROOT/'reader-protocol-v2/source_units.py').read_text()
for who in ['a','b']:(d/f'reader-{who}-prompt.txt').write_text(base.format(summary=(d/'summary-snapshot.md').resolve(),questions=(d/'questions.json').resolve(),output=(d/f'reader-{who}.json').resolve())+helper+'END GENERIC PYTHON CODE')
(d/'prompt-binding.json').write_text(json.dumps({'protocol':'generic-lookup-complete-units-v3-with-exact-prebound-v10-helper-and-status-tool-ban','rules_data':'Summary and questions only; no keys, maps, prior outputs/findings or sources supplied.','same_instructions_except_output':(d/'reader-a-prompt.txt').read_text().replace('reader-a.json','reader-X.json')==(d/'reader-b-prompt.txt').read_text().replace('reader-b.json','reader-X.json'),'embedded_helper_sha256':hashlib.sha256(helper.encode()).hexdigest(),'prompt_hashes':{who:h(d/f'reader-{who}-prompt.txt') for who in ['a','b']},'known_limits':'Known fixed-set tool-assisted regression; instruction/context isolation, no OS file isolation. Supplied code identity and actual returned unit integrity are separate from factual grades.'},indent=2)+'\n')
(d/'input-manifest.json').write_text(json.dumps({'iteration':iteration,'bank_version':'expanded-v5','question_count':76,'required_facts_per_reader':248,'requested_reader_model':'gpt-6-luna','requested_effort':'high','fork_turns':'none','hashes':{n:h(d/n) for n in ['summary-snapshot.md','questions.json','answer-key.json','asked-facts.json','source-manifest.json','source-audit.json','coverage-scope-review.json']},'sources':json.loads((d/'source-manifest.json').read_text())['sources'],'audit_reuse':{'actual_source_only_audit':str(audit),'unchanged_summary_bytes':True,'unchanged_authorities':True,'pure_auditor_no_repairs_questions_keys_readers_grades':True}},indent=2)+'\n')
a=(ROOT/'seed-iteration-03/summary-snapshot.md').read_text();b=(d/'summary-snapshot.md').read_text();(d/'summary-changes.patch').write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='seed-iteration-03',tofile=iteration)))
print('Frozen',iteration,'76 questions248 facts; exact pure source-audit02 text')
