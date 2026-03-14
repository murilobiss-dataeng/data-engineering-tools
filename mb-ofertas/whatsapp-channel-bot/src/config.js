import "dotenv/config";

/**
 * Configuração via variáveis de ambiente.
 */
export const config = {
  /** URL da API que retorna array de posts: [{ title, text, url, imageUrl? }] */
  apiUrl: process.env.API_URL || "",
  /** IDs dos chats (grupos/canais) separados por vírgula */
  chatIds: (process.env.CHAT_IDS || "")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean),
  /** Intervalo em minutos entre cada verificação */
  cronIntervalMinutes: Math.max(1, parseInt(process.env.CRON_INTERVAL_MINUTES || "10", 10)),
  /** Pasta para sessão (LocalAuth) e arquivo de enviados */
  dataPath: process.env.DATA_PATH || "./data",
  /** clientId para LocalAuth (apenas alfanumérico, _ e -) */
  authClientId: process.env.AUTH_CLIENT_ID || "channel_bot",
};
