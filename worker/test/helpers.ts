import type { AssetsLike, Env, KVLike, KVListResult } from "../src/env";
import type { CorpusStore, GameEntry } from "../src/corpus";

export const SAMPLE_GAMES: GameEntry[] = [
  {
    title: "Catan",
    slug: "catan",
    bgg_id: 13,
    player_count: "3-4",
    play_time: "60-120 min",
    verification: "verified",
  },
  {
    title: "Ticket to Ride",
    slug: "ticket-to-ride",
    bgg_id: 9209,
    player_count: "2-5",
    play_time: "30-60 min",
    verification: "verified",
  },
  {
    title: "Ticket to Ride: Europe",
    slug: "ticket-to-ride-europe",
    bgg_id: 14996,
    player_count: "2-5",
    play_time: "30-60 min",
    verification: "unverified",
  },
  {
    title: "A Game of Thrones: The Card Game (Second Edition)",
    slug: "game-of-thrones-the-card-game",
    bgg_id: 169255,
    player_count: "2-6",
    verification: "inaccurate",
  },
];

export const CATAN_RULES_MD = `---
title: "Catan"
---

# Catan

## Overview
Trade wood for sheep.
`;

export const CATAN_EXTRACTED = [
  "CATAN RULEBOOK",
  "Setup: each player places two settlements.",
  "The robber starts in the desert hex.",
  "On a roll of 7, the robber moves.",
  "Trading: players may trade resources freely on their turn.",
  "Maritime trade is available at 4:1 without a harbor.",
  "A settlement costs one wood, one brick, one wool, one grain.",
  "Longest road: five or more continuous road segments.",
  "Victory: first player to reach 10 victory points on their turn wins.",
  "The bank never runs out of resource cards in the base game.",
].join("\n");

export class InMemoryCorpus implements CorpusStore {
  constructor(
    private games: GameEntry[] = SAMPLE_GAMES,
    private rules: Record<string, string> = { catan: CATAN_RULES_MD },
    private extracted: Record<string, string> = { catan: CATAN_EXTRACTED },
  ) {}

  async manifest(): Promise<GameEntry[]> {
    return this.games;
  }
  async rulesMarkdown(slug: string): Promise<string | null> {
    return this.rules[slug] ?? null;
  }
  async extractedText(slug: string): Promise<string | null> {
    return this.extracted[slug] ?? null;
  }
}

export class FakeKV implements KVLike {
  store = new Map<string, string>();

  async put(key: string, value: string): Promise<void> {
    this.store.set(key, value);
  }
  async get(key: string): Promise<string | null> {
    return this.store.get(key) ?? null;
  }
  async list(opts?: { prefix?: string; limit?: number; cursor?: string }): Promise<KVListResult> {
    const prefix = opts?.prefix ?? "";
    const limit = opts?.limit ?? 1000;
    const keys = [...this.store.keys()]
      .filter((k) => k.startsWith(prefix))
      .sort()
      .slice(0, limit)
      .map((name) => ({ name }));
    return { keys, list_complete: true };
  }
  async delete(key: string): Promise<void> {
    this.store.delete(key);
  }

  keysWithPrefix(prefix: string): string[] {
    return [...this.store.keys()].filter((k) => k.startsWith(prefix));
  }
}

export function fakeAssets(files: Record<string, string>): AssetsLike {
  return {
    async fetch(input: Request | string): Promise<Response> {
      const url = typeof input === "string" ? input : input.url;
      const path = new URL(url).pathname;
      const body = files[path];
      if (body === undefined) return new Response("not found", { status: 404 });
      return new Response(body, { status: 200 });
    },
  };
}

/** A fake Env whose assets serve the sample corpus. */
export function fakeEnv(overrides: Partial<Env> = {}): Env {
  return {
    ASSETS: fakeAssets({
      "/games.json": JSON.stringify({ games: SAMPLE_GAMES }),
      "/rules/catan.md": CATAN_RULES_MD,
      "/extracted/catan-rules.txt": CATAN_EXTRACTED,
    }),
    ...overrides,
  };
}

export function rpc(method: string, params?: unknown, id: number | string | null = 1) {
  return { jsonrpc: "2.0", id, method, ...(params !== undefined ? { params } : {}) };
}

export async function postMcp(
  handler: { fetch(req: Request, env: Env): Promise<Response> },
  env: Env,
  body: unknown,
): Promise<Response> {
  return handler.fetch(
    new Request("https://worker.test/mcp", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(body),
    }),
    env,
  );
}
