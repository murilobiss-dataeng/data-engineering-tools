import { Client, LocalAuth } from "whatsapp-web.js";
import qrcode from "qrcode-terminal";
import cron from "node-cron";
import path from "path";
import fs from "fs";
import { config } from "./config.js";
import { logger } from "./logger.js";
import { fetchPosts } from "./api.js";
import { processPosts } from "./sender.js";

if (!fs.existsSync(config.dataPath)) {
  fs.mkdirSync(config.dataPath, { recursive: true });
  logger.info("Pasta de dados criada:", config.dataPath);
}
const AUTH_PATH = path.join(config.dataPath, ".wwebjs_auth");
const CRON_EXPR = `*/${config.cronIntervalMinutes} * * * *`; // a cada N minutos

let client = null;
let isRunning = false;
let cronScheduled = false;

function createClient() {
  const auth = new LocalAuth({
    clientId: config.authClientId,
    dataPath: AUTH_PATH,
  });

  const c = new Client({
    authStrategy: auth,
    puppeteer: {
      headless: true,
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
      ],
    },
  });

  c.on("qr", (qr) => {
    logger.info("Escaneie o QR Code abaixo com o WhatsApp (Aparelhos conectados):");
    qrcode.generate(qr, { small: true });
  });

  c.on("ready", () => {
    logger.info("WhatsApp conectado. Sessão salva em", AUTH_PATH);
    isRunning = true;
  });

  c.on("authenticated", () => {
    logger.info("Autenticado. Salvando sessão...");
  });

  c.on("auth_failure", (msg) => {
    logger.error("Falha de autenticação:", msg);
  });

  c.on("disconnected", (reason) => {
    logger.warn("WhatsApp desconectado:", reason);
    isRunning = false;
  });

  return c;
}

async function runJob() {
  if (!client || !isRunning) {
    logger.warn("Cliente não está pronto. Pulando execução.");
    return;
  }
  if (!config.apiUrl) {
    logger.warn("API_URL não configurada. Configure no .env.");
    return;
  }

  logger.info("Buscando novos posts na API...");
  const posts = await fetchPosts(config.apiUrl);
  if (posts.length === 0) return;

  const sent = await processPosts(client, posts);
  if (sent > 0) {
    logger.info(`${sent} post(s) enviado(s).`);
  }
}

async function start() {
  logger.info("Iniciando bot. Intervalo:", config.cronIntervalMinutes, "minutos");
  logger.info("API:", config.apiUrl || "(não configurada)");
  logger.info("Chats:", config.chatIds.length ? config.chatIds : "(nenhum)");

  client = createClient();

  c.on("ready", async () => {
    const chats = await c.getChats();
    logger.info("Chats disponíveis (use o id no .env CHAT_IDS):");
    for (const chat of chats.slice(0, 20)) {
      const idStr = chat.id?._serialized || chat.id || "";
      logger.info(`  ${chat.name || idStr}: ${idStr}`);
    }
    if (chats.length > 20) logger.info(`  ... e mais ${chats.length - 20} chat(s).`);
    if (!cronScheduled) {
      cron.schedule(CRON_EXPR, runJob, { timezone: "America/Sao_Paulo" });
      cronScheduled = true;
      logger.info(`Cron agendado: a cada ${config.cronIntervalMinutes} minuto(s).`);
    }
    await runJob();
  });

  c.on("disconnected", () => {
    logger.info("Tentando reconectar em 30s...");
    setTimeout(() => {
      if (!isRunning) {
        client = createClient();
        client.initialize().catch((e) => logger.error("Erro ao reconectar:", e.message));
      }
    }, 30000);
  });

  try {
    await client.initialize();
  } catch (err) {
    logger.error("Erro ao inicializar cliente:", err.message);
    process.exit(1);
  }
}

start().catch((e) => {
  logger.error("Falha ao iniciar:", e);
  process.exit(1);
});
