/** URLs de imagem placeholder até ter assets reais */
export const PLACEHOLDER_IMAGE = "https://placehold.co/400x300/faf8f5/c9a227?text=Salmo+do+Dia";

export function productImage(slug: string, title: string): string {
  return `https://placehold.co/400x300/faf8f5/c9a227?text=${encodeURIComponent(title.slice(0, 20))}`;
}
