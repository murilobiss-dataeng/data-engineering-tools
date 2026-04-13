import * as campaignsRepo from "../../repositories/campaigns.repository.js";
import * as productsRepo from "../../repositories/products.repository.js";
import * as shortLinksRepo from "../../repositories/short-links.repository.js";
import { generateOfferMessage } from "../messages/copy-generator.js";
import type { ProductInput } from "../products/types.js";

function normalizeProductPrices(p: ProductInput): ProductInput {
  const prev = p.previousPrice ?? null;
  const curr = p.price;
  if (prev != null && prev > 0 && curr > 0 && prev < curr) {
    return {
      ...p,
      price: prev,
      previousPrice: curr,
      discountPct: Math.round(((curr - prev) / curr) * 100),
    };
  }
  return p;
}

/** Base URL opcional para link curto (ex.: frontend envia X-Short-Link-Base). */
export async function getCampaignWhatsAppMessage(
  campaignId: string,
  options?: { shortLinkBaseUrl?: string }
): Promise<string> {
  const campaign = await campaignsRepo.getCampaignById(campaignId);
  if (!campaign) throw new Error("Campanha não encontrada");
  const productIds = (campaign.product_ids as string[]) ?? [];
  const products = await Promise.all(
    productIds.map((id) => productsRepo.getProductById(id))
  ).then((rows) => rows.filter(Boolean));
  const lines: string[] = [];
  for (const row of products) {
    let p: ProductInput = {
      title: row.title,
      price: parseFloat(row.price),
      previousPrice: row.previous_price ? parseFloat(row.previous_price) : null,
      discountPct: row.discount_pct != null ? parseFloat(row.discount_pct) : null,
      affiliateLink: row.affiliate_link,
      imageUrl: row.image_url,
      installments: row.installments ?? undefined,
      installmentMaxTimes:
        row.installment_max_times != null ? Number(row.installment_max_times) : null,
      installmentUnitPrice:
        row.installment_unit_price != null ? parseFloat(String(row.installment_unit_price)) : null,
    };
    p = normalizeProductPrices(p);
    const short = await shortLinksRepo.createShortLink(row.affiliate_link, options?.shortLinkBaseUrl, row.id);
    lines.push(generateOfferMessage(p, { shortLink: short.shortUrl }));
  }
  return lines.join("\n\n——\n\n");
}
