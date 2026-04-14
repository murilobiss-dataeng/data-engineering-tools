/**
 * Em PaaS (Render etc.), o cache default ~/.cache/ms-playwright do build não vai para o runtime.
 * Fix: browsers dentro do projeto (.cache/ms-playwright) para coincidir com npm run pw:install.
 */
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// src/config e dist/config: dois níveis até a raiz do backend (não confundir com dist/ apenas).
const backendRoot = path.resolve(__dirname, "../..");
if (!process.env.PLAYWRIGHT_BROWSERS_PATH) {
  process.env.PLAYWRIGHT_BROWSERS_PATH = path.join(backendRoot, ".cache", "ms-playwright");
}
