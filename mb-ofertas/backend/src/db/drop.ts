import { config } from "dotenv";
import { resolve } from "path";
config();
if (!process.env.DATABASE_URL) config({ path: resolve(process.cwd(), "..", ".env") });
import { readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { initPool, getPool } from "./client.js";
import { logger } from "../config/logger.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

export async function dropAll(): Promise<void> {
  await initPool();
  const pool = getPool();
  const sqlPath = join(__dirname, "schema-drop.sql");
  const sql = readFileSync(sqlPath, "utf-8");
  await pool.query(sql);
  logger.info("Tabelas apagadas (schema-drop.sql). Rode db:migrate para recriar.");
}

async function main() {
  if (!process.env.DATABASE_URL) {
    console.error("Defina DATABASE_URL no .env");
    process.exit(1);
  }
  try {
    await dropAll();
    process.exit(0);
  } catch (err) {
    logger.error({ err }, "Drop failed");
    process.exit(1);
  }
}

main();
