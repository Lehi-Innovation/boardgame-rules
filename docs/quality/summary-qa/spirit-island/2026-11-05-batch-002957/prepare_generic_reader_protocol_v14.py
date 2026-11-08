"""Generic process repair, with no question IDs, rule facts or expected answers."""
from pathlib import Path
import hashlib
import json

B = Path(__file__).resolve().parent
old = (B / 'reader-protocol-v13-template.txt').read_text()
new = old.replace(
    'TWO STAGES, WITH AN ACTUAL-DELIVERY CHECK BEFORE AUTHORING:',
    'THREE STAGES, WITH AN ACTUAL-DELIVERY CHECK BEFORE AUTHORING AND A SEPARATE FINAL REVIEW TURN:'
)
needle = 'During final review, check all entries again for unanswered clauses and for contradictions between your case prose and the quoted rule.'
replacement = 'After all answer batches are written, set stage to "draft_ready", retain every answer and the complete read ledger, notify the parent, and stop this turn. Do not declare the original reader trial complete. The parent will freeze your own full draft without evaluating it and will send both original readers the same purely technical authorization for stage three. Do not begin stage three until that authorization arrives. In stage three, use only the same two rule inputs and your own working output; the parent supplies no gameplay facts, case identifiers, error locations or grading feedback. During this separate final review turn, check all entries again for unanswered clauses and for contradictions between your case prose and the quoted rule.'
assert new.count(needle) == 1
new = new.replace(needle, replacement)
needle = 'State the requested items themselves in the entry; a coverage label does not supply them.'
replacement = needle + '\n\nIndependently recompute every numerical case result and every volunteered remaining quantity from the question\'s stated starting state and the attached rule. Use arithmetic code when useful; verify starting quantities, each change, any cap or rounding rule, and the final quantity. A correct general quotation does not excuse a wrong numerical statement. Check each separately named permission, prohibition or alternative against the complete relevant source unit; give a distinct ruling for each requested alternative rather than assuming a ruling about one action answers a question about another. Do not invent a prohibition merely from an ordering instruction. Remove unnecessary numerical claims instead of introducing extra guesses; retain every actually asked concrete result. This review is a generic method, not another rules source.'
assert new.count(needle) == 1
new = new.replace(needle, replacement)
new = new.replace('On completion set stage to "complete"', 'Only after stage three is authorized and the separate complete review turn is finished, set stage to "complete"')
p = B / 'reader-protocol-v14-template.txt'
assert not p.exists()
p.write_text(new)
resume = 'The original full draft checkpoint is frozen. Begin stage three of your unchanged blind reader instructions: independently review all literal questions, your own complete entries and their relevant summary procedures, including numerical results and separately requested alternatives. Use only the same two rule inputs and your own working output. No gameplay or evaluation feedback is supplied. Finish your own review, retain the full read ledger, set stage to "complete", and return only the output path and answer count.\n'
(B / 'reader-protocol-v14-stage3-technical-resume.txt').write_text(resume)
H = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
record = {
    'version': 'v14', 'pre_authoring_checkpoint': True,
    'prior_v13_template_sha256': H(B / 'reader-protocol-v13-template.txt'),
    'template_sha256': H(p), 'template_characters': len(new),
    'all_rules_authority_still_only_summary': True,
    'question_id_rule_fact_expected_answer_or_case_hint_added': False,
    'same_generic_process_and_all_native_instructions_for_both_new_readers': True,
    'stage2_draft_frozen_before_stage3_but_not_a_completed_reader_trial': True,
    'no_parent_factual_diagnostics_or_feedback_before_both_completed_original_freezes': True,
    'same_original_actor_self_review_not_reader_resampling': True,
    'stage3_technical_resume': {'path': str(B / 'reader-protocol-v14-stage3-technical-resume.txt'), 'sha256': H(B / 'reader-protocol-v14-stage3-technical-resume.txt')},
    'staged_actual_delivery_checker': {'path': str(B / 'verify_staged_reader_actual_delivery.py'), 'sha256': H(B / 'verify_staged_reader_actual_delivery.py')},
    'new_full173_pair_still_required': True,
    'factual_standard_or_fixed_bank_changed': False,
    'parent_full_new_template_actual_read_pending': True,
}
(B / 'generic-reader-protocol-v14-adoption.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'template_characters': len(new), 'template_sha256': H(p), 'stage3_resume_characters': len(resume)}))
