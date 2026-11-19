import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// Resolve the artwork relative to this entrypoint, regardless of the working directory.
const artwork = join(dirname(fileURLToPath(import.meta.url)), 'entry.png');
const outputDirectory = process.env.MAKEFUN_OUTPUT_DIR || '/output';

try {
  mkdirSync(outputDirectory, { recursive: true });
  // Copy the original PNG bytes directly so repeated offline runs stay identical.
  copyFileSync(artwork, join(outputDirectory, 'entry.png'));
} catch (error) {
  console.error(`Unable to copy the news poster into ${outputDirectory}:`, error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
}
