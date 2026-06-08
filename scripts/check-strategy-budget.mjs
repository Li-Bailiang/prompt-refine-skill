import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dir = join(root, 'strategies');
const maxChars = 3600;
const maxLines = 60;

const errors = [];
for (const file of readdirSync(dir).filter((name) => name.endsWith('.md')).sort()) {
  const text = readFileSync(join(dir, file), 'utf8');
  const lines = text.split(/\r?\n/).length;
  if (text.length > maxChars) {
    errors.push(`${file}: ${text.length} chars exceeds ${maxChars}`);
  }
  if (lines > maxLines) {
    errors.push(`${file}: ${lines} lines exceeds ${maxLines}`);
  }
}

if (errors.length) {
  console.error(`Strategy budget check failed (${errors.length}):`);
  for (const error of errors) console.error(`  - ${error}`);
  process.exit(1);
}

console.log(`Strategy budget check passed: max ${maxChars} chars / ${maxLines} lines.`);
