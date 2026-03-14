import pkg from "whatsapp-web.js";
const { Client, LocalAuth } = pkg;
import qrcode from "qrcode-terminal";
import QRCode from "qrcode";
import cron from "node-cron";
import path from "path";
import fs from "fs";
import { config } from "./config.js";
import { logger } from "./logger.js";
import { fetchPosts } from "./api.js";
import { processPosts } from "./sender.js";

const isGHA = process.env.GITHUB_ACTIONS === "true";

if (!fs.existsSync(config.dataPath)) {
  fs.mkdirSync(config.dataPath, { recursive: true });
  logger.info("Pasta de dados criada:", config.dataPath);
}
const AUTH_PATH = path.join(config.dataPath, ".wwebjs_auth");
const CRON_EXPR = `*/${config.cronIntervalMinutes} * * * *`; // a cada N minutos

let client = null;
let isRunning = false;
let cronScheduled = false;
let qrAlreadyShown = false;

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

  c.on("qr", async (qr) => {
    if (qrAlreadyShown) return;
    qrAlreadyShown = true;

    logger.info("Escaneie o QR Code com o WhatsApp (Aparelhos conectados):");
    if (isGHA) {
      try {
        const qrDataUrl = await QRCode.toDataURL(qr, { margin: 2, width: 280 });
        const qrFilePath = path.resolve(config.dataPath, "qr-url.txt");
        fs.writeFileSync(qrFilePath, qrDataUrl, "utf-8");
        logger.info("QR salvo em:", qrFilePath);
        logger.info("No GHA: baixe o artifact 'whatsapp-qr' (qr.html) na página da execução do workflow.");
      } catch (e) {
        logger.warn("Não foi possível salvar QR:", e.message);
      }
    } else {
      qrcode.generate(qr, { small: true });
      const qrFilePath = path.resolve(config.dataPath, "qr-url.txt");
      try {
        const qrDataUrl = await QRCode.toDataURL(qr, { margin: 2, width: 280 });
        fs.writeFileSync(qrFilePath, qrDataUrl, "utf-8");
        logger.info("QR também salvo em:", qrFilePath);
      } catch (_) {}
    }
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
  const apiOptions = config.singleRun ? { timeout: 60000, retries: 2 } : { timeout: 30000, retries: 1 };
  const posts = await fetchPosts(config.apiUrl, apiOptions);
  if (posts.length === 0) return;

  const sent = await processPosts(client, posts);
  if (sent > 0) {
    logger.info(`${sent} post(s) enviado(s).`);
  }
}

async function start() {
  logger.info("Iniciando bot. Modo:", config.singleRun ? "single-run (GHA)" : `intervalo ${config.cronIntervalMinutes} min`);
  logger.info("API:", config.apiUrl || "(não configurada)");
  logger.info("Chats:", config.chatIds.length ? config.chatIds : "(nenhum)");

  client = createClient();

  client.on("ready", async () => {
    const chats = await client.getChats();
    logger.info("Chats disponíveis (use o id no CHAT_ID):");
    for (const chat of chats.slice(0, 20)) {
      const idStr = chat.id?._serialized || chat.id || "";
      logger.info(`  ${chat.name || idStr}: ${idStr}`);
    }
    if (chats.length > 20) logger.info(`  ... e mais ${chats.length - 20} chat(s).`);
    const isInvite = (v) => {
      const s = (v || "").trim();
      if (/@(g\.us|newsletter|c\.us)/.test(s)) return false;
      return s.length > 0;
    };
    const inviteCode = (v) => {
      const s = (v || "").trim();
      const m = s.match(/whatsapp\.com\/channel\/([A-Za-z0-9_-]+)/);
      return m ? m[1] : s;
    };

    if (typeof client.getChannels === "function") {
      try {
        const channels = await client.getChannels();
        if (channels.length > 0) {
          logger.info("Canais — use o ID abaixo no CHAT_ID:");
          for (const ch of channels.slice(0, 10)) {
            const idStr = ch.id?._serialized || ch.id || "";
            logger.info(`  ${ch.name || idStr}: ${idStr}`);
          }
          if (channels.length > 10) logger.info(`  ... e mais ${channels.length - 10} canal(is).`);
          logger.info("Exemplo CHAT_ID: 12345678901234567@newsletter");
        } else {
          logger.info("Nenhum canal na lista do WhatsApp Web.");
        }
      } catch (e) {
        logger.warn("Listagem de canais falhou:", e.message);
      }
    }

    for (const rawId of config.chatIds) {
      if (!isInvite(rawId)) continue;
      if (typeof client.getChannelByInviteCode !== "function") continue;
      const code = inviteCode(rawId);
      try {
        const channel = await client.getChannelByInviteCode(code);
        const idStr = channel?.id?._serialized || channel?.id || "";
        const name = channel?.name || "Canal";
        logger.info(`Canal resolvido pelo link: ${name} -> ${idStr}`);
        logger.info(`Use em CHAT_ID: ${idStr}`);
      } catch (e) {
        logger.warn(`Não foi possível resolver o canal (${code.slice(0, 20)}...):`, e.message);
      }
    }
    if (config.singleRun) {
      await runJob();
      logger.info("Single-run: envio concluído. Encerrando.");
      try {
        await client.destroy();
      } catch (_) {}
      process.exit(0);
    }
    if (!cronScheduled) {
      cron.schedule(CRON_EXPR, runJob, { timezone: "America/Sao_Paulo" });
      cronScheduled = true;
      logger.info(`Cron agendado: a cada ${config.cronIntervalMinutes} minuto(s).`);
    }
    await runJob();
  });

  if (!config.singleRun) {
    client.on("disconnected", () => {
      logger.info("Tentando reconectar em 30s...");
      setTimeout(() => {
        if (!isRunning) {
          client = createClient();
          client.initialize().catch((e) => logger.error("Erro ao reconectar:", e.message));
        }
      }, 30000);
    });
  }

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
