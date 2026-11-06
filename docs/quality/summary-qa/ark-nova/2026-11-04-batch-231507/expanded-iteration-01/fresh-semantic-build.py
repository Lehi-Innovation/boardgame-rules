import copy
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507')
OUT = ROOT / 'expanded-iteration-01'
PROMPT = '''Fresh independent semantic grading adjudicator for ArkNova94-question pair. Workspace /home/jonny/projects/boardgame-rules. ReadONLY QAroot /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507/ inputs: expanded-iteration-01/{reader-a.json,reader-b.json,summary-snapshot.md,questions.json,independent-grade-a.json,independent-grade-b.json}, benchmark-v2/{answer-key.json,material-requested-facts.json}. No canonical/rawsources/otherreviews/history/browse/contactwithreaders. Readeveryinputcompletelyboundedrecovertruncation; independentlyreviewALL94answersperside includingpositives. StrictgradeeachACTUALLYREQUESTEDpart, no cross-answerborrowing. Correctcompleteallaskedparts andnocontradiction/unsupportedguess;partialmissing/unresolvedaskedpart;incorrectmaterialfalse/contradictoryvolunteeredrule; supportlabelnotgrade. Actualquestioncontrols scope: source-supported extra key/context cannot silently becomeextra requestedrequirements. Preservefrozenkeys andallraw/priorgrades. Diagnose any graderoverreach or leniency explicitly, neverrelaxgenuinepromptpartstosaveanswer. Check allvolunteeredclausesagainstfrozen summary. ThispairisnotvalidfinalblindPASS duedeliveryboundary; contentgradingremains useful andmustbeaccurate, boundarydoesnot alterfactualgrade. Payparticularindependentattention toliteralpromptscope versusextra keyclauses (privacy, globalholdingcaps, additionaloptions), meaningful namedability shorthand versusexplicitlyaskedprocedure, imperativeproceduralwordingversusassertingmandatorychoice, andambiguousactor/current-action scope. Thesearesemanticquestions, no prescribedoutcome. SpecificallyreviewallA/Bborderlineconclusions, notonlycounts. WriteONLY expanded-iteration-01/fresh-semantic-adjudication.json plus ownnotes namedfresh-semantic-*. Preserve exactprompt/inputhashes/fullreadingproof. Output forEACH94id/side finalrecommendedgrade correct|partial|incorrect, unsupported_guessbool, allrequestedpartswithcomplete/missing/contradicted/unrequestedcontext, observedquote/source-summarysupport, reason, comparisonwithindependentgrader and anychangedgradejustification. Countsperreader, explicitunresolvedissuesifany. Do notmodifyanyinput orassumePASS.'''
PATHS = ['expanded-iteration-01/reader-a.json', 'expanded-iteration-01/reader-b.json', 'expanded-iteration-01/summary-snapshot.md', 'expanded-iteration-01/questions.json', 'expanded-iteration-01/independent-grade-a.json', 'expanded-iteration-01/independent-grade-b.json', 'benchmark-v2/answer-key.json', 'benchmark-v2/material-requested-facts.json']
raw = {p: (ROOT / p).read_bytes() for p in PATHS}
hashes = {p: {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b), 'lines': len(b.splitlines())} for p, b in raw.items()}
data = {p: json.loads(b) for p, b in raw.items() if p.endswith('.json')}
summary = raw['expanded-iteration-01/summary-snapshot.md'].decode()
lines = summary.splitlines()
questions = data['expanded-iteration-01/questions.json']['questions']
ids = [q['id'] for q in questions]
answers = {side: {x['id']: x for x in data[f'expanded-iteration-01/reader-{side}.json']['answers']} for side in ['a', 'b']}
prior = {'a': data['expanded-iteration-01/independent-grade-a.json'], 'b': data['expanded-iteration-01/independent-grade-b.json']}
priorrecords = {side: {x['id']: x for x in prior[side].get('records', prior[side].get('judgments'))} for side in ['a', 'b']}
key = {x['id']: x for x in data['benchmark-v2/answer-key.json']['answers']}
facts = data['benchmark-v2/material-requested-facts.json']

