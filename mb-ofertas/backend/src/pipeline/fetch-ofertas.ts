/**
 * Script para buscar ofertas automaticamente (Amazon e Mercado Livre).
 * Lê URLs de scripts/ofertas-urls.json (ou OFERTAS_URLS no .env), scrape e insere no banco.
 * Uso: npm run fetch-ofertas
 * Também pode ser acionado pela UI (Produtos → Buscar ofertas automaticamente).
 */
import "dotenv/config";
import { runFetchOfertas } from "../services/products/fetch-ofertas.service.js";
import { logger } from "../config/logger.js";

async function run() {
  logger.info("Fetch ofertas: start");

  const result = await runFetchOfertas();

  if (result.totalUrls === 0) {
    logger.warn("Nenhuma URL configurada. Use scripts/ofertas-urls.json ou OFERTAS_URLS no .env.");
  } else {
    logger.info({ inserted: result.inserted, failed: result.failed, totalUrls: result.totalUrls }, "Fetch ofertas: done");
  }

  process.exit(0);
}

run().catch((err) => {
  logger.error({ err }, "Fetch ofertas failed");
  process.exit(1);
});
