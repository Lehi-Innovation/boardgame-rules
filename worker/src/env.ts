/** Minimal structural types for the bindings we use, so tests can fake them
 * without depending on @cloudflare/workers-types. */

export interface KVListResult {
  keys: { name: string }[];
  list_complete: boolean;
  cursor?: string;
}

export interface KVLike {
  put(key: string, value: string, opts?: { expirationTtl?: number }): Promise<void>;
  get(key: string): Promise<string | null>;
  list(opts?: { prefix?: string; limit?: number; cursor?: string }): Promise<KVListResult>;
  delete(key: string): Promise<void>;
}

export interface AssetsLike {
  fetch(input: Request | string): Promise<Response>;
}

export interface Env {
  /** Static assets binding — the staged corpus (games.json, rules/, extracted/). */
  ASSETS: AssetsLike;
  /** Optional KV namespace for the feedback queue. Absent = feedback degrades to GitHub links. */
  RULINGS?: KVLike;
  /** Optional bearer token protecting /admin endpoints. Absent = admin API disabled. */
  ADMIN_TOKEN?: string;
}