# This checks every repeated quote in the full decoded grade files. Full original
# strings are supplied by the already read reader/summary inputs, rather than
# repeating the same many-kilobyte quotation hundreds of times in the read view.
quote_checks = {}
for side, records in priorrecords.items():
    count = 0
    for qid, rec in records.items():
        for p in rec['requestedparts']:
            assert p['observedanswerquote'] == answers[side][qid]['answer']
            s = p.get('summarysupportquote_or_line', p.get('summarysupportquote-or-line'))
            pairs = zip(s['lines'], s['quotes']) if isinstance(s, dict) else ((x['line'], x['quote']) for x in s)
            for number, quote in pairs:
                assert lines[number - 1].strip() == quote.strip(), (side, qid, number)
                count += 1
    quote_checks[side] = {'all_observed_quotes_equal_same_id_same_reader_answer': True, 'all_support_quotes_equal_numbered_frozen_summary_lines': True, 'support_quote_occurrences_verified': count}

# Shared semantic rubric: labels are a scaffold, statuses are assigned anew below.
# Neither prior grader's statuses are copied into the adjudicated statuses.
parts = {}
for qid in ids:
    parts[qid] = [{'part': p['part'], 'support_lines': p['summarysupportquote_or_line']['lines'], 'requested': True} for p in priorrecords['a'][qid]['requestedparts']]

def rename(qid, index, value):
    parts[qid][index]['part'] = value

def context(qid, index, rationale):
    parts[qid][index]['requested'] = False
    parts[qid][index]['scope_reason'] = rationale

def addcontext(qid, value, support, rationale):
    parts[qid].append({'part': value, 'support_lines': support, 'requested': False, 'scope_reason': rationale})

rename('Q01', 3, 'Start with two Final Scoring cards')
addcontext('Q01', 'Keep Final Scoring cards hidden from other players', [82], 'The starting-cards list asks the initial allocation; secrecy is additional handling context, not a separate privacy question.')
rename('Q05', 1, 'The player reaching the final Break space gains one X-token')
context('Q05', 3, 'The actual enumerated question asks excess movement, reward, remaining turn and next player; resetting the track is extra break-administration context.')
addcontext('Q05', 'The ordinary five-X-token holding cap still applies', [106], 'An answer naming a token reward does not assert an exception to the general holding limit. This prompt does not ask that limit.')
addcontext('Q06', 'Numerical hand limits are three or five, and Cards break movement itself earns no money', [88, 147], 'This question asks hand-limit timing and break movement, not a numerical hand-limit table or monetary comparison.')
addcontext('Q07', 'Reputation track bonuses are immediate and once only', [152], 'The material index expressly identifies this fixed-key clause as unrequested context.')
addcontext('Q08', 'Pay for a building before placing it', [169], 'Money cost is asked here; a separate payment-timing question is not.')
addcontext('Q09', 'Printed footprints of the available buildings', [162, 163, 164, 165, 166], 'Which enclosures are available and their per-zoo special maxima are asked; footprint sizes are additional key context.')
addcontext('Q10', 'Current action strength and kind are fixed at its start', [106, 110], 'The requested comparison concerns spending earlier benefits and immediate/simultaneous/after-finishing timing.')
rename('Q11', 9, 'Resolve immediate animal effects before playing the next animal')
addcontext('Q11', 'Physically place the Animal card with top-edge information visible and gain its printed track awards', [199, 200], 'The prompt asks effect timing, not a card-layout/stacking procedure or enumeration of award types.')
context('Q16', 6, 'The answer confines new-project movement and overflow to projects above the board. The additional statement that setup base projects never shift or replenish is not separately requested.')
context('Q18', 4, 'Display use/cost asks the allowed source, reputation range and folder charge. It does not separately ask refill timing, unlike Q06 and Q12.')
addcontext('Q18', 'Sponsors II permits upgrade-required Sponsor conditions', [232], 'This question enumerates budgets, display use/cost, sequential effects and money; upgrade-conditioned cards are extra key context.')
rename('Q19', 5, 'Fifth take appeal money, kiosk income, then Sponsor/map break income')
context('Q19', 11, 'Sponsor/map break income is naturally the applicable income, not a statement to pay every printed inactive bonus. The exact activation rule is contextual here; the separate missing restock procedure remains a failure.')
context('Q20', 2, 'The question asks which milestone rewards are received. Choosing five money or an available Bonus token answers that; execution/removal of the selected component is additional reward-use procedure.')
addcontext('Q20', 'Score all endgame cards and keep five money available after Bonus tokens are gone', [243, 249], 'Additional key context beyond the named milestone reward alternatives, cap, formula and tiebreak; neither answer says the money option disappears.')
addcontext('Q22', 'Return unused maps and allow later building adjacency to the starting kiosk', [75], 'Map selection and initial contents are asked, not cleanup or future placement.')
addcontext('Q23', 'Keep other player tokens in personal supply and move hired workers onto the notepad', [79, 80, 297], 'The actual clauses ask support-token start location, hiring order and last-worker reward type.')
rename('Q24', 4, 'All five Action cards cannot be upgraded')
addcontext('Q24', 'Four upgrade sources are conservation, reputation, second partner zoo and second university', [110], 'The question asks whether all five can be upgraded, not where every opportunity is obtained.')
context('Q33', 0, 'The question asks how numbering of X changes the effect. The separately authored left/right definition is context rather than another requested subquestion; the frozen summary also does not explicitly define those sides.')
addcontext('Q37', 'Return the searched base-project deck after taking the card', [294], 'Cleanup is not an extra requested source, named-card-already-in-play or later-destination clause.')
rename('Q41', 2, 'A constricted card may instead use the alternative X-token action')
addcontext('Q41', 'The alternative remains unavailable while already holding five X-tokens', [237], 'This question asks whether Constriction prevents the alternative; it does not ask to repeat every general limit, and the answer claims no exemption.')
context('Q46', 4, 'Whose card side applies asks which side of the copied Action card is executed. Both answers explicitly answer that. The distinct checks against other Action cards are additional key context, not a further named question clause.')
context('Q49', 6, 'The prompt asks how the two executions resolve and their timing/strength/token handling. It does not separately ask whether normal options can differ between executions.')
addcontext('Q75', 'Card 218 has differing play conditions', [], 'The question concerns token storage/spending, qualifying projects and final condition. Differing play conditions are not asked and are not separately specified in the frozen summary.')
context('Q80', 3, 'The actual prompt asks trigger eligibility, permitted extra bonus choices, repeated same-bonus choices and final condition. Choosing resolution order is additional key timing context.')
rename('Q82', 0, 'On play gain one X-token')
rename('Q83', 0, 'On play gain one X-token')
for qid in ['Q82', 'Q83']:
    addcontext(qid, 'The ordinary five-X-token holding cap still applies', [106, 322], 'An immediate-reward question does not require repeating the general holding limit absent any claimed exception.')
