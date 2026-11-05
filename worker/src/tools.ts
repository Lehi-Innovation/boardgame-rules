import type { CorpusStore, GameEntry } from "./corpus";
import { resolveSlug, searchText, readWindow, slugify } from "./corpus";
import type { KVLike } from "./env";
import { REPO_URL } from "./config";

export interface ToolContext {
  corpus: CorpusStore;
  rulings?: KVLike;
}

export interface ToolResult {
  text: string;
  isError?: boolean;
}

interface JsonSchema {
  type: "object";
  properties: Record<string, unknown>;
  required?: string[];
}

export interface ToolDef {
  name: string;
  title: string;
  description: string;
  inputSchema: JsonSchema;
}

const gameParam = {
  type: "string",
  description: "Game name or catalog slug (fuzzy — resolved against the catalog).",
};

export const TOOL_DEFS: ToolDef[] = [
  {
    name: "list_games",
    title: "Search the game catalog",
    description:
      "Search the catalog of board games by name. Returns matching games with " +
      "slug, player count, play time, and verification status. Call with a " +
      "partial name to resolve the game the user means; call with an empty " +
      "query for the catalog size.",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Partial game name. Empty = catalog stats." },
      },
    },
  },
  {
    name: "get_rules",
    title: "Get a game's rules summary",
    description:
      "Get the complete rules summary for a game (markdown). Start here for any " +
      "rules question. The summary begins with a verification banner — if it says " +
      "Unverified or Known errors, double-check important answers with " +
      "search_rulebook. For high-stakes questions (scoring, victory conditions, " +
      "game end) verify against search_rulebook even when the summary answers.",
    inputSchema: {
      type: "object",
      properties: { game: gameParam },
      required: ["game"],
    },
  },
  {
    name: "search_rulebook",
    title: "Search the full rulebook text",
    description:
      "Keyword-search the game's full extracted rulebook text — the authoritative " +
      "source, which outranks the summary. Use when the summary doesn't answer the " +
      "question, for high-stakes rulings, or to verify a summary marked Unverified. " +
      "Returns matching passages with surrounding lines and their line numbers. " +
      "OCR text is imperfect: if a phrase misses, retry with one distinctive word.",
    inputSchema: {
      type: "object",
      properties: {
        game: gameParam,
        query: { type: "string", description: "Keyword or phrase to search for." },
        context_lines: {
          type: "number",
          description: "Lines of context around each match (default 4, max 20).",
        },
      },
      required: ["game", "query"],
    },
  },
  {
    name: "read_rulebook",
    title: "Read rulebook text by line number",
    description:
      "Read a window of the extracted rulebook text by 1-indexed line number. " +
      "Use after search_rulebook when a match needs more surrounding context — " +
      "e.g. to read a full table, list, or section that extends past the search " +
      "context.",
    inputSchema: {
      type: "object",
      properties: {
        game: gameParam,
        start_line: { type: "number", description: "1-indexed first line to read." },
        line_count: { type: "number", description: "Lines to read (default 60, max 200)." },
      },
      required: ["game", "start_line"],
    },
  },
  {
    name: "log_ruling",
    title: "Log a Q&A for the rules database",
    description:
      "Log a rules question and its answer to the database's improvement queue. " +
      "Call this AFTER answering a question the rules summary did not fully " +
      "cover — where you needed the rulebook text, an official FAQ, or the table " +
      "made its own ruling. Send only the distilled question and answer (no " +
      "personal information or conversation content). Maintainers verify " +
      "submissions against the rulebook text before adding them to the game's " +
      "FAQ, so state the source of your answer.",
    inputSchema: {
      type: "object",
      properties: {
        game: gameParam,
        question: { type: "string", description: "The rules question, distilled (max 2000 chars)." },
        answer: { type: "string", description: "The answer given (max 4000 chars)." },
        source: {
          type: "string",
          description:
            'Where the answer came from, e.g. "rulebook text line 340", ' +
            '"publisher FAQ <url>", "table ruling — summary was silent".',
        },
      },
      required: ["game", "question", "answer"],
    },
  },
  {
    name: "report_rule_error",
    title: "Report a wrong rule in the summary",
    description:
      "Report that the rules summary contradicts the actual rulebook or an " +
      "official ruling. Call when the user says the summary was wrong at the " +
      "table. The report is queued for maintainers, verified against the " +
      "rulebook text, and fixed via pull request. Also returns a GitHub link " +
      "the user can open to file or track the report themselves.",
    inputSchema: {
      type: "object",
      properties: {
        game: gameParam,
        summary_claim: { type: "string", description: "What the summary says (the wrong claim)." },
        correction: { type: "string", description: "What the rule actually is, with source if known." },
      },
      required: ["game", "summary_claim", "correction"],
    },
  },
];

