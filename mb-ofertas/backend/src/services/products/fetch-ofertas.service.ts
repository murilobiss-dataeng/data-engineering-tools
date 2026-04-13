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
const DEFAULT_MAX_PER_LISTING = 100;
const SHOPEE_SEARCH_LIMIT_PER_KEYWORD = 10;

const BROWSER_UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";

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

/** Proxy opcional para listagens Amazon (menos bloqueio em alguns ambientes). */
function canUseAmazonSource(): boolean {
  return Boolean(process.env.AMAZON_DEALS_PROXY_URL?.trim());
}

/** Mesma regra de scrape-listing / scrape-url: Playwright para HTML quando fetch falha. */
function useBrowserScraperEnv(): boolean {
  const v = process.env.USE_BROWSER_SCRAPER;
  return v === "true" || v === "1";
}

/** Diretório raiz do backend (funciona com tsx e com node dist/). */
function getBackendRoot(): string {
  const cwd = process.cwd();
  if (cwd.endsWith("backend")) return cwd;
  return join(cwd, "backend");
}

/** URLs padrão quando não há OFERTAS_URLS nem ofertas-urls.json.
 * Amazon/Shopee podem falhar em datacenter (SSL/bot); use AMAZON_DEALS_PROXY_URL ou USE_BROWSER_SCRAPER=true.
 */
export function getDefaultListingUrls(): string[] {
  const urls: string[] = [];
  const proxy = process.env.AMAZON_DEALS_PROXY_URL?.trim();
  if (proxy && proxy.length > 0) {
    urls.push(proxy);
  } else {
    urls.push("https://www.amazon.com.br/deals");
  }
  urls.push("https://www.mercadolivre.com.br/ofertas");
  urls.push("https://www.mercadolivre.com.br/ofertas/do-dia");
  urls.push("https://shopee.com.br/flash-sale");
  return urls;
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

const SHOPEE_KEYWORD_GROUPS: Record<string, string[]> = {
  health: [
    "creatina",
    "whey protein",
    "whey isolado",
    "whey hidrolisado",
    "pré-treino",
    "pré treino",
    "suplemento",
    "suplemento alimentar",
    "vitamina",
    "multivitamínico",
    "vitamina c",
    "vitamina d",
    "vitamina b12",
    "colágeno",
    "colágeno hidrolisado",
    "bcaa",
    "glutamina",
    "hipercalórico",
    "termogênico",
    "omega 3",
    "óleo de peixe",
    "melatonina",
    "magnésio",
    "zinco",
    "coenzima q10",
    "cafeína",
    "barra de proteína",
    "barra proteica",
    "suplemento vegano",
    "proteína vegetal",
    "caseína",
    "isotônico",
    "bebida proteica",
    "shaker",
    "garrafa shaker",
    "energia",
    "imunidade",
    "ganho de massa",
    "massa muscular",
    "recuperação muscular",
    "performance",
    "nutrição esportiva",
  ],
  tech: [
    "notebook",
    "laptop",
    "ultrabook",
    "macbook",
    "chromebook",
    "smartphone",
    "celular",
    "iphone",
    "android",
    "fone bluetooth",
    "fone sem fio",
    "earbuds",
    "airbuds",
    "headset",
    "headset gamer",
    "headphone",
    "monitor",
    "monitor gamer",
    "monitor ultrawide",
    "ssd",
    "ssd nvme",
    "ssd sata",
    "hd externo",
    "pendrive",
    "teclado",
    "teclado mecânico",
    "teclado gamer",
    "mouse",
    "mouse gamer",
    "mouse sem fio",
    "webcam",
    "microfone",
    "microfone usb",
    "cadeira gamer",
    "mesa gamer",
    "placa de vídeo",
    "gpu",
    "processador",
    "cpu",
    "memória ram",
    "gabinete",
    "fonte pc",
    "cooler",
    "water cooler",
    "roteador",
    "wifi",
    "mesh wifi",
    "repetidor wifi",
    "switch rede",
    "câmera de segurança",
    "câmera ip",
    "smartwatch",
    "smartband",
    "tablet",
    "ipad",
    "carregador",
    "carregador turbo",
    "power bank",
    "hub usb",
    "adaptador usb",
    "dock station",
    "suporte notebook",
    "suporte monitor",
  ],
  ofertas: [
    "promoção",
    "oferta",
    "desconto",
    "cupom",
    "cupom desconto",
    "super oferta",
    "mega oferta",
    "oferta relâmpago",
    "oferta do dia",
    "promoção do dia",
    "imperdível",
    "últimas unidades",
    "preço baixo",
    "menor preço",
    "preço especial",
    "desconto exclusivo",
    "liquidação",
    "saldão",
    "promoção limitada",
    "desconto progressivo",
    "frete grátis",
    "frete gratis",
    "entrega grátis",
    "cashback",
    "preço histórico",
    "oferta amazon",
    "oferta mercado livre",
    "achado",
    "achadinho",
    "promo imperdível",
    "desconto relâmpago",
  ],
  faith: [
    "bíblia",
    "bíblia sagrada",
    "bíblia de estudo",
    "bíblia católica",
    "bíblia evangélica",
    "livro evangélico",
    "livro cristão",
    "livro cristão motivacional",
    "devocional",
    "devocional diário",
    "devocional cristão",
    "livro de oração",
    "oração",
    "oração poderosa",
    "oração diária",
    "oração da manhã",
    "oração da noite",
    "oração da família",
    "livro gospel",
    "livro espiritual",
    "livro religioso",
    "louvor",
    "música gospel",
    "cd gospel",
    "dvd gospel",
    "camiseta cristã",
    "camiseta gospel",
    "quadro bíblico",
    "quadro cristão",
    "decoração cristã",
    "presente cristão",
    "presente religioso",
    "terço",
    "terço católico",
    "imagem de santo",
    "estátua religiosa",
    "vela religiosa",
    "cruz",
    "crucifixo",
    "medalha religiosa",
    "medalha de são bento",
    "livro de salmos",
    "salmos",
    "evangelho",
    "palavra de deus",
    "estudo bíblico",
  ],
};

function getRandomItems<T>(arr: T[], count: number): T[] {
  const copy = [...arr];
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [copy[i], copy[j]] = [copy[j], copy[i]];
  }
  return copy.slice(0, count);
}

