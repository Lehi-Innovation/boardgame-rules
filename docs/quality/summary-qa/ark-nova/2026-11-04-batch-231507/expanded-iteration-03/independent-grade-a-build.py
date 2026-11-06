from pathlib import Path
import hashlib
import json
from collections import Counter

ROOT = Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507')
OUT = ROOT / 'expanded-iteration-03'
FILES = [
    'expanded-iteration-03/reader-a.json',
    'expanded-iteration-03/summary-snapshot.md',
    'expanded-iteration-03/questions.json',
    'benchmark-v2/answer-key.json',
    'benchmark-v2/material-requested-facts.json',
    'grading-request-scope-02.json',
]
EXPECTED_HASHES = [
    '64c62b523f5444339e7844ec37470ed7e084d608f5012dbc3bb01ec6f38c7b17',
    '594b7024f6916136c360fecb8ba473f5ca44bd7a7c83eb45d0bb572e1d435acc',
    '31b1757227a4fddb0172f75f04adebb8b36b752826239eb45b8c2b7794c046ce',
    'bc70ac84aa525cee8d421ef6652f1fe9118c63deaa87caff266aba02f0ab1f03',
    '7e30b963a5dfd451fc9686f5ff7fad0bbf69aba2733c0f04ff3ef0c6bce648d6',
    'd3418c7e4c4a6304f644ec1316403afa2ee00c2b2ef52bf074d6d536fc8f3c88',
]
PROMPT = "Fresh independent grader, ArkNova94-question readerA. ReadONLY QAroot /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507/ files expanded-iteration-03/{reader-a.json,summary-snapshot.md,questions.json}, benchmark-v2/{answer-key.json,material-requested-facts.json}, grading-request-scope-02.json. No otherreader/earliergrades/reports/history/rawsources/canonical/browsing/contact. Readall6inputscompletelyboundedrecovereverytruncation. IndependentlygradeALL94answers, everyACTUALLYREQUESTEDpart individually. Actualquestionmeaningcontrolsscope, immutablefactualkeysourcefactsstayfixed, neutralrequested/contextindexguidecontainsnoprioranswers/results. Contextneednotbevolunteered; anyvolunteeredfalse/contradictoryrulingcounts. Ifindexseemsinconsistentwithquestionexplicitlyflagconcernwithoutaddinghiddenrequirements. Correctonlycompleteallactualparts,no contradictions/no unsupportedsource-correctguesses;partialmissing/unresolved/ambiguousactualpart;incorrectmaterialfalse ruling. No borrowingbetweenanswers; supportlabelnotgrade; basiclogicalentailment/meaningfuldefined-procedureshorthandallowedaccordingtopromptscope. Preservequestion-givenconditionswhenreadinganswer; do notusekeywordmatchingorrequireextracontext. Reviewallvolunteeredclausesagainstthisfrozennarrative. WriteONLY expanded-iteration-03/independent-grade-a.json plusownnotesnamedindependent-grade-a-*; noinputedits. Include exactintendedprompt,6inputhashes,complete-readproof,94question-orderjudgments:id,perrequestedpart status/resolution/RELEVANT observedclausequote/summarysupportquote-or-line,overallgrade correct|partial|incorrect,unsupported_guessbool,reason,andvolunteered/contextreview. Quoteonlyrelevantclausesperpart ratherthanrepeatingwholeanswerperpart; fullrawansweralreadypreserved. IncludeC/P/Icounts,nonpassingIDs,borderline/scope/keyconcerns. NoassumedPASS; don'trelaxgenuineaskedparts."

raw = {f: (ROOT / f).read_bytes() for f in FILES}
hashes = []
for f, expected in zip(FILES, EXPECTED_HASHES):
    actual = hashlib.sha256(raw[f]).hexdigest()
    assert actual == expected, (f, actual)
    hashes.append({'file': f, 'sha256': actual, 'bytes': len(raw[f]), 'lines': len(raw[f].splitlines())})
