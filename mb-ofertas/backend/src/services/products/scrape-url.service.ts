/**
 * Extrai dados de produto a partir de uma URL (Amazon, Mercado Livre ou Shopee).
 * Usa fetch + Cheerio; sem API oficial. Para uso ético (delay, cache, ToS).
 */
import * as cheerio from "cheerio";
import { logger } from "../../config/logger.js";
import { env } from "../../config/env.js";
import type { ProductInput } from "./types.js";

const PARTNER_TAG = env.AMAZON_PARTNER_TAG ?? "";

const BROWSER_UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";

export type PriceCandidate = { code: string; value: number };

export type ScrapedProduct = {
  title: string;
  price: number;
  previousPrice: number | null;
  discountPct: number | null;
  imageUrl: string | null;
  affiliateLink: string;
  rawUrl: string;
  installments: string | null;
  /** ID externo (ASIN, MLB..., etc.) para evitar duplicatas. */
  externalId?: string | null;
  /** Todos os preços encontrados na página, com código da origem (para você indicar qual está correto). */
  priceCandidates?: { source: "amazon" | "mercadolivre" | "shopee"; candidates: PriceCandidate[] };
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

/** URLs do ML que são tracking/redirect/ofertas, não página de produto. */
function isMercadoLivreNonProductUrl(url: string): boolean {
  try {
    const u = new URL(url);
    const host = u.hostname.toLowerCase();
    return /^click\d*\.(mercadolivre|mercadolibre)/i.test(host) || /^(tracking|redirect|auth)\.(mercadolivre|mercadolibre)/i.test(host) || /\/mclics\/clicks\//i.test(u.pathname);
  } catch {
    return false;
  }
}

function isShopeeUrl(url: string): boolean {
  try {
    const u = new URL(url);
    const host = u.hostname.replace(/^www\./, "").toLowerCase();
    return host === "shopee.com.br" || host === "shopee.br" || host.endsWith(".shopee.com.br");
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

/** Extrai link curto amzn.to do HTML (Amazon não oferece API para criar; usamos se a página tiver). */
function extractAmznShortLink(html: string): string | null {
  const m = html.match(/https?:\/\/amzn\.to\/[a-zA-Z0-9]+/i) || html.match(/"amzn\.to\/[a-zA-Z0-9]+"/i);
  if (m) {
    const raw = m[0].replace(/^"|"$/g, "");
    return raw.startsWith("http") ? raw : `https://${raw}`;
  }
  return null;
}

/** Extrai ID externo da URL para evitar duplicatas (Amazon ASIN, ML item id, Shopee item). */
function extractExternalIdFromUrl(url: string): string | null {
  try {
    const u = new URL(url);
    const path = u.pathname;
    const host = u.hostname.replace(/^www\./, "").toLowerCase();
    if (/^amazon\.(com|com\.br)/.test(host)) {
      const m = path.match(/\/(?:dp|gp\/product)\/([A-Z0-9]{10})/i);
      return m ? m[1].toUpperCase() : null;
    }
    if (host.includes("mercadolivre") || host.includes("mercadolibre")) {
      const m = path.match(/(ML[BUA]\d+)/i) || path.match(/\/([A-Z]{2,3}\d+)/);
      return m ? m[1].toUpperCase() : null;
    }
    if (host.includes("shopee")) {
      const m = path.match(/-i\.(\d+)\.(\d+)/);
      return m ? `shopee_${m[1]}_${m[2]}` : null;
    }
    return null;
  } catch {
    return null;
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

  let finalPrice = price ?? 0;
  let finalListPrice = listPrice;
  if (finalListPrice != null && finalPrice > 0 && finalListPrice < finalPrice) {
    const tmp = finalPrice;
    finalPrice = finalListPrice;
    finalListPrice = tmp;
  }
  return { price: finalPrice, listPrice: finalListPrice };
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
  let price: number | null = null;
  let listPrice: number | undefined;
  if (priceToPayMatch) {
    const p = parseFloat(priceToPayMatch[1]);
    if (Number.isFinite(p) && p > 0 && p < 1000000) price = p;
  }
  if (price == null) {
    const amountMatch = html.match(/"amount":\s*([\d.]+)/);
    if (amountMatch) {
      const p = parseFloat(amountMatch[1]);
      if (Number.isFinite(p) && p > 0 && p < 1000000) price = p;
    }
  }
  // Preço de lista: basisPrice, savingsBasis, strikePrice, wasPrice, listPrice, regularPrice
  const listPatterns = [
    /basisPrice["\s]*:["\s]*\{[^}]*"amount"["\s]*:["\s]*([\d.]+)/,
    /savingsBasis["\s]*:["\s]*\{[^}]*"amount"["\s]*:["\s]*([\d.]+)/,
    /"strikePrice"["\s]*:["\s]*\{[^}]*"amount"["\s]*:["\s]*([\d.]+)/,
    /"wasPrice"["\s]*:["\s]*\{[^}]*"amount"["\s]*:["\s]*([\d.]+)/,
    /"listPrice"["\s]*:["\s]*\{[^}]*"amount"["\s]*:["\s]*([\d.]+)/,
    /"regularPrice"["\s]*:["\s]*\{[^}]*"amount"["\s]*:["\s]*([\d.]+)/,
  ];
  for (const re of listPatterns) {
    const m = html.match(re);
    if (m) {
      const lp = parseFloat(m[1]);
      if (Number.isFinite(lp) && lp > 0 && lp < 1000000 && (price == null || lp > price)) {
        listPrice = lp;
        break;
      }
    }
  }
  if (price == null) return null;
  let finalPrice = price;
  let finalListPrice = listPrice;
  if (finalListPrice != null && finalListPrice < finalPrice) {
    const tmp = finalPrice;
    finalPrice = finalListPrice;
    finalListPrice = tmp;
  }
  return { price: finalPrice, listPrice: finalListPrice };
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

/** Rejeita valor que parece ser contagem (opiniões, avaliações) e não preço. */
function mlLooksLikeCount(value: number, html: string): boolean {
  const s = String(Math.round(value));
  return new RegExp(`${s.replace(/\./g, "\\.")}\\s*(opiniões|avaliações|reviews)`).test(html);
}

/**
 * Extrai título, preço e imagem da página do Mercado Livre.
 * Regra: preço de VENDA = "price" ou "amount" (no contexto de preço). Preço CHEIO = "original_price"/"regular_amount".
 * Evita pegar "2612 opiniões" ou outros números que não são preço.
 */
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

  // —— 1) JSON no contexto de preço do produto: "price" + "original_price" (estrutura comum do ML) ——
  const priceThenOrig = html.match(/"price"\s*:\s*([\d.]+)[\s\S]{0,300}?"original_price"\s*:\s*([\d.]+)/);
  const origThenPrice = html.match(/"original_price"\s*:\s*([\d.]+)[\s\S]{0,300}?"price"\s*:\s*([\d.]+)/);
  if (priceThenOrig) {
    let p = parseFloat(priceThenOrig[1]);
    let orig = parseFloat(priceThenOrig[2]);
    if (p > 10000 && p < 100000000) p = p / 100;
    if (orig > 10000 && orig < 100000000) orig = orig / 100;
    if (p > 0 && p < 10000000 && !mlLooksLikeCount(p, html)) {
      price = p;
      if (orig > p) listPrice = orig;
    }
  } else if (origThenPrice) {
    let orig = parseFloat(origThenPrice[1]);
    let p = parseFloat(origThenPrice[2]);
    if (orig > 10000 && orig < 100000000) orig = orig / 100;
    if (p > 10000 && p < 100000000) p = p / 100;
    if (p > 0 && p < 10000000 && !mlLooksLikeCount(p, html)) {
      price = p;
      if (orig > p) listPrice = orig;
    }
  }

  // —— 2) JSON: "amount" + "regular_amount" no mesmo bloco (preço em centavos quando > 10000) ——
  if (price == null) {
    const mlAmountThenReg = html.match(/"amount"\s*:\s*([\d.]+)[\s\S]{0,400}?"regular_amount"\s*:\s*([\d.]+)/);
    const mlRegThenAmount = html.match(/"regular_amount"\s*:\s*([\d.]+)[\s\S]{0,400}?"amount"\s*:\s*([\d.]+)/);
    if (mlAmountThenReg) {
      let saleV = parseFloat(mlAmountThenReg[1]);
      if (saleV > 10000 && saleV < 100000000) saleV = saleV / 100;
      let regV = parseFloat(mlAmountThenReg[2]);
      if (regV > 10000 && regV < 100000000) regV = regV / 100;
      if (saleV > 0 && saleV < 10000000 && !mlLooksLikeCount(saleV, html)) {
        price = saleV;
        if (regV > saleV) listPrice = regV;
      }
    } else if (mlRegThenAmount) {
      let regV = parseFloat(mlRegThenAmount[1]);
      if (regV > 10000 && regV < 100000000) regV = regV / 100;
      let saleV = parseFloat(mlRegThenAmount[2]);
      if (saleV > 10000 && saleV < 100000000) saleV = saleV / 100;
      if (saleV > 0 && saleV < 10000000 && !mlLooksLikeCount(saleV, html)) {
        price = saleV;
        if (regV > saleV) listPrice = regV;
      }
    }
  }
  // Não usar primeiro "amount" solto da página (pode ser "amount" de opiniões/avaliações)
  if (price == null) {
    const firstAmount = html.match(/"amount"\s*:\s*([\d.]+)(?=\s*[,}])/);
    if (firstAmount) {
      let v = parseFloat(firstAmount[1]);
      if (v > 10000 && v < 100000000) v = v / 100;
      if (v > 0 && v < 10000000 && !mlLooksLikeCount(v, html)) price = v;
    }
  }

  // —— 3) HTML: bloco principal (preço em destaque). Ignorar nós que contêm "opiniões"/"avaliações". ——
  if (price == null) {
    const mainPriceSelectors = [
      ".ui-pdp-price__main-container .andes-money-amount__fraction",
      ".ui-pdp-price:not(.ui-pdp-price--original) .andes-money-amount__fraction",
      '[data-testid="price"] .andes-money-amount__fraction',
      ".andes-money-amount--cents-superscript .andes-money-amount__fraction",
    ];
    for (const sel of mainPriceSelectors) {
      const el = $(sel).first();
      if (el.length) {
        const text = el.text().trim();
        if (/opiniões|avaliações|reviews/i.test(text)) continue;
        const p = parsePrice(text);
        if (p != null && p > 0 && p < 1000000 && !mlLooksLikeCount(p, html)) {
          price = p;
          break;
        }
      }
    }
  }
  if (price == null) {
    const mainBlock = $(".ui-pdp-price__main-container").first();
    if (mainBlock.length) {
      const text = mainBlock.text().trim();
      if (!/opiniões|avaliações|reviews/i.test(text)) {
        const p = parsePrice(text);
        if (p != null && p > 0 && p < 1000000 && !mlLooksLikeCount(p, html)) price = p;
      }
    }
  }

  // —— 4) Preço CHEIO (só para listPrice): original_price, list_price, regular_amount, base_price. NUNCA usar como price. ——
  const origPriceMatch = html.match(/"original_price"\s*:\s*([\d.]+)/);
  if (origPriceMatch) {
    const p = parseFloat(origPriceMatch[1]);
    if (p > 0 && p < 10000000 && (price == null || p > price)) listPrice = p;
  }
  if (listPrice == null) {
    const listPriceMatch = html.match(/"list_price"\s*:\s*([\d.]+)/);
    if (listPriceMatch) {
      const p = parseFloat(listPriceMatch[1]);
      if (p > 0 && p < 10000000 && (price == null || p > price)) listPrice = p;
    }
  }
  if (listPrice == null) {
    const regAmountMatch = html.match(/"regular_amount"\s*:\s*([\d.]+)/);
    if (regAmountMatch) {
      let v = parseFloat(regAmountMatch[1]);
      if (v > 10000 && v < 100000000) v = v / 100;
      if (v > 0 && v < 10000000 && (price == null || v > price)) listPrice = v;
    }
  }
  if (listPrice == null) {
    const basePriceMatch = html.match(/"base_price"\s*:\s*([\d.]+)/);
    if (basePriceMatch) {
      let v = parseFloat(basePriceMatch[1]);
      if (v > 10000 && v < 100000000) v = v / 100;
      if (v > 0 && v < 10000000 && (price == null || v > price)) listPrice = v;
    }
  }
  if (listPrice == null) {
    const listSelectors = [
      ".ui-pdp-price--original .andes-money-amount__fraction",
      ".ui-pdp-price__original-value .andes-money-amount__fraction",
      '[data-testid="original-price"] .andes-money-amount__fraction',
    ];
    for (const sel of listSelectors) {
      const el = $(sel).first();
      if (el.length) {
        const p = parsePrice(el.text().trim());
        if (p != null && p > 0 && (price == null || p > price)) listPrice = p;
        if (listPrice != null) break;
      }
    }
  }

  // —— 5) Último recurso para price: "price" em JSON (evitar usar "amount" solto que pode ser opiniões). ——
  if (price == null) {
    const jsonPrice = html.match(/"price"\s*:\s*([\d.]+)/);
    if (jsonPrice) {
      let p = parseFloat(jsonPrice[1]);
      if (p > 10000 && p < 100000000) p = p / 100;
      if (p > 0 && p < 10000000 && (listPrice == null || p <= listPrice) && !mlLooksLikeCount(p, html)) price = p;
    }
  }

  // —— 6) Fallback: R$ X no HTML. Descartar valores que parecem contagem. ——
  if (price == null) {
    const reais = html.match(/R\$\s*[\d.,]+/g);
    if (reais && reais.length > 0) {
      const values = reais
        .map((r) => parsePrice(r))
        .filter((p): p is number => p != null && p > 0 && p < 100000 && !mlLooksLikeCount(p, html));
      if (values.length > 0) price = Math.min(...values);
    }
  }

  let imageUrl: string | null =
    $('.ui-pdp-image img[src*="http"]').first().attr("src") ||
    $('[data-zoom]').first().attr("data-zoom") ||
    $(".ui-pdp-image__source").first().attr("src") ||
    null;

  const installments = extractInstallmentsML($);
  let finalPrice = price ?? 0;
  let finalListPrice = listPrice;
  if (finalListPrice != null && finalPrice > 0 && finalListPrice < finalPrice) {
    const swap = finalPrice;
    finalPrice = finalListPrice;
    finalListPrice = swap;
  }
  return { title, price: finalPrice, listPrice: finalListPrice, imageUrl, installments };
}

/** Extrai título, preço e imagem da página da Shopee (og + JSON embutido quando disponível). */
function extractShopeeFromHtml(
  $: cheerio.CheerioAPI,
  html: string
): { title: string; price: number; listPrice: number | null; imageUrl: string | null; installments: string | null } {
  const ogTitle = $('meta[property="og:title"]').attr("content")?.trim() ?? "";
  let title =
    $(".shopee-product-info__header__text").first().text().trim() ||
    $("[data-sqe='name']").first().text().trim() ||
    $("h1").first().text().trim() ||
    ogTitle ||
    "";

  let price: number | null = null;
  let listPrice: number | null = null;

  const saleMatch = html.match(/"sale_price"\s*:\s*([\d.]+)|"min_price"\s*:\s*([\d.]+)/);
  if (saleMatch) {
    const raw = saleMatch[1] ?? saleMatch[2];
    if (raw) {
      const p = parseFloat(raw);
      if (p > 0 && p < 10000000) price = p;
    }
  }
  if (price == null) {
    const priceMatch = html.match(/"price"\s*:\s*([\d.]+)/);
    if (priceMatch) {
      const p = parseFloat(priceMatch[1]);
      if (p > 0 && p < 10000000) price = p;
    }
  }
  const listMatch = html.match(/"price_before_discount"\s*:\s*([\d.]+)|"original_price"\s*:\s*([\d.]+)/);
  if (listMatch && listPrice == null) {
    const raw = listMatch[1] ?? listMatch[2];
    if (raw) {
      const p = parseFloat(raw);
      if (p > 0 && p < 10000000 && (price == null || p > price)) listPrice = p;
    }
  }
  if (price == null) {
    const reais = html.match(/R\$\s*[\d.,]+/g);
    if (reais && reais.length > 0) {
      const p = parsePrice(reais[0]);
      if (p != null && p > 0) price = p;
    }
  }
  const priceText = $(".shopee-product-info__price__current, [data-sqe='price'], .pqTWkA").first().text().trim();
  if (price == null && priceText) {
    const p = parsePrice(priceText);
    if (p != null && p > 0) price = p;
  }

  const ogImage = $('meta[property="og:image"]').attr("content")?.trim() ?? null;
  const imageUrl =
    $(".shopee-product-info__images img").first().attr("src") ||
    $("[data-sqe='image'] img").first().attr("src") ||
    ogImage ||
    null;

  let finalPrice = price ?? 0;
  let finalListPrice = listPrice;
  if (finalListPrice != null && finalPrice > 0 && finalListPrice < finalPrice) {
    const tmp = finalPrice;
    finalPrice = finalListPrice;
    finalListPrice = tmp;
  }
  return { title, price: finalPrice, listPrice: finalListPrice, imageUrl, installments: null };
}

/** Coleta TODOS os preços encontrados na página Amazon com código da origem (para debug). */
function collectAmazonPriceCandidates(html: string, $: cheerio.CheerioAPI): PriceCandidate[] {
  const candidates: PriceCandidate[] = [];
  const add = (code: string, value: number) => {
    if (Number.isFinite(value) && value > 0 && value < 1000000) candidates.push({ code, value });
  };

  const priceToPayM = html.match(/priceToPay["\s]*:["\s]*\{[^}]*"amount"["\s]*:["\s]*([\d.]+)/);
  if (priceToPayM) add("amazon_json_priceToPay", parseFloat(priceToPayM[1]));

  const basisM = html.match(/basisPrice["\s]*:["\s]*\{[^}]*"amount"["\s]*:["\s]*([\d.]+)/);
  if (basisM) add("amazon_json_basisPrice", parseFloat(basisM[1]));

  ["savingsBasis", "strikePrice", "wasPrice", "listPrice", "regularPrice"].forEach((name) => {
    const re = new RegExp(`"${name}"["\\s]*:["\\s]*\\{[^}]*"amount"["\\s]*:["\\s]*([\\d.]+)`);
    const m = html.match(re);
    if (m) add(`amazon_json_${name}`, parseFloat(m[1]));
  });

  const amountM = html.match(/"amount":\s*([\d.]+)/);
  if (amountM) add("amazon_json_amount_first", parseFloat(amountM[1]));

  const htmlSelectorsPrice = [
    "#corePrice_feature_div .a-offscreen",
    ".priceToPay .a-offscreen",
    "#corePriceDisplay_desktop_feature_div .a-offscreen",
    ".a-price .a-offscreen",
    "#priceblock_ourprice",
    "#priceblock_dealprice",
    "#priceblock_saleprice",
    "#priceblock_retailprice",
    ".a-price.a-text-price .a-offscreen",
    ".basisPrice .a-offscreen",
  ];
  for (const sel of htmlSelectorsPrice) {
    const el = $(sel).first();
    if (el.length && !isPerUnitOrPerLiter($, el)) {
      const p = parsePrice(el.text().trim());
      if (p != null && p > 0) add(`amazon_html_${sel.replace(/\s+/g, "_").slice(0, 40)}`, p);
    }
  }

  return candidates;
}

/** Coleta TODOS os preços encontrados na página Mercado Livre com código da origem (para debug). */
function collectMLPriceCandidates($: cheerio.CheerioAPI, html: string): PriceCandidate[] {
  const candidates: PriceCandidate[] = [];
  const add = (code: string, value: number) => {
    if (Number.isFinite(value) && value > 0 && value < 10000000) candidates.push({ code, value });
  };

  const priceSelectors = [
    ".ui-pdp-price__main-container",
    ".ui-pdp-price .andes-money-amount",
    ".ui-pdp-price",
    '[data-testid="price"]',
    ".andes-money-amount--cents-superscript",
    ".ui-pdp-price--original .andes-money-amount__fraction",
    ".ui-pdp-price__original-value .andes-money-amount__fraction",
    ".andes-money-amount--previous .andes-money-amount__fraction",
    ".ui-pdp-price__second-line",
    ".ui-pdp-price--secondary .andes-money-amount__fraction",
  ];
  for (const sel of priceSelectors) {
    const text = $(sel).first().text().trim();
    const p = parsePrice(text);
    if (p != null && p > 0) add(`ml_html_${sel.replace(/\s+/g, "_").slice(0, 35)}`, p);
  }

  const jsonCodes = [
    ["price", /"price":\s*([\d.]+)/],
    ["amount", /"amount":\s*([\d.]+)(?=\s*[,}])/],
    ["regular_amount", /"regular_amount"\s*:\s*([\d.]+)/],
    ["original_price", /"original_price"\s*:\s*([\d.]+)/],
    ["list_price", /"list_price"\s*:\s*([\d.]+)/],
    ["base_price", /"base_price"\s*:\s*([\d.]+)/],
  ];
  for (const [name, re] of jsonCodes) {
    const m = html.match(re);
    if (m) {
      let v = parseFloat(m[1]);
      if (name === "regular_amount" && v > 10000 && v < 100000000) v = v / 100;
      if (v > 0) add(`ml_json_${name}`, v);
    }
  }

  return candidates;
}

/** Coleta TODOS os preços encontrados na página Shopee com código da origem (para debug). */
function collectShopeePriceCandidates($: cheerio.CheerioAPI, html: string): PriceCandidate[] {
  const candidates: PriceCandidate[] = [];
  const add = (code: string, value: number) => {
    if (Number.isFinite(value) && value > 0 && value < 10000000) candidates.push({ code, value });
  };

  const saleM = html.match(/"sale_price"\s*:\s*([\d.]+)/);
  if (saleM) add("shopee_json_sale_price", parseFloat(saleM[1]));
  const minM = html.match(/"min_price"\s*:\s*([\d.]+)/);
  if (minM) add("shopee_json_min_price", parseFloat(minM[1]));
  const priceM = html.match(/"price"\s*:\s*([\d.]+)/);
  if (priceM) add("shopee_json_price", parseFloat(priceM[1]));
  const beforeM = html.match(/"price_before_discount"\s*:\s*([\d.]+)/);
  if (beforeM) add("shopee_json_price_before_discount", parseFloat(beforeM[1]));
  const origM = html.match(/"original_price"\s*:\s*([\d.]+)/);
  if (origM) add("shopee_json_original_price", parseFloat(origM[1]));

  const priceText = $(".shopee-product-info__price__current, [data-sqe='price'], .pqTWkA").first().text().trim();
  const p = parsePrice(priceText);
  if (p != null && p > 0) add("shopee_html_price_current", p);

  return candidates;
}

/**
 * Busca dados do produto na URL (Amazon, Mercado Livre ou Shopee).
 * Retorna dados para preencher ProductInput; falha se não conseguir título ou preço.
 */
export async function scrapeProductFromUrl(url: string): Promise<ScrapedProduct> {
  const normalized = url.trim();
  if (!normalized.startsWith("http")) throw new Error("URL inválida.");
  if (isMercadoLivreNonProductUrl(normalized)) throw new Error("URL não é página de produto (tracking/ofertas).");

  const res = await fetch(normalized, {
    headers: {
      "User-Agent": BROWSER_UA,
      Accept: "text/html,application/xhtml+xml",
      "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    },
    redirect: "follow",
    cache: "no-store",
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
    title = (ml.title || ogTitle).trim().slice(0, 500);
    if (title === "Mercado Livre" || title === "Mercado Libre") title = "";
    if (!title && ogTitle.trim().length > 20 && !/^mercado\s+livre$/i.test(ogTitle.trim())) title = ogTitle.trim().slice(0, 500);
    if (!title) {
      try {
        const u = new URL(normalized);
        const pathMatch = u.pathname.match(/^\/([^/]+)(?:\/p\/|$)/);
        if (pathMatch && pathMatch[1].length > 5) {
          title = pathMatch[1].replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()).slice(0, 500);
        }
      } catch {
        // ignore
      }
    }
    price = ml.price;
    listPrice = ml.listPrice;
    imageUrl = ml.imageUrl || ogImage || null;
    installments = ml.installments;
    if (price <= 0) {
      const fromLd = extractFromJsonLd(html);
      if (fromLd?.price != null && Number(fromLd.price) > 0) price = Number(fromLd.price);
    }
    if (price <= 0) {
      const metaAmount = $('meta[property="product:price:amount"]').attr("content") ?? $('meta[property="og:product:price:amount"]').attr("content");
      if (metaAmount) {
        const p = parseFloat(metaAmount.replace(",", "."));
        if (Number.isFinite(p) && p > 0 && p < 10000000) price = p;
      }
    }
  } else if (isShopeeUrl(normalized)) {
    const shopee = extractShopeeFromHtml($, html);
    title = (shopee.title || ogTitle).trim().slice(0, 500);
    if (!title && ogTitle.trim().length > 10 && !/^shopee$/i.test(ogTitle.trim())) title = ogTitle.trim().slice(0, 500);
    price = shopee.price;
    listPrice = shopee.listPrice;
    imageUrl = shopee.imageUrl || ogImage || null;
    installments = shopee.installments;
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
  if (isAmazonUrl(normalized)) {
    const shortLink = extractAmznShortLink(html);
    if (shortLink) affiliateLink = shortLink;
    else affiliateLink = withPartnerTag(affiliateLink);
  }
  if (isShopeeUrl(normalized)) {
    affiliateLink = ogUrl || normalized;
  }

  // Garantir: price = preço novo (menor), previousPrice = preço cheio (riscado, maior)
  let previousPrice: number | null = null;
  if (listPrice != null && listPrice > price) {
    previousPrice = listPrice;
  } else if (listPrice != null && listPrice < price && listPrice > 0) {
    // Estavam trocados: listPrice era o promocional, price era o cheio
    const salePrice = listPrice;
    const fullPrice = price;
    price = salePrice;
    previousPrice = fullPrice;
  }

  const discountPct =
    previousPrice && previousPrice > 0 ? Math.round(((previousPrice - price) / previousPrice) * 100) : null;

  let priceCandidates: ScrapedProduct["priceCandidates"] | undefined;
  if (isAmazonUrl(normalized)) {
    const candidates = collectAmazonPriceCandidates(html, $);
    priceCandidates = { source: "amazon", candidates };
    logger.info(
      { source: "amazon", url: normalized.slice(0, 60), priceCandidates: candidates, chosen: { price, previousPrice } },
      "Preços encontrados (Amazon) — use os códigos para indicar qual é preço novo e qual é preço cheio"
    );
  } else if (isMercadoLivreUrl(normalized)) {
    const candidates = collectMLPriceCandidates($, html);
    priceCandidates = { source: "mercadolivre", candidates };
    logger.info(
      { source: "mercadolivre", url: normalized.slice(0, 60), priceCandidates: candidates, chosen: { price, previousPrice } },
      "Preços encontrados (Mercado Livre) — use os códigos para indicar qual é preço novo e qual é preço cheio"
    );
  } else if (isShopeeUrl(normalized)) {
    const candidates = collectShopeePriceCandidates($, html);
    priceCandidates = { source: "shopee", candidates };
    logger.info(
      { source: "shopee", url: normalized.slice(0, 60), priceCandidates: candidates, chosen: { price, previousPrice } },
      "Preços encontrados (Shopee) — use os códigos para indicar qual é preço novo e qual é preço cheio"
    );
  }

  const externalId = extractExternalIdFromUrl(normalized) ?? undefined;

  return {
    title,
    price,
    previousPrice: previousPrice ?? null,
    discountPct,
    imageUrl,
    affiliateLink,
    rawUrl: normalized,
    installments,
    priceCandidates,
    externalId,
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
    externalId: scraped.externalId ?? undefined,
    source: "amazon",
    categoryId,
  };
}
