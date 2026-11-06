from pathlib import Path
import json,hashlib,collections
p=Path(__file__).parents[1];o=p/'expanded-iteration-02'
paths=['expanded-iteration-02/reader-a.json','expanded-iteration-02/reader-b.json','expanded-iteration-02/summary-snapshot.md','expanded-iteration-02/questions.json','expanded-iteration-02/independent-grade-a.json','expanded-iteration-02/independent-grade-b.json','benchmark-v2/answer-key.json','benchmark-v2/material-requested-facts.json','grading-request-scope-01.json']
expected=['22bba04ec731b5d911443769c6c48aacb0b005354918a2a0e2005983381bfa54','3a4f176ca7c117b2e166754a827c5e82a7d2d8580e098d9f8a2fdf170c142386','27e24bc5fed7016f3616c44a126eed947f789ea05364622d738677350e4c9f0a','31b1757227a4fddb0172f75f04adebb8b36b752826239eb45b8c2b7794c046ce','6f82948b4ca56ed5925dfc5bef162b6edee82d7d84e22b92bc0bc7a3ebe7d8e0','9515b22f191cc7005c030eeae78ed985e39d1cec8decc5180b62668734e82f04','bc70ac84aa525cee8d421ef6652f1fe9118c63deaa87caff266aba02f0ab1f03','7e30b963a5dfd451fc9686f5ff7fad0bbf69aba2733c0f04ff3ef0c6bce648d6','2a4721e3e736b476541d169f326ac4971dd6092935a7b66ab128f979f5a3a61d']
hashes=[];D={}
for f,h in zip(paths,expected):
 b=(p/f).read_bytes();actual=hashlib.sha256(b).hexdigest();assert actual==h,(f,actual)
 hashes.append({'path':str(p/f),'sha256':actual,'bytes':len(b),'lines':len(b.decode().splitlines())})
 if f.endswith('.json'):D[f]=json.loads(b)
lines=(o/'summary-snapshot.md').read_text().splitlines()
Q=D['expanded-iteration-02/questions.json']['questions'];S=D['grading-request-scope-01.json']['questions']
R={s:{x['id']:x for x in D[f'expanded-iteration-02/reader-{s}.json']['answers']} for s in ['a','b']}
G={s:{x['id']:x for x in D[f'expanded-iteration-02/independent-grade-{s}.json']['judgments']} for s in ['a','b']}
manifest={}
for row in (o/'fresh-semantic-decisions.txt').read_text().splitlines():
 ident,sl,reason=[x.strip() for x in row.split('|',2)];id,g,va,vb=ident.split();assert id not in manifest
 manifest[id]={'grades':g,'a':va,'b':vb,'lines':[int(x) for x in sl.split(',')],'reason':reason}
