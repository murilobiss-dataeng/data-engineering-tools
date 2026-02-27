/**
 * Testa conexão com Postgres e resolução DNS do host.
 * Uso: yarn db:test (na pasta backend) ou npx tsx backend/src/db/test-connection.ts (na raiz).
 */
import { config } from "dotenv";
import { resolve } from "path";
import dns from "dns/promises";
import pg from "pg";

config();
if (!process.env.DATABASE_URL) config({ path: resolve(process.cwd(), "..", ".env") });

const connectionString = process.env.DATABASE_URL;
if (!connectionString) {
  console.error("❌ DATABASE_URL não definido. Configure no .env (raiz ou backend).");
  process.exit(1);
}

function maskUrl(url: string): string {
  try {
    const u = new URL(url);
    if (u.password) u.password = "***";
    return u.toString();
  } catch {
    return "(URL inválida)";
  }
}

async function main() {
  console.log("🔍 DATABASE_URL (mascarado):", maskUrl(connectionString));
  let host: string;
  try {
    const u = new URL(connectionString);
    host = u.hostname;
    console.log("   Host:", host);
  } catch (e) {
    console.error("❌ URL inválida:", e);
    process.exit(1);
  }

  console.log("\n📡 DNS:");
  try {
    const [ipv4] = await dns.resolve4(host).catch(() => []);
    const ipv6 = await dns.resolve6(host).catch(() => []);
    console.log("   resolve4 (A):", ipv4 ?? "(ENODATA ou erro)");
    console.log("   resolve6 (AAAA):", ipv6.length ? ipv6.slice(0, 2) : "(nenhum)");
    const lookupAll = await dns.lookup(host, { all: true });
    console.log("   lookup(all):", lookupAll.map((a) => `${a.family} ${a.address}`).join(", "));
  } catch (e) {
    console.log("   Erro DNS:", (e as Error).message);
  }

  console.log("\n🐘 Postgres:");
  const pool = new pg.Pool({
    connectionString,
    max: 1,
    connectionTimeoutMillis: 15000,
  });
  try {
    const client = await pool.connect();
    const res = await client.query("SELECT 1 as n, current_database() as db");
    client.release();
    console.log("   ✅ Conexão OK:", res.rows[0]);
  } catch (e) {
    const err = e as Error;
    console.log("   ❌ Falha:", err.message);
    if (err.message.includes("ENETUNREACH")) {
      console.log("   (Rede inacessível – ex.: IPv6 bloqueado no ambiente)");
    }
    if (/db\.\w+\.supabase\.co/.test(host)) {
      console.log("\n💡 Use a connection string em **Session mode** (IPv4):");
      console.log("   Dashboard Supabase → Connect → Session (pooler) → URI.");
      console.log("   Host será algo como: aws-0-XX.pooler.supabase.com:5432");
    }
    process.exitCode = 1;
  } finally {
    await pool.end();
  }
}

main();
