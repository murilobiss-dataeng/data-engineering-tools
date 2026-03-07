/** Formata preço para exibição com exatamente 2 casas decimais (ex.: 386.1 → "386,10"). */
export function formatPriceTwoDecimals(price: string | number | null | undefined): string {
  if (price === null || price === undefined) return "0,00";
  const n = typeof price === "string" ? parseFloat(price) : price;
  if (!Number.isFinite(n)) return "0,00";
  return (Math.round(n * 100) / 100).toFixed(2).replace(".", ",");
}
