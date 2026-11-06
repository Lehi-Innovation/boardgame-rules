# Independent scope adjudication 09

**Decisions: Q058 correct; Q088 correct.**

No prior grading, prior adjudications, sibling work, parent-chat content, current candidate, or raw reader-a.json was read. The actual supplied unchanged_raw_entry objects in the packet were evaluated.

Packet read in contiguous marked chunks 1–8; frozen summary read in contiguous marked chunks 1–12; each chunk at most 4000 characters, at most two chunks per call. Inner and outer output budgets at least 6000 tokens.

Both full entries include answer, answer_quotations, support, evidence and verbatim_passages. Neither supplied entry has a case_result field; none was invented or treated as evidence.

Targeted source checks for the two questions. Official Reference PDF p.2 was visually rendered because it has no extractable text. This is not a catalog-wide audit of every unrelated rule in the lengthy quoted entries.

## Q058 — correct

**Asked:** How does Marshes change Search, and does it change a remote Search simply because you rule Marshes?

The full raw entry states the exact local trigger and one-card reduction. Its unqualified rule is mandatory and excludes a remote Search triggered by mere rule. It does not contradict Search stopping rules. Requiring an independent recital of those unchanged general rules would broaden this question.

### Q058.a: Draw one fewer card, mandatorily, when pawn is at Marshes.

**Scope:** materially_requested. Direct answer to how Marshes changes Search.

**Reader evidence:**

> - **Marshes:** Search while pawn there draws 1 fewer card.

**Assessment:** met: “draws 1 fewer” states the result as a rule, not an optional permission.

**Sources:** official_reference_pdf — PDF page 2, Site Reference, Marshes (right column).

### Q058.b: Ordinary unmodified Search therefore draws two rather than three.

**Scope:** material_implication_not_separate_recital. Quantitative consequence of the requested one-card reduction, rather than an additional effect. Arithmetic need not be restated if the reduction is exact.

**Reader evidence:**

> - **Marshes:** Search while pawn there draws 1 fewer card.

**Assessment:** met by exact one-card reduction; 3−1=2. This is not permission to draw two despite an applicable stopping rule.

**Sources:** official_reference_pdf — PDF page 2, Site Reference, Marshes (right column); law — printed p.6, §5.1.2; extracted lines 758–764.

### Q058.c: Rule alone without pawn at Marshes does not modify a remote Search.

**Scope:** materially_requested. Explicit second clause of the question.

**Reader evidence:**

> - **Marshes:** Search while pawn there draws 1 fewer card.

**Assessment:** met semantically: the sole trigger supplied is Search while the pawn is there. The raw sentence gives no trigger based on rule. A separately worded “no” would improve directness but add no rule.

**Sources:** official_reference_pdf — PDF page 2, Site Reference, Marshes (right column).

### Q058.d: Still stop at a world-deck Vision or source exhaustion.

**Scope:** contextual_background. True general Search/availability constraints unchanged by Marshes; the question does not ask to restate Search procedure or pose either stopping case.

**Reader evidence:**

No matching statement in the submitted raw entry.

**Assessment:** not stated in this raw entry; no deduction for this omission. No false claim that Marshes bypasses either constraint. The frozen summary independently states them, but that separate passage is not credited as part of this raw entry.

**Sources:** law — printed p.6, §5.1.2; extracted lines 758–764; law — printed p.11, §9.3; extracted lines 1356–1361.

### Exact proposed scope clarification

No factual correction to gold is needed. A versioned grading-scope precision clarification is recommended.

**Old expected answer (unchanged):** Must draw one fewer if pawn there,so ordinary three becomes two,still stop at world Vision/empty source. Rule alone without pawn there does not trigger it.

**Old material_facts:**

```json
[
  "Must draw one fewer if pawn there,so ordinary three becomes two,still stop at world Vision/empty source. Rule alone without pawn there does not trigger it."
]
```

**New required_facts:**

- A Search with pawn at Marshes must draw one fewer card; ordinary three becomes two.
- Ruling Marshes without having the pawn there does not modify a Search elsewhere.

**New context_notes:**

- Ordinary Search stopping at a world-deck Vision and source exhaustion remains applicable, but reciting those rules is not a separate requirement for this question.

**Grading note:** An exact pawn-conditioned one-card reduction satisfies both requested clauses; explicit “must,” “three becomes two,” and “no remote effect” wording is not independently required when clearly conveyed. Explicit contrary rules remain errors.

## Q088 — correct

**Asked:** What mandatory defense-die bonus does the Oathkeeper title give on its Oathkeeper side versus its Usurper side? Is this a Campaign modifier, and how does Supremacy apply it to Imperial defense?

