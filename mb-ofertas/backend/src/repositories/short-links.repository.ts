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
 * Se nenhum estiver definido, retorna a URL original (fallback para encurtar e esconder tag).
 */
export async function createShortLink(
  longUrl: string,
  baseUrlOverride?: string | null
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
  const existingByUrl = await query<{ code: string }>(
    `SELECT code FROM short_links WHERE long_url = $1 ORDER BY created_at ASC LIMIT 1`,
    [url]
  );
  if (existingByUrl.rows[0]?.code) {
    return { code: existingByUrl.rows[0].code, shortUrl: `${base}/r/${existingByUrl.rows[0].code}` };
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
    `INSERT INTO short_links (code, long_url) VALUES ($1, $2)`,
    [code, url]
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
  const res = await query(
    `SELECT sl.code,
            sl.long_url,
            sl.click_count,
            sl.last_clicked_at,
            sl.created_at,
            p.title AS product_title,
            c.slug AS category_slug
     FROM short_links sl
     LEFT JOIN products p ON p.affiliate_link = sl.long_url
     LEFT JOIN categories c ON c.id = p.category_id
     ORDER BY sl.click_count DESC, sl.last_clicked_at DESC NULLS LAST, sl.created_at DESC
     LIMIT $1`,
    [limit]
  );
  return res.rows.map((row) => ({
    ...row,
    short_url_path: `/r/${row.code}`,
  }));
}
