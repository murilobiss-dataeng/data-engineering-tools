import "dotenv/config";

/**
 * Monta URL do feed com filtro por canal (slug da categoria: health, tech, ofertas, faith).
 */
function buildFeedUrl(apiUrl, channelSlug) {
  const base = (apiUrl || "").trim();
  if (!base) return "";
  const slug = (channelSlug || "").trim();
  if (!slug) return base;
  try {
    const u = new URL(base);
    u.searchParams.set("channelSlug", slug);
    return u.toString();
  } catch {
    return base;
  }
}

/**
 * POST /api/products/feed/mark-posted — pathname derivado da URL do feed, sem query string.
 */
function buildMarkPostedUrl(feedOrApiUrl) {
  const base = (feedOrApiUrl || "").trim();
  if (!base) return "";
  try {
    const u = new URL(base);
    u.pathname = u.pathname.replace(/\/feed\/?$/, "/feed/mark-posted");
    u.search = "";
    return u.toString();
  } catch {
    return base.replace(/\/feed\/?(\?.*)?$/i, "/feed/mark-posted");
  }
}

/**
 * Um ou vários destinos: separados por vírgula, ponto e vírgula ou quebra de linha (útil em secrets do GitHub).
 * Remove aspas acidentais em volta do valor.
 */
function parseChatIdsFromEnv() {
  const raw = process.env.CHAT_ID || "";
  return raw
    .split(/[\n,;]+/)
    .map((s) => s.trim().replace(/^["']+|["']+$/g, "").trim())
    .filter(Boolean);
}

/**
 * Configuração via variáveis de ambiente.
 */
export const config = {
  /** URL base da API (ex.: https://api.example.com/api/products/feed) */
  apiUrl: process.env.API_URL || "",
  /** Slug do canal/categoria (mesmo slug das categorias no painel). Opcional: sem isso, o feed traz todos os aprovados. */
  channelSlug: (process.env.CHANNEL_SLUG || "").trim(),
  /** URL usada no GET (apiUrl + ?channelSlug= quando CHANNEL_SLUG está definido) */
  get feedUrl() {
    const u = buildFeedUrl(this.apiUrl, this.channelSlug);
    return u || this.apiUrl;
  },
  /** URL do mark-posted (sem query) */
  get markPostedUrl() {
    return buildMarkPostedUrl(this.feedUrl || this.apiUrl);
  },
  /** IDs dos canais/chats (ex.: 120363405814099508@newsletter). CHAT_ID pode listar vários separados por vírgula ou linha. */
  chatIds: parseChatIdsFromEnv(),
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
  /** Pausa em minutos entre cada post enviado (evita flood no canal). Padrão: 10. */
  delayBetweenPostsMinutes: Math.max(0, parseInt(process.env.DELAY_BETWEEN_POSTS_MINUTES || "10", 10)),
};
