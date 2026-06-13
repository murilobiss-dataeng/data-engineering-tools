import axios from "axios";
import { logger } from "./logger.js";

/** Base para links curtos (/r/CODE). Prioridade: SHORT_LINK_BASE_URL > origem da API_URL. */
function resolveShortLinkBase(apiUrl) {
  const explicit = (process.env.SHORT_LINK_BASE_URL || "").trim().replace(/\/$/, "");
  if (explicit) return explicit;
  if (!apiUrl) return "";
  try {
    const u = new URL(apiUrl);
    return `${u.protocol}//${u.host}`;
  } catch {
    return "";
  }
}

/**
 * Busca posts na API do site.
 * Espera array: [{ title, text, url, imageUrl? }]
 * Timeout maior e retry para cold start da API (ex.: Render).
 */
export async function fetchPosts(apiUrl, options = {}) {
  const { timeout = 45000, retries = 1, shortLinkBase } = options;
  if (!apiUrl) {
    logger.warn("API_URL não configurada.");
    return [];
  }
  const linkBase = shortLinkBase || resolveShortLinkBase(apiUrl);
  const headers = { Accept: "application/json" };
  if (linkBase) headers["X-Short-Link-Base"] = linkBase;
  let lastErr = null;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      if (attempt > 0) {
        logger.info(`Retentando API em 5s (tentativa ${attempt + 1}/${retries + 1})...`);
        await new Promise((r) => setTimeout(r, 5000));
      }
      const { data } = await axios.get(apiUrl, {
        timeout,
        headers,
        validateStatus: (status) => status >= 200 && status < 300,
      });
      const list = Array.isArray(data) ? data : [];
      logger.info(`API retornou ${list.length} post(s).`);
      return list.filter((p) => p && (p.url || p.title || p.text));
    } catch (err) {
      lastErr = err;
      logger.warn("Tentativa API:", err.message);
      if (err.response) logger.warn("Status:", err.response.status);
    }
  }
  logger.error("Erro ao buscar posts na API:", lastErr?.message);
  if (lastErr?.response) logger.error("Status:", lastErr.response.status, "Data:", lastErr.response?.data);
  return [];
}

/**
 * Marca o produto como postado na API (status = 'sent'). Remove da lista de aprovados.
 * Preferir post.id (vem no feed); post.url é fallback.
 */
export async function markPostAsPosted(apiUrl, post) {
  if (!apiUrl) return false;
  const id = post?.id ? String(post.id).trim() : "";
  const url = post?.url ? String(post.url).trim() : "";
  if (!id && !url) return false;
  let markPostedUrl = apiUrl;
  try {
    const u = new URL(apiUrl);
    u.pathname = u.pathname.replace(/\/feed\/?$/, "/feed/mark-posted");
    u.search = "";
    markPostedUrl = u.toString();
  } catch {
    markPostedUrl = apiUrl.replace(/\/feed\/?(\?.*)?$/i, "/feed/mark-posted");
  }
  const body = id ? { id } : { url };
  try {
    const { status } = await axios.post(markPostedUrl, body, {
      timeout: 15000,
      headers: { "Content-Type": "application/json" },
      validateStatus: () => true,
    });
    if (status >= 200 && status < 300) {
      logger.info("Produto removido da lista de aprovados (mark-posted).");
      return true;
    }
    if (status === 404) logger.warn("mark-posted: produto não encontrado na API.");
    else logger.warn("mark-posted: API retornou", status);
    return false;
  } catch (err) {
    logger.warn("mark-posted falhou:", err.message);
    return false;
  }
}

/**
 * Dispara busca de produtos na API quando a fila do canal está baixa.
 */
export async function triggerRefetchIfLow(apiUrl, channelSlug, currentCount, minCount = 10) {
  if (!apiUrl || currentCount >= minCount) return false;
  let fetchUrl = apiUrl;
  try {
    const u = new URL(apiUrl);
    u.pathname = u.pathname.replace(/\/feed\/?$/, "/fetch-ofertas");
    u.search = "";
    fetchUrl = u.toString();
  } catch {
    fetchUrl = apiUrl.replace(/\/feed\/?(\?.*)?$/i, "/fetch-ofertas");
  }
  try {
    logger.info(`Fila "${channelSlug}" baixa (${currentCount} < ${minCount}). Disparando fetch-ofertas...`);
    await axios.post(
      fetchUrl,
      {},
      { timeout: 120000, headers: { "Content-Type": "application/json" }, validateStatus: () => true }
    );
    return true;
  } catch (err) {
    logger.warn("Refetch automático falhou:", err.message);
    return false;
  }
}
