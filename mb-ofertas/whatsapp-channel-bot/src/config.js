import "dotenv/config";

/**
 * Configuração via variáveis de ambiente.
 */
export const config = {
  /** URL da API que retorna array de posts: [{ title, text, url, imageUrl? }] */
  apiUrl: process.env.API_URL || "",
  /** ID do canal (ex.: 120363405814099508@newsletter). Única variável de destino. */
  chatIds: (() => {
    const id = (process.env.CHAT_ID || "").trim();
    return id ? [id] : [];
  })(),
  /** Intervalo em minutos entre cada verificação */
  cronIntervalMinutes: Math.max(1, parseInt(process.env.CRON_INTERVAL_MINUTES || "10", 10)),
  /** Pasta para sessão (LocalAuth) e arquivo de enviados */
  dataPath: process.env.DATA_PATH || "./data",
  /** clientId para LocalAuth (apenas alfanumérico, _ e -) */
  authClientId: process.env.AUTH_CLIENT_ID || "channel_bot",
  /** Em true: conecta, envia uma vez e encerra (uso no GitHub Actions) */
  singleRun: process.env.SINGLE_RUN === "true" || process.env.SINGLE_RUN === "1" || process.env.GITHUB_ACTIONS === "true",
  /** Em true: não envia posts sem imagem (só envia quando tiver imageUrl) — bom para engajamento */
  skipPostsWithoutImage: process.env.SKIP_POSTS_WITHOUT_IMAGE !== "false" && process.env.SKIP_POSTS_WITHOUT_IMAGE !== "0",
};
