import "dotenv/config";
import { z } from "zod";

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  DATABASE_URL: z.string().default(""),
  DATABASE_POOL_MAX: z.coerce.number().min(1).max(20).optional(),
  /** Fila BullMQ (envio em massa). true/1/yes = não conecta ao Redis (evita ENOTFOUND quando o host Redis expirou). */
  REDIS_DISABLED: z
    .preprocess((v) => {
      if (v === undefined || v === "") return false;
      const s = String(v).toLowerCase();
      return s === "true" || s === "1" || s === "yes";
    }, z.boolean())
    .default(false),
  REDIS_URL: z.string().default("redis://localhost:6379"),
  /** Se false/0/no, conecta sem TLS mesmo com rediss:// (evita ERR_SSL_PACKET_LENGTH_TOO_LONG no Redis Cloud quando a porta é TCP). */
  REDIS_TLS: z
    .string()
    .optional()
    .transform((v) => {
      if (v === undefined || v === "") return undefined;
      const lower = String(v).toLowerCase();
      return lower !== "0" && lower !== "false" && lower !== "no";
    }),
  API_PORT: z.coerce.number().default(4000),
  LOG_LEVEL: z.enum(["trace", "debug", "info", "warn", "error"]).default("info"),

  // Amazon
  AMAZON_ACCESS_KEY: z.string().optional(),
  AMAZON_SECRET_KEY: z.string().optional(),
  AMAZON_PARTNER_TAG: z.string().optional(),
  AMAZON_REGION: z.string().default("br1"),
  /** URL de proxy/espelho para páginas de ofertas Amazon (listagem). Opcional; também use USE_BROWSER_SCRAPER. */
  AMAZON_DEALS_PROXY_URL: z.string().optional(),

  /** Código de afiliado Mercado Livre (ex.: mk20260227092713). Adiciona ?afiliado=... em links ML. */
  ML_AFFILIATE_TAG: z.string().optional(),

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

  // Link curto (base URL para /r/CODE; se vazio, mensagens usam link longo)
  SHORT_LINK_BASE_URL: z.string().optional(),

  // Cron
  CRON_ENABLED: z.coerce.boolean().default(true),
  /** Excluir automaticamente ofertas aprovadas há mais de N horas (0 = desativado). */
  OFFER_EXPIRY_HOURS: z.coerce.number().min(0).max(720).default(24),

  /** Se true, em falha de preço/título usa Playwright (Chromium) para obter HTML. Requer: yarn add playwright && npx playwright install chromium. */
  USE_BROWSER_SCRAPER: z.coerce.boolean().default(false),
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
