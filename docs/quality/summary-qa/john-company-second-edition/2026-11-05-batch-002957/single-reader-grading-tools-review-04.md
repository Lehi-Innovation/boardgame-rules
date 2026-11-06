PASS: separately qualified exact-command syntax equivalence. All 72 independent synthetic checks passed; no remaining concrete findings.

The original proof remains frozen at `72face89f06420bbd65671c3fb475a04a94c100a8dc6243ca8fc72e148ecea63`. The variant is `07b3402017f1207c6b16513614b783f4e554cee0864637e48adc98b2adb37589`.

The variant adds only one literal-form builder, three exact permitted-call mappings, and a qualification field. All other functions are identical; removing these additions from `prove` yields the original function AST. The two expressions decode to identical shell commands and argument vectors, including quoted and Unicode paths. The fixed read program is unchanged.

The variant accepts the original, single-literal, and mixed exact forms. The original checker continues to reject the single-literal interface deviation. Changes to the script, either path, mode, index, extra JavaScript or shell code, output handling, or token budget fail certification. This review establishes a separate equivalence proof; it does not claim that original strict syntax was followed.

All six previous fixes remain effective. Tests include orphan/missing/duplicate/wrong call IDs and mode binding, nested truncated-prefix recovery, real appended foreign content, missing pre-boundary retry, frozen input tampering, and exact strict paired aggregation. Full original entries, reports and collections remain preserved.

Only generic authorized code/templates and reviewer-owned tests were read. All helper roots and imported base roots used a synthetic in-memory filesystem. No real source, bank, reader, grade, runtime, history, session or status inputs were accessed. No helpers or templates were edited; no grader was dispatched.

This verdict covers initial-delivery equivalence. Separate auditing of later calls and actual permitted paths remains necessary. Full input hashes, read record and individual synthetic cases are in the accompanying JSON.
