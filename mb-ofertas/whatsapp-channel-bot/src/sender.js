import pkg from "whatsapp-web.js";
const { MessageMedia } = pkg;
import { logger } from "./logger.js";
import { formatMessage } from "./formatter.js";
import { loadSentIds, markAsSent, postKey } from "./storage.js";
import { config } from "./config.js";

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
      if (post.imageUrl) {
        try {
          const media = await MessageMedia.fromUrl(post.imageUrl, { unsafeMime: true });
          await chat.sendMessage(media, { caption: body });
        } catch (imgErr) {
          logger.warn("Falha ao baixar/enviar imagem, enviando só texto:", imgErr.message);
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
