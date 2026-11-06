import json, pathlib, hashlib, re, collections
BASE=pathlib.Path('/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507')
OUT=BASE/'expanded-iteration-05'
paths=['expanded-iteration-05/reader-b.json','expanded-iteration-05/summary-snapshot.md','expanded-iteration-05/questions.json','benchmark-v3/answer-key.json','benchmark-v3/material-requested-facts.json','grading-request-scope-03.json']
raw={p:(BASE/p).read_bytes() for p in paths}
r={a['id']:a for a in json.loads(raw[paths[0]])['answers']}
qs=json.loads(raw[paths[2]])['questions']
sc=json.loads(raw[paths[5]])['questions']
lines=raw[paths[1]].decode().splitlines()
# Every row was manually adjudicated after the complete read. Columns are:
# ID, explicit final grade, numbered reader clauses in scope-part order,
# manually selected frozen-summary line(s) in that same order.
CONFIG='''
Q01 C 1,2,3,4,5,5,6 81,80,83,82,76,76,78
Q02 C 1,2,2,2,3 69,70,70,70,84
Q03 C 1,1,1,2,2,2,3,4 104,104,104,106,106,106,106,108
Q04 C 1,2,2,2,3 102,248,248,248,248
Q05 C 1,2,3,4 112,112,112,124
Q06 C 1,1,1,2,2,3,3,4,5 147,147+188,147,148,148+189,148,148,271,272
Q07 C 1,2,3,4 163,163,163,163
Q08 C 1,1,1,2,3,3,4,4,5,6 180,182,182,180,181,181,181,181,181,181
Q09 C 1,2,1+2,3,4,4 180,182,179,182,270,270
Q10 C 1,2,1+3,3,4 106,106,211+212,108,278
Q11 P 1,1+4,1,2,2+3,2,2,2,2,4,4 207,208+273,208,199,199,209,209,200,209,211+212,212
Q12 C 1,2,3,3,4,5 213,213,213,213,213,213
Q13 C 1,2,2,2,3,3,3 221+226,221,221,224,223,223,223
Q14 P 1,2,2,3,3,4,2+3 231+232+233+234,229,239,229,229,229,229+239
Q15 C 1,1,1,2,2,2,4,4 232+233,232+233,232+233,232+233,232,623,88,96+233
Q16 P 1,1,4,4,4,2,2,3,3,3 234,239,234,234,276,235,236,236,236,236
Q17 C 1,1,2,2,2,3,3,3 237,237,237,237,237,237,237,237
Q18 C 1,2,2,2,3,3 242,243,243,243,242,243
Q19 C 1+2,1,1,1,1,1,3,3,4,4,1 115,116,117,117,118,119+124,121,121,123,123,124
Q20 C 1,1,1,2,2,3,3,4,5,5,5 253,254,255,257,257,257,257,260,261,262,262
Q21 C 1,1,1,2 64,64,64,282
Q22 C 1,2,2 75,75,75
Q23 C 1,2,3 79,280,280
Q24 C 1,1,2,2,3 110,110,110,110,110
Q25 C 1,1,1,1,1,2 188,188,188,188,188,191
Q28 C 1,1,1,1 286,286,286,286
Q29 C 1,1,1,1,2,2,2,3,3,3 239,239,239,239,239,239,239,239,239,239
Q30 C 1,1,1,1,2,2,3 301,301,301,301,301,301,301
Q31 C 1,1,1+2,2 209,209,209,301
Q32 C 1,1,2,2 237,237,238,238
Q33 C 2,3,3,1 305,305,305,305
Q34 C 1,2,3,4,4 303,303,303,303,303
Q35 C 1,3,1,2,1,2,2 307,307,307,307,307,307,307
Q36 C 1,1,2,2 313,313,313,313
Q37 C 1,1,2,3,3 315,315,315,315,315
Q38 C 1,2,2,2,2 314,314,314,314,314
Q39 C 1,2,2,3 334,334,334,334
Q40 C 1,1,2,2,2,3 344+346,346,346,346,346,346
Q41 C 1,1+2,2 346,346,346
Q42 C 1,2,2 316,316,316
Q43 C 1,2,2,3,3,4,4 317,317,317,317,317,317,317
Q44 C 1,2,3 318,318,318
Q45 C 1 321
Q46 C 1,1,3,2,4,3,3 341+348,348,348,348,348,348,348
Q49 C 1,1,1,1,2,2,3,4 332,332,332,332,332,332,332,332
Q50 C 1,2,2 332,332,332
Q51 C 1,1,1,2,3,3 330,330,330,330,329,329
Q52 C 1,2,3 328,328,328
Q53 C 1,1,2 350,350,350
Q54 C 1,1,2,2,2,3 350,350,350,350,350,350
Q55 C 1,1,1,2 326,326,326,325
Q56 C 1,1,2,2 327,327,327,327
Q57 C 1,1 325,325
Q58 C 1,1,2,2,3 322,322,322,322,322
Q59 C 1,1,2,3,3,4 347,347,347,347,347,347
Q63 C 1,2,3 369,370,371
Q66 C 1,2 384,385
Q67 C 1,1,2 389,389,389
Q68 C 1,2,3 393+355,394,395
Q70 C 1,2,2,3 405+355,406+355,406,407
Q72 C 1,2,3 417+355,418+355,418
Q75 C 1,1,1+2,2,3 433,433,433,433,434
Q77 C 1,1,2,2,2,3 443,443,443,443,443,444
Q78 C 1,2,2,2,3,4 448,449,449,449,449,450
Q80 C 1,2,3,4 460,460,460,461
Q82 C 1,2,2,2,3 469,469,469,469,469
Q83 C 1,2,2,3 473,473,473,474
Q85 C 1,1,3,2,3 483,483,483,483,483
Q86 C 1,2,2,3,3,2 487,487,487,487,487,487
Q90 C 1,2,2,2,3 511,512,512,512,513+303
Q95 C 1,2 534+307,535+355
Q96 C 1,2,2 539,540+355,540
Q98 C 1,2,1+2 551,551,551
Q99 C 1,1+3,1,2,2 555,555,555,555,555
Q100 C 1,2,3 559,559,559
Q102 C 1,1,1,2,2,3 567,567,567,568,568,569
Q104 C 1,1+3,3,2,2 578,578+608,579,579,579
Q106 C 1,2,2 588,589,589
Q107 C 1,2,2,3 593,594,594,594+614
Q112 C 1,1,2,3 609,609,609,609
Q113 C 1,2,3,4 610,610,610,610
Q114 C 1,2,3,4,4 611,611,611,611,611
Q115 C 1,1,2,2,2,3 612,612,612,612,612,612
Q116 C 1,1,2,3,3,1 613,613,613,613,613,613
Q119 C 1,1,2,3,4,4 616,616,616,616,616,616+623
Q123 C 1,2,3 624,624,624
Q124 C 1,1 626,626
Q125 C 1,2,2,2,3,3,3,3,4,4,1+2+3+4 340,341,341,341,342,343,343,343,344,344,336+343+344
Q127 C 1,2,3,4 625,625,625,620
Q133 C 1,1,1 316,316,316
Q134 C 1,1,1 163,163,163
Q137 C 1,2,2 167,167,167
Q139 C 1,1 255,255
Q140 C 1,1,1,2,2 72,72,31,31,106+108+313
Q141 C 1,1 255,255
'''
# Manual explanations cover the reason for the grade, plus all volunteered context.
REVIEWS={
'Q01':('All setup quantities, Action sides/order and turn-order appeal are correct.','Hidden Final Scoring cards and the four-card opening discard are accurate setup details.'),
'Q02':('Correct project count by player count, exact two-player blocking, and reveal timing.','Shuffling, below-board placement and the absence of three/four-player blocking agree with setup.'),
'Q03':('Correct movement, advance strength setting, X strength/cap and deferred effects.','Slot 5 stays by entailment: only cards left of slot 4 shift, while used card moves to 1. Newly gained tokens cannot boost this action.'),
'Q04':('Correct prohibition, alternative reward, card movement and holding cap.','Strength and upgrade irrelevance are expressly supported.'),
'Q05':('Correct excess movement, trigger reward, whole-turn delay and next-player rule.','Resetting the token to its starting space is accurate extra context; numerical cap need not be restated here.'),
'Q06':('Both draw/snap procedures, thresholds, reputation exception, Break movement and timing resolve correctly.','Cards I drawing by its table is meaningful draw-procedure shorthand; the restriction-only-on-II-draw clause establishes unrestricted snaps on either side. The side-II 4-draw/1-discard example is correct.'),
'Q07':('All four asked reputation/discard issues are resolved.','Does not need to volunteer the key\'s unasked track-bonus timing; no unsupported extra claim.'),
'Q08':('All Build budgets, costs, placement restrictions, kiosk distance and pavilion reward are correct.','The final until-Build-II phrase is read as qualifying restricted-icon spaces, rather than allowing water/rock or overlap after upgrade; payment before placement is correct.'),
'Q09':('Correct enclosure availability, per-zoo special limits, unique-building exclusion and full-map bonus.','Four supplied copies of each special type and Build II unlocking marked spaces are accurate; footprints are unasked.'),
'Q10':('Correct sequential funding and immediate/deferred/simultaneous effect handling.','The animal-payment example is supported. Current action strength/kind is unasked context, so its absence is not a deficit.'),
'Q11':('Partial: terrain adjacency is described with standard housing, while special housing is conditioned only on capacity; whether special enclosures must satisfy terrain remains unresolved.','The payment-then-effect sequence entails advance payment, and the per-icon discount entails six for two icons. Multiple-special/one-standard occupancy and after-finishing timing are accurate. No material false ruling is asserted.'),
'Q12':('Every Animals II addition and timing point requested is correct.','Optional initial reputation is explicit; no extraneous unsupported claim.'),
'Q13':('Complete construction-only relocation, individual eligibility/capacity/terrain and all freeing fallbacks.','Bonus construction is accurate. Adds tokens for relocation rather than removing release tokens.'),
'Q14':('Partial: the normal active-worker requirement is expressly attached to Association I; the answer never resolves the baseline worker-per-task requirement for a multi-task Association II action.','Correct strengths, different-task budget, two-worker repetition, three-worker lockout and ignoring opponents. This is an omission/ambiguity rather than a claim that II is worker-free.'),
'Q15':('All acquisition, placement, duplicate, bonus, partner-cap and university-reputation/hand-limit issues resolve correctly.','Printed university reputation is naturally granted on acquiring it in this acquisition answer. Partner icon and three-per-icon discount are accurate extra context.'),
'Q16':('Partial: omits placing the new project leftmost above the board and shifting old ones right, and omits receiving marked recurring uncovered map bonuses again at breaks.','Correct occupied-level and per-player limits, immediate support, origins, immediate bonuses and overflow/token destination. Player-count limit and retained activation are supported extra context; neither supplies the missing recurring payment rule.'),
'Q17':('Correct printed size bands, loss/retention, mandatory special-token priority and all standard fallbacks.','Printed-requirement basis excludes actual enclosure/capacity; First lose states the loss precedes the reward. Extra new-project reputation versus later support is correct. No demand to volunteer flock-specific repetition here.'),
'Q18':('Correct Sponsor budgets, source/cost, sequential effects and full money despite short Break movement.','No demand to restate display-refill or upgrade-conditioned Sponsor permission. After-finishing is deferred until completion.'),
'Q19':('Complete ordered break procedure, hand limit, qualifying kiosk neighbors and combined income order/refill.','Eligible restocking is supported. Detailed composition of other income and one-per-kind restock exceptions are unasked context.'),
'Q20':('All milestone choices, trigger checks/final turns, scoring cap/formula and tiebreak resolve correctly.','Facedown discard destination and no-ten fallback are accurate volunteered facts. The exact Bonus-tile removal procedure is unasked.'),
'Q21':('Complete random tile setup and exhausted-component substitution rule.','Two tiles beside each milestone and preserving explicit per-zoo/availability constraints are accurate.'),
'Q22':('Both advanced-map selection methods and Map A starting enclosure/kiosk are correct.','Returning maps and putting a reminder tile on the already-built kiosk are accurate.'),
'Q23':('Correct token starting location, worker hiring order and possible last-worker conservation reward.','Immediate/recurring support bonuses are accurately volunteered; no reward amount is invented.'),
'Q24':('Correct flip, stationary slot, next-action usability, immediate condition status and inability to upgrade all five.','The alternative upgrade source is accurate context; it is not a full enumeration and the question did not ask for one.'),
'Q25':('All five draw/discard pairs and both permitted discard sources are correct.','The 5+ extension is also supported by the capped table.'),
'Q28':('All seven categories and inclusion of bear/Petting Zoo are correct; naming Petting Zoo as a category resolves its independent category status.','The scope index\'s bear-co-occurrence/nonreplacement fact is extra context beyond this question and is not imposed as a hidden demand.'),
'Q29':('All donation conditions, entire ladder, blocked-space exclusion, source, reward and repeatable final space are correct.','Same-action task prerequisite is explicit and no separate worker is required.'),
'Q30':('Correct counting sources/exclusions, self-counting, doubles and card priority.','Double icons count twice is applied within the immediately preceding for-its-effects context and entails matching repeated triggers; no separate unasked example needed.'),
'Q31':('Distinct actual adjacency, nonmultiplication, region restriction and decorative-art exclusion are all correct.','No claim that connected terrain remotely supplies adjacency.'),
'Q32':('Correct Release play-only reputation and identical-condition free choice for Breeding Programs.','Normal unoccupied-space condition is accurately retained.'),
'Q33':('All syntax cases and X/Y roles are correct.','No additional ruling.'),
'Q34':('All five definitions match the frozen glossary.','No additional ruling.'),
'Q35':('Complete unique-building payment/placement/orientation/housing/terrain rules and unplayability if no legal site.','The matching tile, timing and terrain adjacency are supported.'),
'Q36':('Complete action timing and movement, named-action restriction and Determination X alternative.','Use normally is a meaningful defined procedure, not a missing restatement of every action rule.'),
'Q37':('Correct deck sources, named-project no-effect case, and later Association placement above the board.','Adding to hand and immediately supporting later play are accurate; returning the searched deck is unasked context.'),
'Q38':('Complete timing, allowed destinations and shift directions.','The moving-to-1 shift stated for Clever is the same movement operation used by Boost to 1; no contrary shift is asserted.'),
'Q39':('All asked threshold, acting-appeal timing and multiplayer alternative issues are correct.','The volunteered Pilfering sketch names the highest-appeal target shared by both Pilfering versions; it does not say only that target or deny the extra Pilfering-2 conservation target. It is incomplete extra context rather than a false exclusive rule. Other target sketches are supported.'),
'Q40':('Correct Constriction placement/nonstacking, minus-two strength per execution, X restoration and expiry.','Ahead-on-one/both target context is accurate.'),
'Q41':('Correct nonpositive regular strength, boosting/waiting and X alternative.','Five-X holding restriction is accurate extra context.'),
'Q42':('Correct renewed choice and immediate display replacement/shift/folder-six draw.','Digging 2 can change choices; accurate specific example.'),
'Q43':('All host, repetition, later-sharing and release-history issues are correct.','Release/fallback procedure is meaningful shorthand in a question about historical accommodation, not a demand for a verbatim release algorithm.'),
'Q44':('All Full-throated hiring, immediate usability, reward and no-effect cases resolve correctly.','No extra ruling.'),
'Q45':('Correctly discards all and takes none under the condition given in the question.','No need to restate the entire Hunter procedure.'),
'Q46':('Every requested Hypnosis issue is correct.','Target slots 1–3 and use of own cards for other upgrade checks are accurate extra details.'),
'Q49':('Complete Multiplier placement, sequential execution/strength/movement, X/effect timing, break delay and return/expiry.','Describing next use as executing twice states the double-execution procedure, not a claim forbidding a declined optional execution. No demand to volunteer different options.'),
'Q50':('Correct three-execution total, multiplied X alternative and mixing prohibition.','Two-X example obeys stated cap.'),
'Q51':('Complete Peacocking exception and retained site/limit/map restrictions, plus sequential Posturing placement.','Normal placement is explicitly retained and kiosk spacing named.'),
'Q52':('All appeal steps, three-animal limit and small-animal status are correct.','Single-Petting-Zoo context is supported.'),
'Q53':('All asked Pilfering tie, conservation-minimum and self-target rules are correct.','Separate Pilfering-2 targeting and twice when same zoo are accurate volunteered context.'),
'Q54':('Complete payment choice, allowed random cards, forced/fallback payments and sequential fresh choices.','Final Scoring cards explicitly excluded.'),
'Q55':('Correct Pouch-card inactivity/release disposition/retained appeal and Sunbathing discard.','Two appeal per tucked card and four money per sold card are supported extra amounts.'),
'Q56':('Correct extra-card choice at milestone and scoring all remaining cards with individual caps.','The question supplies Resistance; an extra card drawn in this answer naturally describes that ability\'s grant.'),
'Q57':('Correct random face-down shuffle/draw and restoring face-up pile.','The extra Scavenging-3 example matches the summary exactly.'),
'Q58':('Complete source, reputation, unavailable-Sponsor and refill distinctions.','No unsupported empty-deck workaround.'),
'Q59':('Every Venom placement, use, fee, rollback and expiry issue is correct.','X alternative below cap and inability to avoid fee by spending money are supported extra rulings.'),
'Q63':('All university-money tiers, conservation-strength reduction and final condition correct.','No extra ruling.'),
'Q66':('Correct support counting by missing tokens, two appeal per support and one conservation per break.','No extra ruling.'),
'Q67':('Correct distinct icon pool, complete-pair reward and other-player payment.','Per pair of different icons means complete pairs of the distinct pool; research is expressly excluded. No fractional rounding claim.'),
'Q68':('Correct play reward, any-player trigger with owner as payee and final diversity condition.','Own-zoo default is preserved by the Sponsor effect context; only the recurring effect is broadened to any player.'),
'Q70':('Correct play reward, free kiosk trigger/restrictions and final five-kiosk condition.','Later describes continuing plays, not an express denial of any self-trigger if a matching icon exists. The supplied summary does not identify this card\'s own printed icon, so no contrary self-trigger fact is invented.'),
'Q72':('Correct immediate reward, per-new-icon hand tuck/appeal and inactivity of tucked cards.','Ordinary own-zoo effect scope is maintained; no any-zoo claim.'),
'Q75':('Complete two-token substitute storage/spend, qualifying row and final support count/reward.','One token as one icon in this substitute context does not restrict the permissible icon; exactly one and never both are explicit.'),
'Q77':('All Engineer requirements and final reward are correct.','The retained one-per-type special limit entails no duplicate special enclosure.'),
'Q78':('Correct immediate payment, terrain permission/waiver, preserved icons, covered-terrain effects and scoring cap.','Terrain need not be covered for completion is accurate extra context.'),
'Q80':('Correct actual-border-bonus trigger, any uncovered copy choice, repeat choices and final condition.','Chosen resolution order is accurate extra context.'),
'Q82':('All immediate, extra-conservation, repeated/per-action support and support-count rules correct.','No demand to repeat general X cap.'),
'Q83':('All reward, four immunities, next-target redirection and final continent condition correct.','Choose/find next qualifying means search after ignoring owner counters; no arbitrary next clockwise target is asserted.'),
'Q85':('Complete permanent choice/search, opposite-type prohibition and small/large/size-three rewards.','Does not need to redefine small/large because question asks their rewards and the rules define those types.'),
'Q86':('Correct immediate money, all-small original-action gate, optional extra hand animal and display take.','Refill at turn end is supported extra context; no permission for mixed actions is introduced.'),
'Q90':('Correct play reward, per-covered-hex money with no multiplied water-neighbor pay, and final condition.','Connected is an expressly defined game term: uncovered and beside a covered space. Together with none isolated it does not mean water forms one connected water region.'),
'Q95':('Correct unique-building placement and two-deck-card keep/discard effect.','Own-zoo trigger default is preserved by context; no any-zoo claim or special placement exception is volunteered.'),
'Q96':('Correct water adjacency and optional two-card sales at four money with discard.','Own-zoo trigger default is preserved by context.'),
'Q98':('Correct current-total Hunter X and two sequential double-icon triggers.','Current total in clause 1 includes both icons now on the newly played card for the first Hunter, so naming both again for the second is sufficient by ordinary entailment. No need to repeat Hunter internals or building placement.'),
'Q99':('Correct three supply-token uses, herbivore trigger, hand-only source, money cost/conditions and self-trigger.','Stable enters with three supply tokens is meaningful card-storage shorthand; it does not put them in general supply or on the building.'),
'Q100':('All track rewards, two-border placement and two card-taking choices correct.','The stated chosen ordering of simultaneous benefits qualifies Then; no mandatory reward order is imposed.'),
'Q102':('Correct two-border/no-adjacency placement, later attachment, neighboring-building income and final reward.','May cover two border spaces is read as permission to place the Sponsor building at that described site, not permission to ignore border placement. Other unchanged ordinary placement rules are unasked context; see scope concern.'),
'Q104':('All immediate eligible spaces, terrain/upgrade distinctions and separate-group scoring correct.','Defined connected/uncovered vocabulary is sufficient. No need for an unasked numerical example.'),
'Q106':('Complete distinct-category/continent immediate money, new-icon reward and double-identical novelty rule.','Research excluded; category types need not be re-enumerated.'),
'Q107':('Complete free-building and large-animal left-condition waiver, terrain exception and two-condition stacking.','One left-side condition includes required icons and upgrade symbols without naming examples; Research Institute stacking assumes its usual activated function, not free activation.'),
'Q112':('Complete category comparisons, zero-opponent case and four-point cap.','No need to enumerate unasked normal icon sources/category inclusions.'),
'Q113':('All adjacency, enclosure eligibility, renewed appeal and nonbuilding issues correct.','Two appeal is accurate.'),
'Q114':('All qualifying adjacency, increased size/all purposes, mandatory release/transfer treatment and exclusions correct.','Physical size-2 treated as 4 is an accurate example.'),
'Q115':('Complete activation/first placement, own-turn ability timing/frequency and nonbuilding status.','Break and other-turn exclusions explicit.'),
'Q116':('All covered-hex income distinctions, kiosk exclusion and precise one-special free bonus correct.','Per adjacent covered hex encompasses all building types and both occupancy states; empty enclosures explicitly included.'),
'Q119':('Complete H-space procedure/nonbonus status, three-H discount and retained upgrade restrictions.','General upgrade-marked-space rule plus even-for-bonus-buildings does not exempt Sponsor buildings.'),
'Q123':('All money, conditions, hand-only and stationary-Action-card rules correct.','Sponsors II expressly does not allow display for this bonus.'),
'Q124':('Both exact caps and lost overflow are correct.','No invented conversion.'),
'Q125':('Complete target comparison, tie/self rules, slots and Constriction quantities.','Separate resolution entails twice for one zoo leading both. Qualifying retains the expressly introduced five-appeal eligibility. Slots 5 and 4 respectively is read cumulatively: first token 5, additional token 4; it does not explicitly stack both tokens on 4. This is terse and borderline wording, recorded below.'),
'Q127':('Every condition type/threshold and one-left-condition versus terrain distinction correct.','The appeal-25 marker is accurately identified as a reminder rather than global cap.'),
'Q133':('Both actual Digging choices and up-to-two count correct.','Changing options for second selection is supported extra context.'),
'Q134':('Correct compaction direction, preserved relative order and deck refill.','Extra immediate Digging replacement/folder-six context is accurate.'),
'Q137':('Correct empty-side identification and each-bonus immediate once-only receipt.','Explicitly denies repeating placement bonus on later occupancy; no need to volunteer multiple-building sequence.'),
'Q139':('Correct under-pile destination and facedown orientation under the question\'s given milestone.','Repeating the first-to-ten event and each-player discard is supported.'),
'Q140':('Correct random start, clockwise no-round sequence and one ordinary action with effect-defined additions.','As specified by the effect preserves additional effect timing without requiring all possible bonus procedures.'),
'Q141':('Correct all-player single discard before end-game scoring under the supplied no-player-reaches-ten condition.','Must discard one allows selection; no demand to repeat destination/orientation, Resistance, or individual scoring cap.')
}
# Scope follows actual wording; these three index additions are not hidden demands.
EXCLUSIONS={
 ('Q14',7): 'Actual wording asks worker requirements when repeating a task. The baseline one-active-worker-per-II-task rule is accurate context, but it is not a separate requested baseline-worker question. The answer correctly gives the escalation and lockout.',
 ('Q28',3): 'The question asks which categories count, including bear/Petting Zoo. Whether a bear icon co-occurs with a herbivore/predator icon is additional source context; listing every independent category answers the category question.',
 ('Q102',2): 'The question requests the Side Entrance placement exception, not a recital that every unchanged ordinary placement rule remains in force. The absence of an explicit all-other-rules sentence is not a false exception.'
}
ENTAILMENTS={
 ('Q03',3): 'Moving only the old slots left of slot 4 leaves slot 5 unchanged.',
 ('Q06',2): 'Draw by the Cards I draw table is meaningful shorthand for that defined deck-draw procedure.',
 ('Q06',7): 'The express restriction-only-on-II-draw statement excludes the restriction from either side\'s snap; a snap is instead of a draw.',
 ('Q10',3): 'Resolve items one at a time together with ordinary effects immediately places those effects before the next item.',
 ('Q11',2): 'Pay cost in step 1, before the ordinary play effects in step 4, so that item\'s later gain cannot pay its cost.',
 ('Q11',3): 'Three per matching continent icon gives six for two matching icons by ordinary arithmetic.',
 ('Q15',8): 'Within an acquisition answer, universities grant their printed reputation describes taking that printed reputation on acquisition.',
 ('Q17',2): 'Basing the category on the printed standard-enclosure requirement rules out the physical enclosure and alternative capacity as its basis.',
 ('Q17',3): 'First lose printed appeal states the loss precedes the project reward, without altering retained earlier effects.',
 ('Q28',4): 'The independent seven-category list expressly includes Petting Zoo animal as one of its categories.',
 ('Q30',5): 'For its effects is unqualified and therefore includes both instant and recurring effects.',
 ('Q30',6): 'Double icons count twice within the effects context means matching effects count each icon, including two matching triggers.',
 ('Q38',4): 'The clause describes moving a chosen card to 1 and its shift; Boost choosing 1 performs that same movement.',
 ('Q56',1): 'The question supplies Resistance as the ability; the answer\'s extra Final Scoring card is that ability\'s grant, not an unrelated source.',
 ('Q67',1): 'Different continent or category icons specifies the distinct pool, so copies are not new different icons.',
 ('Q67',2): 'One per pair specifies one reward for each complete two-icon pair.',
 ('Q68',1): 'Ordinary Sponsor-count context uses the owner\'s zoo; broad any-player scope is separately and expressly specified for the recurring trigger.',
 ('Q70',1): 'Ordinary Sponsor-count context uses the owner\'s zoo.',
 ('Q72',1): 'Ordinary Sponsor-count context uses the owner\'s zoo.',
 ('Q72',2): 'Ordinary Sponsor recurring-trigger context uses the owner\'s zoo.',
 ('Q75',2): 'A single token used as one icon in an unrestricted substitute rule can stand for any one needed icon.',
 ('Q77',5): 'The retained one-per-type special limit prevents building another copy of the special already built in that Build action.',
 ('Q90',5): 'Connected and isolated are explicitly defined in the supplied summary; the answer applies those definitions rather than asserting a water-region connectivity rule.',
 ('Q95',2): 'The own-zoo default governs the Sponsor trigger; no any-zoo exception is asserted.',
 ('Q96',2): 'The own-zoo default governs the Sponsor trigger; no any-zoo exception is asserted.',
 ('Q98',3): 'The first sentence uses the current total Predator icons; after a double-icon card is played both icons are in that total for the first Hunter as well as the explicitly mentioned second.',
 ('Q99',1): 'Stable enters play with three supply tokens is meaningful named-card storage shorthand; it does not relocate those tokens elsewhere.',
 ('Q102',1): 'The legal placement described is on two border spaces without existing-building adjacency. May expresses permission for that described placement, not another off-border placement.',
 ('Q107',2): 'One left-side condition is unrestricted among left-side conditions, including required icons and Animals upgrade.',
 ('Q107',4): 'Stacks with Research Institute uses that building\'s defined active waiver; it does not grant unactivated Institute use.',
 ('Q116',2): 'One money per adjacent covered hex, with empty enclosures explicit, covers all building types/occupancy without a building-type exclusion.',
 ('Q119',6): 'Upgrade-marked spaces require Build II is general, and even for bonus buildings adds no Sponsor exemption.',
 ('Q125',6): 'Resolving appeal and conservation targets separately makes one zoo qualifying for both receive two resolutions.',
 ('Q125',11): 'Qualifying refers to the eligibility just introduced as the five-appeal floor; no later target group is exempted.',
 ('Q140',5): 'As specified by the effect preserves each effect\'s own timing; the question does not require enumerating every bonus.',
 ('Q141',1): 'Discard one of the player\'s Final Scoring cards leaves its selection to that player; choose need not be a separate verb.'
}
ISSUES={
 ('Q11',9):('ambiguous', 'Terrain adjacency is attached to the standard-housing discussion. The special-housing clause specifies capacity but never confirms that the special must also meet water/rock requirements. Cannot import the explicit statement from Q13.'),
 ('Q16',3):('missing', 'Overflow rightmost discard does not specify placing the new card leftmost above the board or shifting all existing played projects right.'),
 ('Q16',10):('missing', 'Activated map bonuses remain activated does not explain that a recurring uncovered bonus is received again at each break.')
}
# Baseline workers on II are not an actually asked standalone part in Q14.
CONFIG=CONFIG.replace('Q14 P ', 'Q14 C ')
REVIEWS['Q14']=(
 'Correct task strengths, side-I/II limits, repeating-task worker escalation/lockout and ignoring opposing workers, which are the actual questions asked.',
 'Association I\'s normal active-worker need is accurately volunteered. The index adds a separate baseline-worker-per-II-task requirement beyond the prompt\'s repeating-task worker scope; it is flagged and excluded rather than silently imposed.'
)
PROMPT='''You are a fresh independent grader for Ark Nova's 95-question reader B. Read ONLY these six complete inputs under /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/ark-nova/2026-11-04-batch-231507/: expanded-iteration-05/reader-b.json, expanded-iteration-05/summary-snapshot.md, expanded-iteration-05/questions.json, benchmark-v3/answer-key.json, benchmark-v3/material-requested-facts.json, grading-request-scope-03.json. Do not read another reader, prior grades/reports/history, raw sources, canonical summary, or browse/contact anyone. Read all inputs completely in bounded chunks, recovering truncation. Independently grade ALL 95 answers and every ACTUALLY REQUESTED part. The actual question controls scope; factual keys stay fixed. The neutral scope index contains no prior answers/results. Accurate extra key context is not another demand; any volunteered false ruling still counts. Explicitly flag index/question inconsistencies rather than imposing hidden requirements. Correct requires complete actual requested parts, no contradiction and no unsupported source-correct guess. Partial means a missing, unresolved or ambiguous actual part. Incorrect means a material false or contradictory ruling, including volunteered claims. Do not borrow between answers. The support label is not the grade. Allow ordinary logical entailment and meaningful defined-procedure shorthand according to the prompt's scope; preserve conditions supplied by the question. Review every volunteered clause against this frozen summary. Write ONLY expanded-iteration-05/independent-grade-b.json and own notes named independent-grade-b-*. Include the exact intended prompt, six input hashes, complete-read proof, and 95 ordered judgments: id, each requested part with status, relevant observed clause quote and summary support quote/line, overallgrade correct|partial|incorrect, unsupported_guess boolean, reason and context/volunteered review. Quote relevant clauses rather than repeating whole answers for every part. Include C/P/I counts, nonpassing IDs and any borderline/key/scope concerns. No assumed PASS, no keyword grading, no relaxing genuine requested parts; do not edit inputs.'''

