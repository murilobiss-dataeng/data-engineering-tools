export type ProductInput = {
  title: string;
  /** Preço à vista (PIX / principal). */
  price: number;
  /** Preço cheio / "de" (riscado), quando houver promoção. */
  previousPrice: number | null;
  discountPct: number | null;
  affiliateLink: string;
  imageUrl: string | null;
  externalId?: string;
  source?: string;
  categoryId?: string | null;
  /** Texto livre do parcelamento (ex.: frase da loja). */
  installments?: string | null;
  /** Máximo de parcelas oferecido (ex.: 12). */
  installmentMaxTimes?: number | null;
  /** Valor de cada parcela nessa condição. */
  installmentUnitPrice?: number | null;
  /** Cupom para exibir na copy (WhatsApp). */
  coupon?: string | null;
};

export type ProductCaptureResult = {
  products: ProductInput[];
  total: number;
  source: string;
};
