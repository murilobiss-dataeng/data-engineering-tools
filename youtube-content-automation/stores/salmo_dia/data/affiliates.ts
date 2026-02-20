export interface AffiliateProduct {
  id: string;
  title: string;
  description: string;
  image: string;
  url: string;
  tag: string; // tag de afiliado Amazon
}

export const affiliateProducts: AffiliateProduct[] = [
  {
    id: "a1",
    title: "Bíblia de Estudo",
    description: "Bíblia com notas de estudo e referências. Ideal para aprofundar na Palavra.",
    image: "https://picsum.photos/seed/biblia3/400/300",
    url: "https://www.amazon.com.br/dp/8531112487?tag=salmododia-20",
    tag: "salmododia-20",
  },
  {
    id: "a2",
    title: "Salmos Ilustrados para Crianças",
    description: "Os salmos mais amados em linguagem e imagens para os pequenos.",
    image: "https://picsum.photos/seed/salmos5/400/300",
    url: "https://www.amazon.com.br/dp/6556890123?tag=salmododia-20",
    tag: "salmododia-20",
  },
  {
    id: "a3",
    title: "Devocionário Diário",
    description: "Um ano de meditações diárias com passagens e orações.",
    image: "https://picsum.photos/seed/devoc6/400/300",
    url: "https://www.amazon.com.br/dp/6556890456?tag=salmododia-20",
    tag: "salmododia-20",
  },
];

/** Log simples de clique (em produção seria enviado a analytics/backend) */
export function logAffiliateClick(productId: string, productTitle: string): void {
  if (typeof window !== "undefined") {
    console.info("[Affiliate] Click:", { productId, productTitle, at: new Date().toISOString() });
    // Futuro: fetch('/api/affiliate-click', { method: 'POST', body: JSON.stringify({ productId, productTitle }) })
  }
}
