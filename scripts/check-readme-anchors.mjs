import { readFileSync, readdirSync } from 'node:fs';
import { basename, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

function slugify(heading) {
  return heading
    .trim()
    .toLowerCase()
    .replace(/<[^>]+>/g, '')
    .replace(/[`*_]/g, '')
    .replace(/[^\p{Letter}\p{Number}\s-]/gu, '')
    .trim()
    .replace(/\s+/g, '-');
}

function anchorsFor(text) {
  const anchors = new Set();
  for (const line of text.split(/\r?\n/)) {
    const markdown = /^(#{1,6})\s+(.+?)\s*$/.exec(line);
    if (markdown) anchors.add(slugify(markdown[2]));
    const html = /<h([1-6])[^>]*>(.*?)<\/h\1>/i.exec(line);
    if (html) anchors.add(slugify(html[2]));
  }
  return anchors;
}

function checkFile(file) {
  const text = readFileSync(join(root, file), 'utf8');
  const anchors = anchorsFor(text);
  const errors = [];
  for (const match of text.matchAll(/\[[^\]]+\]\(#([^)]+)\)/g)) {
    const wanted = decodeURIComponent(match[1]);
    if (!anchors.has(wanted)) errors.push(`${file}: missing anchor #${wanted}`);
  }
  return errors;
}

const files = readdirSync(root)
  .filter((file) => /^README(\.[a-z]+)?\.md$/.test(file))
  .sort();

const errors = files.flatMap(checkFile);
if (errors.length) {
  console.error(`README anchor check failed (${errors.length}):`);
  for (const error of errors) console.error(`  - ${error}`);
  process.exit(1);
}

console.log(`README anchor check passed: ${files.map((file) => basename(file)).join(', ')}`);
