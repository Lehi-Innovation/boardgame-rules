from pathlib import Path
import json,hashlib,shutil,datetime
R=Path(__file__).resolve().parent
ROOT=R.parents[4]
def save(p,x):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
rows=[
('How does standard setup distribute equipment, prepare the deck, and place each player’s starting cards? Include card count, placement method and secrecy.', ['Give each player a Clover board and marker.','Shuffle Keyword cards into a face-down deck within everyone’s reach.','Each draws four cards and places them randomly in recessed board spots, hidden from others.'],1,'33–43'),
('Name the two phases in order. During Choosing Clues, who acts when, and which Keywords make the four Pairs?', ['Choosing Clues (individual), then Resolution (team).','All players work simultaneously and secretly.','Use the eight Keywords on the outside card edges: two below each Clue Zone, making four Pairs.'],2,'60–76'),
('What forms can a Clue take? State the word limit, treatment of compound words, and all five permitted categories.', ['A single word; compound words are allowed.','Common noun, proper noun, acronym, number or onomatopoeia.'],2,'72–75'),
('For a Pair containing Love and France, may Love itself be the Clue? Why?', ['No. Neither Keyword itself is a valid Clue.'],3,'91–93'),
('May Amour connect Love and France? Explain the applicable restriction.', ['No. A translation of a Keyword into another language is invalid.'],3,'91–93'),
('May Prince connect Princess and Brother? Explain the applicable restriction.', ['No. A word in the same family as a Keyword is invalid.'],3,'94–95'),
('May a player invent Cuppajo to connect Mug and Morning? Why?', ['No. Made-up words are invalid Clues.'],3,'96–97'),
('How many Clues must each player write, what must each connect, and where is each written?', ['Four Clues, one connecting the two Keywords in each Pair.','Write each secretly on its corresponding Clue Zone.'],2,'65–76'),
('After writing all four Clues, what exact card and board preparation does a player perform before Resolution? Include whether the added card may be inspected.', ['Remove all four Keyword cards from the board.','Draw one new card without looking at it and shuffle it with the original four.','Put the Clover board in front of you and the five cards on top in a face-down pile.'],4,'110–113'),
('One player has prepared their five-card pile while others are still writing. When does Resolution start?', ['Only once everyone has finished writing and preparing their board and five-card pile.'],4,'110–114'),
('How is the first Spectator selected, what do the other players do, and may the Spectator provide spoken hints or gestures during Resolution?', ['Choose the first Spectator.','All other players examine that player’s board and work together to reconstruct its Pairs.','The Spectator cannot communicate in any way, including spoken hints or gestures.'],4,'115–121'),
('What does the Spectator reveal and where? What arrangement are the other players trying to reconstruct from these materials?', ['Place their Clover board and all five Keyword cards face up in the middle of the table.','Use the Clues to reconstruct the original Pairs by returning the four original cards to their correct board spaces (and orientations), leaving the extra card off.'],4,'119–121; p.2 Pair diagram and p.5 verification diagram'),
('The team disagrees about card placement. Who makes the final decision?', ['The player seated to the Spectator’s left.'],4,'122–123'),
('May the guessers physically try card layouts and discuss their reasoning before submitting? At what point does the Spectator verify?', ['Yes, they may place cards on the board to visualize combinations and explain their reasoning.','The Spectator verifies once the players agree on placement.'],4,'124–128'),
('All Pairs are correct on the first attempt. How many points are gained, how are they calculated, and is a second attempt needed?', ['Six points: one per correct card (four) plus two bonus points for first-try perfection.','No second attempt is needed.'],5,'157–166'),
('At least one Pair is wrong on the first attempt. What does the Spectator do with incorrect cards, what feedback may they give, and how many further attempts does the team receive?', ['Silently remove the incorrect card(s) and put them in the middle of the table.','Do not communicate beyond this prescribed removal.','The others get one second and final attempt.'],5,'162–166; p.4 116–118'),
('The first attempt contains an error, but all four cards are correct on the second attempt. What is the score, and is the first-try bonus awarded?', ['Four points, one per correct card on the second attempt.','No two-point first-try bonus.'],5,'158–170'),
('After the second attempt, three cards are correct and one is wrong. What happens to the wrong card, what is the score, and may the team try again?', ['The Spectator removes the wrong card and puts it in the middle of the table.','Score three points, one per correct card.','No third attempt; the second is final.'],5,'166–170'),
('After a board is resolved, how are its points recorded, what happens to all five cards, and who becomes the next Spectator?', ['The Spectator turns over their Clover board and writes the points in its middle.','Discard all five used Keyword cards.','The player to their left becomes the next Spectator and a new Resolution begins.'],5,'171–174'),
('When does the game end, how often does each player act as Spectator, and how is the team’s result recorded and used?', ['End after every player has been Spectator once.','Add everyone’s points and write the team total in the Record of Legends.','Try to beat the team’s high score.'],6,'179–183')]
scope='English Repos base game, 2021 publication; sc-en01 rulebook copyright 2020. Standard setup, Choosing Clues, Resolution, scoring and endgame. Optional Add a Challenge excluded.'
q={'game':'So Clover!','bgg_id':329839,'scope':scope,'benchmark_version':'v1-seed-20','questions':[]}
k={z:q[z] for z in ['game','bgg_id','scope','benchmark_version']};k['answers']=[]
for i,(question,facts,page,lines) in enumerate(rows,1):
 id=f'Q{i:02}'
 q['questions'].append({'id':id,'question':question})
 k['answers'].append({'id':id,'expected_answer':' '.join(facts),'required_facts':facts,'source_references':[{'path':str(ROOT/'extracted/so-clover-rules.txt'),'pdf_page':page,'extraction_lines':lines}]})
for name,obj in [('questions.json',q),('answer-key.json',k)]:save(R/'benchmark-v1'/name,obj)
save(R/'benchmark-v1/input-manifest.json',{'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_first':True,'summary_existed_at_bank_creation':False,'inputs':{str(p):sha(p) for p in [R/'benchmark-v1/questions.json',R/'benchmark-v1/answer-key.json',ROOT/'extracted/so-clover-rules.txt',ROOT/'source_pdfs/so-clover-rules.pdf']}})
shutil.copyfile(ROOT/'extracted/so-clover-rules.txt',R/'baseline/so-clover-rules.txt')
save(R/'progress.json',{'game':'So Clover!','slug':'so-clover','status':'in-progress','phase':'seed-bank-frozen','question_count':20,'iterations':[],'final_reader_scores':None,'coverage_review':'pending','coverage_stopping_rule':'pending','source_audit':'pending','source_paths':[str(ROOT/'extracted/so-clover-rules.txt'),str(ROOT/'source_pdfs/so-clover-rules.pdf')],'final_snapshot_path':None,'report_path':str(R/'README.md'),'blocking_reason':None,'hashes':{str(p):sha(p) for p in [R/'benchmark-v1/questions.json',R/'benchmark-v1/answer-key.json',ROOT/'extracted/so-clover-rules.txt',ROOT/'source_pdfs/so-clover-rules.pdf']}})
