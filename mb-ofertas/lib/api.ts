const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";

/** Base URL para link curto (fallback para encurtar e esconder tag). Enviado no header quando disponível. */
function getShortLinkBaseUrl(): string {
  if (typeof window !== "undefined") {
    return (process.env.NEXT_PUBLIC_APP_URL || (window as Window & { __APP_URL?: string }).__APP_URL || window.location.origin).replace(/\/$/, "");
  }
  return (process.env.NEXT_PUBLIC_APP_URL || process.env.NEXT_PUBLIC_API_URL || "").replace(/\/$/, "");
}

export async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const base = getShortLinkBaseUrl();
  const headers: Record<string, string> = { "Content-Type": "application/json", ...(options?.headers as Record<string, string>) };
  if (base) headers["X-Short-Link-Base"] = base;
  const res = await fetch(`${API_URL}/api${path}`, {
    ...options,
    headers,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: res.statusText }));
    throw new Error((err as { error?: string }).error || "Erro na API");
  }
  return res.json() as Promise<T>;
}

export type Product = {
  id: string;
  category_id: string | null;
  category_name: string | null;
  category_slug: string | null;
  title: string;
  /** Preço à vista (principal). */
  price: string;
  /** Preço cheio / de (riscado). */
  previous_price: string | null;
  discount_pct: string | null;
  affiliate_link: string;
  image_url: string | null;
  source: string;
  status: string;
  created_at: string;
  installments: string | null;
  /** Máximo de parcelas (ex.: 12) quando extraído ou informado. */
  installment_max_times?: number | null;
  /** Valor de cada parcela. */
  installment_unit_price?: string | null;
};

export type Campaign = {
  id: string;
  name: string;
  status: string;
  scheduled_at: string | null;
  product_ids: string[];
  target_type: string;
  created_at: string;
};

export type Category = { id: string; name: string; slug: string };

/** Linha do painel /analytics (links curtos + cliques). */
export type ShortLinkAnalytics = {
  code: string;
  long_url: string;
  short_url_path: string;
  click_count: number;
  last_clicked_at: string | null;
  created_at: string;
  product_title: string | null;
  category_slug: string | null;
};

export type WhatsAppChannel = {
  id: string;
  name: string;
  phone: string;
  channel_link: string | null;
  /** Slug da categoria de ofertas (mesmo do CHANNEL_SLUG no GitHub Actions) */
  category_slug: string | null;
  created_at: string;
};

export type WhatsAppScheduled = {
  id: string;
  channel_id: string;
  message: string;
  scheduled_at: string;
  status: string;
  opened_at: string | null;
  created_at: string;
  channel_name?: string;
  channel_phone?: string;
};

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
  installmentMaxTimes?: number | null;
  installmentUnitPrice?: number | null;
  /** Preços encontrados na página (origem: amazon | mercadolivre | shopee) para você indicar qual usar. */
  priceCandidates?: {
    source: "amazon" | "mercadolivre" | "shopee";
    candidates: PriceCandidate[];
  };
};
