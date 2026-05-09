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

/** Bloco de preços: cheio (se houver), valor à vista, valor parcelado (até Nx ou texto da loja). */
function appendPriceLines(lines: string[], product: ProductInput): void {
  const hasFull = product.previousPrice != null && product.previousPrice > product.price;
  if (hasFull) {
    lines.push(`Preço cheio: ${formatPrice(product.previousPrice!)}`);
  }
  lines.push(`Valor à vista: ${formatPrice(product.price)}`);

  const structured =
    product.installmentMaxTimes != null &&
    product.installmentMaxTimes > 0 &&
    product.installmentUnitPrice != null &&
    product.installmentUnitPrice > 0;

  if (structured) {
    lines.push(
      `Valor parcelado: até ${product.installmentMaxTimes}x de ${formatPrice(product.installmentUnitPrice!)}`
    );
  } else if (product.installments?.trim()) {
    lines.push(`Valor parcelado: ${product.installments.trim()}`);
  }

  if (hasFull && product.discountPct != null && product.discountPct > 0) {
    lines.push(`${product.discountPct}% OFF no valor à vista`);
  }
}

/** Link exibido na mensagem: curto quando a API passa (encurtador /r/...), senão o link de afiliado. */
function resolveDisplayLink(product: ProductInput, options?: { shortLink?: string }): string {
  const short = options?.shortLink?.trim();
  return short || product.affiliateLink;
}

function appendOfferLinkBlock(lines: string[], link: string): void {
  lines.push("");
  lines.push("Oferta por tempo limitado. Aproveite!");
  lines.push("");
  lines.push("Acesse na loja:");
  lines.push(link);
}

/**
 * Gera mensagem de oferta para WhatsApp com:
 * - Título, preço cheio / à vista / parcelas, link.
 * - Sem emojis para evitar desconfiguração em canais.
 */
export function generateOfferMessage(product: ProductInput, options?: { shortLink?: string }): string {
  const link = resolveDisplayLink(product, options);
  const lines: string[] = [];

  const hasFull = product.previousPrice != null && product.previousPrice > product.price;
  if (hasFull && product.discountPct != null && product.discountPct > 0) {
    lines.push("OFERTA COM DESCONTO");
    lines.push("");
  }

  lines.push(product.title);
  lines.push("");

  appendPriceLines(lines, product);

  if (product.coupon?.trim()) {
    lines.push(`CUPOM: ${product.coupon.trim().toUpperCase()}`);
  }

  appendOfferLinkBlock(lines, link);

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
  const link = resolveDisplayLink(product, options);
  const lines: string[] = [];

  const hasFullPost = product.previousPrice != null && product.previousPrice > product.price;
  if (hasFullPost && product.discountPct != null && product.discountPct > 0) {
    lines.push("OFERTA COM DESCONTO");
    lines.push("");
  }

  lines.push(product.title);
  lines.push("");

  appendPriceLines(lines, product);

  const couponText = (options?.coupon?.trim() || product.coupon?.trim() || "").trim();
  if (couponText) {
    lines.push(`CUPOM: ${couponText.toUpperCase()}`);
  }

  appendOfferLinkBlock(lines, link);

  return { text: lines.join("\n"), imageUrl: product.imageUrl ?? null };
}
