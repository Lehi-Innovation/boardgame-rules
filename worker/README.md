# Remote MCP Server (Cloudflare Worker)

A remote [MCP](https://modelcontextprotocol.io) server that lets anyone add
the board game rules corpus to **their own** Claude / ChatGPT account as a
custom connector. All LLM inference runs on the user's account — this Worker
only serves rules text and runs keyword search, which is why it fits in
Cloudflare's free tier.

```
User's phone ──► their AI (their account, their tokens)
                     │  MCP tool calls (Streamable HTTP)
                     ▼
              this Worker ──► static assets (games.json, rules/, extracted/)
                     └──────► Workers KV (optional feedback queue)
```

## Tools

| Tool | Purpose |
|---|---|
| `list_games` | Resolve a fuzzy game name against the catalog |
| `get_rules` | Full rules summary (markdown, with verification banner) |
| `search_rulebook` | Keyword search over the extracted rulebook text (the authoritative source) |
| `read_rulebook` | Read a line window of the rulebook text (follow-up to search) |
| `log_ruling` | Log a Q&A that went beyond the summary → feedback queue |
| `report_rule_error` | Report a wrong summary → feedback queue + prefilled GitHub issue link |

The server is **stateless** (plain JSON responses, no session IDs, no auth on
`/mcp`) and hand-rolls the protocol in ~200 lines — no SDK dependency.

## Deploy

Prereqs: a free Cloudflare account, Node 20+.

```bash
cd worker
npm install
npx wrangler login       # one-time browser auth
npm run deploy           # stages the corpus into public/ and deploys
```

The deploy prints your URL, e.g.
`https://boardgame-rules-mcp.<your-subdomain>.workers.dev`. The MCP endpoint
is that URL plus **`/mcp`**. Sanity-check with:

```bash
curl -s https://<your-worker>/healthz
curl -s https://<your-worker>/mcp -X POST -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

### Optional: the feedback queue

Without this, `log_ruling` / `report_rule_error` degrade to GitHub links.

```bash
npx wrangler kv namespace create RULINGS
# paste the printed id into wrangler.jsonc (uncomment the kv_namespaces block)
npx wrangler secret put ADMIN_TOKEN     # any long random string
npm run deploy
```

### Optional: auto-deploy from GitHub

`.github/workflows/deploy-mcp.yml` redeploys on every push to `main` that
touches `worker/`, `rules/`, `extracted/`, or `games.json` — so the connector
always serves the latest corpus. Add two repo secrets and it activates:
`CLOUDFLARE_API_TOKEN` (Workers Scripts: Edit; plus Workers KV Storage: Edit
if using the queue) and `CLOUDFLARE_ACCOUNT_ID`. Without them it skips cleanly.

## Connecting an assistant

- **Claude (paid plans):** Settings → Connectors → **Add custom connector** →
  paste `https://<your-worker>/mcp`. Works on claude.ai, desktop, and the
  mobile apps — including voice mode at the table.
- **ChatGPT:** Settings → Connectors → Advanced → enable Developer mode →
  add the same URL as an MCP server.
- **Claude Code / other MCP clients:** any Streamable HTTP client config
  pointing at `/mcp` works.
- **No connector support / free tier:** the copy-paste prompt on the
  [site landing page](https://lehi-innovation.github.io/boardgame-rules/)
  remains the zero-setup path — keep pointing people there.

## Local development

```bash
npm test             # vitest — protocol, tools, search, admin API
npm run typecheck
npm run dev          # stages assets + wrangler dev on http://localhost:8787
npx @modelcontextprotocol/inspector   # point it at http://localhost:8787/mcp
```

## Feedback queue admin API

The nightly triage job (or a manual session) drains the queue, verifies
submissions against the extracted rulebook text, merges confirmed ones as
`## FAQ & Rulings` entries or summary fixes, then acks:

```bash
# List queued rulings/error reports (kind=rulings) or catalog misses (kind=misses)
curl -s -H "Authorization: Bearer $ADMIN_TOKEN" \
  "https://<your-worker>/admin/export?kind=rulings&limit=100"

# Delete processed keys
curl -s -X POST -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"keys":["q:2026-08-05T...:ab12cd34"]}' \
  "https://<your-worker>/admin/ack"
```

`miss:` entries record game names users asked for that aren't in the catalog
(auto-expire after 60 days) — a ranked to-add list for free.

## Costs & scaling notes (as of 2026)

- **Workers free tier:** 100k requests/day. Static-asset requests (the corpus
  files) are free and don't count. A busy game night is ~20 tool calls.
- **KV free tier:** 1k writes/day — also a natural spam cap on the queue.
  For abuse beyond that, add a Cloudflare WAF rate-limiting rule on `/mcp`;
  no code changes needed.
- **Corpus updates:** assets ship with each deploy (~46 MB, diffed on upload),
  so the CI workflow keeps the connector in sync with `main`.
- Search is keyword-based (ported from `mcp_server/server.py`), not
  embeddings: free, deterministic, and the client LLM iterates on terms —
  which it's told to do in the tool description.
