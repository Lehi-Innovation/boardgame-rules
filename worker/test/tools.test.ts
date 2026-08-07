import { describe, it, expect } from "vitest";
import { callTool, reportIssueUrl } from "../src/tools";
import { InMemoryCorpus, FakeKV } from "./helpers";

const corpus = new InMemoryCorpus();

describe("list_games", () => {
  it("reports catalog size on empty query", async () => {
    const r = await callTool("list_games", {}, { corpus });
    expect(r.text).toContain("4 game(s):");
  });

  it("filters by name and includes verification status", async () => {
    const r = await callTool("list_games", { query: "ticket" }, { corpus });
    expect(r.text).toContain("2 game(s):");
    expect(r.text).toContain("slug: ticket-to-ride");
    expect(r.text).toContain("verification: unverified");
  });

  it("matches on title when the slug differs", async () => {
    const r = await callTool("list_games", { query: "second edition" }, { corpus });
    expect(r.text).toContain("game-of-thrones-the-card-game");
  });
});

describe("get_rules", () => {
  it("returns the summary markdown", async () => {
    const r = await callTool("get_rules", { game: "Catan" }, { corpus });
    expect(r.isError).toBeFalsy();
    expect(r.text).toContain("# Catan");
    expect(r.text).toContain("Trade wood for sheep");
  });

  it("lists candidates for ambiguous names", async () => {
    const r = await callTool("get_rules", { game: "ticket" }, { corpus });
    expect(r.text).toContain("Ambiguous");
    expect(r.text).toContain("ticket-to-ride-europe");
  });

  it("explains when the game has no summary yet", async () => {
    const r = await callTool("get_rules", { game: "ticket to ride" }, { corpus });
    expect(r.text).toContain("no rules summary yet");
  });

  it("logs a miss to KV for unknown games", async () => {
    const kv = new FakeKV();
    const r = await callTool("get_rules", { game: "Uncatalogued Game" }, { corpus, rulings: kv });
    expect(r.text).toContain("No game matching");
    expect(kv.keysWithPrefix("miss:").length).toBe(1);
    const value = JSON.parse(kv.store.get(kv.keysWithPrefix("miss:")[0])!);
    expect(value.query).toBe("Uncatalogued Game");
  });

  it("flags missing required args as errors", async () => {
    const r = await callTool("get_rules", {}, { corpus });
    expect(r.isError).toBe(true);
    expect(r.text).toContain('"game"');
  });
});

describe("search_rulebook", () => {
  it("returns matching passages", async () => {
    const r = await callTool(
      "search_rulebook",
      { game: "catan", query: "longest road" },
      { corpus },
    );
    expect(r.text).toContain("[line 8]");
    expect(r.text).toContain("five or more continuous road segments");
  });

  it("explains when no extracted text exists", async () => {
    const r = await callTool(
      "search_rulebook",
      { game: "ticket to ride", query: "stations" },
      { corpus },
    );
    expect(r.text).toContain("No extracted rulebook text");
  });
});

describe("read_rulebook", () => {
  it("reads a numbered window", async () => {
    const r = await callTool(
      "read_rulebook",
      { game: "catan", start_line: 9, line_count: 1 },
      { corpus },
    );
    expect(r.text).toContain("9| Victory:");
  });

  it("rejects a bad start_line", async () => {
    const r = await callTool("read_rulebook", { game: "catan", start_line: -2 }, { corpus });
    expect(r.isError).toBe(true);
  });
});

describe("log_ruling", () => {
  const goodArgs = {
    game: "catan",
    question: "Can you trade on another player's turn?",
    answer: "Only with the active player.",
    source: "rulebook text line 5",
  };

  it("queues a ruling with resolved slug", async () => {
    const kv = new FakeKV();
    const r = await callTool("log_ruling", goodArgs, { corpus, rulings: kv });
    expect(r.text).toContain("Ruling logged");
    const keys = kv.keysWithPrefix("q:");
    expect(keys.length).toBe(1);
    const value = JSON.parse(kv.store.get(keys[0])!);
    expect(value.type).toBe("ruling");
    expect(value.slug).toBe("catan");
    expect(value.question).toContain("another player's turn");
    expect(value.ts).toBeTruthy();
  });

  it("logs unknown games as coverage gaps", async () => {
    const kv = new FakeKV();
    const r = await callTool(
      "log_ruling",
      { ...goodArgs, game: "Some Obscure Game" },
      { corpus, rulings: kv },
    );
    expect(r.text).toContain("coverage gap");
    const value = JSON.parse(kv.store.get(kv.keysWithPrefix("q:")[0])!);
    expect(value.slug).toBeNull();
    expect(value.game_query).toBe("Some Obscure Game");
  });

  it("degrades gracefully without the KV binding", async () => {
    const r = await callTool("log_ruling", goodArgs, { corpus });
    expect(r.isError).toBeFalsy();
    expect(r.text).toContain("not configured");
    expect(r.text).toContain("github.com");
  });

  it("rejects oversized submissions", async () => {
    const r = await callTool(
      "log_ruling",
      { ...goodArgs, answer: "x".repeat(5000) },
      { corpus, rulings: new FakeKV() },
    );
    expect(r.isError).toBe(true);
    expect(r.text).toContain("too long");
  });
});

describe("report_rule_error", () => {
  const args = {
    game: "catan",
    summary_claim: "Maritime trade is 3:1 by default.",
    correction: "Base maritime trade is 4:1 without a harbor.",
  };

  it("queues the report and returns the prefilled GitHub link", async () => {
    const kv = new FakeKV();
    const r = await callTool("report_rule_error", args, { corpus, rulings: kv });
    expect(r.text).toContain("Report recorded");
    expect(r.text).toContain(
      "https://github.com/Lehi-Innovation/boardgame-rules/issues/new?template=rule-error.yml",
    );
    expect(r.text).toContain("game=catan");
    const value = JSON.parse(kv.store.get(kv.keysWithPrefix("q:")[0])!);
    expect(value.type).toBe("error_report");
    expect(value.slug).toBe("catan");
  });

  it("still returns the GitHub link without KV", async () => {
    const r = await callTool("report_rule_error", args, { corpus });
    expect(r.text).not.toContain("Report recorded");
    expect(r.text).toContain("issues/new?template=rule-error.yml");
  });
});

describe("reportIssueUrl", () => {
  it("mirrors scripts/site.py encoding", () => {
    const url = reportIssueUrl("Catan", "catan");
    expect(url).toBe(
      "https://github.com/Lehi-Innovation/boardgame-rules/issues/new" +
        "?template=rule-error.yml&labels=rule-error" +
        "&title=%5BRule%20error%5D%20Catan&game=catan",
    );
  });
});
