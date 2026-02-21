/**
 * Captura de ofertas Amazon.
 * - Com API (Product Advertising API): use AMAZON_ACCESS_KEY + SECRET + PARTNER_TAG.
 * - Sem API: scraping controlado (implementar com Playwright/Puppeteer conforme ToS).
 * Este módulo expõe a interface; implementação API ou scraping pode ser preenchida.
 */
import { env } from "../../config/env.js";
import { logger } from "../../config/logger.js";
import type { ProductInput, ProductCaptureResult } from "./types.js";

const PARTNER_TAG = env.AMAZON_PARTNER_TAG ?? "";

/**
 * Busca ofertas na Amazon (placeholder: retorna vazio ou mock).
 * Substitua por:
 * - Chamada à Product Advertising API (paapi5) se tiver acesso aprovado.
 * - Ou scraping ético com delay e cache (playwright).
 */
export async function captureAmazonDeals(categorySlug?: string): Promise<ProductCaptureResult> {
  if (!PARTNER_TAG && !env.AMAZON_ACCESS_KEY) {
    logger.warn("Amazon: AMAZON_PARTNER_TAG ou API não configurado. Retornando vazio.");
    return { products: [], total: 0, source: "amazon" };
  }

  // TODO: integrar Product Advertising API (paapi5) ou módulo de scraping
  // Exemplo API: SearchItemsRequest -> items -> ItemInfo, Offers, Images
  const products: ProductInput[] = [];

  logger.info({ category: categorySlug, count: products.length }, "Amazon capture");
  return { products, total: products.length, source: "amazon" };
}

/**
 * Converte item da API Amazon (ou objeto de scraping) para ProductInput.
 * Use quando tiver resposta real da API/scraping.
 */
export function mapAmazonItemToProduct(item: Record<string, unknown>): ProductInput | null {
  const title = String(item.title ?? item.Title ?? "").trim();
  const link = String(item.link ?? item.AffiliateLink ?? "").trim();
  const image = String(item.image ?? item.ImageUrl ?? "").trim();
  const price = Number(item.price ?? item.Price ?? 0);
  const listPrice = Number(item.listPrice ?? item.PreviousPrice ?? item.ListPrice ?? 0);

  if (!title || !link || price <= 0) return null;

  const previousPrice = listPrice > price ? listPrice : null;
  const discountPct =
    previousPrice && previousPrice > 0
      ? Math.round(((previousPrice - price) / previousPrice) * 100)
      : null;

  return {
    title: title.slice(0, 500),
    price,
    previousPrice: previousPrice || null,
    discountPct,
    affiliateLink: link,
    imageUrl: image || null,
    externalId: String(item.asin ?? item.id ?? "").trim() || undefined,
    source: "amazon",
  };
}
