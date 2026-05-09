/**
 * Obtém HTML de uma URL usando Playwright (Chromium).
 * Usado como fallback quando fetch + Cheerio não trazem preço (página dinâmica).
 * Requer: `npm i playwright` e `npm run pw:install` (chromium + chromium-headless-shell em `.cache/ms-playwright`).
 * (Playwright 1.49+ usa headless shell no launch headless; só `install chromium` não basta.)
 */
import "../../config/playwright-browsers-path.js";
import { logger } from "../../config/logger.js";

const BROWSER_TIMEOUT_MS = Math.min(
  120_000,
  Math.max(15_000, parseInt(process.env.PLAYWRIGHT_NAVIGATION_TIMEOUT_MS || "45000", 10) || 45_000)
);
const WAIT_AFTER_LOAD_MS = 2_000;

/**
 * Abre a URL em um browser headless e retorna o HTML renderizado.
 * Só chame quando USE_BROWSER_SCRAPER=true; o Playwright é importado dinamicamente
 * para não quebrar o app se a dependência não estiver instalada.
 */
export async function getHtmlWithBrowser(url: string): Promise<string> {
  let chromium: any;
  try {
    const pw = await import("playwright");
    chromium = pw.chromium;
  } catch (e) {
    logger.warn(
      { err: e },
      "Playwright não encontrado. Rode: npm i playwright && npx playwright install chromium chromium-headless-shell"
    );
    throw new Error(
      "Playwright não instalado. Para usar fallback com browser: npm i playwright && npx playwright install chromium chromium-headless-shell"
    );
  }

  let browser: any;
  try {
    browser = await chromium.launch({
      headless: true,
      args: ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
    });
  } catch (e) {
    logger.error(
      { err: e },
      "Playwright instalado, mas Chromium/headless-shell não está disponível. Rode: npx playwright install chromium chromium-headless-shell"
    );
    throw new Error(
      "Playwright: Chromium não disponível. Rode: npx playwright install chromium chromium-headless-shell"
    );
  }

  try {
    const page = await browser.newPage({
      userAgent:
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
      viewport: { width: 1280, height: 800 },
    });
    await page.goto(url, {
      waitUntil: "domcontentloaded",
      timeout: BROWSER_TIMEOUT_MS,
    });
    const host = new URL(url).hostname.replace(/^www\./, "").toLowerCase();
    if (/^amazon\.(com|com\.br)$/.test(host)) {
      await page
        .waitForSelector("#productTitle, span#productTitle, #productTitle_feature_div, meta[property='og:title']", {
          timeout: Math.min(12_000, BROWSER_TIMEOUT_MS - 3_000),
        })
        .catch(() => {});
    }
    // Esperar um pouco para JS de preço (ML, Shopee) renderizar
    await new Promise((r) => setTimeout(r, WAIT_AFTER_LOAD_MS));
    const html = await page.content();
    return html;
  } finally {
    await browser.close();
  }
}
