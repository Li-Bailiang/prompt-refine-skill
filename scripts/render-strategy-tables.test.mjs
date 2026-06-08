import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  loadManifest,
  renderReadmeTable,
  renderSkillTable,
} from './render-strategy-tables.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const read = (file) => readFileSync(join(root, file), 'utf8');

test('strategy manifest renders the SKILL.md routing table', () => {
  const manifest = loadManifest();
  const table = renderSkillTable(manifest);

  assert.match(table, /\| GPT \/ GPT-5 \(OpenAI\) \| `strategies\/openai\.md` \|/);
  assert.match(table, /\| DeepSeek V4 \(\+ R1\) \| `strategies\/deepseek\.md` \|/);
  assert.ok(read('SKILL.md').includes(table));
});

test('strategy manifest renders consistent English and Chinese README tables', () => {
  const manifest = loadManifest();
  const enTable = renderReadmeTable(manifest, 'en');
  const zhTable = renderReadmeTable(manifest, 'zh');

  assert.ok(read('README.md').includes(enTable));
  assert.ok(read('README.en.md').includes(enTable));
  assert.ok(read('README.zh.md').includes(zhTable));
  assert.match(zhTable, /OpenAI GPT（GPT-5 系列）/);
  assert.match(zhTable, /DeepSeek V4（含 R1）/);
});
