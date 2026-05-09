import pkg from "whatsapp-web.js";
const { MessageMedia } = pkg;
import axios from "axios";
import { logger } from "./logger.js";
import { formatMessage } from "./formatter.js";
import { loadSentIds, markAsSent, postKey } from "./storage.js";
import { markPostAsPosted } from "./api.js";
import { config } from "./config.js";

/** URL da imagem: aceita imageUrl, image_url ou image (formato da API). */
function getImageUrl(post) {
  const url = post.imageUrl ?? post.image_url ?? post.image ?? "";
  return typeof url === "string" ? url.trim() : "";
}

/**
 * Baixa a imagem e retorna MessageMedia (fallback quando fromUrl falha, ex. em GHA).
 */
async function downloadImageAsMedia(imageUrl) {
  const res = await axios.get(imageUrl, {
    responseType: "arraybuffer",
    timeout: 20000,
    maxRedirects: 5,
    headers: { "User-Agent": "WhatsAppChannelBot/1.0" },
    validateStatus: (s) => s === 200,
  });
  const contentType = res.headers["content-type"] || "image/jpeg";
  const mimetype = contentType.split(";")[0].trim().toLowerCase() || "image/jpeg";
  const base64 = Buffer.from(res.data).toString("base64");
  return new MessageMedia(mimetype, base64);
}

