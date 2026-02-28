/**
 * Lógica de busca automática de ofertas (Amazon e Mercado Livre).
 * Usada pelo script fetch-ofertas e pelo endpoint da API (UI).
 */
import { readFileSync, existsSync } from "fs";
import { join } from "path";
import { scrapeProductFromUrl, scrapedToProductInput } from "./scrape-url.service.js";
import { extractProductUrlsFromListing, looksLikeListingPage } from "./scrape-listing.service.js";
import { inferCategorySlugFromTitle } from "./categorize.service.js";
import * as productsRepo from "../../repositories/products.repository.js";
import * as categoriesRepo from "../../repositories/categories.repository.js";
import { logger } from "../../config/logger.js";

const DEFAULT_DELAY_MS = 2500;
const DEFAULT_MAX_PER_LISTING = 15;

function sleep(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms));
}

function getSource(url: string): "amazon" | "mercadolivre" {
  const u = url.toLowerCase();
  return u.includes("mercadolivre") || u.includes("mercadolibre") ? "mercadolivre" : "amazon";
}

/** Diretório raiz do backend (funciona com tsx e com node dist/). */
function getBackendRoot(): string {
  const cwd = process.cwd();
  if (cwd.endsWith("backend")) return cwd;
  return join(cwd, "backend");
}

function loadUrlsFromConfig(): string[] {
  const envUrls = process.env.OFERTAS_URLS;
  if (envUrls) {
    return envUrls
      .split(/[\n,;]+/)
      .map((s) => s.trim())
      .filter(Boolean);
  }
  const root = getBackendRoot();
  const jsonPath = join(root, "scripts", "ofertas-urls.json");
  if (existsSync(jsonPath)) {
    try {
      const data = JSON.parse(readFileSync(jsonPath, "utf-8"));
      const list = data.urls || data.urlList || [];
      return Array.isArray(list) ? list.filter((u: string) => typeof u === "string" && u.startsWith("http")) : [];
    } catch (e) {
      logger.warn({ err: e, path: jsonPath }, "Could not load ofertas-urls.json");
    }
  }
  const txtPath = join(root, "scripts", "ofertas-urls.txt");
  if (existsSync(txtPath)) {
    return readFileSync(txtPath, "utf-8")
      .split(/\n/)
      .map((s) => s.trim())
      .filter((s) => s && s.startsWith("http"));
  }
  return [];
}

export type FetchOfertasOptions = {
  urls?: string[];
  maxPerListing?: number;
  delayMs?: number;
};

export type FetchOfertasResult = {
  inserted: number;
  failed: number;
  totalUrls: number;
};

/**
 * Busca ofertas nas URLs configuradas (ou nas urls passadas), scrape e insere no banco.
 * Pode ser chamado pelo script CLI ou pelo endpoint da API (UI).
 */
export async function runFetchOfertas(options: FetchOfertasOptions = {}): Promise<FetchOfertasResult> {
  const urls = options.urls?.length ? options.urls : loadUrlsFromConfig();
  const delayMs = options.delayMs ?? DEFAULT_DELAY_MS;
  const maxPerListing = options.maxPerListing ?? DEFAULT_MAX_PER_LISTING;

  if (urls.length === 0) {
    return { inserted: 0, failed: 0, totalUrls: 0 };
  }

  let inserted = 0;
  let failed = 0;

  for (const url of urls) {
    try {
      if (looksLikeListingPage(url)) {
        const productUrls = await extractProductUrlsFromListing(url);
        const toFetch = productUrls.slice(0, maxPerListing);
        for (const productUrl of toFetch) {
          try {
            const scraped = await scrapeProductFromUrl(productUrl);
            const source = getSource(scraped.rawUrl);
            const input = { ...scrapedToProductInput(scraped), source };
            const categorySlug = inferCategorySlugFromTitle(scraped.title);
            const category = await categoriesRepo.getCategoryBySlug(categorySlug);
            if (category) input.categoryId = category.id;
            await productsRepo.insertProduct(input);
            inserted++;
            logger.info({ title: scraped.title.slice(0, 40), source }, "Inserted");
          } catch (e) {
            failed++;
            logger.debug({ err: e, url: productUrl }, "Skip product");
          }
          await sleep(delayMs);
        }
      } else {
        const scraped = await scrapeProductFromUrl(url);
        const source = getSource(scraped.rawUrl);
        const input = { ...scrapedToProductInput(scraped), source };
        const categorySlug = inferCategorySlugFromTitle(scraped.title);
        const category = await categoriesRepo.getCategoryBySlug(categorySlug);
        if (category) input.categoryId = category.id;
        await productsRepo.insertProduct(input);
        inserted++;
        logger.info({ title: scraped.title.slice(0, 40), source }, "Inserted");
      }
    } catch (e) {
      logger.warn({ err: e, url }, "Skip URL");
      failed++;
    }
    await sleep(delayMs);
  }

  return { inserted, failed, totalUrls: urls.length };
}
