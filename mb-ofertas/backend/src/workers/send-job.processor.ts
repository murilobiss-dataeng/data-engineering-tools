import type { Job } from "bullmq";
import { query } from "../db/client.js";
import { sendWhatsAppText } from "../services/whatsapp/whatsapp.service.js";
import { logger } from "../config/logger.js";
import type { SendJobPayload } from "./queues.js";

export async function processSendJob(job: Job<SendJobPayload>): Promise<void> {
  const { campaignId, productId, recipient, body, messageId } = job.data;

  const result = await sendWhatsAppText(recipient, body);

  if (result.success) {
    await query(
      `UPDATE messages SET status = 'sent', sent_at = now() WHERE id = $1`,
      [messageId]
    );
    logger.info({ messageId, recipient }, "Message sent and updated");
  } else {
    await query(
      `UPDATE messages SET status = 'failed', error_message = $1 WHERE id = $2`,
      [result.error ?? "Unknown", messageId]
    );
    throw new Error(result.error);
  }
}
