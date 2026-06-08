import { readFileSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const live = process.argv.includes('--live');
const timeoutMs = 8000;

function strategyUrls() {
  const dir = join(root, 'strategies');
  const urls = [];
  for (const file of readdirSync(dir).filter((name) => name.endsWith('.md')).sort()) {
    const text = readFileSync(join(dir, file), 'utf8');
    for (const match of text.matchAll(/https?:\/\/[^\s)]+/g)) {
      urls.push({ file, url: match[0] });
    }
  }
  return urls;
}

async function fetchWithTimeout(url, method) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { method, redirect: 'follow', signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

async function checkUrl(item) {
  try {
    let response = await fetchWithTimeout(item.url, 'HEAD');
    if ([403, 405].includes(response.status)) {
      response = await fetchWithTimeout(item.url, 'GET');
    }
    if ([404, 410].includes(response.status) || response.status >= 500) {
      return { ...item, status: response.status, level: 'error' };
    }
    if ([401, 403, 429].includes(response.status)) {
      return { ...item, status: response.status, level: 'warning' };
    }
    return { ...item, status: response.status, level: 'ok' };
  } catch (error) {
    return { ...item, status: error.name, level: 'warning' };
  }
}

const urls = strategyUrls();
if (!urls.length) {
  console.error('No strategy source URLs found.');
  process.exit(1);
}

if (!live) {
  console.log(`Link syntax check passed: ${urls.length} strategy source URLs found.`);
  process.exit(0);
}

const results = await Promise.all(urls.map(checkUrl));
const errors = results.filter((result) => result.level === 'error');
const warnings = results.filter((result) => result.level === 'warning');

for (const warning of warnings) {
  console.warn(`Link check warning: ${warning.status} ${warning.file} ${warning.url}`);
}

if (errors.length) {
  console.error(`Link check failed (${errors.length}):`);
  for (const error of errors) console.error(`  - ${error.status} ${error.file} ${error.url}`);
  process.exit(1);
}

console.log(`Live link check passed: ${urls.length - warnings.length}/${urls.length} reachable; ${warnings.length} inconclusive.`);
