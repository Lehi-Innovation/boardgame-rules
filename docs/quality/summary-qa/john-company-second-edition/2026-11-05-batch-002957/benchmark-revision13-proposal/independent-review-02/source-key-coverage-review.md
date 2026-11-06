# Independent revision02 source, key, asked-scope and coverage review

**PASS** for all 116 questions and 914 mandatory atoms within the declared scope. All five review01 findings are resolved. No additional meaningful distinct question is required. One stale rationale sentence merits documentation cleanup; it does not change the key, mandatory facts or grading scope.

The Q115/Q116 question-only prereview was saved before opening the new key, scope or revision02 ledgers. The complete review01 is reused only for exact unchanged same-question facts with unchanged source/input hashes. No summary, readers, grades, outside review history, runtime logs, web or collaboration/status tools were used.

## Correction verification

### Q014: PASS

Exact phrase: “how does Standing change, and when are expectations and dividends checked?”

Source truth: Rules p27 LF1900–1902 says immediate Final Scoring; LF1918–1934 places embarrassment, expectations and dividends in order.

Asked scope: Stopping after failure is consequential to when the later steps occur; conditional rewrites preserve the requested timings rather than narrowing them.

Prior IR01-SCOPE-014 resolved. No additional question needed.

Original rules p27, physical LF1900–1902:

> During this phase, the Company’s Standing will often be adjusted. If the 
> Standing marker is moved to the leftmost position of the Standing track, the 
> Company has failed. Go to the Final Scoring immediately (page 9). 

Original rules p27, physical LF1918–1934:

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

### Q025: PASS

Exact phrase: “Can promises or negotiations continue in Final Scoring?”

Source truth: The original final-scoring paragraph forbids all three activities and permits explicit blackmail-card play. It provides no general permission to negotiate or cash promises.

Asked scope: The question names promises/negotiations. Blackmail exception remains optional here and explicitly tested by Q102.

Prior IR01-SCOPE-025 resolved. Documentation rationale cleanup noted separately; no mandatory-scope issue remains.

Original rules p9, physical LF843–847:

> Once the game is over, players may not 
> negotiate, cash in promises, or play 
> blackmail cards (unless a card’s text explicitly 
> allows it). Then players perform the Final 
> Scoring phase.

### Q024: PASS

Exact phrase: “distribute holdings”

Source truth: LF415 is Page 5. LF422–423 places member in office and gives card to player. Key reference and correction ledger basis/source_references_after all now say p5.

Asked scope: No change to holdings or mandatory obligations.

Prior IR01-CITATION-024 resolved.

Original rules p5, physical LF415–425:

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

### Q114: PASS_UNCHANGED

Exact phrase: “Which Company account is charged for ordinary Revenue expenses”

Source truth: Company Balance marker is lowered by expense total.

Asked scope: Account identity and marker debit are directly asked, distinct from Q100 cost census and Q014 emergency shortfalls.

Prior accepted Q114 novelty preserved.

Original rules p27, physical LF1903–1906:

> Expenses
> First, lower the Company Balance marker by £1 for each debt as indicated by 
> the Company Debt track, each regiment and officer in an Army (do not include 
> Commanders), and each ship in the three sea zones.

### Q115: PASS

Exact phrase: “which region loses a tower level?”

Source truth: LF2208 directly removes one tower level from attacker after failed Invasion.

Asked scope: The single fact states exactly the requested loss destination and quantity, without imposing strength/flags/March context.

Prior IR01-COVERAGE-INVASION closed.

Novelty: Q050 asks comparison/ties/flags but did not mandate this tower outcome; Q015 is Company defense, Q051 failed Rebellion damages capital. This is the distinct ordinary non-Company failure branch.

Original rules p32, physical LF2192–2208:

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

### Q116: PASS

Exact phrase: “Who chooses whether an ordinary non-Hobnobbing firm pays dividends and how many? May the manager choose none even when India-treasury cash is available?”

