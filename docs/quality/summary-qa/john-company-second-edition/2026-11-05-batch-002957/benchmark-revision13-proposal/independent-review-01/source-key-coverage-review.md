# Independent source, key, asked-scope and coverage review

**CONCRETE CHANGES NEEDED.** All 114 questions and 911 proposed atoms were reviewed. All 911 atoms have support within the assigned official-plus-attributed-user scope; 910 are actually requested or clearly implied, and one is unasked context. One removed Q014 condition must be restored. Two distinct core questions remain necessary.

The question-only prereview was saved before opening the key, scopes, corrections, coverage ledgers or baseline. No summary, reader answers, grades, prior review reports, runtime logs, web or collaboration/status tools were used.

All original 113 question entries are identical to v12. Only Q024 changes among the original answer-key entries. The mandatory atom total changes from 919 to 911 through the stated changes and Q114’s two atoms.

## IR01-SCOPE-014

**Question:** If Company revenue cannot cover expenses, how do emergency loans work at and below max Debt, how does Standing change, and when are expectations and dividends checked?

**Exact phrase:** “how does Standing change, and when are expectations and dividends checked?”

**Source truth:** Immediate failure during Revenue goes directly to Final Scoring.

**Asked scope:** Required consequential stopping exception to the expressly requested check/dividend timing.

**Before:** Reaching failure ends game immediately [removed from mandatory facts by FB-Q014-09]

**After:** If an emergency-loan/expectations Standing reduction reaches the failure space, go to Final Scoring immediately; do not proceed with remaining Revenue steps. Otherwise check expectations after expenses/Public Embarrassment, then consider dividends.

**Change:** Restore the removed Q014 failure atom; qualify subsequent timing atoms with survival. The key already contains the failure rule, so preserve it.

The question asks when later checks happen in a shortfall procedure. A loss of Standing can end that procedure before the later steps. Treating this as merely adjacent endgame context would allow an answer that wrongly continues to expectations or dividends after failure. Coverage elsewhere does not make a condition unasked here.

**Coverage:** No new question needed for this condition; retain it under Q014 even though Q025 also tests game end.

Original rules p27, physical LF 1900–1902:

> During this phase, the Company’s Standing will often be adjusted. If the 
> Standing marker is moved to the leftmost position of the Standing track, the 
> Company has failed. Go to the Final Scoring immediately (page 9). 

Original rules p27, physical LF 1918–1934:

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

## IR01-SCOPE-025

**Question:** When does the game end and which phase is completed if failure occurs during Events in India or from legislation? Can promises or negotiations continue in Final Scoring?

**Exact phrase:** “Can promises or negotiations continue in Final Scoring?”

**Source truth:** The explicit-card exception in this paragraph qualifies playing blackmail; it does not provide a general exception to the ban on negotiations or cashing promises.

**Asked scope:** Blackmail permission is not requested by this question.

**Before:** Explicit card permissions can override

**After:** None

**Change:** Move Q025 atom 8 to optional blackmail context, explicitly limited to playing blackmail cards. Keep Q025 atoms 1–7 mandatory.

The two requested final-scoring activities are promises and negotiations. A complete answer can prohibit both and give all ending/timing rules without volunteering blackmail. Q102 expressly asks the blackmail exception. The existing bare atom must also not be read as an exception for promises/negotiations.

**Coverage:** Q102 retains both prohibition and card-text exception; no new question needed.

Original rules p9, physical LF 843–847:

> Once the game is over, players may not 
> negotiate, cash in promises, or play 
> blackmail cards (unless a card’s text explicitly 
> allows it). Then players perform the Final 
> Scoring phase.

## IR01-COVERAGE-INVASION

**Question:** In a non-Company Invasion, which strengths count, does equal strength win, how do flags change and what if no empire flags remain?

**Exact phrase:** “which strengths count, does equal strength win, how do flags change and what if no empire flags remain?”

**Source truth:** A failed Invasion removes one tower level from the attacker.

