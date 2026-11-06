import json,re,hashlib
from pathlib import Path
B=Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507')
P=['expanded-iteration-05/reader-a.json','expanded-iteration-05/summary-snapshot.md','expanded-iteration-05/questions.json','benchmark-v3/answer-key.json','benchmark-v3/material-requested-facts.json','grading-request-scope-03.json']
R=json.loads((B/P[0]).read_text()); S=(B/P[1]).read_text().splitlines();Q=json.loads((B/P[2]).read_text())['questions'];K=json.loads((B/P[3]).read_text());M=json.loads((B/P[4]).read_text());I=json.loads((B/P[5]).read_text())
# Every row is an individually reviewed judgment, not a default grade. Each clause
# number maps one scope-index part to a numbered clause in this answer only.
# Evidence lines map in the same order; '+' gives several relevant source lines.
DATA='''
Q01 C 1,2,3,4,5,5,6 81;80;83;82;76;76;78
Q02 C 1,2,2,2,3 69;70;70;70;84
Q03 C 1,1,1,2,2,2,3,4 104;104;104;106;106;106;106;108
Q04 C 1,2,2,2,3 102;248;248;248;248
Q05 C 1,2,3,4 112;112;112;124
Q06 C 1,1,1,2,2,3,3,4,5 147;147+188;147;148;148+189;148;148;271;272
Q07 C 1,2,3,4 163;163;163;163
Q08 C 1,1,1,2,3,3,4,4,5,6 180;182;182;180;181;181;181;181;181;181
Q09 C 1,1,2,3,4,4 180;182;179;182;182;270
Q10 C 1,1,1+3,3,4 106;106;106+211;108;278
Q11 C 1,1,2,3,3,4,4,4,5,6,6 207;208;208;209;199;209;209;200+209;209;211+212;108+212
Q12 C 1,1,2,2,3,4 213;213;213;213;213;213
Q13 C 1,1,2,3,4,4,4 221;221;221;224;223;223;223
Q14 P 1,2,2,3,3,4,3 231+232+233+234;229;239;229;229;229;229
Q15 C 1,1,1,2,2,3,4,4 232+233;232+233;233;232+233;232;232;88;233+96
Q16 C 1,1,4,4,4,2,2,2,3,3 234;234+239;234;234;276;235+236;235+236;236;236;236
Q17 C 1,1,2,2,2,4,4,4 237;237;237;237;237;237;237;237
Q18 P 1,1,1,1,3,3 242;243;243;243;242;243
Q19 C 1,1,1,1,1,1,2,2,3,3,1 115;116;117;117;118;118+119+124;121;121;123;123;124
Q20 C 1,1,1,2,2,3,3,4,5,5,5 253;254;255;257;257;257;257;260;261;262;262
Q21 C 1,1,1,2 64;64;64;282
Q22 C 1,2,2 75;75;75
Q23 C 1,2,3 79;280;280
Q24 C 1,1,2,2,3 110;110;110;110;110
Q25 C 1,1,1,1,1,2 188;188;188;188;188;191
Q28 C 1,1,1,1 286;286;286;286
Q29 C 1,1,1,1,2,2,2,2,2,3 239;239;239;239;239;239;239;239;239;239
Q30 C 1,1,1,2,3,3,4 301;301;301;301;301;301;301
Q31 C 1,1,1+2,3 209+301;301;301;301
Q32 C 1,1,2,2 237;237;238;238
Q33 C 2,3,3,1 305;305;305;305
Q34 C 1,2,3,4,4 303;303;303;303;303
Q35 C 1,1,3,3,2,4,4 307;307;307;307;307;307;307
Q36 C 1,2,3,3 313;313;313;313
Q37 C 1,1,2,3,3 315;315;315;315;315
Q38 C 1,2,2,2,2 314;314;314;314;314
Q39 C 1,2,2,3 334;334;334;334
Q40 C 1,2,3,3,3,4 346;346;346;346;346;346
Q41 C 1,1+2,2 346;346;346
Q42 C 1,2,2 316;316;316
Q43 C 1,2,1,1,3,4,4 317;317;317;317;317;317;317+237
Q44 C 1,2,3 318;318;318
Q45 C 1 321
Q46 C 1,1,2,2,3,4,4 348;348;348;348;348;348;348
Q49 C 1,1,2,2,2,3,3,4 332;332;332;332;332;332;332;332
Q50 C 1,3,3 332;332;332
Q51 C 1,1,1,1,2,2 330;330;330;330;329;329
Q52 C 1,2,3 328;328;328
Q53 C 1,1,2 350;350;350
Q54 C 1,1,2,2,2,3 350;350;350;350;350;350
Q55 C 1,1,1,2 326;326;326;325
Q56 C 1,1,2,2 327;327;327;327
Q57 C 1,1 325;325
Q58 C 1,1,2,2,3 322;322;322;322;322
Q59 C 1,1,2,3,3,4 347;347;347;347;347;347
Q63 C 1,2,3 369;370;371
Q66 C 1,2 384;385
Q67 C 1,1,2 389;389;389
Q68 C 1,2,3 393+355;394;395
Q70 C 1,2,2,3 405+355;406+355;406;407
Q72 C 1,2,2 417+355;418+355;418
Q75 C 1,1,1,2,3 433;433;433;433;434
Q77 C 1,1,1,2,2,3 443;443;443;443;443;444
Q78 C 1,2,2,2,3,4 448;449;449;449;449;450
Q80 C 1,1,2,3 460;460;460;461
Q82 C 1,2,3,3,4 469;469;469;469;469
Q83 C 1,2,2,3 473;473;473;474
Q85 C 1,1,3,2,3 483;483;483;483;483
Q86 C 1,2,2,2,3,3 487;487;487;487;487;487
Q90 C 1,2,2,2,3 511;512;512;512;513+303
Q95 C 1,2 534;535
Q96 C 1,2,2 539;540;540
Q98 C 1,2,2 551;551;551
Q99 C 1,2,2,3,3 555;555;555;555;555
Q100 C 1,2,3 559;559;559
Q102 C 1,1,1,2,2,3 567;567;567;568;568;569
Q104 C 1,1+3,3,2,2+3 578;578;579;579;579
Q106 C 1,2,3 588;589;589
Q107 C 1,2,2,3 593;594;594;594+614
Q112 C 1,1,2,3 609;609;609;609
Q113 C 1,2,3,2 610;610;610;610
Q114 C 1,2,3,4,4 611;611;611;611;611
Q115 C 1,1,2,2,2,3 612;612;612;612;612;612
Q116 C 1,1+2,3,4,4,1 613;613;613;613;613;613
Q119 C 1,1,2,3,4,4 616;616;616;616;616;616
Q123 C 1,2,3 624;624;624
Q124 C 1,1 626;626
Q125 P 1,2,2,2,3,3,3,3,4,4,1+2+3+4 340;341;341;341;342;343;343;343;344;344;336
Q127 C 1,2,3,4 625;625;625;620
Q133 C 1,1,1 316;316;316
Q134 C 1,1,1 163;163;163
Q137 C 1,2,2 167;167;167
Q139 C 1,1 255;255
Q140 C 1,1,2,3,3 72;72;31;31;108+313
Q141 C 1,1 255;255
'''
# Explicit failures are narrow omissions, not material false rulings.
FAIL={
 'Q14':{7:('partial','The answer specifies worker counts and repeat escalation but never resolves the active-worker availability prerequisite. A reserve/inactive worker cannot simply be sent. This is within the requested worker requirements.')},
 'Q18':{4:('partial','Sequential resolution is stated, but after-finishing effects are not deferred anywhere in this answer. Resolving multiple Sponsors requires distinguishing their immediate effects from effects that wait for the full action. Treat the broad sequential sentence as incomplete, rather than an explicit false denial of the exception.')},
 'Q125':{11:('partial','The five-appeal floor is supplied for Venom, Hypnosis and Constriction, but omitted for both Pilfering targets. The conservation-target minimum of one conservation does not establish the separate five-appeal eligibility requirement.')}
}
NOTES={
'Q01':'Hidden Final Scoring cards are accurate key context rather than another actual request. All seven requested setup parts resolve. Face-up Zoo discard is supported.',
'Q02':'"Two-player game only" entails no such blocking at three/four. The extra statement that no further blocking differences are specified is consistent with this summary.',
'Q03':'Moving only the cards left of slot four entails original slot five stays fixed. Spent-token destination is key context, not another request.',
'Q05':'Reset and the absence of bonus turns for a normal break are volunteered and both supported (112/124/628). The ordinary holding cap need not be restated.',
'Q06':'The draw-table procedure is meaningful shorthand here; the question requests action options and timing, not every table cell (Q25 separately requests I cells). Side-II strength-five example and no-money I advance are accurate.',
'Q09':'The unqualified statement "Covering every map space except water and rock immediately grants 7 appeal" covers completion by other effects too. Supply quantity is volunteered and matches line 179. Printed footprints are unrequested key context.',
'Q10':'"Resolve items one at a time" together with immediate effects during that action resolves before-next-item timing; no need to borrow another answer.',
'Q11':'Payment comes before all effects in this answer, entailing own-payout cannot finance itself. The named after-finishing timing is defined in the frozen summary to include card movement; "Animals action ends" is accepted as procedure shorthand, not an affirmative pre-movement ruling.',
'Q12':'Display in addition to hand states both allowed sources without any exclusivity; an ordinary mixed play is entailed.',
'Q14':'Reputation task reward and break recall are extra factual-key context. Active-worker availability is a genuine requested worker requirement and remains unresolved.',
'Q16':'Normal support restriction and one-token-across-players restriction are both explicit. Player-count project cap is unrequested; mentioning "player-count limit" is accurate. It does not assert any wrong cap.',
'Q17':'The conditional "If ... remove them; otherwise" states mandatory special-token priority. Flock-specific reminder is extra key context; the general release rule is unqualified and does not exempt flock animals. The volunteered new-project reputation is source-supported.',
'Q18':'"Resolves each card before the next" supplies sequential play but does not identify after-finishing deferral. Display refill at turn end is accurate extra context. No unsupported guess or express false ruling is present.',
'Q20':'The never-reached-ten fallback, tile removal, and full scoring sequence are unrequested context here; Q141 actually asks the fallback. All milestone values, timing, cap and tiebreak demanded here are given.',
'Q22':'Returning unused maps and later adjacency are unrequested factual-key context. Reminder tile and already-built kiosk claims agree with line 75.',
'Q23':'The general rule does not enumerate which maps have the last-worker bonus; the volunteered limitation on specificity is accurate.',
'Q24':'The actual question does not ask the names of all four upgrade sources. The volunteered count and alternative choice are true.',
'Q30':'Counting doubled icons twice for a card\'s effects meaningfully entails the two matching triggers; it does not claim one combined trigger. The ordinary zoo-icon list is consistent with lines 238/301.',
'Q32':'"Same condition on all three levels" and "any available level" resolve the request without requiring printing all rewards or program card numbers.',
'Q39':'Extra target summaries are consistent general descriptions with the universal five-appeal floor explicit. They do not expressly waive the more specific self/zero-conservation restrictions, which this question does not request.',
'Q41':'The answer positively permits the alternative. Its final sentence distinguishes an elected alternative from automatic conversion, and does not deny taking the alternative with the constricted card.',
'Q43':'"Another herbivore" is unrestricted as to flock status, so both host types qualify by entailment. The conditional exception plus ordinary housing is adequate procedure shorthand for no suitable host; "usual procedure" expressly invokes release fallback, not another answer. Host type/normal housing are elaborations of the actual when/avoid question, not separate hidden demands.',
'Q45':'Volunteered ordinary successful-Hunter procedure is accurate; the requested no-Animal outcome is explicit.',
'Q46':'The extra slot-one-through-three restriction is accurate. Other-card upgrade checks are unrequested context, per scope. Tied/self targets, borrowed side, own tokens and target token cleanup are all given.',
'Q49':'Bonus-tile any-card permission includes Animals without requiring that example to be restated. Moving after the executions is ordinary Action-card movement, not a claim that it goes anywhere else.',
'Q50':'The extra each-X-token-one-execution clause is correct. Taking two X-token alternatives is expressly limited by the cap and no mixing.',
'Q55':'The volunteered Pouch and Sunbathing quantities/rewards match lines 325–326. They are not unsupported guesses.',
'Q56':'The prompt itself supplies Resistance, so the extra Final Scoring draw in clause one identifies its granted card. It is not an unexplained unrelated draw.',
'Q57':'The extra Scavenging-three counts match the illustrated ability in line 325.',
'Q67':'"Per two different continent/animal-category icons" excludes research/repeated copies and pays per complete pair. Rounding down is normal entailment, not a missing demand.',
'Q68':'Research icons in the default own-zoo scope are sufficient; clause two explicitly changes the trigger to any player and identifies the beneficiary owner.',
'Q70':'Ordinary placement/spacing is meaningful named-rule shorthand; this answer does not suggest a free kiosk bypasses spacing.',
'Q75':'Stored two supply tokens identifies initial program storage; the actual question does not separately ask exact timing beyond the card effect. Both cards are covered by "each card". Different play conditions are unrequested.',
'Q78':'The extra map-completion terrain exclusion is correct. The immediate money amount and final pairs/cap match this frozen summary.',
'Q80':'Volunteered owner-chosen resolution order is source-supported.',
'Q82':'The ordinary five-X-token cap is unrequested context; no unlimited holding permission is asserted.',
'Q83':'The ordinary X-token cap need not be repeated. "Next qualifying player" preserves qualification and does not claim a target exists if none qualifies.',
'Q85':'Size definitions are unrequested context; the permanent choice, prohibition, selected rewards and size-three exception are all stated.',
'Q86':'Only-small condition excludes any original nonsmall animal. The extra display take is into hand, not a free display play.',
'Q90':'"Connected (none isolated)" uses a defined map term; it does not assert a single connected water region. Distinct per-covered-space payments are explicit.',
'Q98':'Hunter is meaningful defined-procedure shorthand. Full Hunter steps and building rock placement are unrequested here; the question targets X and duplicate-trigger calculation.',
'Q99':'Building placement is accurate extra context. Hand-only Sponsor, normal conditions, money cost and three token-funded uses are explicit.',
'Q100':'Owner-chosen simultaneous effect ordering is accurate extra context; the question does not require a reputation-first example.',
'Q102':'The expressly narrow adjacency exception retains all other ordinary placement rules by entailment. Nothing claims a second waiver. Kiosk adjacency, income exceptions and final full-map reward are explicit.',
'Q104':'The example 13,6,3,2 gives 3 is accurate and demonstrates separate flooring. Restricted spaces are expressly included without Build II.',
'Q106':'The category label includes bear/Petting Zoo by definition; no need to repeat the full seven-category list. The research exclusion and double-new-icon once rule are explicit.',
'Q107':'"Stacks with Research Institute" invokes its defined active ability; no claim permits an unactivated Institute. Large-animal and terrain limitations stay explicit.',
'Q112':'Sponsor icons and category examples are unrequested context. Per-category larger icon counts, zero neighbor and cap all resolve.',
'Q114':'The volunteered physical size-two becomes four example is correct. The increase concerns enclosure size, not changing the animal\'s printed release band.',
'Q116':'Per covered hex irrespective of building/occupancy entails several hexes of one building count separately. It does not describe ordinary kiosk income. Choice of one free special enclosure and persistent placement rules are explicit.',
'Q119':'The level reduction is stated after covering all H spaces; no perpetual printed change outside the intended Sponsor use is asserted. Bonus upgrade gates are explicit.',
'Q125':'Separate Pilfering targets entails double resolution if they coincide. The missing Pilfering five-appeal floor is an unresolved actual target-selection part, not an express assertion that sub-five targets are legal.',
'Q127':'The volunteered max-25 reminder is not a track cap matches the summary. Terrain nonwaiver is supported.',
'Q133':'The extra option-switching and immediate display refill are source-supported.',
'Q134':'Volunteered break compaction is accurate. The vague final remark about no separate nonstandard-refill rule is a concern: Digging explicitly has immediate refill (316). Read narrowly as no alternative gap/order mechanism, it does not deny Digging timing or assert a wrong action; normal ordered deck refill is explicit. A broad denial of all special refill timing would be false, but that is not an unambiguous material ruling in this answer.',
'Q137':'Sequential different-building timing is key context rather than a separate demand in this question; every covered bonus immediately once and no occupied-side replay are clear.',
'Q139':'Extra all-player trigger condition matches the summary. Destination and orientation are explicit.',
'Q140':'The answer distinguishes the one ordinary action from bonus actions/effects and invokes their actual timing, without denying named granted additional actions.',
'Q141':'Given no-ten condition is preserved. Discard-one before scoring resolves both actual parts. Its volunteered comment only says fallback destination/orientation is not explicitly specified in this summary; the fallback sentence indeed does not restate either. No extra location/orientation demand is imposed.'
}

