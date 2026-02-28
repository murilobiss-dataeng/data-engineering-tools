/**
 * Extrai links de produtos a partir de páginas de listagem (ofertas, busca)
 * Amazon, Mercado Livre e Shopee. Para uso com o script de busca automática.
 */
import * as cheerio from "cheerio";
import { logger } from "../../config/logger.js";

const BROWSER_UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";

/** Padrões de URL de produto por site */
const AMAZON_PRODUCT_PATH = /^\/(dp|gp\/product)\/[A-Z0-9]{10}/i;
const ML_PRODUCT_PATH = /\/p\/[A-Z0-9]+|(?:listado|item)\.mercadolivre\.com\.br\/[^/]+_[A-Z0-9]+/i;
const SHOPEE_PRODUCT_PATH = /\/[^/]+-i\.(\d+)\.(\d+)/i;

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
    // Mercado Livre: URL canônica do item
    if (host.includes("mercadolivre") || host.includes("mercadolibre")) {
      if (/\/p\/[A-Z0-9]+/.test(path)) return u.origin + path;
      if (path.includes("MLB") && path.length < 200) return u.origin + path;
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
 * Retorna lista única e normalizada de URLs para scrape posterior.
 */
export async function extractProductUrlsFromListing(listingUrl: string): Promise<string[]> {
  const res = await fetch(listingUrl, {
    headers: {
      "User-Agent": BROWSER_UA,
      Accept: "text/html,application/xhtml+xml",
      "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    },
    redirect: "follow",
  });

  if (!res.ok) {
    logger.warn({ url: listingUrl, status: res.status }, "Listing page fetch failed");
    return [];
  }

  const html = await res.text();
  const $ = cheerio.load(html);
  const baseUrl = res.url || listingUrl;
  const seen = new Set<string>();

  $("a[href]").each((_, el) => {
    const href = $(el).attr("href");
    if (!href) return;
    const normalized = normalizeUrl(href, baseUrl);
    if (normalized && !seen.has(normalized)) seen.add(normalized);
  });

  const urls = Array.from(seen);
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