The complete raw entry provides mandatory +1/+2, identifies a Campaign modifier, and explains Chancellor automatic participation and activation/sharing of all relevant modifiers for an Imperial defending side. This gives the requested Supremacy defense application. Supremacy title allocation/qualification is accurate background in the key but is not separately asked here.

### Q088.a: Oathkeeper side must add one defense die; Usurper side must add two.

**Scope:** materially_requested. Explicit first sentence of the question.

**Reader evidence:**

> Apply relevant modifiers and mandatory title defense bonus: Oathkeeper +1 defense die, Usurper +2. The mandatory title bonus is itself a Campaign modifier.

**Assessment:** met explicitly, including mandatory character.

**Sources:** law — printed p.4, §2.11; extracted lines 612–633; law — printed p.8, §7.1.1; extracted lines 1092–1097.

### Q088.b: The title bonus is a Campaign modifier.

**Scope:** materially_requested. Explicit second sentence of the question.

**Reader evidence:**

> Apply relevant modifiers and mandatory title defense bonus: Oathkeeper +1 defense die, Usurper +2. The mandatory title bonus is itself a Campaign modifier.

**Assessment:** met explicitly.

**Sources:** errata — Law Clarifications, §2.11, lines 16–18.

### Q088.c: In Supremacy, apply the held title power when any Imperial player defends, rather than only when Chancellor is declared defender or physically nearby.

**Scope:** materially_requested. The question expressly asks how Supremacy applies the bonus to Imperial defense. This requirement is retained in full.

**Reader evidence:**

> Apply relevant modifiers and mandatory title defense bonus: Oathkeeper +1 defense die, Usurper +2. The mandatory title bonus is itself a Campaign modifier.

> When an Imperial player defends, Chancellor automatically joins as Ally.

> Activate all Campaign modifiers ruled by defender/Allies. **Share powers as one defending side:** their “you,” “your enemy,” and “defender” mean the whole side, while “your site”/“your board” still mean each user’s own location/board. This shares the Oathkeeper defense bonus even outside Supremacy.

**Assessment:** met jointly: Chancellor automatically joins whenever an Imperial player defends; all defender/Ally modifiers activate and the title bonus belongs to the whole side. “Even outside Supremacy” explicitly includes Supremacy as the base case. No pawn-location condition is placed on Chancellor joining. This does not assert the bonus exists when no defending participant holds the title.

**Sources:** law — printed p.4, §2.11; extracted lines 612–633; law — printed p.7, §5.5.2; extracted lines 884–889; errata — Law errata, §5.5 Campaign, lines 81–90.

### Q088.d: For Supremacy, Chancellor physically holds title if Empire meets its goal.

**Scope:** contextual_background. This is title allocation and qualification, not the requested die bonus, modifier classification, or defensive application. It explains why Chancellor normally supplies the power but is not an independent requested fact.

**Reader evidence:**

No matching statement in the submitted raw entry.

**Assessment:** not expressly stated in the submitted raw entry. Do not supply it from frozen-summary line 199 or deduct for its absence in this question. Key fact remains true; no contrary ownership statement appears in raw entry.

**Sources:** law — printed p.4, §2.11; extracted lines 612–633.

### Q088.e: Apply errata side-sharing to participating Imperial defenders/Allies in other Oaths as well.

**Scope:** contextual_background. Question names Supremacy and does not independently ask about other Oaths. The broader errata is relevant authority for interpreting the answer, not an added requested scenario.

**Reader evidence:**

> Activate all Campaign modifiers ruled by defender/Allies. **Share powers as one defending side:** their “you,” “your enemy,” and “defender” mean the whole side, while “your site”/“your board” still mean each user’s own location/board. This shares the Oathkeeper defense bonus even outside Supremacy.

**Assessment:** accurately volunteered and explicitly met; not needed as a separate pass condition.

**Sources:** errata — Law errata, §5.5 Campaign, lines 81–90; law — printed p.7, §5.5.2; extracted lines 884–889.

### Exact proposed scope clarification

No factual correction to gold is needed. A versioned grading-scope precision clarification is recommended.

**Old expected answer (unchanged):** The Oathkeeper must add one defense die; the Usurper must add two. The title bonus is a Campaign modifier. For Supremacy the Chancellor holds the title if the Empire meets the goal and always adds its power when any Imperial player defends. Apply the errata’s side-sharing permissions to participating Imperial defenders/Allies in other Oaths as well.

**Old material_facts:**

```json
[
  "The Oathkeeper must add one defense die; the Usurper must add two",
  "The title bonus is a Campaign modifier",
  "For Supremacy the Chancellor holds the title if the Empire meets the goal and always adds its power when any Imperial player defends",
  "Apply the errata’s side-sharing permissions to participating Imperial defenders/Allies in other Oaths as well."
]
```

**New required_facts:**

- The Oathkeeper must add one defense die; the Usurper must add two.
- The title bonus is a Campaign modifier.
- In Supremacy, the held title power contributes when any Imperial player defends, including when Chancellor is an Ally rather than declared defender.