function buildShopeeProductUrl(shopId: number | string, itemId: number | string): string {
  return `https://shopee.com.br/product/${shopId}/${itemId}`;
}

async function fetchShopeeProductsFromApi(maxPerListing: number): Promise<string[]> {
  const keywords: string[] = [];
  for (const group of Object.values(SHOPEE_KEYWORD_GROUPS)) {
    keywords.push(...getRandomItems(group, Math.min(2, group.length)));
  }

  const seen = new Set<string>();
  let forbiddenCount = 0;

  for (const keyword of keywords) {
    const params = new URLSearchParams({
      by: "relevancy",
      keyword,
      limit: String(Math.min(SHOPEE_SEARCH_LIMIT_PER_KEYWORD, maxPerListing)),
      newest: "0",
      order: "desc",
      page_type: "search",
      version: "2",
    });
    const apiUrl = `https://shopee.com.br/api/v4/search/search_items?${params.toString()}`;
    try {
      const res = await fetch(apiUrl, {
        headers: {
          "User-Agent": BROWSER_UA,
          Accept: "application/json",
          "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
          Origin: "https://shopee.com.br",
          Referer: `https://shopee.com.br/search?keyword=${encodeURIComponent(keyword)}`,
          "sec-ch-ua": '"Chromium";v="120", "Google Chrome";v="120", "Not_A Brand";v="24"',
          "sec-ch-ua-mobile": "?0",
          "sec-ch-ua-platform": '"Windows"',
        },
      });
      if (!res.ok) {
        if (res.status === 403) {
          forbiddenCount++;
          logger.info(
            { keyword },
            "Shopee API 403 (comum em IP de datacenter). Use OFERTAS_URLS com links de produto Shopee se precisar."
          );
        } else {
          logger.warn({ apiUrl, status: res.status }, "Shopee API search failed");
        }
        continue;
      }
      const data: any = await res.json();
      const items: any[] = data?.items ?? data?.data?.items ?? [];
      for (const item of items) {
        const shopid = item.shopid ?? item.shop_id;
        const itemid = item.itemid ?? item.item_id;
        if (shopid == null || itemid == null) continue;
        const url = buildShopeeProductUrl(shopid, itemid);
        if (!seen.has(url)) {
          seen.add(url);
        }
      }
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      logger.warn({ err: e, apiUrl, keyword, message: msg }, "Shopee API search error");
      appendLog("warn", `[Shopee API] ${keyword} → ${msg}`);
    }
    await sleep(DEFAULT_DELAY_MS);
  }

  const urls = Array.from(seen);
  if (forbiddenCount > 0 && urls.length === 0) {
    logger.info(
      { forbiddenCount },
      "Shopee bloqueou todas as buscas da API neste ambiente. Para Shopee, use links de produto em OFERTAS_URLS."
    );
  }
  logger.info({ count: urls.length }, "Shopee API: collected product URLs");
  return urls;
}

