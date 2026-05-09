/**
 * Rodízio entre canais: em cada rodada envia no máximo 1 post por canal (health → tech → ofertas → faith);
 * depois aguarda DELAY_BETWEEN_POSTS_MINUTES antes da próxima rodada.
 */
import { logger } from "./logger.js";
import { config, buildFeedUrl } from "./config.js";
import { fetchPosts } from "./api.js";
import { sendPostToSingleDestination, resolveDestinationChatId } from "./sender.js";

export const ROUND_ROBIN_SLUGS = ["health", "tech", "ofertas", "faith"];

function chatIdEnvForSlug(slug) {
  const map = {
    health: process.env.CHAT_ID_HEALTH,
    tech: process.env.CHAT_ID_TECH,
    ofertas: process.env.CHAT_ID_OFERTAS,
    faith: process.env.CHAT_ID_FAITH,
  };
  return String(map[slug] ?? "").trim();
}

export function isRoundRobinMode() {
  const v = process.env.ROUND_ROBIN_CHANNELS || "";
  return v === "true" || v === "1";
}

/**
 * Busca as filas por canal e envia em rodadas até esgotar.
 */
export async function runRoundRobinJob(client) {
  if (!config.apiUrl) {
    logger.warn("API_URL não configurada.");
    return 0;
  }

  const apiOptions = config.singleRun ? { timeout: 60000, retries: 2 } : { timeout: 30000, retries: 1 };
  const lists = {};
  const indices = {};

  for (const slug of ROUND_ROBIN_SLUGS) {
    const cid = chatIdEnvForSlug(slug);
    if (!cid) {
      logger.info(`Rodízio: sem CHAT_ID_* para o canal "${slug}" — ignorado.`);
      lists[slug] = [];
      indices[slug] = 0;
      continue;
    }
    const feedUrl = buildFeedUrl(config.apiUrl, slug);
    const posts = await fetchPosts(feedUrl, apiOptions);
    lists[slug] = posts;
    indices[slug] = 0;
    logger.info(`Rodízio: fila ${slug} — ${posts.length} post(s).`);
  }

  for (const slug of ROUND_ROBIN_SLUGS) {
    const raw = chatIdEnvForSlug(slug);
    if (!raw) continue;
    const r = resolveDestinationChatId(raw);
    const hasNewsletterJid = /\d{10,22}@newsletter$/i.test(r);
    if (hasNewsletterJid) {
      logger.info(`Rodízio: canal "${slug}" → ID newsletter (ok para envio).`);
    } else {
      logger.warn(
        `Rodízio: canal "${slug}" — o secret não contém um ID …@newsletter reconhecido. Corrija CHAT_ID_${slug.toUpperCase()} no GitHub (use o ID que o bot lista em "Canais").`
      );
    }
  }

  const delayMs = config.delayBetweenPostsMinutes * 60 * 1000;
  let totalSent = 0;
  let round = 0;

  const anyQueueHasWork = () =>
    ROUND_ROBIN_SLUGS.some((slug) => indices[slug] < lists[slug].length);

  if (!anyQueueHasWork()) {
    logger.info("Rodízio: nenhum post pendente em nenhum canal.");
    return 0;
  }

  while (anyQueueHasWork()) {
    round += 1;
    logger.info(`Rodízio: rodada ${round} (health → tech → ofertas → faith)`);

    for (const slug of ROUND_ROBIN_SLUGS) {
      const rawChatId = chatIdEnvForSlug(slug);
      if (!rawChatId) continue;
      const list = lists[slug];
      const i = indices[slug];
      if (i >= list.length) continue;

      const post = list[i];
      indices[slug] = i + 1;

      const ok = await sendPostToSingleDestination(client, post, rawChatId);
      if (ok) totalSent++;
    }

    if (!anyQueueHasWork()) break;

    if (delayMs > 0) {
      logger.info(
        `Rodízio: aguardando ${config.delayBetweenPostsMinutes} min antes da próxima rodada...`
      );
      await new Promise((r) => setTimeout(r, delayMs));
    }
  }

  logger.info(`Rodízio concluído. Total enviado nesta execução: ${totalSent}.`);
  return totalSent;
}
