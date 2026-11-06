# Scope adjudication 09 — versioning supplement

The precise minimal recommendation is **no required-fact change for Q058** and **one scope correction within Q088-F02**. Both questions keep their two frozen fact IDs; the supplied total of **328 fact groups is retained**. No other facts or groups change.

Only the Q058/Q088 rows of expanded-v11/grading-scope.json were inspected for this supplement. No iteration09 readers, snapshots, grading, other rows, or new source audit were inspected. Original files and previous reports remain unchanged.

## Q058

The existing row already matches the independent scope distinction: F01 requires the pawn-conditioned one-card reduction (ordinary three becomes two), F02 requires that rule alone does not affect a remote Search, and Vision/depleted-source stopping is explicitly contextual. **No fact requirement, clause map, or exclusion needs changing.** The earlier report’s generic proposed separation is already implemented here.

An optional semantic-note clarification can make explicit that an exact pawn-conditioned “draw one fewer” rule conveys both the ordinary arithmetic and remote-rule exclusion. It cannot excuse an explicit false rule.

**Old semantic_notes:**

Assess the stated requested rule in context; no exact-keyword demand, confidence-label grading, or borrowing from another answer.

**Optional new semantic_notes:**

Assess the stated requested rule in context; no exact-keyword demand, confidence-label grading, or borrowing from another answer. A pawn-conditioned statement that Search draws one fewer card conveys the ordinary three-to-two implication and the exclusion of a remote Search triggered solely by rule; no separate arithmetic recital or separately worded “no” is required when those meanings are clear. Explicit contrary rules remain errors.

## Q088

Keep F01, both fact IDs, both clause mappings, and the existing non-Supremacy exclusion exactly as frozen. Change only F02’s required text and append the allocation fact as explicit context.

**Old Q088-F02 expected_fact:**

Chancellor holds title if Empire collectively meets goal and adds bonus when any Imperial player defends.

**New Q088-F02 expected_fact:**

In Supremacy, the Chancellor adds the held title's bonus when any Imperial player defends.

This preserves the complete requested application to **any Imperial defender**. “Held title” preserves the condition that the power must actually belong to the defending side; it does not award a title bonus when nobody on that side holds the title.

**Append contextual_exclusions entry:**

```json
{
  "key_or_source_fact": "Chancellor holds the Supremacy title if the Empire collectively meets the goal.",
  "classification": "contextual_not_independently_required",
  "rationale": "Title allocation and goal qualification explain who normally supplies the bonus but are not independently requested by the question about bonus amounts, modifier status, and application to Imperial defense. The requirement that the held title power applies when any Imperial player defends remains in Q088-F02.",
  "contradiction_policy": "Absence alone is not penalized; any volunteered materially false ruling is still incorrect."
}
```

No factual gold correction or question rewrite is proposed. Title allocation remains true; its omission alone is not an error for this particular question. A volunteered materially false title-allocation rule still is an error.

## Freeze and provenance

Preserve expanded-v11 unchanged and freeze the exact minimal changes above in a separately versioned scope artifact before another grader uses them. The independent Q058/Q088 decisions remain correct/correct. This is a requested-scope clarification, not full-source saturation.

The 328 total is supplied by the caller; it was not independently recounted, because this review was restricted to the two rows. No group is added or removed.

Input: `/home/jonny/projects/boardgame-rules/docs/quality/summary-qa/oath-chronicles-of-empire-and-exile/2026-11-05-batch-002957/expanded-v11/grading-scope.json`

SHA-256: `631dc23ede2093589dcb4c3b00cd7eae004b75d82b75d3da5b6c543622743478`

The JSON supplement also records canonical hashes of both inspected rows. The complete frozen-scope input hash was verified unchanged after writing these supplements.
