import axios from "axios";
import { logger } from "./logger.js";

/**
 * Busca posts na API do site.
 * Espera array: [{ title, text, url, imageUrl? }]
 * Timeout maior e retry para cold start da API (ex.: Render).
 */
export async function fetchPosts(apiUrl, options = {}) {
  const { timeout = 45000, retries = 1 } = options;
  if (!apiUrl) {
    logger.warn("API_URL não configurada.");
    return [];
  }
  let lastErr = null;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      if (attempt > 0) {
        logger.info(`Retentando API em 5s (tentativa ${attempt + 1}/${retries + 1})...`);
        await new Promise((r) => setTimeout(r, 5000));
      }
      const { data } = await axios.get(apiUrl, {
        timeout,
        headers: { Accept: "application/json" },
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
