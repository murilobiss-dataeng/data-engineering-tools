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

const app = express();

app.set("trust proxy", 1);
app.use(cors());
app.use(express.json());

const limiter = rateLimit({
  windowMs: env.RATE_LIMIT_WINDOW_MS,
  max: 100,
  message: { error: "Muitas requisições. Tente novamente em breve." },
});
app.use("/api/", limiter);

app.use("/api/products", productsRouter);
app.use("/api/campaigns", campaignsRouter);
app.use("/api/categories", categoriesRouter);

app.get("/api/health", (_req, res) => {
  res.json({ status: "ok", timestamp: new Date().toISOString() });
});

app.use((err: Error, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  logger.error({ err }, "API error");
  res.status(500).json({ error: "Erro interno do servidor" });
});

const port = env.API_PORT;
initPool()
  .then(() => {
    app.listen(port, () => {
      logger.info({ port }, "API listening");
    });
  })
  .catch((err) => {
    logger.error({ err }, "Failed to init DB pool");
    process.exit(1);
  });