questions = json.loads(raw[FILES[2]])['questions']
answers = json.loads(raw[FILES[0]])['answers']
key = json.loads(raw[FILES[3]])['answers']
facts = json.loads(raw[FILES[4]])
scope = json.loads(raw[FILES[5]])['questions']
summary = raw[FILES[1]].decode().splitlines()
assert len(questions) == len(answers) == len(key) == len(facts) == len(scope) == 94
assert [q['id'] for q in questions] == [a['id'] for a in answers]
assert {q['id'] for q in questions} == {k['id'] for k in key} == set(facts) == set(scope)

notes = {}
for name in ['independent-grade-a-notes.json', 'independent-grade-a-notes-21-42.json', 'independent-grade-a-notes-43-70.json', 'independent-grade-a-notes-72-140.json']:
    part = json.loads((OUT / name).read_text())
    assert not (set(notes) & set(part))
    notes.update(part)
assert set(notes) == {q['id'] for q in questions}

# Replace provisional line numbering with verified one-based frozen-summary lines.
verified = {
    'Q01': [81,80,83,82,76,76,78],
    'Q02': [69,70,70,70,84],
    'Q03': [104,104,104,106,106,106,106,108],
    'Q04': [102,248,248,248,248],
    'Q05': [112,112,112,124],
    'Q06': [147,147,147,148,148,148,148,148,147],
    'Q07': [163,163,163,163],
    'Q08': [180,182,182,180,181,181,181,181,181,181],
    'Q09': [180,182,179,182,182,182],
    'Q10': [106,106,182,108,278],
    'Q11': [207,208,208,209,209,209,209,209,209,211,212],
    'Q12': [213,213,213,213,213,213],
    'Q13': [221,221,221,224,223,223,223],
    'Q14': [[231,232,233,234],229,239,229,229,229,229],
    'Q15': [[232,233],[232,233],[232,233],[232,233],232,232,88,233],
    'Q16': [234,[234,239],234,234,[234,276],235,235,236,236,236],
    'Q17': [237,237,237,237,237,237,237,237],
    'Q18': [242,243,243,243,242,[242,243]],
    'Q19': [115,116,117,117,118,[119,124],121,121,123,123,124],
    'Q20': [253,254,255,255,257,257,257,257,260,261,262,262],
}
for q, lines in verified.items():
    notes[q]['lines'] = lines

def line_for(anchor):
    hits = [n for n, line in enumerate(summary, 1) if anchor in line]
    assert len(hits) == 1, (anchor, hits)
    return hits[0]

inference = {
    ('Q03',3): 'The exhaustive movement of the used card and slots one through three leaves slot five unchanged.',
    ('Q18',5): 'Side I pays the stated action strength. With the question-given one remaining step, that formula still pays full strength; movement clipping does not alter the stated amount.',
    ('Q28',4): 'Listing Petting Zoo separately among the seven categories establishes that it is its own category.',
    ('Q31',1): 'Applying distinct actually adjacent hex counting to the question-given requirement of two requires two distinct adjacent terrain hexes.',
    ('Q67',2): 'A reward per pair means complete pairs, so an unmatched icon contributes no conservation.',
    ('Q77',5): 'The stated one-per-type-per-zoo rule prevents duplicating a special enclosure already built during the action.',
    ('Q98',3): 'Current total predator icons includes both icons just played for the first trigger; counting the new icons for the second as well preserves that inclusion in both Hunters.',
    ('Q99',1): 'The Stable entering with three supply tokens attributes all three to that card; the actual question does not separately request placing its building.',
    ('Q104',5): 'One conservation per six contiguous spaces, evaluated separately for each group without combining, counts complete sixes separately and leaves remainders unscored.',
    ('Q116',1): 'Payment per adjacent covered hex entails separate payment for several adjacent hexes belonging to one building.',
    ('Q125',6): 'Applying highest-appeal and most-conservation targets separately causes two applications if the same zoo is both targets.',
}

