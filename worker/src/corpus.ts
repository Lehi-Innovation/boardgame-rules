import type { AssetsLike } from "./env";

export interface GameEntry {
  title: string;
  slug: string;
  bgg_id?: number;
  player_count?: string;
  play_time?: string;
  verification?: string;
  summary_url?: string;
  rulebook_text_url?: string;
}

export interface CorpusStore {
  manifest(): Promise<GameEntry[]>;
  rulesMarkdown(slug: string): Promise<string | null>;
  extractedText(slug: string): Promise<string | null>;
}

export function slugify(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function escapeRegex(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

export interface Resolution {
  slug: string | null;
  candidates: GameEntry[];
}

/** Resolve a user-supplied game name to a catalog slug.
 *
 * Port of mcp_server/server.py::_resolve_slug, extended to also match the
 * slugified title (helps with second editions whose slug differs from the
 * display title). Returns slug=null when there is no confident single match.
 */
export function resolveSlug(games: GameEntry[], name: string): Resolution {
  const q = slugify(name);
  if (!q) return { slug: null, candidates: [] };

  const exactSlug = games.find((g) => g.slug === q);
  if (exactSlug) return { slug: q, candidates: [exactSlug] };

  const exactTitle = games.filter((g) => slugify(g.title ?? "") === q);
  if (exactTitle.length === 1) return { slug: exactTitle[0].slug, candidates: exactTitle };
  if (exactTitle.length > 1) return { slug: null, candidates: exactTitle.slice(0, 10) };

  const qFlat = q.replace(/-/g, "");
  const partial = games.filter((g) => {
    const s = g.slug;
    const t = slugify(g.title ?? "");
    return (
      s.includes(q) ||
      s.replace(/-/g, "").includes(qFlat) ||
      (t.length > 0 && t.includes(q))
    );
  });
  if (partial.length === 1) return { slug: partial[0].slug, candidates: partial };
  return { slug: null, candidates: partial.slice(0, 10) };
}

export interface SearchOutcome {
  found: boolean;
  text: string;
}

/** Keyword search over rulebook text with context blocks.
 *
 * Port of mcp_server/server.py::search_rulebook's matching logic: exact
 * phrase first, then an all-words fallback (words longer than 2 chars) since
 * OCR text often breaks phrases across lines. Returns up to 8 hits as
 * non-overlapping context blocks.
 */
export function searchText(
  raw: string,
  query: string,
  slug: string,
  contextLines = 4,
): SearchOutcome {
  const lines = raw.split(/\r?\n/);
  const phrase = new RegExp(escapeRegex(query), "i");
  const words = query
    .split(/\s+/)
    .filter((w) => w.length > 2)
    .map((w) => new RegExp(escapeRegex(w), "i"));

  const matches = (line: string): boolean =>
    phrase.test(line) || (words.length > 0 && words.every((p) => p.test(line)));

  const hits: number[] = [];
  for (let i = 0; i < lines.length; i++) {
    if (matches(lines[i])) hits.push(i);
  }

  if (hits.length === 0) {
    return {
      found: false,
      text:
        `No match for "${query}" in ${slug}'s rulebook text (${lines.length} lines). ` +
        `Try a different term — OCR text may use other wording.`,
    };
  }

  const blocks: string[] = [];
  let lastEnd = -1;
  for (const i of hits.slice(0, 8)) {
    const start = Math.max(i - contextLines, lastEnd + 1, 0);
    const end = Math.min(i + contextLines + 1, lines.length);
    if (start < end) {
      blocks.push(`[line ${i + 1}]\n` + lines.slice(start, end).join("\n"));
      lastEnd = end - 1;
    }
  }
  const suffix =
    hits.length > 8 ? `\n\n(${hits.length} total matches; showing first 8)` : "";
  return { found: true, text: blocks.join("\n\n---\n\n") + suffix };
}

/** Read a 1-indexed window of rulebook lines, numbered for follow-up reads. */
export function readWindow(
  raw: string,
  slug: string,
  startLine: number,
  lineCount: number,
): string {
  const lines = raw.split(/\r?\n/);
  const total = lines.length;
  const start = Math.max(1, Math.floor(startLine));
  const count = Math.min(Math.max(1, Math.floor(lineCount)), 200);
  if (start > total) {
    return `start_line ${start} is beyond the end of ${slug}'s rulebook text (${total} lines).`;
  }
  const end = Math.min(start + count - 1, total);
  const body = lines
    .slice(start - 1, end)
    .map((line, i) => `${start + i}| ${line}`)
    .join("\n");
  return `Lines ${start}-${end} of ${total} (${slug} rulebook text):\n${body}`;
}

const MANIFEST_TTL_MS = 5 * 60 * 1000;
let manifestCache: { games: GameEntry[]; expires: number } | null = null;

/** For tests. */
export function clearManifestCache(): void {
  manifestCache = null;
}

/** Corpus backed by the Workers static assets binding (worker/public/). */
export class AssetsCorpus implements CorpusStore {
  constructor(private assets: AssetsLike) {}

  private async fetchAsset(path: string): Promise<Response> {
    // Host is ignored by the assets binding; only the path matters.
    return this.assets.fetch(new Request(`https://assets.local${path}`));
  }

  async manifest(): Promise<GameEntry[]> {
    const now = Date.now();
    if (manifestCache && manifestCache.expires > now) return manifestCache.games;
    const res = await this.fetchAsset("/games.json");
    if (!res.ok) throw new Error(`games.json not staged (HTTP ${res.status})`);
    const data = (await res.json()) as { games: GameEntry[] };
    manifestCache = { games: data.games, expires: now + MANIFEST_TTL_MS };
    return data.games;
  }

  async rulesMarkdown(slug: string): Promise<string | null> {
    const res = await this.fetchAsset(`/rules/${slug}.md`);
    return res.ok ? res.text() : null;
  }

  async extractedText(slug: string): Promise<string | null> {
    for (const name of [`${slug}-rules.txt`, `${slug}_rules.txt`, `${slug}.txt`]) {
      const res = await this.fetchAsset(`/extracted/${name}`);
      if (res.ok) return res.text();
    }
    return null;
  }
}
