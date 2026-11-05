/** Board Game Rules — remote MCP server (Cloudflare Worker).
 *
 * Routes:
 *   POST /mcp            MCP Streamable HTTP endpoint (stateless JSON mode)
 *   GET  /               human-facing info page
 *   GET  /healthz        liveness + staged-corpus check
 *   GET  /admin/export   feedback queue export (Bearer ADMIN_TOKEN)
 *   POST /admin/ack      delete processed queue keys (Bearer ADMIN_TOKEN)
 *   GET  /games.json, /rules/<slug>.md, /extracted/<slug>-rules.txt
 *                        served directly by the static assets layer
 */

import type { Env } from "./env";
import { AssetsCorpus } from "./corpus";
import { handleMcpPost } from "./mcp";
import { handleAdmin } from "./rulings";
import { corsHeaders, preflight, json } from "./http";
import { SITE_BASE, REPO_URL, SERVER_TITLE, SERVER_VERSION } from "./config";

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") return preflight();

    if (url.pathname === "/mcp") {
      if (request.method === "POST") return handleMcpPost(request, env);
      return new Response(
        "This is an MCP endpoint (Streamable HTTP, stateless). Connect an MCP client via POST.",
        { status: 405, headers: { allow: "POST, OPTIONS", ...corsHeaders() } },
      );
    }

    if (url.pathname.startsWith("/admin/")) return handleAdmin(request, env);

    if (url.pathname === "/healthz") return healthz(env);

    if (url.pathname === "/" && request.method === "GET") {
      return homePage(url.origin, env);
    }

    // Anything else that reached the Worker missed the static assets too.
    return new Response("Not found", { status: 404, headers: corsHeaders() });
  },
};

async function healthz(env: Env): Promise<Response> {
  try {
    const games = await new AssetsCorpus(env.ASSETS).manifest();
    return json({
      ok: true,
      version: SERVER_VERSION,
      games: games.length,
      feedback_queue: Boolean(env.RULINGS),
    });
  } catch (err) {
    const detail = err instanceof Error ? err.message : String(err);
    return json({ ok: false, error: detail }, 500);
  }
}

async function homePage(origin: string, env: Env): Promise<Response> {
  let gameCount = "1,600+";
  try {
    const games = await new AssetsCorpus(env.ASSETS).manifest();
    gameCount = games.length.toLocaleString("en-US");
  } catch {
    // Cosmetic only.
  }
  const mcpUrl = `${origin}/mcp`;
  const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${SERVER_TITLE} — MCP server</title>
<style>
  body { font-family: system-ui, sans-serif; max-width: 42rem; margin: 2rem auto; padding: 0 1rem; line-height: 1.55; color: #1a1a1a; background: #fff; }
  @media (prefers-color-scheme: dark) { body { color: #e6e6e6; background: #121212; } a { color: #8ab4f8; } code, pre { background: #1e1e1e; } }
  code, pre { background: #f2f2f2; padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.95em; }
  pre { padding: 0.75rem; overflow-x: auto; }
  h1 { font-size: 1.5rem; } h2 { font-size: 1.15rem; margin-top: 2rem; }
</style>
</head>
<body>
<h1>🎲 ${SERVER_TITLE}</h1>
<p>A remote <a href="https://modelcontextprotocol.io">MCP</a> server exposing
AI-friendly rules for <strong>${gameCount} board games</strong> — built for asking your
own AI assistant rules questions in the middle of a game. Your assistant does the
thinking on your account; this server only serves rules text.</p>

<h2>Add to Claude</h2>
<p>In the Claude app or claude.ai: <strong>Settings → Connectors → Add custom
connector</strong>, then paste:</p>
<pre>${mcpUrl}</pre>
<p>Then just ask — <em>"How does trading work in Catan?"</em> Works in voice mode
at the table. Other MCP clients (ChatGPT developer-mode connectors, etc.) use the
same URL.</p>

<h2>No connector? No problem</h2>
<p>Any assistant that can fetch web pages works with the copy-paste prompt on the
<a href="${SITE_BASE}/">rules site</a> — no setup, no account requirements.</p>

<h2>Trust</h2>
<p>Summaries are fact-checked against extracted rulebook text and carry a
verification banner; the full rulebook text is served as the authoritative
fallback. Wrong answer at the table? The assistant can file a report and the
database gets fixed via a source-verified pull request.
<a href="${REPO_URL}">Source &amp; docs</a>.</p>
</body>
</html>`;
  return new Response(html, {
    headers: { "content-type": "text/html; charset=utf-8", ...corsHeaders() },
  });
}