**New context_notes:**

- Chancellor holds the Supremacy title if the Empire meets the goal.
- Errata shares the title bonus among participating Imperial defending players in other Oaths as well.

**Grading note:** Credit the complete entry when mandatory title bonus, Chancellor automatic Ally status, activation of all defender/Ally Campaign modifiers and title-bonus side-sharing jointly establish application to any Imperial defending side. Do not require an independent restatement of who earns/holds Supremacy title. Do not credit a false claim that every Imperial defense gets a title bonus when no participant holds the title.

## Versioning and preservation

Existing gold contains source-correct facts, but its material_facts combines requested obligations with explanatory background. The decisions above are semantic adjudications of the unchanged questions and unchanged gold, not permission to erase an asked fact. For a new grader, preserve a new versioned scope-clarification artifact with the exact proposed required_facts/context_notes above before dispatch; keep the existing key and packet immutable. No rewrite of the questions is proposed.

Q058: split the single existing material_facts item into required pawn-conditioned reduction/remote-rule exclusion, with world-Vision/source-exhaustion rules in context_notes. Q088: retain material_facts items 1 and 2; split item 3 so “always adds its power when any Imperial player defends” remains required and “Chancellor holds the title if Empire meets goal” moves to context_notes; move item 4 (other Oaths) to context_notes. See each key_assessment for exact old text and proposed replacement strings.

Original packet, key representation, snapshot, and source files remain unchanged. SHA-256 hashes were rechecked after writing; the packet is the actual raw-entry input, and no separate reader-a file was accessed.

## Input SHA-256 hashes

- **packet**: `e7482f407d05f445613f61ff145967d56e8788d10e8040e3e3f01cbd93399ba9` — /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957/expanded-iteration-08/scope-review-packet-09.json
- **frozen_summary**: `39dddb1b0c1e5097c2b0cfd09099dfd519b9df1cf37330d17e75db2dd581da61` — /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957/expanded-iteration-08/summary-snapshot.md
- **law**: `f8bf9a48310fb38132084161fd481f7c303d855a44df3e34d5f798b3ac0ec5cf` — /home/jonny/projects/boardgame-rules/extracted/oath-current-law.txt
- **playbook**: `fa9a525128847fae59cfcac652d7f94cad922bb8005a28a2e0fb4dd36eef0384` — /home/jonny/projects/boardgame-rules/extracted/oath-current-playbook.txt
- **errata**: `395816ef41dc98bceb88983e3d0dc8992f44643630182f29f2c5c137c3c6e1ba` — /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957/errata.txt
- **official_reference_pdf**: `73f00c12d8580acb3678004478ded484794127271d8a903c0c8c9b63df65833f` — /home/jonny/projects/boardgame-rules/docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957/reference.pdf
- **Q058_packet_raw_entry_canonical_json**: `4c7360e6976339090077ebf80cbcbbc7711a910ec686aae814b939362128c62c` — canonical JSON of the packet entry (sorted keys, UTF-8, ensure_ascii=False, compact separators).
- **Q088_packet_raw_entry_canonical_json**: `8bb11a78b7322f1fd584935a4d8208288eb23d5a9e097f650134c12ed3fffddf` — canonical JSON of the packet entry (sorted keys, UTF-8, ensure_ascii=False, compact separators).

## Source wording

- **marshes** — official_reference_pdf, PDF page 2, Site Reference, Marshes (right column): When searching, you must draw one fewer card if your pawn is here.
- **search** — law, printed p.6, §5.1.2; extracted lines 758–764: Draw Three Cards; a world-deck Vision requires stopping drawing immediately.
- **limits** — law, printed p.11, §9.3; extracted lines 1356–1361: Components except secrets and dice are limited; take as many as possible if source is insufficient.
- **title** — law, printed p.4, §2.11; extracted lines 612–633: The Oathkeeper must add one defense die as defender; Usurper must add two. Chancellor holds Supremacy title if Empire meets goal, and always adds its power when any Imperial player defends.
- **modifier** — errata, Law Clarifications, §2.11, lines 16–18: Is the defense die added from the Oathkeeper title considered a campaign modifier? Yes!
- **allies** — law, printed p.7, §5.5.2; extracted lines 884–889: When an Imperial player defends, Chancellor joins as Ally; activate all Campaign modifiers ruled by defender and all Allies.
- **sharing** — errata, Law errata, §5.5 Campaign, lines 81–90: Powers referring to the defender refer to the entire defending side; Oathkeeper bonus is shared among Chancellor and Imperial Allies in non-Supremacy games.
- **mandatory** — law, printed p.8, §7.1.1; extracted lines 1092–1097: Holder of Oathkeeper title always has its mandatory power.
