/**
 * Geração de copy persuasiva para WhatsApp: gatilhos (escassez, urgência, benefício).
 * Usa apenas texto/ASCII para evitar emojis desconfigurados em alguns canais.
 */
import type { ProductInput } from "../products/types.js";

function formatPrice(value: number): string {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);
}

/**
 * Gera mensagem de oferta para WhatsApp com:
 * - Título, preço de/por (desconto se houver), link direto (Amazon/ML).
 * - Sem emojis para evitar desconfiguração em canais.
 */
export function generateOfferMessage(product: ProductInput, options?: { shortLink?: string }): string {
  const useShortLink = process.env.USE_APP_SHORT_LINK === "true" || process.env.USE_APP_SHORT_LINK === "1";
  const link = useShortLink && options?.shortLink ? options.shortLink : product.affiliateLink;
  const lines: string[] = [];

  if (product.discountPct != null && product.discountPct > 0) {
    lines.push("OFERTA COM DESCONTO");
    lines.push("");
  }

  lines.push(product.title);
  lines.push("");

  if (product.previousPrice != null && product.previousPrice > product.price) {
    lines.push(`De: ${formatPrice(product.previousPrice)} por ${formatPrice(product.price)}`);
    if (product.discountPct != null && product.discountPct > 0) {
      lines.push(`${product.discountPct}% OFF`);
    }
  } else {
    lines.push(formatPrice(product.price));
  }

  if (product.installments?.trim()) {
    lines.push(product.installments.trim());
  }

  lines.push("");
  lines.push("Oferta por tempo limitado. Aproveite!");
  lines.push("");
  lines.push(link);

  return lines.join("\n");
}

/**
 * Variação com mais urgência (para broadcast).
 */
export function generateUrgentOfferMessage(product: ProductInput, shortLink?: string): string {
  return generateOfferMessage(product, { shortLink });
}

/**
 * Conteúdo pronto para post (rede social / WhatsApp): texto + URL da imagem.
 * options.coupon: se preenchido, inclui linha "CUPOM: XXX" em maiúsculas.
 */
export function generatePostContent(
  product: ProductInput,
  options?: { shortLink?: string; coupon?: string }
): { text: string; imageUrl: string | null } {
  const useShortLink = process.env.USE_APP_SHORT_LINK === "true" || process.env.USE_APP_SHORT_LINK === "1";
  const link = useShortLink && options?.shortLink ? options.shortLink : product.affiliateLink;
  const lines: string[] = [];

  if (product.discountPct != null && product.discountPct > 0) {
    lines.push("OFERTA COM DESCONTO");
    lines.push("");
  }

  lines.push(product.title);
  lines.push("");

  if (product.previousPrice != null && product.previousPrice > product.price) {
    lines.push(`De: ${formatPrice(product.previousPrice)} por ${formatPrice(product.price)}`);
    if (product.discountPct != null && product.discountPct > 0) {
      lines.push(`${product.discountPct}% OFF`);
    }
  } else {
    lines.push(formatPrice(product.price));
  }

  if (product.installments?.trim()) {
    lines.push(product.installments.trim());
  }

  if (options?.coupon?.trim()) {
    lines.push(`CUPOM: ${options.coupon.trim().toUpperCase()}`);
  }

  lines.push("");
  lines.push("Oferta por tempo limitado. Aproveite!");
  lines.push("");
  lines.push(link);

  return { text: lines.join("\n"), imageUrl: product.imageUrl ?? null };
}
