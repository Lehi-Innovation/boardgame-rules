# Independent source interpretation B: John Company Second Edition defense

## Decision for the stated case

**Exhaust the sole active, unused local-alliance piece in full. The strength-1 Crisis fails; the Company defense succeeds.** Move the alliance to the bottom half of its Army box. There is no defense roll in the printed Mounting Defense procedure. Remove all unrest in the attacked region and award the associated Commander a trophy, subject to the rulebook's vacant-Commander exception if that applies.

This follows directly from the p33 instruction to exhaust Army **pieces** equal to Crisis strength: one newly exhausted alliance piece is one newly exhausted Army piece, meeting strength 1. The alliance's printed 2 does not make it two physical pieces. A scenario-specific FAQ is unnecessary to reach this case result.

## Scope and source inspection

I worked independently from the neutral case, consulted only the four authorized primary files, and did not consult other reviews, summaries, keys, prior positions, or web sources. I visually inspected native rulebook printed pages 22 and 33 and both complete player-aid pages, using the rendered images saved here. I read complete extracted p22 and p33 and the surrounding specific sections recorded in `source-read-record.json`. I do not claim to have read the entire rulebook or all published clarifications. Input SHA256 values were captured and rechecked; all four sources remained unchanged.

The request's bounded-output rule was missed once: the initial text response contained two 60-line ranges in one response. There was no truncation; later responses were bounded individually, and complete p22 was reread within 55 lines. This affected output sizing, not which sources were consulted.

## Exact source evidence

**Q1 — rulebook printed p22; supplied text lines 1623–1627.**

> Local alliances are temporary Army pieces. Their strength can be used for two purposes: the Deploy action and to defend against threats in India during the Events in India phase. Each piece can only be used once on the turn they are purchased, and its strength cannot be split among more than one purpose.

**Q2 — rulebook printed p22; supplied text lines 1638–1642.**

> Each officer or regiment you exhaust gives you one die. In addition, each local alliance in your Army you exhaust will give you the number of dice indicated on the piece. To exhaust an officer, regiment, or local alliance, move it to the bottom half of its respective Army box.

**Q3 — rulebook printed p33; supplied text lines 2286–2292.**

> The Commander associated with the region must exhaust pieces in the Army equal to the strength of the Crisis or as many as possible. If the newly-exhausted pieces do not equal the strength of the Crisis, the Crisis succeeds. Perform the steps of Region Loss (page 29). If the attack failed, remove all unrest in the attacked region and the Commander associated with the region should take a trophy token.

**Q4 — player aid PDF page 1; supplied text lines 73–75.**

> Roll 1 die for each officer, regiment used. In addition roll dice equal to the strength of any alliances used.

**Q5 — player aid PDF page 2; supplied text lines 170–175.**

> Defender Strength; Successful (defender wins ties)

Two distinct table column headers; punctuation semicolon added to separate the headers.

**Q6 — player aid PDF page 2; supplied text lines 197–217.**

> Exhausted Regiments, Officers, and Local Alliances

Attack on the Company row, Defender Strength column. Unsuccessful attack column says Clear unrest. Commander gains a trophy.

**Q7 — rulebook printed p36; supplied text lines 2619–2620.**

> Any exhausted officers and regiments become active. Any active local alliances are exhausted.

**Q8 — rulebook printed p17; supplied text lines 1346–1349.**

> Most actions that concern India require the acting player to make a check to see if their actions are successful. Each check requires a roll of the dice. The number of dice you roll is dependent on the resources you have and want to spend as determined by the action.

**Q9 — rulebook printed p3; supplied text lines 148–150.**

> There are 20 regiments and 7 local alliance pieces which strengthen Company armies.

## Literal statements and their application

The literal statements are that alliances are temporary Army pieces (p22), that their strength can be used for Deploy and defense (p22), that each piece is usable once and cannot split its strength among purposes (p22), that exhausted alliances provide the dice printed on them for Deploy (p22), and that defense exhausts newly exhausted pieces equal to Crisis strength or as many as possible (p33). The player aid expressly includes local alliances among the exhausted defenders.

