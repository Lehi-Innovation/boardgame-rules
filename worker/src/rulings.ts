/** Authenticated admin API over the feedback queue (Workers KV).
 *
 * The nightly triage job exports queued rulings/error reports, verifies them
 * against the extracted rulebook text, merges the good ones (FAQ entries or
 * summary fixes), then acks the processed keys.
 *
 *   GET  /admin/export?kind=rulings|misses&limit=100&cursor=...
 *   POST /admin/ack   {"keys": ["q:...", "miss:..."]}
 *
 * Requires `Authorization: Bearer $ADMIN_TOKEN`. With no ADMIN_TOKEN secret
 * configured the API is disabled (503); with no RULINGS binding it is 501.
 */

import type { Env, KVLike } from "./env";
import { json } from "./http";

const PREFIXES: Record<string, string> = {
  rulings: "q:",
  misses: "miss:",
};

function authorized(request: Request, env: Env): Response | null {
  if (!env.ADMIN_TOKEN) {
    return json({ error: "admin API disabled: no ADMIN_TOKEN configured" }, 503);
  }
  const header = request.headers.get("authorization") ?? "";
  if (header !== `Bearer ${env.ADMIN_TOKEN}`) {
    return json({ error: "unauthorized" }, 401);
  }
  return null;
}

export async function handleAdmin(request: Request, env: Env): Promise<Response> {
  const denied = authorized(request, env);
  if (denied) return denied;
  if (!env.RULINGS) {
    return json({ error: "feedback queue not configured: no RULINGS KV binding" }, 501);
  }

  const url = new URL(request.url);
  if (url.pathname === "/admin/export" && request.method === "GET") {
    return exportQueue(url, env.RULINGS);
  }
  if (url.pathname === "/admin/ack" && request.method === "POST") {
    return ackKeys(request, env.RULINGS);
  }
  return json({ error: "not found" }, 404);
}

async function exportQueue(url: URL, kv: KVLike): Promise<Response> {
  const kind = url.searchParams.get("kind") ?? "rulings";
  const prefix = PREFIXES[kind];
  if (!prefix) {
    return json({ error: `unknown kind "${kind}" (expected rulings|misses)` }, 400);
  }
  const limit = Math.min(Math.max(Number(url.searchParams.get("limit") ?? 100) || 100, 1), 200);
  const cursor = url.searchParams.get("cursor") ?? undefined;

  const listed = await kv.list({ prefix, limit, cursor });
  const items = await Promise.all(
    listed.keys.map(async ({ name }) => {
      const value = await kv.get(name);
      let parsed: unknown = null;
      try {
        parsed = value === null ? null : JSON.parse(value);
      } catch {
        parsed = { raw: value };
      }
      return { key: name, value: parsed };
    }),
  );
  return json({
    kind,
    items,
    complete: listed.list_complete,
    ...(listed.cursor ? { cursor: listed.cursor } : {}),
  });
}

async function ackKeys(request: Request, kv: KVLike): Promise<Response> {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return json({ error: "body must be JSON" }, 400);
  }
  const keys = (body as { keys?: unknown }).keys;
  if (!Array.isArray(keys) || keys.some((k) => typeof k !== "string")) {
    return json({ error: 'body must be {"keys": ["q:...", ...]}' }, 400);
  }
  if (keys.length > 200) {
    return json({ error: "too many keys (max 200 per call)" }, 400);
  }
  const valid = (keys as string[]).filter((k) =>
    Object.values(PREFIXES).some((p) => k.startsWith(p)),
  );
  await Promise.all(valid.map((k) => kv.delete(k)));
  return json({ deleted: valid.length, ignored: keys.length - valid.length });
}