**Asked scope:** The listed interrogatives request comparison, ties and flags, not tower loss on failure. The existing Q050 key mentions tower loss, but none of its eight mandatory atoms tests it.

**Before:** No distinct question/mandatory atom directly tests failed non-Company Invasion tower loss.

**After:** {"proposed_question": "When an ordinary non-Company Invasion fails, which region loses a tower level?", "expected_answer": "Remove one tower level from the attacking region.", "required_facts": ["A failed ordinary non-Company Invasion removes one tower level from the attacker."]}

**Change:** Add a distinct question rather than silently making the tower consequence mandatory under the unchanged Q050 wording.

Q051 directly tests failed Rebellion damage to the capital. Q015 tests failed Invasion damage only in successful Company defense. Neither tests the ordinary non-Company branch. This changes future regional strength and is a real consequence, not a new-number fixture.

**Coverage:** At least one additional distinct question is required; zero-addition sweep 23 cannot establish full procedural saturation.

Original rules p32, physical LF 2192–2208:

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

Original rules p32, physical LF 2219–2219:

> If the Rebellion failed, remove one tower level from the capital.

Original rules p33, physical LF 2293–2296:

> M Failed and Successful Invasions. If the primary Crisis was an 
> Invasion that failed, remove one tower level from the attacking 
> region if possible. If it was successful follow the rules of empire 
> creation and growth as described on the previous page.

## IR01-COVERAGE-FIRM-DIVIDENDS

**Question:** How are firm expenses and dividends funded and calculated, and what happens to a failing firm, its shares and workshops?

**Exact phrase:** “How are firm expenses and dividends funded and calculated”

**Source truth:** The firm manager may choose the number of dividends using India cash.

**Asked scope:** Funding/calculation does not itself explicitly ask who decides whether to pay or whether zero may be chosen. Candidate mandatory atoms cover rates/funds, not discretionary authority.

**Before:** No question directly tests ordinary firm-manager discretion to choose whether/how many dividends to pay.

**After:** {"proposed_question": "Who chooses whether an ordinary non-Hobnobbing firm pays dividends and how many? May the manager choose none even when India-treasury cash is available?", "expected_answer": "The firm manager chooses whether to pay dividends and how many, within the available India-treasury cash. The manager may choose zero; available trade cash does not force a payout.", "required_facts": ["Firm manager chooses whether to pay ordinary dividends.", "Manager may choose zero or multiple dividends subject to available India cash."]}

**Change:** Add a distinct authority/discretion question without forcing an unasked actor into Q020.

Q101 tests shareholder waiver with manager consent and marker/remainder handling. Q066 tests a Hobnob prohibition. Q112 asks ordinary Company discretion only. None establishes who chooses an ordinary firm payout, or that an ordinary firm can retain trade cash rather than distribute it. This is a consequential finance decision.

**Coverage:** An additional firm-finance question is required; zero-addition sweep 22 missed an ordinary finance branch.

Original rules p42, physical LF 2888–2893:

> Firm Dividends
> The manager may choose to pay out a number of dividends using cash 
> in the firm’s India treasury. For each dividend, £1 for each share is paid 
> to the player owning that share and £1 is given to the player who is the 
> manager of the firm. All cash from dividends is only taken from the India 
> treasury.

Original rules p42, physical LF 2913–2918:

> M Hobnobbing Firms. Any firm that selected the “Hobnob” 
> strategy should keep their firm’s dividend marker in its present 
> space and not set it to zero to reflect their lack of dividends this 
> turn.
> Finally, any cash remaining in the firm’s India treasury should be 
> moved to its London treasury.

## IR01-CITATION-024

**Question:** How does setup use extra player cards for five or six players, distribute holdings, award starting luxury points and build the London display?

**Exact phrase:** “distribute holdings”

**Source truth:** Correct office-card destination is on printed page 5, physical LF 420–425.

**Asked scope:** The proposed distribution correction is required and correct; only its page attribution needs repair.

**Before:** Rules p4 physicalLF420–425

