/**
 * Worker process: consome fila de envio WhatsApp com delay e rate limit.
 * Rodar: npm run worker (ou node dist/workers/run.js)
 */
import "dotenv/config";
import { createSendWorker } from "./queues.js";
import { processSendJob } from "./send-job.processor.js";
import { logger } from "../config/logger.js";

const worker = createSendWorker(processSendJob);

async function shutdown() {
  logger.info("Shutting down worker...");
  await worker.close();
  process.exit(0);
}

process.on("SIGTERM", shutdown);
process.on("SIGINT", shutdown);

logger.info("Worker started (send queue)");
