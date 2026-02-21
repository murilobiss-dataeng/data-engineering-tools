/**
 * Encurtador de links (extras).
 * - BITLY_ACCESS_TOKEN para Bitly.
 * - Ou implementar interno (redirect + tabela link_clicks para rastreamento).
 */
import { logger } from "../../config/logger.js";

export async function shortenUrl(longUrl: string): Promise<string> {
  // TODO: Bitly API ou redirect interno com tracking
  logger.debug({ longUrl }, "Shortener (passthrough)");
  return longUrl;
}