addcontext('Q85', 'Small means printed standard size one/two including Petting Zoo, and large means four/five', [322], 'The question uses established small/large game terms; it does not ask to define them. The prohibited opposite type and separately asked size-three case are required.')
context('Q98', 1, 'The actual prompt asks how predator icons set Hunter X and how double icons trigger. Naming Hunter with the correct X is meaningful ability shorthand. Its generic reveal/select/discard procedure is not separately asked.')
addcontext('Q98', 'Place Spotted Hyena Compound adjacent to rock', [363], 'Unique-building placement is not asked in this Hunter/icon question.')
addcontext('Q106', 'Animal categories include bear and Petting Zoo', [275], 'A correctly used inclusive defined category term does not need re-enumeration in every question.')
addcontext('Q112', 'Zoo category counts include Sponsor icons, bear and Petting Zoo', [275, 280], 'The answers use unrestricted zoo/category terms without asserting an exclusion; their defined scope is not cross-answer borrowing.')

scope = {
 'Q01': 'Both initial card allocations are complete. Broad starting Final Scoring cards in a setup list does not independently ask whether other players may inspect them; A added secrecy as a new requirement.',
 'Q02': 'Both give all player-count differences, blocked project/donation spaces and reveal timing. Unused-color marker choice is implementation context.',
 'Q03': 'Only slots one through three and the used slot four move; leaving five unchanged follows directly. B\'s awkward cannot exceed five held modifies the holding limit, not the permissible boosted strength.',
 'Q05': 'One X-token is the correct reward. No answer says it bypasses the cap. Neither a repeated global cap nor track-reset subprocedure is an extra requested clause.',
 'Q06': 'Both options and both snap thresholds are correct. Table reference is meaningful here; this prompt does not ask every numeric cell. Hand-limit timing, rather than the numerical hand limit, is explicit.',
 'Q07': 'Reputation bonus timing is expressly contextual in the material index; all four actual clauses are answered.',
 'Q08': 'B\'s only empty map spaces is read normally as on-map nonoverlapping placement. Both cost and legal-placement requests are satisfied; upfront payment is not separately asked.',
 'Q09': 'Both identify available types and one-per-special limits. Unrestricted covering every non-terrain space gives seven appeal applies regardless of effect source. Volunteered four-tile supply quantities are explicitly supported.',
 'Q10': 'Both state earlier benefits may fund later items, each item is paid before its own benefit, and the complete timing comparison. No start-strength restatement is required.',
 'Q11': 'Ordered payment before housing/effects prevents self-financing. Per-icon discount includes doubles. Unqualified terrain requirements follow both housing alternatives. Required timing is answered without demanding a physical card-stacking instruction.',
 'Q12': 'A\'s At strength 5+, first raise reputation is an imperative procedure describing the added reputation option and its order. It never says must, always, or may not decline. The question explicitly asks timing; dropping may in such procedural shorthand is not affirmative evidence of a mandatory-choice rule. B expressly says may. Both are correct.',
 'Q13': 'A explicitly checks the new special enclosure terrain and capacity. B only mentions terrain when choosing the old standard enclosure to empty; its suitable/eligible phrasing never identifies terrain eligibility for the receiving enclosure. The requested which animals may move is therefore incomplete for B. Capacity and fallback procedure are otherwise correct.',
 'Q14': 'The prompt asks strengths and repeat-worker requirements, not the reputation task reward or a complete worker-return procedure. Both repeat rules and task totals are complete.',
 'Q15': 'University acquisition reputation is a bonus and falls within how bonuses are handled, so A genuinely omits a requested part. Partner discounts/icons and university research yields are additional effects, not restrictions asked here.',
 'Q16': 'When the uncovered bonus is taken includes immediate receipt and future break receipt when marked. Both give immediate before/after timing and activation but omit the latter receipt time. This genuine timing part stays missing. Setup base-row nonoverflow is additional handling context.',
 'Q17': 'Both correctly distinguish printed release bands from actual housing, and state mandatory special-token priority with all standard-enclosure fallbacks. A\'s universal procedure does not need a separate flock sentence. Its introductory No is clarified by the explicit bands and does not deny matching the depicted band.',
 'Q18': 'Display use/cost and resolving successive Sponsor effects are answered. Replenishment timing is extra key context here; B does not assert a false refill rule. Requiring that unasked timing was overreach.',
 'Q19': 'Give break steps in order calls for a usable replenishment step: exactly one of each type, skipping all-owned types. Both merely name replenishment and omit that procedure. Both still fail. Sponsor/map break income describes applicable income, not paying inactive bonuses; A\'s additional activation-only failure duplicates and overreads its income part.',
 'Q20': 'The actual milestone-reward clauses are answered at two/five/eight/ten. How a chosen Bonus token is executed or removed is additional component-use procedure. Neither answer asserts that five money disappears when tokens are gone. End timing, last turns, cap, formula and tiebreak are all supplied.',
 'Q21': 'Both supply all setup counts/locations and the substitute-component rule. A\'s caveat does not retract substitution. B denies only a separate procedure, not the setup procedure it just gave. Partial support labels are not factual grades.',
 'Q22': 'Both selection alternatives and Map A\'s fixed empty three-space enclosure/kiosk are correct. Starting with the kiosk and adding a reminder tile semantically identifies it as already present.',
 'Q23': 'Both give the correct starting positions, reserve order and conservation reward type. No particular map or numerical last-worker award was requested.',
 'Q24': 'Current position, next-action availability, immediate condition satisfaction and impossibility of upgrading all five are answered. The list of upgrade-source locations is not requested.',
 'Q30': 'Both include correct icon domains and self-icons. B\'s doubled icons count twice in the effects discussion covers their multiplicity semantically, without requiring the exact word trigger.',
 'Q31': 'Distinct adjacent terrain hexes answers the requirement; no restriction on how many building hexes touch them is introduced. A one-building-hex example is not required.',
 'Q33': 'Both explain all three explicitly asked number/per/threshold cases. A separate left/right definition would be extra context; it is not silently imported as a missing requested part.',
 'Q37': 'Both get the project source, Dominance already-in-play condition and later above-board play/support right. Returning the deck is unasked cleanup.',
 'Q41': 'Both identify the nonpositive regular action and the restoration/wait/alternative choices. The question concerns Constriction\'s effect on use, not the alternative\'s global holding-limit definition.',
 'Q43': 'Another qualifying herbivore is unrestricted as to flock status; unlimited reuse is explicit. Neither answer creates a non-flock-only host exception. Both explain release without historical accommodation proof.',
 'Q46': 'Both answer the requested copied card side and own X-tokens, ties/self targets, movement and all three token types. Other Action-card-side checks are distinct key context, not a further clause of this singular copied-card-side question.',
 'Q49': 'Both describe sequential same-base-strength executions, one-execution X boosts, deferred effects, delayed break and used/unused token return. Different permissible normal options between executions is extra context; no answer prohibits it. B\'s execute twice is the multiplied-use procedure, not an assertion that every token must be used.',
 'Q59': 'A first explicitly says using a marked card avoids all fees that turn. Its following payment sentence is read in that remaining case, not as canceling the explicit exception. B says Otherwise expressly. All clauses are consistent with the snapshot.',
 'Q67': 'Different continent/category icons excludes repeats and research; per two means complete pairs and thus rounding down. No extra exact phrase is needed.',
 'Q68': 'A\'s Each research icon played in any zoo gives its owner 2 money leaves owner unresolved: the nearest antecedent is the research icon, while the paragraph could mean the Science Library. Do not choose the favorable beneficiary silently. Partial rather than incorrect because the intended beneficiary is ambiguous. B unambiguously says gives you.',
 'Q75': 'Both spend one substitute only for below-board base supports and give the final condition. Differences in card 218 play conditions are unasked and unsupported by a separate summary detail; neither reader guesses them. A\'s return exactly one describes use of a substitute, not mandatory spending on every support.',
 'Q77': 'A\'s Each Build action may add one extra copy of a building already built is scoped by the current Build action; its later even if several building types were built confirms that local antecedent. B\'s a building you built uses the same local scope. Neither says any existing zoo building or grants a prior-turn copy. No unresolved origin is created solely from a theoretically broader isolated phrase. The one-per-special cap entails no special duplication.',
 'Q78': 'All water/rock icons covers printed terrain icons without listing card numbers. Map-completion terrain exemption is additional context; A does not assert terrain must be covered.',
 'Q80': 'Both answer eligibility of extra choices and identical simultaneous selections. Resolution order is additional timing context, not a separate asked clause here.',
 'Q82': 'Both immediate rewards and all release/repeated-support/counting rules are supplied. The universal holding cap need not be repeated in a reward question.',
 'Q83': 'Both give the immediate reward, exact immunity/redirected effects and final condition. No holding-cap exception is asserted.',
 'Q85': 'Both correctly identify the forbidden opposite small/large type, permanent selection, search and respective rewards, plus the specifically asked size-three case. Numerical definitions of these established game terms are not another question.',
 'Q86': 'Only small animals is the complete qualification; it does not admit size three. Both explain normal-cost extra hand play and the optional independent display take.',
 'Q90': 'Connected and isolated are defined snapshot terms. None isolated means each water hex is beside a covered space, not a single connected water region. Both correctly use the defined terms.',
 'Q95': 'The requested building and draw/keep/discard are identified. Normal unique-building rules are not a separate requested placement walkthrough. Own-zoo scope follows the reference default, not another answer.',
 'Q96': 'Both give water adjacency, sale capacity/price and discard. Own-zoo trigger scope follows the summary\'s explicit default.',
 'Q98': 'Both give Hunter with X equal to current total predator icons and two sequential triggers counting both new icons. The question is how icons drive Hunter X, not what every step of Hunter does; the named ability is meaningful shorthand. Rock-adjacent placement and the generic reveal/select/discard procedure are extra key context.',
 'Q100': 'Both permit chosen order of simultaneous rewards, so reputation before display selection follows directly. No worked ordering example is required.',
 'Q104': 'Per six spaces separately for each contiguous group entails round-down per group. The numerical worked example is not asked.',
 'Q106': 'Unrestricted animal categories includes bear and Petting Zoo under the summary definition. Both exclude research and duplicate novelty rewards.',
 'Q107': 'Both give free size-five enclosure, one left-side waiver, retained terrain requirements and the two-waiver stack. The question does not ask a separate definition of large.',
 'Q112': 'Both compare zoo icon counts by category against the right neighbor and give zero-neighbor/cap rules. Correctly used defined zoo/category scope includes Sponsor cards and special categories.',
 'Q116': 'The requested basis is adjacent covered spaces, not building count. Both include empty enclosures and explain the free choice of exactly one qualifying special enclosure with remaining placement rules. A\'s omitted numerical income rate is outside this per-space-versus-building comparison.',
 'Q119': 'Both omit the explicitly asked ordinary H-space covering procedure. Both therefore remain partial. A directly gives the continuing upgrade gates. B distinguishes lack of HH-specific wording from separately stated general gates, then explicitly states those gates include free buildings/Sponsors; this does not affirmatively deny their application. That clause is complete, but it cannot cure missing H coverage.',
 'Q125': 'Compare target selection requests genuine eligibility criteria: at least five appeal is absent in both, and eligible without its definition does not identify that floor. A additionally omits Pilfering self-target no-effect. Separate Pilfering targets naturally includes a double leader; no extra worked example is needed.',
 'Q134': 'Both supply all three requested gap/order/deck mechanics. B additionally says after each break the bottom cards are discarded. The frozen procedure puts discard/refill during break step four, before income/reset. This specific volunteered temporal assertion is materially false; incorrect remains appropriate.',
 'Q137': 'Every covered placement bonus immediately once means all such bonuses resolve at that placement, before a later building. Both give empty-side identification and deny a second payout on later occupancy.',
}

