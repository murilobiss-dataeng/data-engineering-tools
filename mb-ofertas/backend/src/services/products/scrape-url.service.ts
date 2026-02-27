/**
 * Extrai dados de produto a partir de uma URL (Amazon ou Mercado Livre).
 * Usa fetch + Cheerio; sem API oficial. Para uso ético (delay, cache, ToS).
 */
import * as cheerio from "cheerio";
import { logger } from "../../config/logger.js";
import { env } from "../../config/env.js";
import type { ProductInput } from "./types.js";

const PARTNER_TAG = env.AMAZON_PARTNER_TAG ?? "";

const BROWSER_UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";

export type ScrapedProduct = {
  title: string;
  price: number;
  previousPrice: number | null;
  discountPct: number | null;
  imageUrl: string | null;
  affiliateLink: string;
  rawUrl: string;
};

function isAmazonUrl(url: string): boolean {
  try {
    const u = new URL(url);
    return /^amazon\.(com|com\.br|de|co\.uk|fr|it|es|ca)$/i.test(u.hostname.replace(/^www\./, ""));
  } catch {
    return false;
  }
}

function isMercadoLivreUrl(url: string): boolean {
  try {
    const u = new URL(url);
    const host = u.hostname.replace(/^www\./, "").toLowerCase();
    return (
      host === "mercadolivre.com.br" ||
      host === "mercadolibre.com.br" ||
      host === "mercadolivre.com" ||
      host === "mercadolibre.com" ||
      host.endsWith(".mercadolivre.com.br") ||
      host.endsWith(".mercadolibre.com.br")
    );
  } catch {
    return false;
  }
}

/** Adiciona/ substitui tag de afiliado na URL da Amazon. */
function withPartnerTag(url: string): string {
  if (!PARTNER_TAG) return url;
  try {
    const u = new URL(url);
    u.searchParams.set("tag", PARTNER_TAG);
    return u.toString();
  } catch {
    return url;
  }
}

/** Extrai preço de string "R$ 99,90" ou "99,90" ou "99.90". */
function parsePrice(text: string): number | null {
  const normalized = text.replace(/\s/g, "").replace(/\./g, "").replace(",", ".");
  const match = normalized.match(/(\d+\.?\d*)/);
  if (!match) return null;
  const n = parseFloat(match[1]);
  return Number.isFinite(n) ? n : null;
}

/** Tenta extrair preço do HTML (Amazon BR/global). */
function extractPriceFromHtml($: cheerio.CheerioAPI): { price: number; listPrice: number | null } {
  let price: number | null = null;
  let listPrice: number | null = null;

  // Preço atual: seletores comuns Amazon
  const selectors = [
    ".a-price .a-offscreen",
    "span.a-price .a-offscreen",
    "#priceblock_ourprice",
    "#priceblock_dealprice",
    "#priceblock_saleprice",
    "#corePrice_feature_div .a-offscreen",
    "#corePriceDisplay_desktop_feature_div .a-offscreen",
    '[data-a-color="price"] .a-offscreen',
    ".priceToPay .a-offscreen",
    "#apex_desktop .a-offscreen",
  ];
  for (const sel of selectors) {
    const el = $(sel).first();
    if (el.length) {
      const text = el.text().trim();
      const p = parsePrice(text);
      if (p != null && p > 0) {
        price = p;
        break;
      }
    }
  }

  // Preço de lista (riscado)
  const listSelectors = [
    ".a-price.a-text-price .a-offscreen",
    "#priceblock_retailprice",
    ".basisPrice .a-offscreen",
    ".a-text-price.a-offscreen",
  ];
  for (const sel of listSelectors) {
    const el = $(sel).first();
    if (el.length) {
      const text = el.text().trim();
      const p = parsePrice(text);
      if (p != null && p > 0 && (price == null || p > price)) {
        listPrice = p;
        break;
      }
    }
  }

  // Fallback: busca por padrão "R$ X,XX" no HTML
  if (price == null) {
    const body = $.html();
    const priceMatch = body.match(/R\$\s*[\d.,]+|[\d.,]+\s*R\$|"amount"\s*:\s*([\d.]+)/);
    if (priceMatch) {
      const raw = priceMatch[1] ? priceMatch[1] : priceMatch[0];
      const p = parsePrice(raw);
      if (p != null && p > 0) price = p;
    }
  }

  return { price: price ?? 0, listPrice };
}

