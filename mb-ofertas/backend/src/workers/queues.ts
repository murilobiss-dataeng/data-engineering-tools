import { Queue, Worker, type Job } from "bullmq";
import type { RedisOptions } from "ioredis";
import { env } from "../config/env.js";
import { logger } from "../config/logger.js";

const QUEUE_NAME = "mb-ofertas-send";

function isRedisConfigured(): boolean {
  if (env.REDIS_DISABLED) return false;
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

function getRedisOptions(): RedisOptions {
  try {
    const u = new URL(env.REDIS_URL || "redis://localhost:6379");
    const port = parseInt(u.port || "6379", 10);
    const opts: RedisOptions = {
      host: u.hostname,
      port,
      maxRetriesPerRequest: null,
      /** Evita reconexão infinita e spam de ENOTFOUND quando o hostname Redis Cloud não existe mais. */
      retryStrategy: (times: number) => {
        if (times > 10) {
          logger.error(
            { host: u.hostname },
            "Redis: desistindo após 10 tentativas (hostname inválido ou Redis indisponível). Defina REDIS_DISABLED=true ou corrija REDIS_URL no painel Redis Cloud."
          );
          return null;
        }
        return Math.min(times * 300, 3000);
      },
      lazyConnect: true,
    };
    if (u.username) opts.username = decodeURIComponent(u.username);
    if (u.password) opts.password = decodeURIComponent(u.password);
    if (u.protocol === "rediss:" && env.REDIS_TLS !== false) opts.tls = {};
    return opts;
  } catch {
    return { host: "localhost", port: 6379, maxRetriesPerRequest: null };
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
  _sendQueue.on("error", (err: Error) => {
    logger.warn({ err: err.message, code: (err as NodeJS.ErrnoException).code }, "Redis/BullMQ queue error");
  });
} else {
  const reason = env.REDIS_DISABLED
    ? "REDIS_DISABLED=true"
    : "REDIS_URL vazio ou localhost";
  logger.info({ reason }, "Fila de envio (BullMQ) desativada — campanhas em massa sem fila Redis");
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
