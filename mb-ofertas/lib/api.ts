const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";

export async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}/api${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
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

export type ScrapedProduct = {
  title: string;
  price: number;
  previousPrice: number | null;
  discountPct: number | null;
  imageUrl: string | null;
  affiliateLink: string;
  rawUrl: string;
};
