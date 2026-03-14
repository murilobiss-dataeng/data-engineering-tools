import pkg from "whatsapp-web.js";
const { MessageMedia } = pkg;
import axios from "axios";
import { logger } from "./logger.js";
import { formatMessage } from "./formatter.js";
import { loadSentIds, markAsSent, postKey } from "./storage.js";
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

/**
 * Envia um post para todos os CHAT_IDS configurados.
 * CHAT_IDS pode ser: ID interno (ex.: 120363xxx@g.us), código do canal (ex.: 0029VbBg6l4DDmFNz3FmUe2T) ou URL (https://whatsapp.com/channel/...).
 * Retorna true se enviou com sucesso em pelo menos um chat.
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
    logger.warn("Nenhum CHAT_ID configurado. Configure CHAT_IDS no .env.");
    return false;
  }

  let sent = false;
  for (const rawId of chatIds) {
    try {
      const chat = await getChatOrChannel(client, rawId);
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
          await chat.sendMessage(media, { caption: body });
        } else {
          await chat.sendMessage(body);
        }
      } else {
        await chat.sendMessage(body);
      }
      const label = chat.name || chat.id?._serialized || rawId;
      logger.info(`Enviado para ${label}: ${(post.title || post.url || "").slice(0, 40)}`);
      sent = true;
    } catch (err) {
      logger.error(`Erro ao enviar para ${rawId}:`, err.message);
      if (!isInternalChatId(normalizeChatId(rawId))) {
        logger.error("Canal: confira se CHAT_IDS tem a URL (https://whatsapp.com/channel/CODIGO) ou o código e se esta conta é admin do canal.");
      }
    }
  }

  if (sent) {
    markAsSent(config.dataPath, key);
  }
  return sent;
}

/**
 * Processa lista de posts: filtra já enviados e envia os novos.
 */
export async function processPosts(client, posts) {
  let sentCount = 0;
  for (const post of posts) {
    const ok = await sendPost(client, post);
    if (ok) sentCount++;
  }
  return sentCount;
}
