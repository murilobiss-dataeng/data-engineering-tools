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
import { isRoundRobinMode, runRoundRobinJob } from "./round-robin.js";

const isGHA = process.env.GITHUB_ACTIONS === "true";

if (!fs.existsSync(config.dataPath)) {
  fs.mkdirSync(config.dataPath, { recursive: true });
  logger.info("Pasta de dados criada:", config.dataPath);
}
const AUTH_PATH = path.join(config.dataPath, ".wwebjs_auth");
const CRON_EXPR = `*/${config.cronIntervalMinutes} * * * *`; // a cada N minutos

/** Um único conjunto de opções para toDataURL e toFile (evita QR “diferente” do workflow). */
const QR_IMAGE_OPTS = {
  margin: 4,
  width: 768,
  errorCorrectionLevel: "M",
};

const MODERN_CHROME_UA =
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36";

/** No GHA o cache restaura a pasta da sessão; locks do Chromium de um job cancelado impedem novo launch. */
function removeChromiumProfileLocksSync(dir) {
  if (!fs.existsSync(dir)) return;
  let list;
  try {
    list = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const e of list) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) {
      removeChromiumProfileLocksSync(full);
    } else if (
      e.name === "SingletonLock" ||
      e.name === "SingletonCookie" ||
      e.name === "SingletonSocket"
    ) {
      try {
        fs.unlinkSync(full);
        if (isGHA) logger.info("Lock do Chromium removido (evita 'profile in use'):", full);
      } catch (_) {}
    }
  }
}

let client = null;
let isRunning = false;
let cronScheduled = false;
let qrAlreadyShown = false;
/** No GHA: o WhatsApp renova o QR muitas vezes — só logamos instruções uma vez; os ficheiros continuam a atualizar. */
let ghaQrInstructionsLogged = false;