/**
 * Busca ofertas nas URLs configuradas (ou nas urls passadas), scrape e insere no banco.
 * Pode ser chamado pelo script CLI ou pelo endpoint da API (UI).
 */
export async function runFetchOfertas(options: FetchOfertasOptions = {}): Promise<FetchOfertasResult> {
  const configUrls = options.urls?.length ? options.urls : loadUrlsFromConfig();
  const rawUrls = configUrls.length > 0 ? configUrls : getDefaultListingUrls();
  const urls = rawUrls;

  logger.info(
    {
      amazonDealsProxyConfigured: canUseAmazonSource(),
      useBrowserScraper: useBrowserScraperEnv(),
      listingUrlCount: urls.length,
    },
    "fetch-ofertas: variáveis de ambiente (Amazon/Shopee)"
  );

  const amazonWithoutMitigation = urls.filter(
    (u) => getSource(u) === "amazon" && !canUseAmazonSource() && !useBrowserScraperEnv()
  );
  if (amazonWithoutMitigation.length > 0) {
    logger.warn(
      { count: amazonWithoutMitigation.length, sample: amazonWithoutMitigation[0] },
      "URLs Amazon na fila sem AMAZON_DEALS_PROXY_URL e sem USE_BROWSER_SCRAPER: listagem pode falhar (SSL/anti-bot)."
    );
  }
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

  // Shopee: busca automática via API (pode retornar 403 em datacenter). Desative com SHOPEE_SEARCH_ENABLED=false.
  const shopeeEnabled = process.env.SHOPEE_SEARCH_ENABLED !== "false" && process.env.SHOPEE_SEARCH_ENABLED !== "0";
  if (shopeeEnabled) {
  try {
    const shopeeUrls = await fetchShopeeProductsFromApi(maxPerListing);
    const toFetch = shopeeUrls.slice(0, maxPerListing);
    for (const productUrl of toFetch) {
      try {
        const scraped = await scrapeProductFromUrlWithFallback(productUrl);
        if (isGenericProductTitle(scraped.title)) {
          logger.info({ url: productUrl, title: scraped.title.slice(0, 30) }, "Skip: título genérico (não é produto)");
          continue;
        }
        const input = { ...scrapedToProductInput(scraped), source: "shopee" as const };
        const categorySlug = inferCategorySlugFromTitle(scraped.title, { discountPct: scraped.discountPct });
        const category = await categoriesRepo.getCategoryBySlug(categorySlug);
        if (category) input.categoryId = category.id;
        input.externalId = (scraped as { externalId?: string }).externalId ?? input.externalId;
        const { isNew } = await productsRepo.insertProduct(input);
        if (isNew) inserted++;
        logger.info(
          { title: scraped.title.slice(0, 40), source: "shopee", isNew },
          isNew ? "Inserted (Shopee API)" : "Skip duplicate (Shopee API)"
        );
      } catch (e) {
        failed++;
        const msg = e instanceof Error ? e.message : String(e);
        logger.warn({ err: e, url: productUrl, message: msg }, "Produto falhou (Shopee API)");
        appendLog("warn", `[Shopee API produto] ${productUrl} → ${msg}`);
      }
      await sleep(delayMs);
    }
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    logger.warn({ err: e, message: msg }, "Shopee API fetch block failed");
    appendLog("warn", `[Shopee API bloco] ${msg}`);
  }
  }

  return { inserted, failed, totalUrls: urls.length };
}
