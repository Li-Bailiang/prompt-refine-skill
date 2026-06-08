import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const manifestFile = join(root, 'data', 'strategies.json');

export function loadManifest(path = manifestFile) {
  const entries = JSON.parse(readFileSync(path, 'utf8'));
  for (const entry of entries) {
    for (const key of [
      'id',
      'file',
      'skillLabel',
      'readmeLabelEn',
      'readmeLabelZh',
      'sourceEn',
      'sourceZh',
    ]) {
      if (!entry[key]) throw new Error(`strategy manifest entry missing ${key}`);
    }
    if (!existsSync(join(root, entry.file))) {
      throw new Error(`strategy manifest references missing file: ${entry.file}`);
    }
  }
  return entries;
}

export function renderSkillTable(entries) {
  return [
    '| If you are running as… | Load |',
    '|---|---|',
    ...entries.map((entry) => `| ${entry.skillLabel} | \`${entry.file}\` |`),
  ].join('\n');
}

export function renderReadmeTable(entries, locale = 'en') {
  const isZh = locale === 'zh';
  const header = isZh
    ? '| 宿主模型 | 策略文件 | 来源家族 |'
    : '| Host model | Strategy file | Source family |';
  return [
    header,
    '|---|---|---|',
    ...entries.map((entry) => {
      const label = isZh ? entry.readmeLabelZh : entry.readmeLabelEn;
      const source = isZh ? entry.sourceZh : entry.sourceEn;
      return `| ${label} | \`${entry.file}\` | ${source} |`;
    }),
  ].join('\n');
}

function replaceTable(text, headerLine, renderedTable) {
  const normalized = text.replace(/\r\n/g, '\n');
  const start = normalized.indexOf(headerLine);
  if (start === -1) throw new Error(`table header not found: ${headerLine}`);
  const end = normalized.indexOf('\n\n', start);
  if (end === -1) throw new Error(`table end not found after: ${headerLine}`);
  return normalized.slice(0, start) + renderedTable + normalized.slice(end);
}

function expectedFiles(entries) {
  const skill = renderSkillTable(entries);
  const readmeEn = renderReadmeTable(entries, 'en');
  const readmeZh = renderReadmeTable(entries, 'zh');
  return [
    {
      path: 'SKILL.md',
      header: '| If you are running as… | Load |',
      table: skill,
    },
    {
      path: 'README.md',
      header: '| Host model | Strategy file | Source family |',
      table: readmeEn,
    },
    {
      path: 'README.en.md',
      header: '| Host model | Strategy file | Source family |',
      table: readmeEn,
    },
    {
      path: 'README.zh.md',
      header: '| 宿主模型 | 策略文件 | 来源家族 |',
      table: readmeZh,
    },
  ];
}

export function renderFiles({ write = false } = {}) {
  const entries = loadManifest();
  const changed = [];
  for (const item of expectedFiles(entries)) {
    const fullPath = join(root, item.path);
    const current = readFileSync(fullPath, 'utf8');
    const next = replaceTable(current, item.header, item.table);
    if (current.replace(/\r\n/g, '\n') !== next) {
      changed.push(item.path);
      if (write) writeFileSync(fullPath, next, 'utf8');
    }
  }
  return changed;
}

if (fileURLToPath(import.meta.url) === process.argv[1]) {
  const write = process.argv.includes('--write');
  const changed = renderFiles({ write });
  if (changed.length && !write) {
    console.error('Strategy tables are out of sync. Run: node scripts/render-strategy-tables.mjs --write');
    for (const file of changed) console.error(`  - ${file}`);
    process.exit(1);
  }
  console.log(
    changed.length
      ? `Updated strategy tables in ${changed.length} file(s).`
      : 'Strategy tables are in sync.',
  );
}
