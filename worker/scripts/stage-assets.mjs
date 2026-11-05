#!/usr/bin/env node
/** Stage the corpus into worker/public/ for Workers static assets.
 *
 * Copies from the repo root:
 *   games.json           -> public/games.json
 *   rules/*.md           -> public/rules/
 *   extracted/*.txt      -> public/extracted/
 *
 * public/ is gitignored and rebuilt from scratch on every run, so a deploy
 * always ships exactly what the repo currently contains.
 */

import { cp, mkdir, rm, readdir, writeFile, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const workerDir = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const repoRoot = path.dirname(workerDir);
const publicDir = path.join(workerDir, "public");

async function copyByExtension(srcDir, destDir, extension) {
  await mkdir(destDir, { recursive: true });
  const entries = await readdir(srcDir);
  let count = 0;
  for (const entry of entries) {
    if (!entry.endsWith(extension)) continue;
    await cp(path.join(srcDir, entry), path.join(destDir, entry));
    count += 1;
  }
  return count;
}

const manifestPath = path.join(repoRoot, "games.json");
await stat(manifestPath).catch(() => {
  console.error(`Missing ${manifestPath} — run \`python -m scripts.generate_manifest\` first.`);
  process.exit(1);
});

await rm(publicDir, { recursive: true, force: true });
await mkdir(publicDir, { recursive: true });

await cp(manifestPath, path.join(publicDir, "games.json"));
const rulesCount = await copyByExtension(
  path.join(repoRoot, "rules"),
  path.join(publicDir, "rules"),
  ".md",
);
const extractedCount = await copyByExtension(
  path.join(repoRoot, "extracted"),
  path.join(publicDir, "extracted"),
  ".txt",
);

const buildInfo = {
  staged_at: new Date().toISOString(),
  rules_files: rulesCount,
  extracted_files: extractedCount,
};
await writeFile(path.join(publicDir, "build-info.json"), JSON.stringify(buildInfo, null, 2));

console.log(
  `Staged corpus into ${publicDir}: games.json, ${rulesCount} rules files, ${extractedCount} extracted texts.`,
);
