Changes requested. The core cross-date collector and exclusive run-local output guard work, but two validation defects remain.

- RP-01: eight synthetic malformed-shape cases crash collection rather than produce issues: nonobject first/later events, null session/context payloads, malformed nested provenance, and unhashable actor/session IDs. Validate shapes and identifiers before .get/Counter operations; disclose the issue and continue unaffected records.
- RP-02: whitespace-only model/effort values produce confirmed=true. Require non-whitespace strings while preserving raw evidence.

The 24 synthetic cases verify date-independent matching, unrelated-parent exclusion, retention of every context including a later mismatch, missing-context rejection, malformed JSON disclosure, duplicate identifiers, exact snapshot hashes, exclusive existing-file protection and traversal/symlink guards. No real runtime inputs were used.

The helper proves observed metadata settings only. It does not prove terminal status, input isolation, fork setting, attention, incoming encrypted prompt content or answer correctness. confirmed is not agreement with requested settings; downstream checks must compare every context and resolve duplicates/issues.

Source SHA256: `d0bce63073145cf4fa7bafe12e317a38cea786070cb3a6f0337f6b0c388af7f7`. Original tools and indexes were not edited.