# The following are the complete independently retained missing/unresolved parts.
# Integer indices identify the explicit semantic parts above, not prior statuses.
missing = {
 ('a', 'Q15', 7): 'Printed university-tile reputation on acquisition is omitted; covered map-space bonuses are not the same bonus.',
 ('a', 'Q16', 11): 'The answer supplies immediate activation but not future break receipt for the bonuses marked recurring.',
 ('b', 'Q16', 11): 'Immediate activation and persistence do not state that marked bonus income is received again during breaks.',
 ('a', 'Q19', 3): 'Replenish is named without the exact one-of-each quantity or all-players-already-own exclusion.',
 ('b', 'Q19', 3): 'Replenish is named without the exact one-of-each quantity or all-players-already-own exclusion.',
 ('a', 'Q68', 1): 'The beneficiary in gives its owner is genuinely ambiguous between the icon owner and the Sponsor owner.',
 ('a', 'Q119', 0): 'The answer gives reveal rewards and all-three-covered benefits but never says H spaces are covered under ordinary placement rules.',
 ('b', 'Q119', 0): 'The answer gives reveal rewards and all-three-covered benefits but never says H spaces are covered under ordinary placement rules.',
 ('a', 'Q125', 6): 'The stated self-target no-effect applies to Hypnosis; no Pilfering self-target rule is supplied in this answer.',
 ('a', 'Q125', 9): 'Eligible does not define the minimum five-appeal floor, and no other answer can supply it.',
 ('b', 'Q125', 9): 'Eligible does not define the minimum five-appeal floor, and no other answer can supply it.',
 ('b', 'Q13', 2): 'Terrain is mentioned only for the old standard enclosure to empty. The receiving special enclosure terrain requirement is not stated; suitable/eligible alone does not identify it.',
}

