// Dependency-free structural validation for the strategy files.
// Run: node scripts/validate-strategies.mjs   (used by .github/workflows/validate.yml)
//
// Checks:
//  1. Every strategies/*.md referenced in SKILL.md exists.
//  2. No orphan strategy file (every strategies/*.md is referenced in SKILL.md).
//  3. Each strategy file has a "# " title, "## Restructuring rules", and an
//     "## Anti-patterns" section.
//  4. Each non-universal strategy cites a "> Source:" line with at least one link.

import { readFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const strategiesDir = join(root, 'strategies');

const errors = [];
const fail = (m) => errors.push(m);

// (1) names referenced in SKILL.md
const skill = readFileSync(join(root, 'SKILL.md'), 'utf8');
const referenced = new Set(
  [...skill.matchAll(/strategies\/([a-z0-9-]+)\.md/g)].map((m) => m[1]),
);

// actual files
const actual = readdirSync(strategiesDir)
  .filter((f) => f.endsWith('.md'))
  .map((f) => f.replace(/\.md$/, ''));

// (1) missing
for (const name of referenced) {
  if (!actual.includes(name)) {
    fail(`SKILL.md references strategies/${name}.md but the file is missing`);
  }
}
// (2) orphan
for (const name of actual) {
  if (!referenced.has(name)) {
    fail(`strategies/${name}.md exists but is not referenced in SKILL.md`);
  }
}

// (3) + (4) per-file structure
for (const name of actual) {
  const text = readFileSync(join(strategiesDir, `${name}.md`), 'utf8');
  if (!/^#\s+/m.test(text)) fail(`${name}.md: missing a top-level "# " title`);
  if (!/^##\s+Restructuring rules/m.test(text)) {
    fail(`${name}.md: missing "## Restructuring rules"`);
  }
  if (!/^##\s+Anti-patterns/m.test(text)) {
    fail(`${name}.md: missing an "## Anti-patterns" section`);
  }
  if (name !== 'universal') {
    const sourceLine = text.split('\n').find((l) => /^>\s*Source:/.test(l));
    if (!sourceLine) fail(`${name}.md: missing a "> Source:" line`);
    else if (!/https?:\/\//.test(sourceLine)) {
      fail(`${name}.md: "> Source:" line has no link`);
    }
  }
}

if (errors.length) {
  console.error(`✗ Strategy validation failed (${errors.length}):`);
  for (const e of errors) console.error('  - ' + e);
  process.exit(1);
}
console.log(
  `✓ Strategy validation passed: ${actual.length} files, all referenced and well-formed.`,
);