def ev(lines):
 return [{'line':n,'quote':S[n-1]} for n in lines]
judgments=[]
for row in DATA.strip().splitlines():
 id,g,c,s=row.split(); qs=next(q for q in Q if q['id']==id); r=next(r for r in R['answers'] if r['id']==id)
 clauses=re.split(r'(?<!\d)\b\d+\. ',r['answer'])[1:]
 cm=[list(map(int,x.split('+'))) for x in c.split(',')];sm=[list(map(int,x.split('+'))) for x in s.split(';')]
 parts=I['questions'][id]['requested_parts'];assert len(cm)==len(sm)==len(parts),(id,len(cm),len(sm),len(parts))
 pj=[]
 for n,(p,ci,si) in enumerate(zip(parts,cm,sm),1):
  status,reason=FAIL.get(id,{}).get(n,('satisfied','The quoted clause resolves this requested part, directly or by the ordinary entailment/defined-procedure reading explained in the answer review.'))
  pj.append({'part':p,'status':status,'observed_clause_quotes':[clauses[i-1].strip() for i in ci],'summary_support':ev(si),'reason':reason})
 judgments.append({'id':id,'question':qs['question'],'requested_parts':pj,'overallgrade':{'C':'correct','P':'partial','I':'incorrect'}[g],'unsupported_guess':False,'reason':'; '.join(v[1] for v in FAIL.get(id,{}).values()) if id in FAIL else 'All actually requested parts resolve; no material contradiction or unsupported source-correct claim.','context_and_volunteered_review':NOTES.get(id,'Checked all volunteered clauses against the quoted frozen-summary rules. Additional ordinary procedure detail is source-supported and does not change any ruling.'),'scope_index_concerns':[]})