/** Prefilled GitHub issue-form URL — mirror of scripts/site.py::report_issue_url. */
export function reportIssueUrl(title: string, slug: string): string {
  return (
    `${REPO_URL}/issues/new` +
    `?template=rule-error.yml` +
    `&labels=rule-error` +
    `&title=${encodeURIComponent(`[Rule error] ${title}`)}` +
    `&game=${encodeURIComponent(slug)}`
  );
}

function candidateList(candidates: GameEntry[]): string {
  return candidates.map((g) => g.slug).join(", ");
}

function newQueueKey(prefix: string): string {
  return `${prefix}:${new Date().toISOString()}:${crypto.randomUUID().slice(0, 8)}`;
}

async function queuePut(
  kv: KVLike,
  prefix: string,
  payload: Record<string, unknown>,
  expirationTtl?: number,
): Promise<void> {
  await kv.put(
    newQueueKey(prefix),
    JSON.stringify({ ...payload, ts: new Date().toISOString() }),
    expirationTtl ? { expirationTtl } : undefined,
  );
}

/** Log a catalog miss (game asked for but absent) — a "please add this game" signal. */
async function logMiss(ctx: ToolContext, tool: string, query: string): Promise<void> {
  if (!ctx.rulings || !query) return;
  try {
    // Auto-expire in 60 days; these are aggregate signals, not records.
    await queuePut(ctx.rulings, "miss", { tool, query }, 60 * 24 * 60 * 60);
  } catch {
    // Analytics must never break a lookup.
  }
}

type Resolved = { ok: true; slug: string; entry: GameEntry | null } | { ok: false; text: string };

async function resolveOrExplain(ctx: ToolContext, tool: string, game: string): Promise<Resolved> {
  const games = await ctx.corpus.manifest();
  const { slug, candidates } = resolveSlug(games, game);
  if (slug) {
    return { ok: true, slug, entry: candidates[0] ?? null };
  }
  if (candidates.length > 0) {
    return {
      ok: false,
      text: `Ambiguous game name "${game}". Candidates: ${candidateList(candidates)}. Retry with one of these slugs.`,
    };
  }
  await logMiss(ctx, tool, game);
  return {
    ok: false,
    text: `No game matching "${game}" in the catalog. Use list_games to search by a shorter or alternate name.`,
  };
}

function requireString(
  args: Record<string, unknown>,
  name: string,
  maxLen: number,
): { ok: true; value: string } | { ok: false; error: string } {
  const v = args[name];
  if (typeof v !== "string" || v.trim().length === 0) {
    return { ok: false, error: `Missing required argument "${name}" (non-empty string).` };
  }
  if (v.length > maxLen) {
    return { ok: false, error: `Argument "${name}" is too long (${v.length} chars; max ${maxLen}).` };
  }
  return { ok: true, value: v.trim() };
}

export async function callTool(
  name: string,
  args: Record<string, unknown>,
  ctx: ToolContext,
): Promise<ToolResult> {
  switch (name) {
    case "list_games":
      return listGames(args, ctx);
    case "get_rules":
      return getRules(args, ctx);
    case "search_rulebook":
      return searchRulebook(args, ctx);
    case "read_rulebook":
      return readRulebook(args, ctx);
    case "log_ruling":
      return logRuling(args, ctx);
    case "report_rule_error":
      return reportRuleError(args, ctx);
    default:
      return { text: `Unknown tool: ${name}`, isError: true };
  }
}

async function listGames(args: Record<string, unknown>, ctx: ToolContext): Promise<ToolResult> {
  const query = typeof args.query === "string" ? args.query : "";
  let games = await ctx.corpus.manifest();
  if (query) {
    const q = slugify(query);
    games = games.filter(
      (g) => g.slug.includes(q) || slugify(g.title ?? "").includes(q),
    );
  }
  if (games.length === 0) {
    await logMiss(ctx, "list_games", query);
    return { text: `No games matching "${query}". Try a shorter or alternate name.` };
  }
  const lines = [`${games.length} game(s):`];
  for (const g of games.slice(0, 50)) {
    lines.push(
      `- ${g.title ?? g.slug} (slug: ${g.slug}, players: ${g.player_count ?? "?"}, ` +
        `verification: ${g.verification ?? "unknown"})`,
    );
  }
  if (games.length > 50) {
    lines.push(`... and ${games.length - 50} more; refine the query.`);
  }
  return { text: lines.join("\n") };
}

async function getRules(args: Record<string, unknown>, ctx: ToolContext): Promise<ToolResult> {
  const game = requireString(args, "game", 200);
  if (!game.ok) return { text: game.error, isError: true };
  const res = await resolveOrExplain(ctx, "get_rules", game.value);
  if (!res.ok) return { text: res.text };
  const md = await ctx.corpus.rulesMarkdown(res.slug);
  if (md === null) {
    return {
      text:
        `Game ${res.slug} is in the catalog but has no rules summary yet. ` +
        `Try search_rulebook — the extracted rulebook text may still exist.`,
    };
  }
  return { text: md };
}

