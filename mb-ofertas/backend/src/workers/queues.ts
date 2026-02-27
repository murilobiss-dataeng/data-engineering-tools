import { Queue, Worker, type Job } from "bullmq";
import { env } from "../config/env.js";
import { logger } from "../config/logger.js";

const QUEUE_NAME = "mb-ofertas-send";

function isRedisConfigured(): boolean {
  const url = env.REDIS_URL || "";
  if (!url.trim()) return false;
  try {
    const u = new URL(url);
    const host = (u.hostname || "").toLowerCase();
    return host !== "localhost" && host !== "127.0.0.1";
  } catch {
    return false;
  }
}

function getRedisOptions(): { host: string; port: number; password?: string } {
  try {
    const u = new URL(env.REDIS_URL || "redis://localhost:6379");
    return {
      host: u.hostname,
      port: parseInt(u.port || "6379", 10),
      ...(u.password ? { password: u.password } : {}),
    };
  } catch {
    return { host: "localhost", port: 6379 };
  }
}

const connection = getRedisOptions();

export type SendJobPayload = {
  campaignId: string;
  productId: string;
  recipient: string;
  body: string;
  messageId: string;
};

let _sendQueue: Queue<SendJobPayload> | null = null;

if (isRedisConfigured()) {
  _sendQueue = new Queue<SendJobPayload>(QUEUE_NAME, {
    connection,
    defaultJobOptions: {
      removeOnComplete: { count: 1000 },
      attempts: 3,
      backoff: { type: "exponential", delay: 5000 },
    },
  });
} else {
  logger.info("REDIS_URL not set or localhost — send queue disabled (envio WhatsApp não disponível)");
}

export const sendQueue = _sendQueue;

export function getSendQueue(): Queue<SendJobPayload> | null {
  return _sendQueue;
}

export function createSendWorker(
  processor: (job: Job<SendJobPayload>) => Promise<void>
): Worker<SendJobPayload> {
  if (!isRedisConfigured()) throw new Error("REDIS_URL not configured");
  const worker = new Worker<SendJobPayload>(QUEUE_NAME, processor, {
    connection: getRedisOptions(),
    concurrency: 1,
  });
  worker.on("completed", (job) => logger.info({ jobId: job.id }, "Send job completed"));
  worker.on("failed", (job, err) => logger.error({ jobId: job?.id, err }, "Send job failed"));
  return worker;
}

export async function addSendJob(payload: SendJobPayload, delayMs?: number): Promise<string> {
  if (!_sendQueue) throw new Error("REDIS_URL não configurado. Envio por WhatsApp indisponível.");
  const job = await _sendQueue.add("send", payload, {
    delay: delayMs ?? env.DELAY_BETWEEN_MESSAGES_MS,
  });
  return job.id ?? "";
}
