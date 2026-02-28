/**
 * Client Postgres. Para Supabase em ambientes sem IPv6 (ex.: Render), use
 * a connection string em Session mode (pooler): Connect → Session no dashboard.
 * Host: aws-0-XX.pooler.supabase.com:5432 — suporta IPv4.
 */
import pg from "pg";
import dns from "dns/promises";
import { env } from "../config/env.js";
import { logger } from "../config/logger.js";

const { Pool } = pg;

let pool: pg.Pool | null = null;
let poolInit: Promise<pg.Pool> | null = null;

async function buildConnectionString(): Promise<string> {
  const url = env.DATABASE_URL;
  if (!url) throw new Error("DATABASE_URL é obrigatório. Configure no .env (Supabase).");
  let connectionString = url;
  if (!url.includes("supabase.co")) return connectionString;
  const u = new URL(connectionString);
  u.searchParams.delete("sslmode");
  connectionString = u.toString();
  try {
    const host = u.hostname;
    const [ipv4] = await dns.resolve4(host);
    if (ipv4) {
      u.hostname = ipv4;
      connectionString = u.toString();
      logger.info({ host, ipv4 }, "Postgres: using IPv4 for Supabase");
    }
  } catch (e) {
    logger.warn({ err: e }, "Postgres: could not resolve IPv4, using hostname");
  }
  return connectionString;
}

export async function initPool(): Promise<pg.Pool> {
  if (pool) return pool;
  if (poolInit) return poolInit;
  poolInit = (async () => {
    const connectionString = await buildConnectionString();
    const isSupabase = connectionString.includes("supabase.co") || connectionString.includes("pooler.supabase.com");
    const maxConnections = env.DATABASE_POOL_MAX ?? (isSupabase ? 3 : 20);
    pool = new Pool({
      connectionString,
      max: maxConnections,
      idleTimeoutMillis: 10000,
      connectionTimeoutMillis: 8000,
      ...(isSupabase && {
        ssl: { rejectUnauthorized: false },
      }),
    });
    pool.on("error", (err) => logger.error({ err }, "Pool PostgreSQL error"));
    return pool;
  })();
  return poolInit;
}

export function getPool(): pg.Pool {
  if (!pool) {
    throw new Error("Pool não inicializado. Chame await initPool() no startup da API.");
  }
  return pool;
}

export async function query<T extends pg.QueryResultRow = pg.QueryResultRow>(
  text: string,
  params?: unknown[]
): Promise<pg.QueryResult<T>> {
  const client = getPool();
  const start = Date.now();
  try {
    const res = await client.query(text, params) as pg.QueryResult<T>;
    logger.debug({ text: text.slice(0, 80), duration: Date.now() - start }, "db query");
    return res;
  } catch (err) {
    logger.error({ err, text: text.slice(0, 80) }, "db query error");
    throw err;
  }
}

export async function closePool(): Promise<void> {
  if (pool) {
    await pool.end();
    pool = null;
    logger.info("Pool PostgreSQL closed");
  }
}

export type Product = {
  id: string;
  category_id: string | null;
  external_id: string | null;
  title: string;
  price: string;
  previous_price: string | null;
  discount_pct: string | null;
  affiliate_link: string;
  image_url: string | null;
  source: string;
  status: string;
  approved_at: string | null;
  created_at: string;
  updated_at: string;
  installments: string | null;
};

export type Category = {
  id: string;
  name: string;
  slug: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};

export type Campaign = {
  id: string;
  name: string;
  status: string;
  scheduled_at: string | null;
  started_at: string | null;
  completed_at: string | null;
  product_ids: string[];
  target_type: string;
  target_ref: string | null;
  created_at: string;
  updated_at: string;
};

export type Message = {
  id: string;
  campaign_id: string;
  product_id: string;
  body: string;
  short_link: string | null;
  status: string;
  sent_at: string | null;
  recipient: string | null;
  error_message: string | null;
  created_at: string;
};