assert list(manifest)==[q['id'] for q in Q]
code={'c':'correct','p':'partial','i':'incorrect'};status={'C':'complete','M':'missing','D':'contradicted','X':'unrequestedcontext'}
corrections={
 'Q03':{'change':'Separate the required X-token strength effect from unrequested spent-token destination.','why':'What can X-tokens do asks their strength function and the question separately asks holding limit/timing. It never asks where a spent token goes. Destination remains source-correct context, with no factual-key change.','scope_index_parts_affected':[4]},
 'Q16':{'change':'Treat the exact above-board project maximum as context to the overflow-handling question.','why':'What happens to overflowing projects/tokens requests discard and token destination, not a separate enumeration of the cap. Independently, both answers identify it as the player-count limit, a meaningful count-equals-players shorthand rather than an unspecified dependent table.','scope_index_parts_affected':[3]},
 'Q19':{'change':'Require the six break steps in order and the explicitly named detailed subquestions; move restock quantities/exclusions and income-type composition order to context.','why':'The literal prompt asks break steps in order, hand limit, kiosk qualifying neighbors, and income order/refill when several players take display cards. The latter is the affected-player ordering, not an added appeal/kiosk/Sponsor suborder demand. Restock is the named Association-board step; its exact per-kind quantities and all-owned exception are not separately requested. Both answers give the six steps and all named details. This is a scope correction, not a claim that restocking rules are optional or different.','scope_index_parts_affected':[3,5]},
 'Q33':{'change':'Treat the X-condition/Y-reward interpretation as requested, rather than context.','why':'How to read an X:Y effect requires what each side means as well as its multiplicity/threshold interpretation. Both answers provide this directly.','scope_index_parts_affected':[]},
 'Q100':{'change':'Treat simultaneous reward-order freedom as unrequested context.','why':'The question asks immediate track rewards, placement restriction and card choices; it does not separately ask simultaneous-effect sequencing. Both answers volunteer the source-correct order choice.','scope_index_parts_affected':[3]},
 'Q14':{'change':'Explicitly record the baseline active-worker requirement in addition to repeating-task escalation.','why':'Worker requirements are part of the request. Both answers give active workers and the normal singular worker requirement; the neutral index individually lists only escalation cases.','scope_index_parts_affected':[]},
 'Q37':{'change':'Do not require an intermediate into-hand destination in a source/later-play-location question.','why':'Where do they get cards asks the unused base-deck source; where later played asks above versus below the Association board. Into hand is true additional context.','scope_index_parts_affected':[0]},
 'Q95':{'change':'Require the Hut unique-building placement but do not demand a fresh statement of general normal placement rules.','why':'The literal request is what unique building and card handling the Hut provides. It asks no placement exception/terrain definition. Ordinary Sponsor placement remains the default; neither answer claims an exemption.','scope_index_parts_affected':[0]},
 'Q137':{'change':'Move inter-building sequencing to context.','why':'The singular standard-enclosure prompt asks its face and when/how often its covered-space bonuses are gained. Each bonus immediately once resolves this. Sequencing several buildings is true but not an independent actual part.','scope_index_parts_affected':[3]}
}
# Explicitly authored actual-part scope refinements; no factual key is edited.
replacement={('Q03',4):'Each spent X-token adds one strength',('Q19',3):'Restock the Association-board partner-zoo/university tiles at the worker-recall step',('Q19',5):'Take income after the display refresh and before resetting the Break token',('Q37',0):'Assertion chooses its project from the unused facedown base-project deck',('Q95',0):'Place the Barred Owl Hut unique building when its Sponsor is played'}
context_added={
 'Q03':[('A spent X-token returns to supply',[106])],
 'Q19':[('Restock one tile per kind, excluding all-owned kinds and without duplicate available tiles',[117]),('Income is composed of appeal money, kiosk income and activated Sponsor/map income',[119,120,121,122])],
 'Q37':[('The retrieved base project enters hand',[304])],
 'Q95':[('Ordinary unique-building placement rules apply',[296])]
}
# Split compound index entries where a genuine subpart is missing, to preserve individual resolution.
split={
 ('Q51',1):[('Peacocking still needs legal placement','C','C'),('Peacocking cannot add an Aviary if this zoo already has one','C','M')],
 ('Q112',0):[('Compare the icon count of each animal category against the player to the right','C','C'),('Gain one conservation for each category with a larger icon count','C','M')],
 ('Q125',1):[('Hypnosis selects highest appeal and chooses among tied leaders','C','C'),('Self-targeted Hypnosis has no effect','M','M')]
}
specific={
 ('Q07','a',0):'The generic range rule is right, but the volunteered numerical mapping labels reputation bands as folder numbers and reverses the correspondence.',
 ('Q15','b',7):'The only immediate bonus described is a covered-space map bonus; the university tile reputation is a separate absent award.',
 ('Q21','a',3):'Suitable substitutes expressly answer shortage handling. The caveat declines the stronger unasked universal that every component is unlimited; it does not withdraw substitution.',
 ('Q21','b',0):'The answer expressly calls the requested selection/placement detail unsupported. A correct setup quotation elsewhere in this same answer cannot resolve its denied mapping.',
 ('Q51','b',1):'Legal site is stated, but a one-per-zoo Aviary ownership cap is not stated by that site requirement.',
 ('Q112','b',0):'The comparison and icon quantity are stated, but no one-point conservation reward is given. One of yours refers to an icon, and four is the overall cap.',
 ('Q125','a',1):'Highest appeal and ties are stated; the no-effect self-target outcome is omitted.',
 ('Q125','b',1):'Highest appeal and ties are stated; the no-effect self-target outcome is omitted.',
 ('Q125','a',4):'Separately targeting each leader means independent applications, including two applications if both selections identify the same zoo. No other answer is needed.',
 ('Q125','a',6):'No Pilfering self-target no-effect outcome appears in this answer.',
 ('Q125','b',6):'No Pilfering self-target no-effect outcome appears in this answer.',
 ('Q125','b',9):'Eligible is left undefined here; the five-appeal eligibility floor is not supplied by any clause in this answer.'
}

def support(ns):
 return [{'line':n,'quote':lines[n-1]} for n in sorted(set(ns))]
def priorgrade(g):return g.get('overallgrade',g.get('overall_grade'))
def priorparts(g):return g.get('requestedparts',g.get('requested_parts'))
def citations(g,j,fallback):
 row=priorparts(g)[j]
 if 'summarysupportquote' in row:return [x['line'] for x in row['summarysupportquote']]
 return row.get('summary_support_lines',fallback)

