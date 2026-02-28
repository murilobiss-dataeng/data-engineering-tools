export type ProductInput = {
  title: string;
  price: number;
  previousPrice: number | null;
  discountPct: number | null;
  affiliateLink: string;
  imageUrl: string | null;
  externalId?: string;
  source?: string;
  categoryId?: string | null;
  installments?: string | null;
};

export type ProductCaptureResult = {
  products: ProductInput[];
  total: number;
  source: string;
};