/** Tenta extrair oferta de JSON embutido no HTML (Amazon). */
function extractFromJsonLd(html: string): Partial<ScrapedProduct> | null {
  const ldMatch = html.match(/<script[^>]*type\s*=\s*["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/i);
  if (!ldMatch) return null;
  try {
    const data = JSON.parse(ldMatch[1].trim());
    const product = Array.isArray(data) ? data.find((d: { "@type"?: string }) => d["@type"] === "Product") : data;
    if (!product || product["@type"] !== "Product") return null;
    const name = product.name ?? product.title ?? "";
    const image = Array.isArray(product.image) ? product.image[0] : product.image;
    const imageUrl = typeof image === "string" ? image : null;
    let price: number | null = null;
    let listPrice: number | null = null;
    const offers = product.offers;
    if (offers) {
      const offer = Array.isArray(offers) ? offers[0] : offers;
      if (offer && offer.price !== undefined) {
        price = typeof offer.price === "number" ? offer.price : parseFloat(String(offer.price)) || null;
      }
      if (offer && offer.priceCurrency === "BRL" && offer.price !== undefined) {
        price = typeof offer.price === "number" ? offer.price : parseFloat(String(offer.price)) || null;
      }
    }
    return { title: name, imageUrl, price: price ?? 0, previousPrice: listPrice };
  } catch {
    return null;
  }
}

/** Busca JSON de estado da página (Amazon às vezes expõe preço aqui). */
function extractPriceFromPageJson(html: string): { price: number; listPrice?: number } | null {
  // Padrão comum: "priceToPay":{"amount":99.9 ou "formattedString":"R$ 99,90"
  const priceToPayMatch = html.match(/priceToPay["\s]*:["\s]*\{[^}]*"amount"["\s]*:["\s]*([\d.]+)/);
  const amountMatch = html.match(/"amount":\s*([\d.]+)/);
  const formattedMatch = html.match(/R\$\s*([\d.,]+)/g);
  if (priceToPayMatch) {
    const p = parseFloat(priceToPayMatch[1]);
    if (Number.isFinite(p)) return { price: p };
  }
  if (amountMatch) {
    const p = parseFloat(amountMatch[1]);
    if (Number.isFinite(p) && p > 0 && p < 1000000) return { price: p };
  }
  if (formattedMatch && formattedMatch.length > 0) {
    const p = parsePrice(formattedMatch[0]);
    if (p != null) return { price: p };
  }
  return null;
}

/** Extrai título, preço e imagem da página do Mercado Livre. */
function extractMercadoLivreFromHtml(
  $: cheerio.CheerioAPI,
  html: string
): { title: string; price: number; listPrice: number | null; imageUrl: string | null } {
  let title =
    $(".ui-pdp-title").first().text().trim() ||
    $("h1.ui-pdp-title").text().trim() ||
    $('[data-testid="product-title"]').text().trim() ||
    $("h1").first().text().trim() ||
    "";

  let price: number | null = null;
  let listPrice: number | null = null;

  // Preço atual — ML: pegar texto do container (ex.: "R$ 1.299" ou "R$ 99,90")
  const priceSelectors = [
    ".ui-pdp-price__main-container",
    ".ui-pdp-price .andes-money-amount",
    ".ui-pdp-price",
    '[data-testid="price"]',
    ".andes-money-amount--cents-superscript",
    ".price-tag",
  ];
  for (const sel of priceSelectors) {
    const el = $(sel).first();
    if (el.length) {
      const full = el.text().trim();
      const parsed = parsePrice(full);
      if (parsed != null && parsed > 0 && parsed < 1000000) {
        price = parsed;
        break;
      }
    }
  }

  // Preço original (riscado)
  const listSelectors = [
    ".andes-money-amount--previous .andes-money-amount__fraction",
    ".ui-pdp-price--original .andes-money-amount__fraction",
    ".andes-money-amount--previous",
  ];
  for (const sel of listSelectors) {
    const el = $(sel).first();
    if (el.length) {
      const text = el.text().trim();
      const p = parsePrice(text);
      if (p != null && p > 0 && (price == null || p > price)) listPrice = p;
      break;
    }
  }

  // Fallback: JSON embutido (ML usa __PRELOADED_STATE__ ou similar)
  if (price == null) {
    const priceInJson = html.match(/"price":\s*([\d.]+)|"original_price":\s*([\d.]+)|"amount":\s*([\d.]+)/g);
    if (priceInJson) {
      for (const part of priceInJson) {
        const m = part.match(/([\d.]+)/);
        if (m) {
          const p = parseFloat(m[1]);
          if (p > 0 && p < 1000000) {
            price = p;
            break;
          }
        }
      }
    }
  }
  if (price == null) {
    const reais = html.match(/R\$\s*[\d.,]+/g);
    if (reais && reais.length > 0) {
      const p = parsePrice(reais[0]);
      if (p != null && p > 0) price = p;
    }
  }

  let imageUrl: string | null =
    $('.ui-pdp-image img[src*="http"]').first().attr("src") ||
    $('[data-zoom]').first().attr("data-zoom") ||
    $(".ui-pdp-image__source").first().attr("src") ||
    null;

  return { title, price: price ?? 0, listPrice, imageUrl };
}

/**
 * Busca dados do produto na URL (Amazon ou Mercado Livre).
 * Retorna dados para preencher ProductInput; falha se não conseguir título ou preço.
 */
export async function scrapeProductFromUrl(url: string): Promise<ScrapedProduct> {
  const normalized = url.trim();
  if (!normalized.startsWith("http")) throw new Error("URL inválida.");

  const res = await fetch(normalized, {
    headers: {
      "User-Agent": BROWSER_UA,
      Accept: "text/html,application/xhtml+xml",
      "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    },
    redirect: "follow",
  });

  if (!res.ok) throw new Error(`Falha ao acessar a página (${res.status}). Tente novamente.`);
  const html = await res.text();

  const $ = cheerio.load(html);
  const ogTitle = $('meta[property="og:title"]').attr("content")?.trim() ?? "";
  const ogImage = $('meta[property="og:image"]').attr("content")?.trim() ?? "";
  const ogUrl = $('meta[property="og:url"]').attr("content")?.trim() || normalized;

  let title: string;
  let price: number;
  let listPrice: number | null = null;
  let imageUrl: string | null = null;

  if (isMercadoLivreUrl(normalized)) {
    const ml = extractMercadoLivreFromHtml($, html);
    title = (ml.title || ogTitle).slice(0, 500);
    price = ml.price;
    listPrice = ml.listPrice;
    imageUrl = ml.imageUrl || ogImage || null;
  } else {
    // Amazon ou genérico
    title =
      $("#productTitle").text().trim() ||
      $("#title").text().trim() ||
      ogTitle ||
      $("h1#title").text().trim() ||
      "";
    title = title.slice(0, 500);

    let result = extractPriceFromHtml($);
    price = result.price;
    listPrice = result.listPrice;
    if (price <= 0) {
      const fromJson = extractPriceFromPageJson(html);
      if (fromJson) {
        price = fromJson.price;
        listPrice = fromJson.listPrice ?? listPrice;
      }
    }
    if (price <= 0) {
      const fromLd = extractFromJsonLd(html);
      if (fromLd?.price) price = fromLd.price as number;
    }
    imageUrl = ogImage || $("#landingImage").attr("src") || $("#imgBlkFront").attr("src") || null;
  }

  if (!title) throw new Error("Não foi possível obter o título do produto.");
  if (price <= 0) throw new Error("Não foi possível obter o preço. A página pode ser dinâmica (JavaScript).");

  let affiliateLink = ogUrl || normalized;
  if (isAmazonUrl(normalized)) affiliateLink = withPartnerTag(affiliateLink);

  const previousPrice = listPrice != null && listPrice > price ? listPrice : null;
  const discountPct =
    previousPrice && previousPrice > 0 ? Math.round(((previousPrice - price) / previousPrice) * 100) : null;

  logger.info({ url: normalized, title: title.slice(0, 60), price }, "Scrape product from URL");

  return {
    title,
    price,
    previousPrice: previousPrice ?? null,
    discountPct,
    imageUrl,
    affiliateLink,
    rawUrl: normalized,
  };
}

/** Converte resultado do scrape para ProductInput (opcional: salvar no banco). */
export function scrapedToProductInput(scraped: ScrapedProduct, categoryId?: string | null): ProductInput {
  return {
    title: scraped.title,
    price: scraped.price,
    previousPrice: scraped.previousPrice,
    discountPct: scraped.discountPct,
    affiliateLink: scraped.affiliateLink,
    imageUrl: scraped.imageUrl,
    source: "amazon",
    categoryId,
  };
}
