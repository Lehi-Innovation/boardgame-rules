export const SERVER_NAME = "boardgame-rules";
export const SERVER_TITLE = "Board Game Rules Database";
export const SERVER_VERSION = "1.0.0";

export const SITE_BASE = "https://lehi-innovation.github.io/boardgame-rules";
export const REPO_URL = "https://github.com/Lehi-Innovation/boardgame-rules";

/** Protocol versions this server accepts, newest first. */
export const SUPPORTED_PROTOCOL_VERSIONS = [
  "2025-06-18",
  "2025-03-26",
  "2024-11-05",
];

export const SERVER_INSTRUCTIONS = `Board game rules lookup for mid-game questions.

Typical flow: (1) resolve the game with list_games — names are fuzzy, confirm
the right game/edition; (2) call get_rules and answer from the summary, noting
its verification banner; (3) if the summary doesn't clearly settle the
question, or the stakes are high (scoring, victory conditions, game end), use
search_rulebook — the full rulebook text outranks the summary — and
read_rulebook to see more context around a hit; (4) tell the user which source
you used; if neither source settles it, say so plainly rather than guessing.

Afterwards: if your answer needed anything beyond the summary (rulebook text,
an official FAQ, or the table's own ruling), call log_ruling so maintainers
can verify it and add it to the game's FAQ. If the summary itself was wrong,
call report_rule_error.`;
