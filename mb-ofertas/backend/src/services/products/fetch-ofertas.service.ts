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
/** URLs de catálogo religioso (não são páginas de ofertas — busca/lista de produtos). */
export function getFaithCatalogUrls(): string[] {
  const env = process.env.FAITH_CATALOG_URLS;
  if (env) {
    return env
      .split(/[\n,;]+/)
      .map((s) => s.trim())
      .filter((u) => u.startsWith("http"));
  }
  return [
    "https://lista.mercadolivre.com.br/biblia",
    "https://lista.mercadolivre.com.br/livro-evangelico",
    "https://lista.mercadolivre.com.br/livro-cristao",
    "https://lista.mercadolivre.com.br/devocional",
    "https://lista.mercadolivre.com.br/terco",
    "https://lista.mercadolivre.com.br/crucifixo",
    "https://lista.mercadolivre.com.br/quadro-biblico",
    "https://lista.mercadolivre.com.br/camiseta-gospel",
    "https://lista.mercadolivre.com.br/musica-gospel",
    "https://lista.mercadolivre.com.br/imagem-de-santo",
    "https://www.amazon.com.br/s?k=biblia+sagrada",
    "https://www.amazon.com.br/s?k=livro+cristao",
    "https://www.amazon.com.br/s?k=devocional+cristao",
    "https://www.amazon.com.br/s?k=terco+catolico",
    "https://www.amazon.com.br/s?k=crucifixo+parede",
    "https://shopee.com.br/search?keyword=biblia",
    "https://shopee.com.br/search?keyword=devocional",
    "https://shopee.com.br/search?keyword=terco",
    "https://shopee.com.br/search?keyword=crucifixo",
    "https://shopee.com.br/search?keyword=livro+cristao",
  ];
}

/** Mínimo de produtos na fila por canal antes de acionar busca extra. */
export const MIN_QUEUE_PER_CHANNEL = Number(process.env.MIN_QUEUE_PER_CHANNEL) || 30;

const SHOPEE_SEARCH_LIMIT_PER_KEYWORD = 15;
/** Quantas keywords Shopee sortear por grupo (faith usa mais para encher o canal). */
const SHOPEE_KEYWORDS_PER_GROUP: Record<string, number> = {
  faith: 12,
  health: 4,
  tech: 4,
  ofertas: 3,
};

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

