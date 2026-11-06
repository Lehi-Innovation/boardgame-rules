# Archived Spirit Island runtime evidence

The original runtime transcript exceeds GitHub's single-file limit. This archive preserves every original byte; compression and decompression were checked against its SHA-256. The original remains unchanged locally and is excluded from Git. Other QA evidence is unchanged.

To restore it in a fresh checkout, run from the repository root:

```sh
cat docs/quality/summary-qa/archives/2026-11-06-spirit-island-runtime/root-tool-transcript.json.gz.part-001 docs/quality/summary-qa/archives/2026-11-06-spirit-island-runtime/root-tool-transcript.json.gz.part-002 | gzip -dc > docs/quality/summary-qa/spirit-island/2026-11-05-batch-002957/runtime/root-tool-transcript.json
```

Original SHA-256: `655844fc16f6523fbb55735eba5eca03091ed2759e9cc012d447eff66bb056f6`. Original size: 428988845 bytes. [Manifest](manifest.json) records archive part hashes and order.