def context_record(part,ans,ns,origin):
 return {'part':part,'status':'unrequestedcontext','observedquote':ans,'summary_support':support(ns),'reason':'Source-correct context; omission is not a missing actual requested part. Any volunteered assertion was still checked for contradiction and support.','origin':origin}
records=[]
for q in Q:
 id=q['id'];m=manifest[id];parts=S[id]['requested_parts'];n=len(parts)
 assert len(m['a'])==n and len(m['b'])==n,(id,n,m['a'],m['b'])
 rec={'id':id,'question':q['question'],'independent_scope_reason':corrections.get(id,{'change':'The neutral index matches the actual requested subject matter.','why':'Each requested part was assessed semantically within this answer; extra key context was not independently demanded.'}),'paired_reason':m['reason']}
 for side in ['a','b']:
  ans=R[side][id]['answer'];g=G[side][id];actual=[];contexts=[]
  for j,(part,ch) in enumerate(zip(parts,m[side])):
   ns=citations(g,j,m['lines']);part=replacement.get((id,j),part)
   if ch=='X':
    contexts.append(context_record(part,ans,ns,'scope index explicitly corrected by fresh adjudication'));continue
   expanded=split.get((id,j))
   entries=[(part,ch)] if expanded is None else [(t,a if side=='a' else b) for t,a,b in expanded]
   for text,c in entries:
    assert c!='X'
    why=specific.get((id,side,j),'The current answer resolves this actual requested proposition through its own words or ordinary logical entailment; cited frozen-summary text supports it.')
    if c=='M' and (id,side,j) not in specific:why='This actual requested part is absent or explicitly unresolved in the current answer.'
    if c=='C' and expanded and id in ['Q51','Q112','Q125']:
     why='This distinct subpart is resolved in the current answer; it is not supplied from any other answer.'
    actual.append({'part':text,'status':status[c],'observedquote':ans,'summary_support':support(ns),'reason':why,'neutral_index_part_position_1_based':j+1})
  if id=='Q14':
   actual.append({'part':'Each Association task needs an active worker, normally one before the own-worker repetition escalation','status':'complete','observedquote':ans,'summary_support':support([218]),'reason':'Both the active-worker requirement and ordinary singular worker are stated in this current answer; repetition rules are separately resolved above.','neutral_index_part_position_1_based':None})
  if id=='Q33':
   actual.append({'part':'In X:Y, X is the condition and Y is the reward','status':'complete','observedquote':ans,'summary_support':support([294]),'reason':'The question asks how to read the expression; both sides are explicitly interpreted here.','neutral_index_part_position_1_based':None})
  for part in S[id]['unrequested_context']:
   if id=='Q33' and part=='In X:Y, X is the condition and Y is the reward':continue
   contexts.append(context_record(part,ans,m['lines'],'neutral index context'))
  for part,ns in context_added.get(id,[]):contexts.append(context_record(part,ans,ns,'fresh literal-scope clarification'))
  extra={'reviewed_entire_current_answer':True,'summary_support_for_answer_and_volunteered_clauses':support(m['lines']),'reason':m['reason'],'material_false_volunteered_clauses':[],'source_correct_unsupported_guess_clauses':[]}
  if id=='Q07' and side=='a':extra['material_false_volunteered_clauses']=[{'observedquote':'spaces 1–6 correspond to folders 1, 2–3, 4–6, 7–9, 10–12 and 13–15','status':'contradicted','summary_support':support([150,152]),'reason':'Folder numbers are one through six; the bands are reputation spaces. These labels are reversed.'}]
  if id=='Q15' and side=='a':extra['material_false_volunteered_clauses']=[{'observedquote':'University research/reputation icons and partner continent icons count as zoo icons.','status':'contradicted','summary_support':support([90,92,93,94,96,222,290]),'reason':'Research and partner continent icons count. University reputation is an acquisition track award, not an additional countable zoo icon.'}]
  final=code[m['grades'][0 if side=='a' else 1]];initial=priorgrade(g)
  rec['reader_'+side]={'final_grade':final,'unsupported_guess':False,'answer_quote':ans,'reader_support_label_for_provenance_only':R[side][id]['support'],'actual_requested_parts':actual,'unrequested_context':contexts,'volunteered_clause_review':extra,'reason':m['reason'],'initial_grader_comparison':{'initial_grade':initial,'final_grade':final,'changed':initial!=final,'initial_reason':g['reason'],'independent_resolution':m['reason'],'initial_part_statuses':[{'part':x['part'],'status':x['status']} for x in priorparts(g)]}}
  hasbad=any(x['status']=='contradicted' for x in actual) or bool(extra['material_false_volunteered_clauses'])
  hasmissing=any(x['status']=='missing' for x in actual)
  assert final==('incorrect' if hasbad else 'partial' if hasmissing else 'correct'),(id,side,final,hasbad,hasmissing)
 records.append(rec)