async function fetchShopeeProductsFromApi(
  maxPerListing: number,
  options?: { groups?: string[]; forceCategorySlug?: string }
): Promise<string[]> {
  const keywords: string[] = [];
  const groups = options?.groups ?? Object.keys(SHOPEE_KEYWORD_GROUPS);
  for (const groupKey of groups) {
    const group = SHOPEE_KEYWORD_GROUPS[groupKey];
    if (!group) continue;
    const pick = SHOPEE_KEYWORDS_PER_GROUP[groupKey] ?? 3;
    keywords.push(...getRandomItems(group, Math.min(pick, group.length)));
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

type InsertScrapeOptions = {
  forceCategorySlug?: string;
  source?: "amazon" | "mercadolivre" | "shopee";
};

async function resolveCategoryId(title: string, discountPct: number | null | undefined, forceSlug?: string): Promise<string | null> {
  const slug = forceSlug ?? inferCategorySlugFromTitle(title, { discountPct });
  const category = await categoriesRepo.getCategoryBySlug(slug);
  return category?.id ?? null;
}

async function insertScrapedProduct(
  scraped: Awaited<ReturnType<typeof scrapeProductFromUrlWithFallback>>,
  options: InsertScrapeOptions = {}
): Promise<{ isNew: boolean; skipped: boolean }> {
  if (isGenericProductTitle(scraped.title)) {
    return { isNew: false, skipped: true };
  }
  const source = options.source ?? getSource(scraped.rawUrl);
  const input = { ...scrapedToProductInput(scraped), source };
  const categoryId = await resolveCategoryId(scraped.title, scraped.discountPct, options.forceCategorySlug);
  if (categoryId) input.categoryId = categoryId;
  input.externalId = (scraped as { externalId?: string }).externalId ?? input.externalId;
  const { id, isNew } = await productsRepo.insertProduct(input);
  if (!isNew && input.coupon) {
    const row = await productsRepo.getProductById(id);
    if (row && (row.coupon == null || String(row.coupon).trim() === "")) {
      await productsRepo.updateProductCoupon(id, input.coupon);
    }
  }
  return { isNew, skipped: false };
}

async function scrapeUrlsBatch(
  urls: string[],
  opts: { maxPerListing: number; delayMs: number; forceCategorySlug?: string }
): Promise<{ inserted: number; failed: number }> {
  let inserted = 0;
  let failed = 0;
  const faithCatalogSet = new Set(getFaithCatalogUrls().map((u) => u.split("?")[0]));

  for (const url of urls) {
    try {
      const forceFaith = opts.forceCategorySlug === "faith" || faithCatalogSet.has(url.split("?")[0]);
      if (looksLikeListingPage(url)) {
        const productUrls = await extractProductUrlsFromListing(url);
        const toFetch = productUrls.slice(0, opts.maxPerListing);
        for (const productUrl of toFetch) {
          try {
            const scraped = await scrapeProductFromUrlWithFallback(productUrl);
            const { isNew, skipped } = await insertScrapedProduct(scraped, {
              forceCategorySlug: forceFaith ? "faith" : opts.forceCategorySlug,
            });
            if (!skipped && isNew) inserted++;
            if (!skipped) {
              logger.info(
                { title: scraped.title.slice(0, 40), isNew, forceFaith },
                isNew ? "Inserted" : "Skip duplicate"
              );
            }
          } catch (e) {
            failed++;
            const msg = e instanceof Error ? e.message : String(e);
            logger.warn({ err: e, url: productUrl, message: msg }, "Produto falhou");
            appendLog("warn", `[Scrape] ${productUrl} → ${msg}`);
          }
          await sleep(opts.delayMs);
        }
      } else {
        const scraped = await scrapeProductFromUrlWithFallback(url);
        const { isNew, skipped } = await insertScrapedProduct(scraped, {
          forceCategorySlug: forceFaith ? "faith" : opts.forceCategorySlug,
        });
        if (!skipped && isNew) inserted++;
        if (!skipped) {
          logger.info({ title: scraped.title.slice(0, 40), isNew }, isNew ? "Inserted" : "Skip duplicate");
        }
      }
    } catch (e) {
      failed++;
      const msg = e instanceof Error ? e.message : String(e);
      logger.warn({ err: e, url }, "Skip URL");
      appendLog("warn", `[Listagem] ${url} → ${msg}`);
    }
    await sleep(opts.delayMs);
  }
  return { inserted, failed };
}

/** Repõe filas baixas buscando catálogo (faith) ou ofertas gerais. */
export async function ensureChannelQueues(delayMs = DEFAULT_DELAY_MS): Promise<{ refetched: string[] }> {
  const channels = ["health", "tech", "ofertas", "faith"] as const;
  const refetched: string[] = [];

  for (const slug of channels) {
    const count = await productsRepo.countPendingByChannel(slug);
    if (count >= MIN_QUEUE_PER_CHANNEL) continue;

    logger.info({ slug, count, min: MIN_QUEUE_PER_CHANNEL }, "Fila baixa — buscando mais produtos");

    if (slug === "faith") {
      const faithUrls = getFaithCatalogUrls();
      const r = await scrapeUrlsBatch(faithUrls, {
        maxPerListing: 60,
        delayMs,
        forceCategorySlug: "faith",
      });
      logger.info({ slug, inserted: r.inserted }, "Faith catalog refill");
      refetched.push(slug);

      const shopeeEnabled = process.env.SHOPEE_SEARCH_ENABLED !== "false" && process.env.SHOPEE_SEARCH_ENABLED !== "0";
      if (shopeeEnabled) {
        try {
          const shopeeUrls = await fetchShopeeProductsFromApi(80, { groups: ["faith"] });
          for (const productUrl of shopeeUrls.slice(0, 80)) {
            try {
              const scraped = await scrapeProductFromUrlWithFallback(productUrl);
              const { isNew, skipped } = await insertScrapedProduct(scraped, {
                forceCategorySlug: "faith",
                source: "shopee",
              });
              if (!skipped && isNew) r.inserted++;
            } catch {
              /* ignore individual failures */
            }
            await sleep(delayMs);
          }
        } catch (e) {
          logger.warn({ err: e }, "Faith Shopee refill failed");
        }
      }
    } else {
      const defaults = getDefaultListingUrls();
      const r = await scrapeUrlsBatch(defaults, { maxPerListing: 40, delayMs });
      logger.info({ slug, inserted: r.inserted }, "General catalog refill");
      refetched.push(slug);
    }
  }
  return { refetched };
}

/**
 * Busca ofertas nas URLs configuradas (ou nas urls passadas), scrape e insere no banco.
 * Inclui catálogo religioso (faith) além das páginas de ofertas.
 */
export async function runFetchOfertas(options: FetchOfertasOptions = {}): Promise<FetchOfertasResult> {
  const configUrls = options.urls?.length ? options.urls : loadUrlsFromConfig();
  const rawUrls = configUrls.length > 0 ? configUrls : getDefaultListingUrls();
  const faithUrls = getFaithCatalogUrls();
  const urls = [...new Set([...rawUrls, ...faithUrls])];

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

  const batch = await scrapeUrlsBatch(urls, { maxPerListing, delayMs });
  let inserted = batch.inserted;
  let failed = batch.failed;

  // Shopee: busca automática via API (pode retornar 403 em datacenter). Desative com SHOPEE_SEARCH_ENABLED=false.
  const shopeeEnabled = process.env.SHOPEE_SEARCH_ENABLED !== "false" && process.env.SHOPEE_SEARCH_ENABLED !== "0";
  if (shopeeEnabled) {
    try {
      const shopeeUrls = await fetchShopeeProductsFromApi(maxPerListing * 2);
      const toFetch = shopeeUrls.slice(0, maxPerListing * 2);
      for (const productUrl of toFetch) {
        try {
          const scraped = await scrapeProductFromUrlWithFallback(productUrl);
          const categorySlug = inferCategorySlugFromTitle(scraped.title, { discountPct: scraped.discountPct });
          const { isNew, skipped } = await insertScrapedProduct(scraped, {
            forceCategorySlug: categorySlug === "faith" ? "faith" : undefined,
            source: "shopee",
          });
          if (!skipped && isNew) inserted++;
          if (!skipped) {
            logger.info(
              { title: scraped.title.slice(0, 40), source: "shopee", isNew },
              isNew ? "Inserted (Shopee API)" : "Skip duplicate (Shopee API)"
            );
          }
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

  await ensureChannelQueues(delayMs);

  return { inserted, failed, totalUrls: urls.length };
}
