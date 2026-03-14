import "dotenv/config";
import dns from "dns";
dns.setDefaultResultOrder("ipv4first");

import express from "express";
import cors from "cors";
import rateLimit from "express-rate-limit";
import { env } from "../config/env.js";
import { logger } from "../config/logger.js";
import { initPool } from "../db/client.js";
import { productsRouter } from "./routes/products.js";
import { campaignsRouter } from "./routes/campaigns.js";
import { categoriesRouter } from "./routes/categories.js";
import { whatsappChannelsRouter } from "./routes/whatsapp-channels.js";
import { whatsappScheduledRouter } from "./routes/whatsapp-scheduled.js";
import { shortLinksRouter } from "./routes/short-links.js";
import { logsRouter } from "./routes/logs.js";
import { getLongUrlByCode } from "../repositories/short-links.repository.js";
import * as productsRepo from "../repositories/products.repository.js";

const app = express();

app.set("trust proxy", 1);
app.use(cors());
app.use(express.json());

// Redirect de link curto (fora do /api para não consumir rate limit)
app.get("/r/:code", async (req, res) => {
  const code = req.params.code?.trim();
  if (!code || code.length > 20) return res.status(404).send("Link não encontrado");
  try {
    const longUrl = await getLongUrlByCode(code);
    if (!longUrl) return res.status(404).send("Link não encontrado");
    res.redirect(302, longUrl);
  } catch {
    res.status(500).send("Erro ao redirecionar");
  }
});

const limiter = rateLimit({
  windowMs: env.RATE_LIMIT_WINDOW_MS,
  max: 100,
  message: { error: "Muitas requisições. Tente novamente em breve." },
});
app.use("/api/", limiter);

app.use("/api/products", productsRouter);
app.use("/api/campaigns", campaignsRouter);
app.use("/api/categories", categoriesRouter);
app.use("/api/whatsapp/channels", whatsappChannelsRouter);
app.use("/api/whatsapp/scheduled", whatsappScheduledRouter);
app.use("/api/short-links", shortLinksRouter);
app.use("/api/logs", logsRouter);

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

app.use((err: Error, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  logger.error({ err }, "API error");
  res.status(500).json({ error: "Erro interno do servidor" });
});

function runExpiryJob() {
  return productsRepo
    .expireApprovedOlderThanHours(env.OFFER_EXPIRY_HOURS)
    .then((deleted) => {
      if (deleted > 0) logger.info({ deleted, hours: env.OFFER_EXPIRY_HOURS }, "Ofertas expiradas (timeout)");
    })
    .catch((err) => logger.error({ err }, "Erro ao expirar ofertas"));
}

function startExpiryJob() {
  if (!env.CRON_ENABLED || env.OFFER_EXPIRY_HOURS <= 0) return;
  runExpiryJob(); // uma vez ao subir
  const intervalMs = 60 * 60 * 1000; // depois a cada 1 hora
  setInterval(runExpiryJob, intervalMs);
  logger.info({ hours: env.OFFER_EXPIRY_HOURS }, "Job de expiração de ofertas ativo (a cada 1h)");
}

const port = env.API_PORT;
initPool()
  .then(() => {
    app.listen(port, () => {
      logger.info({ port }, "API listening");
      startExpiryJob();
    });
  })
  .catch((err) => {
    logger.error({ err }, "Failed to init DB pool");
    process.exit(1);
  });