# Specific short quotes keep evidence about the requested clause rather than
# repeating complete multipoint answers for entailment-heavy parts.
OBSERVED_OVERRIDES={
 ('Q03',1):['put the used card in slot 1'],
 ('Q03',2):['shift the cards that were left of that empty slot one space right'],
 ('Q03',3):['shift the cards that were left of that empty slot one space right'],
 ('Q06',2):['draw the number shown for your slot strength (maximum 3, with any required discard)'],
 ('Q06',7):['A Cards II snap takes exactly 1 display card at strength 3 or more, does not include a deck draw, and is not reputation-restricted; the reputation restriction applies only to the Cards II draw option.'],
 ('Q10',3):['resolve items one at a time.', 'Ordinary effects resolve immediately'],
 ('Q11',2):["Check all left-side play conditions, then pay the Animal's printed cost", 'Resolve ordinary play effects immediately, including before playing a second animal'],
 ('Q11',3):['a matching-continent partner zoo reduces it by 3 money per matching continent icon on the card.'],
 ('Q11',4):['House it in an eligible empty standard enclosure of at least the required size'],
 ('Q11',5):['flipping that whole enclosure to occupied', 'Standard enclosures normally hold one animal'],
 ('Q11',6):['Petting Zoo animals go only in the Petting Zoo'],
 ('Q11',7):['eligible reptiles and birds may instead use the Reptile House or Large Bird Aviary if their indicated capacity fits'],
 ('Q11',8):['marking occupied spaces with supply player tokens and never flipping the special enclosure.'],
 ('Q11',9):['some animals also require distinct adjacent water/rock spaces.', 'eligible reptiles and birds may instead use the Reptile House or Large Bird Aviary if their indicated capacity fits'],
 ('Q16',3):['If a newly played project exceeds the player-count limit, discard the rightmost project'],
 ('Q16',10):['activated map bonuses remain activated.'],
 ('Q17',2):["A release project's size category is based on the animal's printed standard-enclosure requirement"],
 ('Q28',4):['Petting Zoo animal.'],
 ('Q30',5):['A card counts its own icons for its effects'],
 ('Q30',6):['double icons count twice.'],
 ('Q38',4):['Clever puts the chosen Action card into slot 1; cards formerly to its left shift right.', 'Boost puts the named card into slot 1 or 5'],
 ('Q77',5):['special enclosures remain limited to one of each type.'],
 ('Q98',3):['the number of revealed cards equal to your total Predator icons.', "resolve two Hunters sequentially, counting both new icons when determining the second Hunter's draw count."],
 ('Q99',1):['Okapi Stable enters play with 3 supply tokens.'],
 ('Q119',6):['upgrade-marked spaces require Build II even for bonus buildings.'],
 ('Q125',6):['Pilfering 2 resolves the highest-Appeal and most-Conservation qualifying targets separately'],
 ('Q125',10):['one track gives 1 token, both gives 2'],
 ('Q125',11):['each such zoo must have at least 5 Appeal.', 'meeting the 5-Appeal floor', 'highest-Appeal and most-Conservation qualifying targets', 'every other qualifying zoo'],
 ('Q141',1):['all players must discard one Final Scoring card'],
 ('Q141',2):['before end-game scoring begins.']
}

