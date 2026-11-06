"""Freeze an explicit bank/audit and identical generic reader protocol; never overwrite."""
from pathlib import Path
import json,hashlib,shutil,sys,difflib
ROOT=Path(__file__).resolve().parent
CANONICAL=Path('/home/jonny/projects/boardgame-rules/rules/sidereal-confluence.md')
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
iteration,bank,audit_name,previous=sys.argv[1:];d=ROOT/iteration
assert not d.exists();audit=ROOT/audit_name/'source-audit.json';review=ROOT/bank/'clean-coverage-scope-review.json'
assert json.loads(audit.read_text())['verdict']=='PASS'
coverage_verdicts=json.loads(review.read_text())['verdicts']
def status(z):return z.get('verdict',z.get('status')) if isinstance(z,dict) else z
for aliases in [('source_key',),('exact_asked_scope','exact_scope'),('coverage_stopping',)]:
 key=next((z for z in aliases if z in coverage_verdicts),None)
 assert key is not None,(aliases,'Missing explicit independent verdict')
 assert status(coverage_verdicts[key])=='PASS',(key,coverage_verdicts[key],'Refusing freeze before all independent gates PASS')
assert CANONICAL.read_bytes()==(audit.parent/'summary-snapshot.md').read_bytes()
q=json.loads((ROOT/bank/'questions.json').read_text())['questions'];k=json.loads((ROOT/bank/'answer-key.json').read_text())['answers'];count=len(q);facts=sum(len(e['required_facts']) for e in k)
d.mkdir();shutil.copyfile(CANONICAL,d/'summary-snapshot.md')
for n in ['questions.json','answer-key.json','asked-facts.json']:shutil.copyfile(ROOT/bank/n,d/n)
shutil.copyfile(ROOT/'source-manifest.json',d/'source-manifest.json');shutil.copyfile(audit,d/'source-audit.json');shutil.copyfile(review,d/'coverage-scope-review.json')
base=(ROOT/'reader-protocol-v4/dispatched-base.txt').read_text();helper=(ROOT/'reader-protocol-v2/source_units.py').read_text()
for who in ['a','b']:(d/f'reader-{who}-prompt.txt').write_text(base.format(summary=(d/'summary-snapshot.md').resolve(),questions=(d/'questions.json').resolve(),output=(d/f'reader-{who}.json').resolve())+helper+'END GENERIC PYTHON CODE')
(d/'prompt-binding.json').write_text(json.dumps({'protocol':'generic-lookup-complete-units-v4-exact-prebound-v10-helper','rules_data':'Summary and questions only; no keys, maps, prior outputs/findings or sources supplied.','same_instructions_except_output':(d/'reader-a-prompt.txt').read_text().replace('reader-a.json','reader-X.json')==(d/'reader-b-prompt.txt').read_text().replace('reader-b.json','reader-X.json'),'embedded_helper_sha256':hashlib.sha256(helper.encode()).hexdigest(),'prompt_hashes':{who:h(d/f'reader-{who}-prompt.txt') for who in ['a','b']},'known_limits':'Known fixed-set tool-assisted regression; instruction/context isolation, no OS file isolation. Supplied code identity and actual returned unit integrity separate from factual grades.'},indent=2)+'\n')
(d/'input-manifest.json').write_text(json.dumps({'iteration':iteration,'bank_version':bank,'question_count':count,'required_facts_per_reader':facts,'requested_reader_model':'gpt-6-luna','requested_effort':'high','fork_turns':'none','hashes':{n:h(d/n) for n in ['summary-snapshot.md','questions.json','answer-key.json','asked-facts.json','source-manifest.json','source-audit.json','coverage-scope-review.json']},'sources':json.loads((d/'source-manifest.json').read_text())['sources'],'source_audit':{'path':str(audit),'fresh_pure_auditor':True,'exact_summary_bytes':True,'unchanged_authorities':True}},indent=2)+'\n')
a=(ROOT/previous/'summary-snapshot.md').read_text();b=(d/'summary-snapshot.md').read_text();(d/'summary-changes.patch').write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile=previous,tofile=iteration)))
print('Frozen',iteration,count,'questions',facts,'facts',bank,audit_name)
