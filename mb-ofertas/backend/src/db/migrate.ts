import { readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";
import { getPool } from "./client.js";
import { logger } from "../config/logger.js";

const __dirname = dirname(fileURLToPath(import.meta.url));

export async function migrate(): Promise<void> {
  const pool = getPool();
  const schemaPath = join(__dirname, "schema.sql");
  const sql = readFileSync(schemaPath, "utf-8");

  await pool.query(sql);
  logger.info("Migrations applied (schema.sql)");
}

async function main() {
  if (!process.env.DATABASE_URL) {
    console.error("Defina DATABASE_URL no .env (connection string do Supabase).");
    process.exit(1);
  }
  try {
    await migrate();
    process.exit(0);
  } catch (err) {
    logger.error({ err }, "Migration failed");
    process.exit(1);
  }
}

main();