assert [j['id'] for j in judgments]==[q['id'] for q in Q]

# Manually selected short, exact clauses for answers whose numbered item itself
# contains several requested subparts. This is quotation editing, not grading.
OBS={
 'Q01':{5:["Place the Animals Action card side I in the leftmost slot (strength 1)"],6:["place the other four side-I Action cards randomly in the remaining slots."]},
 'Q03':{3:["shift the cards that were left of its now-empty slot one place right, and put the used card in slot 1."]},
 'Q28':{1:["The categories are bird, herbivore, predator, primate, reptile, bear and Petting Zoo animal."],2:["Include both unless specifically excluded."],3:["Bears count as a category even when combined with herbivore or predator"],4:["Petting Zoo animal is its own category."]},
 'Q33':{2:["A numbered threshold pays only once"],3:["with multiple thresholds, use the highest one met."]},
 'Q34':{4:["'Your zoo' includes your played cards, map and personal supply"],5:["'any zoo' includes those areas for all players."]},
 'Q55':{1:["tucked cards have no remaining function."],2:["If the animal is released, discard those tucked cards too"],3:["keeping appeal already earned."],4:["sold cards go to discard."]},
 'Q57':{1:["Shuffle the discard pile face down and draw randomly"],2:["then return the pile face up."]},
 'Q75':{1:["Each card stores two supply tokens."],2:["return exactly one token as any one icon; never use both for one support."],3:["When supporting a Base Conservation Project below the Association board"]},
 'Q82':{3:["You may support the same release project repeatedly with different qualifying animals"],4:["but at most one token on that project per Association action."]},
 'Q85':{1:["Choose small or large permanently and mark the choice with a supply token"],2:["reveal deck cards until finding that animal type, keep it and discard the rest."]},
 'Q124':{1:["Appeal cannot exceed 113", "gains beyond those track ends are lost."],2:["conservation cannot exceed 41", "gains beyond those track ends are lost."]},
 'Q133':{1:["Crested Porcupine's Digging 2 allows up to two selections"],2:["discarding a display card and immediately replenishing it"],3:["discarding a hand card then drawing one deck card."]},
 'Q134':{1:["slide the remaining higher-folder cards down"],2:["in their existing order"],3:["then fill empty spaces from the deck."]},
 'Q137':{2:["Each covered placement-bonus icon is awarded immediately once when covered"],3:["turning the enclosure to occupied later does not award it again."]},
 'Q139':{1:["under the remaining pile."],2:["face down"]},
 'Q140':{1:["Randomly determine the start player"],2:["turns proceed clockwise."]},
 'Q141':{1:["all players must discard one Final Scoring card"],2:["before end-game scoring begins."]}
}
for j in judgments:
 answer=next(r['answer'] for r in R['answers'] if r['id']==j['id'])
 for n,quotes in OBS.get(j['id'],{}).items():
  assert all(q in answer for q in quotes),(j['id'],n,quotes)
  j['requested_parts'][n-1]['observed_clause_quotes']=quotes

