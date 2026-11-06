from pathlib import Path
import json,hashlib
base=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v13-complete-requested-scope/luna-iteration-01/grading-reader-a/block-02')
p=json.loads((base/'packet.json').read_text())
# Explicit human semantic choices: ledger index for each ordered required atom.
choices={
'Q021':[1,1,1,1,0,0,0,1,1,'public',2,2],
'Q022':[0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,'facedown'],
'Q023':[0,0,0,1,1,2,3],
'Q024':[0,0,0,1,1,1,1,1,1,1,2,3,3,3,3],
'Q025':[0,0,0,1,1,2,2],
'Q026':[0,0,0,0,0,0,0,0,1,1,1,2,3,3],
'Q027':[0,0,0,1,1,1],
'Q028':[0,0,0,'discount',1,1,2,2],
'Q029':[0,1],
'Q030':[0,0,0,0,1,1,1,2,2,2,2,2,4,'applicant','prices',2,2,2,2,3],
'Q031':[0,0,1,1],
'Q032':[0,1,1,1,1],
'Q033':[0,1,1,1,'china',1,1,1,1,1,1],
'Q034':[0,0,0,1,2],
'Q035':[0,0,0,1,1,1,1,1,1,2],
'Q036':[0,1,1,1,2,2,3,3,3],
'Q037':[0,1,1],
'Q038':[0,0,0,0,0,'refresh',1,0,1,1,1],
'Q039':[0,1,2],
'Q040':[0,1,1,2,2,2,2]
}
extra={
'public':'All information, including discards and family cash, is public except facedown blackmail and temporarily concealed firm strategies/bids during selection.',
'facedown':'It must stay facedown when traded.',
'discount':'Discounts reduce actual spending and therefore display priority.',
'applicant':'Place a member on an empty Stock Exchange space and pay bank: the five queue spaces are £2, £3, £3, £4, £5 (two distinct £3 spaces). It is an applicant, not yet a share.',
'prices':'the five queue spaces are £2, £3, £3, £4, £5 (two distinct £3 spaces)',
'china':'Chairman chooses any writer; office hired immediately upon creation.',
'refresh':'Refresh exhausts any unused active alliances too; it does not reactivate alliances as it does officers/regiments.'
}
reasons={
'Q021':'All unlimited supplies and tracks, limited-supply fallback and public/hidden-information exceptions are covered.',
'Q022':'Every trade category and the share replacement and blackmail restrictions are covered.',
'Q023':'Binding transfers, future promises, calling limits and both exceptional cases are covered.',
'Q024':'The holdings ledger materially contradicts the correct source passage: it sends matching office cards to offices instead of giving them to their owners. All other requested setup facts are covered. This is reader error; the summary explicitly supplies the correct destination.',
'Q025':'The failure space is identified by Standing reaching failure; scenario ending, ordinary immediate scoring, both phase exceptions and the final-scoring prohibitions are covered.',
'Q026':'The inclusive enterprise category covers applicable prestige enterprises. All Power sources, awards and tie branches are covered.',
'Q027':'All requested survival and failure scoring and retirement branches are covered.',
'Q028':'Spouse restrictions and immediate trades, personal stacking discounts that reduce spending, and both usage windows are covered. The discount refers contextually to its card-defined retirement reduction.',
'Q029':'Both causes retain the fitted ship and prevent repurchase until its return.',
'Q030':'The complete menu supplies costs, placements, types, votes, income and failure scoring. No listed cash cost for either enlistment communicates free enlistment.',
'Q031':'Both required shortage consequences and the no-action marker fallback are covered.',
'Q032':'Automatic return, supply and prize fallbacks with VP loss, and the impossible-placement result are covered.',
'Q033':'All hiring actors, candidate pools, fallback order and Commander exclusion are covered.',
'Q034':'Both successful outcomes, immediate China hiring, repetition and transfer timing are covered.',
'Q035':'The sequence, strict replacement threshold, greatest-family selection, officer movement, incumbent tie and Nepotism exception are covered.',
'Q036':'All scheduling authority, opportunity, decline, interruption and vacant-President limits are covered.',
'Q037':'Ship exhaustion and both requested refresh destinations are covered.',
'Q038':'All purchase, funding, activation, exhaustion, once-only and indivisibility requirements are covered, including unused alliances at Refresh.',
'Q039':'The own-Company-region zero defense, surviving-officer-plus-Commander minimum and zero tower trophies are covered.',
'Q040':'Both build stages and destinations and every requested regiment property are covered.'
}
grades=[]
for entry in p['entries']:
 qid=entry['id']; reader=entry['reader_a_entry']; facts=entry['requested_fact_scope_entry']['material_requested_facts']; selected=choices[qid]
 assert len(facts)==len(selected),(qid,len(facts),len(selected))
 pool=[reader['answer']]+[x['supported_fact_or_case_result'] for x in reader['clause_ledger']]+[x['quote'] for x in reader.get('evidence',[])]
 parts=[]
 for index,(fact,choice) in enumerate(zip(facts,selected)):
  quote=reader['clause_ledger'][choice]['supported_fact_or_case_result'] if isinstance(choice,int) else extra[choice]
  assert any(quote in s for s in pool),(qid,index,quote)
  status='contradicted' if qid=='Q024' and index==4 else 'covered'
  quotes=[quote]
  if status=='contradicted':
   quotes.append("put each office's family member in its office and give its matching office card to that owner")
   assert quotes[-1] in reader['answer']
  parts.append({'requirement':fact,'status':status,'reader_quotes':quotes})
 issue=None
 if qid=='Q024':
  issue={'summary_location':'summary-snapshot.md:41 (Setup step 3)', 'summary_quote':"put each office's family member in its office and give its matching office card to that owner", 'cause':'reader error', 'explanation':"The ledger says 'members and matching office cards to offices'. The matching office card must instead go to the officeholder's owner. The same entry copies the correct summary passage, but that does not erase its contradictory concrete destination."}
 grades.append({'id':qid,'grade':'Incorrect' if qid=='Q024' else 'Correct','reason':reasons[qid],'material_parts':parts,'unsupported_guesses':[],'summary_issue_if_any':issue})
assert len(grades)==20
out={'block_id':'block-02','readers':{'reader-a':{'grades':grades}}}
data=json.dumps(out,ensure_ascii=False,indent=2)+'\n'
target=base/'grades-same-entry.json'
target.write_text(data)
print(json.dumps({'path':str(target),'grades':len(grades),'atoms':sum(len(g['material_parts']) for g in grades),'sha256':hashlib.sha256(data.encode()).hexdigest()}))