/** Stateless MCP Streamable HTTP endpoint.
 *
 * Implements the subset of the Model Context Protocol a read-mostly tools
 * server needs, with plain JSON responses (the spec allows a server to answer
 * a POST with a single application/json body instead of an SSE stream).
 * Stateless: no session IDs are issued and every request carries what it
 * needs, so any isolate can serve any request.
 */

import type { Env } from "./env";
import { AssetsCorpus } from "./corpus";
import { TOOL_DEFS, callTool, type ToolContext } from "./tools";
import {
  SERVER_NAME,
  SERVER_TITLE,
  SERVER_VERSION,
  SERVER_INSTRUCTIONS,
  SUPPORTED_PROTOCOL_VERSIONS,
} from "./config";
import { corsHeaders } from "./http";

const MAX_BODY_BYTES = 128 * 1024;

interface JsonRpcMessage {
  jsonrpc?: string;
  id?: string | number | null;
  method?: string;
  params?: Record<string, unknown>;
  result?: unknown;
  error?: unknown;
}

type JsonRpcResponse = {
  jsonrpc: "2.0";
  id: string | number | null;
  result?: unknown;
  error?: { code: number; message: string };
};

function rpcResult(id: string | number | null, result: unknown): JsonRpcResponse {
  return { jsonrpc: "2.0", id, result };
}

function rpcError(id: string | number | null, code: number, message: string): JsonRpcResponse {
  return { jsonrpc: "2.0", id, error: { code, message } };
}

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", ...corsHeaders() },
  });
}

/** 202 for notification-only posts (no body per Streamable HTTP spec). */
function acceptedResponse(): Response {
  return new Response(null, { status: 202, headers: corsHeaders() });
}

export async function handleMcpPost(request: Request, env: Env): Promise<Response> {
  let bodyText: string;
  try {
    bodyText = await request.text();
  } catch {
    return jsonResponse(rpcError(null, -32700, "Could not read request body"), 400);
  }
  if (bodyText.length > MAX_BODY_BYTES) {
    return jsonResponse(rpcError(null, -32600, "Request body too large"), 413);
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(bodyText);
  } catch {
    return jsonResponse(rpcError(null, -32700, "Parse error: body is not valid JSON"), 400);
  }

  const ctx: ToolContext = { corpus: new AssetsCorpus(env.ASSETS), rulings: env.RULINGS };

  // JSON-RPC batches existed in protocol 2025-03-26 and were removed in
  // 2025-06-18; accepting arrays regardless keeps both client generations happy.
  if (Array.isArray(parsed)) {
    if (parsed.length === 0) {
      return jsonResponse(rpcError(null, -32600, "Invalid request: empty batch"), 400);
    }
    const settled = await Promise.all(parsed.map((m) => handleMessage(m, ctx)));
    const responses = settled.filter((r): r is JsonRpcResponse => r !== null);
    return responses.length > 0 ? jsonResponse(responses) : acceptedResponse();
  }

  const response = await handleMessage(parsed, ctx);
  return response ? jsonResponse(response) : acceptedResponse();
}

/** Handle one JSON-RPC message. Returns null for notifications/responses,
 * which get no reply body. */
async function handleMessage(raw: unknown, ctx: ToolContext): Promise<JsonRpcResponse | null> {
  if (typeof raw !== "object" || raw === null) {
    return rpcError(null, -32600, "Invalid request: not a JSON-RPC message");
  }
  const msg = raw as JsonRpcMessage;
  const hasId = "id" in msg && msg.id !== undefined;

  // Client → server responses (to requests we never send) and notifications
  // must not receive a response.
  if (!("method" in msg) || typeof msg.method !== "string") {
    if (hasId && ("result" in msg || "error" in msg)) return null;
    return hasId
      ? rpcError(msg.id ?? null, -32600, "Invalid request: missing method")
      : null;
  }
  if (!hasId) {
    // Notification (initialized, cancelled, progress, ...): acknowledge silently.
    return null;
  }

  const id = msg.id ?? null;
  const params = (msg.params ?? {}) as Record<string, unknown>;

  try {
    switch (msg.method) {
      case "initialize":
        return rpcResult(id, initializeResult(params));
      case "ping":
        return rpcResult(id, {});
      case "tools/list":
        return rpcResult(id, { tools: TOOL_DEFS });
      case "tools/call":
        return toolsCall(id, params, ctx);
      default:
        return rpcError(id, -32601, `Method not found: ${msg.method}`);
    }
  } catch (err) {
    const detail = err instanceof Error ? err.message : String(err);
    return rpcError(id, -32603, `Internal error: ${detail}`);
  }
}

function initializeResult(params: Record<string, unknown>): unknown {
  const requested = typeof params.protocolVersion === "string" ? params.protocolVersion : "";
  const protocolVersion = SUPPORTED_PROTOCOL_VERSIONS.includes(requested)
    ? requested
    : SUPPORTED_PROTOCOL_VERSIONS[0];
  return {
    protocolVersion,
    capabilities: { tools: { listChanged: false } },
    serverInfo: { name: SERVER_NAME, title: SERVER_TITLE, version: SERVER_VERSION },
    instructions: SERVER_INSTRUCTIONS,
  };
}

async function toolsCall(
  id: string | number | null,
  params: Record<string, unknown>,
  ctx: ToolContext,
): Promise<JsonRpcResponse> {
  const name = typeof params.name === "string" ? params.name : "";
  if (!TOOL_DEFS.some((t) => t.name === name)) {
    return rpcError(id, -32602, `Unknown tool: ${name || "(missing name)"}`);
  }
  const args =
    typeof params.arguments === "object" && params.arguments !== null
      ? (params.arguments as Record<string, unknown>)
      : {};
  try {
    const result = await callTool(name, args, ctx);
    return rpcResult(id, {
      content: [{ type: "text", text: result.text }],
      isError: result.isError === true,
    });
  } catch (err) {
    // Tool execution failures are reported inside the result so the model
    // can see them and adjust (per MCP guidance), not as protocol errors.
    const detail = err instanceof Error ? err.message : String(err);
    return rpcResult(id, {
      content: [{ type: "text", text: `Tool ${name} failed: ${detail}` }],
      isError: true,
    });
  }
}
