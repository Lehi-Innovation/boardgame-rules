import { describe, it, expect } from "vitest";
import { slugify, resolveSlug, searchText, readWindow } from "../src/corpus";
import { SAMPLE_GAMES, CATAN_EXTRACTED } from "./helpers";

describe("slugify", () => {
  it("lowercases and dashes non-alphanumerics", () => {
    expect(slugify("Ticket to Ride: Europe")).toBe("ticket-to-ride-europe");
    expect(slugify("  7 Wonders!! ")).toBe("7-wonders");
    expect(slugify("A.D.E.L.E.")).toBe("a-d-e-l-e");
  });
});

describe("resolveSlug", () => {
  it("resolves an exact slug", () => {
    const r = resolveSlug(SAMPLE_GAMES, "catan");
    expect(r.slug).toBe("catan");
  });

  it("resolves an exact title even when it differs from the slug", () => {
    const r = resolveSlug(SAMPLE_GAMES, "A Game of Thrones: The Card Game (Second Edition)");
    expect(r.slug).toBe("game-of-thrones-the-card-game");
  });

  it("resolves a unique partial match", () => {
    const r = resolveSlug(SAMPLE_GAMES, "thrones");
    expect(r.slug).toBe("game-of-thrones-the-card-game");
  });

  it("returns candidates for ambiguous names", () => {
    const r = resolveSlug(SAMPLE_GAMES, "ticket to ride");
    // Exact slug match wins even though "ticket-to-ride-europe" also contains it.
    expect(r.slug).toBe("ticket-to-ride");
    const r2 = resolveSlug(SAMPLE_GAMES, "ticket");
    expect(r2.slug).toBeNull();
    expect(r2.candidates.length).toBe(2);
  });

  it("returns no candidates for unknown games", () => {
    const r = resolveSlug(SAMPLE_GAMES, "definitely not a game");
    expect(r.slug).toBeNull();
    expect(r.candidates).toEqual([]);
  });
});

describe("searchText", () => {
  it("finds an exact phrase with line numbers and context", () => {
    const r = searchText(CATAN_EXTRACTED, "robber moves", "catan", 1);
    expect(r.found).toBe(true);
    expect(r.text).toContain("[line 4]");
    expect(r.text).toContain("On a roll of 7");
    // context line before the hit:
    expect(r.text).toContain("robber starts in the desert");
  });

  it("falls back to all-words matching when the phrase misses", () => {
    // "settlement wood" is not a contiguous phrase but both words share a line.
    const r = searchText(CATAN_EXTRACTED, "settlement wood", "catan", 0);
    expect(r.found).toBe(true);
    expect(r.text).toContain("A settlement costs one wood");
  });

  it("is case-insensitive", () => {
    const r = searchText(CATAN_EXTRACTED, "VICTORY POINTS", "catan", 0);
    expect(r.found).toBe(true);
  });

  it("reports a miss with the line count", () => {
    const r = searchText(CATAN_EXTRACTED, "zzzzz", "catan", 4);
    expect(r.found).toBe(false);
    expect(r.text).toContain("No match");
    expect(r.text).toContain("10 lines");
  });

  it("does not duplicate lines across adjacent hits", () => {
    const text = ["alpha", "target one", "between", "target two", "omega"].join("\n");
    const r = searchText(text, "target", "t", 4);
    expect(r.found).toBe(true);
    // "between" appears in exactly one block despite being context for both hits.
    expect(r.text.match(/between/g)?.length).toBe(1);
  });

  it("caps at 8 hits and reports the total", () => {
    const text = Array.from({ length: 12 }, (_, i) => `hit number ${i}`).join("\n");
    const r = searchText(text, "hit", "t", 0);
    expect(r.text).toContain("(12 total matches; showing first 8)");
  });
});

describe("readWindow", () => {
  it("returns a numbered window", () => {
    const r = readWindow(CATAN_EXTRACTED, "catan", 4, 2);
    expect(r).toContain("Lines 4-5 of 10");
    expect(r).toContain("4| On a roll of 7");
    expect(r).toContain("5| Trading:");
  });

  it("clamps past-EOF requests", () => {
    expect(readWindow(CATAN_EXTRACTED, "catan", 99, 10)).toContain("beyond the end");
    expect(readWindow(CATAN_EXTRACTED, "catan", 9, 100)).toContain("Lines 9-10 of 10");
  });
});