**After:** Rules p5 physical LF420–425

**Change:** Change p4 to p5 in the Q024 key source-reference suffix and correction ledger basis/source_references_after. The general pp4–5 reference may remain.

Physical LF415 is the Page 5 marker; the cited holdings instructions follow it.

**Coverage:** No gameplay or coverage change.

Original rules p5, physical LF 415–425:

> --- Page 5 ---
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

## Seventeen explicit proposals

| Proposal | Verdict | Independent assessment |
|---|---|---|
| FB-Q006-03 | ACCEPT | The majority threshold, eligibility and first-to-majority resolution govern the election outcome. Announcing that threshold adds no separate substantive condition; retaining the deadlock choice is essential. |
| FB-Q007-12 | ACCEPT | A generic statement that exceptions exist identifies no requested destination or operative exception. Concrete Commander/China/Governor rules remain separately asked. |
| FB-Q014-09 | REJECT_REMOVAL_RESTORE_REQUIRED | REJECT. Immediate failure is the stopping condition for the asked Revenue sequence and changes whether subsequent expectations/dividend steps occur. Restore it; Q025 overlap does not eliminate the asked exception. |
| FB-Q019-09 | ACCEPT | The original source explicitly gates ordinary filling on the President’s successful Trade roll and gives a later fallback. Both timing branches belong in this broad timing question. |
| FB-Q024-05 | ACCEPT | The source places the member in the office and gives the card to the player. The new mandatory sentence is correct. Fix the printed-page citation from p4 to p5. |
| FB-Q034-03 | ACCEPT | Creating China immediately opens a hire; the hire actor and writer pool answer a separate hiring question. Immediate hiring remains mandatory here. |
| FB-Q040-03 | ACCEPT | The question asks construction success count and locations; a separate assertion of unusability is not necessary to state both stages. Q013 broad Administer still requires the no-other-effect construction state. |
| FB-Q041-05 | ACCEPT | General Eastern sea-zone equivalence answers the identity question and implies the source’s applicable uses. Do not insist on four individually enumerated purposes. |
| FB-Q044-07 | ACCEPT | Company ship is the actual generated resource, materially different from a player ship. The new wording correctly preserves the requested option and eligible destinations. |
| FB-Q068-02 | ACCEPT | Only differences and expense obligations are requested here. All-shareholder consent is unchanged and remains explicitly tested by Q065 legality. |
| FB-Q077-02 | ACCEPT | The yes/no unrest contribution is independent of the underlying die formula, which Q054 directly requests. Keep no unrest as mandatory. |
| FB-Q077-03 | ACCEPT | A resulting-tower formula is not needed to answer whether unrest changes it; Q054 directly asks tower changes. Keep both no-unrest and closure conditions. |
| FB-Q082-03 | ACCEPT | Returning the last capital flag regardless of cause is the requested operative action. No separate recital of the empire label is necessary. |
| FB-Q090-04 | ACCEPT | The Cascade condition is expressly asked and source-explicit. The revised atom avoids accidentally demanding a Cascade after closing initially open orders. |
| FB-Q100-01 | ACCEPT | This calculation question asks items/rates and China inclusion. Separate account/debit action is not requested; Q114 now asks it directly. |
| FB-Q100-07 | ACCEPT | The requested answer is China inclusion in the £1 ship expense. Eastern status explains that answer but is independently asked by Q041. |
| FB-Q106-04 | ACCEPT | No duplicate closure/Cascade directly answers the second interrogative. The base attacks’ closing rules explain why and are independently tested. |

## Q114 and coverage

Q114 passes source truth, asked scope and novelty. Rules p27 LF1904 explicitly lowers Company Balance. Q100 asks cost categories, Q014 shortfall handling, and Q112 dividend funding; their contextual key wording does not make the ordinary expense debit an asked fact.

