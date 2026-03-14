/**
 * Lógica de busca automática de ofertas (Amazon e Mercado Livre).
 * Usada pelo script fetch-ofertas e pelo endpoint da API (UI).
 */
import { readFileSync, existsSync } from "fs";
import { join } from "path";
import { scrapeProductFromUrlWithFallback, scrapedToProductInput } from "./scrape-url.service.js";
import { extractProductUrlsFromListing, looksLikeListingPage } from "./scrape-listing.service.js";
import { inferCategorySlugFromTitle } from "./categorize.service.js";
import * as productsRepo from "../../repositories/products.repository.js";
import * as categoriesRepo from "../../repositories/categories.repository.js";
import { logger } from "../../config/logger.js";
import { appendLog } from "../../config/log-buffer.js";

const DEFAULT_DELAY_MS = 2500;
const DEFAULT_MAX_PER_LISTING = 45;

/** Títulos que são do site, não de produto — não inserir. */
const GENERIC_TITLES = new Set(["mercado livre", "mercadolivre", "mercado libre", "amazon", "shopee", "oferta", "ofertas"]);

function isGenericProductTitle(title: string): boolean {
  const t = title.trim().toLowerCase().slice(0, 100);
  if (t.length < 12) return true;
  return GENERIC_TITLES.has(t) || GENERIC_TITLES.has(t.replace(/\s+/g, ""));
}

function sleep(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms));
}

function getSource(url: string): "amazon" | "mercadolivre" | "shopee" {
  const u = url.toLowerCase();
  if (u.includes("mercadolivre") || u.includes("mercadolibre")) return "mercadolivre";
  if (u.includes("shopee")) return "shopee";
  return "amazon";
}

/** Diretório raiz do backend (funciona com tsx e com node dist/). */
function getBackendRoot(): string {
  const cwd = process.cwd();
  if (cwd.endsWith("backend")) return cwd;
  return join(cwd, "backend");
}

/** URLs padrão de listagem para busca automática (Amazon, ML). Shopee não incluído: listagem é carregada por JS e não retorna links no HTML. */
export function getDefaultListingUrls(): string[] {
  return [
    "https://www.amazon.com.br/deals",
    "https://www.mercadolivre.com.br/ofertas",
  ];
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
  const configUrls = options.urls?.length ? options.urls : loadUrlsFromConfig();
  const urls = configUrls.length > 0 ? configUrls : getDefaultListingUrls();
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
            const scraped = await scrapeProductFromUrlWithFallback(productUrl);
            if (isGenericProductTitle(scraped.title)) {
              logger.info({ url: productUrl, title: scraped.title.slice(0, 30) }, "Skip: título genérico (não é produto)");
              continue;
            }
            const source = getSource(scraped.rawUrl);
            const input = { ...scrapedToProductInput(scraped), source };
            const categorySlug = inferCategorySlugFromTitle(scraped.title, { discountPct: scraped.discountPct });
            const category = await categoriesRepo.getCategoryBySlug(categorySlug);
            if (category) input.categoryId = category.id;
            input.externalId = (scraped as { externalId?: string }).externalId ?? input.externalId;
            const { isNew } = await productsRepo.insertProduct(input);
            if (isNew) inserted++;
            logger.info({ title: scraped.title.slice(0, 40), source, isNew }, isNew ? "Inserted" : "Skip duplicate");
          } catch (e) {
            failed++;
            const msg = e instanceof Error ? e.message : String(e);
            logger.warn({ err: e, url: productUrl, message: msg }, "Produto falhou (ML/Amazon/Shopee)");
            appendLog("warn", `[ML/Amazon/Shopee] ${productUrl} → ${msg}`);
          }
          await sleep(delayMs);
        }
      } else {
        const scraped = await scrapeProductFromUrlWithFallback(url);
        if (isGenericProductTitle(scraped.title)) {
          logger.info({ url, title: scraped.title.slice(0, 30) }, "Skip: título genérico (não é produto)");
        } else {
          const source = getSource(scraped.rawUrl);
          const input = { ...scrapedToProductInput(scraped), source };
          const categorySlug = inferCategorySlugFromTitle(scraped.title, { discountPct: scraped.discountPct });
          const category = await categoriesRepo.getCategoryBySlug(categorySlug);
          if (category) input.categoryId = category.id;
          input.externalId = (scraped as { externalId?: string }).externalId ?? input.externalId;
          const { isNew } = await productsRepo.insertProduct(input);
          if (isNew) inserted++;
          logger.info({ title: scraped.title.slice(0, 40), source, isNew }, isNew ? "Inserted" : "Skip duplicate");
        }
      }
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      logger.warn({ err: e, url }, "Skip URL");
      appendLog("warn", `[Listagem] ${url} → ${msg}`);
      failed++;
    }
    await sleep(delayMs);
  }

  return { inserted, failed, totalUrls: urls.length };
}