Source truth: LF2889 says manager may choose a number using India funds; optionality permits zero. India cash bounds the chosen number.

Asked scope: Actor/discretion and zero despite available cash are the two explicit interrogatives. India-funds limitation is both the question context and an appropriate boundary on the number chosen. No extra rate/waiver/marker atoms were introduced.

Prior IR01-COVERAGE-FIRM-DIVIDENDS closed.

Novelty: Q020 asks funding/calculation; Q101 waiver/marker/remainder; Q066 forbids Hobnob dividends; Q112 Company discretion. None asks ordinary firm-manager payout discretion.

Original rules p42, physical LF2888–2893:

> Firm Dividends
> The manager may choose to pay out a number of dividends using cash 
> in the firm’s India treasury. For each dividend, £1 for each share is paid 
> to the player owning that share and £1 is given to the player who is the 
> manager of the firm. All cash from dividends is only taken from the India 
> treasury.

## Exact delta and all-atom accounting

All existing 114 question objects are unchanged; the original 113 also match v12 exactly. Q114 question/key/scope row is identical. Existing key entries change only Q024’s page reference and Q025’s clarified contextual wording. Scope rows change only Q014 and Q025. Grading scope and normative source qualification are unchanged.

914 = 911 + 1 restored Q014 condition − 1 unasked Q025 context atom + 3 new atoms. Two Q014 timing atoms are rewritten conditionally without changing their count. There are 908 exact unchanged same-question atoms and six modified/restored/new atoms explicitly verified here. Every candidate atom is accounted for in the JSON report with separate source and asked-scope verdicts and explicit reuse references.

All 173 registered physical-LF quotations match their actual original source files. Manifest candidate hashes, parent-candidate hashes and every input hash from review01 independently match. Original sources and prior reports remain unchanged.

## Renewed working coverage

Sweeps 25 and 26 support targeted zero-addition findings after the corrections. A broader source-only challenge also considered setup, negotiation, retirement, hiring, office transfers, GG conversion, firm investments, rescues, special retirements, Cascades, voting and final scoring. No remaining consequential distinct procedure was found outside the two questions now added.

| Potential omission | Result | Reason |
|---|---|---|
| Additional separate question for manager-zero versus Hobnob-zero | NO_ADDITION | The genuinely different prohibition/discretion and marker branches are already expressly asked. |
| Another failed ordinary Invasion named-region fixture | NO_ADDITION | Would only recombine comparison/tie rules with the now-direct tower outcome. |
| Army movement activation/trainee destinations omitted outside the new questions | COVERED | Two optional transfers, mandatory trainees, active top-half placement and Commander choice/demotion are actually asked. |
| Director transfer count/China destinations or hiring gates omitted | COVERED | Envoy outcomes/immediate hire, dice, two transfers and China ship eligibility remain directly requested. |
| GG replacement hiring/treasury/time or repeated-check unrest omitted | COVERED_OR_CLEAR_IMPLICATION | Director replacement preserves the hiring/operation context; concrete conversion and new Govern costs/options/conditions are requested. No distinct new decision branch was found. |
| Special retirement with supply piece, discounts, zero marker or final failure omitted | COVERED | Every consequential eligibility/cap/timing distinction is directly asked, including final retirement despite Company failure. |
| Share investment at cap, weak/immature shares or emergency rescue remnants omitted | COVERED | Bank cash source, share/workshop restrictions, continued investment without more shares, Value loss and discarded rescue remainder are directly asked. |
| Cascade triggered merely by full region, or repeated flooding/overflow omitted | COVERED | Need-to-close condition is supplied by the event setting; alternate target, one overflow per tile and repeated floods remain requested. Revised Q090 explicitly retains conditional Cascade. |
| Failure stopping in Events or Parliament confused with Revenue stopping | COVERED | Revenue immediate stopping is now mandatory; Events finishes phase and legislation finishes vote in their own direct questions. |
| Negotiation transfer reactivation, promise choice or card visibility omitted | COVERED | Immediate/future binding difference, simultaneous promise choice, no reactivation, visibility and used-card restrictions are asked. |
| Voting/opposition transition and failed-law policy routing omitted | COVERED | All voting rounds, support setup, coalition/PM exceptions, ties and passed/failed resolution branches are asked. |
| Individual starting holdings/maps or card-power catalog omissions | WITHIN_COMPONENT_REFERENCE_BOUNDARY | Exact holdings/map configurations and individual powers may be read from components; common setup, scenario tracks and retained corrected effects remain asked. |
| Separate questions for initial India/law deck shuffle or the former Chairman announcing a known majority | REJECT_AS_ROUTINE_ADMINISTRATIVE_GRANULARITY | These are true original setup/administration instructions but add no distinct decision, outcome or exception beyond common shuffled-deck preparation/election threshold. Do not silently make them mandatory under unrelated clauses. Working saturation is meaningful procedural coverage, not one interrogative per printed instruction. |