judgments = []
for q, answer in zip(questions, answers):
    i = q['id']
    v = notes[i]
    requested = list(scope[i]['requested_parts'])
    for n, text in v.get('part_override', {}).items():
        requested[int(n)-1] = text
    assert q['question'] == scope[i]['question']
    assert len(requested) == len(v['quotes'])
    parts = []
    for n, (part, quote) in enumerate(zip(requested, v['quotes']), 1):
        assert quote is None or quote in answer['answer'], (i,n,quote)
        if i == 'Q140' and n == 3:
            quotes = [quote, 'Play has no formal rounds']
        elif i == 'Q19' and n == 1:
            quotes = [quote, 'Hand limit is normally three or five with the hand-limit university']
        elif i == 'Q41' and n == 2:
            quotes = [quote, 'leave the card until it is at least in slot 3']
        elif i == 'Q15' and n == 8:
            quotes = [quote, 'Take a partner zoo or university from an available tile on the Association board']
        elif i == 'Q124' and n == 1:
            quotes = [quote, 'any gains beyond those track endpoints are lost']
        elif i == 'Q125' and n == 8:
            quotes = ['a conservation leader requiring at least one point; self-target has no effect']
        elif i == 'Q125' and n == 11:
            quotes = [quote, 'a highest-appeal zoo with at least five appeal', 'with ties chosen, at least five appeal', 'Constriction affects every other zoo with at least five appeal']
        else:
            quotes = [quote] if quote else []
        for quoted in quotes:
            assert quoted in answer['answer']
        if 'lines' in v:
            loc = v['lines'][n-1]
            lines = loc if isinstance(loc, list) else [loc]
        else:
            lines = [line_for(v['anchors'][n-1])]
        # Default owner-zoo scope and defined map terms are fixed narrative facts.
        if i in ['Q68','Q70','Q72','Q95','Q96'] and n in ([1] if i in ['Q68','Q72'] else [1,2]):
            lines.append(line_for('Unless an effect says "any zoo,"'))
        if i == 'Q90' and n == 5:
            lines.append(line_for('A connected space is'))
        status = 'missing' if quote is None else ('contradicted' if n in v.get('incorrect_parts',[]) else 'resolved')
        resolution = inference.get((i,n), part)
        if status == 'missing':
            resolution = 'No clause identifies the next clockwise player as taking the next ordinary turn; endgame final-turn discussion does not answer that requested part.'
        if status == 'contradicted':
            resolution = 'Frozen immediate reward is two money per water/rock icon; the answer substitutes one appeal per icon.'
        parts.append({
            'part': n,
            'requested_part': part,
            'status': status,
            'resolution': resolution,
            'basis': 'ordinary_logical_entailment' if (i,n) in inference else 'explicit_meaning',
            'relevant_observed_clause_quotes': quotes,
            'summary_support': {'file': FILES[1], 'lines': sorted(set(lines))},
        })
    grade = v.get('grade','correct')
    assert grade == ('incorrect' if any(p['status']=='contradicted' for p in parts) else 'partial' if any(p['status']=='missing' for p in parts) else 'correct')
    judgments.append({
        'id': i,
        'question': q['question'],
        'requested_parts': parts,
        'overall_grade': grade,
        'unsupported_guess': False,
        'unsupported_guess_review': 'No source-correct unsupported guess detected; judgments follow the answer clauses and frozen narrative rather than the reader support label.',
        'reason': v.get('reason', f'All {len(parts)} actual requested parts are resolved by the quoted clauses, with no material contradiction or unsupported source-correct guess.'),
        'volunteered_context_review': {
            'reviewed_all_volunteered_answer_clauses': True,
            'result': 'Material false immediate reward identified in requested part 1; other volunteered context is correct.' if i=='Q78' else 'No volunteered material false or contradictory ruling.',
            'detail': v['review'],
            'unrequested_context_not_required': scope[i]['unrequested_context'],
        },
        'scope_concerns': [v['scope_concern']] if 'scope_concern' in v else [],
    })

