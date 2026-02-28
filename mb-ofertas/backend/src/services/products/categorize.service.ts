/**
 * Categoriza produto pelo título (keywords) para segmentação em canais WhatsApp.
 * Retorna o slug da categoria; usado ao inserir produto ou ao editar.
 */
const CATEGORY_KEYWORDS: { slug: string; keywords: string[] }[] = [
  {
    slug: "eletronicos",
    keywords: [
      "celular", "smartphone", "iphone", "samsung", "xiaomi", "motorola",
      "notebook", "laptop", "computador", "pc", "tablet", "ipad",
      "fone", "fone de ouvido", "headset", "airpods", "earphone",
      "tv", "televisão", "monitor", "smart tv", "fire tv",
      "smartwatch", "relógio inteligente", "watch",
      "câmera", "webcam", "mouse", "teclado", "ssd", "hd externo",
      "fritadeira", "air fryer", "liquidificador", "cafeteira", "micro-ondas",
      "geladeira", "lavadora", "secadora", "aspirador", "robô",
      "eletrônico", "eletronicos", "gamer", "console", "playstation", "xbox", "nintendo",
    ],
  },
  {
    slug: "livros",
    keywords: [
      "livro", "livros", "obra", "romance", "literatura", "best-seller",
      "infantil", "infantis", "didático", "enciclopédia", "biografia",
      "quadrinhos", "hq", "manga", "comics",
    ],
  },
  {
    slug: "catolicos",
    keywords: [
      "terço", "terco", "rosário", "rosario", "bíblia", "biblia",
      "santo", "santa", "católico", "catolico", "cristão", "cristao",
      "cruz", "crucifixo", "imagem", "quadro religioso", "nossa senhora",
      "são josé", "sao jose", "padre", "missal", "devocionário",
    ],
  },
  {
    slug: "casa",
    keywords: [
      "panela", "panelas", "frigideira", "talheres", "louça", "louca",
      "cama", "colchão", "colchon", "travesseiro", "lençol", "lencol",
      "sofá", "sofa", "cadeira", "mesa", "estante", "armário", "armario",
      "decoração", "decoracao", "cortina", "tapete", "luminária", "luminaria",
      "organizador", "caixa organizadora", "cozinha", "banheiro",
      "ferramenta", "parafusadeira", "furadeira", "chave", "martelo",
      "jardinagem", "vaso", "planta", "grama", "mangueira",
      "limpeza", "vassoura", "rodo", "balde", "desinfetante",
    ],
  },
];

const DEFAULT_SLUG = "ofertas-do-dia";

/**
 * Infere o slug da categoria a partir do título do produto (e opcionalmente da fonte).
 * Útil para segmentar ofertas por canal WhatsApp.
 */
export function inferCategorySlugFromTitle(title: string): string {
  if (!title || typeof title !== "string") return DEFAULT_SLUG;
  const lower = title.toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "");

  for (const { slug, keywords } of CATEGORY_KEYWORDS) {
    for (const kw of keywords) {
      const kwNorm = kw.normalize("NFD").replace(/\p{Diacritic}/gu, "");
      if (lower.includes(kwNorm)) return slug;
    }
  }

  return DEFAULT_SLUG;
}
