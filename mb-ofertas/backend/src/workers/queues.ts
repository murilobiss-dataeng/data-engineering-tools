import { Queue, Worker, type Job } from "bullmq";
import { env } from "../config/env.js";
import { logger } from "../config/logger.js";

function getRedisOptions(): { host: string; port: number; password?: string } {
  try {
    const u = new URL(env.REDIS_URL);
    const opts: { host: string; port: number; password?: string } = {
      host: u.hostname,
      port: parseInt(u.port || "6379", 10),
    };
    if (u.password) opts.password = u.password;
    return opts;
  } catch {
    return { host: "localhost", port: 6379 };
  }
}

const connection = getRedisOptions();

const QUEUE_NAME = "mb-ofertas:send";

export type SendJobPayload = {
  campaignId: string;
  productId: string;
  recipient: string;
  body: string;
  messageId: string;
};

export const sendQueue = new Queue<SendJobPayload>(QUEUE_NAME, {
  connection,
  defaultJobOptions: {
    removeOnComplete: { count: 1000 },
    attempts: 3,
    backoff: { type: "exponential", delay: 5000 },
  },
});

export function getSendQueue() {
  return sendQueue;
}

export function createSendWorker(
  processor: (job: Job<SendJobPayload>) => Promise<void>
): Worker<SendJobPayload> {
  const worker = new Worker<SendJobPayload>(QUEUE_NAME, processor, {
    connection,
    concurrency: 1,
  });
  worker.on("completed", (job) => logger.info({ jobId: job.id }, "Send job completed"));
  worker.on("failed", (job, err) => logger.error({ jobId: job?.id, err }, "Send job failed"));
  return worker;
}

export async function addSendJob(payload: SendJobPayload, delayMs?: number): Promise<string> {
  const job = await sendQueue.add("send", payload, {
    delay: delayMs ?? env.DELAY_BETWEEN_MESSAGES_MS,
  });
  return job.id ?? "";
}
