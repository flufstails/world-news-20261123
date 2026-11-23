// Copies the rendered Monday 23 November 2026 world news front-page image to /output/entry.png.
import { chmodSync, copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true, mode: 0o755 });
const target = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), target);
chmodSync(target, 0o644);
