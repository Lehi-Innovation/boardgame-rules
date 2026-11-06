# Full-bank independent source/question scope challenge — v1

Reviewed **113 questions and all 919 current mandatory atoms**: **902 affirmed**, **17 with explicit findings**. No sample, readers, grades or summaries were used. The original two-question review remains unchanged.

One literal source error concerns the setup office-card destination. Three wording clarifications preserve genuinely asked source conditions/type/timing. Ten fully contextual atoms and three mixed atoms require scope correction. Most contextual facts are explicitly covered by other exact questions. **CG-01 flags ordinary Company expense funding/debit as a narrow meaningful coverage gap after moving the unasked Q100 Balance instruction to context.**

## Independence and staging

Source/question-only. No reader responses, grades, summaries, audit reports, canonical rules markdown, histories, runtime/status tools or neighboring QA artifacts were opened. Full allowed bank files were parsed for questions/answers/mandatory scope; incidental metadata was not treated as evidence. No desired score or reader outcome was supplied.

Exact-question decomposition was saved first. Then every current mandatory fact and fuller key answer was read, independently compared with original rules and allowed supplements, and accounted for individually below. Clear implications count; no answer from another question is imported to cure a response omission.

`full-bank-question-only-prereview.json` was saved before the full answer key and scope were opened. All five prior review artifacts are preserved byte for byte; see the new input-hash record. The prior Q041/Q100 judgments are incorporated without modifying their original files.

## Exact proposed corrections

Proposal version: `full-bank-source-asked-scope-v1`. These are recommendations only. Correct fuller expected answers may retain optional explanations; mandatory-scope corrections do not authorize changing any live artifact.

### FB-Q006-03 — contextual_only

Question: How is a Chairman elected, how does a deadlocked election resolve, and does the elected Chairman piece remain a tradable Company share?

Requested phrase: “How is a Chairman elected”

Before (atom 3): Former Chairman announces required pure-majority threshold

After mandatory scope: Move to optional context; no independent mandatory clause.

Source truth: **supported**. Evidence: R1175-1187.

Stating the more-than-half threshold, eligibility and first-to-support resolution answers the election rule. The separate administrative act of the former Chairman announcing that already-required threshold is not another material election requirement.

Coverage consequence: No meaningful distinct core-procedure gap: majority election and former-Chairman deadlock authority remain required in Q006. The announcement itself has no separate exact question.

### FB-Q007-12 — contextual_only

Question: Explain success-check results, payment, retries, catastrophic destinations and the restriction against dead actions.

Requested phrase: “catastrophic destinations”

Before (atom 12): Specific office exceptions override general catastrophe rules

After mandatory scope: Move to optional context; no independent mandatory clause.

Source truth: **supported**. Evidence: R1361-1365, R1708-1710.

The question requests general catastrophic destinations, not a generic warning that special rules can differ. This atom names no specific exception or destination and should not be separately mandatory. Specific named office exceptions must still be respected where applicable.

Coverage consequence: No distinct procedure is dropped by removing a generic qualification. Concrete Deploy/Administer/China exceptions remain directly asked in Q012/Q013/Q042.

### FB-Q014-09 — contextual_only

Question: If Company revenue cannot cover expenses, how do emergency loans work at and below max Debt, how does Standing change, and when are expectations and dividends checked?

Requested phrase: “how does Standing change”

Before (atom 9): Reaching failure ends game immediately

After mandatory scope: Move to optional context; no independent mandatory clause.

Source truth: **supported**. Evidence: R1900-1902, R836-847.

Immediate game end on reaching the failure space is true, but describes an endgame transition rather than a Standing change or the asked expense-shortfall procedure.

Coverage consequence: Covered explicitly by Q025: “When does the game end” and its mandatory ordinary failure atom. No core gap.

### FB-Q019-09 — requested_precision_clarification

Question: Explain firm trading strategy, when checks and order filling occur, initiative, capacity, repeat-filled revenue and firm value growth.

Requested phrase: “when checks and order filling occur”

Before (atom 9): Fill in initiative order after successful checks

After mandatory scope: After the President makes a successful Trade roll, fill orders in initiative order; if the President is vacant or does not trade, use the stated later fallback.

Source truth: **supported_in_context_but_incomplete_timing_wording**. Evidence: R2791-2809.

The ordinary filling gate is the President’s successful Trade roll, not merely the firm’s successful check at Presidency start. The existing atom is compatible in context but underspecifies the timing expressly asked. This retains a genuine requirement.

Coverage consequence: No new procedure or question is added: clarify the already-asked timing and retain the existing vacant/nontrading fallback atoms 14–15.

### FB-Q024-05 — source_error_requested_destination

Question: How does setup use extra player cards for five or six players, distribute holdings, award starting luxury points and build the London display?

Requested phrase: “distribute holdings”

Before (atom 5): Put office card and member in indicated office

After mandatory scope: Place a family member in the listed office and take the matching office card.

Source truth: **wrong_card_destination_as_written**. Evidence: R420-425.

The source says to place the family member on the office space and take the matching office card. The mandatory atom literally puts both card and member in the office, which is the wrong card destination.

Coverage consequence: Corrects the explicitly requested distribution of office holdings; no coverage loss or extra obligation.

### FB-Q034-03 — mixed_requested_and_contextual

Question: What can successful Special Envoys accomplish, can they repeat, and when may the Director transfer pieces?

Requested phrase: “What can successful Special Envoys accomplish”

Before (atom 3): China hired immediately by Chairman from any writer

After mandatory scope: Creating China triggers immediate hiring.

Source truth: **supported**. Evidence: R1423-1428, R1808-1811.

Immediate hiring is a substantive result of creating China. The separate hiring actor (Chairman) and candidate pool (any writer) answer how China is hired, which this question does not independently ask. Do not require those two details again under the accomplishments clause.

Coverage consequence: Q033 asks who hires China/candidates; Q041 asks how it is hired and retains Chairman/any-writer scope. Immediate hiring remains in Q034. No gap.

### FB-Q040-03 — contextual_only

Question: How many successes does a Governor need to build a Company ship, where is it during construction and where does it go? How are Governor regiments treated?

Requested phrase: “where is it during construction and where does it go”

Before (atom 3): Unfinished ship has no other effect

After mandatory scope: Move to optional context; no independent mandatory clause.

Source truth: **supported**. Evidence: R1753-1757.

No other effect is a true usability restriction, but the ship clauses ask success count and locations, not what an unfinished ship can do. A complete answer can give both build stages and destinations without this extra clause.

Coverage consequence: Explicitly covered by Q013’s broad Administer request and current atom 15, which includes partially built ship/no other effect. No gap.

### FB-Q041-05 — mixed_requested_and_contextual

Question: What creates China, how is it hired, what resources does its treasury hold, when does it act and what ships count Eastern?

Requested phrase: “what ships count Eastern”

Before (atom 5): Ships in China count Eastern for expenses, storms, events and laws

After mandatory scope: Ships in China count as Eastern sea-zone ships.

Source truth: **supported**. Evidence: R1812-1815.

Preserve the original independent two-question verdict: identity/Eastern treatment is asked; individually enumerating all four source purposes is not. A clear general equivalence conveys those applicable consequences.

Coverage consequence: Q045/Q086 directly ask storms, Q100 expenses, and Q041 retains general Eastern status. Events/laws applications remain part of that equivalence, without a separate per-purpose recital. Shipping destinations are now independently verifiable in Q009 and Q103.

### FB-Q044-07 — requested_precision_clarification

Question: What guaranteed revenue does Governor General earn before Govern checks? Explain unrest from sixes, failure and tax, options per region and success limit.

Requested phrase: “options per region”

Before (atom 7): Ship to any sea zone including China

After mandatory scope: Place a Company ship in any sea zone, including China.

Source truth: **supported_in_context_with_ship_type_implicit**. Evidence: R1870-1878.

The shipbuilding option creates a Company ship, not an arbitrary player-owned ship. The short current atom can be read correctly in context, but preserve the source type when stating the asked option.

Coverage consequence: Strengthens precision of the already-requested option; no new requirement or coverage loss.

### FB-Q068-02 — contextual_only

Question: How does emergency merger differ from a normal multi-firm merger and whose expenses must be paid?

Requested phrase: “How does emergency merger differ from a normal multi-firm merger”

Before (atom 2): Follow normal negotiated all-shareholder consent

After mandatory scope: Move to optional context; no independent mandatory clause.

Source truth: **supported**. Evidence: R2760-2762, R2852-2855.

All-shareholder consent is unchanged from a normal negotiated merger. The question asks differences and whose expenses must be paid, not a restatement of normal legality. The one-other-firm restriction and both expense obligations remain mandatory.

Coverage consequence: All-shareholder consent is explicitly requested under Q065 “What makes a merger legal” and its atom 1. No gap.

### FB-Q077-02 — contextual_only

Question: According to the verified designer ruling, does unrest increase a Foreign Invasion primary attack or its resulting tower strength? What happens to orders?

Requested phrase: “does unrest increase a Foreign Invasion primary attack or its resulting tower strength”

Before (atom 2): Primary strength is ordinary attack die

After mandatory scope: Move to optional context; no independent mandatory clause.

Source truth: **supported**. Evidence: R2303-2312, FOREIGN-DESIGNER.

No unrest contribution answers the primary-attack part. Requiring the base die formula as a separate fact demands an unasked explanation of how the attack is calculated.

Coverage consequence: Q054 explicitly asks to “calculate strength” and retains attack-die atoms 6–7. No gap.

### FB-Q077-03 — contextual_only

Question: According to the verified designer ruling, does unrest increase a Foreign Invasion primary attack or its resulting tower strength? What happens to orders?

Requested phrase: “does unrest increase a Foreign Invasion primary attack or its resulting tower strength”

Before (atom 3): Resulting tower strength is half die rounded down

After mandatory scope: Move to optional context; no independent mandatory clause.

Source truth: **supported**. Evidence: R2303-2312, FOREIGN-DESIGNER.

No unrest contribution also answers the resulting-tower part. Half-die rounded-down is the correct base formula but not a separate requested answer to whether unrest increases it.

Coverage consequence: Q054 asks tower changes and retains half-die rounded-down atom 14. No gap.

### FB-Q082-03 — contextual_only

Question: An empire loses its last dominated region while its capital remains. Does the capital keep its starred flag, and does the answer depend on whether the dominated region was lost to Rebellion or Company conquest?

Requested phrase: “Does the capital keep its starred flag”

Before (atom 3): Capital-only region ceases to be empire

After mandatory scope: Move to optional context; no independent mandatory clause.

Source truth: **supported**. Evidence: R707-714.

The question asks flag disposition and whether the cause matters. No/return the capital flag regardless of the two causes fully answers it. The source’s no-longer-an-empire label is a correct explanation rather than an additional requested assertion.

Coverage consequence: Capital-flag cleanup and both triggering causes remain required in Q082. No meaningful distinct procedure is lost: flag removal is the operational Empire Decline rule. The explanatory status label has no separate interrogative.

### FB-Q090-04 — requested_precision_clarification

Question: When a non-Company Rebellion succeeds, what happens to the rebel region’s sovereignty, flag and orders, including when every order there is already closed?

Requested phrase: “including when every order there is already closed”

Before (atom 4): Then perform Cascade

After mandatory scope: Perform a Cascade only if every order in the rebelling region was already closed.

Source truth: **supported_only_with_the_question_and_key_condition**. Evidence: R2216-2219.

The question and key supply the condition, so read the atom conditionally. Its standalone “Then” wording must not become an instruction to close open orders and also Cascade every time. This is a source-precision correction preserving the requested exception.

Coverage consequence: Restores an explicitly asked condition, rather than relaxing it. Q051/Q046 overlap but cannot substitute for answering Q090.

### FB-Q100-01 — contextual_only

Question: At the Company’s ordinary Revenue expense calculation, what costs £1 each, which military officeholder is excluded, and do ships assigned to China count?

Requested phrase: “At the Company’s ordinary Revenue expense calculation”

Before (atom 1): Ordinary expenses lower Company Balance

After mandatory scope: Move to optional context; no independent mandatory clause.

Source truth: **supported**. Evidence: R1903-1906.

Preserve the two-question verdict: this phrase identifies the setting. The actual interrogatives request cost categories/rates, Commander exclusion and China inclusion, not a separate Balance-marker instruction.

Coverage consequence: FLAG CG-01: no other exact bank question independently asks which account pays/decrements ordinary Company expenses. Q014 asks emergency shortfall handling; Q112 asks dividend funding. Removing this unasked separate atom exposes a narrow core funding/debit coverage gap; do not cure it by imposing it on Q100.

### FB-Q100-07 — mixed_requested_and_contextual

Question: At the Company’s ordinary Revenue expense calculation, what costs £1 each, which military officeholder is excluded, and do ships assigned to China count?

Requested phrase: “do ships assigned to China count”

Before (atom 7): China-assigned ships are included as Eastern sea-zone ships for expenses

After mandatory scope: China-assigned ships are included in those £1-per-ship expenses.

Source truth: **supported**. Evidence: R1812-1815, R1903-1906.

Inclusion at the stated £1 ship rate is required. Eastern classification is a correct explanation, not a separately necessary rationale for the yes/no answer. This preserves the existing independent review.

Coverage consequence: Q041 directly requests Eastern identity; Q100 retains cost/inclusion. No gap.

### FB-Q106-04 — contextual_only

Question: When an ordinary Invasion Crisis causes Company Region Loss, what happens to that region’s orders, including if all are already closed? Does Region Loss impose a second order-closing/Cascade step for a loss caused by Rebellion or Foreign Invasion?

Requested phrase: “Does Region Loss impose a second order-closing/Cascade step for a loss caused by Rebellion or Foreign Invasion”

Before (atom 4): Rebellion and Foreign Invasion already close orders by their own procedures

After mandatory scope: Move to optional context; no independent mandatory clause.

Source truth: **supported**. Evidence: R1999-2007, FOREIGN-DESIGNER.

The requested no-duplicate-step answer is already mandatory in atom 3. This extra atom explains why. The question does not independently ask the reason. A correct no with the right condition is sufficient.

Coverage consequence: The independent closing procedures are directly asked by Q090 for Rebellion and Q054/Q077 for Foreign Invasion; duplicate prevention remains required by Q106 atom 3. No gap.

## Coverage gap

**CG-01 — Ordinary Company expense funding/debit from Company Balance**

No other exact question independently asks which funds pay ordinary Company expenses or instructs the ordinary Balance debit. Q014 asks a revenue shortfall and emergency borrowing/Standing/sequence; Q112 explicitly asks dividend funding. Treating Q100’s unasked marker instruction as context therefore leaves a narrow but meaningful funding/debit procedure without an explicit interrogative. The expense census/rates remain fully tested.

Flag for future bank design; do not silently retain an unasked mandatory clause, alter a question, or pad with a recombination in this review.

## Complete 113-question / 919-atom accounting

Each row below cites the exact original question, a row-specific scope rationale and original-source registry IDs. Every current atom has a separate verdict. Shared IDs resolve to exact original quotations/pages/LF ranges in the appendix. Equivalent wording and clear implications satisfy overlapping atoms without a demand for repeated sentences.

### Q001 — 9 atoms; affirmed

During attrition, how does an office roll resolve, what extra modifier does the Chairman have, and where do a retiring member, card and fatigue go?

The roll, modifier, outcome thresholds and three retirement destinations directly answer the three interrogatives.

Original source evidence: R901-916.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q001.A01 | Roll separately for each office card | supported | affirmed_requested_or_clearly_implied | R901-916 |
| Q001.A02 | Add one per fatigue | supported | affirmed_requested_or_clearly_implied | R901-916 |
| Q001.A03 | Result 1–2 changes nothing | supported | affirmed_requested_or_clearly_implied | R901-916 |
| Q001.A04 | Result 3–4 adds fatigue | supported | affirmed_requested_or_clearly_implied | R901-916 |
| Q001.A05 | Result 5+ retires the member | supported | affirmed_requested_or_clearly_implied | R901-916 |
| Q001.A06 | Chairman adds an additional one | supported | affirmed_requested_or_clearly_implied | R901-916 |
| Q001.A07 | Member goes to Pensioners | supported | affirmed_requested_or_clearly_implied | R901-916 |
| Q001.A08 | Flip card into Vacant Offices | supported | affirmed_requested_or_clearly_implied | R901-916 |
| Q001.A09 | Return fatigue to supply | supported | affirmed_requested_or_clearly_implied | R901-916 |

### Q002 — 9 atoms; affirmed

Who may select London Season cards, in what order and with which tiebreakers? What happens to the display and unused pensioners afterward?

Eligibility includes ordinary pensioner and qualifying firm special retirements. Order, cash/windows/PM tiebreakers, display exhaustion/refill/orientation and unused pensioners are all expressly requested; peeking is contextual here and directly asked by Q094.

Original source evidence: R1002-1014, R2651-2658, R917-928.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q002.A01 | Each player completing at least one pensioner retirement or eligible firm special retirement must take or discard one display card | supported | affirmed_requested_or_clearly_implied | R1002-1014, R2651-2658, R917-928 |
| Q002.A02 | Players are skipped once the display is empty | supported | affirmed_requested_or_clearly_implied | R1002-1014, R2651-2658, R917-928 |
| Q002.A03 | Descending actual total retirement cash spent | supported | affirmed_requested_or_clearly_implied | R1002-1014, R2651-2658, R917-928 |
| Q002.A04 | First tie: most total windows | supported | affirmed_requested_or_clearly_implied | R1002-1014, R2651-2658, R917-928 |
| Q002.A05 | Next tie: clockwise starting with Prime Minister | supported | affirmed_requested_or_clearly_implied | R1002-1014, R2651-2658, R917-928 |
| Q002.A06 | Discard remaining display cards | supported | affirmed_requested_or_clearly_implied | R1002-1014, R2651-2658, R917-928 |
| Q002.A07 | Refill to three even if no cards were taken | supported | affirmed_requested_or_clearly_implied | R1002-1014, R2651-2658, R917-928 |
| Q002.A08 | Prestige faceup and blackmail facedown | supported | affirmed_requested_or_clearly_implied | R1002-1014, R2651-2658, R917-928 |
| Q002.A09 | Return unretired pensioners to their supplies | supported | affirmed_requested_or_clearly_implied | R1002-1014, R2651-2658, R917-928 |

Q002.A01: An eligible firm special retirement counts like a pensioner retirement. No need to repeat the full special-retirement eligibility procedure here.

Existing optional key context (not promoted to mandatory): Acting player may peek at display blackmail..

### Q003 — 8 atoms; affirmed

How do the opportunity marker and extra-action laws affect family actions? If four offices are vacant and the marker already sits on Enlist Writer, how many writers can be placed?

The question requests both marker/law mechanics and a numeric application. Once-per-turn vacancy extra cannot be doubled with the repeated action; three writers is required in the stated fixture.

Original source evidence: R1076-1104.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q003.A01 | Normal selected action once | supported | affirmed_requested_or_clearly_implied | R1076-1104 |
| Q003.A02 | Twice if opportunity marker was already there at phase start | supported | affirmed_requested_or_clearly_implied | R1076-1104 |
| Q003.A03 | Move marker to main selected action | supported | affirmed_requested_or_clearly_implied | R1076-1104 |
| Q003.A04 | Only latest passed extra-action law may be used | supported | affirmed_requested_or_clearly_implied | R1076-1104 |
| Q003.A05 | Extra law action receives no opportunity-marker doubling | supported | affirmed_requested_or_clearly_implied | R1076-1104 |
| Q003.A06 | Extra law action does not move opportunity marker | supported | affirmed_requested_or_clearly_implied | R1076-1104 |
| Q003.A07 | Four or more vacant offices allow one additional writer once per turn | supported | affirmed_requested_or_clearly_implied | R1076-1104 |
| Q003.A08 | Stated repeated-Enlist-Writer fixture places three writers total | supported | affirmed_requested_or_clearly_implied | R1076-1104 |

### Q004 — 6 atoms; affirmed

After Seek Share actions, how are new Company shares created and remaining applicants moved? Where was the initial purchase money paid?

New-share creation and leftover-applicant movement require rightmost-first, Debt reduction and preserved order. Purchase price itself is contextual because the final clause asks where the original money went.

Original source evidence: R1128-1145.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q004.A01 | After all Family actions, move rightmost applicant into Court | supported | affirmed_requested_or_clearly_implied | R1128-1145 |
| Q004.A02 | Issue only while both Debt and applicants remain | supported | affirmed_requested_or_clearly_implied | R1128-1145 |
| Q004.A03 | Each issued share reduces Debt by one | supported | affirmed_requested_or_clearly_implied | R1128-1145 |
| Q004.A04 | When no Debt remains slide remaining applicants as far right as possible | supported | affirmed_requested_or_clearly_implied | R1128-1145 |
| Q004.A05 | Preserve their order | supported | affirmed_requested_or_clearly_implied | R1128-1145 |
| Q004.A06 | Initial Seek Share purchase money goes to bank | supported | affirmed_requested_or_clearly_implied | R1128-1145 |

Existing optional key context (not promoted to mandatory): Seek Share pays printed empty-space price.; Purchase cash does not fund Company treasury..

### Q005 — 8 atoms; affirmed

When hiring, how are vacancies ordered, what consent does hiring your own family require, what happens to promoted fatigue, and what if no candidate or hirer exists?

Vacancy order, consent pool, promoted fatigue and vacancy fallbacks are explicit. The Chairman-election exception qualifies the requested consent rule.

Original source evidence: R1146-1169.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q005.A01 | Ascending office number on card backs | supported | affirmed_requested_or_clearly_implied | R1146-1169 |
| Q005.A02 | Insert promotion-created vacancies in that order | supported | affirmed_requested_or_clearly_implied | R1146-1169 |
| Q005.A03 | Verbal consent from every other family represented in candidate pool | supported | affirmed_requested_or_clearly_implied | R1146-1169 |
| Q005.A04 | Chairman election is exempt | supported | affirmed_requested_or_clearly_implied | R1146-1169 |
| Q005.A05 | Move fatigue to the new office card | supported | affirmed_requested_or_clearly_implied | R1146-1169 |
| Q005.A06 | Skip office if no candidate or hiring office is vacant | supported | affirmed_requested_or_clearly_implied | R1146-1169 |
| Q005.A07 | Office remains vacant | supported | affirmed_requested_or_clearly_implied | R1146-1169 |
| Q005.A08 | Vacant office takes no actions, including hiring | supported | affirmed_requested_or_clearly_implied | R1146-1169 |

### Q006 — 10 atoms; explicit_findings

How is a Chairman elected, how does a deadlocked election resolve, and does the elected Chairman piece remain a tradable Company share?

Eligibility, pure majority, first-to-support rule, deadlock choice and share representation/trade restriction are requested. Taking the title is clearly implied by being elected; a separate announcement by the former Chairman is administrative context.

Original source evidence: R1175-1190.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q006.A01 | Candidate owns a Company share | supported | affirmed_requested_or_clearly_implied | R1175-1190 |
| Q006.A02 | Consent must control more than half of current Company shares | supported | affirmed_requested_or_clearly_implied | R1175-1190 |
| Q006.A03 | Former Chairman announces required pure-majority threshold | supported | contextual_only | R1175-1187 / FB-Q006-03 |
| Q006.A04 | First candidate reaching required support is elected | supported | affirmed_requested_or_clearly_implied | R1175-1190 |
| Q006.A05 | Elected player takes Chairman title | supported | affirmed_requested_or_clearly_implied | R1175-1190 |
| Q006.A06 | Elected player moves own share into Chairman slot | supported | affirmed_requested_or_clearly_implied | R1175-1190 |
| Q006.A07 | Former Chairman chooses any shareholder, including self | supported | affirmed_requested_or_clearly_implied | R1175-1190 |
| Q006.A08 | Nepotism does not apply | supported | affirmed_requested_or_clearly_implied | R1175-1190 |
| Q006.A09 | Piece still counts as Company share | supported | affirmed_requested_or_clearly_implied | R1175-1190 |
| Q006.A10 | Piece cannot be traded | supported | affirmed_requested_or_clearly_implied | R1175-1190 |

Q006.A05: Being elected/becoming Chairman clearly implies taking the title; do not require a separate title sentence.

Existing optional key context (not promoted to mandatory): Chairman share cannot be invested in firm..

### Q007 — 13 atoms; explicit_findings

Explain success-check results, payment, retries, catastrophic destinations and the restriction against dead actions.

General check resources/payment, lowest-die thresholds, retries, catastrophe consequences/destinations and no-dead-action rule are requested. A generic disclaimer about special offices does not supply a requested destination.

Original source evidence: R1331-1365.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q007.A01 | Commit office resources | supported | affirmed_requested_or_clearly_implied | R1331-1365 |
| Q007.A02 | Office check cash is paid from office treasury to bank | supported | affirmed_requested_or_clearly_implied | R1331-1365 |
| Q007.A03 | Gather dice and subtract penalty | supported | affirmed_requested_or_clearly_implied | R1331-1365 |
| Q007.A04 | Lowest die 1–2 succeeds | supported | affirmed_requested_or_clearly_implied | R1331-1365 |
| Q007.A05 | Lowest die 3–4 fails | supported | affirmed_requested_or_clearly_implied | R1331-1365 |
| Q007.A06 | Failed check may be retried with sufficient resources | supported | affirmed_requested_or_clearly_implied | R1331-1365 |
| Q007.A07 | Lowest die 5–6 is catastrophe | supported | affirmed_requested_or_clearly_implied | R1331-1365 |
| Q007.A08 | Catastrophe ends further office actions | supported | affirmed_requested_or_clearly_implied | R1331-1365 |
| Q007.A09 | Return officeholder to family supply | supported | affirmed_requested_or_clearly_implied | R1331-1365 |
| Q007.A10 | Return fatigue to supply | supported | affirmed_requested_or_clearly_implied | R1331-1365 |
| Q007.A11 | Flip card into Vacant Offices | supported | affirmed_requested_or_clearly_implied | R1331-1365 |
| Q007.A12 | Specific office exceptions override general catastrophe rules | supported | contextual_only | R1361-1365, R1708-1710 / FB-Q007-12 |
| Q007.A13 | Cannot take action with neither effect nor chance of success | supported | affirmed_requested_or_clearly_implied | R1331-1365 |

### Q008 — 7 atoms; affirmed

What are the Chairman’s voluntary borrowing and allocation duties, including consent and track limits?

Borrowing amount/count, majority consent, Chairman share, Debt cap and complete allocation are substantive requested duties. Balance reduction follows the asked allocation operation, unlike unasked expense-marker mechanics in Q100.

Original source evidence: R1403-1416.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q008.A01 | Up to three Debt advances without consent | supported | affirmed_requested_or_clearly_implied | R1403-1416 |
| Q008.A02 | Each advance adds £5 Balance | supported | affirmed_requested_or_clearly_implied | R1403-1416 |
| Q008.A03 | Each further advance needs majority-shareholder consent | supported | affirmed_requested_or_clearly_implied | R1403-1416 |
| Q008.A04 | Chairman share counts toward that majority | supported | affirmed_requested_or_clearly_implied | R1403-1416 |
| Q008.A05 | Never advance beyond Debt track end | supported | affirmed_requested_or_clearly_implied | R1403-1416 |
| Q008.A06 | Allocate all Company Balance to other office treasuries | supported | affirmed_requested_or_clearly_implied | R1403-1416 |
| Q008.A07 | Reduce Balance by allocated amount | supported | affirmed_requested_or_clearly_implied | R1403-1416 |

Existing optional key context (not promoted to mandatory): Borrowing may interleave allocation within borrowing limits..

### Q009 — 8 atoms; affirmed

What must Shipping do with its budget? State ship costs, destinations, consent requirements and the prerequisite for buying Company ships.

Budget-spending obligation, each acquisition price, eligible destinations including China, owner consent and no-unfitted-ship prerequisite are all explicit requested categories.

Original source evidence: R1457-1471, R1812-1815.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q009.A01 | Spend until no more than £2 remains | supported | affirmed_requested_or_clearly_implied | R1457-1471, R1812-1815 |
| Q009.A02 | Lease extra ship for £2 | supported | affirmed_requested_or_clearly_implied | R1457-1471, R1812-1815 |
| Q009.A03 | Fit shipyard ship for £3 | supported | affirmed_requested_or_clearly_implied | R1457-1471, R1812-1815 |
| Q009.A04 | Fitting requires no owner consent | supported | affirmed_requested_or_clearly_implied | R1457-1471, R1812-1815 |
| Q009.A05 | Buy Company ship for £5 | supported | affirmed_requested_or_clearly_implied | R1457-1471, R1812-1815 |
| Q009.A06 | Acquired ships go to any eligible sea zone | supported | affirmed_requested_or_clearly_implied | R1457-1471, R1812-1815 |
| Q009.A07 | China is an eligible sea-zone destination once created | supported | affirmed_requested_or_clearly_implied | R1457-1471, R1812-1815 |
| Q009.A08 | No ships may remain on any shipyard | supported | affirmed_requested_or_clearly_implied | R1457-1471, R1812-1815 |

Q009.A08: The no-unfitted-ships prerequisite applies to Company-ship buying, not all Shipping acquisitions.

Existing optional key context (not promoted to mandatory): Extra ships return at Refresh.; Shipping acquisition cash goes to bank..

### Q010 — 12 atoms; affirmed

For a President’s Trade action, explain declared regions, dice penalty, routes and capacity, insufficient writers, protected home regions, bonuses and successful-trade limit.

The enumerated Trade subjects require reachability, penalties, capacity/route, insufficient writers, protected homes, personal bonuses and success limit. General Trade revenue/rate have their own exact questions Q097; no imported answer is needed for this response.

Original source evidence: R1540-1582.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q010.A01 | Declare own home region | supported | affirmed_requested_or_clearly_implied | R1540-1582 |
| Q010.A02 | Declare only additional regions actually reachable through open route with sufficient ships | supported | affirmed_requested_or_clearly_implied | R1540-1582 |
| Q010.A03 | Subtract one die per declared nonhome region | supported | affirmed_requested_or_clearly_implied | R1540-1582 |
| Q010.A04 | After success fill as many declared-region orders as possible | supported | affirmed_requested_or_clearly_implied | R1540-1582 |
| Q010.A05 | Capacity is one order per ship | supported | affirmed_requested_or_clearly_implied | R1540-1582 |
| Q010.A06 | Start at home port | supported | affirmed_requested_or_clearly_implied | R1540-1582 |
| Q010.A07 | Continue through adjacency to own placed writers | supported | affirmed_requested_or_clearly_implied | R1540-1582 |
| Q010.A08 | Use filled tokens when writers run out | supported | affirmed_requested_or_clearly_implied | R1540-1582 |
| Q010.A09 | Cannot fill another Presidency home region even if its President is vacant | supported | affirmed_requested_or_clearly_implied | R1540-1582 |
| Q010.A10 | President receives £1 per filled order | supported | affirmed_requested_or_clearly_implied | R1540-1582 |
| Q010.A11 | Writer owner receives £1 per writer placed | supported | affirmed_requested_or_clearly_implied | R1540-1582 |
| Q010.A12 | At most one successful Trade per President per turn | supported | affirmed_requested_or_clearly_implied | R1540-1582 |

Existing optional key context (not promoted to mandatory): Trade costs £1 Presidency treasury per die.; Company earns listed order revenue.; Company filling previously firm-filled orders earns half listed revenue rounded down, with normal personal bonuses..

### Q011 — 13 atoms; affirmed

What can a Commander target with Deploy, what produces dice and penalties, and when and how are officer losses checked?

Target eligibility/exclusions, active-resource dice, empire penalty and loss-check timing/owner/destination are all requested. Counting the target once follows combined-empire strength rather than adding it twice.

Original source evidence: R1617-1650, R707-711, R1651-1666.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q011.A01 | Home region eligible | supported | affirmed_requested_or_clearly_implied | R1617-1650, R707-711, R1651-1666 |
| Q011.A02 | Associated regions eligible | supported | affirmed_requested_or_clearly_implied | R1617-1650, R707-711, R1651-1666 |
| Q011.A03 | Regions bordering associated regions eligible | supported | affirmed_requested_or_clearly_implied | R1617-1650, R707-711, R1651-1666 |
| Q011.A04 | Another Presidency home excluded | supported | affirmed_requested_or_clearly_implied | R1617-1650, R707-711, R1651-1666 |
| Q011.A05 | Another Presidency Company-controlled region excluded | supported | affirmed_requested_or_clearly_implied | R1617-1650, R707-711, R1651-1666 |
| Q011.A06 | Own Company-controlled target needs closed order or unrest | supported | affirmed_requested_or_clearly_implied | R1617-1650, R707-711, R1651-1666 |
| Q011.A07 | Exhaust active officers and regiments for one die each | supported | affirmed_requested_or_clearly_implied | R1617-1650, R707-711, R1651-1666 |
| Q011.A08 | Exhausted alliance provides printed strength in dice | supported | affirmed_requested_or_clearly_implied | R1617-1650, R707-711, R1651-1666 |
| Q011.A09 | Subtract target and all other empire-region strengths, counting target once | supported_by_clear_rule_implication | affirmed_requested_or_clearly_implied | R1617-1650, R707-711, R1651-1666 |
| Q011.A10 | Company-controlled defending strength is zero | supported | affirmed_requested_or_clearly_implied | R1617-1650, R707-711, R1651-1666 |
| Q011.A11 | After every attempt, including catastrophe, roll per exhausted officer | supported | affirmed_requested_or_clearly_implied | R1617-1650, R707-711, R1651-1666 |
| Q011.A12 | Each six removes one officer of that owner to supply | supported | affirmed_requested_or_clearly_implied | R1617-1650, R707-711, R1651-1666 |
| Q011.A13 | Regiments never take officer-loss checks | supported | affirmed_requested_or_clearly_implied | R1617-1650, R707-711, R1651-1666 |

Q011.A09: Total target empire strength counts the target once. The original example and empire definition resolve the terse additive wording; do not double-count it.

### Q012 — 15 atoms; affirmed

On successful Deploy how are loot and trophies calculated and control imposed? What changes if Deploy catastrophically fails?

Loot and trophy calculation, control/overlay/card destinations and catastrophe changes are requested. Distribution and Elephant redirect are contextual to this wording and independently asked by Q098/Q099.

Original source evidence: R1648-1650, R1674-1710.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q012.A01 | Loot is £4 per target tower level | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A02 | Add faceup loot modifier | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A03 | Minimum loot equals surviving participating officers plus one | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A04 | Commander gains one trophy per target tower level | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A05 | Remove target tower and dome | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A06 | If target was capital remove all matching flags | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A07 | Open all orders | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A08 | Clear unrest | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A09 | Newly conquered region control token moves region-side up above associated President | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A10 | Put Governor overlay in region | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A11 | Put Governor office card in Vacant Offices | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A12 | New region is Company-controlled and associated with that Presidency | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A13 | Return half family trophies rounded up | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A14 | Return Commander to supply | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |
| Q012.A15 | Still perform exhausted-officer loss checks | supported | affirmed_requested_or_clearly_implied | R1648-1650, R1674-1710 |

Existing optional key context (not promoted to mandatory): Loot distributed in repeated rounds: Commander £1 and own surviving officers £1 each, clockwise other officers, then bank £1 per regiment/alliance piece.; Outward-facing Elephant in conquered region redirects inward..

### Q013 — 16 atoms; affirmed

How does Governor Administer work across repeated attempts, including bonuses, tax unrest and stopping?

How Administer works across repeated attempts is a broad procedural request: dice depletion, success options including both construction stages, personal bonus, tax/failure unrest and stop/catastrophe conditions all belong.

Original source evidence: R1742-1771, R1361-1365.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q013.A01 | Start with printed dice pool | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A02 | No dice penalty | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A03 | Remove one die after every attempt | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A04 | Each success chooses a benefit | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A05 | Ship construction requires two build successes | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A06 | Regiment goes to associated Army | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A07 | Tax benefit is unsplit £2 to Balance or associated President treasury | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A08 | Success pays Governor personal £1 | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A09 | Add £1 if preceding attempt was unsuccessful | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A10 | Each tax after first this turn adds local unrest | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A11 | Each unsuccessful check adds local unrest | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A12 | May choose to stop | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A13 | Stop when dice pool exhausted | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A14 | Catastrophe stops action and causes general office vacancy | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A15 | On a successful ship-build choice, if no Company ship is already in the region, place a partially built Company ship there with no other effect | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |
| Q013.A16 | On a successful ship-build choice with a Company ship already in the region, move that ship to the associated Presidency sea zone | supported | affirmed_requested_or_clearly_implied | R1742-1771, R1361-1365 |

### Q014 — 13 atoms; explicit_findings

If Company revenue cannot cover expenses, how do emergency loans work at and below max Debt, how does Standing change, and when are expectations and dividends checked?

The question requests emergency borrowing, Standing changes and the sequence of expectations/dividends. The broad Standing clause supports expectation and enthusiasm effects; separate immediate game-ending consequences are contextual and asked by Q025.

Original source evidence: R1897-1934.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q014.A01 | Borrow compulsorily until expenses covered | supported | affirmed_requested_or_clearly_implied | R1897-1934 |
| Q014.A02 | Each emergency loan supplies £5 | supported | affirmed_requested_or_clearly_implied | R1897-1934 |
| Q014.A03 | Advance Debt if possible | supported | affirmed_requested_or_clearly_implied | R1897-1934 |
| Q014.A04 | At maximum continue borrowing without Debt advance | supported | affirmed_requested_or_clearly_implied | R1897-1934 |
| Q014.A05 | Newly added emergency Debt creates no current-turn interest | supported | affirmed_requested_or_clearly_implied | R1897-1934 |
| Q014.A06 | Then set Balance to zero | supported | affirmed_requested_or_clearly_implied | R1897-1934 |
| Q014.A07 | One or two loans lose one Standing | supported | affirmed_requested_or_clearly_implied | R1897-1934 |
| Q014.A08 | Three or more lose two Standing | supported | affirmed_requested_or_clearly_implied | R1897-1934 |
| Q014.A09 | Reaching failure ends game immediately | supported | contextual_only | R1900-1902, R836-847 / FB-Q014-09 |
| Q014.A10 | After expenses and embarrassment compare Balance to current-Standing expectations | supported | affirmed_requested_or_clearly_implied | R1897-1934 |
| Q014.A11 | Below expectations loses one Standing | supported | affirmed_requested_or_clearly_implied | R1897-1934 |
| Q014.A12 | Then Chairman may pay dividends | supported | affirmed_requested_or_clearly_implied | R1897-1934 |
| Q014.A13 | Total dividend payout strictly greater than expectations improves Standing once | supported | affirmed_requested_or_clearly_implied | R1897-1934 |

Q014.A11: Affirm under the express broad “how does Standing change” clause, even though the supplied generic justification points only to the timing clause.

Q014.A13: Affirm the source-supported enthusiasm change under the broad Standing interrogative. A narrower emergency-loans-only reading is possible, so this is not a basis for adding unrelated dividend calculations.

Existing optional key context (not promoted to mandatory): Company ordinary expense census: current Debt, non-Commander officers/regiments, ships including China at £1 each.; Each dividend pays £1 per share including Chairman.

### Q015 — 17 atoms; affirmed

When Company regions face a Crisis, which regions are attacked, in what order and at what strength? How is defense mounted and what happens on successful defense?

Targets, order, primary/secondary strength, defense actor/fallback/exhaustion and successful results are asked. The greater-than-or-equal comparison is authorized human interpretation, distinct from the literal original equality wording. No official-email claim is required.

Original source evidence: R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q015.A01 | Primary Crisis first | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A02 | Additional Rebellion in every other Company-controlled region with unrest | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A03 | Secondary resolution by Bombay, Madras, Bengal Army order | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A04 | Each Commander chooses order among associated regions | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A05 | Primary strength depends on Crisis type | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A06 | Normal primary Invasion attack is whole attacking empire plus event modifier and target unrest | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A07 | Normal primary Rebellion attack is rebelling-region strength plus event modifier and target unrest | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A08 | Secondary strength equals local unrest only | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A09 | Associated Commander chooses active Army pieces and exhausts them | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A10 | Must meet attacking strength or exhaust as many as possible if insufficient | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A11 | If Commander vacant Military Affairs substitutes | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A12 | If both vacant Chairman substitutes | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A13 | Under accepted user interpretation newly exhausted total defense strength at least attack defeats Crisis | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A14 | Clear target unrest | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A15 | Actual Commander gains one trophy | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A16 | Substitute gains no trophy | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q015.A17 | Defeated normal primary Invasion loses one attacker tower if possible | supported | affirmed_requested_or_clearly_implied | R2262-2296, R2192-2219, FOREIGN-DESIGNER, HUMAN-DEFENSE, APPROVED-SCOPE |

Q015.A13: Human-approved >= rule is normative in this assigned scope and must be attributed appropriately if discussed; it is not a literal quote of the printed equality test.

Existing optional key context (not promoted to mandatory): Explicit strength-two versus strength-one alliance fixture.; Source-audit qualification or publisher-email disclaimer need not be volunteered.; Alliance purchase, indivisibility, once-only use and Refresh mechanics.; Region Loss failure procedure.; Special Foreign Invasion primary die-without-unrest exception.; Substitute does not lose trophies on failed defense..

### Q016 — 11 atoms; affirmed

What happens when a law fails versus passes, including support-zero, policy movement, Prime Minister and effect order?

Threshold including zero, card/token/PM/policy consequences and full resolution order directly answer fail-versus-pass outcomes, including common vote-card cleanup.

Original source evidence: R2570-2587.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q016.A01 | Support at most -1 fails | supported | affirmed_requested_or_clearly_implied | R2570-2587 |
| Q016.A02 | Discard failed law | supported | affirmed_requested_or_clearly_implied | R2570-2587 |
| Q016.A03 | Resolve dilemma If Failed effect | supported | affirmed_requested_or_clearly_implied | R2570-2587 |
| Q016.A04 | Support at least zero passes | supported | affirmed_requested_or_clearly_implied | R2570-2587 |
| Q016.A05 | Passed law joins passed laws | supported | affirmed_requested_or_clearly_implied | R2570-2587 |
| Q016.A06 | PM gains passed-law token | supported | affirmed_requested_or_clearly_implied | R2570-2587 |
| Q016.A07 | Failure: Opposition Leader returns marker | supported | affirmed_requested_or_clearly_implied | R2570-2587 |
| Q016.A08 | Failure: Opposition Leader becomes PM | supported | affirmed_requested_or_clearly_implied | R2570-2587 |
| Q016.A09 | Failure: new PM moves selected policy to either adjacent space and resolves it | supported | affirmed_requested_or_clearly_implied | R2570-2587 |
| Q016.A10 | Passage: selected policy consequence before immediate law effects | supported | affirmed_requested_or_clearly_implied | R2570-2587 |
| Q016.A11 | Restore voting cards after resolution | supported | affirmed_requested_or_clearly_implied | R2570-2587 |

Existing optional key context (not promoted to mandatory): Legislation-triggered failure completes vote before scoring..

### Q017 — 13 atoms; affirmed

When can or must a Deregulation session be called in the relevant scenarios, and what are its success/failure effects and exceptions from ordinary voting?

Scenario/timing eligibility, lined/starred conditions, pass/fail effects and ordinary-voting exceptions are explicit; all listed atoms are required or clear implications.

Original source evidence: R2588-2601, R2626-2630.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q017.A01 | In 1758 or Long 1710 | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2626-2630 |
| Q017.A02 | At start of turn before London Season | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2626-2630 |
| Q017.A03 | May call if Standing or Debt is lined | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2626-2630 |
| Q017.A04 | Must call if either is starred | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2626-2630 |
| Q017.A05 | Pass reduces Debt by one for each two Debt | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2626-2630 |
| Q017.A06 | Pass sets Standing to S | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2626-2630 |
| Q017.A07 | Pass gives PM passed-law token | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2626-2630 |
| Q017.A08 | Pass activates Deregulation | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2626-2630 |
| Q017.A09 | Failure raises Company-share VP value up to ±3 | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2626-2630 |
| Q017.A10 | No policy attached | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2626-2630 |
| Q017.A11 | Failed law remains available | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2626-2630 |
| Q017.A12 | PM stays in office on failure | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2626-2630 |
| Q017.A13 | PM may vote against | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2626-2630 |

### Q018 — 17 atoms; affirmed

How can a firm be formed or invested in, where does money come from, and what restrictions apply to Company shares, invested workshops and the ten-share limit?

Formation and investment mechanisms, eligibility, source/destination of the £5, share/workshop restrictions and cap behavior are requested. No unrelated firm acquisition mechanics are required.

Original source evidence: R2679-2724, R1184-1187.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q018.A01 | Formation requires player not already managing a firm | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A02 | Return eligible Company share or flip uninvested workshop | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A03 | Flip own charter to firm | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A04 | Create initial family firm share | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A05 | Put Value at leftmost space | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A06 | Bank supplies £5 into London treasury | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A07 | Later investment needs manager consent | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A08 | Same eligible share or workshop payment | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A09 | Bank supplies £5 London per investment | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A10 | Create firm share subject to cap | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A11 | Cannot invest Company share when Standing or Debt is weak/lined | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A12 | Cannot invest share created this turn even if transferred | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A13 | Chairman share cannot be invested | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A14 | Invested workshop loses bonus | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A15 | Invested workshop loses Company-failure VP | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A16 | Firm has maximum ten shares | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |
| Q018.A17 | Investment may continue at cap without creating shares | supported | affirmed_requested_or_clearly_implied | R2679-2724, R1184-1187 |

### Q019 — 21 atoms; explicit_findings

Explain firm trading strategy, when checks and order filling occur, initiative, capacity, repeat-filled revenue and firm value growth.

Strategy, check and order-fill timing, initiative, capacity, refilling and Value growth are explicitly asked. The source requires waiting for the President’s successful Trade roll before ordinary order filling; absent/nontrading fallback is separately stated in the current list.

Original source evidence: R2773-2822.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q019.A01 | After investment, secretly select home region or sea zone and London bid | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A02 | Firm needs at least one ship | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A03 | May select closed home | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A04 | Reveal bid cash together | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A05 | Keep strategy secret until associated Presidency starts | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A06 | Reveal strategy at associated Presidency start | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A07 | One check using bid dice | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A08 | Pay bid to bank | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A09 | Fill in initiative order after successful checks | supported_in_context_but_incomplete_timing_wording | requested_precision_clarification | R2791-2809 / FB-Q019-09 |
| Q019.A10 | Initiative is ship count minus count of dice showing 1 or 2 | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A11 | Successful President computes initiative the same way | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A12 | Lowest initiative fills first | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A13 | President breaks ties | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A14 | If President vacant or not trading, wait for Commander and Governors | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A15 | Chairman then breaks ties | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A16 | Fill maximum up to ships plus one open connected orders | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A17 | Start from chosen home | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A18 | Firm fills each order at most once | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A19 | Orders previously filled by others may be filled for half listed revenue rounded down | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A20 | Firm trade revenue enters India | supported | affirmed_requested_or_clearly_implied | R2773-2822 |
| Q019.A21 | Advance Value one space per £6 revenue this turn | supported | affirmed_requested_or_clearly_implied | R2773-2822 |

### Q020 — 12 atoms; affirmed

How are firm expenses and dividends funded and calculated, and what happens to a failing firm, its shares and workshops?

Cost formula, treasury funding, dividend calculation and failure outcomes to shares/ships/charter/workshops are requested. Exact Revenue order, marker/sweep/waiver mechanics are contextual to this row and separately asked by Q092/Q101.

Original source evidence: R2827-2855, R2888-2918.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q020.A01 | Expense is £1 per ship | supported | affirmed_requested_or_clearly_implied | R2827-2855, R2888-2918 |
| Q020.A02 | Also pay greater of share count or Value | supported | affirmed_requested_or_clearly_implied | R2827-2855, R2888-2918 |
| Q020.A03 | Expenses use either or both firm treasuries | supported | affirmed_requested_or_clearly_implied | R2827-2855, R2888-2918 |
| Q020.A04 | Dividends use India only | supported | affirmed_requested_or_clearly_implied | R2827-2855, R2888-2918 |
| Q020.A05 | Each dividend pays £1 per share | supported | affirmed_requested_or_clearly_implied | R2827-2855, R2888-2918 |
| Q020.A06 | Each dividend additionally pays manager £1 | supported | affirmed_requested_or_clearly_implied | R2827-2855, R2888-2918 |
| Q020.A07 | Unpaid expenses require dissolution unless rescued | supported | affirmed_requested_or_clearly_implied | R2827-2855, R2888-2918 |
| Q020.A08 | Shares go to Debtors Prison | supported | affirmed_requested_or_clearly_implied | R2827-2855, R2888-2918 |
| Q020.A09 | Each prison share costs one VP | supported | affirmed_requested_or_clearly_implied | R2827-2855, R2888-2918 |
| Q020.A10 | Ships return matching yards | supported | affirmed_requested_or_clearly_implied | R2827-2855, R2888-2918 |
| Q020.A11 | Charter returns family side | supported | affirmed_requested_or_clearly_implied | R2827-2855, R2888-2918 |
| Q020.A12 | Invested workshops stay invested | supported | affirmed_requested_or_clearly_implied | R2827-2855, R2888-2918 |

Existing optional key context (not promoted to mandatory): Exact firm Revenue order, windows and PM tiebreakers.; Emergency investment and merger rescue procedures.; Record actual total dividends on retirement marker.; Sweep remaining India cash into London after dividends.; Shareholder may forgo own dividends with manager consent..

### Q021 — 12 atoms; affirmed

Which components and tracks are unlimited, what happens when a limited supply runs out, and what information is normally hidden?

Unlimited supplies/tracks, limited-supply fallback and normal/temporary hidden information are the question’s complete categories; provisional firm secrecy is a relevant exception.

Original source evidence: R654-666, R2773-2789.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q021.A01 | Cash unlimited with proxies | supported | affirmed_requested_or_clearly_implied | R654-666, R2773-2789 |
| Q021.A02 | Trophies/passed-law tokens unlimited with proxies | supported | affirmed_requested_or_clearly_implied | R654-666, R2773-2789 |
| Q021.A03 | Dice unlimited with proxies | supported | affirmed_requested_or_clearly_implied | R654-666, R2773-2789 |
| Q021.A04 | Regiments unlimited with proxies | supported | affirmed_requested_or_clearly_implied | R654-666, R2773-2789 |
| Q021.A05 | Balance track unlimited | supported | affirmed_requested_or_clearly_implied | R654-666, R2773-2789 |
| Q021.A06 | VP track unlimited | supported | affirmed_requested_or_clearly_implied | R654-666, R2773-2789 |
| Q021.A07 | Vote track unlimited | supported | affirmed_requested_or_clearly_implied | R654-666, R2773-2789 |
| Q021.A08 | Other component supplies limited | supported | affirmed_requested_or_clearly_implied | R654-666, R2773-2789 |
| Q021.A09 | Complete as much as possible | supported | affirmed_requested_or_clearly_implied | R654-666, R2773-2789 |
| Q021.A10 | Information including discards normally public | supported | affirmed_requested_or_clearly_implied | R654-666, R2773-2789 |
| Q021.A11 | Facedown blackmail hidden | supported | affirmed_requested_or_clearly_implied | R654-666, R2773-2789 |
| Q021.A12 | Firm strategy and bid temporarily secret during selection | supported | affirmed_requested_or_clearly_implied | R654-666, R2773-2789 |

Q021.A12: Temporary firm secrecy is a relevant hidden-information exception, not permission to hide all firm information.

### Q022 — 16 atoms; affirmed

What can be traded in negotiations and what cannot? How is a transferred share represented, and can blackmail be traded after use?

All positive and negative trade categories, Chairman restriction, share replacement/destinations and used-blackmail ban are requested. Luxury VP adjustment and private peeking are not independently demanded here.

Original source evidence: R757-807, R1184-1187, R1039-1042.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q022.A01 | Enterprises tradable | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A02 | Facedown blackmail tradable | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A03 | Family cash tradable | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A04 | Shares tradable | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A05 | Promises tradable | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A06 | Officeholders, writers and officers untradable | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A07 | Prize members untradable | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A08 | Spouses untradable | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A09 | Passed laws untradable | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A10 | PM dial untradable | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A11 | Trophies untradable | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A12 | Chairman piece untradable | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A13 | Replace share with recipient family piece | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A14 | Original piece returns to original owner | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A15 | Played blackmail cannot be traded | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |
| Q022.A16 | Unplayed blackmail trades facedown | supported | affirmed_requested_or_clearly_implied | R757-807, R1184-1187, R1039-1042 |

Existing optional key context (not promoted to mandatory): Luxury VP follows ownership after transfer.; Unplayed blackmail may be privately inspected.; Played blackmail remains faceup.

### Q023 — 7 atoms; affirmed

Are immediate and future deals binding? What limits govern promise calling, simultaneous unfulfillable calls and repeated activation after a transfer?

Enforceability, promise force/timing/endgame limits, unfulfillable simultaneous calls and no-double-activation directly answer the exact wording.

Original source evidence: R762-807, R843-847.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q023.A01 | Immediate transfers binding | supported | affirmed_requested_or_clearly_implied | R762-807, R843-847 |
| Q023.A02 | Future agreements nonbinding | supported | affirmed_requested_or_clearly_implied | R762-807, R843-847 |
| Q023.A03 | Printed promise forces guarantor if able | supported | affirmed_requested_or_clearly_implied | R762-807, R843-847 |
| Q023.A04 | Observe card timing | supported | affirmed_requested_or_clearly_implied | R762-807, R843-847 |
| Q023.A05 | No promise calling during Final Scoring | supported | affirmed_requested_or_clearly_implied | R762-807, R843-847 |
| Q023.A06 | Guarantor chooses which calls to satisfy if unable to satisfy all | supported | affirmed_requested_or_clearly_implied | R762-807, R843-847 |
| Q023.A07 | A transfer does not permit activating a resource twice | supported | affirmed_requested_or_clearly_implied | R762-807, R843-847 |

Existing optional key context (not promoted to mandatory): Promises may be transferred to third party or guarantor..

### Q024 — 15 atoms; explicit_findings

How does setup use extra player cards for five or six players, distribute holdings, award starting luxury points and build the London display?

Extra setup cards, holdings distribution, luxury VP and display construction are requested. The office family member goes to the office; its matching card is taken by the player, not placed at that office.

Original source evidence: R416-433, R453-477.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q024.A01 | Add three matching extra cards for five players | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |
| Q024.A02 | Add six matching extra cards for six players | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |
| Q024.A03 | Shuffle and deal evenly | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |
| Q024.A04 | Take all printed holdings | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |
| Q024.A05 | Put office card and member in indicated office | wrong_card_destination_as_written | source_error_requested_destination | R420-425 / FB-Q024-05 |
| Q024.A06 | Shares in Court | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |
| Q024.A07 | Writers and officers in indicated boxes | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |
| Q024.A08 | Commander in Army slot without office card | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |
| Q024.A09 | Each shipyard gives matching ship | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |
| Q024.A10 | Put ship in listed sea zone, or on yard if unfitted | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |
| Q024.A11 | Two VP per starting luxury | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |
| Q024.A12 | Shuffle prestige and blackmail together | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |
| Q024.A13 | Display three | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |
| Q024.A14 | Prestige faceup | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |
| Q024.A15 | Blackmail facedown | supported | affirmed_requested_or_clearly_implied | R416-433, R453-477 |

Existing optional key context (not promoted to mandatory): Shuffle remaining laws during setup..

### Q025 — 8 atoms; affirmed

When does the game end and which phase is completed if failure occurs during Events in India or from legislation? Can promises or negotiations continue in Final Scoring?

End triggers, immediate-versus-finish-phase exceptions and Final Scoring negotiation/promise limits are explicit; card permission qualifies the requested prohibition.

Original source evidence: R836-853, R1900-1902, R2008-2012, R2586-2587.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q025.A01 | At scenario final turn | supported | affirmed_requested_or_clearly_implied | R836-853, R1900-1902, R2008-2012, R2586-2587 |
| Q025.A02 | On Standing reaching leftmost failure | supported | affirmed_requested_or_clearly_implied | R836-853, R1900-1902, R2008-2012, R2586-2587 |
| Q025.A03 | Ordinary failure leads immediately to Final Scoring | supported | affirmed_requested_or_clearly_implied | R836-853, R1900-1902, R2008-2012, R2586-2587 |
| Q025.A04 | Events failure completes Events phase | supported | affirmed_requested_or_clearly_implied | R836-853, R1900-1902, R2008-2012, R2586-2587 |
| Q025.A05 | Legislation failure completes vote | supported | affirmed_requested_or_clearly_implied | R836-853, R1900-1902, R2008-2012, R2586-2587 |
| Q025.A06 | No negotiations during Final Scoring | supported | affirmed_requested_or_clearly_implied | R836-853, R1900-1902, R2008-2012, R2586-2587 |
| Q025.A07 | No promise calling during Final Scoring | supported | affirmed_requested_or_clearly_implied | R836-853, R1900-1902, R2008-2012, R2586-2587 |
| Q025.A08 | Explicit card permissions can override | supported | affirmed_requested_or_clearly_implied | R836-853, R1900-1902, R2008-2012, R2586-2587 |

Existing optional key context (not promoted to mandatory): Blackmail cannot be played in Final Scoring absent explicit permission..

### Q026 — 14 atoms; affirmed

Explain final Power sources, tied first and tied second awards, and how final victory ties are broken.

The question asks all Power sources, tie awards and victory ties. Equivalent Power descriptions are sufficient; no demand to recite category labels in a particular order.

Original source evidence: R812-853.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q026.A01 | Enterprise Power according to Power track | supported | affirmed_requested_or_clearly_implied | R812-853 |
| Q026.A02 | Applicable prestige enterprises included | supported | affirmed_requested_or_clearly_implied | R812-853 |
| Q026.A03 | Company-share Power according to track | supported | affirmed_requested_or_clearly_implied | R812-853 |
| Q026.A04 | Bottom two track spaces yield zero | supported | affirmed_requested_or_clearly_implied | R812-853 |
| Q026.A05 | Each passed law adds one Power | supported | affirmed_requested_or_clearly_implied | R812-853 |
| Q026.A06 | Each trophy adds one Power | supported | affirmed_requested_or_clearly_implied | R812-853 |
| Q026.A07 | PM adds two Power | supported | affirmed_requested_or_clearly_implied | R812-853 |
| Q026.A08 | Applicable card Power includes faceup or facedown blackmail and relevant spouse | supported | affirmed_requested_or_clearly_implied | R812-853 |
| Q026.A09 | Most and second-most receive final-turn table awards | supported | affirmed_requested_or_clearly_implied | R812-853 |
| Q026.A10 | Tied first each receive lower award only | supported | affirmed_requested_or_clearly_implied | R812-853 |
| Q026.A11 | No other award when first tied | supported | affirmed_requested_or_clearly_implied | R812-853 |
| Q026.A12 | Tied second receive nothing | supported | affirmed_requested_or_clearly_implied | R812-853 |
| Q026.A13 | Most windows first tiebreaker | supported | affirmed_requested_or_clearly_implied | R812-853 |
| Q026.A14 | Then clockwise from Prime Minister | supported | affirmed_requested_or_clearly_implied | R812-853 |

### Q027 — 6 atoms; affirmed

How does Company survival versus failure affect shares, workshops and final retirements?

Survival/failure share/workshop and final-retirement consequences are exactly asked. Firm investment status qualifies workshop scoring; firm-special-retirement timing is contextual here.

Original source evidence: R829-835, R2719-2720, R2665-2674.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q027.A01 | Survival adds current Court VP per Company share | supported | affirmed_requested_or_clearly_implied | R829-835, R2719-2720, R2665-2674 |
| Q027.A02 | Failure subtracts current Court VP per Company share | supported | affirmed_requested_or_clearly_implied | R829-835, R2719-2720, R2665-2674 |
| Q027.A03 | Failure adds one VP per uninvested workshop | supported | affirmed_requested_or_clearly_implied | R829-835, R2719-2720, R2665-2674 |
| Q027.A04 | Survival performs final office attrition | supported | affirmed_requested_or_clearly_implied | R829-835, R2719-2720, R2665-2674 |
| Q027.A05 | Survival permits pensioner retirement without prestige | supported | affirmed_requested_or_clearly_implied | R829-835, R2719-2720, R2665-2674 |
| Q027.A06 | Failure resolves random Company-failure card instead of ordinary final retirements | supported | affirmed_requested_or_clearly_implied | R829-835, R2719-2720, R2665-2674 |

Existing optional key context (not promoted to mandatory): Scores may be negative.; Firm special retirement precedes ordinary final scoring regardless Company outcome..

### Q028 — 8 atoms; affirmed

How do spouses affect transfers, restrictions and retirement discounts, and how often can a discount be used?

Transfer ban, permanent spouse restrictions, immediate required trades, discount magnitude/stacking/personal use and frequency all answer requested effects.

Original source evidence: R1018-1031.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q028.A01 | Spouses cannot be transferred | supported | affirmed_requested_or_clearly_implied | R1018-1031 |
| Q028.A02 | Printed restriction persists rest of game | supported | affirmed_requested_or_clearly_implied | R1018-1031 |
| Q028.A03 | Required trades negotiated immediately on acquisition | supported | affirmed_requested_or_clearly_implied | R1018-1031 |
| Q028.A04 | Discount reduces retirement cost by printed amount | supported | affirmed_requested_or_clearly_implied | R1018-1031 |
| Q028.A05 | Discounts stack | supported | affirmed_requested_or_clearly_implied | R1018-1031 |
| Q028.A06 | Discounts personal and cannot be shared | supported | affirmed_requested_or_clearly_implied | R1018-1031 |
| Q028.A07 | Each discount usable once each London Season | supported | affirmed_requested_or_clearly_implied | R1018-1031 |
| Q028.A08 | Each discount usable once at Final Scoring | supported | affirmed_requested_or_clearly_implied | R1018-1031 |

Existing optional key context (not promoted to mandatory): Discount-reduced actual cash spending affects display priority..

### Q029 — 2 atoms; affirmed

What happens to fitted ships if their shipyards are returned by Violet Effingham or a tax? Can someone buy those shipyards immediately?

The question asks fitted ship persistence and repurchase eligibility after either specified shipyard-return cause, not unrelated loss-of-VP rules.

Original source evidence: R1022-1025, R2344-2357.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q029.A01 | Ships remain fitted and in play | supported | affirmed_requested_or_clearly_implied | R1022-1025, R2344-2357 |
| Q029.A02 | Matching returned yard cannot be purchased while ship is in play | supported | affirmed_requested_or_clearly_implied | R1022-1025, R2344-2357 |

Existing optional key context (not promoted to mandatory): Luxury/prize loss removes its applicable ownership/member VP..

### Q030 — 20 atoms; affirmed

List each family purchase/enlistment cost and immediate effect, including votes, income and failure scoring.

All family action prices and immediate placements/effects, votes, income and failure scoring are requested. The five distinct exchange prices answer the requested purchase-cost list; they are not an invented aggregate.

Original source evidence: R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q030.A01 | Writer free | supported_by_clear_rule_implication | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A02 | Place one member in chosen Presidency writer box | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A03 | Officer free | supported_by_clear_rule_implication | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A04 | Place one member in Officers-in-Training | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A05 | Luxury costs £4 | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A06 | Luxury worth two VP while owned | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A07 | Luxury is social enterprise with window | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A08 | Shipyard costs £2 | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A09 | Shipyard gives matching unfitted ship | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A10 | Shipyard is shipping enterprise | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A11 | Workshop costs £5 | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A12 | Workshop is manufacturing enterprise | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A13 | Seek Share costs printed empty-space price | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A14 | Seek Share places applicant on empty Stock Exchange space | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A15 | Stock Exchange queue prices £2, £3, £3, £4, £5 | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A16 | Shipyard gives one vote | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A17 | Fitted shipyard pays £1 bonus | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A18 | Workshop gives two votes | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A19 | Workshop pays £1 bonus | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |
| Q030.A20 | Uninvested workshop gives one VP on Company failure | supported | affirmed_requested_or_clearly_implied | R1100-1134, R1894-1896, R2719-2720, BOARD-STOCK |

Q030.A01: Free follows the enlistment procedure’s lack of a cash payment; it is not a literal printed £0 charge.

Q030.A03: Free follows the enlistment procedure’s lack of a cash payment; it is not a literal printed £0 charge.

Existing optional key context (not promoted to mandatory): One extra writer for four or more vacancies once in turn.; Seek Share purchase cash is paid to bank.; Luxury, shipyard and workshop purchase cash is paid to bank..

### Q031 — 4 atoms; affirmed

If a family must place a piece but has none in supply, what is required? What if no Family action is possible?

Mandatory prize cannibalization with VP loss and no-action/marker fallback are exactly asked; applying it to firm-share creation is contextual here.

Original source evidence: R1083-1099.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q031.A01 | Must use own prize member if possible | supported | affirmed_requested_or_clearly_implied | R1083-1099 |
| Q031.A02 | Lose that prize member printed VP | supported | affirmed_requested_or_clearly_implied | R1083-1099 |
| Q031.A03 | Take no action | supported | affirmed_requested_or_clearly_implied | R1083-1099 |
| Q031.A04 | Return opportunity marker to supply | supported | affirmed_requested_or_clearly_implied | R1083-1099 |

Existing optional key context (not promoted to mandatory): Family-piece shortage rule also applies to placing firm shares..

### Q032 — 5 atoms; affirmed

What happens if a Chairman must be hired but the Court is empty, including if the former Chairman has no supply pieces or prizes?

The empty-Court procedure and both shortage fallbacks are explicit; prize VP loss is a necessary consequence of the requested shortage case.

Original source evidence: R1191-1194, R1083-1085.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q032.A01 | Former Chairman automatically becomes Chairman | supported | affirmed_requested_or_clearly_implied | R1191-1194, R1083-1085 |
| Q032.A02 | Use family piece from supply | supported | affirmed_requested_or_clearly_implied | R1191-1194, R1083-1085 |
| Q032.A03 | If no supply, must use own prize if possible | supported | affirmed_requested_or_clearly_implied | R1191-1194, R1083-1085 |
| Q032.A04 | Lose prize VP when taking its member | supported | affirmed_requested_or_clearly_implied | R1191-1194, R1083-1085 |
| Q032.A05 | If neither available, there is no Chairman | supported | affirmed_requested_or_clearly_implied | R1191-1194, R1083-1085 |

### Q033 — 11 atoms; affirmed

Who hires the Director, Shipping, Military Affairs, Presidents, Governors and China, and what candidate fallback restrictions apply?

Each listed office’s hirer, candidate pool, ordered fallbacks and exclusions are requested. The Commander exclusion from Governor eligibility is substantive.

Original source evidence: R1234-1254.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q033.A01 | Chairman hires Director | supported | affirmed_requested_or_clearly_implied | R1234-1254 |
| Q033.A02 | Director candidates are officeholders except Chairman and Governors | supported | affirmed_requested_or_clearly_implied | R1234-1254 |
| Q033.A03 | If all offices vacant, Director may be any writer | supported | affirmed_requested_or_clearly_implied | R1234-1254 |
| Q033.A04 | Chairman hires Shipping from any writer | supported | affirmed_requested_or_clearly_implied | R1234-1254 |
| Q033.A05 | Chairman hires China from any writer | supported | affirmed_requested_or_clearly_implied | R1234-1254 |
| Q033.A06 | Chairman hires Military Affairs from Commander | supported | affirmed_requested_or_clearly_implied | R1234-1254 |
| Q033.A07 | If none, Military Affairs candidate is officer | supported | affirmed_requested_or_clearly_implied | R1234-1254 |
| Q033.A08 | If none, candidate is trainee | supported | affirmed_requested_or_clearly_implied | R1234-1254 |
| Q033.A09 | Director hires President from associated writer or Governor | supported | affirmed_requested_or_clearly_implied | R1234-1254 |
| Q033.A10 | President hires Governor from associated writer or officer | supported | affirmed_requested_or_clearly_implied | R1234-1254 |
| Q033.A11 | Governor candidate cannot be Commander | supported | affirmed_requested_or_clearly_implied | R1234-1254 |

### Q034 — 5 atoms; explicit_findings

What can successful Special Envoys accomplish, can they repeat, and when may the Director transfer pieces?

Successful Envoy choices, immediate China creation/hiring result, repetition and transfer timing are requested. Naming the Chairman and writer candidate pool for China is a separate hiring detail, directly asked by Q033/Q041.

Original source evidence: R1417-1433, R1808-1815.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q034.A01 | Open one closed order in non-Company region | supported | affirmed_requested_or_clearly_implied | R1417-1433, R1808-1815 |
| Q034.A02 | Alternatively create China | supported | affirmed_requested_or_clearly_implied | R1417-1433, R1808-1815 |
| Q034.A03 | China hired immediately by Chairman from any writer | supported | mixed_requested_and_contextual | R1423-1428, R1808-1811 / FB-Q034-03 |
| Q034.A04 | May repeat Special Envoy actions while able | supported | affirmed_requested_or_clearly_implied | R1417-1433, R1808-1815 |
| Q034.A05 | Director may transfer after Special Envoy actions | supported | affirmed_requested_or_clearly_implied | R1417-1433, R1808-1815 |

Existing optional key context (not promoted to mandatory): Envoy check costs £1 office treasury per die and no penalty.; Director may make up to two transfers, one writer or ship each, between Presidencies/sea zones including China..

### Q035 — 10 atoms; affirmed

In what order does Military Affairs transfer pieces, assign trainees and appoint Commanders? When is an incumbent replaced and does Nepotism apply?

Action order and Commander appointment/replacement eligibility are requested. Army transfer quantities/placements are contextual here and explicitly asked by Q104.

Original source evidence: R1472-1520.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q035.A01 | Army transfers first | supported | affirmed_requested_or_clearly_implied | R1472-1520 |
| Q035.A02 | Assign trainees second | supported | affirmed_requested_or_clearly_implied | R1472-1520 |
| Q035.A03 | Appoint Commanders last | supported | affirmed_requested_or_clearly_implied | R1472-1520 |
| Q035.A04 | Another family strictly exceeding incumbent family total Army pieces triggers replacement | supported | affirmed_requested_or_clearly_implied | R1472-1520 |
| Q035.A05 | Vacant Commander is appointed | supported | affirmed_requested_or_clearly_implied | R1472-1520 |
| Q035.A06 | Select from families with greatest total Army pieces | supported | affirmed_requested_or_clearly_implied | R1472-1520 |
| Q035.A07 | Move selected officer into Commander slot | supported | affirmed_requested_or_clearly_implied | R1472-1520 |
| Q035.A08 | Previous Commander becomes active officer | supported | affirmed_requested_or_clearly_implied | R1472-1520 |
| Q035.A09 | Incumbent tied for greatest stays | supported | affirmed_requested_or_clearly_implied | R1472-1520 |
| Q035.A10 | Nepotism does not apply | supported | affirmed_requested_or_clearly_implied | R1472-1520 |

Existing optional key context (not promoted to mandatory): Up to two Army transfers, one officer/regiment each, to active top half.; Must assign all trainees into chosen Armies active top halves..

### Q036 — 9 atoms; affirmed

Who orders Presidency actions, can Commander or Governors decline, can their actions be interrupted, and what may Chairman do with vacant President?

Presidency order authority, offered actions, decline/interruption rules and vacant-President Chairman limits are all requested.

Original source evidence: R1527-1544.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q036.A01 | President orders own Trade, Commander and Governors | supported | affirmed_requested_or_clearly_implied | R1527-1544 |
| Q036.A02 | Must offer Commander and Governors opportunity | supported | affirmed_requested_or_clearly_implied | R1527-1544 |
| Q036.A03 | Commander may decline | supported | affirmed_requested_or_clearly_implied | R1527-1544 |
| Q036.A04 | Governors may decline | supported | affirmed_requested_or_clearly_implied | R1527-1544 |
| Q036.A05 | Each position completes all actions before next position | supported | affirmed_requested_or_clearly_implied | R1527-1544 |
| Q036.A06 | Trade can be before or after positions but cannot interrupt | supported | affirmed_requested_or_clearly_implied | R1527-1544 |
| Q036.A07 | Chairman sets order for remaining positions | supported | affirmed_requested_or_clearly_implied | R1527-1544 |
| Q036.A08 | Chairman may not Trade | supported | affirmed_requested_or_clearly_implied | R1527-1544 |
| Q036.A09 | Chairman may not approve local alliance purchases | supported | affirmed_requested_or_clearly_implied | R1527-1544 |

### Q037 — 3 atoms; affirmed

Do trade ships become exhausted, and how do placed writers and Presidency dividers return during Refresh?

Ship exhaustion and writer/divider return are asked. Affiliation must be preserved on return; the detailed divider-placement trigger is contextual and separately asked by Q105.

Original source evidence: R1555-1582, R2612-2619.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q037.A01 | Trade does not exhaust ships | supported | affirmed_requested_or_clearly_implied | R1555-1582, R2612-2619 |
| Q037.A02 | Map writers return to associated Presidency | supported | affirmed_requested_or_clearly_implied | R1555-1582, R2612-2619 |
| Q037.A03 | Dividers return to supply | supported | affirmed_requested_or_clearly_implied | R1555-1582, R2612-2619 |

Existing optional key context (not promoted to mandatory): One order capacity per trade ship.; Divider placed between adjoining writers of different Presidencies preserves affiliation.; Filled tokens return supply at Refresh..

### Q038 — 11 atoms; affirmed

When are local alliances purchased and exhausted, who funds them, and can their strength be split or reused for Deploy and defense?

Alliance purchase/exhaustion timing, funding, indivisibility and once-only use for Deploy/defense are asked. These are real restrictions, not dispensable examples.

Original source evidence: R1617-1627, R2618-2619.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q038.A01 | Commander requests at start of own operations | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2618-2619 |
| Q038.A02 | President approves purchase | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2618-2619 |
| Q038.A03 | President treasury pays printed cost | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2618-2619 |
| Q038.A04 | Purchased alliance enters active/top Army half | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2618-2619 |
| Q038.A05 | Using alliance exhausts it | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2618-2619 |
| Q038.A06 | Unused active alliances exhaust at Refresh | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2618-2619 |
| Q038.A07 | Usable once in turn purchased | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2618-2619 |
| Q038.A08 | May be used for Deploy or defense | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2618-2619 |
| Q038.A09 | Whole alliance strength used for one purpose | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2618-2619 |
| Q038.A10 | Cannot split between purposes | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2618-2619 |
| Q038.A11 | Cannot reuse that turn | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2618-2619 |

Existing optional key context (not promoted to mandatory): No defense-source disclaimer or separate fixture is required.; Officers and regiments reactivate at Refresh..

### Q039 — 3 atoms; affirmed

When a Commander deploys into their own Company region solely to reopen orders or clear unrest, what dice penalty, loot minimum and trophies apply?

The specified own-region case asks only its penalty, loot minimum and trophies. Permission to target and all success-cleanup procedures are contextual to that fixture.

Original source evidence: R1630-1650, R1674-1703.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q039.A01 | Company-controlled defending strength zero | supported | affirmed_requested_or_clearly_implied | R1630-1650, R1674-1703 |
| Q039.A02 | Loot minimum surviving participating officers plus one Commander share | supported | affirmed_requested_or_clearly_implied | R1630-1650, R1674-1703 |
| Q039.A03 | Zero towers means no tower trophies | supported | affirmed_requested_or_clearly_implied | R1630-1650, R1674-1703 |

Existing optional key context (not promoted to mandatory): Own Company target requires closed order or unrest.; Success opens all orders and clears unrest; no new Governorship for already controlled region..

### Q040 — 8 atoms; explicit_findings

How many successes does a Governor need to build a Company ship, where is it during construction and where does it go? How are Governor regiments treated?

Success count and construction/finished destinations are asked, along with regiment treatment (Army placement, strength, bank loot and loss immunity). Lack of any other effect while unfinished is true but not independently asked by the location clauses.

Original source evidence: R1753-1762, R1648-1650.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q040.A01 | Two successful build choices | supported | affirmed_requested_or_clearly_implied | R1753-1762, R1648-1650 |
| Q040.A02 | First puts unfinished ship in region | supported | affirmed_requested_or_clearly_implied | R1753-1762, R1648-1650 |
| Q040.A03 | Unfinished ship has no other effect | supported | contextual_only | R1753-1757 / FB-Q040-03 |
| Q040.A04 | Second moves ship to associated Presidency sea zone | supported | affirmed_requested_or_clearly_implied | R1753-1762, R1648-1650 |
| Q040.A05 | Place in associated Army | supported | affirmed_requested_or_clearly_implied | R1753-1762, R1648-1650 |
| Q040.A06 | Officer-like strength | supported | affirmed_requested_or_clearly_implied | R1753-1762, R1648-1650 |
| Q040.A07 | Regiment loot paid to bank | supported | affirmed_requested_or_clearly_implied | R1753-1762, R1648-1650 |
| Q040.A08 | No officer-loss checks for regiments | supported | affirmed_requested_or_clearly_implied | R1753-1762, R1648-1650 |

Q040.A05: The broad regiment-treatment clause reasonably includes placement in the associated Army. Do not expand it to unrelated Commander operations.

### Q041 — 5 atoms; explicit_findings

What creates China, how is it hired, what resources does its treasury hold, when does it act and what ships count Eastern?

Preserved two-question review applies: creation/hiring/ship-only treasury/timing/Eastern status required; transfer actors contextual; four-purpose enumeration not independently required if Eastern equivalence is clear.

Original source evidence: R1808-1816.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q041.A01 | Successful Special Envoy to China or Envoy to China law creates office | supported | affirmed_requested_or_clearly_implied | R1808-1816 |
| Q041.A02 | Chairman immediately hires any writer | supported | affirmed_requested_or_clearly_implied | R1808-1816 |
| Q041.A03 | Ships only | supported | affirmed_requested_or_clearly_implied | R1808-1816 |
| Q041.A04 | China acts after Bengal | supported | affirmed_requested_or_clearly_implied | R1808-1816 |
| Q041.A05 | Ships in China count Eastern for expenses, storms, events and laws | supported | mixed_requested_and_contextual | R1812-1815 / FB-Q041-05 |

Existing optional key context (not promoted to mandatory): Shipping can send ships to China as eligible sea zone.; Director can transfer ships to China as eligible sea zone..

### Q042 — 6 atoms; affirmed

Can China repeat a failed trade check, trade with no export icons, or earn revenue from non-Company export icons? Give its dice, revenue and bonus.

Each yes/no eligibility limit and dice/revenue/bonus formula is explicitly asked; non-Company exports must be excluded.

Original source evidence: R1817-1823.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q042.A01 | Only one attempt | supported | affirmed_requested_or_clearly_implied | R1817-1823 |
| Q042.A02 | Cannot attempt without export in Company-controlled region | supported | affirmed_requested_or_clearly_implied | R1817-1823 |
| Q042.A03 | Non-Company exports excluded | supported | affirmed_requested_or_clearly_implied | R1817-1823 |
| Q042.A04 | One die per China ship | supported | affirmed_requested_or_clearly_implied | R1817-1823 |
| Q042.A05 | Success gives Balance £4 per export in all Company-controlled regions | supported | affirmed_requested_or_clearly_implied | R1817-1823 |
| Q042.A06 | Superintendent receives £1 per such export | supported | affirmed_requested_or_clearly_implied | R1817-1823 |

### Q043 — 10 atoms; affirmed

What happens when Governor General law passes to Governors, incomplete ships, Director and fatigue? How are subsequent conquests and region losses different?

The law’s effects on Governors, unfinished ships, Director/fatigue and future conquest/loss procedures are asked. Treasury and operation-slot continuity are part of the asked Director replacement.

Original source evidence: R1841-1859.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q043.A01 | Governors retire to Pensioners | supported | affirmed_requested_or_clearly_implied | R1841-1859 |
| Q043.A02 | Remove Governor overlays | supported | affirmed_requested_or_clearly_implied | R1841-1859 |
| Q043.A03 | Remove unfinished Company ships | supported | affirmed_requested_or_clearly_implied | R1841-1859 |
| Q043.A04 | Replace Director holder/card with GG | supported | affirmed_requested_or_clearly_implied | R1841-1859 |
| Q043.A05 | Preserve fatigue | supported | affirmed_requested_or_clearly_implied | R1841-1859 |
| Q043.A06 | Preserve office treasury | supported | affirmed_requested_or_clearly_implied | R1841-1859 |
| Q043.A07 | Preserve operation slot | supported | affirmed_requested_or_clearly_implied | R1841-1859 |
| Q043.A08 | Box Director and Governor cards | supported | affirmed_requested_or_clearly_implied | R1841-1859 |
| Q043.A09 | No new Governors or overlays after conquest | supported | affirmed_requested_or_clearly_implied | R1841-1859 |
| Q043.A10 | Region Loss skips Governor elimination | supported | affirmed_requested_or_clearly_implied | R1841-1859 |

Existing optional key context (not promoted to mandatory): GG hires/is hired like Director and undergoes normal attrition..

### Q044 — 10 atoms; explicit_findings

What guaranteed revenue does Governor General earn before Govern checks? Explain unrest from sixes, failure and tax, options per region and success limit.

Guaranteed revenue, six/failure/tax unrest, mandatory per-region choice, all choice destinations/restrictions and success cap are asked. The created ship is specifically a Company ship.

Original source evidence: R1860-1889.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q044.A01 | Company Balance gains £3 per Company-controlled region before checks | supported | affirmed_requested_or_clearly_implied | R1860-1889 |
| Q044.A02 | Each rolled six adds unrest to every Company region | supported | affirmed_requested_or_clearly_implied | R1860-1889 |
| Q044.A03 | Unsuccessful check adds another unrest to each | supported | affirmed_requested_or_clearly_implied | R1860-1889 |
| Q044.A04 | Each tax choice adds unrest | supported | affirmed_requested_or_clearly_implied | R1860-1889 |
| Q044.A05 | Multiple tax choices use different Company regions | supported | affirmed_requested_or_clearly_implied | R1860-1889 |
| Q044.A06 | Success must benefit each Company-controlled region once | supported | affirmed_requested_or_clearly_implied | R1860-1889 |
| Q044.A07 | Ship to any sea zone including China | supported_in_context_with_ship_type_implicit | requested_precision_clarification | R1870-1878 / FB-Q044-07 |
| Q044.A08 | Or regiment to any Army | supported | affirmed_requested_or_clearly_implied | R1860-1889 |
| Q044.A09 | Or unsplit £2 to Balance or an office treasury except GG own | supported | affirmed_requested_or_clearly_implied | R1860-1889 |
| Q044.A10 | At most one successful Govern | supported | affirmed_requested_or_clearly_implied | R1860-1889 |

Existing optional key context (not promoted to mandatory): Govern costs £1 per die from GG treasury, no penalty.; Successful Govern pays GG family £1 per Company region from bank.; Failed checks may retry with sufficient resources unless catastrophic.

### Q045 — 11 atoms; affirmed

How do storms affect unfatigued/fatigued player ships, Company/extra ships, China and firms?

All storm outcomes and exemptions by fatigue/ownership/China/firm strategy/Hobnob are expressly requested.

Original source evidence: R1943-1954, R1812-1815, R2919-2922.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q045.A01 | Roll per affected player-owned ship | supported | affirmed_requested_or_clearly_implied | R1943-1954, R1812-1815, R2919-2922 |
| Q045.A02 | 1–2 no change | supported | affirmed_requested_or_clearly_implied | R1943-1954, R1812-1815, R2919-2922 |
| Q045.A03 | 3–4 fatigue if unfatigued | supported | affirmed_requested_or_clearly_implied | R1943-1954, R1812-1815, R2919-2922 |
| Q045.A04 | 3–4 sink if already fatigued | supported | affirmed_requested_or_clearly_implied | R1943-1954, R1812-1815, R2919-2922 |
| Q045.A05 | 5–6 sink | supported | affirmed_requested_or_clearly_implied | R1943-1954, R1812-1815, R2919-2922 |
| Q045.A06 | Sunk ship returns matching yard unfatigued | supported | affirmed_requested_or_clearly_implied | R1943-1954, R1812-1815, R2919-2922 |
| Q045.A07 | Company ships exempt | supported | affirmed_requested_or_clearly_implied | R1943-1954, R1812-1815, R2919-2922 |
| Q045.A08 | Extra ships exempt | supported | affirmed_requested_or_clearly_implied | R1943-1954, R1812-1815, R2919-2922 |
| Q045.A09 | China ships count Eastern | supported | affirmed_requested_or_clearly_implied | R1943-1954, R1812-1815, R2919-2922 |
| Q045.A10 | Firm ships use strategy zone | supported | affirmed_requested_or_clearly_implied | R1943-1954, R1812-1815, R2919-2922 |
| Q045.A11 | Hobnob ships exempt | supported | affirmed_requested_or_clearly_implied | R1943-1954, R1812-1815, R2919-2922 |

### Q046 — 7 atoms; affirmed

What happens when an event closes an order containing a writer or filled token, and how does a Cascade handle already closed connected orders and repeated regional flooding?

Writer/token handling and Cascade propagation/closed-target fallback/per-region limits are requested; multiple incoming effects differ from initiating multiple Cascades.

Original source evidence: R1962-1975.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q046.A01 | Writer returns owner supply | supported | affirmed_requested_or_clearly_implied | R1962-1975 |
| Q046.A02 | Flip filled token closed | supported | affirmed_requested_or_clearly_implied | R1962-1975 |
| Q046.A03 | Fully closed source region Cascades to connected orders | supported | affirmed_requested_or_clearly_implied | R1962-1975 |
| Q046.A04 | Already closed connected target redirects to northernmost open order in that region | supported | affirmed_requested_or_clearly_implied | R1962-1975 |
| Q046.A05 | If none open Cascade there | supported | affirmed_requested_or_clearly_implied | R1962-1975 |
| Q046.A06 | Region initiates Cascade at most once per event tile | supported | affirmed_requested_or_clearly_implied | R1962-1975 |
| Q046.A07 | Region may receive multiple effects | supported | affirmed_requested_or_clearly_implied | R1962-1975 |

### Q047 — 9 atoms; affirmed

How do Turmoil, Windfall and Shuffle identify locations and resolve? Include the empty-draw-stack Shuffle exception.

All three named event locations/resolution sequences and the empty-stack Shuffle reversal are requested.

Original source evidence: R2111-2123.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q047.A01 | Top draw-stack region | supported | affirmed_requested_or_clearly_implied | R2111-2123 |
| Q047.A02 | Close northernmost open order | supported | affirmed_requested_or_clearly_implied | R2111-2123 |
| Q047.A03 | If all closed Cascade | supported | affirmed_requested_or_clearly_implied | R2111-2123 |
| Q047.A04 | Top draw-stack region and adjacent regions | supported | affirmed_requested_or_clearly_implied | R2111-2123 |
| Q047.A05 | Pay £1 per writer on orders there | supported | affirmed_requested_or_clearly_implied | R2111-2123 |
| Q047.A06 | Normally March first | supported | affirmed_requested_or_clearly_implied | R2111-2123 |
| Q047.A07 | Shuffle tile into remaining draw stack | supported | affirmed_requested_or_clearly_implied | R2111-2123 |
| Q047.A08 | Shuffle discards and put them on top | supported | affirmed_requested_or_clearly_implied | R2111-2123 |
| Q047.A09 | If draw stack empty March last | supported | affirmed_requested_or_clearly_implied | R2111-2123 |

### Q048 — 4 atoms; affirmed

How does Leader differ in sovereign and dominated regions, and when does it move Elephant?

Leader location, sovereign versus dominated resolution and the restricted Elephant movement are substantive parts of resolving the named event.

Original source evidence: R2124-2132.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q048.A01 | Use top draw-stack region | supported | affirmed_requested_or_clearly_implied | R2124-2132 |
| Q048.A02 | Sovereign gains tower | supported | affirmed_requested_or_clearly_implied | R2124-2132 |
| Q048.A03 | Dominated resolves Rebellion with printed explosion modifier | supported | affirmed_requested_or_clearly_implied | R2124-2132 |
| Q048.A04 | March only if Elephant wholly within Company region that successfully rebelled | supported | affirmed_requested_or_clearly_implied | R2124-2132 |

### Q049 — 5 atoms; affirmed

How does Peace differ with Elephant on a border versus fully within a region, and does it move afterward?

Border versus fully-inside Peace effects and subsequent March are explicit; do not import border tower growth into the wholly-inside case.

Original source evidence: R2133-2139.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q049.A01 | Border: open connected orders across border | supported | affirmed_requested_or_clearly_implied | R2133-2139 |
| Q049.A02 | Border: add tower to each touched non-Company region | supported | affirmed_requested_or_clearly_implied | R2133-2139 |
| Q049.A03 | Fully inside: open all local orders | supported | affirmed_requested_or_clearly_implied | R2133-2139 |
| Q049.A04 | Fully inside: clear unrest | supported | affirmed_requested_or_clearly_implied | R2133-2139 |
| Q049.A05 | Then March | supported | affirmed_requested_or_clearly_implied | R2133-2139 |

### Q050 — 8 atoms; affirmed

In a non-Company Invasion, which strengths count, does equal strength win, how do flags change and what if no empire flags remain?

Strengths, strict comparison and flag/capital/no-flag-supply effects are asked; the failed attacker’s tower loss is contextual to this exact question.

Original source evidence: R2192-2208, R707-714.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q050.A01 | Whole attacking empire plus modifier | supported | affirmed_requested_or_clearly_implied | R2192-2208, R707-714 |
| Q050.A02 | Whole defending empire | supported | affirmed_requested_or_clearly_implied | R2192-2208, R707-714 |
| Q050.A03 | Attacker must be strictly greater | supported | affirmed_requested_or_clearly_implied | R2192-2208, R707-714 |
| Q050.A04 | Tie fails | supported | affirmed_requested_or_clearly_implied | R2192-2208, R707-714 |
| Q050.A05 | Success puts matching attacker dominated flag on defender | supported | affirmed_requested_or_clearly_implied | R2192-2208, R707-714 |
| Q050.A06 | Capturing capital removes all old defender-empire flags | supported | affirmed_requested_or_clearly_implied | R2192-2208, R707-714 |
| Q050.A07 | Unflagged attacker creates capital and dominated flags if set available | supported | affirmed_requested_or_clearly_implied | R2192-2208, R707-714 |
| Q050.A08 | No new flags or empire if no set available | supported | affirmed_requested_or_clearly_implied | R2192-2208, R707-714 |

Existing optional key context (not promoted to mandatory): Failed normal Invasion removes one attacker tower..

### Q051 — 6 atoms; affirmed

In a non-Company Rebellion, which empire regions count, what wins a tie and which side loses a tower on failure?

Regional strength inclusion/exclusion, tie failure and capital tower loss are exactly asked. Successful Rebellion cleanup is contextual here and asked by Q090.

Original source evidence: R2209-2219.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q051.A01 | Rebel region strength plus modifier | supported | affirmed_requested_or_clearly_implied | R2209-2219 |
| Q051.A02 | Defending sovereign capital strength | supported | affirmed_requested_or_clearly_implied | R2209-2219 |
| Q051.A03 | Ignore other empire regions | supported | affirmed_requested_or_clearly_implied | R2209-2219 |
| Q051.A04 | Rebel must be strictly greater | supported | affirmed_requested_or_clearly_implied | R2209-2219 |
| Q051.A05 | Tie fails | supported | affirmed_requested_or_clearly_implied | R2209-2219 |
| Q051.A06 | Capital loses one tower, not rebel | supported | affirmed_requested_or_clearly_implied | R2209-2219 |

Existing optional key context (not promoted to mandatory): Successful non-Company Rebellion sovereignty, flag and order closure/Cascade..

### Q052 — 19 atoms; affirmed

List Region Loss destinations, officer checks, loot status and Standing loss escalation. Do these losses remove other Company regions automatically?

The broad request to list Region Loss destinations includes Commander/Governor/overlay/ship/unrest/dome/flag/control-token treatment, plus officer checks, loot status, escalating Standing and separate regional resolution.

Original source evidence: R1987-2012, R2262-2296.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q052.A01 | Commander returns supply | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A02 | Return half family trophies rounded up | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A03 | Governor card returns unused offices | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A04 | Governor member returns supply | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A05 | Governor fatigue returns supply | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A06 | Remove Governor overlay | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A07 | Remove unfinished ship | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A08 | Remove unrest | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A09 | Restore dome with one tower | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A10 | Apply appropriate normal-Invasion flag | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A11 | Return control token loot-down to region | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A12 | Region no longer associated with Presidency | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A13 | Roll per officer in associated Army | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A14 | Each six removes officer to owner supply | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A15 | Loot side down means no further loot bonus | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A16 | First region lost this turn loses one Standing | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A17 | Second loses two, and so on | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A18 | No automatic loss of other regions | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |
| Q052.A19 | Resolve each region attack separately | supported | affirmed_requested_or_clearly_implied | R1987-2012, R2262-2296 |

Q052.A13: Region Loss checks all officers in the associated Army, unlike Deploy checking only officers exhausted for that action.

Existing optional key context (not promoted to mandatory): Normal Company Invasion loss closes orders/Cascades; other successful attack types close by their own procedure..

### Q053 — 7 atoms; affirmed

How does Elephant March choose a region after successful Invasion versus other Marches, and its posture for Company, dominated, sovereign or fully formed empire?

March destination exception and each posture branch/fully-formed-empire fallback are asked. Imperial Ambitions is not interchangeable with normal top-stack destination.

Original source evidence: R2045-2082.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q053.A01 | Successful Invasion uses successful capital through Imperial Ambitions | supported | affirmed_requested_or_clearly_implied | R2045-2082 |
| Q053.A02 | Other Marches use top draw-stack region | supported | affirmed_requested_or_clearly_implied | R2045-2082 |
| Q053.A03 | Company: fully inside | supported | affirmed_requested_or_clearly_implied | R2045-2082 |
| Q053.A04 | Dominated: faces sovereign | supported | affirmed_requested_or_clearly_implied | R2045-2082 |
| Q053.A05 | Sovereign: tile-shape border toward neighbor | supported | affirmed_requested_or_clearly_implied | R2045-2082 |
| Q053.A06 | Skip own dominated neighbors clockwise | supported | affirmed_requested_or_clearly_implied | R2045-2082 |
| Q053.A07 | All neighbors dominated: redirect-arrow shape border toward empire capital | supported | affirmed_requested_or_clearly_implied | R2045-2082 |

### Q054 — 16 atoms; affirmed

How does Foreign Invasion select targets, calculate strength, alter towers/flags/orders and potentially redirect Elephant?

All Foreign Invasion targets, die strength, success-only orders/flags/towers and conditional circle March are asked; unrest exclusion is supported by the authorized designer ruling.

Original source evidence: R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q054.A01 | Storm die West targets Bombay | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A02 | South targets Madras | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A03 | East targets Bengal | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A04 | All storms targets each once | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A05 | No storms targets top draw-stack region | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A06 | Roll attack die per target | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A07 | Attack strength equals die | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A08 | Resolve as Invasion or Company attack as appropriate | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A09 | Success closes every open order | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A10 | Cascade only if all already closed | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A11 | Return local flag | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A12 | If capital return all matching flags | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A13 | Restore Company dome if applicable | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A14 | Set tower strength to half attack die rounded down | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A15 | If Elephant wholly within invaded Company region March with circle | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |
| Q054.A16 | Otherwise no redirect | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER, RULES33-CIRCLE |

### Q055 — 9 atoms; affirmed

When can PM stop drawing laws and how does a dilemma affect selection? How is the proposed policy chosen?

Drawing stop/selection/dilemma rules and the directional first-matching policy choice with target/consequence are requested. Reading the law and initial support are contextual and Q091 asks support separately.

Original source evidence: R2330-2343, R2365-2367.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q055.A01 | Reveal laws one at a time up to three | supported | affirmed_requested_or_clearly_implied | R2330-2343, R2365-2367 |
| Q055.A02 | May stop and choose an earlier draw | supported | affirmed_requested_or_clearly_implied | R2330-2343, R2365-2367 |
| Q055.A03 | Discard unselected draws | supported | affirmed_requested_or_clearly_implied | R2330-2343, R2365-2367 |
| Q055.A04 | Must stop on dilemma | supported | affirmed_requested_or_clearly_implied | R2330-2343, R2365-2367 |
| Q055.A05 | Must select dilemma | supported | affirmed_requested_or_clearly_implied | R2330-2343, R2365-2367 |
| Q055.A06 | Choose clockwise or counterclockwise | supported | affirmed_requested_or_clearly_implied | R2330-2343, R2365-2367 |
| Q055.A07 | Stop at first matching law icon | supported | affirmed_requested_or_clearly_implied | R2330-2343, R2365-2367 |
| Q055.A08 | Policy includes target and consequence | supported | affirmed_requested_or_clearly_implied | R2330-2343, R2365-2367 |
| Q055.A09 | Move PM arm before vote | supported | affirmed_requested_or_clearly_implied | R2330-2343, R2365-2367 |

Existing optional key context (not promoted to mandatory): Initialize selected-law starting support.; PM reads the selected law aloud..

### Q056 — 8 atoms; affirmed

How do normal taxes, window taxes, bonuses and power policies work, including target already highest in Power track?

Tax/window/bonus amounts, nonpayment consequences, affected prestige enterprises and Power swaps/highest-target exception are requested by the broad policy-procedure wording.

Original source evidence: R2344-2364, R1033-1037.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q056.A01 | £1 per target | supported | affirmed_requested_or_clearly_implied | R2344-2364, R1033-1037 |
| Q056.A02 | Return unpaid target including Chairman | supported | affirmed_requested_or_clearly_implied | R2344-2364, R1033-1037 |
| Q056.A03 | Additional charge for all windows on enterprises and prize members | supported | affirmed_requested_or_clearly_implied | R2344-2364, R1033-1037 |
| Q056.A04 | Return unaffordable enterprise or member | supported | affirmed_requested_or_clearly_implied | R2344-2364, R1033-1037 |
| Q056.A05 | £1 per target | supported | affirmed_requested_or_clearly_implied | R2344-2364, R1033-1037 |
| Q056.A06 | Swap target with next higher marker | supported | affirmed_requested_or_clearly_implied | R2344-2364, R1033-1037 |
| Q056.A07 | If target highest swap any other pair | supported | affirmed_requested_or_clearly_implied | R2344-2364, R1033-1037 |
| Q056.A08 | Prestige enterprises count in their category | supported | affirmed_requested_or_clearly_implied | R2344-2364, R1033-1037 |

### Q057 — 8 atoms; affirmed

How are votes bought and reused across rounds, who may call more rounds, and when must voting stop?

Vote sources/prices, single-use card votes across rounds, round order/authority and mandatory stop are asked. Unlimited track bookkeeping and final cleanup are optional context here.

Original source evidence: R2525-2540, R2584-2584.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q057.A01 | Family cash costs £1 per vote | supported | affirmed_requested_or_clearly_implied | R2525-2540, R2584-2584 |
| Q057.A02 | Card vote icons usable once per entire vote | supported | affirmed_requested_or_clearly_implied | R2525-2540, R2584-2584 |
| Q057.A03 | Rotate card to record use | supported | affirmed_requested_or_clearly_implied | R2525-2540, R2584-2584 |
| Q057.A04 | Card votes do not reset between rounds | supported | affirmed_requested_or_clearly_implied | R2525-2540, R2584-2584 |
| Q057.A05 | PM acts first then clockwise in complete rounds | supported | affirmed_requested_or_clearly_implied | R2525-2540, R2584-2584 |
| Q057.A06 | PM may call another full round | supported | affirmed_requested_or_clearly_implied | R2525-2540, R2584-2584 |
| Q057.A07 | PM may resolve after full round | supported | affirmed_requested_or_clearly_implied | R2525-2540, R2584-2584 |
| Q057.A08 | Round with no votes forces resolution | supported | affirmed_requested_or_clearly_implied | R2525-2540, R2584-2584 |

Existing optional key context (not promoted to mandatory): Vote support track unlimited.; Restore vote cards after the vote..

### Q058 — 10 atoms; affirmed

Can a supporter later oppose, can an opponent later support, how is Opposition Leader selected and how do coalition votes and PM promise exceptions work?

Direction of vote switching, Opposition Leader/ties, coalition consent/counting and PM prohibition/promise exception are explicit.

Original source evidence: R2541-2564.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q058.A01 | Supporter may later oppose | supported | affirmed_requested_or_clearly_implied | R2541-2564 |
| Q058.A02 | Opponent cannot later support same vote | supported | affirmed_requested_or_clearly_implied | R2541-2564 |
| Q058.A03 | Most opposition votes | supported | affirmed_requested_or_clearly_implied | R2541-2564 |
| Q058.A04 | Incumbent retains tie | supported | affirmed_requested_or_clearly_implied | R2541-2564 |
| Q058.A05 | Need recipient consent | supported | affirmed_requested_or_clearly_implied | R2541-2564 |
| Q058.A06 | Recipient already opposing or committed to oppose | supported | affirmed_requested_or_clearly_implied | R2541-2564 |
| Q058.A07 | Coalition votes count toward recipient opposition total | supported | affirmed_requested_or_clearly_implied | R2541-2564 |
| Q058.A08 | PM cannot oppose | supported | affirmed_requested_or_clearly_implied | R2541-2564 |
| Q058.A09 | PM cannot consent enterprises to opposition | supported | affirmed_requested_or_clearly_implied | R2541-2564 |
| Q058.A10 | Vote promise can force PM enterprises against law | supported | affirmed_requested_or_clearly_implied | R2541-2564 |

### Q059 — 11 atoms; affirmed

Must final-turn prizes pay upkeep, what happens to unpaid prizes, and what exactly refreshes on nonfinal turns?

Final-turn upkeep, unpaid member/VP consequences, skip-Refresh branch and all ordinary Refresh items are expressly requested.

Original source evidence: R2602-2621.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q059.A01 | Every prize member pays upkeep even final scheduled turn | supported | affirmed_requested_or_clearly_implied | R2602-2621 |
| Q059.A02 | Unpaid member returns supply | supported | affirmed_requested_or_clearly_implied | R2602-2621 |
| Q059.A03 | Lose its VP | supported | affirmed_requested_or_clearly_implied | R2602-2621 |
| Q059.A04 | Final turn skips Refresh and scores | supported | affirmed_requested_or_clearly_implied | R2602-2621 |
| Q059.A05 | Otherwise map writers return associated Presidencies | supported | affirmed_requested_or_clearly_implied | R2602-2621 |
| Q059.A06 | Filled tokens return supply | supported | affirmed_requested_or_clearly_implied | R2602-2621 |
| Q059.A07 | Dividers return supply | supported | affirmed_requested_or_clearly_implied | R2602-2621 |
| Q059.A08 | Extra ships return supply | supported | affirmed_requested_or_clearly_implied | R2602-2621 |
| Q059.A09 | Officers and regiments reactivate | supported | affirmed_requested_or_clearly_implied | R2602-2621 |
| Q059.A10 | Active alliances exhaust | supported | affirmed_requested_or_clearly_implied | R2602-2621 |
| Q059.A11 | Advance Turn | supported | affirmed_requested_or_clearly_implied | R2602-2621 |

### Q060 — 8 atoms; affirmed

Explain the firm special retirement limit, eligible piece, dividend cap, spouse discounts, zero-marker restriction and Final Scoring timing.

Special-retirement frequency/piece/cash cap/discounts/ineligibility and Final Scoring timing are asked. Ordinary prestige rules remain optional background to this row.

Original source evidence: R2651-2674.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q060.A01 | One special retirement per shareholder per London Season | supported | affirmed_requested_or_clearly_implied | R2651-2674 |
| Q060.A02 | Use family piece from supply | supported | affirmed_requested_or_clearly_implied | R2651-2674 |
| Q060.A03 | Multiple firms do not grant additional retirements | supported | affirmed_requested_or_clearly_implied | R2651-2674 |
| Q060.A04 | Actual cash spending cap is highest dividend marker among owned-share firms | supported | affirmed_requested_or_clearly_implied | R2651-2674 |
| Q060.A05 | No marker or zero marker makes that firm ineligible | supported | affirmed_requested_or_clearly_implied | R2651-2674 |
| Q060.A06 | Personal spouse discounts may permit higher printed-cost prize | supported | affirmed_requested_or_clearly_implied | R2651-2674 |
| Q060.A07 | At start Final Scoring after firm points | supported | affirmed_requested_or_clearly_implied | R2651-2674 |
| Q060.A08 | One eligible special retirement regardless Company outcome | supported | affirmed_requested_or_clearly_implied | R2651-2674 |

Existing optional key context (not promoted to mandatory): Normal retirement rules including London prestige eligibility apply; No prestige at Final Scoring.

### Q061 — 7 atoms; affirmed

Where do firm investments/trade proceeds go, what pays ship fitting/bids, expenses and dividends, and may family cash be gifted into firms?

Each fund origin/destination/use and no-family-cash-transfer restriction is requested. Post-dividend India sweep is contextual here and Q101 directly asks it.

Original source evidence: R2635-2647, R2729-2739, R2773-2779, R2838-2838, R2888-2918.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q061.A01 | Investments enter London | supported | affirmed_requested_or_clearly_implied | R2635-2647, R2729-2739, R2773-2779, R2838-2838, R2888-2918 |
| Q061.A02 | Trade proceeds enter India | supported | affirmed_requested_or_clearly_implied | R2635-2647, R2729-2739, R2773-2779, R2838-2838, R2888-2918 |
| Q061.A03 | London pays ship fitting | supported | affirmed_requested_or_clearly_implied | R2635-2647, R2729-2739, R2773-2779, R2838-2838, R2888-2918 |
| Q061.A04 | London pays bids | supported | affirmed_requested_or_clearly_implied | R2635-2647, R2729-2739, R2773-2779, R2838-2838, R2888-2918 |
| Q061.A05 | Either or both firm treasuries pay expenses | supported | affirmed_requested_or_clearly_implied | R2635-2647, R2729-2739, R2773-2779, R2838-2838, R2888-2918 |
| Q061.A06 | India alone pays dividends | supported | affirmed_requested_or_clearly_implied | R2635-2647, R2729-2739, R2773-2779, R2838-2838, R2888-2918 |
| Q061.A07 | No transfer between family treasury and firm treasuries | supported | affirmed_requested_or_clearly_implied | R2635-2647, R2729-2739, R2773-2779, R2838-2838, R2888-2918 |

Existing optional key context (not promoted to mandatory): Post-dividend India-to-London sweep..

### Q062 — 4 atoms; affirmed

When is Firms phase and who resolves timing conflicts within or between firms?

Phase position and conflict decision makers are asked; Investments ordering and strategy simultaneity are contextual to this wording, with Q107 asking Investments order.

Original source evidence: R2679-2688.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q062.A01 | After all Family including new Company shares | supported | affirmed_requested_or_clearly_implied | R2679-2688 |
| Q062.A02 | Before Hiring | supported | affirmed_requested_or_clearly_implied | R2679-2688 |
| Q062.A03 | Manager decides within firm | supported | affirmed_requested_or_clearly_implied | R2679-2688 |
| Q062.A04 | Prime Minister decides between firms | supported | affirmed_requested_or_clearly_implied | R2679-2688 |

Existing optional key context (not promoted to mandatory): Investments have no set order and continue until nobody wishes to act.; Managers choose strategies simultaneously after investments..

### Q063 — 8 atoms; affirmed

May a firm fit another player’s ship without consent, buy Company or extra ships, or buy a player’s fitted Company ship? State costs and payment destinations.

Consent, permitted/prohibited ship types, fitting/buyback prices and both payment destinations are all explicitly asked.

Original source evidence: R2729-2740.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q063.A01 | Fitting needs shipyard owner consent | supported | affirmed_requested_or_clearly_implied | R2729-2740 |
| Q063.A02 | Fitting costs £3 from London to bank | supported | affirmed_requested_or_clearly_implied | R2729-2740 |
| Q063.A03 | Cannot acquire Company ships | supported | affirmed_requested_or_clearly_implied | R2729-2740 |
| Q063.A04 | Cannot acquire extra ships | supported | affirmed_requested_or_clearly_implied | R2729-2740 |
| Q063.A05 | Needs owner consent | supported | affirmed_requested_or_clearly_implied | R2729-2740 |
| Q063.A06 | Unfatigued costs £3 | supported | affirmed_requested_or_clearly_implied | R2729-2740 |
| Q063.A07 | Fatigued costs £2 | supported | affirmed_requested_or_clearly_implied | R2729-2740 |
| Q063.A08 | Pay from London to Shipping treasury | supported | affirmed_requested_or_clearly_implied | R2729-2740 |

### Q064 — 10 atoms; affirmed

What prerequisites allow hostile takeover, and what moves or stays the same?

Hostile takeover initiator eligibility/consent and movement/preservation/reset of firm assets/markers/charter are requested; initiator shareholding is not a prerequisite.

Original source evidence: R2741-2748.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q064.A01 | Initiator cannot already manage firm | supported | affirmed_requested_or_clearly_implied | R2741-2748 |
| Q064.A02 | Majority shareholder consent | supported | affirmed_requested_or_clearly_implied | R2741-2748 |
| Q064.A03 | Initiator need not own share | supported_by_clear_rule_implication | affirmed_requested_or_clearly_implied | R2741-2748 |
| Q064.A04 | Move ships to new manager charter | supported | affirmed_requested_or_clearly_implied | R2741-2748 |
| Q064.A05 | Move both treasuries | supported | affirmed_requested_or_clearly_implied | R2741-2748 |
| Q064.A06 | Move shares | supported | affirmed_requested_or_clearly_implied | R2741-2748 |
| Q064.A07 | Preserve Value position | supported | affirmed_requested_or_clearly_implied | R2741-2748 |
| Q064.A08 | Preserve dividend marker position | supported | affirmed_requested_or_clearly_implied | R2741-2748 |
| Q064.A09 | Former manager resets cubes | supported | affirmed_requested_or_clearly_implied | R2741-2748 |
| Q064.A10 | Former charter returns family side | supported | affirmed_requested_or_clearly_implied | R2741-2748 |

Q064.A03: No initiating shareholding requirement appears in the complete takeover prerequisites; this is a source-supported eligibility implication.

### Q065 — 6 atoms; affirmed

What makes a merger legal, determines primary firm and handles over-ten shares? What happens to secondary treasuries and charters?

Consent, highest-Value/tie choice, excess-share consent and secondary treasury/charter outcomes are asked. Ships/share consolidation is contextual here and expressly Q108.

Original source evidence: R2749-2768.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q065.A01 | All shareholders of every merging firm consent | supported | affirmed_requested_or_clearly_implied | R2749-2768 |
| Q065.A02 | Highest Value firm | supported | affirmed_requested_or_clearly_implied | R2749-2768 |
| Q065.A03 | Players choose among tied highest | supported | affirmed_requested_or_clearly_implied | R2749-2768 |
| Q065.A04 | Return excess shares only with their owners consent | supported | affirmed_requested_or_clearly_implied | R2749-2768 |
| Q065.A05 | Consolidate secondary treasuries in primary | supported | affirmed_requested_or_clearly_implied | R2749-2768 |
| Q065.A06 | Return secondary charters family side | supported | affirmed_requested_or_clearly_implied | R2749-2768 |

Existing optional key context (not promoted to mandatory): Optional share transfers may be negotiated.; Merger agreement is one binding immediate transfer.; Secondary ships and shares consolidate into primary..

### Q066 — 6 atoms; affirmed

What does Hobnob permit and forbid, what happens to its retirement marker and ships in storms, and must the firm still pay expenses?

No bid/trade/dividends, mandatory expenses, retained retirement marker and storm exemption directly answer each Hobnob clause.

Original source evidence: R2782-2785, R2913-2922.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q066.A01 | No cash bid | supported | affirmed_requested_or_clearly_implied | R2782-2785, R2913-2922 |
| Q066.A02 | No trading | supported | affirmed_requested_or_clearly_implied | R2782-2785, R2913-2922 |
| Q066.A03 | No dividends | supported | affirmed_requested_or_clearly_implied | R2782-2785, R2913-2922 |
| Q066.A04 | Still pays expenses | supported | affirmed_requested_or_clearly_implied | R2782-2785, R2913-2922 |
| Q066.A05 | Keep previous dividend marker | supported | affirmed_requested_or_clearly_implied | R2782-2785, R2913-2922 |
| Q066.A06 | Ships exempt storms | supported | affirmed_requested_or_clearly_implied | R2782-2785, R2913-2922 |

### Q067 — 8 atoms; affirmed

Can a firm at ten shares still receive emergency investment? What resources may be invested, what happens to its Value and unused rescue cash, and does same-turn-share restriction persist?

Cap eligibility, admissible investment resources/restrictions, expense use, lost rescue remainder and per-investment Value loss are requested. Normal manager consent is contextual to this narrow row.

Original source evidence: R2689-2724, R2845-2850.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q067.A01 | Yes | supported | affirmed_requested_or_clearly_implied | R2689-2724, R2845-2850 |
| Q067.A02 | No new shares at cap | supported | affirmed_requested_or_clearly_implied | R2689-2724, R2845-2850 |
| Q067.A03 | Normal eligible Company share or uninvested workshop | supported | affirmed_requested_or_clearly_implied | R2689-2724, R2845-2850 |
| Q067.A04 | Weak/lined Company-share restriction persists | supported | affirmed_requested_or_clearly_implied | R2689-2724, R2845-2850 |
| Q067.A05 | Same-turn Company-share restriction persists even after transfer | supported | affirmed_requested_or_clearly_implied | R2689-2724, R2845-2850 |
| Q067.A06 | Use rescue funds to pay expenses | supported | affirmed_requested_or_clearly_implied | R2689-2724, R2845-2850 |
| Q067.A07 | Unused rescue cash lost | supported | affirmed_requested_or_clearly_implied | R2689-2724, R2845-2850 |
| Q067.A08 | Reduce Value one space per investment | supported | affirmed_requested_or_clearly_implied | R2689-2724, R2845-2850 |

Q067.A06: “Unused rescue cash after paying expenses is lost” clearly conveys the expenses use; no separate sentence is needed.

Existing optional key context (not promoted to mandatory): Manager consent required for investment..

### Q068 — 4 atoms; explicit_findings

How does emergency merger differ from a normal multi-firm merger and whose expenses must be paid?

The one-other-firm limit and responsibility/timing for both sets of expenses are requested differences. Unchanged all-shareholder consent is true background, not a requested difference; Q065 explicitly asks merger legality.

Original source evidence: R2749-2768, R2852-2855.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q068.A01 | Only one other firm | supported | affirmed_requested_or_clearly_implied | R2749-2768, R2852-2855 |
| Q068.A02 | Follow normal negotiated all-shareholder consent | supported | contextual_only | R2760-2762, R2852-2855 / FB-Q068-02 |
| Q068.A03 | Other firm first pays own expenses if not already paid | supported | affirmed_requested_or_clearly_implied | R2749-2768, R2852-2855 |
| Q068.A04 | Pay outstanding endangered-firm expenses | supported | affirmed_requested_or_clearly_implied | R2749-2768, R2852-2855 |

### Q069 — 4 atoms; affirmed

What must shareholders consent to for voluntary dissolution and where do its shares and ships go? Do invested workshops recover?

Full-shareholder dissolution consent and share/ship/workshop destinations/status are asked. Penalty amount and charter reset are fuller dissolution context, separately covered by Q020/Q070.

Original source evidence: R2648-2650, R2839-2843.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q069.A01 | All shareholders must consent to dissolve | supported | affirmed_requested_or_clearly_implied | R2648-2650, R2839-2843 |
| Q069.A02 | Shares to Debtors Prison | supported | affirmed_requested_or_clearly_implied | R2648-2650, R2839-2843 |
| Q069.A03 | Ships to matching shipyards | supported | affirmed_requested_or_clearly_implied | R2648-2650, R2839-2843 |
| Q069.A04 | Workshops remain invested | supported | affirmed_requested_or_clearly_implied | R2648-2650, R2839-2843 |

Existing optional key context (not promoted to mandatory): Debtors Prison shares lose one VP each.; Dissolved charter flips to family side..

### Q070 — 5 atoms; affirmed

How are firm shares and Debtor’s Prison scored relative to ordinary final scoring, including fractional points and Company failure?

Timing relative to normal scoring, firm-share/prison amounts, fractional summing/rounding and applicability regardless Company outcome directly answer the question.

Original source evidence: R2665-2674, R2839-2843.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q070.A01 | At start of Final Scoring before ordinary scoring | supported | affirmed_requested_or_clearly_implied | R2665-2674, R2839-2843 |
| Q070.A02 | Score or lose printed firm Value VP per share | supported | affirmed_requested_or_clearly_implied | R2665-2674, R2839-2843 |
| Q070.A03 | Lose one VP per Debtors Prison piece | supported | affirmed_requested_or_clearly_implied | R2665-2674, R2839-2843 |
| Q070.A04 | Total fractional firm points before rounding down | supported | affirmed_requested_or_clearly_implied | R2665-2674, R2839-2843 |
| Q070.A05 | Firm scoring applies regardless Company survival or failure | supported | affirmed_requested_or_clearly_implied | R2665-2674, R2839-2843 |

Q070.A04: Sum firm-share points/fractions first, then round the remaining fraction down; do not independently round each firm/share.

Existing optional key context (not promoted to mandatory): Eligible special retirement before ordinary final scoring, regardless Company outcome.; Detailed ordinary Power, Court, retirement/failure scoring..

### Q071 — 20 atoms; affirmed

What are the cost, upkeep, VP and windows of each of the five prizes?

Every cell in the five-prize cost/upkeep/VP/windows table is explicitly requested; zero entries must not be invented as nonzero costs.

Original source evidence: BOARD-PRIZES.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q071.A01 | Prize 1: cost £2 per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A02 | Prize 1: upkeep £0 per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A03 | Prize 1: 0 VP per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A04 | Prize 1: 0 windows per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A05 | Prize 2: cost £4 per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A06 | Prize 2: upkeep £1 per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A07 | Prize 2: 2 VP per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A08 | Prize 2: 1 windows per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A09 | Prize 3: cost £8 per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A10 | Prize 3: upkeep £2 per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A11 | Prize 3: 4 VP per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A12 | Prize 3: 2 windows per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A13 | Prize 4: cost £14 per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A14 | Prize 4: upkeep £3 per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A15 | Prize 4: 8 VP per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A16 | Prize 4: 3 windows per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A17 | Prize 5: cost £20 per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A18 | Prize 5: upkeep £4 per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A19 | Prize 5: 12 VP per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |
| Q071.A20 | Prize 5: 4 windows per member | supported | affirmed_requested_or_clearly_implied | BOARD-PRIZES |

### Q072 — 8 atoms; affirmed

Which turns do 1710, 1758, 1813 and Long 1710 start and finish, and which include deregulation?

Each scenario’s start/end turns and Deregulation status are explicit. Long 1710 uses normal 1710 setup through turn 8.

Original source evidence: R358-388, R2626-2630, BOARD-TURNS.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q072.A01 | 1710 starts one and ends five | supported | affirmed_requested_or_clearly_implied | R358-388, R2626-2630, BOARD-TURNS |
| Q072.A02 | 1710 excludes Deregulation | supported | affirmed_requested_or_clearly_implied | R358-388, R2626-2630, BOARD-TURNS |
| Q072.A03 | 1758 starts three and ends seven | supported | affirmed_requested_or_clearly_implied | R358-388, R2626-2630, BOARD-TURNS |
| Q072.A04 | 1758 may Deregulate | supported | affirmed_requested_or_clearly_implied | R358-388, R2626-2630, BOARD-TURNS |
| Q072.A05 | 1813 starts five and ends eight | supported | affirmed_requested_or_clearly_implied | R358-388, R2626-2630, BOARD-TURNS |
| Q072.A06 | 1813 starts Deregulated | supported | affirmed_requested_or_clearly_implied | R358-388, R2626-2630, BOARD-TURNS |
| Q072.A07 | Long 1710 starts one and ends eight | supported | affirmed_requested_or_clearly_implied | R358-388, R2626-2630, BOARD-TURNS |
| Q072.A08 | Long 1710 may Deregulate | supported | affirmed_requested_or_clearly_implied | R358-388, R2626-2630, BOARD-TURNS |

### Q073 — 13 atoms; affirmed

What are 1710 and 1758 initial Standing, Debt, treasury funds, passed laws, regiments and Company ships, including 1758 control token?

Both scenario initial finance/laws/regiments/Company ships and 1758 Bengal control token are explicit; original scenario cards and errata agree.

Original source evidence: FRONTS-P9, ERRATA-SETUP.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q073.A01 | Standing £10 expectations | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q073.A02 | Debt zero | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q073.A03 | £3 each treasury | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q073.A04 | Royal Protection | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q073.A05 | One regiment each Army | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q073.A06 | No Company ships | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q073.A07 | Standing £12 expectations | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q073.A08 | Debt three | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q073.A09 | £4 each treasury | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q073.A10 | Calico Acts | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q073.A11 | One regiment each Army | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q073.A12 | One Company ship Eastern | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q073.A13 | Bengal control token in Bengal Presidency | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |

### Q074 — 13 atoms; affirmed

What changes are required for 1813 setup: initial finance/laws/military/ships, Company share value, Governor General, China and control tokens?

Every listed 1813 setup category is explicit; share-value token, boxed GG law/overlay, China and three control tokens are real mandatory changes.

Original source evidence: FRONTS-P9, ERRATA-SETUP.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q074.A01 | Standing £10 expectations | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q074.A02 | Debt zero | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q074.A03 | £3 each treasury | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q074.A04 | Military Oversight | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q074.A05 | Deregulation with Debtors Prison side up | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q074.A06 | Calico Acts | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q074.A07 | Two regiments each Army | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q074.A08 | One Company ship each zone | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q074.A09 | Court Company-share token +2/−2 | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q074.A10 | Box Governor General law | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q074.A11 | GG overlay replaces Director | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q074.A12 | Create China office | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |
| Q074.A13 | Three home-region control tokens in matching Presidencies | supported | affirmed_requested_or_clearly_implied | FRONTS-P9, ERRATA-SETUP |

### Q075 — 5 atoms; affirmed

What Power awards apply to final turns 1–3, 4–6 and 7–8, and what happens to a tied-first group in each?

Each award pair and tied-first lower-only consequence are directly requested, with native board values verified.

Original source evidence: R825-828, BOARD-POWER-AWARDS.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q075.A01 | Turns 1–3 first three and second one | supported | affirmed_requested_or_clearly_implied | R825-828, BOARD-POWER-AWARDS |
| Q075.A02 | Turns 4–6 first five and second two | supported | affirmed_requested_or_clearly_implied | R825-828, BOARD-POWER-AWARDS |
| Q075.A03 | Turns 7–8 first eight and second four | supported | affirmed_requested_or_clearly_implied | R825-828, BOARD-POWER-AWARDS |
| Q075.A04 | Each gets lower award, respectively one, two, four | supported | affirmed_requested_or_clearly_implied | R825-828, BOARD-POWER-AWARDS |
| Q075.A05 | No other award | supported | affirmed_requested_or_clearly_implied | R825-828, BOARD-POWER-AWARDS |

### Q076 — 12 atoms; affirmed

What are initial Power positions and which Standing/Debt spaces permit or force a Deregulation vote? Where is S?

Initial positions include the distinct order of the two zero-Power spaces; the question also requests lined/starred thresholds and S, verified on the native board.

Original source evidence: R2588-2601, R2361-2364, R814-816, BOARD-TRACKS.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q076.A01 | Social two | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2361-2364, R814-816, BOARD-TRACKS |
| Q076.A02 | Company shares one | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2361-2364, R814-816, BOARD-TRACKS |
| Q076.A03 | Shipping zero | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2361-2364, R814-816, BOARD-TRACKS |
| Q076.A04 | Manufacturing zero | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2361-2364, R814-816, BOARD-TRACKS |
| Q076.A05 | Standing £4, £6, £8 lined | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2361-2364, R814-816, BOARD-TRACKS |
| Q076.A06 | Debt five through eight lined | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2361-2364, R814-816, BOARD-TRACKS |
| Q076.A07 | Lined space permits vote | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2361-2364, R814-816, BOARD-TRACKS |
| Q076.A08 | Standing £4 starred | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2361-2364, R814-816, BOARD-TRACKS |
| Q076.A09 | Debt eight starred | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2361-2364, R814-816, BOARD-TRACKS |
| Q076.A10 | Starred space forces vote | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2361-2364, R814-816, BOARD-TRACKS |
| Q076.A11 | Standing £10 expectations | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2361-2364, R814-816, BOARD-TRACKS |
| Q076.A12 | Among the two zero-Power starting spaces, Manufacturing starts at the bottom/right and Shipping at the next/left space toward Company Share | supported | affirmed_requested_or_clearly_implied | R2588-2601, R2361-2364, R814-816, BOARD-TRACKS |

Q076.A12: The two zero-value spaces remain distinct positions on the native connected Power path.

### Q077 — 5 atoms; explicit_findings

According to the verified designer ruling, does unrest increase a Foreign Invasion primary attack or its resulting tower strength? What happens to orders?

The question asks whether unrest increases either quantity and what happens to orders. It does not ask for the base attack/tower formula; those formulas are explanatory context and Q054 directly requests them.

Original source evidence: R2297-2316, FOREIGN-DESIGNER.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q077.A01 | Unrest adds to neither | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER |
| Q077.A02 | Primary strength is ordinary attack die | supported | contextual_only | R2303-2312, FOREIGN-DESIGNER / FB-Q077-02 |
| Q077.A03 | Resulting tower strength is half die rounded down | supported | contextual_only | R2303-2312, FOREIGN-DESIGNER / FB-Q077-03 |
| Q077.A04 | On success close orders once | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER |
| Q077.A05 | Cascade only if all already closed | supported | affirmed_requested_or_clearly_implied | R2297-2316, FOREIGN-DESIGNER |

Existing optional key context (not promoted to mandatory): Secondary Company unrest attacks remain normal..

### Q078 — 7 atoms; affirmed

Which corrected card rules apply when Mercantile/Diplomatic Connection reduces dice to zero, Company Fraud would overdraw Balance, Public Demands Impeachment removes a holder, or Military Oversight demotes a Commander?

Each specified corrected-card edge case is requested. Fraud timing/dice/raw amount are optional here and directly asked by Q109.

Original source evidence: ERRATA-CARDS, FRAUD-DESIGNER, FRONTS-P1, FRONTS-P6.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q078.A01 | Mercantile or Diplomatic Connection reducing check to zero dice causes failure | supported | affirmed_requested_or_clearly_implied | ERRATA-CARDS, FRAUD-DESIGNER, FRONTS-P1, FRONTS-P6 |
| Q078.A02 | Balance cannot go below zero | supported | affirmed_requested_or_clearly_implied | ERRATA-CARDS, FRAUD-DESIGNER, FRONTS-P1, FRONTS-P6 |
| Q078.A03 | Payout equals actual Balance removed, not uncapped doubled roll | supported | affirmed_requested_or_clearly_implied | ERRATA-CARDS, FRAUD-DESIGNER, FRONTS-P1, FRONTS-P6 |
| Q078.A04 | Holder returns supply | supported | affirmed_requested_or_clearly_implied | ERRATA-CARDS, FRAUD-DESIGNER, FRONTS-P1, FRONTS-P6 |
| Q078.A05 | Card goes to Vacant Offices | supported | affirmed_requested_or_clearly_implied | ERRATA-CARDS, FRAUD-DESIGNER, FRONTS-P1, FRONTS-P6 |
| Q078.A06 | Commander becomes officer | supported | affirmed_requested_or_clearly_implied | ERRATA-CARDS, FRAUD-DESIGNER, FRONTS-P1, FRONTS-P6 |
| Q078.A07 | Former Commander eligible for reappointment | supported | affirmed_requested_or_clearly_implied | ERRATA-CARDS, FRAUD-DESIGNER, FRONTS-P1, FRONTS-P6 |

Existing optional key context (not promoted to mandatory): £10 Balance versus doubled six pays £10, not £12.; Company Fraud starts at Revenue.; Company Fraud rolls one die per own officeholder and uses twice highest roll..

### Q079 — 9 atoms; affirmed

In shared setup, what are the initial Company Balance and family VP positions, where do local alliances and loot tokens start, and how do you set the India map, Turn marker and Prime Minister arm for the chosen scenario?

Shared initial Balance/VP/alliance/loot locations and scenario-instruction/map/date/PM setup are explicit. It does not ask to enumerate every depicted initial region.

Original source evidence: R335-388, BACKS-P9.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q079.A01 | Balance five | supported | affirmed_requested_or_clearly_implied | R335-388, BACKS-P9 |
| Q079.A02 | Each family VP zero | supported | affirmed_requested_or_clearly_implied | R335-388, BACKS-P9 |
| Q079.A03 | Alliances in listed Army boxes | supported | affirmed_requested_or_clearly_implied | R335-388, BACKS-P9 |
| Q079.A04 | Loot tokens in matching regions | supported | affirmed_requested_or_clearly_implied | R335-388, BACKS-P9 |
| Q079.A05 | Loot cash side faceup | supported | affirmed_requested_or_clearly_implied | R335-388, BACKS-P9 |
| Q079.A06 | Follow scenario card front instructions | supported | affirmed_requested_or_clearly_implied | R335-388, BACKS-P9 |
| Q079.A07 | Follow Situation in India diagram | supported | affirmed_requested_or_clearly_implied | R335-388, BACKS-P9 |
| Q079.A08 | Turn marker on scenario date | supported | affirmed_requested_or_clearly_implied | R335-388, BACKS-P9 |
| Q079.A09 | PM arm points at matching date | supported | affirmed_requested_or_clearly_implied | R335-388, BACKS-P9 |

### Q080 — 3 atoms; affirmed

What is the normal turn phase order, where is the Firms phase inserted after Deregulation, and which normal phase is skipped on the first turn of a game?

Complete phase order, conditional Firms insertion and entire first-turn London skip are explicitly requested.

Original source evidence: R862-887, R898-900, R2679-2682.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q080.A01 | London Season → Family → Hiring → Company Operation → Bonuses → Revenue → Events in India → Parliament Meets → Upkeep and Refresh | supported | affirmed_requested_or_clearly_implied | R862-887, R898-900, R2679-2682 |
| Q080.A02 | Between Family and Hiring | supported | affirmed_requested_or_clearly_implied | R862-887, R898-900, R2679-2682 |
| Q080.A03 | Entire London Season skipped on first game turn | supported | affirmed_requested_or_clearly_implied | R862-887, R898-900, R2679-2682 |

Existing optional key context (not promoted to mandatory): Family includes creation of new Company shares..

### Q081 — 10 atoms; affirmed

During the Retirements step, who acts first if the Chairman office is vacant, what order follows, must pensioners retire, and how do pensioner, VP and retirement money move?

Chairman/former fallback, clockwise order, optional retirement and pensioner/VP/cash destinations/timing are all explicit.

Original source evidence: R917-928.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q081.A01 | Former Chairman first if office vacant | supported | affirmed_requested_or_clearly_implied | R917-928 |
| Q081.A02 | Otherwise Chairman first | supported | affirmed_requested_or_clearly_implied | R917-928 |
| Q081.A03 | Then clockwise | supported | affirmed_requested_or_clearly_implied | R917-928 |
| Q081.A04 | Retirement optional | supported | affirmed_requested_or_clearly_implied | R917-928 |
| Q081.A05 | Choose prize | supported | affirmed_requested_or_clearly_implied | R917-928 |
| Q081.A06 | Pay printed cost from family cash | supported | affirmed_requested_or_clearly_implied | R917-928 |
| Q081.A07 | Move pensioner to chosen prize | supported | affirmed_requested_or_clearly_implied | R917-928 |
| Q081.A08 | Increase VP by printed amount | supported | affirmed_requested_or_clearly_implied | R917-928 |
| Q081.A09 | Set retirement spending aside for display priority | supported | affirmed_requested_or_clearly_implied | R917-928 |
| Q081.A10 | Pay it to bank at end of London Season | supported | affirmed_requested_or_clearly_implied | R917-928 |

### Q082 — 6 atoms; explicit_findings

An empire loses its last dominated region while its capital remains. Does the capital keep its starred flag, and does the answer depend on whether the dominated region was lost to Rebellion or Company conquest?

The question asks capital flag disposition and whether the loss cause matters. That cleanup is required for both named causes; the explanatory label no longer an empire is not an additional mandatory sentence.

Original source evidence: R707-714, R1693-1703, R2216-2218.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q082.A01 | No | supported | affirmed_requested_or_clearly_implied | R707-714, R1693-1703, R2216-2218 |
| Q082.A02 | Return remaining capital flag to supply | supported | affirmed_requested_or_clearly_implied | R707-714, R1693-1703, R2216-2218 |
| Q082.A03 | Capital-only region ceases to be empire | supported | contextual_only | R707-714 / FB-Q082-03 |
| Q082.A04 | Same cleanup whenever last dominated region lost | supported | affirmed_requested_or_clearly_implied | R707-714, R1693-1703, R2216-2218 |
| Q082.A05 | Includes Rebellion | supported | affirmed_requested_or_clearly_implied | R707-714, R1693-1703, R2216-2218 |
| Q082.A06 | Includes Company conquest | supported | affirmed_requested_or_clearly_implied | R707-714, R1693-1703, R2216-2218 |

Q082.A01: Returning the capital flag clearly answers no; no separate literal no is required.

### Q083 — 6 atoms; affirmed

What final-scoring VP does each firm share earn or lose at each firm Value from 1 through 10?

All ten Value-to-VP outcomes are explicitly requested, not the broader fractional-totaling procedure.

Original source evidence: RULES42-CHARTER.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q083.A01 | Value 1: −1 per share | supported | affirmed_requested_or_clearly_implied | RULES42-CHARTER |
| Q083.A02 | Value 2: zero | supported | affirmed_requested_or_clearly_implied | RULES42-CHARTER |
| Q083.A03 | Values 3–4: half | supported | affirmed_requested_or_clearly_implied | RULES42-CHARTER |
| Q083.A04 | Values 5–7: one | supported | affirmed_requested_or_clearly_implied | RULES42-CHARTER |
| Q083.A05 | Values 8–9: one and a half | supported | affirmed_requested_or_clearly_implied | RULES42-CHARTER |
| Q083.A06 | Value 10: two | supported | affirmed_requested_or_clearly_implied | RULES42-CHARTER |

Existing optional key context (not promoted to mandatory): Total firm fractions before rounding down..

### Q084 — 3 atoms; affirmed

Who takes the first Family action turn, in which direction do the other players act, and when does the New Company Shares step begin?

First player, clockwise sequence and completion gate before New Shares are the exact requested facts.

Original source evidence: R1076-1082, R1135-1145.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q084.A01 | Chairman title holder first | supported | affirmed_requested_or_clearly_implied | R1076-1082, R1135-1145 |
| Q084.A02 | Then clockwise | supported | affirmed_requested_or_clearly_implied | R1076-1082, R1135-1145 |
| Q084.A03 | After all players complete Family actions | supported | affirmed_requested_or_clearly_implied | R1076-1082, R1135-1145 |

### Q085 — 3 atoms; affirmed

In what order do the Company offices operate, where does the Governor General fit, and what happens to a vacant office in that sequence?

Complete office sequence, GG replacement slot and vacant-office skip are requested. Internal Presidency sequencing is contextual here.

Original source evidence: R1331-1339, R1853-1857, R1816-1816, BOARD-RIBBON.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q085.A01 | Chairman → Director → Shipping → Military Affairs → Bombay → Madras → Bengal → China if created | supported | affirmed_requested_or_clearly_implied | R1331-1339, R1853-1857, R1816-1816, BOARD-RIBBON |
| Q085.A02 | GG replaces Director in that slot | supported | affirmed_requested_or_clearly_implied | R1331-1339, R1853-1857, R1816-1816, BOARD-RIBBON |
| Q085.A03 | Skip vacant office | supported | affirmed_requested_or_clearly_implied | R1331-1339, R1853-1857, R1816-1816, BOARD-RIBBON |

Existing optional key context (not promoted to mandatory): Detailed internal Presidency order.; Follow red ribbon left to right..

### Q086 — 12 atoms; affirmed

How does the Events in India phase begin, which ships face storm checks, and how is the number and order of India event tiles determined?

Storm opening/order, eligible ships/exemptions/zone mappings and die-controlled sequential event count are requested; no detailed storm result table is demanded here.

Original source evidence: R1939-1961, R1812-1815, R2919-2922.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q086.A01 | Roll storm die first | supported | affirmed_requested_or_clearly_implied | R1939-1961, R1812-1815, R2919-2922 |
| Q086.A02 | Resolve storms before India event tiles | supported | affirmed_requested_or_clearly_implied | R1939-1961, R1812-1815, R2919-2922 |
| Q086.A03 | Eligible player-owned ships in indicated zone | supported | affirmed_requested_or_clearly_implied | R1939-1961, R1812-1815, R2919-2922 |
| Q086.A04 | All zones for three storms | supported | affirmed_requested_or_clearly_implied | R1939-1961, R1812-1815, R2919-2922 |
| Q086.A05 | No checks for no storms | supported_by_clear_rule_implication | affirmed_requested_or_clearly_implied | R1939-1961, R1812-1815, R2919-2922 |
| Q086.A06 | Company ships exempt | supported | affirmed_requested_or_clearly_implied | R1939-1961, R1812-1815, R2919-2922 |
| Q086.A07 | Extra ships exempt | supported | affirmed_requested_or_clearly_implied | R1939-1961, R1812-1815, R2919-2922 |
| Q086.A08 | China ships count Eastern | supported | affirmed_requested_or_clearly_implied | R1939-1961, R1812-1815, R2919-2922 |
| Q086.A09 | Firm ships use chosen strategy zone | supported | affirmed_requested_or_clearly_implied | R1939-1961, R1812-1815, R2919-2922 |
| Q086.A10 | Hobnob ships exempt | supported | affirmed_requested_or_clearly_implied | R1939-1961, R1812-1815, R2919-2922 |
| Q086.A11 | Resolve number printed on storm-die face | supported | affirmed_requested_or_clearly_implied | R1939-1961, R1812-1815, R2919-2922 |
| Q086.A12 | Flip and resolve one draw-stack tile per event sequentially | supported | affirmed_requested_or_clearly_implied | R1939-1961, R1812-1815, R2919-2922 |

Q086.A05: No storm checks when the die shows no storms follows the die’s zone procedure; number of event tiles still follows its printed number.

Existing optional key context (not promoted to mandatory): Locations often use back of new top draw-stack tile, subject to event-specific rules..

### Q087 — 7 atoms; affirmed

For an ordinary Crisis event located by the Elephant, how are the attacker and defender identified and Invasion versus Rebellion chosen? Which map components identify sovereign and dominated regions?

Elephant attacker/defender and Crisis branch, including wholly-inside Company Rebellion, plus sovereign/dominated visual markers are requested.

Original source evidence: R698-701, R715-727, R2186-2212.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q087.A01 | Elephant tail identifies attacker | supported | affirmed_requested_or_clearly_implied | R698-701, R715-727, R2186-2212 |
| Q087.A02 | Elephant head identifies defender | supported | affirmed_requested_or_clearly_implied | R698-701, R715-727, R2186-2212 |
| Q087.A03 | Sovereign attacker means Invasion | supported | affirmed_requested_or_clearly_implied | R698-701, R715-727, R2186-2212 |
| Q087.A04 | Dominated attacker means Rebellion against sovereign | supported | affirmed_requested_or_clearly_implied | R698-701, R715-727, R2186-2212 |
| Q087.A05 | Elephant wholly inside Company region means Rebellion against Company | supported | affirmed_requested_or_clearly_implied | R698-701, R715-727, R2186-2212 |
| Q087.A06 | Large flag or unflagged dome sovereign | supported | affirmed_requested_or_clearly_implied | R698-701, R715-727, R2186-2212 |
| Q087.A07 | Small flag or no dome dominated | supported | affirmed_requested_or_clearly_implied | R698-701, R715-727, R2186-2212 |

### Q088 — 10 atoms; affirmed

Under this summary’s user-approved table interpretation, can an active strength-2 local alliance defend a strength-1 Crisis, what is exhausted and what success results apply? Can that alliance be used again that turn, and is this an official ruling or a general rule for other excess-strength cases?

The fixture, whole-alliance exhaustion, success consequences, non-reuse and user-only/general interpretation attribution are all directly requested. No private email inspection is assumed.

Original source evidence: R1617-1627, R2262-2296, HUMAN-DEFENSE, APPROVED-SCOPE.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q088.A01 | Yes under user interpretation | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2262-2296, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q088.A02 | Exhaust whole active strength-two alliance | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2262-2296, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q088.A03 | Clear target unrest | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2262-2296, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q088.A04 | Actual Commander gains trophy | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2262-2296, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q088.A05 | Acting Military Affairs or Chairman gains no trophy for successful defense | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2262-2296, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q088.A06 | Defeated normal primary Invasion loses one attacker tower if possible | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2262-2296, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q088.A07 | No reuse that turn | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2262-2296, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q088.A08 | Attribute to user-approved interpretation | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2262-2296, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q088.A09 | Do not present as independently verified official ruling | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2262-2296, HUMAN-DEFENSE, APPROVED-SCOPE |
| Q088.A10 | Newly exhausted total defense strength at least attack applies generally in this summary | supported | affirmed_requested_or_clearly_implied | R1617-1627, R2262-2296, HUMAN-DEFENSE, APPROVED-SCOPE |

Q088.A09: The question explicitly asks official status; do not require a volunteered source disclaimer in other defense questions that do not ask it.

Existing optional key context (not promoted to mandatory): Private publisher email has not been independently inspected.; Acting Military Affairs or Chairman loses no trophies on failed defense.

### Q089 — 3 atoms; affirmed

After resolving an ordinary Crisis, when does the Elephant March? Does a failed Invasion or either result of a Rebellion skip that movement?

The timing and all successful/failed ordinary Invasion/Rebellion cases are directly asked; March destination/posture is contextual to this row.

Original source evidence: R2186-2191.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q089.A01 | March after every ordinary Crisis | supported | affirmed_requested_or_clearly_implied | R2186-2191 |
| Q089.A02 | Both successful and failed Invasion trigger March | supported | affirmed_requested_or_clearly_implied | R2186-2191 |
| Q089.A03 | Both successful and failed Rebellion trigger March | supported | affirmed_requested_or_clearly_implied | R2186-2191 |

Existing optional key context (not promoted to mandatory): March destinations/postures.; Leader and Foreign Invasion movement exceptions..

### Q090 — 4 atoms; explicit_findings

When a non-Company Rebellion succeeds, what happens to the rebel region’s sovereignty, flag and orders, including when every order there is already closed?

Sovereignty, flag return and order closure/Cascade exception are explicitly requested. Cascade must be conditioned on orders already all closed, not after every successful closure.

Original source evidence: R2216-2219.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q090.A01 | Rebel becomes sovereign | supported | affirmed_requested_or_clearly_implied | R2216-2219 |
| Q090.A02 | Return rebel flag to supply | supported | affirmed_requested_or_clearly_implied | R2216-2219 |
| Q090.A03 | Close every open order in rebel region | supported | affirmed_requested_or_clearly_implied | R2216-2219 |
| Q090.A04 | Then perform Cascade | supported_only_with_the_question_and_key_condition | requested_precision_clarification | R2216-2219 / FB-Q090-04 |

Q090.A04: Condition is present in both exact question and expected answer. Finding is to prevent loss of that condition in standalone atom use, not to accuse the correct expected answer of unconditional Cascade.

Existing optional key context (not promoted to mandatory): Empire Decline when final dominated region lost..

### Q091 — 2 atoms; affirmed

Before players cast votes on a selected law, where is the Votes marker set and where does that starting support value come from?

Initial Votes marker position and source of starting support are requested; PM/read-aloud/detail-of-card-location are contextual here.

Original source evidence: R2365-2367.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q091.A01 | Before voting set Votes marker on track to selected law starting support | supported | affirmed_requested_or_clearly_implied | R2365-2367 |
| Q091.A02 | Use value printed on selected law | supported | affirmed_requested_or_clearly_implied | R2365-2367 |

Existing optional key context (not promoted to mandatory): PM performs the step and reads law aloud.; Printed support is at bottom right of selected law..

### Q092 — 6 atoms; affirmed

At what point in Revenue do firms pay expenses and dividends, in which order do trading and other firms act, and how are ties broken?

Start-of-Revenue placement, initiative/other firms order and windows/PM tiebreakers are all explicit.

Original source evidence: R2827-2830.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q092.A01 | Start of Revenue | supported | affirmed_requested_or_clearly_implied | R2827-2830 |
| Q092.A02 | Before Company expenses | supported | affirmed_requested_or_clearly_implied | R2827-2830 |
| Q092.A03 | Initiative order first | supported | affirmed_requested_or_clearly_implied | R2827-2830 |
| Q092.A04 | Then all other firms | supported | affirmed_requested_or_clearly_implied | R2827-2830 |
| Q092.A05 | Break ties by Managers windows | supported | affirmed_requested_or_clearly_implied | R2827-2830 |
| Q092.A06 | Then clockwise from Prime Minister | supported | affirmed_requested_or_clearly_implied | R2827-2830 |

Existing optional key context (not promoted to mandatory): Expense/dividend amounts and sources.; Investment phase timing.; Emergency merger payments..

### Q093 — 6 atoms; affirmed

How does the Governor General fund the Govern dice pool, is there a dice penalty, and what personal bonus follows success, including who receives it and where it comes from?

Funding treasury, paid-die rate/no penalty and bonus amount/recipient/source are explicitly requested. Bank sourcing is an ordinary take-a-bonus inference from the action and parallel personal bonus text, not a literal bank word in the Govern paragraph.

Original source evidence: R1864-1872, R1344-1354, R662-668, R1821-1823.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q093.A01 | GG own office treasury | supported | affirmed_requested_or_clearly_implied | R1864-1872, R1344-1354, R662-668, R1821-1823 |
| Q093.A02 | £1 per die | supported | affirmed_requested_or_clearly_implied | R1864-1872, R1344-1354, R662-668, R1821-1823 |
| Q093.A03 | No dice penalty | supported | affirmed_requested_or_clearly_implied | R1864-1872, R1344-1354, R662-668, R1821-1823 |
| Q093.A04 | £1 per Company-controlled region on success | supported | affirmed_requested_or_clearly_implied | R1864-1872, R1344-1354, R662-668, R1821-1823 |
| Q093.A05 | GG family receives bonus | supported | affirmed_requested_or_clearly_implied | R1864-1872, R1344-1354, R662-668, R1821-1823 |
| Q093.A06 | Take bonus from bank | supported_by_clear_rule_implication | affirmed_requested_or_clearly_implied | R1864-1872, R1344-1354, R662-668, R1821-1823 |

Q093.A06: The Govern paragraph says take £1, not literally from the bank. Bank source is inferred from personal-bonus convention and parallel office payouts; do not misquote LF1870 as containing bank.

Existing optional key context (not promoted to mandatory): Guaranteed Company revenue and other Govern outcomes..

### Q094 — 2 atoms; affirmed

Who may inspect facedown blackmail in the London Season Display when selecting a card, and under whose permission may other players inspect the facedown blackmail you hold during negotiations?

Both inspection permissions are explicit; there is no unconditional right to inspect another player’s held blackmail.

Original source evidence: R1003-1009, R779-785.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q094.A01 | The acting player choosing a London Season card may inspect any blackmail card in the display | supported | affirmed_requested_or_clearly_implied | R1003-1009, R779-785 |
| Q094.A02 | A holder may permit other players to inspect their facedown blackmail cards | supported | affirmed_requested_or_clearly_implied | R1003-1009, R779-785 |

### Q095 — 5 atoms; affirmed

May the Chairman increase Debt while allocating the Company Balance, and which voluntary-borrowing consent and track limits still apply to those interleaved advances?

Interleaving, free-three advances, each further majority consent, Chairman share and track end all directly answer the borrowing-limit question.

Original source evidence: R1403-1416.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q095.A01 | The Chairman may increase Debt while allocating Company Balance | supported | affirmed_requested_or_clearly_implied | R1403-1416 |
| Q095.A02 | Up to three advances need no shareholder consent | supported | affirmed_requested_or_clearly_implied | R1403-1416 |
| Q095.A03 | Each additional advance requires consent of players controlling a majority of Company shares | supported | affirmed_requested_or_clearly_implied | R1403-1416 |
| Q095.A04 | The Chairman counts as a share for that majority | supported | affirmed_requested_or_clearly_implied | R1403-1416 |
| Q095.A05 | Debt cannot advance beyond the end of its track | supported | affirmed_requested_or_clearly_implied | R1403-1416 |

### Q096 — 6 atoms; affirmed

Who receives the cash for ordinary Family-action purchases of a luxury, shipyard or workshop from supply, and for Shipping’s leasing of extra ships, fitting of shipyard ships or purchase of Company ships?

All six cash recipients are asked. Stating bank for all six suffices; individual amount/ownership discussion is not a separate requirement.

Original source evidence: R1107-1121, R1458-1471.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q096.A01 | Luxury purchase cash goes to the bank | supported | affirmed_requested_or_clearly_implied | R1107-1121, R1458-1471 |
| Q096.A02 | Shipyard purchase cash goes to the bank | supported | affirmed_requested_or_clearly_implied | R1107-1121, R1458-1471 |
| Q096.A03 | Workshop purchase cash goes to the bank | supported | affirmed_requested_or_clearly_implied | R1107-1121, R1458-1471 |
| Q096.A04 | Extra-ship lease cash goes to the bank | supported | affirmed_requested_or_clearly_implied | R1107-1121, R1458-1471 |
| Q096.A05 | Shipyard-ship fitting cash goes to the bank | supported | affirmed_requested_or_clearly_implied | R1107-1121, R1458-1471 |
| Q096.A06 | Company-ship purchase cash goes to the bank | supported | affirmed_requested_or_clearly_implied | R1107-1121, R1458-1471 |

### Q097 — 7 atoms; affirmed

For a President’s Trade check, what is the paid-dice rate and which treasury funds it? How much normal Company order revenue does each filled order generate, where does that revenue go, and how do revenue and personal bonuses change when the Company fills an order already filled by a firm that turn?

Rate/funding, ordinary full-order revenue/destination and the firm-filled half-rounded-down/unmodified-bonus exception are all explicit.

Original source evidence: R1344-1354, R1549-1575, R2817-2820, R2870-2879.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q097.A01 | Trade buys one die per £1 spent | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1549-1575, R2817-2820, R2870-2879 |
| Q097.A02 | The President’s office treasury funds those dice | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1549-1575, R2817-2820, R2870-2879 |
| Q097.A03 | Each ordinarily filled Company order generates its full listed value | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1549-1575, R2817-2820, R2870-2879 |
| Q097.A04 | Normal Company order revenue goes to Company Balance | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1549-1575, R2817-2820, R2870-2879 |
| Q097.A05 | The Company may fill orders already filled by firms during that turn | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1549-1575, R2817-2820, R2870-2879 |
| Q097.A06 | Such refilled orders pay half listed value rounded down to Company Balance | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1549-1575, R2817-2820, R2870-2879 |
| Q097.A07 | Normal President and placed-writer personal bonuses are unchanged by refilling | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1549-1575, R2817-2820, R2870-2879 |

### Q098 — 7 atoms; affirmed

Once a successful Deploy’s loot pool has been established, how is it distributed among surviving participants: what is the payment order and amount per round, how are regiments and local alliances handled, and what happens when cash runs out or remains?

Surviving participant eligibility, Commander-first/clockwise £1 rounds, bank shares for regiments/alliance pieces and repetition/cash exhaustion are explicitly requested.

Original source evidence: R1681-1692.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q098.A01 | Only participating surviving officers receive officer shares | supported | affirmed_requested_or_clearly_implied | R1681-1692 |
| Q098.A02 | The Commander is paid first: £1 Commander share plus £1 per own participating surviving officer | supported | affirmed_requested_or_clearly_implied | R1681-1692 |
| Q098.A03 | Other players receive £1 per participating surviving officer in clockwise order | supported | affirmed_requested_or_clearly_implied | R1681-1692 |
| Q098.A04 | Stop paying when no loot cash remains | supported | affirmed_requested_or_clearly_implied | R1681-1692 |
| Q098.A05 | After paying players, remaining cash pays the bank £1 per participating regiment | supported | affirmed_requested_or_clearly_implied | R1681-1692 |
| Q098.A06 | After paying players, remaining cash pays the bank £1 per participating local-alliance piece regardless of its strength | supported | affirmed_requested_or_clearly_implied | R1681-1692 |
| Q098.A07 | Repeat from the Commander’s share and officers while cash remains | supported | affirmed_requested_or_clearly_implied | R1681-1692 |

### Q099 — 2 atoms; affirmed

After a successful Company Deploy conquers a region containing the Elephant, what happens if the Elephant had been facing another region, and what does its new position indicate?

The conditional inward redirect and its intended Company Rebellion meaning are explicitly requested.

Original source evidence: R1697-1707.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q099.A01 | An Elephant in the conquered region that faced another region is moved to that region’s center | supported | affirmed_requested_or_clearly_implied | R1697-1707 |
| Q099.A02 | The centered Elephant indicates intended rebellion against the Company | supported | affirmed_requested_or_clearly_implied | R1697-1707 |

### Q100 — 7 atoms; explicit_findings

At the Company’s ordinary Revenue expense calculation, what costs £1 each, which military officeholder is excluded, and do ships assigned to China count?

Preserved review applies: full expense census/rates/Army/Commander/sea-zone/China qualifications required. A separate Balance-marker instruction and Eastern rationale are correct context, not extra requested clauses.

Original source evidence: R1903-1916, R1812-1815.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q100.A01 | Ordinary expenses lower Company Balance | supported | contextual_only | R1903-1906 / FB-Q100-01 |
| Q100.A02 | Each current Debt costs £1 | supported | affirmed_requested_or_clearly_implied | R1903-1916, R1812-1815 |
| Q100.A03 | Each regiment in an Army costs £1 | supported | affirmed_requested_or_clearly_implied | R1903-1916, R1812-1815 |
| Q100.A04 | Each officer in an Army costs £1 | supported | affirmed_requested_or_clearly_implied | R1903-1916, R1812-1815 |
| Q100.A05 | Commanders do not incur the officer expense | supported | affirmed_requested_or_clearly_implied | R1903-1916, R1812-1815 |
| Q100.A06 | Each ship in the three sea zones costs £1 | supported | affirmed_requested_or_clearly_implied | R1903-1916, R1812-1815 |
| Q100.A07 | China-assigned ships are included as Eastern sea-zone ships for expenses | supported | mixed_requested_and_contextual | R1812-1815, R1903-1906 / FB-Q100-07 |

Q100.A05: Commanders are excluded from the officer expense, not an exemption for the associated Army or its officers.

### Q101 — 5 atoms; affirmed

For an ordinary non-Hobnobbing firm’s dividend step, may a shareholder waive dividends on their shares and whose consent is needed? How is the dividend/special-retirement marker set, and where does remaining India-treasury cash go afterward?

Waiver scope/manager consent, actual-total dividend cube and track position plus India-to-London remainder are all asked.

Original source evidence: R2888-2918.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q101.A01 | A shareholder may decline payment on any number of their shares on any dividend | supported | affirmed_requested_or_clearly_implied | R2888-2918 |
| Q101.A02 | The firm manager must consent to that waiver | supported | affirmed_requested_or_clearly_implied | R2888-2918 |
| Q101.A03 | Set the dividend cube to the actual total cash paid out in dividends | supported | affirmed_requested_or_clearly_implied | R2888-2918 |
| Q101.A04 | Place that cube on the Company Balance track | supported | affirmed_requested_or_clearly_implied | R2888-2918 |
| Q101.A05 | Move all remaining India-treasury cash to that firm’s London treasury after dividends | supported | affirmed_requested_or_clearly_implied | R2888-2918 |

### Q102 — 2 atoms; affirmed

Once the game is over and Final Scoring is being resolved, may players play blackmail cards, and what is the exception?

Endgame blackmail ban and explicit card-text exception are the exact two requested facts.

Original source evidence: R843-847.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q102.A01 | Blackmail cannot be played once the game is over during Final Scoring | supported | affirmed_requested_or_clearly_implied | R843-847 |
| Q102.A02 | Explicit permission in a card’s text is the exception | supported | affirmed_requested_or_clearly_implied | R843-847 |

### Q103 — 7 atoms; affirmed

For the Director of Trade’s Special Envoy, what resources buy dice, at what rate, and with what dice penalty? In the subsequent transfer step, how many transfers are permitted, what moves in each, and which origins and destinations are eligible, including China?

Envoy cash treasury/rate/penalty and transfer number/type/origins/destinations/China eligibility are explicitly requested; no success-outcome expansion is required.

Original source evidence: R1344-1354, R1417-1433, R1812-1815.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q103.A01 | Special Envoy dice are bought with the Director’s office-treasury cash | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1417-1433, R1812-1815 |
| Q103.A02 | Each £1 buys one die | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1417-1433, R1812-1815 |
| Q103.A03 | Special Envoy has no dice penalty | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1417-1433, R1812-1815 |
| Q103.A04 | The subsequent transfer step permits up to two transfers | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1417-1433, R1812-1815 |
| Q103.A05 | Each transfer moves one writer or one ship | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1417-1433, R1812-1815 |
| Q103.A06 | Transfers move between Presidencies or sea zones | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1417-1433, R1812-1815 |
| Q103.A07 | China is an eligible sea zone for ship transfers | supported | affirmed_requested_or_clearly_implied | R1344-1354, R1417-1433, R1812-1815 |

### Q104 — 7 atoms; affirmed

During Military Affairs, how many Army transfers may be made, which piece and destination are allowed in each, and in which half of the Army box are transferred pieces placed? Must all officers-in-training be assigned, to which Armies, and into which half?

Transfer count/type/destination/top-half plus assignment of all trainees to any Army/top-half are explicitly requested.

Original source evidence: R1472-1484.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q104.A01 | Military Affairs may make up to two Army transfers | supported | affirmed_requested_or_clearly_implied | R1472-1484 |
| Q104.A02 | Each transfer moves one officer or regiment | supported | affirmed_requested_or_clearly_implied | R1472-1484 |
| Q104.A03 | A transfer moves from one Army to any other Army | supported | affirmed_requested_or_clearly_implied | R1472-1484 |
| Q104.A04 | Transferred pieces are in the top half of the destination Army box | supported | affirmed_requested_or_clearly_implied | R1472-1484 |
| Q104.A05 | Every piece in Officers-in-Training must be assigned | supported | affirmed_requested_or_clearly_implied | R1472-1484 |
| Q104.A06 | Each trainee may be assigned to any of the three Armies | supported | affirmed_requested_or_clearly_implied | R1472-1484 |
| Q104.A07 | New officers are placed in the top half of their Army box | supported | affirmed_requested_or_clearly_implied | R1472-1484 |

### Q105 — 3 atoms; affirmed

When placement makes writers from different Presidencies adjacent on connected orders, where must a Presidency divider be placed, and what does it preserve for Refresh?

Placement trigger, connecting route location and retained affiliation for Refresh directly answer the question.

Original source evidence: R1580-1582.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q105.A01 | Adjacent writers from different Presidencies trigger placing a divider | supported | affirmed_requested_or_clearly_implied | R1580-1582 |
| Q105.A02 | Place the divider on their connecting route | supported | affirmed_requested_or_clearly_implied | R1580-1582 |
| Q105.A03 | The divider preserves separate Presidency affiliation during Refresh | supported | affirmed_requested_or_clearly_implied | R1580-1582 |

### Q106 — 4 atoms; explicit_findings

When an ordinary Invasion Crisis causes Company Region Loss, what happens to that region’s orders, including if all are already closed? Does Region Loss impose a second order-closing/Cascade step for a loss caused by Rebellion or Foreign Invasion?

The ordinary Invasion closure/Cascade condition and no duplicate step for Rebellion/Foreign Invasion are asked. Explaining that those types already close orders is correct but not an independent required rationale.

Original source evidence: R1999-2007, FOREIGN-DESIGNER.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q106.A01 | Ordinary Invasion Crisis Company Region Loss closes every open order in the lost region | supported | affirmed_requested_or_clearly_implied | R1999-2007, FOREIGN-DESIGNER |
| Q106.A02 | Resolve a Cascade if all orders in that region were already closed | supported | affirmed_requested_or_clearly_implied | R1999-2007, FOREIGN-DESIGNER |
| Q106.A03 | Region Loss does not add a second closure/Cascade step for Rebellion or Foreign Invasion | supported | affirmed_requested_or_clearly_implied | R1999-2007, FOREIGN-DESIGNER |
| Q106.A04 | Rebellion and Foreign Invasion already close orders by their own procedures | supported | contextual_only | R1999-2007, FOREIGN-DESIGNER / FB-Q106-04 |

### Q107 — 4 atoms; affirmed

Within Firm Investments, is there a fixed player action order, and when do investment actions finish so that play can proceed to Firm Strategy?

No fixed order, anytime actions, no-further-wishes stopping gate and subsequent Strategy are requested; anytime is equivalent to no fixed order, not an extra response sentence.

Original source evidence: R2679-2688, R2773-2775.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q107.A01 | Firm Investments has no fixed player action order | supported | affirmed_requested_or_clearly_implied | R2679-2688, R2773-2775 |
| Q107.A02 | Players may take investment actions at any time during the step | supported | affirmed_requested_or_clearly_implied | R2679-2688, R2773-2775 |
| Q107.A03 | Investment actions finish when no player wishes to take further actions | supported | affirmed_requested_or_clearly_implied | R2679-2688, R2773-2775 |
| Q107.A04 | Firm Strategy follows the Firm Investments step | supported | affirmed_requested_or_clearly_implied | R2679-2688, R2773-2775 |

Q107.A02: No fixed order/anytime actions are equivalent parts of one requested rule; either clear statement can satisfy both.

### Q108 — 2 atoms; affirmed

After a normal negotiated merger has been agreed, what happens to the secondary firms’ ships and shareholders’ shares?

Only secondary ship/share consolidation into primary is asked; no unasked treasury or legality procedure is imported.

Original source evidence: R2750-2768.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q108.A01 | Secondary firms’ ships consolidate into the surviving primary firm | supported | affirmed_requested_or_clearly_implied | R2750-2768 |
| Q108.A02 | Secondary shareholders/shares consolidate into the surviving primary firm | supported | affirmed_requested_or_clearly_implied | R2750-2768 |

### Q109 — 3 atoms; affirmed

Under the corrected Company Fraud card, when may it be played, how many dice are rolled and for whose pieces, and how is the raw amount calculated from the roll before applying the Company Balance cap?

Corrected timing, own-officeholder dice and twice-highest raw amount are explicit; cap arithmetic is outside this question’s pre-cap request.

Original source evidence: ERRATA-FRAUD, FRONTS-P1.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q109.A01 | Company Fraud is played at the start of Revenue | supported | affirmed_requested_or_clearly_implied | ERRATA-FRAUD, FRONTS-P1 |
| Q109.A02 | Roll one die for each of your own officeholders | supported | affirmed_requested_or_clearly_implied | ERRATA-FRAUD, FRONTS-P1 |
| Q109.A03 | The raw amount is twice the highest die result | supported | affirmed_requested_or_clearly_implied | ERRATA-FRAUD, FRONTS-P1 |

### Q110 — 4 atoms; affirmed

After a successful Deploy, may the same Commander make further successful Deploy actions during that operation? Must further actions still satisfy the ordinary targeting/no-dead-action restrictions, and how do available active resources or catastrophic failure limit repetition?

Success repetition, continued target/no-dead-action rules, still-active resources and catastrophe stop are all explicit; success does not refresh exhausted resources.

Original source evidence: R1617-1647, R1341-1364.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q110.A01 | The same Commander may successfully Deploy again during the operation as many times as desired and affordable | supported | affirmed_requested_or_clearly_implied | R1617-1647, R1341-1364 |
| Q110.A02 | Further actions must use still-available active resources rather than reuse exhausted pieces | supported | affirmed_requested_or_clearly_implied | R1617-1647, R1341-1364 |
| Q110.A03 | The ordinary target/no-dead-action restrictions still apply to further Deploy actions | supported | affirmed_requested_or_clearly_implied | R1617-1647, R1341-1364 |
| Q110.A04 | Catastrophic failure ends that Commander’s operation | supported | affirmed_requested_or_clearly_implied | R1617-1647, R1341-1364 |

### Q111 — 4 atoms; affirmed

How often may a blackmail card’s effect be used, where and in what orientation is the card kept after use, and does using it remove any Power printed on that card?

One-use effect, retained card/player area/faceup and retained printed Power are explicit. Still counts clearly implies the relevant faceup/facedown Power rule; no separate recital of both orientations is required.

Original source evidence: R1039-1042, R821-822.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q111.A01 | A blackmail card’s effect may be used only once | supported | affirmed_requested_or_clearly_implied | R1039-1042, R821-822 |
| Q111.A02 | Keep the used card in its player’s area | supported | affirmed_requested_or_clearly_implied | R1039-1042, R821-822 |
| Q111.A03 | The used card is kept faceup | supported | affirmed_requested_or_clearly_implied | R1039-1042, R821-822 |
| Q111.A04 | Using the effect does not remove the card’s printed Power, which still counts at Final Scoring whether faceup or facedown | supported | affirmed_requested_or_clearly_implied | R1039-1042, R821-822 |

Q111.A04: “The printed Power still counts after use” suffices. It implies the relevant faceup rule; do not require an additional unrelated statement about unplayed facedown cards.

### Q112 — 9 atoms; affirmed

Who chooses whether and how many ordinary Company dividends are paid, what limits their affordability, which funds pay them, and what does each dividend cost and pay per share, including the Chairman? May an individual shareholder forgo payment as in a firm, and exactly when does total dividend payout increase Standing?

Every dividend choice/count/funding/affordability/cost/payout/Chairman/waiver/Standing threshold is explicitly requested. Equality is excluded by strictly greater.

Original source evidence: R1925-1934, R2895-2902.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q112.A01 | The Chairman chooses whether to pay ordinary Company dividends | supported | affirmed_requested_or_clearly_implied | R1925-1934, R2895-2902 |
| Q112.A02 | The Chairman may pay multiple dividends | supported | affirmed_requested_or_clearly_implied | R1925-1934, R2895-2902 |
| Q112.A03 | Dividend payments must fit within available Company Balance | supported_by_clear_rule_implication | affirmed_requested_or_clearly_implied | R1925-1934, R2895-2902 |
| Q112.A04 | Company Balance funds the dividends | supported | affirmed_requested_or_clearly_implied | R1925-1934, R2895-2902 |
| Q112.A05 | Each dividend costs the total number of Company shares | supported | affirmed_requested_or_clearly_implied | R1925-1934, R2895-2902 |
| Q112.A06 | Each dividend pays every shareholder £1 for each Company share owned | supported | affirmed_requested_or_clearly_implied | R1925-1934, R2895-2902 |
| Q112.A07 | The Chairman counts as a Company share for dividend cost and payout | supported | affirmed_requested_or_clearly_implied | R1925-1934, R2895-2902 |
| Q112.A08 | Individual Company shareholders cannot use the firm dividend-waiver permission | supported | affirmed_requested_or_clearly_implied | R1925-1934, R2895-2902 |
| Q112.A09 | Advance Standing one space when total cash paid in dividends is strictly greater than Expectations | supported | affirmed_requested_or_clearly_implied | R1925-1934, R2895-2902 |

Q112.A03: Affordability is the ordinary cash-availability implication of paying from Company Balance, not permission to borrow for dividends.

### Q113 — 2 atoms; affirmed

Where is the opportunity marker at the start of a game, and can the first chosen main Family action be taken twice under the marker’s normal repeat rule?

Initial marker absence and inability to double the first normal action directly answer the question; the second is a clear implication of the first and the phase-start repeat rule.

Original source evidence: R1080-1088.

| Atom | Exact current mandatory fact | Source truth | Asked scope | Evidence / finding |
|---|---|---|---|---|
| Q113.A01 | At game start the opportunity marker is not on any Family action | supported | affirmed_requested_or_clearly_implied | R1080-1088 |
| Q113.A02 | The first main Family action cannot be doubled under the opportunity marker’s normal repeat rule | supported_by_clear_rule_implication | affirmed_requested_or_clearly_implied | R1080-1088 |

Q113.A02: Clear implication of no initial action placement plus the start-of-phase repeat condition is sufficient.

## Source quote and graphic-transcription appendix

LF indices refer to the original extraction split on literal newline (`text.split("\n")`), not `splitlines()`. Native graphic transcriptions are identified as such and are not presented as prose quotations.

### R901-916

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p11; physical LF901–916

> Attrition
> This step should be completed simultaneously by all players. 
> Roll one die for each office card you hold. Each fatigue on a card adds +1 to the 
> result of that office’s die roll. The result determines what happens:
> 	
> Ƙ 1 or 2: Nothing happens.
> 	
> Ƙ 3 or 4: Add a fatigue to the office card.
> 	
> Ƙ 5 or more: That officeholder retires. Move the family member holding 
> that office to the Pensioners box on the board. Then, flip the office card 
> to its vacant side and place it in the Vacant Offices box nearby. Any 
> fatigue that was on the office card should be returned to the supply.
> 	
> M The Stress of Being Chairman. When rolling for the Chairman, add 
> +1 to the result.

### R1002-1014

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p12; physical LF1002–1014

> Prestige Cards
> Beginning with the player who spent the most total cash on retirements this turn, 
> each player who retired at least one pensioner this turn must take or discard one 
> card from the London Season Display. Any ties are broken in favor of most total 
> window icons (including from retirements this turn!) and then in Prime Minister order 
> (clockwise, starting with the Prime Minister). 
> When choosing their card, the acting player is welcome to peek at any blackmail 
> card in the London Season Display.
> If there are no cards remaining in the display, all remaining players are skipped. 
> Then, discard any remaining cards and refill the London Season Display to three 
> cards. Place blackmail cards facedown. Place regular prestige cards faceup. Note: 
> this is done even if there were no cards taken this turn!
> Lastly, return any family members in the Pensioners box to their supplies. 

### R2651-2658

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p37; physical LF2651–2658

> Special Retirement
> During the London Season phase, each player with at least one firm share 
> may take one additional retirement using a piece from their supply instead 
> of a pensioner. The total amount of money spent for this retirement 
> cannot exceed the value of the highest total dividend paid out by a 
> firm in which they own a share. This retirement is otherwise like any 
> other retirement a player can make with a pensioner. Note: even if a 
> player owns shares in multiple firms, only one special retirement can be taken! 

### R917-928

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p11; physical LF917–928

> Retirements
> Starting with the Chairman (or former Chairman if the office is vacant) and 
> going clockwise, each player may retire their pensioner(s). For each pensioner, 
> choose a prize on the left side of the board, pay the cost indicated on the top left 
> of the prize box, and move your pensioner to that box. Increase your victory 
> point marker by the amount listed.
> Note: most prizes also have an upkeep value listed to the right of their cost which must be 
> paid during the Upkeep and Refresh phase. In addition, many prizes also have window 
> tax icons, which may need to be paid for during the Parliament Meets phase. 
> Instead of paying the cost of your retirements directly to the bank, set it near 
> your player area. It will be used to determine turn order in the next step and 
> should be paid to the bank at the end of the London Season.

### R1076-1104

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p13; physical LF1076–1104

> II. Family
> This phase has two steps. First, all players will take their family action. Then, new Company 
> shares may be created.
> Family Action
> Starting with the player with the Chairman title and proceeding clockwise, each player 
> selects one family action from those listed in this section and places their opportunity 
> marker on the action they choose. (Note: at the start of the game, this marker is not on any action.) 
> Out of Family Pieces? If you need to place a family piece but have none, you must choose 
> to take one from any prize. If taken from a prize, lower your victory point marker by the 
> printed value of that prize. (Note: this rule also applies to creating Firm shares in Deregulation.)
> If a player’s opportunity marker was already on the action they chose at the start of this 
> phase, they may take that action twice instead. Example: your opportunity marker is on the 
> purchase shipyard action. This turn you could take that action twice. If you take a different action, 
> you will only take it once.
> 	
> M Extra Actions. Some laws enable players to take an additional action after they 
> have taken their main action. Only the most recently-passed extra action can be 
> used. This action does not benefit from a player’s opportunity marker, nor does 
> a player move their opportunity marker to the space corresponding to the extra 
> action. 
> 	
> M No Action. Rarely, players may be unable to take a family action. In these cases, 
> no action is taken and their opportunity token should be placed in their supply 
> of pieces. In practice this only happens if a player has no family pieces, prizes, or money. 
> Enlist Writer
> Place one family member in one of the three regional Writers boxes. If there are four 
> or more vacant offices, you may place an additional writer once this turn. This might 
> allow you to place two or three writers in a turn depending on the location of your opportunity 
> marker. 

### R1128-1145

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p14; physical LF1128–1145

> Seek Share
> Place a family member on an empty space on the Stock Exchange track 
> above the Court of Directors and pay the price printed on that space to 
> the bank. These family members may become shares at the end of the 
> Family phase. Once shares, they may provide income through dividends 
> and will be worth victory points at the end of the game if the Company 
> survives. If the Company fails, they will cost victory points instead.
> New Company Shares
> Once all players have completed their turn, check to see if any family members 
> on the Stock Exchange track are added to the Court. One will be added for 
> each Company Debt as described below.
> If the Company has Debt, move the rightmost family member on the Stock 
> Exchange into the Court box and lower the Company Debt marker by one. 
> A family member in the Court is called a Company share. If Company Debt 
> remains, repeat this step again. 
> Finally, if there are still pieces in the Stock Exchange track but no Company 
> Debt, slide rightward all remaining family members on the Stock Exchange as 
> far as possible, preserving their order.

### R1146-1169

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p14; physical LF1146–1169

> III. Hiring
> In this phase, all vacant offices in the Company are filled through hiring. 
> General Hiring Procedure
> Offices are hired in ascending order using the number on the back of each office 
> card. Vacant offices can only be hired by certain officeholders who choose from 
> a specific pool of candidates. The hiring office and the available candidates are 
> listed on the back of the office card. Once a candidate is hired, move that family 
> member to the new office and give that player the matching office card. 
> 	
> M Nepotism. You may select your own family member to hire, but you 
> must have the verbal consent of every other player in that office’s 
> candidate pool. This does not apply to electing the Chairman.
> 	
> M Promotions. Some higher offices (like the Director of Trade) are hired 
> from family members who already hold offices. Whenever a family 
> member is promoted in this way, their previously held office card 
> should be flipped over and added to the stack of vacant offices in the 
> appropriate order (ascending). Any fatigue tokens on the promoted 
> officeholder’s previous card are moved over to the new office card.
> No Candidates or Hirer? In some circumstances there may be no eligible 
> candidates for an office. When this happens the office is skipped in the hiring 
> process and will remain vacant through the turn, taking no actions (including 
> hiring others). If the office responsible for hiring a candidate is vacant, that 
> office is skipped.

### R1175-1190

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p15; physical LF1175–1190

> Chairman
> Any player with a Company share may attempt to become the new Chairman. To be 
> elected the new Chairman you need consent from players that control a majority of 
> the current Company shares.
> At the start of the election, the former Chairman should declare the number of 
> Company shares required to achieve a pure majority (more than half of total). Then, 
> any player is welcome to campaign for their candidacy. As soon as a candidate has the 
> required number of supporting Company shares, the election is over, and that player 
> is chosen as the new Chairman. 
> The newly-elected Chairman takes the Chairman marker and moves one of their 
> Company shares to the Chairman slot on the board. This piece still counts as a 
> Company share, but cannot be traded in a negotiation or used for firm investments 
> (if playing with Deregulation).
> If no candidate can receive the necessary support, the former Chairman picks any 
> player with at least one Company share to become the new Chairman, including 
> themselves. This choice is not subject to the Nepotism rule.

### R1331-1365

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p17; physical LF1331–1365

> IV. Company Operation
> Starting with the Chairman, each Company office acts in order, left to right, 
> following the red ribbon on the game board. The Chairman is responsible for 
> making sure players realize whose turn it is to act and that this phase proceeds 
> in a timely fashion. Use of a gavel or bell is encouraged.
> 	
> M Vacant Offices. Sometimes offices will remain vacant if there were no 
> eligible candidates to hire or if the hiring office was vacant. In this 
> case, the office is skipped.
> 	
> M No Dead Actions. A player cannot take an action that would have no 
> effect or chance of success e.g. trading without having a ship to fill an order 
> or deploying without a dice to trigger potential officer losses.
> Success Checks
> Doing business in India is risky. Most actions that concern India require the 
> acting player to make a check to see if their actions are successful. Each check 
> requires a roll of the dice. The number of dice you roll is dependent on the 
> resources you have and want to spend as determined by the action. Any money 
> spent comes from the office’s treasury and is paid to the bank.
> When making a check, first, decide on the amount of resources you want to 
> spend or exhaust, and gather the appropriate number of dice equal to the 
> amount shown on the office card. 
> Then, remove dice equal to the penalty. Finally, roll the dice. Use the lowest 
> rolled value to determine one of three results.
> 	
> Ƙ 1 or 2 is a success.
> 	
> Ƙ 3 or 4 is a failure. The check may be attempted again if there are 
> sufficient resources.
> 	
> Ƙ 5 or 6 is a catastrophic failure. The office will take no further actions. 
> The acting officeholder is immediately returned to its player’s supply, 
> and that office card is flipped and placed in the Vacant Offices box. Any 
> fatigue that was on the office card should be returned to the supply. 
> Note: some offices will use the result of a check in other ways, as detailed in their rules.

### R1403-1416

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p18; physical LF1403–1416

> Chairman
> The Chairman may first increase Company Debt and then must allocate the 
> Company Balance.
> You may advance the Company Debt marker up to three times. For each 
> advance, increase the Company Balance by £5. If you wish to advance the Debt 
> marker additional times, you must have the consent of players who control a 
> majority of Company shares for each additional advancement (Remember: the 
> Chairman counts as a share for this purpose!). The Chairman may not advance the 
> debt beyond the end of the track. 
> Then, allocate all funds on the Company Balance track to any other office 
> treasuries. Reduce the marker on the Company Balance track by the amount 
> transferred and add it to the respective office treasuries. Note: a Chairman may 
> wish to increase Debt as they allocate to make it easier to plan. As long as they follow the 
> rules for taking debt described in the previous paragraph, this is fine. 

### R1457-1471

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p19; physical LF1457–1471

> Manager of Shipping
> The Manager of Shipping fits, buys, and leases ships on behalf of the Company.
> You must spend funds in your treasury until it has at most £2 remaining. Funds 
> can be spent to: 
> 	
> Ƙ Lease Extra Ships. Pay £2 to the bank to place an extra ship from the 
> general supply in a sea zone. Extra ships are ships on short-term leases 
> that will be returned to the supply during the Refresh step.
> 	
> Ƙ Fit Ships on Shipyards. Pay £3 to the bank to take a ship from a shipyard 
> and place it in any of the three sea zones. Note: this does not require the 
> shipyard owner’s consent.
> 	
> Ƙ Buy Company Ships. If there are no ships on shipyards, pay £5 to the 
> bank and place a Company ship from the general supply in a sea zone.

### R1812-1815

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p25; physical LF1812–1815

> Unlike a President’s treasury, the Superintendent’s treasury only contains ships. 
> Ships can be sent here by the Manager of Shipping or the Director of Trade as if 
> it were a sea zone. These ships count as if they were in the Eastern sea zone for 
> storms, expenses, events, and laws.

### R1540-1582

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p20,21; physical LF1540–1582

> Trade
> You may fill open orders in India using the Trade action, starting from 
> your Presidency’s home port and continuing through any open orders 
> you fill. The Trade action may be taken before or after the Commander 
> or each Governor. The procedure for trading is as follows:
> 1.	 Declare the regions in which you wish to trade. You must include 
> your home region and cannot include regions that you could not 
> trade in because you do not have enough ships or because you 
> could not fill an order because a connecting order is closed.
> 2.	 Make a check. Each £1 you spend gives you one die. Subtract one 
> for each region outside of your home region that you declared in 
> step 1 from your total dice.
> Reminder: as with any check, if it is unsuccessful, you may attempt it again 
> during your Presidency Operations so long as you have sufficient resources for 
> another check and the check did not end in catastrophic failure.
> If successful, place one writer on an open, empty order space for each 
> ship in this Presidency’s sea zone. You must place as many writers as 
> possible, but can only place them in the declared regions. The first writer 
> must be placed on the Presidency’s home port (marked with a thick black 
> line). After that order is filled, additional writers must be adjacent to a 
> writer you already placed. For each order filled, increase the Company 
> Balance by the amount listed on the order. 
> 	
> M Out of Writers? If all writers have been placed and ships remain 
> to fill additional orders, place filled order tokens (on the reverse 
> of the closed order token) on the orders to show they have been 
> filled.
> 	
> M Home Region Privileges. A President may not fill an order in 
> another President’s home region (even if that President is vacant).
> 	
> M One Trade. Each President may only successfully trade at most 
> once per game turn. 
> Then, you take £1 from the bank for each order you filled.
> Finally, each player takes £1 from the bank for each of their writers you 
> placed on an order.
> 20
> 
> 
> --- Page 21 ---
> The Association of Writers: If a writer is ever placed on an order adjacent to a writer 
> from a different Presidency, place a Presidency divider on the connection so that the 
> affiliation of writers is kept separate during the Refresh step.

### R1617-1650

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p22; physical LF1617–1650

> Commanders
> First, you may request funds from your President to purchase any local alliances 
> located in your Army box and shift them to the top of the Army box. The cost of each 
> is listed on the alliance piece and is paid from your President’s treasury.
> 	
> M Local Alliances. Local alliances are temporary Army pieces. Their strength 
> can be used for two purposes: the Deploy action and to defend against 
> threats in India during the Events in India phase. Each piece can only be 
> used once on the turn they are purchased, and its strength cannot be split 
> among more than one purpose. 
> Then you may take the Deploy action as many times as you wish and can afford.
> Deploy 
> The procedure for deploying is as follows:
> 1.	 Select a target. You may select your President’s home region, a region 
> associated with your Presidency, or a region that shares a border with 
> a region associated with your Presidency. You cannot target another 
> President’s home region or a Company-controlled region associated 
> with another Presidency. Remember: you cannot take actions that would 
> have no effect if you were successful and therefore you cannot declare a 
> Company-controlled region unless it has at least one closed order or one unrest.
> 2.	 Make a check. Each officer or regiment you exhaust gives you one 
> die. In addition, each local alliance in your Army you exhaust will 
> give you the number of dice indicated on the piece. To exhaust an 
> officer, regiment, or local alliance, move it to the bottom half of its 
> respective Army box. Subtract the strength of the region from your 
> total number of dice. If the region is part of an empire, also subtract 
> the strength of every region associated with it. Remember: as with any 
> check, if it is unsuccessful, you may attempt it again so long as it did not end 
> in catastrophic failure and you have sufficient resources. Also, note that regions 
> that are Company-controlled never reduce your dice as they have a strength of 
> zero when defending.
> 3.	 Check for losses. Each player must roll a die for each of their officers 
> that were exhausted in this action (never regiments!). For each 6 rolled, 
> they must return one of their officers to their supply. 

### R707-711

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p7; physical LF707–711

> When a region conquers another region, it either forms an empire or expands its 
> existing empire. All empires are composed of one capital region (marked by a 
> flag with a star) and at least one dominated region (marked by a smaller version 
> of that flag). Empires combine the strengths of their regions when attacking 
> and defending in many situations, as described later in the rules.

### R1651-1666

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p22; physical LF1651–1666

> DEPLOYING
> The Commander of Madras is taking the Deploy 
> action. Their options are Madras (Company-
> controlled), Hyderabad, and Mysore. 
> Though Madras has a closed order which a 
> Deploy action could open, the Commander 
> is looking to make a profit. Mysore would 
> generate £9 loot with 3 strength (since it is part 
> of an empire based in Bombay). Hyderabad 
> would generate £15 loot with 2 strength. 
> The Commander decides to attack Hyderabad 
> and exhausts 3 officers and 2 regiments for 5 
> dice. Two dice are subtracted because of the 
> region’s strength. The roll is a success. 
> Then, all players with officers used in the Deploy must 
> check for losses. No sixes are rolled so all are safe.

### R1648-1650

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p22; physical LF1648–1650

> 3.	 Check for losses. Each player must roll a die for each of their officers 
> that were exhausted in this action (never regiments!). For each 6 rolled, 
> they must return one of their officers to their supply. 

### R1674-1710

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p23; physical LF1674–1710

> If successful, perform the following steps: 
> 1.	 Divide Loot. Gather cash from the bank based on the target region: 
> Each Tower Level
> Loot Modifier (if faceup)
> +£4
> +£4 to +£9
> 	
> M Loot Minimum. If there is less cash than the number of 
> officers + 1 (that were used in this action and that survived), 
> increase it by the difference from the bank. 
> Distribute this cash among those that participated and survived the 
> Deploy action. First, give yourself £1 (the Commander’s share) and £1 
> for each of your officers. Then continue clockwise to the next player 
> and give them £1 for each of their officers. Continue clockwise in this 
> fashion until all players with officers have been paid or no further 
> cash remains. After paying players, if cash remains, give £1 to the 
> bank for each regiment and local alliance (regardless of strength). If 
> cash remains, continue distributing as described, starting with your 
> Commander’s share and officers.
> 2.	 Take Trophies. Take one trophy token for each level in the targeted 
> region’s tower (since you are the Commander). Then, remove the tower 
> and dome. If it was a capital, remove all matching flags. 
> 3.	 Impose Order. Open all orders and remove any unrest in the region. 
> 4.	 Form Governorship. If the region is not Company-controlled, 
> move the region’s loot/control token to the space above the 
> President’s box with the region symbol side faceup. This region is 
> now associated with this President. Place the matching Governor 
> overlay in the region. Finally, take the matching Governor card 
> from the stack of unused offices and place it in the Vacant Offices 
> box. This region is now Company-controlled.
> 	
> M Elephant Redirect. If the Elephant was in the invaded region and 
> faced another region, place it in the center of the invaded region 
> to show that it now intends to rebel against the Company.
> If the Deploy action is a catastrophic failure, first return half (rounding 
> up) of your trophies to the supply and return the Commander to your 
> supply. 

### R1742-1771

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p24; physical LF1742–1771

> Governors
> Governors are created through the Deploy action. 
> Governors take a series of Administer actions using a diminishing dice pool. 
> First, take dice equal to the number listed on the office card. Then you may take 
> an Administer action.
> Administer
> Make a check using the number of dice remaining in the pool. There is 
> no penalty.
> If successful, take £1 then choose one of the three following options. If 
> the previous roll was not a success, take an additional £1. 
> 	
> Ƙ Build Company Ship. Building a ship occurs over two successful 
> actions. If there is no Company ship in your region, place one there. If 
> there is already a Company ship in your region, move that ship to the 
> sea zone associated with your President. Note: a ship in a region represents 
> a ship that is partially built and has no other effect. 
> 	
> Ƙ Commission Regiment. Place a regiment from the supply in the Army 
> associated with your President. Regiments are treated as officers, but 
> any loot they earn is paid to the bank and they cannot be removed 
> through a loss check.
> 	
> Ƙ Tax. Add £2 from the bank to either the Company Balance or your 
> President’s treasury. You may not split this amount. Each time you 
> choose this after your first time this turn, add one unrest to the 
> region. 
> If the check did not succeed, add an unrest to the region. 
> Then lower the number of dice in the pool by 1 regardless of its result. 
> You may continue taking actions until one the following happens: you 
> roll a catastrophic failure, you run out of dice, or you decide to stop.

### R1361-1365

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p17; physical LF1361–1365

> Ƙ 5 or 6 is a catastrophic failure. The office will take no further actions. 
> The acting officeholder is immediately returned to its player’s supply, 
> and that office card is flipped and placed in the Vacant Offices box. Any 
> fatigue that was on the office card should be returned to the supply. 
> Note: some offices will use the result of a check in other ways, as detailed in their rules.

### R1897-1934

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p27; physical LF1897–1934

> VI. Revenue
> During the Revenue phase, the Company will pay expenses, check expectations, 
> and then pay dividends. 
> During this phase, the Company’s Standing will often be adjusted. If the 
> Standing marker is moved to the leftmost position of the Standing track, the 
> Company has failed. Go to the Final Scoring immediately (page 9). 
> Expenses
> First, lower the Company Balance marker by £1 for each debt as indicated by 
> the Company Debt track, each regiment and officer in an Army (do not include 
> Commanders), and each ship in the three sea zones.
> 	
> M Emergency Loans. If the Company cannot pay its expenses, emergency 
> loans must be taken to cover those expenses. For each emergency loan 
> taken, move the Company Debt marker one space to the right and 
> add £5 to the Company Balance track. If the Company Debt marker 
> is already on the rightmost space, you still take out emergency loans 
> but do not advance the Company Debt marker further. Do this until 
> all expenses have been met. Emergency loan advancements of the 
> Company Debt marker do not incur expenses during this game turn. 
> Finally, set the Company Balance to zero.
> 	
> M Public Embarrassment. Lower the Company’s Standing one space to 
> the left if one or two emergency loans were taken this turn. Lower it 
> two spaces if three or more emergency loans were taken this turn.
> Check Expectations
> Next, lower the Company’s Standing one space to the left if the Company 
> Balance is less than the Expectations value listed beneath the Company’s 
> Standing.
> Pay Dividends
> Finally, the Chairman may pay out dividends.
> The cost of each dividend is equal to the number of Company shares. When 
> a dividend is paid, lower the Balance by an amount equal to the number of 
> Company shares. Each player takes £1 for each of their Company shares. 
> Multiple dividends may be paid. Remember: the Chairman counts as a Company 
> share for dividends.
> 	
> M Public Enthusiasm. Advance Standing one space to the right if more 
> total cash was paid in dividends than Expectations. 

### R2262-2296

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p33; physical LF2262–2296

> Attacks Against the Company
> Both Invasions and Rebellions against Company-controlled regions are 
> resolved the same way. Whenever attacked by any type of Crisis, the 
> Company must resolve the Crisis (called the primary Crisis) and then must 
> resolve an additional Rebellion Crisis in each other region with unrest 
> cubes using the following rules:
> 	
> Ƙ Order of Resolution. Always resolve the primary Crisis first. Then, 
> starting with the Commander of the Army of Bombay and proceeding 
> downwards, each Commander resolves attacks in regions associated 
> with their Presidency in any order. 
> 	
> M Vacant Commander. If the Commander is vacant, Military 
> Affairs will act in its stead (choosing which pieces to exhaust etc.) If 
> that office is also vacant, the Chairman will choose. The player 
> acting as Commander will not lose or gain trophies. 
> 	
> Ƙ Attack Strength. In the primary Crisis, calculate strength depending 
> on the Crisis type (Invasion or Rebellion). In addition, add one to 
> the strength for every unrest in this region. In other regions, the 
> strength of each Rebellion is equal to the number of unrest in that 
> region. 
> 	
> Ƙ Mounting Defense. The Commander associated with the region 
> must exhaust pieces in the Army equal to the strength of the Crisis 
> or as many as possible. If the newly-exhausted pieces do not equal 
> the strength of the Crisis, the Crisis succeeds. Perform the steps of 
> Region Loss (page 29). 
> If the attack failed, remove all unrest in the attacked region and the 
> Commander associated with the region should take a trophy token. 
> 	
> M Failed and Successful Invasions. If the primary Crisis was an 
> Invasion that failed, remove one tower level from the attacking 
> region if possible. If it was successful follow the rules of empire 
> creation and growth as described on the previous page.

### R2192-2219

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p32; physical LF2192–2219

> Invasion 
> If the attacker is a sovereign region, resolve an Invasion. Determine 
> whether the attacker’s strength (including the strength of any other regions 
> in its empire) plus the modifier listed on the event tile is greater than 
> the defender’s strength (including the strength of any other regions in its 
> empire). If so, the Invasion is successful; otherwise, the Invasion fails. 
> If the Invasion succeeded, remove any flag on the defending region’s 
> dome and place a flag matching the attacker. 
> 	
> M Shattered Empire. If the defending region was a capital, any 
> flags matching its empire are returned to the supply. 
> 	
> M New Empire. If the attacker was successful and does not have a 
> flag, place any flag with a star still in the supply on their dome. 
> If none remain, a new empire cannot be formed and no flag is 
> added to the attacker or defender.
> If the Invasion failed, remove one tower level from the attacker.
> Rebellion
> If the attacker is a dominated region, resolve a Rebellion. In a 
> Rebellion, the Crisis is only between a dominated region and the region 
> that dominates it (other regions in the empire have no impact!). Determine 
> whether the attacker’s strength plus the modifier listed on the event 
> tile is greater than the defender’s strength. If so, the Rebellion is 
> successful; otherwise it fails. 
> When a Rebellion is successful the attacking region is now sovereign. 
> Return its flag to the supply. Then, close every open order in the 
> attacking region. If all are already closed, resolve a Cascade.
> If the Rebellion failed, remove one tower level from the capital.

### R2570-2587

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p36; physical LF2570–2587

> Resolving the Vote
> When voting stops, the law passes or fails depending on the position of the Votes 
> marker. There are two possible outcomes: 
> 	
> Ƙ If the law has -1 support or less, it fails. Discard the law, resolving any “If 
> Failed” effects if it is a dilemma. Then, the player with the Opposition 
> Leader token returns it to the supply and takes the Prime Minister wheel. 
> Finally, the new Prime Minister moves the selected policy to either adjacent 
> space on the Policy track and then resolves its effect.
> 	
> Ƙ Otherwise, the law passes. Place the law near the board next to the other 
> passed laws. The Prime Minister should take a passed law token into their 
> play area. Then, resolve the policy consequence in the space selected and 
> then any immediate effects of the law.
> Finally, return any cards used for votes to their regular orientation.
> 	
> M Legislated Company Failure. If a law causes the Company to fail, the 
> game is over. Finish resolving the vote then perform Final Scoring.

### R2588-2601

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p36; physical LF2588–2601

> The Vote to Deregulate
> In the 1758 and long 1710 scenarios, the Prime Minister may initiate a special session 
> of Parliament at the start of the turn before the London Season phase. To do this, 
> the Company Standing marker and/or Company Debt marker must be on a lined 
> space. If at least one of these markers is on one of the spaces marked with a star, the 
> Prime Minister must initiate a special session to vote on Deregulation. 
> If the vote passes, lower Company Debt one space for every two Debt and place the 
> Standing marker on the space marked “S.” The Prime Minister gains a passed law 
> token. Refer to the Deregulation rules for additional changes. 
> If the law fails, increase the value of Company shares by placing (or flipping) the 
> Company share victory point token in the Court. Shares cannot be worth more 
> than +/-3 victory points. Unlike other proposed laws, this law is not associated 
> with a policy. If it fails, the current Prime Minister will remain in power and this 
> law is not discarded. The Prime Minister may also vote against the law.

### R2626-2630

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p37; physical LF2626–2630

> The next section is only used when players are playing games with Deregulation. 
> Deregulation
> These rules are in play during the 1813 scenario. In addition, they may be 
> triggered if players vote to deregulate the Company during the long 1710 
> scenario or the 1758 scenario.

### R2679-2724

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p38; physical LF2679–2724

> The Firms Phase
> After the Family phase is complete and before the Hiring phase, players will 
> now perform the Firms phase. The Firms phase has two steps: Firm Investments 
> and Firm Strategy. 
> Firm Investments
> The first step of the Firms phase has no set order and players can take the 
> following actions at any time during it. The Firms phase ends when no player 
> wishes to take further actions. Any timing conflicts related to a firm are resolved 
> by the firm’s manager. Any timing conflicts between firms are resolved by the 
> Prime Minister.
> Two of the actions described in this section use Company shares. These rules are 
> restricted by the two caveats described below:
> 	
> M Weak Company Shares. If the Company Standing and/or Debt 
> marker is on a lined space, you may not use Company shares to form 
> a firm or invest.
> 	
> M Immature Company Shares. You may not invest with a Company 
> share that was created this turn. You may not avoid this rule by trading 
> your share to another player. (Players may find it helpful to flip over any 
> newly-created Company shares until the end of the turn to show that they 
> cannot be invested.)
> Forming a Firm
> A player who does not currently manage a firm may form one by returning 
> one of their Company shares to its supply or flipping one workshop to its 
> invested side. Flip your family board over to its firm charter side. Place 
> one family member from your supply on the firm’s Shares box to represent 
> the firm’s first share. Place one of your cubes on the leftmost space of the 
> Value track (the other will be used to record the total dividends paid). 
> Add £5 from the bank to this firm’s London treasury. Your family is now 
> considered a firm and you are the firm manager.
> Court and Workshop Investment
> With the consent of the firm’s manager, players may invest in a firm. For 
> each investment, add £5 from the bank to this firm’s London treasury and 
> place a family member on the firm’s Shares box. A family member in a 
> firm’s Shares box is called a firm share. Reminder: like Company shares, firm 
> shares can be traded by players.
> To invest, a player must first either return one of their Company shares to 
> its supply or flip one of their workshops to its invested side. 
> 	
> M Invested Workshops. An invested workshop is not scored if the 
> Company fails and no longer generates a bonus.
> 	
> M Firm Share Limit. Firms may only have 10 shares. A firm with 
> 10 shares may still be invested in, but will not create any further 
> shares.

### R1184-1187

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p15; physical LF1184–1187

> The newly-elected Chairman takes the Chairman marker and moves one of their 
> Company shares to the Chairman slot on the board. This piece still counts as a 
> Company share, but cannot be traded in a negotiation or used for firm investments 
> (if playing with Deregulation).

### R2773-2822

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p40; physical LF2773–2822

> Firm Strategy
> After the Firm Investments step, all firm managers must simultaneously and secretly 
> decide their trading sea zone and how much money to spend trading.
> First, each firm manager secretly selects which sea zone and home port they intend 
> to use in trade and how much cash from their firm’s London treasury they will 
> spend in the attempt. They indicate this by placing the matching firm strategy card 
> facedown near their player board and placing the money they wish to spend on the 
> matching box of the firm board. A firm may select a sea zone as long as they have 
> at least one ship, even if the associated home port is closed.
> Firm managers that do not wish to trade may select the “Hobnob” strategy. No 
> cash may be placed on this strategy. A firm with this strategy will not trade or pay 
> dividends (it must still pay expenses!), but it will allow a firm to keep its previous 
> dividend marker for the purposes of special retirements.
> Players should cover any money allocated to their strategy with their hands or by 
> any method they agree upon. Once all players have made their decisions, players 
> reveal the amount they have spent, however their strategy card should remain 
> facedown. Note: firms only get a single trade attempt each turn, so make sure you allocate 
> enough!
> Filling Orders as a Firm
> At the start of a Presidency’s Operations (before any actions are taken), any firm with 
> a strategy that is associated with that Presidency reveals their strategy and makes a 
> check with dice equal to the cash allocated to their strategy. The cash is then paid 
> to the bank. If at least one success is rolled, the firm may trade. Each firm that 
> successfully trades has an initiative value equal to the total of their ships minus 
> the number of successful dice (1s and 2s) they rolled. This number can be negative. 
> Orders are filled after the President has made a successful roll while taking the 
> Trade action. A President’s roll determines their initiative like a firm and counts all 
> ships in their Presidency’s sea zone. 
> 	
> M Vacant Presidency or Failure to Trade. If the President is vacant or does 
> not trade (for any reason), ties in initiative are decided by the Chairman 
> marker. Firms with strategies associated with this Presidency fill orders 
> after its Commander or Governors have had a chance to act.
> Players then fill orders starting with the firm or Company with the lowest initiative 
> and proceeding to the highest. When it is their turn, the President or firm manager 
> trading in the associated Presidency fills as many orders as possible. Any ties in 
> initiative are decided by the operating President.
> Firms fill a number of open orders up to the number of ships they own plus one. 
> Orders must be filled starting with the home port listed on their strategy. When 
> filling an order, you must be able to trace a path back to this port through any 
> number of orders that you have filled. 
> You may only fill each order once. When a firm first fills an order, mark it with a 
> filled order token. Then, add the value of the order(s) to your firm’s India treasury.
> 	
> M Previously-Filled Orders. Firms may fill orders previously filled this turn 
> by other firms or the Company. The Company may fill orders previously 
> filled by firms this turn. The filling of a previously-filled order will generate 
> half of its listed value, rounding down.
> Finally, advance your firm’s Value marker one space for each £6 you added to the 
> firm’s India treasury this turn. 

### R2827-2855

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p41; physical LF2827–2855

> Firm Expenses and Dividends
> At the start of the Revenue phase, before the Company pays expenses, firms will pay expenses 
> and dividends in initiative order followed by all other firms with any ties broken by their 
> Manager’s windows and then clockwise starting with the Prime Minister. 
> Firm Expenses and Dissolution
> Each firm must pay for the following expenses:
> 	
> Ƙ Pay £1 for each ship on the firm’s charter. 
> 	
> Ƙ Pay £1 for each share in the firm’s Share box or pay £ equal to the firm value, 
> whichever is higher. 
> Expenses can be paid from a firm’s London and/or India treasury.
> If a firm cannot pay expenses it must be dissolved. Move each share piece to the 
> Debtor’s Prison box on the Deregulation card (pieces here lower a player’s score by one 
> victory point). All ships owned by the firm are returned to their matching shipyard. The 
> manager of the firm then flips their firm’s charter back to the family side. Note: any 
> workshops invested in the firm will remain on their invested side for the rest of the game!
> 	
> M Emergency Investments. A firm facing dissolution may receive investments 
> from any player and use that money to cover expenses following the Court and 
> Workshops Investment rules (page 38). Any cash remaining after expenses are 
> paid is lost. Finally, lower the firm’s value by 1 space per emergency investment 
> received. Note: if a firm has 10 shares, it is still possible to invest in a firm, but no new 
> shares are generated. 
> 	
> M Emergency Mergers. A firm facing dissolution may participate in a negotiated 
> merger with one other firm at this time. As part of the merger, the other firm 
> must first pay their own expenses (if it hasn’t already done so), and pay any 
> outstanding expenses owed by the firm facing dissolution.

### R2888-2918

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p42; physical LF2888–2918

> Firm Dividends
> The manager may choose to pay out a number of dividends using cash 
> in the firm’s India treasury. For each dividend, £1 for each share is paid 
> to the player owning that share and £1 is given to the player who is the 
> manager of the firm. All cash from dividends is only taken from the India 
> treasury.
> 	
> M Optional 
> Dividends. 
> Unlike 
> Company 
> dividends, 
> any 
> shareholder may elect to not be paid for any number of their 
> shares on any dividend, so long as the manager consents. For 
> example, a firm has the following shareholders Blue (2 + Manager) and 
> Yellow (2) and £8 to payout. Normally each dividend would pay out 
> £5, but that doesn’t allow the manager to pay out all £8. If Blue forgoes 
> a share of dividends twice, all £8 could be paid out. Blue and Yellow 
> would take £4 each. 
> Then, the firm manager should record the total amount of cash paid out in 
> dividends by placing the firm’s dividend cube on the Company Balance 
> track. This value will be used by shareholders to determine the max value of their 
> special retirement (page 37).
> 	
> M Hobnobbing Firms. Any firm that selected the “Hobnob” 
> strategy should keep their firm’s dividend marker in its present 
> space and not set it to zero to reflect their lack of dividends this 
> turn.
> Finally, any cash remaining in the firm’s India treasury should be 
> moved to its London treasury.

### R654-666

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p6; physical LF654–666

> Component Limits and Infinite Tracks
> Most components in John Company are limited by the pieces included. If a supply 
> of pieces is empty, complete as much of the action as possible. However, players may 
> use proxies if they run out of cash, trophy/passed law tokens, dice, and regiments. 
> The Company Balance, Victory Point, and Vote tracks have no limit. 
> Your Play Area and Hidden Information
> Players maintain a play area that contains everything they own. All information 
> (including the contents of discard piles) is public except facedown blackmail cards.
> Cash Flow
> In John Company, cash always has a location, and its location determines how it 
> can be spent, traded, or paid. You can spend cash in your family treasury on various 
> family actions, retirements, upkeep, taxes, and negotiations. Cash within a Company 
> office can only be spent by that office. 

### R2773-2789

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p40; physical LF2773–2789

> Firm Strategy
> After the Firm Investments step, all firm managers must simultaneously and secretly 
> decide their trading sea zone and how much money to spend trading.
> First, each firm manager secretly selects which sea zone and home port they intend 
> to use in trade and how much cash from their firm’s London treasury they will 
> spend in the attempt. They indicate this by placing the matching firm strategy card 
> facedown near their player board and placing the money they wish to spend on the 
> matching box of the firm board. A firm may select a sea zone as long as they have 
> at least one ship, even if the associated home port is closed.
> Firm managers that do not wish to trade may select the “Hobnob” strategy. No 
> cash may be placed on this strategy. A firm with this strategy will not trade or pay 
> dividends (it must still pay expenses!), but it will allow a firm to keep its previous 
> dividend marker for the purposes of special retirements.
> Players should cover any money allocated to their strategy with their hands or by 
> any method they agree upon. Once all players have made their decisions, players 
> reveal the amount they have spent, however their strategy card should remain 
> facedown. Note: firms only get a single trade attempt each turn, so make sure you allocate 

### R757-807

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p8; physical LF757–807

> Negotiation
> John Company is a negotiation game. Players can transfer a wide range of assets to one another. 
> This includes: enterprises, facedown blackmail cards, cash in your family’s treasury, shares, and 
> promise cards. You cannot transfer officeholders, writers, officers, pieces on prizes, spouses, 
> passed laws, played blackmail cards, Prime Minister dial, or trophies.
> Promise Cards
> Each player has a set of five promise cards they may give other players as part of a 
> negotiation. You may “call in” a promise card and force the player who guaranteed the 
> promise to fulfill the promise if they can. Critically, you cannot “call in” a promise card 
> once the game is over and players are resolving Final Scoring. If multiple players call 
> in a promise at the same time, the player who guaranteed them chooses which to fulfill 
> if they cannot fulfill all of them. All promise cards contain details of their use on their 
> back sides. 
> When transferring resources there is one golden rule: something 
> transferred cannot activate twice. For instance, during the 
> Bonuses phase, Cati collects £1 for her workshop’s profits. If she sells 
> her workshop at this time to another player, it will not generate £1 
> again this round.
> Negotiations involving immediate transfers are binding. All 
> other negotiations are non-binding.
> Further transferring details are described here:
> 	
> Ƙ Enterprises and Blackmail Cards. You may 
> trade any enterprise card. You may allow others 
> to peek at your facedown blackmail cards 
> and trade them, but they cannot be 
> traded faceup. Remember to adjust 
> the victory point total if transferring 
> luxuries.
> 	
> Ƙ Family Cash. You may freely  
> transfer money from your family’s 
> treasury to the treasuries of other 
> families. 
> 	
> Ƙ Shares. When 
> exchanging these 
> pieces, the player 
> gaining the piece should 
> return the previous owner’s 
> piece to their supply and place 
> a family member from their 
> supply in its place. You may 
> not transfer the Chairman.
> 	
> Ƙ Promise Cards. You may 
> trade promise cards with 
> any player, including 
> returning them to their 
> guarantor or giving 
> them to a third party. 

### R1039-1042

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p12; physical LF1039–1042

> Ƙ Blackmails offer one-time effects. After they are used they are placed 
> in your player area faceup and cannot be transferred. At the end 
> of the game, all blackmail cards in a player’s area (faceup or down) 
> count for power during Final Scoring. 

### R762-807

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p8; physical LF762–807

> Promise Cards
> Each player has a set of five promise cards they may give other players as part of a 
> negotiation. You may “call in” a promise card and force the player who guaranteed the 
> promise to fulfill the promise if they can. Critically, you cannot “call in” a promise card 
> once the game is over and players are resolving Final Scoring. If multiple players call 
> in a promise at the same time, the player who guaranteed them chooses which to fulfill 
> if they cannot fulfill all of them. All promise cards contain details of their use on their 
> back sides. 
> When transferring resources there is one golden rule: something 
> transferred cannot activate twice. For instance, during the 
> Bonuses phase, Cati collects £1 for her workshop’s profits. If she sells 
> her workshop at this time to another player, it will not generate £1 
> again this round.
> Negotiations involving immediate transfers are binding. All 
> other negotiations are non-binding.
> Further transferring details are described here:
> 	
> Ƙ Enterprises and Blackmail Cards. You may 
> trade any enterprise card. You may allow others 
> to peek at your facedown blackmail cards 
> and trade them, but they cannot be 
> traded faceup. Remember to adjust 
> the victory point total if transferring 
> luxuries.
> 	
> Ƙ Family Cash. You may freely  
> transfer money from your family’s 
> treasury to the treasuries of other 
> families. 
> 	
> Ƙ Shares. When 
> exchanging these 
> pieces, the player 
> gaining the piece should 
> return the previous owner’s 
> piece to their supply and place 
> a family member from their 
> supply in its place. You may 
> not transfer the Chairman.
> 	
> Ƙ Promise Cards. You may 
> trade promise cards with 
> any player, including 
> returning them to their 
> guarantor or giving 
> them to a third party. 

### R843-847

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p9; physical LF843–847

> Once the game is over, players may not 
> negotiate, cash in promises, or play 
> blackmail cards (unless a card’s text explicitly 
> allows it). Then players perform the Final 
> Scoring phase.

### R416-433

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p5; physical LF416–433

> Next, take the player setup cards matching the date of the 
> chosen scenario. If playing with 5 players, add 3 of that 
> scenario’s extra cards. If playing with 6 players, add 6. 
> Shuffle these cards together.
> Next, deal out the setup cards evenly among the players. 
> Each player should take everything listed on their setup 
> cards. For each office listed, place a family member on 
> the listed office space and take the matching office card. 
> For cash listed, take that amount from the bank. The 
> remaining icons are explained on the right. 
> Then, complete setup:
> 11.	Set any remaining office cards near the board.
> 12.	Build the London Season Display. Shuffle the 
> prestige cards and blackmail cards together and 
> deal three. Prestige cards should be placed faceup, 
> blackmail cards should be placed facedown. 
> 13.	Shuffle the remaining law cards and place them 
> near the board.

### R453-477

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p5; physical LF453–477

> Take a shipyard. 
> Place the matching 
> ship in the indicated 
> sea zone or place on 
> shipyard if unfitted.
> Take a workshop.
> Place family member pieces in the corresponding 
> box on the board depending on the icon. 
> Commanders should be placed on the matching 
> slot in their Armies (they do not have office cards).
> Take a luxury. 
> Increase your 
> victory point marker 
> by 2 for each 
> starting luxury.
> Place a family 
> member in the Court 
> of Directors. It is 
> now referred to as a 
> Company share.
> Writer
> Officer
> Officer-in-
> Training
> Commander

### R836-853

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p9; physical LF836–853

> Game End
> Each scenario of John Company concludes 
> at the end of the turn indicated by 
> the scenario. The game can also end 
> immediately if the Company Standing 
> marker ever moves to the leftmost space on 
> the Standing track.
> Once the game is over, players may not 
> negotiate, cash in promises, or play 
> blackmail cards (unless a card’s text explicitly 
> allows it). Then players perform the Final 
> Scoring phase.
> Final Scoring
> Final scoring has several steps which are described 
> in the list below. Any ties after Final Scoring 
> are broken in favor of the player with the most 
> window icons and then in Prime Minister order 
> (clockwise, starting with the Prime Minister).

### R1900-1902

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p27; physical LF1900–1902

> During this phase, the Company’s Standing will often be adjusted. If the 
> Standing marker is moved to the leftmost position of the Standing track, the 
> Company has failed. Go to the Final Scoring immediately (page 9). 

### R2008-2012

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p29; physical LF2008–2012

> 5.	 Company Humiliation. Lower the Company’s Standing by one to the 
> left for each region lost this turn (including this region). E.g. The first lost 
> region lowers Standing by 1 space, the second lowers Standing an additional 2 
> spaces, etc. This can cause Company failure. If this happens the game is 
> over. Finish the Events in India phase, then resolve Final Scoring.

### R2586-2587

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p36; physical LF2586–2587

> M Legislated Company Failure. If a law causes the Company to fail, the 
> game is over. Finish resolving the vote then perform Final Scoring.

### R812-853

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p9; physical LF812–853

> 1.	 Power Award. Each player totals their power. Power comes from these sources:
> 	
> Ƙ Power Track. Each enterprise (remember: some prestige cards are enterprises) or 
> Company share is worth the amount of power indicated next to its token on 
> the Power track. The bottom two spaces are worth 0 power.
> 	
> Ƙ Prime Minister and Laws. Each passed law token in your play area is worth 
> +1 power. The Prime Minister grants its holder +2 power. 
> 	
> Ƙ Cards. Some blackmail cards and one spouse are worth power. Power for 
> blackmail cards in your player area is gained if the card is faceup or down.
> 	
> Ƙ Trophies. Each trophy token in your play area is worth +1 power.
> The players with the most and second most power gain victory points depending 
> on which turn was the final game turn, as indicated by the table on the board. If 
> players are tied for the most power, award the lower value to the tied players only, 
> and no other power award is given. Players tied for second place get nothing.
> 2.	 Score Court and Workshops. If the Company survived, each Company share is 
> worth the number of victory points indicated on the Court. If the Company failed, 
> players lower their score by that number instead for each, and players score 1 for 
> each workshop they own. Scores may drop below zero.
> 3.	 Final Retirement or Consequence of Failure. If the Company survived, all players 
> roll for attrition and retire any pensioners. No prestige cards are gained. If the 
> Company failed, draw one Company failure card and resolve it. 
> Game End
> Each scenario of John Company concludes 
> at the end of the turn indicated by 
> the scenario. The game can also end 
> immediately if the Company Standing 
> marker ever moves to the leftmost space on 
> the Standing track.
> Once the game is over, players may not 
> negotiate, cash in promises, or play 
> blackmail cards (unless a card’s text explicitly 
> allows it). Then players perform the Final 
> Scoring phase.
> Final Scoring
> Final scoring has several steps which are described 
> in the list below. Any ties after Final Scoring 
> are broken in favor of the player with the most 
> window icons and then in Prime Minister order 
> (clockwise, starting with the Prime Minister).

### R829-835

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p9; physical LF829–835

> 2.	 Score Court and Workshops. If the Company survived, each Company share is 
> worth the number of victory points indicated on the Court. If the Company failed, 
> players lower their score by that number instead for each, and players score 1 for 
> each workshop they own. Scores may drop below zero.
> 3.	 Final Retirement or Consequence of Failure. If the Company survived, all players 
> roll for attrition and retire any pensioners. No prestige cards are gained. If the 
> Company failed, draw one Company failure card and resolve it. 

### R2719-2720

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p38; physical LF2719–2720

> M Invested Workshops. An invested workshop is not scored if the 
> Company fails and no longer generates a bonus.

### R2665-2674

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p37; physical LF2665–2674

> Firms in Final Scoring
> At the start of Final Scoring, players will score or lose the number 
> of victory points indicated by the firm’s value for each firm 
> share they own or each family piece they have in Debtor’s Prison. 
> After totaling victory points earned, any remaining fractions are 
> rounded down.
> Then, regardless of Company success or failure, shareholders may 
> perform one special retirement before proceeding with the rest of 
> Final Scoring. Note: as this is not a London Season phase, no cards are 
> taken from the London Season Display. 

### R1018-1031

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p12; physical LF1018–1031

> Ƙ Spouses usually increase your family’s victory points, but most 
> come with a restriction you must follow for the rest of the game. 
> Spouses cannot be transferred. If a restriction requires you to 
> discard or trade enterprises/shares, players must negotiate any 
> trades immediately after they take the spouse. Regarding Violet 
> Effingham, any fitted ships connected to returned shipyards 
> will still remain in play, but their attached shipyards may not be 
> purchased during the Family Action phase if the ship is in play. 
> Most spouses also have a retirement discount that lowers the cost 
> of a retirement by the amount shown. These discounts can be 
> stacked, but may only be used by you alone. Each discount may 
> be used once per London Season and once per Final Scoring. Note: 
> these discounts will lower the amount you spend in retirement, which can 
> influence the order in which prestige cards are taken.

### R1022-1025

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p12; physical LF1022–1025

> trades immediately after they take the spouse. Regarding Violet 
> Effingham, any fitted ships connected to returned shipyards 
> will still remain in play, but their attached shipyards may not be 
> purchased during the Family Action phase if the ship is in play. 

### R2344-2357

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p34; physical LF2344–2357

> There are three policy consequences:
> 	
> Ƙ Tax. Each player must pay £1 to the bank for each target they own. For 
> each they cannot pay for, the target should be returned to its supply 
> (this includes the Chairman!). Any fitted ships connected to returned 
> shipyards remain in play, but their attached shipyards may not be 
> taken during the Family Action phase if the ship is in play.
> 	
> M Window Tax. Some tax policy spaces have a window icon. If 
> a law passes and a policy space with this icon is selected, all 
> players must pay cash equal to the number of window icons 
> associated with each of their family members on a prize and 
> each of their enterprises. If they cannot, the enterprise or 
> family member on the prize is returned to its supply.

### R1100-1134

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p13,14; physical LF1100–1134

> Enlist Writer
> Place one family member in one of the three regional Writers boxes. If there are four 
> or more vacant offices, you may place an additional writer once this turn. This might 
> allow you to place two or three writers in a turn depending on the location of your opportunity 
> marker. 
> Enlist Officer
> Place one family member in the Officers-in-Training box.
> Purchase Luxury
> Pay £4 to the bank and take one luxury. Each luxury gives you 2 victory points 
> as long as they are in your possession. Adjust your victory point marker to reflect 
> your purchase. Each luxury has a window tax icon, which may need to be paid 
> for during the Parliament Meets phase. Each luxury counts as a social enterprise. 
> Purchase Shipyard
> Pay £2 to the bank and take one shipyard. Place the matching ship token on the 
> shipyard in the space indicated. Shipyards provide a £1 bonus each turn if their 
> ship has been fitted and provide a single vote in the Parliament Meets phase. Each 
> shipyard counts as a shipping enterprise.
> Purchase Workshop
> Pay £5 to the bank and take one workshop. A workshop provides a £1 bonus each 
> turn and two votes in the Parliament Meets phase. If the Company fails, it is worth 
> 1 victory point during Final Scoring. Each workshop counts as a manufacturing 
> enterprise.
> Window Tax
> Icon
> 13
> 
> 
> --- Page 14 ---
> Seek Share
> Place a family member on an empty space on the Stock Exchange track 
> above the Court of Directors and pay the price printed on that space to 
> the bank. These family members may become shares at the end of the 
> Family phase. Once shares, they may provide income through dividends 
> and will be worth victory points at the end of the game if the Company 
> survives. If the Company fails, they will cost victory points instead.

### R1894-1896

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p27; physical LF1894–1896

> V. Bonuses
> During this phase, players collect bonuses. Every player should take £1 for each 
> shipyard with a fitted ship and each workshop they own. 

### R1083-1099

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p13; physical LF1083–1099

> Out of Family Pieces? If you need to place a family piece but have none, you must choose 
> to take one from any prize. If taken from a prize, lower your victory point marker by the 
> printed value of that prize. (Note: this rule also applies to creating Firm shares in Deregulation.)
> If a player’s opportunity marker was already on the action they chose at the start of this 
> phase, they may take that action twice instead. Example: your opportunity marker is on the 
> purchase shipyard action. This turn you could take that action twice. If you take a different action, 
> you will only take it once.
> 	
> M Extra Actions. Some laws enable players to take an additional action after they 
> have taken their main action. Only the most recently-passed extra action can be 
> used. This action does not benefit from a player’s opportunity marker, nor does 
> a player move their opportunity marker to the space corresponding to the extra 
> action. 
> 	
> M No Action. Rarely, players may be unable to take a family action. In these cases, 
> no action is taken and their opportunity token should be placed in their supply 
> of pieces. In practice this only happens if a player has no family pieces, prizes, or money. 

### R1191-1194

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p15; physical LF1191–1194

> An Empty Court? In some scenarios it is possible for the Court to be empty. In this 
> case the former Chairman will automatically become the next Chairman, and should 
> place a family member from their supply to the Chairman slot. If empty, they must 
> take from a prize if possible. If that is not possible, there will be no Chairman.

### R1083-1085

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p13; physical LF1083–1085

> Out of Family Pieces? If you need to place a family piece but have none, you must choose 
> to take one from any prize. If taken from a prize, lower your victory point marker by the 
> printed value of that prize. (Note: this rule also applies to creating Firm shares in Deregulation.)

### R1234-1254

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p16; physical LF1234–1254

> Director of Trade
> The Chairman hires from any current officeholder except the Chairman or a 
> Governor. If all offices are vacant, any writer can be chosen. Note: Commanders 
> are not officeholders.
> Manager of Shipping 
> The Chairman hires any writer for this position. 
> Military Affairs
> The Chairman hires any Commander in a Presidential Army for this position. If 
> there are none, they may hire any officer, or, if none, any piece in the Officers-
> in-Training box. 
> Presidents
> The Director of Trade hires any writer or Governor associated with that region’s 
> Presidency for this position.
> Governors 
> The President associated with the Governorship hires from any writer or officer 
> in the region. The family member holding this position should be placed on top 
> of the corresponding Governor overlay. Note: a Commander is not an officer and 
> cannot be promoted to a Governor.
> If there is a Governor General, these positions no longer exist (page 26).
> Superintendent of Trade in China
> The Chairman hires any writer for this position.

### R1417-1433

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p18; physical LF1417–1433

> Director of Trade
> The Director of Trade may take the Special Envoy action and then may move 
> writers and ships between the Presidencies. The Special Envoy action can be 
> taken multiple times.
> Special Envoy
> Make a check. Each £1 you spend gives you one die. There is no penalty. 
> If you are successful, choose one of the following:
> 	
> Ƙ Open trade with China. Create the Superintendent of Trade in 
> China by placing the office overlay to the right of the board near 
> the Bengal Presidency and taking its office card from the stack of 
> unused offices. The office should be hired immediately.
> 	
> Ƙ Open an Order. Open one closed order in any region in India 
> that is not controlled by the Company. 
> Then, you may make up to two transfers. In each, move one writer or ship from 
> one Presidency or sea zone to any other. 

### R1808-1815

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p25; physical LF1808–1815

> Superintendent of Trade in China 
> This office is created either if the Director of Trade’s Special Envoy to China is 
> successful or if Parliament passes the “Envoy to China” law. When created, the 
> office is hired immediately by the Chairman who may promote any writer. 
> Unlike a President’s treasury, the Superintendent’s treasury only contains ships. 
> Ships can be sent here by the Manager of Shipping or the Director of Trade as if 
> it were a sea zone. These ships count as if they were in the Eastern sea zone for 
> storms, expenses, events, and laws.

### R1472-1520

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p19; physical LF1472–1520

> Military Affairs
> Military Affairs moves officers and regiments 
> between Armies, assigns new officers, and 
> assigns Commanders.
> First, you may make up to two Army transfers. 
> In each, move one officer or regiment from 
> one Army to any other Army. Moved pieces 
> always remain in the top half of the Army 
> box. 
> Then, you must assign each piece in the 
> Officers-in-Training box to any of the three 
> Armies. New officers are placed in the top 
> half of their Army box.
> Finally, for each Army, if there is a player 
> with more total pieces than the current 
> Commander player or if the Commander slot 
> is vacant, assign a new Commander. Choose 
> a player from among those having the 
> greatest number of total pieces in that Army. 
> Move one of their officers to the Commander 
> slot, putting any previous Commander there 
> back into the top half of the Army box as an 
> officer. 
> ASSIGNING COMMANDERS
> Military Affairs (Blue) 
> has finished transfers 
> and assigning officers 
> and will now appoint 
> Commanders.
> The Army of Bombay is 
> skipped, as no player has 
> more pieces here than the 
> current Commander.
> The Army of Madras 
> has no Commander, so 
> Military Affairs chooses 
> between Blue and 
> Yellow and picks Blue.
> The Commander of the 
> Army of Bengal no longer 
> has the most pieces, so a 
> new Commander will be 
> appointed. Military Affairs 
> opts to appoint their 
> own officer, and Pink’s 
> Commander reverts to an 
> officer. Because this isn’t 
> hiring, Blue disregards 
> the Nepotism rule.

### R1527-1544

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p20; physical LF1527–1544

> Presidency Operations
> Each President generates revenue for the Company with the Trade action and 
> decides the order in which they, their Commander, and their Governor(s) act. 
> Commanders and Governors are not required to take any actions but they must 
> be given the opportunity to act. Each position must finish all of its actions 
> before the next one may begin (players may flip their family members facedown 
> after to track which have acted). The Trade action can be taken anytime during a 
> Presidency’s operations so long as it does not interrupt another position. 
> 	
> M Vacant President. If a President is vacant, the Chairman will decide 
> the order of the Commander and Governor(s). A Chairman acting in 
> this way cannot approve local alliance purchases or take the Trade 
> action.
> Trade
> You may fill open orders in India using the Trade action, starting from 
> your Presidency’s home port and continuing through any open orders 
> you fill. The Trade action may be taken before or after the Commander 
> or each Governor. The procedure for trading is as follows:

### R1555-1582

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p20,21; physical LF1555–1582

> If successful, place one writer on an open, empty order space for each 
> ship in this Presidency’s sea zone. You must place as many writers as 
> possible, but can only place them in the declared regions. The first writer 
> must be placed on the Presidency’s home port (marked with a thick black 
> line). After that order is filled, additional writers must be adjacent to a 
> writer you already placed. For each order filled, increase the Company 
> Balance by the amount listed on the order. 
> 	
> M Out of Writers? If all writers have been placed and ships remain 
> to fill additional orders, place filled order tokens (on the reverse 
> of the closed order token) on the orders to show they have been 
> filled.
> 	
> M Home Region Privileges. A President may not fill an order in 
> another President’s home region (even if that President is vacant).
> 	
> M One Trade. Each President may only successfully trade at most 
> once per game turn. 
> Then, you take £1 from the bank for each order you filled.
> Finally, each player takes £1 from the bank for each of their writers you 
> placed on an order.
> 20
> 
> 
> --- Page 21 ---
> The Association of Writers: If a writer is ever placed on an order adjacent to a writer 
> from a different Presidency, place a Presidency divider on the connection so that the 
> affiliation of writers is kept separate during the Refresh step.

### R2612-2619

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p36; physical LF2612–2619

> Ƙ Return writers to their associated Presidency. 
> 	
> Ƙ Return filled order tokens and Presidency dividers to the supply. 
> 	
> Ƙ Return all extra ships to the supply.
> 	
> Ƙ Any exhausted officers and regiments become active. Any active local 
> alliances are exhausted.

### R1617-1627

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p22; physical LF1617–1627

> Commanders
> First, you may request funds from your President to purchase any local alliances 
> located in your Army box and shift them to the top of the Army box. The cost of each 
> is listed on the alliance piece and is paid from your President’s treasury.
> 	
> M Local Alliances. Local alliances are temporary Army pieces. Their strength 
> can be used for two purposes: the Deploy action and to defend against 
> threats in India during the Events in India phase. Each piece can only be 
> used once on the turn they are purchased, and its strength cannot be split 
> among more than one purpose. 
> Then you may take the Deploy action as many times as you wish and can afford.

### R2618-2619

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p36; physical LF2618–2619

> Ƙ Any exhausted officers and regiments become active. Any active local 
> alliances are exhausted.

### R1630-1650

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p22; physical LF1630–1650

> 1.	 Select a target. You may select your President’s home region, a region 
> associated with your Presidency, or a region that shares a border with 
> a region associated with your Presidency. You cannot target another 
> President’s home region or a Company-controlled region associated 
> with another Presidency. Remember: you cannot take actions that would 
> have no effect if you were successful and therefore you cannot declare a 
> Company-controlled region unless it has at least one closed order or one unrest.
> 2.	 Make a check. Each officer or regiment you exhaust gives you one 
> die. In addition, each local alliance in your Army you exhaust will 
> give you the number of dice indicated on the piece. To exhaust an 
> officer, regiment, or local alliance, move it to the bottom half of its 
> respective Army box. Subtract the strength of the region from your 
> total number of dice. If the region is part of an empire, also subtract 
> the strength of every region associated with it. Remember: as with any 
> check, if it is unsuccessful, you may attempt it again so long as it did not end 
> in catastrophic failure and you have sufficient resources. Also, note that regions 
> that are Company-controlled never reduce your dice as they have a strength of 
> zero when defending.
> 3.	 Check for losses. Each player must roll a die for each of their officers 
> that were exhausted in this action (never regiments!). For each 6 rolled, 
> they must return one of their officers to their supply. 

### R1674-1703

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p23; physical LF1674–1703

> If successful, perform the following steps: 
> 1.	 Divide Loot. Gather cash from the bank based on the target region: 
> Each Tower Level
> Loot Modifier (if faceup)
> +£4
> +£4 to +£9
> 	
> M Loot Minimum. If there is less cash than the number of 
> officers + 1 (that were used in this action and that survived), 
> increase it by the difference from the bank. 
> Distribute this cash among those that participated and survived the 
> Deploy action. First, give yourself £1 (the Commander’s share) and £1 
> for each of your officers. Then continue clockwise to the next player 
> and give them £1 for each of their officers. Continue clockwise in this 
> fashion until all players with officers have been paid or no further 
> cash remains. After paying players, if cash remains, give £1 to the 
> bank for each regiment and local alliance (regardless of strength). If 
> cash remains, continue distributing as described, starting with your 
> Commander’s share and officers.
> 2.	 Take Trophies. Take one trophy token for each level in the targeted 
> region’s tower (since you are the Commander). Then, remove the tower 
> and dome. If it was a capital, remove all matching flags. 
> 3.	 Impose Order. Open all orders and remove any unrest in the region. 
> 4.	 Form Governorship. If the region is not Company-controlled, 
> move the region’s loot/control token to the space above the 
> President’s box with the region symbol side faceup. This region is 
> now associated with this President. Place the matching Governor 
> overlay in the region. Finally, take the matching Governor card 
> from the stack of unused offices and place it in the Vacant Offices 
> box. This region is now Company-controlled.

### R1753-1762

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p24; physical LF1753–1762

> Ƙ Build Company Ship. Building a ship occurs over two successful 
> actions. If there is no Company ship in your region, place one there. If 
> there is already a Company ship in your region, move that ship to the 
> sea zone associated with your President. Note: a ship in a region represents 
> a ship that is partially built and has no other effect. 
> 	
> Ƙ Commission Regiment. Place a regiment from the supply in the Army 
> associated with your President. Regiments are treated as officers, but 
> any loot they earn is paid to the bank and they cannot be removed 
> through a loss check.

### R1808-1816

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p25; physical LF1808–1816

> Superintendent of Trade in China 
> This office is created either if the Director of Trade’s Special Envoy to China is 
> successful or if Parliament passes the “Envoy to China” law. When created, the 
> office is hired immediately by the Chairman who may promote any writer. 
> Unlike a President’s treasury, the Superintendent’s treasury only contains ships. 
> Ships can be sent here by the Manager of Shipping or the Director of Trade as if 
> it were a sea zone. These ships count as if they were in the Eastern sea zone for 
> storms, expenses, events, and laws.
> This office acts after the Presidency of Bengal operates. 

### R1817-1823

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p25; physical LF1817–1823

> Trade in China
> To trade in China, make a check. Roll one die for each ship in your 
> office’s treasury. This check may only be attempted once and cannot be 
> attempted if there are no export icons in Company-controlled regions. 
> If successful, increase the Company Balance by £4 for each export icon 
> in all Company-controlled regions. Then, you take £1 from the bank for 
> each export icon in all Company-controlled regions.

### R1841-1859

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p26; physical LF1841–1859

> Governor General
> The Governor General is created by passing a law of the same name. When 
> passed, all Governors immediately become pensioners. Remove any Governor 
> overlays on the map and any partially-built Company ships. No new Governors 
> are created (or overlays placed) when additional regions become Company-
> controlled. Note: the printed Company icons on the board show players which regions 
> are Company-controlled when the Governor General is in play.
> The player holding the Director of Trade card should replace it with the 
> Governor General card and place the Governor General overlay on the ribbon. 
> Any fatigue on the Director of Trade office card should be moved to the new 
> office card. Return all Governor cards and the Director of Trade card to the 
> box. 
> The Governor General is hired like the Director of Trade by the Chairman and 
> is subject to attrition like any other office.
> The Governor General hires Presidents and performs all of its actions during the 
> part of the Company Operation phase formerly used by the Director of Trade 
> office. The Director of Trade’s treasury is now used by the Governor General. 
> From now on, if any regions are lost via attacks on the Company, follow the 
> Region Loss rules but skip the Governor Elimination step.

### R1860-1889

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p26; physical LF1860–1889

> When acting, first increase the Company Balance by £3 for each region that is 
> Company-controlled. 
> Then the Governor General may attempt the Govern action any number of 
> times. 
> Govern
> The procedure for governing is as follows: 
> 1.	 Make a check. Each £1 you spend gives you one die. There is no 
> penalty. 
> 2.	 For each 6 rolled, place one unrest in each Company-controlled 
> region.
> If you are successful, take £1 for each region that is Company-controlled. 
> Then, for each region that is Company-controlled, choose one of the 
> following (note: you must choose an option!):
> 	
> Ƙ Governor General’s Shipbuilding. Place a Company ship in 
> any sea zone (including China). 
> 	
> Ƙ Governor General’s Commission Regiment. Place a regiment 
> from the supply in any Army.
> 	
> Ƙ Governor General’s Tax. Either increase the Company Balance 
> by £2 or place £2 in any Company treasury except your own. 
> Then place an unrest in a Company-controlled region. If you 
> make this choice multiple times in a single turn, you must place 
> the unrest in a different region for each.
> If the check did not succeed, place 1 unrest in each Company-controlled 
> region.
> 	
> M One Govern. The Governor General may only successfully 
> govern at most once per game turn.

### R1943-1954

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p28; physical LF1943–1954

> The Storm Die
> Roll the storm die. The resulting face indicates which ships are subject to storms 
> and how many events occur in India.
> 	
> M Storms. If one of the three sea zones is rolled, roll a die for each ship in 
> that sea zone except Company and Extra ships. If the die face with three 
> storms is rolled, you must check for all sea zones.
> On a 1 or 2, nothing happens to the ship. On a 3 or 4, flip the ship to its 
> fatigued side. If the ship is already fatigued, the ship is sunk and should 
> be returned to its shipyard. On a 5 or 6, the ship is sunk and returned to 
> its shipyard. When a ship is returned to a shipyard, it should be flipped 
> to its non-fatigued side.

### R2919-2922

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p42; physical LF2919–2922

> Firms and Storms
> When rolling for storms during the Events in India phase, treat all firm ships as 
> if they were in the sea zone indicated by the firm’s strategy. If the strategy was 
> “Hobnob,” firm ships will not be affected by storms.

### R1962-1975

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p28; physical LF1962–1975

> Writer Loss
> When resolving events, orders sometimes become closed. If a writer is 
> on such an order, the writer is returned to its owner’s supply. If the order 
> has a filled order token, flip it instead.
> Cascade
> If you are ever required to close an order but all orders in that region are 
> already closed, a Cascade occurs. Close all open orders connected to the 
> orders in that region. When doing this, if a connected order is already 
> closed, close the northernmost open order in that region instead. If every 
> order in that region is already closed, trigger an additional Cascade. 
> Each region can only Cascade once during the resolution of each event 
> tile. However, a region may receive the effects of more than one Cascade 
> per tile. In other words, while a region might be “flooded” by closed 
> orders from more than one region, it can only “overflow” once.

### R2111-2123

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p31; physical LF2111–2123

> Turmoil
> Close the northernmost open order in the region pictured on the top of 
> the draw stack. Any writer on the order is returned to that player’s supply. 
> If all orders in this region are already closed, perform a Cascade. 
> Windfall
> Players take £1 from the bank for each writer they have on an order in the 
> region pictured on the top of the draw stack and all adjacent regions i.e. 
> regions that share a border with that region. 
> Shuffle
> First, perform the Elephant’s March. Then, shuffle this tile in with the 
> remainder of the draw stack. Finally, shuffle the discards and place them 
> on top of the draw stack, facedown. In the rare instance the draw stack is 
> empty, perform the Elephant’s March last.

### R2124-2132

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p31; physical LF2124–2132

> Leader
> If the region pictured on the top of the draw stack is sovereign, add a 
> tower level to it. Otherwise, treat this event as a Rebellion in the pictured 
> region with a strength modifier equal to the number on the explosion 
> symbol (see Crisis rules).
> 	
> M Elephant Redirect. If the Elephant was fully within a Company-
> controlled region that successfully rebelled, perform an 
> Elephant’s March. (Otherwise this event does not move the Elephant.) 

### R2133-2139

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p31; physical LF2133–2139

> Peace
> Open any orders that are connected through the border the Elephant 
> stands on. Then add one tower level to each region touching the Elephant 
> that is not controlled by the Company. If the Elephant was wholly within 
> a region (indicating a potential Rebellion), open all orders in that region 
> and remove any unrest in this region. Then, perform the Elephant’s 
> March.

### R2192-2208

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p32; physical LF2192–2208

> Invasion 
> If the attacker is a sovereign region, resolve an Invasion. Determine 
> whether the attacker’s strength (including the strength of any other regions 
> in its empire) plus the modifier listed on the event tile is greater than 
> the defender’s strength (including the strength of any other regions in its 
> empire). If so, the Invasion is successful; otherwise, the Invasion fails. 
> If the Invasion succeeded, remove any flag on the defending region’s 
> dome and place a flag matching the attacker. 
> 	
> M Shattered Empire. If the defending region was a capital, any 
> flags matching its empire are returned to the supply. 
> 	
> M New Empire. If the attacker was successful and does not have a 
> flag, place any flag with a star still in the supply on their dome. 
> If none remain, a new empire cannot be formed and no flag is 
> added to the attacker or defender.
> If the Invasion failed, remove one tower level from the attacker.

### R707-714

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p7; physical LF707–714

> When a region conquers another region, it either forms an empire or expands its 
> existing empire. All empires are composed of one capital region (marked by a 
> flag with a star) and at least one dominated region (marked by a smaller version 
> of that flag). Empires combine the strengths of their regions when attacking 
> and defending in many situations, as described later in the rules.
> 	
> M Empire Decline. If an empire is ever reduced to only its capital region, 
> return its flag to the supply. It is no longer an empire.

### R2209-2219

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p32; physical LF2209–2219

> Rebellion
> If the attacker is a dominated region, resolve a Rebellion. In a 
> Rebellion, the Crisis is only between a dominated region and the region 
> that dominates it (other regions in the empire have no impact!). Determine 
> whether the attacker’s strength plus the modifier listed on the event 
> tile is greater than the defender’s strength. If so, the Rebellion is 
> successful; otherwise it fails. 
> When a Rebellion is successful the attacking region is now sovereign. 
> Return its flag to the supply. Then, close every open order in the 
> attacking region. If all are already closed, resolve a Cascade.
> If the Rebellion failed, remove one tower level from the capital.

### R1987-2012

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p29; physical LF1987–2012

> Region Loss
> Attacks against the Company can trigger the loss of a Company-controlled 
> region. When this occurs, follow these steps:
> 1.	 Tarnish the Commander’s Name. The Commander of the Army 
> associated with this region returns half (rounding up) of the trophies 
> their family owns to the supply e.g. a player with 3 trophies would lose 2. 
> Return the Commander to its supply. 
> 2.	 Officer Rout. Roll a die for every officer in the Army and remove it if 
> the roll is a 6.
> 3.	 Governor Elimination. If this region has a Governor, return it to the 
> unused offices stack and return the officeholder’s family member to that 
> player’s supply. Any fatigue on the office card is returned to the supply.
> 4.	 Restore Local Authority. Remove the Governor overlay, any Company 
> ship, and any unrest in the region, and place a dome back in the region 
> with one tower level (place the appropriate flag if this region fell as part 
> of a successful Invasion Crisis). Place the region’s control token back in 
> its region with the loot side facedown (it will not generate additional loot 
> in the future and is no longer associated with the Presidency). If triggered 
> by an Invasion Crisis, close every open order in the region, resolving 
> a Cascade if all are already closed. Note: this closing only occurs in an 
> Invasion Crisis because a Foreign Invasion and Rebellion close orders by default.
> 5.	 Company Humiliation. Lower the Company’s Standing by one to the 
> left for each region lost this turn (including this region). E.g. The first lost 
> region lowers Standing by 1 space, the second lowers Standing an additional 2 
> spaces, etc. This can cause Company failure. If this happens the game is 
> over. Finish the Events in India phase, then resolve Final Scoring.

### R2045-2082

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p30; physical LF2045–2082

> Elephant’s March
> After resolving some events, the Elephant will move. First, check for Imperial 
> Ambitions. Otherwise, it will move to the region pictured on the top of the draw stack. 
> 	
> M Imperial Ambitions. After resolving a successful Invasion Crisis, the Elephant 
> will always be moved to the successful capital’s region, regardless of which 
> tile is on top of the draw stack. 
> After moving the Elephant, determine its position using the following procedure: 
> 	
> Ƙ If the region is Company-controlled, put the 
> Elephant in the center of the region.
> 	
> Ƙ If the region is currently dominated by 
> another region, place the Elephant on the 
> border facing its current sovereign to indicate 
> a looming Rebellion.
> 	
> Ƙ If the region is sovereign, place the Elephant 
> on the border matching the shape (circle, 
> triangle, or square) printed on the tile to 
> indicate a looming Invasion. The Elephant 
> should be facing towards the region on the 
> other side of that border. If the Elephant 
> faces a region that is already dominated by 
> the acting region (with the Elephant’s tail), 
> use the first clockwise region from that border 
> where this is not true.
> 	
> M Fully-Formed 
> Empires. 
> In 
> the 
> rare instance that all neighbors are 
> dominated, place the Elephant on 
> the border matching the shape on the 
> Elephant redirect arrow and position 
> it so that it is pointing at the empire’s 
> capital.

### R2297-2316

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p33; physical LF2297–2316

> Foreign Invasion
> Roll the storm die and resolve an Invasion Crisis and/or Attack against the 
> Company in each region linked to a storm (Bombay for West Indian, Madras for 
> South Indian, and Bengal for East Indian). If all storms are rolled, resolve this 
> event once in each. If no storms are rolled, resolve this event in the region on 
> the top card of the draw stack instead. 
> For each event, roll a die. Treat this like an Invasion with strength equal to 
> the roll. In addition to those rules, if the Foreign Invasion is successful:
> 	
> Ƙ Close every open order in the region. If all orders are already closed, 
> perform a Cascade.
> 	
> Ƙ Return any flag on this region’s dome to the supply. If it was a capital, 
> return all flags of that color to the supply. If Company-controlled, 
> return its dome to the board. In any case, set the region’s strength 
> to half the strength of the Invasion (round down).
> 	
> M Elephant Redirect. If the Elephant was fully within a Company-
> controlled region that was invaded, perform an Elephant’s March 
> using  for the shape. (Otherwise this event does not move the Elephant.)

### R2330-2343

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p34; physical LF2330–2343

> VIII. Parliament Meets
> The player with the Prime Minister dial must select a law and bring it up for a 
> vote. They do this by drawing and revealing, one at a time, up to three cards 
> from the law deck and selecting one. The remainder are discarded. Players are 
> welcome to discuss each law before the next is drawn. However, if a dilemma 
> (indicated at the top of the card) is drawn, the Prime Minister must stop 
> drawing and select that law. 
> After selecting the law, the Prime Minister must select a policy by rotating the 
> dial’s arm either clockwise or counter-clockwise. The Prime Minister must stop 
> at the first space that matches the icon printed on the bottom of the law card. 
> Each space on the Policy track has two elements, a policy consequence and a 
> target. If the law passes, the selected policy consequence will affect the target 
> (either an enterprise type, Company share or a prize as indicated by the space’s 
> color and icon). 

### R2365-2367

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p34; physical LF2365–2367

> Next, the Prime Minister reads the text of the law aloud and marks its starting 
> support (printed on bottom right of law) using the Votes marker on its track. The 
> Prime Minister should allow some time for debate before proceeding to voting.

### R2344-2364

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p34; physical LF2344–2364

> There are three policy consequences:
> 	
> Ƙ Tax. Each player must pay £1 to the bank for each target they own. For 
> each they cannot pay for, the target should be returned to its supply 
> (this includes the Chairman!). Any fitted ships connected to returned 
> shipyards remain in play, but their attached shipyards may not be 
> taken during the Family Action phase if the ship is in play.
> 	
> M Window Tax. Some tax policy spaces have a window icon. If 
> a law passes and a policy space with this icon is selected, all 
> players must pay cash equal to the number of window icons 
> associated with each of their family members on a prize and 
> each of their enterprises. If they cannot, the enterprise or 
> family member on the prize is returned to its supply.
> 	
> Ƙ Bonus. Each player takes £1 from the bank for each target they own. 
> 	
> Ƙ Power. Swap the position of the Power marker matching the target 
> with the next higher Power marker. If the target’s Power marker is 
> already in the highest position, swap the position of any two other 
> Power markers. 

### R1033-1037

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p12; physical LF1033–1037

> Ƙ Enterprises on prestige cards offer special powers which a player 
> may use. These enterprises may be worth power during Final 
> Scoring like other enterprises of their type and are likewise affected 
> by policies during the Parliament Meets phase. These enterprises 
> can be transferred.

### R2525-2540

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p35; physical LF2525–2540

> Voting
> Starting with the Prime Minister, players take turns voting. After a player has 
> voted, the next player in clockwise order votes. After all players have had a 
> chance to vote, the Prime Minister can decide to initiate an additional round 
> of voting or to stop and resolve the vote. If no votes were cast in the round, the 
> vote must be resolved. 
> A player’s votes come from several sources. Each £1 they spend from their family 
> treasury is worth 1 vote. In addition, any card in their play area is worth votes 
> equal to the number of vote icons on the card. When casting these votes, rotate 
> the card to indicate it has been used. It will be rotated back after the vote is resolved.
> As players vote, adjust the Votes marker one space for each vote cast. Players 
> may advance or lower the marker. There is no limit to the number of votes that 
> can be cast. If the Votes marker would advance beyond the end of either side of 
> the track, place cash from the bank near its position to track additional votes. If 
> it would be moved in the opposite direction, subtract any cash before moving 
> it in that direction.

### R2584-2584

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p36; physical LF2584–2584

> Finally, return any cards used for votes to their regular orientation.

### R2541-2564

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p35; physical LF2541–2564

> The Opposition 
> Any player who votes against the law is part of the opposition. Once a 
> player votes against a law, they may not vote in favor of it later during 
> that vote. All members of the opposition should count how many votes 
> they have cast against this law using any method (for instance, they could 
> group all of their cards used to vote plus any money spent).
> A player who previously voted for the law may change their mind and 
> join the opposition with later votes.
> 	
> M The Opposition Leader. The player who has cast the most votes 
> against the law is the Opposition Leader and should take the 
> Opposition Leader marker. If there is a tie, the previous holder 
> will continue to hold it. 
> 	
> M Coalitions in Opposition. Players may cast votes on behalf of 
> another player with that player’s consent. This player must have 
> voted against the law or commit to doing so. These votes should 
> be added to their total when determining the Opposition Leader.
> 	
> M The Prime Minister’s Honor. The Prime Minister cannot vote 
> against the current law or consent to their enterprises being 
> used to vote for that purpose. However, their enterprises may be 
> used to vote against a law if their “Vote with my enterprises...” 
> promise is used. 

### R2602-2621

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p36; physical LF2602–2621

> IX. Upkeep and Refresh
> Everyone must pay for their family members on prizes. Each is paid for individually, 
> using the indicated amount on that prize (printed to the right of the prize’s cost). If a 
> player cannot pay for a prize’s expense, instead return the family member to its 
> supply and lower their owner’s victory point marker by that prize’s value.
> Remember, players can transfer funds to each other at any time. If you’re having trouble 
> meeting your expenses, see if other players might be willing to loan you some money.
> Players now prepare the board for the next turn. If it is the final turn of the game, 
> skip this step and proceed to Final Scoring (page 9).
> 	
> Ƙ Return writers to their associated Presidency. 
> 	
> Ƙ Return filled order tokens and Presidency dividers to the supply. 
> 	
> Ƙ Return all extra ships to the supply.
> 	
> Ƙ Any exhausted officers and regiments become active. Any active local 
> alliances are exhausted.
> 	
> Ƙ Then, advance the turn marker and proceed with the first phase. 

### R2651-2674

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p37; physical LF2651–2674

> Special Retirement
> During the London Season phase, each player with at least one firm share 
> may take one additional retirement using a piece from their supply instead 
> of a pensioner. The total amount of money spent for this retirement 
> cannot exceed the value of the highest total dividend paid out by a 
> firm in which they own a share. This retirement is otherwise like any 
> other retirement a player can make with a pensioner. Note: even if a 
> player owns shares in multiple firms, only one special retirement can be taken! 
> Furthermore, note that discounts on spouses can be used to retire on prizes with 
> a value higher than the dividend paid by a firm.
> 	
> M Disreputable Firms. A firm that has not yet placed its dividend 
> cube or that has its dividend cube on the zero space may not be 
> used for any special retirement. 
> Firms in Final Scoring
> At the start of Final Scoring, players will score or lose the number 
> of victory points indicated by the firm’s value for each firm 
> share they own or each family piece they have in Debtor’s Prison. 
> After totaling victory points earned, any remaining fractions are 
> rounded down.
> Then, regardless of Company success or failure, shareholders may 
> perform one special retirement before proceeding with the rest of 
> Final Scoring. Note: as this is not a London Season phase, no cards are 
> taken from the London Season Display. 

### R2635-2647

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p37; physical LF2635–2647

> The Two Firm Treasuries
> Each firm has two treasury boxes: the London treasury and the India 
> treasury.
> 	
> M London Treasury. The London treasury is used to pay expenses 
> and fit new ships. Any cash raised from investments is placed 
> in this treasury. Note: players may not transfer cash in their family 
> treasury to or from firm treasuries!
> 	
> M India Treasury. The India treasury holds revenue gained from 
> trade in India. This treasury is used to pay dividends and 
> expenses. Any remainder is then transferred to the London 
> treasury.

### R2729-2739

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p39; physical LF2729–2739

> Acquiring Ships as a Firm
> A firm manager may spend cash from the firm’s London treasury to the 
> bank to fit ships on shipyards which are placed on the firm’s charter. 
> Each costs £3. Unlike the Company, a firm manager may only fit ships 
> with the consent of shipyard owner.
> 	
> M Player-owned Company Ship Buyback. A firm manager may 
> buy any player-owned ship in the Company with its owner’s 
> consent by spending cash from the firm’s London treasury. 
> An unfatigued ship costs £3 and a fatigued ship costs £2. Any 
> money spent should be added to the Shipping office’s treasury.

### R2773-2779

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p40; physical LF2773–2779

> Firm Strategy
> After the Firm Investments step, all firm managers must simultaneously and secretly 
> decide their trading sea zone and how much money to spend trading.
> First, each firm manager secretly selects which sea zone and home port they intend 
> to use in trade and how much cash from their firm’s London treasury they will 
> spend in the attempt. They indicate this by placing the matching firm strategy card 
> facedown near their player board and placing the money they wish to spend on the 

### R2838-2838

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p41; physical LF2838–2838

> Expenses can be paid from a firm’s London and/or India treasury.

### R2679-2688

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p38; physical LF2679–2688

> The Firms Phase
> After the Family phase is complete and before the Hiring phase, players will 
> now perform the Firms phase. The Firms phase has two steps: Firm Investments 
> and Firm Strategy. 
> Firm Investments
> The first step of the Firms phase has no set order and players can take the 
> following actions at any time during it. The Firms phase ends when no player 
> wishes to take further actions. Any timing conflicts related to a firm are resolved 
> by the firm’s manager. Any timing conflicts between firms are resolved by the 
> Prime Minister.

### R2729-2740

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p39; physical LF2729–2740

> Acquiring Ships as a Firm
> A firm manager may spend cash from the firm’s London treasury to the 
> bank to fit ships on shipyards which are placed on the firm’s charter. 
> Each costs £3. Unlike the Company, a firm manager may only fit ships 
> with the consent of shipyard owner.
> 	
> M Player-owned Company Ship Buyback. A firm manager may 
> buy any player-owned ship in the Company with its owner’s 
> consent by spending cash from the firm’s London treasury. 
> An unfatigued ship costs £3 and a fatigued ship costs £2. Any 
> money spent should be added to the Shipping office’s treasury.
> Note: unlike the Company, firms may not acquire Company ships or extra ships. 

### R2741-2748

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p39; physical LF2741–2748

> Hostile Takeovers
> If you do not manage a firm and have the consent of players who 
> collectively hold a majority of a firm’s shares, you may initiate a hostile 
> takeover. Flip your board to its firm charter side. Place your two firm 
> cubes on the tracks in the matching spaces as the firm you are taking 
> over. Move any ships, treasury funds, and shares to your board. The 
> previous owner then returns their cubes to their supply and returns their 
> firm charter to the family side.

### R2749-2768

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p39; physical LF2749–2768

> Mergers
> Firm managers may consolidate any number of firms into a single firm 
> through a negotiated merger. 
> In a merger, the highest value firm among those merging will be the 
> primary firm (if there is a tie, the players will pick from among those 
> tied). This firm will remain after the merger is completed. The other firms 
> in the merger are called secondary firms. 
> As part of a merger, players may negotiate for the transfer of firm shares 
> to other players. If the primary firm would have more than ten shares 
> after merger, any excess shares must be returned to their owner’s supply 
> with their owner’s consent. 
> In order for a negotiated merger to take place, all involved firms must 
> have the full consent of every shareholder. All merger negotiations are 
> considered a single immediate transfer (and therefore binding). 
> After a merger is agreed to, all secondary firms 
> transfer and consolidate their treasuries, 
> shareholders, and ships into a single firm. 
> Then, the secondary 
> firms flip to their 
> family side.

### R2782-2785

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p40; physical LF2782–2785

> Firm managers that do not wish to trade may select the “Hobnob” strategy. No 
> cash may be placed on this strategy. A firm with this strategy will not trade or pay 
> dividends (it must still pay expenses!), but it will allow a firm to keep its previous 
> dividend marker for the purposes of special retirements.

### R2913-2922

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p42; physical LF2913–2922

> M Hobnobbing Firms. Any firm that selected the “Hobnob” 
> strategy should keep their firm’s dividend marker in its present 
> space and not set it to zero to reflect their lack of dividends this 
> turn.
> Finally, any cash remaining in the firm’s India treasury should be 
> moved to its London treasury.
> Firms and Storms
> When rolling for storms during the Events in India phase, treat all firm ships as 
> if they were in the sea zone indicated by the firm’s strategy. If the strategy was 
> “Hobnob,” firm ships will not be affected by storms.

### R2689-2724

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p38; physical LF2689–2724

> Two of the actions described in this section use Company shares. These rules are 
> restricted by the two caveats described below:
> 	
> M Weak Company Shares. If the Company Standing and/or Debt 
> marker is on a lined space, you may not use Company shares to form 
> a firm or invest.
> 	
> M Immature Company Shares. You may not invest with a Company 
> share that was created this turn. You may not avoid this rule by trading 
> your share to another player. (Players may find it helpful to flip over any 
> newly-created Company shares until the end of the turn to show that they 
> cannot be invested.)
> Forming a Firm
> A player who does not currently manage a firm may form one by returning 
> one of their Company shares to its supply or flipping one workshop to its 
> invested side. Flip your family board over to its firm charter side. Place 
> one family member from your supply on the firm’s Shares box to represent 
> the firm’s first share. Place one of your cubes on the leftmost space of the 
> Value track (the other will be used to record the total dividends paid). 
> Add £5 from the bank to this firm’s London treasury. Your family is now 
> considered a firm and you are the firm manager.
> Court and Workshop Investment
> With the consent of the firm’s manager, players may invest in a firm. For 
> each investment, add £5 from the bank to this firm’s London treasury and 
> place a family member on the firm’s Shares box. A family member in a 
> firm’s Shares box is called a firm share. Reminder: like Company shares, firm 
> shares can be traded by players.
> To invest, a player must first either return one of their Company shares to 
> its supply or flip one of their workshops to its invested side. 
> 	
> M Invested Workshops. An invested workshop is not scored if the 
> Company fails and no longer generates a bonus.
> 	
> M Firm Share Limit. Firms may only have 10 shares. A firm with 
> 10 shares may still be invested in, but will not create any further 
> shares.

### R2845-2850

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p41; physical LF2845–2850

> M Emergency Investments. A firm facing dissolution may receive investments 
> from any player and use that money to cover expenses following the Court and 
> Workshops Investment rules (page 38). Any cash remaining after expenses are 
> paid is lost. Finally, lower the firm’s value by 1 space per emergency investment 
> received. Note: if a firm has 10 shares, it is still possible to invest in a firm, but no new 
> shares are generated. 

### R2852-2855

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p41; physical LF2852–2855

> M Emergency Mergers. A firm facing dissolution may participate in a negotiated 
> merger with one other firm at this time. As part of the merger, the other firm 
> must first pay their own expenses (if it hasn’t already done so), and pay any 
> outstanding expenses owed by the firm facing dissolution.

### R2648-2650

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p37; physical LF2648–2650

> Dissolving a Firm
> If all shareholders consent, a firm may be dissolved following the firm 
> dissolution rules described later (page 41).

### R2839-2843

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p41; physical LF2839–2843

> If a firm cannot pay expenses it must be dissolved. Move each share piece to the 
> Debtor’s Prison box on the Deregulation card (pieces here lower a player’s score by one 
> victory point). All ships owned by the firm are returned to their matching shipyard. The 
> manager of the firm then flips their firm’s charter back to the family side. Note: any 
> workshops invested in the firm will remain on their invested side for the rest of the game!

### R358-388

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p4; physical LF358–388

> 10.	Next, choose a scenario.
> 	
> Ƙ The 1710 Scenario should be played first.
> 	
> Ƙ The 1758 Scenario is recommended for those 
> who have played the 1710 scenario a couple 
> times. Here, the Company begins with its 
> monopoly, but this can be broken, opening 
> the gates of India to private firms. 
> 	
> Ƙ The 1813 Scenario is the most advanced 
> scenario. In it, the Company starts without 
> its monopoly, and players may start private 
> trading firms. This scenario is best with 5 or 
> 6 players.
> 	
> Ƙ The Long 1710 Scenario is intended for 
> players who have the time to play through 
> the full history of the Company. This scenario 
> begins identically to the 1710 scenario, but 
> it gives players the tools of Deregulation. 
> This scenario may go up to 8 turns and often 
> takes twice as long as the other scenarios.
> After choosing a scenario, take the matching scenario 
> setup card. Follow any instructions on the front of the 
> card, taking components as needed and using pawns 
> to mark the listed position on various tracks. Then, 
> set up the regions of India as shown on the card. 
> Place a black pawn on the space with the matching 
> date on the Turn track, and the arm on the Prime 
> Minister dial to point to the matching date.

### R825-828

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p9; physical LF825–828

> The players with the most and second most power gain victory points depending 
> on which turn was the final game turn, as indicated by the table on the board. If 
> players are tied for the most power, award the lower value to the tied players only, 
> and no other power award is given. Players tied for second place get nothing.

### R2361-2364

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p34; physical LF2361–2364

> Ƙ Power. Swap the position of the Power marker matching the target 
> with the next higher Power marker. If the target’s Power marker is 
> already in the highest position, swap the position of any two other 
> Power markers. 

### R814-816

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p9; physical LF814–816

> Ƙ Power Track. Each enterprise (remember: some prestige cards are enterprises) or 
> Company share is worth the amount of power indicated next to its token on 
> the Power track. The bottom two spaces are worth 0 power.

### R335-388

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p4; physical LF335–388

> Setup
> 1.	 Place the game board and component 
> trays in the center of the table. 
> 2.	 Shuffle the India event tiles and place 
> them next to the board.
> 3.	 Place the local alliance tiles in the Army 
> boxes where they are listed.
> 4.	 Place a marker on the “5” space of the 
> Company Balance track located on the 
> bottom edge of the board. 
> 5.	 Place the four power tokens on their 
> indicated spaces on the Power track. 
> 6.	 Every player should take a set of player 
> pieces including their family board. 
> Place each family’s victory point marker 
> on the “0” space of the Victory Point 
> track (top left of the board). 
> 7.	 Place the tower levels, domes, and flags 
> near the right side of the board.
> 8.	 Place the laws, office, prestige, 
> blackmail, and setup cards nearby.
> 9.	 Place each loot token in the matching 
> region (£ side face up).
> 10.	Next, choose a scenario.
> 	
> Ƙ The 1710 Scenario should be played first.
> 	
> Ƙ The 1758 Scenario is recommended for those 
> who have played the 1710 scenario a couple 
> times. Here, the Company begins with its 
> monopoly, but this can be broken, opening 
> the gates of India to private firms. 
> 	
> Ƙ The 1813 Scenario is the most advanced 
> scenario. In it, the Company starts without 
> its monopoly, and players may start private 
> trading firms. This scenario is best with 5 or 
> 6 players.
> 	
> Ƙ The Long 1710 Scenario is intended for 
> players who have the time to play through 
> the full history of the Company. This scenario 
> begins identically to the 1710 scenario, but 
> it gives players the tools of Deregulation. 
> This scenario may go up to 8 turns and often 
> takes twice as long as the other scenarios.
> After choosing a scenario, take the matching scenario 
> setup card. Follow any instructions on the front of the 
> card, taking components as needed and using pawns 
> to mark the listed position on various tracks. Then, 
> set up the regions of India as shown on the card. 
> Place a black pawn on the space with the matching 
> date on the Turn track, and the arm on the Prime 
> Minister dial to point to the matching date.

### R862-887

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p10; physical LF862–887

> Sequence of Play
> John Company is a procedural game played over a set number of game turns. 
> Each game turn consists of phases performed in the following order:
> I.	
> The London Season. Officeholders retire and compete for prestige 
> cards. 
> II.	
> Family. Players invest in the Company and increase their holdings. 
> Then new Company shares may be created. 
> III.	
> Hiring. The Company fills all vacant positions. 
> IV.	
> Company Operation. Each Company office operates following the 
> red ribbon from left to right on the game board.
> V.	
> Bonuses. Players take bonus income.
> VI.	
> Revenue. The Company pays its expenses, the Chairman may pay 
> dividends, and the Company adjusts its Standing.
> VII.	
> Events in India. Storms and events in India are resolved. 
> VIII.	
> Parliament Meets. Parliament meets to vote on a law.
> IX.	
> Upkeep and Refresh. Players pay upkeep on their prizes and 
> prepare for the next game turn. 

### R898-900

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p11; physical LF898–900

> I. The London Season
> The London Season has three steps: Attrition, Retirements, and Prestige Cards. 
> This phase is skipped on the game’s first turn.

### R2679-2682

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p38; physical LF2679–2682

> The Firms Phase
> After the Family phase is complete and before the Hiring phase, players will 
> now perform the Firms phase. The Firms phase has two steps: Firm Investments 
> and Firm Strategy. 

### R1693-1703

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p23; physical LF1693–1703

> 2.	 Take Trophies. Take one trophy token for each level in the targeted 
> region’s tower (since you are the Commander). Then, remove the tower 
> and dome. If it was a capital, remove all matching flags. 
> 3.	 Impose Order. Open all orders and remove any unrest in the region. 
> 4.	 Form Governorship. If the region is not Company-controlled, 
> move the region’s loot/control token to the space above the 
> President’s box with the region symbol side faceup. This region is 
> now associated with this President. Place the matching Governor 
> overlay in the region. Finally, take the matching Governor card 
> from the stack of unused offices and place it in the Vacant Offices 
> box. This region is now Company-controlled.

### R2216-2218

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p32; physical LF2216–2218

> When a Rebellion is successful the attacking region is now sovereign. 
> Return its flag to the supply. Then, close every open order in the 
> attacking region. If all are already closed, resolve a Cascade.

### R1076-1082

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p13; physical LF1076–1082

> II. Family
> This phase has two steps. First, all players will take their family action. Then, new Company 
> shares may be created.
> Family Action
> Starting with the player with the Chairman title and proceeding clockwise, each player 
> selects one family action from those listed in this section and places their opportunity 
> marker on the action they choose. (Note: at the start of the game, this marker is not on any action.) 

### R1135-1145

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p14; physical LF1135–1145

> New Company Shares
> Once all players have completed their turn, check to see if any family members 
> on the Stock Exchange track are added to the Court. One will be added for 
> each Company Debt as described below.
> If the Company has Debt, move the rightmost family member on the Stock 
> Exchange into the Court box and lower the Company Debt marker by one. 
> A family member in the Court is called a Company share. If Company Debt 
> remains, repeat this step again. 
> Finally, if there are still pieces in the Stock Exchange track but no Company 
> Debt, slide rightward all remaining family members on the Stock Exchange as 
> far as possible, preserving their order.

### R1331-1339

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p17; physical LF1331–1339

> IV. Company Operation
> Starting with the Chairman, each Company office acts in order, left to right, 
> following the red ribbon on the game board. The Chairman is responsible for 
> making sure players realize whose turn it is to act and that this phase proceeds 
> in a timely fashion. Use of a gavel or bell is encouraged.
> 	
> M Vacant Offices. Sometimes offices will remain vacant if there were no 
> eligible candidates to hire or if the hiring office was vacant. In this 
> case, the office is skipped.

### R1853-1857

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p26; physical LF1853–1857

> The Governor General is hired like the Director of Trade by the Chairman and 
> is subject to attrition like any other office.
> The Governor General hires Presidents and performs all of its actions during the 
> part of the Company Operation phase formerly used by the Director of Trade 
> office. The Director of Trade’s treasury is now used by the Governor General. 

### R1816-1816

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p25; physical LF1816–1816

> This office acts after the Presidency of Bengal operates. 

### R1939-1961

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p28; physical LF1939–1961

> VII. Events in India
> During this phase, roll the storm die, resolve any storms and then resolve a 
> number of events in India during which the political and economic landscape of 
> India will shift and Company-controlled regions may face Rebellion.
> The Storm Die
> Roll the storm die. The resulting face indicates which ships are subject to storms 
> and how many events occur in India.
> 	
> M Storms. If one of the three sea zones is rolled, roll a die for each ship in 
> that sea zone except Company and Extra ships. If the die face with three 
> storms is rolled, you must check for all sea zones.
> On a 1 or 2, nothing happens to the ship. On a 3 or 4, flip the ship to its 
> fatigued side. If the ship is already fatigued, the ship is sunk and should 
> be returned to its shipyard. On a 5 or 6, the ship is sunk and returned to 
> its shipyard. When a ship is returned to a shipyard, it should be flipped 
> to its non-fatigued side.
> 	
> M Events in India. After resolving any storms, resolve as many events in 
> India as indicated by the number on the storm die. For each event in 
> India, flip one tile from the draw stack. These events will often open or 
> close orders, alter a region’s strength, and may lead to Cascades. The 
> location of the event often depends on the back of the top tile in the 
> India draw stack. 

### R698-701

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p6; physical LF698–701

> Ƙ Every region has a political alignment: either sovereign or dominated. 
> Sovereign regions (those with a large flag or a dome without any flag) will 
> attempt to invade their neighbors. Dominated regions (those with a small 
> flag or no dome) will attempt to rebel to regain their sovereignty.

### R715-727

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p7; physical LF715–727

> The Looming Crisis (The Elephant)
> India is always faced with a looming Crisis. This is represented by the Elephant 
> and its position and direction on the map. The Elephant is always in play.
> It indicates one of two types of Crisis:
> 	
> Ƙ Impending Invasions. When the Elephant is placed on a border 
> between two regions, the acting region (with the Elephant’s tail) is 
> getting ready to invade the region the Elephant faces.
> 	
> Ƙ Impending Rebellions. If the Elephant is in the center of a region or 
> facing the region that dominates it, the acting region is getting ready 
> to rebel against its sovereign.
> Invasions and Rebellions are described in detail in the Events in India phase.

### R2186-2212

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p32; physical LF2186–2212

> Crisis
> Like Peace, the location of the Crisis is determined by the placement of 
> the Elephant piece, not by the top tile of the draw stack. The Elephant’s 
> tail (where it is walking from) indicates the attacker. The Elephant’s head 
> (where it is walking to) indicates the defender. After resolving a Crisis, 
> perform the Elephant’s March.
> Invasion 
> If the attacker is a sovereign region, resolve an Invasion. Determine 
> whether the attacker’s strength (including the strength of any other regions 
> in its empire) plus the modifier listed on the event tile is greater than 
> the defender’s strength (including the strength of any other regions in its 
> empire). If so, the Invasion is successful; otherwise, the Invasion fails. 
> If the Invasion succeeded, remove any flag on the defending region’s 
> dome and place a flag matching the attacker. 
> 	
> M Shattered Empire. If the defending region was a capital, any 
> flags matching its empire are returned to the supply. 
> 	
> M New Empire. If the attacker was successful and does not have a 
> flag, place any flag with a star still in the supply on their dome. 
> If none remain, a new empire cannot be formed and no flag is 
> added to the attacker or defender.
> If the Invasion failed, remove one tower level from the attacker.
> Rebellion
> If the attacker is a dominated region, resolve a Rebellion. In a 
> Rebellion, the Crisis is only between a dominated region and the region 
> that dominates it (other regions in the empire have no impact!). Determine 

### R2186-2191

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p32; physical LF2186–2191

> Crisis
> Like Peace, the location of the Crisis is determined by the placement of 
> the Elephant piece, not by the top tile of the draw stack. The Elephant’s 
> tail (where it is walking from) indicates the attacker. The Elephant’s head 
> (where it is walking to) indicates the defender. After resolving a Crisis, 
> perform the Elephant’s March.

### R2216-2219

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p32; physical LF2216–2219

> When a Rebellion is successful the attacking region is now sovereign. 
> Return its flag to the supply. Then, close every open order in the 
> attacking region. If all are already closed, resolve a Cascade.
> If the Rebellion failed, remove one tower level from the capital.

### R2827-2830

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p41; physical LF2827–2830

> Firm Expenses and Dividends
> At the start of the Revenue phase, before the Company pays expenses, firms will pay expenses 
> and dividends in initiative order followed by all other firms with any ties broken by their 
> Manager’s windows and then clockwise starting with the Prime Minister. 

### R1864-1872

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p26; physical LF1864–1872

> Govern
> The procedure for governing is as follows: 
> 1.	 Make a check. Each £1 you spend gives you one die. There is no 
> penalty. 
> 2.	 For each 6 rolled, place one unrest in each Company-controlled 
> region.
> If you are successful, take £1 for each region that is Company-controlled. 
> Then, for each region that is Company-controlled, choose one of the 
> following (note: you must choose an option!):

### R1344-1354

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p17; physical LF1344–1354

> Success Checks
> Doing business in India is risky. Most actions that concern India require the 
> acting player to make a check to see if their actions are successful. Each check 
> requires a roll of the dice. The number of dice you roll is dependent on the 
> resources you have and want to spend as determined by the action. Any money 
> spent comes from the office’s treasury and is paid to the bank.
> When making a check, first, decide on the amount of resources you want to 
> spend or exhaust, and gather the appropriate number of dice equal to the 
> amount shown on the office card. 
> Then, remove dice equal to the penalty. Finally, roll the dice. Use the lowest 
> rolled value to determine one of three results.

### R662-668

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p6; physical LF662–668

> Cash Flow
> In John Company, cash always has a location, and its location determines how it 
> can be spent, traded, or paid. You can spend cash in your family treasury on various 
> family actions, retirements, upkeep, taxes, and negotiations. Cash within a Company 
> office can only be spent by that office. 
> Some Company positions will reward players with extra income during their actions. 
> In the rules, these payments are highlighted by boxes like this one.

### R1821-1823

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p25; physical LF1821–1823

> If successful, increase the Company Balance by £4 for each export icon 
> in all Company-controlled regions. Then, you take £1 from the bank for 
> each export icon in all Company-controlled regions.

### R1003-1009

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p12; physical LF1003–1009

> Beginning with the player who spent the most total cash on retirements this turn, 
> each player who retired at least one pensioner this turn must take or discard one 
> card from the London Season Display. Any ties are broken in favor of most total 
> window icons (including from retirements this turn!) and then in Prime Minister order 
> (clockwise, starting with the Prime Minister). 
> When choosing their card, the acting player is welcome to peek at any blackmail 
> card in the London Season Display.

### R779-785

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p8; physical LF779–785

> Ƙ Enterprises and Blackmail Cards. You may 
> trade any enterprise card. You may allow others 
> to peek at your facedown blackmail cards 
> and trade them, but they cannot be 
> traded faceup. Remember to adjust 
> the victory point total if transferring 
> luxuries.

### R1107-1121

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p13; physical LF1107–1121

> Purchase Luxury
> Pay £4 to the bank and take one luxury. Each luxury gives you 2 victory points 
> as long as they are in your possession. Adjust your victory point marker to reflect 
> your purchase. Each luxury has a window tax icon, which may need to be paid 
> for during the Parliament Meets phase. Each luxury counts as a social enterprise. 
> Purchase Shipyard
> Pay £2 to the bank and take one shipyard. Place the matching ship token on the 
> shipyard in the space indicated. Shipyards provide a £1 bonus each turn if their 
> ship has been fitted and provide a single vote in the Parliament Meets phase. Each 
> shipyard counts as a shipping enterprise.
> Purchase Workshop
> Pay £5 to the bank and take one workshop. A workshop provides a £1 bonus each 
> turn and two votes in the Parliament Meets phase. If the Company fails, it is worth 
> 1 victory point during Final Scoring. Each workshop counts as a manufacturing 
> enterprise.

### R1458-1471

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p19; physical LF1458–1471

> The Manager of Shipping fits, buys, and leases ships on behalf of the Company.
> You must spend funds in your treasury until it has at most £2 remaining. Funds 
> can be spent to: 
> 	
> Ƙ Lease Extra Ships. Pay £2 to the bank to place an extra ship from the 
> general supply in a sea zone. Extra ships are ships on short-term leases 
> that will be returned to the supply during the Refresh step.
> 	
> Ƙ Fit Ships on Shipyards. Pay £3 to the bank to take a ship from a shipyard 
> and place it in any of the three sea zones. Note: this does not require the 
> shipyard owner’s consent.
> 	
> Ƙ Buy Company Ships. If there are no ships on shipyards, pay £5 to the 
> bank and place a Company ship from the general supply in a sea zone.

### R1549-1575

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p20; physical LF1549–1575

> 2.	 Make a check. Each £1 you spend gives you one die. Subtract one 
> for each region outside of your home region that you declared in 
> step 1 from your total dice.
> Reminder: as with any check, if it is unsuccessful, you may attempt it again 
> during your Presidency Operations so long as you have sufficient resources for 
> another check and the check did not end in catastrophic failure.
> If successful, place one writer on an open, empty order space for each 
> ship in this Presidency’s sea zone. You must place as many writers as 
> possible, but can only place them in the declared regions. The first writer 
> must be placed on the Presidency’s home port (marked with a thick black 
> line). After that order is filled, additional writers must be adjacent to a 
> writer you already placed. For each order filled, increase the Company 
> Balance by the amount listed on the order. 
> 	
> M Out of Writers? If all writers have been placed and ships remain 
> to fill additional orders, place filled order tokens (on the reverse 
> of the closed order token) on the orders to show they have been 
> filled.
> 	
> M Home Region Privileges. A President may not fill an order in 
> another President’s home region (even if that President is vacant).
> 	
> M One Trade. Each President may only successfully trade at most 
> once per game turn. 
> Then, you take £1 from the bank for each order you filled.
> Finally, each player takes £1 from the bank for each of their writers you 
> placed on an order.

### R2817-2820

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p40; physical LF2817–2820

> M Previously-Filled Orders. Firms may fill orders previously filled this turn 
> by other firms or the Company. The Company may fill orders previously 
> filled by firms this turn. The filling of a previously-filled order will generate 
> half of its listed value, rounding down.

### R2870-2879

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p41; physical LF2870–2879

> Orders are filled in initiative order. Green’s 
> firm fills the two orders in Madras and the 
> one in Hyderabad (£16 total). Remember: firms 
> fill one more order than they have ships! Green 
> then advances their Value marker 2 spaces 
> (1 for every £6 generated in Trade) and the 
> £16 is added to the firm’s India treasury. 
> The President goes next. They fill those same orders but only take half of their value and 
> fill an additional order in Maratha with their last ship (£9 total). The President then takes 
> their bonus of £4 and each writer placed generates £1 (£2 for Yellow, £1 for Pink).

### R1681-1692

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p23; physical LF1681–1692

> M Loot Minimum. If there is less cash than the number of 
> officers + 1 (that were used in this action and that survived), 
> increase it by the difference from the bank. 
> Distribute this cash among those that participated and survived the 
> Deploy action. First, give yourself £1 (the Commander’s share) and £1 
> for each of your officers. Then continue clockwise to the next player 
> and give them £1 for each of their officers. Continue clockwise in this 
> fashion until all players with officers have been paid or no further 
> cash remains. After paying players, if cash remains, give £1 to the 
> bank for each regiment and local alliance (regardless of strength). If 
> cash remains, continue distributing as described, starting with your 
> Commander’s share and officers.

### R1697-1707

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p23; physical LF1697–1707

> 4.	 Form Governorship. If the region is not Company-controlled, 
> move the region’s loot/control token to the space above the 
> President’s box with the region symbol side faceup. This region is 
> now associated with this President. Place the matching Governor 
> overlay in the region. Finally, take the matching Governor card 
> from the stack of unused offices and place it in the Vacant Offices 
> box. This region is now Company-controlled.
> 	
> M Elephant Redirect. If the Elephant was in the invaded region and 
> faced another region, place it in the center of the invaded region 
> to show that it now intends to rebel against the Company.

### R1903-1916

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p27; physical LF1903–1916

> Expenses
> First, lower the Company Balance marker by £1 for each debt as indicated by 
> the Company Debt track, each regiment and officer in an Army (do not include 
> Commanders), and each ship in the three sea zones.
> 	
> M Emergency Loans. If the Company cannot pay its expenses, emergency 
> loans must be taken to cover those expenses. For each emergency loan 
> taken, move the Company Debt marker one space to the right and 
> add £5 to the Company Balance track. If the Company Debt marker 
> is already on the rightmost space, you still take out emergency loans 
> but do not advance the Company Debt marker further. Do this until 
> all expenses have been met. Emergency loan advancements of the 
> Company Debt marker do not incur expenses during this game turn. 
> Finally, set the Company Balance to zero.

### R1472-1484

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p19; physical LF1472–1484

> Military Affairs
> Military Affairs moves officers and regiments 
> between Armies, assigns new officers, and 
> assigns Commanders.
> First, you may make up to two Army transfers. 
> In each, move one officer or regiment from 
> one Army to any other Army. Moved pieces 
> always remain in the top half of the Army 
> box. 
> Then, you must assign each piece in the 
> Officers-in-Training box to any of the three 
> Armies. New officers are placed in the top 
> half of their Army box.

### R1580-1582

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p21; physical LF1580–1582

> The Association of Writers: If a writer is ever placed on an order adjacent to a writer 
> from a different Presidency, place a Presidency divider on the connection so that the 
> affiliation of writers is kept separate during the Refresh step.

### R1999-2007

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p29; physical LF1999–2007

> 4.	 Restore Local Authority. Remove the Governor overlay, any Company 
> ship, and any unrest in the region, and place a dome back in the region 
> with one tower level (place the appropriate flag if this region fell as part 
> of a successful Invasion Crisis). Place the region’s control token back in 
> its region with the loot side facedown (it will not generate additional loot 
> in the future and is no longer associated with the Presidency). If triggered 
> by an Invasion Crisis, close every open order in the region, resolving 
> a Cascade if all are already closed. Note: this closing only occurs in an 
> Invasion Crisis because a Foreign Invasion and Rebellion close orders by default.

### R2773-2775

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p40; physical LF2773–2775

> Firm Strategy
> After the Firm Investments step, all firm managers must simultaneously and secretly 
> decide their trading sea zone and how much money to spend trading.

### R2750-2768

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p39; physical LF2750–2768

> Firm managers may consolidate any number of firms into a single firm 
> through a negotiated merger. 
> In a merger, the highest value firm among those merging will be the 
> primary firm (if there is a tie, the players will pick from among those 
> tied). This firm will remain after the merger is completed. The other firms 
> in the merger are called secondary firms. 
> As part of a merger, players may negotiate for the transfer of firm shares 
> to other players. If the primary firm would have more than ten shares 
> after merger, any excess shares must be returned to their owner’s supply 
> with their owner’s consent. 
> In order for a negotiated merger to take place, all involved firms must 
> have the full consent of every shareholder. All merger negotiations are 
> considered a single immediate transfer (and therefore binding). 
> After a merger is agreed to, all secondary firms 
> transfer and consolidate their treasuries, 
> shareholders, and ships into a single firm. 
> Then, the secondary 
> firms flip to their 
> family side.

### R1617-1647

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p22; physical LF1617–1647

> Commanders
> First, you may request funds from your President to purchase any local alliances 
> located in your Army box and shift them to the top of the Army box. The cost of each 
> is listed on the alliance piece and is paid from your President’s treasury.
> 	
> M Local Alliances. Local alliances are temporary Army pieces. Their strength 
> can be used for two purposes: the Deploy action and to defend against 
> threats in India during the Events in India phase. Each piece can only be 
> used once on the turn they are purchased, and its strength cannot be split 
> among more than one purpose. 
> Then you may take the Deploy action as many times as you wish and can afford.
> Deploy 
> The procedure for deploying is as follows:
> 1.	 Select a target. You may select your President’s home region, a region 
> associated with your Presidency, or a region that shares a border with 
> a region associated with your Presidency. You cannot target another 
> President’s home region or a Company-controlled region associated 
> with another Presidency. Remember: you cannot take actions that would 
> have no effect if you were successful and therefore you cannot declare a 
> Company-controlled region unless it has at least one closed order or one unrest.
> 2.	 Make a check. Each officer or regiment you exhaust gives you one 
> die. In addition, each local alliance in your Army you exhaust will 
> give you the number of dice indicated on the piece. To exhaust an 
> officer, regiment, or local alliance, move it to the bottom half of its 
> respective Army box. Subtract the strength of the region from your 
> total number of dice. If the region is part of an empire, also subtract 
> the strength of every region associated with it. Remember: as with any 
> check, if it is unsuccessful, you may attempt it again so long as it did not end 
> in catastrophic failure and you have sufficient resources. Also, note that regions 
> that are Company-controlled never reduce your dice as they have a strength of 
> zero when defending.

### R1341-1364

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p17; physical LF1341–1364

> M No Dead Actions. A player cannot take an action that would have no 
> effect or chance of success e.g. trading without having a ship to fill an order 
> or deploying without a dice to trigger potential officer losses.
> Success Checks
> Doing business in India is risky. Most actions that concern India require the 
> acting player to make a check to see if their actions are successful. Each check 
> requires a roll of the dice. The number of dice you roll is dependent on the 
> resources you have and want to spend as determined by the action. Any money 
> spent comes from the office’s treasury and is paid to the bank.
> When making a check, first, decide on the amount of resources you want to 
> spend or exhaust, and gather the appropriate number of dice equal to the 
> amount shown on the office card. 
> Then, remove dice equal to the penalty. Finally, roll the dice. Use the lowest 
> rolled value to determine one of three results.
> 	
> Ƙ 1 or 2 is a success.
> 	
> Ƙ 3 or 4 is a failure. The check may be attempted again if there are 
> sufficient resources.
> 	
> Ƙ 5 or 6 is a catastrophic failure. The office will take no further actions. 
> The acting officeholder is immediately returned to its player’s supply, 
> and that office card is flipped and placed in the Vacant Offices box. Any 
> fatigue that was on the office card should be returned to the supply. 

### R821-822

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p9; physical LF821–822

> Ƙ Cards. Some blackmail cards and one spouse are worth power. Power for 
> blackmail cards in your player area is gained if the card is faceup or down.

### R1925-1934

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p27; physical LF1925–1934

> Pay Dividends
> Finally, the Chairman may pay out dividends.
> The cost of each dividend is equal to the number of Company shares. When 
> a dividend is paid, lower the Balance by an amount equal to the number of 
> Company shares. Each player takes £1 for each of their Company shares. 
> Multiple dividends may be paid. Remember: the Chairman counts as a Company 
> share for dividends.
> 	
> M Public Enthusiasm. Advance Standing one space to the right if more 
> total cash was paid in dividends than Expectations. 

### R2895-2902

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p42; physical LF2895–2902

> M Optional 
> Dividends. 
> Unlike 
> Company 
> dividends, 
> any 
> shareholder may elect to not be paid for any number of their 
> shares on any dividend, so long as the manager consents. For 

### R1080-1088

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p13; physical LF1080–1088

> Starting with the player with the Chairman title and proceeding clockwise, each player 
> selects one family action from those listed in this section and places their opportunity 
> marker on the action they choose. (Note: at the start of the game, this marker is not on any action.) 
> Out of Family Pieces? If you need to place a family piece but have none, you must choose 
> to take one from any prize. If taken from a prize, lower your victory point marker by the 
> printed value of that prize. (Note: this rule also applies to creating Firm shares in Deregulation.)
> If a player’s opportunity marker was already on the action they chose at the start of this 
> phase, they may take that action twice instead. Example: your opportunity marker is on the 
> purchase shipyard action. This turn you could take that action twice. If you take a different action, 

### FOREIGN-DESIGNER

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/foreign-invasion-designer-ruling.json

verbatim_original_source; https://boardgamegeek.com/thread/2962161/article/42192767#42192767

> Sorry for the long delay in responding here. 
> 
> So, as discussed on the discord, closing them twice (and cascading) is not intended. The Region Loss rules have been slightly amended to clarify that the order closing step only occurs during an invasion crisis (because Foreign Invasion and Rebellion already do it be default.  
> 
> When it comes to the unrest cubes, they shouldn't count for Foreign Invasions. This means they don't add to strength of the attack and they don't inform the number of tower levels that might be placed in the region if it is not defended. 
> 
> 

### HUMAN-DEFENSE

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/human-defense-interpretation-source.json

verbatim_original_source

> I got an answer! The publisher says that as long as the strength of the exhausted pieces used in defense is equal to or greater than the attacking strength, the Crisis fails. Does that answer your question?
> It was in an email.
> Just accept my answer. You can note it as my interpretation.

### APPROVED-SCOPE

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/batches/2026-11-05-batch-002957/john-company-user-approved-scope.json

verbatim_original_source

> I got an answer! The publisher says that as long as the strength of the exhausted pieces used in defense is equal to or greater than the attacking strength, the Crisis fails. Does that answer your question?
> It was in an email.
> Just accept my answer. You can note it as my interpretation.

### ERRATA-SETUP

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/full-official-errata.txt

verbatim_original_source; physical LF192–204

> 	1813 Setup Card (bridge card front)
> 	Omission
> 	Add “Place Company share victory point token (+2 /-2 VP side) in Court of Directors” (optionaly - “Advance the value of Company Shares from +1/-1 VP to +2/-2 VP”
> 
> 
> Edit final line to read: 
> Place China office to right of board. Place the Bombay/Madras/Bengal control tokens in the matching Presidencies.
> 	YES
> 	1758 Setup card (bridge card front)
> 	Omission
> 	Add line at end:
> Place the Bengal control token in the Bengal Presidency.
> 	YES

### ERRATA-CARDS

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/full-official-errata.txt

verbatim_original_source; physical LF205–243

> 	Mercantile Connection (BRIDGE CARD)
> 	Omission
> (Edge Case)
> 	Add sentence in italics at end:
> If reduced to zero dice, treat roll as failure.
> 	YES
> 	Diplomatic Connection (BRIDGE CARD)
> 	Omission
> (Edge Case)
> 	Add sentence in italics at end:
> If reduced to zero dice, treat roll as failure.
> 	YES
> 	Inclosure Acts
> (BRIDGE CARD)
> 	Typo
> 	“Its” should be “their”
> 	YES
> 	Military Oversight
> BRIDGE CARD)
> 	Typo
> 	Hiring should be lowercase, “hiring”
> 	YES
> 	Company Fraud
> (BRIDGE CARD)
> 	Clarification
> 	Reword to read: 
> Play at the start of the Revenue phase. Roll one die for each of your officeholders. Lower the Company Balance equal to twice highest roll 
> (to a minimum of zero) and take that much from the bank.
> 
> 
> 	YES
> 	Law Card - Public Demands Impeachment
> 	Clarification
> 	Return officeholder to supply and add office card to the Vacant Offices box. 
> 	YES
> 	Law Card - Military Oversight
> 	Clarification
> 	Delete the word “new” to make it clear that the previous commander is still a candidate. Adjusted card reads: “...demote one Commander to an officer and then appoint a Commander from officers…”
> 	YES

### ERRATA-FRAUD

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/full-official-errata.txt

verbatim_original_source; physical LF227–235

> 	Company Fraud
> (BRIDGE CARD)
> 	Clarification
> 	Reword to read: 
> Play at the start of the Revenue phase. Roll one die for each of your officeholders. Lower the Company Balance equal to twice highest roll 
> (to a minimum of zero) and take that much from the bank.
> 
> 
> 	YES

### FRAUD-DESIGNER

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/ruling-thread-2938749.json

verbatim_original_source; https://boardgamegeek.com/thread/2938749/article/40850873#40850873

> The text of Company Fraud Blackmail card is:
> [q]Play anytime on a turn before Company expenses are paid.  Roll one die for each of your officeholders.  Lower the Company Balance equal to twice highest roll and take that much from the bank.[/q]
> 
> As the card doesn't say, 'Play immediately before Company expenses are paid', I assume that it can be paid before the Revenue Phase for the turn, at a time when the holder might need some extra cash.  What is the position if the die roll would result in the Company Balance being lowered by an amount that exceeds the current Company Balance?  (For example, a 6 is rolled (doubled to 12), but the current Company Balance is 10 pounds.) The track doesn't contain 'negative spaces.'
> 
> I can envisage 3 possible possibilities.
> 1.  The Company Balance is reduced to zero and the player takes 12 pounds from the Bank.
> 2. The Company Balance is reduced to zero and the player takes 10 pounds from the Bank.
> 3. The *[-]Company[/-] [I]Player[/I] takes 12 pounds from the Bank and the Company Balance is notionally reduced to -2 pounds, meaning that the Chairman needs to take debt in the Company Operation Phase (if the card were played before that phase) or the Company needs to take an Emergency Loan (if the card were played in the period between the Chairman acting in the Company Operating Phase and the payment of company expenses in the  Revenue Phase).
> 
> Reading the card literally and noting there is no negative space of the Company Balance Track, I'd guess that the answer would be #1.  But I'm not sure and might very well be overlooking something.
> 
> * Edit: I found a really bad error in #3.  Now fixed.
>  
> 
> DESIGNER REPLY: #2 is correct. I'll see about clarifying the card. 

The designer explicitly endorses option 2, actual Company Balance removed. Other commenters were not treated as rule authority.

### FRONTS-P1

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/pnp/Cards/John Company Cards (Bridge, Fronts).pdf

verbatim_original_source; PDF p1

> Bridge Cards (Fronts)
> 1
> 2
> 9
>   Diplomatic
> Connection
> Play after a check to 
> force a Commander to 
> reroll any Deploy roll 
> with half as many dice, 
> rounding down. 
> If reduced to zero dice, 
> treat roll as failure.
> 1
> 8
>  Mercantile 
> Connection
> Play after a check to 
> force a President or firm 
> to reroll any Trade roll 
> with half as many dice, 
> rounding down. 
> If reduced to zero dice, 
> treat roll as failure.
> 7
>  Envoy to the 
> Mughals
> Play anytime on a turn 
> before the Events in 
> India phase. Move the 
> Elephant to any legal 
> position and then take £ 
> equal to the highest open 
> order in the region with 
> the Elephant’s tail.
> 1
> 6
> Hiring Preference
> Play during hiring if 
> you are a candidate.  
> The hiring player must 
> choose you. You may 
> use this to ignore the 
> Nepotism rule.
> 2
> 5
> Scandal in
>  India
> Play when taken from the 
> display or anytime after 
> the Revenue phase on a 
> turn to force a President 
> or Governor (or Governor 
> General) to vacate 
> their office without 
> retirement.
> 2
> 4
> Scandal on
>  Leadenhall Street
> Play when taken from the 
> display or anytime after the 
> Revenue phase on a turn to 
> force any office that is not 
> President or Governor 
> (or Governor General) 
> to vacate their office 
> without retirement.
> 1
> 3
> Letters of 
> Introduction
> Play when retiring one or 
> more pieces (in London 
> Season or Final Scoring). 
> Act as if you also have 
> retirement discounts 
> equal to those on 
> all other players’ 
> spouses. 
> 2
> Company Fraud
> Play at the start of the 
> Revenue phase. Roll 
> one die for each of your 
> officeholders. Lower the 
> Company Balance equal to 
> twice the highest roll 
> (to a minimum of zero) 
> and take that much 
> from the bank.
> 2
> 1
> The Prime 
> Minister’s Ear
> Play anytime on a turn 
> before the Family phase 
> to swap two adjacent 
> power markers.
> 

Direct PDF extraction. Relevant scenario/card prose also checked in native page images where needed; unusual control-character glyphs do not substitute for graphic inspection.

### FRONTS-P2

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/pnp/Cards/John Company Cards (Bridge, Fronts).pdf

verbatim_original_source; PDF p2

> Bridge Cards (Fronts)
> 2
> 18
> Lady Glencora
> Remove your opportunity marker 
> from the game. It is never placed 
> when you take an action. Note: 
> you may still gain extra actions 
> from laws and an extra writer 
> when there are + vacancies.
> SPOUSE
> You cannot transfer this card.
> 2
> -£2
> 17
> William Collins
> You may no longer enlist officers 
> as your family action. Note: 
> the extra officer from the Army 
> Spending law is still permitted.
> SPOUSE
> You cannot transfer this card.
> 2
> -£1
> 16
> Becky Sharp
> When taking prestige cards, you 
> may take a card from the top of 
> the deck instead as long as there 
> is at least one card in the display. 
> SPOUSE
> You cannot transfer this card.
> 2
> 15
> Joseph Sedley
> You may no longer seek or 
> own Company shares. If you 
> are Chairman, move your 
> family member back into the 
> Court as a share and vacate 
> the office. Any shares you have 
> must be traded or removed.
> SPOUSE
> You cannot transfer this card.
> 2
> -£1
> 14
> Violet Effingham
> You may no longer purchase or 
> own shipyards. Any you currently 
> have must be traded or discarded. 
> (Fitted ships associated with 
> discarded shipyards remain in play.)
> SPOUSE
> You cannot transfer this card.
> 3
> -£1
> 13
> John Thorpe
> You may no longer purchase 
> or own workshops. Any 
> you currently have must 
> be traded or discarded.
> SPOUSE
> You cannot transfer this card.
> 2
> -£2
> 12
> Esther Summerson
> You may no longer take 
> or own blackmail cards. 
> Any you currently have 
> facedown must be traded or 
> discarded. Faceup blackmail 
> cards must be discarded.
> SPOUSE
> You cannot transfer this card.
> 2
> -£1
> 11
> Mr. Rochester
> You may no longer enlist writers 
> as your family action. Note: 
> the extra writer from the Tenure 
> Limits law is still permitted.
> SPOUSE
> You cannot transfer this card.
> 2
> -£2
> 1
> 1
> 10
>  Man on the Inside
> Play this card to cancel 
> the effect of a blackmail 
> card when played. The 
> canceled card should be 
> taken into your play area 
> face up. You cannot play 
> this card to cancel Letters 
> of Introduction during 
> Final Scoring.
> 

Direct PDF extraction. Relevant scenario/card prose also checked in native page images where needed; unusual control-character glyphs do not substitute for graphic inspection.

### FRONTS-P5

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/pnp/Cards/John Company Cards (Bridge, Fronts).pdf

verbatim_original_source; PDF p5

> Bridge Cards (Fronts)
> 5
> 45
> Players gain an additional £1 for 
> each of their writers placed on an 
> order in India. If the Writer Graft 
> Reform law is in effect, discard it.
> If voting on deregulation, add 5 
> to its initial support. Historical 
> note: relaxed restrictions led to 
> cheaper prices on Indian goods 
> in Britain and popular support 
> for broader deregulation.
> Writer 
> Privileges
> Law before Parliament
> -3 
> 44
> If your opportunity token is 
> not on the workshop space and 
> you take the purchase workshop 
> action, pay only £3 (not £5). 
> Note: this does not apply to a 
> workshop purchased with Calico 
> Acts. Furthermore, a player (or the 
> Crown) without an opportunity token 
> will always benefit from this law.
> Discard this law if deregulation 
> occurs. Note: If deregulation has already 
> occurred, this law may still be passed.
> Industry
> subsidy
> Law before Parliament
> T
> A
> X
> -3 
> 43
> The Director of Trade becomes 
> the Governor General. All 
> Governors become pensioners. 
> Return the Director of Trade 
> and Governor cards to the box. 
> Any Company ships on regions 
> (those unfinished by Governors) 
> are returned to the supply.
> Governor 
> General
> Law before Parliament
> +1 
> 42
> All loot is now added to 
> the Company Balance.
> Treasure 
> Reform
> Law before Parliament
> -3 
> 41
> All Governors add one die to 
> their dice pool. Failed Administer 
> actions place 2 unrest instead of 1.
> If the Governor General is in 
> play, they earn an additional 
> £3 as part of their bonus for a 
> successful Govern action. Failed 
> Govern actions place 2 unrest 
> in each region instead of 1.
> ZAMINDAR
> Taxes
> Law before Parliament
> -2 
> 40
> Each President’s 
> bonus is added to the 
> Company Balance.
> Trade
> Regulations
> Law before Parliament
> -1 
> 39
> Fitting player ships 
> now costs £2 for the 
> Manager of Shipping 
> and for private ﬁ rms.
> Ship Subsidy
> Law before Parliament
> Extra Action
> After taking any 
> family action(s), you 
> may buy a shipyard. 
> T
> A
> X
> -3 
> 38
> Regiments no longer add 
> to Company expenses.
> In attacks against the 
> Company, each unrest 
> is worth +1 strength.
> Sepoy
> Recruitment
> B
> O
> N
> U
> S
> Law before Parliament
> -3 
> 37
>  e Chairman will always 
> retire during the ﬁ rst step 
> of the London Season.
> Tenure 
> limits
> Law before Parliament
> Extra Action
> After taking any family 
> action(s) other than 
> enlist writer, you may 
> gain a single writer.
> P
> O
> W
> E
> R
> 0 
> 

Direct PDF extraction. Relevant scenario/card prose also checked in native page images where needed; unusual control-character glyphs do not substitute for graphic inspection.

### FRONTS-P6

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/pnp/Cards/John Company Cards (Bridge, Fronts).pdf

verbatim_original_source; PDF p6

> Bridge Cards (Fronts)
> 6
> 54
> If passed: Rotten Boroughs are 
> now only worth one vote each. 
> Votes now cost £2 instead of £1.
> If failed: Nothing happens.
> Masses
>  Demand
> Franchise!
> Dilemma before Parliament
> +1 
> 53
> If passed: Enact this policy 
> consequence a second time.
> If failed: The Turmoil 
> event occurs in each home 
> region. Add 1 unrest to every 
> Company-controlled region.
> Relief 
> Demanded 
> for Indian 
> Famine!
> T
> A
> X
> Dilemma before Parliament
> +1 
> 52
> Immediately search the discard 
> pile and select one law (you may 
> select a dilemma). Note: cards drawn 
> this turn are not yet in the discard pile. 
> After resolving the vote, shuffle 
> all discards, cards drawn this 
> turn, and this law into the deck. 
> If there are no cards in the 
> discard pile, ignore this card, 
> shuffle it back into the deck, 
> and draw a new law. 
>  
> Old Ideas 
> Made New!
> Dilemma before Parliament
> 51
> First, the Prime Minister 
> picks one officeholder.
> If passed: Return officeholder 
> to supply, and add office card 
> to the Vacant Offices box. 
> If failed: Company Standing 
> falls one space. This may 
> cause Company failure.
> Public 
> Demands 
> Impeachment!
> P
> O
> W
> E
> R
> Dilemma before Parliament
> +1 
> 50
> If the Company would take 
> any emergency loans the 
> Chairman may discard this card 
> to avoid those loans and cancel 
> any remaining expenses. 
> Note: this means that Standing will 
> not be reduced from emergency loans, 
> but will still be reduced from the 
> Company not meeting expectations. 
> Royal 
> Protection
> Law before Parliament
> -3 
> 49
> Advance the value of Company 
> Shares if possible e.g. from 
> +1/-1 VP to +2/-2 VP.
> Each Company Debt now 
> costs £2 during Expenses.
> Company Aids 
> Government
> P
> O
> W
> E
> R
> Law before Parliament
> +1 
> 48
> Writer bonuses are paid to 
> the Company Balance track 
> instead. Note: writers still make 
> money from the Windfall event.
> If the Writer Privileges law 
> is in effect, discard it.
> Writer graft 
> reform
> P
> O
> W
> E
> R
> Law before Parliament
> 0 
> 47
> Immediately after Military 
> Affairs acts, the Prime Minister 
> may demote one Commander 
> to an officer and then appoint 
> a Commander from officers in 
> that army following the rules 
> for hiring and Nepotism.
> Military 
> Oversight
> Law before Parliament
> +5 
> 46
> Players no longer pay 
> window taxes.
> However, a player with the 
> Tax Collector enterprise may 
> still add a single window tax 
> exempt from this law as per 
> the rules on that card.
> Window tax 
> repeal
> Law before Parliament
> Extra Action
> After taking any 
> family action(s), you 
> may buy a luxury. 
> -5 
> 

Direct PDF extraction. Relevant scenario/card prose also checked in native page images where needed; unusual control-character glyphs do not substitute for graphic inspection.

### FRONTS-P7

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/pnp/Cards/John Company Cards (Bridge, Fronts).pdf

verbatim_original_source; PDF p7

> Bridge Cards (Fronts)
> 7
> 63
> PRESIDEN T OF
> BENGAL
> A er a success you may not Trade again this turn.
> Success
> Fill orders and increase 
> the Company Balance.
> For each 
> other 
> region 
> declared.
> You gain £1 per order.
> Players gain £1 for each
> .
> Dice Pool
> £1
> Decide the order of operations. 
> May take Trade actions:
> 62
> PRESIDEN T OF
> MADRAS
> A er a success you may not Trade again this turn.
> Success
> Fill orders and increase 
> the Company Balance.
> For each 
> other 
> region 
> declared.
> You gain £1 per order.
> Players gain £1 for each
> .
> Dice Pool
> £1
> Decide the order of operations. 
> May take Trade actions:
> 61
> Decide the order of operations. 
> May take Trade actions:
> A er a success you may not Trade again this turn.
> Success
> Fill orders and increase 
> the Company Balance.
> For each 
> other 
> region 
> declared.
> You gain £1 per order.
> Players gain £1 for each
> .
> Dice Pool
> £1
> PRESIDEN T OF
> BOMBAY
> 60
> May transfer two pieces:
> Then, assign Oﬃ  cers-in-Training: 
> Lastly, appoint Commanders.
> MILITARY 
> AFFAIRS
> 59
> Fit ships until your oﬃ  ce 
> has £2 or less remaining:
> Place ﬁ tted ships 
> in any sea zone.
> Fit only if all 
> player ships 
> are ﬁ tted.
> £2
> £3
> £5
> MANAGER OF 
> SHIPPING
> 58
> Success
> Open one order in a 
> region not controlled 
> by the Company or 
> open trade with China.
> May take Special Envoy actions:
> Then, may transfer two pieces: 
> Dice Pool
> £1
> DIRECTOR OF
> TRADE
> 57
> May seek debt up to track max.
> Taking more than 3 requires 
> the Court’s approval.
> per
> Then, allocate Company Balance. 
> Add one to 
> this oﬃ  ce’s 
> attrition roll.
>  
>  
>  
> £5
> CHAIRMAN
> 56
> The Company loses its trade 
> monopoly. Players may now start a 
> firm. Clear half (rounding down) 
> of Company Debt and place the 
> Standing marker on the “S” space 
> on the track. Flip this card.
> If this law fails, set it aside. 
> The Prime Minister will remain 
> in power and the value of 
> Company shares is advanced.
> At the start of a turn, the Prime Minister may call 
> a session of Parliament to vote on this law if either 
> Standing or Debt is on a lined space. If either 
> piece is on a space with a star, the session must 
> be called. In either case, no policy is proposed.
> The initial support 
> of the law depends 
> on the status of 
> Standing and Debt:
> Deregulation
> Special Session of Parliament
> +2 +6 
> 55
> If passed: The Prime Minister 
> selects 3 non-extra ships and 
> 3 officers/regiments. Return 
> ships to shipyards or their 
> supply. Officers/regiments are 
> returned to their supplies. 
> If failed: Roll the storm die and 
> resolve a Foreign Invasion event in 
> the home region(s) associated 
> with any sea zone shown 
> (if none, no invasion occurs).
> War Against 
> France!
> T
> A
> X
> Dilemma before Parliament
> +1 
> 

Direct PDF extraction. Relevant scenario/card prose also checked in native page images where needed; unusual control-character glyphs do not substitute for graphic inspection.

### FRONTS-P9

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/pnp/Cards/John Company Cards (Bridge, Fronts).pdf

verbatim_original_source; PDF p9

> Bridge Cards (Fronts)
> 9
> Military
> Rebuked!
> Lower each player’s score 
> by half of the sum of their 
> officers, Commanders, and 
> trophies (rounding down).
> 81
> Parliament
> Exposed!
> Lower each player’s score by 
> VP for each of their passed law 
> tokens. Then, the Prime Minister 
> lowers their score by VP.
> The cartoon on this card captures the public’s 
> skepticism towards Prime Minister Disraeli’s 
> imperial ambitions. The depiction of Disraeli 
> as the villain Abanazar from an adaptation 
> of Aladdin also underlines his Jewish ancestry 
> in ways that demonstrate how racism 
> permeated even anti-imperialist positions. 80
> Industry’s 
> Greed
> Condemned!
> Do not score workshops. 
> If deregulated, do not 
> score firm shares or pieces 
> in Debtor's Prison.
> 79
> Careless 
> Shipbuilders 
> indicted!
> Lower each player’s 
> score by VP for each 
> of their shipyards.
> 78
> Court of
> directors
> blameless!
> Treat the value of Company 
> shares as if the Company 
> had been successful.
> 77
> 76
> Company Standing and Debt: Place the 
> Standing marker on the space above £10 
> expectations. Place the Debt marker on 
> the 0 space. 
> Company Treasuries: Place £3 in every 
> Company treasury. 
> Passed Laws: Place Military Oversight, 
> Deregulation (Debtor’s Prison side), and 
> Calico Acts near the area of play. Return 
> Governor General law to box and place 
> its overlay over the Director of Trade.
> Starting Regiments: Place 2 regiments in 
> each Army.
> Starting Company Ships: Place 1 Company 
> Ship in each sea zone. 
> Company Shares: Place Company share 
> victory point token (+2 /-2 VP side) in the 
> Court of Directors.
> Place China oﬃ  ce to right of board. Place 
> the Bombay/Madras/Bengal control 
> tokens in the matching Presidencies.
> 1813
> POST MONOPOLY
> 75
> Company Standing and Debt: 
> Place the Standing marker on the 
> space above £12 expectations. 
> Place the Debt marker on the 3 
> space.
> Company Treasuries: Place £4 
> in every Company treasury. 
> Passed Laws: Place Calico Acts 
> near the area of play.
> Starting Regiments: Place 1 
> regiment in the Army of Bombay, 
> 1 in the Army of Madras, and 1 in 
> the Army of Bengal.
> Starting Company Ships: Place 
> 1 Company Ship in East Indian. 
> Place the Bengal control token in the 
> Bengal Presidency.
> 1758
> COMPANY UNDER SIEGE
> 74
> Company Standing and Debt: 
> Place the Standing marker on the 
> space above £10 expectations. 
> Place the Debt marker on the 0 
> space.
> Company Treasuries: Place £3 
> in every Company treasury. 
> Passed Laws: Place Royal 
> Protection near the area of play.
> Starting Regiments: Place 1 
> regiment in the Army of Bombay, 
> 1 in the Army of Madras, and 1 in 
> the Army of Bengal.
> Starting Company Ships: 
> None. 
> 1710
> EARLY COMPANY
> 73
> GOVERNOR OF
> MYSORE
> Lower a er 
> each check.
> Success
> Failure
> May take Administer actions:
> or
> You gain £1 (or £2) and:
> for each Tax
> a er ﬁ rst.
> Initial 
> Dice Pool
> £2
> 3
> 

Direct PDF extraction. Relevant scenario/card prose also checked in native page images where needed; unusual control-character glyphs do not substitute for graphic inspection.

### BACKS-P9

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/pnp/Cards/John Company Cards (Bridge, Bridge).pdf

verbatim_original_source; PDF p9

> 20
> COMPANY
> FAILURE
> COMPANY
> FAILURE
> COMPANY
> FAILURE
> COMPANY
> FAILURE
> COMPANY
> FAILURE
> 2
> 1
> 2
> 2
> 1
> Situation in India
> X
> Dome with 
> tower levels 
> equal to X.
> Closed Order.
> Elephant
> Empire 
> ﬂ ags.
> Governor 
> overlay.
> Legend
> Situation in India
> 1
> 1
> 2
> 2
> 1
> 2
> 1
> X
> Dome with 
> tower levels 
> equal to X.
> Closed Order.
> Elephant
> Empire 
> ﬂ ags.
> Governor 
> overlay.
> Legend
> 0
> 1
> 1
> 1
> 1
> 1
> X
> 2
> 1
> Dome with 
> tower levels 
> equal to X.
> Closed Order.
> Elephant
> Empire 
> ﬂ ags.
> Governor 
> overlay.
> Situation in India
> Legend
> 16
> Chosen by:
> Its President
> GOVERNOR OF
> MYSORE
> Candidates:
> Consider writers 
> and oﬃ  cers in 
> this Presidency.
> Bridge Cards (Backs)
> 

Original Situation in India diagrams; Q079 asks to follow the chosen diagram, not to enumerate its map states.

### BOARD-PRIZES

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/pnp/Board/John Company Game Board.pdf

native_pdf_visual_transcription; PDF p1

```json
{
  "columns": [
    "cost",
    "upkeep",
    "VP",
    "windows"
  ],
  "rows": [
    [
      2,
      0,
      0,
      0
    ],
    [
      4,
      1,
      2,
      1
    ],
    [
      8,
      2,
      4,
      2
    ],
    [
      14,
      3,
      8,
      3
    ],
    [
      20,
      4,
      12,
      4
    ]
  ]
}
```

Visual evidence: /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v12-complete-requested-scope/luna-iteration-05/source-scope-review-q041-q100/full-bank-board-native-left.png

Numbers and repeated window icons inspected on the native original board. Zero upkeep/windows are blank on the first prize; values are per member.

### BOARD-STOCK

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/pnp/Board/John Company Game Board.pdf

native_pdf_visual_transcription; PDF p1

Stock Exchange arrow path: £2 → £3 → £3 → £4 → £5. Two separate £3 spaces.

Visual evidence: /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v12-complete-requested-scope/luna-iteration-05/source-scope-review-q041-q100/full-bank-board-native-left.png

### BOARD-TURNS

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/pnp/Board/John Company Game Board.pdf

native_pdf_visual_transcription; PDF p1

1710 date at turn 1; 1758 at turn 3; 1813 at turn 5. End arrows: 1710 after turn 5; 1758 after turn 7; 1813 after turn 8.

Visual evidence: /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v12-complete-requested-scope/luna-iteration-05/source-scope-review-q041-q100/full-bank-board-native-left.png

### BOARD-POWER-AWARDS

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/pnp/Board/John Company Game Board.pdf

native_pdf_visual_transcription; PDF p1

```json
{
  "final_turns_1_to_3": {
    "first": 3,
    "second": 1
  },
  "final_turns_4_to_6": {
    "first": 5,
    "second": 2
  },
  "final_turns_7_to_8": {
    "first": 8,
    "second": 4
  }
}
```

Visual evidence: /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v12-complete-requested-scope/luna-iteration-05/source-scope-review-q041-q100/full-bank-board-native-left.png

### BOARD-TRACKS

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/pnp/Board/John Company Game Board.pdf

native_pdf_visual_transcription; PDF p1

Power initial positions: Social at 2; Company Share at 1; Shipping then Manufacturing at the two zero-Power spaces, Manufacturing bottom/right and Shipping next/left on the connected path. Standing lined £4, £6, £8; star £4. Debt lined 5,6,7,8; star 8. S is above £10 Expectations.

Visual evidence: /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v12-complete-requested-scope/luna-iteration-05/source-scope-review-q041-q100/full-bank-board-native-left.png

### BOARD-RIBBON

/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/supplements/pnp/Board/John Company Game Board.pdf

native_pdf_visual_transcription; PDF p1

Chairman → Director of Trade (Governor General overlay slot) → Manager of Shipping → Military Affairs → Presidency of Bombay → Presidency of Madras → Presidency of Bengal → China if opened. Firms if Deregulation appears between Family and Hiring.

Visual evidence: /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v12-complete-requested-scope/luna-iteration-05/source-scope-review-q041-q100/full-bank-board-native-overview.png

### RULES33-CIRCLE

/home/jonny/projects/boardgame-rules/source_pdfs/john-company-second-edition-rules.pdf

native_pdf_visual_transcription; PDF p33

> If the Elephant was fully within a Company-controlled region that was invaded, perform an Elephant’s March using ● for the shape. (Otherwise this event does not move the Elephant.)

Visual evidence: /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v12-complete-requested-scope/luna-iteration-05/source-scope-review-q041-q100/full-bank-rules-page-33.png

● is the solid circle icon omitted by the supplied original text extraction at LF2316.

### RULES42-CHARTER

/home/jonny/projects/boardgame-rules/source_pdfs/john-company-second-edition-rules.pdf

native_pdf_visual_transcription; PDF p42

```json
{
  "firm_value": [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10
  ],
  "VP_per_share": [
    -1,
    0,
    0.5,
    0.5,
    1,
    1,
    1,
    1.5,
    1.5,
    2
  ]
}
```

Visual evidence: /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/john-company-second-edition/2026-11-05-batch-002957/expanded-v12-complete-requested-scope/luna-iteration-05/source-scope-review-q041-q100/full-bank-rules-charter-value-zoom.png

Charter illustration enlarged from the original rules PDF; all ten positions inspected.

### R1175-1187

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p15; physical LF1175–1187

> Chairman
> Any player with a Company share may attempt to become the new Chairman. To be 
> elected the new Chairman you need consent from players that control a majority of 
> the current Company shares.
> At the start of the election, the former Chairman should declare the number of 
> Company shares required to achieve a pure majority (more than half of total). Then, 
> any player is welcome to campaign for their candidacy. As soon as a candidate has the 
> required number of supporting Company shares, the election is over, and that player 
> is chosen as the new Chairman. 
> The newly-elected Chairman takes the Chairman marker and moves one of their 
> Company shares to the Chairman slot on the board. This piece still counts as a 
> Company share, but cannot be traded in a negotiation or used for firm investments 
> (if playing with Deregulation).

### R1708-1710

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p23; physical LF1708–1710

> If the Deploy action is a catastrophic failure, first return half (rounding 
> up) of your trophies to the supply and return the Commander to your 
> supply. 

### R836-847

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p9; physical LF836–847

> Game End
> Each scenario of John Company concludes 
> at the end of the turn indicated by 
> the scenario. The game can also end 
> immediately if the Company Standing 
> marker ever moves to the leftmost space on 
> the Standing track.
> Once the game is over, players may not 
> negotiate, cash in promises, or play 
> blackmail cards (unless a card’s text explicitly 
> allows it). Then players perform the Final 
> Scoring phase.

### R2791-2809

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p40; physical LF2791–2809

> Filling Orders as a Firm
> At the start of a Presidency’s Operations (before any actions are taken), any firm with 
> a strategy that is associated with that Presidency reveals their strategy and makes a 
> check with dice equal to the cash allocated to their strategy. The cash is then paid 
> to the bank. If at least one success is rolled, the firm may trade. Each firm that 
> successfully trades has an initiative value equal to the total of their ships minus 
> the number of successful dice (1s and 2s) they rolled. This number can be negative. 
> Orders are filled after the President has made a successful roll while taking the 
> Trade action. A President’s roll determines their initiative like a firm and counts all 
> ships in their Presidency’s sea zone. 
> 	
> M Vacant Presidency or Failure to Trade. If the President is vacant or does 
> not trade (for any reason), ties in initiative are decided by the Chairman 
> marker. Firms with strategies associated with this Presidency fill orders 
> after its Commander or Governors have had a chance to act.
> Players then fill orders starting with the firm or Company with the lowest initiative 
> and proceeding to the highest. When it is their turn, the President or firm manager 
> trading in the associated Presidency fills as many orders as possible. Any ties in 
> initiative are decided by the operating President.

### R420-425

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p5; physical LF420–425

> Next, deal out the setup cards evenly among the players. 
> Each player should take everything listed on their setup 
> cards. For each office listed, place a family member on 
> the listed office space and take the matching office card. 
> For cash listed, take that amount from the bank. The 
> remaining icons are explained on the right. 

### R1423-1428

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p18; physical LF1423–1428

> If you are successful, choose one of the following:
> 	
> Ƙ Open trade with China. Create the Superintendent of Trade in 
> China by placing the office overlay to the right of the board near 
> the Bengal Presidency and taking its office card from the stack of 
> unused offices. The office should be hired immediately.

### R1808-1811

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p25; physical LF1808–1811

> Superintendent of Trade in China 
> This office is created either if the Director of Trade’s Special Envoy to China is 
> successful or if Parliament passes the “Envoy to China” law. When created, the 
> office is hired immediately by the Chairman who may promote any writer. 

### R1753-1757

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p24; physical LF1753–1757

> Ƙ Build Company Ship. Building a ship occurs over two successful 
> actions. If there is no Company ship in your region, place one there. If 
> there is already a Company ship in your region, move that ship to the 
> sea zone associated with your President. Note: a ship in a region represents 
> a ship that is partially built and has no other effect. 

### R1870-1878

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p26; physical LF1870–1878

> If you are successful, take £1 for each region that is Company-controlled. 
> Then, for each region that is Company-controlled, choose one of the 
> following (note: you must choose an option!):
> 	
> Ƙ Governor General’s Shipbuilding. Place a Company ship in 
> any sea zone (including China). 
> 	
> Ƙ Governor General’s Commission Regiment. Place a regiment 
> from the supply in any Army.

### R2760-2762

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p39; physical LF2760–2762

> In order for a negotiated merger to take place, all involved firms must 
> have the full consent of every shareholder. All merger negotiations are 
> considered a single immediate transfer (and therefore binding). 

### R2303-2312

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p33; physical LF2303–2312

> For each event, roll a die. Treat this like an Invasion with strength equal to 
> the roll. In addition to those rules, if the Foreign Invasion is successful:
> 	
> Ƙ Close every open order in the region. If all orders are already closed, 
> perform a Cascade.
> 	
> Ƙ Return any flag on this region’s dome to the supply. If it was a capital, 
> return all flags of that color to the supply. If Company-controlled, 
> return its dome to the board. In any case, set the region’s strength 
> to half the strength of the Invasion (round down).

### R1903-1906

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p27; physical LF1903–1906

> Expenses
> First, lower the Company Balance marker by £1 for each debt as indicated by 
> the Company Debt track, each regiment and officer in an Army (do not include 
> Commanders), and each ship in the three sea zones.

### R1432-1433

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p18; physical LF1432–1433

> Then, you may make up to two transfers. In each, move one writer or ship from 
> one Presidency or sea zone to any other. 

### R1253-1254

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p16; physical LF1253–1254

> Superintendent of Trade in China
> The Chairman hires any writer for this position.

### R2303-2307

/home/jonny/projects/boardgame-rules/extracted/john-company-second-edition-rules.txt

verbatim_original_source; Rules printed p33; physical LF2303–2307

> For each event, roll a die. Treat this like an Invasion with strength equal to 
> the roll. In addition to those rules, if the Foreign Invasion is successful:
> 	
> Ƙ Close every open order in the region. If all orders are already closed, 
> perform a Cascade.

## Limits and preservation

- Original designer/source copies supplied in the run are accepted as the authorized original evidence; no internet fetch or external provenance verification was performed.
- The full-bank review uses only exact fixed bank questions and authorized original rules/supplements. No existing broad audit or reader artifact was consulted.
- Incidental nonquestion metadata embedded in allowed JSON files is not evidence of any actual runtime, score or approval state.
- A per-atom source reference may point to a shared complete procedure quote; supporting evidence is centralized in the registry to avoid duplicating the same original passage hundreds of times. Native graphic tables are transcribed from the original PDF, not from existing audit crops.
- Q093’s bank bonus source is an inference from take-a-personal-bonus convention and parallel office income, not a verbatim bank word in the Govern paragraph.
- Free enlistment, no initial marker doubling, no takeover shareholding prerequisite and ordinary dividend affordability are clear structural implications of complete original procedures. These are individually marked as such.
- Q015/Q088 use the expressly authorized human >= interpretation instead of pretending the printed equality sentence literally says >=. The reported private publisher email was not inspected.

No questions, keys, scopes, summaries or current grades were edited. The five original two-question review outputs and all authorized inputs remain byte-identical. Recommendations do not change or predict grades.