function createClient() {
  const auth = new LocalAuth({
    clientId: config.authClientId,
    dataPath: AUTH_PATH,
  });

  const c = new Client({
    authStrategy: auth,
    authTimeoutMs: 120000,
    qrMaxRetries: 0,
    takeoverOnConflict: true,
    takeoverTimeoutMs: 10000,
    userAgent: MODERN_CHROME_UA,
    puppeteer: {
      headless: true,
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        `--user-agent=${MODERN_CHROME_UA}`,
      ],
    },
  });

  c.on("qr", async (qr) => {
    // No GHA o WhatsApp renova o QR; gravamos cada versão. Só uma fonte de imagem: o bot (não re-gerar no workflow).
    if (!isGHA && qrAlreadyShown) return;
    if (!isGHA) qrAlreadyShown = true;

    const payload = typeof qr === "string" ? qr : String(qr ?? "");
    if (!payload) {
      logger.warn("Evento qr sem payload; ignorando.");
      return;
    }

    if (!isGHA || !ghaQrInstructionsLogged) {
      logger.info("Escaneie o QR em Aparelhos conectados (Linked devices):");
      logger.info(
        "Ligue o bot só a uma conta: use o app WhatsApp normal ou o WhatsApp Business (não misture). Business: app WhatsApp Business, menu, Aparelhos conectados, Conectar um aparelho."
      );
      logger.info(
        "Se só o Messenger funcionar: apague data/.wwebjs_auth (ou mude AUTH_CLIENT_ID), desvincule aparelhos no telefone e escaneie de novo com o app desejado."
      );
      if (isGHA) ghaQrInstructionsLogged = true;
    }
    if (isGHA) {
      try {
        const qrDataUrl = await QRCode.toDataURL(payload, QR_IMAGE_OPTS);
        const qrFilePath = path.resolve(config.dataPath, "qr-url.txt");
        fs.writeFileSync(qrFilePath, qrDataUrl, "utf-8");
        const qrPngPath = path.resolve(config.dataPath, "qr.png");
        await QRCode.toFile(qrPngPath, payload, QR_IMAGE_OPTS);
        const qrRawPath = path.resolve(config.dataPath, "qr-raw.txt");
        fs.writeFileSync(qrRawPath, payload, "utf-8");
      } catch (e) {
        logger.warn("Não foi possível salvar QR:", e.message);
      }
    } else {
      qrcode.generate(payload, { small: true });
      const qrFilePath = path.resolve(config.dataPath, "qr-url.txt");
      try {
        const qrDataUrl = await QRCode.toDataURL(payload, QR_IMAGE_OPTS);
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

  c.on("change_state", (state) => {
    logger.info("Estado do WhatsApp:", state);
    if (state === "DEPRECATED_VERSION") {
      logger.error("O WhatsApp Web reportou versão obsoleta.");
    }
    if (state === "TOS_BLOCK" || state === "SMB_TOS_BLOCK") {
      logger.error("A conta foi bloqueada ou restringida pelo WhatsApp Web.");
    }
  });

  c.on("disconnected", (reason) => {
    logger.warn("WhatsApp desconectado:", reason);
    isRunning = false;
  });

  return c;
}

async function runScheduledWork() {
  if (isRoundRobinMode()) {
    const n = await runRoundRobinJob(client);
    if (n > 0) logger.info(`${n} envio(s) no rodízio.`);
    return;
  }
  await runJob();
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

  const feedUrl = config.feedUrl || config.apiUrl;
  logger.info("Buscando novos posts na API...", config.channelSlug ? `(canal: ${config.channelSlug})` : "(todos os canais)");
  const apiOptions = config.singleRun ? { timeout: 60000, retries: 2 } : { timeout: 30000, retries: 1 };
  const posts = await fetchPosts(feedUrl, apiOptions);
  if (posts.length === 0) return;

  const sent = await processPosts(client, posts);
  if (sent > 0) {
    logger.info(`${sent} post(s) enviado(s).`);
  }
}

async function start() {
  const modeLabel = isRoundRobinMode()
    ? "rodízio (health→tech→ofertas→faith, pausa entre rodadas)"
    : config.singleRun
      ? "single-run (GHA)"
      : `intervalo ${config.cronIntervalMinutes} min`;
  logger.info("Iniciando bot. Modo:", modeLabel);
  logger.info("API:", config.apiUrl || "(não configurada)", config.channelSlug ? `CHANNEL_SLUG=${config.channelSlug}` : "");
  if (isRoundRobinMode()) {
    logger.info(
      "Rodízio: destinos = CHAT_ID_HEALTH, CHAT_ID_TECH, CHAT_ID_OFERTAS, CHAT_ID_FAITH (secrets do workflow), ou 4 linhas no secret CHAT_ID na mesma ordem."
    );
  }
  logger.info("Chats (modo normal / CHAT_ID):", config.chatIds.length ? config.chatIds : "(nenhum)");

  if (isGHA) {
    removeChromiumProfileLocksSync(AUTH_PATH);
  }

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
      let s = (v || "").trim().replace(/^["']+|["']+$/g, "").trim();
      if (!s) return s;
      try {
        if (/^https?:\/\//i.test(s)) {
          const u = new URL(s);
          const parts = u.pathname.split("/").filter(Boolean);
          const idx = parts.indexOf("channel");
          if (idx >= 0 && parts[idx + 1]) return parts[idx + 1];
        }
      } catch (_) {}
      const m = s.match(/whatsapp\.com\/channel\/([^/?#\s]+)/i);
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
          logger.info("Nenhum canal na lista (normal no GHA/headless). Use CHAT_ID com o ID do canal (ex.: 120363405814099508@newsletter).");
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
      await runScheduledWork();
      logger.info("Single-run: envio concluído. Encerrando.");
      try {
        await client.destroy();
      } catch (_) {}
      process.exit(0);
    }
    if (!cronScheduled) {
      cron.schedule(CRON_EXPR, runScheduledWork, { timezone: "America/Sao_Paulo" });
      cronScheduled = true;
      logger.info(`Cron agendado: a cada ${config.cronIntervalMinutes} minuto(s).`);
    }
    await runScheduledWork();
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