/** Extrai o código de convite / pathname do canal a partir da URL ou devolve o valor já normalizado. */
function normalizeChatId(value) {
  let s = (value || "").trim().replace(/^["']+|["']+$/g, "").trim();
  if (!s) return "";
  try {
    if (/^https?:\/\//i.test(s)) {
      const u = new URL(s);
      const parts = u.pathname.split("/").filter(Boolean);
      const idx = parts.indexOf("channel");
      if (idx >= 0 && parts[idx + 1]) return parts[idx + 1];
    }
  } catch {
    /* fallback abaixo */
  }
  const match = s.match(/whatsapp\.com\/channel\/([^/?#\s]+)/i);
  if (match) return match[1];
  return s;
}

/** Log seguro (URLs longas não parecem `.../channel/0` por truncagem). */
function previewChatDest(s) {
  const t = String(s ?? "");
  if (t.length <= 72) return t;
  return `${t.slice(0, 40)}…${t.slice(-28)}`;
}

/**
 * Normaliza valor do secret: remove rótulo mb.health:, aspas; extrai 120363...@newsletter
 * se existir em qualquer linha (evita getChannelByInviteCode quebrado no WA Web).
 */
export function resolveDestinationChatId(raw) {
  let s = String(raw ?? "")
    .replace(/\r/g, "")
    .trim()
    .replace(/^["']+|["']+$/g, "")
    .trim();
  if (!s) return "";
  try {
    s = s.normalize("NFKC");
  } catch {
    /* ignore */
  }
  s = s.replace(/^\s*(?:mb\.)?(?:health|tech|ofertas|faith)\s*:\s*/i, "").trim();
  const jidRe = /\b(\d{10,}@newsletter)\b/i;
  const direct = s.match(jidRe);
  if (direct) return direct[1];
  for (const line of s.split(/[\n,;]+/)) {
    const m = line.trim().match(jidRe);
    if (m) return m[1];
  }
  return s.trim();
}

/** True quando já é só o JID do canal (…@newsletter), após resolveDestinationChatId. */
export function isNewsletterJidResolved(s) {
  return /^\d{10,}@newsletter$/i.test(String(s ?? "").trim());
}

/** ID serializado para sendMessage (whatsapp-web.js usa string ou objeto com _serialized). */
function serializeWhatsAppId(chatOrChannel) {
  if (!chatOrChannel) return null;
  if (typeof chatOrChannel === "string" && /@/.test(chatOrChannel)) return chatOrChannel;
  const ch = chatOrChannel;
  const fromObj =
    ch.id?._serialized ||
    (typeof ch.id === "string" && ch.id.includes("@") ? ch.id : null) ||
    ch._serialized ||
    (typeof ch.chatId === "string" && ch.chatId.includes("@") ? ch.chatId : null);
  return fromObj || null;
}

/** Retorna true se o valor parece ID interno (ex.: 120363xxx@g.us). */
function isInternalChatId(value) {
  return /@(g\.us|newsletter|c\.us)/.test(value);
}

/**
 * Resolve chat ou canal: ID interno -> getChatById; código de canal (ou URL) -> getChannelByInviteCode.
 * Pode retornar undefined se a lib não resolver (ex.: canal por link em alguns ambientes).
 */
async function getChatOrChannel(client, rawId) {
  const normalized = normalizeChatId(rawId);
  if (isInternalChatId(normalized)) {
    return client.getChatById(normalized);
  }
  if (typeof client.getChannelByInviteCode === "function") {
    return client.getChannelByInviteCode(normalized);
  }
  return client.getChatById(normalized);
}

/** Obtém o ID serializado para envio (client.sendMessage). Se chat for undefined mas rawId for ID interno, usa rawId. */
function getSendableChatId(chat, rawId) {
  const serialized = serializeWhatsAppId(chat);
  if (serialized) return serialized;
  const normalized = normalizeChatId(rawId);
  if (isInternalChatId(normalized)) return normalized;
  return null;
}

/**
 * Entrega o post a um único destino (sem marcar envio — uso interno ou composição).
 */
async function deliverPostToChat(client, post, rawId) {
  const dest = resolveDestinationChatId(rawId);
  if (!dest) {
    logger.warn("Destino vazio após normalizar CHAT_ID.");
    return false;
  }
  if (/^https?:\/\//i.test(dest) && !isNewsletterJidResolved(dest)) {
    logger.warn(
      `Destino parece só URL de convite (${previewChatDest(dest)}). Coloque no secret o ID no formato 120363...@newsletter (veja no log do bot: "Canais — use o ID abaixo").`
    );
  }

  const imageUrl = getImageUrl(post);
  const body = formatMessage(post);

  try {
    const chat = await getChatOrChannel(client, dest);
    const chatId = getSendableChatId(chat, dest);
    if (!chatId) {
      logger.warn(`Não foi possível resolver canal/chat para ${previewChatDest(dest)}`);
      return false;
    }
    if (imageUrl) {
      let media = null;
      try {
        media = await MessageMedia.fromUrl(imageUrl, { unsafeMime: true });
      } catch (fromUrlErr) {
        logger.warn("fromUrl falhou, tentando download com axios:", fromUrlErr.message);
        try {
          media = await downloadImageAsMedia(imageUrl);
        } catch (axiosErr) {
          logger.warn("Falha ao baixar imagem, enviando só texto:", axiosErr.message);
        }
      }
      if (media) {
        await client.sendMessage(chatId, media, { caption: body });
      } else {
        await client.sendMessage(chatId, body);
      }
    } else {
      await client.sendMessage(chatId, body);
    }
    const label = chat?.name || chatId;
    logger.info(`Enviado para ${label}: ${(post.title || post.url || "").slice(0, 40)}`);
    return true;
  } catch (err) {
    logger.error(`Erro ao enviar para ${previewChatDest(dest)}:`, err.message);
    if (!isInternalChatId(normalizeChatId(dest))) {
      logger.error("Canal: use em CHAT_ID o ID (ex.: 120363405814099508@newsletter).");
    }
    return false;
  }
}

/**
 * Um destino: marca envio + mark-posted na API (modo rodízio por canal).
 */
export async function sendPostToSingleDestination(client, post, rawChatId) {
  const key = postKey(post);
  const sentIds = loadSentIds(config.dataPath);
  if (sentIds.includes(key)) {
    logger.info(`Post já enviado (ignorado): ${key.slice(0, 60)}...`);
    return false;
  }

  const imageUrl = getImageUrl(post);
  if (config.skipPostsWithoutImage && !imageUrl) {
    logger.info(`Post sem imagem (ignorado por SKIP_POSTS_WITHOUT_IMAGE): ${(post.title || post.url || "").slice(0, 50)}...`);
    return false;
  }

  if (!String(rawChatId || "").trim()) {
    logger.warn("CHAT_ID vazio para este canal.");
    return false;
  }

  const resolved = resolveDestinationChatId(rawChatId);
  if (!resolved) {
    logger.warn("CHAT_ID inválido após normalização.");
    return false;
  }

  const ok = await deliverPostToChat(client, post, resolved);
  if (ok) {
    markAsSent(config.dataPath, key);
    await markPostAsPosted(config.markPostedUrl || config.apiUrl, post);
  }
  return ok;
}

/**
 * Envia um post para o destino configurado em CHAT_ID (ex.: 120363405814099508@newsletter).
 * Retorna true se enviou com sucesso para pelo menos um destino.
 */
export async function sendPost(client, post) {
  const key = postKey(post);
  const sentIds = loadSentIds(config.dataPath);
  if (sentIds.includes(key)) {
    logger.info(`Post já enviado (ignorado): ${key.slice(0, 60)}...`);
    return false;
  }

  const imageUrl = getImageUrl(post);
  if (config.skipPostsWithoutImage && !imageUrl) {
    logger.info(`Post sem imagem (ignorado por SKIP_POSTS_WITHOUT_IMAGE): ${(post.title || post.url || "").slice(0, 50)}...`);
    return false;
  }

  const chatIds = config.chatIds;

  if (chatIds.length === 0) {
    logger.warn("Nenhum CHAT_ID configurado. Configure CHAT_ID no .env.");
    return false;
  }

  let sent = false;
  for (const rawId of chatIds) {
    const ok = await deliverPostToChat(client, post, rawId);
    if (ok) sent = true;
  }

  if (sent) {
    markAsSent(config.dataPath, key);
    await markPostAsPosted(config.markPostedUrl || config.apiUrl, post);
  }
  return sent;
}

/**
 * Processa lista de posts: filtra já enviados e envia os novos.
 * Entre cada envio bem-sucedido aguarda config.delayBetweenPostsMinutes (padrão 10 min).
 */
export async function processPosts(client, posts) {
  const delayMs = config.delayBetweenPostsMinutes * 60 * 1000;
  let sentCount = 0;
  for (let i = 0; i < posts.length; i++) {
    const ok = await sendPost(client, posts[i]);
    if (ok) {
      sentCount++;
      if (delayMs > 0 && i < posts.length - 1) {
        logger.info(`Aguardando ${config.delayBetweenPostsMinutes} min antes do próximo envio...`);
        await new Promise((r) => setTimeout(r, delayMs));
      }
    }
  }
  return sentCount;
}
