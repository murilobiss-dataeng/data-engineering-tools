/**
 * Extrai links de produtos a partir de páginas de listagem (ofertas, busca)
 * Amazon, Mercado Livre e Shopee. Para uso com o script de busca automática.
 * Para listagem Amazon (/deals) pode usar Playwright (USE_BROWSER_SCRAPER=true) para evitar bloqueio/SSL.
 */
import * as cheerio from "cheerio";
import { logger } from "../../config/logger.js";

const BROWSER_UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";

function isAmazonListingUrl(url: string): boolean {
  try {
    const u = new URL(url);
    const host = u.hostname.replace(/^www\./, "").toLowerCase();
    const path = u.pathname.toLowerCase();
    if (!host.includes("amazon")) return false;
    return path.includes("/deals") || path.includes("/s?") || path.includes("/b/") || path.includes("/gp/offer-listing");
  } catch {
    return false;
  }
}

function useBrowserForAmazonListing(): boolean {
  const v = process.env.USE_BROWSER_SCRAPER;
  return v === "true" || v === "1";
}

function extractUrlsFromHtml(html: string, baseUrl: string): string[] {
  const $ = cheerio.load(html);
  const seen = new Set<string>();
  $("a[href]").each((_, el) => {
    const href = $(el).attr("href");
    if (!href) return;
    const normalized = normalizeUrl(href, baseUrl);
    if (normalized && !seen.has(normalized)) seen.add(normalized);
  });
  return Array.from(seen);
}

/** Padrões de URL de produto por site */
const AMAZON_PRODUCT_PATH = /^\/(dp|gp\/product)\/[A-Z0-9]{10}/i;
const ML_PRODUCT_PATH = /\/p\/[A-Z0-9]+|(?:listado|item)\.mercadolivre\.com\.br\/[^/]+_[A-Z0-9]+/i;
const SHOPEE_PRODUCT_PATH = /\/[^/]+-i\.(\d+)\.(\d+)/i;

/** Subdomínios do ML que NUNCA são página de produto (tracking, redirect, ofertas). */
const ML_NON_PRODUCT_HOSTS = /^(click\d*|tracking|redirect|ofertas|auth)\.(mercadolivre|mercadolibre)(\.com\.br)?$/i;

function normalizeUrl(href: string, baseUrl: string): string | null {
  try {
    const u = new URL(href, baseUrl);
    if (u.protocol !== "http:" && u.protocol !== "https:") return null;
    const path = u.pathname;
    const host = u.hostname.replace(/^www\./, "").toLowerCase();
    // Amazon: apenas /dp/ASIN ou /gp/product/ASIN (remover query para dedupe)
    if (/^amazon\.(com|com\.br)/.test(host)) {
      const match = path.match(/\/(dp|gp\/product)\/([A-Z0-9]{10})/i);
      if (match) return `https://www.amazon.com.br/dp/${match[2]}`;
      return null;
    }
    // Mercado Livre: só aceitar páginas de produto (www ou produto), nunca click/tracking
    if (host.includes("mercadolivre") || host.includes("mercadolibre")) {
      if (ML_NON_PRODUCT_HOSTS.test(host)) return null;
      const isProductHost = host === "mercadolivre.com.br" || host === "mercadolibre.com.br" || host === "produto.mercadolivre.com.br" || host === "produto.mercadolibre.com.br" || /^(listado|item)\.(mercadolivre|mercadolibre)\.com\.br$/.test(host);
      if (!isProductHost) return null;
      if (/\/p\/[A-Z0-9]+/.test(path)) return u.origin + path.split("?")[0];
      if (/\/MLB\d+/.test(path) && path.length < 200) return u.origin + path.split("?")[0];
      return null;
    }
    // Shopee: produto -i.shopid.itemid
    if (host.includes("shopee")) {
      if (SHOPEE_PRODUCT_PATH.test(path) && path.length < 500) return u.origin + path;
      return null;
    }
    return null;
  } catch {
    return null;
  }
}

/**
 * Busca uma página e extrai URLs de produtos (Amazon ou Mercado Livre).
 * Para listagem Amazon, se USE_BROWSER_SCRAPER=true usa Playwright para evitar bloqueio/SSL.
 */
export async function extractProductUrlsFromListing(listingUrl: string): Promise<string[]> {
  const isAmazon = isAmazonListingUrl(listingUrl);
  const useBrowser = useBrowserForAmazonListing();

  const tryFetch = async (): Promise<{ html: string; baseUrl: string } | null> => {
    try {
      const res = await fetch(listingUrl, {
        headers: {
          "User-Agent": BROWSER_UA,
          Accept: "text/html,application/xhtml+xml",
          "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
        },
        redirect: "follow",
        cache: "no-store",
      });
      if (!res.ok) {
        logger.warn({ url: listingUrl, status: res.status }, "Listing page fetch failed");
        return null;
      }
      const html = await res.text();
      return { html, baseUrl: res.url || listingUrl };
    } catch (err: unknown) {
      const code = err && typeof err === "object" && "code" in err ? (err as { code?: string }).code : undefined;
      if (code === "ERR_SSL_PACKET_LENGTH_TOO_LONG") {
        logger.warn({ url: listingUrl }, "Listing fetch: SSL error");
      }
      return null;
    }
  };

  const tryPlaywright = async (): Promise<{ html: string; baseUrl: string } | null> => {
    if (!useBrowser) return null;
    try {
      const { getHtmlWithBrowser } = await import("./browser-scraper.service.js");
      const html = await getHtmlWithBrowser(listingUrl);
      return { html, baseUrl: listingUrl };
    } catch (e) {
      logger.warn({ url: listingUrl, err: e }, "Listing fetch via Playwright failed");
      return null;
    }
  };

  let result: { html: string; baseUrl: string } | null = null;

  if (isAmazon && useBrowser) {
    logger.info({ url: listingUrl }, "Amazon listing: using Playwright");
    result = await tryPlaywright();
    if (!result) result = await tryFetch();
  } else {
    result = await tryFetch();
    if (!result && isAmazon && useBrowser) {
      logger.info({ url: listingUrl }, "Amazon listing: retrying with Playwright");
      result = await tryPlaywright();
    }
  }

  if (!result) {
    return [];
  }

  const urls = extractUrlsFromHtml(result.html, result.baseUrl);
  logger.info({ listingUrl, count: urls.length }, "Extracted product URLs from listing");
  return urls;
}

/**
 * Indica se a URL parece ser de uma página de listagem (vários produtos)
 * em vez de uma página de um único produto.
 */
export function looksLikeListingPage(url: string): boolean {
  try {
    const u = new URL(url);
    const path = u.pathname.toLowerCase();
    const host = u.hostname.replace(/^www\./, "").toLowerCase();
    // Amazon: /deals, /s?k=, /b/, /gp/offer-listing
    if (host.includes("amazon")) {
      return path.includes("/deals") || path.includes("/s?") || path.includes("/b/") || path.includes("/gp/offer-listing");
    }
    // ML: /ofertas, /lista, busca
    if (host.includes("mercadolivre") || host.includes("mercadolibre")) {
      return path.includes("/ofertas") || path.includes("/lista") || path.includes("/busca") || path === "/";
    }
    // Shopee: flash sale, categorias, busca
    if (host.includes("shopee")) {
      return path.includes("/flash-sale") || path.includes("/cat/") || path.includes("/search") || path === "/" || path === "";
    }
    return false;
  } catch {
    return false;
  }
}
