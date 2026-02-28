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
  {
    slug: "fitness",
    keywords: [
      "fitness", "academia", "musculação", "musculacao", "treino", "suplemento",
      "whey", "proteína", "proteina", "creatina", "pré-treino", "pre treino",
      "bcaa", "termogênico", "termogenico", "colchonete", "peso", "halter",
      "elástico", "elastico", "corda", "pular", "abdominal", "esteira",
      "bicicleta ergométrica", "ergometrica", "luvas academia", "cinta",
    ],
  },
];

const SLUG_OUTROS = "outros";
const SLUG_OFERTA_DO_DIA = "oferta-do-dia";
const DESCONTO_MIN_OFERTA_DIA = 40;

/**
 * Infere o slug da categoria a partir do título (e opcionalmente do desconto).
 * Oferta do dia: somente quando desconto > 40% e nenhuma outra categoria bateu.
 * Caso contrário, fallback em "outros".
 */
export function inferCategorySlugFromTitle(
  title: string,
  options?: { discountPct?: number | null }
): string {
  if (!title || typeof title !== "string") {
    return options?.discountPct != null && options.discountPct > DESCONTO_MIN_OFERTA_DIA
      ? SLUG_OFERTA_DO_DIA
      : SLUG_OUTROS;
  }
  const lower = title.toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "");

  for (const { slug, keywords } of CATEGORY_KEYWORDS) {
    for (const kw of keywords) {
      const kwNorm = kw.normalize("NFD").replace(/\p{Diacritic}/gu, "");
      if (lower.includes(kwNorm)) return slug;
    }
  }

  if (options?.discountPct != null && options.discountPct > DESCONTO_MIN_OFERTA_DIA) {
    return SLUG_OFERTA_DO_DIA;
  }
  return SLUG_OUTROS;
}