async function searchRulebook(args: Record<string, unknown>, ctx: ToolContext): Promise<ToolResult> {
  const game = requireString(args, "game", 200);
  if (!game.ok) return { text: game.error, isError: true };
  const query = requireString(args, "query", 500);
  if (!query.ok) return { text: query.error, isError: true };
  const ctxLines = Math.min(Math.max(Number(args.context_lines ?? 4) || 4, 0), 20);

  const res = await resolveOrExplain(ctx, "search_rulebook", game.value);
  if (!res.ok) return { text: res.text };
  const raw = await ctx.corpus.extractedText(res.slug);
  if (raw === null) {
    return {
      text:
        `No extracted rulebook text exists for ${res.slug}; the summary is the ` +
        `only source available and cannot be double-checked.`,
    };
  }
  return { text: searchText(raw, query.value, res.slug, ctxLines).text };
}

async function readRulebook(args: Record<string, unknown>, ctx: ToolContext): Promise<ToolResult> {
  const game = requireString(args, "game", 200);
  if (!game.ok) return { text: game.error, isError: true };
  const startLine = Number(args.start_line);
  if (!Number.isFinite(startLine) || startLine < 1) {
    return { text: `Argument "start_line" must be a positive line number.`, isError: true };
  }
  const lineCount = Number(args.line_count ?? 60) || 60;

  const res = await resolveOrExplain(ctx, "read_rulebook", game.value);
  if (!res.ok) return { text: res.text };
  const raw = await ctx.corpus.extractedText(res.slug);
  if (raw === null) {
    return { text: `No extracted rulebook text exists for ${res.slug}.` };
  }
  return { text: readWindow(raw, res.slug, startLine, lineCount) };
}

async function logRuling(args: Record<string, unknown>, ctx: ToolContext): Promise<ToolResult> {
  const game = requireString(args, "game", 200);
  if (!game.ok) return { text: game.error, isError: true };
  const question = requireString(args, "question", 2000);
  if (!question.ok) return { text: question.error, isError: true };
  const answer = requireString(args, "answer", 4000);
  if (!answer.ok) return { text: answer.error, isError: true };
  const source = typeof args.source === "string" ? args.source.slice(0, 500) : "";

  if (!ctx.rulings) {
    return {
      text:
        `The feedback queue is not configured on this server, so the ruling was ` +
        `not stored. It can still reach maintainers as a GitHub issue: ` +
        `${REPO_URL}/issues/new?labels=rule-error`,
    };
  }

  // A ruling for an uncataloged game is still valuable — it is a coverage gap.
  const games = await ctx.corpus.manifest();
  const { slug } = resolveSlug(games, game.value);

  await queuePut(ctx.rulings, "q", {
    type: "ruling",
    game_query: game.value,
    slug: slug ?? null,
    question: question.value,
    answer: answer.value,
    source,
  });

  const gapNote = slug
    ? ""
    : ` (Note: "${game.value}" is not in the catalog — logged as a coverage gap.)`;
  return {
    text:
      `Ruling logged. Maintainers verify submissions against the rulebook text ` +
      `before adding them to the game's FAQ & Rulings section.${gapNote}`,
  };
}

async function reportRuleError(args: Record<string, unknown>, ctx: ToolContext): Promise<ToolResult> {
  const game = requireString(args, "game", 200);
  if (!game.ok) return { text: game.error, isError: true };
  const claim = requireString(args, "summary_claim", 2000);
  if (!claim.ok) return { text: claim.error, isError: true };
  const correction = requireString(args, "correction", 4000);
  if (!correction.ok) return { text: correction.error, isError: true };

  const res = await resolveOrExplain(ctx, "report_rule_error", game.value);
  if (!res.ok) return { text: res.text };
  const title = res.entry?.title ?? res.slug;
  const url = reportIssueUrl(title, res.slug);

  let queued = false;
  if (ctx.rulings) {
    await queuePut(ctx.rulings, "q", {
      type: "error_report",
      slug: res.slug,
      title,
      summary_claim: claim.value,
      correction: correction.value,
    });
    queued = true;
  }

  const queueLine = queued
    ? `Report recorded — maintainers will verify it against the rulebook text and fix the summary via pull request.\n\n`
    : ``;
  return {
    text:
      queueLine +
      `To file or track the report on GitHub directly, open this prefilled link:\n${url}\n\n` +
      `Include in the form:\n- What the summary says: ${claim.value}\n` +
      `- What the rule actually is: ${correction.value}`,
  };
}
