import { describe, it, expect, beforeEach } from "vitest";
import worker from "../src/index";
import { clearManifestCache } from "../src/corpus";
import { fakeEnv, postMcp, rpc } from "./helpers";

beforeEach(() => clearManifestCache());

describe("initialize", () => {
  it("echoes a supported protocol version", async () => {
    const res = await postMcp(worker, fakeEnv(), rpc("initialize", {
      protocolVersion: "2025-03-26",
      capabilities: {},
      clientInfo: { name: "test", version: "0" },
    }));
    expect(res.status).toBe(200);
    const body = await res.json();
    expect(body.result.protocolVersion).toBe("2025-03-26");
    expect(body.result.serverInfo.name).toBe("boardgame-rules");
    expect(body.result.capabilities.tools).toBeDefined();
    expect(body.result.instructions).toContain("list_games");
  });

  it("falls back to the newest supported version for unknown requests", async () => {
    const res = await postMcp(worker, fakeEnv(), rpc("initialize", { protocolVersion: "1999-01-01" }));
    const body = await res.json();
    expect(body.result.protocolVersion).toBe("2025-06-18");
  });
});

describe("lifecycle & errors", () => {
  it("accepts the initialized notification with a 202", async () => {
    const res = await postMcp(worker, fakeEnv(), {
      jsonrpc: "2.0",
      method: "notifications/initialized",
    });
    expect(res.status).toBe(202);
    expect(await res.text()).toBe("");
  });

  it("answers ping", async () => {
    const res = await postMcp(worker, fakeEnv(), rpc("ping"));
    const body = await res.json();
    expect(body.result).toEqual({});
  });

  it("rejects unknown methods with -32601", async () => {
    const res = await postMcp(worker, fakeEnv(), rpc("resources/list"));
    const body = await res.json();
    expect(body.error.code).toBe(-32601);
  });

  it("rejects invalid JSON with -32700", async () => {
    const res = await worker.fetch(
      new Request("https://worker.test/mcp", { method: "POST", body: "{nope" }),
      fakeEnv(),
    );
    expect(res.status).toBe(400);
    const body = await res.json();
    expect(body.error.code).toBe(-32700);
    expect(body.id).toBeNull();
  });

  it("handles batch requests", async () => {
    const res = await postMcp(worker, fakeEnv(), [rpc("ping", undefined, 1), rpc("ping", undefined, 2)]);
    const body = await res.json();
    expect(Array.isArray(body)).toBe(true);
    expect(body.length).toBe(2);
  });

  it("rejects non-POST on /mcp", async () => {
    const res = await worker.fetch(new Request("https://worker.test/mcp"), fakeEnv());
    expect(res.status).toBe(405);
    expect(res.headers.get("allow")).toContain("POST");
  });

  it("answers CORS preflight", async () => {
    const res = await worker.fetch(
      new Request("https://worker.test/mcp", { method: "OPTIONS" }),
      fakeEnv(),
    );
    expect(res.status).toBe(204);
    expect(res.headers.get("access-control-allow-origin")).toBe("*");
  });
});

describe("tools over HTTP", () => {
  it("lists all six tools with schemas", async () => {
    const res = await postMcp(worker, fakeEnv(), rpc("tools/list"));
    const body = await res.json();
    const names = body.result.tools.map((t: { name: string }) => t.name);
    expect(names).toEqual([
      "list_games",
      "get_rules",
      "search_rulebook",
      "read_rulebook",
      "log_ruling",
      "report_rule_error",
    ]);
    for (const tool of body.result.tools) {
      expect(tool.inputSchema.type).toBe("object");
      expect(tool.description.length).toBeGreaterThan(40);
    }
  });

  it("serves get_rules end to end from assets", async () => {
    const res = await postMcp(worker, fakeEnv(), rpc("tools/call", {
      name: "get_rules",
      arguments: { game: "catan" },
    }));
    const body = await res.json();
    expect(body.result.isError).toBe(false);
    expect(body.result.content[0].text).toContain("# Catan");
  });

  it("serves search_rulebook end to end from assets", async () => {
    const res = await postMcp(worker, fakeEnv(), rpc("tools/call", {
      name: "search_rulebook",
      arguments: { game: "catan", query: "victory points" },
    }));
    const body = await res.json();
    expect(body.result.content[0].text).toContain("10 victory points");
  });

  it("rejects unknown tools with -32602", async () => {
    const res = await postMcp(worker, fakeEnv(), rpc("tools/call", { name: "nope", arguments: {} }));
    const body = await res.json();
    expect(body.error.code).toBe(-32602);
  });
});

describe("service endpoints", () => {
  it("healthz reports the staged corpus", async () => {
    const res = await worker.fetch(new Request("https://worker.test/healthz"), fakeEnv());
    const body = await res.json();
    expect(body.ok).toBe(true);
    expect(body.games).toBe(4);
    expect(body.feedback_queue).toBe(false);
  });

  it("home page shows the connector URL", async () => {
    const res = await worker.fetch(new Request("https://worker.test/"), fakeEnv());
    expect(res.status).toBe(200);
    const html = await res.text();
    expect(html).toContain("https://worker.test/mcp");
    expect(html).toContain("Add custom");
  });

  it("404s unknown paths", async () => {
    const res = await worker.fetch(new Request("https://worker.test/nope"), fakeEnv());
    expect(res.status).toBe(404);
  });
});
