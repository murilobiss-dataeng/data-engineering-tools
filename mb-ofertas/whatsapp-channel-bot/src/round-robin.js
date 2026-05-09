/**
 * Rodízio entre canais: em cada rodada envia no máximo 1 post por canal (health → tech → ofertas → faith);
 * depois aguarda DELAY_BETWEEN_POSTS_MINUTES antes da próxima rodada.
 */
import { logger } from "./logger.js";
import { config, buildFeedUrl } from "./config.js";
import { fetchPosts } from "./api.js";
import {
  sendPostToSingleDestination,
  resolveDestinationChatId,
  isNewsletterJidResolved,
} from "./sender.js";

export const ROUND_ROBIN_SLUGS = ["health", "tech", "ofertas", "faith"];

function splitChatIdMultiline(raw) {
  return String(raw ?? "")
    .replace(/\r/g, "")
    .split(/[\n,;]+/)
    .map((s) => s.trim().replace(/^["']+|["']+$/g, "").trim())
    .filter(Boolean);
}

/**
 * Um destino por canal: CHAT_ID_HEALTH / TECH / OFERTAS / FAITH.
 * Se algum estiver vazio, usa a linha correspondente de CHAT_ID (1ª=health, 2ª=tech, …) — útil quando só existe um secret multilinha no GitHub.
 */
export function chatIdEnvForSlug(slug) {
  const key = `CHAT_ID_${slug.toUpperCase()}`;
  const specific = String(process.env[key] ?? "")
    .replace(/\r/g, "")
    .trim()
    .replace(/^["']+|["']+$/g, "")
    .trim();
  if (specific) return specific;
  const parts = splitChatIdMultiline(process.env.CHAT_ID || "");
  const idx = ROUND_ROBIN_SLUGS.indexOf(slug);
  if (idx >= 0 && idx < parts.length) return parts[idx];
  return "";
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
      logger.info(
        `Rodízio: sem destino para o canal "${slug}" (CHAT_ID_${slug.toUpperCase()} vazio e sem linha em CHAT_ID) — ignorado.`
      );
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
    const key = `CHAT_ID_${slug.toUpperCase()}`;
    const directSet = Boolean(String(process.env[key] ?? "").replace(/\r/g, "").trim());
    const raw = chatIdEnvForSlug(slug);
    if (!raw) {
      logger.info(`Rodízio: sem destino para "${slug}" (${key} vazio e sem linha correspondente em CHAT_ID).`);
      continue;
    }
    const src = directSet ? key : "CHAT_ID (ordem: health → tech → ofertas → faith)";
    const resolved = resolveDestinationChatId(raw);
    if (isNewsletterJidResolved(resolved)) {
      logger.info(`Rodízio: canal "${slug}" → ID @newsletter ok (fonte: ${src}).`);
    } else {
      logger.warn(
        `Rodízio: canal "${slug}" — em ${src} não há um ID …@newsletter reconhecível. No GitHub use os secrets CHAT_ID_HEALTH / TECH / OFERTAS / FAITH ou um secret CHAT_ID com 4 linhas (uma JID por canal, na ordem acima).`
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
      await new Promise((resolve) => setTimeout(resolve, delayMs));
    }
  }

  logger.info(`Rodízio concluído. Total enviado nesta execução: ${totalSent}.`);
  return totalSent;
}