The two zero-addition ledgers record zero additions but do not establish working saturation: sweep 22 misses ordinary firm-manager dividend discretion; sweep 23 does not directly cover failed non-Company Invasion tower loss and accepts removing the Q014 stopping condition. Add the two concrete questions above, restore Q014, remove Q025 blackmail context from mandatory scope, and repair the Q024 page attribution.

The user’s general newly exhausted defense strength ≥ attack interpretation is faithfully attributed. It is normative for this assignment; independently verified official/email authority is not claimed or required.

The review covers standard 3–6 multiplayer, all 1710/1758/1813/Long 1710 scenarios and firms. Crown/solo/two-player, optional draft, an exhaustive card-power catalog and live source verification remain outside scope. Individual holdings/maps may be read from components. Working saturation is not yet established and would not prove every possible interaction.

## All-question accounting

The JSON report contains a separate source-truth and asked-scope decision for every one of the 911 atoms, exact original question strings and regenerated original-source evidence.

| Question | Atoms reviewed | Source truth | Asked scope |
|---|---:|---|---|
| Q001 | 9 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q002 | 9 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q003 | 8 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q004 | 6 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q005 | 8 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q006 | 9 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q007 | 12 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q008 | 7 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q009 | 8 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q010 | 12 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q011 | 13 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q012 | 15 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q013 | 16 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q014 | 12 | Supported | RESTORE_FAILURE_CONDITION |
| Q015 | 17 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q016 | 11 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q017 | 13 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q018 | 17 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q019 | 21 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q020 | 12 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q021 | 12 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q022 | 16 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q023 | 7 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q024 | 15 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q025 | 8 | Supported | REMOVE_ONE_UNASKED_ATOM |
| Q026 | 14 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q027 | 6 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q028 | 8 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q029 | 2 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q030 | 20 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q031 | 4 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q032 | 5 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q033 | 11 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q034 | 5 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q035 | 10 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q036 | 9 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q037 | 3 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q038 | 11 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q039 | 3 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q040 | 7 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q041 | 5 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q042 | 6 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q043 | 10 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q044 | 10 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q045 | 11 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q046 | 7 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q047 | 9 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q048 | 4 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q049 | 5 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q050 | 8 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q051 | 6 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q052 | 19 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q053 | 7 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q054 | 16 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q055 | 9 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q056 | 8 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q057 | 8 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q058 | 10 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q059 | 11 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q060 | 8 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q061 | 7 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q062 | 4 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q063 | 8 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q064 | 10 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q065 | 6 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q066 | 6 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q067 | 8 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q068 | 3 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q069 | 4 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q070 | 5 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q071 | 20 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q072 | 8 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q073 | 13 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q074 | 13 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q075 | 5 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q076 | 12 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q077 | 3 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q078 | 7 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q079 | 9 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q080 | 3 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q081 | 10 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q082 | 5 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q083 | 6 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q084 | 3 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q085 | 3 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q086 | 12 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q087 | 7 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q088 | 10 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q089 | 3 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q090 | 4 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q091 | 2 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q092 | 6 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q093 | 6 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q094 | 2 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q095 | 5 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q096 | 6 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q097 | 7 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q098 | 7 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q099 | 2 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q100 | 6 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q101 | 5 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q102 | 2 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q103 | 7 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q104 | 7 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q105 | 3 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q106 | 3 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q107 | 4 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q108 | 2 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q109 | 3 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q110 | 4 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q111 | 4 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q112 | 9 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q113 | 2 | Supported | ACCEPT_PROPOSED_ATOMS |
| Q114 | 2 | Supported | ACCEPT_PROPOSED_ATOMS |

**Totals:** 114 questions; 911 atoms; 911 source-supported; 910 requested/clear implications; 1 contextual atom; 1 actually asked condition to restore; 17 proposals reviewed (16 accepted in substance, 1 rejected); 2 additional distinct questions required.

Artifacts: question-only-prereview.json/.md; source-read-record.json; input-hashes.json; baseline-explicit-diff.json; original-evidence-regenerated.json; source-key-coverage-review.json; own native-source extractions and renders. All outputs are confined to independent-review-01.
