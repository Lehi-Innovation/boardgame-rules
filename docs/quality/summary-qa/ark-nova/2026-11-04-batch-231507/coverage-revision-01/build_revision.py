import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
QA=HERE.parent
DRAFT=QA/'coverage-draft'
BASE=QA/'benchmark-v1.1'
def read(path): return json.loads(path.read_text())
def write(name,data): (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def filehash(path): return hashlib.sha256(path.read_bytes()).hexdigest()

oldq=read(DRAFT/'questions.json')
olda=read(DRAFT/'answer-key.json')
oldfacts=read(DRAFT/'material-requested-facts.json')
oldmap=read(DRAFT/'coverage-map.json')
oldledger=read(DRAFT/'novelty-rejection-ledger.json')
challenge=read(QA/'coverage-challenge/report.json')
bq=read(BASE/'questions.json')
ba=read(BASE/'answer-key.json')
sc01=read(QA/'source-key-correction-SC01.json')
reject={r['question_id']:r for r in challenge['novelty_rejections']}
assert set(reject)=={'Q48','Q109','Q110','Q126'}
assert bq['questions']==oldq['questions'][:20]
assert [x['id'] for x,y in zip(olda['answers'][:20],ba['answers']) if x!=y]==['Q17']

new=[]
def add(qid,question,facts,refs,origin,novelty):
    new.append({'id':qid,'question':question,'expected_answer':' '.join(facts),
                'material_requested_facts':facts,'source_references':refs,
                'origin':origin,'distinct_novelty':novelty})

add('Q133','What are the two actual options of the Crested Porcupine Digging 2 ability illustrated in the rules, and how many selections does it provide?',[
    'Make 2 selections.',
    'One option is to discard 1 card from the display and replenish the display.',
    'The other option is to discard 1 card from your hand and draw 1 card from the deck.'
], 'Main p13 Crested Porcupine illustrated Digging 2 text; Glossary p2 Digging (choice-by-choice timing remains Q42)',
    'Independent challenge F04; original Q42 preserved by parent instruction',
    'Q42 asks whether choices can differ and refill timing, but never asks what the choices are; this adds the actual card sources/destinations, not another choice-timing example.')
add('Q134','When replenishing the display, how do remaining cards fill gaps, must their order be preserved, and how are the final empty folders filled?',[
    'Move remaining cards from higher-numbered folders down into the lower gaps.',
    'Preserve the relative order of those cards.',
    'Then fill each remaining empty folder with a card from the deck.'
], 'Main p9 The Reputation Track and the Display, paragraph beginning If you have taken one or more cards from the display',
    'Independent challenge F07 and proposed Q06 amendment; Q06 preserved by parent instruction',
    'Q06 tests refill timing, while Q42 mentions normal shift/refill but never requests preservation of relative order and final deck fill; this adds the explicit ordered compaction procedure.')
add('Q135','For the Species Diversity base conservation project illustrated in the rules, what is counted, do repeated icons of one animal category increase that count, and which category counts give which conservation rewards?',[
    'Count different animal-category icons in your zoo, rather than all copies of those icons; repeated copies of one category do not add another different category.',
    'Bear and Petting Zoo animal are animal categories; continent and research icons are not.',
    'The illustrated tiers are 5, 4 or 3 different animal categories for 5, 3 or 2 conservation points respectively; choose a fulfilled unoccupied tier under the normal support rules.'
], 'Main p2 Species Diversity base-project illustration; Main p7 Species Diversity illustration; Main p13 animal categories; Main p15 normal support conditions',
    'Independent challenge ADD01/F01',
    'A distinct-category project is a different counting rule from ordinary total-icon projects. One question covers the complete tier table, without numerical scenario variants.')

income=[('0',5),('1',6),('2',7),('3',8),('4',9),('5',10),('6–7',11),('8–9',12),('10–11',13),('12–14',14),('15–17',15),('18–20',16),('21–23',17),('24–26',18),('27–29',19),('30–33',20),('34–37',21),('38–41',22),('42–45',23),('46–49',24),('50–54',25),('55–59',26),('60–64',27),('65–69',28),('70–74',29),('75–79',30),('80–84',31),('85–89',32),('90–94',33),('95–99',34),('100–104',35),('105–109',36),('110–113',37)]
add('Q136','State the printed appeal-income table as ranges of appeal and the money each range earns during break income.',[
    'Appeal '+span+' gives '+str(money)+' money.' for span,money in income
]+['This is the appeal portion of income; kiosk and activated card/map income are additional.'],
    'Main pp4–5 setup-board appeal/income diagrams; Main p18 income step 5a',
    'Independent challenge ADD02/F02',
    'Q19 requests income order and kiosk eligibility, but no prior question requests the appeal-to-money payoff table. One question covers the whole table.')
add('Q137','Which side faces up when a standard enclosure is built, and when and how often do you gain the placement bonuses of the spaces it covers?',[
    'Place the newly built standard enclosure with its empty side up, identified by its yellow edge and enclosure-size number.',
    'Gain the corresponding placement bonus immediately when its space is covered, once only; if several bonus spaces are covered, gain each corresponding bonus.',
    'When building multiple buildings, resolve the first building placement bonuses before placing the next building.'
], 'Main p10 Build I empty-side and placement-bonus paragraphs; Main p6 Your Zoo Map placement-bonus paragraph; Main p10 Build II sequential building paragraph',
    'Independent challenge ADD03/F03',
    'The general newly built enclosure state and once-only placement-bonus activation were not requested earlier. Sequential funding is existing context, not credited as new novelty.')

primary_ref_fixes={
 'Q131':'Main pp2,4,9 original English reputation-track diagrams; Main p5 personal counter setup; official original English base Icon Overview p1 reputation/worker/upgrade/conservation/X/card-choice glyphs; publisher original base component photograph Spielzene.jpg central reputation track corroborates tiny component numerals only; no German rules prose adopted',
 'Q132':'Main p6 original English Map A left-edge support-bonus diagram; official original English base Icon Overview p1 snap/free-enclosure/reputation/money/conservation/X glyphs and p2 yellow immediate versus purple immediate-plus-income timing'
}

def build(source_gaps_only=False):
    selected=[r for r in new if not source_gaps_only or r['id'] in {'Q135','Q136','Q137'}]
    questions=copy.deepcopy(oldq)
    questions['benchmark_version']='coverage-revision-01-source-corrected'
    questions['baseline_benchmark']='benchmark-v1.1 / SC01'
    questions['questions']=copy.deepcopy(bq['questions'])+[
        copy.deepcopy(r) for r in oldq['questions'][20:] if r['id'] not in reject]+[
        {'id':r['id'],'question':r['question']} for r in selected]
    answers=copy.deepcopy(olda)
    answers['benchmark_version']=questions['benchmark_version']
    answers['baseline_benchmark']=questions['baseline_benchmark']
    answers['answers']=copy.deepcopy(ba['answers'])+[
        copy.deepcopy(r) for r in olda['answers'][20:] if r['id'] not in reject]+[
        {k:r[k] for k in ['id','expected_answer','source_references','material_requested_facts']} for r in selected]
    questions['questions'].sort(key=lambda x:int(x['id'][1:]))
    answers['answers'].sort(key=lambda x:int(x['id'][1:]))
    for a in answers['answers']:
        if a['id'] in primary_ref_fixes: a['source_references']=primary_ref_fixes[a['id']]
    write('questions.json',questions);write('answer-key.json',answers)
    write('new-questions.json',selected)
    write('SC01-source-key-correction.json',sc01)
    historical=[]
    for qid,r in reject.items():
        historical.append({'id':qid,'status':'rejected_as_novel_candidate_not_active','rejection':r,
            'historical_question':next(r for r in oldq['questions'] if r['id']==qid),
            'historical_answer':next(r for r in olda['answers'] if r['id']==qid),
            'historical_material_facts':oldfacts[qid]})
    write('rejected-candidate-entries.json',historical)
    assert questions['questions'][:20]==bq['questions']
    assert answers['answers'][:20]==ba['answers']
    assert [x['id'] for x in questions['questions']]==[x['id'] for x in answers['answers']]
    for qid in ['Q06','Q42']:
        assert next(x for x in questions['questions'] if x['id']==qid)==next(x for x in oldq['questions'] if x['id']==qid)
        assert next(x for x in answers['answers'] if x['id']==qid)==next(x for x in olda['answers'] if x['id']==qid)
    print(f'{len(questions["questions"])} active questions; selected additions '+', '.join(r['id'] for r in selected)+'; corrected baseline and Q06/Q42 exact')
    return questions,answers

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-gaps-only',action='store_true')
    args=parser.parse_args()
    build(args.source_gaps_only)
