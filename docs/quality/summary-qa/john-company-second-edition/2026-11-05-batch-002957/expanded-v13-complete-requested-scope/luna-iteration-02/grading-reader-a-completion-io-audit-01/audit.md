# Reader A completion IO audit 01

All six actors received the complete source, metadata and every complete assigned opaque entry before their first report write. All contexts are gpt-6.1-sol/high with the expected actor and parent. All six primary reports reproduce byte for byte using inspected programs with filesystem operations replaced by an in-memory allowlist. Originals are unchanged.

| Block | Frozen strict | Actual input delivery | Report byte replay |
|---|---|---|---|
| block-01 | PASS | Complete | Exact |
| block-02 | PASS | Complete | Exact |
| block-03 | FALSE (preserved) | Complete | Exact |
| block-04 | PASS | Complete | Exact |
| block-05 | FALSE (preserved) | Complete | Exact |
| block-06 | PASS | Complete | Exact |

A03’s extra fixed-reader call fails argument unpacking before any file read; the valid retry delivers the missing chunk. A05 uses identical fixed shell commands with outer JavaScript whitespace differences. These actual findings do not change either frozen strict false result.

Post-boundary programs read only their own packet and, for A01’s follow-up and A06’s hash, their own report. They write only their own report. Every grade, coverage status, reason and quote selection is literal model-selected material; the code only checks identity, counts and literal substrings and assembles the report. No cleanup path, semantic coverage algorithm, factual score cap or authority cap was found.

Replay executes inspected Python only with substituted in-memory Path and restricted imports/builtins. The original shell and original write paths are never executed by this audit. The saved replay files have the exact original report SHA-256 values.

Retained evidence contains only allowlisted tool fields, narrow settings/identity metadata, original physical ordinals and record hashes. No raw sessions or prohibited message/context/reasoning bodies are copied. Initial provenance discovery accidentally printed narrow runtime path/model/effort metadata for other provenance records; no other runtime was opened, and none of that metadata is retained here.

This is a technical delivery/IO audit, not gameplay regrading or proof of attention/correctness. Key and scope files referenced inside packet metadata were not opened.

Evidence: `audit.json`, `input-read-records.json`, `originals-unchanged.json`, and six minimal runtime projections plus six exact replayed reports.