def summary_ref(n):
 return {'path':paths[1], 'line':n, 'quote':lines[n-1]}

def points(answer):
 markers=list(re.finditer(r'(?:^|(?<=\.)\s+)(\d+)\.\s+',answer))
 return {int(m.group(1)):answer[m.end():markers[i+1].start() if i+1<len(markers) else len(answer)].strip() for i,m in enumerate(markers)}

judgments=[]
configs={}
for row in CONFIG.strip().splitlines():
 ident,grade,obs,sup=row.split()
 configs[ident]=(grade,obs.split(','),sup.split(','))
assert len(configs)==95==len(REVIEWS)
for q in qs:
 ident=q['id']; grade,obs,sup=configs[ident]; requested=sc[ident]['requested_parts']; ps=points(r[ident]['answer'])
 assert len(requested)==len(obs)==len(sup),(ident,len(requested),len(obs),len(sup))
 assert sc[ident]['question']==q['question']
 results=[]; exclusions=[]
 for i,(d,o,s) in enumerate(zip(requested,obs,sup),1):
  assert all(int(n) in ps for n in o.split('+')), (ident, i, ps, o)
  quote_parts=OBSERVED_OVERRIDES.get((ident,i), [ps[int(n)] for n in o.split('+')])
  assert all(t in r[ident]['answer'] for t in quote_parts), (ident,i,quote_parts)
  result={
   'scope_index_part':i, 'requested_part':d,
   'status':'resolved_entailment' if (ident,i) in ENTAILMENTS else 'resolved',
   'observed_clause_quotes':quote_parts,
   'summary_support':[summary_ref(int(n)) for n in s.split('+')]
  }
  if (ident,i) in EXCLUSIONS:
   result['status']='not_actually_requested';result['reason']=EXCLUSIONS[(ident,i)];exclusions.append(result);continue
  if (ident,i) in ISSUES:
   result['status'],result['reason']=ISSUES[(ident,i)]
   result['observed_clause_role']='nearest relevant clause; it does not resolve the omitted/ambiguous requirement'
  elif (ident,i) in ENTAILMENTS:result['reason']=ENTAILMENTS[(ident,i)]
  else:result['reason']='The quoted answer clause resolves this actual part and agrees with the quoted frozen-summary rule.'
  results.append(result)
 actual_issues=[x for x in results if x['status'] in ['missing','ambiguous','contradicted']]
 assert (grade=='P')==bool(actual_issues),(ident,grade,actual_issues)
 reason,review=REVIEWS[ident]
 item={'id':ident,'question':q['question'],'requested_parts':results,'overallgrade':{'C':'correct','P':'partial','I':'incorrect'}[grade], 'unsupported_guess':False, 'reason':reason,'context_volunteered_review':review}
 if exclusions:item['scope_index_exclusions']=exclusions
 judgments.append(item)
