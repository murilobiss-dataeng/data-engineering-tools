/** Base sem barra final; se NEXT_PUBLIC_API_URL terminar em /api, remove para não duplicar em /api/... */
export function getPublicApiBaseUrl(): string {
  let u = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000").trim().replace(/\/$/, "");
  if (u.endsWith("/api")) u = u.slice(0, -4);
  return u;
}

/** Base URL para link curto (pra abrir em /r/[code]). Preferir URL pública do app. */
function getShortLinkBaseUrl(): string {
  if (typeof window !== "undefined") {
    return (
      process.env.NEXT_PUBLIC_APP_URL ||
      (window as Window & { __APP_URL?: string }).__APP_URL ||
      window.location.origin
    ).replace(/\/$/, "");
  }
  return (process.env.NEXT_PUBLIC_APP_URL || "").replace(/\/$/, "");
}

const API_URL = getPublicApiBaseUrl();

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
  title: string;
  price: string;
  previous_price: string | null;
  discount_pct: string | null;
  affiliate_link: string;
  image_url: string | null;
  status: string;
  created_at: string;
  category_id?: string | null;
  category_name?: string | null;
  category_slug?: string | null;
  /** Cupom salvo (mensagem WhatsApp). */
  coupon?: string | null;
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
