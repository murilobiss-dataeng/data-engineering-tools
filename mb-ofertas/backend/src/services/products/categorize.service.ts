/**
 * Categoriza produto pelos slugs usados nos canais:
 * `health`, `tech`, `ofertas`, `faith` e `fitness`.
 */
const CATEGORY_KEYWORDS: { slug: string; keywords: string[] }[] = [
  {
    slug: "health",
    keywords: [
      "whey",
      "creatina",
      "suplemento",
      "vitamina",
      "multivitaminico",
      "omega 3",
      "colageno",
      "bcaa",
      "glutamina",
      "termogenico",
      "melatonina",
      "protein",
      "proteina",
      "capsulas",
      "saude",
      "imunidade",
      "pre treino",
      "pre-treino",
    ],
  },
  {
    slug: "fitness",
    keywords: [
      "fitness",
      "academia",
      "musculacao",
      "treino",
      "halter",
      "peso",
      "anilha",
      "esteira",
      "ergometrica",
      "bicicleta ergometrica",
      "colchonete",
      "elastico",
      "corda de pular",
      "luvas academia",
      "faixa elastica",
      "par de dumbbell",
    ],
  },
  {
    slug: "tech",
    keywords: [
      "celular",
      "smartphone",
      "iphone",
      "samsung",
      "xiaomi",
      "motorola",
      "notebook",
      "laptop",
      "computador",
      "pc",
      "tablet",
      "ipad",
      "fone",
      "headset",
      "airpods",
      "monitor",
      "smart tv",
      "tv",
      "smartwatch",
      "ssd",
      "hd externo",
      "mouse",
      "teclado",
      "roteador",
      "wifi",
      "webcam",
      "microfone",
      "gpu",
      "placa de video",
      "console",
      "playstation",
      "xbox",
      "nintendo",
    ],
  },
  {
    slug: "faith",
    keywords: [
      "biblia",
      "salmos",
      "evangelho",
      "devocional",
      "livro cristao",
      "livro evangelico",
      "terco",
      "crucifixo",
      "cruz",
      "imagem de santo",
      "catolico",
      "cristao",
      "gospel",
      "oracao",
      "religioso",
      "presente cristao",
      "quadro biblico",
    ],
  },
];

const SLUG_OFERTAS = "ofertas";

/**
 * Infere o slug da categoria a partir do título.
 * Todo item não reconhecido cai em `ofertas`, para sempre ter canal de fallback.
 */
export function inferCategorySlugFromTitle(
  title: string,
  options?: { discountPct?: number | null }
): string {
  if (!title || typeof title !== "string") {
    return SLUG_OFERTAS;
  }
  const lower = title.toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "");

  for (const { slug, keywords } of CATEGORY_KEYWORDS) {
    for (const kw of keywords) {
      const kwNorm = kw.normalize("NFD").replace(/\p{Diacritic}/gu, "");
      if (lower.includes(kwNorm)) return slug;
    }
  }
  return SLUG_OFERTAS;
}