counts=collections.Counter(j['overallgrade'] for j in judgments)
assert len(judgments)==95
assert len({j['id'] for j in judgments})==95
# Confirm input immutability at output time.
for p,b in raw.items():assert (BASE/p).read_bytes()==b,p
result={
 'grader':'fresh independent grader B; expanded iteration 05',
 'intended_prompt_exact':PROMPT,
 'input_hashes':[{'path':p,'sha256':hashlib.sha256(raw[p]).hexdigest(),'bytes':len(raw[p]),'lines':len(raw[p].splitlines())} for p in paths],
 'complete_read_proof':{
  'method':'Frozen summary was displayed and read in complete bounded line ranges; all five JSON documents were parsed and every complete record was displayed/read in aligned batches. No other content inputs were opened. No browsing or source access. A parent-agent progress message reported my own findings; no other reader or grader results were received or used.',
  'summary_line_ranges':[[1,130],[131,250],[251,390],[391,520],[521,644]],
  'json_metadata':'Top-level metadata and reader inputs_read array were separately displayed. The initial metadata inspection accidentally expanded nested material/scope objects and was truncated; none of the truncated output was relied on as complete. All nested records were recovered by the aligned full-record batches below. All actual question texts match scope-index question texts.',
  'json_records_bounded_read':[
   {'ordinal_range':[start+1,min(start+8,95)],'ids':[x['id'] for x in qs[start:start+8]],'fields_read':['complete question object','complete reader answer object including support and evidence','complete answer-key object including references/facts','complete material-requested-facts object','complete neutral-scope object including given/unrequested context']}
   for start in range(0,95,8)
  ],
  'summary_references':'Later numbered excerpts selected evidence lines. A line-preview listing was itself truncated; original complete summary ranges already covered all lines, and preview middle 250–318 was recovered with a bounded numbered excerpt.',
  'counts_verified':{'questions':95,'reader_answers':95,'answer_key_answers':95,'material_fact_entries':95,'scope_entries':95,'ordered_judgments':95},
  'frozen_inputs_unchanged':True,
  'notes':'Labels supported were read but did not determine grades. Judgments/entailments/scope exclusions were individually chosen by semantic review, not keyword match. No information from one answer supplies a missing requested part of another.'
 },
 'counts':{'correct':counts['correct'],'partial':counts['partial'],'incorrect':counts['incorrect'],'C':counts['correct'],'P':counts['partial'],'I':counts['incorrect']},
 'nonpassing_ids':[j['id'] for j in judgments if j['overallgrade']!='correct'],
 'borderline_key_scope_concerns':[
  {'id':'Q11','kind':'actual-part ambiguity','decision':'partial','detail':'Standard-housing terrain statement and special-housing capacity permission do not explicitly resolve terrain at special housing. The key fixes terrain applicability; nothing in another answer may repair it.'},
  {'id':'Q14','kind':'index/question inconsistency','decision':'exclude scope-index part 7 as independent demand','detail':EXCLUSIONS[('Q14',7)]},
  {'id':'Q28','kind':'index/question inconsistency','decision':'exclude scope-index part 3 as independent demand','detail':EXCLUSIONS[('Q28',3)]},
  {'id':'Q102','kind':'index/question inconsistency','decision':'exclude scope-index part 2 as independent demand','detail':EXCLUSIONS[('Q102',2)]},
  {'id':'Q39','kind':'volunteered-context interpretation','decision':'correct','detail':'Pilfering does target the highest-appeal zoo in both versions. The sketch does not claim it has only that target, so do not turn unrequested omitted Pilfering-2 context into a contradictory exclusivity claim.'},
  {'id':'Q98','kind':'ordinary logical entailment','decision':'correct','detail':'Current total predator icons in clause 1 already includes both icons of a new double-predator card; the later second-Hunter clarification need not state first again.'},
  {'id':'Q102','kind':'permission phrasing','decision':'correct','detail':'May cover two border spaces describes the legal Sponsor placement; it does not affirm that covering fewer/no border spaces is legal.'},
  {'id':'Q125','kind':'terse volunteered placement wording','decision':'correct, borderline','detail':'Placed in slots 5 and 4 respectively is interpreted as first token on 5, added token on 4. It is not treated as an explicit assertion to stack two tokens on slot 4. The actually asked counts are fully resolved.'},
  {'id':'Q90','kind':'defined-term shorthand','decision':'correct','detail':'Connected and isolated invoke the frozen glossary definition (each uncovered terrain space beside covered space), not connected water region topology.'},
  {'id':'Q07','kind':'key extra context','decision':'not an additional demand','detail':'Immediate once-only reputation bonus timing in unchanged factual key is expressly unasked context.'},
  {'id':'Q141','kind':'given-condition scope','decision':'correct','detail':'Question supplies no-player-reaches-ten scenario; all-player single discard before scoring is complete. Selection is inherent in discard one, without an extra choose verb.'}
 ],
 'judgments':judgments
}
(OUT/'independent-grade-b.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'file':str(OUT/'independent-grade-b.json'),'counts':result['counts'],'nonpassing_ids':result['nonpassing_ids'],'parts':sum(len(x['requested_parts']) for x in judgments),'scope_index_exclusions':sum(len(x.get('scope_index_exclusions',[])) for x in judgments),'bytes':(OUT/'independent-grade-b.json').stat().st_size},indent=2))