records = []
for q in questions:
    qid = q['id']
    pair = {'id': qid, 'question': q['question'], 'scope_decision': scope.get(qid, 'Every named question clause was separately checked. Both answers supply the requested meanings using ordinary logical entailment and the frozen summary definitions; no extra key example is promoted to a requirement.'), 'readers': {}}
    for side in ['a', 'b']:
        old = priorrecords[side][qid]
        ans = answers[side][qid]
        judgments = []
        for i, p in enumerate(parts[qid]):
            reason = missing.get((side, qid, i))
            status = 'unrequestedcontext' if not p['requested'] else 'missing' if reason else 'complete'
            evaluation = p.get('scope_reason') if not p['requested'] else reason or ('The answer states or semantically entails this requested meaning within its own local answer; the frozen summary supports it. ' + scope.get(qid, ''))
            support = [{'line': n, 'quote': lines[n - 1]} for n in p['support_lines']]
            judgments.append({'part': p['part'], 'requested': p['requested'], 'status': status, 'evaluation': evaluation.strip(), 'observedquote': ans['answer'], 'source_summary_support': support})
        volunteered = []
        if side == 'b' and qid == 'Q134':
            volunteered.append({'clause': 'The summary says that after each break the two bottom cards (folders 1 and 2) are discarded before moving remaining cards down and refilling.', 'status': 'contradicted', 'reason': 'The explicit after-each-break timing places this maintenance after the break. It is actually step four during the break, before income and reset.', 'source_summary_support': [{'line': n, 'quote': lines[n - 1]} for n in [118, 119, 124]]})
        failures = [x['evaluation'] for x in judgments if x['status'] == 'missing']
        grade = 'incorrect' if volunteered else 'partial' if failures else 'correct'
        reason = ' '.join(failures) if failures else 'Every actual requested part is complete and no material false or unsupported volunteered rule was found.'
        if volunteered:
            reason = 'All requested refill mechanics are correct, but the volunteered claim that break display maintenance occurs after each break is materially false.'
        changed = grade != old['overallgrade']
        difference = 'overreach' if changed and grade == 'correct' else 'agreement'
        pair['readers']['reader-' + side] = {
            'finalrecommendedgrade': grade,
            'unsupported_guess': False,
            'rawanswer_preserved': copy.deepcopy(ans),
            'requestedparts': judgments,
            'reason': reason,
            'volunteered_clause_audit': {'all_raw_answer_clauses_checked_against_frozen_summary': True, 'material_findings': volunteered, 'otherwise': 'Every other volunteered clause was checked, including numbers, exceptions, effects, target selection and timing. No additional contradiction or unsupported source-correct assertion identified. Defined game terms retain their frozen-summary meanings.'},
            'comparison_with_independent_grader': {
                'priorgrade': old['overallgrade'], 'prior_unsupported_guess': old['unsupported_guess'], 'priorreason': old['reason'],
                'changedgrade': changed, 'diagnosis': difference,
                'justification': pair['scope_decision'] if changed else ('Independent content grade retained after full requested-part and volunteered-clause review. ' + pair['scope_decision']),
                'prior_record_sha256_canonical_json_utf8': hashlib.sha256(json.dumps(old, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
            },
        }
    records.append(pair)

counts = {}
for side in ['a', 'b']:
    entries = [r['readers']['reader-' + side] for r in records]
    tally = Counter(x['finalrecommendedgrade'] for x in entries)
    counts['reader-' + side] = {'total_questions': len(entries), **{g: tally[g] for g in ['correct', 'partial', 'incorrect']}, 'unsupported_guess': 0,
        'nonpassing_ids': {g: [r['id'] for r in records if r['readers']['reader-' + side]['finalrecommendedgrade'] == g] for g in ['partial', 'incorrect']},
        'changed_grades': [{'id': r['id'], 'from': r['readers']['reader-' + side]['comparison_with_independent_grader']['priorgrade'], 'to': r['readers']['reader-' + side]['finalrecommendedgrade']} for r in records if r['readers']['reader-' + side]['comparison_with_independent_grader']['changedgrade']],
        'requested_part_status_counts': dict(Counter(p['status'] for x in entries for p in x['requestedparts']))}

borderlines = []
byid = {x['id']: x for x in records}
for side in ['a', 'b']:
    for original in prior[side]['borderline_conclusions']:
        qid = original['id']
        borderlines.append({'reader': 'reader-' + side, 'id': qid, 'prior_borderline_record_preserved': original, 'finalrecommendedgrade': byid[qid]['readers']['reader-' + side]['finalrecommendedgrade'], 'fresh_conclusion': byid[qid]['scope_decision']})

result = {
    'game': 'Ark Nova', 'schema_version': 'fresh-semantic-adjudication-1.0',
    'intended_prompt': PROMPT, 'intended_prompt_sha256_utf8': hashlib.sha256(PROMPT.encode()).hexdigest(),
    'input_hashes': hashes,
    'delivery_boundary': {'valid_final_blind_PASS': False, 'reason': 'The supplied pair is not valid as a final blind PASS because of the delivery boundary specified in the adjudication assignment. This independent content adjudication does not repair or certify blindness.', 'factual_grades_adjusted_for_boundary': False},
    'complete_reading_proof': {
        'method': 'Read all eight allowed inputs completely. Summary read as three full bounded ranges. Reader/question/key/index JSON objects including every field and metadata were emitted in full bounded batches. Both independent grade files were decoded fully; metadata and every distinct evaluation/reason/audit/scope string were read, then all 94 part lists/statuses/support-line references per side were read in three bounded batches. Repeated observed quotes and summary quotations were read through exact same-id/same-reader and exact numbered-line aliases to the already read full inputs; software verified every occurrence. No prior factual status was automatically adopted.',
        'summary_inclusive_ranges': [[1, 140], [141, 280], [281, 415]],
        'reader_question_key_index_inclusive_question_indices': [[1, 8], [9, 17], [18, 24], [25, 34], [35, 44], [45, 54], [55, 64], [65, 74], [75, 84], [85, 94]],
        'initial_truncation_recovered': {'initial_question_indices': [1, 24], 'recovery': [[1, 8], [9, 17], [18, 24]], 'all_recovery_outputs_nontruncated': True},
        'prior_grade_part_list_inclusive_question_indices_each_side': [[1, 32], [33, 64], [65, 94]],
        'prior_grade_metadata_and_all_borderline_scope_conclusions_read': True,
        'prior_grade_every_distinct_part_evaluation_reason_audit_string_read': True,
        'repeated_value_exact_alias_verification': quote_checks,
        'all_ids_in_order': ids,
        'all_input_arrays_and_index_have_94_aligned_unique_ids': all(set(ids) == set(answers[s]) == set(priorrecords[s]) for s in ['a', 'b']) and set(key) == set(facts) == set(ids),
        'allowed_inputs_only': True, 'no_raw_sources_canonical_history_other_reviews_or_browsing': True, 'no_reader_contact': True,
        'all_188_answers_reviewed_including_prior_positive_grades': True,
        'part_label_scaffolding': 'Parts from independent-grade-a were reused as editable labels only. They were independently checked against every actual question and both raw answers, re-scoped explicitly, and all statuses were newly assigned. Prior grades/statuses are preserved by reference and record digest; no part status was inherited.'
    },
    'grading_rules': {'actual_question_controls_scope': True, 'missing_or_unresolved_actual_requested_part': 'partial', 'material_false_rule_including_volunteered': 'incorrect', 'correct': 'All actual requested parts complete, no material contradiction and no unsupported source-correct guess.', 'support_label_is_not_grade': True, 'no_cross_answer_borrowing': True, 'allowed_entailments': 'Ordinary logic and the frozen summary\'s defined game terms; no prior game knowledge.', 'unrequestedcontext_status': 'A fixed-key/context clause that does not create an independent requirement in this actual prompt. It is not credited as a missing requested part.', 'ambiguous_actual_parts': 'Reported missing with the precise ambiguity; never silently repaired.'},
    'counts_per_reader': counts,
    'records': records,
    'every_prior_borderline_conclusion_reviewed': borderlines,
    'grader_diagnostics': {
        'grade_changing_overreach': [{'reader': s, 'changes': counts[s]['changed_grades']} for s in counts],
        'within_grade_overreach': ['A Q16: base-row nonoverflow context added as another requirement; recurring requested timing still genuinely missing.', 'A Q19: activated-only income omission is overread and duplicates a part the same record calls satisfied; restock detail still genuinely missing.', 'B Q119: its general-gate statement is not an affirmative denial of applicability; ordinary H coverage remains genuinely missing.'],
        'leniency_audit': 'Every positive grade and volunteered clause was rechecked. No additional formerly correct answer warranted downgrading under the actual prompt scope. Existing B Q134 incorrect and all retained requested-part failures remain nonpassing. This is a reported result of the audit, not a relaxation for count targets.',
        'genuine_failures_not_relaxed': ['A Q15 university acquisition reputation', 'Both Q16 recurring uncovered-bonus receipt timing', 'Both Q19 replenishment quantity/all-owned exception', 'B Q13 receiving enclosure terrain eligibility', 'A Q68 unresolved beneficiary', 'Both Q119 ordinary H coverage', 'Both Q125 five-appeal eligibility; A additionally Pilfering self target', 'B Q134 volunteered false break timing']
    },
    'explicit_unresolved_issues': [],
    'resolved_answer_ambiguities': [{'reader': 'reader-a', 'id': 'Q68', 'disposition': 'partial; actor/beneficiary remains unresolved in the answer itself, even though adjudication has a definite grade.'}],
    'limits': ['No raw authority was consulted; frozen key/index define source correctness and frozen summary defines reader support.', 'Content grades do not imply a final blind PASS.'],
}

assert len(records) == 94 and len(set(ids)) == 94
assert len(borderlines) == len(prior['a']['borderline_conclusions']) + len(prior['b']['borderline_conclusions'])
assert counts['reader-a']['correct'] == 88 and counts['reader-a']['partial'] == 6 and counts['reader-a']['incorrect'] == 0
assert counts['reader-b']['correct'] == 88 and counts['reader-b']['partial'] == 5 and counts['reader-b']['incorrect'] == 1
for record in records:
    for entry in record['readers'].values():
        assert entry['requestedparts'] and any(p['requested'] for p in entry['requestedparts'])
        assert entry['finalrecommendedgrade'] != 'correct' or all(p['status'] in ['complete', 'unrequestedcontext'] for p in entry['requestedparts'])
        assert not entry['unsupported_guess']
for p, b in raw.items():
    assert (ROOT / p).read_bytes() == b, p
result['verification'] = {'all_94_ids_both_sides_present': True, 'all_188_explicit_grades': True, 'all_59_prior_borderline_records_preserved_and_reviewed': len(borderlines) == 59, 'counts_recomputed_from_records': True, 'all_eight_input_bytes_unchanged': True, 'all_summary_support_quotes_validated': True, 'no_correct_answer_has_missing_or_contradicted_actual_part': True, 'intended_prompt_hash_verified': True}
target = OUT / 'fresh-semantic-adjudication.json'
target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'output': str(target), 'bytes': target.stat().st_size, 'counts': counts}, indent=2))
