import "dotenv/config";
import { z } from "zod";

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  DATABASE_URL: z.string().default(""),
  REDIS_URL: z.string().default("redis://localhost:6379"),
  API_PORT: z.coerce.number().default(4000),
  LOG_LEVEL: z.enum(["trace", "debug", "info", "warn", "error"]).default("info"),

  // Amazon
  AMAZON_ACCESS_KEY: z.string().optional(),
  AMAZON_SECRET_KEY: z.string().optional(),
  AMAZON_PARTNER_TAG: z.string().optional(),
  AMAZON_REGION: z.string().default("br1"),

  // WhatsApp
  WHATSAPP_ACCOUNT_SID: z.string().optional(),
  WHATSAPP_AUTH_TOKEN: z.string().optional(),
  WHATSAPP_PHONE_NUMBER_ID: z.string().optional(),
  WHATSAPP_FROM_NUMBER: z.string().optional(),

  // Limites
  MAX_MESSAGES_PER_MINUTE: z.coerce.number().default(10),
  MAX_MESSAGES_PER_DAY: z.coerce.number().default(500),
  DELAY_BETWEEN_MESSAGES_MS: z.coerce.number().default(6000),
  RATE_LIMIT_WINDOW_MS: z.coerce.number().default(60000),

  // Cron
  CRON_ENABLED: z.coerce.boolean().default(true),
});

export type Env = z.infer<typeof envSchema>;

function loadEnv(): Env {
  const parsed = envSchema.safeParse(process.env);
  if (!parsed.success) {
    console.error("Invalid environment variables:", parsed.error.flatten());
    throw new Error("Invalid env");
  }
  return parsed.data;
}

export const env = loadEnv();