# Index distinctions are recorded rather than silently becoming extra demands.
CONCERNS=[
 {'id':'Q01','type':'key-context','finding':'Key/material includes hidden Final Scoring cards; actual question requests starting cards/count. Scope correctly excludes secrecy.'},
 {'id':'Q03','type':'entailment','finding':'Scope explicitly lists unchanged slot five. Answer states the precise set of moving cards, which entails that result.'},
 {'id':'Q09','type':'entailment','finding':'Scope spells out completion outside Build; answer gives the unconditional coverage trigger, which includes it.'},
 {'id':'Q14','type':'borderline','finding':'Active-worker qualification is a real worker-availability requirement, not just key context. Counts alone do not settle it.'},
 {'id':'Q18','type':'borderline','finding':'Sequential card resolution alone omits after-finishing deferral; interpreted as partial rather than material false claim.'},
 {'id':'Q43','type':'scope-elaboration','finding':'Host flock/non-flock and no-host ordinary housing are elaborations not expressly separate subquestions. They are nevertheless entailed by unrestricted another-herbivore exception and ordinary housing. No hidden separate recitation requirement imposed.'},
 {'id':'Q46','type':'key-context','finding':'Other-card upgrade checks are not requested here. Five-appeal threshold is not separately asked here, unlike Q39/Q125.'},
 {'id':'Q98','type':'key-context','finding':'Building placement and full Hunter procedure in key/material are explicitly unrequested in scope. Hunter shorthand is meaningful.'},
 {'id':'Q102','type':'scope-elaboration','finding':'Other placement rules persist under a narrow adjacency exception; they need not all be restated.'},
 {'id':'Q107','type':'entailment','finding':'Research Institute is a defined ability requiring activation; citing that ability does not affirm it works while inactive.'},
 {'id':'Q125','type':'actual-omission','finding':'Universal five-appeal eligibility does form part of target comparison. Answer qualifies three abilities but never Pilfering.'},
 {'id':'Q134','type':'volunteered-ambiguity','finding':'Digging has special immediate refill timing. The vague nonstandard-refill remark is accepted only as saying there is no other gap/order mechanism; it cannot support denying the explicit Digging exception. No concrete conflicting timing ruling is expressed.'},
 {'id':'Q137','type':'key-context','finding':'Before-next-building bonus timing is factual key context rather than another actual requested part.'},
 {'id':'Q141','type':'given-condition','finding':'No-ten condition is supplied by the question and preserved. Fallback discard destination/orientation is not requested; summary fallback sentence does not expressly repeat it.'}
]
for j in judgments:j['scope_index_concerns']=[c for c in CONCERNS if c['id']==j['id']]
counts={g:sum(j['overallgrade']==g for j in judgments) for g in ['correct','partial','incorrect']}
PROMPT='''You are a fresh independent grader for Ark Nova's 95-question reader A. Read ONLY these six complete inputs under /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507/: expanded-iteration-05/reader-a.json, expanded-iteration-05/summary-snapshot.md, expanded-iteration-05/questions.json, benchmark-v3/answer-key.json, benchmark-v3/material-requested-facts.json, grading-request-scope-03.json. Do not read another reader, prior grades/reports/history, raw sources, canonical summary, or browse/contact anyone. Read all inputs completely in bounded chunks, recovering truncation. Independently grade ALL 95 answers and every ACTUALLY REQUESTED part. The actual question controls scope; factual keys stay fixed. The neutral scope index contains no prior answers/results. Accurate extra key context is not another demand; any volunteered false ruling still counts. Explicitly flag index/question inconsistencies rather than imposing hidden requirements. Correct requires complete actual requested parts, no contradiction and no unsupported source-correct guess. Partial means a missing, unresolved or ambiguous actual part. Incorrect means a material false or contradictory ruling, including volunteered claims. Do not borrow between answers. The support label is not the grade. Allow ordinary logical entailment and meaningful defined-procedure shorthand according to the prompt's scope; preserve conditions supplied by the question. Review every volunteered clause against this frozen summary. Write ONLY expanded-iteration-05/independent-grade-a.json and own notes named independent-grade-a-*. Include the exact intended prompt, six input hashes, complete-read proof, and 95 ordered judgments: id, each requested part with status, relevant observed clause quote and summary support quote/line, overallgrade correct|partial|incorrect, unsupported_guess boolean, reason and context/volunteered review. Quote relevant clauses rather than repeating whole answers for every part. Include C/P/I counts, nonpassing IDs and any borderline/key/scope concerns. No assumed PASS, no keyword grading, no relaxing genuine requested parts; do not edit inputs.'''
proof=[]
for p in P:
 raw=(B/p).read_bytes();proof.append({'path':p,'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'physical_lines':len(raw.splitlines()),'complete_read':True})
result={'reader':'reader-a','iteration':'expanded-iteration-05','grader':'fresh independent grader A','exact_intended_prompt':PROMPT,'inputs':proof,'complete_read_proof':{'summary_chunks':[[1,155],[156,310],[311,465],[466,644]],'companion_chunks':'All five JSON inputs fully parsed; every field of all 95 question/answer/key/material/scope records displayed in ten bounded batches of ordered positions 1–10, 11–20, 21–30, 31–40, 41–50, 51–60, 61–70, 71–80, 81–90, 91–95. All metadata displayed separately. Each five inputs has exactly these same 95 IDs; no unbanked records remain.','truncation':'No six-input content read was truncated. An initial workspace status/listing was truncated and contained file names only; no forbidden file contents were read. It was not grading evidence.','method':'Manual semantic reading and explicit per-part clause-to-summary evidence mapping; no reader-label grading, answer borrowing, assumed passing default, or keyword grading.'},'counts':counts,'C_P_I':{'C':counts['correct'],'P':counts['partial'],'I':counts['incorrect']},'nonpassing_ids':[j['id'] for j in judgments if j['overallgrade']!='correct'],'unsupported_guess_ids':[],'scope_index_inconsistencies':[],'scope_index_consistency_note':'Question texts match throughout. Scope elaborations and unrequested key context are explicitly distinguished in the concerns; no hidden recitation requirements imposed.','borderline_key_scope_concerns':CONCERNS,'judgments':judgments}
out=B/'expanded-iteration-05/independent-grade-a.json';out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'path':str(out),'counts':counts,'nonpassing_ids':result['nonpassing_ids'],'parts':sum(len(j['requested_parts']) for j in judgments)}))
