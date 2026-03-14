import axios from "axios";
import { logger } from "./logger.js";

/**
 * Busca posts na API do site.
 * Espera array: [{ title, text, url, imageUrl? }]
 */
export async function fetchPosts(apiUrl) {
  if (!apiUrl) {
    logger.warn("API_URL não configurada.");
    return [];
  }
  try {
    const { data } = await axios.get(apiUrl, {
      timeout: 15000,
      headers: { Accept: "application/json" },
      validateStatus: (status) => status >= 200 && status < 300,
    });
    const list = Array.isArray(data) ? data : [];
    logger.info(`API retornou ${list.length} post(s).`);
    return list.filter((p) => p && (p.url || p.title || p.text));
  } catch (err) {
    logger.error("Erro ao buscar posts na API:", err.message);
    if (err.response) logger.error("Status:", err.response.status, "Data:", err.response.data);
    return [];
  }
}
