import { randomBytes } from "crypto";
import { query } from "../db/client.js";

const CODE_LENGTH = 8;
const CODE_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

function generateCode(): string {
  const bytes = randomBytes(CODE_LENGTH);
  let s = "";
  for (let i = 0; i < CODE_LENGTH; i++) {
    s += CODE_CHARS[bytes[i]! % CODE_CHARS.length];
  }
  return s;
}

/**
 * Cria link curto. Base URL: override baseUrl, ou SHORT_LINK_BASE_URL, ou API_URL, ou NEXT_PUBLIC_APP_URL.
 * `productId` opcional: grava vínculo para analytics (evita "Sem produto" quando affiliate_link ≠ long_url por query).
 */
export async function createShortLink(
  longUrl: string,
  baseUrlOverride?: string | null,
  productId?: string | null
): Promise<{ code: string; shortUrl: string } | { shortUrl: string }> {
  const base = (
    (baseUrlOverride && baseUrlOverride.trim()) ||
    process.env.SHORT_LINK_BASE_URL ||
    process.env.API_URL ||
    process.env.NEXT_PUBLIC_APP_URL ||
    ""
  ).trim().replace(/\/$/, "");
  const url = longUrl.trim();
  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    return { shortUrl: url };
  }
  if (!base) return { shortUrl: url };
  const existingByUrl = await query<{ code: string; product_id: string | null }>(
    `SELECT code, product_id FROM short_links WHERE long_url = $1 ORDER BY created_at ASC LIMIT 1`,
    [url]
  );
  const existingRow = existingByUrl.rows[0];
  if (existingRow?.code) {
    if (productId && !existingRow.product_id) {
      await query(`UPDATE short_links SET product_id = $1 WHERE code = $2 AND product_id IS NULL`, [
        productId,
        existingRow.code,
      ]);
    }
    return { code: existingRow.code, shortUrl: `${base}/r/${existingRow.code}` };
  }
  let code: string;
  let attempts = 0;
  while (true) {
    code = generateCode();
    const existing = await query<{ id: string }>(`SELECT id FROM short_links WHERE code = $1`, [code]);
    if (existing.rows.length === 0) break;
    if (++attempts > 5) return { shortUrl: url };
  }
  await query(
    `INSERT INTO short_links (code, long_url, product_id) VALUES ($1, $2, $3)`,
    [code, url, productId ?? null]
  );
  const shortUrl = `${base}/r/${code}`;
  return { code, shortUrl };
}

export async function getLongUrlByCode(code: string): Promise<string | null> {
  const res = await query<{ long_url: string }>(
    `SELECT long_url FROM short_links WHERE code = $1`,
    [code]
  );
  return res.rows[0]?.long_url ?? null;
}

export async function registerShortLinkClick(code: string): Promise<string | null> {
  const res = await query<{ long_url: string }>(
    `UPDATE short_links
     SET click_count = click_count + 1, last_clicked_at = now()
     WHERE code = $1
     RETURNING long_url`,
    [code]
  );
  return res.rows[0]?.long_url ?? null;
}

export async function listShortLinkAnalytics(limit = 100): Promise<
  {
    code: string;
    long_url: string;
    short_url_path: string;
    click_count: number;
    last_clicked_at: string | null;
    created_at: string;
    product_title: string | null;
    category_slug: string | null;
  }[]
> {
  type AnalyticsRow = {
    code: string;
    long_url: string;
    click_count: number;
    last_clicked_at: string | null;
    created_at: string;
    product_title: string | null;
    category_slug: string | null;
    product_status: string | null;
  };
  const res = await query<AnalyticsRow>(
    `SELECT * FROM (
       SELECT DISTINCT ON (sl.code)
         sl.code,
         sl.long_url,
         sl.click_count,
         sl.last_clicked_at,
         sl.created_at,
         p.title AS product_title,
         c.slug AS category_slug,
         p.status AS product_status
       FROM short_links sl
       LEFT JOIN products p ON p.id = sl.product_id
         OR p.affiliate_link = sl.long_url
         OR regexp_replace(p.affiliate_link, '/$', '') = regexp_replace(sl.long_url, '/$', '')
         OR split_part(p.affiliate_link, '?', 1) = split_part(sl.long_url, '?', 1)
       LEFT JOIN categories c ON c.id = p.category_id
       ORDER BY sl.code,
         CASE
           WHEN p.status IN ('pending', 'approved', 'sent') AND sl.product_id IS NOT NULL AND p.id = sl.product_id THEN 0
           WHEN p.status IN ('pending', 'approved', 'sent') AND p.affiliate_link = sl.long_url THEN 1
           WHEN p.status IN ('pending', 'approved', 'sent') THEN 2
           ELSE 3
         END,
         p.id NULLS LAST
     ) sub
     WHERE sub.product_status IN ('pending', 'approved', 'sent')
     ORDER BY sub.click_count DESC, sub.last_clicked_at DESC NULLS LAST, sub.created_at DESC
     LIMIT $1`,
    [limit]
  );
  return res.rows.map((row) => ({
    ...row,
    short_url_path: `/r/${row.code}`,
  }));
}
