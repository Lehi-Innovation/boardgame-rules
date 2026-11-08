from pathlib import Path
import datetime, hashlib, json, shutil

B = Path(__file__).parent
O, V = B / 'expanded-candidate-v5', B / 'expanded-candidate-v6'
assert not V.exists(), 'Never overwrite a historical candidate'
V.mkdir()
for name in ['questions.json', 'answer-key.json', 'asked-clause-map.json', 'coverage-map.json', 'coverage-ledger.json']:
    shutil.copyfile(O / name, V / name)
q = json.loads((V / 'questions.json').read_text())
k = json.loads((V / 'answer-key.json').read_text())
s = json.loads((V / 'asked-clause-map.json').read_text())
qm, km, sm = ({x['id']: x for x in a} for a in [q['questions'], k['answers'], s])
changes = []

def scope(i, asked, extra=(), givens=None):
    sm[i]['asked_facts'] = asked
    sm[i]['contextual_background'] += list(extra)
    if givens is not None:
        sm[i]['scenario_givens'] = givens
    km[i]['required_facts'] = asked.copy()
    km[i]['contextual_background'] = sm[i]['contextual_background'].copy()
    changes.append(i)

a = sm['Q01']['asked_facts'].copy()
a[0] = 'Separately shuffle asset, demand, event and investment decks, and the five action-type decks (construction, biotech, labor, media and security).'
a[4] = 'Randomly select a capital token to choose the active player, who starts at 10 capital; clockwise players start at 11, 12, and so on.'
scope('Q01', a)
scope('Q09', [
    'Produce before increasing unrest, using existing applicable production modifiers: stable/protest produce under those modifiers; strike/outage produce no resources.',
    *sm['Q09']['asked_facts']
])
sm['Q09']['contextual_background'] = ['No district resource quantities are supplied; do not invent production amounts.']
km['Q09']['contextual_background'] = sm['Q09']['contextual_background'].copy()
km['Q09']['expected_answer'] = km['Q09']['expected_answer'].replace('Produce first under existing modifiers.', 'Produce first under existing modifiers: stable/protest can produce; strike/outage produce nothing.')
a = sm['Q15']['asked_facts'].copy(); a[-1] = 'After a nonfinal demand round, advance to the next standard round; the third demand ends the game.'
scope('Q15', a)
km['Q15']['expected_answer'] = km['Q15']['expected_answer'].replace('Advance round to standard.', 'After a nonfinal demand, advance round to standard; there is no next standard round after the third demand.')
scope('Q16', sm['Q16']['asked_facts'], givens=['The third demand fails, pushing threat to 25.', 'The Federalist has 25 capital.'])
scope('Q22', sm['Q22']['asked_facts'], givens=['Starting capital is 44.', 'The corporation then loses 7 capital.'])
qm['Q31']['question'] = 'When may Chief Gorman be used on an ordinary hand-action counteroffer, what payment avoids its return, and what happens to the returned proposer’s status, that proposer’s further counteroffers and already-paid proposal discards?'
sm['Q31']['question'] = qm['Q31']['question']
sm['Q31']['scenario_givens'] = ['Ordinary hand-action counteroffer, not Fall Guy bypass or an emergency action.']
changes.append('Q31')
a = sm['Q33']['asked_facts'].copy(); a[1] = 'An eligible owner may normally support the main offer.'
scope('Q33', a, ['Normal eligibility to support the counteroffer is correct background; the question specifically asks the main offer.'])
scope('Q47', [
    'Coach pays when the owner’s right neighbor wins the deal.',
    'Monica’s owner may steal from the countering player when her owner loses a deal as the active player.',
    'Saul responds to the countering player’s victory: the user gains capital first, then the active player gains capital.'
], ['Coach’s payout is one, Monica’s theft is two, and Saul’s two gains are one each. These quantities are correct context rather than separately requested quantities. A volunteered false amount remains a material contradiction.'])
scope('Q57', [
    'Media Circus decreases strike two stages to stable, then places one Human First.',
    '24/7 Live Feeds may instead remove one orgcrime.'
], ['Media Circus places its Human First in any district. The unchosen 24/7 alternative decreases unrest by one stage. Neither extra detail is separately requested.'])
scope('Q60', [
    'Arrest Orders places one prisec in any district to remove all other units there, not tokens.',
    'Units are the plastic Human First, orgcrime and prisec components; androids are tokens.',
    'Scorched Earth places one outage in a district not already in outage to remove enemies there and in another district in the same tier.'
])
km['Q60']['expected_answer'] += ' Units are plastic Human First, orgcrime and prisec; androids are tokens.'
scope('Q74', [
    'Resolve Human First from the highest-numbered district first; apply two movement instructions per unit, subject to the Root returning it to the reserve.',
    'Ordinary duplicate/prisec blocking cascades apply; entering the Root returns the unit to the reserve and adds two threat.'
], ['Locations are not supplied: do not invent final districts, guarantee two successful on-board moves for a unit removed at the Root, or calculate an overall threat change.'])
km['Q74']['expected_answer'] = 'Highest-numbered district first. Each Human First receives two movement instructions, with normal duplicate/prisec blocking and cascades. Entry into the Root returns that unit to the reserve and adds two threat; do not continue moving a unit removed from the board.'
scope('Q87', [
    'The number of bars under the district name identifies its tier.',
    'Tier has no inherent production/threat effect; printed card instructions can refer to tier.'
], ['Matching district-border color is a supplementary identification aid, not an additional completeness prerequisite.'])
qm['Q91']['question'] = qm['Q91']['question'].replace('When an action is stolen', 'When an ordinary hand action is stolen')
sm['Q91']['question'] = qm['Q91']['question']; changes.append('Q91')
q['benchmark_version'] = k['benchmark_version'] = 'expanded-candidate-v6'
for name, obj in [('questions.json', q), ('answer-key.json', k), ('asked-clause-map.json', s)]:
    (V / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')
report = B / 'full-bank-scope-validator/scope-review.json'
version = {'from': 'candidate-v5', 'to': 'candidate-v6', 'question_count': 93,
           'source_outcomes_changed': False, 'new_questions': [],
           'changed_records': changes, 'wording_clarifications': ['Q31', 'Q91'],
           'scope_correction_source': str(report.resolve()),
           'scope_correction_source_sha256': hashlib.sha256(report.read_bytes()).hexdigest(),
           'corrections': json.loads(report.read_text())['issues_and_proposed_versioned_corrections'],
           'history_preserved': True, 'readers_not_yet_run': True,
           'historical_seed_pass_scope': 'Historical seed results do not establish the newly explicit Q09 production requirement; the full new bank will be tested by new readers.'}
(V / 'version-changes.json').write_text(json.dumps(version, indent=2, ensure_ascii=False) + '\n')
ledger = json.loads((V / 'coverage-ledger.json').read_text())
ledger['scope_version_corrections'] = {'version': 'v6', 'source': str(report.resolve()), 'outcome_or_novelty_changes': False, 'record_ids': changes}
ledger['stopping_rule']['NEW_scope_validator'] = 'v5 complete93 review accepted conditionally; v6 applies all13 findings; followup confirmation pending'
(V / 'coverage-ledger.json').write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + '\n')
parts = ['# New Angeles candidate bank v6', '93 entries. Versioned actual-clause corrections and two hand-action wording clarifications were applied before any expanded readers. SG01 remains pending.']
for x in q['questions']:
    i = x['id']; parts += ['## ' + i, x['question'], '**Required answer facts:**\n\n' + '\n'.join('- ' + f for f in sm[i]['asked_facts']), '**Sources:** ' + '; '.join(km[i]['source_refs'])]
(V / 'question-bank.md').write_text('\n\n'.join(parts) + '\n')
names = ['questions.json', 'answer-key.json', 'asked-clause-map.json', 'coverage-map.json', 'coverage-ledger.json', 'question-bank.md', 'version-changes.json']
(V / 'input-manifest.json').write_text(json.dumps({'status': 'candidate frozen for source/scope followup confirmation', 'question_count': 93, 'hashes': {n: hashlib.sha256((V/n).read_bytes()).hexdigest() for n in names}, 'frozen_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}, indent=2) + '\n')
p = B / 'progress.json'; progress = json.loads(p.read_text()); progress['candidate_bank_path'] = str(V.resolve()); progress['phase'] = 'candidate_v6_scope_corrections_followups_pending'; p.write_text(json.dumps(progress, indent=2) + '\n')
assert len(qm) == len(km) == len(sm) == 93
print('Created v6 with all13 scope findings addressed; prior candidates unchanged.')
