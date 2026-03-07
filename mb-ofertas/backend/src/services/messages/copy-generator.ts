/**
 * Geração de copy persuasiva para WhatsApp: gatilhos (escassez, urgência, benefício), emojis moderados.
 */
import type { ProductInput } from "../products/types.js";

const EMOJIS = {
  fire: "🔥",
  money: "💰",
  arrow: "👉",
  tag: "🏷️",
  clock: "⏰",
  check: "✅",
} as const;

function formatPrice(value: number): string {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);
}

/**
 * Gera mensagem de oferta para WhatsApp com:
 * - Título chamativo
 * - Preço de/por (desconto se houver)
 * - Gatilhos: urgência, benefício, escassez
 * - Link de afiliado
 * - Emojis moderados
 */
export function generateOfferMessage(product: ProductInput, options?: { shortLink?: string }): string {
  const link = options?.shortLink ?? product.affiliateLink;
  const lines: string[] = [];

  lines.push(`${EMOJIS.fire} OFERTA DO DIA`);
  lines.push("");
  lines.push(product.title);
  lines.push("");

  if (product.previousPrice != null && product.previousPrice > product.price) {
    lines.push(`${EMOJIS.money} De: ${formatPrice(product.previousPrice)} por ${formatPrice(product.price)}`);
    if (product.discountPct != null && product.discountPct > 0) {
      lines.push(`${EMOJIS.tag} ${product.discountPct}% OFF`);
    }
  } else {
    lines.push(`${EMOJIS.money} ${formatPrice(product.price)}`);
  }

  if (product.installments?.trim()) {
    lines.push(product.installments.trim());
  }

  lines.push("");
  lines.push("⏰ Oferta por tempo limitado. Aproveite!");
  lines.push("");
  lines.push(`${EMOJIS.arrow} ${link}`);
  lines.push("");
  lines.push("⚠️ Valores e disponibilidade podem variar.");

  return lines.join("\n");
}

/**
 * Variação com mais urgência (para broadcast).
 */
export function generateUrgentOfferMessage(product: ProductInput, shortLink?: string): string {
  const base = generateOfferMessage(product, { shortLink });
  const header = `${EMOJIS.fire} OFERTA DO DIA ${EMOJIS.fire}\n`;
  return header + base.replace(`${EMOJIS.fire} OFERTA DO DIA`, "").trim();
}

/**
 * Conteúdo pronto para post (rede social / WhatsApp): texto + URL da imagem.
 * options.coupon: se preenchido, inclui linha "CUPOM: XXX" em maiúsculas.
 */
export function generatePostContent(
  product: ProductInput,
  options?: { shortLink?: string; coupon?: string }
): { text: string; imageUrl: string | null } {
  const link = options?.shortLink ?? product.affiliateLink;
  const lines: string[] = [];

  lines.push(`${EMOJIS.fire} OFERTA DO DIA`);
  lines.push("");
  lines.push(product.title);
  lines.push("");

  if (product.previousPrice != null && product.previousPrice > product.price) {
    lines.push(`${EMOJIS.money} De: ${formatPrice(product.previousPrice)} por ${formatPrice(product.price)}`);
    if (product.discountPct != null && product.discountPct > 0) {
      lines.push(`${EMOJIS.tag} ${product.discountPct}% OFF`);
    }
  } else {
    lines.push(`${EMOJIS.money} ${formatPrice(product.price)}`);
  }

  if (product.installments?.trim()) {
    lines.push(`${product.installments.trim()}`);
  }

  if (options?.coupon?.trim()) {
    lines.push(`CUPOM: ${options.coupon.trim().toUpperCase()}`);
  }

  lines.push("");
  lines.push("⏰ Oferta por tempo limitado. Aproveite!");
  lines.push("");
  lines.push(`${EMOJIS.arrow} ${link}`);
  lines.push("");
  lines.push("⚠️ Valores e disponibilidade podem variar.");

  return { text: lines.join("\n"), imageUrl: product.imageUrl ?? null };
}
