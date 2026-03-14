import { MessageMedia } from "whatsapp-web.js";
import { logger } from "./logger.js";
import { formatMessage } from "./formatter.js";
import { loadSentIds, markAsSent, postKey } from "./storage.js";
import { config } from "./config.js";

/**
 * Envia um post para todos os CHAT_IDS configurados.
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
  for (const chatId of chatIds) {
    try {
      const chat = await client.getChatById(chatId);
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
      logger.info(`Enviado para ${chatId}: ${(post.title || post.url || "").slice(0, 40)}`);
      sent = true;
    } catch (err) {
      logger.error(`Erro ao enviar para ${chatId}:`, err.message);
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