My application of the specific defense instruction counts eligible physical Army pieces: officers, regiments, and local alliances. Already exhausted pieces cannot become newly exhausted for this attack. Nothing in p33 says to roll their Deploy dice or to replace one alliance piece with a number of pieces equal to its printed dice. The strength-2 alliance is one piece when exhausted, even though it would provide two dice for Deploy.

The general Success Checks section (p17) says dice resources depend on the particular action. Deploy explicitly makes a check and specifies alliance dice. Mounting Defense specifies exhaustion and a result without a check. The Deploy example and Company-controlled regions' zero defending regional strength in the Deploy paragraph concern that action's dice penalty; they do not replace the separate p33 defense procedure.

The once-per-piece rule requires full exhaustion for this defense. No unused printed point remains available. Spending the piece for this attack does not split its strength among Deploy and defense, or between uses. Even if both uses were described as defense, the separate once-per-piece restriction prevents reusing it in a second attack this turn. The no-splitting sentence is not an exact-match restriction on a piece's printed number.

## Alternative readings and their limits

1. **Weighted defense:** p22's sentence that alliance strength can defend provides a real basis to infer that a strength-2 alliance contributes defense 2. That is a whole-text inference; p33 does not expressly say “sum the printed strengths.” The player aid's Defender Strength column and “defender wins ties” heading support an ordinary comparison of attacker and defender, but supply no additional numerical formula for alliances. I retain this as a competing reading for cases where weight and piece count diverge. I prefer the specific p33 physical-piece instruction as the most direct application.
2. **One alliance literally becomes two pieces:** rejected as a literal claim. Printed strength and physical piece count are different quantities in p22 itself: exhausting one alliance grants its indicated number of dice. A weighted interpretation must acknowledge its substitution rather than call it an express piece-count rule.
3. **Strength 2 cannot defend against strength 1 because it cannot be split:** rejected. The whole piece is used once for one purpose. Neither p22 nor the aid forbids a use whose printed capacity exceeds the immediate need. Under the p33 physical count, the equality is exactly 1 = 1.
4. **Weighted exact equality makes excess defense fail:** not adopted. This imports a weighted metric while retaining a strict equality sentence phrased in pieces, and sits poorly with the aid's defender-wins-ties comparison. It is not a basis to claim the stated case is unresolved.
5. **A missing scenario FAQ prevents any answer:** rejected. The stated case has a direct p33 application. Uncertainty about numerical weighting in other cases should not be transferred into this case.

## Generalization and genuine uncertainty

For a **strength-2 Crisis with only this alliance**, my preferred literal p33 application exhausts the one piece as many as possible. One newly exhausted physical piece is insufficient against 2, so the Crisis succeeds. Confidence in that extension is lower than in the stated strength-1 outcome: under the competing p22 weighted-strength inference, the alliance supplies 2 and holds instead. I do not present this extension as an unqualified designer ruling. The precise unresolved broader issue is whether the general p22 alliance-strength language is intended to override the specific p33 piece count when those metrics diverge. No extra numerical conversion rule appears in the inspected defense text or aid. This uncertainty does not affect the requested strength-1 decision.

For **more active physical pieces than Crisis strength**, p33 says to exhaust the required number, not every available piece. “Or as many as possible” covers a shortage; it does not instruct intentional over-exhaustion when exact physical counts are available. Since each physical piece increments the count by one, physical-piece overshoot need never be forced.

For **printed alliance strength greater than Crisis strength**, the stated case is already such an example: the whole printed-2 piece exhausts, its newly exhausted piece count is 1, and defense holds against 1. This is not permission to save or split the spare point. On a weighted approach the player aid supports the normal defender-at-least-as-strong interpretation, but p33 supplies no explicit weighted-overshoot selection algorithm. I therefore do not invent a universal exact-match or overkill rule for weighted armies.

## Evidence artifacts

- `source-interpretation.json`: machine-readable verdict, cases, uncertainty, alternatives, and quotes.
- `input-manifest.json`: four primary input paths, original and final SHA256 values, unchanged flags.
- `source-read-record.json`: exact text ranges, complete pages, discovery searches, and inspected image record.
- `rules-page-22.png` and `rules-page-33.png`: native rulebook pages actually inspected.
- `aid-page-1.png` and `aid-page-2.png`: both native player-aid pages actually inspected.
- Four `*-native-extraction.txt` files: own page-specific derivatives; the supplied extracts were used for line references.
