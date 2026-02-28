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
  installments: string | null;
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

/** Retorna true se o nó ou pais próximos indicam "preço por litro/kg" (não é o preço do produto). */
function isPerUnitOrPerLiter($: cheerio.CheerioAPI, el: { closest: (s: string) => { length: number; text: () => string }; text: () => string }): boolean {
  const block = el.closest("#corePrice_feature_div, #apex_desktop, .a-section, #twisterContainer");
  const text = (block.length ? block : el).text().toLowerCase();
  return (
    /por\s*litro|por\s*kg|por\s*100\s*g|por\s*unidade\s*\(|preço\s*por\s*litro|preço\s*por\s*kg/i.test(text) &&
    !/preço\s*por\s*unidade\s*[R$]|cada\s*unidade\s*[R$]/i.test(text)
  );
}

/** Tenta extrair preço do HTML (Amazon BR/global). Evita preço "por litro/kg". */
function extractPriceFromHtml($: cheerio.CheerioAPI): { price: number; listPrice: number | null } {
  let price: number | null = null;
  let listPrice: number | null = null;

  // Preço atual: priorizar blocos que são claramente o preço de compra (não por litro)
  const selectors = [
    "#corePrice_feature_div .a-offscreen",
    "#corePriceDisplay_desktop_feature_div .a-offscreen",
    ".priceToPay .a-offscreen",
    ".a-price .a-offscreen",
    "span.a-price .a-offscreen",
    "#priceblock_ourprice",
    "#priceblock_dealprice",
    "#priceblock_saleprice",
    '[data-a-color="price"] .a-offscreen',
    "#apex_desktop .a-offscreen",
  ];
  for (const sel of selectors) {
    const el = $(sel).first();
    if (el.length) {
      if (isPerUnitOrPerLiter($, el)) continue;
      const text = el.text().trim();
      const p = parsePrice(text);
      if (p != null && p > 0 && p < 100000) {
        price = p;
        break;
      }
    }
  }

  // Preço de lista (riscado) — evitar blocos "por litro"
  const listSelectors = [
    ".a-price.a-text-price .a-offscreen",
    "#priceblock_retailprice",
    ".basisPrice .a-offscreen",
    ".a-text-price.a-offscreen",
  ];
  for (const sel of listSelectors) {
    const el = $(sel).first();
    if (el.length) {
      if (isPerUnitOrPerLiter($, el)) continue;
      const text = el.text().trim();
      const p = parsePrice(text);
      if (p != null && p > 0 && p < 100000 && (price == null || p > price)) {
        listPrice = p;
        break;
      }
    }
  }

  // Fallback: busca por padrão "R$ X,XX" no HTML (evitar valores absurdos tipo 102 quando é "por litro")
  if (price == null) {
    const body = $.html();
    const priceMatch = body.match(/R\$\s*[\d.,]+|[\d.,]+\s*R\$|"amount"\s*:\s*([\d.]+)/);
    if (priceMatch) {
      const raw = priceMatch[1] ? priceMatch[1] : priceMatch[0];
      const p = parsePrice(raw);
      if (p != null && p > 0 && p < 100000) price = p;
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

/** Busca JSON de estado da página (Amazon). priceToPay = preço real de compra (não por litro). */
function extractPriceFromPageJson(html: string): { price: number; listPrice?: number } | null {
  // priceToPay = preço que o cliente paga (evita confusão com "por litro")
  const priceToPayMatch = html.match(/priceToPay["\s]*:["\s]*\{[^}]*"amount"["\s]*:["\s]*([\d.]+)/);
  if (priceToPayMatch) {
    const p = parseFloat(priceToPayMatch[1]);
    if (Number.isFinite(p) && p > 0 && p < 1000000) {
      let listPrice: number | undefined;
      const listMatch = html.match(/basisPrice["\s]*:["\s]*\{[^}]*"amount"["\s]*:["\s]*([\d.]+)/);
      if (listMatch) {
        const lp = parseFloat(listMatch[1]);
        if (Number.isFinite(lp) && lp > p) listPrice = lp;
      }
      return { price: p, listPrice };
    }
  }
  const amountMatch = html.match(/"amount":\s*([\d.]+)/);
  if (amountMatch) {
    const p = parseFloat(amountMatch[1]);
    if (Number.isFinite(p) && p > 0 && p < 1000000) return { price: p };
  }
  return null;
}

/** Extrai texto de parcelamento (ex.: "em 12x de R$ 25,00 sem juros"). */
function extractInstallmentsAmazon($: cheerio.CheerioAPI, html: string): string | null {
  const selectors = [
    "#installmentCalculatorFeature .a-text-bold",
    ".installmentPrice",
    "[data-cel-widget*='installment']",
    ".a-section .a-size-base.a-color-secondary",
  ];
  for (const sel of selectors) {
    const el = $(sel).first();
    if (el.length) {
      const text = el.text().trim();
      const m = text.match(/em\s*\d+x\s*(?:de\s*)?R\$\s*[\d.,]+(?:\s*sem\s*juros)?/i) || text.match(/\d+x\s*de\s*R\$\s*[\d.,]+/i);
      if (m && m[0].length > 5) return m[0].trim();
    }
  }
  const match = html.match(/(?:em\s*)?(\d+x)\s*de\s*R\$\s*[\d.,]+(?:\s*sem\s*juros)?/i);
  return match ? (match[0].startsWith("em") ? match[0] : `em ${match[0]}`).trim() : null;
}

/** Extrai parcelamento Mercado Livre. */
function extractInstallmentsML($: cheerio.CheerioAPI): string | null {
  const sel = [
    ".ui-pdp-payment__title",
    ".ui-pdp-installments",
    "[data-testid='installment-option']",
    ".cf-installments",
  ];
  for (const s of sel) {
    const text = $(s).first().text().trim();
    const m = text.match(/em\s*\d+x\s*(?:de\s*)?R\$\s*[\d.,]+(?:\s*sem\s*juros)?/i) || text.match(/\d+x\s*de\s*R\$\s*[\d.,]+/i);
    if (m && m[0].length > 5) return m[0].trim();
  }
  return null;
}

/** Extrai título, preço e imagem da página do Mercado Livre. */
function extractMercadoLivreFromHtml(
  $: cheerio.CheerioAPI,
  html: string
): { title: string; price: number; listPrice: number | null; imageUrl: string | null; installments: string | null } {
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

  // Preço original (riscado) — ML: várias classes possíveis
  const listSelectors = [
    ".ui-pdp-price--original .andes-money-amount__fraction",
    ".andes-money-amount--previous .andes-money-amount__fraction",
    ".andes-money-amount--previous",
    ".ui-pdp-price__original-value",
    '[data-testid="original-price"] .andes-money-amount__fraction',
  ];
  for (const sel of listSelectors) {
    const el = $(sel).first();
    if (el.length) {
      const text = el.text().trim();
      const p = parsePrice(text);
      if (p != null && p > 0 && (price == null || p > price)) listPrice = p;
      if (listPrice != null) break;
    }
  }

  // Fallback preço atual e original no JSON (ML: __PRELOADED_STATE__, window.__PRELOADED_STATE__, etc.)
  const jsonPriceMatch = html.match(/"price":\s*([\d.]+)/);
  const jsonOriginalMatch = html.match(/"original_price":\s*([\d.]+)|"list_price":\s*([\d.]+)|"prices"\s*:\s*\{[^}]*"original"\s*:\s*([\d.]+)/);
  if (jsonPriceMatch && price == null) {
    const p = parseFloat(jsonPriceMatch[1]);
    if (p > 0 && p < 1000000) price = p;
  }
  if (jsonOriginalMatch && listPrice == null) {
    const raw = jsonOriginalMatch[1] ?? jsonOriginalMatch[2] ?? jsonOriginalMatch[3];
    if (raw) {
      const p = parseFloat(raw);
      if (p > 0 && p < 1000000 && (price == null || p > price)) listPrice = p;
    }
  }
  if (price == null) {
    const priceInJson = html.match(/"amount":\s*([\d.]+)/g);
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

  const installments = extractInstallmentsML($);
  return { title, price: price ?? 0, listPrice, imageUrl, installments };
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
  let price: number = 0;
  let listPrice: number | null = null;
  let imageUrl: string | null = null;
  let installments: string | null = null;

  if (isMercadoLivreUrl(normalized)) {
    const ml = extractMercadoLivreFromHtml($, html);
    title = (ml.title || ogTitle).slice(0, 500);
    price = ml.price;
    listPrice = ml.listPrice;
    imageUrl = ml.imageUrl || ogImage || null;
    installments = ml.installments;
  } else {
    // Amazon: priorizar priceToPay do JSON (preço real de compra, não "por litro")
    title =
      $("#productTitle").text().trim() ||
      $("#title").text().trim() ||
      ogTitle ||
      $("h1#title").text().trim() ||
      "";
    title = title.slice(0, 500);

    const fromJson = extractPriceFromPageJson(html);
    if (fromJson) {
      price = fromJson.price;
      listPrice = fromJson.listPrice ?? listPrice;
    }
    if (price <= 0) {
      const result = extractPriceFromHtml($);
      price = result.price;
      listPrice = result.listPrice ?? listPrice;
    }
    if (price <= 0) {
      const fromLd = extractFromJsonLd(html);
      if (fromLd?.price) price = fromLd.price as number;
    }
    imageUrl = ogImage || $("#landingImage").attr("src") || $("#imgBlkFront").attr("src") || null;
    installments = extractInstallmentsAmazon($, html);
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
    installments,
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
    installments: scraped.installments ?? undefined,
    source: "amazon",
    categoryId,
  };
}
