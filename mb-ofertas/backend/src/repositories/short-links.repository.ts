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
 * Cria link curto. Se SHORT_LINK_BASE_URL não estiver definido, retorna a URL original.
 */
export async function createShortLink(longUrl: string): Promise<{ code: string; shortUrl: string } | { shortUrl: string }> {
  const base = process.env.SHORT_LINK_BASE_URL?.replace(/\/$/, "") || "";
  const url = longUrl.trim();
  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    return { shortUrl: url };
  }
  if (!base) return { shortUrl: url };
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
