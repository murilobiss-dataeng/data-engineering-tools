export type ProductType = "digital" | "affiliate";

export interface Product {
  id: string;
  slug: string;
  title: string;
  description: string;
  price?: number; // em centavos ou undefined para afiliado
  image: string; // URL ou path; use lib/placeholder para mock
  type: ProductType;
  affiliateUrl?: string;
  category: string;
}

export const products: Product[] = [
  {
    id: "1",
    slug: "ebook-salmos-para-o-dia-a-dia",
    title: "Salmos para o Dia a Dia",
    description: "E-book com 30 reflexões baseadas nos Salmos para fortalecer sua vida de oração.",
    price: 1990,
    image: "https://picsum.photos/seed/ebook1/400/300",
    type: "digital",
    category: "E-books",
  },
  {
    id: "2",
    slug: "guia-oracao-morning-prayer",
    title: "Guia de Oração Matinal",
    description: "PDF com orações e salmos organizados para começar o dia com paz.",
    price: 990,
    image: "https://picsum.photos/seed/guia2/400/300",
    type: "digital",
    category: "E-books",
  },
  {
    id: "3",
    slug: "biblia-estudo",
    title: "Bíblia de Estudo",
    description: "Bíblia com notas de estudo e referências cruzadas. Link para compra na Amazon.",
    image: "https://picsum.photos/seed/biblia3/400/300",
    type: "affiliate",
    affiliateUrl: "https://www.amazon.com.br/dp/8531112487?tag=salmododia-20",
    category: "Afiliados",
  },
  {
    id: "4",
    slug: "devocionario-30-dias",
    title: "Devocionário 30 Dias",
    description: "Um mês de meditações diárias. Entrega digital após a compra.",
    price: 1490,
    image: "https://picsum.photos/seed/devoc4/400/300",
    type: "digital",
    category: "E-books",
  },
  {
    id: "5",
    slug: "livro-salmos-ilustrados",
    title: "Salmos Ilustrados para Crianças",
    description: "Livro físico com os salmos mais amados, ilustrados. Comprar na Amazon.",
    image: "https://picsum.photos/seed/salmos5/400/300",
    type: "affiliate",
    affiliateUrl: "https://www.amazon.com.br/dp/6556890123?tag=salmododia-20",
    category: "Afiliados",
  },
];

export function getProductBySlug(slug: string): Product | undefined {
  return products.find((p) => p.slug === slug);
}

export function getDigitalProducts(): Product[] {
  return products.filter((p) => p.type === "digital");
}

export function getAffiliateProducts(): Product[] {
  return products.filter((p) => p.type === "affiliate");
}
