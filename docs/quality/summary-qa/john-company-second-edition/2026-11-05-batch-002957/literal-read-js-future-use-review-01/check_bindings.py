"""Static prospective-plan bindings; never imports/calls proposal or opens planned data."""
import ast
import hashlib
import json
from pathlib import Path
import re

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
PLAN = ROOT / 'literal-read-js-future-use-plan.json'
PROP = ROOT / 'literal-read-js-format-proposal-01'
PRIOR = ROOT / 'literal-read-js-format-review-01'
MODULE = PROP / 'read_call_format_proposal.py'
ORIGINALS = [ROOT / 'prove-single-reader-grading-delivery-literal-equivalent.py',
             ROOT / 'prove-bounded-delivery.py']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# File traversal is restricted to the two explicitly allowed artifact directories.
# Plan data paths are strings checked below, never opened or traversed.
paths = [PLAN] + ORIGINALS
paths += [p for d in [PROP, PRIOR] for p in sorted(d.rglob('*')) if p.is_file()]
bindings = {str(p): sha(p) for p in paths}
plan = json.loads(PLAN.read_text())
prior = json.loads((PRIOR / 'review.json').read_text())
neutral = json.loads((PRIOR / 'neutral-results.json').read_text())
source = MODULE.read_text()
tree = ast.parse(source)
frozen = next(ast.literal_eval(n.value) for n in tree.body
              if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name)
                  and t.id == '_FROZEN_SOURCE_HASHES' for t in n.targets))
checks = []
def check(name, value):
    checks.append({'name': name, 'passed': bool(value)})

check('plan-remains-prospective', plan['status'] == 'PROSPECTIVE_USE_NOT_YET_ADOPTED_NO_ACTUAL_CALL')
check('exact-module-path', plan['module'] == str(MODULE))
check('exact-reviewed-root-location', plan['runtime_root'] == str(ROOT)
      and MODULE.resolve().parent.parent == ROOT.resolve())
check('exact-module-hash', plan['module_sha256'] == sha(MODULE) == prior['proposal_source_sha256'])
check('exact-prior-review-path', plan['fresh_independent_technical_review'] == str(PRIOR / 'review.json'))
check('exact-prior-review-hash', plan['review_sha256'] == sha(PRIOR / 'review.json'))
check('prior-generic-review-pass', prior['verdict'] == 'PASS' and not prior['blocking_findings'])
check('prior-neutral-evidence-813-pass', neutral['total'] == neutral['passed'] == 813 and neutral['failed'] == 0
      and prior['final_tests']['total'] == 813)
check('prior-review-did-not-adopt-or-run-proof', prior['adopted'] is False and prior['actual_proof_invocations'] == 0)
check('both-original-hashes-match-loader-and-review', all(
      sha(p) == frozen[p.name] == prior['original_source_sha256'][p.name] for p in ORIGINALS))

manifest = json.loads((PRIOR / 'sha256-manifest.json').read_text())
prior_allowed = {str(p.relative_to(PRIOR)): sha(p) for p in paths if p.parent == PRIOR
                 and p.name != 'sha256-manifest.json'}
check('prior-review-artifact-manifest-intact', manifest == prior_allowed)
previous_inputs = json.loads((PRIOR / 'input-hashes.json').read_text())
check('prior-review-proposal-and-original-bindings-still-intact', all(
      key in bindings and bindings[key] == value for key, value in previous_inputs.items()))
check('bank-parameter-fixed-in-plan', plan['bank_name'] == 'expanded-v13-complete-requested-scope')
check('roles-fixed-in-plan', plan['roles'] == ['a', 'b'])
check('separate-role-output-basenames', plan['output_names'] == {
      'a': 'grading-reader-a-js-format-proposal-proof.json',
      'b': 'grading-reader-b-js-format-proposal-proof.json'})
check('all-output-names-pass-reviewed-wrapper-grammar', all(
      re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*-js-format-proposal-proof\.json', value)
      for value in plan['output_names'].values()))

original_tree = ast.parse(ORIGINALS[0].read_text())
prove = next(n for n in original_tree.body if isinstance(n, ast.FunctionDef) and n.name == 'prove')
check('exclusive-output-creation-still-present', any(isinstance(n, ast.Call)
      and isinstance(n.func, ast.Attribute) and n.func.attr == 'open' and n.args
      and isinstance(n.args[0], ast.Constant) and n.args[0].value == 'x' for n in ast.walk(prove)))
check('all-input-hashes-unchanged-after-static-checks', all(sha(Path(path)) == value
      for path, value in bindings.items()))

(OUT / 'input-hash-bindings.json').write_text(json.dumps(bindings, indent=2) + '\n')
result = {'total': len(checks), 'passed': sum(c['passed'] for c in checks),
          'failed': sum(not c['passed'] for c in checks), 'checks': checks,
          'actual_proof_invocations': 0, 'proposal_imported': False,
          'planned_data_paths_opened': False, 'plan_sha256': sha(PLAN)}
(OUT / 'static-check-results.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, indent=2))
raise SystemExit(bool(result['failed']))