counts={};nonpassing={};changes=[]
for side in ['a','b']:
 counts['reader_'+side]=dict(collections.Counter(r['reader_'+side]['final_grade'] for r in records))
 for grade in ['correct','partial','incorrect']:counts['reader_'+side].setdefault(grade,0)
 nonpassing['reader_'+side]=[r['id'] for r in records if r['reader_'+side]['final_grade']!='correct']
 for r in records:
  if r['reader_'+side]['initial_grader_comparison']['changed']:changes.append({'id':r['id'],'reader':'reader-'+side,**r['reader_'+side]['initial_grader_comparison']})
prior_concerns=[]
for side in ['a','b']:
 gd=D[f'expanded-iteration-02/independent-grade-{side}.json']
 for c in gd['borderline_key_scope_concerns']:
  id=c['id'];prior_concerns.append({'reader':'reader-'+side,'initial_concern_verbatim':c,'fresh_grade':next(r['reader_'+side]['final_grade'] for r in records if r['id']==id),'independent_resolution':manifest[id]['reason'],'scope_correction':corrections.get(id)})
 assert not gd.get('scope_index_inconsistencies_requiring_override',[])
intended_prompt='''Fresh independent semantic grading adjudicator for ArkNova94-question pair02. ReadONLY QAroot /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507/: expanded-iteration-02/{reader-a.json,reader-b.json,summary-snapshot.md,questions.json,independent-grade-a.json,independent-grade-b.json}; benchmark-v2/{answer-key.json,material-requested-facts.json}; grading-request-scope-01.json. No earlieriterations/rawsources/canonical/reviews/history/browsing/contactwithreaders. Readallinputscompletelyboundedrecovertruncation; independentlyreviewALL94answerspersideincludingpositives. Actualquestionmeaningcontrols scope; unchangedfactualkeyandneutralindexareguides, notpermissiontoaddunaskedrequirements. Strictcorrectallactualparts,nocontradiction/no unsupportedguess;partialmissing/unresolved/ambiguousactualpart;incorrectmaterialfalsevolunteeredrule. No cross-answerborrowing; readerlabelnotgrade; basic logicalentailment/meaningfuldefined-termshorthandperquestion scope allowed. ExplicitlyunresolvedACTUALrequestedpartcannotpass, butcaveataboutstrongerunaskedclaimdoesnotcreatemissingpart. Review allvolunteeredclausesagainstTHISsnapshot only. Resolvegraderborderlines independentlywithoutassumingcounts. Particularsemanticchecks: implicitconditionprovidedbyquestionitselfversusunconditionalfalse rule; 'player-countlimit' meaning; broadresource/general-unlimitedcaveats; literalrequestedversuscontextualtoken-disposaldestination; rewardquantitymeaningbeyondsimplekeyword; localactorownership/number mappings. Thesearequestions, no prescribedoutcome. Readeverypriorborderline/scopeconcern inbothgradefiles; ifscopeindexclassificationincorrectunderactualprompt documentcorrectionexplicitlywithoutchanginginput/keys orrelaxinggenuineparts. WriteONLY expanded-iteration-02/fresh-semantic-adjudication.json plusownnotesnamedfresh-semantic-*. Saveexactintendedprompt,inputhashes,fullreadingproof,94pairedrecords eachwithquestionandsidefinalgrade/unsupported_guessbool,allactualrequestedparts complete/missing/contradicted/unrequestedcontext,observedquote/summarysupport/reason/initialgradercomparison. Countcorrect/partial/incorrectperreaderandanyunresolvedissues. Keepallinputbytes/priorgrades unchanged. No assumedPASS,no keywordgrading,noreadercommunication.'''
chunks=[(1,5,'b354e4'),(6,12,'bfcd7a'),(13,15,'7fce26'),(16,16,'621615'),(17,19,'7fce26'),(20,24,'3eddee'),(25,29,'d12ad4'),(30,34,'96f49c'),(35,40,'186d2d'),(41,45,'b0d54a'),(46,50,'49b1eb'),(51,56,'2fbbff'),(57,62,'b3dafb'),(63,68,'448467'),(69,74,'1fb811'),(75,80,'4383a1'),(81,86,'668d9e'),(87,90,'6f030e'),(91,94,'7a30cf')]
result={'adjudicator':'fresh-independent-semantic-pair02','intended_prompt_exact':intended_prompt,'input_hashes':hashes,'fullreadingproof':{'complete':True,'summary_full_text_chunks':[{'inclusive_lines':span,'tool_output_chunk_id':cid,'truncated':False} for span,cid in [([1,110],'248434'),([111,220],'13c6af'),([221,315],'3ea7a4'),([316,370],'80ff37'),([371,426],'d9c083')]],'complete_json_semantic_chunks':[{'question_positions_1_based':[a,b],'tool_output_chunk_id':cid,'all_eight_json_documents_bundled':True,'content_read':'Complete questions, both answers/support/evidence, key/all facts and source metadata, neutral scope and both grader judgments including every requested-part status/evidence/reason/context clause. Exact repeated strings point to their previously read occurrence; support text equal to or contained in already fully read summary points to those lines. No semantic content was summarized away.'} for a,b,cid in chunks],'metadata_read_chunks':['18872e','52314d','d3f860'],'deduplication_templates':{'purpose':'Read the 1.53 MB of prior graders without repeatedly rendering identical full-answer and frozen-summary strings. This was a complete semantic read with explicit backreferences, not a search or hash substitute.','scripts':[str(o/'fresh-semantic-read.py'),str(o/'fresh-semantic-compact.py')],'reference_rules':'@Qxx.path denotes exact earlier string; @Lnn denotes exact previously read summary line; @Lnn[exact substring] denotes source text contained in the fully read summary starting at that line. Grader templates remove id/question only after equality to the current question, whole observed answer only after equality to the current reader answer, and boilerplate only after exact literal equality. Every nondefault field remains rendered. scope[n] denotes that current question neutral requested-parts string. Compact-key aliases are specified in the reading script.','template_defaults':'Grader A whole-current-answer observations and scope note; generic individually-reviewed note. Grader B whole-current-answer observations and resolved-with-summary explanation. Common context booleans true/false and generic entire-answer review note are exact defaults defined in fresh-semantic-compact.py and read initially at Q01. No verdict was templated or inferred.'},'truncation_recovery':[{'tool_output_chunk_id':'f8c601','issue':'Preliminary structure/sample output was truncated.','recovery':'All source metadata recovered in 18872e/52314d/d3f860; all complete Q01 judgments recovered in b354e4; it is not relied on for missing content.'},{'tool_output_chunk_id':'7fce26','issue':'The 13–19 bundle was truncated in Q16.','recovery_chunk_id':'621615','recovered_range':[16,16],'unaffected_visible_ranges':[[13,15],[17,19]]}],'all_94_ids_in_order':[q['id'] for q in Q],'independent_review':'Every positive and nonpassing answer on both sides was reviewed, including all volunteered clauses. Explicit per-question grade/status vectors and rationales were authored in fresh-semantic-decisions.txt after reading. Assembly code only attaches exact observations/citations and validates consistency; it does not keyword-grade or inherit initial verdicts.','boundaries':'Only the nine authorized inputs were read for rules/grading. No earlier iterations, raw/canonical sources, browsing or reader contact. Inputs were read-only; all writes are fresh-semantic-*.'},'rubric':{'correct':'All actual requested parts complete; no material false/contradictory rule and no source-correct unsupported guess.','partial':'A genuine requested part is absent, unresolved or ambiguous.','incorrect':'A material false or contradictory rule, including a volunteered clause.','scope':'Actual question controls; exact key facts unchanged; unrequested context omission is not failure. Meaningful defined-term shorthand and logical entailment within the current answer are allowed.','unsupported_guess':'Source-correct fact asserted without support in this frozen summary. False rules are contradicted, not source-correct unsupported guesses.','no_cross_answer_borrowing':True,'reader_label_not_verdict':True},'scope_corrections':[{'id':id,**v} for id,v in corrections.items()],'prior_borderline_and_scope_concerns_reviewed':prior_concerns,'counts':counts,'nonpassing_ids':nonpassing,'unsupported_guess_ids':{'reader_a':[],'reader_b':[]},'grade_changes':changes,'paired_records':records,'unresolved_issues':[],'input_integrity':{'all_nine_sha256_match_initial_read':True,'prior_grade_and_key_bytes_unchanged':True}}
(o/'fresh-semantic-adjudication.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'records':len(records),'counts':counts,'nonpassing_ids':nonpassing,'changes':[(x['id'],x['reader'],x['initial_grade'],x['final_grade']) for x in changes],'path':str(o/'fresh-semantic-adjudication.json')},indent=2))