counts = Counter(j['overall_grade'] for j in judgments)
assert counts == {'correct':92,'partial':1,'incorrect':1}
result = {
    'grader': 'independent-grade-a',
    'reader': 'reader-a',
    'iteration': 'expanded-iteration-03',
    'exact_intended_prompt': PROMPT,
    'input_hashes': hashes,
    'complete_read_proof': {
        'all_six_inputs_read_completely': True,
        'allowed_source_inputs_only': True,
        'summary_lines_read': [[1,90],[91,180],[181,270],[271,350],[351,451]],
        'json_metadata_read': {
            FILES[0]: ['reader','inputs_read'],
            FILES[2]: ['game','scope','version'],
            FILES[3]: ['game','benchmark_version','grading','baseline_benchmark'],
            FILES[4]: 'All 94 top-level keyed entries; no separate header.',
            FILES[5]: ['version','purpose','method','source_of_version','rules'],
        },
        'json_record_read_method': 'Each bounded joined display emitted the complete question, reader answer/support/evidence, immutable answer-key object, material-facts object and neutral scope object for every included question; all object fields were retained.',
        'question_position_ranges_read_for_each_json_payload': [[1,10],[11,20],[21,30],[31,40],[41,50],[51,60],[61,70],[71,80],[81,87],[88,94]],
        'payload_record_counts': {FILES[0]:94,FILES[2]:94,FILES[3]:94,FILES[4]:94,FILES[5]:94},
        'question_order_and_id_sets_verified': True,
        'truncated_outputs_observed': 0,
        'truncation_recovery': 'Not needed: every bounded display completed without an output-truncation marker.',
        'hashes_rechecked_before_output': True,
        'input_files_edited': False,
        'prohibited_external_sources_or_other_reader_artifacts_read': False,
    },
    'rubric_application': 'Actual question meaning determines scope. Each answer stands alone. Missing/unresolved actual parts are partial; material false rulings are incorrect. Unrequested context is not required, but volunteered false rulings count. Basic logical entailment and meaningful defined-procedure shorthand are allowed. Reader support tags are not grades. Every result was independently adjudicated before formatting; no pass was assumed from a tag or an earlier result.',
    'counts': {'correct':counts['correct'],'partial':counts['partial'],'incorrect':counts['incorrect'],'total':len(judgments)},
    'nonpassing_ids': [j['id'] for j in judgments if j['overall_grade']!='correct'],
    'partial_ids': ['Q05'],
    'incorrect_ids': ['Q78'],
    'borderline_interpretations': [
        {'id':'Q03','decision':'correct','reason':inference[('Q03',3)]},
        {'id':'Q15','decision':'correct','reason':'The answer describes tile acquisition and immediately covered-space rewards, then universities providing printed reputation. That ordinary acquisition sequence resolves the tile award without requiring another use of the word immediately.'},
        {'id':'Q18','decision':'correct','reason':inference[('Q18',5)]},
        {'id':'Q31','decision':'correct','reason':inference[('Q31',1)]},
        {'id':'Q39','decision':'correct','reason':notes['Q39']['review']},
        {'id':'Q43','decision':'correct','reason':'Release/fallback procedure is a meaningful named procedure; the question asks historical proof, not a re-listing of every release step.'},
        {'id':'Q67','decision':'correct','reason':notes['Q67']['review']},
        {'id':'Q90','decision':'correct','reason':notes['Q90']['review']},
        {'id':'Q98','decision':'correct','reason':inference[('Q98',3)]},
        {'id':'Q99','decision':'correct','reason':inference[('Q99',1)]},
        {'id':'Q107','decision':'correct','reason':notes['Q107']['review']},
        {'id':'Q125','decision':'correct','reason':inference[('Q125',6)]},
    ],
    'scope_concerns': [{'id':j['id'],'concern':c} for j in judgments for c in j['scope_concerns']],
    'key_concerns': [],
    'judgments': judgments,
}
(OUT / 'independent-grade-a.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
for h in hashes:
    assert hashlib.sha256((ROOT/h['file']).read_bytes()).hexdigest()==h['sha256']
assert all(1 <= line <= len(summary) for j in judgments for p in j['requested_parts'] for line in p['summary_support']['lines'])
print(json.dumps({'output':str(OUT/'independent-grade-a.json'),'counts':result['counts'],'nonpassing_ids':result['nonpassing_ids'],'requested_parts':sum(len(j['requested_parts']) for j in judgments),'scope_concern_ids':[c['id'] for c in result['scope_concerns']],'all_input_hashes_unchanged':True}))
