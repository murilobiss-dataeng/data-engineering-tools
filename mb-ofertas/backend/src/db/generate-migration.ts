/**
 * Gera um novo arquivo de migration vazio (para evoluções futuras do schema).
 * Uso: npm run db:generate -- nome_da_migracao
 */
import { writeFileSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const name = process.argv[2] ?? "custom";
const slug = name.replace(/\s+/g, "_").toLowerCase();
const filename = `${Date.now()}_${slug}.sql`;
const migrationsDir = join(__dirname, "migrations");
mkdirSync(migrationsDir, { recursive: true });
const filePath = join(migrationsDir, filename);

writeFileSync(
  filePath,
  `-- ${name}\n-- Adicione os comandos SQL abaixo.\n\n`,
  "utf-8"
);
console.log("Created:", filePath);