This signoff covers standard 3–6 multiplayer, all four named scenarios and firms, plus the attributed general user-approved defense-strength ≥ attack interpretation. The reported publisher email remains unverified and is not a blocker. Crown/solo/two-player, optional draft and exhaustive card catalogs are excluded; exact holdings/maps and individual powers may be read from components. Working saturation concerns meaningful procedures and outcomes, not one question per routine setup instruction or proof of all possible interactions.

## Nonblocking documentation cleanup

Q025’s seven `fact_justifications` still repeat this obsolete sentence:

> End triggers, immediate-versus-finish-phase exceptions and Final Scoring negotiation/promise limits are explicit; card permission qualifies the requested prohibition.

Replace it with:

> End triggers, immediate-versus-finish-phase exceptions and Final Scoring negotiation/promise limits are explicit. The card-text exception concerns blackmail play, is contextual here, and is directly asked by Q102.

The current seven mandatory facts, corrected expected answer and `contextual_extra_dispositions` already use the right boundary. This cleanup requires no atom or question change.

## All-question accounting

| Question | Atoms | Source / asked scope |
|---|---:|---|
| Q001 | 9 | PASS / PASS |
| Q002 | 9 | PASS / PASS |
| Q003 | 8 | PASS / PASS |
| Q004 | 6 | PASS / PASS |
| Q005 | 8 | PASS / PASS |
| Q006 | 9 | PASS / PASS |
| Q007 | 12 | PASS / PASS |
| Q008 | 7 | PASS / PASS |
| Q009 | 8 | PASS / PASS |
| Q010 | 12 | PASS / PASS |
| Q011 | 13 | PASS / PASS |
| Q012 | 15 | PASS / PASS |
| Q013 | 16 | PASS / PASS |
| Q014 | 13 | PASS / PASS |
| Q015 | 17 | PASS / PASS |
| Q016 | 11 | PASS / PASS |
| Q017 | 13 | PASS / PASS |
| Q018 | 17 | PASS / PASS |
| Q019 | 21 | PASS / PASS |
| Q020 | 12 | PASS / PASS |
| Q021 | 12 | PASS / PASS |
| Q022 | 16 | PASS / PASS |
| Q023 | 7 | PASS / PASS |
| Q024 | 15 | PASS / PASS |
| Q025 | 7 | PASS / PASS |
| Q026 | 14 | PASS / PASS |
| Q027 | 6 | PASS / PASS |
| Q028 | 8 | PASS / PASS |
| Q029 | 2 | PASS / PASS |
| Q030 | 20 | PASS / PASS |
| Q031 | 4 | PASS / PASS |
| Q032 | 5 | PASS / PASS |
| Q033 | 11 | PASS / PASS |
| Q034 | 5 | PASS / PASS |
| Q035 | 10 | PASS / PASS |
| Q036 | 9 | PASS / PASS |
| Q037 | 3 | PASS / PASS |
| Q038 | 11 | PASS / PASS |
| Q039 | 3 | PASS / PASS |
| Q040 | 7 | PASS / PASS |
| Q041 | 5 | PASS / PASS |
| Q042 | 6 | PASS / PASS |
| Q043 | 10 | PASS / PASS |
| Q044 | 10 | PASS / PASS |
| Q045 | 11 | PASS / PASS |
| Q046 | 7 | PASS / PASS |
| Q047 | 9 | PASS / PASS |
| Q048 | 4 | PASS / PASS |
| Q049 | 5 | PASS / PASS |
| Q050 | 8 | PASS / PASS |
| Q051 | 6 | PASS / PASS |
| Q052 | 19 | PASS / PASS |
| Q053 | 7 | PASS / PASS |
| Q054 | 16 | PASS / PASS |
| Q055 | 9 | PASS / PASS |
| Q056 | 8 | PASS / PASS |
| Q057 | 8 | PASS / PASS |
| Q058 | 10 | PASS / PASS |
| Q059 | 11 | PASS / PASS |
| Q060 | 8 | PASS / PASS |
| Q061 | 7 | PASS / PASS |
| Q062 | 4 | PASS / PASS |
| Q063 | 8 | PASS / PASS |
| Q064 | 10 | PASS / PASS |
| Q065 | 6 | PASS / PASS |
| Q066 | 6 | PASS / PASS |
| Q067 | 8 | PASS / PASS |
| Q068 | 3 | PASS / PASS |
| Q069 | 4 | PASS / PASS |
| Q070 | 5 | PASS / PASS |
| Q071 | 20 | PASS / PASS |
| Q072 | 8 | PASS / PASS |
| Q073 | 13 | PASS / PASS |
| Q074 | 13 | PASS / PASS |
| Q075 | 5 | PASS / PASS |
| Q076 | 12 | PASS / PASS |
| Q077 | 3 | PASS / PASS |
| Q078 | 7 | PASS / PASS |
| Q079 | 9 | PASS / PASS |
| Q080 | 3 | PASS / PASS |
| Q081 | 10 | PASS / PASS |
| Q082 | 5 | PASS / PASS |
| Q083 | 6 | PASS / PASS |
| Q084 | 3 | PASS / PASS |
| Q085 | 3 | PASS / PASS |
| Q086 | 12 | PASS / PASS |
| Q087 | 7 | PASS / PASS |
| Q088 | 10 | PASS / PASS |
| Q089 | 3 | PASS / PASS |
| Q090 | 4 | PASS / PASS |
| Q091 | 2 | PASS / PASS |
| Q092 | 6 | PASS / PASS |
| Q093 | 6 | PASS / PASS |
| Q094 | 2 | PASS / PASS |
| Q095 | 5 | PASS / PASS |
| Q096 | 6 | PASS / PASS |
| Q097 | 7 | PASS / PASS |
| Q098 | 7 | PASS / PASS |
| Q099 | 2 | PASS / PASS |
| Q100 | 6 | PASS / PASS |
| Q101 | 5 | PASS / PASS |
| Q102 | 2 | PASS / PASS |
| Q103 | 7 | PASS / PASS |
| Q104 | 7 | PASS / PASS |
| Q105 | 3 | PASS / PASS |
| Q106 | 3 | PASS / PASS |
| Q107 | 4 | PASS / PASS |
| Q108 | 2 | PASS / PASS |
| Q109 | 3 | PASS / PASS |
| Q110 | 4 | PASS / PASS |
| Q111 | 4 | PASS / PASS |
| Q112 | 9 | PASS / PASS |
| Q113 | 2 | PASS / PASS |
| Q114 | 2 | PASS / PASS |
| Q115 | 1 | PASS / PASS |
| Q116 | 2 | PASS / PASS |

**Total: 116 questions; 914 source-supported and requested/clearly implied atoms; zero wrong or unasked mandatory atoms; zero additional meaningful questions required.**

See source-key-coverage-review.json for every atom, exact-delta.json for the complete changed entries, original-LF-quote-validation.json for source reconstruction, source-read-record.json for staging, and input-hashes.json for all inputs.
