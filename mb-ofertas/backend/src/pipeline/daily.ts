/**
 * Pipeline diário: buscar produtos → filtrar → gerar copy → salvar.
 * Agende com cron: 0 9,12,18 * * * (9h, 12h, 18h)
 */
import "dotenv/config";
import { captureAmazonDeals } from "../services/products/amazon.service.js";
import * as productsRepo from "../repositories/products.repository.js";
import { logger } from "../config/logger.js";

async function run() {
  logger.info("Pipeline daily: start");

  const categories = ["ofertas-do-dia", "eletronicos", "livros"];
  let totalInserted = 0;

  for (const slug of categories) {
    try {
      const result = await captureAmazonDeals(slug);
      for (const p of result.products) {
        try {
          await productsRepo.insertProduct({ ...p, categoryId: undefined });
          totalInserted++;
        } catch (e) {
          // duplicata por external_id
          logger.debug({ err: e }, "Skip duplicate product");
        }
      }
    } catch (err) {
      logger.warn({ err, slug }, "Capture failed for category");
    }
  }

  logger.info({ totalInserted }, "Pipeline daily: done");
  process.exit(0);
}

run().catch((err) => {
  logger.error({ err }, "Pipeline failed");
  process.exit(1);
});
