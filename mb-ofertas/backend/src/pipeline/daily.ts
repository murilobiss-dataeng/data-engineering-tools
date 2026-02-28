/**
 * Pipeline diário: buscar produtos em listagens (Amazon, ML, Shopee) → categorizar → salvar.
 * Agende com cron: 0 9,12,18 * * * (9h, 12h, 18h)
 */
import "dotenv/config";
import { runFetchOfertas, getDefaultListingUrls } from "../services/products/fetch-ofertas.service.js";
import { logger } from "../config/logger.js";

async function run() {
  logger.info("Pipeline daily: start");

  const urls = getDefaultListingUrls();
  const result = await runFetchOfertas({
    urls,
    maxPerListing: 15,
    delayMs: 2500,
  });

  logger.info({ inserted: result.inserted, failed: result.failed, totalUrls: result.totalUrls }, "Pipeline daily: done");
  process.exit(0);
}

run().catch((err) => {
  logger.error({ err }, "Pipeline failed");
  process.exit(1);
});
