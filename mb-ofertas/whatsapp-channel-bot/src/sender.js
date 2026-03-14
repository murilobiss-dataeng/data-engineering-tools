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

/** Extrai o código de convite do canal a partir da URL ou devolve o valor se já for código/ID. */
function normalizeChatId(value) {
  const s = (value || "").trim();
  const match = s.match(/whatsapp\.com\/channel\/([A-Za-z0-9_-]+)/);
  return match ? match[1] : s;
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
  if (chat?.id?._serialized) return chat.id._serialized;
  const normalized = normalizeChatId(rawId);
  if (isInternalChatId(normalized)) return normalized;
  return null;
}

/**
 * Envia um post para o destino configurado em CHAT_ID (ex.: 120363405814099508@newsletter).
 * Retorna true se enviou com sucesso.
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

  const body = formatMessage(post);
  const chatIds = config.chatIds;

  if (chatIds.length === 0) {
    logger.warn("Nenhum CHAT_ID configurado. Configure CHAT_ID no .env.");
    return false;
  }

  let sent = false;
  for (const rawId of chatIds) {
    try {
      const chat = await getChatOrChannel(client, rawId);
      const chatId = getSendableChatId(chat, rawId);
      if (!chatId) {
        logger.warn(`Não foi possível resolver canal/chat para ${rawId.slice(0, 40)}... Use o ID do canal em CHAT_ID (ex.: 120363405814099508@newsletter).`);
        continue;
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
      sent = true;
    } catch (err) {
      logger.error(`Erro ao enviar para ${rawId}:`, err.message);
      if (!isInternalChatId(normalizeChatId(rawId))) {
        logger.error("Canal: use em CHAT_ID o ID (ex.: 120363405814099508@newsletter). Obtenha o ID rodando o bot e vendo 'Canal resolvido pelo link'.");
      }
    }
  }

  if (sent) {
    markAsSent(config.dataPath, key);
    if (post.url) await markPostAsPosted(config.apiUrl, post.url);
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
